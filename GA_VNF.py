import numpy as np
import operator
import Graph_directed
import math
import Graph


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


class GeneticAlgorithmTSP:
    def __init__(self, generations=100, population_size=10, tournamentSize=4, mutationRate=0.1, elitismRate=0.1):
        self.generations = generations
        self.population_size = population_size
        self.tournamentSize = tournamentSize
        self.mutationRate = mutationRate
        self.elitismRate = elitismRate

    def optimize(self, graph):
        list_nodes = list(graph.getVertices())
        list_nodes.remove(self.start)
        list_nodes.remove(self.end)
        population = self.__makePopulation(list_nodes)
        print(list_nodes)
        elitismOffset = math.ceil(self.population_size*self.elitismRate)

        if (elitismOffset > self.population_size):
            raise ValueError('Elitism Rate must be in [0,1].')

        print('Optimizing TSP Route for Graph:\n{0}'.format(graph))

        for generation in range(self.generations):
            print('\nGeneration: {0}'.format(generation + 1))
            print('Population: {0}'.format(population))

            newPopulation = []
            fitness = self.__computeFitness(graph, population)
            print('Fitness:    {0}'.format(fitness))
            fittest = np.argmin(fitness)

            print('Fittest Route: {0} ({1})'.format(
                population[fittest], fitness[fittest]))

            if elitismOffset:
                elites = np.array(fitness).argsort()[:elitismOffset]
                [newPopulation.append(population[i]) for i in elites]
            for gen in range(elitismOffset, self.population_size):
                parent1 = self.__tournamentSelection(graph, population)
                parent2 = self.__tournamentSelection(graph, population)
                offspring = self.__crossover(parent1, parent2)
                newPopulation.append(offspring)
                # print ('\nParent 1: {0}'.format(parent1))
                # print ('Parent 2: {0}'.format(parent2))
                # print ('Offspring: {0}\n'.format(offspring))
            for gen in range(elitismOffset, self.population_size):
                newPopulation[gen] = self.__mutate(newPopulation[gen])

            population = newPopulation

            if self.__converged(population):
                print('\nConverged to a local minima.', end='')
                break

        return (population[fittest], fitness[fittest])

    def __makePopulation(self, graph_nodes):
        return [''.join(v for v in np.random.permutation(graph_nodes)) for i in range(self.population_size)]

    def __computeFitness(self, graph, population):
        return [graph.getPathCost(path) for path in population]

    def __tournamentSelection(self, graph, population):
        tournament_contestants = np.random.choice(
            population, size=self.tournamentSize)
        # print (tournament_contestants)
        tournament_contestants_fitness = self.__computeFitness(
            graph, tournament_contestants)
        return tournament_contestants[np.argmin(tournament_contestants_fitness)]

    def __crossover(self, parent1, parent2):
        offspring = ['' for allele in range(len(parent1))]
        index_low, index_high = self.__computeLowHighIndexes(parent1)

        offspring[index_low:index_high +
                  1] = list(parent1)[index_low:index_high+1]
        offspring_available_index = list(
            range(0, index_low)) + list(range(index_high+1, len(parent1)))
        for allele in parent2:
            if '' not in offspring:
                break
            if allele not in offspring:
                offspring[offspring_available_index.pop(0)] = allele
        return ''.join(v for v in offspring)

    def __mutate(self, genome):
        if np.random.random() < self.mutationRate:
            index_low, index_high = self.__computeLowHighIndexes(genome)
            return self.__swap(index_low, index_high, genome)
        else:
            return genome

    def __computeLowHighIndexes(self, string):
        index_low = np.random.randint(0, len(string)-1)
        index_high = np.random.randint(index_low+1, len(string))
        while index_high - index_low > math.ceil(len(string)//2):
            try:
                index_low = np.random.randint(0, len(string))
                index_high = np.random.randint(index_low+1, len(string))
            except ValueError:
                pass
        return (index_low, index_high)

    def __swap(self, index_low, index_high, string):
        string = list(string)
        string[index_low], string[index_high] = string[index_high], string[index_low]
        return ''.join(string)

    def __converged(self, population):
        return all(genome == population[0] for genome in population)


if __name__ == '__main__':
    graph = Graph_directed.Graph()
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

    ga_tsp = GeneticAlgorithmTSP(
        generations=20, population_size=100, tournamentSize=2, mutationRate=0.2, elitismRate=0.1)

    optimal_path, path_cost = ga_tsp.optimize(graph)
    print('\nPath: {0}, Cost: {1}'.format(optimal_path, path_cost))
