from snake import *
from map import *
from hud import *

class Game:
    def __init__(self):
        self.snake_move_cycle = Cycle(2, 0)

        self.map = map1

        self.snake = None

        self.scene = None

        self.info_hud = None

    def get_offset(self):
        return -int(self.snake.position[0] - screen_width/2), -int(self.snake.position[1] - screen_height/2)

    def start_scene(self, scene):
        self.scene = scene

    def start(self):
        self.snake = Snake(self)
        for _ in range(5):
            self.snake.grow()
        self.info_hud = InfoBar(self.snake)
        self.map.set_snake(self.snake)
        self.update()

    def draw(self):
        if not self.scene:
            self.map.draw_background(self.get_offset())
            self.snake.draw()
            self.map.draw(self.get_offset())

            self.info_hud.draw()
        else:
            self.scene.draw()

    def handle_event(self, event):
        if not self.scene:
            pass
        else:
            self.scene.handle_event(event)

    def update(self):
        if not self.scene:
            self.snake.set_direction(env["mouse_direction"])

            self.map.update()

            if self.snake_move_cycle.get() == 0:
                self.snake.crawl()
            self.snake.update()

            self.info_hud.update()
        else:
            self.scene.update()
            if self.scene.is_ended():
                self.scene = None
