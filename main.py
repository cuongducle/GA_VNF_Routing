from Graph_directed import Graph
from GeneticAlgorithmTSP import GeneticAlgorithmTSP
import heapq
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def dijsktra(graph, initial):
    visited = {initial: 0}
    path = {}
    nodes = set(graph.getVertices())
    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node
        if min_node is None:
            break
        nodes.remove(min_node)
        current_weight = visited[min_node]
        for edge in graph.getAdjacent(min_node):
            weight = current_weight + graph.getDistance(min_node, edge)
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node
    return visited, path

def int_data(data):
    out = []
    for item in data:
        out.append(int(item))
    return out

def draw_way(graph,path):
    G = nx.DiGraph(directed=True,format='weighted_adjacency_matrix')
    for i in range(len(path)-1):
        start = path[i]
        target = path[i+1]
        G.add_edge(start, target, weight=graph.getDistance(start,target))

    # Need to create a layout when doing
    options = {
        'node_color': 'red',
        'node_size': 500,
        'width': 3,
        'arrowstyle': '-|>',
        'arrowsize': 12,
    }

    pos = nx.spring_layout(G)
    nodes = {}
    for item in path:
        nodes[item] = str(item)
    nx.draw_networkx_edges(G,pos, connectionstyle='arc3, rad = 0.3', alpha=0.2)
    nx.draw_networkx_labels(G,pos,nodes,font_size=16,font_color='r')
    plt.savefig("output/Graph.png", format="PNG")
    plt.show()

def full_path(path,dijsktra_path):
    fullpath = ''
    for i in range(len(path)-1):
        tmp = dijsktra_path[path[i]][path[i+1]]
        if tmp != path[i]:
            fullpath = fullpath + path[i] + tmp
        else:
            fullpath = fullpath + path[i]
    return fullpath + path[-1]

if __name__ == '__main__':

    input_graph = Graph({})
    sfc = []
    with open("input.txt","r") as f:
        n,m = int_data(f.readline().split())
        for _ in range(m):
            a,b,c = f.readline().split()
            input_graph.setAdjacent(a, b, int(c))
        start,finish = f.readline().split()
        num_sfc = int(f.readline())
        sfc.append(start)
        for _ in range(num_sfc):
            sfc.append(f.readline().split())
        sfc.append(finish)

    input_graph.setStartEnd(start,finish)

    sfc_item = []
    for sfc_part in sfc:
        for item in sfc_part:
            sfc_item.append(item)

    sfc_item.append(start)
    sfc_item.append(finish)
    sfc_item = set(sfc_item)

    dijsktra_dic = {}
    dijsktra_way = {}
    for item in sfc_item:
        dijsktra_dic[item] = dijsktra(input_graph,item)[0]
        dijsktra_way[item] = dijsktra(input_graph,item)[1]

    #print(dijsktra_dic)

    sfc_graph = Graph({})
    for i in range(len(sfc)-1):
        for vertex in sfc_item:
            for adj in sfc_item:
                if adj == vertex:
                    sfc_graph.setAdjacent(vertex, adj, 0)
                else:
                    try:
                        sfc_graph.setAdjacent(vertex, adj, dijsktra_dic[vertex][adj])
                        # print(vertex,' ', adj)
                    except:
                        import sys
                        sfc_graph.setAdjacent(vertex, adj, sys.maxsize)
                        # print(vertex,' ', adj)

    sfc_graph.start = start
    sfc_graph.end = finish
    sfc_graph.sfc = sfc
    ga_tsp = GeneticAlgorithmTSP(generations=20, population_size=20, tournamentSize=2, mutationRate=0, elitismRate=0.1)

    optimal_path, path_cost = ga_tsp.optimize(sfc_graph)
    fullpath = full_path(optimal_path,dijsktra_way)
    print ('\nPath: {0}, Cost: {1}'.format(optimal_path, path_cost))

    print( '---  final path --- :', fullpath)
    draw_way(input_graph,fullpath)
