import pygame, sys, random, os
from math import *
from cycle import *

pygame.init()

env = {"mouse_direction": 0, "mouse_x": 0, "mouse_y": 0, "mouse_down": False}

screen_width, screen_height = 600, 400
screen = pygame.display.set_mode((screen_width, screen_height))

chat_font_size = 20
chat_font = pygame.font.Font("sanji.ttf", chat_font_size)

level_font = pygame.font.Font("sanji.ttf", 40)

clock = pygame.time.Clock()

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

class AudioPlayer():
    def __init__(self,id,type,volume=0.2):
        self.id = id
        self.music = pygame.mixer.Sound(os.path.join('audio', id+'.ogg'))
        self.music.set_volume(volume)
        if type == "bg":
            self.channel = pygame.mixer.Channel(1)
        if type == "se":
            self.channel = pygame.mixer.Channel(2)

    def playNonStop(self):
        self.channel.play(self.music,-1)

    def playOnce(self):
        self.channel.play(self.music, 0)

    def stop(self):
        self.channel.stop()

bgs = (AudioPlayer("menubg", "bg"),
       AudioPlayer("gamebg", "bg"),
       AudioPlayer("gamebg2", "bg"),
       AudioPlayer("chat", "bg"),
       AudioPlayer("map", "bg", volume=0.06))