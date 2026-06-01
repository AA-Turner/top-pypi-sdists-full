"""Scanner recommendations — test profile generation and recommendation logic."""
from __future__ import annotations

import fnmatch
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class InfrastructureGap:
    category: str
    tool: str
    config_file: str
    detected: bool
    suggestion: str


@dataclass
class ScanReport:
    project_root: str
    language: str = "unknown"
    has_kanban: bool = False
    agent_conflicts: list = field(default_factory=list)
    existing_skills: list[str] = field(default_factory=list)
    testing_skills: list[str] = field(default_factory=list)
    infrastructure_gaps: list[InfrastructureGap] = field(default_factory=list)
    skill_gaps: list = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)


def _read_deps(root: Path, language: str) -> str:
    """Read dependency file content for framework detection."""
    if language in ("python",):
        for name in ("requirements.txt", "pyproject.toml", "setup.py", "Pipfile"):
            f = root / name
            if f.exists():
                return f.read_text(encoding="utf-8").lower()
    elif language in ("javascript", "typescript"):
        f = root / "package.json"
        if f.exists():
            return f.read_text(encoding="utf-8").lower()
    return ""


def detect_e2e_recommendation(language: str, root: Path) -> dict:
    """Detect E2E test recommendation based on project language and framework."""
    e2e_map = {
        "python": {
            "fastapi": {"e2e_tool": "pytest + httpx/testclient", "test_target": "API 端点完整链路"},
            "flask": {"e2e_tool": "pytest + Flask test client", "test_target": "API 端点完整链路"},
            "django": {"e2e_tool": "pytest + django.test.Client", "test_target": "视图完整链路"},
        },
        "javascript": {
            "express": {"e2e_tool": "jest + supertest", "test_target": "API 端点完整链路"},
        },
        "typescript": {
            "express": {"e2e_tool": "jest + supertest", "test_target": "API 端点完整链路"},
            "react": {"e2e_tool": "jest + Playwright", "test_target": "页面交互完整流程"},
            "next": {"e2e_tool": "jest + Playwright", "test_target": "页面交互完整流程"},
        },
        "go": {
            "_default": {"e2e_tool": "go test + httptest", "test_target": "HTTP 处理器完整链路"},
        },
    }
    fallback = {"e2e_tool": "项目测试框架", "test_target": "完整用户操作流程"}

    if language == "go":
        return e2e_map["go"]["_default"]

    lang_map = e2e_map.get(language, {})
    if not lang_map:
        return fallback

    deps = _read_deps(root, language)
    for fw_name, rec in lang_map.items():
        if fw_name in deps:
            return rec

    if language == "python":
        return {"e2e_tool": "pytest + subprocess", "test_target": "CLI 完整流程"}

    return fallback


def generate_default_test_profile(language: str, output_dir: str, root: Path) -> str:
    """Generate default test_profile.md content based on project type."""
    has_games = (root / "games").exists() or output_dir == "games"

    e2e_rec = detect_e2e_recommendation(language, root)
    e2e_section = (
        "\n## E2E 测试策略\n\n"
        f"本项目推荐 E2E 测试。基于检测到的技术栈，"
        f"建议使用 {e2e_rec['e2e_tool']} 对 {e2e_rec['test_target']} 做完整链路验证。\n"
        "覆盖场景应包括：用户完整操作流程、跨模块数据流转、"
        "外部服务集成点。QA agent 应根据 spec.md 中的功能范围"
        "自动决定 E2E 测试的具体覆盖粒度。\n"
    )

    if has_games:
        return (
            "# 测试与验收规范\n\n"
            "## 测试框架\n"
            "使用 pytest\n\n"
            "## 测试编写要求\n"
            "- 游戏逻辑模块必须用 pytest 编写单元测试\n"
            "- 覆盖边界情况：空状态、极值、状态转换、碰撞检测\n\n"
            "## 验收流程\n"
            "1. 启动游戏主程序，验证主界面正常加载\n"
            "2. 通过 GM 指令模拟游戏操作，验证核心游戏逻辑\n"
            "3. 检查异常输入时程序不会崩溃，有合理的错误提示\n\n"
            "## 验收文档要求\n"
            "acceptance.md 需包含：\n"
            "- 功能验收清单（按 spec.md 的 FR-XXX 逐条勾选）\n"
            "- 测试覆盖报告\n"
            "- 变更文件列表\n"
            "- 已知遗留问题\n"
        ) + e2e_section
    elif language == "python":
        return (
            "# 测试与验收规范\n\n"
            "## 测试框架\n"
            "使用 pytest，测试文件放 test/ 目录\n\n"
            "## 测试编写要求\n"
            "- 每个模块必须有对应的单元测试\n"
            "- 覆盖正常输入和边界情况\n\n"
            "## 验收流程\n"
            "1. 运行全部测试，确认无失败\n"
            "2. 检查测试覆盖率\n\n"
            "## 验收文档要求\n"
            "acceptance.md 需包含：\n"
            "- 功能验收清单（按 spec.md 的 FR-XXX 逐条勾选）\n"
            "- 测试覆盖报告（单元测试数、通过率）\n"
            "- 变更文件列表（新增/修改/删除）\n"
            "- 已知遗留问题\n"
        ) + e2e_section
    else:
        return (
            "# 测试与验收规范\n\n"
            "## 测试框架\n"
            "使用项目标准测试框架\n\n"
            "## 测试编写要求\n"
            "- 每个模块必须有对应的测试\n"
            "- 覆盖正常输入和边界情况\n\n"
            "## 验收流程\n"
            "1. 运行全部测试，确认无失败\n\n"
            "## 验收文档要求\n"
            "acceptance.md 需包含：\n"
            "- 功能验收清单\n"
            "- 测试覆盖报告\n"
            "- 变更文件列表\n"
            "- 已知遗留问题\n"
        ) + e2e_section


def generate_recommendations(report: ScanReport) -> list[str]:
    recs = []

    if report.agent_conflicts:
        conflict_roles = [c.role for c in report.agent_conflicts]
        recs.append(f"检测到 {len(report.agent_conflicts)} 个 agent 冲突: {', '.join(conflict_roles)}，建议合并到 kanban agent")

    if report.existing_skills:
        recs.append(f"检测到 {len(report.existing_skills)} 个自定义 skills: {', '.join(report.existing_skills)}")

    missing = [g for g in report.infrastructure_gaps if not g.detected]
    if missing:
        tools = [m.tool for m in missing]
        recs.append(f"缺少 {len(missing)} 项基础设施: {', '.join(tools)}，建议补充")

    if not report.has_kanban:
        recs.append("项目尚未初始化 kanban，运行 /kanban init 完成初始化")

    if report.skill_gaps:
        missing = [g.skill_name for g in report.skill_gaps]
        recs.append(f"缺少 {len(report.skill_gaps)} 个必需的 superpowers skill: {', '.join(missing)}，建议安装后再使用 kanban")

    return recs


def check_gitignore(root: Path, output_dir: str) -> list[InfrastructureGap]:
    import fnmatch
    gaps = []
    gitignore = root / ".gitignore"
    if not gitignore.exists():
        return gaps
    lines = gitignore.read_text(encoding="utf-8").split("\n")
    for line in lines:
        pat = line.strip()
        if pat and not pat.startswith("#"):
            if fnmatch.fnmatch(output_dir, pat) or fnmatch.fnmatch(f"{output_dir}/", pat):
                gaps.append(InfrastructureGap(
                    category="domain", tool="gitignore", config_file=".gitignore",
                    detected=False,
                    suggestion=f"output_dir '{output_dir}' 被 .gitignore 排除，Agent 需 git add -f 或修改 .gitignore",
                ))
                break
    return gaps
