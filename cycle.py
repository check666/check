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