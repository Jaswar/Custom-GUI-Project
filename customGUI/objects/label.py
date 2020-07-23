import pygame as pg
from .utils import init_events, check_name_eligibility, str_to_tuple, find_font
from .base_icon import BaseIcon

class Label(BaseIcon):

    defaults = {'type' : 'Label',
                'name' : None,
                'width' : 100,
                'height' : 30,
                'x' : None,
                'y' : None,
                'text' : 'Label',
                'font_type' : 'arial',
                'font_size' : 20,
                'font_color' : [0, 0, 0],
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

    def draw(self):
        self.font = pg.font.SysFont(self.font_type, self.font_size)
        main_text = self.font.render(self.text, False, self.font_color)
        if self.visible:
            self.form.surface.blit(main_text, (self.x, self.y))
        w, h = main_text.get_rect().width, main_text.get_rect().height
        if self.is_selected:
            pg.draw.rect(self.form.surface, (255, 0, 0), (self.x, self.y, w, h), 1)
        self.abs_x = self.x + self.form.x
        self.abs_y = self.y + self.form.y
        self.width = w
        self.height = h

    def copy(self):
        copied = Label(self.form, self.x, self.y, self.exception_handler)
        for key in self.updated:
            copied.__dict__[key] = self.__dict__[key]
        return copied