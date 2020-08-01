import random

class Cycle:
    def __init__(self, num, speed):
        self.tick = 0
        self.current = 0
        self.speed = speed
        self.num = num
        self.one = False
        self.prev = self.current

    def get(self):
        self.tick += 1
        self.prev = self.current
        if self.tick > self.speed:
            self.tick = 0
            self.current += 1
            if self.current >= self.num:
                self.current = 0
        if self.tick+1 > self.speed and self.current+1 >= self.num:
            self.one = True
        return self.current

    def reset(self):
        self.tick = 0
        self.current = 0

    def changed(self):
        return self.prev != self.current

class ReCycle:
    def __init__(self, num, speed, start=0):
        self.tick = 0
        self.current = start
        self.speed = speed
        self.num = num
        self.one = False
        self.v = 1
        self.prev = self.current

    def get(self):
        self.tick += 1
        if self.tick > self.speed:
            self.tick = 0
            self.prev = self.current
            self.current += self.v
            if self.current >= self.num:
                self.current = self.num - 1
                self.v = -1
                self.one = True
            elif self.current < 0:
                self.current = 0
                self.v = 1
        return  self.current

    def reset(self):
        self.tick = 0
        self.current = 0

    def changed(self):
        return self.prev != self.current

class RandCycle:
    def __init__(self, num, speed, range):
        self.tick = 0
        self.current = 0
        self.speed = speed
        self.num = num
        self.one = False
        self.range = range
        self.prev = self.current

    def changed(self):
        return self.prev != self.current

    def get(self):
        self.tick += random.randint(self.range[0], self.range[1])
        self.prev = self.current
        if self.tick > self.speed:
            self.tick = 0
            self.current += 1
            if self.current >= self.num:
                self.current = 0
        if self.tick+1 > self.speed and self.current+1 >= self.num:
            self.one = True
        return self.current

    def reset(self):
        self.tick = 0
        self.current = 0

