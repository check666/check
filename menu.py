from config import *

class RectPoint:
    def __init__(self, pos, speed, deme):
        self.start = (pos[0], pos[1])
        self.pos = pos
        self.vel = (speed, 0)
        self.speed = speed
        self.deme = deme

    def move(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        if self.pos[0] < self.start[0]:
            self.pos[0] = self.start[0]
            self.vel = (0, -self.speed)
        elif self.pos[0] > self.start[0] + self.deme[0]:
            self.pos[0] = self.start[0] + self.deme[0]
            self.vel = (0, self.speed)
        elif self.pos[1] < self.start[1]:
            self.pos[1] = self.start[1]
            self.vel = (self.speed, 0)
        elif self.pos[1] > self.start[1] + self.deme[1]:
            self.pos[1] = self.start[1] + self.deme[1]
            self.vel = (-self.speed, 0)


    def get(self):
        return self.pos

class MainMenu:
    def __init__(self):
        self.points = [-150, 0, 150, 300, 450]
        self.float_cycle = ReCycle(8, 3)
        self.float_cycle2 = ReCycle(8, 3, 3)
        self.point_set1 = [RectPoint([207, 198], 10, (190, 40)) for _ in range(15)]
        for i in range(len(self.point_set1)):
            for _ in range(i*2):
                self.point_set1[i].move()
        self.hovered = 1

    def update(self):
        for i in range(5):
            self.points[i] += 2
            if self.points[i] >= 600:
                self.points[i] = -150
        if self.hovered == 1:
            for point in self.point_set1:
                point.move()

        self.hovered = 0
        if 207 < env["mouse_x"] < 397:
            if 198 < env["mouse_y"] < 238:
                self.hovered = 1

    def draw(self):
        screen.blit(texture_lib["title_shadow"], (0, 46 + self.float_cycle.get()))
        screen.blit(texture_lib["title"], (0, 47 + self.float_cycle2.get()))
        if self.hovered == 1:
            screen.blit(texture_lib["start_button_hovered"], (0, 197))
        else:
            screen.blit(texture_lib["start_button"], (0, 197))
        screen.blit(texture_lib["continue_button"], (0, 248))
        screen.blit(texture_lib["settings_button"], (0, 335))
        screen.blit(texture_lib["help_button"], (59, 341))
        for point in self.points:
            pygame.draw.polygon(screen, (170, 170, 170),
                                ((point, 163), (point+75, 161), (point+150, 163), (point+75, 165), (point, 163)))
        if self.hovered == 1:
            for i in range(len(self.point_set1)-1):
                pygame.draw.line(screen, (255, 255, 255), self.point_set1[i].get(), self.point_set1[i+1].get())

class LevelSelect:
    pass