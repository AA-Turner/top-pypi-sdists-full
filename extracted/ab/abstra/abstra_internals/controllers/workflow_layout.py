from typing import NamedTuple

NODE_WIDTH = 200
NODE_HEIGHT = 70
ROW_GAP = 60


class Box(NamedTuple):
    x: int
    y: int
    width: int = NODE_WIDTH
    height: int = NODE_HEIGHT


def find_free_position(existing: list[Box]) -> tuple[int, int]:
    if not existing:
        return (0, 0)

    lowest = max(existing, key=lambda box: (box.y + box.height, -box.x))
    return (lowest.x, lowest.y + lowest.height + ROW_GAP)
