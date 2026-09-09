"""Tests for _read_open_pr_page()."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.watchdog_command import _read_open_pr_page


class TestReadOpenPrPage:
    """Open PR inventory decoding guards."""

    def test_returns_decoded_list_of_dicts(self) -> None:
        with patch("agentic_devtools.cli.ci.watchdog_command._gh_api", return_value='[{"id":1}]'):
            decoded = _read_open_pr_page("o/r", "token", 1)

        assert decoded == [{"id": 1}]

    def test_rejects_non_list_payload(self) -> None:
        with patch("agentic_devtools.cli.ci.watchdog_command._gh_api", return_value='{"id":1}'):
            with pytest.raises(RuntimeError, match="malformed"):
                _read_open_pr_page("o/r", "token", 1)

    def test_rejects_list_with_non_dict_entries(self) -> None:
        with patch("agentic_devtools.cli.ci.watchdog_command._gh_api", return_value="[1]"):
            with pytest.raises(RuntimeError, match="malformed"):
                _read_open_pr_page("o/r", "token", 1)

    def test_rejects_non_json_payload(self) -> None:
        with patch("agentic_devtools.cli.ci.watchdog_command._gh_api", return_value="not-json"):
            with pytest.raises(RuntimeError, match="malformed"):
                _read_open_pr_page("o/r", "token", 1)
