import pygame as pg

def init_events():
    events = ['mouse_button_left_down', 'mouse_button_left_up', 'backspace_down', 'enter_down', 'space_down', 'delete_down',
              'mouse_button_right_down', 'mouse_button_right_up', 'cCTRL_down', 'vCTRL_down', 'sCTRL_down']
    for i in range(33, 127):
        events.append(chr(i) + '_down')
        events.append(chr(i).upper() + '_down')
    events_dict = {}
    for event in events:
        events_dict[event] = None
    return events_dict

def check_name_eligibility(name, form):
    if form.name == name:
        raise Exception
    for object in form.objects:
        if object.name == name:
            raise Exception
    return name

def str_to_tuple(data):
    data = str(data)
    conv_data = ''
    for char in data:
        if char != ' ':
            conv_data += char
    if (conv_data[0] != '[' and conv_data[0] != '(') or (conv_data[-1] != ']' and conv_data[-1] != ')'):
        raise Exception
    conv_data = conv_data[1:-1]
    conv_data = conv_data.split(',')
    if len(conv_data) != 3:
        raise Exception
    for i, value in enumerate(conv_data):
        conv_data[i] = int(value)
        if int(value) < 0 or int(value) > 255:
            raise Exception
    return conv_data

def find_font(font):
    if font in pg.font.get_fonts():
        return font
    else:
        raise Exception



