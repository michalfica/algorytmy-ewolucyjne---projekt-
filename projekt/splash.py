import numpy as np

class Splash:
    DEFAULT_R = 100 
    MAX_RANK  = 10 
    LENGTH, WIDTH = 480, 405  # obrazka - redundancja - co z tym zrobic ?? 
    number_of_parameters = 4
    COLOR, RANK, LOCATION, RADIUS = 0, 1, 2, 3, 

    BLACK = np.array([0, 0, 0], dtype=np.uint64)

    def __init__(self, color=BLACK, rank=MAX_RANK, x=0, y=0, r=DEFAULT_R):
        self.color = color
        self.rank  = rank 
        self.r = r 
        self.x, self.y = x, y 

    def random_splash(self, max_rank, length, width):
        self.color = np.array([np.random.randint(0,255) for _ in range(3)], dtype=np.uint64)
        self.rank = np.random.randint(0, max_rank)
        self.r = np.random.randint(1, Splash.DEFAULT_R+1)
        self.x = np.random.randint(0, length)
        self.y = np.random.randint(0, width)

    def change_slightly(self, parametr):
        if parametr==Splash.COLOR:
            epsilon = np.array([np.random.randint(-40,40) for _ in range(3)], dtype=np.int64)

            print('zmieniam kolory o : ', epsilon)
            self.color[0] += epsilon[0]
            self.color[1] += epsilon[1]
            self.color[2] += epsilon[2]
            
            for i in range(3):
                self.color[i] = min(255, self.color[i])
                self.color[i] = max(0, self.color[i]) 

        if parametr==Splash.RANK:
            epsilon = np.random.randint(-3,3)
            self.rank += epsilon
            self.rank = min(Splash.MAX_RANK, self.rank)
            self.rank = max(0, self.rank)
        
        if parametr==Splash.LOCATION:
            epsilon = [np.random.randint(-40,40) for _ in range(2)]
            self.x += epsilon[0]
            self.y += epsilon[1]

            print('przesuwam środek: ', epsilon)
            self.x = max(0, self.x)
            self.x = min(Splash.LENGTH-1, self.x)
            self.y = max(0, self.y)
            self.y = min(Splash.WIDTH-1, self.y)
        
        if parametr==Splash.RADIUS:
            epsilon = np.random.randint(-30,30)
            self.r += epsilon
            print('zmieniam promien o ', epsilon)
            self.r = max(1, self.r)
            self.r = min(Splash.DEFAULT_R, self.r)


    def __str__(self):
        return f'<{self.color[0]}, {self.color[1]}, {self.color[2]}>'

    def __repr__(self):
        return f'[{self.color[0]}, {self.color[1]}, {self.color[2]}]'
    