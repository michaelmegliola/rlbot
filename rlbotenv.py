import math
import numpy as np

degrees = lambda x: round(x * 360 / (math.pi*2),3)

class RlBotEnv:

    def __init__(self, bot, renderer = None):
        self.bot = bot
        self.renderer = renderer

    def reset(self):
        self.n = 0
        self.bot.reset()
        if self.renderer != None:
            self.renderer.render_reset_turtle(self.bot)
        obs = self.bot.get_distance()
        self.min_distance = min(obs)            # for use in first call to step()
        return obs

    def step(self, action):
        self.bot.move(action)
        obs = self.bot.get_distance()
        reward = self.min_distance-min(obs)
        self.min_distance = min(obs)            # for use in next call to step()
        self.n += 1
        done = min(obs) < 10 #or self.n > 200
        return obs, reward, done

    def sample(self):
        return np.random.randint(3)

    def render(self):
        if self.renderer != None:
            self.renderer.render_bot(self.bot)
