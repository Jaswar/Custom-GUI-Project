# Loading the libraries
import pygame as pg
import os

# Loading the icons
from objects.form import Form
from objects.textbox import Textbox
from objects.button import Button
from objects.label import Label
from objects.canvas import Canvas

# Loading tools
from tools.specification_viewer import SpecificationViewer
from tools.listener import Listener
from tools.toolbar import Toolbar
from tools.memory import Memory
from tools.exception_handler import ExceptionHandler


class FormLoader(object):

    def __init__(self, save_filepath, screen=None):
        pg.init()
        self.save_filepath = save_filepath
        self.screen = screen
        self.listener = Listener()
        self.exception_handler = ExceptionHandler(self.screen)
        self.form = None
        self.objects = {}
        self.item_selected = None

    def draw(self):
        self.screen.fill((0, 0, 0))
        if self.form is not None:
            self.form.draw()
        pg.display.flip()

    def detect_object(self, x, y):
        for obj in self.form.objects:
            if obj.abs_x <= x <= obj.abs_x + obj.width and obj.abs_y <= y <= obj.abs_y + obj.height:
                return obj
        if self.form.x <= x <= self.form.x + self.form.width and self.form.y <= y <= self.form.y + self.form.height:
            return self.form
        return None

    def update(self):
        self.draw()
        event = self.listener.listen()
        x, y = pg.mouse.get_pos()
        if event == 'quit':
            pg.quit()
        elif event == 'mouse_button_left_down':
            object_detected = self.detect_object(x, y)
            if object_detected is None:
                self.item_selected.is_selected = False
                self.item_selected = None
            else:
                if self.item_selected is not None:
                    self.item_selected.is_selected = False
                self.item_selected = object_detected
        elif event == 'backspace_down':
            if self.item_selected is not None and self.item_selected.type == 'Textbox' and len(
                    self.item_selected.text) > 0:
                if self.item_selected.enabled:
                    self.item_selected.text = self.item_selected.text[:-1]
        elif event == 'enter_down':
            if self.item_selected is not None and self.item_selected.type == 'Textbox' and len(
                    self.item_selected.text) < self.item_selected.max_len:
                if self.item_selected.enabled:
                    self.item_selected.text += '\n'
        elif event == 'space_down':
            if self.item_selected is not None and self.item_selected.type == 'Textbox' and len(
                    self.item_selected.text) < self.item_selected.max_len:
                if self.item_selected.enabled:
                    self.item_selected.text += ' '
        elif event is not None and len(event) == 6 and event[-4:] == 'down':
            if self.item_selected is not None and self.item_selected.type == 'Textbox' and len(
                    self.item_selected.text) < self.item_selected.max_len:
                if self.item_selected.enabled:
                    self.item_selected.text += event[0]

        if self.item_selected is not None:
            self.item_selected.is_selected = True
            if event is not None:
                return self.item_selected.call_event(event)

    def load(self):
        data_separator = '##END DATA##'
        savefile = open(self.save_filepath, 'r').read().splitlines()
        loaded_objects = []
        cur_object = {}
        for line in savefile:
            if line == data_separator:
                loaded_objects.append(cur_object)
                cur_object = {}
            else:
                key, value = line.split(':')
                if key == 'text':
                    value = value.replace('#', '\n')
                cur_object[key] = value
        for object_data in loaded_objects:
            if object_data['type'] == 'Form':
                x, y = int(object_data['x']), int(object_data['y'])
                os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
                if self.screen is None:
                    self.screen = pg.display.set_mode((int(object_data['width']), int(object_data['height'])))
                    self.exception_handler.screen = self.screen
                    self.form = Form(self.screen, 0, 0, self.exception_handler)
                    object_data['x'] = object_data['y'] = 0
                else:
                    self.form = Form(self.screen, int(object_data['x']), int(object_data['y']), self.exception_handler)
                self.form.updated.update(object_data)
                self.form.convert_variables()
                self.objects[object_data['name']] = self.form
            elif object_data['type'] == 'Button':
                x, y = int(object_data['x']), int(object_data['y'])
                button = Button(self.form, x, y, self.exception_handler)
                button.updated.update(object_data)
                button.convert_variables()
                self.form.objects.append(button)
                self.objects[object_data['name']] = button
            elif object_data['type'] == 'Textbox':
                x, y = int(object_data['x']), int(object_data['y'])
                textbox = Textbox(self.form, x, y, self.exception_handler)
                textbox.updated.update(object_data)
                textbox.convert_variables()
                self.form.objects.append(textbox)
                self.objects[object_data['name']] = textbox
            elif object_data['type'] == 'Label':
                x, y = int(object_data['x']), int(object_data['y'])
                label = Label(self.form, x, y, self.exception_handler)
                label.updated.update(object_data)
                label.convert_variables()
                self.form.objects.append(label)
                self.objects[object_data['name']] = label
            elif object_data['type'] == 'Canvas':
                x, y = int(object_data['x']), int(object_data['y'])
                canvas = Canvas(self.form, x, y, self.exception_handler)
                canvas.updated.update(object_data)
                canvas.convert_variables()
                self.form.objects.append(canvas)
                self.objects[object_data['name']] = canvas
        print('Form Loaded')