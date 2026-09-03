"""Unit tests for file classification precedence and specialization (FR-007, FR-008)."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.file_classification import (
    classify_candidate_list,
    provision_subtask_agents,
)
from agentic_devtools.orchestration.hierarchy.scopes import SpecializationCategory

_TASKS_MD = """\
# Tasks

- [ ] T001 Create `agentic_devtools/foo.py` and `docs/foo.md`
- [ ] T002 Create `agentic_devtools/bar.py` for a sibling task
"""


def test_provision_subtask_agents_creates_disjoint_specialized_boundaries() -> None:
    result = classify_candidate_list(("a.py", "b.md", "c.bin"))
    agents = provision_subtask_agents("42", result)
    assert {agent.specialization for agent in agents} == {
        SpecializationCategory.PYTHON,
        SpecializationCategory.MARKDOWN,
        SpecializationCategory.UNSUPPORTED_OR_BINARY,
    }
    assert {path for agent in agents for path in agent.file_boundary.paths} == set(result.paths)
    assert all(agent.can_modify_files for agent in agents)


def test_provision_subtask_agents_keeps_exhausted_source_discovery_only() -> None:
    agents = provision_subtask_agents("42", classify_candidate_list(()))
    assert len(agents) == 1
    assert agents[0].discovery_only
    assert agents[0].file_boundary.is_empty
