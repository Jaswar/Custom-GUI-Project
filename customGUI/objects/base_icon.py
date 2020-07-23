import pygame as pg
from .utils import init_events, check_name_eligibility, str_to_tuple, find_font

class BaseIcon(object):

    defaults = {'type': None,
                'name': None,
                'width': None,
                'height': None,
                'x': None,
                'y': None}

    updated = defaults.copy()

    def __init__(self, exception_handler):
        self.__dict__.update(self.defaults)
        self.events = init_events()
        self.exception_handler = exception_handler
        self.is_selected = False
        self.times_copied = 0

    def add_event(self, event, callback):
        if event not in self.events:
            raise Exception(f'{event} is not a correct event')
        else:
            self.events[event] = callback

    def call_event(self, event):
        if self.events[event] is not None:
            return self.events[event]()

    def update_dictionary(self):
        for key in self.updated:
            self.updated[key] = self.__dict__[key]

    def convert_variables(self):
        error = False
        if self.updated['width'] == '':
            self.updated['width'] = '0'
        if self.updated['height'] == '':
            self.updated['height'] = '0'
        if self.updated['x'] == '':
            self.updated['x'] = '0'
        if self.updated['y'] == '':
            self.updated['y'] = '0'

        if self.updated['type'] != self.type:
            error = True
            self.exception_handler.message = 'Changing the type of an icon is impossible.'

        try:
            if self.type != 'Form':
                self.name = check_name_eligibility(self.updated['name'], self.form)
                self.name = self.updated['name']
            else:
                self.name = check_name_eligibility(self.updated['name'], self)
                self.name = self.updated['name']
        except:
            if self.name != self.updated['name']:
                error = True
                self.exception_handler.message = 'The following name: {} already exists in the project.'.format(self.updated['name'])
        try:
            self.width = int(self.updated['width'])
            self.width = max(0, self.width)
        except:
            error = True
            self.exception_handler.message = 'Width must be a positive integer.'
        try:
            self.height = int(self.updated['height'])
            self.height = max(0, self.height)
        except:
            error = True
            self.exception_handler.message = 'Height must be a positive integer.'
        try:
            self.x = int(self.updated['x'])
            self.x = max(0, self.x)
        except:
            error = True
            self.exception_handler.message = 'x coordinate must be a positive integer.'
        try:
            self.y = int(self.updated['y'])
            self.y = max(0, self.y)
        except:
            error = True
            self.exception_handler.message = 'y coordinate must be a positive integer.'
        if 'max_len' in self.updated:
            try:
                self.max_len = int(self.updated['max_len'])
            except:
                error = True
                self.exception_handler.message = 'The maximum text length must be a positive integer.'
        if 'text' in self.updated:
            try:
                if len(self.updated['text']) <= self.max_len:
                    self.text = self.updated['text']
                else:
                    self.text = self.updated['text'][:self.max_len]
            except:
                error = True
                self.exception_handler.message = 'Failed to update text.'
        if 'text_align' in self.updated:
            try:
                if self.updated['text_align'] in ['left-top', 'middle-top', 'right-top',
                                                  'left-middle', 'middle', 'right-middle',
                                                  'left-down', 'middle-down', 'right-down']:
                    self.text_align = self.updated['text_align']
                else:
                    raise Exception
            except:
                error = True
                self.exception_handler.message = 'This text align is not supported. The following is a list of all text-aligns:\n' \
                                                 'left-top, middle-top, right-top\n' \
                                                 'left-middle, middle, right-middle\n' \
                                                 'left-down, middle-down, right-down'
        if 'bg_color' in self.updated:
            try:
                self.bg_color = str_to_tuple(self.updated['bg_color'])
            except:
                error = True
                self.exception_handler.message = 'This is not a correct color value. Color should be input with the following scheme: [R, G, B] where:\n' \
                                                 'R is an integer from 0 to 255 signifying color red,\n' \
                                                 'G is an integer from 0 to 255 signifying color green,\n' \
                                                 'B is an integer from 0 to 255 signifying color blue.'
        if 'font_type' in self.updated:
            try:
                self.font_type = find_font(self.updated['font_type'])
            except:
                error = True
                self.exception_handler.message = '{} is not an existing pygame font. Run pygame.font.get_fonts() to see available fonts.'.format(self.updated['font_type'])
        if 'font_size' in self.updated:
            try:
                self.font_size = int(self.updated['font_size'])
                self.font_size = max(0, self.font_size)
            except:
                error = True
                self.exception_handler.message = 'Font size must be a positive integer.'
        if 'font_color' in self.updated:
            try:
                self.font_color = str_to_tuple(self.updated['font_color'])
            except:
                error = True
                self.exception_handler.message = 'This is not a correct color value. Color should be input with the following scheme: [R, G, B] where:\n' \
                                                 'R is an integer from 0 to 255 signifying color red,\n' \
                                                 'G is an integer from 0 to 255 signifying color green,\n' \
                                                 'B is an integer from 0 to 255 signifying color blue.'
        if 'enabled' in self.updated:
            try:
                if self.updated['enabled'] in [True, 'true', 'True', '1']:
                    self.enabled = True
                elif self.updated['enabled'] in [False, 'false', 'False', '0']:
                    self.enabled = False
                else:
                    raise Exception
            except:
                error = True
                self.exception_handler.message = 'This is an incorrect boolean type. In order to set a boolean variable, type:\n' \
                                                 'For True: True, true or 1,\n' \
                                                 'For False: False, false or 0.'
        if 'visible' in self.updated:
            try:
                if self.updated['visible'] in [True, 'true', 'True', '1']:
                    self.visible = True
                elif self.updated['visible'] in [False, 'false', 'False', '0']:
                    self.visible = False
                else:
                    raise Exception
            except:
                error = True
                self.exception_handler.message = 'This is an incorrect boolean type. In order to set a boolean variable, type:\n' \
                                                 'For True: True, true or 1,\n' \
                                                 'For False: False, false or 0.'
        return error


