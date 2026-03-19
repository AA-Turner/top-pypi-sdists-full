"""Workflow simulation engine for testing definitions without side effects (#968)."""

from __future__ import annotations

import asyncio
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .workflow_engine import ValidationResult, load_definition, validate_workflow_definition


@dataclass
class SimulationResult:
    """Result of simulating a workflow definition."""

    final_status: str
    steps_executed: list[dict[str, Any]] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)
    error: str | None = None


class WorkflowSimulator:
    """Run a workflow definition with stub runners for testing."""

    def __init__(self, stub_results: dict[str, dict[str, Any]] | None = None) -> None:
        self._stub_results = stub_results or {}

    def validate(self, source: str | Path) -> ValidationResult:
        """Validate a workflow definition without executing it."""
        return validate_workflow_definition(source)

    def simulate(self, source: str | Path) -> SimulationResult:
        """Simulate a workflow with stub runners. Runs synchronously."""
        return asyncio.run(self._simulate_async(source))

    async def _simulate_async(self, source: str | Path) -> SimulationResult:
        from ..db import init_db
        from . import workflow_storage as ws
        from .workflow_engine import WorkflowEngine
        from .workflow_runners import create_stub_registry

        defn = load_definition(source)

        with tempfile.TemporaryDirectory() as td:
            db = init_db(Path(td) / "sim.db")
            try:
                from ..config import WorkflowConfig

                config = WorkflowConfig()
                registry = create_stub_registry()

                engine = WorkflowEngine(db, config, registry)
                engine._stub_results = self._stub_results  # type: ignore[attr-defined]

                try:
                    run = await engine.start_run(defn, target_kind="simulation", target_ref="sim")
                except Exception as exc:
                    # Try to find the run that was created before the error
                    runs = ws.list_workflow_runs(db, status="failed")
                    run_after = runs[0] if runs else None
                    run_id = run_after["id"] if run_after else ""
                    events = ws.list_workflow_events(db, run_id) if run_id else []
                    steps = ws.list_workflow_steps(db, run_id) if run_id else []
                    return SimulationResult(
                        final_status=run_after["status"] if run_after else "failed",
                        steps_executed=[dict(s) for s in steps],
                        events=[dict(e) for e in events],
                        error=str(exc),
                    )

                run_id = run["id"]
                run_after = ws.get_workflow_run(db, run_id)
                events = ws.list_workflow_events(db, run_id)
                steps = ws.list_workflow_steps(db, run_id)

                return SimulationResult(
                    final_status=run_after["status"] if run_after else "unknown",
                    steps_executed=[dict(s) for s in steps],
                    events=[dict(e) for e in events],
                )
            finally:
                db.close()
