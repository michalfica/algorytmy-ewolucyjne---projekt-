import cv2
import numpy as np
import json
from imp import reload 

import utils
reload(utils)

import splash
reload(splash)

import individual 
reload(individual)

import population 
reload(population)

from splash import Splash
from individual import Individual
from population import Population
from utils import Utils 

class Evolution:

    def __init__(self, problem=None, num_of_generations=20000, population_size=25, tournament_prob=0.9, 
                 cross_over_param=2, mutation_param=5):
        self.utils = Utils('pics/GirlwithaPearl.jpg')
        self.population = None
        self.num_of_generations = num_of_generations
        self.best_of_generations = []
        self.population_size = population_size
        self.no_difference_counter = 0
        self.previous_best_score = None

    def evolve(self):
        # -------------------------------------------------------------------------
        some_statistics = []
        cnt = 0 
        print('startuje ewolucje !')
        # -------------------------------------------------------------------------
        
        self.population = self.utils.create_initial_population(self.population_size)
        self.utils.evaluate_population(self.population)

        number_of_parents = int(self.population.population_size/4)
        number_of_parents += number_of_parents%2
        for t in range(self.num_of_generations):
            # -------------------------------------------------------------------------    
            some_statistics.append(min([x.objective_value for x in self.population.population]))
            # -------------------------------------------------------------------------

            if self.previous_best_score is None:
                self.previous_best_score = some_statistics[cnt]
            elif some_statistics[cnt] < self.previous_best_score:
                self.previous_best_score = some_statistics[cnt]
            else:
                self.no_difference_counter += 1

            if self.no_difference_counter == 10:
                print('juz od ', self.no_difference_counter, 'nic sie nie zmienia !')
                self.utils.add_splash_to_population(self.population)
                self.no_difference_counter = 0

            parent_index = self.utils.parents_selection(self.population, number_of_parents)
            children_population = self.utils.create_children_population(self.population, parent_index)
            self.population = self.utils.replace(self.population, children_population)

            # -------------------------------------------------------------------------

            if cnt%10 == 0:
                print('genracja nr: ', cnt, ', bestobj value: ', some_statistics[cnt])
                image_name = "LOG/" + str(t) + ".png"
                img = self.population.population[0].pixels_array
                BRG_img = np.flip(img, axis=-1) 
                cv2.imwrite(image_name, BRG_img)

            cnt += 1 
            # -------------------------------------------------------------------------

        best_individual = self.population.population[0]
        return best_individual, some_statistics
    
    def save_population(self, path):
        """ Save population to json file """
        out = [indiv.splash_parameters.tolist() for indiv in self.population.population]
        with open(path, "w") as f:
            json.dump(out, f)
            
    # def load(self, path):
    #     """ Load population from json file """
    #     with open(path) as f:
    #         inp = json.load(f)

    #     self.population = [Organism(np.array(x)) for x in inp]
    #     for o in self.population:
    #         self.calc_fitness(o)