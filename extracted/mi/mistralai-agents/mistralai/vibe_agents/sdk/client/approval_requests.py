"""Approval requests: the tool call that an approval is for, as a handler and a turn's record get it."""

from __future__ import annotations

import types
from collections.abc import Iterable, Mapping
from typing import Any, Literal, cast, get_args

from pydantic import BaseModel, ConfigDict, JsonValue, ValidationError

from mistralai.vibe.harness.app_server import session as harness_session
from mistralai.vibe.harness.core import protocol as core_protocol
from mistralai.vibe_agents.sdk.authoring.tool import ClientTool, ClientToolDefinition, PythonTool
from mistralai.vibe_agents.sdk.authoring.tool_definition import ToolAnnotations, ToolDefinition
from mistralai.vibe_agents.sdk.client.unknown_values import UnknownValue, read_value

__all__ = [
    "NO_TOOLS",
    "ApprovalRequest",
    "ApprovalTool",
    "ApprovalToolKind",
    "approval_request",
    "approval_tool",
    "tools_by_id",
]


type _Tool = PythonTool[..., Any] | ClientTool[..., Any] | ClientToolDefinition[Any]

type ApprovalToolKind = Literal["builtin", "client", "mcp", "connector", "plugin"]

_KINDS: frozenset[str] = frozenset(get_args(ApprovalToolKind.__value__))
# The MCP names of the fields and hints a tool definition models.
_FIELDS = frozenset(str(field.validation_alias) for field in ToolDefinition.model_fields.values())
_HINTS = frozenset(str(field.alias) for field in ToolAnnotations.model_fields.values())


class ApprovalTool(BaseModel):
    """The tool that an approval is for.

    ``id`` is the tool's stable id, the one permission rules use, such as ``"file_system.bash"``,
    ``"client.open_case"``, ``"billing.charge"`` or ``"github.create_issue"``. ``name`` is the name
    the model called, which changes with how it called the tool (``deploy_service`` directly,
    ``tools.client.deploy_service`` from ``run_typescript``), so decide on ``id``, never on ``name``.
    ``kind`` says where the tool comes from: ``"builtin"`` for the runtime's own
    tools, ``"client"`` for the agent's ``@agents.tool`` and client tools, ``"mcp"`` for an MCP
    server's, ``"connector"`` for a Mistral connector's, ``"plugin"`` for any other, and an
    :class:`UnknownValue` for a kind a newer host added.

    ``description``, ``input_schema`` and ``output_schema`` are the tool's, as the model reads
    them; they are ``None`` for builtins, and ``output_schema`` for a tool that declares none.
    ``definition`` is the tool's definition. For a tool of the agent or of one of its subagents,
    it is the tool object the agent was given, such as the one ``@agents.tool`` returned; it is
    ``None`` on a session handle that does not hold the agent's tools. For an MCP server's or a
    connector's tool, it is an ``agents.ToolDefinition`` of the whole tool as the server listed
    it, such as its ``title``, ``annotations``, ``output_schema`` and ``meta``, with the server's
    name as ``source``; the host sends it, so it is there with or without the agent, unless the
    host runs a Harness older than the SDK. It is ``None`` for the other tools. Each kind has
    ``display_title``, the name to show people.

    ``annotations`` are the hints the tool declares, such as ``read_only_hint``: those of
    ``annotations=`` on ``@agents.tool``, ``agents.PythonTool`` and ``agents.client_tool``, and
    those an MCP server or a connector declares for its tool. The host sends them with the
    approval, so every approver reads the same ones, with or without the agent. A hint the tool
    does not declare takes MCP's default, which assumes the worst: a policy that allows only
    read-only tools allows a tool only if it declares ``read_only_hint=True``.
    """

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    id: str
    name: str
    kind: ApprovalToolKind | UnknownValue
    description: str | None = None
    input_schema: dict[str, JsonValue] | None = None
    output_schema: dict[str, JsonValue] | None = None
    definition: _Tool | ToolDefinition | None = None
    annotations: ToolAnnotations = ToolAnnotations()


class ApprovalRequest(BaseModel):
    """A tool call that waits for an approval. The ids are in the handler's ``ctx``.

    ``tool`` is the tool the call is for. ``hook`` is the name of the ``pre_tool_call`` hook that asked for the
    approval, or ``None`` when the agent's permission policy asked. A hook's approval cannot be
    allowed for the session: answer it with ``AllowApproval()``, once. ``input`` is the arguments
    of the call, as the model wrote them.
    """

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    tool: ApprovalTool
    hook: str | None = None
    title: str
    input: JsonValue = None


# A handle made without the agent has no tool objects.
NO_TOOLS: Mapping[str, _Tool] = types.MappingProxyType({})


def tools_by_id(tools: Iterable[_Tool]) -> Mapping[str, _Tool]:
    """``tools`` by the id the host gives a tool, ``<namespace>.<name>``. A tool id that two
    different objects share has no tool object."""
    by_id: dict[str, _Tool | None] = {}
    for tool in tools:
        tool_id = _tool_id(tool)
        by_id[tool_id] = tool if by_id.get(tool_id, tool) is tool else None
    return {tool_id: tool for tool_id, tool in by_id.items() if tool is not None}


def approval_request(callback: harness_session.ApprovalCallback, tools: Mapping[str, _Tool]) -> ApprovalRequest:
    """The request of ``callback``, with its tool object from ``tools`` by tool id."""
    return ApprovalRequest(
        tool=approval_tool(callback, tools), hook=callback.hook, title=callback.title, input=callback.input
    )


def approval_tool(callback: harness_session.ApprovalCallback, tools: Mapping[str, _Tool]) -> ApprovalTool:
    """The tool of ``callback``, with its tool object from ``tools`` by tool id."""
    tool_id = callback.tool_id or callback.name or ""
    name = callback.name or tool_id
    return ApprovalTool(
        id=tool_id,
        name=name,
        kind=_tool_kind(callback.tool_kind, tool_id, tools),
        description=callback.tool_description,
        input_schema=callback.input_schema,
        output_schema=callback.output_schema,
        definition=_definition(callback, tools.get(tool_id)),
        annotations=_annotations(callback.tool_annotations),
    )


def _definition(callback: harness_session.ApprovalCallback, tool: _Tool | None) -> _Tool | ToolDefinition | None:
    """The agent's own tool object, else the definition of the tool the host sent, if any."""
    if tool is not None or callback.tool_definition is None:
        return tool
    try:
        listed = ToolDefinition.model_validate(
            _without_nulls(callback.tool_definition), by_alias=True, extra="allow", strict=True
        )
    except ValidationError:
        # A tool the host sends with no name or with a value MCP does not allow, such as a hint
        # that is not a boolean: the approval goes on, without a definition.
        return None
    return listed.model_copy(update={"source": callback.tool_source})


def _without_nulls(listed: Mapping[str, JsonValue]) -> dict[str, JsonValue]:
    """``listed`` without the MCP fields and hints it sends as null. The host writes what the server
    did not declare as null, and a null field takes its default, as an absent one does."""
    declared = {key: value for key, value in listed.items() if not (key in _FIELDS and value is None)}
    annotations = declared.get("annotations")
    if isinstance(annotations, dict):
        declared["annotations"] = {
            key: value for key, value in annotations.items() if not (key in _HINTS and value is None)
        }
    return declared


def _annotations(declared: harness_session.ToolAnnotations | None) -> ToolAnnotations:
    """The hints of an approval: those the host sent, and MCP's default for each one it did not."""
    if declared is None:
        return ToolAnnotations()
    return ToolAnnotations(**declared.model_dump(by_alias=False, exclude_none=True))


def _tool_kind(
    host_kind: harness_session.ToolKind | harness_session.UnknownValue | None, tool_id: str, tools: Mapping[str, _Tool]
) -> ApprovalToolKind | UnknownValue:
    if isinstance(host_kind, harness_session.UnknownValue):
        return read_value(host_kind, "ApprovalTool.kind")
    if host_kind in _KINDS:
        return cast(ApprovalToolKind, host_kind)
    # A host that does not say, or names "local", a kind the SDK does not have.
    if tool_id in core_protocol.RUNTIME_BUILTIN_TOOL_NAMES:
        return "builtin"
    if tool_id.startswith("client.") or tool_id in tools:
        return "client"
    return "plugin"


def _tool_id(tool: _Tool) -> str:
    # A tool that names no namespace is in "client", the namespace a tool has by default.
    return f"{getattr(tool, 'namespace', 'client')}.{tool.name}"
