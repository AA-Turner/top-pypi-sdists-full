"""JSON object keys must not be silently overwritten."""

import pytest

from agentic_devtools.cli.ci.windows_specific_cli import _unique_object


def test_preserves_order_and_values():
    assert list(_unique_object([("second", []), ("first", 2)]).items()) == [("second", []), ("first", 2)]
    assert _unique_object([]) == {}


def test_rejects_duplicate_key():
    with pytest.raises(ValueError, match="Duplicate"):
        _unique_object([("key", 1), ("key", 1)])
