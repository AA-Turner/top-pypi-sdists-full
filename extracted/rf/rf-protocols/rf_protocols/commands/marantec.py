"""Encoder for Marantec garage door / gate RF remotes.

868.35 MHz OOK (433.92 MHz variant available), Manchester-coded. Encodes a
static, indefinitely valid (non-rolling) 49-bit code. Does not cover
rolling-code Marantec systems or the unrelated 24-bit "Marantec24" cloner
protocol.
"""

from __future__ import annotations

from typing import override

from . import ModulationType, RadioFrequencyCommand

_MARANTEC_FREQUENCY = 868_350_000
_MARANTEC_REPEAT_COUNT = 4

_TE_SHORT = 1000
_TE_LONG = 2000
_HEADER_LOW = _TE_LONG * 5

_BIT_COUNT = 49


class MarantecCommand(RadioFrequencyCommand):
    """Encode a Marantec static-code garage door / gate frame."""

    code: int

    def __init__(
        self,
        *,
        code: int,
        frequency: int = _MARANTEC_FREQUENCY,
    ) -> None:
        """Initialize the Marantec command."""
        if code < 0 or code >= (1 << _BIT_COUNT):
            raise ValueError("code must be a 49-bit value (0..2**49-1)")
        super().__init__(
            frequency=frequency,
            modulation=ModulationType.OOK,
            repeat_count=_MARANTEC_REPEAT_COUNT,
        )
        self.code = code

    @override
    def get_raw_timings(self) -> list[int]:
        """Compute the frame timings as signed mark/space microseconds.

        Manchester (bit 0 = mark then space, bit 1 = space then mark), 49 bits,
        trailing inter-frame gap. Frame starts on a mark so polarity (assigned
        by index parity) stays correct; the first bit's leading space and the
        gap are reconstructed across the repeated transmissions.
        """
        timings: list[int] = []

        def add(us: int) -> None:
            if timings and (us > 0) == (timings[-1] > 0):
                timings[-1] += us
            else:
                timings.append(us)

        for idx in range(_BIT_COUNT):
            bit = (self.code >> (_BIT_COUNT - 1 - idx)) & 1
            if idx == 0 and bit:
                add(_TE_SHORT)
                continue
            if bit:
                add(-_TE_SHORT)
                add(_TE_SHORT)
            else:
                add(_TE_SHORT)
                add(-_TE_SHORT)

        add(-_HEADER_LOW)
        return timings
