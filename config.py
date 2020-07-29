import pygame, sys, random
from math import *
from cycle import *

pygame.init()

env = {"mouse_direction": 0, "mouse_x": 0, "mouse_y": 0}

screen_width, screen_height = 600, 400
screen = pygame.display.set_mode((screen_width, screen_height))

chat_font_size = 20
chat_font = pygame.font.Font("sanji.ttf", chat_font_size)

clock = pygame.time.Clock()

def get_distance(p1, p2):
    d1, d2 = p1[0] - p2[0], p1[1] - p2[1]
    return sqrt(d1*d1 + d2*d2)


def load(n):
    return pygame.image.load("texture\\" + n + ".png").convert_alpha()


texture_names = ["close_snake_1", "close_snake_2", "mouse_click", "exp_bar", "hp_bar"]

texture_lib = {}

for name in texture_names:
    texture_lib[name] = load(name)
