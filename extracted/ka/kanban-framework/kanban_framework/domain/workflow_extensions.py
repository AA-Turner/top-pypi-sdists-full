"""Workflow extensions — per-project custom phases and steps via workflow.json.

Reads the ``extensions`` section from workflow.json and merges custom phases/
steps into the standard workflow at runtime.  Backward compatible: no
extensions → identical behavior.
"""
from __future__ import annotations

import copy
from typing import Optional

from kanban_framework.domain.steps_types import StepDef


class WorkflowExtension:
    """Parse and apply workflow.json extensions to produce customised
    phase order and step definitions."""

    _DEFAULT_MODES = ["full"]

    def __init__(self, workflow: dict):
        self._extensions = workflow.get("extensions", {})
        self._modes = self._extensions.get("modes", self._DEFAULT_MODES)
        self._phases_config = {
            p["id"]: p for p in workflow.get("phases", []) if "id" in p
        }

    def is_active_for_mode(self, mode: str) -> bool:
        """Check if extensions should apply for the given workflow mode."""
        return mode in self._modes

    # ── Phase order ─────────────────────────────────────────────────────

    def build_phase_order(self, base_order: list[str], mode: str = "full") -> list[str]:
        """Return *base_order* with add_phases inserted and remove_phases removed.
        Only applies if *mode* is in the extensions' modes list.
        """
        if not self.is_active_for_mode(mode):
            return list(base_order)
        order = list(base_order)
        for phase_id in self._extensions.get("remove_phases", []):
            if phase_id in order:
                order.remove(phase_id)
        for phase_def in self._extensions.get("add_phases", []):
            pid = phase_def["id"]
            after = phase_def.get("insert_after")
            if after and after in order:
                idx = order.index(after)
                order.insert(idx + 1, pid)
            else:
                order.append(pid)
        return order

    # ── Step map ─────────────────────────────────────────────────────────

    def build_step_map(
        self, base_steps: dict[str, list[StepDef]], mode: str = "full"
    ) -> dict[str, list[StepDef]]:
        """Return *base_steps* with add_steps injected and remove_steps filtered.
        Only applies if *mode* is in the extensions' modes list.
        """
        if not self.is_active_for_mode(mode):
            return copy.deepcopy(base_steps)
        steps = copy.deepcopy(base_steps)

        for step_id in self._extensions.get("remove_steps", []):
            _remove_step(steps, step_id)

        for item in self._extensions.get("add_steps", []):
            phase = item.get("phase", "")
            after = item.get("insert_after")
            step_dict = item.get("step", {})
            _insert_step(steps, phase, after, step_dict)

        for phase_def in self._extensions.get("add_phases", []):
            pid = phase_def["id"]
            phase_steps = [
                _dict_to_stepdef(s, pid)
                for s in phase_def.get("steps", [])
            ]
            if phase_steps:
                steps[pid] = phase_steps
        return steps

    # ── Agent / artifact lookups ─────────────────────────────────────────

    def get_agents_for_phase(self, phase_id: str) -> Optional[list[dict]]:
        """Return agents config for a custom phase, or None."""
        for phase_def in self._extensions.get("add_phases", []):
            if phase_def["id"] == phase_id:
                return phase_def.get("agents")
        return None

    def get_required_artifacts(self, phase_id: str) -> list[str]:
        """Return required_artifacts for a custom phase."""
        for phase_def in self._extensions.get("add_phases", []):
            if phase_def["id"] == phase_id:
                return phase_def.get("required_artifacts", [])
        return []

    def get_quality_gate(self, phase_id: str) -> dict:
        """Return quality_gate config for a custom phase."""
        for phase_def in self._extensions.get("add_phases", []):
            if phase_def["id"] == phase_id:
                return phase_def.get("quality_gate", {})
        return {}

    # ── Validation ───────────────────────────────────────────────────────

    def validate(self) -> list[str]:
        """Return list of error messages (empty = valid)."""
        errors: list[str] = []
        for i, phase_def in enumerate(self._extensions.get("add_phases", [])):
            if "id" not in phase_def:
                errors.append(f"add_phases[{i}]: missing 'id'")
            if "insert_after" not in phase_def:
                errors.append(f"add_phases[{i}]: missing 'insert_after'")
            for j, step_dict in enumerate(phase_def.get("steps", [])):
                if "id" not in step_dict:
                    errors.append(
                        f"add_phases[{i}].steps[{j}]: missing 'id'"
                    )
        for i, item in enumerate(self._extensions.get("add_steps", [])):
            if "phase" not in item:
                errors.append(f"add_steps[{i}]: missing 'phase'")
            if "step" not in item:
                errors.append(f"add_steps[{i}]: missing 'step'")
        return errors


# ── Helper functions ─────────────────────────────────────────────────────


def _dict_to_stepdef(step_dict: dict, phase_id: str) -> StepDef:
    """Convert a workflow.json step dict to a StepDef dataclass.

    Step IDs in extensions are relative (e.g. ``"spawn"``) and get
    prefixed with ``phase_id.`` to form the full step ID.
    """
    raw_id = step_dict.get("id", "unknown")
    full_id = raw_id if "." in raw_id else f"{phase_id}.{raw_id}"
    return StepDef(
        id=full_id,
        description=step_dict.get("description", ""),
        actions=step_dict.get("actions", []),
        agent_type=step_dict.get("agent_type"),
        parallel=step_dict.get("parallel", False),
        user_action=step_dict.get("user_action", False),
        spawn_prompt=step_dict.get("spawn_prompt"),
        interactive=step_dict.get("interactive", False),
        required_artifacts=step_dict.get("required_artifacts", []),
    )


def _remove_step(steps: dict[str, list[StepDef]], step_id: str) -> None:
    """Remove a step by its full ID (e.g. ``plan.check_constraints``)."""
    parts = step_id.split(".", 1)
    if len(parts) != 2:
        return
    phase_id, local_id = parts
    if phase_id in steps:
        steps[phase_id] = [s for s in steps[phase_id] if s.id != step_id]


def _insert_step(
    steps: dict[str, list[StepDef]],
    phase_id: str,
    after: Optional[str],
    step_dict: dict,
) -> None:
    """Insert a step into a phase's step list after the specified step."""
    step = _dict_to_stepdef(step_dict, phase_id)
    if phase_id not in steps:
        steps[phase_id] = [step]
        return
    if not after:
        steps[phase_id].append(step)
        return
    step_list = steps[phase_id]
    for i, existing in enumerate(step_list):
        if existing.id == after:
            step_list.insert(i + 1, step)
            return
    step_list.append(step)
