"""Encoder for Novy cooker-hood RF remotes.

433.92 MHz OOK. Compatible with Novy 4-button remotes (models 840029,
840039, 840049). The remote has 10 user-selectable channels; pair this
encoder to the channel your hood is set to.

References:
- https://github.com/martijndierckx/novy-433
- https://github.com/renedis/ESP32_Novy_Controller
- https://github.com/RFD-FHEM/RFFHEM (Protocol 86, also implemented in
  ``14_SD_UT.pm`` as ``Novy_840029`` / ``Novy_840039``)
"""

from __future__ import annotations

from typing import override

from . import ModulationType, RadioFrequencyCommand

_DEFAULT_FREQUENCY = 433_920_000
_DEFAULT_REPEATS = 5
_DEFAULT_TIMEBASE_US = 360
_INTER_FRAME_US = 10_000

_CHANNEL_CODES: dict[int, int] = {
    1: 0x2AA,
    2: 0x1AA,
    3: 0x3AA,
    4: 0x06A,
    5: 0x26A,
    6: 0x16A,
    7: 0x36A,
    8: 0x0EA,
    9: 0x2EA,
    10: 0x1EA,
}


class NovyCookerHoodCommand(RadioFrequencyCommand):
    """Encode a Novy cooker-hood RF remote frame.

    Sends one of the 10 channels with the given key. Button names and
    their key codes are exposed by ``rf_protocols.codes.novy.cooker_hood``.
    """

    channel: int
    key: int
    key_width: int
    timebase_us: int

    def __init__(
        self,
        *,
        channel: int,
        key: int,
        key_width: int,
        timebase_us: int = _DEFAULT_TIMEBASE_US,
        frequency: int = _DEFAULT_FREQUENCY,
        repeat_count: int = _DEFAULT_REPEATS,
    ) -> None:
        """Initialize the Novy command."""
        if channel not in _CHANNEL_CODES:
            raise ValueError("channel must be in range 1..10")
        if key < 0 or key >= (1 << key_width):
            raise ValueError(f"key must fit in {key_width} bits")

        super().__init__(
            frequency=frequency,
            modulation=ModulationType.OOK,
            repeat_count=repeat_count,
        )
        self.channel = channel
        self.key = key
        self.key_width = key_width
        self.timebase_us = timebase_us

    @override
    def get_raw_timings(self) -> list[int]:
        """Compute the frame timings as signed mark/space microseconds."""
        short_us = self.timebase_us
        long_us = 2 * short_us
        channel_code = _CHANNEL_CODES[self.channel]

        channel_bits = [(channel_code >> i) & 1 for i in range(9, -1, -1)]
        key_bits = [(self.key >> i) & 1 for i in range(self.key_width - 1, -1, -1)]

        timings: list[int] = [short_us]  # leading start mark
        for bit in channel_bits + key_bits:
            if bit:
                timings += [-short_us, long_us]
            else:
                timings += [-long_us, short_us]
        timings.append(-_INTER_FRAME_US)
        return timings
