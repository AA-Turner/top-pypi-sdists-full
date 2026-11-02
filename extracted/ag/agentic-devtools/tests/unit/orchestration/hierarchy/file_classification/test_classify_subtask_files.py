"""Unit tests for file classification precedence and specialization (FR-007, FR-008)."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.file_classification import (
    classify_subtask_files,
)

_TASKS_MD = """\
# Tasks

- [ ] T001 Create `agentic_devtools/foo.py` and `docs/foo.md`
- [ ] T002 Create `agentic_devtools/bar.py` for a sibling task
"""


def test_classification_preserves_extensionless_and_dotfile_paths() -> None:
    tasks_md = "- [ ] T001 Create `Dockerfile`, `Makefile`, and `.gitignore`\n"
    result = classify_subtask_files(tasks_md_content=tasks_md, task_id="T001")
    assert result.paths == ("Dockerfile", "Makefile", ".gitignore")
