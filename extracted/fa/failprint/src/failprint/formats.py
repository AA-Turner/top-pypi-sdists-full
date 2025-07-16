"""Deprecated. Import from `failprint` directly."""

# YORE: Bump 2: Remove file.

import warnings
from typing import Any

from failprint._internal import formats


def __getattr__(name: str) -> Any:
    warnings.warn(
        "Importing from `failprint.formats` is deprecated. Import from `failprint` directly.",
        DeprecationWarning,
        stacklevel=2,
    )
    return getattr(formats, name)
