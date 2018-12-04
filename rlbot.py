import math

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
        self.obstacles = Obstacle.make_obstacles(4)

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

    def get_distance(self):
        ranges = []
        for n in range(self.obs_count):
            min_range = self.sensor_range
            sensor_bearing = n * self.sensor_fov + self.heading
            sensor_bearing = sensor_bearing if sensor_bearing < math.pi*2 else sensor_bearing-math.pi*2
            for ob in self.obstacles:
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
