from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Device:
    index: int
    name: str
    max_input_channels: int
    max_output_channels: int
    default_samplerate: float
