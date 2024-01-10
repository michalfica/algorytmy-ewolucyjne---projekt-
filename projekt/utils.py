from skimage import io

import individual 
from imp import reload 
reload(individual)

from individual import Individual
from individual import Splash
import numpy as np

class Utils:

    def __init__(self, picture_name):
        self.objective_picture = io.imread(picture_name)
        l, w, t = self.objective_picture.shape
        self.length, self.width = l, w 


    def objective_function(self, individual):
        result = 0 
        # przechodze po kazdym pixelu obrazka 
        # sprawdzam jaki kolor ma tam individual a jaki ma tam docelowy obrazek i dodaje 
        return result 
