r"""Define some PyTest fixtures."""

from __future__ import annotations

__all__ = ["objectory_available", "objectory_not_available"]

import pytest

from minrecord.utils.imports import is_objectory_available

objectory_available: pytest.MarkDecorator = pytest.mark.skipif(
    not is_objectory_available(), reason="Require objectory"
)
objectory_not_available: pytest.MarkDecorator = pytest.mark.skipif(
    is_objectory_available(), reason="Skip because objectory is available"
)
