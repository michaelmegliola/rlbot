import math
import numpy as np
import rcpy
import rcpy.mpu9250 as mpu9250
import rcpy.motor as motor
from stepper import Stepper
from distancesensor import *

class RlHwBot():
    def __init__(self, sensor_sectors=4, turn_sectors=4):
        self.lidar = LidarSensor()
        self.sensor_sectors = sensor_sectors
        self.turn_sectors = turn_sectors
        
    def move(self, action):
        degree_duration_left = .0045             #length of time for one degree of rotation, tuned for left
        degree_duration_right = .0046             #length of time for one degree of rotation, tuned for right
        travel_duration = 0.25              #length of time to travel linearly
        if action == 0:
            motor.motor1.set(-1 * 0.35)
            motor.motor2.set(1 * 0.36)
            time.sleep(degree_duration)
        elif action == 1:
            motor.motor1.set(-1 * 0.35)
            motor.motor2.set(-1 * 0.36)
            time.sleep(degree_duration_right*360/self.turn_sectors)
        elif action == 2:
            motor.motor1.set(1 * 0.35)
            motor.motor2.set(1 * 0.36)
            time.sleep(degree_duration_left*360/self.turn_sectors)
        motor.motor1.set(0.00)
        motor.motor2.set(0.00)

    def get_distance(self):
        return self.lidar.get_observation()

    def reset(self):
        pass