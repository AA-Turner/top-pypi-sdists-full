import pytest

from agentic_devtools.cli.github.single_finding_dispatch import _validate_identifier


@pytest.mark.parametrize("value", ["task-1", "session_1", "abc123"])
def test_validate_identifier_returns_safe_identifier(value):
    assert _validate_identifier("identifier", value) == value


@pytest.mark.parametrize("value", ["", "bad/id", "bad id", None, 1])
def test_validate_identifier_rejects_unsafe_identifier(value):
    with pytest.raises(ValueError, match="identifier"):
        _validate_identifier("identifier", value)
