"""Tests for the hallucinated-command guard in execute_command.

Catches the bug from the user's live sage session:

  you> [paste of long ad-platform prompt]
  sage> ## STEP 1: ...
  - **Command:**
    `python -m CREATE_DBAPI_TABLES --model_path=models/ --db_path=/db Postgres`
  /usr/local/anaconda3/bin/python: No module named CREATE_DBAPI_TABLES

Sage tried to subprocess a fictional module the model invented. The new
guard short-circuits these before they reach subprocess.
"""

from __future__ import annotations

import pytest

from sage.core.commands import _check_hallucinated_command, execute_command


class TestUppercaseHallucination:
    """All-uppercase module names are never real Python modules."""

    def test_create_dbapi_tables_is_caught(self):
        result = _check_hallucinated_command(
            "python -m CREATE_DBAPI_TABLES --model_path=models/"
        )
        assert result is not None
        assert "all-uppercase" in result.lower() or "hallucinated" in result.lower()

    def test_screaming_snake_case_is_caught(self):
        result = _check_hallucinated_command("python -m INIT_DATABASE")
        assert result is not None

    def test_real_module_passes(self):
        # `pytest` is definitely installed in any sage dev environment
        result = _check_hallucinated_command("python -m pytest tests/")
        assert result is None


class TestModuleSpecLookup:
    """Modules that aren't installed are caught even if they look real."""

    def test_unknown_lowercase_module_is_caught(self):
        result = _check_hallucinated_command(
            "python -m totally_fake_module_xyz123 --arg foo"
        )
        assert result is not None
        assert "not installed" in result.lower()

    def test_installed_module_with_args_passes(self):
        result = _check_hallucinated_command("python -m sage --help")
        assert result is None


class TestEdgeCases:

    def test_short_python_command_ignored(self):
        # `python -c "..."` is not a module load — should pass
        result = _check_hallucinated_command('python -c "print(1)"')
        assert result is None

    def test_non_python_command_ignored(self):
        result = _check_hallucinated_command("ls -la")
        assert result is None

    def test_unparseable_command_passes_through(self):
        # Bad quoting should not raise from the guard
        result = _check_hallucinated_command('python -m "unterminated')
        assert result is None  # Defers to downstream parser

    def test_python3_alias_handled(self):
        result = _check_hallucinated_command("python3 -m TOTALLY_FAKE_MODULE")
        assert result is not None


class TestExecuteCommandIntegration:
    """The guard hooks into execute_command and returns a CommandResult."""

    def test_execute_command_rejects_hallucinated_module(self):
        result = execute_command(
            "python -m CREATE_DBAPI_TABLES",
            validate=False,  # Bypass other allowlist checks
        )
        assert result.success is False
        assert result.returncode == -1
        assert "hallucinated" in (result.error or "").lower() or \
               "all-uppercase" in (result.error or "").lower()
