import pytest

from agentic_devtools.cli.ci.dispatch_reservation import _reject_duplicate_keys


def test_returns_unique_pairs_as_dict() -> None:
    assert _reject_duplicate_keys([("one", 1), ("two", 2)]) == {"one": 1, "two": 2}


def test_rejects_duplicate_key() -> None:
    with pytest.raises(ValueError, match="duplicate"):
        _reject_duplicate_keys([("one", 1), ("one", 2)])
