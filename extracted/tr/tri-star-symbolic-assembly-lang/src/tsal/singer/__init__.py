from __future__ import annotations

from typing import Union

def audio_to_opcode(freq: float) -> str:
    """Map frequency to TSAL opcode name."""
    if freq < 200:
        return "SEEK"
    if freq < 500:
        return "SPIRAL"
    return "RECOG"

__all__ = ["audio_to_opcode"]
