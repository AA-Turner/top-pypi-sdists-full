"""Unit tests for file classification precedence and specialization (FR-007, FR-008)."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.file_classification import (
    ClassificationSource,
    classify_subtask_files,
)

_TASKS_MD = """\
# Tasks

- [ ] T001 Create `agentic_devtools/foo.py` and `docs/foo.md`
- [ ] T002 Create `agentic_devtools/bar.py` for a sibling task
"""


def test_secondary_source_fallback_when_planning_artifact_empty() -> None:
    result = classify_subtask_files(
        tasks_md_content=None,
        task_id="T001",
        issue_description="Please update `src/thing.ts`",
    )
    assert result.source == ClassificationSource.SECONDARY_ISSUE_OR_DIFF
    assert result.paths == ("src/thing.ts",)


def test_secondary_source_uses_diff_paths_too() -> None:
    result = classify_subtask_files(
        tasks_md_content="",
        task_id="T001",
        issue_description="",
        diff_paths=("a/b.yaml",),
    )
    assert result.source == ClassificationSource.SECONDARY_ISSUE_OR_DIFF
    assert result.paths == ("a/b.yaml",)
