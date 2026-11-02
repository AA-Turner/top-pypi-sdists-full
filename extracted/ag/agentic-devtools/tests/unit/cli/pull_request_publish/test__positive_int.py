import pytest

from agentic_devtools.cli.pull_request_publish import _positive_int


@pytest.mark.parametrize("value", [True, [], 0, "bad"])
def test_rejects_invalid_numbers(value: object) -> None:
    with pytest.raises(ValueError, match="positive integer"):
        _positive_int(value, "pull_request_id")


def test_converts_number() -> None:
    assert _positive_int("12", "pull_request_id") == 12
