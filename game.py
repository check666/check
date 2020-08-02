from snake import *
from map import *
from hud import *
from menu import *

class Game:
    def __init__(self):
        self.snake_move_cycle = Cycle(2, 1)

        self.map = Level1()

        self.snake = None

        self.scene = None

        self.info_hud = None

        self.menu = LevelSelect()

    def get_offset(self):
        return -int(self.snake.position[0] - screen_width/2), -int(self.snake.position[1] - screen_height/2)

    def start_scene(self, scene):
        self.scene = scene

    def start(self):
        self.map = Level5()
        self.snake = Snake(self)
        for _ in range(5):
            self.snake.grow()
        self.info_hud = InfoBar(self.snake)
        self.map.set_snake(self.snake)
        self.update()

    def draw(self):
        if self.menu:
            self.menu.draw()
        elif not self.scene:
            self.map.draw_background(self.get_offset())
            self.snake.draw()
            self.map.draw(self.get_offset())

            self.info_hud.draw()
        else:
            self.scene.draw()

    def handle_event(self, event):
        if self.menu:
            result = self.menu.handle_event(event)
            if result != -1:
                self.start()
                self.menu = None
        elif not self.scene:
            pass
        else:
            self.scene.handle_event(event)

    def update(self):
        if self.menu:
            self.menu.update()
        elif not self.scene:
            self.snake.set_direction(env["mouse_direction"])

            self.map.update()

            if self.snake_move_cycle.get() == 0:
                self.snake.crawl()
            self.snake.update()

            self.info_hud.update()

            if self.map.is_passed():
                self.menu = LevelSelect()
        else:
            self.scene.update()
            if self.scene.is_ended():
                self.scene = None
