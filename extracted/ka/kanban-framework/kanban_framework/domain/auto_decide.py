"""Auto-decider integration for --auto-mode all.

When auto_mode flags are enabled, user_action steps get an auto-decider
spawn_prompt injected so the orchestrator can handle them via normal
spawn flow instead of blocking for human input.
"""
from __future__ import annotations

import json
from pathlib import Path

from kanban_framework.types import Task, Phase


_CONFIDENCE_THRESHOLD = 0.7

# Step ID prefixes that map to auto_mode flags
# NOTE: user_decision intentionally NOT in auto-decide — human must always
# review before archive. Auto-mode advances through plan/execute/evaluate
# but stops at user_decision for human verification.
_STEP_FLAG_MAP = {
    "plan": "auto_brainstorm",
    "evaluate": "auto_iteration",
}

# Valid decisions per phase
_VALID_DECISIONS = {
    "brainstorm": {"approve", "revise", "defer_to_user"},
    "iteration": {"archive", "hot_iteration", "full_iteration", "defer_to_user"},
    "archive": {"approve_and_archive", "approve", "abort", "restart_from_plan",
                "restart_from_execute", "defer_to_user"},
}

# Map auto-decider decisions to kanban decide actions
_DECISION_ACTION_MAP = {
    "approve": "approve_and_archive",
    "approve_and_archive": "approve_and_archive",
    "abort": "abort",
    "restart_from_plan": "restart_from_plan",
    "restart_from_execute": "restart_from_execute",
    "hot_iteration": "restart_from_execute",
    "full_iteration": "restart_from_plan",
}


def should_auto_decide(task: Task, step_id: str) -> bool:
    """Check if this user_action step should trigger auto-decision."""
    phase = task.phase_id
    flag_name = None
    for prefix, flag in _STEP_FLAG_MAP.items():
        if phase == prefix or step_id.startswith(prefix + "."):
            flag_name = flag
            break
    if flag_name is None:
        return False
    return bool(getattr(task.auto_mode, flag_name, False))


def _decide_mode(task: Task) -> str:
    """Determine the auto-decider mode from task phase."""
    phase = task.phase_id
    if phase == "plan":
        return "brainstorm"
    if phase == "evaluate":
        return "iteration"
    if phase == "user_decision":
        return "archive"
    # For steps in other phases that have user_action (e.g. plan.user_confirm_spec)
    return "brainstorm"


def build_auto_decide_prompt(task: Task, step_id: str, fs) -> str | None:
    """Generate auto-decider spawn_prompt for a user_action step."""
    mode = _decide_mode(task)
    task_dir = fs.task_dir(task.id)
    iter_dir = task_dir / f"iteration-{task.iteration}"

    builders = {
        "brainstorm": _build_brainstorm_prompt,
        "iteration": _build_iteration_prompt,
        "archive": _build_archive_prompt,
    }
    builder = builders.get(mode)
    if builder is None:
        return None
    return builder(task, task_dir, iter_dir)


def _build_brainstorm_prompt(task: Task, task_dir: Path, iter_dir: Path) -> str:
    spec_path = task_dir / "spec.md"
    return f"""你是任务 {task.id} 的 auto-decider agent。
模式: brainstorm-approval

评估 spec.md 是否满足要求。读取文件: {spec_path}

任务原始描述:
标题: {task.title}
描述: {task.description}

评估标准 (每项 0-10):
1. 需求清晰度: spec.md 是否包含明确的功能需求、非功能需求、验收标准
2. 技术可行性: 技术栈选择是否合理
3. 范围完整性: 是否覆盖原始描述的所有要点
4. 歧义检查: 是否存在模糊描述

产出 JSON 文件: {iter_dir}/auto_decision_brainstorm.json
格式:
{{
  "decision": "approve|revise|defer_to_user",
  "confidence": 0.0,
  "scores": {{
    "requirement_clarity": 0.0,
    "technical_feasibility": 0.0,
    "scope_completeness": 0.0,
    "ambiguity_check": 0.0
  }},
  "findings": ["..."],
  "issues": ["..."],
  "reasoning": "..."
}}

决策规则:
- 均分 >= 7.0 且无 critical issues → approve
- 均分 < 7.0 或有 critical issues → revise
- 不确定时 → defer_to_user

完成标志: {iter_dir}/auto_decision_brainstorm.json 存在且为合法 JSON。"""


def _build_iteration_prompt(task: Task, task_dir: Path, iter_dir: Path) -> str:
    score_path = iter_dir / "score.json"
    reviews_dir = iter_dir / "reviews"
    return f"""你是任务 {task.id} 的 auto-decider agent。
模式: iteration-routing

评估当前迭代结果，决定下一步方向。

读取文件:
- 评分报告: {score_path}
- 评审报告: {reviews_dir}/
- 任务状态: {task_dir}/task.json

当前迭代: {task.iteration}
评估标准:
1. 评分分析: 各维度评分是否达标 (>= pass_threshold)
2. 架构风险: critical_issues 中是否有架构级问题
3. 改进可行性: issues 是否可在 hot iteration 中修复
4. 迭代预算: 当前 iteration={task.iteration}

产出 JSON 文件: {iter_dir}/auto_decision_iteration.json
格式:
{{
  "decision": "archive|hot_iteration|full_iteration|defer_to_user",
  "confidence": 0.0,
  "reasoning": "...",
  "key_factors": ["..."],
  "suggested_focus": "..."
}}

决策规则:
- 全部通过 + iterations 未超限 → archive
- 评分 >= 7.0 + 无架构问题 → hot_iteration
- 评分 < 7.0 或有架构问题 → full_iteration
- 已达 max_iterations → archive
- 不确定 → defer_to_user

完成标志: {iter_dir}/auto_decision_iteration.json 存在且为合法 JSON。"""


def _build_archive_prompt(task: Task, task_dir: Path, iter_dir: Path) -> str:
    retro_path = task_dir / "retrospective.md"
    acceptance_path = task_dir / "acceptance.md"
    return f"""你是任务 {task.id} 的 auto-decider agent。
模式: archive-approval

评估任务是否可以归档。

读取文件:
- 复盘总结: {retro_path}
- 验收文档: {acceptance_path}
- 所有迭代评分: {task_dir}/

评估标准:
1. 产物完整性: 所有 required_artifacts 存在且非空
2. 复盘质量: retrospective.md 是否包含 pitfalls + decisions
3. 验收覆盖: acceptance.md 是否覆盖功能需求
4. 评分趋势: 最终评分是否达标

产出 JSON 文件: {iter_dir}/auto_decision_archive.json
格式:
{{
  "decision": "approve_and_archive|abort|defer_to_user",
  "confidence": 0.0,
  "reasoning": "...",
  "checks": {{
    "artifacts_complete": true,
    "retrospective_quality": true,
    "acceptance_coverage": true,
    "score_acceptable": true
  }}
}}

决策规则:
- 所有 checks 通过 → approve_and_archive
- 关键产物缺失 → abort
- 不确定 → defer_to_user

完成标志: {iter_dir}/auto_decision_archive.json 存在且为合法 JSON。"""


def parse_auto_decision(task_dir: Path, iteration: int,
                        phase: str) -> dict | None:
    """Read and validate auto_decision_{phase}.json."""
    iter_dir = task_dir / f"iteration-{iteration}"
    decision_path = iter_dir / f"auto_decision_{phase}.json"
    if not decision_path.is_file():
        return None

    try:
        data = json.loads(decision_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None

    decision = data.get("decision", "")
    valid = _VALID_DECISIONS.get(phase, set())
    if decision not in valid:
        # Try archive decisions as fallback
        if decision in _VALID_DECISIONS.get("archive", set()):
            pass
        else:
            return None

    confidence = float(data.get("confidence", 0))
    action = _DECISION_ACTION_MAP.get(decision, decision)

    return {
        "decision": decision,
        "confidence": confidence,
        "action": action,
        "reasoning": data.get("reasoning", ""),
        "auto_decided": confidence >= _CONFIDENCE_THRESHOLD,
        "defer_to_user": confidence < _CONFIDENCE_THRESHOLD or decision == "defer_to_user",
        "raw": data,
    }


def dispatch_decision(fs, config, task_id: str, decision: dict) -> dict | None:
    """Auto-execute a parsed decision. Returns dispatch result or None if skipped.

    Only dispatches when confidence >= threshold and defer_to_user is False.
    """
    if not decision:
        return None
    if decision.get("defer_to_user", True):
        return None
    if decision.get("confidence", 0) < _CONFIDENCE_THRESHOLD:
        return None

    action = decision.get("action")
    if not action:
        return None

    try:
        from kanban_framework.cli.run import cmd_decide
        result = cmd_decide([task_id, "--action", action])
        result["auto_dispatched"] = True
        return result
    except Exception as exc:
        return {"auto_dispatched": False, "error": str(exc)}
