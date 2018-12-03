
from rlbotenv import *
from rlbot import *
from renderer import Renderer

a = RlBot()
b = Renderer()

e = RlBotEnv(RlBot(), Renderer())
mr = -99999
q = np.zeros((12,3))

explore = 0.1
alpha = 0.1
gamma = 0.9

for n in range(100000):
    ob_x = np.random.randint(-300,300)
    ob_y = np.random.randint(-300,300)
    while ((ob_x**2 + ob_y**2)**0.5) < 100:
        ob_x = np.random.randint(-300,300)
        ob_y = np.random.randint(-300,300)
    e.obstacles = [Obstacle(ob_x,ob_y,20)]

    obs = e.reset()

    state = np.argmin(obs)
    done = False
    while not done:
        if np.random.random() < explore:
            action = e.sample()
        else:
            action = np.argmax(q[state])
        obs, reward, done = e.step(action)
        next_state = np.argmin(obs)
        q[state][action] = (1-alpha) * q[state][action] + alpha * (reward + gamma * np.max(q[next_state]))
        state = next_state
        e.render()
