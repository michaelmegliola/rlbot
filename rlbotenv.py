import math
import numpy as np

degrees = lambda x: round(x * 360 / (math.pi*2),3)

class Obstacle:
    def __init__(self,x,y,r):
        self.x = x
        self.y = y
        self.radius = r

class RlBotEnv:

    def __init__(self, bot, renderer = None):
        self.bot = bot
        self.renderer = renderer

    def reset(self):
        self.n = 0
        self.bot.reset()
        if self.renderer != None:
            self.renderer.render_reset_turtle(self.bot)
        return self.bot.get_distance(self.obstacles)

    def step(self, action):
        distance = min(self.bot.get_distance(self.obstacles))
        self.bot.move(action)
        obs = self.bot.get_distance(self.obstacles)
        reward = distance-min(obs)
        self.n += 1
        done = min(obs) < 10 #or self.n > 200
        return obs, reward, done

    def sample(self):
        return np.random.randint(3)

    def render(self):
        if self.renderer != None:
            self.renderer.render_bot(self.bot)
