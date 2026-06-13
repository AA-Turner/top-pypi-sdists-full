"""Step loader: read step definitions from workflow.json, per-mode or global.

Priority: modes.<mode>.phases[].steps[] → .kanban/workflows/<mode>.json → package workflows/<mode>.json → top-level phases[].steps[] → hardcoded defaults.
"""
from __future__ import annotations

from kanban_framework.domain.steps_types import StepDef
from kanban_framework.domain.steps_lightweight import LIGHTWEIGHT_STEPS

# Emergency fallback — only used when all loading paths fail
_FALLBACK_STEPS = LIGHTWEIGHT_STEPS


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
            use_subagent = s.get("use_subagent")
            steps.append(StepDef(
                id=full_id,
                description=s.get("description", ""),
                actions=s.get("actions", []),
                agent_type=s.get("agent_type"),
                parallel=s.get("parallel", False),
                user_action=s.get("user_action", False),
                spawn_prompt=s.get("spawn_prompt") or ("\n".join(a for a in s.get("actions", []) if a and a.strip()) or None),
                interactive=s.get("interactive", False),
                required_artifacts=s.get("required_artifacts", []),
                after=s.get("after", []),
                type=s.get("type", "action"),
                guard=guard_cfg,
                gateway=gateway_cfg,
                knowledge=s.get("knowledge") if isinstance(s.get("knowledge"), dict) else None,
                use_subagent=use_subagent if use_subagent is not None else None,
            ))
            # Validate: use_subagent=true requires spawn_prompt
            if use_subagent is True and not s.get("spawn_prompt"):
                import sys
                print(
                    f"WARNING: step '{full_id}' has use_subagent=true but no spawn_prompt. "
                    f"A basic prompt will be auto-generated from step metadata at runtime. "
                    f"Fix: add 'spawn_prompt' field to the step definition.",
                    file=sys.stderr,
                )
        result[phase_id] = steps
    return result


def _load_template_steps(mode: str) -> dict[str, list[StepDef]] | None:
    """Load steps from package workflows/<mode>.json."""
    from pathlib import Path
    template_file = Path(__file__).resolve().parent.parent / "workflows" / f"{mode}.json"
    if not template_file.is_file():
        return None
    try:
        import json
        data = json.loads(template_file.read_text(encoding="utf-8"))
        phases = data.get("phases", [])
        if phases and any(p.get("steps") for p in phases if isinstance(p, dict)):
            return _parse_phases_to_steps(phases)
    except (json.JSONDecodeError, OSError):
        pass
    return None


def load_steps_for_mode(workflow: dict, mode: str,
                        kanban_dir=None) -> dict[str, list[StepDef]]:
    """Load steps for a mode.

    Priority:
      1. modes.<mode>.phases[].steps[] — per-mode in workflow.json
      2. .kanban/workflows/<mode>.json — user project directory
      3. package workflows/<mode>.json — framework template
      4. top-level phases[].steps[] — global fallback
      5. Python hardcoded constants — emergency fallback
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

    # Priority 3: package templates
    template_result = _load_template_steps(mode)
    if template_result is not None:
        return template_result

    # Priority 4: top-level phases[].steps[]
    top_phases = workflow.get("phases", [])
    if top_phases and isinstance(top_phases, list):
        if any(p.get("steps") for p in top_phases if isinstance(p, dict)):
            return _parse_phases_to_steps(top_phases)

    # Priority 5: Python hardcoded defaults (emergency fallback)
    return _FALLBACK_STEPS
