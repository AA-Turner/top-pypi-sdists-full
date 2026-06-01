"""Protocol for Pilota Casa compatible devices.

Pulse Width Modulation with 32 symbols, used by Pilota Casa remote controls.

Symbols use a time base ``T`` of 600 µS:

             ______________
Bit 0    : _|              |______
            |<----2T------>|-<1T>-|

             ______
Bit 1    : _|      |______________
            |-<1T>-|<----2T----->|

Telegram layout:
- 32 data bits
  - 2 bits device type (01 = remote control)
  - 6 bits group, channel, command (via lookup table)
  - 16 bits ID
  - 8 bits always 1 (11111111)

Each transmission is typically repeated multiple times.

Reference chapter:
https://www.seegel-systeme.de/2015/09/05/funksteckdosen-mit-dem-raspberry-pi-steuern/
"""

from __future__ import annotations

from typing import override

from . import ModulationType, RadioFrequencyCommand

_DEFAULT_FREQUENCY = 433_920_000
_DEFAULT_REPEATS = 5
_DEFAULT_TIMEBASE_US = 600

# Lookup table: (group, channel, on) -> 6-bit data value
_CMD_TABLE = {
    (1, 1, True): 0b110001,
    (1, 1, False): 0b111110,
    (1, 2, True): 0b011001,
    (1, 2, False): 0b010001,
    (1, 3, True): 0b101001,
    (1, 3, False): 0b100001,
    (2, 1, True): 0b111010,
    (2, 1, False): 0b110010,
    (2, 2, True): 0b010110,
    (2, 2, False): 0b011010,
    (2, 3, True): 0b100110,
    (2, 3, False): 0b101010,
    (3, 1, True): 0b110111,
    (3, 1, False): 0b111011,
    (3, 2, True): 0b011111,
    (3, 2, False): 0b010111,
    (3, 3, True): 0b101111,
    (3, 3, False): 0b100111,
    (4, 1, True): 0b111101,
    (4, 1, False): 0b110101,
    (4, 2, True): 0b010011,
    (4, 2, False): 0b011101,
    (4, 3, True): 0b100011,
    (4, 3, False): 0b101101,
    (0, 0, True): 0b101100,
    (0, 0, False): 0b011100,
}


class PilotaCasaCommand(RadioFrequencyCommand):
    """Encode a Pilota Casa PWM frame."""

    id: int
    group: int
    channel: int
    on: bool
    timebase_us: int

    def __init__(
        self,
        *,
        id: int,
        group: int,
        channel: int,
        on: bool,
        frame_repeats: int = _DEFAULT_REPEATS,
        frequency: int = _DEFAULT_FREQUENCY,
        timebase_us: int = _DEFAULT_TIMEBASE_US,
    ) -> None:
        """Initialize the Pilota Casa command.

        Args:
                id: 16-bit device ID (0-65535)
                group: Group number (1-4) or 0 for all groups
                channel: Channel number (1-4) or 0 for all channels
                on: True for on command, False for off command
                frame_repeats: Number of frame repetitions
                frequency: RF frequency in Hz
                timebase_us: Time base in microseconds
        """

        if id < 0 or id >= (1 << 16):
            raise ValueError("id must be in range 0..65535 (16-bit)")
        if group < 0 or group > 4:
            raise ValueError("group must be in range 0..4 (0=all, 1-4=specific group)")
        if channel < 0 or channel > 4:
            raise ValueError(
                "channel must be in range 0..4 (0=all, 1-4=specific channel)"
            )
        if (group, channel, on) not in _CMD_TABLE:
            raise ValueError(
                f"Invalid group/channel/on combination: ({group}, {channel}, {on})"
            )

        super().__init__(
            frequency=frequency,
            modulation=ModulationType.OOK,
            repeat_count=frame_repeats,
        )
        self.id = id
        self.group = group
        self.channel = channel
        self.on = on
        self.timebase_us = timebase_us

    @override
    def get_raw_timings(self) -> list[int]:
        """Compute Pilota Casa PWM frame timings."""
        _symbols = {
            "0": [2 * self.timebase_us, -self.timebase_us],
            "1": [self.timebase_us, -2 * self.timebase_us],
            "pause": [self.timebase_us, -11 * self.timebase_us],
        }

        # Build the 32-bit data string
        # 2 bits: device type (01 for remote control)
        symstr: list[str] = ["0", "1"]

        # 6 bits: encoded group, channel, and on/off from lookup table
        data_byte = _CMD_TABLE[(self.group, self.channel, self.on)]
        symstr.extend(format(data_byte, "06b"))

        # 16 bits: ID
        symstr.extend(format(self.id, "016b"))

        # 8 bits: always 1
        symstr.extend("11111111")

        # Convert symbol string to timings
        timings: list[int] = []
        for s in symstr:
            timings.extend(_symbols[s])
        timings.extend(_symbols["pause"])

        return timings
