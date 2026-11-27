# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["CommandHeld"]


class CommandHeld(BaseModel):
    """Input still held down on a tab. It applies to later input until released."""

    keys: List[str]
    """Keys still held down, for example with keyboard down."""

    tab: str

    button: Optional[Literal["left", "right", "middle"]] = None
    """A mouse button held down with mouse down."""
