from dataclasses import dataclass

@dataclass(slots=True)
class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    