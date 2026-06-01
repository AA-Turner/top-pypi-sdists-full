"""State machine driver for kanban workflow orchestration.

Instead of the orchestrator remembering the full FSM, it calls
`next_step(task_id)` and receives precise instructions for what to do next.

Step definitions, progress tracking, and context building live in sibling
modules (steps.py, progress.py, context.py) — this file keeps only the
core orchestration logic and re-exports for backward compatibility.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from kanban_framework.types import Task, Phase, ControlMode
from kanban_framework.infra.config import Config
from kanban_framework.infra.filesystem import Filesystem

# Re-export from extracted modules for backward compatibility
from kanban_framework.domain.steps import (  # noqa: F401
    StepDef,
    KNOWLEDGE_SEARCH_PROTOCOL,
    _resolve_workflow_prompt,
    _inject_knowledge_json,
    FULL_STEPS,
    LIGHTWEIGHT_STEPS,
    QUICK_STEPS,
    _get_steps,
    _get_phase_order,
)
from kanban_framework.domain.step_progress import (  # noqa: F401
    load_progress,
    save_progress,  # noqa: F401
    mark_step,
)
from kanban_framework.domain.context import (  # noqa: F401
    _is_knowledge_available,
    _load_knowledge_summary,
    _auto_knowledge_retrieval,
    _build_codegraph_context,
    _resolve_prompt_hooks,
    _get_context_files,
    _build_worker_context,
)
from kanban_framework.domain.state_machine_subtask import (  # noqa: F401
    _step_depends_on,
    _interactive_prompts,
)


def _output_dir_hint(output_dir: str) -> str:
    return f"保存到 {output_dir}/" if output_dir else "在现有目录中修改文件"


def _load_extension(config: Config):
    """Load WorkflowExtension from config if extensions exist."""
    wf = config.workflow
    if wf.get("extensions"):
        from kanban_framework.domain.workflow_extensions import WorkflowExtension
        ext = WorkflowExtension(wf)
        if ext.validate():
            return None  # Invalid extensions, ignore
        return ext
    return None


@dataclass
class NextStepResult:
    task_id: str
    phase: str
    step_id: str
    step_index: int
    total_steps: int
    description: str
    step_type: str = "action"  # "spawn" | "interactive" | "action"
    actions: list[str] = field(default_factory=list)
    agent_type: Optional[str] = None
    parallel: bool = False
    user_action: bool = False
    phase_complete: bool = False
    all_complete: bool = False
    context_files: list[str] = field(default_factory=list)
    knowledge_summary: Optional[dict] = None
    knowledge_context: list[dict] = field(default_factory=list)
    codegraph_context: Optional[str] = None
    depends_on_files: list[str] = field(default_factory=list)
    knowledge_available: bool = True
    interactive_prompt: Optional[str] = None
    message: str = ""
    spawn_prompt: Optional[str] = None
    interactive: bool = False
    available_steps: list[dict] = field(default_factory=list)
    control_mode: str = "semi"


def next_step(fs: Filesystem, config: Config, task: Task) -> NextStepResult:
    """Determine the exact next action for a task."""
    mode = task.mode if task.mode not in ("full", "lightweight", "quick") else ("quick" if task.mode == "quick" else ("lightweight" if task.lightweight else "full"))
    ext = _load_extension(config)
    base_order = _get_phase_order(task.lightweight, quick=(task.mode == "quick"))
    custom_order = ext.build_phase_order([p.value if isinstance(p, Phase) else str(p) for p in base_order], mode=mode) if ext else None
    base_steps = _get_steps(mode)
    custom_steps = ext.build_step_map(base_steps, mode=mode) if ext else None
    steps_map = custom_steps if custom_steps is not None else base_steps
    progress = load_progress(fs, task.id)
    completed_steps = {k for k, v in progress.get("steps", {}).items()
                       if v.get("status") in ("completed", "skipped")}

    phase_value = task.phase_id

    if task.status.value == "draft":
        return NextStepResult(
            task_id=task.id, phase=phase_value, step_id="draft.promote",
            step_index=0, total_steps=1,
            description="任务处于 draft 状态，需要 promote 到正式流程",
            actions=["kanban task promote " + task.id],
            message="draft 任务需要先 promote",
        )

    if task.status.value in ("archived", "cancelled"):
        return NextStepResult(
            task_id=task.id, phase=phase_value, step_id="done",
            step_index=0, total_steps=0,
            description="任务已归档/取消",
            actions=[], all_complete=True,
            message="任务已结束",
        )

    if task.control_mode == ControlMode.MANUAL:
        return _handle_manual_mode(fs, task, completed_steps, progress, custom_order, custom_steps)

    phase_steps = steps_map.get(phase_value, [])
    if not phase_steps:
        # Phase not in current mode's step map — try redirect to nearest valid phase
        return _build_phase_transition(task, phase_value, [], task.lightweight, custom_order)

    for i, step in enumerate(phase_steps):
        if step.id not in completed_steps:
            # execute.spawn: dynamically inject per-subtask execution steps
            if step.id == "execute.spawn" and phase_value == "execute":
                if not step.spawn_prompt:
                    result = _try_subtask_step(fs, config, task)
                    if result is not None:
                        return result
                    mark_step(fs, task.id, "execute.spawn")
                    continue

            return _build_step_result(fs, config, task, step, i, phase_steps, phase_value)

    return _build_phase_transition(task, phase_value, phase_steps, task.lightweight, custom_order)


def _handle_manual_mode(fs, task, completed_steps, progress,
                        custom_order=None, custom_steps=None):
    from kanban_framework.domain.step_registry import build_step_dag, get_available_steps
    skipped = {k for k, v in progress.get("steps", {}).items() if v.get("status") == "skipped"}
    dag = build_step_dag(lightweight=task.lightweight, quick=(task.mode == "quick"),
                         custom_order=custom_order, custom_steps=custom_steps)
    available = get_available_steps(dag, completed_steps, skipped)
    if not available:
        return NextStepResult(
            task_id=task.id, phase=task.phase.value, step_id="all_done",
            step_index=0, total_steps=0,
            description="所有步骤已完成",
            actions=[], all_complete=True, control_mode="manual",
        )
    return NextStepResult(
        task_id=task.id, phase=task.phase.value,
        step_id="manual.select", step_index=0,
        total_steps=len(dag["steps"]),
        description="手动模式 — 请选择下一步",
        actions=[], user_action=True,
        available_steps=available, control_mode="manual",
        message=f"手动模式: {len(available)} 个可用步骤",
    )


def _try_subtask_step(fs, config, task):
    from kanban_framework.domain.state_machine_subtask import inject_subtask_steps
    fresh_progress = load_progress(fs, task.id)
    fresh_completed = {k for k, v in fresh_progress.get("steps", {}).items()
                       if v.get("status") in ("completed", "skipped")}
    return inject_subtask_steps(fs, config, task, fresh_progress, fresh_completed, NextStepResult)


def _build_step_result(fs, config, task, step, i, phase_steps, phase_value):
    context_files = _get_context_files(fs, task, phase_value)
    prompt = step.spawn_prompt
    if prompt:
        td = fs.task_dir(task.id)
        iter_dir = td / f"iteration-{task.iteration}"
        prompt = prompt.replace("$knowledge_protocol", _resolve_workflow_prompt(config.workflow, "knowledge_protocol", KNOWLEDGE_SEARCH_PROTOCOL))
        prompt = prompt.replace("$task_id", task.id)
        prompt = prompt.replace("$task_dir", str(td))
        prompt = prompt.replace("$report_dir", str(iter_dir))
        prompt = prompt.replace("$iteration", str(task.iteration))
        prompt = prompt.replace("$output_dir", _output_dir_hint(config.output_dir))
        prompt = prompt.replace("$kanban_dir", str(fs.kanban_dir))
        wctx = _build_worker_context(fs, task)
        if wctx:
            prompt = prompt + "\n\n" + wctx

    knowledge_ctx = _auto_knowledge_retrieval(fs, task, step.id, getattr(step, "knowledge", None))
    codegraph_ctx = _build_codegraph_context(fs, task, step.id)
    if codegraph_ctx and prompt:
        prompt = prompt + "\n\n" + codegraph_ctx
    elif codegraph_ctx:
        prompt = codegraph_ctx

    hooks = _resolve_prompt_hooks(config, phase_value, step.id, task.mode)
    if hooks:
        hook_text = "\n\n## 项目定制要求（prompt_hooks）\n" + "\n".join(f"- {h}" for h in hooks)
        prompt = (prompt + hook_text) if prompt else hook_text

    if prompt and task.test_config and phase_value == "evaluate":
        level = task.test_config.get("level", "")
        if level:
            prompt += f"\n\n## 测试级别: {level}\n按 {level} 级别深度执行验证。"

    # Auto mode: inject framework issue tracking instruction
    if (prompt and task.control_mode == ControlMode.AUTO
            and phase_value == "execute" and step.spawn_prompt):
        prompt += _FRAMEWORK_ISSUES_INSTRUCTION

    stype = "spawn" if step.spawn_prompt else ("interactive" if step.interactive else "action")

    return NextStepResult(
        task_id=task.id, phase=phase_value,
        step_id=step.id, step_index=i,
        total_steps=len(phase_steps),
        description=step.description,
        step_type=stype,
        actions=_inject_knowledge_json(
            [a.replace("$task_id", task.id) for a in step.actions]),
        agent_type=step.agent_type,
        parallel=step.parallel,
        user_action=step.user_action,
        context_files=context_files,
        knowledge_summary=_load_knowledge_summary(fs, task),
        knowledge_context=knowledge_ctx,
        codegraph_context=codegraph_ctx if codegraph_ctx else None,
        depends_on_files=_step_depends_on.get(step.id, []),
        knowledge_available=_is_knowledge_available(fs),
        interactive_prompt=_interactive_prompts.get(step.id),
        message=f"当前阶段: {phase_value}, 步骤 {i+1}/{len(phase_steps)}: {step.description}",
        spawn_prompt=prompt,
        interactive=step.interactive,
    )


def _build_phase_transition(task, phase_value, phase_steps, lightweight, custom_order=None):
    phase_order = _get_phase_order(lightweight, quick=(task.mode == "quick"),
                                   custom_order=custom_order)
    str_order = [p.value if isinstance(p, Phase) else str(p) for p in phase_order]
    current_idx = None
    for idx, p_str in enumerate(str_order):
        if p_str == phase_value:
            current_idx = idx
            break

    if current_idx is not None and current_idx < len(str_order) - 1:
        next_str = str_order[current_idx + 1]
        return NextStepResult(
            task_id=task.id, phase=phase_value,
            step_id=f"transition_to_{next_str}",
            step_index=len(phase_steps), total_steps=len(phase_steps),
            description=f"阶段 {phase_value} 全部完成，准备进入 {next_str}",
            actions=[
                f"kanban workflow transition {task.id} {next_str}",
                f"kanban workflow next-step {task.id}",
            ],
            phase_complete=True,
            message=f"阶段 {phase_value} 完成 → {next_str}",
        )

    # Current phase not in order (e.g., evaluate in quick mode) — guide to nearest valid phase
    if current_idx is None and str_order:
        _FULL_ORDER = [p.value for p in [
            Phase.PLAN, Phase.PLAN_REVIEW, Phase.QA_SPEC, Phase.SPEC_REVIEW,
            Phase.EXECUTE, Phase.EVALUATE, Phase.RETROSPECTIVE,
            Phase.USER_DECISION, Phase.ARCHIVE,
        ]]
        try:
            full_idx = _FULL_ORDER.index(phase_value)
        except ValueError:
            full_idx = 0
        # Find the first target phase at or after current position
        target = str_order[0]
        for tp in str_order:
            try:
                tp_idx = _FULL_ORDER.index(tp)
            except ValueError:
                continue
            if tp_idx <= full_idx:
                target = tp
        return NextStepResult(
            task_id=task.id, phase=phase_value,
            step_id=f"redirect_to_{target}",
            step_index=0, total_steps=0,
            description=f"当前阶段 {phase_value} 不在当前模式流程中，跳转到 {target}",
            actions=[
                f"kanban workflow transition {task.id} {target}",
                f"kanban workflow next-step {task.id}",
            ],
            message=f"阶段 {phase_value} 不在流程中 → 跳转 {target}",
        )

    return NextStepResult(
        task_id=task.id, phase=phase_value, step_id="all_done",
        step_index=len(phase_steps), total_steps=len(phase_steps),
        description="所有阶段已完成",
        actions=[], all_complete=True,
        message="任务流程全部完成",
    )


# Re-export utility functions for backward compatibility
from kanban_framework.domain.state_machine_utils import next_step_to_dict, rollback_step  # noqa: F401
