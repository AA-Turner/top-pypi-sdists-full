"""OOK (On-Off Keying) RF command with raw timings."""

from __future__ import annotations

from typing import override

from . import ModulationType, RadioFrequencyCommand


class OOKCommand(RadioFrequencyCommand):
    """OOK command with raw timings."""

    timings: list[int]

    def __init__(
        self,
        *,
        frequency: int,
        timings: list[int],
        repeat_count: int = 0,
        symbol_rate: int | None = None,
        output_power: float | None = None,
    ) -> None:
        """Initialize the OOK command."""
        super().__init__(
            frequency=frequency,
            modulation=ModulationType.OOK,
            repeat_count=repeat_count,
            symbol_rate=symbol_rate,
            output_power=output_power,
        )
        self.timings = timings

    @override
    def get_raw_timings(self) -> list[int]:
        """Get raw timings."""
        return self.timings
