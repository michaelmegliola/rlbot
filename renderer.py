import turtle

class Renderer:

    def __init__(self):
        turtle.radians()

    def render(self, obstacle):
        turtle.hideturtle()
        turtle.penup()
        turtle.goto(obstacle.x+obstacle.radius,obstacle.y)
        turtle.setheading(math.pi/2)
        turtle.pendown()
        turtle.circle(obstacle.radius)

    def render_backdrop(self, env):
        turtle.colormode(255)
        turtle.pencolor((np.random.randint(255),np.random.randint(255),np.random.randint(255)))
        turtle.pensize(3+np.random.randint(5))
        for o in env.obstacles:
            o.render()
        self.render_reset_turtle()

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
        turtle.hideturtle()
        turtle.penup()
        turtle.goto(bot.x, bot.y)
        turtle.setheading(bot.heading)
        turtle.showturtle()

    def render_bot(self, bot):
        turtle.pendown()
        turtle.goto(bot.x,bot.y)
