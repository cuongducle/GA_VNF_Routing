class Graph:
    def __init__(self, graph_struct={}):
        self.graph = graph_struct
        self.start = ''
        self.end = ''

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
        return list(self.graph.keys())

    def getAdjacent(self, vertex):
        if vertex in self.graph.keys():
            return self.graph[vertex]

    def getPathCost(self, path):
        pathCost = 0
        path = self.start + path + self.end
        for vrt, adj in zip(path, path[1:]):
            pathCost += self.graph[vrt][adj]
        return pathCost


if __name__ == '__main__':
    graph = Graph()
    graph.setAdjacent('a', 'b', 4)
    graph.setAdjacent('a', 'c', 4)
    graph.setAdjacent('a', 'd', 7)
    graph.setAdjacent('a', 'e', 3)
    graph.setAdjacent('b', 'c', 2)
    graph.setAdjacent('b', 'd', 3)
    graph.setAdjacent('b', 'e', 5)
    graph.setAdjacent('c', 'd', 2)
    graph.setAdjacent('c', 'e', 3)
    graph.setAdjacent('d', 'e', 6)

    print(graph.getVertices(), '\n')
    #print (graph)

    path = 'abcde'
    print(graph.getPathCost(path))
