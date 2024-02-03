from PhysicsObject import *
import pygame
import numpy as np

class Polygon(PhysicsObject):
    def __init__(self, mass, points, static=False) -> None:
        position = np.mean(np.array(points), axis=0)

        super().__init__(position, mass, static)
        self._points = []
        for p in points:
            self._points.append(np.array(p) - position)
        self._transformedPoints = self._points
        self._updateTransformedPoints()
        self._type = "POLYGON"
        self._needTransforming = False


    def _updateTransformedPoints(self):
        p = []

        for i in range(len(self._points)):
            va = self._points[i]
            a = self._angle
            va = np.array((va[0]*np.cos(a) - va[1]*np.sin(a),
                        va[0]*np.sin(a) + va[1]*np.cos(a)))
            va += self.position

            p.append(va)
        
        self._transformedPoints = p
        self._needTransforming = False

    def getTransformedPoints(self):
        if self._needTransforming:
            self._updateTransformedPoints()
        return self._transformedPoints

    @property
    def points(self):
        return self._points
    
    def draw(self, screen):
        if self.filled:
            pygame.draw.polygon(screen, self.color, self.getTransformedPoints())
        else:
            pygame.draw.polygon(screen, self.color, self.getTransformedPoints(), self.line_thickness)