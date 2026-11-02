"""Foundation map keys must be strings, never implicitly coerced identifiers."""

import pytest

from agentic_devtools.cli.ci.reconciliation.models import _read_string_value


def test_string_or_explicit_error():
    assert _read_string_value("id", "attempt") == "id"
    with pytest.raises(ValueError, match="attempt must be a str"):
        _read_string_value(42, "attempt")
