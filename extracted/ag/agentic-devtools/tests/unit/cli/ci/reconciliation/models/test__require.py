"""Invariant assertions fail with the caller's diagnostic."""

import pytest

from agentic_devtools.cli.ci.reconciliation.models import _require


def test_assertion_contract():
    assert _require(True, "valid") is None
    with pytest.raises(ValueError, match="invalid"):
        _require(False, "invalid")
