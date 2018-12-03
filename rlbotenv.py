import math
import numpy as np
import rcpy
import rcpy.mpu9250 as mpu9250
import rcpy.motor as motor
from stepper import Stepper
from distancesensor import *

degrees = lambda x: round(x * 360 / (math.pi*2),3)


      
class RlHwBot(RlBot):
    def __init__(self):
        lidar = LidarSensor()
        
    def move(self, action):
        if action == 0:
            motor.motor1.set(-1 * 0.35)
            motor.motor2.set(1 * 0.36)
        elif action == 1:
            motor.motor1.set(-1 * 0.35)
            motor.motor2.set(-1 * 0.36)
        elif action == 2:
            motor.motor1.set(1 * 0.35)
            motor.motor2.set(1 * 0.36)
        time.sleep(0.21)
        motor.motor1.set(0.00)
        motor.motor2.set(0.00)

    def get_distance(self):
        return self.lidar.get_observation()

class Obstacle:
    def __init__(self,x,y,r):
        self.x = x
        self.y = y
        self.radius = r

    def render(self):
        turtle.hideturtle()
        turtle.penup()
        turtle.goto(self.x+self.radius,self.y)
        turtle.setheading(math.pi/2)
        turtle.pendown()
        turtle.circle(self.radius)

class RlBotEnv:

    def __init__(self):
        turtle.radians()
        self.bot = RlHwBot()
        #self.obstacles = [Obstacle(60,60,20), Obstacle(-300,-200,20), Obstacle(-50,-20, 40), Obstacle(0, 400, 40)]
        self.obstacles = [Obstacle(-300,-200,20),Obstacle(-300,200,20),Obstacle(300,-200,20),Obstacle(200,200,20)]

    def reset(self):
        self.n = 0
        self.bot.reset()
        self.render_reset_turtle()
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

    def render_backdrop(self):
        turtle.colormode(255)
        turtle.pencolor((np.random.randint(255),np.random.randint(255),np.random.randint(255)))
        turtle.pensize(3+np.random.randint(5))
        for o in self.obstacles:
            o.render()
        self.render_reset_turtle()

    def render_raytrace(self):
        turtle.hideturtle()
        turtle.goto(self.bot.x, self.bot.y)
        turtle.showturtle()
        for o in self.obstacles:
            a,b,m,n = self.bot.bearings_to_ob(o)
            d = self.bot.distance_to_ob(o)
            self.render_reset_turtle()
            turtle.pendown()
            turtle.goto(m[0], m[1])
            self.render_reset_turtle()
            turtle.pendown()
            turtle.goto(n[0], n[1])
        self.render_reset_turtle()

    def render_reset_turtle(self):
        turtle.hideturtle()
        turtle.penup()
        turtle.goto(self.bot.x, self.bot.y)
        turtle.setheading(self.bot.heading)
        turtle.showturtle()

    def render(self):
        self.bot.render()

e = RlBotEnv()
mr = -99999
q = np.zeros((12,3))

explore = 0.1
alpha = 0.1
gamma = 0.9

'''for n in range(100000):
    ob_x = np.random.randint(-300,300)
    ob_y = np.random.randint(-300,300)
    while ((ob_x**2 + ob_y**2)**0.5) < 100:
        ob_x = np.random.randint(-300,300)
        ob_y = np.random.randint(-300,300)
    e.obstacles = [Obstacle(ob_x,ob_y,20)]'''

obs = e.reset()
#e.render_backdrop()
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
