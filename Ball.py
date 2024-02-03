from PhysicsObject import *
import pygame

class Ball(PhysicsObject):
    def __init__(self, position, mass:float, radius:float, static:bool = False) -> None:
        super().__init__(position, mass, static)
        self._radius = radius
        self._restitution = 0.85    #Izmereno u stvarnom svetu
        self._type = "BALL"
        self._momentOfInertia = 0.4 * self._mass * self._radius**2

        self._falling_through_hoop = False

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), self._position, self._radius)
        
        a = self._angle
        rotMatrix = np.array((np.cos(a), -np.sin(a),np.sin(a), np.cos(a))).reshape((2,2))

        left_point = np.array((self.radius, 0)).reshape((2, 1))
        left_point = np.matmul(rotMatrix, left_point).reshape((-1,))

        right_point = -left_point

        upper_point = np.array((0, -self.radius)).reshape((2, 1))
        upper_point = np.matmul(rotMatrix, upper_point).reshape((-1,))

        lower_point = -upper_point

        rightish_point = np.array((self.radius/5, 0)).reshape((2, 1))
        rightish_point = np.matmul(rotMatrix, rightish_point).reshape((-1,))

        leftish_point = -rightish_point

        bottomright_point = np.array((self.radius * np.cos(np.pi/4), self.radius * np.sin(np.pi/4))).reshape((2,1))
        bottomleft_point = bottomright_point.copy()
        bottomleft_point[0, 0] *= -1.0
        topright_point = bottomright_point.copy()
        topright_point[1, 0] = topright_point[1, 0] * -1.0
        topleft_point = -bottomright_point

        bottomright_point = np.matmul(rotMatrix, bottomright_point).reshape((-1,))
        bottomleft_point = np.matmul(rotMatrix, bottomleft_point).reshape((-1,))
        topright_point = np.matmul(rotMatrix, topright_point).reshape((-1,))
        topleft_point = np.matmul(rotMatrix, topleft_point).reshape((-1,))
        

        pygame.draw.line(screen, (0, 0, 0), self.position + left_point, self.position + right_point)
        pygame.draw.line(screen, (0, 0, 0), self.position + upper_point, self.position + lower_point)
        pygame.draw.line(screen, (0, 0, 0), self.position + topright_point, self.position + rightish_point)
        pygame.draw.line(screen, (0, 0, 0), self.position + bottomright_point, self.position + rightish_point)
        pygame.draw.line(screen, (0, 0, 0), self.position + topleft_point, self.position + leftish_point)
        pygame.draw.line(screen, (0, 0, 0), self.position + bottomleft_point, self.position + leftish_point)

    @property
    def radius(self) -> float:
        return self._radius