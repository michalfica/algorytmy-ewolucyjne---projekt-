import matplotlib.pyplot as plt
from skimage import io

import individual 
from imp import reload 
reload(individual)

from individual import Individual
from individual import Splash
import numpy as np

class Utils:


    #  TE RZECZY POWINNY WYLĄDOWAĆ JEDNAK W  klasie PROBLEM !! 
    def each_pixel_of_picture(picture_name):
        image = io.imread(picture_name)
        each_pixel = image.ravel()
        return each_pixel

    def __init__(self, picture_name):
        self.objective_picture = Utils.each_pixel_of_picture(picture_name)  
    
    def objective_function(self, individual):
        result = 0 
        # przechodze po kazdym pixelu obrazka 
        # sprawdzam jaki kolor ma tam individual a jaki ma tam docelowy obrazek i dodaje 
        return result 
