import pygame

class HardDropEffect:
    CELL_SIZE = 30
    CELL_PADDING = 1
    MAX_LIFE = 6

    def __init__(self, block, start_tiles, end_tiles):
        self.color = block.colors[block.id]

        self.start_tiles = start_tiles
        self.end_tiles = end_tiles

        self.life = self.MAX_LIFE

    def update(self):
        self.life -= 1

    @property
    def alive(self):
        return self.life > 0

    def get_fade_color(self):
        alpha = self.life / self.MAX_LIFE

        return (
            int(self.color[0] * alpha),
            int(self.color[1] * alpha),
            int(self.color[2] * alpha)
        )

    def draw(self, screen, offset_x, offset_y):

        color = self.get_fade_color()

        for start, end in zip(self.start_tiles, self.end_tiles):

            for row in range(start.row, end.row + 1):

                rect = pygame.Rect(
                    offset_x + start.col * self.CELL_SIZE,
                    offset_y + row * self.CELL_SIZE,
                    self.CELL_SIZE - self.CELL_PADDING,
                    self.CELL_SIZE - self.CELL_PADDING
                )

                pygame.draw.rect(screen, color, rect)