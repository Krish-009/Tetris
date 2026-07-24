from grid import Grid
from pathlib import Path
from blockTypes import *
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


    def move_right(self):
        self.current_block.move(0, 1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, -1)

    def move_down(self):
        self.current_block.move(1, 0)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1, 0)
            self.lock_block()
            
    def rotate(self):
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.undo_rotation()
        else:
            self.rotate_sound.play()

    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.col] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        if rows_cleared > 0:
            self.clear_sound.play()
            self.update_score(rows_cleared, 0)
        if self.block_fits() == False:
            self.game_over = True
        

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

    def draw(self, screen):
            self.grid.draw(screen)
            self.current_block.draw(screen, 11, 11)
            if self.next_block.id == 3:
                self.next_block.draw(screen, 255, 290)
            elif self.next_block.id == 4:
                self.next_block.draw(screen, 255, 280)
            else:
                self.next_block.draw(screen, 270, 270)

