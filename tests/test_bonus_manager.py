from modules.ball_generator import BallGenerator
from modules.path_generator import PathGenerator
from modules.score_manager import ScoreManager
from modules.bonus_manager import BonusManager
from modules.sprite_manager.ball import Ball
from modules.bonuses.bonuses import Bonuses
from modules.colors import *


class TestBonusManager:
    def setup_class(self):
        self.score_manager = ScoreManager()
        self.path = PathGenerator(1)
        self.ball_generator = BallGenerator(4, self.path, self.score_manager)
        self.colors = [RED, RED, GREEN, YELLOW]
        self.bonus_manager = BonusManager(self.ball_generator)

    def setup_method(self):
        for color in self.colors:
            self.ball_generator.balls.insert(0, Ball(color, self.path, 0))

    def test_start_pause_bonus(self):
        self.ball_generator.balls[2].bonus = Bonuses.Pause
        self.bonus_manager.start(self.ball_generator.balls[2].bonus)
        assert self.ball_generator.pause is True

    def test_end_pause_bonus(self):
        self.bonus_manager.end_pause_bonus()
        assert self.ball_generator.pause is False
