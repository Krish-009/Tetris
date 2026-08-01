import sys
import pygame 

from game import Game
from colors import Colors
from inputManager import Input_Manager, Action


#Initilization
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 620
FPS = 60
GRAVITY_INTERVAL_MS = 400

FONT_SIZE = 40
TEXT_COLOR = Colors.white
PANEL_RADIUS = 10

SIDEBAR_X = 320
SIDEBAR_WIDTH = 170

# UI Layout
SCORE_RECT = pygame.Rect(320, 50, 170, 60)
NEXT_RECT = pygame.Rect(320, 160, 170, 180)
HOLD_RECT = pygame.Rect(320, 390, 170, 180)

SCORE_LABEL_POS = (365, 20)
NEXT_LABEL_POS = (375, 130)
HOLD_LABEL_POS = (375, 360)
GAME_OVER_LABEL_POS = (330, 450)

GAME_UPDATE = pygame.USEREVENT


class UI:

    def __init__(self):
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.score_label = self.font.render("Score", True, TEXT_COLOR)
        self.next_label = self.font.render("Next", True, TEXT_COLOR)
        self.hold_label = self.font.render("Hold", True, TEXT_COLOR)
        self.game_over_label = self.font.render("Game Over", True, TEXT_COLOR)

        self._cached_score = None
        self._score_surface = None

    def score_surface(self, score):
        """Only re-render the score text when the score actually changes."""
        if score != self._cached_score:
            self._cached_score = score
            self._score_surface = self.font.render(str(score), True, TEXT_COLOR)
        return self._score_surface


def create_window():
    pygame.display.set_caption("Tetris")
    return pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


def handle_events(game, input_manager):
    """Process the pygame event queue. Returns False when the app should quit."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and game.game_over:
            game.game_over = False
            game.reset()

        input_manager.process_event(event)

        if event.type == GAME_UPDATE and not game.game_over and not game.grid.is_clearing:
            game.move_down()

    return True


def apply_action(game, action):
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


def process_actions(game, actions):
    if game.game_over or game.grid.is_clearing:
        return

    for action in actions:
        apply_action(game, action)


def render(screen, game, ui):
    screen.fill(Colors.dark_blue)

    screen.blit(ui.score_label, SCORE_LABEL_POS)
    screen.blit(ui.next_label, NEXT_LABEL_POS)
    screen.blit(ui.hold_label, HOLD_LABEL_POS)

    if game.game_over:
        screen.blit(ui.game_over_label, GAME_OVER_LABEL_POS)

    pygame.draw.rect(screen, Colors.light_blue, SCORE_RECT, 0, PANEL_RADIUS)
    score_surface = ui.score_surface(game.score)
    screen.blit(score_surface, score_surface.get_rect(center=SCORE_RECT.center))

    pygame.draw.rect(screen, Colors.light_blue, NEXT_RECT, 0, PANEL_RADIUS)
    pygame.draw.rect(screen, Colors.light_blue, HOLD_RECT, 0, PANEL_RADIUS)

    game.draw(screen)


def main():
    pygame.init()

    screen = create_window()
    clock = pygame.time.Clock()

    game = Game()
    input_manager = Input_Manager()
    ui = UI()

    pygame.time.set_timer(GAME_UPDATE, GRAVITY_INTERVAL_MS)

    running = True
    while running:
        running = handle_events(game, input_manager)
        if not running:
            break

        input_manager.update()
        process_actions(game, input_manager.get_actions())

        render(screen, game, ui)
        game.update_effects()
        pygame.display.update()
        game.update(clock.tick(FPS))

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()