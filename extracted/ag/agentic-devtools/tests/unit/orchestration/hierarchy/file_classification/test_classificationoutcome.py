"""Unit tests for file classification precedence and specialization (FR-007, FR-008)."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.file_classification import (
    ClassificationOutcome,
    ClassificationSource,
    classify_subtask_files,
)

_TASKS_MD = """\
# Tasks

- [ ] T001 Create `agentic_devtools/foo.py` and `docs/foo.md`
- [ ] T002 Create `agentic_devtools/bar.py` for a sibling task
"""


def test_planning_artifact_is_authoritative_and_excludes_sibling_paths() -> None:
    result = classify_subtask_files(tasks_md_content=_TASKS_MD, task_id="T001")
    assert result.source == ClassificationSource.PLANNING_ARTIFACT
    assert result.outcome == ClassificationOutcome.CLASSIFIED
    assert set(result.paths) == {"agentic_devtools/foo.py", "docs/foo.md"}
    assert "agentic_devtools/bar.py" not in result.paths


def test_exhausted_sources_yields_discovery_only_unclassified() -> None:
    result = classify_subtask_files(tasks_md_content=None, task_id="T001")
    assert result.source == ClassificationSource.EXHAUSTED_SOURCES
    assert result.outcome == ClassificationOutcome.DISCOVERY_ONLY_UNCLASSIFIED
    assert result.paths == ()
    assert result.is_discovery_only
