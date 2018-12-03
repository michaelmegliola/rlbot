import math
import numpy as np
import rcpy
import rcpy.mpu9250 as mpu9250
import rcpy.motor as motor
from stepper import Stepper
from distancesensor import *

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
