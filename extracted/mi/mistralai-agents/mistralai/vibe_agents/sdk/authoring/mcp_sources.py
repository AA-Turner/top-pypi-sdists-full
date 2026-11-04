"""Checks on authored MCP sources that need only the configuration, not the servers' tool lists.

The Harness identifies an MCP source and names its tools from its key. It routes the tools' calls
by the source's ``id``, puts the tools in its ``namespace`` spelled as a core identifier, and starts
a ``direct`` tool's name with its ``name`` in snake_case; each falls back to the key. Two sources
whose names meet there, or a source in a namespace the Harness or the SDK fills, fail only once a
Session starts. These checks raise ``SdkError`` when the agent is defined instead.

A collision that depends on the tools a server lists, such as a direct MCP tool with the name of a
direct Python tool, can only be found when the Session starts.
"""

from collections.abc import Mapping, Sequence
from typing import Any

from mistralai.vibe.harness.app_server.session import McpSourceConfiguration
from mistralai.vibe.harness.runtime.capabilities.identifiers import (
    normalize_core_tool_identifier,
    normalize_source_identifier,
)

from . import tool as tool_authoring
from .errors import SdkError


def check_mcp_sources(
    mcps: Mapping[str, McpSourceConfiguration],
    *,
    programmatic: bool | None,
    owner: str | None = None,
) -> None:
    """Raise ``SdkError`` for MCP sources whose tools the Harness would refuse to name.

    ``programmatic`` is whether the agent calls tools from programs: a source that leaves
    ``model_access`` unset is direct when it is ``False``. ``None`` means not known yet, so only an
    explicit ``direct`` or ``both`` counts. ``owner`` names the Subagent the sources belong to.
    """

    where = f"{owner}: " if owner else ""
    ids: dict[str, str] = {}
    namespaces: dict[str, str] = {}
    prefixes: dict[str, str] = {}
    for key, source in mcps.items():
        # The Harness routes each tool call by its source's id, else its key.
        source_id = source.id or key
        previous = ids.setdefault(source_id, key)
        if previous != key:
            raise SdkError(
                f"{where}MCP sources {previous!r} and {key!r} both have id {source_id!r}; "
                "give one of them another id= or leave id unset"
            )
        namespace = normalize_core_tool_identifier(source.namespace or key)
        if tool_authoring.is_reserved_namespace(namespace):
            raise SdkError(
                f"{where}MCP source {key!r}: namespace {namespace!r} holds the Harness's or the SDK's "
                "own tools; give the source another namespace= or key"
            )
        previous = namespaces.setdefault(namespace, key)
        if previous != key:
            raise SdkError(
                f"{where}MCP sources {previous!r} and {key!r} both put their tools in namespace "
                f"{namespace!r}; give one of them another namespace= or key"
            )
        if not _is_direct(source, programmatic=programmatic):
            continue
        prefix = normalize_source_identifier(source.name or key)
        previous = prefixes.setdefault(prefix, key)
        if previous != key:
            raise SdkError(
                f"{where}MCP sources {previous!r} and {key!r} both name their direct tools "
                f"'{prefix}_<tool>', so a tool both servers list would collide; give one of them "
                "another name= or key"
            )


def refuse_tool_namespaces(
    tools: Sequence[tool_authoring.PythonTool[..., Any] | tool_authoring.ClientToolDefinition[Any]],
    mcps: Mapping[str, McpSourceConfiguration],
    *,
    subagent: tuple[str, ...] = (),
) -> None:
    """Raise ``SdkError`` for one of an agent's ``tools`` in the namespace of one of its ``mcps``."""

    sources = {normalize_core_tool_identifier(source.namespace or key): key for key, source in mcps.items()}
    where = f" in subagent {'/'.join(subagent)!r}" if subagent else ""
    for tool in tools:
        source = sources.get(tool.namespace)
        if source is not None:
            raise SdkError(
                f"Tool {tool_authoring.tool_name(tool)!r}{where}: namespace {tool.namespace!r} holds the tools of "
                f"MCP source {source!r}; give the tool another namespace= or the source another name"
            )


def _is_direct(source: McpSourceConfiguration, *, programmatic: bool | None) -> bool:
    if source.model_access in {"direct", "both"}:
        return True
    return programmatic is False and "model_access" not in source.model_fields_set


__all__ = ["check_mcp_sources", "refuse_tool_namespaces"]
