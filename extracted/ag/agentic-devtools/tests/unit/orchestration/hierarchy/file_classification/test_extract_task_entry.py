"""Unit tests for extracting a task entry from tasks.md content."""

from __future__ import annotations


def test_extract_task_entry_includes_indented_continuations_only() -> None:
    """Planning extraction keeps continuation lines and stops at the next task."""
    from agentic_devtools.orchestration.hierarchy.file_classification import extract_task_entry

    content = "- [ ] T001 Create `src/main.py`\n  also updates `README.md`\n- [ ] T002 `other.py`"
    assert extract_task_entry(content, "T001") == "- [ ] T001 Create `src/main.py`\n  also updates `README.md`"
