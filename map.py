from config import *
from fights import *

class Level:
    def __init__(self):
        pass

    def is_passed(self):
        return False

class Map(Level):
    def __init__(self):
        Level.__init__(self)
        self.objects = []
        self.exp_balls = []
        self.deme = [300, 300]
        self.snake = None
        self.attacks = []
        self.food_count = 5

        self.boarder_cycle = ReCycle(6, 1)

    def draw_boarder(self, offset):
        c = self.boarder_cycle.get()
        pygame.draw.line(screen, (255, 255, 255),
                         (-self.deme[0] + offset[0] + c, -self.deme[1] + offset[1]),
                         (-self.deme[0] + offset[0] + c, self.deme[1] + offset[1]), 2)
        pygame.draw.line(screen, (255, 255, 255),
                         (-self.deme[0] + offset[0] - c, -self.deme[1] + offset[1]),
                         (-self.deme[0] + offset[0] - c, self.deme[1] + offset[1]), 2)

        pygame.draw.line(screen, (255, 255, 255),
                         (self.deme[0] + offset[0] + c, -self.deme[1] + offset[1]),
                         (self.deme[0] + offset[0] + c, self.deme[1] + offset[1]), 2)
        pygame.draw.line(screen, (255, 255, 255),
                         (self.deme[0] + offset[0] - c, -self.deme[1] + offset[1]),
                         (self.deme[0] + offset[0] - c, self.deme[1] + offset[1]), 2)

        pygame.draw.line(screen, (255, 255, 255),
                         (self.deme[0] + offset[0], self.deme[1] + offset[1] + c),
                         (-self.deme[0] + offset[0], self.deme[1] + offset[1] + c), 2)
        pygame.draw.line(screen, (255, 255, 255),
                         (self.deme[0] + offset[0], self.deme[1] + offset[1] - c),
                         (-self.deme[0] + offset[0], self.deme[1] + offset[1] - c), 2)

        pygame.draw.line(screen, (255, 255, 255),
                         (self.deme[0] + offset[0], -self.deme[1] + offset[1] + c),
                         (-self.deme[0] + offset[0], -self.deme[1] + offset[1] + c), 2)
        pygame.draw.line(screen, (255, 255, 255),
                         (self.deme[0] + offset[0], -self.deme[1] + offset[1] - c),
                         (-self.deme[0] + offset[0], -self.deme[1] + offset[1] - c), 2)

        pygame.draw.rect(screen, (255, 255, 255),
                         pygame.Rect(offset[0] - self.deme[0] - 15, offset[1] - self.deme[1] - 15, 30,
                                     30))
        pygame.draw.rect(screen, (255, 255, 255),
                         pygame.Rect(offset[0] + self.deme[0] - 15, offset[1] - self.deme[1] - 15, 30,
                                     30))
        pygame.draw.rect(screen, (255, 255, 255),
                         pygame.Rect(offset[0] - self.deme[0] - 15, offset[1] + self.deme[1] -15, 30,
                                     30))
        pygame.draw.rect(screen, (255, 255, 255),
                         pygame.Rect(offset[0] + self.deme[0] - 15, offset[1] + self.deme[1] - 15, 30,
                                     30))

    def add_beam(self, position, length, direction, width=30):
        self.attacks.append(Beam(position, length, direction, width))

    def add_bullet(self, position, speed, radius, damage):
        self.attacks.append(Bullet(damage, radius, position[0], position[1], speed[0], speed[1]))

    def set_snake(self, snake):
        self.snake = snake

    def draw_background(self, offset):
        pygame.draw.rect(screen, (70, 70, 70),
                         pygame.Rect(offset[0] - self.deme[0], offset[1] - self.deme[1], self.deme[0] * 2,
                                     self.deme[1] * 2))

    def draw(self, offset):
        for i in range(len(self.exp_balls)-1, -1, -1):
            self.exp_balls[i].draw(offset)
        for i in range(len(self.attacks) - 1, -1, -1):
            self.attacks[i].draw(offset)
        for i in range(len(self.objects) - 1, -1, -1):
            self.objects[i].draw(offset)

        if self.snake.outofbound:
            screen.blit(texture_lib["danger"], (0, 0))

        self.draw_boarder(offset)

    def update(self):
        for i in range(len(self.exp_balls)-1, -1, -1):
            if get_distance(self.snake.position, self.exp_balls[i].pos) < 20:
                self.snake.current_exp += self.exp_balls[i].points
                del self.exp_balls[i]

        for i in range(len(self.attacks)-1, -1, -1):
            self.attacks[i].update()
            if self.attacks[i].attack:
                if self.attacks[i].collide_with(self.snake):
                    self.snake.hp -= self.attacks[i].damage
            if self.attacks[i].bounded:
                if self.attacks[i].pos[0] > self.deme[0] or \
                     self.attacks[i].pos[0] < -self.deme[0] or \
                     self.attacks[i].pos[1] > self.deme[1] or \
                     self.attacks[i].pos[1] < -self.deme[1]:
                    self.attacks[i].dead = True
            if self.attacks[i].dead:
                del self.attacks[i]

        for i in range(len(self.objects)-1, -1, -1):
            self.objects[i].update()
            if self.objects[i].dead:
                del self.objects[i]

        if len(self.exp_balls) < self.food_count:
            self.exp_balls.append(ExpBall((random.randint(-self.deme[0], self.deme[0]),
                                           random.randint(-self.deme[1], self.deme[1]))))

        if (self.snake.position[0] < -self.deme[0] or
                self.snake.position[0] > self.deme[0] or
                self.snake.position[1] < -self.deme[1] or
                self.snake.position[1] > self.deme[1]):
            self.snake.outofbound = True
        else:
            self.snake.outofbound = False

class Level1(Map):
    def __init__(self):
        Map.__init__(self)
        self.deme[0] = 200
        self.deme[1] = 200

    def is_passed(self):
        if self.snake.level >= 3:
            return True
        return False

class Level2(Map):
    def __init__(self):
        Map.__init__(self)
        self.deme[0] = 250
        self.deme[1] = 250

        self.objects.append(OneCanon((-310, 100)))
        self.objects.append(OneCanon((-310, -100)))

    def is_passed(self):
        if self.snake.level >= 5:
            return True
        return False

    def update(self):
        Map.update(self)
        if self.objects[0].cast:
            self.add_bullet((self.objects[0].pos[0]+70, self.objects[0].pos[1]+40), (5, 0), 15, 10)
        if self.objects[1].cast:
            self.add_bullet((self.objects[1].pos[0]+70, self.objects[1].pos[1]+40), (5, 0), 15, 10)

