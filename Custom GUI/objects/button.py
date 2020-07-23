import pygame as pg
from utils import init_events, check_name_eligibility, str_to_tuple, find_font
from base_icon import BaseIcon

class Button(BaseIcon):

    defaults = {'type' : 'Button',
                'name' : None,
                'width' : 100,
                'height' : 30,
                'x' : None,
                'y' : None,
                'text' : 'Button',
                'max_len' : 10,
                'bg_color' : [169, 169, 169],
                'font_type' : 'arial',
                'font_size' : 24,
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
        self.conv_text = self.text.split('\n')
        surface = pg.Surface((self.width, self.height))
        if self.is_selected:
            surface.fill((255, 0, 0))
        else:
            surface.fill((0, 0, 0))
        pg.draw.rect(surface, self.bg_color, (1, 1, self.width - 2, self.height - 2))
        tot_h = 0
        for line in self.conv_text:
            main_text = self.font.render(line, False, self.font_color)
            w, h = main_text.get_rect().width, main_text.get_rect().height
            surface.blit(main_text, (self.width // 2 - w//2, tot_h))
            tot_h += h
        if self.visible:
            self.form.surface.blit(surface, (self.x, self.y))
        self.abs_x = self.x + self.form.x
        self.abs_y = self.y + self.form.y

    def copy(self):
        copied = Button(self.form, self.x, self.y, self.exception_handler)
        for key in self.updated:
            copied.__dict__[key] = self.__dict__[key]
        return copied