from config import *

class ChatBox:
    def __init__(self, text, pos, start):
        self.start = start
        self.width = 200
        self.lines = []
        self.stage = 0
        self.tick = 0
        self.show_time = 10
        self.dead = False
        self.click_cycle = Cycle(2, 8)
        while text:
            self.lines.append(text[0])
            text = text[1:]
            flag = True
            while flag and text:
                if chat_font.size(self.lines[-1] + text[0])[0] > self.width:
                    flag = False
                else:
                    self.lines[-1] += text[0]
                    text = text[1:]
        for i in range(len(self.lines)):
            self.lines[i] = chat_font.render(self.lines[i], True, (255, 255, 255))
        self.height = len(self.lines * chat_font_size) + 10
        self.pos = (pos[0], pos[1] - self.height)
        self.rect = pygame.Rect((self.pos[0] - 5, self.pos[1] - 3),
                                (self.width + 10, self.height))

    def draw(self):
        if self.stage == 0:
            if self.tick < self.show_time:
                dif1 = ((self.pos[0] + self.width / 2 - 15 - self.start[0])/self.show_time*self.tick,
                         (self.pos[1] + self.height - 3 - self.start[1])/self.show_time*self.tick)
                dif2 = ((self.pos[0] + self.width / 2 + 15 - self.start[0])/self.show_time*self.tick,
                        (self.pos[1] + self.height - 3 - self.start[1])/self.show_time*self.tick)
                pygame.draw.line(screen, (255, 255, 255), self.start,
                                 (self.start[0] + dif1[0], self.start[1] + dif1[1]), 2)
                pygame.draw.line(screen, (255, 255, 255), self.start,
                                 (self.start[0] + dif2[0], self.start[1] + dif2[1]), 2)
            else:
                pygame.draw.line(screen, (255, 255, 255), self.start,
                                 (self.pos[0] + self.width / 2 - 15, self.pos[1] + self.height - 3), 2)
                pygame.draw.line(screen, (255, 255, 255), self.start,
                                 (self.pos[0] + self.width / 2 + 15, self.pos[1] + self.height - 3), 2)
            self.tick += 1
            if self.tick > self.show_time + 5:
                self.stage += 1
                self.tick = 0
        elif self.stage == 1:
            for i in range(len(self.lines)):
                screen.blit(self.lines[i], (self.pos[0], self.pos[1] + i * chat_font_size))
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
            pygame.draw.line(screen, (255, 255, 255), self.start,
                             (self.pos[0] + self.width/2 - 15, self.pos[1] + self.height - 3), 2)
            pygame.draw.line(screen, (255, 255, 255), self.start,
                             (self.pos[0] + self.width / 2 + 15, self.pos[1] + self.height - 3), 2)
            if self.tick < 60:
                self.tick += 1
            else:
                screen.blit(texture_lib["mouse_click"], (self.pos[0] + self.width - 10, self.pos[1] + 10),
                            pygame.Rect(0, 25*self.click_cycle.get(), 25, 25))

class TalkScene:
    def __init__(self, character1, character2, chats):
        self.c1 = "close_" + character1
        self.c2 = "close_" + character2
        self.stage = 0
        self.stage_tick = 0
        self.stage_duration = [50, 0, 25]
        self.chats = chats[1:]
        self.current_chat = None
        if chats[0][0] == 1:
            self.current_chat = ChatBox(chats[0][1], (130, 200), (180, 240))
        elif chats[0][0] == 2:
            self.current_chat = ChatBox(chats[0][1], (270, 200), (420, 240))

    def is_ended(self):
        return self.stage == 3

    def next_chat(self):
        chat = self.chats.pop(0)
        if chat[0] == 1:
            self.current_chat = ChatBox(chat[1], (130, 200), (180, 240))
        elif chat[0] == 2:
            self.current_chat = ChatBox(chat[1], (270, 200), (420, 240))

    def handle_event(self, event):
        if self.current_chat:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.current_chat.stage == 1:
                    self.current_chat.dead = True
                elif self.current_chat.stage == 0:
                    self.current_chat.stage = 1
                    self.current_chat.tick = 0

    def update(self):
        if self.stage == 1:
            if not self.chats and (not self.current_chat or self.current_chat.dead):
                self.stage_tick = 0
                self.stage += 1
            elif self.current_chat.dead:
                self.next_chat()
        else:
            self.stage_tick += 1
            if self.stage_tick > self.stage_duration[self.stage]:
                self.stage_tick = 0
                self.stage += 1

    def draw(self):
        if self.stage == 0:
            if self.stage_tick < 25:
                screen.blit(texture_lib[self.c1], (self.stage_tick*12 - 300, 250))
            else:
                screen.blit(texture_lib[self.c1], (0, 250))
                screen.blit(texture_lib[self.c2], (600 - (self.stage_tick-25) * 12, 250))

        elif self.stage == 1:
            self.current_chat.draw()
            screen.blit(texture_lib[self.c1], (0, 250))
            screen.blit(texture_lib[self.c2], (300, 250))
        elif self.stage == 2:
            screen.blit(texture_lib[self.c1], (-self.stage_tick*13, 250))
            screen.blit(texture_lib[self.c2], (300+self.stage_tick*13, 250))
        else:
            screen.blit(texture_lib[self.c1], (0, 250))
            screen.blit(texture_lib[self.c2], (300, 250))
