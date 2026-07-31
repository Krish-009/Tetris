import pygame
import copy
from colors import Colors
from position import Position

class Block:
    def __init__(self, block_id: int):
        self.id = block_id
        self.cells = {}
        self.cell_size = 30
        self.row_offset = 0
        self.col_offset = 0
        self.rotation_state = 0
        self.colors = Colors.get_cell_colors()
        self.ghost_colors = Colors.get_ghost_colors()

    # ---------
    # Movement
    # ---------
    def move(self, rows, cols):
        self.row_offset += rows
        self.col_offset += cols

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

    # -------
    # Helpers
    # -------
    def get_cell_positions(self) -> list[Position]:
        positions = []
        for tile in self.cells[self.rotation_state]:
            positions.append(
                Position(
                    tile.row + self.row_offset,
                    tile.col + self.col_offset
                )
            )
        return positions

    def copy(self):
        return copy.deepcopy(self)

    # -------
    # Drawing
    # -------
    def draw_tiles(
        self,
        screen,
        tiles,
        offset_x: int,
        offset_y: int,
        fill_colors = None,
        outline_colors = None,
        outline_width = 2
    ):

        for tile in tiles:

            rect = pygame.Rect(
                offset_x + tile.col * self.cell_size,
                offset_y + tile.row * self.cell_size,
                self.cell_size - 1,
                self.cell_size - 1
            )

            if fill_colors is not None:
                pygame.draw.rect(screen, fill_colors[self.id], rect)
            

            if outline_colors is not None:
                pygame.draw.rect(
                    screen,
                    self.colors[self.id],
                    rect,
                    outline_width
                )
        
    def draw_ghost(self, screen, offset_x: int, offset_y: int) -> None:
        self.draw_tiles(
            screen,
            self.get_cell_positions(),
            offset_x,
            offset_y,
            fill_colors=None,
            outline_colors=self.ghost_colors
        )

    def draw_preview(self, screen, offset_x: int, offset_y: int) -> None:
        self.draw_tiles(
            screen,
            self.cells[self.rotation_state],
            offset_x,
            offset_y,
            fill_colors=self.colors
        )

    def draw(self, screen, offset_x, offset_y):
        self.draw_tiles(
            screen,
            
            self.get_cell_positions(),
            offset_x,
            offset_y,
            fill_colors=self.colors
        )
