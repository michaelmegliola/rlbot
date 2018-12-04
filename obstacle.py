import numpy as np

class Obstacle:
    def __init__(self,x,y,r):
        self.x = x
        self.y = y
        self.radius = r

    def make_obstacles(n, radius=20, max_x=300, max_y=300):
        obs = []
        ob_x = np.random.randint(-max_x,max_x)
        ob_y = np.random.randint(-max_y,max_y)
        while ((ob_x**2 + ob_y**2)**0.5) < 100:
            ob_x = np.random.randint(-max_x,max_x)
            ob_y = np.random.randint(-max_y,max_y)
        obs.append(Obstacle(ob_x,ob_y,radius))
        return obs