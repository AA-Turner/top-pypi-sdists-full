"""Dynamic subtask execution — spawns child kanban tasks for subtasks with workflow.

Reads task_breakdown.json and when a subtask has a "workflow" field,
creates an independent kanban task instead of executing inline.
"""
from __future__ import annotations

import json
import time
from typing import Optional

from kanban_framework.types import Task
from kanban_framework.infra.config import Config
from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.domain.step_progress import save_progress


def _output_dir_hint(output_dir: str) -> str:
    return f"保存到 {output_dir}/" if output_dir else "在现有目录中修改文件"


def inject_subtask_steps(
    fs: Filesystem, config: Config, task: Task, progress: dict, completed_steps: set[str],
    result_class,
) -> Optional[object]:
    """Read task_breakdown.json. Subtasks with workflow field → spawn as child tasks."""
    from kanban_framework.domain.steps import _EXECUTOR_SUBTASK_PROMPT, _resolve_workflow_prompt

    td = fs.task_dir(task.id)
    breakdown_file = td / "task_breakdown.json"
    if not breakdown_file.is_file():
        return None

    try:
        data = json.loads(breakdown_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None

    subtasks = data.get("subtasks", [])
    if not subtasks:
        return None

    for st in subtasks:
        st_id = st.get("id", "")
        if not st_id:
            continue
        step_key = f"execute.exec_{st_id}"
        if step_key not in progress["steps"]:
            entry: dict = {"status": "pending", "updated_at": time.time()}
            if st.get("workflow"):
                entry["subworkflow"] = st.get("workflow")
                entry["subtask_title"] = st.get("title", st_id)
            progress["steps"][step_key] = entry

    save_progress(fs, task.id, progress)

    for st in subtasks:
        st_id = st.get("id", "")
        if not st_id:
            continue
        step_key = f"execute.exec_{st_id}"
        step_status = progress["steps"].get(step_key, {}).get("status", "pending")
        if step_status in ("completed", "skipped", "spawned"):
            continue

        st_title = st.get("title", st_id)
        has_sw = st.get("workflow")

        if has_sw:
            from kanban_framework.domain.subworkflow import spawn_subtask
            child_id = spawn_subtask(fs.kanban_dir, task, st)
            if child_id:
                progress["steps"][step_key]["child_task_id"] = child_id
                progress["steps"][step_key]["subworkflow"] = has_sw
                save_progress(fs, task.id, progress)

            return result_class(
                task_id=task.id, phase="execute",
                step_id=step_key, step_index=0, total_steps=len(subtasks),
                description=f"子任务 [{has_sw}]: {st_title} → {child_id or 'pending'}",
                step_type="spawn", actions=[f"kanban run {child_id}", f"kanban workflow next-step {child_id}"],
                agent_type="general-purpose", parallel=False,
                spawn_prompt=(
                    f"已为 subtask {st_id} ({st_title}) 创建独立看板任务: {child_id}\n\n"
                    f"该子任务使用 {has_sw} 模式运行。请按标准看板流程执行:\n"
                    f"1. kanban run {child_id}  → 进入第一个阶段\n"
                    f"2. kanban workflow next-step {child_id}  → 获取下一步\n"
                    f"3. 按步骤逐步执行，直到子任务归档\n"
                    f"4. 子任务完成后，回到父任务继续\n\n"
                    f"参考父任务 spec.md 和 plan 文件了解子任务上下文。"
                ),
                message=f"独立子任务 [{has_sw}]: {st_title} → {child_id or 'failed'}",
            )

        # Legacy inline executor
        plan_slug = st_title.lower().replace(" ", "_")
        plan_file = f"{st_id}_{plan_slug}.md"
        td_path = str(td)
        iter_dir = str(td / f"iteration-{task.iteration}")

        prompt = _resolve_workflow_prompt(config.workflow, "executor_subtask", _EXECUTOR_SUBTASK_PROMPT)
        prompt = prompt.replace("$task_id", task.id)
        prompt = prompt.replace("$task_dir", td_path)
        prompt = prompt.replace("$report_dir", iter_dir)
        prompt = prompt.replace("$output_dir", _output_dir_hint(config.output_dir))
        prompt = prompt.replace("$subtask_id", st_id)
        prompt = prompt.replace("$subtask_title", st_title)
        prompt = prompt.replace("$subtask_plan", plan_file)

        return result_class(
            task_id=task.id, phase="execute", step_id=step_key, step_index=0,
            total_steps=len(subtasks), description=f"执行 subtask {st_id}: {st_title}",
            step_type="spawn", actions=[f"执行 subtask {st_id}"],
            agent_type="general-purpose", parallel=False,
            spawn_prompt=prompt,
            message=f"执行 subtask {st_id}: {st_title}",
        )

    return None


# ── Step dependency and interactive prompt tables ────────────────────────

_step_depends_on: dict[str, list[str]] = {
    "plan.plan_B": ["spec.md"],
    "execute.spawn": ["task_breakdown.json", "plan/index.md"],
    "evaluate.spawn": ["execution_summary.md"],
    "evaluate.spawn_qa": ["execution_summary.md"],
}

_interactive_prompts: dict[str, str] = {
    "plan.plan_A": (
        "使用 Skill 工具调用 superpowers:brainstorming，与用户交互完成需求澄清。\n\n"
        "**步骤 0 — 知识库检索（必须最先执行）：**\n"
        "1. kanban knowledge hybrid \"<任务标题>\" --json\n"
        "2. kanban knowledge search \"<领域关键词>\" --intent pitfall_check --json\n"
        "3. kanban knowledge search \"<领域关键词>\" --intent experience_reuse --json\n"
        "4. 将检索到的知识条目摘要（id + title + 关键内容一行）放入 spec.md 的「知识库参考」章节\n\n"
        "**步骤 1-4 — 需求澄清：**\n"
        "1. 询问功能需求 2. 询问非功能需求 3. 询问技术约束 4. 询问验收标准\n\n"
        "完成后将结果写入 $task_dir/spec.md。"
    ),
    "plan.user_confirm_spec": (
        "向用户展示 spec.md 的内容摘要，请用户确认。"
    ),
}
