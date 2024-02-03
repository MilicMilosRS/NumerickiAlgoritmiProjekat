import numpy as np
from Ball import *
from Line import *
from Polygon import *

def perpendicular(vector: np.array) -> np.array:
    return np.array((-vector[1], vector[0]))

#returns the min and max
def projectCircle(circle: Ball, axis: np.array) -> (float, float):
    direction = normalize(axis)
    p1 = circle.position + direction * circle.radius
    p2 = circle.position - direction * circle.radius
    
    p1 = np.dot(p1, axis)
    p2 = np.dot(p2, axis)

    if p1 < p2:
        return p1, p2
    else:
        return p2, p1 
    
def projectPolygon(polygon: Polygon, axis: np.array) -> (float, float):
    minimum = float("inf")
    maximum = float("-inf")
    for i in range(len(polygon.getTransformedPoints())):
        point = polygon.getTransformedPoints()[i]
        proj = np.dot(point, axis)
        if proj < minimum:
            minimum = proj
        if proj > maximum:
            maximum = proj
    return minimum, maximum

def projectLine(line: Line, axis: np.array) -> (float, float):
    p1 = np.dot(line.transformedPointA(), axis)
    p2 = np.dot(line.transformedPointB(), axis)

    if p1 < p2:
        return p1, p2
    else:
        return p2, p1

def intersectCirclePolygon(circle: Ball, polygon: Polygon) -> (bool, np.array, float):
    normal = np.zeros(2)
    depth = float("inf")

    axis = np.zeros(2)
    axisDepth = 0
    
    for i in range(len(polygon.getTransformedPoints())):
        #Point A
        pa = polygon.getTransformedPoints()[i]
        #Point B
        pb = polygon.getTransformedPoints()[(i+1) % len(polygon.points)]

        edge = pb - pa
        #Vector perpendicular to the edge
        axis = perpendicular(edge)
        axis = normalize(axis)

        minA, maxA = projectPolygon(polygon, axis)
        minB, maxB = projectCircle(circle, axis)

        if minA > maxB or minB > maxA:
            return False, np.zeros(2), 0
        
        axisDepth = min(maxB - minA, maxA - minB)

        if axisDepth < depth:
            depth = axisDepth
            normal = axis

    #Closest point of polygon to the circle
    cpIndex = findClosestPoint(circle, polygon.getTransformedPoints())
    cp = polygon.getTransformedPoints()[cpIndex]

    axis = cp - circle.position
    axis = normalize(axis)

    minA, maxA = projectPolygon(polygon, axis)
    minB, maxB = projectCircle(circle, axis)

    if minA > maxB or minB > maxA:
        return False, np.zeros(2), 0
    
    axisDepth = min(maxB - minA, maxA - minB)

    if axisDepth < depth:
        depth = axisDepth
        normal = axis

    if np.dot(polygon.position - circle.position, normal) > 0.0:
        normal = -normal

    return True, normal, depth


#return the index of the closest point to the shape
def findClosestPoint(shape: PhysicsObject, points: np.array) -> (int):
    minDistance = float("+inf")
    minIndex = -1
    for i in range(len(points)):
        vec = shape.position - points[i]
        distance = np.sqrt(np.sum(np.square(vec)))
        
        if distance < minDistance:
            minDistance = distance
            minIndex = i
    
    return minIndex

def intersectCircleLine(circle: Ball, line: Line) -> (bool, np.array, float):
    depth = float("inf")
    normal = line.getNormal()

    axes = [line.getNormal()]
    for axis in axes:
        axis = normalize(axis)

        min1, max1 = projectCircle(circle, axis)
        min2, max2 = projectLine(line, axis)

        if min1 > max2 or min2 > max1:
            return False, np.zeros(2), 0
        
        axisDepth = min(max2 - min1, max1 - min2)

        if axisDepth < depth:
            normal = axis
            depth = axisDepth

    #closest line end
    cpIndex = findClosestPoint(circle, np.array((line.transformedPointA(), line.transformedPointB())))
    cp = line.transformedPointB()
    if cpIndex == 0:
        cp = line.transformedPointA()


    axis = normalize(cp - circle.position)
    
    min1, max1 = projectCircle(circle, axis)
    min2, max2 = projectLine(line, axis)

    if min1 > max2 or min2 > max1:
        return False, np.zeros(2), 0
        
    axisDepth = min(max2 - min1, max1 - min2)
    if axisDepth < depth:
        depth = axisDepth
        normal = axis

    if np.dot(line.position - circle.position, normal) > 0.0:
        normal = -normal
    
    return True, normal, depth
        
def intersectCircles(c1: Ball, c2: Ball) -> (bool, np.array, float):
    vec = c1.position - c2.position
    distance = np.sqrt(np.sum(np.square(vec)))
    radii = c1.radius + c2.radius

    normal = np.zeros(2)
    depth = float("inf")

    if distance >= radii:
        return False, normal, depth
    
    normal = normalize(vec)
    depth = radii - distance

    return True, normal, depth

def collide(body1, body2) -> (bool, np.array, float):
    normal = np.zeros(2)
    depth = 0

    if body1.type == "LINE":
        if body2.type == "BALL":
            collided, normal, depth =  intersectCircleLine(body2, body1)
            return collided, -normal, depth
    elif body1.type == "BALL":
        if body2.type == "LINE":
            return intersectCircleLine(body1, body2)
        elif body2.type == "BALL":
            return intersectCircles(body1, body2)
        elif body2.type == "POLYGON":
            return intersectCirclePolygon(body1, body2)
    elif body1.type == "POLYGON":
        if body2.type == "BALL":
            collided, normal, depth = intersectCirclePolygon(body2, body1)
            return collided, -normal, depth
            
        
    return False, normal, depth

#Distance from point p to line segment AB
def pointLineDistance(p, a, b) -> (float, np.array):
    ab = b - a
    ap = p - a

    proj = np.dot(ap, ab) / np.linalg.norm(ab)
    #Ratio of the length from point A to the point of projection
    #and the length of the line AB
    ratio = proj / np.linalg.norm(ab)

    #Contact point on line ab
    cp = 0
    if ratio < 0:
        cp = a
    elif ratio > 1:
        cp = b
    else:
        cp = a + ab * ratio

    
    distance = np.sqrt(np.sum(np.square(p - cp)))

    return distance, cp

def contactCircles(c1: Ball, c2: Ball):
    dir = c2.position - c1.position
    dir = normalize(dir)
    return [c1.position + c1.radius * dir]

def contactCircleLine(body1: Ball, body2: Line) -> list:
    distance, cp = pointLineDistance(body1.position, body2.transformedPointA(), body2.transformedPointB())
    return [cp]

def contactCirclePolygon(body1: Ball, body2: Polygon) -> list:
    cp = np.zeros(2)

    mindDist = float("inf")
    
    for i in range(len(body2.getTransformedPoints())):
        pa = body2.getTransformedPoints()[i]
        pb = body2.getTransformedPoints()[(i+1) % len(body2.points)]

        dist, contact = pointLineDistance(body1.position, pa, pb)
        if dist < mindDist:
            mindDist = dist
            cp = [contact]
    return cp

def findPointsOfContact(body1, body2) -> list:
    if body1.type == "LINE":
        if body2.type == "BALL":
            return contactCircleLine(body2, body1)
    elif body1.type == "BALL":
        if body2.type == "LINE":
            return contactCircleLine(body1, body2)
        elif body2.type == "BALL":
            return contactCircles(body1, body2)
        elif body2.type == "POLYGON":
            return contactCirclePolygon(body1, body2)
    elif body1.type == "POLYGON":
        if body2.type == "BALL":
            return contactCirclePolygon(body2, body1)