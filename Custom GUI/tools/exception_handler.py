import pygame as pg

class ExceptionHandler(object):

    def __init__(self, screen):
        self.screen = screen
        self.message = ''
        self.font = pg.font.SysFont('Arial', 20)

    def draw(self):
        to_display = self.message.split('\n')
        cur_h = 0
        init_height_offset = 200
        width, height = self.screen.get_rect().width, self.screen.get_rect().height
        for i, line in enumerate(to_display):
            text = self.font.render(line, False, (0, 0, 0))
            w, h = text.get_rect().width, text.get_rect().height
            self.screen.blit(text, (5, height - init_height_offset + cur_h))
            cur_h += h
        pg.draw.line(self.screen, (0, 0, 0), (0, height - init_height_offset - 5), (width, height - init_height_offset - 5), 2)
