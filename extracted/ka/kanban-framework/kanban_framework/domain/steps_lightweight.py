"""Lightweight mode step definitions — streamlined for fast iteration."""
from __future__ import annotations
from kanban_framework.domain.steps_types import StepDef

LIGHTWEIGHT_STEPS: dict[str, list[StepDef]] = {
    "plan": [
        StepDef("plan.knowledge_search", "知识库检索 — 强制产出 knowledge_used.json",
                agent_type="general-purpose",
                spawn_prompt=(
                    "你是 kanban 任务 $task_id 的知识检索 Agent（轻量模式）。\n"
                    "任务目标：从知识库中找到与当前任务相关的所有知识条目，并产出引用清单。\n\n"
                    "参考文件：$task_dir/task.json（任务标题和描述）\n"
                    "如果 task.json 中有 biz_tag 字段，所有知识库查询命令必须带 --biz $biz_tag 参数\n\n"
                    "执行步骤：\n"
                    "1. 读取 task.json 获取任务标题和描述\n"
                    "2. kanban knowledge hybrid \"<任务标题+描述关键词>\" --biz $biz_tag --json --summary-only\n"
                    "3. 对搜索结果逐一判断相关性，筛选出 medium/high 的条目\n"
                    "4. 如无匹配，kanban knowledge search \"<关键词>\" --biz $biz_tag --intent experience_reuse --json --summary-only\n"
                    "5. 仍无匹配则记录原因（如：全新领域、无相关经验）\n\n"
                    "$knowledge_protocol\n\n"
                    "输出：写入 $task_dir/plan/knowledge_used.json\n"
                    "完成标志：$task_dir/plan/knowledge_used.json 文件存在且非空。"
                )),
        StepDef("plan.plan_A", "Plan: 需求澄清（brainstorming，轻量）",
                actions=["使用 Skill tool 调用 superpowers:brainstorming",
                         "产出 spec.md 保存到 $task_dir/spec.md"],
                interactive=True),
        StepDef("plan.plan_B", "Plan: 任务拆解（writing-plans）",
                agent_type="general-purpose",
                spawn_prompt=(
                    "你是 kanban 任务 $task_id 的 writing-plans 子任务。"
                    "使用 superpowers:writing-plans 技能完成任务拆解。\n\n"
                    "参考文件：\n"
                    "- $task_dir/spec.md（已由 brainstorming 产出）\n"
                    "- $task_dir/plan/knowledge_used.json（知识库引用清单，必须参考）\n\n"
                    "重要约束：\n"
                    "- 每个 subtask 的 plan/ST-NNN_*.md 必须在开头引用相关知识条目：\n"
                    '  \"知识库参考: [K001] xxx 模式 — 避免 xx 问题\"\n'
                    "- 如 knowledge_used.json 为空或无匹配，请在 plan/index.md 中说明原因\n\n"
                    "任务边界：\n"
                    "- 产出 plan/index.md、plan/ST-NNN_*.md、task_breakdown.json 保存到 $task_dir/\n"
                    "- 完成后立即停止，不要建议或选择执行方式\n"
                    "- 不要调用任何 kanban CLI 命令\n\n"
                    "完成标志：$task_dir/plan/index.md 和 $task_dir/task_breakdown.json 文件存在且非空。"
                )),
    ],
    "execute": [
        StepDef("execute.spawn", "执行编码（轻量模式）",
                agent_type="general-purpose",
                spawn_prompt=(
                    "你是 kanban 任务 $task_id 的执行 Agent（轻量模式）。\n"
                    "根据任务描述和 plan 直接执行代码修改，无需全量评审流程。\n\n"
                    "参考文件：$task_dir/spec.md、$task_dir/task_breakdown.json\n\n"
                    "任务边界：\n"
                    "- 编写代码并运行测试确认正确\n"
                    "- 运行测试确认修改正确\n"
                    "- 产出 execution_summary.md 保存到 $task_dir/\n"
                    "- 完成后立即停止\n"
                    "- 不要调用任何 kanban CLI 命令\n\n"
                    "完成标志：$task_dir/execution_summary.md 文件存在且非空。"
                )),
        StepDef("execute.verify", "验证执行产物",
                actions=["kanban guard check-artifacts $task_id execute"]),
    ],
    "evaluate": [
        StepDef("evaluate.spawn_review", "通用审核 (lightweight)",
                agent_type="general-purpose",
                spawn_prompt=(
                    "你是 kanban 任务 $task_id 的轻量质量审核员。\n"
                    "不要求测试覆盖率或测试用例（轻量模式无 qa_spec），聚焦实际产出质量。\n\n"
                    "审核维度（逐项检查，产出报告中每项给出结论 + 证据）：\n"
                    "1. 需求符合性 — 对照 $task_dir/spec.md，检查实现是否覆盖了所有功能点\n"
                    "2. 知识库对照 — 读取 $task_dir/plan/knowledge_used.json：\n"
                    "   - 检查实现是否应用了 high/medium 条目的建议\n"
                    "   - 搜索知识库中相关踩坑，验证代码是否避开了已知问题\n"
                    "   - 如发现未覆盖的新模式/踩坑，kanban knowledge add --biz $biz_tag 补充写入\n"
                    "3. 功能合理性 — 代码逻辑是否清晰、有没有明显 bug（人工审读即可）\n"
                    "4. 代码质量 — 命名是否合理、结构是否清晰、有无硬编码的安全问题\n\n"
                    "参考文件：$task_dir/spec.md、$task_dir/plan/knowledge_used.json、$task_dir/ 下的实现代码\n\n"
                    "任务边界：\n"
                    "- 产出 $report_dir/reviews/review_report.json\n"
                    "- 报告中必须包含「知识库对照」章节（逐条说明每个引用条目是否被正确应用）\n"
                    "- 完成后立即停止，不要进入后续阶段\n\n"
                    "完成标志：$report_dir/reviews/review_report.json 文件存在且非空。"
                )),
    ],
    "user_decision": [
        StepDef("user_decision.present", "展示变更摘要",
                actions=["展示 retrospective + acceptance + 变更全景"],
                user_action=True),
        StepDef("user_decision.wait", "等待用户决策",
                actions=["kanban decide $task_id --action <approve_and_archive|abort|restart>"],
                user_action=True),
    ],
    "archive": [
        StepDef("archive.guard", "归档 Guards — inbox + subtask + stray",
                actions=["kanban guard check-inbox $task_id",
                         "kanban guard check-pending-subtasks $task_id",
                         "kanban guard check-archive-stray $task_id"]),
    ],
}
