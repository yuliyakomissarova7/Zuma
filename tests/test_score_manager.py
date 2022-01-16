from modules.score_manager import ScoreManager
from modules.path_generator import PathGenerator
from modules.ball_generator import BallGenerator
from modules.sprite_manager.ball import Ball
from modules.sprite_manager.ball_for_shoot import ShootBall
from modules.colors import *


class TestScoreManager:
    def setup_class(self):
        self.score_manager = ScoreManager()
        self.path = PathGenerator(1)
        self.ball_generator = BallGenerator(4, self.path, self.score_manager)
        self.colors = [RED, RED]
        self.shoot_ball = ShootBall(RED)

    def setup_method(self):
        for color in self.colors:
            self.ball_generator.balls.insert(0, Ball(color, self.path, 0))
        self.ball_generator.need_generate = 2

    def test_take_lives(self):
        self.score_manager.take_live()
        assert self.score_manager.count_of_lives == 2

    def test_game_lose_when_count_of_lives_0(self):
        for i in range(3):
            self.score_manager.take_live()
        assert self.score_manager.is_lose_game is True

    def test_game_win(self):
        self.ball_generator.insert(1, self.shoot_ball)
        self.ball_generator.destroy([self.ball_generator.balls[i] for i in range(0, len(self.ball_generator.balls))])
        self.ball_generator.generated += 2
        self.ball_generator.update()
        assert self.score_manager.is_win_game is True
