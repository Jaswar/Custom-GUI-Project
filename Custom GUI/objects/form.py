import pygame as pg
from utils import init_events, check_name_eligibility, str_to_tuple, find_font
from base_icon import BaseIcon

class Form(BaseIcon):

    defaults = {'type' : 'Form',
                 'name' : None,
                 'width' : 700,
                 'height' : 700,
                 'x' : None,
                 'y' : None,
                 'bg_color' : [211, 211, 211]}

    updated = defaults.copy()

    def __init__(self, screen, x, y, exception_handler):
        super().__init__(exception_handler)
        self.__dict__.update(self.defaults)
        self.screen = screen
        self.x = x
        self.y = y
        self.updated['x'], self.updated['y'] = x, y
        self.objects = []
        self.events = init_events()


    def draw(self):
        self.surface = pg.Surface((self.width, self.height))
        if self.is_selected:
            self.surface.fill((255, 0, 0))
        else:
            self.surface.fill((0, 0, 0))
        pg.draw.rect(self.surface, self.bg_color, (2, 2, self.width-4, self.height-4))
        self.draw_objects()
        self.screen.blit(self.surface, (self.x, self.y))

    def draw_objects(self):
        for object in self.objects:
            object.draw()

    def copy(self):
        copied = Form(self.screen, self.x, self.y, self.exception_handler)
        for key in self.updated:
            copied.__dict__[key] = self.__dict__[key]
        if self.is_selected:
            copied.is_selected = True
        for obj in self.objects:
            new_obj = obj.copy()
            if obj.is_selected:
                new_obj.is_selected = True
            new_obj.form = copied
            copied.objects.append(new_obj)
        return copied
