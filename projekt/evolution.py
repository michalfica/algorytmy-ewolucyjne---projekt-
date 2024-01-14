import utils
from imp import reload 
reload(utils)

import population
from imp import reload 
reload(population)

from utils import Utils 
from population import Population 

class Evolution:

    def __init__(self, problem=None, num_of_generations=1, population_size=10, tournament_prob=0.9, 
                 cross_over_param=2, mutation_param=5):
        self.utils = Utils('monalisa.jpg')
        self.population = None
        self.num_of_generations = num_of_generations
        self.best_of_generations = []
        self.population_size = population_size

    def evolve(self):
        some_statistics = []

        self.population = self.utils.create_initial_population(self.population_size)
        self.utils.evaluate_population(self.population)

        number_of_parents = int(self.population.population_size/2)
        for _ in range(self.num_of_generations):
            
            some_statistics.append(max([x.objective_value for x in self.population.population]))

            parent_index = self.utils.parents_selection(self.population, number_of_parents)
            children_population = self.utils.create_children_population(self.population, parent_index)

            self.population = self.utils.replace(self.population, children_population)

        best_individual = self.population[0]
        return best_individual, some_statistics