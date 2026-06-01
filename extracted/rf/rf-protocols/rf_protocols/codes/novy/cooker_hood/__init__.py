"""Novy cooker-hood button codes."""

from enum import Enum

from ....commands.novy import NovyCookerHoodCommand


class NovyCookerHoodButton(Enum):
    """Novy cooker-hood button identifiers.

    Each member's value is the (key_code, key_width_bits) pair
    transmitted in the frame.
    """

    MINUS = (0x1, 2)
    PLUS = (0x2, 2)
    AMBIENT = (0x3, 2)
    POWER = (0x2C, 8)
    LIGHT = (0x2E, 8)
    LIGHT_MINUS = (0x31, 8)
    LIGHT_PLUS = (0x34, 8)
    AMBIENT_MINUS = (0x29, 8)
    AMBIENT_PLUS = (0x32, 8)
    MINUS_PLUS = (0x37, 8)

    def __init__(self, code: int, width: int) -> None:
        """Initialize the button with its key code and frame width."""
        self.code = code
        self.width = width

    def to_command(
        self,
        *,
        channel: int,
        timebase_us: int = 360,
        frequency: int = 433_920_000,
        repeat_count: int = 5,
    ) -> NovyCookerHoodCommand:
        """Build a NovyCookerHoodCommand for this button."""
        return NovyCookerHoodCommand(
            channel=channel,
            key=self.code,
            key_width=self.width,
            timebase_us=timebase_us,
            frequency=frequency,
            repeat_count=repeat_count,
        )
