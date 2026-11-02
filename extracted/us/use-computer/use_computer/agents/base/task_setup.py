"""Task setup for CUA Harbor runs."""

from __future__ import annotations

import asyncio
import importlib.util
import inspect
import json
import logging
import re
import shlex
import sys
from pathlib import Path
from typing import Any

from use_computer.agents.types import Platform
from use_computer.automation.ax_transpile import (
    PRE_COMMAND_OSASCRIPT_TIMEOUT_S,
    needs_exec_ax,
    transpile,
)
from use_computer.setup_files import read_setup_files

PATH_PREFIX = "/tmp/harbor"
_SENSITIVE_ASSIGNMENT_RE = re.compile(
    r"\b([A-Z0-9_]*(?:TOKEN|KEY|SECRET|PASSWORD)[A-Z0-9_]*)=(?:'[^']*'|\"[^\"]*\"|[^ ;]+)"
)
_ANTHROPIC_TOKEN_RE = re.compile(r"sk-ant-[A-Za-z0-9_-]+")


async def run_task_setup(environment: Any, logger: logging.Logger) -> None:
    task_dir = _task_dir_from_env(environment)
    if task_dir is None:
        logger.debug("CUA task setup skipped: environment has no task_dir")
        return

    setup_dir = task_dir / "tests" / "setup"
    platform = _platform_from_env(environment)

    _load_in_process_config(environment, setup_dir)
    await _run_task_local_setup(environment, setup_dir, logger)

    await _upload_setup_files(environment, setup_dir, platform, logger)
    await _run_pre_command(environment, setup_dir, platform, logger)

    if setup_dir.exists():
        logger.info("CUA task setup complete")


def _task_dir_from_env(environment: Any) -> Path | None:
    return task_dir_from_env(environment)


def task_dir_from_env(environment: Any) -> Path | None:
    raw = getattr(environment, "_task_dir", None) or getattr(environment, "task_dir", None)
    if raw:
        return Path(raw).resolve()

    environment_dir = getattr(environment, "environment_dir", None)
    if environment_dir:
        path = Path(environment_dir).resolve()
        if path.name == "environment" and _looks_like_task_dir(path.parent):
            return path.parent

    return None


def _looks_like_task_dir(path: Path) -> bool:
    return (path / "task.toml").exists() and (path / "instruction.md").exists()


def _platform_from_env(environment: Any) -> Platform:
    raw = getattr(environment, "_platform", None)
    if raw is None:
        sandbox = getattr(environment, "sandbox", None)
        raw = getattr(sandbox, "type", None)
    return Platform.parse(raw, default=Platform.MACOS)


def _load_in_process_config(environment: Any, setup_dir: Path) -> None:
    environment._in_process_cmd = None
    environment._in_process_step = None
    config_path = setup_dir / "config.json"
    if not config_path.exists():
        return
    cfg = json.loads(config_path.read_text())
    in_process = cfg.get("in_process")
    if in_process and isinstance(in_process, list) and len(in_process) >= 2:
        environment._in_process_cmd = in_process[0]
        environment._in_process_step = in_process[1]


async def _upload_setup_files(
    environment: Any,
    setup_dir: Path,
    platform: Platform,
    logger: logging.Logger,
) -> None:
    try:
        setup_files = read_setup_files(setup_dir)
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"setup files manifest parse failed: {exc}")
        return

    for setup_file in setup_files:
        target = setup_file.target_path
        if not target:
            logger.warning(f"setup file missing target path: {setup_file}")
            continue

        local = setup_file.local_path(setup_dir)
        if not local.exists():
            logger.warning(f"setup file missing on disk: {local}")
            continue

        if local.is_dir():
            logger.info(f"uploading setup dir {local.name}/ -> {target}")
            await environment.upload_dir(local, target)
            continue

        await _ensure_parent_dir(environment, platform, target)
        logger.info(f"uploading setup file {local.name} -> {target} ({local.stat().st_size}B)")
        await environment.upload_file(local, target)


async def _ensure_parent_dir(environment: Any, platform: Platform, target: str) -> None:
    parent = str(Path(target).parent)
    if parent in ("", "."):
        return
    await environment.sandbox.exec_ssh(f"mkdir -p {shlex.quote(parent)}", timeout=60)


async def _run_pre_command(
    environment: Any,
    setup_dir: Path,
    platform: Platform,
    logger: logging.Logger,
) -> None:
    await _run_macos_pre_command(environment, setup_dir, logger)


async def _run_task_local_setup(
    environment: Any,
    setup_dir: Path,
    logger: logging.Logger,
) -> None:
    setup_py = setup_dir / "setup.py"
    if not setup_py.exists():
        return

    logger.info("running setup.py")
    spec = importlib.util.spec_from_file_location(
        f"_harbor_task_setup_{abs(hash(setup_py.resolve()))}",
        setup_py,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load task setup script: {setup_py}")

    module = importlib.util.module_from_spec(spec)
    setup_path = str(setup_dir)
    sys.path.insert(0, setup_path)
    try:
        spec.loader.exec_module(module)
        setup_task = getattr(module, "setup_task", None)
        if not callable(setup_task):
            raise RuntimeError(f"task setup script lacks setup_task(): {setup_py}")

        result = setup_task(environment, logger, setup_dir)
        if inspect.isawaitable(result):
            await result
    finally:
        if sys.path and sys.path[0] == setup_path:
            sys.path.pop(0)
        else:
            try:
                sys.path.remove(setup_path)
            except ValueError:
                pass


async def _run_macos_pre_command(
    environment: Any,
    setup_dir: Path,
    logger: logging.Logger,
) -> None:
    pre_cmd = setup_dir / "pre_command.sh"
    if not pre_cmd.exists():
        return
    raw = pre_cmd.read_text().strip()
    if not raw:
        return

    lines = [
        line.strip()
        for line in raw.split("\n")
        if line.strip() and not line.startswith("#!") and not line.strip().startswith("#")
    ]
    for i, line in enumerate(lines):
        transpiled, replacements = transpile(
            line,
            fallback_timeout_s=PRE_COMMAND_OSASCRIPT_TIMEOUT_S,
        )
        result = await _exec_macos_pre_line(environment, line, transpiled, replacements)
        if result.return_code == 0:
            out = ((result.stdout or "") + (result.stderr or "")).strip()
            logger.info(
                f"pre_command [{i + 1}/{len(lines)}] ok"
                + (f" (output: {out[:120]})" if out else "")
            )
            continue

        combined = (result.stdout or "") + (result.stderr or "")
        if result.return_code == -14:
            logger.warning(
                f"pre_command [{i + 1}/{len(lines)}] ALARM-KILLED. cmd={_cmd_snippet(line, 80)}"
            )
        if any(error in combined for error in ["-1712", "-1728"]):
            logger.warning(f"pre_command [{i + 1}/{len(lines)}] AE error, retrying in 15s...")
            await asyncio.sleep(15)
            result = await _exec_macos_pre_line(environment, line, transpiled, replacements)
        if result.return_code != 0:
            raise RuntimeError(
                f"pre_command [{i + 1}/{len(lines)}] failed (rc={result.return_code}):\n"
                f"cmd: {line}\nstdout: {result.stdout or ''}\nstderr: {result.stderr or ''}"
            )


async def _exec_macos_pre_line(
    environment: Any,
    raw: str,
    transpiled: str,
    replacements: int,
) -> Any:
    timeout = PRE_COMMAND_OSASCRIPT_TIMEOUT_S + 10
    if replacements > 0:
        if needs_exec_ax(transpiled):
            return await _exec_macos_ax(environment, transpiled)
        return await environment.exec(transpiled, timeout_sec=timeout)
    return await environment.exec(raw, timeout_sec=timeout)


async def _exec_macos_ax(environment: Any, command: str, timeout_sec: int = 30) -> Any:
    full_cmd = _wrap_with_timeout(_remap_macos_str(command), timeout_sec)
    return await environment.sandbox.exec_ax(full_cmd, timeout=timeout_sec)


def _remap_macos_str(value: str) -> str:
    return (
        value.replace("/logs/", f"{PATH_PREFIX}/logs/")
        .replace('/logs"', f'{PATH_PREFIX}/logs"')
        .replace("/logs'", f"{PATH_PREFIX}/logs'")
        .replace("/tests/", f"{PATH_PREFIX}/tests/")
        .replace("/solution/", f"{PATH_PREFIX}/solution/")
        .replace("/installed-agent", f"{PATH_PREFIX}/installed-agent")
        .replace("/app/", "/Users/lume/")
        .replace("/workspace/", "/Users/lume/")
    )


def _wrap_with_timeout(command: str, timeout: int) -> str:
    kill_after = max(timeout - 2, 5)
    escaped = command.replace("'", "'\\''")
    return f"perl -e 'alarm {kill_after}; exec @ARGV' -- bash -c '{escaped}'"


def _cmd_snippet(command: str, limit: int = 100) -> str:
    redacted = _SENSITIVE_ASSIGNMENT_RE.sub(r"\1=<redacted>", command)
    redacted = _ANTHROPIC_TOKEN_RE.sub("<redacted>", redacted)
    return redacted[:limit]


def _sh_quote(value: str) -> str:
    return "'" + str(value).replace("'", "'\"'\"'") + "'"
