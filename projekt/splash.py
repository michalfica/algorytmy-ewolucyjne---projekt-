import numpy as np

class Splash:
    DEFAULT_R = 100 
    INITIAL_MAX_RANK  = 10 
    LENGTH, WIDTH = 480, 405  # obrazka - redundancja - co z tym zrobic ?? 

    number_of_parameters = 4
    COLOR, RANK, LOCATION, RADIUS = 0, 1, 2, 3

    BLACK = np.array([0, 0, 0], dtype=np.uint64)

    def __init__(self, color=BLACK, rank=INITIAL_MAX_RANK, x=0, y=0, r=DEFAULT_R):
        self.color = color
        self.rank  = rank 
        self.r = r 
        self.x, self.y = x, y 

    def random_splash(self, max_rank, length, width, set_specific_ranking=False, ranking=None, objective_picture=None):
        self.color = np.array([np.random.randint(0,255) for _ in range(3)], dtype=np.uint64)
        self.rank = np.random.randint(0, max_rank)
        self.r = np.random.randint(1, Splash.DEFAULT_R+1)
        self.x = np.random.randint(0, length)
        self.y = np.random.randint(0, width)

        if set_specific_ranking == True:
            self.rank = ranking


        def outside_of_frame(pixel):
            return ((pixel[0] < 0 or Splash.LENGTH <= pixel[0]) or
                    (pixel[1] < 0 or Splash.WIDTH <= pixel[1]))
         
        def outside_of_splash(pixel, x, y, r):
            return (pixel[0]-x)**2 + (pixel[1]-y)**2 > r**2

        if objective_picture is not None:
            
            counter = 0
            red, green, blue = 0, 0, 0

            for t in range(-self.r,self.r+1):
                for s in range(-self.r,self.r+1):

                    pixel = (int(self.x+t), int(self.y+s))
                    if outside_of_frame(pixel) or outside_of_splash(pixel, self.x, self.y, self.r):
                        continue

                    red += objective_picture[pixel[0]][pixel[1]][0]
                    green += objective_picture[pixel[0]][pixel[1]][1]
                    blue += objective_picture[pixel[0]][pixel[1]][2]
                    counter += 1

            if counter != 0:
                red = int(np.floor(red / counter))
                green = int(np.floor(green / counter))
                blue = int(np.floor(blue / counter))

            # print('srednia ktora wybralem to: ', red, green, blue)
            self.color = [red, green, blue]

        # print('KONCZEEEE ')

    def count_distance(self, x, y, r):
        length = abs(self.y - y)
        width = abs(self.x - x)
        return length ** 2 + width ** 2 <= r ** 2
    
    def change_slightly(self, parametr):

        # print('bede zmienial: ', parametr)
        if parametr==Splash.COLOR:
            epsilon = np.array([np.random.randint(-40,40) for _ in range(3)], dtype=np.int64)
            # print('zmieniam kolor o ', epsilon)
            self.color[0] += epsilon[0]
            self.color[1] += epsilon[1]
            self.color[2] += epsilon[2]
            
            for i in range(3):
                self.color[i] = min(255, self.color[i])
                self.color[i] = max(0, self.color[i]) 

        if parametr==Splash.RANK:
            
            epsilon = np.random.randint(-2,2)
            # print('zmieniam rank o:', epsilon)
            self.rank += epsilon
            # self.rank = min(Splash.MAX_RANK, self.rank)
            self.rank = max(0, self.rank)
        
        if parametr == Splash.LOCATION:
            epsilon = [np.random.randint(-40,40) for _ in range(2)]
            # print('zmieniam polozenie o: ', epsilon)
            self.x += epsilon[0]
            self.y += epsilon[1]
            self.x = max(0, self.x)
            self.x = min(Splash.LENGTH-1, self.x)
            self.y = max(0, self.y)
            self.y = min(Splash.WIDTH-1, self.y)
        
        if parametr==Splash.RADIUS:
            epsilon = np.random.randint(-30,30)
            # print('zmienam promien o: ', epsilon)
            self.r += epsilon
            self.r = max(1, self.r)
            self.r = min(Splash.DEFAULT_R, self.r)


    def __str__(self):
        return f'<{self.color[0]}, {self.color[1]}, {self.color[2]}>'

    def __repr__(self):
        return f'[{self.color[0]}, {self.color[1]}, {self.color[2]}]'
    