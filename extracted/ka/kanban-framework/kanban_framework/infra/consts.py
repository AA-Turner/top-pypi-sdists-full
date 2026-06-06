from __future__ import annotations
from enum import IntEnum

# Embedded workflow.json template — eliminates file dependency for pip install.
# synced from kanban/templates/workflow.json
# fmt: off
DEFAULT_WORKFLOW = r"""{"_comment": "Agent 条目支持 agent_file 字段指向自定义 Agent 文件。不填则使用 agents/kanban-{role}.md", "phases": [{"id": "plan", "name": "规划阶段", "agents": [{"role": "planner", "required": true}, {"role": "researcher", "required": false, "trigger_condition": {"keywords": ["调研", "选型", "对比", "analysis", "research", "技术选型", "竞品"], "match_field": "description"}}], "required_artifacts": ["spec.md", "plan/index.md", "task_breakdown.json"], "required_checks": ["worktree_exists", "framework_check"], "exit_condition": "all_artifacts_present AND all_checks_pass", "quality_gate": {"enabled": true, "pass_threshold": 8.5, "max_rounds": 3, "dimensions": [{"id": "requirement_clarity", "name": "需求清晰度", "description": "检查 spec.md 是否包含功能需求、非功能需求、验收标准、模块设计", "weight": 0.25}, {"id": "technical_feasibility", "name": "技术可行性", "description": "检查技术约束和 estimated_files 是否具体", "weight": 0.25}, {"id": "task_decomposition", "name": "任务拆解合理性", "description": "检查 subtask 数量、字段完整性、依赖关系", "weight": 0.25}, {"id": "acceptance_criteria", "name": "验收标准完整性", "description": "检查验收标准是否可验证", "weight": 0.25}]}}, {"id": "plan_review", "name": "Plan 评审阶段", "agents": [{"role": "requirement_clarity", "required": true, "parallel": true, "agent_type": "kanban-plan-reviewer"}, {"role": "technical_feasibility", "required": true, "parallel": true, "agent_type": "kanban-plan-reviewer"}, {"role": "task_decomposition", "required": true, "parallel": true, "agent_type": "kanban-plan-reviewer"}, {"role": "acceptance_criteria", "required": true, "parallel": true, "agent_type": "kanban-plan-reviewer"}, {"role": "research_completeness", "required": false, "parallel": true, "agent_type": "kanban-plan-reviewer"}, {"role": "parallel_safety", "required": true, "parallel": true, "agent_type": "kanban-plan-reviewer"}], "required_artifacts": ["plan_review_report.json"], "quality_gate": {"dimensions": [{"id": "requirement_clarity", "weight": 0.2}, {"id": "technical_feasibility", "weight": 0.2}, {"id": "task_decomposition", "weight": 0.2}, {"id": "acceptance_criteria", "weight": 0.2}, {"id": "research_completeness", "weight": 0.0}, {"id": "parallel_safety", "weight": 0.2}], "pass_threshold": 8.5, "max_rounds": 3}, "exit_condition": "all_required_roles_scored"}, {"id": "qa_spec", "name": "QA 测试规格阶段", "agents": [{"role": "qa", "required": true, "agent_type": "kanban-qa", "mode": "spec"}]}, {"id": "spec_review", "name": "测试规格评审阶段", "agents": [{"role": "test_spec_reviewer", "required": true, "agent_type": "kanban-test-spec-reviewer"}], "quality_gate": {"dimensions": [], "pass_threshold": 8.5, "max_rounds": 3}, "exit_condition": "all_required_roles_scored"}, {"id": "execute", "name": "执行阶段", "agents": [{"role": "executor", "required": true}], "required_artifacts": ["execution_summary.md", "execution_pitfalls.md", "execution_decisions.md"], "required_checks": ["tests_run"], "exit_condition": "all_artifacts_present AND all_checks_pass"}, {"id": "evaluate", "name": "评估阶段", "agents": [{"role": "code_reviewer", "required": true}, {"role": "qa", "required": true}, {"role": "product_reviewer", "required": true}], "roles": ["code_reviewer", "qa", "product_reviewer"], "pass_threshold": 9.0, "report_required_fields": ["score", "improvements", "risks"], "exit_condition": "all_roles_scored"}, {"id": "retrospective", "name": "迭代复盘", "description": "对当前迭代进行复盘总结，提取经验教训", "agents": [{"role": "retrospective_writer", "required": true, "parallel": true, "agent_type": "kanban-knowledge-manager"}, {"role": "acceptance_writer", "required": true, "parallel": true, "agent_type": "kanban-knowledge-manager"}, {"role": "knowledge_extractor", "required": true, "parallel": true, "agent_type": "kanban-knowledge-manager"}], "required_artifacts": ["retrospective.md", "acceptance.md"], "quality_gate": {"dimensions": [], "pass_threshold": 0}, "exit_condition": "all_artifacts_present"}, {"id": "archive", "name": "归档阶段", "agents": [], "required_artifacts": ["archive_summary.md"], "exit_condition": "all_artifacts_present"}], "self_improve": {"max_iterations": 6, "exit_all_pass": true, "default_restart_from": "plan", "hot_iteration": {"trigger": "score >= 7.0 AND no_architecture_issues AND plan_artifacts_still_valid", "restart_from": "execute", "guard_check": "previous_plan_artifacts_exist_and_not_expired"}, "full_iteration": {"trigger": "DEFAULT", "restart_from": "plan"}}, "user_decision": {"trigger": "all_pass OR max_iterations_reached", "prerequisite_phase": "retrospective", "options": ["approve_and_archive", "restart_from_plan", "restart_from_execute", "abort"]}}"""
# fmt: on

class _Consts:
    PASS_THRESHOLD: float = 8.0
    HOT_ITERATION_MIN_SCORE: float = 7.0
    MAX_ITERATIONS: int = 6
    TASK_ID_PREFIX: str = "TASK-"
    KNOWLEDGE_LOG: str = "knowledge-log.md"  # legacy; new system uses knowledge/
    KNOWLEDGE_DIR: str = "knowledge"
    OUTPUT_DIR_DEFAULT: str = "src"
    DEFAULT_MODE: str = "lightweight"
    DEFAULT_EMBEDDING_MODEL: str = "BAAI/bge-small-zh-v1.5"


Consts = _Consts()


class ExitCode(IntEnum):
    SUCCESS = 0
    GUARD_FAILED = 1
    MISSING_ARTIFACT = 2
    TASK_NOT_FOUND = 3
