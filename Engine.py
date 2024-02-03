import pygame
from PhysicsObject import *
from Ball import *
from Polygon import *
from Line import *
import CollisionHandler as ch
from FixedJoint import FixedJointConstraint

class GameEngine(object):
    def __init__(self, grav) -> None:
        self._contactPairs = []
        self._objects = []
        self._balls = []
        self._grabbed_ball = None
        self._gravity = np.array(grav)
        self._wind = np.zeros(2)

        #Screen borders
        self.addObject(Line((0, 0), (0, 480), 10, True))
        self.addObject(Line((0, 480), (640, 480), 10, True))
        self.addObject(Line((640, 480), (640, 0), 10, True))
        self.addObject(Line((640, 0), (0, 0), 10, True))

        #Floor
        self._floor = Polygon(10, [(0, 400), (640, 400), (640, 480), (0, 480)], True)
        self._floor.color = (30, 30, 30)
        self._floor.filled = True
        self.addObject(self._floor)
        
        #Basketball hoop
        temp = Polygon(100, [(500, 400), (600, 400), (560, 210), (510, 210)], True)
        temp.color = (70, 70, 70)
        temp.line_thickness = 5
        temp.filled = False
        self.addObject(temp)
        temp = Polygon(100, [(505, 230), (560, 210), (460, 175), (460, 200)], True)
        temp.color = (70, 70, 70)
        temp.line_thickness = 5
        temp.filled = False
        self.addObject(temp)

        #Basketball table
        self._table = Line((460, 135), (460, 255), 10, False)
        self._table.momentOfInertia = 100000
        self._table.line_thickness = 5
        self.addObject(self._table)
        self._ball = Ball((390.0, 225.0), 2, 3)
        # self._ball.momentOfInertia = 1000
        self.addObject(self._ball)

        self._board_constraint = FixedJointConstraint(self._table, self._floor)
        self._constraint = FixedJointConstraint(self._ball, self._table)

        self._score = 0
        self._font = pygame.font.Font(None, 40)
        self._small_font = pygame.font.Font(None, 20)
        self._show_extra_text = False
        
    def detectCollisions(self):
        for i in range(len(self._balls)):
            for j in range(len(self._objects)):
                collided, normal, depth = ch.collide(self._balls[i], self._objects[j])

                if collided:
                    self.seperateBodies(self._balls[i], self._objects[j], normal * depth)
                    poc = ch.findPointsOfContact(self._balls[i], self._objects[j])
                    self.resolveCollisions(self._balls[i], self._objects[j], normal, depth, poc)

        for i in range(len(self._balls) - 1):
            for j in range(i+1, len(self._balls)):
                collided, normal, depth = ch.collide(self._balls[i], self._balls[j])

                if collided:
                    self.seperateBodies(self._balls[i], self._balls[j], normal * depth)
                    poc = ch.findPointsOfContact(self._balls[i], self._balls[j])
                    self.resolveCollisions(self._balls[i], self._balls[j], normal, depth, poc)


        

    def seperateBodies(self, body1, body2, mov: np.array):
        if body1.isStatic():
            body2.position -= mov
        elif body2.isStatic():
            body1.position += mov
        else:
            body1.position += mov/2
            body2.position -= mov/2

    def resolveCollisions(self, body1, body2, normal: np.array, depth: float, pointsOfContact: list):
        jList = [0] * len(pointsOfContact)
        impulseList = [np.zeros(2)] * len(pointsOfContact)
        frictionImpulseList = [np.zeros(2)] * len(pointsOfContact)
        raList = [np.zeros(2)] * len(pointsOfContact)
        rbList = [np.zeros(2)] * len(pointsOfContact)
        e = min(body1._restitution, body2._restitution)
        sf = (body1.staticFriction + body2.staticFriction)/2
        df = (body1.dynamicFriction + body2.dynamicFriction)/2

        for i in range(len(pointsOfContact)):
            #Vector from center of mass to point of contact
            ra = pointsOfContact[i] - body1.position
            rb = pointsOfContact[i] - body2.position

            raList[i] = ra
            rbList[i] = rb


            raPerp = np.array((-ra[1], ra[0]))
            rbPerp = np.array((-rb[1], rb[0]))

            angLinVelocityA = raPerp * body1.angularVelocity
            angLinVelocityB = rbPerp * body2.angularVelocity

            relativeVelocity = (body2.speed + angLinVelocityB) - (body1.speed + angLinVelocityA)

            contactVelocityMagnitude = np.dot(relativeVelocity, normal)

            if contactVelocityMagnitude < 0:
                continue

            raPerpDotN = np.dot(raPerp, normal)
            if body1.isStatic():
                raPerpDotN = 0
            rbPerpDotN = np.dot(rbPerp, normal)
            if body2.isStatic():
                rbPerpDotN = 0

            denominator = (1/body1.mass + 1/body2.mass)+(raPerpDotN**2)/body1.momentOfInertia + (rbPerpDotN**2)/body2.momentOfInertia

            j = -(1+e)*contactVelocityMagnitude
            j /= denominator
            j /= len(pointsOfContact)


            jList[i] = j
            impulse = j * normal
            impulseList[i] = impulse


        for i in range(len(pointsOfContact)):
            #Vector from center of mass to point of contact
            ra = pointsOfContact[i] - body1.position
            rb = pointsOfContact[i] - body2.position

            raList[i] = ra
            rbList[i] = rb

            raPerp = np.array((-ra[1], ra[0]))
            rbPerp = np.array((-rb[1], rb[0]))

            angLinVelocityA = raPerp * body1.angularVelocity
            angLinVelocityB = rbPerp * body2.angularVelocity

            relativeVelocity = (body2.speed + angLinVelocityB) - (body1.speed + angLinVelocityA)

            tangent = relativeVelocity - np.dot(relativeVelocity, normal) * normal

            if np.isclose(np.sum(np.square(tangent)), 0, 0, 0.0005**2):
                continue

            tangent = ch.normalize(tangent)

            raPerpDotT = np.dot(raPerp, tangent)
            if body1.isStatic():
                raPerpDotT = 0
            rbPerpDotT = np.dot(rbPerp, tangent)
            if body2.isStatic():
                rbPerpDotT = 0

            denominator = (1/body1.mass + 1/body2.mass)+(raPerpDotT**2)/body1.momentOfInertia + (rbPerpDotT**2)/body2.momentOfInertia

            jt = -np.dot(relativeVelocity, tangent)
            jt /= denominator
            jt /= len(pointsOfContact)

            frictionImpulse = 0
            if(np.abs(jt) <= jList[i] * sf):
                frictionImpulse = jt * tangent
            else:
                frictionImpulse = -jList[i] * tangent * df

            frictionImpulseList[i] = frictionImpulse
        
        for i in range(len(pointsOfContact)):
            body1.speed = np.subtract(body1.speed, np.divide(impulseList[i], body1.mass))
            body1.angularVelocity -= np.cross(raList[i], impulseList[i])/body1.momentOfInertia
            body2.speed = np.add(body2.speed, np.divide(impulseList[i], body2.mass))
            body2.angularVelocity += np.cross(rbList[i], impulseList[i])/body2.momentOfInertia

        for i in range(len(pointsOfContact)):
            test = np.cross(raList[i], frictionImpulseList[i])/body1.momentOfInertia
            body1.speed = body1.speed + np.divide(frictionImpulseList[i], body1.mass)
            body1.angularVelocity = body1.angularVelocity + np.cross(raList[i], frictionImpulseList[i])/body1.momentOfInertia
            body2.speed = body2.speed - np.divide(frictionImpulseList[i], body2.mass)
            body2.angularVelocity = body2.angularVelocity - np.cross(rbList[i], frictionImpulseList[i])/body2.momentOfInertia



    def draw(self, screen):
        for o in self._objects:
            o.draw(screen)
        for b in self._balls:
            b.draw(screen)

        self._ball.draw(screen)
        self._floor.draw(screen)

        #Draw hoop line
        pygame.draw.line(screen, (252, 78, 3), self._ball.position, self._table.position + np.array((0.0, 32.0)), 6)

        text = self._font.render(f"Score: {self._score}", False, (255, 255, 255), (0, 0, 0))
        textRect = text.get_rect()
        textRect.topleft = (0, 0)
        screen.blit(text, textRect)

        if self._show_extra_text:
            extra_text = f"""'d' to make the wind blow right
            'a' to make the wind blow left
            'w' to make the gravity weaker
            's' to make the gravity stronger
            'e' to add more balls
            'i' to hide extra information
            Wind strength: ({self._wind[0]:.2f}, {self._wind[1]:.2f})
            Gravity strength: ({self._gravity[0]:.2f}, {self._gravity[1]:.2f})"""
            
            x, y = 640, 0
            lines = extra_text.split('\n')
            for line in lines:
                text = self._small_font.render(line, False, (255, 255, 255), (0, 0, 0))
                text_width, text_height = text.get_size()

                text_rect = text.get_rect()
                text_rect.topright = (640, y)
                y += text_height
                screen.blit(text, text_rect)

        else:
            extraText = self._small_font.render("'i' for more information", False, (255, 255, 255), (0, 0, 0))
            extraTextRect = extraText.get_rect()
            extraTextRect.topright = (640, 0)
            screen.blit(extraText, extraTextRect)

    def _check_if_falling_through_hoop(self):
        for b in self._balls:
            collided, _, _ = ch.collide(b, Line(self._ball.position, self._table.position + np.array((0.0, 32.0)), 0.0, True))
            if collided:
                if b.speed[1] > 0.0:
                    b._falling_through_hoop = True
                else:
                    b._falling_through_hoop = False
            else:
                if b._falling_through_hoop:
                    self._score += 1
                    print(self._score)
                b._falling_through_hoop = False

    def tick(self, mousePos: np.array):
        self._contactPairs = []
        for o in self._objects:
            if not o.isStatic():
                o.tick(self._gravity, [self._wind])

        for b in self._balls:
            if b is not self._grabbed_ball:
                b.tick(self._gravity, [self._wind])
            else:
                delta_p = mousePos - b.position
                # wanted_velocity = delta_p * 0.05
                # b.speed = delta_p / 2
                b.tick(np.array((0.0, 0.0)), [delta_p/640, self._wind])
        
        self._ball.tick(self._gravity)
        self._floor.tick(self._gravity)
        self._table.tick(self._gravity)
        self.detectCollisions()


        self._board_constraint.calculate_impulse(self._table, self._floor)
        self._constraint.calculate_impulse(self._ball, self._table)

        self._check_if_falling_through_hoop()

    def addObject(self, obj: PhysicsObject):
        self._objects.append(obj)

    def addBall(self, x, y):
        self._balls.append(Ball((x, y), 1, 30))

    def grabBall(self, x, y):
        if self._grabbed_ball is not None:
            return
        
        mousePos = np.array((x, y))
        for b in self._balls:
            if np.sqrt(np.sum(np.square(b.position - mousePos))) < b.radius:
                self._grabbed_ball = b

    def releaseBall(self):
        self._grabbed_ball = None

    def key_released(self, key):
        if key == pygame.K_e:
            x, y = pygame.mouse.get_pos()
            self.addBall(x, y)
        elif key == pygame.K_i:
            self._show_extra_text = not self._show_extra_text
        elif key == pygame.K_a:
            self._wind[0] -= 0.01
        elif key == pygame.K_d:
            self._wind[0] += 0.01
        elif key == pygame.K_w:
            self._gravity[1] -= 0.03
        elif key == pygame.K_s:
            self._gravity[1] += 0.03