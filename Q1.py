import sys
import networkx as nx
import itertools
from itertools import combinations
from collections import defaultdict
from networkx.algorithms.graph_hashing import weisfeiler_lehman_graph_hash

#returns all connected graphs with n vertices.
def connectedGraphs(n) : 
    nodes = list(range(n));
    allEdges = list(combinations(nodes, 2));
    graphs = [];

    uniquesGraphs = []
    for i in range(1, 2 ** len(allEdges)):
        edges = [allEdges[j] for j in range(len(allEdges)) 
        if (i >> j) & 1]
        #if len(edges) < (n -1) :  continue; """ cannot be connected graphs """
        graph = nx.Graph();
        graph.add_nodes_from(nodes);
        graph.add_edges_from(edges);

        if nx.is_connected(graph) : 
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

        
def main() :
    arg = int(sys.argv[1]);
    a = connectedGraphs(arg);
    e = getIsometricEquivalanceClasses(a);
    directedGraphs =[]
    for x in e:
        """ print ("original graph",x.edges); """
        directedGraphs.extend( generate_all_directed_versions(x[0]));
    isometric = getIsometricEquivalanceClasses(directedGraphs);
    
    print("n=", arg)
    print("count=", len(isometric));
    for idx, gr in enumerate(isometric):
        print("#", idx + 1);
        for u, v in gr[0].edges:
            print(u, v);

        
if __name__=="__main__":
    main()
