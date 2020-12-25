from Graph_directed import Graph
from GeneticAlgorithmTSP import GeneticAlgorithmTSP
import heapq
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

def map_to_char(num):
    return chr(int(num)+97)
def map_to_int(char):
    return ord(char) - 97
def map_string_to_list(string):
    out = ''
    list_int = []
    for char in string:
        list_int.append(str(map_to_int(char))) 
    return '-'.join(list_int)


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

def replace_extra_path(path):
    out = ''
    path = '.'+ path
    for i in range(1,len(path)):
        if path[i] != path[i-1]:
            out = out + path[i]
    return out

def full_path_small(start,end,dijsktra_path):
    out = end 
    while end != start:
        end = dijsktra_path[start][end]
        out = end  + out
        # print(out)
    return out[:-1]

def full_path(path,dijsktra_path):
    path = replace_extra_path(path)
    fullpath = ''
    for i in range(len(path)-1):
        fullpath = fullpath + full_path_small(path[i],path[i+1],dijsktra_path)
        # if tmp != path[i]:
        #     fullpath = fullpath + path[i] + tmp
        # else:
        #     fullpath = fullpath + path[i]
    return fullpath + path[-1]

def generate_data_txt(n,m,l,f_out,max_weight = 10, max_len_sfc = 4):
    with open(f_out,'w') as f:
    # input_graph = Graph({})
        sfc = []
        f.write(str(n)+' '+str(m)+'\n')
        if (m > n*(n-1)):
            print('Too many vertex')
            return
        c = 1
        list_vertex = []
        while c <= m:
            a = random.randint(1,n)
            b = random.randint(1,n)
            if (a != b) and ((a,b) not in list_vertex):
                list_vertex.append((a,b))
                f.write(str(a)+' '+ str(b)+' '+str(random.randint(1,max_weight))+'\n')
                c = c + 1
        start,end = random.sample(range(1,n), 2)
        f.write(str(start) + ' '+str(end)+'\n')
        f.write(str(l)+'\n')
        # input_graph.setStartEnd(start,finish)
        # sfc.append(start)
        count = 0
        while count < l:
            # sfc.append(
            tmp = random.sample(range(1,n), random.randint(2,max_len_sfc))
            if start not in tmp and end not in tmp:
                sfc.append(tmp)
                count = count + 1
        for i in range(l):
            out = ''
            for item in sfc[i]: 
                out = out + str(item) + ' '
            f.write(out+'\n')
        # sfc.append(end)


def draw_way(graph,path):
    plt.subplot(122)
    H = nx.DiGraph(directed=True,format='weighted_adjacency_matrix')
    for i in range(len(path)-1):
        start = path[i]
        target = path[i+1]
        H.add_edge(start, target, weight=graph.getDistance(start,target))

    options = {
        'node_color': 'red',
        'node_size': 500,
        'width': 3,
        'arrowstyle': '-|>',
        'arrowsize': 12,
    }

    pos_2 = nx.spring_layout(H)
    nodes_2 = {}
    for item in path:
        nodes_2[item] = str(map_to_int(item))
    nx.draw_networkx_edges(H,pos_2, connectionstyle='arc3, rad = 0.3', alpha=0.2)
    nx.draw_networkx_labels(H,pos_2,nodes_2,font_size=16,font_color='r')
    plt.savefig("output/Graph.png", format="PNG")
    plt.show()


def draw_graph(graph):
    plt.subplot(122)
    G = nx.DiGraph(directed=True,format='weighted_adjacency_matrix')
    for key in input_graph.graph.keys():
        value = input_graph.graph[key]
        for key2 in value.keys():
            G.add_edge(key, key2, weight=graph.getDistance(key,key2))
    # Need to create a layout when doing
    options = {
        'node_color': 'red',
        'node_size': 500,
        'width': 3,
        'arrowstyle': '-|>',
        'arrowsize': 12,
        # 'edge_labels':True,
        #  'graph_border':True
    }

    #pos = nx.spring_layout(G)
    #nx.draw_networkx(G, arrows=True, **options)
    pos = nx.spring_layout(G)
    emp = input_graph.getVertices()
    nodes = {}
    for item in emp:
        nodes[item] = str(map_to_int(item))
# Here there is the addition:

    edge_labels = dict([((u,v), round(d['weight'], 3))
             for u,v,d in G.edges(data=True)])

    #nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels,label_pos=0.15, font_size=10)
    nx.draw_networkx_edges(G,pos, connectionstyle='arc3, rad = 0.3', alpha=0.2)
    nx.draw_networkx_labels(G,pos,nodes,font_size=20,font_color='r')
    plt.show()
    plt.savefig("output/input.png", format="PNG")

if __name__ == '__main__':
    # generate_data_txt(25,100,50,'random.txt')
    input_graph = Graph({})
    sfc = []
    with open("random.txt","r") as f:
        n,m = int_data(f.readline().split())
        for _ in range(m):
            a,b,c = f.readline().split()
            input_graph.setAdjacent(map_to_char(a), map_to_char(b), int(c))
        start,finish = f.readline().split()
        start = map_to_char(start)
        finish = map_to_char(finish)
        num_sfc = int(f.readline())
        sfc.append(start)
        for _ in range(num_sfc):
            tmp = f.readline().split()
            tmp_convert = []
            for item in tmp:
                tmp_convert.append(map_to_char(item))
            sfc.append(tmp_convert)
        sfc.append(finish)

    input_graph.setStartEnd(start,finish)

    sfc_item = []
    for sfc_part in sfc:
        for item in sfc_part:
            sfc_item.append(item)

    sfc_item.append(start)
    sfc_item.append(finish)
    sfc_item = set(sfc_item)

# bắt đầu từ đây
    import time 
    time_start = time.time()

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
    ga_tsp = GeneticAlgorithmTSP(generations=100, population_size=100, tournamentSize=2, mutationRate=0.1, elitismRate=0.1)

    optimal_path, path_cost , generation_plot,fitness_plot = ga_tsp.optimize(sfc_graph)
    # print (fitness_plot)
    plt.plot(generation_plot,fitness_plot)
    plt.show()
    plt.savefig("output/convert.png", format="PNG")
    fullpath = full_path(optimal_path,dijsktra_way)
    
    print ('\nPath: {0}, Cost: {1}'.format(map_string_to_list(optimal_path), path_cost))

    print( '---  final path --- :', map_string_to_list(fullpath))
    print('time : ', time.time() - time_start)
    # draw_graph(input_graph)
    draw_way(input_graph,fullpath)
    print(map_to_int(start),' ',map_to_int(finish))
