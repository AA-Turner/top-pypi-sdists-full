"""A refused definition's sentence quotes an ERROR, and notices sort last (lane 6i, review of 6g).

Some checks only warn (an unknown step key, a step that keeps no chat). When a definition also has a real
error, the compile sentence quoted ``issues[0]`` — which could be a warning — as "first:", so a person read
the warning as the reason their workflow was refused.
"""

from __future__ import annotations

import pytest

from matrx_graph import Definition, NodeRegistry, compile_graph, register_builtin_nodes
from matrx_graph.errors import CompilationError
from matrx_graph.validation import ValidationIssue, ordered_issues, validate_definition


def _definition() -> Definition:
    return Definition.model_validate({
        "nodes": [
            {"id": "a", "type": "data.transform", "position": {"x": 0, "y": 0},
             # Two warnings (validation offers, never blocks): a chat nobody can open, an unknown key.
             "data": {"on_failure": "continue", "inputs": {"store": False},
                      "config": {"expression": "{'n': 1}"}}},
        ],
        "edges": [{"id": "e1", "source": "a", "target": "ghost", "data": {"kind": "data"}}],
    })


def test_the_sentence_names_the_error_even_when_a_warning_sorts_first():
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    issues = validate_definition(_definition(), registry=registry).issues
    # Warnings and an error together: the validator lists the error first.
    assert issues[0].severity == "error" and any(i.severity == "warning" for i in issues)
    with pytest.raises(CompilationError) as refused:
        compile_graph(_definition(), registry=registry)
    first = str(refused.value).split("first: ", 1)[1]
    error = next(i for i in issues if i.severity == "error")
    assert first.startswith(error.message)
    assert not any(first.startswith(i.message) for i in issues if i.severity == "warning")


def test_notices_sort_after_errors_and_every_other_warning():
    """An unknown step key is a notice: an open plan's warning (appended later by the publish door) and
    every error come before it (test_the_studio_publish_route_shows_open_plans_as_warnings, 2026-11-10)."""
    notice = ValidationIssue(path="n.data.template", message="Unknown step key", severity="warning", code="unknown_step_key")
    plan = ValidationIssue(path="n", message="This step is planned but not built yet", severity="warning")
    error = ValidationIssue(path="e", message="Edge targets a missing node", severity="error")
    other = ValidationIssue(path="m", message="keeps no chat", severity="warning")
    assert ordered_issues([notice, other, plan, error]) == [error, other, plan, notice]


def test_the_unknown_key_warning_is_marked_a_notice():
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    issues = validate_definition(_definition(), registry=registry).issues
    unknown = [i for i in issues if "Unknown step key" in i.message]
    assert unknown and all(i.code == "unknown_step_key" for i in unknown)
    assert issues[-len(unknown):] == unknown
