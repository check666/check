from config import *

class ChargeLine:
    def __init__(self, pos, width, height):
        self.height = height
        self.pos = [pos[0], pos[1]]
        self.distance = width
        self.color = random.randint(100, 200)
        self.thickness = random.randint(2, 5)
        self.dead = False

    def draw(self, offset):
        pygame.draw.line(screen, (self.color, self.color, self.color),
                         (self.pos[0] + self.distance + offset[0], self.pos[1] + offset[1]),
                         (self.pos[0] + self.distance + offset[0], self.pos[1] + self.height + offset[1]),
                         self.thickness)

        pygame.draw.line(screen, (self.color, self.color, self.color),
                         (self.pos[0] - self.distance + offset[0], self.pos[1] + offset[1]),
                         (self.pos[0] - self.distance + offset[0], self.pos[1] + self.height + offset[1]),
                         self.thickness)
        self.distance -= 10
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
        self.dead = False
        self.current_chance = num_lines/2

    def draw(self, offset):
        for i in range(len(self.lines) - 1, -1, -1):
            if self.lines[i].dead:
                del self.lines[i]
            else:
                self.lines[i].draw(offset)

    def update(self):
        if self.count < self.num_lines:
            if random.randint(0, int(self.current_chance)) == 0:
                self.count += 1
                self.current_chance -= 0.5
                self.lines.append(ChargeLine(self.pos, self.width, self.height))
        elif not self.lines:
            self.dead = True
