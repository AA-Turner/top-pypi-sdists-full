"""Integration tests for ``task --syntax`` CLI mode.

These tests exercise the full pipeline: CLI argument parsing → syntax
short-circuit → SyntaxChecker → SyntaxReport → stdout / exit code.

Tests run in-process (like ``test_workers_cli.py``) to avoid PYTHONPATH
complications caused by Cython extensions not being compiled in the
worktree.  The same code paths are exercised.

CLI syntax used in tests:
    task --syntax -P /path/to/file.yaml
    task --syntax --syntax-path /path/to/file.yaml
    task --syntax --syntax-path -    (stdin)
    task -p PROGRAM -t TASK --syntax
"""
import sys
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import orjson
import pytest

from flowtask.parsers.argparser import ConfigParser
from flowtask.parsers.syntax.checker import SyntaxChecker
from flowtask.parsers.syntax.registry import ComponentSchemaRegistry


# Directory containing the fixture task files.
FIXTURES = Path(__file__).parent / "fixtures" / "syntax"


def _parse_args(args):
    """Return the parsed options namespace for a list of CLI args."""
    p = ConfigParser()
    p.parse(args)
    return p.options


def _fake_registry(tmp_path: Path) -> ComponentSchemaRegistry:
    """Build a minimal docs/ tree with AddDataset for testing."""
    components = tmp_path / "components"
    components.mkdir()
    (tmp_path / "index.json").write_bytes(orjson.dumps({
        "components": {
            "AddDataset": {
                "schema": "components/AddDataset.schema.json",
                "doc": "components/AddDataset.doc.json",
            }
        }
    }))
    (components / "AddDataset.schema.json").write_bytes(orjson.dumps({
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "title": "AddDataset",
        "properties": {"dataset": {"type": "string"}},
        "required": ["dataset"],
        "additionalProperties": False,
    }))
    return ComponentSchemaRegistry(docs_dir=tmp_path)


# ---------------------------------------------------------------------------
# Argparser tests
# ---------------------------------------------------------------------------

def test_argparser_syntax_flag_sets_syntax_true():
    """``--syntax`` sets options.syntax = True."""
    opts = _parse_args(["--syntax", "-P", str(FIXTURES / "clean.yaml")])
    assert opts.syntax is True


def test_argparser_syntax_path_captured():
    """The -P / --syntax-path flag captures the path in ``syntax_path``."""
    opts = _parse_args(["--syntax", "-P", str(FIXTURES / "clean.yaml")])
    assert opts.syntax_path == str(FIXTURES / "clean.yaml")


def test_argparser_syntax_path_long_form():
    """``--syntax-path`` (long form) also captures the path."""
    opts = _parse_args(["--syntax", "--syntax-path", str(FIXTURES / "clean.yaml")])
    assert opts.syntax_path == str(FIXTURES / "clean.yaml")


def test_argparser_syntax_format_default_text():
    """``--syntax-format`` defaults to ``'text'``."""
    opts = _parse_args(["--syntax", "-P", str(FIXTURES / "clean.yaml")])
    assert opts.syntax_format == "text"


def test_argparser_syntax_format_json():
    """``--syntax-format json`` is accepted."""
    opts = _parse_args([
        "--syntax", "--syntax-format", "json",
        "-P", str(FIXTURES / "clean.yaml"),
    ])
    assert opts.syntax_format == "json"


def test_argparser_strict_flag():
    """``--strict`` sets ``syntax_strict = True``."""
    opts = _parse_args([
        "--syntax", "--strict",
        "-P", str(FIXTURES / "clean.yaml"),
    ])
    assert opts.syntax_strict is True


def test_argparser_existing_flags_unchanged():
    """Existing flags still parse correctly alongside the new ones."""
    opts = _parse_args(["-p", "myprogram", "-t", "mytask"])
    assert opts.program == "myprogram"
    assert opts.task == "mytask"


def test_argparser_workers_subcommand_unchanged():
    """The workers subcommand still works with the new flags present."""
    opts = _parse_args(["workers", "queues"])
    assert opts.workers_command == "workers"
    assert opts.workers_action == "queues"


# ---------------------------------------------------------------------------
# _handle_syntax_command tests
# ---------------------------------------------------------------------------

def test_handle_syntax_command_no_path_returns_two(capsys):
    """With no path and no -t TASK, exit code should be 2."""
    from flowtask.__main__ import _handle_syntax_command
    opts = _parse_args(["--syntax"])  # no path, no -t
    result = _handle_syntax_command(opts)
    assert result == 2


def test_handle_syntax_command_clean_task_exit_zero(tmp_path, capsys):
    """A valid task file with a known component should exit 0."""
    registry = _fake_registry(tmp_path)

    from flowtask.__main__ import _handle_syntax_command
    opts = _parse_args(["--syntax", "-P", str(FIXTURES / "clean.yaml")])

    with patch(
        "flowtask.parsers.syntax.checker.ComponentSchemaRegistry",
        return_value=registry,
    ):
        result = _handle_syntax_command(opts)

    assert result == 0, capsys.readouterr().out


def test_handle_syntax_command_error_task_exit_one(tmp_path, capsys):
    """A task missing required attributes should exit 1."""
    registry = _fake_registry(tmp_path)

    from flowtask.__main__ import _handle_syntax_command
    opts = _parse_args([
        "--syntax",
        "-P", str(FIXTURES / "missing_required.yaml"),
    ])

    with patch(
        "flowtask.parsers.syntax.checker.ComponentSchemaRegistry",
        return_value=registry,
    ):
        result = _handle_syntax_command(opts)

    assert result == 1


def test_handle_syntax_command_json_format(tmp_path, capsys):
    """``--syntax-format json`` should emit a JSON document on stdout."""
    # Empty registry — AddDataset will be flagged as W_UNDOCUMENTED.
    registry = ComponentSchemaRegistry(docs_dir=tmp_path)

    from flowtask.__main__ import _handle_syntax_command
    opts = _parse_args([
        "--syntax", "--syntax-format", "json",
        "-P", str(FIXTURES / "clean.yaml"),
    ])

    with patch(
        "flowtask.parsers.syntax.checker.ComponentSchemaRegistry",
        return_value=registry,
    ):
        _handle_syntax_command(opts)

    captured = capsys.readouterr().out
    payload = orjson.loads(captured)
    assert set(payload.keys()) >= {"file", "fmt", "ok", "issues"}


def test_handle_syntax_root_error_text_output(tmp_path, capsys):
    """A task missing 'name' should produce E_ROOT_SCHEMA in text output."""
    bad_task = tmp_path / "no_name.yaml"
    bad_task.write_text("steps:\n  - AddDataset:\n      dataset: x\n")

    registry = ComponentSchemaRegistry(docs_dir=tmp_path)

    from flowtask.__main__ import _handle_syntax_command
    opts = _parse_args(["--syntax", "-P", str(bad_task)])

    with patch(
        "flowtask.parsers.syntax.checker.ComponentSchemaRegistry",
        return_value=registry,
    ):
        result = _handle_syntax_command(opts)

    assert result == 1
    captured = capsys.readouterr().out
    assert "E_ROOT_SCHEMA" in captured


def test_handle_syntax_stdin(capsys, monkeypatch):
    """``--syntax-path -`` reads from stdin and validates."""
    content = "name: t\nsteps:\n  - AddDataset:\n      dataset: x\n"
    monkeypatch.setattr(sys, "stdin", StringIO(content))

    opts = _parse_args(["--syntax", "--syntax-path", "-"])

    from flowtask.__main__ import _handle_syntax_command
    result = _handle_syntax_command(opts)
    # We accept 0 or 1 depending on whether registry resolves AddDataset.
    assert result in (0, 1)


def test_cli_syntax_does_not_load_taskrunner():
    """Importing the syntax subpackage must NOT import flowtask.runner.TaskRunner.

    This test verifies the module-level guarantee using in-process
    sys.modules inspection.
    """
    # Remove flowtask.runner from sys.modules if present to get a clean slate.
    sys.modules.pop("flowtask.runner", None)
    # Import the syntax subpackage (triggering all lazy imports).
    import flowtask.parsers.syntax  # noqa: F401
    assert "flowtask.runner" not in sys.modules, (
        "flowtask.runner was imported as a side-effect of importing the "
        "syntax subpackage.  The --syntax path must not load TaskRunner."
    )


def test_handle_syntax_command_does_not_invoke_taskrunner(tmp_path, capsys):
    """Running the full --syntax dispatch must never load flowtask.runner.

    This is a stronger guard than just importing the syntax subpackage:
    it verifies that the actual CLI dispatch path (_handle_syntax_command)
    does not trigger TaskRunner as a side-effect.
    """
    from flowtask.__main__ import _handle_syntax_command

    registry = _fake_registry(tmp_path)
    opts = _parse_args(["--syntax", "-P", str(FIXTURES / "clean.yaml")])

    # Ensure flowtask.runner is absent before the call.
    sys.modules.pop("flowtask.runner", None)

    with patch(
        "flowtask.parsers.syntax.checker.ComponentSchemaRegistry",
        return_value=registry,
    ):
        result = _handle_syntax_command(opts)

    assert "flowtask.runner" not in sys.modules, (
        "flowtask.runner was imported as a side-effect of running "
        "_handle_syntax_command. The --syntax dispatch must never load TaskRunner."
    )
    assert result in (0, 1), f"Expected exit 0 or 1, got {result}"


def test_handle_syntax_command_program_task_resolution(tmp_path):
    """``task -p PROGRAM -t TASK --syntax`` resolves through _resolve_task_path.

    Spec §5 acceptance criterion: the -p/-t path reaches the checker and
    returns exit 0 or 1 (not 2, which would mean path resolution failed).

    ``_resolve_task_path`` is patched to return a real file so the test does
    not need to import ``flowtask.conf`` (which requires a live navconfig env).
    """
    from flowtask.__main__ import _handle_syntax_command

    # A real YAML task file for the checker to validate.
    task_file = tmp_path / "demo.yaml"
    task_file.write_text("name: demo\nsteps:\n  - AddDataset:\n      dataset: x\n")

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    registry = _fake_registry(docs_dir)

    opts = _parse_args(["-p", "testprog", "-t", "demo", "--syntax"])

    with patch("flowtask.__main__._resolve_task_path", return_value=task_file), \
         patch("flowtask.parsers.syntax.checker.ComponentSchemaRegistry", return_value=registry):
        result = _handle_syntax_command(opts)

    # Exit 0 (no errors) or 1 (issues found) are both valid — 2 means not found.
    assert result in (0, 1), (
        f"Expected exit 0 or 1, got {result}. "
        "This means _handle_syntax_command did not route through the checker "
        "for the -p/-t path."
    )


def test_handle_syntax_text_format_contains_file_name(tmp_path, capsys):
    """Text output must contain the filename of the checked file."""
    registry = ComponentSchemaRegistry(docs_dir=tmp_path)

    from flowtask.__main__ import _handle_syntax_command
    opts = _parse_args(["--syntax", "-P", str(FIXTURES / "clean.yaml")])

    with patch(
        "flowtask.parsers.syntax.checker.ComponentSchemaRegistry",
        return_value=registry,
    ):
        _handle_syntax_command(opts)

    captured = capsys.readouterr().out
    assert "clean.yaml" in captured
