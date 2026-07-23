from grid import Grid
from blockTypes import *
import random

class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [L_Block(), J_Block(), I_Block(), O_Block(), S_Block(), T_Block(), Z_Block()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False

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

    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.col] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        self.grid.clear_full_rows()
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

    def draw(self, screen):
            self.grid.draw(screen)
            self.current_block.draw(screen)
