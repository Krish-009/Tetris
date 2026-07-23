import pygame, sys
from grid import Grid
from blockTypes import *

pygame.init()

screen = pygame.display.set_mode((300, 600))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

screen_color = (44, 44, 127)

game_grid = Grid()

block = I_Block()


game_grid.print_grid()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(screen_color)
    game_grid.draw(screen)
    block.draw(screen)

    pygame.display.update()
    clock.tick(60)




