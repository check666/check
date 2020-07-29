from config import *
from fights import *

class Wall:
    def __init__(self, x, y, w, h):
        self.pos = [x, y]
        self.deme = [w, h]

    def draw(self, offset):
        pygame.draw.rect(screen, (100, 100, 100), pygame.Rect((self.pos[0] + offset[0], self.pos[1] + offset[1])
                                                              , self.deme), 4)

class Map:
    def __init__(self):
        self.walls = []
        self.exp_balls = []
        self.deme = [300, 300]
        self.snake = None
        self.attacks = []
        self.add_beam([0, -300], 600, "v", 40)

    def add_beam(self, position, length, direction, width=30):
        self.attacks.append(Beam(position, length, direction, width))

    def set_snake(self, snake):
        self.snake = snake

    def add_wall(self, x, y, w, h):
        self.walls.append(Wall(x, y, w, h))

    def draw_background(self, offset):
        pygame.draw.rect(screen, (50, 50, 50),
                         pygame.Rect(offset[0] - self.deme[0], offset[1] - self.deme[1], self.deme[0] * 2,
                                     self.deme[1] * 2))

    def draw(self, offset):
        for i in range(len(self.walls)-1, -1, -1):
            self.walls[i].draw(offset)
        for i in range(len(self.exp_balls)-1, -1, -1):
            self.exp_balls[i].draw(offset)
        for i in range(len(self.attacks) - 1, -1, -1):
            self.attacks[i].draw(offset)

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
            if self.attacks[i].dead:
                del self.attacks[i]

        if len(self.exp_balls) < 10:
            self.exp_balls.append(ExpBall((random.randint(-self.deme[0], self.deme[0]),
                                           random.randint(-self.deme[1], self.deme[1]))))

        if not self.attacks:
            self.add_beam([0, -300], 600, "v", 40)

map1 = Map()
