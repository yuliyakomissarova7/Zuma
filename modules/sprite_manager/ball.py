import pygame

from modules.parameters import *


class Ball(pygame.sprite.Sprite):
    def __init__(self, color, path, path_position):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.path = path
        self.path_position = path_position
        self.ball = pygame.Surface((BALL_DIAMETER, BALL_DIAMETER))
        self.position = self.path.ball_positions[self.path_position]
        self.rect = self.ball.get_rect(center=(round(self.position.x),
                                               round(self.position.y)))
        self.can_move = True
        self.bonus = None

    def set_bonus(self, bonus):
        self.bonus = bonus

    def update(self):
        if self.can_move:
            self.path_position += 1
            if self.path_position >= 0:
                self.position = pygame.math.Vector2(
                    self.path.ball_positions[self.path_position])
                self.rect.center = (round(self.position.x), round(self.position.y))

    def draw_sprite(self, display):
        pygame.draw.circle(display, self.color, self.rect.center, BALL_DIAMETER / 2)
        if self.bonus is not None:
            display.blit(pygame.image.load(PAUSE), (self.rect.x + 5, self.rect.y + 5))

    def set_position(self, path_position):
        self.path_position = path_position
        self.position = self.path.ball_positions[self.path_position]
        self.rect.center = (round(self.position.x), round(self.position.y))
