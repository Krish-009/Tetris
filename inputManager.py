import pygame
from enum import Enum, auto

class Action(Enum):
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    SOFT_DROP = auto()
    ROTATE = auto()
    HARD_DROP = auto()
    HOLD = auto()
    PAUSE = auto()

class Input_Manager:
    DAS = 150
    ARR = 40

    def __init__(self):
        self.left_held = False
        self.right_held = False
        self.down_held = False

        self.left_start = 0
        self.right_start = 0

        self.left_repeat = 0
        self.right_repeat = 0

        self.actions = []

    # ----------------
    # Event Processing
    # ----------------
    def process_event(self, event):

        if event.type == pygame.KEYDOWN:
            self.handle_keydown(event.key)
        
        elif event.type == pygame.KEYUP:
                self.handle_keyup(event.key)

    def handle_keydown(self, key):
        now = pygame.time.get_ticks()

        if key == pygame.K_LEFT:
            self.left_held = True
            self.left_start = now
            self.left_repeat = now
            self.actions.append(Action.MOVE_LEFT)

        elif key == pygame.K_RIGHT:
            self.right_held = True
            self.right_start = now
            self.right_repeat = now
            self.actions.append(Action.MOVE_RIGHT)

        elif key == pygame.K_DOWN:
            self.down_held = True

        elif key == pygame.K_UP:
            self.actions.append(Action.ROTATE)

        elif key == pygame.K_SPACE:
            self.actions.append(Action.HARD_DROP)

        elif key == pygame.K_c:
            self.actions.append(Action.HOLD)

        elif key == pygame.K_ESCAPE:
            self.actions.append(Action.PAUSE)

    def handle_keyup(self, key):
        if key == pygame.K_LEFT:
            self.left_held = False

        elif key == pygame.K_RIGHT:
            self.right_held = False

        elif key == pygame.K_DOWN:
            self.down_held = False

    # ---------
    # DAS / ARR
    # ---------
    def update(self):
        now = pygame.time.get_ticks()

        self.update_horizontal(
            now,
            held=self.left_held,
            start=self.left_start,
            last_repeat=self.left_repeat,
            action=Action.MOVE_LEFT
        )

        self.update_horizontal(
            now,
            held=self.right_held,
            start=self.right_start,
            last_repeat=self.right_repeat,
            action=Action.MOVE_RIGHT
        )

        if self.down_held:
            self.actions.append(Action.SOFT_DROP)

    def update_horizontal(self, now, held, start, last_repeat, action):
        if not held:
            return

        if now - start < self.DAS:
            return

        if now - last_repeat >= self.ARR:
            self.actions.append(action)

            if action == Action.MOVE_LEFT:
                self.left_repeat = now
            else:
                self.right_repeat = now

    # -------
    # Actions
    # -------
    def get_actions(self):
        
        current_actions = self.actions.copy()
        self.actions.clear()

        return current_actions
