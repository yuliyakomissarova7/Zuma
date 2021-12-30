import math

import pygame

from modules.parameters import *


class ShootBall(pygame.sprite.Sprite):
    def __init__(self, color, position=DISPLAY_CENTER):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.ball = pygame.Surface((BALL_DIAMETER, BALL_DIAMETER))
        self.rect = self.ball.get_rect(center=position)
        self.speed = 20
        self.point = (0, 0)

    def set_points(self, target):
        self.point = (target[0] - self.rect.center[0],
                      target[1] - self.rect.center[1])
        self.point = (self.point[0] / math.hypot(self.point[0], self.point[1]), self.point[1]
                      / math.hypot(self.point[0], self.point[1]))

    def update(self):
        self.rect.center = (self.rect.center[0] + self.point[0] * self.speed,
                            self.rect.center[1] + self.point[1] * self.speed)

    def draw_sprite(self, display):
        pygame.draw.circle(display, self.color, self.rect.center, BALL_DIAMETER / 2)
