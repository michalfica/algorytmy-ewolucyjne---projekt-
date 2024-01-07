import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

class Splash:
    """
    R             - promień plamy 
    """
    R = 5 
    MAX_RANK  = 10 

    RED_COL = np.array([255, 0, 0], dtype=np.int64)
    GREEN_COL = np.array([0, 255, 0], dtype=np.int64)
    BLUE_COL = np.array([0, 0, 25], dtype=np.int64)

    def __init__(self, color, rank):
        self.color = color
        self.rank  = rank 

    def random_splash(self, max_rank):
        self.color = np.array([np.random.randint(0,255) for i in range(3)], dtype=np.int64)
        self.rank = np.random.randint(0, max_rank)
    
    def red_splash(self, max_rank= MAX_RANK):
        self.color = Splash.RED_COL
        self.rank = max_rank

    def __str__(self):
        return f'<{self.color[0]}, {self.color[1]}, {self.color[2]}>'

    def __repr__(self):
        return f'[{self.color[0]}, {self.color[1]}, {self.color[2]}]'
    
class Individual:
    """
    LENGTH, WIDTH - parametry obrazka
    N             - liczba plam  
    """
    LENGTH, WIDTH = 200, 200   
    N             = 100

    """
    splash_parameters - tablica z parametrami kolejnych plam (kolorem rangą)
    splash_layout     - tablica z rozmieszczeniem kolejnych plam (para współrzędnych)
    """
    def __init__(self, splash_parameters, splash_layout):
        self.splash_parameters = splash_parameters
        self.splash_layout = splash_layout

    """
    zwraca tablice z wartością koloru w kazdym pixelu obrazka 
    """
    def convert_to_pixels_array(self):

        def outside_of_frame(pixel):
            return ((pixel[0] < 0 or Individual.LENGTH <= pixel[0]) or
                    (pixel[1] < 0 or Individual.WIDTH <= pixel[1]))
         
        def outside_of_splash(pixel, x, y):
            return (pixel[0]-x)**2 + (pixel[1]-y)**2 > Splash.R**2
        
        pixels_array = np.zeros((Individual.WIDTH, Individual.LENGTH, 3), dtype=np.int64)
        pixels_array_ranks = np.zeros((Individual.WIDTH, Individual.LENGTH, 1))

        splash_index = 0 
        for x,y in self.splash_layout:
            splash = self.splash_parameters[splash_index]
            splash_index += 1

            for t in range(-Splash.R,Splash.R+1):
                for s in range(-Splash.R,Splash.R+1):

                    pixel = (int(x+t), int(y+s))
                    if outside_of_frame(pixel) or outside_of_splash(pixel, x, y):
                        continue

                    if pixels_array_ranks[pixel[0]][pixel[1]] < splash.rank:
                        pixels_array[pixel[0]][pixel[1]] = splash.color
                        pixels_array_ranks[pixel[0]][pixel[1]] = splash.rank
        
        return pixels_array
    
    """
    wyświetla obrazek zakodowany w danym osobnuiku za pomocą plt.imshow()
    """
    def show_image(self):
        plt.imshow(self.convert_to_pixels_array())