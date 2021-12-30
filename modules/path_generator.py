import math

import pygame.draw
from modules.colors import *


class PathGenerator:
    def __init__(self, level_number):
        self.points = []
        self.ball_positions = []
        self.step = 2
        if level_number == 1:
            self.spiral_path()
        elif level_number == 2:
            self.triangle_path()

    def spiral_path(self):
        self.points = [(0, 100), (700, 100), (900, 370), (700, 700), (300, 700), (100, 450), (300, 200), (600, 200),
                       (760, 370), (600, 600), (400, 600), (280, 450), (400, 300)]
        self.get_ball_positions()

    def triangle_path(self):
        self.points = [(0, 100), (900, 100), (520, 650), (150, 200), (700, 200), (610, 310)]
        self.get_ball_positions()

    def get_ball_positions(self):
        point_index = 0
        pos = pygame.math.Vector2(self.points[0])
        direction = pygame.math.Vector2((0, 0))
        while point_index < len(self.points):
            pos = pos + (direction * self.step)
            self.ball_positions.append(pos)

            if (round(pos.x), round(pos.y)) == self.points[point_index]:
                point_index += 1
                if point_index == len(self.points):
                    break
                direction = self.new_direction(point_index, pos)

    def new_direction(self, point_index, pos):
        direction = pygame.math.Vector2((self.points[point_index][0] - pos[0],
                                         self.points[point_index][1] - pos[1]))
        return pygame.math.Vector2((direction[0] / math.hypot(*direction),
                                    direction[1] / math.hypot(*direction)))

    def draw_sprite(self, display):
        for i in range(len(self.points) - 1):
            pygame.draw.line(display, PATH_COLOR, self.points[i], self.points[i + 1], 10)
