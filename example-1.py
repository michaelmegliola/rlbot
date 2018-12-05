from rlbotenv import *
from qbot import *
from renderer import Renderer

e = RlBotEnv(QBot(36,36,1), Renderer(150))
q = np.zeros((36,36))

explore = 0.1
alpha = 0.1
gamma = 0.9

for n in range(100000):
    print(n)
    obs = e.reset()

    state = np.argmin(obs)
    done = False
    while not done:
        if np.random.random() < explore:
            action = e.bot.sample()
        else:
            action = np.argmax(q[state])
        obs, reward, done = e.step(action)
        next_state = np.argmin(obs)
        q[state][action] = (1-alpha) * q[state][action] + alpha * (reward + gamma * np.max(q[next_state]))
        state = next_state
