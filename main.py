from game import *
from scene import *

if os.path.exists("save"):
    f = open("save", "r")
    c_level = int(f.read())
    f.close()
    g = Game(c_level)
else:
    g = Game()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            f = open("save", "w")
            f.write(str(g.current_level))
            f.close()
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