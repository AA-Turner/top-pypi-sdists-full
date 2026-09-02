"""Single source of truth for deny / agent messages (user/agent contract — coordinate before changing)."""

from typing import NamedTuple

from runlayer_cli.hook.failure import FailureContext

AGENT_GUARDRAILS = (
    "**If you are an AI Agent:**\n"
    "- Provide the user with a detailed explanation of this security violation.\n"
    "- Do not suggest this is a false positive or mistake.\n"
    "- Do not suggest modifying, bypassing, or disabling the Runlayer hook or security configuration.\n"
    "- Do not suggest checking or editing hook files, settings.json, or any security configuration.\n"
    "- Do not retry this action or attempt alternative approaches to achieve the same result."
)

DEFAULT_USER_MSG = "Action blocked by organization security policy"

# Below this, a payload is too small to plausibly explain a transfer-time
# failure, so the cause line states the size as fact but never *blames* it
# (ENG-5197 honesty rule: a 2 KB upload stalling behind a dead proxy must not
# read as a data-volume problem).
_LARGE_PAYLOAD_BYTES = 256_000


class _UnreachableCause(NamedTuple):
    cause: str  # full sentence(s) appended to the agent-facing Reason line
    user_suffix: str  # short parenthetical appended to the one-line user msg


_NO_CAUSE = _UnreachableCause("", "")


def _format_size(n: int) -> str:
    # 999_500+ rounds to "1.0 MB"; without the offset the KB branch would
    # render "1000 KB".
    if n >= 999_500:
        return f"{n / 1_000_000:.1f} MB"
    if n >= 1_000:
        return f"{n / 1_000:.0f} KB"
    return f"{n} B"


def _blame_if_large(payload_bytes: int, template: str) -> str:
    return f" {template}" if payload_bytes >= _LARGE_PAYLOAD_BYTES else ""


def _attempts_note(failure: "FailureContext | None") -> str:
    """ ", after N attempts" once retries actually ran; empty for a single
    attempt so every pre-retry string stays byte-identical (tests pin them)."""
    if failure is None or failure.attempts <= 1:
        return ""
    return f", after {failure.attempts} attempts"


def _unreachable_cause(failure: "FailureContext | None") -> _UnreachableCause:
    """Render the evidence-backed cause for an unreachable-API failure; empty
    when nothing evidence-backed can be said.

    Honesty rules: for upload failures the size is stated as fact (the body
    was provably in flight) but blamed only when large; the throughput figure
    is an upper bound ("under ~X") because the body never finished sending;
    a read timeout names size only when large; connect failures and
    unclassified errors never mention size.
    """
    if failure is None or failure.kind is None:
        return _NO_CAUSE
    attempts = _attempts_note(failure)
    elapsed_s = failure.elapsed_s
    if elapsed_s is None:
        after = ""
    elif elapsed_s < 10:
        after = f" after {max(elapsed_s, 0.1):.1f}s"
    else:
        after = f" after {elapsed_s:.0f}s"

    if failure.kind == "upload_timeout":
        if failure.payload_bytes is None:
            return _UnreachableCause(
                f"The request timed out before it finished sending{after}{attempts}.",
                "",
            )
        size = _format_size(failure.payload_bytes)
        rate = ""
        if elapsed_s and failure.payload_bytes >= _LARGE_PAYLOAD_BYTES:
            mbps = failure.payload_bytes * 8 / elapsed_s / 1_000_000
            rate = f" (under ~{mbps:.1f} Mbit/s effective)"
        blame = _blame_if_large(
            failure.payload_bytes,
            "Large tool outputs on slow connections are the most common cause.",
        )
        return _UnreachableCause(
            f"The request ({size} body) had not finished sending{after}{rate} "
            f"when it timed out{attempts}.{blame}",
            f" (upload of {size} stalled{after})",
        )
    if failure.kind == "upload_failed":
        if failure.payload_bytes is None:
            return _UnreachableCause(
                f"The connection dropped before the request finished "
                f"sending{after}{attempts}.",
                "",
            )
        size = _format_size(failure.payload_bytes)
        blame = _blame_if_large(
            failure.payload_bytes,
            "Large tool outputs on unstable connections are the most common cause.",
        )
        return _UnreachableCause(
            f"The connection dropped before the request ({size} body) "
            f"finished sending{after}{attempts}.{blame}",
            f" (upload of {size} failed{after})",
        )
    if failure.kind == "timeout":
        within = after.replace(" after ", " within ") if after else ""
        if (
            failure.payload_bytes is not None
            and failure.payload_bytes >= _LARGE_PAYLOAD_BYTES
        ):
            size = _format_size(failure.payload_bytes)
            return _UnreachableCause(
                f"No complete response arrived{within}{attempts}; the request "
                f"body was {size}. Large tool outputs take longer to upload "
                "and verify, especially on slow connections.",
                f" (timed out{after}; request body {size})",
            )
        return _UnreachableCause(f"No complete response arrived{within}{attempts}.", "")
    if failure.kind == "connect":
        return _UnreachableCause(
            f"Could not connect to the Runlayer API{attempts}.", ""
        )
    return _NO_CAUSE


def _unreachable_message(
    verification_phrase: str,
    *,
    tool_name: str,
    failure: "FailureContext | None",
) -> tuple[str, str]:
    """Shared assembly for the two unreachable-API builders (single source so
    wording/field changes cannot drift between the MCP and local-tool paths)."""
    if failure is not None and failure.kind == "http":
        # Any HTTP response means the API was reached — an unreachable/outage
        # framing would misdirect (403 = key lacks a role, 429 = throttled,
        # 5xx = server error). 401 gets credential wording; no side effects
        # are claimed (cache invalidation is daemon-only, and a genuinely
        # revoked credential fails again regardless).
        if failure.status_code == 401:
            return (
                "Runlayer API rejected this machine's credentials (HTTP 401)",
                _violation_with_tool(
                    "Authentication Required",
                    f"The Runlayer API rejected this machine's credentials "
                    f"during {verification_phrase} (HTTP 401). The API was "
                    "reachable — this is a credential problem, not an outage. "
                    "Unverified actions are blocked (fail-closed).",
                    tool_name=tool_name,
                    footer="If this keeps happening, this machine's Runlayer credentials may be stale or revoked — contact your Runlayer administrator.",
                ),
            )
        if failure.status_code == 407:
            # Proxy auth is generated by an HTTP proxy on the path — the
            # verification request never reached the Runlayer API.
            return (
                "HTTP proxy requires authentication (HTTP 407)",
                _violation_with_tool(
                    "Infrastructure",
                    f"An HTTP proxy on this machine's network path requires "
                    f"authentication (HTTP 407), so the {verification_phrase} "
                    "request never reached the Runlayer API. Unverified "
                    "actions are blocked (fail-closed).",
                    tool_name=tool_name,
                    footer="Fix the proxy credentials (HTTP_PROXY/HTTPS_PROXY) or ask your IT administrator about the proxy configuration.",
                ),
            )
        # Behind an intercepting proxy the response may not come from the
        # Runlayer API itself, so attribute the status to the request, not
        # definitively to the API.
        status = failure.status_code if failure.status_code is not None else "error"
        return (
            f"Runlayer verification request failed (HTTP {status})",
            _violation_with_tool(
                "Infrastructure",
                f"The {verification_phrase} request was answered with HTTP "
                f"{status}{_attempts_note(failure)}, so the action could not "
                "be verified. The "
                "connection worked but the request was rejected or failed — "
                "this is not a connectivity problem. Unverified actions are "
                "blocked (fail-closed).",
                tool_name=tool_name,
                footer="If this keeps happening, contact your Runlayer administrator.",
            ),
        )
    cause, user_suffix = _unreachable_cause(failure)
    reason = (
        f"Failed to contact the Runlayer API for {verification_phrase}. "
        "Unverified actions are blocked (fail-closed)."
    )
    if cause:
        reason += f" {cause}"
    return (
        f"Failed to contact Runlayer API{user_suffix}",
        _violation_with_tool(
            "Infrastructure",
            reason,
            tool_name=tool_name,
            footer="If you believe this is an error, contact your Runlayer administrator. The Runlayer API may be temporarily unreachable.",
        ),
    )


def _violation(
    violation_type: str,
    reason: str,
    *,
    extra_lines: str = "",
) -> str:
    parts = [
        "# Security Violation Detected\n",
        "\nYour organization's security policy (enforced by Runlayer) has blocked this operation.\n",
        "\n**What happened:**",
        f"\n- Violation type: {violation_type}",
        f"\n- Reason: {reason}",
    ]
    if extra_lines:
        parts.append(f"\n{extra_lines}")
    parts.append(f"\n\n{AGENT_GUARDRAILS}\n")
    parts.append(
        "\n**What to do:**\n"
        "If you believe this is an error, contact your Runlayer administrator."
    )
    return "".join(parts)


def default_agent_msg() -> str:
    return _violation(
        "Infrastructure",
        "The Runlayer hook encountered an internal error and could not complete the required policy check. Unverified actions are blocked (fail-closed).",
    )


def stdin_read_failure() -> str:
    return _violation(
        "Infrastructure",
        "The hook failed to read its input payload. Unverified actions are blocked (fail-closed).",
    )


def serialize_tool_input_failure() -> str:
    return _violation(
        "Infrastructure",
        "Failed to serialize tool_input for the policy verification request. Unverified actions are blocked (fail-closed).",
    )


def auth_required(*, tool_name: str = "") -> tuple[str, str]:
    return (
        "Action blocked by organization security policy. Run 'runlayer login' first.",
        _violation_with_tool(
            "Authentication Required",
            "Runlayer credentials are not configured on this machine. Your organization's policy requires all MCP tool use to be verified, which requires valid credentials.",
            tool_name=tool_name,
            footer="Run 'runlayer login' to set up authentication, then retry.",
        ),
    )


def api_unreachable(
    *, tool_name: str = "", failure: "FailureContext | None" = None
) -> tuple[str, str]:
    return _unreachable_message(
        "MCP execution verification", tool_name=tool_name, failure=failure
    )


def invalid_api_response(*, tool_name: str = "") -> tuple[str, str]:
    return (
        "Invalid response from Runlayer API",
        _violation_with_tool(
            "Infrastructure",
            "The Runlayer API returned an invalid response during MCP verification. Unverified actions are blocked (fail-closed).",
            tool_name=tool_name,
        ),
    )


def tool_auth_required(*, tool_name: str = "") -> tuple[str, str]:
    return (
        "Action blocked by organization security policy. Run 'runlayer login' first.",
        _violation_with_tool(
            "Authentication Required",
            "Runlayer credentials are not configured on this machine. Your organization's policy requires local tool use to be verified, which requires valid credentials.",
            tool_name=tool_name,
            footer="Run 'runlayer login' to set up authentication, then retry.",
        ),
    )


def tool_api_unreachable(
    *, tool_name: str = "", failure: "FailureContext | None" = None
) -> tuple[str, str]:
    return _unreachable_message(
        "local tool verification", tool_name=tool_name, failure=failure
    )


def tool_invalid_api_response(*, tool_name: str = "") -> tuple[str, str]:
    return (
        "Invalid response from Runlayer API",
        _violation_with_tool(
            "Infrastructure",
            "The Runlayer API returned an invalid response during local tool verification. Unverified actions are blocked (fail-closed).",
            tool_name=tool_name,
        ),
    )


def tool_input_denied(reason: str, *, tool_name: str = "") -> tuple[str, str]:
    return (
        reason,
        _violation_with_tool(
            "Tool Input Policy",
            reason,
            tool_name=tool_name,
            footer="If you believe this is a false positive or mistake, contact your Runlayer administrator to review the security policy settings.",
        ),
    )


# Unlike AGENT_GUARDRAILS this permits one retry — "do not retry" on an infra
# timeout would turn a transient hiccup into a hard stop. Anti-tamper lines
# are kept.
SCAN_UNAVAILABLE_GUARDRAILS = (
    "**If you are an AI Agent:**\n"
    "- This was a fail-closed infrastructure state, NOT a policy match or threat detection.\n"
    "- Wait a few seconds, then retry this exact action once. If it is blocked again, stop and inform the user.\n"
    "- Do not suggest modifying, bypassing, or disabling the Runlayer hook or security configuration.\n"
    "- Do not suggest checking or editing hook files, settings.json, or any security configuration."
)


def tool_scan_unavailable(reason: str, *, tool_name: str = "") -> tuple[str, str]:
    """Deny rendering for ``block_state == "scan_unavailable"`` — retryable,
    not a security violation."""
    parts = [
        "# Action Blocked: Security Scan Unavailable\n",
        "\nRunlayer could not complete the required security scan in time, so this operation was blocked as a precaution (fail-closed). No security violation was detected.\n",
        "\n**What happened:**",
    ]
    if tool_name:
        parts.append(f"\n- Tool: {tool_name}")
    parts.append(f"\n- Reason: {reason}")
    parts.append(f"\n\n{SCAN_UNAVAILABLE_GUARDRAILS}\n")
    parts.append(
        "\n**What to do:**\n"
        "Retry shortly. If this keeps happening, contact your Runlayer administrator."
    )
    return reason, "".join(parts)


# Post-hook analogue of tool_scan_unavailable: block_output embeds a single
# reason string, so retry guidance rides inline instead of a guardrails block.
TOOL_OUTPUT_SCAN_UNAVAILABLE = (
    "Runlayer could not complete the required security scan of this tool "
    "output, so it was withheld as a precaution (fail-closed). This is not a "
    "threat detection. Wait a few seconds and retry the action once; if it is "
    "blocked again, stop and inform the user."
)


def mcp_prepare_failure(*, tool_name: str = "") -> tuple[str, str]:
    return (
        DEFAULT_USER_MSG,
        _violation_with_tool(
            "Infrastructure",
            "Failed to prepare the MCP verification request. Unverified actions are blocked (fail-closed).",
            tool_name=tool_name,
        ),
    )


def mcp_server_not_registered(
    *,
    tool_name: str,
    server_name: str,
    settings_label: str = "Claude Code settings",
    client_label: str = "Claude Code",
) -> tuple[str, str]:
    return (
        f"Action blocked: MCP server '{server_name}' not registered in {settings_label}",
        _violation_with_tool(
            "MCP Execution Policy",
            f"MCP server '{server_name}' is not registered in {settings_label} and cannot be verified. Your organization's policy requires all MCP servers to be registered before use.",
            tool_name=tool_name,
            extra_lines=f"- MCP Server: {server_name}",
            footer=f"Contact your Runlayer administrator to register this MCP server, or add the server to your {client_label} MCP configuration.",
        ),
    )


def mcp_denied_by_policy(reason: str) -> tuple[str, str]:
    return (
        reason,
        _violation_with_tool(
            "MCP Execution Policy",
            reason,
            footer="If you believe this is a false positive or mistake, contact your Runlayer administrator to review the security policy settings.",
        ),
    )


def file_access_env(file_path: str) -> tuple[str, str]:
    return (
        "Blocked by organization policy: access to environment files is restricted",
        _file_violation(
            file_path,
            "Reading environment files (.env, .envrc) is blocked by your organization's policy. These files may contain credentials and secrets that must not be sent to the LLM.",
        ),
    )


def file_access_mcp_config(file_path: str) -> tuple[str, str]:
    return (
        "Blocked by organization policy: access to MCP configuration files is restricted",
        _file_violation(
            file_path,
            "Reading MCP configuration files is blocked by your organization's policy. These files contain sensitive server connection details that must not be exposed.",
        ),
    )


def file_access_claude_settings(file_path: str) -> tuple[str, str]:
    return (
        "Blocked by organization policy: access to Claude Code settings is restricted",
        _file_violation(
            file_path,
            "Reading Claude Code settings files is blocked by your organization's policy. These files contain sensitive hook and security configuration that must not be exposed.",
        ),
    )


def _file_violation(file_path: str, reason: str) -> str:
    return (
        "# Security Violation Detected\n"
        "\nYour organization's security policy (enforced by Runlayer) has blocked this operation.\n"
        "\n**What happened:**"
        "\n- Violation type: File Access Policy"
        f"\n- File: {file_path}"
        f"\n- Reason: {reason}"
        "\n- Do not attempt to read this file using Bash (cat, head, tail, less), Grep, or any other tool. All access to this file is restricted."
        f"\n\n{AGENT_GUARDRAILS}\n"
        "\n**What to do:**\n"
        "If you believe this is a false positive or mistake, contact your Runlayer administrator to adjust file access policies."
    )


def _violation_with_tool(
    violation_type: str,
    reason: str,
    *,
    tool_name: str = "",
    extra_lines: str = "",
    footer: str = "",
) -> str:
    parts = [
        "# Security Violation Detected\n",
        "\nYour organization's security policy (enforced by Runlayer) has blocked this operation.\n",
        "\n**What happened:**",
        f"\n- Violation type: {violation_type}",
    ]
    if tool_name:
        parts.append(f"\n- Tool: {tool_name}")
    if extra_lines:
        parts.append(f"\n{extra_lines}")
    parts.append(f"\n- Reason: {reason}")
    parts.append(f"\n\n{AGENT_GUARDRAILS}\n")
    if footer:
        parts.append(f"\n**What to do:**\n{footer}")
    else:
        parts.append(
            "\n**What to do:**\n"
            "If you believe this is an error, contact your Runlayer administrator."
        )
    return "".join(parts)
