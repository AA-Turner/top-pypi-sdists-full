"""Harbor Breeze A25 RF command encoder."""

from __future__ import annotations

from typing import override

from . import ModulationType, RadioFrequencyCommand

_DEFAULT_FREQUENCY = 315_000_000
_DEFAULT_FRAME_COUNT = 6


class HarborBreezeA25Command(RadioFrequencyCommand):
    """Encode Harbor Breeze A25 transmissions.

    The frame layout consists of a three-symbol preamble, a 13-bit address,
    two fixed bits, a 6-bit command field, two fixed trailer bits, and a final
    inter-frame gap. The complete frame is emitted six times per transmission.
    """

    address: int
    command: int

    def __init__(
        self,
        *,
        address: int,
        command: int,
        frequency: int = _DEFAULT_FREQUENCY,
    ) -> None:
        """Initialize the Harbor Breeze command.

        Args:
            address: 13-bit receiver address (0..8191).
            command: 6-bit command value (0..63).
            frequency: RF frequency in Hz.
        """
        if address < 0 or address >= (1 << 13):
            raise ValueError("address must be in range 0..8191 (13-bit)")
        if command < 0 or command >= (1 << 6):
            raise ValueError("command must be in range 0..63 (6-bit)")

        super().__init__(
            frequency=frequency,
            modulation=ModulationType.OOK,
            repeat_count=0,
        )
        self.address = address
        self.command = command

    @override
    def get_raw_timings(self) -> list[int]:
        """Compute the repeated Harbor Breeze transmission timings."""
        short_us = 493
        long_us = 952
        frame_gap_us = 10_936

        payload_bits = f"{self.address:013b}00{self.command:06b}10"

        frame: list[int] = [short_us, -long_us, short_us]
        for bit in payload_bits:
            if bit == "0":
                frame.extend([-long_us, short_us])
            else:
                frame.extend([-short_us, long_us])
        frame.append(-frame_gap_us)

        timings: list[int] = []
        for _ in range(_DEFAULT_FRAME_COUNT):
            timings.extend(frame)
        return timings
