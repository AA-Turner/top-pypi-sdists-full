"""Shared fixtures and helpers for generate_epic_progress_report tests."""

from __future__ import annotations

import datetime as dt
import importlib.util
import sys
from pathlib import Path


def _load_module():
    """Load scripts/generate_epic_progress_report.py as a module."""
    repo_root = Path(__file__).resolve().parents[3]
    script_path = repo_root / "scripts" / "generate_epic_progress_report.py"
    spec = importlib.util.spec_from_file_location("generate_epic_progress_report", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load generate_epic_progress_report.py from {script_path!s}")
    module = importlib.util.module_from_spec(spec)
    # sys.modules registration is required so that @dataclass can resolve
    # forward references via sys.modules.get(cls.__module__).__dict__.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


report = _load_module()


def _node(
    number: int,
    *,
    state: str = "OPEN",
    labels: list[str] | None = None,
    children: list | None = None,
    child_total: int | None = None,
):
    """Build a report node for tests."""
    nodes = [] if children is None else children
    return report.Node(
        number=number,
        title=f"Issue {number}",
        state=state,
        updated_at="2026-07-10T00:00:00Z",
        labels=[] if labels is None else labels,
        assignees=[],
        children=nodes,
        child_total=len(nodes) if child_total is None else child_total,
    )


NOW = dt.datetime(2026, 7, 10, tzinfo=dt.timezone.utc)
PREV_RUN_AT = dt.datetime(2026, 7, 9, tzinfo=dt.timezone.utc)
