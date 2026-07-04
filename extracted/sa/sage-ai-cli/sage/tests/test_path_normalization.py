from __future__ import annotations

from pathlib import Path


def test_normalize_platform_prefix_to_ai_platform(tmp_path: Path) -> None:
    from sage.cli_core import _normalize_workspace_relative_path

    (tmp_path / "ai-platform").mkdir()
    normalized = _normalize_workspace_relative_path("platform/sage/main.py", tmp_path)
    assert normalized == "ai-platform/sage/main.py"


def test_strip_ai_platform_prefix_when_running_inside_ai_platform(tmp_path: Path) -> None:
    from sage.cli_core import _normalize_workspace_relative_path

    root = tmp_path / "ai-platform"
    root.mkdir()
    normalized = _normalize_workspace_relative_path("ai-platform/sage/main.py", root)
    assert normalized == "sage/main.py"


def test_normalize_platform_prefix_when_running_inside_ai_platform(tmp_path: Path) -> None:
    from sage.cli_core import _normalize_workspace_relative_path

    root = tmp_path / "ai-platform"
    root.mkdir()
    # If ai-platform exists inside ai-platform, the bug was that it returned ai-platform/sage/main.py
    # because has_ai_platform_child was True.
    (root / "ai-platform").mkdir()
    normalized = _normalize_workspace_relative_path("platform/sage/main.py", root)
    assert normalized == "sage/main.py"


def test_extract_and_write_files_normalizes_and_writes_existing_file(tmp_path: Path) -> None:
    from sage.cli_core import _extract_and_write_files

    root = tmp_path / "ai-platform"
    (root / "sage").mkdir(parents=True)
    target = root / "sage" / "notes.md"
    target.write_text("before\n", encoding="utf-8")

    output = """FILE: ai-platform/sage/notes.md
```md
after
```
"""
    written = _extract_and_write_files(
        output,
        root,
        protected_files=set(),
        files_read=set(),
    )
    assert written == ["sage/notes.md"]
    assert target.read_text(encoding="utf-8") == "after\n"
