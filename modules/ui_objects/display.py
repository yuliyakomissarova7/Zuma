from modules.parameters import *
from modules.colors import *


class Display:
    def __init__(self, background=BACKGROUND_COLOR, buttons=None, images=None, inscriptions=None):
        self.background = background
        self.buttons = buttons if buttons is not None else []
        self.images = images if images is not None else []
        self.inscriptions = inscriptions if inscriptions is not None else []
