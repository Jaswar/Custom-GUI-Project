import pygame as pg

class SpecificationViewer(object):

    def __init__(self, screen):
        self.screen = screen
        self.cell_width = 180
        self.cell_height = 30
        self.font = pg.font.SysFont('Arial', 26)
        self.displayed_object = None

    def draw(self, item):
        self.displayed_object = item
        w, h = self.screen.get_rect().width, self.screen.get_rect().height
        pg.draw.rect(self.screen, (0, 0, 0), (w - 2 * self.cell_width, 0, self.cell_width, self.cell_height), 2)
        pg.draw.rect(self.screen, (0, 0, 0), (w - self.cell_width, 0, self.cell_width, self.cell_height), 2)
        field_text = self.font.render('Field', False, (0, 0, 0))
        tw1, th1 = field_text.get_rect().width, field_text.get_rect().height
        self.screen.blit(field_text, (w - 3*self.cell_width//2 - tw1//2, self.cell_height//2 - th1//2))
        value_text = self.font.render('Value', False, (0, 0, 0))
        tw2, th2 = value_text.get_rect().width, value_text.get_rect().height
        self.screen.blit(value_text, (w - self.cell_width//2 - tw2//2, self.cell_height//2 - th2//2))

        for i, (key, value) in enumerate(item.updated.items()):
            pg.draw.rect(self.screen, (0, 0, 0), (w - 2 * self.cell_width, (i+1)*self.cell_height, self.cell_width, self.cell_height), 2)
            pg.draw.rect(self.screen, (0, 0, 0), (w - self.cell_width, (i+1)*self.cell_height, self.cell_width, self.cell_height), 2)
            field_text = self.font.render(str(key), False, (0, 0, 0))
            tw1, th1 = field_text.get_rect().width, field_text.get_rect().height
            self.screen.blit(field_text, (w - 3 * self.cell_width // 2 - tw1 // 2, self.cell_height // 2 - th1 // 2 + (i+1)*self.cell_height))
            value_text = self.font.render(str(value), False, (0, 0, 0))
            tw2, th2 = value_text.get_rect().width, value_text.get_rect().height
            if tw2 < self.cell_width - 4:
                self.screen.blit(value_text, (w - self.cell_width // 2 - tw2 // 2, self.cell_height // 2 - th2 // 2 + (i+1)*self.cell_height))
            else:
                value_text = self.font.render('--too long--', False, (0, 0, 0))
                tw2, th2 = value_text.get_rect().width, value_text.get_rect().height
                self.screen.blit(value_text, (
                w - self.cell_width // 2 - tw2 // 2, self.cell_height // 2 - th2 // 2 + (i + 1) * self.cell_height))

    def find_field(self, x, y):
        if self.displayed_object is not None:
            w = self.screen.get_rect().width
            if x < w - 2*self.cell_width:
                return None
            for i, (field, value) in enumerate(self.displayed_object.updated.items()):
                if (i + 1)*self.cell_height <= y <= (i + 2)*self.cell_height:
                    return field
            return None

