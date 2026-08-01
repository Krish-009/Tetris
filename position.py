from dataclasses import dataclass

@dataclass(slots=True)
class Position:
    row: int
    col: int
