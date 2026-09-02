"""Cross-derivation helpers for media-gen dimensions.

UnifiedConfig has three canonical dimension fields:
  - aspect_ratio: "16:9" / "1:1" / etc (intent)
  - width: int
  - height: int

Translators need to emit whatever shape the provider accepts:
  - "size" string ("1536x1024") → OpenAI gpt-image-*, Sora
  - aspect_ratio string → Imagen, Veo, Replicate FLUX, xAI
  - width + height ints → Together FLUX, SD-style

These helpers derive any form from any other so the user can set the most
convenient form on the agent and Python translates per provider.

Precedence (when multiple are set on UnifiedConfig):
  1. Explicit width + height (most specific)
  2. aspect_ratio + a base resolution (least specific)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from matrx_ai.config import UnifiedConfig


# Common base resolutions per aspect ratio. Used when only aspect_ratio is set
# and the provider needs concrete pixels.
_ASPECT_TO_DEFAULT_WH: dict[str, tuple[int, int]] = {
    "1:1": (1024, 1024),
    "16:9": (1536, 1024),
    "9:16": (1024, 1536),
    "4:3": (1408, 1024),
    "3:4": (1024, 1408),
    "21:9": (1920, 832),
    "9:21": (832, 1920),
    "3:2": (1536, 1024),
    "2:3": (1024, 1536),
}


def derive_wh(config: "UnifiedConfig") -> tuple[int | None, int | None]:
    """Return (width, height) from UnifiedConfig.

    Priority: explicit width+height first, else map aspect_ratio to a default
    pair, else (None, None).
    """
    if config.width and config.height:
        return int(config.width), int(config.height)
    if config.aspect_ratio:
        wh = _ASPECT_TO_DEFAULT_WH.get(config.aspect_ratio)
        if wh:
            return wh
        # Try to parse "W:H" arbitrary ratios with a 1024 base.
        try:
            a, b = (int(x) for x in config.aspect_ratio.split(":", 1))
            if a >= b:
                return (round(1024 * a / b / 16) * 16, 1024)
            return (1024, round(1024 * b / a / 16) * 16)
        except (ValueError, TypeError):
            return (None, None)
    return (None, None)


def derive_size_string(config: "UnifiedConfig") -> str | None:
    """Return a "WxH" string for providers (gpt-image-*, Sora) that take it.

    Returns None if neither width+height nor aspect_ratio is set.
    """
    w, h = derive_wh(config)
    if w and h:
        return f"{w}x{h}"
    return None


def derive_aspect_ratio(config: "UnifiedConfig") -> str | None:
    """Return aspect_ratio string ("16:9") from UnifiedConfig.

    Priority: explicit aspect_ratio, else compute from width+height (reduced
    to common form), else None.
    """
    if config.aspect_ratio:
        return config.aspect_ratio
    if config.width and config.height:
        from math import gcd
        g = gcd(int(config.width), int(config.height))
        a, b = int(config.width) // g, int(config.height) // g
        return f"{a}:{b}"
    return None


def derive_duration_str(config: "UnifiedConfig") -> str | None:
    """For providers (Sora, Together video) that take duration as a string.

    Reads UnifiedConfig.duration_seconds (int) and stringifies.
    """
    if config.duration_seconds is not None:
        return str(int(config.duration_seconds))
    return None
