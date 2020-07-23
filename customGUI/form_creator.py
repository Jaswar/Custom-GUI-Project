# Loading the libraries
import pygame as pg
import os

# Loading the icons
from .objects.form import Form
from .objects.textbox import Textbox
from .objects.button import Button
from .objects.label import Label
from .objects.canvas import Canvas

# Loading tools
from .tools.specification_viewer import SpecificationViewer
from .tools.listener import Listener
from .tools.toolbar import Toolbar
from .tools.memory import Memory
from .tools.exception_handler import ExceptionHandler

from .form_loader import FormLoader


class FormCreator(object):

    def __init__(self, save_filepath, load_from_save=True):
        pg.init()
        self.save_filepath = save_filepath
        self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        self.listener = Listener()
        self.specification_viewer = SpecificationViewer(self.screen)
        self.exception_handler = ExceptionHandler(self.screen)
        self.memory = Memory()
        self.items = ['Form', 'Textbox', 'Button', 'Label', 'Canvas']
        self.items_count = {}
        for item in self.items:
            self.items_count[item] = 0
        self.toolbar = Toolbar(self.screen, items=self.items)
        self.form = None
        self.item_held = None
        self.prev_pos_left_down = (None, None)
        self.init_pos_right_down = (None, None)
        self.resize_action = None
        self.item_resized = None
        self.group_selected = []
        self.to_copy = None
        self.has_changed = False
        self.last_pattern_pos = (None, None)
        self.value_change = None
        if os.path.exists(self.save_filepath) and load_from_save:
            self.load()
            if self.form is not None:
                for obj in self.form.objects:
                    self.items_count[obj.type] += 1

    def detect_rect_edge(self, x, y, w, h):
        mx, my = pg.mouse.get_pos()
        tolerance = 3
        if x - tolerance <= mx <= x + tolerance and y - tolerance <= my <= y + tolerance:
            return 0
        elif x + tolerance <= mx <= x + w - tolerance and y - tolerance <= my <= y + tolerance:
            return 1
        elif x + w - tolerance <= mx <= x + w + tolerance and y - tolerance <= my <= y + tolerance:
            return 2
        elif x + w - tolerance <= mx <= x + w + tolerance and y + tolerance <= my <= y + h - tolerance:
            return 3
        elif x + w - tolerance <= mx <= x + w + tolerance and y + h - tolerance <= my <= y + h + tolerance:
            return 4
        elif x + tolerance <= mx <= x + w - tolerance and y + h - tolerance <= my <= y + h + tolerance:
            return 5
        elif x - tolerance <= mx <= x + tolerance and y + h - tolerance <= my <= y + h + tolerance:
            return 6
        elif x - tolerance <= mx <= x + tolerance and y + tolerance <= my <= y + h - tolerance:
            return 7
        return None

    def mouse_in_item(self, item, is_on_form=False):
        x, y = pg.mouse.get_pos()
        if not is_on_form and item.x <= x <= item.x + item.width and item.y <= y <= item.y + item.height:
            return True
        elif is_on_form and item.abs_x <= x <= item.abs_x + item.width and item.abs_y <= y <= item.abs_y + item.height:
            return True
        return False

    def left_mouse_down(self):
        return pg.mouse.get_pressed()[0] == 1

    def draw_objects(self):
        self.toolbar.draw()
        self.exception_handler.draw()
        if self.form is not None:
            self.form.draw()

        if len(self.group_selected) == 1:
            self.specification_viewer.draw(self.group_selected[0])
        else:
            self.specification_viewer.displayed_object = None

    def update_screen(self):
        self.screen.fill((255, 255, 255))
        self.draw_objects()
        if self.init_pos_right_down != (None, None):
            x, y = self.init_pos_right_down
            mx, my = pg.mouse.get_pos()
            pg.draw.rect(self.screen, (0, 0, 0), (x, y, mx - x, my - y), 1)
        pg.display.flip()

    def find_selected_group(self):
        if self.init_pos_right_down != (None, None):
            for obj in self.group_selected:
                obj.is_selected = False
            self.group_selected = []
            x, y = self.init_pos_right_down
            mx, my = pg.mouse.get_pos()
            if x > mx:
                x, mx = mx, x
            if y > my:
                y, my = my, y
            w, h = mx - x, my - y
            for obj in self.form.objects:
                if x <= obj.abs_x <= x + w and y <= obj.abs_y <= y + h:
                    self.group_selected.append(obj)

    def create_new_object(self, type):
        x, y = pg.mouse.get_pos()
        item_to_create = None
        if type == 'Form' and self.form is None:
            self.form = Form(self.screen, 300, 100, self.exception_handler)
            item_to_create = self.form
            self.has_changed = False
            self.form.name = type + str(self.items_count[type])
            self.items_count[type] += 1
        elif type == 'Textbox' and self.form is not None:
            textbox = Textbox(self.form, 100, 100, self.exception_handler)
            textbox.name = type + str(self.items_count[type])
            textbox.name = self.get_unique_name(textbox)
            item_to_create = textbox
            self.form.objects.append(textbox)
            self.has_changed = False
            self.items_count[type] += 1
        elif type == 'Button' and self.form is not None:
            button = Button(self.form, 100, 120, self.exception_handler)
            button.name = type + str(self.items_count[type])
            button.name = self.get_unique_name(button)
            item_to_create = button
            self.form.objects.append(button)
            self.has_changed = False
            self.items_count[type] += 1
        elif type == 'Label' and self.form is not None:
            label = Label(self.form, 100, 140, self.exception_handler)
            label.name = type + str(self.items_count[type])
            label.name = self.get_unique_name(label)
            item_to_create = label
            self.form.objects.append(label)
            self.has_changed = False
            self.items_count[type] += 1
        elif type == 'Canvas' and self.form is not None:
            canvas = Canvas(self.form, 100, 160, self.exception_handler)
            canvas.name = type + str(self.items_count[type])
            canvas.name = self.get_unique_name(canvas)
            item_to_create = canvas
            self.form.objects.append(canvas)
            self.has_changed = False
            self.items_count[type] += 1

        if item_to_create is not None:
            self.group_selected = [item_to_create]
            item_to_create.is_selected = True
            self.memory.remember(self.form.copy())
            if item_to_create.type != 'Form':
                return item_to_create

    def get_unique_name(self, item):
        unique = True
        if self.form.name == item.name:
            unique = False
        for obj in self.form.objects:
            if obj.name == item.name:
                unique = False
        if unique:
            return item.name
        else:
            max_inx = 0
            for obj in self.form.objects:
                if obj.type == item.type and len(obj.name) > len(obj.type) and obj.name[:len(obj.type)] == obj.type:
                    inx = obj.name[len(obj.type):]
                    try:
                        inx = int(inx)
                        if inx > max_inx:
                            max_inx = inx
                    except:
                        pass
            self.items_count[obj.type] = max_inx + 1
            return item.type + str(max_inx + 1)

    def copy_group(self):
        if self.form not in self.to_copy:
            for obj in self.group_selected:
                obj.is_selected = False
            self.group_selected = []
            for obj in self.to_copy:
                if obj.type != 'Form':
                    new_obj = obj.copy()
                    new_obj.x = obj.x + 10 * (obj.times_copied + 1)
                    new_obj.y = obj.y + 10 * (obj.times_copied + 1)
                    new_obj.name = new_obj.type + str(self.items_count[new_obj.type])
                    new_obj.name = self.get_unique_name(new_obj)
                    self.form.objects.append(new_obj)
                    self.group_selected.append(new_obj)
                    new_obj.is_selected = True
                    obj.times_copied += 1
                    self.items_count[new_obj.type] += 1
            self.memory.remember(self.form.copy())
            self.has_changed = False

    def resize_item(self, item):
        if self.resize_action is not None and self.left_mouse_down():
            x, y = pg.mouse.get_pos()
            prev_x, prev_y = self.prev_pos_left_down
            diffx, diffy = x - prev_x, y - prev_y
            if self.resize_action == 0 and item.width - diffx >= 0 and item.height - diffy >= 0:
                item.x += diffx
                item.y += diffy
                item.width -= diffx
                item.height -= diffy
                self.has_changed = True
            elif self.resize_action == 1 and item.height - diffy >= 0:
                item.y += diffy
                item.height -= diffy
                self.has_changed = True
            elif self.resize_action == 2 and item.height - diffy >= 0 and item.width + diffx >= 0:
                item.width += diffx
                item.y += diffy
                item.height -= diffy
                self.has_changed = True
            elif self.resize_action == 3 and item.width + diffx >= 0:
                item.width += diffx
                self.has_changed = True
            elif self.resize_action == 4 and item.width + diffx >= 0 and item.height + diffy >= 0:
                item.width += diffx
                item.height += diffy
                self.has_changed = True
            elif self.resize_action == 5 and item.height + diffy >= 0:
                item.height += diffy
                self.has_changed = True
            elif self.resize_action == 6 and item.width - diffx >= 0 and item.height + diffy >= 0:
                item.x += diffx
                item.width -= diffx
                item.height += diffy
                self.has_changed = True
            elif self.resize_action == 7 and item.width - diffx >= 0:
                item.x += diffx
                item.width -= diffx
                self.has_changed = True
            self.prev_pos_left_down = pg.mouse.get_pos()

    def update(self):
        event = self.listener.listen()
        if event == 'quit':
            pg.quit()
        elif event == 'mouse_button_left_down':
            self.value_change = None
            self.prev_pos_left_down = pg.mouse.get_pos()
            x, y = self.prev_pos_left_down
            if self.form is not None and not (self.form.x <= x <= self.form.x + self.form.width and self.form.y <= y <= self.form.y + self.form.height):
                if self.toolbar.item_width <= x <= self.screen.get_rect().width - 2 * self.specification_viewer.cell_width:
                    for obj in self.group_selected:
                        obj.update_dictionary()
                        obj.is_selected = False
                    self.group_selected = []
                elif self.screen.get_rect().width - 2 * self.specification_viewer.cell_width <= x <= self.screen.get_rect().width and len(self.group_selected) == 1:
                    for obj in self.group_selected:
                        obj.update_dictionary()
                    self.value_change = self.specification_viewer.find_field(x, y)
                else:
                    for obj in self.group_selected:
                        obj.update_dictionary()
                        obj.is_selected = False
                    self.group_selected = []
                    if self.item_held is not None:
                        self.item_held.is_selected = False
                        self.item_held = None

            if self.item_held is None:
                item = self.toolbar.find_button(x, y)
                if item is not None:
                    self.create_new_object(item)
            else:
                self.item_held = None
        elif event == 'mouse_button_left_up':
            self.resize_action = None
            self.item_held = None
            self.item_resized = None
            if self.has_changed:
                self.memory.remember(self.form.copy())
                self.has_changed = False
        elif event == 'mouse_button_right_down':
            x, y = pg.mouse.get_pos()
            self.init_pos_right_down = (x, y)
        elif event == 'mouse_button_right_up':
            self.init_pos_right_down = (None, None)
        elif event == 'backspace_down':
            if self.value_change is None and len(self.group_selected) == 1 is not None and self.group_selected[0].type == 'Textbox' and len(self.group_selected[0].text) > 0:
                self.group_selected[0].text = self.group_selected[0].text[:-1]
                self.memory.remember(self.form.copy())
                self.has_changed = False
            elif self.value_change is not None and len(self.group_selected) == 1:
                value = self.group_selected[0].updated[self.value_change]
                if len(str(value)) > 0:
                    self.group_selected[0].updated[self.value_change] = str(value)[:-1]
        elif event == 'space_down':
            if self.value_change is None and len(self.group_selected) == 1 and self.group_selected[0].type == 'Textbox' and len(self.group_selected[0].text) < self.group_selected[0].max_len:
                self.group_selected[0].text += ' '
                self.memory.remember(self.form.copy())
                self.has_changed = False
            elif self.value_change is not None and len(self.group_selected) == 1:
                self.group_selected[0].updated[self.value_change] = str(
                    self.group_selected[0].updated[self.value_change]) + ' '
        elif event == 'enter_down':
            if self.value_change is None and len(self.group_selected) == 1 and self.group_selected[0].type == 'Textbox' and len(self.group_selected[0].text) < self.group_selected[0].max_len:
                self.group_selected[0].text += '\n'
                self.memory.remember(self.form.copy())
                self.has_changed = False
            elif self.value_change is not None and len(self.group_selected) == 1:
                error = self.group_selected[0].convert_variables()
                self.group_selected[0].update_dictionary()
                if not error:
                    self.memory.remember(self.form.copy())
                self.has_changed = False
        elif event == 'delete_down' and len(self.group_selected) != 0:
            for obj in self.group_selected:
                if obj is not self.form:
                    self.form.objects.remove(obj)
            self.group_selected = []
            self.memory.remember(self.form.copy())
            self.has_changed = False
        elif event == 'sCTRL_down':
            self.save()
            self.exception_handler.message = 'Form saved.'
        elif event == 'cCTRL_down':
            self.to_copy = self.group_selected
        elif event == 'vCTRL_down':
            self.copy_group()
        elif event == 'zCTRL_down':
            self.form = self.memory.move_record(-1).copy()
            self.group_selected = []
            if self.form.is_selected:
                self.group_selected = [self.form]
            for obj in self.form.objects:
                if obj.is_selected:
                    self.group_selected.append(obj)
            self.item_held = None
            self.item_resized = None
            self.value_change = None
            self.resize_action = None
            self.to_copy = []
        elif event == 'yCTRL_down':
            self.form = self.memory.move_record(1).copy()
            self.group_selected = []
            if self.form.is_selected:
                self.group_selected = [self.form]
            for obj in self.form.objects:
                if obj.is_selected:
                    self.group_selected.append(obj)
            self.item_held = None
            self.item_resized = None
            self.value_change = None
            self.resize_action = None
            self.to_copy = []
        elif event is not None and len(event) == 6 and event[-4:] == 'down':
            if self.value_change is None and len(self.group_selected) == 1 and self.group_selected[0].type == 'Textbox' and len(self.group_selected[0].text) < self.group_selected[0].max_len:
                self.group_selected[0].text += event[0]
                self.memory.remember(self.form.copy())
                self.has_changed = False
            elif self.value_change is not None and len(self.group_selected) == 1:
                self.group_selected[0].updated[self.value_change] = str(
                    self.group_selected[0].updated[self.value_change]) + event[0]

        if self.form is not None and self.item_held is None and self.resize_action is None and self.left_mouse_down() and self.value_change is None:
            self.resize_action = self.detect_rect_edge(self.form.x, self.form.y, self.form.width, self.form.height)
            if self.resize_action is not None and 0 <= self.resize_action <= 7:
                for obj in self.group_selected:
                    obj.update_dictionary()
                    obj.is_selected = False
                self.item_resized = self.form
                on_other_item = False
                for obj in self.form.objects:
                    if self.mouse_in_item(obj, is_on_form=True):
                        on_other_item = True
                if not on_other_item:
                    self.group_selected = [self.form]
                self.item_held = None
            elif self.resize_action is None and self.mouse_in_item(self.form):
                for obj in self.group_selected:
                    obj.update_dictionary()
                    obj.is_selected = False
                on_other_item = False
                for obj in self.form.objects:
                    if self.mouse_in_item(obj, is_on_form=True):
                        on_other_item = True
                if not on_other_item:
                    self.group_selected = [self.form]
                self.item_held = self.form
                self.item_resized = None
            for object in reversed(self.form.objects):
                ra = self.detect_rect_edge(object.abs_x, object.abs_y, object.width, object.height)
                if ra is not None:
                    self.resize_action = ra
                    self.item_resized = object
                    if object not in self.group_selected:
                        for obj in self.group_selected:
                            obj.update_dictionary()
                            obj.is_selected = False
                        self.group_selected = [object]
                    self.item_held = None
                    break
                elif self.mouse_in_item(object, is_on_form=True):
                    if object not in self.group_selected:
                        for obj in self.group_selected:
                            obj.update_dictionary()
                            obj.is_selected = False
                        self.group_selected = [object]
                    self.item_held = object
                    self.item_resized = None
                    break
        elif self.form is not None and self.item_resized is not None:
            self.resize_item(self.item_resized)

        self.find_selected_group()
        for obj in self.group_selected:
            obj.is_selected = True

        if len(self.group_selected) != 0 and self.left_mouse_down() and self.value_change is None:
            for obj in self.group_selected:
                diffx, diffy = pg.mouse.get_pos()[0] - self.prev_pos_left_down[0], pg.mouse.get_pos()[1] - self.prev_pos_left_down[1]
                obj.x += diffx
                obj.y += diffy
                if diffx != 0 or diffy != 0:
                    self.has_changed = True
            self.prev_pos_left_down = pg.mouse.get_pos()

        if self.value_change is None:
            for obj in self.group_selected:
                obj.update_dictionary()

        if self.item_held is not None:
            self.item_held.update_dictionary()

        self.update_screen()

    def load(self):
        loader = FormLoader(self.save_filepath, self.screen)
        loader.load()
        self.form = loader.form
        self.memory.remember(self.form.copy())
        self.exception_handler = loader.exception_handler

    def save(self):
        data_separator = '##END DATA##\n'
        to_save = []
        for (key, value) in [(key, value) for (key, value) in self.form.__dict__.items() if key in self.form.defaults]:
            to_save.append(f'{key}:{value}\n')
        to_save.append(data_separator)
        for object in self.form.objects:
            for (key, value) in [(key, value) for (key, value) in object.__dict__.items() if key in object.defaults]:
                if key == 'text':
                    value = value.replace('\n', '#')
                to_save.append(f'{key}:{value}\n')
            to_save.append(data_separator)
        savefile = open(self.save_filepath, 'w')
        savefile.writelines(to_save)
        savefile.close()