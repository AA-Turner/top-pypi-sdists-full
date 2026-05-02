from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Union


class PositionType(str, Enum):
    """CSS position property values."""
    RELATIVE = 'relative'  # In flow, but offsets apply
    ABSOLUTE = 'absolute'  # Out of flow, positioned relative to nearest positioned ancestor
    FIXED = 'fixed'        # Out of flow, positioned relative to canvas (viewport)


# Type for inset values: pixels (float/int) or percentage string ("50%")
InsetValue = Optional[Union[float, int, str]]


@dataclass
class Inset:
    """CSS inset values (top, right, bottom, left).
    
    Values can be:
    - None: auto (not set)
    - float/int: pixels
    - str: percentage (e.g., "50%")
    """
    top: InsetValue = None
    right: InsetValue = None
    bottom: InsetValue = None
    left: InsetValue = None


@dataclass
class Position:
    """CSS-like position configuration.
    
    Combines position type (relative/absolute/fixed) with inset values.
    """
    type: PositionType = PositionType.RELATIVE
    inset: Inset = field(default_factory=Inset)
