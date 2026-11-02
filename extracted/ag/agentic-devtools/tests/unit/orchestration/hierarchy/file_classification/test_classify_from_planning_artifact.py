"""Unit tests for file classification precedence and specialization (FR-007, FR-008)."""

from __future__ import annotations

_TASKS_MD = """\
# Tasks

- [ ] T001 Create `agentic_devtools/foo.py` and `docs/foo.md`
- [ ] T002 Create `agentic_devtools/bar.py` for a sibling task
"""


def test_classify_from_planning_artifact_returns_empty_when_task_id_absent() -> None:
    from agentic_devtools.orchestration.hierarchy.file_classification import classify_from_planning_artifact

    assert classify_from_planning_artifact(_TASKS_MD, "T999") == ()
