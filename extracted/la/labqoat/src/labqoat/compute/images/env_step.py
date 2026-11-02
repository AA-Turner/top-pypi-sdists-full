"""Literal environment entries at one point in an ordered image recipe."""

from dataclasses import dataclass


@dataclass(frozen=True)
class EnvStep:
    """Freeze a caller mapping so later mutation cannot alter an image."""

    values: tuple[tuple[str, str], ...]
