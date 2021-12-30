import math
import pygame

from modules.colors import *
from modules.parameters import *


class Frog(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.position = DISPLAY_CENTER
        self.frog = pygame.transform.smoothscale(pygame.image.load(FROG), (130, 130))
        self.frog.set_colorkey(BLACK)
        self.image = self.frog
        self.rect = self.image.get_rect(center=self.position)
        self.angle = 0

    def update(self):
        pos_mouse = pygame.mouse.get_pos()
        self.angle = (180 / math.pi) * (-math.atan2(pos_mouse[1] - self.rect.y, pos_mouse[0] - self.rect.x)) + 90
        self.image = pygame.transform.rotate(self.frog, self.angle)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw_sprite(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))
