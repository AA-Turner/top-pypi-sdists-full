"""Tests for resolve_autorun_enabled — combinatorial matrix over CLI flags × env vars × TTY/CI."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from agentic_devtools.cli.setup.autorun_resolution import (
    _is_ci_environment,
    _is_env_truthy,
    _is_interactive,
    resolve_autorun_enabled,
)


# ---------------------------------------------------------------------------
# _is_env_truthy
# ---------------------------------------------------------------------------
class TestIsEnvTruthy:
    """Tests for the _is_env_truthy helper."""

    @pytest.mark.parametrize("value", ["1", "true", "yes", "TRUE", "True", "YES", "Yes"])
    def test_truthy_values(self, value: str) -> None:
        with patch.dict("os.environ", {"MY_VAR": value}):
            assert _is_env_truthy("MY_VAR") is True

    @pytest.mark.parametrize("value", ["0", "false", "no", "maybe", ""])
    def test_non_truthy_values(self, value: str) -> None:
        with patch.dict("os.environ", {"MY_VAR": value}):
            assert _is_env_truthy("MY_VAR") is False

    def test_unset_variable(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            assert _is_env_truthy("NONEXISTENT") is False


# ---------------------------------------------------------------------------
# _is_ci_environment
# ---------------------------------------------------------------------------
class TestIsCiEnvironment:
    """Tests for CI environment detection."""

    @pytest.mark.parametrize("var", ["CI", "GITHUB_ACTIONS", "TF_BUILD", "BUILD_BUILDID"])
    def test_each_ci_indicator_detected(self, var: str) -> None:
        with patch.dict("os.environ", {var: "true"}, clear=True):
            assert _is_ci_environment() is True

    def test_no_ci_vars(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            assert _is_ci_environment() is False

    def test_ci_var_empty_string(self) -> None:
        with patch.dict("os.environ", {"CI": ""}, clear=True):
            assert _is_ci_environment() is False


# ---------------------------------------------------------------------------
# _is_interactive
# ---------------------------------------------------------------------------
class TestIsInteractive:
    """Tests for TTY/interactive detection."""

    def test_tty_true(self) -> None:
        with patch("sys.stdin") as mock_stdin:
            mock_stdin.isatty.return_value = True
            assert _is_interactive() is True

    def test_tty_false(self) -> None:
        with patch("sys.stdin") as mock_stdin:
            mock_stdin.isatty.return_value = False
            assert _is_interactive() is False

    def test_isatty_raises_oserror(self) -> None:
        with patch("sys.stdin") as mock_stdin:
            mock_stdin.isatty.side_effect = OSError("stdin closed")
            assert _is_interactive() is False

    def test_isatty_raises_attribute_error(self) -> None:
        with patch("sys.stdin", None):
            assert _is_interactive() is False


# ---------------------------------------------------------------------------
# resolve_autorun_enabled — full decision matrix
# ---------------------------------------------------------------------------
class TestResolveAutorunEnabled:
    """Combinatorial tests for the precedence chain in resolve_autorun_enabled."""

    # --- Tier 0: fail-fast guard ---
    def test_both_flags_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="mutually exclusive"):
            resolve_autorun_enabled(cli_run=True, cli_no_run=True)

    # --- Tier 1: --run flag ---
    def test_cli_run_true_returns_true(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            with patch("agentic_devtools.cli.setup.autorun_resolution._is_interactive", return_value=False):
                assert resolve_autorun_enabled(cli_run=True, cli_no_run=None) is True

    def test_cli_run_overrides_ci(self) -> None:
        with patch.dict("os.environ", {"CI": "true"}, clear=True):
            assert resolve_autorun_enabled(cli_run=True, cli_no_run=None) is True

    def test_cli_run_overrides_no_autorun_env(self) -> None:
        with patch.dict("os.environ", {"AGDT_SETUP_NO_AUTORUN": "1"}, clear=True):
            assert resolve_autorun_enabled(cli_run=True, cli_no_run=None) is True

    # --- Tier 2: --no-run flag ---
    def test_cli_no_run_true_returns_false(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            with patch("agentic_devtools.cli.setup.autorun_resolution._is_interactive", return_value=True):
                assert resolve_autorun_enabled(cli_run=None, cli_no_run=True) is False

    def test_cli_no_run_overrides_interactive(self) -> None:
        with patch("agentic_devtools.cli.setup.autorun_resolution._is_interactive", return_value=True):
            with patch.dict("os.environ", {}, clear=True):
                assert resolve_autorun_enabled(cli_run=None, cli_no_run=True) is False

    def test_cli_no_run_overrides_setup_run_env(self) -> None:
        with patch.dict("os.environ", {"AGDT_SETUP_RUN": "1"}, clear=True):
            assert resolve_autorun_enabled(cli_run=None, cli_no_run=True) is False

    # --- Tier 3: AGDT_SETUP_NO_AUTORUN ---
    def test_no_autorun_env_truthy_returns_false(self) -> None:
        with patch.dict("os.environ", {"AGDT_SETUP_NO_AUTORUN": "1"}, clear=True):
            with patch("agentic_devtools.cli.setup.autorun_resolution._is_interactive", return_value=True):
                assert resolve_autorun_enabled(cli_run=None, cli_no_run=None) is False

    def test_no_autorun_env_overrides_setup_run_env(self) -> None:
        with patch.dict("os.environ", {"AGDT_SETUP_NO_AUTORUN": "yes", "AGDT_SETUP_RUN": "1"}, clear=True):
            assert resolve_autorun_enabled(cli_run=None, cli_no_run=None) is False

    def test_no_autorun_env_overrides_interactive(self) -> None:
        with patch.dict("os.environ", {"AGDT_SETUP_NO_AUTORUN": "true"}, clear=True):
            with patch("agentic_devtools.cli.setup.autorun_resolution._is_interactive", return_value=True):
                assert resolve_autorun_enabled(cli_run=None, cli_no_run=None) is False

    def test_no_autorun_env_non_truthy_ignored(self) -> None:
        with patch.dict("os.environ", {"AGDT_SETUP_NO_AUTORUN": "0"}, clear=True):
            with patch("agentic_devtools.cli.setup.autorun_resolution._is_interactive", return_value=True):
                assert resolve_autorun_enabled(cli_run=None, cli_no_run=None) is True

    # --- Tier 4: AGDT_SETUP_RUN ---
    def test_setup_run_env_truthy_returns_true(self) -> None:
        with patch.dict("os.environ", {"AGDT_SETUP_RUN": "1"}, clear=True):
            assert resolve_autorun_enabled(cli_run=None, cli_no_run=None) is True

    def test_setup_run_env_overrides_ci(self) -> None:
        with patch.dict("os.environ", {"AGDT_SETUP_RUN": "true", "CI": "true"}, clear=True):
            assert resolve_autorun_enabled(cli_run=None, cli_no_run=None) is True

    def test_setup_run_env_overrides_non_tty(self) -> None:
        with patch.dict("os.environ", {"AGDT_SETUP_RUN": "yes"}, clear=True):
            with patch("agentic_devtools.cli.setup.autorun_resolution._is_interactive", return_value=False):
                assert resolve_autorun_enabled(cli_run=None, cli_no_run=None) is True

    def test_setup_run_env_non_truthy_ignored(self) -> None:
        with patch.dict("os.environ", {"AGDT_SETUP_RUN": "false"}, clear=True):
            with patch("agentic_devtools.cli.setup.autorun_resolution._is_interactive", return_value=True):
                assert resolve_autorun_enabled(cli_run=None, cli_no_run=None) is True

    @pytest.mark.parametrize("value", ["1", "true", "yes", "TRUE", "YES"])
    def test_setup_run_env_case_insensitive(self, value: str) -> None:
        with patch.dict("os.environ", {"AGDT_SETUP_RUN": value}, clear=True):
            assert resolve_autorun_enabled(cli_run=None, cli_no_run=None) is True

    # --- Tier 5: CI detected ---
    @pytest.mark.parametrize("var", ["CI", "GITHUB_ACTIONS", "TF_BUILD", "BUILD_BUILDID"])
    def test_ci_var_no_flags_returns_false(self, var: str) -> None:
        with patch.dict("os.environ", {var: "true"}, clear=True):
            assert resolve_autorun_enabled(cli_run=None, cli_no_run=None) is False

    def test_non_tty_no_ci_returns_false(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            with patch("agentic_devtools.cli.setup.autorun_resolution._is_interactive", return_value=False):
                assert resolve_autorun_enabled(cli_run=None, cli_no_run=None) is False

    # --- Tier 5 edge: isatty exception paths ---
    def test_isatty_oserror_returns_false(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            with patch("sys.stdin") as mock_stdin:
                mock_stdin.isatty.side_effect = OSError("stdin closed")
                assert resolve_autorun_enabled(cli_run=None, cli_no_run=None) is False

    def test_isatty_attribute_error_returns_false(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            with patch("sys.stdin", None):
                assert resolve_autorun_enabled(cli_run=None, cli_no_run=None) is False

    # --- Tier 6: interactive fallback ---
    def test_interactive_no_flags_no_env_returns_true(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            with patch("agentic_devtools.cli.setup.autorun_resolution._is_interactive", return_value=True):
                assert resolve_autorun_enabled(cli_run=None, cli_no_run=None) is True

    # --- None flags (not provided) ---
    def test_both_flags_none_falls_through(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            with patch("agentic_devtools.cli.setup.autorun_resolution._is_interactive", return_value=True):
                assert resolve_autorun_enabled(cli_run=None, cli_no_run=None) is True

    # --- False flags (explicit False, not None) ---
    def test_cli_run_false_treated_as_not_set(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            with patch("agentic_devtools.cli.setup.autorun_resolution._is_interactive", return_value=True):
                assert resolve_autorun_enabled(cli_run=False, cli_no_run=None) is True

    def test_cli_no_run_false_treated_as_not_set(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            with patch("agentic_devtools.cli.setup.autorun_resolution._is_interactive", return_value=True):
                assert resolve_autorun_enabled(cli_run=None, cli_no_run=False) is True
