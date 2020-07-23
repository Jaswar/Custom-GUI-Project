import pygame as pg
from .utils import init_events, check_name_eligibility, str_to_tuple, find_font
from .base_icon import BaseIcon

class Textbox(BaseIcon):

    defaults = {'type' : 'Textbox',
                 'name' : None,
                 'width' : 100,
                 'height' : 30,
                 'x' : None,
                 'y' : None,
                 'text' : 'Textbox',
                 'text_align' : 'left-top',
                 'max_len' : 10,
                 'bg_color' : [255, 255, 255],
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
        self.conv_text = self.text.split('\n')
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
        text_to_blit = []
        for line in self.conv_text:
            main_text = self.font.render(line, False, self.font_color)
            w, h = main_text.get_rect().width, main_text.get_rect().height
            text_to_blit.append(main_text)
            tot_h += h

        if self.text_align == 'left-top':
            cur_h = 0
            for line in text_to_blit:
                h = line.get_rect().height
                surface.blit(line, (5, cur_h))
                cur_h += h
        elif self.text_align == 'middle-top':
            cur_h = 0
            for line in text_to_blit:
                w, h = line.get_rect().width, line.get_rect().height
                surface.blit(line, (self.width//2 - w//2, cur_h))
                cur_h += h
        elif self.text_align == 'right-top':
            cur_h = 0
            for line in text_to_blit:
                w, h = line.get_rect().width, line.get_rect().height
                surface.blit(line, (self.width - 5 - w, cur_h))
                cur_h += h
        elif self.text_align == 'left-middle':
            cur_h = 0
            for line in text_to_blit:
                h = line.get_rect().height
                surface.blit(line, (5, self.height//2 - tot_h//2 + cur_h))
                cur_h += h
        elif self.text_align == 'middle':
            cur_h = 0
            for line in text_to_blit:
                w, h = line.get_rect().width, line.get_rect().height
                surface.blit(line, (self.width//2 - w//2, self.height//2 - tot_h//2 + cur_h))
                cur_h += h
        elif self.text_align == 'right-middle':
            cur_h = 0
            for line in text_to_blit:
                w, h = line.get_rect().width, line.get_rect().height
                surface.blit(line, (self.width - w - 5, self.height//2 - tot_h//2 + cur_h))
                cur_h += h
        elif self.text_align == 'left-down':
            cur_h = 0
            for line in text_to_blit:
                h = line.get_rect().height
                surface.blit(line, (5, self.height - tot_h + cur_h))
                cur_h += h
        elif self.text_align == 'middle-down':
            cur_h = 0
            for line in text_to_blit:
                w, h = line.get_rect().width, line.get_rect().height
                surface.blit(line, (self.width//2 - w//2, self.height - tot_h + cur_h))
                cur_h += h
        elif self.text_align == 'right-down':
            cur_h = 0
            for line in text_to_blit:
                w, h = line.get_rect().width, line.get_rect().height
                surface.blit(line, (self.width - w - 5, self.height - tot_h + cur_h))
                cur_h += h

        if self.visible:
            self.form.surface.blit(surface, (self.x, self.y))
        self.abs_x = self.x + self.form.x
        self.abs_y = self.y + self.form.y

    def copy(self):
        copied = Textbox(self.form, self.x, self.y, self.exception_handler)
        for key in self.updated:
            copied.__dict__[key] = self.__dict__[key]
        return copied