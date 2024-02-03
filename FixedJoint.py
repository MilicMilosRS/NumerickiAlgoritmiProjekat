from PhysicsObject import *
import numpy as np

class FixedJointConstraint(object):
    def __init__(self, obj1, obj2) -> None:
        self._relative_position = obj2.position - obj1.position
        self._relative_angle = obj2._angle - obj1._angle

    def calculate_impulse(self, obj1: PhysicsObject, obj2: PhysicsObject) -> np.array:
        delta_p = obj2.position - obj1.position
        relative_velocity = obj2.speed - obj1.speed
        wanted_velocity = (self._relative_position - delta_p)/2

        impulse = (obj1.mass * obj2.mass) * (relative_velocity - wanted_velocity) / 20

        obj1.speed = obj1.speed + impulse / obj1.mass
        # obj1.speed = wanted_velocity
        obj2.speed = obj2.speed - impulse / obj2.mass
        # obj2.speed = -wanted_velocity

        delta_a1 = obj1._angle - self._relative_angle
        delta_a2 = obj2._angle - self._relative_angle

        wanted_ang_velocity1 = -delta_a1 / 2
        wanted_ang_velocity2 = -delta_a2 / 2

        obj1.angularVelocity = obj1.angularVelocity + (wanted_ang_velocity1 - obj1.angularVelocity)
        obj2.angularVelocity = obj2.angularVelocity + (wanted_ang_velocity2 - obj2.angularVelocity)