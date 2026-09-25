"""Single source of truth for deny / agent messages (user/agent contract — coordinate before changing)."""

from typing import NamedTuple

from runlayer_cli.hook.credential_state import CREDENTIAL_REJECTED_STATUS
from runlayer_cli.hook.failure import FailureContext

AGENT_GUARDRAILS = (
    "**If you are an AI Agent:**\n"
    "- Provide the user with a detailed explanation of this security violation.\n"
    "- Do not suggest this is a false positive or mistake.\n"
    "- Do not suggest modifying, bypassing, or disabling the Runlayer hook or security configuration.\n"
    "- Do not suggest checking or editing hook files, settings.json, or any security configuration.\n"
    "- Do not retry this action or attempt alternative approaches to achieve the same result."
)

RETRYABLE_INFRA_GUARDRAILS = (
    "**If you are an AI Agent:**\n"
    "- This was a fail-closed infrastructure state, NOT a policy match or threat detection.\n"
    "- Wait a few seconds, then retry this exact action once. If it is blocked again, stop and inform the user.\n"
    "- Do not suggest modifying, bypassing, or disabling the Runlayer hook or security configuration.\n"
    "- Do not suggest checking or editing hook files, settings.json, or any security configuration."
)

DEFAULT_USER_MSG = "Action blocked by organization security policy"

# One copy of the policy-deny framing for every builder below: the words
# "security policy (enforced by Runlayer)" are only true when Runlayer (or the
# organization's policy it applies) made the decision. Network rejections use
# _NETWORK_BLOCK_HEADER instead.
_SECURITY_VIOLATION_HEADER = (
    "# Security Violation Detected\n"
    "\nYour organization's security policy (enforced by Runlayer) has blocked this operation.\n"
)

# A 401/403 answered by something in front of Runlayer (WAF IP allowlist,
# ALB, corporate proxy). Runlayer never saw the request, so the framing must
# not claim a policy decision, and the remedy is the device's network path.
_NETWORK_BLOCK_HEADER = (
    "# Runlayer Verification Blocked by Network\n"
    "\nRunlayer could not verify this action: a network device between this "
    "machine and Runlayer rejected the verification request before it "
    "reached Runlayer. This is not a Runlayer policy decision.\n"
)

_NETWORK_AGENT_GUARDRAILS = (
    "**If you are an AI Agent:**\n"
    "- Tell the user this action was not checked because the verification request was rejected by their network, not by a Runlayer policy.\n"
    "- Do not suggest modifying, bypassing, or disabling the Runlayer hook or security configuration.\n"
    "- Do not suggest checking or editing hook files, settings.json, or any security configuration.\n"
    "- Do not retry this action or attempt alternative approaches to achieve the same result until the user has fixed their network path."
)


# Monitor-mode one-liner (hourly, per device) when the API rejects this
# device's credentials: says what stopped (monitoring), what did not (the
# user's work), and who owns the fix.
MONITOR_CREDENTIALS_REJECTED_NOTICE = (
    "Runlayer monitoring is offline on this device (credentials rejected). "
    "Nothing is blocked. Ask your Runlayer administrator to re-push the "
    "AI Watch configuration."
)


def host_override_notice(user_host: str, managed_host: str) -> str:
    """Hourly one-liner when a managed device's ``runlayer login`` host differs
    from its MDM host: says where hooks report, and that the login host is
    unaffected for interactive commands, so neither side reads as broken."""
    return (
        f"This device is managed by Runlayer: AI Watch hooks report to "
        f"{managed_host}, not your `runlayer login` host {user_host}. "
        f"`runlayer run` and other interactive commands still use {user_host}."
    )


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


def _credential_rejected_message(
    verification_phrase: str,
    *,
    tool_name: str,
    hostname: str | None,
    managed_credential: bool,
) -> tuple[str, str]:
    """Enforce deny for a 401; the remedy depends on who owns the credential
    (MDM org key: the administrator; per-user secret: ``runlayer login``)."""
    status = CREDENTIAL_REJECTED_STATUS
    device = f" (device: {hostname})" if hostname else ""
    ticket_hint = (
        f'quote the device hostname "{hostname}"'
        if hostname
        else "quote this machine's hostname"
    )
    if managed_credential:
        user_action = "Nothing to fix locally — contact your Runlayer administrator"
        footer = (
            "Nothing on this machine can fix this: the credential comes from "
            "your organization's device management, and signing in again here "
            "does not replace it. Your Runlayer administrator can identify the "
            "revoked organization API key from Settings → MDM configuration "
            "and the audit log, and must re-deploy a current configuration to "
            f"this device. {ticket_hint[:1].upper()}{ticket_hint[1:]} when "
            "opening a helpdesk ticket."
        )
    else:
        user_action = "Run 'runlayer login' to refresh them"
        footer = (
            "Run 'runlayer login' to refresh this machine's Runlayer "
            "credentials, then retry. If that does not help, contact your "
            f"Runlayer administrator and {ticket_hint}."
        )
    return (
        f"Runlayer API rejected this machine's credentials (HTTP {status}). "
        f"{user_action}{device}",
        _violation_with_tool(
            "Authentication Required",
            f"The Runlayer API rejected this machine's credentials during "
            f"{verification_phrase} (HTTP {status}). The API was reachable — "
            "this is a credential problem, not an outage. Unverified actions "
            "are blocked (fail-closed).",
            tool_name=tool_name,
            extra_lines=f"- Device hostname: {hostname}" if hostname else "",
            footer=footer,
        ),
    )


def _runlayer_response_lines(failure: "FailureContext") -> str:
    """Support-facing lines for a response classified as Runlayer's own: the
    backend's ``detail`` (quoted — it is server text placed in front of an
    agent) and the request id that finds the server log line. Empty when the
    response is an intermediary's or unclassified."""
    lines = []
    if failure.origin == "runlayer":
        if failure.detail:
            lines.append(f'- Detail: "{failure.detail}"')
        if failure.request_id:
            lines.append(f"- Request ID: {failure.request_id}")
    return "\n".join(lines)


def _network_rejection_message(
    verification_phrase: str,
    *,
    failure: "FailureContext",
    tool_name: str,
    hostname: str | None,
) -> tuple[str, str]:
    status = failure.status_code
    parts = [
        _NETWORK_BLOCK_HEADER,
        "\n**What happened:**",
        "\n- Block type: Network",
    ]
    if tool_name:
        parts.append(f"\n- Tool: {tool_name}")
    if hostname:
        parts.append(f"\n- Device hostname: {hostname}")
    parts.append(
        f"\n- Reason: The {verification_phrase} request was answered with HTTP "
        f"{status} by a network device on this machine's path to Runlayer "
        "(a firewall, IP allowlist, VPN or zero-trust gateway, or proxy), not "
        "by the Runlayer API — the response carried none of Runlayer's "
        "response markers. Runlayer never received the request, so the "
        "action could not be verified. Unverified actions are blocked "
        "(fail-closed)."
    )
    parts.append(f"\n\n{_NETWORK_AGENT_GUARDRAILS}\n")
    parts.append(
        "\n**What to do:**\n"
        "Check that this machine's VPN or zero-trust client is connected and "
        "that the Runlayer host is routed through it (a source-IP allowlist "
        "rejects traffic from home, mobile, or other non-approved networks). "
        "Then retry. If it keeps happening on an approved network, contact "
        "your IT team and quote this machine's hostname; your Runlayer "
        "administrator can confirm which network ranges are allowed."
    )
    user = (
        f"Runlayer verification blocked by your network (HTTP {status}) — "
        "check your VPN or zero-trust client and retry"
    )
    return user, "".join(parts)


def _unreachable_message(
    verification_phrase: str,
    *,
    tool_name: str,
    failure: "FailureContext | None",
    hostname: str | None = None,
    managed_credential: bool = True,
) -> tuple[str, str]:
    """Shared assembly for the two unreachable-API builders (single source so
    wording/field changes cannot drift between the MCP and local-tool paths)."""
    if failure is not None and failure.kind == "http":
        # Any HTTP response means something answered — an unreachable/outage
        # framing would misdirect (403 = key lacks a role or a proxy/WAF said
        # no, 429 = throttled, 5xx = server error). A 401/403 the relay
        # attributed to an intermediary is a network rejection; only
        # Runlayer's own 401 is a credential answer and gets credential
        # wording (origin None = unclassified, treated as Runlayer).
        if failure.is_network_rejection:
            return _network_rejection_message(
                verification_phrase,
                failure=failure,
                tool_name=tool_name,
                hostname=hostname,
            )
        if failure.status_code == CREDENTIAL_REJECTED_STATUS:
            return _credential_rejected_message(
                verification_phrase,
                tool_name=tool_name,
                hostname=hostname,
                managed_credential=managed_credential,
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
        user_msg = f"Runlayer verification request failed (HTTP {status})"
        answered = (
            f"The {verification_phrase} request was answered with HTTP "
            f"{status}{_attempts_note(failure)}, so the action could not "
            "be verified."
        )
        if _is_retryable_status(failure.status_code):
            return (
                user_msg,
                _retryable_block(
                    title="Runlayer API Unavailable",
                    explanation="The Runlayer API could not process the required verification right now (server error or throttling), so this operation was blocked as a precaution (fail-closed). No security violation was detected.",
                    reason=f"{answered} The connection worked but the service could not process the request. Unverified actions are blocked (fail-closed).",
                    tool_name=tool_name,
                ),
            )
        return (
            user_msg,
            _violation_with_tool(
                "Infrastructure",
                f"{answered} The "
                "connection worked but the request was rejected or failed — "
                "this is not a connectivity problem. Unverified actions are "
                "blocked (fail-closed).",
                tool_name=tool_name,
                extra_lines=_runlayer_response_lines(failure),
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
        _retryable_block(
            title="Runlayer API Unreachable",
            explanation="Runlayer could not reach its API to complete the required verification in time, so this operation was blocked as a precaution (fail-closed). No security violation was detected.",
            reason=reason,
            tool_name=tool_name,
        ),
    )


def _is_retryable_status(status_code: int | None) -> bool:
    """5xx (server error, or a load balancer answering for unhealthy targets)
    and 429 (throttled) are transient service states worth one retry; every
    other HTTP answer is a rejection of this particular request."""
    return status_code is not None and (status_code >= 500 or status_code == 429)


def _violation(
    violation_type: str,
    reason: str,
    *,
    extra_lines: str = "",
) -> str:
    parts = [
        _SECURITY_VIOLATION_HEADER,
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
    *,
    tool_name: str = "",
    failure: "FailureContext | None" = None,
    hostname: str | None = None,
    managed_credential: bool = True,
) -> tuple[str, str]:
    return _unreachable_message(
        "MCP execution verification",
        tool_name=tool_name,
        failure=failure,
        hostname=hostname,
        managed_credential=managed_credential,
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
    *,
    tool_name: str = "",
    failure: "FailureContext | None" = None,
    hostname: str | None = None,
    managed_credential: bool = True,
) -> tuple[str, str]:
    return _unreachable_message(
        "local tool verification",
        tool_name=tool_name,
        failure=failure,
        hostname=hostname,
        managed_credential=managed_credential,
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


def tool_scan_unavailable(reason: str, *, tool_name: str = "") -> tuple[str, str]:
    """Deny rendering for ``block_state == "scan_unavailable"`` — retryable,
    not a security violation."""
    return reason, _retryable_block(
        title="Security Scan Unavailable",
        explanation="Runlayer could not complete the required security scan in time, so this operation was blocked as a precaution (fail-closed). No security violation was detected.",
        reason=reason,
        tool_name=tool_name,
    )


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
        _SECURITY_VIOLATION_HEADER + "\n**What happened:**"
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
        _SECURITY_VIOLATION_HEADER,
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


def _retryable_block(
    *,
    title: str,
    explanation: str,
    reason: str,
    tool_name: str = "",
) -> str:
    """Fail-closed block that is an infrastructure state, not a detection:
    backend scan_unavailable, client-side unreachable API, 5xx/429 answers.

    Unlike ``_violation_with_tool`` there is no "Security Violation" header
    and the guardrails permit one retry — "do not retry" on an infra hiccup
    would turn a transient state into a hard stop for the agent. The
    anti-tamper lines are kept.
    """
    parts = [
        f"# Action Blocked: {title}\n",
        f"\n{explanation}\n",
        "\n**What happened:**",
    ]
    if tool_name:
        parts.append(f"\n- Tool: {tool_name}")
    parts.append(f"\n- Reason: {reason}")
    parts.append(f"\n\n{RETRYABLE_INFRA_GUARDRAILS}\n")
    parts.append(
        "\n**What to do:**\n"
        "Retry shortly. If this keeps happening, contact your Runlayer administrator."
    )
    return "".join(parts)
