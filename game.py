from grid import Grid
from pathlib import Path
from blockTypes import *
from hardDropEffect import HardDropEffect
from srs import get_wall_kicks
import random
import pygame

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOUNDS_DIR = PROJECT_ROOT / "sounds"

class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [L_Block(), J_Block(), I_Block(), O_Block(), S_Block(), T_Block(), Z_Block()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        self.held_block = None
        self.can_hold = True
        self.hard_drop_effects = []
        self.lock_delay = 500
        self.lock_timer = 0
        self.is_grounded = False
        self.lock_reset_count = 0
        self.max_lock_resets = 15
        self.grounded_time_total = 0       # NEW
        self.max_grounded_time = 5000      # NEW: hard cap, e.g. 5s
        self.rotate_sound = pygame.mixer.Sound(SOUNDS_DIR / "Sounds_rotate.ogg")
        self.clear_sound = pygame.mixer.Sound(SOUNDS_DIR / "Sounds_clear.ogg")

        pygame.mixer.music.load(SOUNDS_DIR / "Sounds_music.ogg")
        pygame.mixer.music.play(-1)

    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        self.score += move_down_points
        

    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [L_Block(), J_Block(), I_Block(), O_Block(), S_Block(), T_Block(), Z_Block()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def move_left(self):
        self.current_block.move(0, -1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, 1)

        else:
            self.reset_lock_delay()


    def move_right(self):
        self.current_block.move(0, 1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, -1)

        else:
            self.reset_lock_delay()

    def move_down(self):
        self.current_block.move(1, 0)

        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1, 0)
            self.is_grounded = True

        else:
            self.is_grounded = False
            self.lock_timer = 0
            self.lock_reset_count = 0
            self.grounded_time_total = 0
        
            
    def rotate(self):

        old_state = self.current_block.rotation_state
        self.current_block.rotate()
        new_state = self.current_block.rotation_state

        kicks = get_wall_kicks(
            self.current_block.id,
            old_state,
            new_state
        )

        for row_offset, col_offset in kicks:

            self.current_block.move(row_offset, col_offset)
            if self.block_inside() and self.block_fits():
                self.rotate_sound.play()
                self.reset_lock_delay()
                return

            # Undo this kick and try the next one
            self.current_block.move(-row_offset, -col_offset)


        # No kick worked, undo the rotation
        self.current_block.undo_rotation()

    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        self.is_grounded = False
        self.lock_timer = 0
        self.lock_reset_count = 0

        for position in tiles:
            self.grid.grid[position.row][position.col] = self.current_block.id

        self.current_block = self.next_block
        self.current_block.reset_position()

        self.next_block = self.get_random_block()

        # Allow holding again for the new piece
        self.can_hold = True

        rows_cleared = self.grid.clear_full_rows()

        if rows_cleared > 0:
            self.clear_sound.play()
            self.update_score(rows_cleared, 0)

        if self.block_fits() == False:
            self.game_over = True

    def reset_lock_delay(self):
        if self.is_grounded and self.lock_reset_count < self.max_lock_resets:
            self.lock_timer = 0
            self.lock_reset_count += 1

    def update_effects(self):

        for effect in self.hard_drop_effects:
            effect.update()

        self.hard_drop_effects = [
            e for e in self.hard_drop_effects
            if e.alive()
        ]

    def hard_drop(self):

        start_tiles = self.current_block.get_cell_positions()

        distance = 0

        while True:

            self.current_block.move(1,0)

            if not self.block_inside() or not self.block_fits():
                self.current_block.move(-1,0)
                break

            distance += 1

        end_tiles = self.current_block.get_cell_positions()

        self.hard_drop_effects.append(
            HardDropEffect(
                self.current_block,
                start_tiles,
                end_tiles
            )
        )

        self.update_score(0, distance * 2)

        self.lock_block()

    def hold_piece(self):

        # Prevent holding multiple times per piece
        if self.can_hold == False:
            return

        self.can_hold = False

        # If there is nothing in hold
        if self.held_block is None:

            self.held_block = self.current_block
            self.held_block.reset_position()
            self.current_block = self.next_block
            self.next_block = self.get_random_block()

        else:
            # Swap current and held pieces
            temp = self.current_block
            
            self.current_block = self.held_block

            self.held_block = temp
            self.held_block.reset_position()
            

        # Reset the new current piece
        self.current_block.reset_position()
        print(
            self.held_block.id,
            self.held_block.row_offset,
            self.held_block.col_offset,
            self.held_block.rotation_state
        )

    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.col) == False:
                return False
        return True

    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.col) == False:
                return False
        return True

    def reset(self):
        self.grid.reset()
        self.blocks = [L_Block(), J_Block(), I_Block(), O_Block(), S_Block(), T_Block(), Z_Block()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0

    def get_ghost_block(self):
        ghost = self.current_block.copy()

        while True:
            ghost.move(1, 0)

            tiles = ghost.get_cell_positions()

            valid = True

            for tile in tiles:
                if not self.grid.is_inside(tile.row, tile.col):
                    valid = False
                    break

                if not self.grid.is_empty(tile.row, tile.col):
                    valid = False
                    break

            if not valid:
                ghost.move(-1, 0)
                break

        return ghost

    def update(self, dt):

        self.update_effects()

        # Only run lock delay if touching the ground
        if self.is_grounded:
            self.lock_timer += dt
            self.grounded_time_total += dt
            if self.lock_timer >= self.lock_delay or self.grounded_time_total >= self.max_grounded_time:
                self.lock_block()

    def draw(self, screen):

        self.grid.draw(screen)
        
        for effect in self.hard_drop_effects:
            effect.draw(screen, 11, 11)

        # Draw ghost block
        ghost = self.get_ghost_block()
        ghost.draw_ghost(screen, 11, 11)

        # Draw current falling block
        self.current_block.draw(screen, 11, 11)

        # Draw next block preview
        if self.next_block.id == 3:
            self.next_block.draw(screen, 255, 240)
        elif self.next_block.id == 4:
            self.next_block.draw(screen, 255, 230)
        else:
            self.next_block.draw(screen, 270, 220)

        # Draw held block preview
        if self.held_block is not None:
        
            if self.held_block.id == 3:
                self.held_block.draw_preview(screen, 345, 440)
            elif self.held_block.id == 4:
                self.held_block.draw_preview(screen, 375, 450)
            else:
                self.held_block.draw_preview(screen, 360, 450)

