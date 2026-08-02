"""CSS transform model.

This module provides the Transform dataclass for translate transforms,
which are applied post-layout as visual offsets.
"""
from dataclasses import dataclass
from typing import Optional, Union


# Type for translate values: pixels (float/int) or percentage string ("-50%")
TranslateValue = Optional[Union[float, int, str]]


@dataclass
class Transform:
    """CSS-like translate transform.
    
    Values can be:
    - None: no translation
    - float/int: pixels
    - str: percentage of element's own size (e.g., "-50%" for centering)
    """
    translate_x: TranslateValue = None
    translate_y: TranslateValue = None
