import math
import turtle
import numpy as np

degrees = lambda x: round(x * 360 / (math.pi*2),3)

class RlBot:
    def __init__(self):
        self.obs_count = 12  # equivalent to: 30 degree field of view
        self.sensor_fov = math.pi*2.0/self.obs_count
        self.sensor_range = 1000
        self.reset()

    def reset(self):
        self.x = 0
        self.y = 0
        self.heading = 0  # points directly to the right -->
        self.n_heading = 0 # eliminates rounding error

    def move(self, action):
        if action == 0:
            self.x += 10.0 * math.cos(self.heading)
            self.y += 10.0 * math.sin(self.heading)
        elif action == 1:
            self.n_heading += 1
        elif action == 2:
            self.n_heading -= 1

        self.n_heading %= 8
        self.heading = self.n_heading * math.pi/4

    def render(self):
        turtle.pendown()
        turtle.goto(self.x,self.y)

    # distance to center point x,y of an obstacle
    def distance_to_ob(self, ob):
        return self.distance(ob.x,ob.y) - ob.radius

    # distance to point x,y
    def distance(self, x, y):
        return math.sqrt((self.x-x)**2+(self.y-y)**2)

    # absolute bearing to point x,y
    def bearing(self, x, y):
        if x==self.x and y==self.y:
            return 0.0
        elif y >= self.y:
            return math.acos((x-self.x)/self.distance(x,y))
        else:
            return 2*math.pi - math.acos((x-self.x)/self.distance(x,y))

    # absolute bearing to center point x,y of an obstacle (in radians)
    def bearing_to_ob(self, ob):
        return self.bearing(ob.x,ob.y)

    def bearings_to_ob(self, ob, correction=0.0):
        b = self.bearing_to_ob(ob)
        dx = ob.radius * math.cos(b+math.pi/2)
        dy = ob.radius * math.sin(b+math.pi/2)
        left = self.bearing(ob.x+dx,ob.y+dy)
        right = self.bearing(ob.x-dx,ob.y-dy)
        left -= correction
        right -= correction
        left = left if left < math.pi else left-2*math.pi
        left = left if left > -math.pi else left+2*math.pi
        right = right if right < math.pi else right-2*math.pi
        right = right if right > -math.pi else right+2*math.pi
        return left, right, (ob.x+dx,ob.y+dy), (ob.x-dx,ob.y-dy)

    def get_distance(self, obstacles):
        ranges = []
        for n in range(self.obs_count):
            min_range = self.sensor_range
            sensor_bearing = n * self.sensor_fov + self.heading
            sensor_bearing = sensor_bearing if sensor_bearing < math.pi*2 else sensor_bearing-math.pi*2
            for ob in obstacles:
                left, right, _0, _1 = self.bearings_to_ob(ob, sensor_bearing)
                left_edge = abs(left) < self.sensor_fov/2
                right_edge = abs(right) < self.sensor_fov/2
                both_edges = self.sensor_fov/2 < left and -self.sensor_fov/2 > right
                if left_edge or right_edge or both_edges:
                    min_range = min(min_range, self.distance_to_ob(ob))
            ranges.append(min_range)
        return ranges

    def __str__(self):
      return 'RlBot x={} y={} heading={}'.format(self.x, self.y, self.heading)

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

    def __str__(self):
        return 'Obs x={} y={} radius={}'.format(self.x, self.y, self.radius)

class RlBotEnv:

    def __init__(self):
        turtle.radians()
        self.bot = RlBot()
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
        if min(obs) < 10: #or self.n > 200
            distances = [self.bot.distance_to_ob(o) for o in self.obstacles]
            self.obstacles.pop(np.argmin(distances))

        done = len(self.obstacles) == 0
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

for n in range(100000):
    e.obstacles = []
    for x in range(4):
        ob_x = np.random.randint(-300,300)
        ob_y = np.random.randint(-300,300)
        while ((ob_x**2 + ob_y**2)**0.5) < 100:
            ob_x = np.random.randint(-300,300)
            ob_y = np.random.randint(-300,300)
        e.obstacles.append(Obstacle(ob_x,ob_y,20))

    obs = e.reset()
    if n % 100 == 0:
        e.render_backdrop()
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
        if n % 100 == 0:
            e.render()
