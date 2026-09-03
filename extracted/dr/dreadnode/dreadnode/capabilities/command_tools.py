import contextlib
import json
import math
import os
import selectors
import shutil
import signal
import string
import subprocess
import time
import typing as t
from pathlib import Path
from uuid import UUID

from jsonschema import Draft202012Validator
from loguru import logger

from dreadnode.agents.tools import Tool
from dreadnode.packaging.manifest import SHELL_EXECUTABLE_NAMES, CommandWrapperManifest

RESOLVED_COMMANDS_FILE = ".resolved_commands.json"
_MAX_OUTPUT_BYTES = 16_384
_TRUNCATED = b"\n...[truncated]"


class ResolvedCommandTool(CommandWrapperManifest):
    """A command declaration pinned to its immutable registry revision."""

    tool_revision_id: UUID


class CommandExecutionError(RuntimeError):
    """A bounded command-tool failure safe to return to an agent."""


class CommandTimeoutError(CommandExecutionError):
    """A command or version probe exceeded its declared timeout."""


def write_resolved_commands(capability_root: Path, commands: object) -> None:
    """Persist validated, revision-pinned command metadata beside a runtime capability."""
    resolved: list[dict[str, t.Any]] = []
    if isinstance(commands, list):
        for item in commands:
            if not isinstance(item, dict) or not item.get("tool_revision_id"):
                continue
            try:
                command = ResolvedCommandTool.model_validate(item)
            except Exception as exc:
                logger.warning("Ignoring invalid resolved command revision: {}", exc)
                continue
            resolved.append(command.model_dump(mode="json", exclude_none=True))
    (capability_root / RESOLVED_COMMANDS_FILE).write_text(
        json.dumps(resolved, indent=2, sort_keys=True)
    )


def load_command_tools(
    *,
    capability_name: str,
    capability_root: Path,
    workspace_root: Path,
    declarations: list[CommandWrapperManifest],
    component_health: list[dict[str, t.Any]],
) -> list[Tool]:
    """Load only registered command revisions that currently pass their version probe."""
    sidecar = capability_root / RESOLVED_COMMANDS_FILE
    declared = {
        command.name: command.model_dump(mode="json", exclude_none=True) for command in declarations
    }
    if not sidecar.is_file():
        for name in declared:
            _record_health(component_health, name, "Missing registered command revision")
        return []

    try:
        raw = json.loads(sidecar.read_text())
    except Exception as exc:
        for name in declared:
            _record_health(component_health, name, f"Invalid command revision sidecar: {exc}")
        return []
    if not isinstance(raw, list):
        for name in declared:
            _record_health(component_health, name, "Invalid command revision sidecar")
        return []

    names = [item.get("name") for item in raw if isinstance(item, dict)]
    duplicate_names = {name for name in names if name and names.count(name) > 1}
    tools: list[Tool] = []
    loaded_names: set[str] = set()
    for item in raw:
        if not isinstance(item, dict) or not item.get("tool_revision_id"):
            continue
        try:
            command = ResolvedCommandTool.model_validate(item)
        except Exception as exc:
            name = str(item.get("name") or "<unknown>")
            _record_health(component_health, name, f"Invalid registered command revision: {exc}")
            continue
        if command.name in duplicate_names:
            _record_health(component_health, command.name, "Duplicate registered command revisions")
            continue
        declaration = command.model_dump(
            mode="json", exclude={"tool_revision_id"}, exclude_none=True
        )
        if declared.get(command.name) != declaration:
            _record_health(component_health, command.name, "Registered command revision drift")
            continue
        try:
            _verify_command(command, capability_root, workspace_root)
        except CommandExecutionError as exc:
            _record_health(component_health, command.name, str(exc))
            continue

        tools.append(
            Tool(
                name=command.name,
                source="command",
                namespace=(capability_name,),
                description=command.description or f"Run {command.name}",
                parameters_schema=command.input_schema,
                fn=_command_runner(command, capability_root, workspace_root),
                catch=True,
                offload=False,
            )
        )
        loaded_names.add(command.name)
        component_health.append(
            {
                "kind": "tool",
                "name": command.name,
                "status": "ok",
                "detail": f"Verified command revision {command.tool_revision_id}",
            }
        )

    for name in declared.keys() - loaded_names:
        if not any(
            entry.get("kind") == "tool" and entry.get("name") == name for entry in component_health
        ):
            _record_health(component_health, name, "Missing registered command revision")
    return tools


def _record_health(health: list[dict[str, t.Any]], name: str, error: str) -> None:
    health.append(
        {
            "kind": "tool",
            "name": name,
            "status": "degraded",
            "error": error,
        }
    )


def _command_runner(
    command: ResolvedCommandTool, capability_root: Path, workspace_root: Path
) -> t.Callable[..., dict[str, t.Any]]:
    def execute(**inputs: t.Any) -> dict[str, t.Any]:
        return _execute_command(command, capability_root, workspace_root, inputs)

    return execute


def _working_directory(
    command: ResolvedCommandTool, capability_root: Path, workspace_root: Path
) -> Path:
    directory = capability_root if command.working_directory == "capability" else workspace_root
    resolved = directory.resolve()
    if not resolved.is_dir():
        raise CommandExecutionError("Configured command working directory is unavailable")
    return resolved


def _resolve_executable(command: ResolvedCommandTool, capability_root: Path) -> Path:
    executable = command.executable
    if Path(executable).is_absolute():
        candidate = Path(executable)
    elif "/" in executable or "\\" in executable:
        candidate = capability_root / executable
    else:
        resolved = shutil.which(executable)
        if resolved is None:
            raise CommandExecutionError("Configured command executable is unavailable")
        candidate = Path(resolved)
    try:
        candidate = candidate.resolve(strict=True)
    except OSError as exc:
        raise CommandExecutionError("Configured command executable is unavailable") from exc
    if candidate.name.lower() in SHELL_EXECUTABLE_NAMES:
        raise CommandExecutionError(
            "Configured command executable resolves to an unsupported shell"
        )
    if not candidate.is_file() or not os.access(candidate, os.X_OK):
        raise CommandExecutionError("Configured command executable is unavailable")
    return candidate


def _run_process(
    argv: list[str], cwd: Path, timeout_seconds: float
) -> tuple[int, bytes, bytes, bool]:
    deadline = time.monotonic() + timeout_seconds
    process = subprocess.Popen(  # noqa: S603 - argv is fixed and shell execution is never used
        argv,
        cwd=cwd,
        env={},
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,
    )
    assert process.stdout is not None
    assert process.stderr is not None
    streams = (process.stdout, process.stderr)
    captures = (bytearray(), bytearray())
    truncated = [False, False]
    timed_out = False
    selector = selectors.DefaultSelector()
    try:
        for index, stream in enumerate(streams):
            os.set_blocking(stream.fileno(), False)
            selector.register(stream, selectors.EVENT_READ, index)

        while selector.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                timed_out = True
                break
            ready = selector.select(remaining)
            if not ready:
                timed_out = True
                break
            for key, _events in ready:
                index: int = key.data
                try:
                    chunk = os.read(key.fd, 8192)
                except BlockingIOError:
                    continue
                if not chunk:
                    selector.unregister(key.fileobj)
                    continue
                if truncated[index]:
                    continue
                capture = captures[index]
                capacity = _MAX_OUTPUT_BYTES - len(_TRUNCATED) - len(capture)
                capture.extend(chunk[:capacity])
                if len(chunk) > capacity:
                    capture.extend(_TRUNCATED)
                    truncated[index] = True

        if not timed_out:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                timed_out = True
            else:
                try:
                    process.wait(timeout=remaining)
                except subprocess.TimeoutExpired:
                    timed_out = True

        if timed_out:
            with contextlib.suppress(ProcessLookupError):
                os.killpg(process.pid, signal.SIGKILL)
    finally:
        selector.close()
        for stream in streams:
            stream.close()

    if timed_out:
        process.wait()
    assert process.returncode is not None
    return process.returncode, bytes(captures[0]), bytes(captures[1]), timed_out


def _verify_command(
    command: ResolvedCommandTool, capability_root: Path, workspace_root: Path
) -> Path:
    executable = _resolve_executable(command, capability_root)
    cwd = _working_directory(command, capability_root, workspace_root)
    try:
        exit_status, stdout, _stderr, timed_out = _run_process(
            [str(executable), *command.version_probe], cwd, command.timeout_seconds
        )
    except OSError as exc:
        raise CommandExecutionError("Configured command version probe failed") from exc
    if timed_out:
        raise CommandTimeoutError("Configured command version probe timed out")
    if exit_status != 0:
        raise CommandExecutionError("Configured command version probe failed")
    if stdout.decode(errors="replace").strip() != command.expected_version:
        raise CommandExecutionError("Configured command version does not match its revision")
    return executable


def _render_scalar(name: str, value: t.Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float) and math.isfinite(value):
        return str(value)
    raise CommandExecutionError(f"Command argument {name!r} must be a finite JSON scalar")


def _render_argv(command: ResolvedCommandTool, inputs: dict[str, t.Any]) -> list[str]:
    properties = command.input_schema.get("properties", {})
    undeclared = inputs.keys() - properties.keys()
    if undeclared:
        raise CommandExecutionError(
            f"Command arguments contain undeclared fields: {', '.join(sorted(undeclared))}"
        )
    rendered = {name: _render_scalar(name, value) for name, value in inputs.items()}
    errors = list(Draft202012Validator(command.input_schema).iter_errors(inputs))
    if errors:
        error = errors[0]
        field = ".".join(str(part) for part in error.absolute_path) or "<root>"
        raise CommandExecutionError(
            f"Command arguments failed JSON Schema validation at {field} ({error.validator})"
        )

    argv: list[str] = []
    formatter = string.Formatter()
    for template in command.argv:
        parts: list[str] = []
        for literal, field_name, _format_spec, _conversion in formatter.parse(template):
            parts.append(literal)
            if field_name is not None:
                if field_name not in rendered:
                    raise CommandExecutionError(f"Command argument {field_name!r} is missing")
                parts.append(rendered[field_name])
        argv.append("".join(parts))
    return argv


def _bounded_output(value: bytes) -> str:
    return value.decode(errors="replace")


def _record_execution(
    command: ResolvedCommandTool,
    state: t.Literal["start", "success", "failure", "timeout"],
    started_at: float,
    exit_status: int | None,
) -> None:
    logger.bind(
        tool_revision_id=str(command.tool_revision_id),
        lifecycle_state=state,
        duration_ms=round((time.perf_counter() - started_at) * 1000, 3),
        exit_status=exit_status,
    ).info("Command tool execution")


def _execute_command(
    command: ResolvedCommandTool,
    capability_root: Path,
    workspace_root: Path,
    inputs: dict[str, t.Any],
) -> dict[str, t.Any]:
    started_at = time.perf_counter()
    _record_execution(command, "start", started_at, None)
    try:
        executable = _verify_command(command, capability_root, workspace_root)
        argv = [str(executable), *_render_argv(command, inputs)]
        cwd = _working_directory(command, capability_root, workspace_root)
        exit_status, stdout, stderr, timed_out = _run_process(argv, cwd, command.timeout_seconds)
    except CommandTimeoutError:
        _record_execution(command, "timeout", started_at, None)
        raise
    except CommandExecutionError:
        _record_execution(command, "failure", started_at, None)
        raise
    except Exception as exc:
        _record_execution(command, "failure", started_at, None)
        raise CommandExecutionError("Command execution failed") from exc

    if timed_out:
        _record_execution(command, "timeout", started_at, exit_status)
        raise CommandTimeoutError("Command execution timed out")
    if exit_status != 0:
        _record_execution(command, "failure", started_at, exit_status)
        raise CommandExecutionError(f"Command execution failed with exit status {exit_status}")
    _record_execution(command, "success", started_at, exit_status)
    return {
        "exit_status": exit_status,
        "stdout": _bounded_output(stdout),
        "stderr": _bounded_output(stderr),
    }
