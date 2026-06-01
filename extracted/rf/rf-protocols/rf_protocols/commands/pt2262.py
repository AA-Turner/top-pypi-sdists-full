"""Encoder for PT2262 / HX2262 and compatible tristate RF chips.

Chip datasheet: https://cdn-shop.adafruit.com/datasheets/PT2262.pdf

Devices which use PT2262 or compatible chips include:

- BAT RC 3500-A
- Brennenstuhl RCS 1000 N Comfort
- Emil Lux GmbH RCS-14G
- ELRO AB440D, AB440IS, AB440L, AB440S, AB440WD
- Intertechno CMR-1000, CMR-1224, CMR-300, CMR-500, ...
- Intertechno IT-1500, IT-1500R, IT-2000, IT-2000R, ...
- me FLS 100
- mumbi FS300
- REV Ritter 8342C
- Vivanco FSS 31000W
- RSL366
- Goobay 94503

A frame consists of 12 symbols (0/1/F) followed by a sync symbol. The chip has
12 inputs A0..A11 which can be tied to VCC, GND, or left floating. GND sends
symbol 0, VCC sends symbol 1, and floating sends symbol F. The symbols are
encoded against a time base ``a`` determined by the crystal connected to the
chip::

              ____              ____
    Bit 0 : _|    |____________|    |____________
             |<4a>|<---12a---->|<4a>|<---12a---->|

              ____________      ____________
    Bit 1 : _|            |____|            |____
             |<---12a---->|<4a>|<---12a---->|<4a>|

              ____              ____________
    Bit F : _|    |____________|            |____
             |<4a>|<---12a---->|<---12a---->|<4a>|

              ____
    Sync  : _|    |___________ _ _ _ ____________
             |<4a>|<-----------124a------------->|

References:

- https://www.seegel-systeme.de/2017/03/28/uebersicht-funksteckdosen/
- https://www.seegel-systeme.de/2015/09/05/funksteckdosen-mit-dem-raspberry-pi-steuern/
"""

from __future__ import annotations

from typing import override

from . import ModulationType, RadioFrequencyCommand

_VALID_SYMBOLS = frozenset("01FX")


class PT2262Command(RadioFrequencyCommand):
    """OOK command for PT2262 / HX2262 and compatible tristate chips."""

    data: str
    timebase_us: int

    def __init__(
        self,
        *,
        data: str,
        timebase_us: int = 350, # length of a short pulse
        frequency: int = 433_920_000,
        repeat_count: int = 5,
    ) -> None:
        """Initialize the PT2262 command from a 12-symbol tristate string."""
        normalized_data = data.upper()
        if len(normalized_data) != 12:
            raise ValueError("data must be exactly 12 characters long")
        if not set(normalized_data).issubset(_VALID_SYMBOLS):
            raise ValueError("data must contain only symbols '0', '1', 'F', and 'X'")

        super().__init__(
            frequency=frequency,
            modulation=ModulationType.OOK,
            repeat_count=repeat_count,
        )
        self.data = normalized_data
        self.timebase_us = timebase_us

    @override
    def get_raw_timings(self) -> list[int]:
        """Compute the PT2262 frame timings followed by the sync symbol."""
        short_us = self.timebase_us
        long_us = 3 * self.timebase_us
        sync_low_us = 31 * self.timebase_us
        symbols = {
            "0": [short_us, -long_us, short_us, -long_us],
            "1": [long_us, -short_us, long_us, -short_us],
            "F": [short_us, -long_us, long_us, -short_us],
            "X": [short_us, -long_us, short_us, -short_us],
        }

        timings: list[int] = []
        for symbol in self.data:
            timings.extend(symbols[symbol])
        timings.extend([short_us, -sync_low_us])
        return timings
