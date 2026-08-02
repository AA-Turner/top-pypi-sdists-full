from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from .paint_source import PaintSource

@dataclass
class TextDecoration:
    """Represents a line drawn over, under, or through the text."""
    color: Optional[PaintSource] = None  # If None, use the text's color.
    thickness: float = 4.0
