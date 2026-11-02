from unittest.mock import patch

import pytest

from agentic_devtools.cli.pull_request_publish import _dry_run_flag


@patch("agentic_devtools.cli.pull_request_publish.is_dry_run", return_value=True)
def test_reads_dry_run_from_state(mock_is_dry_run) -> None:
    assert _dry_run_flag() is True
    mock_is_dry_run.assert_called_once_with()


@pytest.mark.parametrize("value", [True, False])
def test_accepts_boolean_override(value: bool) -> None:
    assert _dry_run_flag(value) is value


def test_rejects_non_boolean_override() -> None:
    with pytest.raises(ValueError, match="dry_run must be a boolean"):
        _dry_run_flag("true")  # type: ignore[arg-type]
