import pygame
import copy
from colors import Colors
from position import Position

class Block:
    def __init__(self, id):
        self.id = id
        self.cells = {}
        self.cell_size = 30
        self.row_offset = 0
        self.col_offset = 0
        self.rotation_state = 0
        self.colors = Colors.get_cell_colors()

    def move(self, rows, cols):
        self.row_offset += rows
        self.col_offset += cols

    def get_cell_positions(self):
        tiles = self.cells[self.rotation_state]
        moved_tiles = []
        for position in tiles:
            position = Position(position.row + self.row_offset, position.col + self.col_offset)
            moved_tiles.append(position)
        return moved_tiles

    def rotate(self):
        self.rotation_state += 1
        if self.rotation_state == len(self.cells):
            self.rotation_state = 0

    def undo_rotation(self):
        self.rotation_state -= 1
        if self.rotation_state < 0:
            self.rotation_state = len(self.cells) - 1

    def reset_position(self):
        self.row_offset = 0
        self.col_offset = 3
        self.rotation_state = 0

    def copy(self):
        return copy.deepcopy(self)

    def draw_ghost(self, screen, offset_x, offset_y):
        tiles = self.get_cell_positions()

        for tile in tiles:
            tile_rect = pygame.Rect(
                offset_x + tile.col * self.cell_size,
                offset_y + tile.row * self.cell_size,
                self.cell_size - 1,
                self.cell_size - 1
            )

            # Original block color
            color = self.colors[self.id]

            # Darkened fill
            ghost_fill = (
                color[0] // 3,
                color[1] // 3,
                color[2] // 3
            )

            # Fill the ghost
            pygame.draw.rect(screen, ghost_fill, tile_rect)

            # Draw the normal colored outline
            pygame.draw.rect(screen, color, tile_rect, 2)

    def draw_preview(self, screen, offset_x, offset_y):
        tiles = self.cells[self.rotation_state]

        for tile in tiles:
            tile_rect = pygame.Rect(
                offset_x + tile.col * self.cell_size,
                offset_y + tile.row * self.cell_size,
                self.cell_size - 1,
                self.cell_size - 1
            )

            pygame.draw.rect(screen, self.colors[self.id], tile_rect)

    def draw(self, screen, offset_x, offset_y):
        tiles = self.get_cell_positions()
        for tile in tiles:
            tile_rect = pygame.Rect(
                offset_x + tile.col * self.cell_size, 
                offset_y + tile.row * self.cell_size, 
                self.cell_size - 1, 
                self.cell_size - 1
            )
            pygame.draw.rect(screen, self.colors[self.id], tile_rect)
