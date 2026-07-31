import pygame
from colors import Colors

class Grid:
    NUM_ROWS = 20
    NUM_COLS = 10
    CELL_SIZE = 30
    GRID_OFFSET = 11

    FLASH_DURATION = 160
    PEEL_STEP_DURATION = 35

    def __init__(self):
        self.num_rows = self.NUM_ROWS
        self.num_cols = self.NUM_COLS
        self.cell_size = self.CELL_SIZE

        self.grid = [
            [0 for j in range(self.num_cols)] 
            for i in range(self.num_rows)
        ]

        self.colors = Colors.get_cell_colors()

        # Line Clear Animation
        self.clearing_rows = []
        self.trigger_cols = {}
        self.is_clearing = False
        self.phase = None
        self.phase_timer = 0
        self.peel_radius = 0

    # -----
    # Debug
    # -----
    def print_grid(self):
        for row in self.grid:
            print(*row)

    # -----------
    # Cell Checks
    # -----------
    def is_inside(self, row, col):
        return(
            0 <= row < self.num_rows 
            and 0 <= col < self.num_cols
        )

    def is_empty(self, row, col):
        return self.grid[row][col] == 0

    def is_row_full(self, row):
        return all(cell != 0 for cell in self.grid[row])

    # -----------------
    # Grid modification
    # -----------------
    def clear_row(self, row):
        self.grid[row] = [0] * self.num_cols

    def move_row_down(self, row, amount):
        self.grid[row + amount] = self.grid[row]
        self.clear_row(row)

    def reset(self):
        self.grid = [
            [0 for _ in range(self.num_cols)]
            for _ in range(self.num_rows)
        ]

    # -----------
    # Row Helpers
    # -----------
    def get_full_rows(self):
        return [
            row
            for row in range(self.num_rows)
            if self.is_row_full(row)
        ]

    # --------------------
    # Line Clear Animation
    # --------------------
    def start_clear_animation(self, rows, trigger_tiles=None):
        self.clearing_rows = rows
        self.trigger_cols = {}
        for row in rows:
            if trigger_tiles:
                cols = sorted(
                    tile.col
                    for tile in trigger_tiles
                    if tile.row == row
                )

                if cols:
                    self.trigger_cols[row] = cols[len(cols) // 2]
                    continue
            self.trigger_cols[row] = self.num_cols // 2
 
        self.is_clearing = True
        self.phase = "flash"
        self.phase_timer = pygame.time.get_ticks()
        self.peel_radius = 0
 
    def update_clear_animation(self):
        if not self.is_clearing:
            return None
 
        now = pygame.time.get_ticks()

        if self.phase == "flash":
            if now - self.phase_timer >= self.FLASH_DURATION:
                self.phase = "peel"
                self.phase_timer = now
                self.peel_radius = 0
            return None
        
        max_radius = self.num_cols - 1

        if now - self.phase_timer >= self.PEEL_STEP_DURATION:
            self.phase_timer = now
            self.peel_radius += 1
 
            if self.peel_radius > max_radius:
                cleared = len(self.clearing_rows)

                self.compact_after_clear()

                self.is_clearing = False
                self.clearing_rows.clear()
                self.trigger_cols.clear()
                self.phase = None

                return cleared
 
        return None
 
    def compact_after_clear(self):
        cleared_set = set(self.clearing_rows)

        new_grid = [
            [0] * self.num_cols 
            for _ in range(self.num_rows)
        ]

        write_row = self.num_rows - 1

        for row in range(self.num_rows - 1, -1, -1):
            if row not in cleared_set:
                new_grid[write_row] = self.grid[row]
                write_row -= 1

        self.grid = new_grid

    # -------
    # Drawing
    # -------
    def draw_animation_cell(self, screen, row, col, rect):
            if not self.is_clearing or row not in self.clearing_rows:
                return False
    
            if self.phase == "flash":
                pygame.draw.rect(screen, (255, 255, 255), rect)
                return True
    
            trigger = self.trigger_cols[row]
    
            if abs(col - trigger) > self.peel_radius:
                pygame.draw.rect(screen, (255, 255, 255), rect)
    
            return True
    
    def draw(self, screen):
        for row in range(self.num_rows):
            for col in range(self.num_cols):

                rect = pygame.Rect(
                    col * self.cell_size + self.GRID_OFFSET, 
                    row * self.cell_size + self.GRID_OFFSET, 
                    self.cell_size - 1, 
                    self.cell_size - 1
                )

                if self.draw_animation_cell(screen, row, col, rect):
                    continue

                pygame.draw.rect(
                    screen,
                    self.colors[self.grid[row][col]],
                    rect
                )

    