from Graph_directed import Graph
from GeneticAlgorithmTSP import GeneticAlgorithmTSP
import heapq
import numpy as np


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

input_graph = Graph({})
sfc = []
with open("input.txt","r") as f:
    n,m = int_data(f.readline().split())
    for _ in range(m):
        a,b,c = f.readline().split()
        input_graph.setAdjacent(a, b, int(c))
    start,finish = f.readline().split()
    num_sfc = int(f.readline())
    #sfc.append(start)
    for _ in range(num_sfc):
        sfc.append(f.readline().split())
    #sfc.append(finish)

input_graph.setStartEnd(start,finish)

sfc_item = []
for sfc_part in sfc:
    for item in sfc_part:
        sfc_item.append(item)
sfc_item.append(start)
sfc_item.append(finish)
sfc_item = set(sfc_item)

dijsktra_dic = {}
for item in sfc_item:
    dijsktra_dic[item] = dijsktra(input_graph,item)[0]

#print(dijsktra_dic)

sfc_graph = Graph({})
for i in range(len(sfc)-1):
    for vertex in sfc[i]:
        for adj in sfc[i+1]:  
            try:
                sfc_graph.setAdjacent(vertex, adj, dijsktra_dic[vertex][adj])
                # print(vertex,' ', adj)
            except:
                import sys
                sfc_graph.setAdjacent(vertex, adj, sys.maxsize)
                # print(vertex,' ', adj)

for item in sfc[0]:
    #print(start,' ', item, ' ', dijsktra_dic['1']['2'])
    sfc_graph.addVertex(start,item,dijsktra_dic[start][item])
    

for item in sfc[-1]:
    #print(item,' ', finish)
    sfc_graph.addVertex(item,finish,dijsktra_dic[item][finish])

print(sfc_graph.graph)

# ga_tsp = GeneticAlgorithmTSP(generations=20, population_size=100, tournamentSize=2, mutationRate=0.2, elitismRate=0.1)

# optimal_path, path_cost = ga_tsp.optimize(sfc_graph)
# print ('\nPath: {0}, Cost: {1}'.format(optimal_path, path_cost))
