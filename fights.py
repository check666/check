from config import *

class Beam:
    def __init__(self, pos, length, direction, width=30, pre_t=120, last_t=2, color=(242, 245, 66), damage=10):
        self.damage = damage
        self.color = color
        self.pos = pos
        self.point1 = [pos[0], pos[1]]
        self.point2 = [pos[0], pos[1]]
        self.attack = False
        self.dead = False
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

class ExpBall:
    def __init__(self, pos, points=10):
        self.pos = pos
        self.points = points

    def draw(self, offset):
        pygame.draw.circle(screen, (255, 255, 255), (self.pos[0] + offset[0], self.pos[1] + offset[1]), self.points)

