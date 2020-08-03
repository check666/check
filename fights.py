from config import *

from animations import *

class Obstacles:
    def __init__(self):
        self.damage = 0
        self.attack = False
        self.dead = False
        self.bounded = False
        self.pos = [0, 0]

    def collide_with(self, snake):
        pass

    def draw(self, offset):
        pass

    def update(self):
        pass

class Beam(Obstacles):
    def __init__(self, pos, length, direction, width=30, pre_t=100, last_t=6, color=(242, 245, 66), damage=20):
        Obstacles.__init__(self)
        self.damage = damage
        self.color = color
        self.pos = pos
        self.point1 = [pos[0], pos[1]]
        self.point2 = [pos[0], pos[1]]
        if direction == "v":
            self.point2[1] += length
        elif direction == "h":
            self.point2[0] += length
        self.width = width
        self.tick = 0
        self.direction = direction

        self.pre_t = pre_t
        self.last_t = last_t

        self.speed = width / self.last_t

    def collide_with(self, snake):
        if self.direction == "v":
            for i in range(0, len(snake.hit_points)-2, 2):
                if not(self.pos[0] - self.width/2 > max(snake.hit_points[i][0], snake.hit_points[i+2][0]) or
                        self.pos[0] + self.width/2 < min(snake.hit_points[i][0], snake.hit_points[i+2][0])):
                    return True

        elif self.direction == "h":
            for i in range(0, len(snake.hit_points)-2, 2):
                if not (self.pos[1] - self.width/2 > max(snake.hit_points[i][1], snake.hit_points[i + 2][1]) or
                        self.pos[1] + self.width/2 < min(snake.hit_points[i][1], snake.hit_points[i + 2][1])):
                    return True
        return False


    def update(self):
        if self.tick > self.pre_t + self.last_t*2:
            self.dead = True
        else:
            self.tick += 1

        if self.tick == self.pre_t + self.last_t:
            self.attack = True
        else:
            self.attack = False

    def draw(self, offset):
        if self.tick < self.pre_t:
            pygame.draw.line(screen, (255, 100, 100),
                         (self.point1[0] + offset[0], self.point1[1] + offset[1]),
                         (self.point2[0] + offset[0], self.point2[1] + offset[1]), 2)
        elif self.tick < self.pre_t + self.last_t:
            pygame.draw.line(screen, self.color,
                             (self.point1[0] + offset[0], self.point1[1] + offset[1]),
                             (self.point2[0] + offset[0], self.point2[1] + offset[1]),
                             int(self.speed * (self.tick - self.pre_t)))
        elif self.tick < self.pre_t + self.last_t*2:
            pygame.draw.line(screen, self.color,
                             (self.point1[0] + offset[0], self.point1[1] + offset[1]),
                             (self.point2[0] + offset[0], self.point2[1] + offset[1]),
                             int(self.speed * (self.pre_t + self.last_t*2 - self.tick)))

class LastBeam(Obstacles):
    def __init__(self, pos, height, orientation, objectT, width=30, pre_t=100, dur_t=60, last_t=6, color=(242, 245, 66), damage=20):
        Obstacles.__init__(self)
        self.damage = damage
        self.color = color
        self.pos = [pos[0], pos[1]]
        self.point1 = [pos[0], pos[1]]
        self.point2 = [pos[0], pos[1]]
        self.orientation = orientation
        if self.orientation == "v":
            self.point2[1] += height
        else:
            self.point2[0] += height
        self.width = width
        self.tick = 0
        self.height = height

        self.pre_t = pre_t
        self.dur_t = dur_t
        self.last_t = last_t
        self.objectT = objectT

        self.speed = width / self.last_t
        self.attack_cycle = Cycle(20, 0)

    def collide_with(self, snake):
        if self.orientation == "v":
            for i in range(0, len(snake.hit_points)-2, 2):
                if not(self.pos[0] - self.width/2 > max(snake.hit_points[i][0], snake.hit_points[i+2][0]) or
                        self.pos[0] + self.width/2 < min(snake.hit_points[i][0], snake.hit_points[i+2][0])):
                    return True

        elif self.orientation == "h":
            for i in range(0, len(snake.hit_points)-2, 2):
                if not (self.pos[1] - self.width/2 > max(snake.hit_points[i][1], snake.hit_points[i + 2][1]) or
                        self.pos[1] + self.width/2 < min(snake.hit_points[i][1], snake.hit_points[i + 2][1])):
                    return True
        return False


    def update(self):
        self.tick += 1
        self.attack = False
        if self.pre_t + self.last_t < self.tick < self.pre_t + self.last_t + self.dur_t:
            if self.attack_cycle.get() == 0:
                self.attack = True

    def draw(self, offset):
        if self.tick < self.pre_t:
            pygame.draw.line(screen, (255, 100, 100),
                         (self.point1[0] + offset[0], self.point1[1] + offset[1]),
                         (self.point2[0] + offset[0], self.point2[1] + offset[1]), 2)
        elif self.tick < self.pre_t + self.last_t:
            pygame.draw.line(screen, self.color,
                             (self.point1[0] + offset[0], self.point1[1] + offset[1]),
                             (self.point2[0] + offset[0], self.point2[1] + offset[1]),
                             int(self.speed * (self.tick - self.pre_t)))
        elif self.tick < self.pre_t + self.last_t + self.dur_t:
            pygame.draw.line(screen, self.color,
                             (self.point1[0] + offset[0], self.point1[1] + offset[1]),
                             (self.point2[0] + offset[0], self.point2[1] + offset[1]),
                             self.width)
        elif self.tick < self.pre_t + self.last_t*2 + self.dur_t:
            pygame.draw.line(screen, self.color,
                             (self.point1[0] + offset[0], self.point1[1] + offset[1]),
                             (self.point2[0] + offset[0], self.point2[1] + offset[1]),
                             int(self.speed * (self.pre_t + self.last_t*2 + self.dur_t - self.tick)))
        else:
            self.dead = True

class Bullet(Obstacles):
    def __init__(self, damage, radius, x, y, vx, vy, one_time=True):
        Obstacles.__init__(self)
        self.damage = damage
        self.radius = radius
        self.speed = [vx, vy]
        self.pos = [x, y]
        self.bounded = True

        self.attack = True
        self.dead_on_collide = one_time

    def update(self):
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]

    def draw(self, offset):
        pygame.draw.circle(screen, (170, 0, 0), (self.pos[0] + offset[0], self.pos[1] + offset[1]), self.radius)

    def collide_with(self, snake):
        for i in range(0, len(snake.hit_points), 2):
            if get_distance(snake.hit_points[i], self.pos) < snake.width + self.radius - 3:
                if self.dead_on_collide:
                    self.dead = True
                return True
        return False

class ExpBall:
    def __init__(self, pos, points=10):
        self.pos = pos
        self.points = points

    def draw(self, offset):
        pygame.draw.circle(screen, (255, 255, 255), (self.pos[0] + offset[0], self.pos[1] + offset[1]), self.points)

class OneCanon:
    def __init__(self, pos):
        self.cast = False
        self.attacking = False
        self.attack_cycle = Cycle(2, 50)
        self.attack_ani_cycle = Cycle(4, 2)
        self.pos = [pos[0], pos[1]]
        self.dead = False

    def attack(self):
        self.attacking = True
        self.attack_ani_cycle = Cycle(4, 4)

    def update(self):
        self.cast = False
        if self.attacking:
            if self.attack_ani_cycle.one:
                self.attacking = False
                self.cast = True
        else:
            if self.attack_cycle.get() == 0 and self.attack_cycle.changed():
                self.attack()
                self.attack_cycle.current += random.randint(0, 20)

    def draw(self, offset):
        if self.attacking:
            screen.blit(texture_lib["one_cannon"], (self.pos[0]+offset[0], self.pos[1]+offset[1]),
                        pygame.Rect(0, self.attack_ani_cycle.get() * 80, 80, 80))
        else:
            screen.blit(texture_lib["one_cannon"], (self.pos[0] + offset[0], self.pos[1] + offset[1]),
                        pygame.Rect(0, 0, 80, 80))

class CrossCanon:
    def __init__(self, pos):
        self.cast = False
        self.attacking = False
        self.attack_cycle = Cycle(2, 80)
        self.attack_ani_cycle = Cycle(4, 4)
        self.pos = [pos[0], pos[1]]
        self.dead = False

    def attack(self):
        self.attacking = True
        self.attack_ani_cycle = Cycle(4, 4)

    def update(self):
        self.cast = False
        if self.attacking:
            if self.attack_ani_cycle.one:
                self.attacking = False
                self.cast = True
        else:
            if self.attack_cycle.get() == 0 and self.attack_cycle.changed():
                self.attack()
                self.attack_cycle.tick += random.randint(0, 40)

    def draw(self, offset):
        if self.attacking:
            screen.blit(texture_lib["cross_cannon"], (self.pos[0]+offset[0], self.pos[1]+offset[1]),
                        pygame.Rect(0, self.attack_ani_cycle.get() * 80, 80, 80))
        else:
            screen.blit(texture_lib["cross_cannon"], (self.pos[0] + offset[0], self.pos[1] + offset[1]),
                        pygame.Rect(0, 0, 80, 80))

class MovingBeamCannon:
    def __init__(self, pos, orientation, direction, length, height, cd=60):
        self.orientation = orientation
        self.height = height
        self.cast = False
        self.attacking = False
        self.pos = [pos[0], pos[1]]
        self.speed = 2
        if self.orientation == "v":
            self.end = pos[0] + length * direction
        else:
            self.end = pos[1] + length * direction
        self.dead = False
        self.length = length
        self.cd = cd
        self.direction = direction
        self.end_tick = cd
        self.dying = False
        self.beam = LastBeam(self.pos, self.height, self.orientation, self,
                             pre_t=cd-20, last_t=20, dur_t=self.length/self.speed)

    def get_beam(self):
        return self.beam

    def update(self):
        if not self.attacking:
            if self.cd > 0:
                self.cd -= 1
            else:
                self.attacking = True
        elif self.dying:
            self.end_tick -= 1
            if self.end_tick < 0:
                self.dead = True
        else:
            if self.direction == 1:
                if self.orientation == "v":
                    self.pos[0] += self.speed
                    if self.pos[0] > self.end:
                        self.dying = True
                elif self.orientation == "h":
                    self.pos[1] += self.speed
                    if self.pos[1] > self.end:
                        self.dying = True

            elif self.direction == -1:
                if self.orientation == "v":
                    self.pos[0] -= self.speed
                    if self.pos[0] < self.end:
                        self.dying = True
                elif self.orientation == "h":
                    self.pos[1] -= self.speed
                    if self.pos[1] < self.end:
                        self.dying = True
            self.beam.pos[0] = self.pos[0]
            self.beam.pos[1] = self.pos[1]
            if self.orientation == "v":
                self.beam.point1[0] = self.pos[0]
                self.beam.point2[0] = self.pos[0]
            else:
                self.beam.point1[1] = self.pos[1]
                self.beam.point2[1] = self.pos[1]

    def draw(self, offset):
        if self.orientation == "v":
            screen.blit(texture_lib["line_top"], (self.pos[0] + offset[0] - 40, self.pos[1] + offset[1] - 50))
            screen.blit(texture_lib["line_bottom"], (self.pos[0] + offset[0] - 40, self.pos[1] + offset[1] - 40 + self.height))
        else:
            screen.blit(texture_lib["line_right"], (self.pos[0] + offset[0] - 50, self.pos[1] + offset[1] - 40))
            screen.blit(texture_lib["line_left"], (self.pos[0] + offset[0] + self.height - 40, self.pos[1] + offset[1] - 40))

class CenterSlice(Obstacles):
    def __init__(self, damage, speed, boxed):
        Obstacles.__init__(self)
        self.boxed = boxed
        self.damage = damage
        self.radius = boxed*1.414

        self.angle = 0.0
        self.speed = speed
        self.pos = [0, 0]
        self.bounded = False
        self.attack = True
        self.dead_on_collide = False
        self.shade = 0.05

        self.current_rise = [0, 0, 0, 0]
        self.attack = True

    def update(self):
        self.angle += self.speed
        if self.angle > pi:
            self.angle -= 2 * pi
        self.current_rise[0] = cos(self.angle - self.shade) * self.radius
        self.current_rise[1] = sin(self.angle - self.shade) * self.radius
        self.current_rise[2] = cos(self.angle + self.shade) * self.radius
        self.current_rise[3] = sin(self.angle + self.shade) * self.radius

    def draw(self, offset):
        pygame.draw.polygon(screen, (170, 0, 0),
                            ((-self.current_rise[0] + offset[0], -self.current_rise[1] + offset[1]),
                             (self.current_rise[0] + offset[0], self.current_rise[1] + offset[1]),
                             (self.current_rise[2] + offset[0], self.current_rise[3] + offset[1]),
                             (-self.current_rise[2] + offset[0], -self.current_rise[3] + offset[1])))

        pygame.draw.polygon(screen, (170, 0, 0),
                            ((-self.current_rise[1] + offset[0], self.current_rise[0] + offset[1]),
                             (self.current_rise[1] + offset[0], -self.current_rise[0] + offset[1]),
                             (self.current_rise[3] + offset[0], -self.current_rise[2] + offset[1]),
                             (-self.current_rise[3] + offset[0], self.current_rise[2] + offset[1])))

    def collide_with(self, snake):
        for i in range(0, len(snake.hit_points), 2):
            for l in range(4):
                diff = self.angle + (l*pi/2) - get_angle(snake.hit_points[i][0], snake.hit_points[i][1])
                while diff > pi:
                    diff -= pi * 2
                if -self.shade < diff < self.shade:
                    return True
        return False
