import networkx as nx
import matplotlib.pyplot as plt
import time

def check_child(a,b):
    for i in a:
        # print("i",i)
        if(i not in b):
            return False
    return True

file='/home/hoangntbn/Desktop/20201/ttth/random_1.txt'
f=open(file,'r')

contents=[]
for line in f:
    line=line.rstrip()
    contents.append(line)
f.close()
G = nx.DiGraph()
socanh=int(contents[0].split(" ")[1])
for i in range(socanh):
    canh=contents[i+1].split(" ")
    G.add_edge(str(canh[0]),str(canh[1]),weight=int(canh[2]))
list_node=G.nodes
for i in list_node:
    G.nodes[str(i)]['nfv']=[]
print(G.nodes.data())
# plt.subplot(121)
# nx.draw_shell(G, with_labels=True, font_weight='bold')
# plt.show()
# exit()
print(contents[socanh+1])
node_goc=str(contents[socanh+1].split(" ")[0])
node_dich=str(contents[socanh+1].split(" ")[1])

nfv_list1=[i+1 for i in range(int(contents[socanh+2]))]
print(nfv_list1)
so_nfv=int(contents[socanh+2])
for i in range(so_nfv):
    nfv=contents[socanh+3+i].split(" ")
    for j in nfv:
        if(j in list_node):
            G.nodes[str(j)]['nfv'].append(nfv_list1[i])




# G = nx.DiGraph()
# G.add_edge("v1", "v2", weight=4 )
# G.add_edge("v1", "v3", weight=3 )
# G.add_edge("v2", "v3", weight=6 )
# G.add_edge("v3", "v4", weight=9 )
# G.add_edge("v2", "v4", weight=8 )
# G.add_edge("v3", "v5", weight=7 )
# G.add_edge("v7", "v2", weight=2 )
# G.add_edge("v7", "v4", weight=5 )
# G.add_edge("v4", "v5", weight=3 )
# G.add_edge("v4", "v6", weight=6 )
# G.add_edge("v5", "v6", weight=2 )

# G.nodes["v1"]['nfv'] = []
# G.nodes["v2"]['nfv'] = [1]
# G.nodes["v3"]['nfv'] = [1,3]
# G.nodes["v4"]['nfv'] = [2,3]
# G.nodes["v5"]['nfv'] = [2]
# G.nodes["v6"]['nfv'] = []
# G.nodes["v7"]['nfv'] = []
# node_goc="v1"
# node_dich="v6"
# nfv_list=[1,2]

nfv_list=[4,5,7,8]
t1=time.time()
num=len(nfv_list)+1
G1 = nx.DiGraph()
for node in list(G.nodes):
    for i in range(num):
        G1.add_node(str(node)+"_"+str(i))
# print(G.nodes.data())
# print(G1.nodes.data())

for edge in list(G.edges):
    #print(edge)
    weight=G.edges[edge[0],edge[1]]['weight']
    #exit()
    arr=[]
    # print(edge[1])
    # print(G.nodes[edge[1]]['nfv'])
    # print(edge[1])
    # exit()
    nfv=G.nodes[edge[1]]['nfv']
    # if(type(nfv) is int):
    #     nfv=tuple([G.nodes[edge[1]]['nfv']])
        
    #print(nfv)
    for node in list(G1.nodes):
        if(edge[0] in node):
            arr.append(node)
    for i in range(len(arr)):
        #print(i)
        j_list=[]
        for j in nfv_list:
            if(j>=i):
                lis=[i1 for i1 in range(i+1,j+1)]
                #print("lis",lis)
                #print("nfv",nfv)
                if(check_child(lis,nfv)):
                    j_list.append(j)
        #print(j_list)
        if(len(j_list)==0):
            j1=i
        else:
            j1=max(j_list)
        dinh2=edge[1]+"_"+str(j1)
        G1.add_edge(arr[i],dinh2,weight=weight)
        #print(j1)

node_g=node_goc+"_"+str(0)
node_d=node_dich+"_"+str(num-1)
# node_g=list(G1.nodes)[0]
# node_d=list(G1.nodes)[len(list(G1.nodes))-1]

for node in list(G1.nodes):
    if(node==node_g or node==node_d):
        print("nut goc hoac nut dich")
        continue
    count_ra=0
    count_vao=0
    for edge in list(G1.edges):
        if node==edge[0]:
            count_ra=count_ra+1
        if node==edge[1]:
            count_vao=count_vao+1
        if(count_ra!=0 and count_vao !=0):
            break
    if(count_ra==0 or count_vao ==0):
        G1.remove_node(node)

# print(G1.nodes.data())
# print(G1.edges.data())



length,path=nx.single_source_dijkstra(G1,node_g,node_d)
t2=time.time()
print(length)
print(path)
print(t2-t1)
    
plt.subplot(122)
nx.draw_shell(G1, with_labels=True, font_weight='bold')
plt.subplot(121)
nx.draw_shell(G, with_labels=True, font_weight='bold')
plt.show()


# print(G.nodes.data())
# print(list(G.edges))
# print(G["v1"]["v2"]["weight"])


# length,path=nx.single_source_dijkstra(G,"v1","v5")
# print(length)
# print(path)




# G2 = nx.DiGraph()
# G2.add_edge("v1_0", "v2_2", weight=3 )
# G2.add_edge("v1_0", "v3_0", weight=1 )
# G2.add_edge("v1_0", "v4_1", weight=5 )
# G2.add_edge("v3_0", "v4_1", weight=3 )
# G2.add_edge("v4_1", "v3_2", weight=1 )
# G2.add_edge("v3_2", "v4_2", weight=1 )
# G2.add_edge("v3_2", "v5_2", weight=1 )
# G2.add_edge("v2_2", "v5_2", weight=5 )

# length,path=nx.single_source_dijkstra(G2,"v1_0","v5_2")
# print(length)
# print(path)


# G1=nx.DiGraph()
# G1.add_edge("v1_0", "v2_2", weight=3 )
# G1.add_edge("v1_1", "v2_2", weight=3 )
# G1.add_edge("v1_2", "v2_2", weight=3 )

# G1.add_edge("v1_0", "v4_1", weight=5 )
# G1.add_edge("v1_1", "v4_1", weight=5 )
# G1.add_edge("v1_2", "v4_2", weight=5 )

# G1.add_edge("v1_0", "v3_0", weight=1 )
# G1.add_edge("v1_1", "v3_2", weight=1 )
# G1.add_edge("v1_2", "v3_2", weight=1 )

# G1.add_edge("v4_0", "v3_0", weight=1 )
# G1.add_edge("v4_1", "v3_2", weight=1 )
# G1.add_edge("v4_2", "v3_2", weight=1 )

# G1.add_edge("v3_0", "v4_1", weight=3 )
# G1.add_edge("v3_1", "v4_1", weight=3 )
# G1.add_edge("v3_2", "v4_2", weight=3 )

# G1.add_edge("v3_0", "v5_0", weight=1 )
# G1.add_edge("v3_1", "v5_1", weight=1 )
# G1.add_edge("v3_2", "v5_2", weight=1 )

# G1.add_edge("v2_0", "v5_0", weight=5 )
# G1.add_edge("v2_1", "v5_1", weight=5 )
# G1.add_edge("v2_2", "v5_2", weight=5 )




# plt.subplot(122)
# nx.draw_shell(G, with_labels=True, font_weight='bold')
# plt.show()