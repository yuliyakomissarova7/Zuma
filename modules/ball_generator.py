import random

from modules.bonuses.bonuses import Bonuses
from modules.colors import *
from modules.parameters import *
from modules.sprite_manager.ball import Ball
from modules.bonus_manager import BonusManager


class BallGenerator:
    def __init__(self, number_of_balls, path, score_manager):
        self.score_manager = score_manager
        self.colors = [BLUE, GREEN, RED, YELLOW]
        self.number_of_balls = number_of_balls
        self.bonus_manager = BonusManager(self)
        self.path = path
        self.balls = []
        self.need_generate = number_of_balls
        self.generated = 0
        self.pause = False

    def generate_balls(self):
        if self.generated < self.need_generate and (len(self.balls) == 0 or
                                                    self.balls[0].path_position >= BALL_DIAMETER // 2):
            self.generated += 1
            self.balls.insert(0, Ball(random.choice(self.colors), self.path, 0))

    def update_chain(self):
        for i in range(1, len(self.balls)):
            right_ball = self.balls[i]
            left_ball = self.balls[i - 1]
            if right_ball.path_position - left_ball.path_position > 20:
                self.dont_move_balls(i)
                if right_ball.color == left_ball.color and right_ball.path_position - left_ball.path_position == 21:
                    chain_of_ball = self.find_chain(left_ball, left_ball.color)
                    self.check_same_color_balls(chain_of_ball)
                    for ball in chain_of_ball:
                        if ball.bonus is Bonuses.Pause:
                            self.bonus_manager.start(ball.bonus)
                    break

    def check_same_color_balls(self, chain_of_ball):
        if len(chain_of_ball) >= 3:
            self.score_manager.add_score(20 * len(chain_of_ball))
            self.destroy(chain_of_ball)

    def find_chain(self, ball, color):
        index = self.balls.index(ball)
        left_half = self.find_half_of_chain(index, -1, color)
        right_half = self.find_half_of_chain(index + 1, 1, color)
        return left_half + right_half

    def find_half_of_chain(self, i, delta, color):
        half_chain = []
        while len(self.balls) > i >= 0 and \
                self.balls[i].color == color:
            half_chain.append(self.balls[i])
            i += delta
        return half_chain

    def dont_move_balls(self, index):
        for i in range(index, len(self.balls)):
            self.balls[i].can_move = False

    def update_balls(self):
        for i in range(len(self.balls)):
            self.balls[i].update()
            if not self.balls[i].can_move:
                if i == 0:
                    self.balls[i].can_move = True

                elif self.balls[i - 1].can_move and self.balls[i - 1].rect.colliderect(self.balls[i].rect):
                    self.balls[i].can_move = True

    def insert(self, index, shooting_ball):
        ball = self.convert_shooting_ball(index, shooting_ball)
        self.balls.insert(index + 1, ball)
        for i in range(index + 2, len(self.balls)):
            if self.balls[i].path_position - self.balls[i - 1].path_position >= \
                    BALL_DIAMETER // 2:
                break
            self.balls[i].set_position(self.balls[i - 1].path_position + BALL_DIAMETER // self.path.step)

    def convert_shooting_ball(self, index, shooting_ball):
        ball = Ball(shooting_ball.color, self.path,
                    self.balls[index].path_position + BALL_DIAMETER // self.path.step)
        ball.can_move = self.balls[index].can_move
        return ball

    def which_ball_colors_available(self):
        available_colors = []
        for ball in self.balls:
            if ball.color not in available_colors:
                available_colors.insert(0, ball.color)
        return available_colors

    def update(self):
        self.update_chain()
        self.bonus_manager.update()
        if not self.pause:
            self.update_balls()
        if len(self.balls) == 0 and self.generated == self.need_generate:
            self.score_manager.game_win()

    def destroy(self, chain):
        for ball in chain:
            self.balls.remove(ball)

    def draw_sprite(self, screen):
        for ball in self.balls:
            ball.draw_sprite(screen)
