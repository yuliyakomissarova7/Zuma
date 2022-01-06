import pygame

from modules.parameters import *
from modules.colors import *


class Inscription:
    def __init__(self, text, position, color=BLACK, font_size=FONT_SIZE):
        self.color = color
        self.font = pygame.font.Font(FONT, font_size)
        self.text = self.font.render(text, True, color)
        self.width, self.height = self.font.size(text)
        self.x_start, self.y_start = position[0] - self.width // 2, position[1] - self.height // 2
