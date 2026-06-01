"""Shared utilities for CLI task commands."""
from __future__ import annotations

import os
import re
import shutil
import subprocess

from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.infra.config import Config
from kanban_framework.domain.task import TaskManager
from kanban_framework.domain.scanner import scan_project, ScanReport


def _resolve() -> tuple[Filesystem, Config, TaskManager]:
    root = Filesystem.find_project_root()
    fs = Filesystem(root=root)
    cfg = Config(fs)
    return fs, cfg, TaskManager(fs, cfg)


def _serialize_report(report: ScanReport) -> dict:
    return {
        "project_root": report.project_root,
        "language": report.language,
        "has_kanban": report.has_kanban,
        "agent_conflicts": [
            {
                "role": c.role,
                "kanban_agent": c.kanban_agent,
                "project_file": c.project_agent_file,
                "action": c.action,
                "description": c.description,
            }
            for c in report.agent_conflicts
        ],
        "existing_skills": report.existing_skills,
        "infrastructure_gaps": [
            {
                "category": g.category,
                "tool": g.tool,
                "detected": g.detected,
                "suggestion": g.suggestion,
            }
            for g in report.infrastructure_gaps
        ],
        "skill_gaps": [
            {
                "skill_name": g.skill_name,
                "required_by": g.required_by,
                "suggestion": g.suggestion,
            }
            for g in report.skill_gaps
        ],
        "recommendations": report.recommendations,
    }


def _check_kb_deps() -> dict:
    """Check knowledge base dependency availability."""
    missing = []
    available = []
    try:
        import jieba
        available.append("jieba (中文分词)")
    except ImportError:
        missing.append("jieba (中文分词)")
    try:
        import chromadb
        available.append("chromadb (语义搜索)")
    except ImportError:
        missing.append("chromadb (语义搜索)")
    try:
        from fastembed import TextEmbedding
        available.append("fastembed (向量嵌入)")
    except ImportError:
        missing.append("fastembed (向量嵌入)")
    try:
        cb = shutil.which("codeburn") or shutil.which("npx")
        if cb:
            available.append("codeburn (token 分析)")
        else:
            missing.append("codeburn (token 分析)")
    except Exception:
        missing.append("codeburn (token 分析)")
    return {
        "available": available,
        "missing": missing,
        "status": "ready" if not missing else "incomplete",
        "install_hint": _install_hint(missing) if missing else None,
    }


def _install_hint(missing: list[str]) -> str:
    if "codeburn" in " ".join(missing):
        return "npm install -g codeburn"
    return "pip install kanban-framework"


def _install_superpowers_skills(root, skill_gaps: list) -> dict:
    """Auto-install missing superpowers skills via npx skills add."""
    result: dict = {"attempted": False, "installed": [], "warnings": []}

    npx_bin = shutil.which("npx")
    if not npx_bin:
        result["warnings"].append(
            "npx not found — cannot auto-install superpowers skills. "
            "Install Node.js or run manually: "
            "npx skills add obra/superpowers -s brainstorming,writing-plans,test-driven-development -a claude-code -y"
        )
        return result

    _SKILL_MAP = {
        "superpowers:brainstorming": "brainstorming",
        "superpowers:writing-plans": "writing-plans",
        "superpowers:test-driven-development": "test-driven-development",
    }
    missing_skills = []
    for g in skill_gaps:
        short = _SKILL_MAP.get(g.skill_name)
        if short:
            missing_skills.append(short)

    if not missing_skills:
        return result

    skill_list = ",".join(missing_skills)
    cmd = [
        npx_bin, "skills", "add", "obra/superpowers",
        "-s", skill_list,
        "-a", "claude-code",
        "-y",
    ]

    result["attempted"] = True
    result["command"] = " ".join(cmd)

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(root),
        )
        result["exit_code"] = proc.returncode
        if proc.returncode == 0:
            result["installed"] = missing_skills
            result["message"] = f"Installed {len(missing_skills)} superpowers skills: {skill_list}"
        else:
            result["warnings"].append(
                f"npx skills add failed (exit {proc.returncode}): "
                f"{proc.stderr[:200] if proc.stderr else 'unknown error'}"
            )
    except subprocess.TimeoutExpired:
        result["warnings"].append("npx skills add timed out (120s)")
    except Exception as e:
        result["warnings"].append(f"npx skills add error: {e}")

    return result


def _compute_default_scope() -> str:
    """Compute default scope from env var or username."""
    scope = os.environ.get("KANBAN_KNOWLEDGE_SCOPE", "")
    if scope:
        return scope
    import getpass
    scope = re.sub(r'[^a-z0-9-]', '', getpass.getuser().lower().replace(" ", "-"))
    if not scope:
        scope = "default"
    return scope


_SCOPE_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,15}$")


def _prompt_scope(default: str) -> str:
    """Interactive prompt for knowledge.scope."""
    import sys as _sys
    print(f"\n  ▸ kanban 初始化向导\n", flush=True)
    while True:
        try:
            _sys.stdout.flush()
            raw = input(f"  工号（用于知识库个人标识）: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return default
        if not raw:
            print(f"  ✗ 请输入工号（建议: {default}），不能为空")
            continue
        scope = re.sub(r'[^a-z0-9-]', '', raw.lower().replace(" ", "-"))
        if scope and _SCOPE_RE.match(scope):
            # Extract numeric part for task_id_base (e.g. "6696" → TASK-6696001)
            task_base = extract_task_base(raw)
            if task_base:
                print(f"  ✓ scope: {scope} | task_id_base: {task_base} (TASK-{task_base}001...)")
            else:
                print(f"  ✓ scope: {scope}")
            print(f"  ✓ 知识库: knowledge-{scope}.db\n")
            return scope
        print(f"  ✗ 无效输入: 只允许小写字母、数字、连字符，2-16 字符")


def extract_task_base(raw: str) -> int:
    """Extract numeric part from worker ID for task_id_base. 0 if no digits."""
    digits = re.sub(r'[^0-9]', '', raw)
    return int(digits) if digits else 0


def cmd_install_codeburn(args: list[str]) -> dict:
    """Install CodeBurn globally via npm."""
    if shutil.which("codeburn"):
        return {"installed": True, "message": "codeburn already installed"}
    try:
        result = subprocess.run(
            ["npm", "install", "-g", "codeburn"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120
        )
        if result.returncode == 0:
            return {"installed": True, "message": "codeburn installed successfully"}
        return {"installed": False, "error": result.stderr.strip()}
    except Exception as e:
        return {"installed": False, "error": str(e)}


def cmd_scan(args: list[str]) -> dict:
    """Explicit scan command for debugging/testing."""
    root = Filesystem.find_project_root()
    report = scan_project(root)
    return _serialize_report(report)
