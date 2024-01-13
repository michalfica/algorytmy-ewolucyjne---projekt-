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
        self.population = self.utils.create_initial_population(self.population_size)
        self.utils.evaluate_population(self.population)

        number_of_parents = int(self.population.population_size/2)
        for _ in range(self.num_of_generations):
            parent_index = self.utils.parents_selection(self.population, number_of_parents)
            # return parent_index


        return self.population