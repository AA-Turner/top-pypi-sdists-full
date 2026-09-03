"""Unit tests for file classification precedence and specialization (FR-007, FR-008)."""

from __future__ import annotations

_TASKS_MD = """\
# Tasks

- [ ] T001 Create `agentic_devtools/foo.py` and `docs/foo.md`
- [ ] T002 Create `agentic_devtools/bar.py` for a sibling task
"""


def test_classification_excludes_code_identifiers_in_backtick_tokens() -> None:
    """Tokens with parentheses (function calls) and bare identifiers are filtered out."""
    from agentic_devtools.orchestration.hierarchy.file_classification import (
        _looks_like_file_path,
    )

    assert _looks_like_file_path("agentic_devtools/foo.py") is True
    assert _looks_like_file_path("foo.py") is True
    assert _looks_like_file_path(".gitignore") is True
    assert _looks_like_file_path("Dockerfile") is True
    assert _looks_like_file_path("orchestrate_hierarchy_cmd()") is False
    assert _looks_like_file_path("__all__") is False
    assert _looks_like_file_path("SomeClass") is False


def test_classification_excludes_non_repository_paths() -> None:
    from agentic_devtools.orchestration.hierarchy.file_classification import _looks_like_file_path

    assert _looks_like_file_path("/etc/passwd") is False
    assert _looks_like_file_path("../outside.py") is False
    assert _looks_like_file_path("https://example.com/file.py") is False
