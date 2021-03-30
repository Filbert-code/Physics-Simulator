import pymunk as pm
import pygame as pg
from Car import Car
from RoadBuilder import RoadBuilder
import constants


class ObstacleCourse:
    def __init__(self, space):
        self._space = space
        self._rb = rb = RoadBuilder(self._space)
        # create a Car instance to use it's box creation function
        self._c = Car(self._space)
        self._road_body = None
        self.spring_trap_pin = None
        self.dynamic_bodies = []
        self.box_fort_image = pg.image.load("images/box_fort_img.png")

    def _create_road(self):
        vs = [((0, constants.HEIGHT), (2000, constants.HEIGHT)), ((2000, constants.HEIGHT), (2200, constants.HEIGHT-50)),
              ((2200, constants.HEIGHT-50), (2400, constants.HEIGHT-200)),
              ((3400, constants.HEIGHT-150), (3600, constants.HEIGHT-75)),
              ((3600, constants.HEIGHT - 75), (3800, constants.HEIGHT)),
              ((3800, constants.HEIGHT), (5000, constants.HEIGHT)),
              ]
        self._road_body, segments = self._rb.build_road(vs, 5)
        return segments

    def _box_fort(self):
        # first line of boxes
        # mass, x_pos, y_pos, w, h, vs=0, elasticity=0.3, friction=0.9
        fort_height = 0
        radius = 35
        starting_pos = 50
        fort_length = 350
        color = (50, 120, 240, 255)  # blue
        for i in range(10):
            b1, s1 = self._c.create_poly(50, 50, constants.HEIGHT - radius * i, radius, radius, friction=1, color=color)
            b2, s2 = self._c.create_poly(50, 50 + fort_length, constants.HEIGHT - radius * i, radius, radius, friction=1, color=color)
            fort_height = constants.HEIGHT - radius * i
            self.dynamic_bodies.append(b1)
            self.dynamic_bodies.append(b2)
        b, s = self._c.create_poly(200, starting_pos + fort_length / 2, fort_height - radius, fort_length, 35, color=color)
        self.dynamic_bodies.append(b)

    def _spring_trap(self):
        # create the spring body
        mass = 500
        width, length = 250, 0.01
        body, shape = self._c.create_poly(mass, 800, 595, width, length)
        # create the springs
        x, y = (800, 600)
        strength = 200000
        rest_length = 100
        spring_1 = pm.constraints.DampedSpring(body, self._road_body, (0, 0), (x, y + 20), rest_length, strength, 1)
        spring_2 = pm.constraints.DampedSpring(body, self._road_body, (-50, 0), (x - 50, y + 20), rest_length, strength, 1)
        spring_3 = pm.constraints.DampedSpring(body, self._road_body, (50, 0), (x + 50, y + 20), rest_length, strength, 1)
        # create stabilizer slider joints
        stabilizer_1 = pm.constraints.SlideJoint(body, self._road_body, (-75, 0), (x + 75, y + 20), 0, 180)
        stabilizer_2 = pm.constraints.SlideJoint(body, self._road_body, (75, 0), (x - 75, y + 20), 0, 180)
        self.spring_trap_pin = pm.constraints.PinJoint(body, self._road_body, (0, 0), (x, y))
        self._space.add(spring_1, spring_2, spring_3, stabilizer_1, stabilizer_2)
        self._space.add(self.spring_trap_pin)

    def build(self):
        segments = self._create_road()
        self._box_fort()
        self._spring_trap()
        return self.dynamic_bodies, segments
