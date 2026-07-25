import pygame
from enum import Enum

class Action(Enum):
    MOVE_LEFT = 1
    MOVE_RIGHT = 2
    SOFT_DROP = 3
    ROTATE = 4
    HARD_DROP = 5
    HOLD = 6
    PAUSE = 7

class Input_Manager:
    def __init__(self):
        self.left_held = False
        self.right_held = False
        self.down_held = False

        self.das = 150
        self.arr = 40

        self.left_start_time = 0
        self.right_start_time = 0

        self.last_left_move = 0
        self.last_right_move = 0

        self.action = []

    def process_event(self, event):

        if event.type == pygame.KEYDOWN:

            # Left Movement
            if event.key == pygame.K_LEFT:
                self.left_held = True

                self.action.append(Action.MOVE_LEFT)

                current_time = pygame.time.get_ticks()
                self.left_start_time = current_time
                self.last_left_move = current_time

            # Right Movement
            elif event.key == pygame.K_RIGHT:
                self.right_held = True

                self.action.append(Action.MOVE_RIGHT)

                current_time = pygame.time.get_ticks()
                self.right_start_time = current_time
                self.last_right_move = current_time

            # Soft Drop
            elif event.key == pygame.K_DOWN:
                self.down_held = True

            # Rotation
            elif event.key == pygame.K_UP:
                self.action.append(Action.ROTATE)

            # Hard Drop
            elif event.key == pygame.K_SPACE:
                self.action.append(Action.HARD_DROP)

            # Hold
            elif event.key == pygame.K_c:
                self.action.append(Action.HOLD)

            # Pause
            elif event.key == pygame.K_ESCAPE:
                self.action.append(Action.PAUSE)

        elif event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT:
                self.left_held = False

            if event.key == pygame.K_RIGHT:
                self.right_held = False

            if event.key == pygame.K_DOWN:
                self.down_held = False

    def update(self):
        current_time = pygame.time.get_ticks()

        # LEFT DAS/ARR
        if self.left_held:

            # Wait for DAS
            if current_time - self.left_start_time >= self.das:

                # Move every ARR milliseconds
                if current_time - self.last_left_move >= self.arr:
                    self.actions.append(Action.MOVE_LEFT)
                    self.last_left_move = current_time

        # RIGHT DAS/ARR
        if self.right_held:

            if current_time - self.right_start_time >= self.das:

                if current_time - self.last_right_move >= self.arr:
                    self.actions.append(Action.MOVE_RIGHT)
                    self.last_right_move = current_time

        # Soft drop
        if self.down_held:
            self.actions.append(Action.SOFT_DROP)

    def get_actions(self):
        
        current_actions = self.actions.copy()
        self.actions.clear()

        return current_actions


            
