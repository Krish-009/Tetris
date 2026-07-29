import sys
import pygame 

from game import Game
from colors import Colors
from inputManager import Input_Manager, Action


#Initilization
pygame.init()

screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

game = Game()
input_manager = Input_Manager()


# Fonts
title_font = pygame.font.Font(None, 40)
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("Game Over", True, Colors.white)
hold_surface = title_font.render("Hold", True, Colors.white)


# UI Layout
score_rect = pygame.Rect(320, 50, 170, 60)
next_rect = pygame.Rect(320, 160, 170, 180)
hold_rect = pygame.Rect(320, 390, 170, 180)

pygame.Rect()


# Timers
GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 400)


# Main Game Loop
while True:


    # Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Game Reset
        if event.type == pygame.KEYDOWN and game.game_over and event.key == pygame.K_RETURN:
                game.game_over = False
                game.reset()

        input_manager.process_event(event)

        # Gravity
        if event.type == GAME_UPDATE and not game.game_over and not game.grid.is_clearing:
            game.move_down()


    # Input Update
    input_manager.update()

    actions = input_manager.get_actions()

    for action in actions:

        if game.game_over or game.grid.is_clearing:
            continue

        if action == Action.MOVE_LEFT:
            game.move_left()

        elif action == Action.MOVE_RIGHT:
            game.move_right()

        elif action == Action.SOFT_DROP:
            game.move_down()
            game.update_score(0, 1)

        elif action == Action.ROTATE:
            game.rotate()

        elif action == Action.HOLD:
            game.hold_piece()

        elif action == Action.HARD_DROP:
            game.hard_drop()


    # Render
    score_val_surface = title_font.render(str(game.score), True, Colors.white)     

    screen.fill(Colors.dark_blue)
    screen.blit(score_surface, (365, 20, 50, 50))
    screen.blit(next_surface, (375, 130, 50, 50))
    screen.blit(hold_surface, (375, 360, 50, 50))

    if game.game_over == True:
        screen.blit(game_over_surface, (330, 450, 50, 50))
    
    pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
    screen.blit(score_val_surface, score_val_surface.get_rect(center = score_rect.center))

    pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
    pygame.draw.rect(screen, Colors.light_blue, hold_rect, 0, 10)
    game.draw(screen)

    game.update_effects()
    pygame.display.update()
    game.update(clock.tick(60))
    




