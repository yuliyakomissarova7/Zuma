import pygame

from modules.bonus_manager import BonusManager
from modules.parameters import *
from modules.colors import *
from modules.path_generator import PathGenerator
from modules.shoot_manager import ShootManager
from modules.sprite_manager.frog import Frog
from modules.sprite_manager.skull import Skull
from modules.ball_generator import BallGenerator
from modules.ui_objects.display import Display
from modules.ui_objects.inscriptions import Inscription
from modules.ui_objects.button import Button
from modules.cheats import Cheats


class Level:
    def __init__(self, number, display, score_manager):
        self.path = PathGenerator(number)
        self.number = number
        self.ball_generator = BallGenerator(50, self.path, score_manager)
        self.frog = Frog()
        self.skull = Skull(self.path, self.ball_generator.balls, score_manager)
        self.display = display
        self.bonus_manager = BonusManager(self.ball_generator)
        self.cheats = Cheats(self.bonus_manager, score_manager)
        self.shooting_manager = ShootManager(self.ball_generator, self.frog.position, score_manager, self.bonus_manager)

        self.level_inscription = Inscription(f'LEVEL {number}', (100, 40), font_size=30)
        images = [self.path, self.frog, self.skull, self.ball_generator, self.shooting_manager]
        self.level_display = Display(inscriptions=[self.level_inscription], images=[image for image in images])

        self.continue_btn = Button('CONTINUE', DISPLAY_CENTER)
        self.continue_display = Display(buttons=[self.continue_btn])

        self.restart_btn = Button('RESTART', DISPLAY_CENTER,
                                  background=BLACK,
                                  text_color=WHITE)
        self.restart_display = Display(BACKGROUND_COLOR,
                                       buttons=[self.restart_btn])
        self.exit_btn = Button('EXIT', DISPLAY_CENTER)
        self.win_label = Inscription('WIN!', (WIDTH // 2, HEIGHT // 2 - 2 * 80), font_size=30)
        self.win_game_display = Display(buttons=[self.exit_btn],
                                        inscriptions=[self.win_label])

        self.new_game_button = Button('NEW GAME', DISPLAY_CENTER,
                                      background=BLACK,
                                      text_color=WHITE)
        self.new_game_display = Display(BACKGROUND_COLOR, buttons=[self.new_game_button])

    def show_score(self, points):
        points_label = Inscription(f'SCORE: {points}', (300, 40), font_size=20)
        self.put_label(points_label)

    def show_lives(self, lives):
        for i in range(lives):
            self.display.blit(pygame.transform.smoothscale(
                pygame.image.load(LIFE), (40, 40)),
                (3 * WIDTH // 4 + i * 40, 20))

    def put_label(self, label, color=BACKGROUND_COLOR):
        pygame.draw.rect(self.display, color, (label.x_start - label.width / 2,
                                               label.y_start, label.width,
                                               label.height))
        self.display.blit(label.text, (label.x_start, label.y_start))

    def draw_button(self, button):
        width, height = button.width, button.height
        x_start, y_start = button.x_start, button.y_start
        title_params = (x_start + width / 2 - button.title_width / 2,
                        y_start + height / 2 - button.title_height / 2)
        pygame.draw.rect(self.display, button.background,
                         (x_start, y_start, width, height))
        self.display.blit(button.font.render(button.text, True,
                                             button.text_color), title_params)
        button.rect = pygame.Rect((x_start, y_start, width, height))

    def draw_level_display(self, display):
        self.display.fill(BACKGROUND_COLOR)
        for inscript in display.inscriptions:
            pygame.draw.rect(self.display, BACKGROUND_COLOR, (inscript.x_start - inscript.width / 2,
                                                              inscript.y_start, inscript.width,
                                                              inscript.height))
            self.display.blit(inscript.text, (inscript.x_start, inscript.y_start))
        for sprite in display.images:
            sprite.draw_sprite(self.display)
        for button in display.buttons:
            self.draw_button(button)
