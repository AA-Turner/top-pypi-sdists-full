"""The object hook rejects repeated keys."""

import pytest

from agentic_devtools.cli.ci.pipeline.conflict_reconciliation import ReconciliationValidationError, _json_object


def test_object_pairs():
    assert _json_object([("a", 1), ("b", 2)]) == {"a": 1, "b": 2}
    with pytest.raises(ReconciliationValidationError, match="invalid_json"):
        _json_object([("a", 1), ("a", 2)])
