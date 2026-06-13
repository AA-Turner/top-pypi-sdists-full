"""Harbor Breeze A25 command identifiers."""

from enum import IntEnum

from ....commands.harbor_breeze_a25 import HarborBreezeA25Command


class HarborBreezeA25Button(IntEnum):
    """Known Harbor Breeze A25 button codes.

    Values are the decoded 6-bit command field found in the normalized frame.
    """

    BLOW = 0b111010
    BREEZE = 0b000110
    FAN_1 = 0b011110
    FAN_2 = 0b101110
    FAN_3 = 0b001110
    FAN_4 = 0b110110
    FAN_5 = 0b010110
    FAN_6 = 0b100110
    HOME = 0b000011
    LIGHT = 0b011010
    POWER = 0b111110
    SUCK = 0b111000
    TIMER = 0b001000
    TIMER_2H = 0b011011
    TIMER_4H = 0b101011
    TIMER_8H = 0b001011

    def to_command(self, *, address: int) -> HarborBreezeA25Command:
        """Build a Harbor Breeze command for this button and address."""
        return HarborBreezeA25Command(address=address, command=self.value)

