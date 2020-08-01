from game import *
from scene import *

g = Game()
g.start()

#g.start_scene(TalkScene("snake_1", "snake_2", [(1, "哈喽"), (1, "你也好啊"), (2, "我又说一句"), (1, "我再来一句")]))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            env["mouse_x"] = pygame.mouse.get_pos()[0]
            env["mouse_y"] = pygame.mouse.get_pos()[1]
            env["mouse_direction"] = atan2(env["mouse_y"] - screen_height/2, env["mouse_x"] - screen_width/2)
        g.handle_event(event)
    g.update()

    screen.fill(0)
    g.draw()
    pygame.display.flip()

    clock.tick(40)