import sys
import networkx as nx
import itertools
from itertools import combinations
from collections import defaultdict
from networkx.algorithms.graph_hashing import weisfeiler_lehman_graph_hash

def allGraphs(n, e) : 
    nodes = list(range(n));
    allEdges = list(combinations(nodes, 2));
    graphs = [];

    uniquesGraphs = []
    for i in range(1, 2 ** len(allEdges)):
        edges = [allEdges[j] for j in range(len(allEdges)) 
        if (i >> j) & 1]
        #if len(edges) < (n -1) :  continue; """ cannot be connected graphs """
        if not ( len(edges) == e ): continue;
        graph = nx.Graph();
        graph.add_nodes_from(nodes);
        graph.add_edges_from(edges);
        graphs.append(graph);

    return graphs;


#Given a graph, n, returns all sub-graphs of size n.
def subGraphs(graph, n) : 
    nodes = graph.nodes;
    allEdges = graph.edges;
    edgeNo =defaultdict();
    for idx, e in enumerate(allEdges):
        edgeNo[idx] = e;
    graphs = [];

    for i in range(1, 2 ** len(edgeNo)):
        edges = [edgeNo[j] for j in range(len(edgeNo)) 
        if (i >> j) & 1]
        #if len(edges) < (n -1) :  continue; """ cannot be connected graphs """
        if (len(edges) != n): continue;
        graph = nx.DiGraph();
        graph.add_nodes_from(nodes);
        graph.add_edges_from(edges);
        graphs.append(graph);

    return graphs;

#given a set of graphs returns a list of (lists, which are isomorphic
# to each other). This method uses weisfeiler lehman graph hash, which
# is different if the 2 graphs are not isomorphic. And there are strong
# gurantees that the hash will be the same incase he graphs are 
#isomorphic.
def getIsomorphicEquivalanceClasses(graphs): 


    hash_buckets = defaultdict(list)
    
    for G in graphs:
        h = weisfeiler_lehman_graph_hash(G)
        hash_buckets[h].append(G)

    isomorphic_groups = []
    still_ungrouped = []
    for bucket in hash_buckets.values():
        ungrouped = list(bucket)
        while ungrouped:
            base = ungrouped.pop(0)
            group = [base]
            
            for other in ungrouped:
                if nx.is_isomorphic(base, other):
                    group.append(other)
                else:
                    still_ungrouped.append(other)
            isomorphic_groups.append(group)
            ungrouped = still_ungrouped
 
    return isomorphic_groups

def generate_all_directed_versions(G_undirected):
    edges = list(G_undirected.edges())
    directed_graphs = []

    # Each edge has 3 choices: (a->b), (b->a), or both
    choices = []
    for u, v in edges:
        choices.append([
            [(u, v)],
            [(v, u)],
            [(u, v), (v, u)]
        ])

    # Cartesian product of all edge choices
    for combination in itertools.product(*choices):
        DG = nx.DiGraph()
        DG.add_nodes_from(G_undirected.nodes())
        for edge_group in combination:
            DG.add_edges_from(edge_group)
        directed_graphs.append(DG)

    return directed_graphs



def parse_graph_file(filename):
    G = nx.DiGraph();

    with open(filename, 'r') as f:
        lines = f.readlines()
    
    n = int(lines[0].strip())
    yield n;
    #G.add_nodes_from(range(n))  # Nodes: 0 to n-1
    high = 0;
    for line in lines[1:]:
        if line.strip():  # Skip empty lines
            u, v = map(int, line.strip().split())
            G.add_edge(u, v);
            high = max (u, v, high);
    G.add_nodes_from(range (high));
    yield G

        
def main() :
    arg = sys.argv[1];
    """ arg = 'test'; """
    n, g = parse_graph_file(arg);
    """ print(g.edges); """
    """ edgeNo = defaultdict();
    for idx, e in enumerate(g.edges):
        edgeNo[idx] = e;
     """#print(len(edgeNo));
    sGraphs = subGraphs(g, n);
    
    isomorphic = getIsomorphicEquivalanceClasses(sGraphs);
    print("n=", n)
    print("count=", len(isomorphic));
    k = 0;
    for idx, gr in enumerate(isomorphic):
        print("#", idx + 1, "count=", len(gr));
        k = idx;
        for u, v in gr[0].edges:
            print(u, v);

    graphs = allGraphs(len(g.nodes), n);
    allDirected = [];
    for x in graphs:
        allDirected.extend(generate_all_directed_versions(x));
    allIsomorphic = getIsomorphicEquivalanceClasses(allDirected);
    k = k + 1;
    for x  in allIsomorphic : 
        c = 1;
        for y in isomorphic:
            if nx.is_isomorphic(x[0], y[0]) : 
                c = 0;

        if (c == 1) : 
            print( "#",k +1, "count = 0");
            k = k + 1;
            for u, v in x[0].edges:
                print(u, v);


"""     allIsomorphic = getIsometricEquivalanceClasses(
        generate_all_directed_versions(graphs));
 """    
if __name__=="__main__":
    main()
