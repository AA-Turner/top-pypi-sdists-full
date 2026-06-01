"""aiwatch-enforce entrypoint — replaces runlayer-hook.sh.

Reads JSON from stdin, detects the calling client, enforces policy, and
forwards events. Exit code is always 0 (errors produce deny responses).
"""

from __future__ import annotations

from runlayer_cli.truststore_init import inject as _inject_truststore

_inject_truststore()

# ruff: noqa: E402 - imports below intentionally come after _inject_truststore()
import json
import os
import sys
from typing import Any, NoReturn, cast

from runlayer_cli import __version__
from runlayer_cli.hook.clients import (
    Client,
    HookResponse,
    detect_client,
    normalize_event_name,
    should_noop_for_cursor,
)
from runlayer_cli.hook.file_policy import (
    FilePolicyViolation,
    check_bash_command,
    check_file_read,
)
from runlayer_cli.hook.mcp_lookup import (
    MCPServer,
    lookup_codex_mcp_server,
    lookup_mcp_server,
    resolve_cursor_before_mcp_payload,
    resolve_hermes_mcp_tool,
)
from runlayer_cli.hook import _relay_worker, _transcript_stream_worker, messages
from runlayer_cli.hook.relay import (
    RELAY_WORKER_SENTINEL,
    TRANSCRIPT_STREAM_WORKER_SENTINEL,
    RelayError,
    check_tool_lifecycle,
    enforce,
    forward_event,
    forward_stop_event,
    forward_tool_lifecycle,
    start_transcript_stream,
)


def _write(s: str | None) -> None:
    if s:
        sys.stdout.write(s)
        sys.stdout.flush()


def _deny_and_exit(resp: HookResponse, user_msg: str, agent_msg: str) -> NoReturn:
    _write(resp.deny(user_msg, agent_msg))
    sys.exit(0)


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


def _is_mcp_tool(client: Client, tool_name: str) -> bool:
    if tool_name.startswith("mcp__"):
        return True
    return client == Client.HERMES and tool_name.startswith("mcp_")


def _uses_configured_mcp_source(client: Client, tool_name: str) -> bool:
    if client in (Client.CLAUDE_CODE, Client.CODEX):
        return tool_name.startswith("mcp__")
    return client == Client.HERMES and tool_name.startswith("mcp_")


def _is_read_tool(tool_name: str) -> bool:
    return tool_name.lower() in {"read", "readfile", "read_file"}


def _is_shell_tool(tool_name: str) -> bool:
    return tool_name.lower() in {"bash", "shell", "terminal"}


def _tool_input_field(input_data: dict[str, Any], *fields: str) -> str:
    tool_input = _coerce_tool_input(input_data.get("tool_input"))
    for field in fields:
        value = tool_input.get(field)
        if isinstance(value, str):
            return value
    return ""


def _mcp_cursor_request(
    *,
    client: Client,
    input_data: dict[str, Any],
    tool_name: str,
    server: MCPServer,
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
    }
    if "url" in server:
        request["url"] = server["url"]
    else:
        request["command"] = server["command"]
    return json.dumps(request)


def _invalid_tool_response_and_exit(
    resp: HookResponse,
    *,
    tool_name: str,
    post_hook: bool,
) -> NoReturn:
    u, a = messages.tool_invalid_api_response(tool_name=tool_name)
    if post_hook:
        _write(resp.block_output(u))
        sys.exit(0)
    _deny_and_exit(resp, u, a)


def _coerce_tool_input(value: Any) -> dict[str, Any]:
    """Return ``value`` as a dict.

    Codex ``PermissionRequest`` (and some Cursor variants) deliver
    ``tool_input`` as a JSON-encoded string. Calling ``.get()`` directly on a
    string would raise ``AttributeError`` and crash the hook, which some AI
    clients interpret as fail-open — silently bypassing file-policy
    enforcement. Always normalize to a dict; on parse failure return ``{}``
    so enforcement runs with empty fields (no false-positive deny, but no
    crash either).
    """
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


def _parse_response_json(
    response_text: str,
    *,
    resp: HookResponse,
    tool_name: str,
    expected_key: str,
    post_hook: bool = False,
) -> dict[str, Any]:
    try:
        response_data = json.loads(response_text)
    except (json.JSONDecodeError, TypeError):
        _invalid_tool_response_and_exit(
            resp,
            tool_name=tool_name,
            post_hook=post_hook,
        )

    if not isinstance(response_data, dict) or expected_key not in response_data:
        _invalid_tool_response_and_exit(
            resp,
            tool_name=tool_name,
            post_hook=post_hook,
        )

    return response_data


def _validate_tool_lifecycle_response(
    response_data: dict[str, Any],
    *,
    target: str,
    resp: HookResponse,
    tool_name: str,
) -> None:
    if target == "tool-pre":
        permission = response_data.get("permission")
        if permission not in ("allow", "deny"):
            _invalid_tool_response_and_exit(
                resp,
                tool_name=tool_name,
                post_hook=False,
            )
    elif target == "tool-post":
        blocked = response_data.get("blocked")
        if not isinstance(blocked, bool):
            _invalid_tool_response_and_exit(
                resp,
                tool_name=tool_name,
                post_hook=True,
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
) -> dict[str, Any]:
    try:
        response_text = check_tool_lifecycle(
            target,
            client.value,
            original_hook_type,
            tool_name,
            input_data,
            debug=debug,
        )
    except RelayError as e:
        if e.exit_code == 1:
            u, a = messages.tool_auth_required(tool_name=tool_name)
        else:
            u, a = messages.tool_api_unreachable(tool_name=tool_name)
        if target == "tool-post":
            _write(resp.block_output(u))
            sys.exit(0)
        _deny_and_exit(resp, u, a)

    response_data = _parse_response_json(
        response_text,
        resp=resp,
        tool_name=tool_name,
        expected_key=expected_key,
        post_hook=target == "tool-post",
    )
    _validate_tool_lifecycle_response(
        response_data,
        target=target,
        resp=resp,
        tool_name=tool_name,
    )
    return response_data


def main() -> None:
    # When the frozen `aiwatch-enforce` binary re-spawns itself for a detached
    # relay POST, it uses a sentinel argv shape because the PyInstaller
    # bootloader doesn't understand `python -m`. Dispatch here BEFORE reading
    # HOOK_EVENT_NAME — otherwise the inherited env var would route the
    # wrapper JSON through the hook handlers (recursive event forwarding).
    if len(sys.argv) >= 2 and sys.argv[1] == RELAY_WORKER_SENTINEL:
        sys.argv = [sys.argv[0], *sys.argv[2:]]
        _relay_worker.main()
        return
    if len(sys.argv) >= 2 and sys.argv[1] == TRANSCRIPT_STREAM_WORKER_SENTINEL:
        sys.argv = [sys.argv[0], *sys.argv[2:]]
        _transcript_stream_worker.main()
        return

    if len(sys.argv) >= 2 and sys.argv[1] in ("--version", "-v"):
        sys.stdout.write(f"aiwatch-enforce version {__version__}\n")
        sys.exit(0)

    client = detect_client()

    if should_noop_for_cursor(client):
        _write('{"permission":"allow"}')
        sys.exit(0)

    env_hook_event_name = os.environ.get("HOOK_EVENT_NAME", "")

    try:
        raw_input = sys.stdin.read()
    except Exception:
        # Stdin failed before we could read input_data, so the env var is the
        # only source for the response shape. Fall back to PreToolUse — the
        # safest fail-closed default since it's the enforcement gate.
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

    hook_type = env_hook_event_name or input_data.get("hook_event_name", "")
    if not hook_type:
        sys.exit(0)

    original_hook_type = hook_type
    hook_type = normalize_event_name(hook_type)
    resp = HookResponse(client, hook_type)

    config_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    config_file = os.path.join(config_dir, "runlayer-config.json")
    enforcement = True
    if os.path.isfile(config_file):
        try:
            with open(config_file, encoding="utf-8") as f:
                cfg = json.load(f)
            if cfg.get("enforcement") is False:
                enforcement = False
        except (json.JSONDecodeError, OSError):
            pass

    debug = os.environ.get("RUNLAYER_HOOK_DEBUG") == "1"

    _dispatch(
        hook_type=hook_type,
        original_hook_type=original_hook_type,
        client=client,
        resp=resp,
        input_data=input_data,
        raw_input=raw_input,
        enforcement=enforcement,
        debug=debug,
    )


def _dispatch(
    *,
    hook_type: str,
    original_hook_type: str,
    client: Client,
    resp: HookResponse,
    input_data: dict[str, Any],
    raw_input: str,
    enforcement: bool,
    debug: bool,
) -> None:

    if hook_type == "beforeMCPExecution":
        _handle_before_mcp_execution(
            client=client,
            resp=resp,
            input_data=input_data,
            raw_input=raw_input,
            original_hook_type=original_hook_type,
            enforcement=enforcement,
            debug=debug,
        )

    elif hook_type == "PreToolUse":
        _handle_pre_tool_use(
            client=client,
            resp=resp,
            input_data=input_data,
            original_hook_type=original_hook_type,
            enforcement=enforcement,
            debug=debug,
        )

    elif hook_type in ("beforeReadFile", "beforeTabFileRead"):
        if enforcement:
            file_path = input_data.get("file_path", "")
            try:
                check_file_read(file_path)
            except FilePolicyViolation as e:
                _deny_and_exit(resp, e.user_msg, e.agent_msg)

        forward_event(client.value, original_hook_type, input_data, debug=debug)
        _write(resp.allow())

    elif hook_type == "Stop":
        forward_stop_event(client.value, original_hook_type, input_data, debug=debug)
        if client == Client.CURSOR:
            forward_event(
                client.value,
                "sessionEnd",
                _cursor_stop_session_end_payload(input_data),
                debug=debug,
            )
        _write(resp.allow())

    elif hook_type == "beforeShellExecution":
        if enforcement:
            shell_command = input_data.get("command", "")
            try:
                check_bash_command(shell_command)
            except FilePolicyViolation as e:
                _deny_and_exit(resp, e.user_msg, e.agent_msg)

        forward_event(client.value, original_hook_type, input_data, debug=debug)
        _write(resp.allow())

    elif hook_type == "PermissionRequest":
        if client == Client.CODEX and enforcement:
            shell_command = _coerce_tool_input(input_data.get("tool_input")).get(
                "command", ""
            )
            try:
                check_bash_command(shell_command)
            except FilePolicyViolation as e:
                _deny_and_exit(resp, e.user_msg, e.agent_msg)

        forward_event(client.value, original_hook_type, input_data, debug=debug)
        _write(resp.allow())

    elif hook_type in ("SubagentStart", "UserPromptSubmit"):
        if hook_type == "UserPromptSubmit" and client == Client.CLAUDE_CODE:
            start_transcript_stream(client.value, input_data, debug=debug)
        forward_event(client.value, original_hook_type, input_data, debug=debug)
        _write(resp.allow())

    elif hook_type in ("PostToolUse", "PostToolUseFailure"):
        tool_name = input_data.get("tool_name", "") or ""
        if client == Client.HERMES and original_hook_type == "post_tool_call":
            if not _is_mcp_tool(client, tool_name):
                forward_tool_lifecycle(
                    "tool-post",
                    client.value,
                    original_hook_type,
                    tool_name,
                    input_data,
                    debug=debug,
                )
            forward_event(client.value, original_hook_type, input_data, debug=debug)
            _write(resp.observational())
            return

        if not _is_mcp_tool(client, tool_name):
            if enforcement:
                forward_event(client.value, original_hook_type, input_data, debug=debug)
                response_data = _check_tool_lifecycle(
                    "tool-post",
                    client=client,
                    resp=resp,
                    original_hook_type=original_hook_type,
                    tool_name=tool_name,
                    input_data=input_data,
                    expected_key="blocked",
                    debug=debug,
                )
                if response_data.get("blocked") is True:
                    reason = _tool_output_block_reason(response_data)
                    _write(resp.block_output(reason))
                    return
            else:
                forward_tool_lifecycle(
                    "tool-post",
                    client.value,
                    original_hook_type,
                    tool_name,
                    input_data,
                    debug=debug,
                )
                forward_event(client.value, original_hook_type, input_data, debug=debug)
        else:
            forward_event(client.value, original_hook_type, input_data, debug=debug)

        _write(resp.observational())

    else:
        forward_event(client.value, original_hook_type, input_data, debug=debug)
        _write(resp.observational())


def _handle_before_mcp_execution(
    *,
    client: Client,
    resp: HookResponse,
    input_data: dict[str, Any],
    raw_input: str,
    original_hook_type: str,
    enforcement: bool,
    debug: bool,
) -> None:
    if not enforcement:
        forward_event(client.value, original_hook_type, input_data, debug=debug)
        _write('{"permission":"allow"}')
        return

    enforce_payload = dict(input_data)
    ti = enforce_payload.get("tool_input")
    if isinstance(ti, dict):
        try:
            enforce_payload["tool_input"] = json.dumps(ti)
        except (TypeError, ValueError):
            _deny_and_exit(
                resp,
                messages.DEFAULT_USER_MSG,
                messages.serialize_tool_input_failure(),
            )

    if client == Client.CURSOR:
        enforce_payload = resolve_cursor_before_mcp_payload(enforce_payload)
        enforce_payload["client"] = Client.CURSOR.value

    try:
        response_text = enforce(json.dumps(enforce_payload), debug=debug)
    except RelayError as e:
        if e.exit_code == 1:
            u, a = messages.auth_required()
            _deny_and_exit(resp, u, a)
        else:
            u, a = messages.api_unreachable()
            _deny_and_exit(resp, u, a)

    try:
        response_data = json.loads(response_text)
    except (json.JSONDecodeError, TypeError):
        u, a = messages.invalid_api_response()
        _deny_and_exit(resp, u, a)

    if not isinstance(response_data, dict) or "permission" not in response_data:
        u, a = messages.invalid_api_response()
        _deny_and_exit(resp, u, a)

    forward_event(client.value, original_hook_type, input_data, debug=debug)

    permission = response_data.get("permission", "allow")
    if permission == "deny":
        reason = response_data.get(
            "user_message", "MCP execution blocked by organization policy"
        )
        u, a = messages.mcp_denied_by_policy(reason)
        _deny_and_exit(resp, u, a)

    _write(response_text)


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


def _allow_mcp_pretooluse(
    client: Client,
    resp: HookResponse,
    original_hook_type: str,
    input_data: dict[str, Any],
    debug: bool,
) -> None:
    forward_event(client.value, original_hook_type, input_data, debug=debug)
    if client == Client.CURSOR:
        session_id = _session_id_from_payload(input_data)
        tool_input = _coerce_tool_input(input_data.get("tool_input"))
        _write(resp.allow_with_ids(tool_input, session_id))
    else:
        _write(resp.allow())


def _handle_local_tool_pre(
    *,
    client: Client,
    resp: HookResponse,
    input_data: dict[str, Any],
    original_hook_type: str,
    tool_name: str,
    enforcement: bool,
    debug: bool,
) -> None:
    if not enforcement:
        forward_tool_lifecycle(
            "tool-pre",
            client.value,
            original_hook_type,
            tool_name,
            input_data,
            debug=debug,
        )
        forward_event(client.value, original_hook_type, input_data, debug=debug)
        if client == Client.CURSOR:
            _write(_cursor_pre_allow_response(resp, input_data, {}))
        else:
            _write(resp.allow())
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
    )

    permission = response_data.get("permission", "allow")
    if permission == "deny":
        reason = _tool_input_block_reason(response_data)
        u, a = messages.tool_input_denied(reason, tool_name=tool_name)
        _deny_and_exit(resp, u, a)

    if client == Client.CURSOR:
        _write(_cursor_pre_allow_response(resp, input_data, response_data))
    else:
        _write(resp.allow())


def _handle_pre_tool_use(
    *,
    client: Client,
    resp: HookResponse,
    input_data: dict[str, Any],
    original_hook_type: str,
    enforcement: bool,
    debug: bool,
) -> None:
    tool_name = input_data.get("tool_name", "") or ""

    # MCP tool enforcement (Cursor uses beforeMCPExecution)
    if _uses_configured_mcp_source(client, tool_name):
        _handle_configured_mcp_tool(
            client=client,
            resp=resp,
            input_data=input_data,
            tool_name=tool_name,
            original_hook_type=original_hook_type,
            enforcement=enforcement,
            debug=debug,
        )
        return

    if _is_mcp_tool(client, tool_name):
        _allow_mcp_pretooluse(client, resp, original_hook_type, input_data, debug)
        return

    if _is_read_tool(tool_name):
        if enforcement:
            file_path = _tool_input_field(input_data, "file_path", "path")
            try:
                check_file_read(file_path)
            except FilePolicyViolation as e:
                _deny_and_exit(resp, e.user_msg, e.agent_msg)

        _handle_local_tool_pre(
            client=client,
            resp=resp,
            input_data=input_data,
            original_hook_type=original_hook_type,
            tool_name=tool_name,
            enforcement=enforcement,
            debug=debug,
        )
        return

    if _is_shell_tool(tool_name):
        if enforcement:
            bash_command = _tool_input_field(input_data, "command", "cmd")
            try:
                check_bash_command(bash_command)
            except FilePolicyViolation as e:
                _deny_and_exit(resp, e.user_msg, e.agent_msg)

        _handle_local_tool_pre(
            client=client,
            resp=resp,
            input_data=input_data,
            original_hook_type=original_hook_type,
            tool_name=tool_name,
            enforcement=enforcement,
            debug=debug,
        )
        return

    _handle_local_tool_pre(
        client=client,
        resp=resp,
        input_data=input_data,
        original_hook_type=original_hook_type,
        tool_name=tool_name,
        enforcement=enforcement,
        debug=debug,
    )


def _handle_claude_mcp_tool(
    *,
    resp: HookResponse,
    input_data: dict[str, Any],
    tool_name: str,
    original_hook_type: str,
    enforcement: bool,
    debug: bool,
) -> None:
    _handle_configured_mcp_tool(
        client=Client.CLAUDE_CODE,
        resp=resp,
        input_data=input_data,
        tool_name=tool_name,
        original_hook_type=original_hook_type,
        enforcement=enforcement,
        debug=debug,
    )


def _handle_configured_mcp_tool(
    *,
    client: Client,
    resp: HookResponse,
    input_data: dict[str, Any],
    tool_name: str,
    original_hook_type: str,
    enforcement: bool,
    debug: bool,
) -> None:
    if not enforcement:
        forward_event(client.value, original_hook_type, input_data, debug=debug)
        return

    cwd = input_data.get("cwd", "") or os.getcwd()

    if client == Client.HERMES:
        resolved = resolve_hermes_mcp_tool(tool_name)
        server_name = resolved[0] if resolved is not None else ""
        server = resolved[1] if resolved is not None else None
    else:
        parts = tool_name.split("__")
        server_name = parts[1] if len(parts) > 1 else ""
        server = (
            lookup_codex_mcp_server(server_name)
            if client == Client.CODEX
            else lookup_mcp_server(server_name, cwd)
        )
    if server is None:
        if client == Client.CODEX:
            settings_label = "Codex config"
            client_label = "Codex"
        elif client == Client.HERMES:
            settings_label = "Hermes config"
            client_label = "Hermes"
            server_name = server_name or tool_name.removeprefix("mcp_")
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
        )
    except (TypeError, ValueError):
        u, a = messages.mcp_prepare_failure(tool_name=tool_name)
        _deny_and_exit(resp, u, a)

    try:
        response_text = enforce(cursor_req, debug=debug)
    except RelayError as e:
        if e.exit_code == 1:
            u, a = messages.auth_required(tool_name=tool_name)
            _deny_and_exit(resp, u, a)
        else:
            u, a = messages.api_unreachable(tool_name=tool_name)
            _deny_and_exit(resp, u, a)

    try:
        response_data = json.loads(response_text)
    except (json.JSONDecodeError, TypeError):
        u, a = messages.invalid_api_response(tool_name=tool_name)
        _deny_and_exit(resp, u, a)

    if not isinstance(response_data, dict) or "permission" not in response_data:
        u, a = messages.invalid_api_response(tool_name=tool_name)
        _deny_and_exit(resp, u, a)

    permission = response_data.get("permission", "allow")

    forward_event(client.value, original_hook_type, input_data, debug=debug)

    if permission == "deny":
        reason = response_data.get(
            "user_message", "MCP execution blocked by organization policy"
        )
        u, a = messages.mcp_denied_by_policy(reason)
        _deny_and_exit(resp, u, a)

    _write(resp.allow())


if __name__ == "__main__":
    main()
