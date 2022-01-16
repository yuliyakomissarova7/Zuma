import random

from modules.parameters import *
from modules.sprite_manager.ball_for_shoot import ShootBall


class ShootManager:
    def __init__(self, ball_generator, position, score_manager, bonus_manager):
        self.ball_generator = ball_generator
        self.score_manager = score_manager
        self.position = position
        self.charged_ball = ShootBall(random.choice(self.ball_generator.colors), self.position)
        self.bonus_manager = bonus_manager
        self.shooting_balls = []
        self.combo_chain = []
        self.speed = 15

    def shoot(self, target):
        shooting_ball = self.charged_ball
        shooting_ball.set_points(target)
        self.shooting_balls.append(shooting_ball)
        self.charged_ball = ShootBall(random.choice(self.ball_generator.which_ball_colors_available()),
                                      self.position)

    def draw_sprite(self, screen):
        self.charged_ball.draw_sprite(screen)
        for ball in self.shooting_balls:
            ball.draw_sprite(screen)

    def update(self):
        self.charged_ball.update()
        for ball in self.shooting_balls:
            ball.update()
            self.remove_flown_away(ball)
            self.handle_shoot(ball)

    def remove_flown_away(self, ball):
        x, y = ball.rect.center[0], ball.rect.center[1]
        if x < 0 or x > WIDTH or y < 0 or y > HEIGHT:
            self.shooting_balls.remove(ball)

    def handle_shoot(self, shooting_ball):
        for ball in self.ball_generator.balls:
            if shooting_ball.rect.colliderect(ball.rect):
                chain = self.find_chain(ball, shooting_ball.color)
                if len(chain) >= 2:
                    self.ball_generator.check_for_bonus(chain)
                    self.score_manager.add_score(20 * len(chain))
                    self.ball_generator.destroy(chain)
                    if self.charged_ball.color not in self.ball_generator.which_ball_colors_available() and \
                            len(self.ball_generator.balls) != 0:
                        self.charged_ball = ShootBall(random.choice(self.ball_generator.which_ball_colors_available()),
                                                      self.position)
                else:
                    ball_index = self.ball_generator.balls.index(ball)
                    self.ball_generator.insert(ball_index, shooting_ball)
                self.shooting_balls.remove(shooting_ball)
                break

    def find_chain(self, ball, color):
        ball_index = self.ball_generator.balls.index(ball)
        ball_color = ball.color

        left_half = self.ball_generator.find_half_of_chain(ball_index - 1, -1, color)
        right_half = self.ball_generator.find_half_of_chain(ball_index + 1, 1, color)

        if ball_color == color:
            chain = left_half + [self.ball_generator.balls[ball_index]] + right_half
            return chain

        return right_half
