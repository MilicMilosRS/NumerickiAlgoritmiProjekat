import numpy as np

class PhysicsObject(object):
    def __init__(self, position = np.zeros(2), mass = 5.0, static=False, color = (0, 0, 0), line_thickness = 1, filled = False) -> None:

        self._angle = 0.0
        self._angular_velocity = 0.0
        self._angular_acceleration = 0.0
        self._torque = 0.0
        self._momentOfInertia = 5.0
        
        self._position = np.array(position)
        self._speed = np.zeros(2)
        self._acceleration = np.zeros(2)
        self._force = np.zeros(2)
        self._mass = mass

        self._restitution = 1.0

        self._type = ""
        self._static = static

        self._staticFriction = 0.1
        self._dynamicFriction = 0.2

        self._needTransforming = True

        #Render options
        self.line_thickness = line_thickness
        self.color = color
        self.filled = filled

    @property
    def staticFriction(self):
        return self._staticFriction
    
    @property
    def dynamicFriction(self):
        return self._dynamicFriction

    @property
    def momentOfInertia(self):
        return self._momentOfInertia

    @momentOfInertia.setter
    def momentOfInertia(self, m):
        self._momentOfInertia = m

    @property
    def angularVelocity(self):
        return self._angular_velocity
    
    @angularVelocity.setter
    def angularVelocity(self, a):
        if not self.isStatic():
            self._angular_velocity = a

    @property
    def mass(self):
        return self._mass

    @property
    def type(self):
        return self._type
    
    @property
    def position(self) -> np.array:
        return self._position
    
    @position.setter
    def position(self, p):
        self._position = p

    @property
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self, s):
        if not self.isStatic():
            self._speed = s

    def tick(self, gravity_acceleration, outside_forces=None):
        if not self.isStatic():
            force = self._force + np.array(gravity_acceleration) * self._mass
            if outside_forces is not None:
                for f in outside_forces:
                    force += f

            self._acceleration = force / self._mass
            self._speed = self._speed + self._acceleration
            self._position = self._position + self._speed

            self._angular_acceleration = self._torque / self._momentOfInertia
            self._angular_velocity += self._angular_acceleration
            self._angle += self._angular_velocity
            self._needTransforming = True

    def isStatic(self):
        return self._static
    
    def setStatic(self, s: bool):
        self._static = s

    def draw(self, screen):
        pass

