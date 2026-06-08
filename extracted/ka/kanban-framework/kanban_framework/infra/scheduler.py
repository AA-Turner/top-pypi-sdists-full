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

    @staticmethod
    def _load_phase_order_from_json(path) -> list:
        """Extract phase_order from a workflow JSON file."""
        try:
            import json
            data = json.loads(path.read_text(encoding="utf-8"))
            phase_names = data.get("phase_order", [])
            resolved = []
            for pn in phase_names:
                try:
                    resolved.append(Phase(pn))
                except ValueError:
                    resolved.append(pn)
            return resolved
        except Exception:
            return []

    # Deprecated since v0.84 — kept for backward compat.
    PHASE_ORDER = [
        Phase.PLAN,
        Phase.EXECUTE,
        Phase.EVALUATE,
        Phase.USER_DECISION,
        Phase.ARCHIVE,
    ]

    LIGHTWEIGHT_EVAL_ROLES = [
        {"name": "review", "agent_type": "general-purpose"},
    ]

    @classmethod
    def get_modes(cls, workflow: dict | None = None,
                  kanban_dir=None) -> dict[str, list]:
        """Return mode definitions from workflow.json + directories.

        Priority: workflow.json modes > .kanban/workflows/ > package workflows/.
        """
        from pathlib import Path as _Path
        result: dict[str, list] = {}

        # Scan package workflows/ for available modes
        pkg_dir = Path(__file__).resolve().parent.parent / "workflows"
        if pkg_dir.is_dir():
            for wf_file in sorted(pkg_dir.glob("*.json")):
                name = wf_file.stem
                if name not in result:
                    result[name] = cls._load_phase_order_from_json(wf_file)

        # Scan .kanban/workflows/ for user/installed modes (overrides package)
        if kanban_dir and isinstance(kanban_dir, _Path):
            user_dir = kanban_dir / "workflows"
            if user_dir.is_dir():
                for wf_file in sorted(user_dir.glob("*.json")):
                    result[wf_file.stem] = cls._load_phase_order_from_json(wf_file)

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

        return result

    @classmethod
    def eval_roles(cls, mode: str | None = None,
                   kanban_dir: Path | None = None) -> list[dict]:
        """Derive eval roles from the mode's evaluate phase step definitions."""
        from kanban_framework.infra.consts import Consts
        return cls._derive_eval_roles(mode or Consts.DEFAULT_MODE, kanban_dir)

    @classmethod
    def _derive_eval_roles(cls, mode: str, kanban_dir: Path | None = None) -> list[dict]:
        """Derive eval roles from mode's evaluate phase step definitions.

        Scans the evaluate phase for agent steps (with spawn_prompt/agent_type)
        and generates a role entry for each. Falls back to EVAL_ROLES if no
        evaluate phase found.
        """
        from kanban_framework.domain.steps import _get_steps
        mode_steps = _get_steps(mode)
        evaluate_steps = mode_steps.get("evaluate", [])
        if not evaluate_steps:
            return list(cls.EVAL_ROLES)

        roles = []
        for s in evaluate_steps:
            if s.id.endswith((".complete", ".collect_score", ".collect_scores",
                              ".check_score", ".commit", ".e2e_run",
                              ".collect_issues", ".capture_knowledge")):
                continue
            # Agent steps: have spawn_prompt or agent_type
            if s.spawn_prompt or s.agent_type:
                # Derive role name from step id (e.g. evaluate.spawn_qa → qa)
                step_name = s.id.split(".")[-1] if "." in s.id else s.id
                # Map common prefixes to standard role names
                role = step_name.replace("spawn_", "").replace("evaluate_", "")
                if not role or role == "spawn":
                    role = step_name
                roles.append({"name": role, "agent_type": s.agent_type or "general-purpose"})

        return roles if roles else list(cls.EVAL_ROLES)

    @classmethod
    def plan_review_dimensions(cls) -> list[dict]:
        return list(cls.PLAN_REVIEW_DIMENSIONS)

    @classmethod
    def retrospective_roles(cls, mode: str | None = None) -> list[dict]:
        return list(cls.RETROSPECTIVE_ROLES)

    @classmethod
    def dispatch_order(cls, custom_order: list[str] | None = None,
                       workflow: dict | None = None,
                       kanban_dir=None,
                       mode: str | None = None) -> list:
        if custom_order is not None:
            return list(custom_order)
        from kanban_framework.infra.consts import Consts
        resolved_mode = mode or Consts.DEFAULT_MODE
        modes = cls.get_modes(workflow, kanban_dir=kanban_dir)
        if resolved_mode in modes:
            order = list(modes[resolved_mode])
        else:
            order = list(cls.PHASE_ORDER)
        # Apply extensions if present
        if workflow and isinstance(workflow, dict) and workflow.get("extensions"):
            from kanban_framework.domain.workflow_extensions import WorkflowExtension
            ext = WorkflowExtension(workflow)
            if ext.is_active_for_mode(resolved_mode):
                str_order = [p.value if isinstance(p, Phase) else str(p) for p in order]
                str_order = ext.build_phase_order(str_order, mode=resolved_mode)
                return [Phase(p) for p in str_order]
        return order

    @classmethod
    def next_phase(cls, current, custom_order: list[str] | None = None,
                   workflow: dict | None = None,
                   mode: str | None = None,
                   kanban_dir: Path | None = None) -> Phase | str | None:
        order = custom_order if custom_order is not None else cls._dispatch_from_mode(workflow, mode, kanban_dir)
        try:
            idx = order.index(current)
            return order[idx + 1]
        except (ValueError, IndexError):
            return None

    @classmethod
    def previous_phase(cls, current, custom_order: list[str] | None = None,
                       workflow: dict | None = None,
                       mode: str | None = None,
                       kanban_dir=None) -> Phase | str | None:
        order = custom_order if custom_order is not None else cls._base_order(workflow, mode, kanban_dir)
        try:
            idx = order.index(current)
            if idx > 0:
                return order[idx - 1]
        except ValueError:
            pass
        return None

    @classmethod
    def _base_order(cls, workflow: dict | None = None,
                    mode: str | None = None,
                    kanban_dir=None) -> list:
        from kanban_framework.infra.consts import Consts
        resolved_mode = mode or Consts.DEFAULT_MODE
        modes = cls.get_modes(workflow, kanban_dir=kanban_dir)
        if resolved_mode in modes:
            order = list(modes[resolved_mode])
        else:
            order = list(cls.PHASE_ORDER)
        if workflow and isinstance(workflow, dict) and workflow.get("extensions"):
            from kanban_framework.domain.workflow_extensions import WorkflowExtension
            ext = WorkflowExtension(workflow)
            if ext.is_active_for_mode(resolved_mode):
                str_order = [p.value if isinstance(p, Phase) else str(p) for p in order]
                str_order = ext.build_phase_order(str_order, mode=resolved_mode)
                return [Phase(p) for p in str_order]
        return order

    @classmethod
    def _dispatch_from_mode(cls, workflow: dict | None = None,
                            mode: str | None = None,
                            kanban_dir: Path | None = None) -> list[Phase | str]:
        return cls._base_order(workflow, mode, kanban_dir)

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
