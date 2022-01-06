import datetime

import pygame

from modules.parameters import *
from modules.level import Level
from modules.score_manager import ScoreManager


class Zuma:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("ZUMA")
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.display_center = (self.display.get_width() / 2, self.display.get_height() / 2)
        self.level_num = 1
        self.score_manager = ScoreManager()
        self.level = Level(self.level_num, self.display, self.score_manager)
        self.is_quit = False
        self.clock = pygame.time.Clock()
        self.FPS = 60

    def start(self):
        while not self.is_quit:
            self.level = Level(self.level_num, self.display, self.score_manager)
            self.start_zuma()

    def start_zuma(self):
        is_game_finish = False

        while not is_game_finish and not self.is_quit:
            self.level.ball_generator.generate_balls()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_quit = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.level.shooting_manager.shoot(pygame.mouse.get_pos())
            self.update_level()
            self.update_display(self.level.level_display)
            self.clock.tick(self.FPS)
            if self.score_manager.is_lose_game:
                is_game_finish = True
                self.handle_lose()
            elif self.score_manager.is_win_game:
                is_game_finish = True
                self.handle_win()

    def update_level(self):
        self.level.frog.update()
        self.level.shooting_manager.update()
        self.level.ball_generator.update()
        self.level.bonus_manager.update()
        self.level.skull.update()
        self.level.cheats.update()
        self.check_slowing_cheat()

    def check_slowing_cheat(self):
        if self.level.cheats.slowing is True:
            self.FPS = 20
            if (datetime.datetime.now() - self.level.cheats.start_time).seconds == 5:
                self.FPS = 60
                self.level.cheats.slowing = False

    def handle_win(self):
        if self.level_num != 2:
            self.continue_game(self.level.continue_btn,
                               self.level.win_level_display)
            self.level_num += 1
            self.score_manager.setup_next_level()
        else:
            self.win_game()

    def win_game(self):
        on_win_window = True
        while on_win_window and not self.is_quit:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_quit = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.level.start_game_again_btn.rect.collidepoint(mouse):
                        self.is_quit = True

            self.update_display(self.level.win_game_display)

    def handle_lose(self):
        self.score_manager.take_live()
        if self.score_manager.is_lose_game:
            self.continue_game(self.level.new_game_button,
                               self.level.lose_game_display)
            self.level_num = 1
            self.score_manager = ScoreManager(self.score_manager.count_of_lives)
        else:
            self.continue_game(self.level.start_level_again_btn,
                               self.level.lose_level_display)
            self.score_manager.setup_next_level()

    def continue_game(self, button, window):
        game_continued = False
        while not game_continued and not self.is_quit:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_quit = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button.rect.collidepoint(mouse):
                        game_continued = True
            self.update_display(window)

    def update_display(self, display):
        self.level.draw_level_display(display)
        if display is self.level.level_display:
            self.level.show_lives(self.score_manager.count_of_lives)
            self.level.show_score(self.score_manager.score)
        pygame.display.update()


if __name__ == '__main__':
    zuma = Zuma()
    zuma.start()
