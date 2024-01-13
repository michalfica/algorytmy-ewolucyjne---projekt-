from skimage import io
import numpy as np 

import individual 
from imp import reload 
reload(individual)

import population 
from imp import reload 
reload(population)

from individual import Individual
from population import Population

class Utils:

    def __init__(self, picture_name):
        self.objective_picture = io.imread(picture_name)
        l, w, t = self.objective_picture.shape
        self.length, self.width = l, w 


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