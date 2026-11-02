"""Tests for _build_copilot_args internal function."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.copilot import session as session_module
from agentic_devtools.cli.copilot.session import _build_copilot_args


class TestBuildCopilotArgsAutopilot:
    """Tests for the autopilot parameter in _build_copilot_args."""

    # ------------------------------------------------------------------
    # Standalone binary — interactive mode
    # ------------------------------------------------------------------

    def test_standalone_interactive_autopilot_true_includes_flag(self):
        """Standalone + interactive + autopilot=True → --autopilot before -i."""
        with patch.object(session_module, "_get_copilot_binary", return_value="/usr/bin/copilot"):
            result = _build_copilot_args("hello", interactive=True, autopilot=True)

        assert result is not None
        assert result[0] == "/usr/bin/copilot"
        assert "--autopilot" in result
        assert result.index("--autopilot") < result.index("-i")
        assert result[-1] == "hello"

    def test_standalone_interactive_autopilot_default_includes_flag(self):
        """Standalone + interactive + autopilot defaults to True → --autopilot included."""
        with patch.object(session_module, "_get_copilot_binary", return_value="/usr/bin/copilot"):
            result = _build_copilot_args("hello", interactive=True)

        assert result is not None
        assert "--autopilot" in result

    def test_standalone_interactive_autopilot_false_excludes_flag(self):
        """Standalone + interactive + autopilot=False → no --autopilot in args."""
        with patch.object(session_module, "_get_copilot_binary", return_value="/usr/bin/copilot"):
            result = _build_copilot_args("hello", interactive=True, autopilot=False)

        assert result is not None
        assert "--autopilot" not in result
        assert "-i" in result

    # ------------------------------------------------------------------
    # Standalone binary — non-interactive mode
    # ------------------------------------------------------------------

    def test_standalone_non_interactive_autopilot_true_excludes_flag(self):
        """Standalone + non-interactive + autopilot=True → no --autopilot (only --allow-all)."""
        with patch.object(session_module, "_get_copilot_binary", return_value="/usr/bin/copilot"):
            result = _build_copilot_args("hello", interactive=False, autopilot=True)

        assert result is not None
        assert "--autopilot" not in result
        assert "--allow-all" in result
        assert "-p" in result

    def test_standalone_non_interactive_autopilot_false_excludes_flag(self):
        """Standalone + non-interactive + autopilot=False → no --autopilot."""
        with patch.object(session_module, "_get_copilot_binary", return_value="/usr/bin/copilot"):
            result = _build_copilot_args("hello", interactive=False, autopilot=False)

        assert result is not None
        assert "--autopilot" not in result
        assert "--allow-all" in result

    # ------------------------------------------------------------------
    # Ordering: --autopilot before -i and before the prompt
    # ------------------------------------------------------------------

    def test_standalone_interactive_autopilot_ordering(self):
        """--autopilot then --allow-all appear after binary, before -i and prompt."""
        with patch.object(session_module, "_get_copilot_binary", return_value="/usr/bin/copilot"):
            result = _build_copilot_args("my prompt", interactive=True, autopilot=True)

        assert result == ["/usr/bin/copilot", "--autopilot", "--allow-all", "-i", "my prompt"]

    # ------------------------------------------------------------------
    # gh copilot fallback — interactive mode
    # ------------------------------------------------------------------

    def test_fallback_interactive_autopilot_true_emits_warning(self):
        """gh copilot fallback + interactive + autopilot=True → warning emitted."""
        with patch.object(session_module, "_get_copilot_binary", return_value=None):
            with patch.object(session_module.shutil, "which", return_value=None):
                with pytest.warns(UserWarning, match="--autopilot is not supported"):
                    result = _build_copilot_args("hello", interactive=True, autopilot=True)

        assert result == ["gh", "copilot", "suggest", "hello"]

    def test_fallback_interactive_autopilot_false_no_warning(self):
        """gh copilot fallback + interactive + autopilot=False → no warning."""
        with patch.object(session_module, "_get_copilot_binary", return_value=None):
            with patch.object(session_module.shutil, "which", return_value=None):
                result = _build_copilot_args("hello", interactive=True, autopilot=False)

        assert result == ["gh", "copilot", "suggest", "hello"]

    def test_fallback_non_interactive_autopilot_true_no_warning(self):
        """gh copilot fallback + non-interactive + autopilot=True → no warning."""
        with patch.object(session_module, "_get_copilot_binary", return_value=None):
            with patch.object(session_module.shutil, "which", return_value=None):
                result = _build_copilot_args("hello", interactive=False, autopilot=True)

        assert result == ["gh", "copilot", "suggest", "hello"]


class TestBuildCopilotArgsModel:
    """Tests for the model parameter in _build_copilot_args."""

    # ------------------------------------------------------------------
    # Standalone binary — model included
    # ------------------------------------------------------------------

    def test_standalone_interactive_model_included(self):
        """Standalone + interactive + model → --model <value> before -i."""
        with patch.object(session_module, "_get_copilot_binary", return_value="/usr/bin/copilot"):
            result = _build_copilot_args("hello", interactive=True, model="gemini-pro-3.1")

        assert result is not None
        assert "--model" in result
        assert "gemini-pro-3.1" in result
        model_idx = result.index("--model")
        assert result[model_idx + 1] == "gemini-pro-3.1"
        assert model_idx < result.index("-i")

    def test_standalone_non_interactive_model_included(self):
        """Standalone + non-interactive + model → --model <value> before -p."""
        with patch.object(session_module, "_get_copilot_binary", return_value="/usr/bin/copilot"):
            result = _build_copilot_args("hello", interactive=False, model="gemini-pro-3.1")

        assert result is not None
        assert "--model" in result
        model_idx = result.index("--model")
        assert result[model_idx + 1] == "gemini-pro-3.1"
        assert model_idx < result.index("-p")

    def test_standalone_model_none_excludes_flag(self):
        """Standalone + model=None → no --model in args."""
        with patch.object(session_module, "_get_copilot_binary", return_value="/usr/bin/copilot"):
            result = _build_copilot_args("hello", interactive=True, model=None)

        assert result is not None
        assert "--model" not in result

    def test_standalone_model_empty_string_excludes_flag(self):
        """Standalone + model="" → treated as None, no --model in args."""
        with patch.object(session_module, "_get_copilot_binary", return_value="/usr/bin/copilot"):
            result = _build_copilot_args("hello", interactive=True, model="")

        assert result is not None
        assert "--model" not in result

    def test_standalone_model_whitespace_only_excludes_flag(self):
        """Standalone + model="  " → treated as None, no --model in args."""
        with patch.object(session_module, "_get_copilot_binary", return_value="/usr/bin/copilot"):
            result = _build_copilot_args("hello", interactive=True, model="   ")

        assert result is not None
        assert "--model" not in result

    # ------------------------------------------------------------------
    # Ordering: --autopilot, --model, -i, prompt
    # ------------------------------------------------------------------

    def test_standalone_interactive_model_ordering(self):
        """--autopilot before --allow-all before --model before -i before prompt."""
        with patch.object(session_module, "_get_copilot_binary", return_value="/usr/bin/copilot"):
            result = _build_copilot_args("my prompt", interactive=True, autopilot=True, model="gpt-4")

        assert result == ["/usr/bin/copilot", "--autopilot", "--allow-all", "--model", "gpt-4", "-i", "my prompt"]

    def test_standalone_non_interactive_model_ordering(self):
        """--allow-all before --model before -p before prompt."""
        with patch.object(session_module, "_get_copilot_binary", return_value="/usr/bin/copilot"):
            result = _build_copilot_args("my prompt", interactive=False, model="gpt-4")

        assert result == ["/usr/bin/copilot", "--allow-all", "--model", "gpt-4", "-p", "my prompt"]

    # ------------------------------------------------------------------
    # gh copilot fallback — model warning
    # ------------------------------------------------------------------

    def test_fallback_model_emits_warning(self):
        """gh copilot fallback + model → warning emitted, no --model in args."""
        with patch.object(session_module, "_get_copilot_binary", return_value=None):
            with patch.object(session_module.shutil, "which", return_value=None):
                with pytest.warns(UserWarning, match="--model is not supported"):
                    result = _build_copilot_args("hello", interactive=True, autopilot=False, model="gpt-4")

        assert result == ["gh", "copilot", "suggest", "hello"]
        assert "--model" not in result

    def test_fallback_model_none_no_warning(self):
        """gh copilot fallback + model=None → no model warning."""
        with patch.object(session_module, "_get_copilot_binary", return_value=None):
            with patch.object(session_module.shutil, "which", return_value=None):
                result = _build_copilot_args("hello", interactive=True, autopilot=False, model=None)

        assert result == ["gh", "copilot", "suggest", "hello"]


class TestBuildCopilotArgsAllowAll:
    """Tests for the allow_all parameter in _build_copilot_args."""

    def test_standalone_interactive_allow_all_default_includes_flag(self):
        """Standalone + interactive + allow_all defaults to True → --allow-all included."""
        with patch.object(session_module, "_get_copilot_binary", return_value="/usr/bin/copilot"):
            result = _build_copilot_args("hello", interactive=True)

        assert result is not None
        assert "--allow-all" in result

    def test_standalone_interactive_allow_all_true_before_flag(self):
        """Standalone + interactive + allow_all=True → --allow-all before -i."""
        with patch.object(session_module, "_get_copilot_binary", return_value="/usr/bin/copilot"):
            result = _build_copilot_args("hello", interactive=True, allow_all=True)

        assert result is not None
        assert "--allow-all" in result
        assert result.index("--allow-all") < result.index("-i")

    def test_standalone_interactive_allow_all_false_excludes_flag(self):
        """Standalone + interactive + allow_all=False → no --allow-all (restores prompt)."""
        with patch.object(session_module, "_get_copilot_binary", return_value="/usr/bin/copilot"):
            result = _build_copilot_args("hello", interactive=True, allow_all=False)

        assert result is not None
        assert "--allow-all" not in result
        assert "-i" in result

    def test_standalone_interactive_allow_all_false_keeps_autopilot(self):
        """Standalone + interactive + allow_all=False keeps --autopilot but drops --allow-all."""
        with patch.object(session_module, "_get_copilot_binary", return_value="/usr/bin/copilot"):
            result = _build_copilot_args("hi", interactive=True, autopilot=True, allow_all=False)

        assert result == ["/usr/bin/copilot", "--autopilot", "-i", "hi"]

    def test_standalone_non_interactive_allow_all_false_still_includes_flag(self):
        """Standalone + non-interactive + allow_all=False → --allow-all still forced."""
        with patch.object(session_module, "_get_copilot_binary", return_value="/usr/bin/copilot"):
            result = _build_copilot_args("hello", interactive=False, allow_all=False)

        assert result is not None
        assert "--allow-all" in result
        assert "-p" in result

    def test_standalone_non_interactive_allow_all_true_includes_flag(self):
        """Standalone + non-interactive + allow_all=True → --allow-all included."""
        with patch.object(session_module, "_get_copilot_binary", return_value="/usr/bin/copilot"):
            result = _build_copilot_args("hello", interactive=False, allow_all=True)

        assert result is not None
        assert "--allow-all" in result

    def test_standalone_interactive_allow_all_ordering(self):
        """--autopilot before --allow-all before --model before -i before prompt."""
        with patch.object(session_module, "_get_copilot_binary", return_value="/usr/bin/copilot"):
            result = _build_copilot_args("my prompt", interactive=True, autopilot=True, allow_all=True, model="gpt-4")

        assert result == [
            "/usr/bin/copilot",
            "--autopilot",
            "--allow-all",
            "--model",
            "gpt-4",
            "-i",
            "my prompt",
        ]

    def test_fallback_interactive_allow_all_no_extra_flag(self):
        """gh copilot fallback ignores allow_all (no --allow-all in positional args)."""
        with patch.object(session_module, "_get_copilot_binary", return_value=None):
            with patch.object(session_module.shutil, "which", return_value=None):
                result = _build_copilot_args("hello", interactive=True, autopilot=False, allow_all=True)

        assert result == ["gh", "copilot", "suggest", "hello"]
        assert "--allow-all" not in result
