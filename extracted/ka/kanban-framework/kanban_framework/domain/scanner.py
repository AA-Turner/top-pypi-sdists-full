"""
Project Scanner — 在 kanban init 时分析项目已有 agent/skills/基础设施。

检测维度:
1. Agent 冲突检测 — 项目自有的 agent 与 kanban 默认 agent 合并建议
2. Skills 关联分析 — 项目已有的 skills
3. 语言/框架基建 — Python/JS/TS/Go 等项目所需工具
4. 领域特定基建 — 游戏/Web/CLI 等领域所需工具
"""

from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path

# Re-exports for backward compatibility
from kanban_framework.domain.scanner_detection import (  # noqa: F401
    detect_agent_conflicts as _detect_agent_conflicts,
    detect_language as _detect_language,
    detect_skills as _detect_skills,
    detect_superpowers_skill_gaps as _detect_superpowers_skill_gaps,
    detect_testing_skills as _detect_testing_skills,
)
from kanban_framework.domain.scanner_infra import (  # noqa: F401
    _check_python_infra,
    detect_infrastructure_gaps as _detect_infrastructure_gaps,
)
from kanban_framework.domain.scanner_recommend import (  # noqa: F401
    detect_e2e_recommendation,
    generate_default_test_profile,
    generate_recommendations as _generate_recommendations,
)

KANBAN_DEFAULT_AGENTS = [
    "kanban-planner",
    "kanban-executor",
    "kanban-code-reviewer",
    "kanban-product-reviewer",
    "kanban-qa",
    "kanban-researcher",
    "kanban-knowledge-manager",
    "kanban-plan-reviewer",
    "kanban-test-spec-reviewer",
]

KANBAN_SKILL_NAME = "kanban"

REQUIRED_SUPERPOWERS_SKILLS = [
    "superpowers:brainstorming",
    "superpowers:writing-plans",
    "superpowers:test-driven-development",
]


@dataclass
class AgentConflict:
    role: str
    kanban_agent: str
    project_agent_file: str
    action: str  # "merge" | "replace" | "keep_both"
    description: str


@dataclass
class SkillGap:
    skill_name: str
    required_by: str  # which FSM phase depends on it
    suggestion: str


@dataclass
class InfrastructureGap:
    category: str  # "language" | "domain" | "testing" | "linting"
    tool: str
    config_file: str
    detected: bool
    suggestion: str


@dataclass
class ScanReport:
    project_root: str
    language: str = "unknown"
    has_kanban: bool = False
    agent_conflicts: list[AgentConflict] = field(default_factory=list)
    existing_skills: list[str] = field(default_factory=list)
    testing_skills: list[str] = field(default_factory=list)
    infrastructure_gaps: list[InfrastructureGap] = field(default_factory=list)
    skill_gaps: list[SkillGap] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)


def scan_project(root: Path) -> ScanReport:
    report = ScanReport(project_root=str(root))

    report.language = _detect_language(root)
    report.has_kanban = (root / ".kanban").exists()
    report.agent_conflicts = _detect_agent_conflicts(root)
    report.existing_skills = _detect_skills(root)
    report.testing_skills = _detect_testing_skills(root)
    report.infrastructure_gaps = _detect_infrastructure_gaps(root, report.language)
    report.skill_gaps = _detect_superpowers_skill_gaps(root)
    report.recommendations = _generate_recommendations(report)

    return report
