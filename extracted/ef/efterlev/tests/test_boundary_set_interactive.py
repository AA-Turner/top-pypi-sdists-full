"""Tests for `efterlev boundary set --interactive`.

Held in LIMITATIONS.md "Future ideas" since v0.1.18+; ships as a
single-PR feature in v0.1.54. The interactive helper walks the user
through include + exclude glob entry instead of requiring them to
remember the --include/--exclude flag syntax.

Tests use the typer CliRunner's `input=` parameter to feed the
prompt; the prompt collects globs until an empty input ends each
section, then asks for confirmation before writing config.toml.
"""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from efterlev.cli.main import app

runner = CliRunner()


def _init_workspace(tmp_path: Path) -> None:
    """Run `efterlev init` in tmp_path so config.toml exists."""
    result = runner.invoke(app, ["init", "--target", str(tmp_path)])
    assert result.exit_code == 0, result.output


def _read_config(tmp_path: Path) -> str:
    return (tmp_path / ".efterlev" / "config.toml").read_text(encoding="utf-8")


# --- happy path: includes + excludes via interactive prompt ------------------


def test_interactive_collects_includes_and_excludes(tmp_path: Path) -> None:
    """Two include globs + one exclude glob via interactive prompts;
    config.toml ends up with both."""
    _init_workspace(tmp_path)
    # Sequence: 2 includes, empty (end includes), 1 exclude, empty (end
    # excludes), confirm "y".
    user_input = "infra/**\n.github/workflows/**\n\nvendor/**\n\ny\n"
    result = runner.invoke(
        app,
        ["boundary", "set", "--target", str(tmp_path), "--interactive"],
        input=user_input,
    )
    assert result.exit_code == 0, result.output
    config = _read_config(tmp_path)
    assert 'include = ["infra/**", ".github/workflows/**"]' in config
    assert 'exclude = ["vendor/**"]' in config


def test_interactive_only_includes_no_excludes(tmp_path: Path) -> None:
    """User can finish the exclude section immediately (just hit
    enter)."""
    _init_workspace(tmp_path)
    # 1 include, empty (end includes), empty (end excludes immediately), confirm.
    user_input = "infra/**\n\n\ny\n"
    result = runner.invoke(
        app,
        ["boundary", "set", "--target", str(tmp_path), "--interactive"],
        input=user_input,
    )
    assert result.exit_code == 0, result.output
    config = _read_config(tmp_path)
    assert 'include = ["infra/**"]' in config
    # The TOML serializer omits empty list fields under [boundary]; verify
    # by searching for the explicit empty-exclude-list serialization OR the
    # absence of an exclude line.
    assert "exclude = []" in config or "exclude = " not in config


# --- mutual exclusion + empty inputs ----------------------------------------


def test_interactive_mutually_exclusive_with_include_flag(tmp_path: Path) -> None:
    """--interactive + --include is rejected with exit 2 and a clear
    error message."""
    _init_workspace(tmp_path)
    result = runner.invoke(
        app,
        [
            "boundary",
            "set",
            "--target",
            str(tmp_path),
            "--interactive",
            "--include",
            "infra/**",
        ],
    )
    assert result.exit_code == 2
    assert "mutually exclusive" in result.output


def test_interactive_mutually_exclusive_with_exclude_flag(tmp_path: Path) -> None:
    """Same for --exclude."""
    _init_workspace(tmp_path)
    result = runner.invoke(
        app,
        [
            "boundary",
            "set",
            "--target",
            str(tmp_path),
            "--interactive",
            "--exclude",
            "vendor/**",
        ],
    )
    assert result.exit_code == 2
    assert "mutually exclusive" in result.output


def test_interactive_empty_globs_aborts(tmp_path: Path) -> None:
    """No includes AND no excludes supplied: refuses to write
    (would wipe existing config) with exit 2."""
    _init_workspace(tmp_path)
    # End each section immediately.
    user_input = "\n\n"
    result = runner.invoke(
        app,
        ["boundary", "set", "--target", str(tmp_path), "--interactive"],
        input=user_input,
    )
    assert result.exit_code == 2
    assert "no include or exclude globs supplied" in result.output


# --- confirmation aborts cleanly --------------------------------------------


def test_interactive_decline_confirmation_does_not_write(tmp_path: Path) -> None:
    """If the user answers 'n' to the confirmation prompt, no config
    changes are written. Exit 0 (clean abort)."""
    _init_workspace(tmp_path)
    config_before = _read_config(tmp_path)
    user_input = "infra/**\n\n\nn\n"
    result = runner.invoke(
        app,
        ["boundary", "set", "--target", str(tmp_path), "--interactive"],
        input=user_input,
    )
    assert result.exit_code == 0
    assert "Aborted" in result.output
    config_after = _read_config(tmp_path)
    assert config_before == config_after  # unchanged
