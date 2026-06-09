"""Lightweight mode step definitions — 14 steps with full KB constraint chain."""
from __future__ import annotations
from kanban_framework.domain.steps_types import StepDef

LIGHTWEIGHT_STEPS: dict[str, list[StepDef]] = {
    "plan": [
        StepDef("plan.knowledge_search", "知识库检索 — 强制产出 knowledge_used.json", agent_type="general-purpose", spawn_prompt="""\
你是 kanban 任务 $task_id 的知识检索 Agent（轻量模式）。
任务目标：从知识库中找到与当前任务相关的所有知识条目，并产出引用清单。

参考文件：$task_dir/task.json（任务标题和描述）
如果 task.json 中有 biz_tag 字段，所有知识库查询命令必须带 --biz $biz_tag 参数

执行步骤：
1. 读取 task.json 获取任务标题和描述
2. kanban knowledge hybrid "<任务标题+描述关键词>" --biz $biz_tag --json --summary-only
3. 对搜索结果逐一判断相关性，筛选出 medium/high 的条目
4. 如无匹配，kanban knowledge search "<关键词>" --biz $biz_tag --intent experience_reuse --json --summary-only
5. 仍无匹配则记录原因（如：全新领域、无相关经验）

$knowledge_protocol

输出：写入 $task_dir/plan/knowledge_used.json
完成标志：$task_dir/plan/knowledge_used.json 文件存在且非空。""", use_subagent=True),
        StepDef("plan.plan_A", "Plan: 需求澄清（brainstorming）", actions=["使用 Skill tool 调用 superpowers:brainstorming", "产出 spec.md 保存到 $task_dir/spec.md"], interactive=True),
        StepDef("plan.inject_constraints", "知识库约束注入 — 将 KB 规范/反模式/踩坑写入 spec.md 验收标准", agent_type="general-purpose", spawn_prompt="""\
你是 kanban 任务 $task_id 的约束注入 Agent。
目标：将知识库中的项目规范、反模式、已知踩坑明确写入 spec.md，使其成为硬性验收标准。

参考文件（必须读取）：
1. $task_dir/plan/knowledge_used.json — 知识库引用清单
2. $task_dir/spec.md — 当前需求规格（只读，不修改原有内容）

执行步骤：
1. 读取 knowledge_used.json，提取所有 high/medium 条目
2. 对每个条目，用 kanban knowledge get <id> --json 读取完整内容（code_example、tags、severity）
3. 按类别整理：
   - 规范约束（category=架构/最佳实践）：必须遵守的编码规范
   - 反模式/踩坑（category=踩坑/反模式）：禁止出现的错误模式
   - 工具/接口（category=工具/接口）：必须使用的 API 或工具
4. 追加到 spec.md 末尾，格式：

   ## 知识库约束（自动注入，请遵守）

   ### 必须遵守的规范
   - [K001] <标题>：<约束说明>
     - 代码证据：<code_example 中的关键模式>

   ### 禁止出现的反模式
   - [K002] <标题>：<为什么是反模式>
     - 错误示例：<code_example 中的错误模式>
     - 正确做法：<替代方案>

   ### 验收检查清单
   - [ ] spec.md 原始需求与 KB 约束无冲突
   - [ ] 所有必须遵守的规范已列出
   - [ ] 所有已知踩坑已标记为禁止

任务边界：
- 只追加内容到 spec.md 末尾，不修改原有内容
- 如 knowledge_used.json 为空，在 spec.md 末尾注明「本轮无 KB 约束」
- 完成后立即停止，不要调用任何 kanban CLI 命令

完成标志：spec.md 中包含「## 知识库约束（自动注入，请遵守）」章节。""", after=["plan.plan_A"], use_subagent=True),
        StepDef("plan.plan_B", "Plan: 任务拆解（writing-plans）", agent_type="general-purpose", spawn_prompt="""\
你是 kanban 任务 $task_id 的 writing-plans 子任务。使用 superpowers:writing-plans 技能完成任务拆解。

参考文件：
- $task_dir/spec.md（已由 brainstorming 产出）
- $task_dir/plan/knowledge_used.json（知识库引用清单，必须参考）

重要约束：
- 每个 subtask 的 plan/ST-NNN_*.md 必须在开头引用相关知识条目：
  "知识库参考: [K001] xxx 模式 — 避免 xx 问题"
- 如 knowledge_used.json 为空或无匹配，请在 plan/index.md 中说明原因

任务边界：
- 产出 task_breakdown.json 保存到 $task_dir/
- 产出 plan/index.md 保存到 $task_dir/plan/
- 不要修改代码
- 不要调用任何 kanban CLI 命令

完成标志：$task_dir/plan/index.md 和 $task_dir/task_breakdown.json 文件存在且非空。""", use_subagent=True),
    ],
    "execute": [
        StepDef("execute.spawn", "执行编码（轻量模式）", agent_type="general-purpose", spawn_prompt="""\
你是 kanban 任务 $task_id 的执行 Agent（轻量模式）。
根据任务描述和 plan 直接执行代码修改，无需全量评审流程。

$knowledge_protocol

参考文件（按优先级，必须全部读取）：
1. $task_dir/spec.md — 需求规格 +「知识库约束」章节（硬性验收标准，必须逐条满足）
2. $task_dir/plan/knowledge_used.json — 知识库引用清单
3. $task_dir/task_breakdown.json — 任务拆解方案
4. $task_dir/plan/index.md — 执行计划

编码约束（硬性要求，违反视为任务失败）：
- spec.md 中「知识库约束」章节的每一条规范必须落实
- spec.md 中「禁止出现的反模式」章节的每一条必须回避
- 代码风格、命名、架构必须与 knowledge_used.json 中引用的模式一致
- 如 knowledge_used.json 中有 code_example，优先复用而非重写

遇到不确定的情况时（动态查询）：
- kanban knowledge search "<问题关键词>" --biz $biz_tag --intent pitfall_check --json --summary-only
- kanban knowledge search "<技术关键词> 最佳实践 规范" --biz $biz_tag --json --summary-only

任务边界：
- 编写代码实现功能
- 产出 execution_summary.md 保存到 $task_dir/
- 在 execution_summary.md 中必须包含「KB 约束落实清单」章节，逐条标注每个约束的落实情况
- 完成后立即停止
- 不要调用任何 kanban CLI 命令
- 不要编写测试代码（测试由下一个步骤独立负责）

代码质量检查：
- 编码完成后运行 pylint 检查代码规范：pylint --output-format=text $output_dir/ 2>&1 | head -50
- 修复所有 Error 级别问题 (E0001-E9999)，Warning 级别 (W0001-W9999) 尽量修复

完成标志：$task_dir/execution_summary.md 文件存在且非空。""", type="checkpoint", guard={"external_tools": [{"name": "pylint", "command": "pylint --output-format=text ${files}", "scope": "changed", "fail_pattern": ": E\\d+:", "fail_on_exit_code": False, "severity": "error", "warn_pattern": ": [WCR]\\d+:"}], "guard_prompt": "\u786e\u8ba4 pylint \u68c0\u67e5\u901a\u8fc7\uff08Error \u7ea7\u522b\u4e3a 0\uff09\uff0c\u4ee3\u7801\u53ef\u6b63\u5e38\u8fd0\u884c"}, use_subagent=True),
        StepDef("execute.test", "编写并运行 pytest 单元测试", agent_type="general-purpose", spawn_prompt="""\
你是 kanban 任务 $task_id 的测试 Agent。
负责为上一步实现的代码编写 pytest 单元测试并运行验证。

参考文件（必须全部读取）：
1. $task_dir/spec.md — 需求规格 +「知识库约束」章节（测试必须覆盖所有验收标准）
2. $task_dir/plan/knowledge_used.json — 知识库引用清单
3. $task_dir/execution_summary.md — 已实现的代码变更 + KB 约束落实清单

测试编写要求（硬性）：
- 先查询知识库：kanban knowledge search "<项目关键词> 测试 规范 踩坑" --biz $biz_tag --intent pitfall_check --json --summary-only
- 测试必须覆盖 spec.md 中「知识库约束」章节的每一条验收标准
- 测试必须验证「禁止出现的反模式」中的模式没有出现在代码中
- 只为本轮任务涉及的文件编写测试
- 测试文件放在项目约定的测试目录下（如 test/、tests/），命名遵循 test_*.py 或 *_test.py
- 如果 $task_dir/test_spec.md 存在，按其中的验收规范编写测试
- 覆盖正常路径和关键边界 case
- 先运行 pylint 检查测试代码规范，再运行 pytest 确认所有测试通过，如有失败则修复

遇到不确定的测试策略时（动态查询）：
- kanban knowledge search "<测试关键词> 测试 验证" --biz $biz_tag --json --summary-only

任务边界：
- 只编写和修复测试代码，不要修改业务代码
- 完成后立即停止
- 不要调用任何 kanban CLI 命令

完成标志：pytest 全部通过（guard 会自动验证）。""", type="checkpoint", guard={"checks": ["test_files"], "external_tools": [{"name": "pytest", "command": "pytest --tb=short -q", "scope": "worktree", "fail_on_exit_code": True, "severity": "error"}, {"name": "pylint", "command": "pylint --output-format=text ${files}", "scope": "changed", "fail_pattern": ": E\\d+:", "fail_on_exit_code": False, "severity": "error", "warn_pattern": ": [WCR]\\d+:"}], "guard_prompt": "\u786e\u8ba4 pytest \u5168\u90e8\u901a\u8fc7\uff0cpylint \u6d4b\u8bd5\u4ee3\u7801\u68c0\u67e5\u901a\u8fc7\uff08Error \u7ea7\u522b\u4e3a 0\uff09"}, use_subagent=True),
        StepDef("execute.verify", "验证执行产物", actions=["kanban guard check-artifacts $task_id execute"], use_subagent=False),
    ],
    "evaluate": [
        StepDef("evaluate.spawn_review", "通用审核 (lightweight)", agent_type="general-purpose", spawn_prompt="""\
你是 kanban 任务 $task_id 的轻量质量审核员。
不要求测试覆盖率或测试用例（轻量模式无 qa_spec），聚焦实际产出质量。

审核维度（逐项检查，产出报告中每项给出结论 + 证据）：
1. 需求符合性 — 对照 $task_dir/spec.md，检查实现是否覆盖了所有功能点
2. KB 约束落实（关键）— 读取 $task_dir/spec.md 中「知识库约束」章节：
   - 逐条检查「必须遵守的规范」是否已在代码中落实
   - 逐条检查「禁止出现的反模式」是否已回避
   - 检查 execution_summary.md 中的「KB 约束落实清单」是否与代码一致
   - 如发现未落实的约束，报告为 blocking issue
3. 知识库对照 — 读取 $task_dir/plan/knowledge_used.json：
   - 检查实现是否应用了 high/medium 条目的建议
   - 搜索知识库中相关踩坑，验证代码是否避开了已知问题
   - 如发现未覆盖的新模式/踩坑，kanban knowledge add --biz $biz_tag 补充写入
4. 功能合理性 — 代码逻辑是否清晰、有没有明显 bug（人工审读即可）
5. 代码质量 — 命名是否合理、结构是否清晰、有无硬编码的安全问题

参考文件：$task_dir/spec.md、$task_dir/plan/knowledge_used.json、$task_dir/execution_summary.md、$task_dir/ 下的实现代码

任务边界：
- 产出 $report_dir/reviews/review_report.json
- 报告中必须包含「KB 约束落实审核」章节（逐条 audit 每个 KB 约束的落实情况，给出 pass/fail）
- 完成后立即停止，不要进入后续阶段

完成标志：$report_dir/reviews/review_report.json 文件存在且非空。""", use_subagent=True),
        StepDef("evaluate.capture_knowledge", "知识提取 — 从任务产物中提取结构化知识条目（模式/踩坑/决策）", agent_type="general-purpose", spawn_prompt="""\
你是 kanban 任务 $task_id 的知识提取 Agent。
目标：从本轮任务的所有产物中系统化提取可复用的知识条目。

参考文件（必须全部读取）：
1. $task_dir/execution_summary.md — 执行摘要 + KB 约束落实清单
2. $task_dir/spec.md — 需求规格（含知识库约束章节）
3. $task_dir/plan/knowledge_used.json — 本轮引用的知识条目
4. $task_dir/plan/index.md — 执行计划

提取步骤：
1. 识别新增模式（execution_summary.md 中的新代码模式、架构决策）
2. 识别新踩坑（执行中遇到的坑，knowledge_used.json 中未覆盖的）
3. 识别决策记录（为什么选方案 A 而非方案 B）
4. 对每个发现，判断是否值得写入知识库：
   - 可复用的模式/规范 → category=最佳实践
   - 避免重复的错误 → category=踩坑
   - 关键架构决策 → category=架构
   - 通用工具/接口 → category=工具
5. 用 kanban knowledge add 写入，status=pending（走人工审核）：
   kanban knowledge add --domain <推断领域> --category <类别> \\
       --title "<简明标题>" --content "<详细内容>" \\
       --tags "<逗号分隔标签>" --status pending \\
       --severity <high|medium|low> \\
       --biz $biz_tag

质量要求：
- 每条的 content 必须包含具体代码示例或错误信息，不能泛泛而谈
- 标题不超过 40 字，清晰描述模式/问题
- 如本轮无新增知识（所有发现已被 KB 覆盖），输出「本轮无新增知识」
- 如 knowledge_used.json 为空，仍可提取 spec.md 中隐含的规范作为新条目

任务边界：
- 只提取和写入，不修改业务代码
- 所有条目 status=pending，由人工审核后 activate
- 完成后立即停止

$knowledge_protocol

完成标志：如有新增条目，kanban knowledge list --status pending 能看到本轮新增的条目。""", after=["evaluate.spawn_review"], use_subagent=True),
        StepDef("evaluate.collect_issues", "收集框架问题 — 扫描 framework_issues.md 并整理为可提交的 GitHub issue 格式", agent_type="general-purpose", spawn_prompt="""\
你是 kanban 任务 $task_id 的框架问题收集 Agent。
目标：扫描任务执行过程中记录的框架问题，整理为结构化的 issue 草稿。

参考文件：
- $task_dir/framework_issues.md — execute 阶段记录的原始问题（可能存在）
- $task_dir/execution_summary.md — 执行摘要
- $task_dir/spec.md — 需求规格

执行步骤：
1. 检查 $task_dir/framework_issues.md 是否存在：
   - 如果存在，读取并整理
   - 如果不存在，扫描以下来源寻找框架问题线索：
     a. $task_dir/execution_summary.md 中的异常/错误描述
     b. 本迭代中的 guard 错误（如 artifacts missing）
     c. step 执行中的阻塞情况
2. 对每个发现的问题，按以下格式整理到 $task_dir/issues.md：

   ## [Issue] <问题标题>
   **严重程度**: high/medium/low
   **发现阶段**: <plan/execute/evaluate>
   **现象**: <描述实际问题>
   **影响**: <对任务执行的影响>
   **复现**: <如何复现>
   **建议**: <修复建议>
   **关联**: <相关 K-NNN 条目或 issue>

3. 对每个问题判断是否值得提交 GitHub issue：
   - 框架 bug（CLI 报错、workflow 行为异常）→ 建议提交
   - Agent prompt 问题（指令不清、矛盾）→ 建议提交
   - 一次性偶发问题 → 标记为 skip
4. 产出一份汇总：issues.md 顶部添加摘要章节

   ## 汇总
   - 发现问题: N 个
   - 建议提交 GitHub issue: M 个
   - 跳过: K 个（原因）

任务边界：
- 只收集和整理，不提交任何 issue（由用户决定是否提交）
- 如无任何框架问题，issues.md 仍产出但标注「本轮未发现框架问题」
- 完成后立即停止

完成标志：$task_dir/issues.md 文件存在且非空。""", after=["evaluate.spawn_review"], use_subagent=True),
    ],
    "user_decision": [
        StepDef("user_decision.present", "展示决策依据 — 汇总本轮执行全景供用户决策", actions=["📋 变更摘要（execution_summary.md 核心内容）", "🧪 测试结果（pytest pass/fail + 覆盖率）", "🔍 KB 约束落实（review_report.json 中 pass/fail 逐条结论）", "📝 新增知识条目（capture_knowledge 提取的 pending 条目清单）", "🐛 框架问题（issues.md 中建议提交的问题数量）", "━━━━━━━━━━━━━━━━━━━━━━━━━━━", "请用户选择: approve_and_archive / restart_from_execute / abort"], user_action=True),
        StepDef("user_decision.wait", "等待用户决策", actions=["kanban decide $task_id --action <approve_and_archive|abort|restart>"], user_action=True),
    ],
    "archive": [
        StepDef("archive.guard", "归档 Guards — inbox + subtask + stray", actions=["kanban guard check-inbox $task_id", "kanban guard check-subtask-cleanup $task_id", "kanban guard check-stray-artifacts $task_id"], use_subagent=False),
        StepDef("archive.audit_kb", "知识库审计 — 归档时自动检查 KB 健康状态", actions=["kanban knowledge audit", "如有 zombie>5 或低质量>5 或领域失衡，输出 warning 提示 curator agent 介入"], use_subagent=False),
    ],
}