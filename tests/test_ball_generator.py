from modules.ball_generator import BallGenerator
from modules.path_generator import PathGenerator
from modules.score_manager import ScoreManager
from modules.sprite_manager.ball_for_shoot import ShootBall
from modules.sprite_manager.ball import Ball
from modules.colors import *


def check_moved_balls(balls, index):
    return True if ((not balls[i].can_move for i in range(0, index)) and
                    (balls[i].can_move for i in range(index, len(balls)))) else False


class TestBallGenerator:
    def setup_class(self):
        self.score_manager = ScoreManager()
        self.path = PathGenerator(1)
        self.ball_generator = BallGenerator(4, self.path, self.score_manager)
        self.colors = [RED, RED, GREEN, YELLOW]
        self.shoot_ball = ShootBall(RED)

    def setup_method(self):
        for color in self.colors:
            self.ball_generator.balls.insert(0, Ball(color, self.path, 0))

    def test_destroy_balls(self):
        self.expected_chain = [self.ball_generator.balls[2], self.ball_generator.balls[3]]
        self.ball_generator.destroy([self.ball_generator.balls[0], self.ball_generator.balls[1]])
        assert self.ball_generator.balls == self.expected_chain

    def test_insert_ball_on_level_1(self):
        self.ball_generator.insert(1, self.shoot_ball)
        actual_colors = [self.ball_generator.balls[4].color, self.ball_generator.balls[3].color,
                         self.ball_generator.balls[2].color, self.ball_generator.balls[1].color,
                         self.ball_generator.balls[0].color]
        assert actual_colors == [RED, RED, RED, GREEN, YELLOW]

    def test_which_color_are_available(self):
        actual_colors = self.ball_generator.which_ball_colors_available()
        expected_colors = [RED, GREEN, YELLOW]
        assert actual_colors == expected_colors

    def test_find_half_of_chain(self):
        self.ball_generator.insert(3, ShootBall(GREEN))
        index = self.ball_generator.balls.index(self.ball_generator.balls[4])
        right_half_of_chain = self.ball_generator.find_half_of_chain(index, -1, GREEN)
        assert right_half_of_chain == [self.ball_generator.balls[4]]

    def test_find_chain_when_exist_chain_of_3_balls(self):
        self.ball_generator.insert(2, self.shoot_ball)
        actual_chain = []
        for ball in self.ball_generator.find_chain(self.ball_generator.balls[2], RED):
            actual_chain.insert(0, ball.color)
        assert actual_chain == [RED, RED, RED]

    def test_find_chain_when_exist_chain_of_1_balls(self):
        actual_chain = []
        for ball in self.ball_generator.find_chain(self.ball_generator.balls[0], YELLOW):
            actual_chain.insert(0, ball.color)
        assert actual_chain == [YELLOW]

    def test_find_chain_when_not_exist_chain(self):
        actual_chain = []
        for ball in self.ball_generator.find_chain(self.ball_generator.balls[1], BLUE):
            actual_chain.insert(0, ball.color)
        assert actual_chain == []

    def test_find_chain_when_exist_chain_and_start_from_different_color(self):
        actual_chain = []
        for ball in self.ball_generator.find_chain(self.ball_generator.balls[3], RED):
            actual_chain.insert(0, ball.color)
        assert actual_chain == [RED, RED]

    def test_update_chain_when_dont_moved_balls(self):
        self.ball_generator.destroy([self.ball_generator.balls[1]])
        self.ball_generator.update_chain()
        assert check_moved_balls(self.ball_generator.balls, 1) is True
