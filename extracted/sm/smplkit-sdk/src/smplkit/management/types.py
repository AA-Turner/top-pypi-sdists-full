"""Shared types for ``client.management.*``."""

from __future__ import annotations

import dataclasses
import enum
import re


class EnvironmentClassification(str, enum.Enum):
    """Whether an environment participates in the canonical ordering.

    STANDARD environments are the customer's deploy targets — production,
    staging, development, etc. They participate in
    ``account_settings.environment_order`` and appear in the standard
    Console environment columns.

    AD_HOC environments are transient targets (preview branches,
    individual developer sandboxes) that should not appear in the
    standard ordering.
    """

    AD_HOC = "AD_HOC"
    STANDARD = "STANDARD"


_HEX_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")


@dataclasses.dataclass(frozen=True)
class Color:
    """A color, expressed as a CSS hex string.

    Examples::

        Color("#ef4444")            # 6-digit hex
        Color("#fff")               # 3-digit shorthand
        Color("#ef4444aa")          # 8-digit with alpha
        Color.rgb(239, 68, 68)      # RGB components

    Frozen — construct a fresh ``Color`` to change a value.
    """

    hex: str

    def __post_init__(self) -> None:
        if not isinstance(self.hex, str):
            raise TypeError(f"Color hex must be a string, got {self.hex.__class__.__name__}: {self.hex!r}")
        if not _HEX_RE.match(self.hex):
            raise ValueError(
                f"Invalid color {self.hex!r}: must be a CSS hex string like '#RGB', '#RRGGBB', or '#RRGGBBAA'"
            )
        # normalize to lowercase so equality is canonical
        object.__setattr__(self, "hex", self.hex.lower())

    @classmethod
    def rgb(cls, r: int, g: int, b: int) -> Color:
        """Construct a ``Color`` from 0–255 RGB components."""
        for name, val in (("r", r), ("g", g), ("b", b)):
            if not isinstance(val, int) or isinstance(val, bool):
                raise TypeError(f"Color.rgb {name} must be an integer, got {val.__class__.__name__}: {val!r}")
            if not 0 <= val <= 255:
                raise ValueError(f"Color.rgb {name} must be in range 0–255, got {val!r}")
        return cls(f"#{r:02x}{g:02x}{b:02x}")

    def __str__(self) -> str:
        return self.hex
