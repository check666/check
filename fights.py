from config import *

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
    def __init__(self, pos, length, direction, width=30, pre_t=120, last_t=2, color=(242, 245, 66), damage=10):
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
                if not(self.pos[0] - self.width > max(snake.hit_points[i][0], snake.hit_points[i+2][0]) or
                        self.pos[0] + self.width < min(snake.hit_points[i][0], snake.hit_points[i+2][0])):
                    return True

        elif self.direction == "h":
            for i in range(0, len(snake.hit_points)-2, 2):
                if not (self.pos[1] - self.width > max(snake.hit_points[i][1], snake.hit_points[i + 2][1]) or
                        self.pos[1] + self.width < min(snake.hit_points[i][1], snake.hit_points[i + 2][1])):
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
        self.attack_cycle = RandCycle(2, 90, (1, 2))
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

    def draw(self, offset):
        if self.attacking:
            screen.blit(texture_lib["one_cannon"], (self.pos[0]+offset[0], self.pos[1]+offset[1]),
                        pygame.Rect(0, self.attack_ani_cycle.get() * 80, 80, 80))
        else:
            screen.blit(texture_lib["one_cannon"], (self.pos[0] + offset[0], self.pos[1] + offset[1]),
                        pygame.Rect(0, 0, 80, 80))

