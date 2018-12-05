from rlbotenv import *
from qvbot import *
from renderer import Renderer

e = RlBotEnv(QvBot(24,24,1), Renderer(500))
q = np.random.rand(e.bot.observation_space(), e.bot.action_space())

explore = 0.1
alpha = 0.1
gamma = 0.9

for n in range(100000):
    state = e.reset()
    done = False
    while not done:
        if np.random.random() < explore:
            action = e.bot.sample()
        else:
            action = np.argmax(q[state])
        next_state, reward, done = e.step(action)
        q[state][action] = (1-alpha) * q[state][action] + alpha * (reward + gamma * np.max(q[next_state]))
        state = next_state
    print(n)
