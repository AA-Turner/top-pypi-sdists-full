"""Quick mode step definitions."""
from __future__ import annotations
from kanban_framework.domain.steps_types import StepDef

QUICK_STEPS: dict[str, list[StepDef]] = {
    "execute": [
        StepDef("execute.pitfall_check", "踩坑预警：搜索相关踩坑记录",
                actions=["kanban knowledge hybrid \"$task_title 踩坑 注意事项 错误\" --biz $biz_tag --json --summary-only",
                         "检查是否有与当前任务相关的已知踩坑记录",
                         "将匹配到的踩坑写入 $task_dir/pitfall_warnings.md"]),
        StepDef("execute.tech_review", "技术方案评审：多方案时模型推理比较+用户确认",
                actions=["kanban knowledge hybrid \"$task_title 技术方案 实现 approach best-practice\" --biz $biz_tag --json --summary-only",
                         "对搜索结果中 category 为 最佳实践/架构/优化 的条目进一步分析",
                         "如有相关条目，用 kanban knowledge get <id> --json 取完整内容",
                         "将条目归类为不同技术方案（不同实现路径或技术选型）",
                         "如果只有 0-1 个方案：写入 $task_dir/tech_choice.md 标记方案唯一，跳过确认",
                         "如果有 2+ 个方案：深入分析每个方案的优缺点、适用场景、与当前任务的匹配度",
                         "使用 AskUserQuestion 向用户展示方案对比和推荐，等待用户选择",
                         "将分析过程和用户选择写入 $task_dir/tech_choice.md"],
                interactive=True),
        StepDef("execute.spawn", "直接执行（quick 模式）",
                agent_type="kanban-executor",
                spawn_prompt=(
                    "你是 kanban 任务 $task_id 的执行 Agent（quick 模式）。\n"
                    "直接根据任务描述执行代码修改，无需规划或评审。\n\n"
                    "参考文件：$task_dir/task.json（任务描述）\n"
                    "           $task_dir/spec.md（如有，需求设计文档）\n"
                    "           $task_dir/task_breakdown.json（如有，按子任务逐个执行）\n"
                    "踩坑预警：$task_dir/pitfall_warnings.md（如有）\n"
                    "技术方案选择：$task_dir/tech_choice.md（如有，优先按此方案执行）\n\n"
                    "任务边界：\n"
                    "- 如果 task_breakdown.json 存在，按子任务逐个执行并记录完成状态\n"
                    "- 如果不存在，直接根据 task.json 描述执行\n"
                    "- 修改代码完成任务目标\n"
                    "- 运行测试确认修改正确\n"
                    "- 产出 execution_summary.md 保存到 $task_dir/\n"
                    "- 完成后立即停止\n"
                    "- 不要调用任何 kanban CLI 命令\n\n"
                    "【Quick 模式约束】\n"
                    "- 最多修改 3 个文件，超过则说明任务不适用于 quick 模式\n"
                    "- 改动总量不超过 20 行（新增+删除）\n"
                    "- 禁止修改与任务描述无直接关系的文件\n"
                    "- 禁止大规模重构或格式化变更\n"
                    "- 如果发现问题超出 quick 模式范围（需新增多个文件、改动超 20 行），"
                    "在 execution_summary.md 中写明原因并建议切换到 lightweight 模式\n"
                    "- execution_summary.md 必须包含「改动行数统计」：列出每个文件的新增/删除行数\n\n"
                    "完成标志：$task_dir/execution_summary.md 文件存在且非空。"
                )),
        StepDef("execute.verify", "验证修改",
                actions=["运行测试验证修改正确",
                         "kanban guard check-artifacts $task_id execute"]),
        StepDef("execute.checkpoint", "Git 提交代码改动",
                actions=["kanban workflow checkpoint $task_id execute"]),
        StepDef("execute.complete", "Execute 完成",
                actions=["kanban workflow complete-phase $task_id"]),
    ],
    "user_decision": [
        StepDef("user_decision.present", "展示执行摘要",
                actions=["展示 execution_summary.md 和变更摘要"],
                user_action=True),
        StepDef("user_decision.wait", "等待用户决策",
                actions=["kanban decide $task_id --action <approve_and_archive|abort>"],
                user_action=True),
    ],
    "archive": [
        StepDef("archive.guard", "归档检查",
                actions=["kanban guard check-inbox $task_id"]),
        StepDef("archive.knowledge", "轻量级知识积累 (#361)",
                actions=["complete-phase 自动提取 execution_pitfalls.md / execution_decisions.md"]),
        StepDef("archive.cleanup", "归档清理",
                actions=["kanban clean $task_id"]),
    ],
}
