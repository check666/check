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
        self.point_set2 = [RectPoint([206, 250], 10, (191, 40)) for _ in range(15)]
        for i in range(len(self.point_set1)):
            for _ in range(i*2):
                self.point_set1[i].move()
                self.point_set2[i].move()
        self.hovered = 1
        self.con_hovered = 1
        bgs[0].playNonStop()

    def update(self):
        for i in range(5):
            self.points[i] += 2
            if self.points[i] >= 600:
                self.points[i] = -150
        if self.hovered == 1:
            for point in self.point_set1:
                point.move()
        if self.con_hovered == 1:
            for point in self.point_set2:
                point.move()
        self.hovered = 0
        self.con_hovered = 0
        if 207 < env["mouse_x"] < 397:
            if 198 < env["mouse_y"] < 238:
                self.hovered = 1
        if 210 < env["mouse_x"] < 420:
            if 250 < env["mouse_y"] < 290:
                self.con_hovered = 1

    def draw(self):
        screen.blit(texture_lib["title_shadow"], (0, 46 + self.float_cycle.get()))
        screen.blit(texture_lib["title"], (0, 47 + self.float_cycle2.get()))
        if self.hovered == 1:
            screen.blit(texture_lib["start_button_hovered"], (0, 197))
        else:
            screen.blit(texture_lib["start_button"], (0, 197))
        if self.con_hovered == 1:
            screen.blit(texture_lib["continue_button_hovered"], (0, 240))
        else:
            screen.blit(texture_lib["continue_button"], (0, 240))
        for point in self.points:
            pygame.draw.polygon(screen, (170, 170, 170),
                                ((point, 163), (point+75, 161), (point+150, 163), (point+75, 165), (point, 163)))
        if self.hovered == 1:
            for i in range(len(self.point_set1)-1):
                pygame.draw.line(screen, (255, 255, 255), self.point_set1[i].get(), self.point_set1[i+1].get())
        if self.con_hovered == 1:
            for i in range(len(self.point_set2)-1):
                pygame.draw.line(screen, (255, 255, 255), self.point_set2[i].get(), self.point_set2[i+1].get())
        screen.blit(texture_lib["copyright"], (0, 0))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.hovered:
                ses[1].playOnce()
                return -2
            elif self.con_hovered:
                ses[1].playOnce()
                return -3
        return -1


class LevelSelect:
    status_texture = (texture_lib["level_d"], texture_lib["level_p"], texture_lib["level_c"], texture_lib["level_s"])
    def __init__(self, level_at):
        bgs[4].playNonStop()
        self.float_cycle = ReCycle(6, 4)
        self.level_float = ReCycle(6, 2)
        self.level_points = ((46, 144), (134, 227), (290, 202), (412, 274), (558, 241), (734, 302), (872, 231),
                             (729, 194))
        self.scroll = 0

        self.point_status = [0 for _ in range(9)]
        self.point_status[0] = 2

        self.c_float = 0

        self.current_level = 0

        for _ in range(level_at):
            self.next_level()
        self.arrow_cycle = ReCycle(10, 3)

    def next_level(self):
        self.point_status[self.current_level] = 1
        self.current_level += 1
        self.point_status[self.current_level] = 2

    def draw(self):
        screen.blit(texture_lib["menu_route"], (-self.scroll, self.c_float))
        for i in range(len(self.level_points)):
            screen.blit(self.status_texture[self.point_status[i]], (self.level_points[i][0] - self.scroll,
                                                 self.level_points[i][1] + self.c_float))
            title = chat_font.render("关卡" + str(i+1), False, (255, 255, 255))
            title2 = chat_font.render("关卡" + str(i + 1), False, (0, 0, 0))
            screen.blit(title, (self.level_points[i][0] - self.scroll + 10,
                                                                    self.level_points[i][1] + self.c_float + 35))
            screen.blit(title2, (self.level_points[i][0] - self.scroll + 8,
                                self.level_points[i][1] + self.c_float + 33))
            if self.point_status[i] == 3:
                screen.blit(texture_lib["level_base"], (self.level_points[i][0] + 7 - self.scroll,
                                                 self.level_points[i][1] + self.c_float + self.level_float.get() - 75))
                screen.blit(texture_lib["icon" + str(i+1)], (self.level_points[i][0] + 7 - self.scroll,
                                                        self.level_points[i][
                                                            1] + self.c_float + self.level_float.get() - 75))
        arrow_way = self.arrow_cycle.get()
        if self.scroll > 0:
            screen.blit(texture_lib["left_arrow"], (arrow_way, 0))
        if self.scroll < 450:
            screen.blit(texture_lib["right_arrow"], (550-arrow_way, 0))

    def update(self):
        self.c_float = self.float_cycle.get()
        for i in range(len(self.level_points)):
            if self.point_status[i] != 0:
                if i == self.current_level:
                    self.point_status[i] = 2
                else:
                    self.point_status[i] = 1
                if self.level_points[i][0] - self.scroll < env["mouse_x"] < self.level_points[i][0] + 75 - self.scroll:
                    if self.level_points[i][1] + self.c_float < env["mouse_y"] \
                            < self.level_points[i][1] + 33 + self.c_float:
                        self.point_status[i] = 3
        if env["mouse_x"] < 50:
            self.scroll -= 5
            if self.scroll < 0:
                self.scroll = 0
        elif env["mouse_x"] > 550:
            self.scroll += 5
            if self.scroll > 450:
                self.scroll = 450

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            for i in range(len(self.point_status)):
                if self.point_status[i] == 3:
                    ses[1].playOnce()
                    return i
        return -1
