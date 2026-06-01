"""Scanner detection — language, agents, skills, and superpowers gap detection."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


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
    action: str
    description: str


@dataclass
class SkillGap:
    skill_name: str
    required_by: str
    suggestion: str


def detect_language(root: Path) -> str:
    indicators = {
        "python": ["pyproject.toml", "setup.py", "setup.cfg", "requirements.txt", "Pipfile"],
        "typescript": ["tsconfig.json"],
        "javascript": ["package.json", "package-lock.json", "yarn.lock"],
        "go": ["go.mod", "go.sum"],
        "rust": ["Cargo.toml"],
    }
    scores = {}
    for lang, files in indicators.items():
        scores[lang] = sum(1 for f in files if (root / f).exists())

    if any(scores.values()):
        return max(scores, key=scores.get)  # type: ignore[arg-type]

    for f in root.iterdir():
        if f.is_file() and f.suffix in (".py",):
            return "python"
        if f.is_file() and f.suffix in (".js", ".jsx"):
            return "javascript"
        if f.is_file() and f.suffix in (".ts", ".tsx"):
            return "typescript"
        if f.is_file() and f.suffix == ".go":
            return "go"
    return "unknown"


def detect_agent_conflicts(root: Path) -> list[AgentConflict]:
    agents_dir = root / ".claude" / "agents"
    if not agents_dir.exists():
        return []

    conflicts = []
    kanban_role_map = {
        "planner": "kanban-planner",
        "executor": "kanban-executor",
        "code-reviewer": "kanban-code-reviewer",
        "product-reviewer": "kanban-product-reviewer",
        "qa": "kanban-qa",
        "researcher": "kanban-researcher",
        "knowledge-manager": "kanban-knowledge-manager",
    }

    for agent_file in agents_dir.glob("*.md"):
        if agent_file.is_symlink():
            try:
                target = agent_file.resolve()
                target_parts = [p.lower() for p in target.parts]
                if "kanban" in target_parts and "agents" in target_parts:
                    continue
            except OSError:
                continue

        name = agent_file.stem
        if name.startswith("kanban-"):
            continue

        if name in kanban_role_map:
            conflicts.append(AgentConflict(
                role=name,
                kanban_agent=kanban_role_map[name],
                project_agent_file=str(agent_file.relative_to(root)),
                action="merge",
                description=f"项目已有 {name} agent，建议与 kanban 默认 {kanban_role_map[name]} 合并",
            ))

    return conflicts


def detect_skills(root: Path) -> list[str]:
    skills_dir = root / ".claude" / "skills"
    if not skills_dir.exists():
        return []

    skills = []
    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir() and skill_dir.name != KANBAN_SKILL_NAME:
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                skills.append(skill_dir.name)
    return sorted(skills)


def detect_testing_skills(root: Path) -> list[str]:
    """Detect testing-related skills that could integrate with kanban workflow."""
    skills_dir = root / ".claude" / "skills"
    if not skills_dir.exists():
        return []
    test_keywords = ["test", "pytest", "unittest", "tdd", "spec", "qa", "coverage", "mock"]
    testing = []
    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir() and skill_dir.name != KANBAN_SKILL_NAME:
            name_lower = skill_dir.name.lower()
            if any(kw in name_lower for kw in test_keywords):
                testing.append(skill_dir.name)
    return sorted(testing)


def detect_superpowers_skill_gaps(root: Path) -> list[SkillGap]:
    """Detect missing superpowers skills required by kanban FSM."""
    gaps: list[SkillGap] = []
    superpowers_dir = root / ".superpowers"
    skills_dir = root / ".claude" / "skills"
    home = Path.home()
    plugins_dir = home / ".claude" / "plugins"

    skill_phase_map = {
        "superpowers:brainstorming": "Plan Step A (需求澄清)",
        "superpowers:writing-plans": "Plan Step B (实施计划)",
        "superpowers:test-driven-development": "Execute (TDD 循环)",
    }

    for skill_name in REQUIRED_SUPERPOWERS_SKILLS:
        found = False
        for search_dir in (superpowers_dir, skills_dir, plugins_dir):
            if not search_dir.exists():
                continue
            for sf in search_dir.glob("**/SKILL.md"):
                try:
                    content = sf.read_text(encoding="utf-8")
                    short_name = skill_name.split(":")[-1] if ":" in skill_name else skill_name
                    if f"name: {skill_name}" in content or f"name: {short_name}" in content:
                        found = True
                        break
                except OSError:
                    pass
            if found:
                break

        if not found:
            parts = skill_name.split(":")
            skill_short = parts[-1] if len(parts) > 1 else skill_name
            gaps.append(SkillGap(
                skill_name=skill_name,
                required_by=skill_phase_map.get(skill_name, "unknown"),
                suggestion=(
                    f"缺少 {skill_name}（用于 {skill_phase_map.get(skill_name, 'FSM 流程')}）。"
                    f"kanban init 会自动安装，或手动执行: "
                    f"npx skills add obra/superpowers -s {skill_short} -a claude-code -y"
                ),
            ))
    return gaps
