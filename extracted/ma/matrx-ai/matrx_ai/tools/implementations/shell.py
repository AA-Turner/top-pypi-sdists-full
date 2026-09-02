from __future__ import annotations

import asyncio
import logging
import shlex
import time
from pathlib import Path
from typing import Any

from matrx_ai.tools._call_logger import write_tool_call_log
from matrx_ai.tools._sandbox_proxy import (
    SandboxProxyError,
    exec_command as _proxy_exec,
    get_active_sandbox,
)
from matrx_ai.tools._sandbox_runtime import sandbox_mode_active, scoped_base_for
from matrx_ai.tools.arg_models.shell_args import ShellExecuteArgs, ShellPythonArgs
from matrx_ai.tools.kinds.execution import ShellExecution
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult

logger = logging.getLogger(__name__)

MAX_OUTPUT_SIZE = 10_240  # 10 KB

# Multi-token destructive PHRASES — these never appear in legitimate
# command lines as substrings (the spaces and slashes save us). Matched
# with leading-whitespace anchoring so they only fire as actual command
# fragments, not as substrings inside flags like ``--phrase``.
_BLOCKED_PHRASES = (
    "rm -rf /",
    "rm -rf /*",
    "rm -rf /home",
    "rm -rf ~",
    "dd if=/dev/zero",
    ":(){ :|:& };:",
)

# Single-token destructive PROGRAMS — checked against the actual program
# being executed (the first token, or the token after sudo/exec/env).
# Substring-matching these against the whole command line was the bug
# that produced "Command blocked: git log --format=" — ``format`` and
# ``halt`` are common substrings of innocent flags / paths / arguments.
# This list is what the bash shell would actually invoke as a binary.
_BLOCKED_PROGRAMS = frozenset(
    {
        "mkfs",  # fs format — different from the false-positive "format" string
        "fdisk",
        "shutdown",
        "reboot",
        "poweroff",
    }
)

# Tokens we look through to find the *real* program (sudo cat, env -i bash, etc.).
_PASSTHROUGH_TOKENS = frozenset({"sudo", "doas", "exec", "env", "nohup", "time", "command"})


def _real_program_token(tokens: list[str]) -> str:
    """Walk past prefix tokens like ``sudo``, ``env -i``, ``exec`` etc.
    and return the program token that's actually being executed. Lowercased,
    basename only (so ``/usr/sbin/shutdown`` still matches ``shutdown``).
    """
    i = 0
    while i < len(tokens):
        t = tokens[i].lower()
        if t in _PASSTHROUGH_TOKENS:
            i += 1
            # ``env`` and ``time`` accept their own flags before the real cmd —
            # skip flag-shaped args.
            while i < len(tokens) and tokens[i].startswith("-"):
                i += 1
            # ``env`` also takes ``KEY=VALUE`` pairs before the program.
            while i < len(tokens) and "=" in tokens[i] and not tokens[i].startswith("-"):
                # crude check for VAR=value vs --flag=value; --flags already stripped above
                i += 1
            continue
        # Strip any path component to compare on basename.
        return Path(t).name
    return ""


def _is_blocked(command: str) -> bool:
    """Decide whether to refuse a shell command at the matrx-ai layer.

    Inside a sandbox the container IS the boundary. Even ``rm -rf /``,
    a fork bomb, or ``mkfs`` only damages the one disposable container,
    which the operator can recreate via the FE Reset action. Blocking
    them here would prevent legitimate recovery work for no net safety
    benefit. So in sandbox mode (running INSIDE a sandbox via
    ``mtx aidream serve``) and in sandbox-bound mode (matrx-ai running
    on aidream's host but routed into a sandbox via the proxy), this
    returns ``False`` unconditionally.

    Multi-tenant aidream still applies the blocklist because in that
    path the host process IS shared and a destructive command affects
    every tenant.

    Matching strategy is **token-aware**, not substring. The previous
    substring approach blocked every ``--format=`` flag because ``format``
    was on the list — that's a false-positive magnet. Now we tokenize
    via shlex, walk past sudo/env/exec wrappers, and only block when the
    actual program being executed is one of ``_BLOCKED_PROGRAMS``. We
    also keep a short list of ``_BLOCKED_PHRASES`` (e.g. ``rm -rf /``)
    matched at start-of-command or after a separator so they catch
    chained shell expressions but not substrings of unrelated flags.
    """
    if sandbox_mode_active() or get_active_sandbox() is not None:
        return False

    raw = command.strip()
    if not raw:
        return False

    # ── Phrase check on the WHOLE command ──────────────────────────────────
    # Some destructive forms (the fork bomb) contain shell separators inside
    # the phrase itself, so segment-splitting first would miss them. Match
    # the whole stripped command against an exact-equality first, then per
    # segment so both forms are caught.
    raw_lower = raw.lower()
    for phrase in _BLOCKED_PHRASES:
        if (
            raw_lower == phrase
            or raw_lower.startswith(phrase + " ")
            or raw_lower.startswith(phrase + "\n")
        ):
            return True

    segments = _split_segments(raw)
    for seg in segments:
        seg_lower = seg.strip().lower()
        for phrase in _BLOCKED_PHRASES:
            if seg_lower == phrase or seg_lower.startswith(phrase + " "):
                return True

    # ── Program-token check ────────────────────────────────────────────────
    # mkfs has many real-world variants (mkfs.ext4, mkfs.xfs, mkfs.btrfs).
    # Bare ``mkfs`` rarely exists as a binary; the family is what we mean.
    for seg in segments:
        try:
            tokens = shlex.split(seg, comments=False, posix=True)
        except ValueError:
            # Unbalanced quotes — let the shell return the error to the agent
            # rather than us pretending we know what was meant.
            continue
        if not tokens:
            continue
        program = _real_program_token(tokens)
        if program in _BLOCKED_PROGRAMS:
            return True
        if program.startswith("mkfs."):
            return True
    return False


def _split_segments(command: str) -> list[str]:
    """Split a shell line on common separators (``&&``, ``||``, ``;``, ``|``)
    so we can analyze each pipeline stage separately. Best-effort — we
    don't try to parse subshells or backticks. The fallback is "whole line
    as one segment" which is still correct for the program-token check.
    """
    out: list[str] = []
    current: list[str] = []
    i = 0
    while i < len(command):
        c = command[i]
        nxt = command[i + 1] if i + 1 < len(command) else ""
        if (c == "&" and nxt == "&") or (c == "|" and nxt == "|"):
            out.append("".join(current))
            current = []
            i += 2
            continue
        if c in ";|":
            out.append("".join(current))
            current = []
            i += 1
            continue
        current.append(c)
        i += 1
    out.append("".join(current))
    return [s for s in (seg.strip() for seg in out) if s]


def _build_exit_error_message(
    *,
    command: str,
    exit_code: int,
    stdout: str,
    stderr: str,
) -> str:
    """Compose the failure message returned to the LLM.

    Principle: the model is an expert reader of raw terminal output. Hand
    it the full stderr (and stdout when stderr is empty) verbatim, plus a
    recovery hint when the failure pattern is one we recognize. Never
    truncate — the previous ``stderr_str[:500]`` line was hiding the
    ``hint:`` lines git emits AFTER the headline error.
    """
    parts = [
        f"Command exited with code {exit_code}.",
        f"\nCommand:\n{command}",
    ]
    if stderr.strip():
        parts.append(f"\nstderr:\n{stderr}")
    if stdout.strip() and not stderr.strip():
        # When stderr is empty but stdout has content, surface stdout
        # — some tools write everything to stdout (npm, docker, etc.).
        parts.append(f"\nstdout:\n{stdout}")

    hint = _recovery_hint_for(stderr or stdout, command)
    if hint:
        parts.append(f"\nrecovery hint:\n{hint}")

    return "".join(parts)


def _recovery_hint_for(error_text: str, command: str) -> str | None:
    """Pattern-match common terminal failures and return a hint that tells
    the agent EXACTLY how to recover. Pure additive — never replaces the
    original error, just appends actionable guidance.
    """
    text = (error_text or "").lower()
    cmd = (command or "").lower()

    # Git HTTPS auth failure — the most common one we've seen.
    if "could not read username for 'https://github.com'" in text or (
        "fatal: authentication" in text and "github" in cmd
    ):
        return (
            "Git is asking for HTTPS credentials but the sandbox has none. Two ways to fix:\n"
            "  1. Register a GitHub token via the orchestrator's credentials API:\n"
            '       POST /sandboxes/{id}/credentials  body: {"kind":"github","token":"<pat>"}\n'
            "     The sandbox configures git's credential helper; subsequent clones/pulls work.\n"
            "  2. OR clone via SSH: change the URL to git@github.com:<owner>/<repo>.git and ensure\n"
            "     ~/.ssh/id_ed25519 is configured (the sandbox's ssh setup populates a key on\n"
            "     boot for orchestrator-spawned sandboxes).\n"
            "  3. OR for read-only public repos, append ``|| true`` to skip auth — but that\n"
            "     only works for genuinely-public repos."
        )

    # SSH auth failure.
    if "permission denied (publickey)" in text:
        return (
            "SSH key auth failed. The sandbox has no key registered for the target host. "
            "Drop a private key in /home/agent/.ssh/id_ed25519 (chmod 600) and the matching "
            "public key into the remote's authorized_keys. For GitHub specifically, prefer "
            "the /credentials API (token-based) — it's simpler than SSH key plumbing."
        )

    # No internet egress (rare but happens during ops work).
    if "could not resolve host" in text or "name or service not known" in text:
        return (
            "DNS resolution failed inside the sandbox. The sandbox network may be misconfigured "
            "or the orchestrator's network policy may have changed. Try `cat /etc/resolv.conf` "
            "and `curl -v https://1.1.1.1` to confirm; if both fail, ping the operator to "
            "check the orchestrator's docker network."
        )

    # Out-of-disk on the sandbox volume.
    if "no space left on device" in text:
        return (
            "The sandbox volume is full. List large directories with `du -sh /home/agent/* | sort -h` "
            "and clean up. Reset the sandbox (FE Inspector → Reset, optionally with 'wipe volume') "
            "if you want a fresh /home/agent."
        )

    # Python ModuleNotFoundError.
    if "modulenotfounderror" in text:
        return (
            "Module not installed. Inside a sandbox, `pip install <pkg>` (or `uv pip install`) is "
            "always available — go ahead and install it. The sandbox is the boundary; don't ask "
            "the user to install for you."
        )

    return None


def _workspace_dir(ctx: ToolContext, working_dir: str = ".") -> str:
    base = scoped_base_for(ctx.user_id, ctx.project_id)
    base.mkdir(parents=True, exist_ok=True)
    resolved = (base / working_dir).resolve()
    if not str(resolved).startswith(str(base.resolve())):
        return str(base)
    resolved.mkdir(parents=True, exist_ok=True)
    return str(resolved)


async def shell_execute(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = ShellExecuteArgs(**args)

    if _is_blocked(parsed.command):
        # Surface the FULL command and explain what tripped the block, so the
        # agent (an expert reader) can adjust without guessing. Never truncate
        # the command — the agent needs to see exactly what we rejected.
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="permission",
                message=(
                    "Command refused by matrx-ai's multi-tenant safety guard "
                    "(running on the central aidream backend, not in a sandbox).\n"
                    f"\nFull command:\n{parsed.command}\n\n"
                    "Refused programs (token-matched): mkfs, fdisk, shutdown, "
                    "reboot, poweroff. Refused phrases (anchored): "
                    "'rm -rf /', 'rm -rf /*', 'rm -rf /home', 'rm -rf ~', "
                    "'dd if=/dev/zero', fork-bomb."
                ),
                suggested_action=(
                    "If this command is genuinely needed, bind a sandbox to this "
                    "conversation — inside a sandbox there is NO blocklist, the "
                    "container is the security boundary. The FE editor's "
                    '"Sandbox Inspector" pane has a Reset / activate flow.'
                ),
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="shell_execute",
            call_id=ctx.call_id,
        )

    # No sandbox + a durable VFS backend → run the command in the durable code_files
    # shell (the ~50 coreutils over the user's persistent filesystem) instead of the
    # ephemeral real-disk host. A sandbox always wins (real container) via the branch below.
    from matrx_ai.tools.vfs.workspace import has_durable_backend

    if not sandbox_mode_active() and get_active_sandbox() is None and has_durable_backend():
        from matrx_ai.tools.implementations import vfs_shell

        return await vfs_shell.shell_execute(args, ctx)

    # Sandbox-bound chat: route the shell command into the container's
    # /exec endpoint instead of running on the aidream host. This is the
    # unrestricted run-anything escape hatch — the agent gets a real bash
    # shell inside the sandbox, with grep, find, git, npm, pip, anything
    # the image already has installed.
    if (binding := get_active_sandbox()) is not None:
        try:
            cwd_path = (
                parsed.working_dir
                if parsed.working_dir.startswith("/")
                else f"{binding.root_path.rstrip('/')}/{parsed.working_dir.lstrip('./')}"
                if parsed.working_dir not in ("", ".", "./")
                else binding.root_path
            )
            result = await _proxy_exec(
                binding,
                parsed.command,
                cwd=cwd_path,
                timeout=parsed.timeout_seconds,
            )
            exit_code = int(result.get("exit_code", 0))
            stdout_text = str(result.get("stdout", ""))
            stderr_text = str(result.get("stderr", ""))
            stdout_truncated = len(stdout_text) > MAX_OUTPUT_SIZE
            stderr_truncated = len(stderr_text) > MAX_OUTPUT_SIZE
            duration_ms = int((time.time() - started_at) * 1000)

            # Persist the FULL call (untruncated stdout/stderr + metadata)
            # to ~/.matrx/runtime/tool-calls/<conv>/<file>.md so the agent
            # can fs_read it later, and a future context-demoter can swap
            # the truncated message for a "(see file)" pointer.
            log_path = await write_tool_call_log(
                tool="shell_execute",
                call_id=ctx.call_id,
                inputs={
                    "command": parsed.command,
                    "working_dir": parsed.working_dir,
                    "timeout_seconds": parsed.timeout_seconds,
                },
                stdout=stdout_text,
                stderr=stderr_text,
                success=exit_code == 0,
                exit_code=exit_code,
                duration_ms=duration_ms,
                message_id=getattr(ctx, "message_id", None),
                conversation_id=getattr(ctx, "conversation_id", None),
                user_id=getattr(ctx, "user_id", None),
                output_truncated_in_response=stdout_truncated or stderr_truncated,
            )

            return ToolResult(
                success=exit_code == 0,
                # KindModel result (KIND_TOOL_LEDGER): shared shell_execution
                # shape — carried on failure too (a nonzero exit is a result).
                output=ShellExecution(
                    stdout=stdout_text[-MAX_OUTPUT_SIZE:] if stdout_truncated else stdout_text,
                    stderr=stderr_text[-MAX_OUTPUT_SIZE:] if stderr_truncated else stderr_text,
                    stdout_truncated=stdout_truncated,
                    stderr_truncated=stderr_truncated,
                    exit_code=exit_code,
                    cwd=str(result.get("cwd", cwd_path)),
                    log_path=log_path,
                ).model_dump(mode="json"),
                error=ToolError(
                    error_type="exit_code",
                    message=_build_exit_error_message(
                        command=parsed.command,
                        exit_code=exit_code,
                        stdout=stdout_text,
                        stderr=stderr_text,
                    ),
                )
                if exit_code != 0
                else None,
                started_at=started_at,
                completed_at=time.time(),
                tool_name="shell_execute",
                call_id=ctx.call_id,
            )
        except SandboxProxyError as exc:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type=getattr(exc, "error_type", "sandbox_error"),
                    message=str(exc),
                ),
                started_at=started_at,
                completed_at=time.time(),
                tool_name="shell_execute",
                call_id=ctx.call_id,
            )

    cwd = _workspace_dir(ctx, parsed.working_dir)

    try:
        process = await asyncio.create_subprocess_shell(
            parsed.command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd,
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=parsed.timeout_seconds,
            )
        except TimeoutError:
            process.kill()
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="timeout",
                    message=f"Command timed out after {parsed.timeout_seconds}s",
                    is_retryable=True,
                    suggested_action="Try a simpler command or increase the timeout.",
                ),
                started_at=started_at,
                completed_at=time.time(),
                tool_name="shell_execute",
                call_id=ctx.call_id,
            )

        stdout_text = stdout.decode("utf-8", errors="replace")
        stderr_text = stderr.decode("utf-8", errors="replace")

        # Spill files for large outputs go to ``<base>/.matrx/runtime/shell-logs/``
        # — never cwd. Putting them in cwd polluted the workspace and made
        # ``ls`` confusing for both the agent and the user. Falls back to
        # the workspace base when the directory can't be created.
        spill_dir = Path(cwd) / ".matrx" / "runtime" / "shell-logs"
        try:
            spill_dir.mkdir(parents=True, exist_ok=True)
        except OSError:
            spill_dir = Path(cwd)

        stdout_str = stdout_text
        if len(stdout_text) > MAX_OUTPUT_SIZE:
            log_path = spill_dir / f"{int(started_at)}-stdout.log"
            try:
                log_path.write_text(stdout_text)
                stdout_str = (
                    f"...(Truncated {len(stdout_text)} bytes. Full output: {log_path})...\n"
                    + stdout_text[-MAX_OUTPUT_SIZE:]
                )
            except OSError:
                stdout_str = (
                    f"...(Truncated {len(stdout_text)} bytes; spill write failed)...\n"
                    + stdout_text[-MAX_OUTPUT_SIZE:]
                )

        stderr_str = stderr_text
        if len(stderr_text) > MAX_OUTPUT_SIZE:
            err_path = spill_dir / f"{int(started_at)}-stderr.log"
            try:
                err_path.write_text(stderr_text)
                stderr_str = (
                    f"...(Truncated {len(stderr_text)} bytes. Full output: {err_path})...\n"
                    + stderr_text[-MAX_OUTPUT_SIZE:]
                )
            except OSError:
                stderr_str = (
                    f"...(Truncated {len(stderr_text)} bytes; spill write failed)...\n"
                    + stderr_text[-MAX_OUTPUT_SIZE:]
                )

        return ToolResult(
            success=process.returncode == 0,
            # KindModel result (KIND_TOOL_LEDGER): shared shell_execution shape.
            output=ShellExecution(
                stdout=stdout_str,
                stderr=stderr_str,
                exit_code=process.returncode,
            ).model_dump(mode="json"),
            error=ToolError(
                error_type="exit_code",
                message=_build_exit_error_message(
                    command=parsed.command,
                    exit_code=process.returncode or 0,
                    stdout=stdout_str,
                    stderr=stderr_str,
                ),
            )
            if process.returncode != 0
            else None,
            started_at=started_at,
            completed_at=time.time(),
            tool_name="shell_execute",
            call_id=ctx.call_id,
        )

    except Exception as exc:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc, error_type="execution", message=f"Shell execution failed: {exc}"
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="shell_execute",
            call_id=ctx.call_id,
        )


async def shell_python(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = ShellPythonArgs(**args)

    # Sandbox-bound: run the script via /exec inside the container so
    # imports / fs access / environment match what the user's actual code
    # sees. The script body becomes stdin to ``python3 -`` so we don't have
    # to write a temp file in the container.
    if (binding := get_active_sandbox()) is not None:
        try:
            result = await _proxy_exec(
                binding,
                "python3 -",
                cwd=binding.root_path,
                stdin=parsed.code,
                timeout=parsed.timeout_seconds,
            )
            exit_code = int(result.get("exit_code", 0))
            stdout_text = str(result.get("stdout", ""))
            stderr_text = str(result.get("stderr", ""))
            stdout_truncated = len(stdout_text) > MAX_OUTPUT_SIZE
            stderr_truncated = len(stderr_text) > MAX_OUTPUT_SIZE
            duration_ms = int((time.time() - started_at) * 1000)

            log_path = await write_tool_call_log(
                tool="shell_python",
                call_id=ctx.call_id,
                inputs={
                    "code": parsed.code,
                    "timeout_seconds": parsed.timeout_seconds,
                },
                stdout=stdout_text,
                stderr=stderr_text,
                success=exit_code == 0,
                exit_code=exit_code,
                duration_ms=duration_ms,
                message_id=getattr(ctx, "message_id", None),
                conversation_id=getattr(ctx, "conversation_id", None),
                user_id=getattr(ctx, "user_id", None),
                output_truncated_in_response=stdout_truncated or stderr_truncated,
            )

            return ToolResult(
                success=exit_code == 0,
                # KindModel result (KIND_TOOL_LEDGER): shared shell_execution
                # shape — carried on failure too (a nonzero exit is a result).
                output=ShellExecution(
                    stdout=stdout_text[-MAX_OUTPUT_SIZE:] if stdout_truncated else stdout_text,
                    stderr=stderr_text[-MAX_OUTPUT_SIZE:] if stderr_truncated else stderr_text,
                    stdout_truncated=stdout_truncated,
                    stderr_truncated=stderr_truncated,
                    exit_code=exit_code,
                    log_path=log_path,
                ).model_dump(mode="json"),
                error=ToolError(
                    error_type="exit_code",
                    message=_build_exit_error_message(
                        command="python3 -",
                        exit_code=exit_code,
                        stdout=stdout_text,
                        stderr=stderr_text,
                    ),
                )
                if exit_code != 0
                else None,
                started_at=started_at,
                completed_at=time.time(),
                tool_name="shell_python",
                call_id=ctx.call_id,
            )
        except SandboxProxyError as exc:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type=getattr(exc, "error_type", "sandbox_error"),
                    message=str(exc),
                ),
                started_at=started_at,
                completed_at=time.time(),
                tool_name="shell_python",
                call_id=ctx.call_id,
            )

    cwd = _workspace_dir(ctx)
    script_path = Path(cwd) / "_tool_exec.py"

    try:
        script_path.write_text(parsed.code)

        process = await asyncio.create_subprocess_exec(
            "python3",
            str(script_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd,
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=parsed.timeout_seconds,
            )
        except TimeoutError:
            process.kill()
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="timeout",
                    message=f"Python execution timed out after {parsed.timeout_seconds}s",
                    is_retryable=True,
                ),
                started_at=started_at,
                completed_at=time.time(),
                tool_name="shell_python",
                call_id=ctx.call_id,
            )
        finally:
            try:
                script_path.unlink()
            except Exception:
                pass

        stdout_text = stdout.decode("utf-8", errors="replace")
        stderr_text = stderr.decode("utf-8", errors="replace")

        stdout_str = stdout_text
        if len(stdout_text) > MAX_OUTPUT_SIZE:
            log_path = Path(cwd) / f"_python_stdout_{int(started_at)}.log"
            log_path.write_text(stdout_text)
            stdout_str = (
                f"...(Truncated {len(stdout_text)} bytes. Full output written to {log_path})...\n"
                + stdout_text[-MAX_OUTPUT_SIZE:]
            )

        stderr_str = stderr_text
        if len(stderr_text) > MAX_OUTPUT_SIZE:
            err_path = Path(cwd) / f"_python_stderr_{int(started_at)}.log"
            err_path.write_text(stderr_text)
            stderr_str = (
                f"...(Truncated {len(stderr_text)} bytes. Full output written to {err_path})...\n"
                + stderr_text[-MAX_OUTPUT_SIZE:]
            )

        return ToolResult(
            success=process.returncode == 0,
            # KindModel result (KIND_TOOL_LEDGER): shared shell_execution shape.
            output=ShellExecution(
                stdout=stdout_str,
                stderr=stderr_str,
                exit_code=process.returncode,
            ).model_dump(mode="json"),
            error=ToolError(
                error_type="exit_code",
                message=_build_exit_error_message(
                    command=f"python3 {script_path}",
                    exit_code=process.returncode,
                    stdout=stdout_text,
                    stderr=stderr_text,
                ),
            )
            if process.returncode != 0
            else None,
            started_at=started_at,
            completed_at=time.time(),
            tool_name="shell_python",
            call_id=ctx.call_id,
        )

    except Exception as exc:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc, error_type="execution", message=f"Python execution failed: {exc}"
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="shell_python",
            call_id=ctx.call_id,
        )
