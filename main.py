import pygame
from pygame.locals import *

import sys

from grid import Grid


WIN_SIZE = 640, 480
TARGET_FPS = 0

CELL_SIZE = 20

GEN_TIME_MS = 500
SPEED_MULTIPLIERS = [1, 2, 4, 8, 16]


class Application:

    def __init__(self):
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Cellular Automata')
        self.screen = pygame.display.set_mode(WIN_SIZE)

        self.grid = Grid(*WIN_SIZE, CELL_SIZE)
        self.paused = True
        self.current_gen_time_ms = 0
        self.current_speed_index = 2

        self.lmb_pressed = False

    def run(self):
        while True:

            frame_time_ms = self.clock.tick(TARGET_FPS)

            new_caption = f'Cellular Automata ' \
                          f'(FPS: {self.clock.get_fps():.2f}) ' \
                          f'({SPEED_MULTIPLIERS[self.current_speed_index]}x speed)'
            if self.paused:
                new_caption += ' (paused)'
            pygame.display.set_caption(new_caption)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.terminate()
                    elif event.key == K_SPACE:
                        self.paused = not self.paused
                    elif event.key == K_UP:
                        self.current_speed_index = min(self.current_speed_index + 1, len(SPEED_MULTIPLIERS) - 1)
                    elif event.key == K_DOWN:
                        self.current_speed_index = max(self.current_speed_index - 1, 0)
                    elif event.key == K_c:
                        self.grid.clear()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.lmb_pressed = True
                        # self.grid.add_cell(*event.pos)
                    elif event.button == 3:
                        self.grid.remove_cell(*event.pos)
                elif event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        self.lmb_pressed = False

            if self.lmb_pressed:
                self.grid.add_cell(*pygame.mouse.get_pos())

            if not self.paused:
                self.current_gen_time_ms += frame_time_ms
                if self.current_gen_time_ms >= GEN_TIME_MS / SPEED_MULTIPLIERS[self.current_speed_index]:
                    self.current_gen_time_ms = 0
                    self.grid.update()

            self.screen.fill((255, 255, 255))
            self.grid.draw(self.screen)
            pygame.display.update()

    def terminate(self):
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    app = Application()
    app.run()
