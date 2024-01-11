class Evolution:

    def __init__(self, problem, num_of_generations=10, population_size=100, tournament_prob=0.9, 
                 cross_over_param=2, mutation_param=5):
        self.population = None
        self.num_of_generations = num_of_generations
        self.best_of_generations = []
        self.population_size = population_size

    def evolve(self):
        return 0