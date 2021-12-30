import random

from modules.colors import *
from modules.parameters import *
from modules.sprite_manager.ball import Ball


class BallGenerator:
    def __init__(self, number_of_balls, path, score_manager):
        self.score_manager = score_manager
        self.colors = [BLUE, GREEN, RED, YELLOW]
        self.number_of_balls = number_of_balls
        self.path = path
        self.balls = []
        self.need_generate = number_of_balls
        self.generated = 0
        self.reverse = False

    def generate_balls(self):
        if self.generated < self.need_generate and (len(self.balls) == 0 or
                                                    self.balls[0].path_position >= BALL_DIAMETER // 2):
            self.generated += 1
            self.balls.insert(0, Ball(random.choice(self.colors), self.path, 0))

    def update_chain(self):
        for i in range(1, len(self.balls)):
            right_ball, left_ball = self.balls[i], self.balls[i - 1]
            if right_ball.path_position - left_ball.path_position > 20:
                if right_ball.color == left_ball.color:
                    self.join_balls(i - 1)
                else:
                    self.stop_balls(i)

    def join_balls(self, index):
        for i in range(index, len(self.balls)):
            self.balls[i].set_position(self.balls[i - 1].path_position + BALL_DIAMETER // self.path.step)

    def stop_balls(self, index):
        for i in range(index, len(self.balls)):
            self.balls[i].can_move = False

    def update_balls(self):
        for i in range(len(self.balls)):
            self.balls[i].update()
            if not self.balls[i].can_move:
                if i == 0:
                    self.balls[i].can_move = True

                elif self.balls[i - 1].can_move and \
                        self.balls[i - 1].rect.colliderect(self.balls[i].rect):
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
        return [ball.color for ball in self.balls]

    def update(self):
        self.update_chain()
        self.update_balls()
        if len(self.balls) == 0 and self.generated == self.need_generate:
            self.score_manager.game_win()

    def destroy(self, chain):
        for ball in chain:
            self.balls.remove(ball)

    def draw_sprite(self, screen):
        for ball in self.balls:
            ball.draw_sprite(screen)
