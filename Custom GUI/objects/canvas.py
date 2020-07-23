import pygame as pg
from utils import init_events, check_name_eligibility, str_to_tuple, find_font
from base_icon import BaseIcon

class Canvas(BaseIcon):

    defaults = {'type' : 'Canvas',
                'name' : None,
                'width' : 200,
                'height' : 200,
                'x' : None,
                'y' : None,
                'bg_color' : [255, 255, 255],
                'enabled' : True,
                'visible' : True}

    updated = defaults.copy()

    def __init__(self, form, x, y, exception_handler):
        super().__init__(exception_handler)
        self.__dict__.update(self.defaults)
        self.form = form
        self.x = x
        self.y = y
        self.abs_x = x + self.form.x
        self.abs_y = y + self.form.y
        self.events = init_events()
        self.surface = None
        self.draw_function = None

    def draw(self):
        self.surface = pg.Surface((self.width, self.height))
        if self.is_selected:
            self.surface.fill((255, 0, 0))
        else:
            self.surface.fill((0, 0, 0))
        pg.draw.rect(self.surface, self.bg_color, (1, 1, self.width - 2, self.height - 2))
        if self.draw_function is not None:
            self.draw_function()
        self.form.surface.blit(self.surface, (self.x, self.y))
        self.abs_x = self.x + self.form.x
        self.abs_y = self.y + self.form.y

    def copy(self):
        copied = Canvas(self.form, self.x, self.y, self.exception_handler, )
        for key in self.updated:
            copied.__dict__[key] = self.__dict__[key]
        return copied

