"""Unit tests for workflow.py trace-recording helpers, completion wiring, and status messages."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.scopes import (
    FileBoundary,
    SpecializationCategory,
    make_subtask_scope,
)
from agentic_devtools.orchestration.hierarchy.workflow import (
    provision_scope_agent,
)


def test_provision_scope_agent_maps_capabilities_without_mutating_scope() -> None:
    agent = make_subtask_scope(
        agent_id="subtask-1",
        issue_key="1",
        file_boundary=FileBoundary(("a.py",)),
        specialization=SpecializationCategory.PYTHON,
    )
    available = frozenset(
        (
            "read_repository",
            "search_repository",
            "inspect_diff",
            "report_result",
            "write_files",
            "version_control",
            "python_language",
            "python_test",
            "python_lint_typecheck",
        )
    )
    provisioned = provision_scope_agent(agent, available)
    assert provisioned.capabilities[-1] == "python_lint_typecheck"
    assert provisioned.file_boundary == agent.file_boundary
