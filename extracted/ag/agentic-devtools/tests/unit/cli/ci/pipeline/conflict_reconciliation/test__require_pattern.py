"""Pattern validation does not accept a trailing newline."""

import pytest

from agentic_devtools.cli.ci.pipeline.conflict_reconciliation import ReconciliationValidationError, _require_pattern


def test_full_match():
    assert _require_pattern("abc", "[a-z]+", "invalid_login") is None
    with pytest.raises(ReconciliationValidationError, match="invalid_login"):
        _require_pattern("abc\n", "[a-z]+", "invalid_login")
