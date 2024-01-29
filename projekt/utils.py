from skimage import io
import numpy as np 
import copy 
from functools import cmp_to_key
from operator import itemgetter

import cv2
import colour

import splash
from imp import reload 
reload(splash)

import individual 
from imp import reload 
reload(individual)

import population 
from imp import reload 
reload(population)

from splash import Splash
from individual import Individual
from population import Population

class Utils:

    def __init__(self, picture_name, mutation_probability=0.1):
        self.objective_picture = io.imread(picture_name)
        l, w, t = self.objective_picture.shape
        self.length, self.width = l, w 
        self.mutation_probability = mutation_probability
    """
    compute RBG distance 
    """
    def objective_function_RGB(self, individual):
        result = 0 
        for i in range(self.length):
            for j in range(self.width):
                for c in range(3):
                    pixel_docelowy = int(self.objective_picture[i][j][c])
                    pixel_aktualny = int(individual.pixels_array[i][j][c])
                    difference = int(abs( pixel_aktualny - pixel_docelowy ))  
                    result += difference*difference
        return result 
    
    """
    compute delta_E distance 
    """
    def objective_function(self, indiv):
        # objective_image_lab = cv2.cvtColor(self.objective_picture, cv2.COLOR_RGB2Lab)
        # current_image_lab = cv2.cvtColor(np.float32(indiv.pixels_array), cv2.COLOR_RGB2Lab)
        # return np.mean(colour.difference.delta_e.delta_E_CIE2000(objective_image_lab, current_image_lab))

        return np.mean(colour.difference.delta_e.delta_E_CIE2000(np.array(self.objective_picture), np.array(indiv.pixels_array)))

    
    def create_initial_population(self, n):
        population = Population()
        population.population_size = n
        for _ in range(population.population_size):
            individual = Individual()
            individual.generate_random_inidividual(self.objective_picture)
            population.append(individual)
        return population

    def evaluate_population(self, P):
        for i in range(P.population_size):
            P.population[i].objective_value = self.objective_function(P.population[i])

    """
    zwraca indeksy osobników wylosowanych na rodziców metodą ruletki 
    """
    def parents_selection(self, P, number_of_parents):
        objective_values = np.array([x.objective_value for x in P.population])
        fitness_values = objective_values.max() - objective_values
        if fitness_values.sum() > 0:
            fitness_values = fitness_values / fitness_values.sum()
        else:
            fitness_values = np.ones(P.population_size) / P.population_size
        parent_index = np.random.choice(P.population_size, number_of_parents, True, fitness_values).astype(np.int64)
        return parent_index

    """
    zwraca populację dzieci, każdy osobnik już zewaluowany 
    """
    def create_children_population(self, P, parent_indexes, splahes_to_evolve=None):
        children = Population()
        amount_of_gentle_mutation = int(3*P.population_size/4)
        children.population_size = parent_indexes.size

        assert parent_indexes.size%2==0, 'liczba rodziców musi byc parzysta !'
        # ----------------------------------------------------------------------------------
        # tworzenie dzieci za pomocą krzyżowania  

        for i in range(0, parent_indexes.size-1, 2):
            parent1, parent2 = P.population[i], P.population[i+1]
            child1, child2 = self.crossover(parent1, parent2)
            children.extend([child1, child2])
        
        # for i in range(children.population_size):
        #     if np.random.random() < self.mutation_probability:
        #         self.mutate_completely_random(children.population[i])
        # ----------------------------------------------------------------------------------
        # tworzenie dzieci z 'prawie napewno' najlepszego osobnika za pomocą mutacji mutate_slightly 
                
        children.population_size += amount_of_gentle_mutation
        parent_index = self.parents_selection(P, 1)[0]
        children.extend(self.mutate_slightly(copy.deepcopy(P.population[parent_index]), amount_of_gentle_mutation, splahes_to_evolve=splahes_to_evolve))
        # ----------------------------------------------------------------------------------

        """
        wylicz tablice pikseli oraz wartość funkcji celu każdego osbonika z populacji dzieci 
        """
        for i in range(children.population_size):
            children.population[i].pixels_array = children.population[i].convert_to_pixels_array()
        self.evaluate_population(children)

        return children 

    """
    pierwsza połowa plamek od rodzca trafia do drugiego dzieca , a reszta plamek do drugiego dziecka 
    zwraca 2 osobników z ustalonymi 'splash_parameters' ALE BEZ 'pixels_array' 
    """
    def crossover(self, indiv1, indiv2):
        num_of_splashes = indiv1.N

        assert num_of_splashes%2==0, 'liczba plam powinna byc parzysta !'

        splashes_1_x_sorted = [(indiv1.splash_parameters[i].x,i) for i in range(num_of_splashes)]
        splashes_1_x_sorted = sorted(splashes_1_x_sorted, key=cmp_to_key(lambda item1, item2: item1[0] - item2[0]))

        splashes_2_x_sorted = [(indiv2.splash_parameters[i].x,i) for i in range(num_of_splashes)]
        splashes_2_x_sorted = sorted(splashes_2_x_sorted, key=cmp_to_key(lambda item1, item2: item1[0] - item2[0]))

        splashes1, splashes2 = list(), list()
        for i in range(int(num_of_splashes/2)):
            splash2, splash1 = indiv2.splash_parameters[splashes_2_x_sorted[i][1]], indiv1.splash_parameters[splashes_1_x_sorted[i][1]]
            splashes1.append(copy.deepcopy(splash2))
            splashes2.append(copy.deepcopy(splash1))
    
        for i in range(int(num_of_splashes/2), num_of_splashes):
            splashes1.append(copy.deepcopy(indiv1.splash_parameters[splashes_1_x_sorted[i][1]]))
            splashes2.append(copy.deepcopy(indiv2.splash_parameters[splashes_2_x_sorted[i][1]]))
        
        child1, child2 = Individual(splashes1), Individual(splashes2)
        return child1, child2

    """
    zmienia kolor, promień oraz położenie dwóm losowym plamkom 
    """
    def mutate_completely_random(self, child):
        num_of_splashes = len(child.splash_parameters)
        i, j = np.random.randint(num_of_splashes), np.random.randint(num_of_splashes)

        child.splash_parameters[i].random_splash(Splash.INITIAL_MAX_RANK, Individual.LENGTH, Individual.WIDTH)
        child.splash_parameters[j].random_splash(Splash.INITIAL_MAX_RANK, Individual.LENGTH, Individual.WIDTH)
    
    """
    mutuje 'delikatnie' danego osobnika k razy, szansa na zmiane koloru: 
    zwraca liste nowych osobnikw 
    """
    def mutate_slightly(self, parent, k=1, default_parametr=-1, splahes_to_evolve=None):
        children = Population()
        for _ in range(k):
            child = copy.deepcopy(parent)
        
            num_of_splashes = len(child.splash_parameters)
            if splahes_to_evolve is None: 
                i = np.random.randint(num_of_splashes)
            else: 
                i = np.random.randint(num_of_splashes-splahes_to_evolve, num_of_splashes) # losuj do zmiany tylko ostanie splahes_to_evolve plam

            parametr = np.random.choice(Splash.number_of_parameters, 1, True, np.array([1/3, 1/10, 3/10, 4/15])).astype(np.int64)[0]
                                                                                                                            # [1/3, 2/9, 2/9, 2/9]
            if default_parametr==Splash.COLOR:
                parametr = Splash.COLOR

            child.splash_parameters[i].change_slightly(parametr)
            children.append(child)
    
        return children
    
    """
    dodaje 2 plamki do kazdego osobnika w populacji     
    """
    def add_splash_to_population(self, P, number_of_new_splashes=2):
        for individual in P.population:
            for _ in range(number_of_new_splashes):
                individual.add_splash(self.objective_picture)

        self.evaluate_population(P)

    """
    zwraca populacje skladajaca sie z najlepszych osobnikow z pośród sumy zbiorów 'P' oraz 'children'
    """
    def replace(self, P, children): 
        intitial_population_size = P.population_size
        children_population_size = children.population_size

        P.extend(children)
        objective_values = [(P.population[i].objective_value, i) for i in range(len(P.population))]
        objective_values = sorted(objective_values, key=cmp_to_key(lambda item1, item2: item1[0] - item2[0]))

        assert len(objective_values)==intitial_population_size+children_population_size, 'zgubiłem kogos lub dodalem za duzo'
        
        indexes_of_best_individuals = [objective_values[i][1] for i in range(P.population_size)]
        new_population = Population(P.population_size)
        for idx in indexes_of_best_individuals:
            new_population.append(P.population[idx])
        
        assert len(new_population.population)==intitial_population_size, 'przy zastepowaniu dodałem złą liczbe osobnikow do nowej populacji !'
        
        return new_population