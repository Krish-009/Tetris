import pygame

class HardDropEffect:
    def __init__(self, block, start_tiles, end_tiles):
        self.block = block.copy()

        self.start_tiles = start_tiles
        self.end_tiles = end_tiles

        self.life = 6
        self.max_life = 6

    def update(self):
        self.life -= 1

    def alive(self):
        return self.life > 0

    def draw(self, screen, offset_x, offset_y):

        color = self.block.colors[self.block.id]

        alpha = self.life / self.max_life

        fade = (
            int(color[0] * alpha),
            int(color[1] * alpha),
            int(color[2] * alpha)
        )

        for start, end in zip(self.start_tiles, self.end_tiles):

            for row in range(start.row, end.row + 1):

                rect = pygame.Rect(
                    offset_x + start.col * 30,
                    offset_y + row * 30,
                    29,
                    29
                )

                pygame.draw.rect(screen, fade, rect)