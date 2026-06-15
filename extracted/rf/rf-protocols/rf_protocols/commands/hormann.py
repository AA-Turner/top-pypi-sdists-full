"""Encoder for Hörmann garage door / gate RF remotes (HSM fixed-code).

433.92 MHz and 868.3 MHz OOK, pulse-width coded. Encodes a static,
indefinitely valid (non-rolling) 44-bit code. Covers the fixed-code "blue
button" Hörmann remotes (HSM2, HSM4, HS1, HS2, HS4, HSE2, HSE4, HSZ1, HSZ2,
HSP4, HSP4-C, HSD2-A, HSD2-C at 868.3 MHz; HS4, HSM4, HSE2 at 433.92 MHz).
Does not cover the BiSecur ("BS") rolling-code remotes or the older 40.685 MHz
("grey button") generation.
"""

from __future__ import annotations

from typing import override

from . import ModulationType, RadioFrequencyCommand

_FREQUENCY_868 = 868_300_000
_REPEAT_COUNT = 10

_TE_SHORT = 500
_TE_LONG = 1000
_SYNC_MARK = _TE_SHORT * 24

_BIT_COUNT = 44


class HormannCommand(RadioFrequencyCommand):
    """Encode a Hörmann HSM static-code garage door / gate frame."""

    code: int

    def __init__(
        self,
        *,
        code: int,
        frequency: int = _FREQUENCY_868,
    ) -> None:
        """Initialize the Hörmann command."""
        if code < 0 or code >= (1 << _BIT_COUNT):
            raise ValueError("code must be a 44-bit value (0..2**44-1)")
        super().__init__(
            frequency=frequency,
            modulation=ModulationType.OOK,
            repeat_count=_REPEAT_COUNT,
        )
        self.code = code

    @override
    def get_raw_timings(self) -> list[int]:
        """Compute the frame timings as signed mark/space microseconds.

        A long sync mark and short space precede 44 pulse-width-coded bits
        (bit 1 = long mark then short space, bit 0 = short mark then long
        space), MSB first. The frame is mark-first and ends on a space; the
        sync mark of the next repeat provides inter-frame separation.
        """
        timings: list[int] = [_SYNC_MARK, -_TE_SHORT]

        for i in range(_BIT_COUNT - 1, -1, -1):
            if (self.code >> i) & 1:
                timings.append(_TE_LONG)
                timings.append(-_TE_SHORT)
            else:
                timings.append(_TE_SHORT)
                timings.append(-_TE_LONG)

        return timings
