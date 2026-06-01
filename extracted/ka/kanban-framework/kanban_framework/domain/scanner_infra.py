"""Scanner infrastructure — language-specific and domain infrastructure checks."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class InfrastructureGap:
    category: str
    tool: str
    config_file: str
    detected: bool
    suggestion: str


def detect_infrastructure_gaps(root: Path, language: str) -> list[InfrastructureGap]:
    gaps = []

    if language == "python":
        gaps.extend(_check_python_infra(root))
    elif language in ("javascript", "typescript"):
        gaps.extend(_check_js_infra(root))
    elif language == "go":
        gaps.extend(_check_go_infra(root))

    gaps.extend(_check_domain_infra(root, language))

    try:
        import jieba  # noqa: F401
    except ImportError:
        gaps.append(InfrastructureGap(
            category="knowledge", tool="jieba",
            detected=False,
            suggestion="知识库中文搜索依赖 jieba，建议安装: pip install jieba",
        ))

    return gaps


def _check_python_infra(root: Path) -> list[InfrastructureGap]:
    import subprocess
    gaps = []
    has_pyproject = (root / "pyproject.toml").exists()

    try:
        result = subprocess.run(["pylint", "--version"], capture_output=True, timeout=10)
        pylint_ok = result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pylint_ok = False

    if not pylint_ok and not (root / ".pylintrc").exists():
        gaps.append(InfrastructureGap(
            category="linting", tool="pylint",
            config_file=".pylintrc",
            detected=False,
            suggestion="建议安装 pylint: pip install pylint",
        ))

    try:
        result = subprocess.run(["pytest", "--version"], capture_output=True, timeout=10)
        pytest_ok = result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pytest_ok = False

    if not pytest_ok:
        gaps.append(InfrastructureGap(
            category="testing", tool="pytest",
            config_file="pytest.ini",
            detected=False,
            suggestion="建议安装 pytest: pip install pytest",
        ))

    try:
        result = subprocess.run(["coverage", "--version"], capture_output=True, timeout=10)
        cov_ok = result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        cov_ok = False

    if not cov_ok and not has_pyproject:
        gaps.append(InfrastructureGap(
            category="testing", tool="coverage",
            config_file=".coveragerc",
            detected=False,
            suggestion="建议安装 coverage: pip install coverage",
        ))

    return gaps


def _check_js_infra(root: Path) -> list[InfrastructureGap]:
    gaps = []
    pkg = root / "package.json"

    if pkg.exists():
        import json
        try:
            data = json.loads(pkg.read_text(encoding="utf-8"))
            dev_deps = {**data.get("devDependencies", {}), **data.get("dependencies", {})}

            if "eslint" not in dev_deps:
                gaps.append(InfrastructureGap(
                    category="linting", tool="eslint",
                    config_file=".eslintrc.*",
                    detected=False,
                    suggestion="建议添加 ESLint 配置以进行代码规范检查",
                ))

            if "jest" not in dev_deps and "vitest" not in dev_deps and "mocha" not in dev_deps:
                gaps.append(InfrastructureGap(
                    category="testing", tool="jest",
                    config_file="jest.config.*",
                    detected=False,
                    suggestion="建议添加测试框架配置（Jest/Vitest）",
                ))
        except (json.JSONDecodeError, OSError):
            pass

    return gaps


def _check_go_infra(root: Path) -> list[InfrastructureGap]:
    gaps = []
    if not (root / ".golangci.yml").exists():
        gaps.append(InfrastructureGap(
            category="linting", tool="golangci-lint",
            config_file=".golangci.yml",
            detected=False,
            suggestion="建议添加 golangci-lint 配置以进行代码质量检查",
        ))
    return gaps


def _check_domain_infra(root: Path, language: str) -> list[InfrastructureGap]:
    gaps = []
    cfg = root / ".kanban" / "config.json"
    output_dir = "src"
    if cfg.exists():
        import json
        try:
            data = json.loads(cfg.read_text(encoding="utf-8"))
            output_dir = data.get("output_dir", "src")
        except (json.JSONDecodeError, OSError):
            pass

    games_dir = root / "games"
    if output_dir == "games" or games_dir.exists():
        found_gm = False
        for sub in (games_dir if games_dir.exists() else root).iterdir():
            if sub.is_dir():
                for f in sub.rglob("gm*.py"):
                    found_gm = True
                    break
                for f in sub.rglob("gm*.js"):
                    found_gm = True
                    break

        if not found_gm:
            gaps.append(InfrastructureGap(
                category="domain", tool="gm_commands",
                config_file="gm_commands.py",
                detected=False,
                suggestion="游戏项目建议添加 GM 指令系统，方便 QA 调测（如创建 gm_commands.py/j模块，包含常用调试指令）",
            ))

    from kanban_framework.domain.scanner_recommend import check_gitignore
    gaps.extend(check_gitignore(root, output_dir))
    return gaps
