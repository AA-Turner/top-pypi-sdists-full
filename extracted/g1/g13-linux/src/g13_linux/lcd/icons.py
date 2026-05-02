"""
LCD Icons

Bitmap icon definitions for G13 LCD display.
"""

from dataclasses import dataclass


@dataclass
class Icon:
    """Bitmap icon definition."""

    width: int
    height: int
    data: bytes


# 8x8 icons
# Data is column-major, bit 0 is top row

ICON_PROFILE = Icon(
    width=8,
    height=8,
    data=bytes(
        [
            0x00,  # ....
            0x1C,  # .###
            0x22,  # #..#
            0x22,  # #..#
            0x1C,  # .###
            0x00,  #
            0x3E,  # #####
            0x00,  #
        ]
    ),
)

ICON_MACRO = Icon(
    width=8,
    height=8,
    data=bytes(
        [
            0x04,  # ..#..
            0x0C,  # .##..
            0x1C,  # ###..
            0x3E,  # #####
            0x1C,  # ###..
            0x0C,  # .##..
            0x04,  # ..#..
            0x00,
        ]
    ),
)

ICON_LED = Icon(
    width=8,
    height=8,
    data=bytes(
        [
            0x08,  # ...#...
            0x14,  # ..#.#..
            0x22,  # .#...#.
            0x41,  # #.....#
            0x22,  # .#...#.
            0x14,  # ..#.#..
            0x08,  # ...#...
            0x00,
        ]
    ),
)

ICON_SETTINGS = Icon(
    width=8,
    height=8,
    data=bytes(
        [
            0x00,
            0x18,  # .##.
            0x24,  # #..#
            0x5A,  # #.##.#
            0x5A,  # #.##.#
            0x24,  # #..#
            0x18,  # .##.
            0x00,
        ]
    ),
)

ICON_INFO = Icon(
    width=8,
    height=8,
    data=bytes(
        [
            0x00,
            0x1C,  # .###.
            0x22,  # #...#
            0x32,  # .##.#
            0x22,  # #...#
            0x22,  # #...#
            0x1C,  # .###.
            0x00,
        ]
    ),
)

ICON_ARROW_RIGHT = Icon(
    width=8,
    height=8,
    data=bytes(
        [
            0x00,
            0x08,  # ...#
            0x1C,  # ..###
            0x3E,  # .#####
            0x7F,  # #######
            0x3E,  # .#####
            0x1C,  # ..###
            0x08,  # ...#
        ]
    ),
)

ICON_ARROW_LEFT = Icon(
    width=8,
    height=8,
    data=bytes(
        [
            0x08,  # #...
            0x1C,  # ###..
            0x3E,  # #####.
            0x7F,  # #######
            0x3E,  # #####.
            0x1C,  # ###..
            0x08,  # #...
            0x00,
        ]
    ),
)

ICON_ARROW_UP = Icon(
    width=8,
    height=8,
    data=bytes(
        [
            0x00,
            0x08,
            0x0C,
            0x7E,
            0x7E,
            0x0C,
            0x08,
            0x00,
        ]
    ),
)

ICON_ARROW_DOWN = Icon(
    width=8,
    height=8,
    data=bytes(
        [
            0x00,
            0x10,
            0x30,
            0x7E,
            0x7E,
            0x30,
            0x10,
            0x00,
        ]
    ),
)

ICON_CHECK = Icon(
    width=8,
    height=8,
    data=bytes(
        [
            0x00,
            0x40,  # .....#
            0x20,  # ....#
            0x10,  # ...#
            0x08,  # ..#
            0x14,  # .#.#
            0x22,  # #..#
            0x00,
        ]
    ),
)

ICON_CROSS = Icon(
    width=8,
    height=8,
    data=bytes(
        [
            0x00,
            0x41,  # #....#
            0x22,  # .#..#.
            0x14,  # ..##..
            0x08,  # ...#...
            0x14,  # ..##..
            0x22,  # .#..#.
            0x41,  # #....#
        ]
    ),
)

ICON_RECORDING = Icon(
    width=8,
    height=8,
    data=bytes(
        [
            0x00,
            0x1C,  # .###.
            0x3E,  # #####
            0x7F,  # #######
            0x7F,  # #######
            0x3E,  # #####
            0x1C,  # .###.
            0x00,
        ]
    ),
)

ICON_PLAY = Icon(
    width=8,
    height=8,
    data=bytes(
        [
            0x00,
            0x7F,  # #######
            0x3E,  # .#####
            0x1C,  # ..###
            0x08,  # ...#
            0x00,
            0x00,
            0x00,
        ]
    ),
)

ICON_PAUSE = Icon(
    width=8,
    height=8,
    data=bytes(
        [
            0x00,
            0x7F,  # #######
            0x7F,  # #######
            0x00,
            0x00,
            0x7F,  # #######
            0x7F,  # #######
            0x00,
        ]
    ),
)

ICON_STOP = Icon(
    width=8,
    height=8,
    data=bytes(
        [
            0x00,
            0x7E,
            0x7E,
            0x7E,
            0x7E,
            0x7E,
            0x7E,
            0x00,
        ]
    ),
)

ICON_CLOCK = Icon(
    width=8,
    height=8,
    data=bytes(
        [
            0x00,
            0x1C,  # .###.
            0x22,  # #...#
            0x2A,  # #.#.#
            0x2E,  # #.###
            0x22,  # #...#
            0x1C,  # .###.
            0x00,
        ]
    ),
)

ICON_KEYBOARD = Icon(
    width=8,
    height=8,
    data=bytes(
        [
            0x00,
            0x7F,  # #######
            0x55,  # #.#.#.#
            0x7F,  # #######
            0x55,  # #.#.#.#
            0x7F,  # #######
            0x00,
            0x00,
        ]
    ),
)
