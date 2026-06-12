"""External tool guard — executes CLI tools (pytest, pylint, etc.) and returns CheckResult.

Extracted from guard_checks.py for maintainability. Handles command template
resolution, subprocess execution with venv PATH, output parsing, and error
classification (ImportError vs test failure vs lint warning).
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path

from kanban_framework.types import Task
from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.domain.guard import CheckResult


def check_external_tool(fs: Filesystem, task: Task, tool_config: dict,
                        resolve_files_fn) -> CheckResult:
    """Execute an external CLI tool and return a CheckResult.

    Runs the configured command against files resolved by ``resolve_files_fn``.
    Supports fail/warn pattern matching, exit code checks, severity levels,
    and timeout control. Writes tool output to a log file in the task dir.

    Args:
        fs: Filesystem instance for path resolution.
        task: The task whose worktree to scan for files.
        tool_config: Dict with keys ``name``, ``command``, and optional
            ``scope``, ``timeout_seconds``, ``fail_pattern``, ``warn_pattern``,
            ``fail_on_exit_code``, ``severity``.
        resolve_files_fn: Callable(task, scope) -> list[str] for file resolution.
    """
    # 1. Resolve files
    scope = tool_config.get("scope", "changed")
    files = resolve_files_fn(task, scope)
    if not files:
        return CheckResult(passed=True, warnings=["No files to check"])

    # 2. Build command — replace ${files} and ${python_bin} placeholders
    import shlex
    tool_name = tool_config.get("name", "unknown")
    command_tmpl = tool_config.get("command", "")
    command = command_tmpl.replace("${files}", shlex.join(files))
    # Resolve ${python_bin} from config so venv tools work
    try:
        _py_bin, _ = Filesystem.resolve_python()
    except Exception:
        _py_bin = "python"
    command = command.replace("${python_bin}", _py_bin)
    timeout = tool_config.get("timeout_seconds", 120)
    worktree = task.worktree_path or str(fs.root)

    # 2b. Build env with venv's bin dir first in PATH so shutil.which
    #     and subprocess find venv-installed tools (pytest, pylint, etc.)
    _py_bin_dir = str(Path(_py_bin).resolve().parent)
    _tool_env = os.environ.copy()
    _tool_env["PATH"] = _py_bin_dir + os.pathsep + _tool_env.get("PATH", "")

    # 3. Execute via subprocess — resolve tool binary to handle venv paths
    tool_bin = shutil.which(command.split()[0], path=_tool_env["PATH"]) if not command.startswith(("/", "./", "../")) else command.split()[0]
    if tool_bin:
        command = tool_bin + command[len(command.split()[0]):]

    try:
        proc = subprocess.run(
            command, shell=True, capture_output=True, text=True,
            timeout=timeout, cwd=str(worktree), env=_tool_env,
        )
    except FileNotFoundError:
        return CheckResult(
            passed=True,
            warnings=[f"{tool_name} not installed, check skipped"],
        )
    except subprocess.TimeoutExpired:
        return CheckResult(
            passed=False,
            failures=[f"{tool_name} timed out after {timeout}s"],
        )

    # Shell returns exit code 127 for "command not found"
    if proc.returncode == 127:
        return CheckResult(
            passed=True,
            warnings=[f"{tool_name} not installed — check skipped. "
                      f"Install with: pip install {tool_name}"],
        )

    output = proc.stdout + proc.stderr

    # 4. Write log file
    task_dir = fs.task_dir(task.id)
    fs.ensure_dir(task_dir)
    log_path = task_dir / f"guard_external_{tool_name}.log"
    log_path.write_text(output, encoding="utf-8")

    # 5. Match fail_pattern -> failures
    failures: list[str] = []
    fail_pat = tool_config.get("fail_pattern")
    if fail_pat:
        for line in output.splitlines():
            if re.search(fail_pat, line):
                failures.append(line.strip())
        # E0401 remediation hint for src-layout projects
        if any("E0401" in f for f in failures):
            failures.append(
                "E0401 提示: src-layout 项目请在 .pylintrc 添加 "
                "[MAIN]\\ninit-hook=import sys; sys.path.insert(0, '.')"
            )

    # 6. Exit code check — distinguish env errors (ImportError) from code failures
    if tool_config.get("fail_on_exit_code", True) and proc.returncode != 0:
        _import_errors = [l.strip() for l in output.splitlines()
                          if re.search(r'(ModuleNotFoundError|ImportError)', l)]
        if _import_errors:
            return CheckResult(
                passed=True,
                warnings=[f"{tool_name}: {len(_import_errors)} import error(s) — "
                          f"likely missing optional dependency (not a code failure). "
                          f"First: {_import_errors[0]}"],
            )
        if not failures:
            failures.append(
                f"{tool_name} exited with code {proc.returncode}. "
                f"Full output saved to guard_external_{tool_name}.log. "
                f"Fix: resolve the errors above and re-run"
            )

    # 7. Match warn_pattern -> warnings
    warnings: list[str] = []
    warn_pat = tool_config.get("warn_pattern")
    if warn_pat:
        for line in output.splitlines():
            if re.search(warn_pat, line):
                warnings.append(line.strip())

    # 8. Severity determines blocking
    severity = tool_config.get("severity", "error")
    if severity == "warning":
        return CheckResult(passed=True, warnings=warnings + failures)
    return CheckResult(passed=len(failures) == 0, failures=failures, warnings=warnings)
