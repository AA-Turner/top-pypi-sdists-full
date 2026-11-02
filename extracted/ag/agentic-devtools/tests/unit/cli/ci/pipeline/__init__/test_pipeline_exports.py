"""Tests for the stable pipeline package exports."""

from importlib import import_module

from agentic_devtools.cli.ci.pipeline import (
    DerivedState,
    PRStateSnapshot,
    build_pr_state_snapshot,
    run_pipeline,
)


def test_exports_pipeline_public_api() -> None:
    initializer = import_module("agentic_devtools.cli.ci.pipeline.__init__")
    assert DerivedState is not None
    assert PRStateSnapshot is not None
    assert callable(build_pr_state_snapshot)
    assert callable(run_pipeline)
    assert initializer.__all__ == [
        "ActionDecision",
        "ActionResult",
        "DerivedState",
        "PRStateSnapshot",
        "PipelineRunSummary",
        "build_pr_state_snapshot",
        "run_pipeline",
    ]
