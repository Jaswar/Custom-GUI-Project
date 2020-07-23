import pygame as pg

class Toolbar(object):

    def __init__(self, screen, items = ['Form', 'Textbox']):
        self.screen = screen
        self.items = items
        self.item_width = 180
        self.item_height = 30
        self.font = pg.font.SysFont('Arial', 26)

    def draw(self):
        pg.draw.rect(self.screen, (0, 0, 0), (0, 0, self.item_width, self.item_height), 2)
        main_text = self.font.render('Items:', False, (0, 0, 0))
        w, h = main_text.get_rect().width, main_text.get_rect().height
        self.screen.blit(main_text, (self.item_width//2 - w//2, 0))

        for i, item in enumerate(self.items):
            pg.draw.rect(self.screen, (0, 0, 0), (0, (i + 1)*self.item_height, self.item_width, self.item_height), 2)
            item_text = self.font.render(item, False, (0, 0, 0))
            w, h = item_text.get_rect().width, item_text.get_rect().height
            self.screen.blit(item_text, (self.item_width // 2 - w // 2, (i + 1)*self.item_height))

    def find_button(self, x, y):
        if x > self.item_width or x < 0:
            return None
        for i, item in enumerate(self.items):
            if (i + 1)*self.item_height <= y < (i + 2)*self.item_height:
                return item
        return None