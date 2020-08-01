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

    status_texture = (texture_lib["level_d"], texture_lib["level_p"], texture_lib["level_c"], texture_lib["level_s"])
    def __init__(self):
        self.float_cycle = ReCycle(6, 4)
        self.level_float = ReCycle(6, 2)
        self.level_points = ((46, 144), (134, 227), (290, 202), (412, 274))

        self.point_status = [0 for _ in range(9)]
        self.point_status[0] = 2

        self.c_float = 0

        self.current_level = 0

        self.next_level()
        self.next_level()

    def next_level(self):
        self.point_status[self.current_level] = 1
        self.current_level += 1
        self.point_status[self.current_level] = 2

    def draw(self):
        screen.blit(texture_lib["menu_route"], (0, self.c_float))
        for i in range(len(self.level_points)):
            screen.blit(self.status_texture[self.point_status[i]], (self.level_points[i][0],
                                                 self.level_points[i][1] + self.c_float))
            if self.point_status[i] == 3:
                screen.blit(texture_lib["level_base"], (self.level_points[i][0] + 7,
                                                 self.level_points[i][1] + self.c_float + self.level_float.get() - 75))

    def update(self):
        self.c_float = self.float_cycle.get()
        for i in range(len(self.level_points)):
            if self.point_status[i] != 0:
                if i == self.current_level:
                    self.point_status[i] = 2
                else:
                    self.point_status[i] = 1
                if self.level_points[i][0] < env["mouse_x"] < self.level_points[i][0] + 75:
                    if self.level_points[i][1] + self.c_float < env["mouse_y"] \
                            < self.level_points[i][1] + 33 + self.c_float:
                        self.point_status[i] = 3
