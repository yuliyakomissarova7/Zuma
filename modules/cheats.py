import datetime
import pygame


class Cheats:
    def __init__(self, bonus_manager, score_manager):
        self.bonus_manager = bonus_manager
        self.score_manager = score_manager
        self.start_time = None
        self.slowing = False

    def pause_bonus_activate(self):
        keyboard_dictionary = pygame.key.get_pressed()
        if keyboard_dictionary[pygame.K_LCTRL] and keyboard_dictionary[pygame.K_LSHIFT] and \
                keyboard_dictionary[pygame.K_p]:
            self.bonus_manager.pause_bonus()

    def moving_to_the_next_level(self):
        keyboard_dictionary = pygame.key.get_pressed()
        if keyboard_dictionary[pygame.K_LCTRL] and keyboard_dictionary[pygame.K_LSHIFT] and \
                keyboard_dictionary[pygame.K_l]:
            self.score_manager.is_win_game = True

    def add_live(self):
        keyboard_dictionary = pygame.key.get_pressed()
        if keyboard_dictionary[pygame.K_LCTRL] and keyboard_dictionary[pygame.K_LSHIFT] and \
                keyboard_dictionary[pygame.K_a]:
            if self.score_manager.count_of_lives < 3:
                self.score_manager.count_of_lives = 3

    def slowing_down_balls(self):
        keyboard_dictionary = pygame.key.get_pressed()
        if keyboard_dictionary[pygame.K_LCTRL] and keyboard_dictionary[pygame.K_LSHIFT] and \
                keyboard_dictionary[pygame.K_s]:
            self.start_time = datetime.datetime.now()
            self.slowing = True

    def update(self):
        self.pause_bonus_activate()
        self.moving_to_the_next_level()
        self.add_live()
        self.slowing_down_balls()
