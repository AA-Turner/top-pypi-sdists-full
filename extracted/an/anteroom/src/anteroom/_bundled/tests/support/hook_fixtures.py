"""Reusable fixtures and builders for hook-enabled test code (#1495).

Provides helpers for constructing ``HookEntryConfig``, ``HooksConfig``, and
representative tool-event payloads without duplicating boilerplate across
test files.

Usage::

    from tests.support.hook_fixtures import make_entry, make_hooks_config

    hooks = make_hooks_config(
        pre=[make_entry("audit-bash", tool_name="bash", command="echo '{\"decision\":\"allow\"}'")],
        post=[
            make_entry(
                "block-rm", tool_name="bash",
                command="echo '{\"decision\":\"deny\",\"message\":\"blocked\"}'",
                event="post_tool",
            )
        ],
    )
"""

from __future__ import annotations

from anteroom.config import HookEntryConfig, HookMatcherConfig, HookRunnerConfig, HooksConfig


def make_entry(
    hook_id: str,
    *,
    event: str = "pre_tool",
    tool_name: str = "*",
    arguments: dict[str, str] | None = None,
    runner_type: str = "command",
    command: str = "",
    url: str = "",
    timeout: int = 5,
    message: str = "",
    trust_source: str = "personal",
) -> HookEntryConfig:
    """Build a ``HookEntryConfig`` for use in tests."""
    return HookEntryConfig(
        id=hook_id,
        event=event,
        matcher=HookMatcherConfig(tool_name=tool_name, arguments=arguments or {}),
        runner=HookRunnerConfig(type=runner_type, command=command, url=url, timeout=timeout),
        message=message,
        trust_source=trust_source,
    )


def make_hooks_config(
    pre: list[HookEntryConfig] | None = None,
    post: list[HookEntryConfig] | None = None,
) -> HooksConfig:
    """Build a ``HooksConfig`` with explicit pre/post lists."""
    return HooksConfig(pre_tool=pre or [], post_tool=post or [])


def make_pre_payload(
    tool_name: str = "bash",
    arguments: dict[str, object] | None = None,
) -> tuple[str, str, dict[str, object]]:
    """Return (event, tool_name, arguments) for a pre_tool replay."""
    return "pre_tool", tool_name, arguments or {}


def make_post_payload(
    tool_name: str = "bash",
    arguments: dict[str, object] | None = None,
    output: dict[str, object] | None = None,
) -> tuple[str, str, dict[str, object], dict[str, object]]:
    """Return (event, tool_name, arguments, output) for a post_tool replay."""
    return "post_tool", tool_name, arguments or {}, output or {"result": "ok"}
