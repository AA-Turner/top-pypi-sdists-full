"""Tests for supervisor_dispatch_slugs in derive_customization_disposition."""

from __future__ import annotations

from tests.scripts.derive_customization_disposition import derive, unit


def test_supervisor_agent_type_reference_is_dispatched() -> None:
    """A supervisor `agent_type` reference dispatches a loaded supervision unit."""
    child = unit(slug="agdt.ai-pr-loop-supervision.worker", body="Work.\n")
    text = "Delegate to `agent_type: ai-pr-loop-supervision-worker`.\n"
    assert derive.supervisor_dispatch_slugs([child], text) == frozenset({"agdt.ai-pr-loop-supervision.worker"})


def test_supervisor_prose_reference_is_not_dispatched() -> None:
    """A prose mention of a supervision unit is not a dispatch declaration."""
    child = unit(slug="agdt.ai-pr-loop-supervision.worker", body="Work.\n")
    text = "The retired ai-pr-loop-supervision-worker must not be dispatched.\n"
    assert derive.supervisor_dispatch_slugs([child], text) == frozenset()


def test_supervisor_workflow_monitor_alias_is_mapped() -> None:
    """The workflow-monitor invocation name maps to its legacy supervision slug."""
    child = unit(slug="agdt.ai-pr-loop-supervision.workflow-monitor", body="Work.\n")
    text = "Use `agent_type: ai-pr-loop-workflow-monitor` before worker fan-out.\n"
    assert derive.supervisor_dispatch_slugs([child], text) == frozenset(
        {"agdt.ai-pr-loop-supervision.workflow-monitor"}
    )


def test_supervisor_legal_target_reference_is_mapped() -> None:
    """A legal target reference maps to its legacy supervision slug."""
    child = unit(slug="agdt.ai-pr-loop-supervision.pattern-auditor", body="Work.\n")
    text = "Use `agent_type: agdt-ai-pr-loop-supervision-pattern-auditor`.\n"
    assert derive.supervisor_dispatch_slugs([child], text) == frozenset({"agdt.ai-pr-loop-supervision.pattern-auditor"})


def test_supervisor_references_are_ignored_when_child_dispatch_is_disabled() -> None:
    """Disabled child dispatch keeps future extension references out of T4."""
    child = unit(slug="agdt.ai-pr-loop-supervision.worker", body="Work.\n")
    text = (
        "<!-- derive_customization_disposition: child_dispatch: false -->\n"
        "Use `agent_type: ai-pr-loop-supervision-worker`.\n"
    )
    assert derive.supervisor_dispatch_slugs([child], text) == frozenset()
