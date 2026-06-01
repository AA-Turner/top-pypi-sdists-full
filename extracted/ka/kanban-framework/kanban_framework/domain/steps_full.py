"""Full mode step definitions."""
from __future__ import annotations
from kanban_framework.domain.steps_types import StepDef

FULL_STEPS: dict[str, list[StepDef]] = {
    "plan": [
        StepDef("plan.knowledge_search", "知识库检索 — 强制产出 knowledge_used.json",
                actions=["kanban time start $task_id knowledge_search",
                         "spawn kanban-knowledge-capture agent 执行知识检索",
                         "kanban time end $task_id knowledge_search"],
                agent_type="general-purpose",
                spawn_prompt=(
                    "你是 kanban 任务 $task_id 的知识检索 Agent。\n"
                    "任务目标：从知识库中找到与当前任务相关的所有知识条目，并产出引用清单。\n\n"
                    "参考文件：$task_dir/task.json（任务标题和描述）\n\n"
                    "执行步骤：\n"
                    "1. 读取 task.json 获取任务标题和描述\n"
                    "2. kanban knowledge hybrid \"<任务标题+描述关键词>\" --json --summary-only\n"
                    "3. 对搜索结果逐一判断相关性，筛选出 medium/high 的条目\n"
                    "4. 如无匹配，kanban knowledge semantic \"<任务描述>\" --json --summary-only 扩大搜索\n"
                    "5. 仍无匹配则记录原因（如：全新领域、无相关经验）\n\n"
                    "$knowledge_protocol\n\n"
                    "输出：写入 $task_dir/plan/knowledge_used.json，格式：\n"
                    "{\n"
                    '  "matched": [\n'
                    '    {"id": "K001", "title": "...", "relevance": "high",\n'
                    '     "source": "local",\n'
                    '     "how_to_apply": "当前任务可如何借鉴该条目的具体方式"},\n'
                    '    {"id": "K005", "title": "...", "relevance": "medium",\n'
                    '     "source": "share",\n'
                    '     "how_to_apply": "..."}\n'
                    "  ],\n"
                    '  "search_queries": ["hybrid --json 搜索词1", "semantic --json 搜索词2"],\n'
                    '  "no_match_reason": null\n'
                    "}\n"
                    "source 字段取自搜索结果中的 _source 值（\"local\" 为个人知识库，\"share\" 为共享知识库）。\n\n"
                    "任务边界：\n"
                    "- 只产出 knowledge_used.json，不修改任何其他文件\n"
                    "- 完成后立即停止，不调用 kanban run/transition/complete-phase\n"
                    "- 不要进入后续阶段\n\n"
                    "完成标志：$task_dir/plan/knowledge_used.json 文件存在且非空。"
                )),
        StepDef("plan.plan_A", "Plan A: 需求澄清（brainstorming）",
                actions=["kanban time start $task_id plan_A",
                         "使用 Skill tool 调用 superpowers:brainstorming，与用户交互完成需求澄清",
                         "产出 spec.md 保存到 $task_dir/spec.md",
                         "kanban time end $task_id plan_A"],
                interactive=True),
        StepDef("plan.check_constraints", "知识库约束检查：编码前搜索相关约束与模式",
                actions=["kanban knowledge hybrid \"$task_title\" --json",
                         "搜索知识库中与当前任务相关的约束条件、架构模式和已知踩坑记录",
                         "将发现的约束记录到 plan/constraints.md"],
                agent_type="general-purpose"),
        StepDef("plan.user_confirm_spec", "用户确认 spec.md",
                actions=["展示 spec.md 内容给用户确认"],
                user_action=True),
        StepDef("plan.plan_B", "Plan B: 任务拆解（writing-plans）",
                actions=["kanban time start $task_id plan_B",
                         "spawn writing-plans agent",
                         "kanban time end $task_id plan_B"],
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
                    "- 不要调用任何 kanban CLI 命令\n"
                    "- 不要启动 subagent-driven-development 或任何执行流程\n\n"
                    "完成标志：$task_dir/plan/index.md 和 $task_dir/task_breakdown.json 文件存在且非空。"
                )),
        StepDef("plan.complete", "Plan 阶段完成",
                actions=["kanban time end $task_id plan",
                         "kanban guard check-artifacts $task_id plan",
                         "kanban workflow checkpoint $task_id plan",
                         "kanban workflow complete-phase $task_id"]),
    ],
    "plan_review": [
        StepDef("plan_review.spawn", "并行启动 6 维度 Plan Review agents",
                actions=["kanban workflow get-phase-agents plan_review",
                         "spawn 6 plan-reviewer agents (run_in_background=true)"],
                agent_type="general-purpose", parallel=True,
                spawn_prompt=(
                    "你是 kanban 任务 $task_id 的 Plan Review 评审员。"
                    "从你负责的维度评审 spec.md 和 plan/ 下的文件。\n\n"
                    "参考文件：$task_dir/spec.md、$task_dir/plan/index.md、$task_dir/task_breakdown.json\n\n"
                    "任务边界：\n"
                    "- 产出评审报告保存到 $report_dir/reviews/plan_review_report.json\n"
                    "- 完成后立即停止\n"
                    "- 不要调用任何 kanban CLI 命令\n"
                    "- 不要修改 spec.md 或 plan 文件\n\n"
                    "完成标志：$report_dir/reviews/plan_review_report.json 文件存在且非空。"
                )),
        StepDef("plan_review.collect", "收集评审报告",
                actions=["kanban workflow collect-plan-review $task_id"]),
        StepDef("plan_review.knowledge_cross_validate", "知识库交叉验证：验证知识引用完整性",
                actions=["kanban time start $task_id knowledge_cross_validate",
                         "spawn kanban-plan-reviewer agent 执行知识引用验证",
                         "kanban time end $task_id knowledge_cross_validate"],
                agent_type="general-purpose",
                spawn_prompt=(
                    "你是 kanban 任务 $task_id 的知识引用验证 Agent。\n"
                    "检查任务是否充分引用了知识库中的相关经验。\n\n"
                    "参考文件：\n"
                    "- $task_dir/plan/knowledge_used.json（知识检索产出）\n"
                    "- $task_dir/plan/index.md\n"
                    "- $task_dir/plan/ST-NNN_*.md（各 subtask 文件）\n"
                    "- $task_dir/spec.md\n\n"
                    "验证清单（每个维度 0-3 分）：\n"
                    "1. 知识检索完整性 (3分)：knowledge_used.json 是否存在且非空？如为空，无匹配原因是 否合理？\n"
                    "2. 引用到位率 (3分)：plan/*.md 中引用的 K-NNN 条目数是否覆盖了 knowledge_used.json 中的 high+medium 条目？\n"
                    "3. 应用合理性 (3分)：每个引用的 how_to_apply 是否在 subtask 中具体体现？是否存在形式化引用（标了但 没用）？\n\n"
                    "评分规则：\n"
                    "- 总分 = (知识检索完整性 + 引用到位率 + 应用合理性) / 9 * 10\n"
                    "- 总分 < 6.0 视为不通过，需回退到 plan.knowledge_search 重做\n"
                    "- knowledge_used.json 为空但原因合理 → 知识检索完整性给 3 分\n\n"
                    "输出：写入 $report_dir/reviews/knowledge_citation_report.json，格式：\n"
                    '{"scores": {"检索完整性": N, "引用到位率": N, "应用合理性": N},\n'
                    ' "total": N.N, "passed": true/false,\n'
                    ' "unreferenced": ["K001 已匹配但未被任何 plan 文件引用"],\n'
                    ' "formality_only": ["K003 被引用但 subtask 中未体现具体应用"],\n'
                    ' "suggestions": ["建议在 ST-002 中引用 K005 的模式"]}\n\n'
                    "任务边界：\n"
                    "- 只产出 knowledge_citation_report.json，不修改任何其他文件\n"
                    "- 完成后立即停止\n\n"
                    "完成标志：$report_dir/reviews/knowledge_citation_report.json 文件存在且非空。"
                )),
        StepDef("plan_review.check", "评分检查（不达标则重试）",
                actions=["检查 plan_review_report.json 总分 >= pass_threshold"]),
        StepDef("plan_review.complete", "Plan Review 完成",
                actions=["kanban workflow complete-phase $task_id"]),
    ],
    "qa_spec": [
        StepDef("qa_spec.spawn", "QA Agent 生成 test_spec.md",
                actions=["kanban workflow get-phase-agents qa_spec",
                         "spawn kanban-qa agent (mode=spec)"],
                agent_type="general-purpose",
                spawn_prompt=(
                    "你是 kanban 任务 $task_id 的 QA Spec 生成器。"
                    "基于 spec.md 和 plan 文件生成测试规格。\n\n"
                    "参考文件：$task_dir/spec.md、$task_dir/plan/index.md、$task_dir/task_breakdown.json\n\n"
                    "任务边界：\n"
                    "- 产出 test_spec.md 保存到 $task_dir/test_spec.md\n"
                    "- 完成后立即停止\n"
                    "- 不要调用任何 kanban CLI 命令\n"
                    "- 不要进入 spec_review 或执行阶段\n\n"
                    "完成标志：$task_dir/test_spec.md 文件存在且非空。"
                )),
        StepDef("qa_spec.complete", "QA Spec 完成",
                actions=["kanban guard check-artifacts $task_id qa_spec",
                         "kanban workflow complete-phase $task_id"]),
    ],
    "spec_review": [
        StepDef("spec_review.spawn", "Test Spec Reviewer 审核",
                actions=["kanban workflow get-phase-agents spec_review",
                         "spawn kanban-test-spec-reviewer agent"],
                agent_type="general-purpose",
                spawn_prompt=(
                    "你是 kanban 任务 $task_id 的测试规格评审员。"
                    "审核 test_spec.md 的质量和完整性。\n\n"
                    "参考文件：$task_dir/test_spec.md、$task_dir/spec.md\n\n"
                    "任务边界：\n"
                    "- 产出评审报告保存到 $report_dir/reviews/spec_review_report.json\n"
                    "- 完成后立即停止\n"
                    "- 不要调用任何 kanban CLI 命令\n"
                    "- 不要修改 test_spec.md\n\n"
                    "完成标志：$report_dir/reviews/spec_review_report.json 文件存在且非空。"
                )),
        StepDef("spec_review.check", "评分检查",
                actions=["检查 spec_review_report.json 总分 >= pass_threshold"]),
        StepDef("spec_review.user_confirm", "用户确认测试用例",
                actions=["展示 review 摘要 + test_spec.md，approve / revise"],
                user_action=True),
        StepDef("spec_review.complete", "Spec Review 完成",
                actions=["kanban workflow complete-phase $task_id"]),
    ],
    "execute": [
        StepDef("execute.pitfall_check", "踩坑预警：执行前搜索相关踩坑记录",
                actions=["kanban knowledge similar --tags \"$(kanban knowledge match '$task_title' --json | python3 -c 'import sys,json;print(\\\",\\\".join(json.load(sys.stdin)[\\\"data\\\"][\\\"domains\\\"][:3]))')\" 2>/dev/null || kanban knowledge hybrid \"$task_title 踩坑 注意事项 错误\" --json",
                         "检查是否有与当前任务相关的已知踩坑记录",
                         "将匹配到的踩坑写入 plan/pitfall_warnings.md"],
                agent_type="general-purpose"),
        StepDef("execute.tech_review", "技术方案评审：多方案时模型推理比较+用户确认",
                actions=["kanban knowledge hybrid \"$task_title 技术方案 实现 approach best-practice\" --json --summary-only",
                         "对搜索结果中 category 为 最佳实践/架构/优化 的条目进一步分析",
                         "如有相关条目，用 kanban knowledge get <id> --json 取完整内容",
                         "将条目归类为不同技术方案（不同实现路径或技术选型）",
                         "如果只有 0-1 个方案：写入 $task_dir/tech_choice.md 标记方案唯一，跳过确认",
                         "如果有 2+ 个方案：深入分析每个方案的优缺点、适用场景、与当前任务的匹配度",
                         "使用 AskUserQuestion 向用户展示方案对比和推荐，等待用户选择",
                         "将分析过程和用户选择写入 $task_dir/tech_choice.md"],
                interactive=True),
        StepDef("execute.spawn", "为每个 subtask 准备独立执行步骤",
                actions=["读取 task_breakdown.json 中的 subtask 列表",
                         "为每个 subtask 动态创建 execute.exec_ST-NNN 步骤"]),
        StepDef("execute.verify", "验证执行产物",
                actions=["kanban guard check-artifacts $task_id execute"]),
        StepDef("execute.commit", "Git 提交执行产物",
                actions=["kanban workflow checkpoint $task_id execute"]),
        StepDef("execute.complete", "Execute 完成",
                actions=["kanban workflow complete-phase $task_id"]),
    ],
    "evaluate": [
        StepDef("evaluate.spawn", "并行启动评估 agents",
                actions=["kanban workflow get-phase-agents evaluate",
                         "spawn 4 角色 agents (run_in_background=true)"],
                agent_type="general-purpose", parallel=True,
                spawn_prompt=(
                    "你是 kanban 任务 $task_id 的评估员。"
                    "从你负责的角色（code_reviewer/qa/product_reviewer）评估代码质量。\n\n"
                    "参考文件：$task_dir/ 下的所有实现代码和测试\n\n"
                    "任务边界：\n"
                    "- 产出评审报告保存到 $report_dir/reviews/{role}_report.json\n"
                    "- 完成后立即停止\n"
                    "- 不要调用任何 kanban CLI 命令\n"
                    "- 不要修改任何代码文件\n\n"
                    "完成标志：$report_dir/reviews/{role}_report.json 文件存在且非空。"
                )),
        StepDef("evaluate.e2e_run", "E2E 测试执行（如项目配置了 E2E）",
                actions=["检查 $task_dir/test_spec.md 是否包含 E2E 用例",
                         "如有 E2E 用例则执行浏览器测试",
                         "无 E2E 用例则跳过此步骤"],
                agent_type="general-purpose",
                spawn_prompt=(
                    "你是 kanban 任务 $task_id 的 E2E 测试执行器。\n"
                    "在浏览器中实际验证功能是否正常工作。\n\n"
                    "参考文件：\n"
                    "- $task_dir/test_spec.md（测试用例）\n"
                    "- $task_dir/ 下的实现代码\n\n"
                    "任务边界：\n"
                    "- 启动浏览器执行 E2E 场景\n"
                    "- 产出 E2E 测试报告保存到 $report_dir/reviews/e2e_report.json\n"
                    "- 如无 E2E 配置或浏览器不可用，产出说明性报告并完成\n"
                    "- 完成后立即停止\n"
                    "- 不要调用任何 kanban CLI 命令\n\n"
                    "完成标志：$report_dir/reviews/e2e_report.json 文件存在且非空。"
                )),
        StepDef("evaluate.collect_scores", "收集评分（自动同步）",
                actions=["评分已由 complete-phase 自动同步"]),
        StepDef("evaluate.check_score", "自迭代决策（禁止询问用户）",
                actions=["kanban workflow self-improve-check $task_id",
                         "all_pass → Retrospective",
                         "hot(>=7.0) → 自动回 Execute",
                         "full(<7.0) → 自动回 Plan"]),
        StepDef("evaluate.commit", "Git 提交评估结果",
                actions=["kanban workflow checkpoint $task_id evaluate"]),
        StepDef("evaluate.complete", "Evaluate 完成",
                actions=["kanban workflow complete-phase $task_id"]),
    ],
    "retrospective": [
        StepDef("retrospective.spawn", "并行启动复盘 agents",
                actions=["kanban workflow get-phase-agents retrospective",
                         "spawn 3 agents: retrospective/acceptance/knowledge (parallel)"],
                parallel=True,
                spawn_prompt=(
                    "你是 kanban 任务 $task_id 的复盘 agent。"
                    "完成复盘总结、验收文档和知识提取。\n\n"
                    "参考文件：$task_dir/ 下的所有产物\n\n"
                    "任务边界：\n"
                    "- 产出 retrospective.md 和 acceptance.md 保存到 $task_dir/\n"
                    "- 产出 knowledge_extracted.json 保存到 $report_dir/\n"
                    "- 完成后立即停止\n"
                    "- 不要调用任何 kanban CLI 命令\n\n"
                    "完成标志：$task_dir/retrospective.md 和 $task_dir/acceptance.md 文件存在。"
                )),
        StepDef("retrospective.audit_realtime_knowledge", "审计 execute 阶段实时写入的知识条目",
                actions=["检查 source.type=executor_realtime 且 source.task_id=$task_id 的条目",
                         "确认条目的通用性（非项目特化）和准确性（无误解）",
                         "标记低质量条目为 deprecated 或删除"],
                agent_type="general-purpose"),
        StepDef("retrospective.knowledge_import", "导入提取的知识",
                actions=["complete-phase 自动导入 knowledge_extracted.json"]),
        StepDef("retrospective.complete", "Retrospective 完成",
                actions=["kanban guard check-artifacts $task_id retrospective",
                         "kanban workflow checkpoint $task_id retrospective",
                         "kanban workflow complete-phase $task_id"]),
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
        StepDef("archive.merge", "合并 worktree 代码",
                actions=["kanban worktree merge $task_id"]),
        StepDef("archive.guard", "归档 Guards — inbox + subtask + stray",
                actions=["kanban guard check-inbox $task_id",
                         "kanban guard check-pending-subtasks $task_id",
                         "kanban guard check-archive-stray $task_id"]),
        StepDef("archive.cleanup", "清理 worktree",
                actions=["kanban worktree remove $task_id",
                         "kanban clean $task_id"]),
    ],
}
