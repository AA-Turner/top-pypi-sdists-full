from unittest.mock import patch

import pytest

from agentic_devtools.cli import pull_request_create


@pytest.mark.parametrize(("value", "expected"), [("explicit", "explicit"), ("", "")])
def test_state_or_returns_value_when_not_none(value: object, expected: object) -> None:
    with patch.object(pull_request_create, "get_value") as get_value:
        assert pull_request_create._state_or(value, "some_key") == expected
    get_value.assert_not_called()


def test_state_or_falls_back_to_state_when_value_is_none() -> None:
    with patch.object(pull_request_create, "get_value", return_value="from_state") as get_value:
        result = pull_request_create._state_or(None, "some_key")

    get_value.assert_called_once_with("some_key")
    assert result == "from_state"
