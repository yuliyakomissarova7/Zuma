

class ScoreManager:
    def __init__(self, count_of_lives=3):
        self.count_of_lives = count_of_lives
        self.score = 0
        self.is_win_game, self.is_lose_game = False, False

    def game_lose(self):
        self.is_lose_game = True

    def game_win(self):
        self.is_win_game = True

    def check_is_game_lose(self):
        if self.count_of_lives == 0:
            self.is_lose_game = True

    def take_live(self):
        self.count_of_lives -= 1
        self.check_is_game_lose()

    def add_score(self, score):
        self.score += 2 * score

    def setup_next_level(self):
        self.is_win_game = False
        self.is_lose_game = False
