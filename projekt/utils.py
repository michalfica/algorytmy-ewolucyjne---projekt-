from skimage import io

class Utils:

    def __init__(self, picture_name):
        self.objective_picture = io.imread(picture_name)
        l, w, t = self.objective_picture.shape
        self.length, self.width = l, w 


    def objective_function(self, individual):
        result = 0 
        # przechodze po kazdym pixelu obrazka 
        # sprawdzam jaki kolor ma tam individual a jaki ma tam docelowy obrazek i dodaje rożnice 

        for i in range(self.length):
            for j in range(self.width):
                for c in range(3):
                    result += abs(self.objective_picture[i][j][c] - individual.pixels_array[i][j][c])
        return result 
