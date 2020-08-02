from config import *

class ChargeLine:
    def __init__(self, pos, width, height):
        self.height = height
        self.pos = [pos[0], pos[1]]
        self.distance = width
        self.color = random.randint(100, 200)
        self.thickness = random.randint(1, 5)
        self.dead = False

    def draw(self):
        pygame.draw.line(screen, (self.color, self.color, self.color),
                         (self.pos[0] + self.distance, self.pos[1]),
                         (self.pos[0] + self.distance, self.pos[1] + self.height))

        pygame.draw.line(screen, (self.color, self.color, self.color),
                         (self.pos[0] - self.distance, self.pos[1]),
                         (self.pos[0] - self.distance, self.pos[1] + self.height))
        self.distance -= 5
        if self.distance <= 0:
            self.dead = True

class Charge:
    def __init__(self, pos, width, height, num_lines):
        self.lines = []
        self.num_lines = num_lines
        self.width = width
        self.height = height
        self.pos = pos
        self.count = 0
        self.dead = True

    def draw(self):
        for i in range(len(self.lines) - 1, -1, -1):
            if self.lines[i].dead:
                del self.lines[i]
            else:
                self.lines[i].draw()

    def update(self):
        if self.count < self.num_lines:
            if random.randint(1, 6) == 1:
                self.count += 1
                self.lines.append(ChargeLine(self.pos, self.width, self.height))
        else:
            self.dead = True
