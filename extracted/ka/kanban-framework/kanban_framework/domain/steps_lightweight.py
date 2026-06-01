"""Lightweight mode step definitions."""
from __future__ import annotations
from kanban_framework.domain.steps_types import StepDef
from kanban_framework.domain.steps_full import FULL_STEPS

LIGHTWEIGHT_STEPS: dict[str, list[StepDef]] = {
    "plan": [
        StepDef("plan.knowledge_search", "知识库检索 — 强制产出 knowledge_used.json",
                actions=["kanban time start $task_id knowledge_search",
                         "spawn kanban-knowledge-capture agent 执行知识检索",
                         "kanban time end $task_id knowledge_search"],
                agent_type="general-purpose",
                spawn_prompt=(
                    "你是 kanban 任务 $task_id 的知识检索 Agent（轻量模式）。\n"
                    "任务目标：从知识库中找到与当前任务相关的所有知识条目，并产出引用清单。\n\n"
                    "参考文件：$task_dir/task.json（任务标题和描述）\n\n"
                    "执行步骤：\n"
                    "1. 读取 task.json 获取任务标题和描述\n"
                    "2. kanban knowledge hybrid \"<任务标题+描述关键词>\" --json --summary-only\n"
                    "3. 对搜索结果逐一判断相关性，筛选出 medium/high 的条目\n"
                    "4. 如无匹配，kanban knowledge search \"<关键词>\" --intent experience_reuse --json --summary-only\n"
                    "5. 仍无匹配则记录原因（如：全新领域、无相关经验）\n\n"
                    "$knowledge_protocol\n\n"
                    "输出：写入 $task_dir/plan/knowledge_used.json\n"
                    "完成标志：$task_dir/plan/knowledge_used.json 文件存在且非空。"
                )),
        StepDef("plan.plan_A", "Plan: 需求澄清（brainstorming，轻量）",
                actions=["kanban time start $task_id plan_A",
                         "使用 Skill tool 调用 superpowers:brainstorming",
                         "产出 spec.md 保存到 $task_dir/spec.md",
                         "kanban time end $task_id plan_A"],
                interactive=True),
        StepDef("plan.check_constraints", "知识库约束检查：编码前搜索相关约束与模式",
                actions=["kanban knowledge hybrid \"$task_title\" --json",
                         "搜索知识库中与当前任务相关的约束条件、架构模式和已知踩坑记录",
                         "将发现的约束记录到 plan/constraints.md"],
                agent_type="general-purpose"),
        # Lightweight: no user_confirm_spec - brainstorming already
        # gathered requirements interactively, proceed to task breakdown
        StepDef("plan.plan_B", "Plan: 任务拆解（writing-plans）",
                actions=["kanban time start $task_id plan_B",
                         "spawn writing-plans agent",
                         "kanban time end $task_id plan_B"],
                agent_type="general-purpose",
                spawn_prompt=(
                    "你是 kanban 任务 $task_id 的 writing-plans 子任务。"
                    "使用 superpowers:writing-plans 技能完成任务拆解。\n\n"
                    "参考文件：$task_dir/spec.md（已由 brainstorming 产出）\n\n"
                    "任务边界：\n"
                    "- 产出 plan/index.md、plan/ST-NNN_*.md、task_breakdown.json 保存到 $task_dir/\n"
                    "- 完成后立即停止，不要建议或选择执行方式\n"
                    "- 不要调用任何 kanban CLI 命令\n\n"
                    "完成标志：$task_dir/plan/index.md 和 $task_dir/task_breakdown.json 文件存在且非空。"
                )),
        StepDef("plan.complete", "Plan 阶段完成",
                actions=["kanban time end $task_id plan",
                         "kanban guard check-artifacts $task_id plan",
                         "kanban workflow checkpoint $task_id plan",
                         "kanban workflow complete-phase $task_id"]),
    ],
    "execute": FULL_STEPS["execute"],
    "evaluate": [
        StepDef("evaluate.spawn_qa", "QA 单角色评估 (lightweight)",
                actions=["spawn kanban-qa agent (eval mode)"],
                agent_type="general-purpose"),
        StepDef("evaluate.e2e_run", "E2E 测试执行（如项目配置了 E2E）",
                actions=["检查 $task_dir/test_spec.md 是否包含 E2E 用例",
                         "如有 E2E 用例则执行浏览器测试",
                         "无 E2E 用例则跳过此步骤"],
                agent_type="general-purpose",
                spawn_prompt=(
                    "你是 kanban 任务 $task_id 的 E2E 测试执行器。\n"
                    "在浏览器中实际验证功能是否正常工作。\n\n"
                    "参考文件：$task_dir/test_spec.md\n\n"
                    "任务边界：\n"
                    "- 启动浏览器执行 E2E 场景\n"
                    "- 产出报告保存到 $report_dir/reviews/e2e_report.json\n"
                    "- 如无 E2E 配置或浏览器不可用，产出说明性报告并完成\n"
                    "- 完成后立即停止\n\n"
                    "完成标志：$report_dir/reviews/e2e_report.json 文件存在且非空。"
                )),
        StepDef("evaluate.collect_score", "收集评分",
                actions=["评分已由 complete-phase 自动同步"]),
        StepDef("evaluate.check_score", "评分检查",
                actions=["kanban workflow self-improve-check $task_id"]),
        StepDef("evaluate.complete", "Evaluate 完成",
                actions=["kanban workflow complete-phase $task_id"]),
    ],
    "user_decision": FULL_STEPS["user_decision"],
    "archive": FULL_STEPS["archive"],
}
