import pygame

from modules.colors import *
from modules.parameters import *


class Skull(pygame.sprite.Sprite):
    def __init__(self, path, balls, score_manager):
        pygame.sprite.Sprite.__init__(self)
        self.skull = pygame.transform.smoothscale(pygame.image.load(SKULL), (80, 80))
        self.score_manager = score_manager
        self.skull.set_colorkey(BLACK)
        self.balls = balls
        self.rect = self.skull.get_rect(center=path.points[-1])

    def update(self):
        for ball in self.balls:
            if self.rect.colliderect(ball.rect):
                self.score_manager.game_lose()

    def draw_sprite(self, display):
        display.blit(self.skull, (self.rect.x, self.rect.y))
