import pygame
from pygame.locals import *

import sys

from grid import Grid


WIN_SIZE = 640, 420
TARGET_FPSs = [6, 12, 24, 48]
CELL_SIZE = 10


class Application:

    def __init__(self):
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Cellular Automata')
        self.screen = pygame.display.set_mode(WIN_SIZE)

        self.grid = Grid(*WIN_SIZE, CELL_SIZE)
        self.paused = True
        self.speed = 3

    def run(self):
        while True:

            frame_time_ms = self.clock.tick(TARGET_FPSs[self.speed])

            new_caption = f'Cellular Automata (FPS: {TARGET_FPSs[self.speed]})'
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
                        self.speed = min(self.speed + 1, len(TARGET_FPSs) - 1)
                    elif event.key == K_DOWN:
                        self.speed = max(self.speed - 1, 0)
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.grid.add_cell(*event.pos)
                    elif event.button == 3:
                        self.grid.remove_cell(*event.pos)

            if not self.paused:
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
