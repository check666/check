import pygame
import os
from math import *

pygame.init()

env = {"mouse_direction": 0, "mouse_x": 0, "mouse_y": 0, "mouse_down": False}

screen_width, screen_height = 600, 400
screen = pygame.display.set_mode((screen_width, screen_height))

chat_font_size = 20
chat_font = pygame.font.Font("sanji.ttf", chat_font_size)

level_font = pygame.font.Font("sanji.ttf", 40)

clock = pygame.time.Clock()

pygame.display.set_caption('SnakeQuest')


def get_distance(p1, p2):
    d1, d2 = p1[0] - p2[0], p1[1] - p2[1]
    return sqrt(d1*d1 + d2*d2)


def get_angle(x, y):
    return atan2(y, x)


textures = os.listdir("texture")


def load(n):
    return pygame.image.load(os.path.join("texture", n + ".png")).convert_alpha()


texture_names = [name[:-4] for name in textures]

texture_lib = {}

for name in texture_names:
    texture_lib[name] = load(name)


class AudioPlayer:
    def __init__(self, id_in, type_in, volume=0.2):
        self.id = id_in
        self.music = pygame.mixer.Sound(os.path.join('audio', id_in + '.ogg'))
        self.music.set_volume(volume)
        if type_in == "bg":
            self.channel = pygame.mixer.Channel(1)
        if type_in == "se":
            self.channel = pygame.mixer.Channel(2)
        if type_in == "sn":
            self.channel = pygame.mixer.Channel(3)

    def play_non_stop(self):
        self.channel.play(self.music, -1)

    def play_once(self):
        self.channel.play(self.music, 0)

    def stop(self):
        self.channel.stop()


bgs = (AudioPlayer("menubg", "bg"),
       AudioPlayer("gamebg", "bg"),
       AudioPlayer("gamebg2", "bg"),
       AudioPlayer("chat", "bg"),
       AudioPlayer("map", "bg", volume=0.06))

ses = (AudioPlayer("sebigcannon", "se"),
       AudioPlayer("sebutton", "se"),
       AudioPlayer("seeat", "sn"),
       AudioPlayer("sehit", "sn"),
       AudioPlayer("selevelup", "sn"),
       AudioPlayer("sesmallcannon", "se"),
       AudioPlayer("sebeam", "se"),
       AudioPlayer("sechat", "se"))
