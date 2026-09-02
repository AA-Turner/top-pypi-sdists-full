"""
Tests for scripts/verify_pypi_latest.py -- the CI guard that fails a
release if PyPI doesn't resolve it as latest (see docs/VERSION_MANAGEMENT.md
"Reset history" for why this matters: a stale, higher-numbered release
left un-yanked on PyPI sorts above any reset MAJOR.MINOR line under real
PEP 440 ordering).
"""

import importlib.util
import sys
from pathlib import Path
from unittest.mock import patch

_SCRIPT_PATH = (
    Path(__file__).resolve().parent.parent / "scripts" / "verify_pypi_latest.py"
)
_spec = importlib.util.spec_from_file_location("verify_pypi_latest", _SCRIPT_PATH)
verify_pypi_latest = importlib.util.module_from_spec(_spec)
sys.modules["verify_pypi_latest"] = verify_pypi_latest
_spec.loader.exec_module(verify_pypi_latest)


class TestMain:
    def test_passes_when_pypi_resolves_the_new_version_as_latest(self, capsys):
        with (
            patch.object(
                verify_pypi_latest, "_fetch_pypi_latest", return_value="0.1.3b0"
            ),
            patch("sys.argv", ["verify_pypi_latest.py", "0.1.3-beta"]),
        ):
            assert verify_pypi_latest.main() == 0
        assert "OK" in capsys.readouterr().out

    def test_fails_when_pypi_resolves_a_stale_higher_numbered_release(self, capsys):
        """The exact real-world bug: 0.111.10b0 was never yanked and,
        despite being numerically HIGHER than the reset 0.1.x line, is
        still the wrong version -- the just-published release is
        unreachable via a plain `pip install --upgrade` / `uvx`."""
        with (
            patch.object(
                verify_pypi_latest, "_fetch_pypi_latest", return_value="0.111.10b0"
            ),
            patch.object(verify_pypi_latest, "time") as mock_time,
            patch("sys.argv", ["verify_pypi_latest.py", "0.1.3-beta"]),
        ):
            assert verify_pypi_latest.main() == 1
        mock_time.sleep.assert_called()
        assert "FAIL" in capsys.readouterr().err

    def test_fails_when_pypi_resolves_a_different_version_entirely(self, capsys):
        """A mismatch in either direction is a failure -- exact match is
        required, not just >=, since a concurrent/unexpected publish
        landing in between is just as broken as a stale un-yanked one."""
        with (
            patch.object(
                verify_pypi_latest, "_fetch_pypi_latest", return_value="0.1.4b0"
            ),
            patch.object(verify_pypi_latest, "time") as mock_time,
            patch("sys.argv", ["verify_pypi_latest.py", "0.1.3-beta"]),
        ):
            assert verify_pypi_latest.main() == 1
        mock_time.sleep.assert_called()

    def test_retries_before_succeeding_on_index_lag(self, capsys):
        with (
            patch.object(
                verify_pypi_latest,
                "_fetch_pypi_latest",
                side_effect=["0.1.2b0", "0.1.2b0", "0.1.3b0"],
            ),
            patch.object(verify_pypi_latest, "time") as mock_time,
            patch("sys.argv", ["verify_pypi_latest.py", "0.1.3-beta"]),
        ):
            assert verify_pypi_latest.main() == 0
        assert mock_time.sleep.call_count == 2

    def test_requires_exactly_one_argument(self):
        with patch("sys.argv", ["verify_pypi_latest.py"]):
            assert verify_pypi_latest.main() == 2

    def test_retries_through_transient_network_errors_then_succeeds(self):
        """_fetch_pypi_latest() returns None on a request exception (see
        its own try/except) -- main() must treat that as retryable, not
        let the exception crash the script on the first attempt with zero
        retries used."""
        with (
            patch.object(
                verify_pypi_latest,
                "_fetch_pypi_latest",
                side_effect=[None, None, "0.1.3b0"],
            ),
            patch.object(verify_pypi_latest, "time") as mock_time,
            patch("sys.argv", ["verify_pypi_latest.py", "0.1.3-beta"]),
        ):
            assert verify_pypi_latest.main() == 0
        assert mock_time.sleep.call_count == 2

    def test_fails_with_distinct_message_when_pypi_never_reachable(self, capsys):
        with (
            patch.object(verify_pypi_latest, "_fetch_pypi_latest", return_value=None),
            patch.object(verify_pypi_latest, "time") as mock_time,
            patch("sys.argv", ["verify_pypi_latest.py", "0.1.3-beta"]),
        ):
            assert verify_pypi_latest.main() == 1
        assert mock_time.sleep.call_count == verify_pypi_latest.MAX_ATTEMPTS - 1
        err = capsys.readouterr().err
        assert "FAIL" in err
        assert "could not reach PyPI" in err

    def test_fetch_pypi_latest_returns_none_on_request_exception(self):
        import requests

        with patch.object(
            verify_pypi_latest.requests,
            "get",
            side_effect=requests.exceptions.ConnectionError("boom"),
        ):
            assert verify_pypi_latest._fetch_pypi_latest() is None
