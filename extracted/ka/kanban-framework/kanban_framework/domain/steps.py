"""Step definitions for each workflow mode (full / lightweight / quick).

Separated from state_machine.py for maintainability — step definitions
are pure data and rarely change together with the orchestration logic.
"""
from __future__ import annotations

from kanban_framework.types import Phase
from kanban_framework.infra.scheduler import Scheduler

from kanban_framework.domain.steps_types import StepDef  # noqa: F401
from kanban_framework.domain.steps_full import FULL_STEPS  # noqa: F401
from kanban_framework.domain.steps_lightweight import LIGHTWEIGHT_STEPS  # noqa: F401
from kanban_framework.domain.steps_quick import QUICK_STEPS  # noqa: F401

# Knowledge retrieval preamble — first agent seeds the pool, all agents read + supplement dynamically
_KNOWLEDGE_PREAMBLE_FIRST = (
    "【知识库检索 — 首个 Agent，建立共享知识池】\n"
    "根据任务的实际内容动态检索，而非预设关键词：\n"
    "1. 全局检索：kanban knowledge hybrid \"$task_title 踩坑 注意事项 最佳实践\" --json --summary-only\n"
    "2. 筛选 3-10 条最相关的条目，kanban knowledge get <id> --json 取详情\n"
    '3. 将筛选结果写入 $task_dir/plan/knowledge_used.json（后续 Agent 复用）：\n'
    '   {"matched": [{"id": "K001", "title": "...", "relevance": "high", "how_to_apply": "..."}]}\n'
    "4. 在你的产出文档中标注「知识库参考」章节，列出你实际引用了哪些条目\n"
    "5. 如发现新的通用模式/踩坑，kanban knowledge add 写入知识库\n\n"
)

_KNOWLEDGE_PREAMBLE_REUSE = (
    "【知识库参考 — 共享知识池】\n"
    "任务已有知识池：$task_dir/plan/knowledge_used.json\n"
    "1. 首先读取该文件，应用其中 high/medium 条目\n"
    "2. 工作中遇到具体问题时，按需动态检索（不要预设式搜索）：\n"
    "   - 遇到报错/异常 → kanban knowledge hybrid \"<错误关键词>\" --json --summary-only\n"
    "   - 技术选型不确定 → kanban knowledge hybrid \"<技术点> 最佳实践\" --json --summary-only\n"
    "   - 需要参考模式 → kanban knowledge hybrid \"<模式名> 踩坑\" --json --summary-only\n"
    "3. 检索到的新条目追加写入 knowledge_used.json（合并，保留已有条目）\n"
    "4. 在你的产出文档中标注「知识库参考」章节，列出你实际引用了哪些条目（格式：[K001] 条目标题 — 如何应用）\n"
    "5. 发现新通用模式/踩坑 → kanban knowledge add 补充写入\n\n"
)

_KNOWLEDGE_PROTOCOL = (
    "【知识库检索协议 — 必须遵守】\n"
    "- 检索前先查已有踩坑记录，避免重蹈覆辙\n"
    "- 方案选型时搜索最佳实践，不要凭经验猜测\n"
    "- 完成编码后，提取通用模式写入知识库\n"
    "$knowledge_protocol"
)

# Step types that should NOT get knowledge auto-injection
_KNOWLEDGE_SKIP_PREFIXES = (
    "plan.complete", "execute.complete", "evaluate.complete",
    "retrospective.complete", "spec_review.complete", "plan_review.complete",
    "qa_spec.complete", "user_decision.", "archive.",
)

KNOWLEDGE_SEARCH_PROTOCOL = (
    "知识库检索协议（Token 高效模式）：\n"
    "- 所有 kanban knowledge search/hybrid/semantic 必须加 --json --summary-only\n"
    "- --summary-only 会省略 content/code_example 等重字段，只返回元数据\n"
    "- 先用 .data.summary（id+title+relevance）筛选 2-5 条最相关条目\n"
    "- 对筛选出的条目：kanban knowledge get <id> --json 取完整详情\n"
    "- 例外：--intent pitfall_check 结果 ≤5 条，可用 --json（不带 --summary-only）"
)

_EXECUTOR_SUBTASK_PROMPT = (
    "你是 kanban 任务 $task_id 的执行器。"
    "按 TDD 方式实现分配给你的 subtask。\n\n"
    "你的 subtask: $subtask_id — $subtask_title\n"
    "参考文件：$task_dir/plan/$subtask_plan（你的 subtask plan）、$task_dir/test_spec.md\n"
    "技术方案选择：$task_dir/tech_choice.md（如有，优先按此方案执行）\n\n"
    "实时知识库贡献（执行中发现通用模式/踩坑时立即写入，不要等到归档）：\n"
    "- **何时写**：发现通用技术模式、框架 API 的坑、跨项目可复用的方案时\n"
    "- **如何写**：`kanban knowledge add --domain <对应领域> --category <架构|踩坑|反模式|最佳实践|优化|流程|接口|工具> --severity <high|medium|low> --ttl 90 --title \"<简短标题>\" --content \"<问题+方案>\" --source '{\"type\":\"executor_realtime\",\"task_id\":\"$task_id\"}'`\n"
    "- category 和 severity 必须从标准枚举中选，否则写入失败。`kanban knowledge categories` 查看完整列表\n"
    "  --source 标记来源为 executor_realtime，便于后续审计和质量检查\n"
    "- 知识条目写入后状态为 pending，需人工审核后正式入库。\n"
    "- **不要写**：本项目特有的业务逻辑、一次性的配置值\n"
    "- **注意**：如果知识库中已有类似条目（同 title+domain），add_entry 会自动去重跳过\n\n"
    "任务边界：\n"
    "- 实现代码并保存到 $output_dir\n"
    "- 编写测试并确保通过\n"
    "- 产出 execution_summary.md 保存到 $report_dir/execute/\n"
    "- 完成后立即停止\n"
    "- 除 `kanban knowledge add` 外不要调用其他 kanban CLI 命令\n"
    "- 不要进入 evaluate 或后续阶段\n\n"
    "【遇到错误时先查知识库（重要）】\n"
    "- 遇到报错、异常、环境问题、依赖冲突等，先搜索知识库：\n"
    "  kanban knowledge hybrid \"<错误关键词>\" --json --summary-only\n"
    "- 如果知识库有相关踩坑记录，按记录中的方案优先尝试\n"
    "- 同问题尝试 3 次仍未解决，记录到 execution_pitfalls.md 并标记为需人工介入\n"
    "- 不要反复尝试同样的方案——每次尝试前先查知识库找新思路\n\n"
    "【test_spec.md 覆盖硬约束】\n"
    "- 你必须逐一实现 $task_dir/test_spec.md 中与当前 subtask 相关的 UT-xxx 测试用例\n"
    "- 每个测试函数名或 docstring 中标注对应的 UT-xxx 编号（如 test_xxx_ut001 或 # UT-001）\n"
    "- execution_summary.md 的 TDD 证据表中标注每个 UT-xxx 的实现状态\n"
    "- Guard 会自动检查覆盖率：覆盖率 < 50% 将阻塞流程\n\n"
    "完成标志：$report_dir/execute/execution_summary.md 文件存在且非空。"
)


def _inject_knowledge_json(actions: list[str]) -> list[str]:
    """Auto-append --json --summary-only to knowledge search/hybrid/semantic commands."""
    import re
    result = []
    for a in actions:
        if re.search(r'\bkanban knowledge (search|hybrid|semantic)\b', a):
            if '--json' not in a:
                a = a + ' --json'
            if '--summary-only' not in a and 'pitfall_check' not in a:
                a = a + ' --summary-only'
        result.append(a)
    return result


_EXECUTOR_SUBTASK_PROMPT = (
    "你是 kanban 任务 $task_id 的执行器。"
    "按 TDD 方式实现分配给你的 subtask。\n\n"
    "你的 subtask: $subtask_id — $subtask_title\n"
    "参考文件：$task_dir/plan/$subtask_plan（你的 subtask plan）、$task_dir/test_spec.md\n"
    "技术方案选择：$task_dir/tech_choice.md（如有，优先按此方案执行）\n\n"
    "实时知识库贡献（执行中发现通用模式/踩坑时立即写入，不要等到归档）：\n"
    "- **何时写**：发现通用技术模式、框架 API 的坑、跨项目可复用的方案时\n"
    "- **如何写**：`kanban knowledge add --domain <对应领域> --category <架构|踩坑|反模式|最佳实践|优化|流程|接口|工具> --severity <high|medium|low> --ttl 90 --title \"<简短标题>\" --content \"<问题+方案>\" --source '{\"type\":\"executor_realtime\",\"task_id\":\"$task_id\"}'`\n"
    "- category 和 severity 必须从标准枚举中选，否则写入失败。`kanban knowledge categories` 查看完整列表\n"
    "  --source 标记来源为 executor_realtime，便于后续审计和质量检查\n"
    "- 知识条目写入后状态为 pending，需人工审核后正式入库。\n"
    "- **不要写**：本项目特有的业务逻辑、一次性的配置值\n"
    "- **注意**：如果知识库中已有类似条目（同 title+domain），add_entry 会自动去重跳过\n\n"
    "任务边界：\n"
    "- 实现代码并保存到 $output_dir\n"
    "- 编写测试并确保通过\n"
    "- 产出 execution_summary.md 保存到 $report_dir/execute/\n"
    "- 完成后立即停止\n"
    "- 除 `kanban knowledge add` 外不要调用其他 kanban CLI 命令\n"
    "- 不要进入 evaluate 或后续阶段\n\n"
    "【遇到错误时先查知识库（重要）】\n"
    "- 遇到报错、异常、环境问题、依赖冲突等，先搜索知识库：\n"
    "  kanban knowledge hybrid \"<错误关键词>\" --json --summary-only\n"
    "- 如果知识库有相关踩坑记录，按记录中的方案优先尝试\n"
    "- 同问题尝试 3 次仍未解决，记录到 execution_pitfalls.md 并标记为需人工介入\n"
    "- 不要反复尝试同样的方案——每次尝试前先查知识库找新思路\n\n"
    "【test_spec.md 覆盖硬约束】\n"
    "- 你必须逐一实现 $task_dir/test_spec.md 中与当前 subtask 相关的 UT-xxx 测试用例\n"
    "- 每个测试函数名或 docstring 中标注对应的 UT-xxx 编号（如 test_xxx_ut001 或 # UT-001）\n"
    "- execution_summary.md 的 TDD 证据表中标注每个 UT-xxx 的实现状态\n"
    "- Guard 会自动检查覆盖率：覆盖率 < 50% 将阻塞流程\n\n"
    "完成标志：$report_dir/execute/execution_summary.md 文件存在且非空。"
)


def _resolve_workflow_prompt(workflow: dict | None, key: str, default: str) -> str:
    """Read a prompt override from workflow.json, falling back to the hardcoded default."""
    if not workflow or not isinstance(workflow, dict):
        return default
    prompts = workflow.get("prompts", {})
    if isinstance(prompts, dict):
        val = prompts.get(key)
        if val and isinstance(val, str):
            return val
    return default


def _get_steps(mode: str, custom_steps: dict[str, list[StepDef]] | None = None) -> dict[str, list[StepDef]]:
    if custom_steps is not None:
        return custom_steps
    try:
        from kanban_framework.domain.steps_loader import load_steps_for_mode
        from kanban_framework.infra.filesystem import Filesystem
        from kanban_framework.infra.config import Config
        root = Filesystem.find_project_root()
        fs = Filesystem(root)
        cfg = Config(fs)
        result = load_steps_for_mode(cfg.workflow, mode, kanban_dir=fs.kanban_dir)
        if result and any(v for v in result.values()):
            # Apply extensions if active for this mode
            from kanban_framework.domain.workflow_extensions import WorkflowExtension
            ext = WorkflowExtension(cfg.workflow)
            if ext.is_active_for_mode(mode):
                result = ext.build_step_map(result, mode=mode)
            return result
    except (OSError, ValueError, KeyError):
        pass
    if mode == "quick":
        return QUICK_STEPS
    if mode == "lightweight":
        return LIGHTWEIGHT_STEPS
    return FULL_STEPS


def _get_phase_order(lightweight: bool, quick: bool = False,
                     custom_order: list[str] | None = None,
                     workflow: dict | None = None,
                     mode: str | None = None,
                     kanban_dir=None) -> list[Phase | str]:
    if custom_order is not None:
        return custom_order
    return Scheduler.dispatch_order(lightweight=lightweight, quick=quick,
                                     mode=mode, workflow=workflow,
                                     kanban_dir=kanban_dir)
