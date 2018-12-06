import numpy as np

class QBot:
    def action_space(self):
        return self.turn_sectors

    def observation_space(self):
        return self.sensor_sectors

    def sample(self):
        return np.random.randint(self.action_space())

