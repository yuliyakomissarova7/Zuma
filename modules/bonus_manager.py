import datetime
import random

from modules.bonuses.bonuses import Bonuses


class BonusManager:
    def __init__(self, ball_generator):
        self.ball_generator = ball_generator
        self.start_time_pause = None
        self.start_time_game = datetime.datetime.now()
        self.balls_with_bonuses = []

    def start(self, ball_bonus):
        if ball_bonus is Bonuses.Pause:
            self.pause_bonus()

    def pause_bonus(self):
        self.start_time_pause = datetime.datetime.now()
        self.ball_generator.pause = True

    def end_pause_bonus(self):
        self.start_time_pause = None
        self.ball_generator.pause = False

    def time_pause_for_ball(self):
        if self.start_time_pause is not None:
            if (datetime.datetime.now() - self.start_time_pause).seconds == 5:
                self.end_pause_bonus()

    def time_generate_bonus(self):
        cur_time = datetime.datetime.now()
        if (cur_time - self.start_time_game).seconds == 10:
            ball_with_bonus = random.choice(self.ball_generator.balls)
            ball_with_bonus.set_bonus(Bonuses.Pause)
            self.balls_with_bonuses.append((ball_with_bonus, cur_time))
            self.start_time_game = cur_time

    def time_remove_bonus_from_ball(self):
        for ball, time in self.balls_with_bonuses:
            if (datetime.datetime.now() - time).seconds == 15:
                ball.set_bonus(None)

    def update(self):
        self.time_pause_for_ball()
        self.time_remove_bonus_from_ball()
        self.time_generate_bonus()
