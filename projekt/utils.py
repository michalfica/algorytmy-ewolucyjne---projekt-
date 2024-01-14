from skimage import io
import numpy as np 
import copy 

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

    def __init__(self, picture_name, mutation_probability=0.05):
        self.objective_picture = io.imread(picture_name)
        l, w, t = self.objective_picture.shape
        self.length, self.width = l, w 
        self.mutation_probability = mutation_probability
    """
    compute RBG distance 
    """
    def objective_function(self, individual):
        result = 0 
        for i in range(self.length):
            for j in range(self.width):
                for c in range(3):
                    result += abs(self.objective_picture[i][j][c] - individual.pixels_array[i][j][c])
        return result 
    
    def create_initial_population(self, n):
        population = Population()
        population.population_size = n
        for _ in range(population.population_size):
            individual = Individual()
            individual.generate_random_inidividual()
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

    def create_children_population(self, P, parent_indexes):
        children = Population()
        children.population_size = parent_indexes.size

        assert parent_indexes.size%2==0, 'liczba rodziców musi byc parzysta !'

        for i in range(0, parent_indexes.size-1, 2):
            parent1, parent2 = P.population[i], P.population[i+1]
            child1, child2 = self.crossover(parent1, parent2)
            children.extend([child1, child2])
        
        for i in range(children.population_size):
            if np.random.random() < self.mutation_probability:
                self.mutate(children.population[i])
        
        """
        wylicz tablice pikseli oraz wartość funkcji celu każdego osbonika z populacji dzieci 
        """
        for i in range(children.population_size):
            children.population[i].pixels_array = children.population[i].convert_to_pixels_array()
            children.population[i].objective_value = self.objective_function(children.population[i])
        return children 

    """
    pierwsza połowa plamek od rodzca trafia do drugiego dzieca , a reszta plamek do drugiego dziecka 
    zwraca 2 osobników z ustalonymi 'splash_parameters' ALE BEZ 'pixels_array' 
    """
    def crossover(self, indiv1, indiv2):
        num_of_splashes = Individual.N

        assert num_of_splashes%2==0, 'liczba plam powinna byc parzysta !'

        splashes1, splashes2 = list(), list()
        for i in range(int(num_of_splashes/2)):
            splash2, splash1 = indiv2.splash_parameters[i], indiv1.splash_parameters[i]
            copy_of_splash2, copy_of_splash1 = copy.deepcopy(splash2), copy.deepcopy(splash1)  
            splashes1.append(copy_of_splash2)
            splashes2.append(copy_of_splash1)
    
        for i in range(int(num_of_splashes/2), num_of_splashes):
            splashes1.append(copy.deepcopy(indiv1.splash_parameters[i]))
            splashes2.append(copy.deepcopy(indiv2.splash_parameters[i]))
        
        child1, child2 = Individual(splashes1), Individual(splashes2)
        return child1, child2

    """
    zmienia kolor, promień oraz położenie dwóm losowym plamkom 
    """
    def mutate(self, child):
        num_of_splashes = len(child.splash_parameters)
        i, j = np.random.randint(num_of_splashes), np.random.randint(num_of_splashes)

        child.splash_parameters[i].random_splash(Splash.MAX_RANK, Individual.LENGTH, Individual.WIDTH)
        child.splash_parameters[j].random_splash(Splash.MAX_RANK, Individual.LENGTH, Individual.WIDTH)
         
