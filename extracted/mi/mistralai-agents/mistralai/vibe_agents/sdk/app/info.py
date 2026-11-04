from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from urllib.parse import urlsplit

from rich.cells import cell_len
from rich.text import Text

from mistralai.vibe_agents.session_workflow import SubagentPolicy

from ..authoring.connector_selection import AllConnectors
from ..authoring.permissions import PermissionPolicy
from ..authoring.subagent import Subagent
from ..authoring.tool import tool_id
from ..authoring.types import builtins_to_config
from .loader import AgentApp

if TYPE_CHECKING:
    from mistralai.vibe.harness.app_server.session.models.configuration import McpHttpSourceConfiguration
    from mistralai.workflows.plugins.mistralai.connectors.decorator import ConnectorSlot

# Truecolor styles; rich lowers them to what the terminal supports and drops them when output is not a terminal.
_ACCENT = "bold #fa520f"
_LABEL = "#89b4fa"
_DIM = "#7f849c"
_STRONG = "bold"
_VARIABLE = "#f9e2af"
_WARNING = "bold #f9e2af"
_ERROR = "bold #f38ba8"
# Wide enough for the longest row label, "subagent policy", plus a gap.
_LABEL_WIDTH = 17
_NONE = Text("(none)", style=_DIM)
_SEPARATOR = (" · ", _DIM)


@dataclass
class _Item:
    """One entry of a section: a name, what follows it on its line, and labelled lines under it."""

    name: str
    detail: Text = field(default_factory=Text)
    rows: list[tuple[str, Text]] = field(default_factory=list)


class _Tree:
    def __init__(self) -> None:
        self.lines: list[Text] = []

    def blank(self) -> None:
        if self.lines and self.lines[-1].plain:
            self.lines.append(Text())

    def row(self, label: str, value: Text) -> None:
        self.lines.append(Text.assemble("  ", (f"{label:<{_LABEL_WIDTH}}", _LABEL), value))

    def section(self, title: str, items: Sequence[_Item]) -> None:
        """A row reading ``(none)`` when empty; otherwise a heading with its items aligned under it."""

        if not items:
            self.row(title, _NONE)
            return
        self.blank()
        self.lines.append(Text(f"  {title}", style=_STRONG))
        name_width = max(cell_len(item.name) for item in items) + 3
        for item in items:
            line = Text.assemble("    ", (_pad(item.name, name_width), _LABEL), item.detail)
            line.rstrip()
            self.lines.append(line)
            if not item.rows:
                continue
            row_width = max(len(label) for label, _ in item.rows) + 3
            for label, value in item.rows:
                indent = " " * (4 + name_width)
                self.lines.append(Text.assemble(indent, (f"{label:<{row_width}}", _LABEL), value))
        self.blank()

    def render(self) -> Text:
        while self.lines and not self.lines[-1].plain:
            self.lines.pop()
        return Text("\n").join(self.lines)


def render(app: AgentApp, *, errors: Sequence[str] = (), warnings: Sequence[str] = ()) -> Text:
    """The agent surface as an aligned tree, then the checks: ``errors`` stop the agent, ``warnings`` do not."""

    tree = _Tree()
    tree.lines.append(Text.assemble((app.name, _ACCENT), "  ", (app.agent.model, _DIM)))
    tree.blank()
    if app.description is not None:
        tree.row("description", Text(_truncate(app.description)))
    if app.agent.instructions is not None:
        tree.row("instructions", Text(_truncate(app.agent.instructions)))
    sandbox = Text("executable") if app.harness.sandbox.is_executable else Text("none", style=_DIM)
    if app.harness.sandbox.access is not None:
        sandbox.append_text(Text.assemble(_SEPARATOR, f"access {app.harness.sandbox.access}"))
    tree.row("sandbox", sandbox)

    tree.section("tools", [_Item(tool_id(t)) for t in app.harness.tools])

    # Connectors and MCP servers keep their declaration order, so the list reads like the code.
    connectors = [_describe_connector(slot) for slot in app.harness.connectors]
    if app.harness.connector_discovery is not None:
        connectors.append(_describe_discovery(app.harness.connector_discovery))
    tree.section("connectors", connectors)

    # Resolved by assembly's own rule, so the model access shown is the one a Session gets.
    from ..assembly.assemble import _resolve_mcp_model_access  # noqa: PLC0415

    programmatic = builtins_to_config(app.agent.builtins).programmatic_enabled
    resolved = _resolve_mcp_model_access(app.harness.mcps, programmatic=programmatic)
    tree.section(
        "mcps", [_describe_mcp(name, source, resolved[name].model_access) for name, source in app.harness.mcps.items()]
    )

    # Shown with the description, unlike the other sections: only the description reaches the base
    # system prompt (the body is fetched on demand through the `skill` tool), so it is the whole of
    # what makes a skill discoverable, and the thing worth eyeballing here.
    skills = [
        _Item(skill.name, Text(_truncate(skill.description)))
        for skill in sorted(app.skills, key=lambda skill: skill.name)
    ]
    if app.harness.skill_discovery is not None:
        skills.append(_Item("all_registry_skills()"))
    tree.section("skills", skills)

    tree.section("guardrails", [_Item(type(guardrail).__name__) for guardrail in app.harness.guardrails])
    tree.section("hooks", [_Item(type(hook).__name__) for hook in app.harness.hooks])

    tree.section("subagents", _describe_subagents(app.agent.subagents))
    tree.row("subagent policy", _describe_subagent_policy(app.agent.subagents, app.agent.subagent_policy))
    permissions = Text(str(app.agent.permission_mode))
    if app.agent.permission_policy is None:
        permissions.append_text(Text.assemble(_SEPARATOR, ("no policy", _DIM)))
    tree.row("permissions", permissions)
    if app.agent.permission_policy is not None:
        tree.section("permission rules", _describe_permission_policy(app.agent.permission_policy))

    if errors or warnings:
        tree.blank()
        tree.lines.append(Text("  checks", style=_STRONG))
        tree.lines.extend(Text.assemble("    ", ("✗ ", _ERROR), error) for error in errors)
        tree.lines.extend(Text.assemble("    ", ("⚠ ", _WARNING), warning) for warning in warnings)
    return tree.render()


def _pad(text: str, width: int) -> str:
    """Pad to ``width`` terminal cells: a wide character, such as CJK or an emoji, takes two."""

    return text + " " * max(width - cell_len(text), 0)


def _options(*parts: tuple[str, str] | str) -> Text:
    """``key value`` pairs (or bare words), joined by a dim separator: the options an author set."""

    text = Text()
    for index, part in enumerate(parts):
        if index:
            text.append(*_SEPARATOR)
        if isinstance(part, str):
            text.append(part)
        else:
            key, value = part
            text.append(f"{key} ")
            text.append(value, style=_STRONG)
    return text


def _describe_connector(slot: ConnectorSlot) -> _Item:
    """Name the connector with the options that were set."""

    options: list[tuple[str, str] | str] = []
    if slot.run_as_explicit:
        options.append(("run_as", slot.run_as.value))
    if slot.credentials_name is not None:
        options.append(("credentials", slot.credentials_name))
    if not slot.auto_auth:
        options.append(("auto_auth", "off"))
    if slot.allow_mcp_ui:
        options.append("MCP UI allowed")
    return _Item(slot.connector_name, _options(*options))


def _describe_discovery(discovery: AllConnectors) -> _Item:
    """Name the selection the way it was authored, keeping only the options that were set."""

    options: list[tuple[str, str] | str] = []
    if discovery.exclude:
        options.append(("exclude", ", ".join(discovery.exclude)))
    if discovery.max_connectors is not None:
        options.append(("max", str(discovery.max_connectors)))
    if not discovery.auto_auth:
        options.append(("auto_auth", "off"))
    if discovery.allow_mcp_ui:
        options.append("MCP UI allowed")
    return _Item("all_connectors()", _options(*options))


def _describe_mcp(name: str, source: McpHttpSourceConfiguration, model_access: str) -> _Item:
    """The server's host and the options that decide which of its tools the model gets.

    ``model_access`` is the effective one, dim when the author left it to the default.
    Header and variable names are shown, never a value: the variable is read where the agent runs.
    """

    declared = source.model_fields_set
    explicit_access = "model_access" in declared
    rows = [("model access", Text(model_access, style="" if explicit_access else _DIM))]
    # The harness prefixes direct tool names with the source's name, so one that differs from the
    # key explains tool names the key does not.
    if source.name is not None and source.name != name:
        rows.append(("name", Text(source.name)))
    if source.id is not None:
        rows.append(("id", Text(source.id)))
    if source.namespace is not None and source.namespace != name:
        rows.append(("namespace", Text(source.namespace)))
    if source.disabled_tools:
        rows.append(("disabled", Text(", ".join(source.disabled_tools))))
    for index, (header, variable) in enumerate(source.auth_header_env_vars.items()):
        rows.append(
            ("auth headers" if index == 0 else "", Text.assemble(header, (" ← ", _DIM), (f"${variable}", _VARIABLE)))
        )
    for timeout, label in (("startup_timeout_seconds", "startup timeout"), ("tool_timeout_seconds", "tool timeout")):
        if timeout in declared:
            rows.append((label, Text(f"{getattr(source, timeout):g}s")))
    return _Item(name, Text(_mcp_host(source.url), style=_STRONG), rows)


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


def _describe_subagents(subagents: Sequence[Subagent], depth: int = 0) -> list[_Item]:
    """List each child configuration with its own tools, nested under the configuration that declares it."""

    items: list[_Item] = []
    for subagent in subagents:
        tools = (
            "inherited" if subagent.tools is None else ", ".join(sorted(tool_id(t) for t in subagent.tools)) or "none"
        )
        detail = Text.assemble(_truncate(subagent.description), _SEPARATOR, ("tools ", _DIM), tools)
        items.append(_Item(f"{'  ' * depth}{subagent.name}", detail))
        items.extend(_describe_subagents(subagent.subagents or (), depth + 1))
    return items


def _describe_subagent_policy(subagents: Sequence[Subagent], policy: SubagentPolicy | None) -> Text:
    """Show the policy the worker registers: the authored one, or the default when children are declared."""

    if policy is None and not subagents:
        return _NONE.copy()
    effective = policy or SubagentPolicy()
    text = _options(
        ("concurrent_child_turn_limit", str(effective.concurrent_child_turn_limit)),
        ("idle_message_starts", str(effective.idle_message_starts)),
    )
    if policy is None:
        text.append(" (default)", style=_DIM)
    return text


def _describe_permission_policy(policy: PermissionPolicy) -> list[_Item]:
    """Count the argument patterns of each rule: a pattern can hold a token or a private path."""

    items: list[_Item] = []
    for rule in policy.rules:
        detail = Text(rule.decision, style=_STRONG)
        for kind, patterns in (
            ("allowlist", rule.allowlist),
            ("denylist", rule.denylist),
            ("sensitive", rule.sensitive),
        ):
            if patterns:
                detail.append_text(
                    Text.assemble(_SEPARATOR, f"{kind} {len(patterns)} pattern{'' if len(patterns) == 1 else 's'}")
                )
        items.append(_Item(", ".join(rule.tools), detail))
    items.append(_Item("anything else", Text(policy.default, style=_STRONG)))
    return items


def _truncate(text: str, limit: int = 80) -> str:
    flat = " ".join(text.split())
    return flat if len(flat) <= limit else flat[: limit - 1] + "…"
