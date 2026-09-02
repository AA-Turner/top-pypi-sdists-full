"""Hook dispatch entrypoint shared by ``aiwatch hook`` and ``python -m runlayer_cli.hook``."""

from __future__ import annotations

import json
import os
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, NoReturn, cast

from runlayer_cli import __version__, flow_spool, flow_trace, regex_safe
from runlayer_cli.hook import hook_io, messages
from runlayer_cli.hook.clients import (
    Client,
    HookResponse,
    detect_client,
    normalize_event_name,
    should_noop_for_cursor,
    should_noop_for_devin,
)
from runlayer_cli.hook.file_policy import (
    FilePolicyViolation,
    check_bash_command,
    check_file_read,
)
from runlayer_cli.hook.log_silence import silence_hook_logging
from runlayer_cli.hook.mcp_lookup import (
    MCPServer,
    cline_cli_tool_resolves_mcp_source,
    github_copilot_cli_tool_resolves_mcp_source,
    is_github_copilot_cli_mcp_tool_name_shape,
    is_goose_mcp_extension,
    lookup_cline_cli_mcp_server,
    lookup_codex_mcp_server,
    lookup_devin_cli_mcp_server,
    lookup_gemini_cli_mcp_server,
    lookup_github_copilot_cli_mcp_server,
    lookup_goose_mcp_server,
    lookup_grok_cli_mcp_server,
    lookup_mcp_server,
    lookup_vscode_mcp_server,
    lookup_windsurf_mcp_server,
    resolve_cline_cli_mcp_tool,
    resolve_cursor_before_mcp_payload,
    resolve_gemini_cli_mcp_context,
    resolve_gemini_cli_mcp_tool,
    resolve_github_copilot_cli_mcp_source_from_payload,
    resolve_github_copilot_cli_mcp_tool,
    resolve_hermes_mcp_tool,
)
from runlayer_cli.hook.relay import (
    RelayError,
    check_tool_lifecycle,
    enforce,
    forward_event,
    forward_mcp_usage_metadata,
    forward_stop_event,
    forward_tool_lifecycle,
    start_transcript_stream,
)
from runlayer_cli.hook.windsurf_payload import adapt_windsurf_payload
from runlayer_cli.mdm_config import (
    AIWatchMode,
    resolve_install_hooks,
    resolve_mcp_usage_metadata_only,
    resolve_mode,
)
from runlayer_cli.skills.marker import (
    CANONICAL_BASE,
    SKILLS_DIR_MAP,
    managed_marker_skill_id,
)

_GOOSE_BUILTIN_LOCAL_EXTENSIONS = frozenset({"developer"})
_GOOSE_MASK_BLOCK_REASON = (
    "Tool output blocked by organization policy because Goose cannot apply "
    "Runlayer redactions."
)
_NO_ENFORCEMENT_ARG = "--no-enforcement"
_MODE_ARG = "--mode"
_CLINE_HASHED_MCP_TOOL_NAME = regex_safe.compile(r"[A-Za-z0-9_-]{55}_[0-9a-f]{8}")
_SKILL_NAME_RE = regex_safe.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def _write(s: str | None) -> None:
    if s:
        hook_io.write_stdout(s)


# Flow operation per normalized hook event (bounded cardinality; everything
# else is an observational event). Contract with the backend ingest allowlist
# (flow_trace.CLIENT_FLOW_OPERATIONS).
_HOOK_FLOW_OPERATIONS = {
    "PreToolUse": "cli.hook_pre_tool",
    "beforeMCPExecution": "cli.hook_pre_tool",
    "PermissionRequest": "cli.hook_pre_tool",
    "PostToolUse": "cli.hook_post_tool",
    "PostToolUseFailure": "cli.hook_post_tool",
    "Stop": "cli.hook_stop",
}


def _hook_operation(hook_type: str) -> str:
    return _HOOK_FLOW_OPERATIONS.get(hook_type, "cli.hook_event")


# Upper clamp for client-reported startup overhead: the stamp and this process
# share one machine clock, so anything past this is a clock step (NTP jump,
# suspend/resume), not a plausible process startup.
_STARTUP_CLAMP_MS = 60_000.0


def _record_startup_ms() -> None:
    """Fold the entry-path start stamp into the active flow as startup_ms.

    The stamp is epoch ms from the Go shim (IPC frame / fallback env var) or
    the thin client's module import, threaded here via HookIO. Clamped to
    [0, 60s] for clock sanity; no stamp means no startup_ms in the summary.
    """
    client_start_ms = hook_io.client_start_ms()
    if client_start_ms is None:
        return
    elapsed_ms = time.time() * 1000.0 - client_start_ms
    flow_trace.set_startup_ms(min(max(elapsed_ms, 0.0), _STARTUP_CLAMP_MS))


def _policy_violation(check: Callable[[], None]) -> FilePolicyViolation | None:
    """Run a local policy check inside a timed step; return the violation or None.

    Returns the violation instead of letting it cross the step boundary so a
    policy deny records as a normal step (an outcome, not a failure) and the
    flow stays status="ok".
    """
    with flow_trace.step("policy_check", kind="cpu"):
        try:
            check()
        except FilePolicyViolation as e:
            return e
    return None


def _deny_and_exit(resp: HookResponse, user_msg: str, agent_msg: str) -> NoReturn:
    # Windsurf blocks on 2 and shows stderr. Structured-output clients write
    # their native deny JSON; HookResponse owns whether that response also needs
    # a nonzero status (Grok does).
    stderr_msg = resp.deny_stderr(user_msg, agent_msg)
    if stderr_msg is not None:
        hook_io.write_stderr(stderr_msg + "\n")
        sys.exit(2)
    _write(resp.deny(user_msg, agent_msg))
    sys.exit(resp.deny_exit_code())


def _cursor_stop_session_end_payload(payload: dict[str, Any]) -> dict[str, Any]:
    reason = (
        payload.get("reason")
        or payload.get("stop_reason")
        or payload.get("status")
        or "completed"
    )
    return {**payload, "hook_event_name": "sessionEnd", "reason": reason}


def _nonempty_str(value: Any) -> str | None:
    if isinstance(value, str) and value:
        return value
    return None


def _first_nonempty_str(input_data: dict[str, Any], *fields: str) -> str | None:
    for field in fields:
        value = _nonempty_str(input_data.get(field))
        if value is not None:
            return value
    return None


def _adapt_cline_payload(input_data: dict[str, Any]) -> dict[str, Any]:
    adapted = dict(input_data)
    session_context = input_data.get("sessionContext")
    root_session_id = (
        session_context.get("rootSessionId")
        if isinstance(session_context, dict)
        else None
    )
    session_id = _nonempty_str(root_session_id) or _nonempty_str(
        input_data.get("taskId")
    )
    workspace_roots = input_data.get("workspaceRoots")
    cwd = (
        workspace_roots[0]
        if isinstance(workspace_roots, list) and workspace_roots
        else None
    )
    client_version = _nonempty_str(input_data.get("clineVersion"))

    if session_id is not None:
        adapted["session_id"] = session_id
    if isinstance(cwd, str) and cwd:
        adapted["cwd"] = cwd
    if client_version is not None:
        adapted["client_version"] = client_version

    tool_data = input_data.get("tool_call")
    is_result = not isinstance(tool_data, dict)
    if is_result:
        tool_data = input_data.get("tool_result")
    if isinstance(tool_data, dict):
        tool_name = _nonempty_str(tool_data.get("name"))
        tool_use_id = _nonempty_str(tool_data.get("id"))
        if tool_name is not None:
            adapted["tool_name"] = tool_name
        if isinstance(tool_data.get("input"), dict):
            adapted["tool_input"] = tool_data["input"]
        if tool_use_id is not None:
            adapted["tool_use_id"] = tool_use_id
        if is_result and "output" in tool_data:
            adapted["tool_output"] = tool_data["output"]
    return adapted


def _adapt_grok_payload(input_data: dict[str, Any]) -> dict[str, Any]:
    """Add the canonical snake_case fields used by the shared dispatcher."""
    adapted = dict(input_data)
    field_map = {
        "hookEventName": "hook_event_name",
        "sessionId": "session_id",
        "workspaceRoot": "workspace_root",
        "toolName": "tool_name",
        "toolInput": "tool_input",
        "toolUseId": "tool_use_id",
        "transcriptPath": "transcript_path",
        "toolOutput": "tool_output",
        "toolResult": "tool_response",
    }
    for source, target in field_map.items():
        if target not in adapted and source in input_data:
            adapted[target] = input_data[source]
    if not adapted.get("cwd") and isinstance(adapted.get("workspace_root"), str):
        adapted["cwd"] = adapted["workspace_root"]
    if "tool_response" not in adapted and "error" in input_data:
        adapted["tool_response"] = input_data["error"]
    return adapted


def _grok_cli_mcp_tool_name_shape(tool_name: str) -> bool:
    server_name, separator, mcp_tool_name = tool_name.partition("__")
    return bool(server_name and separator and mcp_tool_name)


def _is_mcp_tool(
    client: Client, tool_name: str, input_data: dict[str, Any] | None = None
) -> bool:
    if tool_name.startswith("mcp__"):
        return True
    if _is_goose_extension_tool(client, tool_name):
        return True
    # Cursor names MCP tools "MCP:<tool>" (e.g. MCP:searchJiraIssuesUsingJql),
    # not mcp__*. Match so they take the MCP path, not the local-tool path.
    if client == Client.CURSOR and tool_name.startswith("MCP:"):
        return True
    if client == Client.GITHUB_COPILOT_CLI:
        return github_copilot_cli_tool_resolves_mcp_source(tool_name, input_data)
    if client == Client.GEMINI_CLI:
        context_resolved = resolve_gemini_cli_mcp_context(input_data)
        return context_resolved is not None or tool_name.startswith("mcp_")
    if client == Client.CLINE_CLI:
        return cline_cli_tool_resolves_mcp_source(tool_name)
    if client == Client.GROK_CLI:
        return _grok_cli_mcp_tool_name_shape(tool_name)
    # Hermes namespaces MCP tools with a single-underscore ``mcp_`` prefix.
    return client == Client.HERMES and tool_name.startswith("mcp_")


def _is_goose_extension_tool(client: Client, tool_name: str) -> bool:
    if client != Client.GOOSE:
        return False
    extension_name = _goose_extension_name(tool_name)
    if not extension_name or extension_name in _GOOSE_BUILTIN_LOCAL_EXTENSIONS:
        return False
    mcp_extension = is_goose_mcp_extension(extension_name)
    return mcp_extension is not False


def _goose_extension_name(tool_name: str) -> str | None:
    extension_name, sep, tool = tool_name.partition("__")
    if not (extension_name and sep and tool):
        return None
    return extension_name


def _is_cline_mcp_tool_name_shape(tool_name: str) -> bool:
    server_name, separator, mcp_tool_name = tool_name.partition("__")
    return bool(
        (server_name and separator and mcp_tool_name)
        or _CLINE_HASHED_MCP_TOOL_NAME.fullmatch(tool_name)
    )


def _local_tool_name(client: Client, tool_name: str) -> str:
    extension_name = (
        _goose_extension_name(tool_name) if client == Client.GOOSE else None
    )
    if extension_name in _GOOSE_BUILTIN_LOCAL_EXTENSIONS:
        return tool_name.partition("__")[2]
    return tool_name


def _uses_configured_mcp_source(
    client: Client, tool_name: str, input_data: dict[str, Any] | None = None
) -> bool:
    if client == Client.GOOSE:
        return tool_name.startswith("mcp__") or _is_goose_extension_tool(
            client, tool_name
        )
    if client == Client.GITHUB_COPILOT_CLI:
        return tool_name.startswith(
            "mcp__"
        ) or github_copilot_cli_tool_resolves_mcp_source(
            tool_name,
            input_data,
        )
    if client == Client.CLINE_CLI:
        return _is_cline_mcp_tool_name_shape(tool_name)
    if client == Client.GROK_CLI:
        return _grok_cli_mcp_tool_name_shape(tool_name)
    if client in (
        Client.VSCODE,
        Client.CLAUDE_CODE,
        Client.CODEX,
        Client.WINDSURF,
        Client.WINDSURF,
        # Qwen names MCP tools ``mcp__<server>__<tool>`` like Claude Code. Names
        # over 63 chars (or carrying characters outside [A-Za-z0-9_-]) are
        # sanitized and truncated with a hash suffix, which cuts the TAIL — the
        # ``mcp__`` prefix always survives, so prefix matching stays correct even
        # for mangled names.
        Client.QWEN_CODE,
        # Devin exposes MCP tools as ``mcp__<server>__<tool>``, the same shape
        # Claude Code uses, and matches permissions against that literal name.
        Client.DEVIN_CLI,
    ):
        return tool_name.startswith("mcp__")
    if client == Client.GEMINI_CLI:
        context_resolved = resolve_gemini_cli_mcp_context(input_data)
        return context_resolved is not None or tool_name.startswith("mcp_")
    return client == Client.HERMES and tool_name.startswith("mcp_")


def _configured_mcp_server_name(client: Client, tool_name: str) -> str:
    if client == Client.GROK_CLI:
        return tool_name.partition("__")[0]
    if client == Client.CLINE_CLI:
        # Never split on "__": Cline's transform is lossy (sha1 truncation) and
        # "__" is legal inside server/tool names. Resolve against known servers.
        resolved = resolve_cline_cli_mcp_tool(tool_name)
        return resolved[0] if resolved is not None else ""
    if client == Client.GOOSE and not tool_name.startswith("mcp__"):
        return tool_name.partition("__")[0]
    if client == Client.GITHUB_COPILOT_CLI and not tool_name.startswith("mcp__"):
        return ""
    if client == Client.GEMINI_CLI and not tool_name.startswith("mcp__"):
        # Sanitized ``mcp_<server>_<tool>`` has no unambiguous separator; the
        # dedicated resolver recovers the server name.
        return ""
    parts = tool_name.split("__")
    return parts[1] if len(parts) > 1 else ""


def _is_read_tool(tool_name: str) -> bool:
    return tool_name.lower() in {
        "beforereadfile",
        "read",
        "readfile",
        "read_file",
        "read_file_contents",
        "read_many_files",
        "readfilecontents",
        "readfilecontent",
    }


def _is_shell_tool(tool_name: str) -> bool:
    return tool_name.lower() in {
        "bash",
        "beforeshellexecution",
        "shell",
        "terminal",
        "runterminalcommand",
        "run_shell_command",
        "run_terminal_command",
        "run_terminal_cmd",
        "run_in_terminal",
        "runinterminal",
        # Qwen Code's built-in shell tool id.
        "run_shell_command",
        # Cline CLI's built-in shell tool id.
        "run_commands",
    }


def _tool_input_field(input_data: dict[str, Any], *fields: str) -> str:
    tool_input = _coerce_tool_input(input_data.get("tool_input"))
    for field in fields:
        value = tool_input.get(field)
        if isinstance(value, str):
            return value
    return ""


def _tool_input_paths(input_data: dict[str, Any]) -> list[str]:
    file_path = _tool_input_field(input_data, "file_path", "filePath", "path")
    paths = [file_path] if file_path else []
    tool_input = _coerce_tool_input(input_data.get("tool_input"))
    for field in ("paths", "include"):
        multiple_paths = tool_input.get(field)
        if isinstance(multiple_paths, list):
            paths.extend(path for path in multiple_paths if isinstance(path, str))
    return paths


def _check_file_reads(file_paths: list[str]) -> None:
    for file_path in file_paths:
        check_file_read(file_path)


def _mcp_cursor_request(
    *,
    client: Client,
    input_data: dict[str, Any],
    tool_name: str,
    server: MCPServer,
    mode: AIWatchMode,
) -> str:
    conversation_id = _first_nonempty_str(
        input_data,
        "conversation_id",
        "session_id",
        "transcript_id",
        "chat_id",
    ) or ("claude-code" if client == Client.CLAUDE_CODE else client.value)
    generation_id = (
        _first_nonempty_str(
            input_data,
            "generation_id",
            "tool_use_id",
            "request_id",
            "message_id",
        )
        or conversation_id
    )
    request: dict[str, Any] = {
        "hook_event_name": "beforeMCPExecution",
        "client": client.value,
        "conversation_id": conversation_id,
        "generation_id": generation_id,
        "tool_name": tool_name,
        "tool_input": input_data.get("tool_input"),
        "mode": mode.value,
    }
    server_name = server.get("name")
    if isinstance(server_name, str) and server_name.strip():
        request["mcp_server_name"] = server_name
    if "url" in server:
        request["url"] = server["url"]
    elif server.get("source"):
        # URL-less trusted sources (GitHub Copilot CLI built-ins, claude.ai
        # connectors): forward name + source for backend authorization.
        if not isinstance(server_name, str) or not server_name.strip():
            raise ValueError("source-tagged MCP server requires a nonblank name")
        request["mcp_server_source"] = server["source"]
        request["mcp_server_name"] = server_name
    else:
        request["command"] = server["command"]
    return json.dumps(request)


def _invalid_tool_response_and_exit(
    resp: HookResponse,
    *,
    tool_name: str,
    post_hook: bool,
    original_output: object = None,
) -> NoReturn:
    u, a = messages.tool_invalid_api_response(tool_name=tool_name)
    if post_hook:
        _write(
            resp.block_output(
                u,
                tool_name=tool_name,
                original_output=original_output,
            )
        )
        sys.exit(0)
    _deny_and_exit(resp, u, a)


def _coerce_tool_input(value: Any) -> dict[str, Any]:
    """Normalize ``tool_input`` to a dict (Codex PermissionRequest sends a JSON string)."""
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except (json.JSONDecodeError, ValueError):
            return {}
        if isinstance(parsed, dict):
            return parsed
    return {}


def _maybe_enrich_skill_payload(client: Client, input_data: dict[str, Any]) -> None:
    """Stamp ``skill_id`` (top-level) on Skill-tool payloads for managed installs."""
    try:
        if input_data.get("tool_name") != "Skill":
            return
        name = _coerce_tool_input(input_data.get("tool_input")).get("skill")
        if not isinstance(name, str) or not name:
            return
        if ":" in name or not _SKILL_NAME_RE.match(name) or ".." in name:
            return

        project_rel, global_rel = SKILLS_DIR_MAP.get(
            client.value, (CANONICAL_BASE, CANONICAL_BASE)
        )
        skill_dirs: list[Path] = []
        cwd = input_data.get("cwd") or hook_io.getcwd()
        if cwd:
            skill_dirs.append(Path(cwd) / project_rel / name)

        home = Path.home()
        global_skill_dir = home / global_rel / name
        skill_dirs.append(global_skill_dir)
        canonical_skill_dir = home / CANONICAL_BASE / name
        if canonical_skill_dir != global_skill_dir:
            skill_dirs.append(canonical_skill_dir)

        for skill_dir in skill_dirs:
            # The first existing dir is the copy the client actually resolves.
            # Never fall through past an unmanaged copy to a lower-priority
            # managed one — a shadowing local skill would borrow its badge.
            if not skill_dir.is_dir():
                continue
            skill_id = managed_marker_skill_id(skill_dir)
            if skill_id is not None:
                input_data["skill_id"] = skill_id
            return
    except Exception:
        return


def _parse_response_json(
    response_text: str,
    *,
    resp: HookResponse,
    tool_name: str,
    expected_key: str,
    post_hook: bool = False,
    original_output: object = None,
) -> dict[str, Any]:
    try:
        response_data = json.loads(response_text)
    except (json.JSONDecodeError, TypeError):
        _invalid_tool_response_and_exit(
            resp,
            tool_name=tool_name,
            post_hook=post_hook,
            original_output=original_output,
        )

    if not isinstance(response_data, dict) or expected_key not in response_data:
        _invalid_tool_response_and_exit(
            resp,
            tool_name=tool_name,
            post_hook=post_hook,
            original_output=original_output,
        )

    return response_data


def _validate_tool_lifecycle_response(
    response_data: dict[str, Any],
    *,
    target: str,
    resp: HookResponse,
    tool_name: str,
    original_output: object = None,
) -> None:
    if target == "tool-pre":
        permission = response_data.get("permission")
        if permission not in ("allow", "deny"):
            _invalid_tool_response_and_exit(
                resp,
                tool_name=tool_name,
                post_hook=False,
                original_output=original_output,
            )
    elif target == "tool-post":
        blocked = response_data.get("blocked")
        modified_output = response_data.get("modified_output")
        modified_output_is_invalid = modified_output is not None and not isinstance(
            modified_output, str
        )
        if not isinstance(blocked, bool) or modified_output_is_invalid:
            _invalid_tool_response_and_exit(
                resp,
                tool_name=tool_name,
                post_hook=True,
                original_output=original_output,
            )


def _check_tool_lifecycle(
    target: str,
    *,
    client: Client,
    resp: HookResponse,
    original_hook_type: str,
    tool_name: str,
    input_data: dict[str, Any],
    expected_key: str,
    debug: bool,
    mode: AIWatchMode | None = None,
) -> dict[str, Any]:
    try:
        mode_kwargs = {"mode": mode.value} if mode is not None else {}
        response_text = check_tool_lifecycle(
            target,
            client.value,
            original_hook_type,
            tool_name,
            input_data,
            debug=debug,
            **mode_kwargs,
        )
    except RelayError as e:
        # Infra denies exit before the error propagates through flow(), so
        # without mark_error the flow spools status="ok" and per-customer
        # failure alerting undercounts fail-closed blocks. Policy denies stay
        # status="ok" on purpose: intentional enforcement, not failure.
        # Auth failures (exit_code 1) are user-actionable, not an outage;
        # count them under their own error type.
        # ``override``: this handler exits the process, so what it marks IS
        # the flow's terminal outcome — it must replace a provisional mark
        # from earlier in the same flow (Protect's HookInfraFailOpen on an
        # enforce failure that then continued into this scanner call).
        if e.exit_code == 1:
            flow_trace.mark_error("HookAuthRequired", override=True)
            u, a = messages.tool_auth_required(tool_name=tool_name)
        else:
            flow_trace.mark_error("HookInfraDeny", override=True)
            u, a = messages.tool_api_unreachable(tool_name=tool_name, failure=e.failure)
        if target == "tool-post":
            _write(
                resp.block_output(
                    u,
                    tool_name=tool_name,
                    original_output=input_data.get("tool_response"),
                )
            )
            sys.exit(0)
        _deny_and_exit(resp, u, a)

    response_data = _parse_response_json(
        response_text,
        resp=resp,
        tool_name=tool_name,
        expected_key=expected_key,
        post_hook=target == "tool-post",
        original_output=input_data.get("tool_response"),
    )
    _validate_tool_lifecycle_response(
        response_data,
        target=target,
        resp=resp,
        tool_name=tool_name,
        original_output=input_data.get("tool_response"),
    )
    return response_data


def _resolve_mode() -> AIWatchMode:
    """Resolve endpoint mode while preserving the legacy hook contract.

    ``--mode`` carries the explicit operator setup mode. When absent,
    ``--no-enforcement`` remains the compatibility override for user-scope
    configs without a sibling ``runlayer-config.json`` shim.

    Frozen ``aiwatch hook`` reads managed ``Mode`` first, then falls back to
    legacy ``Enforcement``; managed configuration ignores command-line mode.

    Without either command-line selector, unfrozen hooks and frozen non-aiwatch
    binaries preserve the legacy ``sys.argv[0]``-adjacent config lookup and
    enforce-by-default behavior.
    """
    from runlayer_cli.runtime import is_frozen_aiwatch_bundle  # noqa: PLC0415

    if is_frozen_aiwatch_bundle():
        from runlayer_cli.mdm_config import read_managed_config  # noqa: PLC0415

        return resolve_mode(read_managed_config())

    argv = hook_io.argv()
    args = argv[1:]
    for index, arg in enumerate(args):
        value: str | None = None
        if arg == _MODE_ARG and index + 1 < len(args):
            value = args[index + 1]
        elif arg.startswith(f"{_MODE_ARG}="):
            value = arg.partition("=")[2]
        if value is not None:
            try:
                return AIWatchMode(value.strip().lower())
            except ValueError:
                break

    if _NO_ENFORCEMENT_ARG in args:
        return AIWatchMode.MONITOR

    config_dir = os.path.dirname(hook_io.abspath(argv[0]))
    config_file = os.path.join(config_dir, "runlayer-config.json")
    if not os.path.isfile(config_file):
        return AIWatchMode.ENFORCE
    try:
        with open(config_file, encoding="utf-8") as f:
            cfg = json.load(f)
    except (json.JSONDecodeError, OSError):
        return AIWatchMode.ENFORCE
    if not isinstance(cfg, dict):
        return AIWatchMode.ENFORCE
    if cfg.get("enforcement") is False:
        return AIWatchMode.MONITOR
    return AIWatchMode.ENFORCE


def _resolve_metadata_only() -> bool:
    """Enable the privacy profile only for the managed frozen AI Watch binary."""
    from runlayer_cli.runtime import is_frozen_aiwatch_bundle  # noqa: PLC0415

    return is_frozen_aiwatch_bundle() and resolve_mcp_usage_metadata_only()


def _resolve_scan_only() -> bool:
    """The managed profile wants no hooks at all; a firing hook is stale.

    Monitor + Sessions off + MCPUsageMetadata off is the scan-only fleet
    contract: the reconciler removes Runlayer hook entries, but until it runs
    (or if it can't) a leftover hook still fires. Nothing may leave the
    device in that state — the caller answers allow without relaying.
    """
    from runlayer_cli.runtime import is_frozen_aiwatch_bundle  # noqa: PLC0415

    return is_frozen_aiwatch_bundle() and not resolve_install_hooks()


def run_hook() -> None:
    """Hook entrypoint shared by ``aiwatch hook`` and ``python -m runlayer_cli.hook``."""
    # Hooks must never emit log output: stdout is the protocol channel and
    # clients treat any stderr as a hook error. Silence before anything logs.
    silence_hook_logging()

    argv = hook_io.argv()
    if len(argv) >= 2 and argv[1] in ("--version", "-v"):
        hook_io.write_stdout(f"aiwatch version {__version__}\n")
        sys.exit(0)

    client = detect_client()

    if should_noop_for_cursor(client):
        _write('{"permission":"allow"}')
        sys.exit(0)

    if should_noop_for_devin(client):
        # Devin treats exit 0 with no stdout as "continue"; the hook Devin
        # imported from another client's config is handled by Runlayer's own
        # ``--client devin-cli`` entry instead.
        sys.exit(0)

    env_hook_event_name = hook_io.getenv("HOOK_EVENT_NAME", "")
    if client == Client.GROK_CLI and not env_hook_event_name:
        env_hook_event_name = hook_io.getenv("GROK_HOOK_EVENT", "")

    try:
        raw_input = hook_io.read_stdin()
    except Exception:
        _deny_and_exit(
            HookResponse(client, env_hook_event_name or "PreToolUse"),
            messages.DEFAULT_USER_MSG,
            messages.stdin_read_failure(),
        )
        return

    try:
        input_data: dict[str, Any] = json.loads(raw_input) if raw_input else {}
    except json.JSONDecodeError:
        input_data = {}

    if client == Client.WINDSURF:
        # Cascade nests detail under tool_info and names the event
        # ``agent_action_name``; flatten before anything reads the payload.
        input_data = adapt_windsurf_payload(input_data)
    if client == Client.CLINE_CLI:
        input_data = _adapt_cline_payload(input_data)
    if client == Client.GROK_CLI:
        input_data = _adapt_grok_payload(input_data)

    hook_type = env_hook_event_name or input_data.get("hook_event_name", "")
    if not hook_type and client == Client.GOOSE:
        hook_type = input_data.get("event", "")
    if not hook_type and client == Client.CLINE_CLI:
        hook_type = input_data.get("hookName", "")
    if not hook_type:
        sys.exit(0)

    original_hook_type = hook_type
    hook_type = normalize_event_name(hook_type)
    if hook_type == "beforeMCPExecution" and client != Client.CURSOR:
        # Only Cursor emits this event. Promote fallback detections so the
        # request and response retain Cursor's enforcement contract.
        client = Client.CURSOR
    resp = HookResponse(client, hook_type)

    mode = _resolve_mode()
    metadata_only = _resolve_metadata_only()

    debug = hook_io.getenv("RUNLAYER_HOOK_DEBUG") == "1"

    if metadata_only:
        _handle_mcp_usage_metadata_only(
            hook_type=hook_type,
            original_hook_type=original_hook_type,
            client=client,
            resp=resp,
            input_data=input_data,
            debug=debug,
        )
        return

    if _resolve_scan_only():
        _write(resp.allow())
        return

    # Flow tracing: summaries spool to disk (never stdout — that's the hook
    # protocol channel) and the next invocation's `event` POST delivers them
    # (see flow_spool). RUNLAYER_FLOW_TRACE=0 disables. The flow emits even on
    # the sys.exit() deny/allow paths (SystemExit unwinds the `with`).
    flow_trace.enable_flow_tracing(flow_spool.spool_append)

    with flow_trace.flow(_hook_operation(hook_type)):
        flow_trace.set_session_id(_session_id_from_payload(input_data))
        # The entry-path stamp (shim/thin client) covers what the flow timer
        # cannot: process exec, stdin read, and the IPC handoff before now.
        _record_startup_ms()
        if hook_io.is_daemon_served():
            # Flow timing starts inside run_hook(), so this marks the served
            # cohort but excludes thin-client startup and the IPC round trip;
            # startup_ms above carries that overhead for daemon requests too.
            flow_trace.marker("daemon_ipc")
        elif hook_io.is_daemon_fallback():
            # Includes version-skew drain windows: rollout spikes are expected;
            # sustained elevation indicates supervision failure.
            flow_trace.marker("daemon_fallback")
        _dispatch(
            hook_type=hook_type,
            original_hook_type=original_hook_type,
            client=client,
            resp=resp,
            input_data=input_data,
            raw_input=raw_input,
            debug=debug,
            mode=mode,
        )


@dataclass(frozen=True)
class _DispatchCtx:
    """Bundle of params each ``_handle_*`` registry entry receives."""

    hook_type: str
    original_hook_type: str
    client: Client
    resp: HookResponse
    input_data: dict[str, Any]
    raw_input: str
    mode: AIWatchMode
    debug: bool


def _handle_file_read(ctx: _DispatchCtx) -> None:
    if ctx.client == Client.WINDSURF:
        _handle_pre_tool_use(
            client=ctx.client,
            resp=ctx.resp,
            input_data=ctx.input_data,
            original_hook_type=ctx.original_hook_type,
            mode=ctx.mode,
            debug=ctx.debug,
        )
        return

    if ctx.mode is AIWatchMode.ENFORCE:
        file_path = ctx.input_data.get("file_path") or ctx.input_data.get(
            "matcher_context", ""
        )
        if not isinstance(file_path, str):
            file_path = ""
        violation = _policy_violation(lambda: check_file_read(file_path))
        if violation is not None:
            _deny_and_exit(ctx.resp, violation.user_msg, violation.agent_msg)

    forward_event(
        ctx.client.value, ctx.original_hook_type, ctx.input_data, debug=ctx.debug
    )
    _write(ctx.resp.allow())


def _handle_stop(ctx: _DispatchCtx) -> None:
    forward_stop_event(
        ctx.client.value, ctx.original_hook_type, ctx.input_data, debug=ctx.debug
    )
    if ctx.client == Client.CURSOR:
        # Session-end delivery stays synchronous like the stop event itself.
        forward_event(
            ctx.client.value,
            "sessionEnd",
            _cursor_stop_session_end_payload(ctx.input_data),
            debug=ctx.debug,
            defer=False,
        )
    _write(ctx.resp.allow())


def _handle_shell_execution(ctx: _DispatchCtx) -> None:
    if ctx.client == Client.WINDSURF:
        _handle_pre_tool_use(
            client=ctx.client,
            resp=ctx.resp,
            input_data=ctx.input_data,
            original_hook_type=ctx.original_hook_type,
            mode=ctx.mode,
            debug=ctx.debug,
        )
        return

    if ctx.mode is AIWatchMode.ENFORCE:
        shell_command = ctx.input_data.get("command") or ctx.input_data.get(
            "matcher_context", ""
        )
        if not isinstance(shell_command, str):
            shell_command = ""
        violation = _policy_violation(lambda: check_bash_command(shell_command))
        if violation is not None:
            _deny_and_exit(ctx.resp, violation.user_msg, violation.agent_msg)

    forward_event(
        ctx.client.value, ctx.original_hook_type, ctx.input_data, debug=ctx.debug
    )
    _write(ctx.resp.allow())


def _handle_permission_request(ctx: _DispatchCtx) -> None:
    if ctx.client == Client.CODEX and ctx.mode is AIWatchMode.ENFORCE:
        shell_command = _coerce_tool_input(ctx.input_data.get("tool_input")).get(
            "command", ""
        )
        violation = _policy_violation(lambda: check_bash_command(shell_command))
        if violation is not None:
            _deny_and_exit(ctx.resp, violation.user_msg, violation.agent_msg)

    forward_event(
        ctx.client.value, ctx.original_hook_type, ctx.input_data, debug=ctx.debug
    )
    _write(ctx.resp.allow())


def _handle_session_event(ctx: _DispatchCtx) -> None:
    if ctx.hook_type == "UserPromptSubmit" and ctx.client in (
        Client.CLAUDE_CODE,
        Client.CODEX,
    ):
        start_transcript_stream(ctx.client.value, ctx.input_data, debug=ctx.debug)
    forward_event(
        ctx.client.value, ctx.original_hook_type, ctx.input_data, debug=ctx.debug
    )
    _write(ctx.resp.allow())


def _handle_post_tool_use(ctx: _DispatchCtx) -> None:
    tool_name = ctx.input_data.get("tool_name", "") or ""
    _maybe_enrich_skill_payload(ctx.client, ctx.input_data)
    is_mcp_tool = _is_mcp_tool(ctx.client, tool_name, ctx.input_data)

    if ctx.client == Client.GROK_CLI:
        # Grok consumes decisions only for PreToolUse; post-hook output is ignored.
        if not is_mcp_tool or ctx.mode is AIWatchMode.PROTECT:
            forward_tool_lifecycle(
                "tool-post",
                ctx.client.value,
                ctx.original_hook_type,
                tool_name,
                ctx.input_data,
                debug=ctx.debug,
            )
        forward_event(
            ctx.client.value,
            ctx.original_hook_type,
            ctx.input_data,
            debug=ctx.debug,
        )
        _write(ctx.resp.observational())
        return

    if ctx.hook_type == "PostToolUseFailure" and ctx.client in (
        Client.CLAUDE_CODE,
        Client.GITHUB_COPILOT_CLI,
        Client.QWEN_CODE,
    ):
        # These clients cannot replace or suppress a failed tool's raw error.
        # Keep this surface observational instead of claiming Block/Mask applied.
        if not is_mcp_tool or ctx.mode is AIWatchMode.PROTECT:
            forward_tool_lifecycle(
                "tool-post",
                ctx.client.value,
                ctx.original_hook_type,
                tool_name,
                ctx.input_data,
                debug=ctx.debug,
            )
        forward_event(
            ctx.client.value,
            ctx.original_hook_type,
            ctx.input_data,
            debug=ctx.debug,
        )
        _write(ctx.resp.observational())
        return

    if ctx.client == Client.HERMES and ctx.original_hook_type == "post_tool_call":
        # Hermes ignores this return value. transform_tool_result immediately
        # follows and is the decision-capable output-replacement surface.
        if not is_mcp_tool:
            forward_tool_lifecycle(
                "tool-post",
                ctx.client.value,
                ctx.original_hook_type,
                tool_name,
                ctx.input_data,
                debug=ctx.debug,
            )
        forward_event(
            ctx.client.value, ctx.original_hook_type, ctx.input_data, debug=ctx.debug
        )
        _write(ctx.resp.observational())
        return

    if ctx.client == Client.DEVIN_CLI:
        # Devin consumes a decision only from PreToolUse; its PostToolUse hook is
        # documented as logging-only, so any block or mask emitted here would be
        # silently dropped rather than applied.
        if not is_mcp_tool or ctx.mode is AIWatchMode.PROTECT:
            forward_tool_lifecycle(
                "tool-post",
                ctx.client.value,
                ctx.original_hook_type,
                tool_name,
                ctx.input_data,
                debug=ctx.debug,
            )
        forward_event(
            ctx.client.value, ctx.original_hook_type, ctx.input_data, debug=ctx.debug
        )
        _write(ctx.resp.observational())
        return

    if is_mcp_tool and ctx.mode is not AIWatchMode.PROTECT:
        forward_event(
            ctx.client.value, ctx.original_hook_type, ctx.input_data, debug=ctx.debug
        )
        _write(ctx.resp.observational())
        return

    if ctx.mode is AIWatchMode.MONITOR:
        forward_tool_lifecycle(
            "tool-post",
            ctx.client.value,
            ctx.original_hook_type,
            tool_name,
            ctx.input_data,
            debug=ctx.debug,
        )
        forward_event(
            ctx.client.value, ctx.original_hook_type, ctx.input_data, debug=ctx.debug
        )
        _write(ctx.resp.observational())
        return

    forward_event(
        ctx.client.value, ctx.original_hook_type, ctx.input_data, debug=ctx.debug
    )
    response_data = _check_tool_lifecycle(
        "tool-post",
        client=ctx.client,
        resp=ctx.resp,
        original_hook_type=ctx.original_hook_type,
        tool_name=tool_name,
        input_data=ctx.input_data,
        expected_key="blocked",
        debug=ctx.debug,
    )
    original_output = ctx.input_data.get("tool_response")
    if response_data.get("blocked") is True:
        if response_data.get("block_state") == "scan_unavailable":
            reason = messages.TOOL_OUTPUT_SCAN_UNAVAILABLE
        else:
            reason = _tool_output_block_reason(response_data)
        _write(
            ctx.resp.block_output(
                reason,
                tool_name=tool_name,
                original_output=original_output,
            )
        )
        return

    # Presence check (not truthiness) so masking to the empty string is applied.
    modified = response_data.get("modified_output")
    if isinstance(modified, str):
        masked = ctx.resp.mask_output(
            modified,
            tool_name=tool_name,
            original_output=original_output,
        )
        if masked is not None:
            _write(masked)
            return

        reason = (
            _GOOSE_MASK_BLOCK_REASON
            if ctx.client == Client.GOOSE
            else (
                "Tool output blocked by organization policy because this "
                "client cannot apply Runlayer output redactions."
            )
        )
        _write(
            ctx.resp.block_output(
                reason,
                tool_name=tool_name,
                original_output=original_output,
            )
        )
        return

    _write(ctx.resp.observational())


def _handle_unknown_event(ctx: _DispatchCtx) -> None:
    forward_event(
        ctx.client.value, ctx.original_hook_type, ctx.input_data, debug=ctx.debug
    )
    _write(ctx.resp.observational())


# Wires hook event names to handler callables. ``_handle_before_mcp_execution`` /
# ``_handle_pre_tool_use`` keep their explicit-kwargs signatures (covered by a
# dense test surface); a one-line lambda adapts them to the ``_DispatchCtx`` shape.
_DISPATCH_TABLE: dict[str, Callable[[_DispatchCtx], None]] = {
    "beforeMCPExecution": lambda ctx: _handle_before_mcp_execution(
        client=ctx.client,
        resp=ctx.resp,
        input_data=ctx.input_data,
        raw_input=ctx.raw_input,
        original_hook_type=ctx.original_hook_type,
        mode=ctx.mode,
        debug=ctx.debug,
    ),
    "PreToolUse": lambda ctx: _handle_pre_tool_use(
        client=ctx.client,
        resp=ctx.resp,
        input_data=ctx.input_data,
        original_hook_type=ctx.original_hook_type,
        debug=ctx.debug,
        mode=ctx.mode,
    ),
    "beforeReadFile": _handle_file_read,
    "BeforeReadFile": _handle_file_read,
    "beforeTabFileRead": _handle_file_read,
    "Stop": _handle_stop,
    "beforeShellExecution": _handle_shell_execution,
    "BeforeShellExecution": _handle_shell_execution,
    "PermissionRequest": _handle_permission_request,
    "SubagentStart": _handle_session_event,
    "UserPromptSubmit": _handle_session_event,
    "PostToolUse": _handle_post_tool_use,
    "PostToolUseFailure": _handle_post_tool_use,
}


def _dispatch(
    *,
    hook_type: str,
    original_hook_type: str,
    client: Client,
    resp: HookResponse,
    input_data: dict[str, Any],
    raw_input: str,
    mode: AIWatchMode,
    debug: bool,
) -> None:
    ctx = _DispatchCtx(
        hook_type=hook_type,
        original_hook_type=original_hook_type,
        client=client,
        resp=resp,
        input_data=input_data,
        raw_input=raw_input,
        mode=mode,
        debug=debug,
    )
    _DISPATCH_TABLE.get(hook_type, _handle_unknown_event)(ctx)


# Pre-call hook event names of the metadata-only install profile — the union
# of hook_install.clients._MCP_USAGE_METADATA_HOOKS, kept as a literal because
# that module imports yaml, which must stay off the hook hot path (drift is
# pinned by test_metadata_pre_call_events_match_install_profile). Post-call
# events from stale pipeline hooks must not observe: they'd double-count the
# call the pre hook already reported.
_MCP_USAGE_PRE_CALL_EVENTS = frozenset(
    {
        "BeforeTool",
        "PreToolUse",
        "beforeMCPExecution",
        "pre_mcp_tool_use",
        "pre_tool_call",
    }
)


def _mcp_usage_server_name(
    client: Client,
    tool_name: str,
    input_data: dict[str, Any],
) -> str | None:
    for key in ("mcp_server_name", "server_name"):
        value = input_data.get(key)
        if isinstance(value, str) and value:
            return value
    if client == Client.CURSOR:
        cursor_server_name = _nonempty_str(input_data.get("command"))
        if cursor_server_name is not None:
            # Cursor appends ``::mcpScope:`` routing metadata to the config-key
            # name and prefixes profile-scoped servers with ``user-``;
            # mcp_lookup treats the prefixed and bare names as the same server,
            # so normalize both away — only the bare server name may leave the
            # device, and either artifact would fragment the aggregation key
            # the enforce path's rows use.
            bare = cursor_server_name.partition("::mcpScope:")[0]
            return bare.removeprefix("user-") or None
    try:
        if client == Client.GITHUB_COPILOT_CLI and not tool_name.startswith("mcp__"):
            resolved = resolve_github_copilot_cli_mcp_source_from_payload(
                tool_name,
                input_data,
            )
            return resolved[0] if resolved is not None else None
        if client == Client.GEMINI_CLI:
            resolved = resolve_gemini_cli_mcp_context(input_data)
            if resolved is not None:
                return resolved[0]
        if client == Client.HERMES:
            resolved = resolve_hermes_mcp_tool(tool_name)
            if resolved is not None:
                return resolved[0]
        return _configured_mcp_server_name(client, tool_name) or None
    except Exception:
        return None


def _handle_mcp_usage_metadata_only(
    *,
    hook_type: str,
    original_hook_type: str,
    client: Client,
    resp: HookResponse,
    input_data: dict[str, Any],
    debug: bool,
) -> None:
    """Observe an MCP attempt without relaying or persisting hook contents."""
    raw_tool_name = input_data.get("tool_name")
    tool_name = raw_tool_name if isinstance(raw_tool_name, str) else ""
    is_pre_call = (
        hook_type in _MCP_USAGE_PRE_CALL_EVENTS
        or original_hook_type in _MCP_USAGE_PRE_CALL_EVENTS
    )
    is_mcp = (
        hook_type == "beforeMCPExecution"
        or original_hook_type == "pre_mcp_tool_use"
        or _is_mcp_tool(client, tool_name, input_data)
        or _uses_configured_mcp_source(client, tool_name, input_data)
    )
    # Allow before the best-effort send: with no daemon seam the send falls
    # back to a bounded synchronous POST, and observation must never sit in
    # front of the tool call — clients that stream the response proceed
    # immediately; exit-waiting clients at worst see the same window.
    _write(resp.allow())
    if is_pre_call and is_mcp and tool_name:
        forward_mcp_usage_metadata(
            client_name=client.value,
            tool_name=tool_name,
            mcp_server_name=_mcp_usage_server_name(client, tool_name, input_data),
            debug=debug,
        )


def _mcp_enforce_and_respond(
    *,
    client: Client,
    resp: HookResponse,
    input_data: dict[str, Any],
    original_hook_type: str,
    enforce_payload: str,
    mode: AIWatchMode,
    debug: bool,
    tool_name: str = "",
    make_allow_response: Callable[[str | None], str | None],
    defer_protect_allow: bool = False,
) -> bool:
    """Run MCP source governance.

    Returns whether a configured-MCP caller should continue into Protect's
    scanner tool-pre path. Cursor's dedicated ``beforeMCPExecution`` hook leaves
    ``defer_protect_allow`` false and receives its allow response immediately.
    """

    def _allow_protect_failure() -> bool:
        if defer_protect_allow:
            return True
        forward_event(client.value, original_hook_type, input_data, debug=debug)
        _write(make_allow_response(None))
        return False

    if mode is AIWatchMode.MONITOR:
        forward_event(client.value, original_hook_type, input_data, debug=debug)
        _write(make_allow_response(None))
        return False

    try:
        response_text = enforce(enforce_payload, debug=debug)
    except RelayError as e:
        # Three distinct operational states for failure alerting (marked here
        # because the deny exits before flow() would see the error): missing
        # credentials, Protect's by-design fail-open allow, and the
        # fail-closed infra deny.
        if e.exit_code == 1:
            flow_trace.mark_error("HookAuthRequired")
        elif mode is AIWatchMode.PROTECT:
            flow_trace.mark_error("HookInfraFailOpen")
        else:
            flow_trace.mark_error("HookInfraDeny")
        if mode is AIWatchMode.PROTECT:
            return _allow_protect_failure()
        if e.exit_code == 1:
            u, a = messages.auth_required(tool_name=tool_name)
        else:
            u, a = messages.api_unreachable(tool_name=tool_name, failure=e.failure)
        _deny_and_exit(resp, u, a)

    try:
        response_data = json.loads(response_text)
    except (json.JSONDecodeError, TypeError):
        if mode is AIWatchMode.PROTECT:
            return _allow_protect_failure()
        u, a = messages.invalid_api_response(tool_name=tool_name)
        _deny_and_exit(resp, u, a)

    if not isinstance(response_data, dict) or "permission" not in response_data:
        if mode is AIWatchMode.PROTECT:
            return _allow_protect_failure()
        u, a = messages.invalid_api_response(tool_name=tool_name)
        _deny_and_exit(resp, u, a)

    if mode is AIWatchMode.PROTECT:
        # An org-key request can be upgraded server-side to its authoritative
        # Enforce posture. Both known acknowledgements are safe to honor;
        # missing or unknown acknowledgements retain Protect's version-skew
        # fail-open behavior.
        if response_data.get("evaluated_mode") not in (
            AIWatchMode.PROTECT.value,
            AIWatchMode.ENFORCE.value,
        ) or response_data.get("permission") not in ("allow", "deny"):
            return _allow_protect_failure()

        if response_data["permission"] == "deny":
            forward_event(client.value, original_hook_type, input_data, debug=debug)
            reason = response_data.get(
                "user_message", "MCP execution blocked by organization policy"
            )
            u, a = messages.mcp_denied_by_policy(reason)
            _deny_and_exit(resp, u, a)

        if defer_protect_allow:
            return True
        forward_event(client.value, original_hook_type, input_data, debug=debug)
        _write(make_allow_response(response_text))
        return False

    forward_event(client.value, original_hook_type, input_data, debug=debug)

    if response_data.get("permission", "allow") == "deny":
        reason = response_data.get(
            "user_message", "MCP execution blocked by organization policy"
        )
        u, a = messages.mcp_denied_by_policy(reason)
        _deny_and_exit(resp, u, a)

    _write(make_allow_response(response_text))
    return False


def _cursor_before_mcp_allow_response(response_text: str | None) -> str:
    if response_text is None:
        return '{"permission":"allow"}'

    response_data = json.loads(response_text)
    safe_response = {
        key: value
        for key, value in response_data.items()
        if key != "evaluated_mode" and value is not None
    }
    return json.dumps(safe_response)


def _handle_before_mcp_execution(
    *,
    client: Client,
    resp: HookResponse,
    input_data: dict[str, Any],
    raw_input: str,
    original_hook_type: str,
    mode: AIWatchMode,
    debug: bool,
) -> None:
    enforce_payload_str = ""
    if mode is not AIWatchMode.MONITOR:
        enforce_payload = dict(input_data)
        ti = enforce_payload.get("tool_input")
        if isinstance(ti, dict):
            try:
                enforce_payload["tool_input"] = json.dumps(ti)
            except (TypeError, ValueError):
                if mode is AIWatchMode.PROTECT:
                    forward_event(
                        client.value,
                        original_hook_type,
                        input_data,
                        debug=debug,
                    )
                    _write(_cursor_before_mcp_allow_response(None))
                    return
                _deny_and_exit(
                    resp,
                    messages.DEFAULT_USER_MSG,
                    messages.serialize_tool_input_failure(),
                )

        try:
            if client == Client.CURSOR:
                enforce_payload = resolve_cursor_before_mcp_payload(enforce_payload)
                enforce_payload["client"] = Client.CURSOR.value
            enforce_payload["mode"] = mode.value
            enforce_payload_str = json.dumps(enforce_payload)
        except Exception:
            if mode is not AIWatchMode.PROTECT:
                raise
            forward_event(
                client.value,
                original_hook_type,
                input_data,
                debug=debug,
            )
            _write(_cursor_before_mcp_allow_response(None))
            return

    _mcp_enforce_and_respond(
        client=client,
        resp=resp,
        input_data=input_data,
        original_hook_type=original_hook_type,
        enforce_payload=enforce_payload_str,
        mode=mode,
        debug=debug,
        make_allow_response=_cursor_before_mcp_allow_response,
    )


def _tool_input_block_reason(response_data: dict[str, Any]) -> str:
    return (
        response_data.get("block_reason")
        or response_data.get("user_message")
        or response_data.get("reason")
        or "Tool use blocked by organization policy"
    )


def _tool_output_block_reason(response_data: dict[str, Any]) -> str:
    reason = response_data.get("block_reason")
    if reason:
        return reason

    scan_results = response_data.get("scan_results") or []
    if isinstance(scan_results, list):
        for result in scan_results:
            if isinstance(result, dict) and result.get("scan_action") == "block":
                return (
                    result.get("reason")
                    or result.get("error")
                    or "Tool output blocked by organization policy"
                )

    return "Tool output blocked by organization policy"


def _session_id_from_payload(input_data: dict[str, Any]) -> str:
    for field in ("session_id", "conversation_id", "transcript_id", "chat_id"):
        value = input_data.get(field)
        if isinstance(value, str) and value:
            return value
    return ""


def _cursor_pre_allow_response(
    resp: HookResponse,
    input_data: dict[str, Any],
    response_data: dict[str, Any],
) -> str | None:
    session_id = _session_id_from_payload(input_data)
    tool_input: dict[str, Any] = _coerce_tool_input(input_data.get("tool_input"))
    modified_args = response_data.get("modified_args")
    has_modified_args = isinstance(modified_args, dict)
    if has_modified_args:
        tool_input = cast(dict[str, Any], modified_args)
    if has_modified_args and not session_id:
        return json.dumps({"permission": "allow", "updated_input": tool_input})
    return resp.allow_with_ids(tool_input, session_id)


def _local_pre_allow_response(
    client: Client,
    resp: HookResponse,
    input_data: dict[str, Any],
    response_data: dict[str, Any],
) -> str | None:
    if client == Client.CURSOR:
        return _cursor_pre_allow_response(resp, input_data, response_data)

    modified_args = response_data.get("modified_args")
    if isinstance(modified_args, dict):
        updated_input = resp.allow_with_updated_input(
            cast(dict[str, Any], modified_args)
        )
        if updated_input is None:
            reason = (
                "Tool use blocked because this client cannot apply Runlayer "
                "input redactions."
            )
            tool_name = input_data.get("tool_name", "")
            u, a = messages.tool_input_denied(
                reason,
                tool_name=tool_name if isinstance(tool_name, str) else "",
            )
            _deny_and_exit(resp, u, a)
        return updated_input

    return resp.allow()


def _scanner_pre_allow_response(
    client: Client,
    resp: HookResponse,
    input_data: dict[str, Any],
    response_data: dict[str, Any],
    *,
    mcp_tool: bool,
) -> str | None:
    if client == Client.CURSOR and mcp_tool:
        modified_args = response_data.get("modified_args")
        if isinstance(modified_args, dict):
            return json.dumps({"permission": "allow", "updated_input": modified_args})
        return '{"permission":"allow"}'
    return _local_pre_allow_response(client, resp, input_data, response_data)


def _allow_mcp_pretooluse(
    client: Client,
    resp: HookResponse,
    original_hook_type: str,
    input_data: dict[str, Any],
    debug: bool,
) -> None:
    forward_event(client.value, original_hook_type, input_data, debug=debug)
    if client == Client.CURSOR:
        # Cursor MCP tools are enforced and session-linked via
        # beforeMCPExecution (conversation_id). Do NOT inject
        # _runlayer_session_id into updated_input here — strict MCP arg schemas
        # (additionalProperties:false, e.g. Atlassian Jira) reject the extra
        # field client-side before the call reaches Runlayer.
        _write('{"permission":"allow"}')
    else:
        _write(resp.allow())


def _handle_local_tool_pre(
    *,
    client: Client,
    resp: HookResponse,
    input_data: dict[str, Any],
    original_hook_type: str,
    tool_name: str,
    mode: AIWatchMode,
    debug: bool,
    mcp_tool: bool = False,
) -> None:
    if mode is AIWatchMode.MONITOR:
        forward_tool_lifecycle(
            "tool-pre",
            client.value,
            original_hook_type,
            tool_name,
            input_data,
            debug=debug,
        )
        forward_event(client.value, original_hook_type, input_data, debug=debug)
        _write(
            _scanner_pre_allow_response(
                client,
                resp,
                input_data,
                {},
                mcp_tool=mcp_tool,
            )
        )
        return

    forward_event(client.value, original_hook_type, input_data, debug=debug)
    response_data = _check_tool_lifecycle(
        "tool-pre",
        client=client,
        resp=resp,
        original_hook_type=original_hook_type,
        tool_name=tool_name,
        input_data=input_data,
        expected_key="permission",
        debug=debug,
        mode=mode if mode is AIWatchMode.PROTECT else None,
    )

    permission = response_data.get("permission", "allow")
    if permission == "deny":
        reason = _tool_input_block_reason(response_data)
        if response_data.get("block_state") == "scan_unavailable":
            u, a = messages.tool_scan_unavailable(reason, tool_name=tool_name)
        else:
            u, a = messages.tool_input_denied(reason, tool_name=tool_name)
        _deny_and_exit(resp, u, a)

    _write(
        _scanner_pre_allow_response(
            client,
            resp,
            input_data,
            response_data,
            mcp_tool=mcp_tool,
        )
    )


def _handle_pre_tool_use(
    *,
    client: Client,
    resp: HookResponse,
    input_data: dict[str, Any],
    original_hook_type: str,
    mode: AIWatchMode,
    debug: bool,
) -> None:
    tool_name = input_data.get("tool_name", "") or ""
    _maybe_enrich_skill_payload(client, input_data)
    local_tool_name = _local_tool_name(client, tool_name)
    github_copilot_cli_resolved_mcp_tool: tuple[str, MCPServer] | None = None

    # MCP tool enforcement (Cursor uses beforeMCPExecution)
    if client == Client.GITHUB_COPILOT_CLI and not tool_name.startswith("mcp__"):
        github_copilot_cli_resolved_mcp_tool = (
            resolve_github_copilot_cli_mcp_source_from_payload(
                tool_name,
                input_data,
            )
        )
        uses_configured_mcp_source = (
            github_copilot_cli_resolved_mcp_tool is not None
            or is_github_copilot_cli_mcp_tool_name_shape(tool_name)
        )
    else:
        uses_configured_mcp_source = _uses_configured_mcp_source(
            client,
            tool_name,
            input_data,
        )

    if uses_configured_mcp_source:
        continue_to_scanner = _handle_configured_mcp_tool(
            client=client,
            resp=resp,
            input_data=input_data,
            tool_name=tool_name,
            original_hook_type=original_hook_type,
            mode=mode,
            debug=debug,
            github_copilot_cli_resolved_mcp_tool=(github_copilot_cli_resolved_mcp_tool),
        )
        if not continue_to_scanner:
            return
        _handle_local_tool_pre(
            client=client,
            resp=resp,
            input_data=input_data,
            original_hook_type=original_hook_type,
            tool_name=tool_name,
            mode=mode,
            debug=debug,
            mcp_tool=True,
        )
        return

    if _is_mcp_tool(client, tool_name, input_data):
        if mode is not AIWatchMode.PROTECT:
            _allow_mcp_pretooluse(
                client,
                resp,
                original_hook_type,
                input_data,
                debug,
            )
            return
        _handle_local_tool_pre(
            client=client,
            resp=resp,
            input_data=input_data,
            original_hook_type=original_hook_type,
            tool_name=tool_name,
            mode=mode,
            debug=debug,
            mcp_tool=True,
        )
        return

    if _is_read_tool(local_tool_name):
        if mode is AIWatchMode.ENFORCE:
            file_paths = _tool_input_paths(input_data)
            violation = _policy_violation(lambda: _check_file_reads(file_paths))
            if violation is not None:
                _deny_and_exit(resp, violation.user_msg, violation.agent_msg)

        _handle_local_tool_pre(
            client=client,
            resp=resp,
            input_data=input_data,
            original_hook_type=original_hook_type,
            tool_name=tool_name,
            mode=mode,
            debug=debug,
        )
        return

    if _is_shell_tool(local_tool_name):
        if mode is AIWatchMode.ENFORCE:
            bash_command = _tool_input_field(input_data, "command", "cmd")
            violation = _policy_violation(lambda: check_bash_command(bash_command))
            if violation is not None:
                _deny_and_exit(resp, violation.user_msg, violation.agent_msg)

        _handle_local_tool_pre(
            client=client,
            resp=resp,
            input_data=input_data,
            original_hook_type=original_hook_type,
            tool_name=tool_name,
            mode=mode,
            debug=debug,
        )
        return

    _handle_local_tool_pre(
        client=client,
        resp=resp,
        input_data=input_data,
        original_hook_type=original_hook_type,
        tool_name=tool_name,
        mode=mode,
        debug=debug,
    )


def _handle_configured_mcp_tool(
    *,
    client: Client,
    resp: HookResponse,
    input_data: dict[str, Any],
    tool_name: str,
    original_hook_type: str,
    mode: AIWatchMode,
    debug: bool,
    github_copilot_cli_resolved_mcp_tool: tuple[str, MCPServer] | None = None,
) -> bool:
    cursor_req = ""
    if mode is not AIWatchMode.MONITOR:
        cwd = input_data.get("cwd", "") or hook_io.getcwd()

        try:
            if client == Client.HERMES:
                resolved = resolve_hermes_mcp_tool(tool_name)
                server_name = resolved[0] if resolved is not None else ""
                server = resolved[1] if resolved is not None else None
            elif client == Client.GEMINI_CLI:
                context_resolved = resolve_gemini_cli_mcp_context(input_data)
                if context_resolved is not None:
                    server_name, server = context_resolved
                elif tool_name.startswith("mcp__"):
                    server_name = _configured_mcp_server_name(client, tool_name)
                    server = lookup_gemini_cli_mcp_server(server_name, cwd)
                else:
                    resolved = resolve_gemini_cli_mcp_tool(tool_name, cwd)
                    server_name = resolved[0] if resolved is not None else ""
                    server = resolved[1] if resolved is not None else None
            elif client == Client.GROK_CLI:
                server_name = _configured_mcp_server_name(client, tool_name)
                server = lookup_grok_cli_mcp_server(server_name, cwd)
            else:
                server_name = _configured_mcp_server_name(client, tool_name)
                if client == Client.CODEX:
                    server = lookup_codex_mcp_server(server_name)
                elif client == Client.CLINE_CLI:
                    server = lookup_cline_cli_mcp_server(server_name)
                elif client == Client.GOOSE:
                    server = lookup_goose_mcp_server(server_name)
                elif client == Client.VSCODE:
                    server = lookup_vscode_mcp_server(server_name, cwd)
                elif client == Client.WINDSURF:
                    server = lookup_windsurf_mcp_server(server_name, cwd)
                elif client == Client.DEVIN_CLI:
                    server = lookup_devin_cli_mcp_server(server_name, cwd)
                elif client == Client.GITHUB_COPILOT_CLI:
                    if tool_name.startswith("mcp__"):
                        server = lookup_github_copilot_cli_mcp_server(
                            server_name,
                            cwd,
                            input_data,
                        )
                    else:
                        resolved = github_copilot_cli_resolved_mcp_tool
                        if resolved is None:
                            resolved = resolve_github_copilot_cli_mcp_tool(
                                tool_name,
                                cwd,
                                input_data,
                            )
                        server_name = (
                            resolved[0] if resolved is not None else server_name
                        )
                        server = resolved[1] if resolved is not None else None
                else:
                    server = lookup_mcp_server(server_name, cwd)
        except Exception:
            if mode is AIWatchMode.PROTECT:
                return True
            raise
        if server is None:
            if mode is AIWatchMode.PROTECT:
                return True
            if client == Client.CODEX:
                settings_label = "Codex config"
                client_label = "Codex"
            elif client == Client.GOOSE:
                settings_label = "Goose config"
                client_label = "Goose"
            elif client == Client.VSCODE:
                settings_label = "VS Code MCP config"
                client_label = "VS Code"
            elif client == Client.WINDSURF:
                settings_label = "Windsurf MCP config"
                client_label = "Windsurf"
            elif client == Client.GITHUB_COPILOT_CLI:
                settings_label = "GitHub Copilot CLI MCP config"
                client_label = "GitHub Copilot CLI"
            elif client == Client.CLINE_CLI:
                settings_label = "Cline MCP settings"
                client_label = "Cline"
            elif client == Client.DEVIN_CLI:
                settings_label = "Devin CLI config"
                client_label = "Devin CLI"
            elif client == Client.HERMES:
                settings_label = "Hermes config"
                client_label = "Hermes"
                server_name = server_name or tool_name.removeprefix("mcp_")
            elif client == Client.GEMINI_CLI:
                settings_label = "Gemini CLI settings"
                client_label = "Gemini CLI"
                server_name = server_name or tool_name.removeprefix("mcp_")
            elif client == Client.GROK_CLI:
                settings_label = "Grok CLI config"
                client_label = "Grok CLI"
            else:
                settings_label = "Claude Code settings"
                client_label = "Claude Code"
            u, a = messages.mcp_server_not_registered(
                tool_name=tool_name,
                server_name=server_name,
                settings_label=settings_label,
                client_label=client_label,
            )
            _deny_and_exit(resp, u, a)

        try:
            cursor_req = _mcp_cursor_request(
                client=client,
                input_data=input_data,
                tool_name=tool_name,
                server=server,
                mode=mode,
            )
        except Exception as exc:
            if mode is AIWatchMode.PROTECT:
                return True
            if not isinstance(exc, (TypeError, ValueError)):
                raise
            u, a = messages.mcp_prepare_failure(tool_name=tool_name)
            _deny_and_exit(resp, u, a)

    return _mcp_enforce_and_respond(
        client=client,
        resp=resp,
        input_data=input_data,
        original_hook_type=original_hook_type,
        enforce_payload=cursor_req,
        mode=mode,
        debug=debug,
        tool_name=tool_name,
        # No stdout on configured-MCP allow (Claude/Codex/Hermes); matches bash shim.
        make_allow_response=lambda _rt: None,
        defer_protect_allow=True,
    )
