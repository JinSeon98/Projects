import pygame
from marketGameSettings import *

class Button:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def put_img(self, address):
        self.img = pygame.image.load(address).convert_alpha()
        self.sx, self.sy = self.img.get_size()
    def set_position(self, x, y):
        self.x, self.y = x, y
    def get_position(self):
        return (self.x, self.y)

class Puppy(Button):
    def __init__(self, x, y):
        Button.__init__(self, x, y)

class Product(Button):
    def __init__(self, x, y, price):
        Button.__init__(self, x, y)
        self.price = price
    # 인벤토리에 들어갈 이미지
    def put_in_img(self, address):
        self.in_img = pygame.image.load(address).convert_alpha()
        self.in_sx, self.in_sy = self.in_img.get_size()