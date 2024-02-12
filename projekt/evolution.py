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

from utils import Utils 

class Evolution:

    def __init__(self, num_of_generations=20000, population_size=25):
        self.utils = Utils('pics/GirlwithaPearl.jpg')
        self.population = None
        self.num_of_generations = num_of_generations
        self.population_size = population_size

        self.portion_size = 6 
        self.minimal_iteration_with_portion = 50 
        self.time_to_add_new_portion = 20                                          # liczba iteracji bez zmian, po której dodaję nową porcje plam do populacji 
        self.number_of_iteration_with_current_portion = 0 

    def evolve(self):
        # -------------------------------------------------------------------------
        some_statistics = []
        cnt = 0 
        print('startuje ewolucje !')
        # -------------------------------------------------------------------------
        
        self.population = self.utils.create_initial_population(self.population_size)
        self.utils.evaluate_population(self.population)

        number_of_parents = int(self.population.population_size/2)
        number_of_parents += number_of_parents%2

        assert self.minimal_iteration_with_portion > self.time_to_add_new_portion, 'za wczesnie chce dodawać nowe porcje!'

        for t in range(self.num_of_generations):
            # -------------------------------------------------------------------------    
            some_statistics.append(min([x.objective_value for x in self.population.population]))
            # -------------------------------------------------------------------------

            """
            dodawanie porcji nowych plam 
            """
            if self.number_of_iteration_with_current_portion >= self.minimal_iteration_with_portion \
                and (some_statistics[cnt] == some_statistics[cnt - self.time_to_add_new_portion] \
                     or self.number_of_iteration_with_current_portion >= 155) :
                self.utils.add_splash_to_population(self.population, self.portion_size)
                self.number_of_iteration_with_current_portion = 0

            parent_index = self.utils.parents_selection(self.population, number_of_parents)
            children_population = self.utils.create_children_population(self.population, parent_index, splahes_to_evolve=self.portion_size)
            self.population = self.utils.replace(self.population, children_population)

            # -------------------------------------------------------------------------
            if cnt%10 == 0:
                print('genracja nr: ', cnt, ', bestobj value: ', some_statistics[cnt])
                image_name = "LOG/" + str(t) + ".png"
                img = self.population.population[0].pixels_array
                BRG_img = np.flip(img, axis=-1) 
                cv2.imwrite(image_name, BRG_img)

            cnt += 1 
            self.number_of_iteration_with_current_portion += 1 
            # -------------------------------------------------------------------------

        best_individual = self.population.population[0]
        return best_individual, some_statistics
    
    def save_population(self, path):
        """ Save population to json file """
        out = [indiv.splash_parameters.tolist() for indiv in self.population.population]
        with open(path, "w") as f:
            json.dump(out, f)