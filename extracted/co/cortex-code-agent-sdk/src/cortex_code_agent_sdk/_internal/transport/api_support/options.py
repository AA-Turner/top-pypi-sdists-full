"""Mode selection and option validation for direct Agent API transport."""

from __future__ import annotations

from ....types import CortexCodeAgentOptions
from .settings import _is_truthy, _merged_env


def should_use_api_mode(options: CortexCodeAgentOptions) -> bool:
    """Return whether SDK options select direct Agent API mode."""

    if options.mode == "cli":
        return False
    if options.mode == "api":
        return True
    env = _merged_env(options)
    return _is_truthy(env.get("ASYNC_API")) or _is_truthy(
        env.get("CORTEX_CODE_AGENT_SDK_ASYNC_API")
    )

def validate_api_mode_options(options: CortexCodeAgentOptions) -> None:
    """Reject options that require the CLI control/tooling surface."""

    if options.permission_mode and options.permission_mode != "default":
        raise ValueError(
            'API mode does not support permission_mode; use mode="cli" '
            "for plan and permission-mode controls"
        )
    if options.max_turns is not None:
        raise ValueError(
            "API mode does not support max_turns; sandbox runs may perform "
            "multiple server-side turns"
        )
    if options.hooks and any(options.hooks.values()):
        raise ValueError('API mode does not support hooks; use mode="cli" for hooks')
    if options.mcp_servers:
        raise ValueError(
            'API mode does not support MCP; use mode="cli" for MCP servers'
        )
    if options.resume or options.continue_conversation:
        raise ValueError(
            "API mode does not support CLI session resume/continue; "
            "pass session_id to reuse an Agent API thread"
        )
    if options.resume_session_at and not options.fork_session:
        raise ValueError("API mode supports resume_session_at only with fork_session")
    if options.fork_session and not options.session_id:
        raise ValueError(
            "API mode fork_session requires session_id with the source Agent API thread ID"
        )
    api = options.api
    if api and api.token is not None:
        raise ValueError(
            "API mode does not support api.token; pass api.token_provider so "
            "the SDK can refresh expired Snowflake session tokens"
        )
    if api and api.rest_url and api.token_provider is None:
        raise ValueError(
            "API mode api.rest_url requires api.token_provider so the SDK can "
            "refresh expired Snowflake session tokens"
        )
    if api and api.token_provider is not None and not api.rest_url:
        raise ValueError("API mode api.token_provider requires api.rest_url")
    v_stages = options.api.v_stages if options.api else None
    if v_stages and v_stages[0].mount_path != "/workspace":
        raise ValueError(
            "API mode api.v_stages requires the first VStage to mount /workspace"
        )
