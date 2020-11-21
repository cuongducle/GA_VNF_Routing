class Graph:
    def __init__(self, graph_init):
        self.graph = graph_init
        self.start = ''
        self.end = ''
        self.vertex_add = {}
        self.sfc = []
    def __str__(self):
        grh = ''
        for vrt in self.getVertices():
            for adj in self.getAdjacent(vrt):
                grh += '({0}, {1}, {2})\t'.format(vrt,
                                                  adj, self.graph[vrt][adj])
        return grh

    def setStartEnd(self,start,end):
        self.start = start
        self.end = end

    def addVertex(self,vertex, adj, weight=0):
        if vertex not in self.vertex_add.keys():
            self.vertex_add[vertex] = {}
        # if adj not in self.graph.keys():
        #     self.vertex_add[adj] = {}
        self.vertex_add[vertex][adj] = weight

    def setVertex(self, vertex):
        if vertex not in self.graph.keys():
            self.graph[vertex] = {}
        return self

    def setAdjacent(self, vertex, adj, weight=0):
        if vertex not in self.graph.keys():
            self.graph[vertex] = {}
        if adj not in self.graph.keys():
            self.graph[adj] = {}

        self.graph[vertex][adj] = weight
        return self

    def getDistance(self,node1,nodes):
        return self.graph[node1][nodes]

    def getVertices(self):
        # list_nodes = list(self.graph.keys())
        # list_nodes.remove(self.start)
        # list_nodes.remove(self.end)
        return list(self.graph.keys())

    def getAdjacent(self, vertex):
        if vertex in self.graph.keys():
            return self.graph[vertex]

    def getPathCost(self, path):
        pathCost = 0
        for vrt, adj in zip(path, path[1:]):
            try:
                pathCost += self.graph[vrt][adj]
            except:
                import sys
                pathCost =  sys.maxsize
                return pathCost

    # def getPathCost(self, path):
    #     pathCost = 0
    #     path = self.start + path + self.end
    #     for vrt, adj in zip(path, path[1:]):
    #         try:
    #             pathCost += self.graph[vrt][adj]
    #         except:
    #             import sys
    #             pathCost =  sys.maxsize
    #             return pathCost
        # try:
        #     pathCost += self.vertex_add[self.start][path[0]]
        # except:
        #     pass

        # try:
        #     pathCost += self.vertex_add[path[-1]][self.end]
        # except:
        #     pass

        return pathCost


# if __name__ == '__main__':
#     graph = Graph()
#     graph.setAdjacent('a', 'b', 4)
#     graph.setAdjacent('a', 'c', 4)
#     graph.setAdjacent('a', 'd', 7)
#     graph.setAdjacent('a', 'e', 3)
#     graph.setAdjacent('b', 'c', 2)
#     graph.setAdjacent('b', 'd', 3)
#     graph.setAdjacent('b', 'e', 5)
#     graph.setAdjacent('c', 'd', 2)
#     graph.setAdjacent('c', 'e', 3)
#     graph.setAdjacent('d', 'e', 6)

#     print(graph.getVertices(), '\n')
#     #print (graph)

#     path = 'edcba'
#     print(graph.getPathCost(path))
