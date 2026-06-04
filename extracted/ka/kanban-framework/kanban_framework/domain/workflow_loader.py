"""Workflow loader — scan .kanban/workflows/ directory for mode definitions.

Each .json file in the directory defines a mode.  Built-in modes
(full/lightweight/quick) are always available even without files.
"""
from __future__ import annotations
import json
from pathlib import Path


def scan_workflows(kanban_dir: Path) -> dict[str, dict]:
    """Scan .kanban/workflows/*.json and return {mode_name: config}.

    Each file defines one mode.  File stem (without .json) = mode name.
    Built-in modes are always included as base entries.
    """
    result: dict[str, dict] = {
        "lightweight": {"builtin": True},
        "quick":       {"builtin": True},
    }
    wf_dir = kanban_dir / "workflows"
    if not wf_dir.is_dir():
        return result
    for f in sorted(wf_dir.glob("*.json")):
        try:
            cfg = json.loads(f.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        name = f.stem  # filename without .json
        result[name] = cfg
    return result


def merge_workflow_modes(workflow_json: dict, kanban_dir: Path) -> dict:
    """Merge modes from workflow.json and .kanban/workflows/ directory.

    workflow.json modes take priority over directory files.
    Built-in modes (full/lightweight/quick) always present.
    """
    modes: dict[str, dict] = scan_workflows(kanban_dir)
    # Merge from workflow.json (takes priority)
    wf_modes = workflow_json.get("modes", {})
    if isinstance(wf_modes, dict):
        for name, cfg in wf_modes.items():
            modes[name] = cfg
    return modes
