"""An explicit dependency on another immutable authored build stage."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from labqoat.compute.image import Image


@dataclass(frozen=True)
class StageStep:
    """Copy one absolute output path without shipping the compiler stage into the worker image."""

    image: Image
    source: str
    destination: str
