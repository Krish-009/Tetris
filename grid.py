import pygame
from colors import Colors

class Grid:
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 30
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
        self.colors = Colors.get_cell_colors()

        self.clearing_rows = []
        self.trigger_cols = {}
        self.is_clearing = False
        self.phase = None
        self.phase_timer = 0
        self.flash_hold_duration = 160
        self.peel_step_duration = 35
        self.peel_radius = 0

    def print_grid(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                print(self.grid[row][col], end=" ")
            print()

    def is_inside(self, row, col):
        if row >= 0 and row < self.num_rows and col >= 0 and col < self.num_cols:
            return True
        return False

    def is_empty(self, row, col):
        if self.grid[row][col] == 0:
            return True
        return False

    def is_row_full(self, row):
        for col in range(self.num_cols):
            if self.grid[row][col] == 0:
                return False
        return True

    def clear_row(self, row):
        for col in range(self.num_cols):
            self.grid[row][col] = 0

    def move_row_down(self, row, num_rows):
        for col in range(self.num_cols):
            self.grid[row + num_rows][col] = self.grid[row][col]
            self.grid[row][col] = 0

    def get_full_rows(self):
        full_rows = []
        for row in range(self.num_rows):
            if self.is_row_full(row):
                full_rows.append(row)
        return full_rows
 
    def start_clear_animation(self, rows, trigger_tiles=None):
        self.clearing_rows = rows
        self.trigger_cols = {}
        for row in rows:
            cols_in_row = []
            if trigger_tiles:
                cols_in_row = [t.col for t in trigger_tiles if t.row == row]
 
            if cols_in_row:
                cols_in_row.sort()
                self.trigger_cols[row] = cols_in_row[len(cols_in_row) // 2]
            else:
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
            if now - self.phase_timer >= self.flash_hold_duration:
                self.phase = "peel"
                self.phase_timer = now
                self.peel_radius = 0
            return None
        
        max_distance = self.num_cols - 1
        if now - self.phase_timer >= self.peel_step_duration:
            self.phase_timer = now
            self.peel_radius += 1
 
            if self.peel_radius > max_distance:
                cleared = len(self.clearing_rows)
                self._compact_after_clear(self.clearing_rows)
                self.is_clearing = False
                self.clearing_rows = []
                self.trigger_cols = {}
                self.phase = None
                return cleared
 
        return None
 
    def _compact_after_clear(self, cleared_rows):
        cleared_set = set(cleared_rows)
        new_grid = [[0] * self.num_cols for _ in range(self.num_rows)]
        write_row = self.num_rows - 1
        for row in range(self.num_rows - 1, -1, -1):
            if row not in cleared_set:
                new_grid[write_row] = self.grid[row]
                write_row -= 1
        self.grid = new_grid

    def reset(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self.grid[row][col] = 0


    def draw(self, screen):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                cell_value = self.grid[row][col]
                cell_rect = pygame.Rect(
                    col * self.cell_size + 11, 
                    row * self.cell_size + 11, 
                    self.cell_size - 1, 
                    self.cell_size - 1
                )
                if self.is_clearing and row in self.clearing_rows:
                    if self.phase == "flash":
                        pygame.draw.rect(screen, (255, 255, 255), cell_rect)
                    else:
                        trigger_col = self.trigger_cols[row]
                        if abs(col - trigger_col) <= self.peel_radius:
                            pass
                        else:
                            pygame.draw.rect(screen, (255, 255, 255), cell_rect)
                    continue
                pygame.draw.rect(screen, self.colors[cell_value], cell_rect)