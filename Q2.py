import sys
import networkx as nx
import itertools
from itertools import combinations
from collections import defaultdict
from networkx.algorithms.graph_hashing import weisfeiler_lehman_graph_hash

# from networkx.algorithms.isomorphism import DiGraphMatcher
#from networkx.algorithms.isomorphism import GraphMatcher

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
        graph = nx.Graph();
        graph.add_nodes_from(nodes);
        graph.add_edges_from(edges);
        graphs.append(graph);

    return graphs;

def getIsometricEquivalanceClasses(graphs): 

    # Step 1: Hash graphs to reduce comparisons
    hash_buckets = defaultdict(list)
    
    for G in graphs:
        h = weisfeiler_lehman_graph_hash(G)
        hash_buckets[h].append(G)

    # Step 2: Within each bucket, group by exact isomorphism
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
    """ while still_ungrouped:
        base = still_ungrouped.pop
 """

    return isomorphic_groups


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
    n, g = parse_graph_file(arg);
    """ print(g.edges); """
    edgeNo = defaultdict();
    for idx, e in enumerate(g.edges):
        edgeNo[idx] = e;
    #print(len(edgeNo));
    sGraphs = subGraphs(g, n);
    
    isometric = getIsometricEquivalanceClasses(sGraphs);
    print("n=", arg)
    print("count=", len(isometric));
    for idx, gr in enumerate(isometric):
        print("#", idx + 1, "count=", len(gr));
        for u, v in gr[0].edges:
            print(u, v);
        
if __name__=="__main__":
    main()
