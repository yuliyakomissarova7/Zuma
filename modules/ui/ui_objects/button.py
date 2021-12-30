import pygame

from modules.colors import *
from modules.parameters import *


class Button:
    def __init__(self, text='', position=DISPLAY_CENTER, background=BLACK, text_color=WHITE, width=160, height=80):
        self.text, self.width, self.height = text, width, height
        self.text = text
        self.font = pygame.font.Font(FONT, FONT_SIZE)
        self.title_width, self.title_height = self.font.size(self.text)
        self.background = background
        self.text_color = text_color
        self.center = (position[0], position[1])
        self.x_start, self.y_start = self.center[0] - self.width // 2, self.center[1] - self.height // 2
        self.rect = pygame.Rect((self.x_start, self.y_start, width, height))
