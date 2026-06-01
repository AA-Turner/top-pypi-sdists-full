from __future__ import annotations
from pathlib import Path
from kanban_framework.types import Phase


class Scheduler:
    EVAL_ROLES = [
        {"name": "code_reviewer", "agent_type": "general-purpose"},
        {"name": "qa", "agent_type": "general-purpose"},
        {"name": "product_reviewer", "agent_type": "general-purpose"},
    ]

    PLAN_REVIEW_DIMENSIONS = [
        {"name": "requirement_clarity", "agent_type": "general-purpose"},
        {"name": "technical_feasibility", "agent_type": "general-purpose"},
        {"name": "task_decomposition", "agent_type": "general-purpose"},
        {"name": "acceptance_criteria", "agent_type": "general-purpose"},
        {"name": "research_completeness", "agent_type": "general-purpose"},
        {"name": "parallel_safety", "agent_type": "general-purpose"},
    ]

    RETROSPECTIVE_ROLES = [
        {"name": "retrospective_writer", "agent_type": "general-purpose"},
        {"name": "acceptance_writer", "agent_type": "general-purpose"},
        {"name": "knowledge_extractor", "agent_type": "general-purpose"},
    ]

    @staticmethod
    def scan_agents(fs) -> list[dict]:
        """Scan .claude/agents/ directory for agent definitions."""
        agents_dir = fs.kanban_dir.parent / ".claude" / "agents"
        if not agents_dir.exists() or not agents_dir.is_dir():
            return []
        agents = []
        for f in sorted(agents_dir.glob("*.md")):
            name = f.stem
            agents.append({"name": name, "file": str(f)})
        return agents

    # Deprecated since v0.84 — kept for backward compat.
    PHASE_ORDER = [
        Phase.PLAN,
        Phase.PLAN_REVIEW,
        Phase.QA_SPEC,
        Phase.SPEC_REVIEW,
        Phase.EXECUTE,
        Phase.EVALUATE,
        Phase.RETROSPECTIVE,
        Phase.USER_DECISION,
        Phase.ARCHIVE,
    ]

    LIGHTWEIGHT_PHASE_ORDER = [
        Phase.PLAN,
        Phase.EXECUTE,
        Phase.EVALUATE,
        Phase.USER_DECISION,
        Phase.ARCHIVE,
    ]

    QUICK_PHASE_ORDER = [
        Phase.EXECUTE,
        Phase.USER_DECISION,
        Phase.ARCHIVE,
    ]

    LIGHTWEIGHT_EVAL_ROLES = [
        {"name": "qa", "agent_type": "general-purpose"},
    ]

    _BUILTIN_MODES: dict[str, list[Phase]] = {
        "full":        [Phase.PLAN, Phase.PLAN_REVIEW, Phase.QA_SPEC, Phase.SPEC_REVIEW, Phase.EXECUTE, Phase.EVALUATE, Phase.RETROSPECTIVE, Phase.USER_DECISION, Phase.ARCHIVE],
        "lightweight": [Phase.PLAN, Phase.EXECUTE, Phase.EVALUATE, Phase.USER_DECISION, Phase.ARCHIVE],
        "quick":       [Phase.EXECUTE, Phase.USER_DECISION, Phase.ARCHIVE],
    }

    @classmethod
    def get_modes(cls, workflow: dict | None = None,
                  kanban_dir: Path | None = None) -> dict[str, list[Phase | str]]:
        """Return mode definitions from workflow.json + .kanban/workflows/ directory.

        Priority: workflow.json modes > directory files > builtin defaults.
        """
        from pathlib import Path as _Path
        # Start with builtin base
        result: dict[str, list[Phase | str]] = {}
        for name in ("full", "lightweight", "quick"):
            result[name] = list(cls._BUILTIN_MODES.get(name, cls.PHASE_ORDER))

        # Scan .kanban/workflows/ directory
        if kanban_dir and isinstance(kanban_dir, _Path):
            from kanban_framework.domain.workflow_loader import merge_workflow_modes
            dir_modes = merge_workflow_modes(workflow or {}, kanban_dir)
            for name, cfg in dir_modes.items():
                phase_names = cfg.get("phase_order", []) if isinstance(cfg, dict) else []
                resolved: list[Phase | str] = []
                for pn in phase_names:
                    try:
                        resolved.append(Phase(pn))
                    except ValueError:
                        resolved.append(pn)
                if resolved:
                    result[name] = resolved

        # workflow.json modes (highest priority)
        if workflow and isinstance(workflow, dict):
            modes = workflow.get("modes", {})
            if isinstance(modes, dict):
                for name, cfg in modes.items():
                    phase_names = cfg.get("phase_order", []) if isinstance(cfg, dict) else []
                    resolved = []
                    for pn in phase_names:
                        try:
                            resolved.append(Phase(pn))
                        except ValueError:
                            resolved.append(pn)
                    if resolved:
                        result[name] = resolved
        return result if result else dict(cls._BUILTIN_MODES)

    @classmethod
    def eval_roles(cls, lightweight: bool = False) -> list[dict]:
        if lightweight:
            return list(cls.LIGHTWEIGHT_EVAL_ROLES)
        return list(cls.EVAL_ROLES)

    @classmethod
    def plan_review_dimensions(cls) -> list[dict]:
        return list(cls.PLAN_REVIEW_DIMENSIONS)

    @classmethod
    def retrospective_roles(cls, lightweight: bool = False) -> list[dict]:
        if lightweight:
            return [{"name": "acceptance_writer", "agent_type": "general-purpose"}]
        return list(cls.RETROSPECTIVE_ROLES)

    @classmethod
    def dispatch_order(cls, lightweight: bool = False, quick: bool = False,
                       custom_order: list[str] | None = None,
                       workflow: dict | None = None,
                       kanban_dir: Path | None = None,
                       mode: str | None = None) -> list[Phase | str]:
        if custom_order is not None:
            return list(custom_order)
        if mode and mode not in ("full", "lightweight", "quick"):
            modes = cls.get_modes(workflow, kanban_dir=kanban_dir)
            if mode in modes:
                return list(modes[mode])
        mode = mode if mode in ("full", "lightweight", "quick") else ("quick" if quick else ("lightweight" if lightweight else "full"))
        modes = cls.get_modes(workflow, kanban_dir=kanban_dir)
        if mode in modes:
            return list(modes[mode])
        return [p for p in cls._BUILTIN_MODES.get(mode, cls.PHASE_ORDER)]

    @classmethod
    def next_phase(cls, current, lightweight: bool = False, quick: bool = False,
                   custom_order: list[str] | None = None,
                   workflow: dict | None = None,
                   mode: str | None = None,
                   kanban_dir: Path | None = None) -> Phase | str | None:
        order = custom_order if custom_order is not None else cls._dispatch_from_mode(lightweight, quick, workflow, mode, kanban_dir)
        try:
            idx = order.index(current)
            return order[idx + 1]
        except (ValueError, IndexError):
            return None

    @classmethod
    def previous_phase(cls, current, lightweight: bool = False, quick: bool = False,
                       custom_order: list[str] | None = None) -> Phase | str | None:
        order = custom_order if custom_order is not None else cls._base_order(lightweight, quick)
        try:
            idx = order.index(current)
            if idx > 0:
                return order[idx - 1]
        except ValueError:
            pass
        return None

    @classmethod
    def _base_order(cls, lightweight: bool, quick: bool, workflow: dict | None = None,
                    mode: str | None = None,
                    kanban_dir: Path | None = None) -> list[Phase | str]:
        if mode and mode not in ("full", "lightweight", "quick"):
            modes = cls.get_modes(workflow, kanban_dir=kanban_dir)
            if mode in modes:
                return list(modes[mode])
        mode = mode if mode in ("full", "lightweight", "quick") else ("quick" if quick else ("lightweight" if lightweight else "full"))
        modes = cls.get_modes(workflow, kanban_dir=kanban_dir)
        if mode in modes:
            return list(modes[mode])
        return [p for p in cls._BUILTIN_MODES.get(mode, cls.PHASE_ORDER)]

    @classmethod
    def _dispatch_from_mode(cls, lightweight: bool, quick: bool, workflow: dict | None = None,
                            mode: str | None = None,
                            kanban_dir: Path | None = None) -> list[Phase | str]:
        return cls._base_order(lightweight, quick, workflow, mode, kanban_dir)

    @staticmethod
    def compute_parallel_batches(subtasks: list[dict]) -> list[list[dict]]:
        """Group subtasks into parallel batches by dependency topology.

        Two subtasks can run in parallel ONLY if:
        - Neither depends on the other
        - Their file_ownership sets have zero overlap
        - Both have parallelizable=true (or are forced into parallel)

        Returns list of batches, each batch is a list of subtask dicts.
        """
        remaining = {s["id"]: s for s in subtasks}
        completed: set[str] = set()
        batches: list[list[dict]] = []

        while remaining:
            batch = []
            for sid, st in list(remaining.items()):
                deps = set(st.get("dependencies", []))
                # All dependencies must be in completed
                if not deps.issubset(completed):
                    continue
                # Check file ownership conflicts with current batch
                my_files = set(st.get("file_ownership", []))
                conflict = any(
                    my_files & set(b.get("file_ownership", []))
                    for b in batch
                )
                if conflict:
                    continue
                batch.append(st)
                del remaining[sid]

            if not batch:
                # Deadlock: circular dependency or conflict. Force sequential.
                first = min(remaining.values(),
                           key=lambda s: len(s.get("dependencies", [])))
                batch = [first]
                del remaining[first["id"]]

            batches.append(batch)
            completed.update(s["id"] for s in batch)

        return batches
