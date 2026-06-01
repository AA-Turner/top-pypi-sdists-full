"""Step loader: read step definitions from workflow.json, per-mode or global.

Priority: modes.<mode>.phases[].steps[] → top-level phases[].steps[] → hardcoded defaults.
"""
from __future__ import annotations

from kanban_framework.domain.steps_types import StepDef
from kanban_framework.domain.steps_full import FULL_STEPS
from kanban_framework.domain.steps_lightweight import LIGHTWEIGHT_STEPS
from kanban_framework.domain.steps_quick import QUICK_STEPS

_DEFAULTS = {
    "full":        FULL_STEPS,
    "lightweight": LIGHTWEIGHT_STEPS,
    "quick":       QUICK_STEPS,
}


def _parse_phases_to_steps(phases_config: list[dict]) -> dict[str, list[StepDef]]:
    """Convert a phases list (each with optional steps[]) to phase_id → [StepDef]."""
    result: dict[str, list[StepDef]] = {}
    for phase in phases_config:
        phase_id = phase.get("id")
        steps_cfg = phase.get("steps")
        if not phase_id or not steps_cfg:
            continue
        steps = []
        for s in steps_cfg:
            sid = s.get("id", "")
            full_id = sid if "." in sid else f"{phase_id}.{sid}"
            guard_cfg = s.get("guard")
            if not isinstance(guard_cfg, dict):
                guard_cfg = None
            gateway_cfg = s.get("gateway")
            if not isinstance(gateway_cfg, dict):
                gateway_cfg = None
            steps.append(StepDef(
                id=full_id,
                description=s.get("description", ""),
                actions=s.get("actions", []),
                agent_type=s.get("agent_type"),
                parallel=s.get("parallel", False),
                user_action=s.get("user_action", False),
                spawn_prompt=s.get("spawn_prompt"),
                interactive=s.get("interactive", False),
                required_artifacts=s.get("required_artifacts", []),
                after=s.get("after", []),
                type=s.get("type", "action"),
                guard=guard_cfg,
                gateway=gateway_cfg,
                knowledge=s.get("knowledge") if isinstance(s.get("knowledge"), dict) else None,
            ))
        result[phase_id] = steps
    return result


def load_steps_for_mode(workflow: dict, mode: str,
                        kanban_dir: Path | None = None) -> dict[str, list[StepDef]]:
    """Load steps for a mode.

    Priority:
      1. modes.<mode>.phases[].steps[] — per-mode in workflow.json
      2. .kanban/workflows/<mode>.json — directory file
      3. top-level phases[].steps[] — global fallback
      4. Python hardcoded constants — ultimate default
    """
    from pathlib import Path as _Path

    # Priority 1: per-mode phases in modes.<mode>
    modes_cfg = workflow.get("modes", {})
    if isinstance(modes_cfg, dict):
        mode_cfg = modes_cfg.get(mode)
        if isinstance(mode_cfg, dict):
            mode_phases = mode_cfg.get("phases")
            if mode_phases and isinstance(mode_phases, list):
                if any(p.get("steps") for p in mode_phases if isinstance(p, dict)):
                    return _parse_phases_to_steps(mode_phases)

    # Priority 2: .kanban/workflows/<mode>.json directory file
    if kanban_dir and isinstance(kanban_dir, _Path):
        wf_file = kanban_dir / "workflows" / f"{mode}.json"
        if wf_file.is_file():
            try:
                import json
                dir_cfg = json.loads(wf_file.read_text(encoding="utf-8"))
                dir_phases = dir_cfg.get("phases")
                if dir_phases and isinstance(dir_phases, list):
                    if any(p.get("steps") for p in dir_phases if isinstance(p, dict)):
                        return _parse_phases_to_steps(dir_phases)
            except (json.JSONDecodeError, OSError):
                pass

    # Priority 3: top-level phases[].steps[]
    top_phases = workflow.get("phases", [])
    if top_phases and isinstance(top_phases, list):
        if any(p.get("steps") for p in top_phases if isinstance(p, dict)):
            return _parse_phases_to_steps(top_phases)

    # Priority 4: hardcoded defaults
    return _DEFAULTS.get(mode, FULL_STEPS)
