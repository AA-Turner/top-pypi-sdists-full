"""Quick mode — KB + superpowers plan + human review."""
from __future__ import annotations
from kanban_framework.domain.steps_types import StepDef

QUICK_STEPS: dict[str, list[StepDef]] = {
    "plan": [
        StepDef("plan.knowledge_search", "知识库检索：查踩坑 + 最佳实践", agent_type="general-purpose", spawn_prompt="""\
你是 kanban 任务 $task_id 的快速知识检索 Agent。
任务目标：快速检索知识库中与当前任务相关的踩坑和规范。

参考文件：$task_dir/task.json（任务标题和描述）

执行步骤：
1. kanban knowledge hybrid "<任务标题> 踩坑 注意事项" --biz $biz_tag --json --summary-only
2. kanban knowledge search "<关键词> 规范 best-practice" --biz $biz_tag --intent pitfall_check --json --summary-only
3. 筛选最相关的 2-3 条（high/medium）
4. 写入 $task_dir/pitfall_warnings.md：
   - 每个条目一行：`[ID] 标题 — 关键建议`

$knowledge_protocol

完成标志：$task_dir/pitfall_warnings.md 存在。""", use_subagent=True),
        StepDef("plan.plan_writer", "编写执行计划：superpowers:writing-plans + KB 约束", agent_type="general-purpose", spawn_prompt="""\
你是 kanban 任务 $task_id 的快速规划 Agent。
使用 superpowers:writing-plans 技能编写精简执行计划。

参考文件：
- $task_dir/task.json（任务标题和描述）
- $task_dir/pitfall_warnings.md（⚠️ KB 检索的踩坑预警）

任务边界：
- 产出 $task_dir/spec.md（需求设计，1 页）
- 产出 $task_dir/plan/index.md（执行步骤，3-5 步）
- spec.md 中必须包含「KB 约束」章节，引用 pitfall_warnings.md 中的条目
- 不需要 task_breakdown.json（quick 模式无多任务拆解）
- 完成后立即停止

$knowledge_protocol

完成标志：$task_dir/spec.md 和 $task_dir/plan/index.md 存在且非空。""", use_subagent=True),
        StepDef("plan.user_confirm", "人工确认：审核执行计划 + KB 踩坑预警", actions=["📋 展示 spec.md 执行计划", "⚠️ 展示 pitfall_warnings.md KB 踩坑预警", "🔍 kanban knowledge hybrid \"$task_title 技术方案\" --biz $biz_tag --json --summary-only", "如仅 0-1 个方案：确认后直接编码", "如有 2+ 方案：AskUserQuestion 对比后用户选择写入 tech_choice.md", "━━━━━━━━━━━━━━━━━━━━━━━━━━━", "用户确认后继续执行，或 abort 取消"], interactive=True),
    ],
    "execute": [
        StepDef("execute.spawn", "直接执行（quick 模式）", agent_type="general-purpose", spawn_prompt="""\
你是 kanban 任务 $task_id 的执行 Agent（quick 模式）。
直接根据任务描述和 plan 执行代码修改，无需评审。

参考文件：$task_dir/task.json（任务描述）
           $task_dir/spec.md（需求设计 + KB 约束）
           $task_dir/plan/index.md（执行步骤）
           $task_dir/pitfall_warnings.md（⚠️ 踩坑预警 — 必须回避）
           $task_dir/tech_choice.md（技术方案选择，如有）

$knowledge_protocol

编码约束：
- pitfall_warnings.md 列出的踩坑必须回避
- spec.md 中「KB 约束」章节的规范必须遵守
- 如不确定，kanban knowledge search "<问题>" --biz $biz_tag --intent pitfall_check --json --summary-only 动态查询

完成标志：$task_dir/execution_summary.md 存在且非空。""", use_subagent=True),
        StepDef("execute.verify", "验证修改", actions=["运行测试验证修改正确", "kanban guard check-artifacts $task_id execute"]),
    ],
    "user_decision": [
        StepDef("user_decision.present", "展示执行摘要", actions=["📋 变更摘要（execution_summary.md）", "⚠️ KB 踩坑回避确认", "━━━━━━━━━━━━━━━━━━━━━━━━━━━", "请用户选择: approve_and_archive / abort"], user_action=True),
        StepDef("user_decision.wait", "等待用户决策", actions=["kanban decide $task_id --action <approve_and_archive|abort>"], user_action=True),
    ],
    "archive": [
        StepDef("archive.guard", "归档检查", actions=["kanban guard check-inbox $task_id", "kanban clean $task_id"]),
    ],
}