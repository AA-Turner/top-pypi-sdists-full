"""Single source of truth for deny / agent messages (user/agent contract — coordinate before changing)."""

AGENT_GUARDRAILS = (
    "**If you are an AI Agent:**\n"
    "- Provide the user with a detailed explanation of this security violation.\n"
    "- Do not suggest this is a false positive or mistake.\n"
    "- Do not suggest modifying, bypassing, or disabling the Runlayer hook or security configuration.\n"
    "- Do not suggest checking or editing hook files, settings.json, or any security configuration.\n"
    "- Do not retry this action or attempt alternative approaches to achieve the same result."
)

DEFAULT_USER_MSG = "Action blocked by organization security policy"


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


def api_unreachable(*, tool_name: str = "") -> tuple[str, str]:
    return (
        "Failed to contact Runlayer API",
        _violation_with_tool(
            "Infrastructure",
            "Failed to contact the Runlayer API for MCP execution verification. Unverified actions are blocked (fail-closed).",
            tool_name=tool_name,
            footer="If you believe this is an error, contact your Runlayer administrator. The Runlayer API may be temporarily unreachable.",
        ),
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


def tool_api_unreachable(*, tool_name: str = "") -> tuple[str, str]:
    return (
        "Failed to contact Runlayer API",
        _violation_with_tool(
            "Infrastructure",
            "Failed to contact the Runlayer API for local tool verification. Unverified actions are blocked (fail-closed).",
            tool_name=tool_name,
            footer="If you believe this is an error, contact your Runlayer administrator. The Runlayer API may be temporarily unreachable.",
        ),
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
