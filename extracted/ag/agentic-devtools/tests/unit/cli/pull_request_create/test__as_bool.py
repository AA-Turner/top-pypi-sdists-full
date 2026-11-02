import pytest

from agentic_devtools.cli import pull_request_create


@pytest.mark.parametrize(
    ("value", "expected"),
    [(None, True), (True, True), (False, False), ("yes", True), ("off", False)],
)
def test_as_bool_parses_supported_values(value: object, expected: bool) -> None:
    assert pull_request_create._as_bool(value) is expected
