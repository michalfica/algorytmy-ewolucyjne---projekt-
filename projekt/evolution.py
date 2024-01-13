import utils
from imp import reload 
reload(utils)

import population
from imp import reload 
reload(population)

from utils import Utils 
from population import Population 

class Evolution:

    def __init__(self, problem=None, num_of_generations=10, population_size=1, tournament_prob=0.9, 
                 cross_over_param=2, mutation_param=5):
        self.utils = Utils('monalisa.jpg')
        self.population = None
        self.num_of_generations = num_of_generations
        self.best_of_generations = []
        self.population_size = population_size

    def evolve(self):
        self.population = self.utils.create_initial_population(self.population_size)
        self.utils.evaluate_population(self.population)

        return self.population
    
        # self.population = self.utils.create_initial_population()
        # self.utils.fast_nondominated_sort(self.population)
        # for front in self.population.fronts:
        #     self.utils.calculate_crowding_distance(front)
        # children = self.utils.create_children(self.population)
        # returned_population = None
        # for i in tqdm(range(self.num_of_generations)):
        #     self.population.extend(children)
        #     self.utils.fast_nondominated_sort(self.population)
        #     new_population = Population()
        #     front_num = 0
        #     while len(new_population) + len(self.population.fronts[front_num]) <= self.num_of_individuals:
        #         self.utils.calculate_crowding_distance(self.population.fronts[front_num])
        #         new_population.extend(self.population.fronts[front_num])
        #         front_num += 1
        #     self.utils.calculate_crowding_distance(self.population.fronts[front_num])
        #     self.population.fronts[front_num].sort(key=lambda individual: individual.crowding_distance, reverse=True)
        #     new_population.extend(self.population.fronts[front_num][0:self.num_of_individuals - len(new_population)])
        #     returned_population = self.population
        #     self.population = new_population
        #     self.utils.fast_nondominated_sort(self.population)
        #     for front in self.population.fronts:
        #         self.utils.calculate_crowding_distance(front)
        #     children = self.utils.create_children(self.population)
        # return returned_population.fronts[0]