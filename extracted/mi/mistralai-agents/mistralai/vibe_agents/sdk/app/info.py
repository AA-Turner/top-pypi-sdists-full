from __future__ import annotations

from collections.abc import Sequence
from urllib.parse import urlsplit

from mistralai.vibe_agents.session_workflow import SubagentPolicy

from ..authoring.connector_selection import AllConnectors
from ..authoring.permissions import PermissionPolicy
from ..authoring.subagent import Subagent
from ..authoring.tool import tool_id
from .loader import AgentApp


def render(app: AgentApp) -> str:
    lines: list[str] = []
    lines.append(f"agent: {app.name}")
    lines.append(f"  model: {app.agent.model}")
    if app.description is not None:
        lines.append(f"  description: {_truncate(app.description)}")
    if app.agent.instructions is not None:
        lines.append(f"  instructions: {_truncate(app.agent.instructions)}")
    if app.harness.sandbox.access is not None:
        lines.append(f"  sandbox access: {app.harness.sandbox.access}")
    lines.append(f"  sandbox: {'executable' if app.harness.sandbox.is_executable else 'none'}")

    tools = sorted(tool_id(t) for t in app.harness.tools)
    lines.append(_section("tools", tools))

    connectors = sorted(slot.connector_name for slot in app.harness.connectors)
    if app.harness.connector_discovery is not None:
        connectors.append(_describe_discovery(app.harness.connector_discovery))
    lines.append(_section("connectors", connectors))

    mcps = [f"{name} ({_mcp_host(source.url)})" for name, source in sorted(app.harness.mcps.items())]
    lines.append(_section("mcps", mcps))

    # Shown with the description, unlike the other sections: only the description reaches the base
    # system prompt (the body is fetched on demand through the `skill` tool), so it is the whole of
    # what makes a skill discoverable, and the thing worth eyeballing here.
    skills = [
        f"{skill.name}: {_truncate(skill.description)}" for skill in sorted(app.skills, key=lambda skill: skill.name)
    ]
    if app.harness.skill_discovery is not None:
        skills.append("all_registry_skills()")
    lines.append(_section("skills", skills))

    guardrails = [type(guardrail).__name__ for guardrail in app.harness.guardrails]
    lines.append(_section("guardrails", guardrails))

    hooks = [type(hook).__name__ for hook in app.harness.hooks]
    lines.append(_section("hooks", hooks))

    lines.append(_section("subagents", _describe_subagents(app.agent.subagents)))
    lines.append(f"  subagent policy: {_describe_subagent_policy(app.agent.subagents, app.agent.subagent_policy)}")
    lines.append(f"  permission mode: {app.agent.permission_mode}")
    lines.append(_describe_permission_policy(app.agent.permission_policy))
    return "\n".join(lines)


def _mcp_host(url: str) -> str:
    """Only the host and port: a URL can carry a token in its user info, path or query."""

    parts = urlsplit(url)
    if parts.hostname is None:
        return "host not shown"
    try:
        port = parts.port
    except ValueError:
        port = None
    if port is None:
        return parts.hostname
    host = f"[{parts.hostname}]" if ":" in parts.hostname else parts.hostname
    return f"{host}:{port}"


def _describe_subagents(subagents: Sequence[Subagent], depth: int = 0) -> list[str]:
    """List each child configuration with its own tools, nested under the configuration that declares it."""

    items: list[str] = []
    for subagent in subagents:
        tools = (
            "inherited" if subagent.tools is None else ", ".join(sorted(tool_id(t) for t in subagent.tools)) or "none"
        )
        items.append(f"{'  ' * depth}{subagent.name} (tools: {tools}): {_truncate(subagent.description)}")
        items.extend(_describe_subagents(subagent.subagents or (), depth + 1))
    return items


def _describe_subagent_policy(subagents: Sequence[Subagent], policy: SubagentPolicy | None) -> str:
    """Show the policy the worker registers: the authored one, or the default when children are declared."""

    if policy is None and not subagents:
        return "(none)"
    effective = policy or SubagentPolicy()
    suffix = "" if policy is not None else " (default)"
    return (
        f"concurrent_child_turn_limit={effective.concurrent_child_turn_limit}, "
        f"idle_message_starts={effective.idle_message_starts}{suffix}"
    )


def _describe_permission_policy(policy: PermissionPolicy | None) -> str:
    """Count the argument patterns of each rule: a pattern can hold a token or a private path."""

    if policy is None:
        return "  permission policy: (none)"
    rules: list[str] = []
    for rule in policy.rules:
        argument_patterns = [
            f"{name}: {len(patterns)} pattern{'' if len(patterns) == 1 else 's'}"
            for name, patterns in (
                ("allowlist", rule.allowlist),
                ("denylist", rule.denylist),
                ("sensitive", rule.sensitive),
            )
            if patterns
        ]
        extra = f" ({', '.join(argument_patterns)})" if argument_patterns else ""
        rules.append(f"{', '.join(rule.tools)}: {rule.decision}{extra}")
    rules.append(f"anything else: {policy.default}")
    return _section("permission policy", rules)


def _describe_discovery(discovery: AllConnectors) -> str:
    """Name the selection the way it was authored, keeping only the options that were set."""

    options: list[str] = []
    if discovery.exclude:
        options.append(f"exclude={list(discovery.exclude)!r}")
    if discovery.max_connectors is not None:
        options.append(f"max_connectors={discovery.max_connectors}")
    if not discovery.auto_auth:
        options.append("auto_auth=False")
    if discovery.allow_mcp_ui:
        options.append("allow_mcp_ui=True")
    return f"all_connectors({', '.join(options)})"


def _section(title: str, items: list[str]) -> str:
    if not items:
        return f"  {title}: (none)"
    body = "\n".join(f"    - {item}" for item in items)
    return f"  {title}:\n{body}"


def _truncate(text: str, limit: int = 80) -> str:
    flat = " ".join(text.split())
    return flat if len(flat) <= limit else flat[: limit - 1] + "\u2026"
