"""Unit tests for file classification precedence and specialization (FR-007, FR-008)."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.file_classification import (
    ClassificationOutcome,
    ClassificationSource,
    classify_candidate_list,
)
from agentic_devtools.orchestration.hierarchy.scopes import SpecializationCategory

_TASKS_MD = """\
# Tasks

- [ ] T001 Create `agentic_devtools/foo.py` and `docs/foo.md`
- [ ] T002 Create `agentic_devtools/bar.py` for a sibling task
"""


def test_classify_candidate_list_empty_remains_discovery_only() -> None:
    result = classify_candidate_list(())
    assert result.outcome == ClassificationOutcome.DISCOVERY_ONLY_UNCLASSIFIED


def test_classify_candidate_list_nonempty_classifies() -> None:
    result = classify_candidate_list(("a.py", "b.md", "c.bin"))
    assert result.source == ClassificationSource.DISCOVERY_CANDIDATE_LIST
    assert result.outcome == ClassificationOutcome.CLASSIFIED
    assert SpecializationCategory.PYTHON in result.by_category
    assert SpecializationCategory.MARKDOWN in result.by_category
    assert SpecializationCategory.UNSUPPORTED_OR_BINARY in result.by_category
