import pygame as pg

class Memory(object):

    def __init__(self, max_len = 20):
        self.max_len = max_len
        self.memory = []
        self.memory_index = -1

    def remember(self, form):
        if self.memory_index >= 0:
            self.memory = self.memory[:self.memory_index + 1]
        self.memory.append(form)
        if len(self.memory) > self.max_len:
            self.memory.pop(0)
        self.memory_index += 1

    def move_record(self, action):
        if len(self.memory) > 0:
            self.memory_index += action
            self.memory_index = min(len(self.memory) - 1, self.memory_index)
            self.memory_index = max(0, self.memory_index)
            return self.memory[self.memory_index]