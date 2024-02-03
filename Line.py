from PhysicsObject import *
import numpy as np
import pygame

def normalize(vector: np.array) -> np.array:
    total = np.sqrt(np.sum(np.square(vector)))
    return np.divide(vector, total) 

class Line(PhysicsObject):
    def __init__(self, pointA, pointB, mass: float, static: bool) -> None:
        super().__init__((np.array(pointA) + np.array(pointB)) / 2, mass, static)
        self._type = "LINE"
        self._pointA = np.array(pointA) - self.position
        self._pointB = np.array(pointB) - self.position

        self._needTransforming = True
        self._tPointA = self._pointA
        self._tPointB = self._pointB


    @property
    def pointA(self) -> np.array:
        return self._pointA

    @property
    def pointB(self) -> np.array:
        return self._pointB
    
    def _updateTransformedPoints(self):
        a = self._angle

        va = self.pointA
        va = np.array((va[0]*np.cos(a) - va[1]*np.sin(a),
                    va[0]*np.sin(a) + va[1]*np.cos(a)))
        va += self.position

        vb = self.pointB
        vb = np.array((vb[0]*np.cos(a) - vb[1]*np.sin(a),
                    vb[0]*np.sin(a) + vb[1]*np.cos(a)))
        vb += self.position

        self._tPointA = va
        self._tPointB = vb
        self._needTransforming = False

    def transformedPointA(self):
        if self._needTransforming:
            self._updateTransformedPoints()
        return self._tPointA
    
    
    def transformedPointB(self):
        if self._needTransforming:
            self._updateTransformedPoints()
        return self._tPointB

    def getNormal(self) -> np.array:
        line = self.transformedPointB() - self.transformedPointA()
        return normalize(np.array((line[1], -line[0])))
    
    def getLine(self) -> np.array:
        return self.transformedPointB() - self.transformedPointA()
    
    def draw(self, screen):
        pygame.draw.line(screen, self.color, self.transformedPointA(), self.transformedPointB(), self.line_thickness)