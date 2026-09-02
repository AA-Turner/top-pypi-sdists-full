"""Tests for path_globs in derive_customization_disposition."""

from __future__ import annotations

from tests.scripts.derive_customization_disposition import derive


def test_finds_path_and_extension_globs() -> None:
    """A glob needs a path separator or a file extension to be one."""
    body = "Applies to `agentic_devtools/**/*.py` and to `*.md`.\n"
    assert derive.path_globs(body) == ["agentic_devtools/**/*.py", "*.md"]


def test_non_glob_spans_are_ignored() -> None:
    """A bare wildcard in prose is not a path glob."""
    assert derive.path_globs("Use `agdt-set` and `a*b`.") == []


def test_finds_glob_inside_key_value_inline_code() -> None:
    """A wildcard path in a quoted inline-code value is still a glob."""
    body = 'Use `applyTo: "agentic_devtools/cli/**/*.py"` for this rule.\n'
    assert derive.path_globs(body) == ["agentic_devtools/cli/**/*.py"]
