
from rlbotenv import *
from rlbot import *
from renderer import Renderer

e = RlBotEnv(RlBot(1), None)
q = np.zeros((12,3))

explore = 0.1
alpha = 0.1
gamma = 0.9

for n in range(100):

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
    print(explore)
