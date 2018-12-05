import turtle
import numpy as np
import math

class Renderer:

    def __init__(self, n=1):
        turtle.radians()
        self.n = n
        self.count = -1

    def reset(self):
        self.count += 1

    def render_obstacle(self, obstacle):
        if self.count % self.n == 0:
            turtle.hideturtle()
            turtle.penup()
            turtle.goto(obstacle.x+obstacle.radius,obstacle.y)
            turtle.setheading(math.pi/2)
            turtle.pendown()
            turtle.circle(obstacle.radius)

    def render_backdrop(self, bot):
        if self.count % self.n == 0:
            turtle.colormode(255)
            turtle.pencolor((np.random.randint(255),np.random.randint(255),np.random.randint(255)))
            turtle.pensize(3+np.random.randint(5))
            for o in bot.obstacles:
                self.render_obstacle(o)
            self.render_reset_turtle(bot)

    def render_raytrace(self, env):
        turtle.hideturtle()
        turtle.goto(env.bot.x, env.bot.y)
        turtle.showturtle()
        for o in self.obstacles:
            a,b,m,n = env.bot.bearings_to_ob(o)
            d = env.bot.distance_to_ob(o)
            env.render_reset_turtle()
            turtle.pendown()
            turtle.goto(m[0], m[1])
            env.render_reset_turtle()
            turtle.pendown()
            turtle.goto(n[0], n[1])
        env.render_reset_turtle()

    def render_reset_turtle(self, bot):
        if self.count % self.n == 0:
            turtle.hideturtle()
            turtle.penup()
            turtle.goto(bot.x, bot.y)
            turtle.setheading(bot.heading)
            turtle.showturtle()

    def render_bot(self, bot):
        if self.count % self.n == 0:
            turtle.pendown()
            turtle.goto(bot.x,bot.y)
