import pygame as pg

class Listener(object):

    def __init__(self):
        pass

    def listen(self):
        mods = pg.key.get_mods()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 'quit'
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return 'quit'
                elif event.key == pg.K_s and mods & pg.KMOD_CTRL:
                    return 'sCTRL_down'
                elif event.key == pg.K_c and mods & pg.KMOD_CTRL:
                    return 'cCTRL_down'
                elif event.key == pg.K_v and mods & pg.KMOD_CTRL:
                    return 'vCTRL_down'
                elif event.key == pg.K_z and mods & pg.KMOD_CTRL:
                    return 'zCTRL_down'
                elif event.key == pg.K_y and mods & pg.KMOD_CTRL:
                    return 'yCTRL_down'
                elif 33 <= event.key <= 126 and not (mods & pg.KMOD_SHIFT or mods & pg.KMOD_CAPS):
                    return chr(event.key) + '_down'
                elif 33 <= event.key <= 126 and (mods & pg.KMOD_SHIFT or mods & pg.KMOD_CAPS):
                    return chr(event.key).upper() + '_down'
                elif event.key == pg.K_BACKSPACE:
                    return 'backspace_down'
                elif event.key == pg.K_SPACE:
                    return 'space_down'
                elif event.key == pg.K_RETURN:
                    return 'enter_down'
                elif event.key == pg.K_DELETE:
                    return 'delete_down'
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return 'mouse_button_left_down'
                elif event.button == 3:
                    return 'mouse_button_right_down'
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    return 'mouse_button_left_up'
                elif event.button == 3:
                    return 'mouse_button_right_up'
        return None