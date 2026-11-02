"""Compile authored ``agents.Subagent`` trees into the ``SubagentConfig`` layers the Runtime resolves."""

from __future__ import annotations

from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass
from typing import cast

from pydantic import JsonValue

from mistralai.vibe.harness.app_server.session import (
    AgentConfig,
    BuiltinsConfig,
    McpHttpSourceConfiguration,
    SubagentBuiltinsConfig,
    SubagentConfig,
    SubagentPolicy,
)
from mistralai.vibe.harness.runtime.agents.configuration import resolve_subagent_config
from mistralai.vibe.harness.runtime.completion import (
    CompletionConfig,
    UnsupportedCompletionProviderError,
    parse_completion_config,
)
from mistralai.vibe.harness.runtime.completion.providers.anthropic import AnthropicCompletionConfig
from mistralai.vibe.harness.runtime.completion.providers.mistral import MistralCompletionConfig
from mistralai.vibe.harness.runtime.completion.providers.openai import OpenAICompletionConfig
from mistralai.vibe_agents import session_workflow as wire
from mistralai.vibe_agents.sdk.authoring import contracts
from mistralai.vibe_agents.sdk.authoring import subagent as subagent_authoring
from mistralai.vibe_agents.sdk.authoring import tool as tool_authoring
from mistralai.vibe_agents.sdk.authoring import types as authoring_types
from mistralai.vibe_agents.sdk.authoring.errors import SdkError, UnsupportedAgentFeatureError

from . import assemble, sandbox_skills
from . import mcp as mcp_assembly


@dataclass(frozen=True, slots=True)
class SubagentHarness:
    """What the agent's Harness gives a subagent tree.

    ``tools`` and ``mcps`` are the authored ones a child inherits when it declares none. A tool or
    MCP source that leaves ``model_access`` unset follows the programmatic tool calling of the agent
    it runs in, so a child that changes that setting gets its own compiled copy.
    """

    tools: Sequence[assemble._AuthoredTool]
    mcps: Mapping[str, McpHttpSourceConfiguration]
    sandbox: contracts.Sandbox


def compile_subagents(
    parent: AgentConfig,
    subagents: Sequence[subagent_authoring.Subagent],
    *,
    policy: wire.SubagentPolicy | None = None,
) -> dict[str, object]:
    """Compile a root agent's children and Session Tree policy into ``AgentConfig.subagents`` and
    ``AgentConfig.subagent_policy``.

    An agent that declares children and no policy gets the default policy from
    ``AgentConfig.effective_subagent_policy``.
    """

    return {
        "subagent_policy": None if policy is None else SubagentPolicy.model_validate(policy.model_dump()),
        "subagents": compile_subagent_catalog(parent, subagents),
    }


def compile_subagent_catalog(
    parent: AgentConfig,
    subagents: Sequence[subagent_authoring.Subagent],
    *,
    harness: SubagentHarness | None = None,
    path: tuple[str, ...] = (),
) -> dict[str, SubagentConfig]:
    """Compile authored children into the replace-only overlays the Runtime resolves, keyed by name.

    An ``agents.Subagent`` is compiled against the configuration of the agent it is declared
    on: its ``model`` replaces the model of that agent's completion, and each field it sets
    replaces the inherited one. With ``harness``, each child also gets the tool and MCP access
    that fits its own built-ins, and its sandbox access is checked against the sandbox.
    """

    catalog: dict[str, SubagentConfig] = {}
    for entry in subagents:
        entry_path = (*path, entry.name)
        if entry.name in catalog:
            raise SdkError(f"Subagent name {'/'.join(entry_path)!r} is declared twice; subagent names must be unique")
        catalog[entry.name] = _compile_subagent(parent, entry, entry_path, harness)
    return catalog


def _compile_subagent(
    parent: AgentConfig,
    layer: subagent_authoring.Subagent,
    path: tuple[str, ...],
    harness: SubagentHarness | None,
) -> SubagentConfig:
    values: dict[str, object] = {
        "description": layer.description,
        "instructions": layer.instructions,
    }
    completion = _compile_subagent_completion(parent, layer, path)
    if completion is not None:
        values["completion"] = completion
    if layer.max_iterations is not None:
        values["max_iterations"] = layer.max_iterations
    if layer.first_output_timeout_seconds is not None:
        values["first_output_timeout_seconds"] = layer.first_output_timeout_seconds
    if layer.auto_compact_threshold is not None:
        values["auto_compact_threshold"] = layer.auto_compact_threshold
    builtins = _compile_subagent_builtins(layer)
    if builtins is not None:
        values["builtins"] = builtins
    if layer.sandbox_access is not None:
        if harness is not None:
            _require_access_in_sandbox(harness.sandbox, layer.sandbox_access, path)
        values["sandbox_access"] = layer.sandbox_access
    programmatic = _resolved_subagent_builtins(parent.builtins, builtins, path).programmatic_enabled
    # Inherited tools and MCP sources were compiled for the parent; a child whose programmatic tool
    # calling differs gets its own copy.
    inherited = harness if harness is not None and programmatic != parent.builtins.programmatic_enabled else None
    tools = subagent_tools(layer, path)
    if tools is not None:
        values["tools"] = [assemble._build_tool_definition(tool, programmatic=programmatic) for tool in tools]
    elif inherited is not None and inherited.tools:
        values["tools"] = [assemble._build_tool_definition(tool, programmatic=programmatic) for tool in inherited.tools]
    if layer.hooks is not None:
        values["hooks"] = [
            compiled.definition
            for index, hook in enumerate(layer.hooks)
            for compiled in assemble._compile_hook(index, hook, scope=path)
        ]
    mcps = layer.mcps
    if harness is not None and (tools is not None or mcps is not None):
        mcp_assembly.refuse_tool_namespaces(
            harness.tools if tools is None else tools, harness.mcps if mcps is None else mcps, subagent=path
        )
    if mcps is not None:
        values["mcps"] = assemble._resolve_mcp_model_access(mcps, programmatic=programmatic)
    elif inherited is not None and inherited.mcps:
        values["mcps"] = assemble._resolve_mcp_model_access(inherited.mcps, programmatic=programmatic)
    if layer.connectors is not None:
        values["connectors"] = assemble._build_connector_configuration(
            tuple(layer.connectors), layer.connector_discovery
        )
    if layer.skills is not None:
        values["skill_sources"] = sandbox_skills.skill_sources(layer.skills)
    if layer.subagents is None:
        return SubagentConfig.model_validate(values)
    resolved = resolve_subagent_config(parent, SubagentConfig.model_validate(values))
    nested_harness = (
        None
        if harness is None
        else SubagentHarness(
            tools=harness.tools if tools is None else tools,
            mcps=harness.mcps if mcps is None else mcps,
            sandbox=harness.sandbox,
        )
    )
    return SubagentConfig.model_validate(
        {
            **values,
            "subagents": compile_subagent_catalog(resolved, layer.subagents, harness=nested_harness, path=path),
        }
    )


def _compile_subagent_builtins(layer: subagent_authoring.Subagent) -> SubagentBuiltinsConfig | None:
    """Return the built-in switches the child sets; the ones it leaves out inherit."""

    if layer.builtins is None:
        return None
    config = authoring_types.builtins_to_config(layer.builtins)
    return SubagentBuiltinsConfig.model_validate(
        {name: getattr(config, name) for name in layer.builtins.model_fields_set}
    )


def _resolved_subagent_builtins(
    parent: BuiltinsConfig,
    layer: SubagentBuiltinsConfig | None,
    path: tuple[str, ...],
) -> BuiltinsConfig:
    if layer is None:
        return parent
    try:
        return layer.apply(parent)
    except ValueError as error:
        raise SdkError(f"Subagent {'/'.join(path)!r} builtins: {error}") from error


def _require_access_in_sandbox(
    sandbox: contracts.Sandbox, access: contracts.SandboxAccess, path: tuple[str, ...]
) -> None:
    """Reject a subagent access level the tree's sandbox cannot give."""

    if sandbox.is_executable:
        if contracts.access_covers(sandbox.supported_access, access):
            return
        raise SdkError(
            f"Subagent {'/'.join(path)!r} sets sandbox_access={access!r}, but {type(sandbox).__name__} "
            f"supports access up to {sandbox.supported_access!r}"
        )
    if access == "none":
        return
    raise SdkError(
        f"Subagent {'/'.join(path)!r} sets sandbox_access={access!r}, but the agent has "
        "no sandbox; without one, only 'none' is possible"
    )


def _compile_subagent_completion(
    parent: AgentConfig,
    layer: subagent_authoring.Subagent,
    path: tuple[str, ...],
) -> dict[str, JsonValue] | None:
    """Return the child's completion, or None when it inherits its parent's unchanged.

    ``provider`` or ``completion`` replace the parent's completion under the rules of
    ``agents.Agent``. ``model``, ``reasoning_effort`` and ``temperature`` change the inherited
    one, which must then use a built-in provider, and which loses its ``response_format``.
    """

    label = "/".join(path)
    if layer.provider is not None or layer.completion is not None:
        model = layer.model if layer.model is not None else cast(CompletionConfig, layer.completion).model
        try:
            return assemble.build_agent_config(
                model=model,
                provider=str(layer.provider or authoring_types.LLMProvider.MISTRAL),
                completion=layer.completion,
                name=parent.name,
                instructions=None,
                max_iterations=None,
                auto_compact_threshold=None,
                reasoning_effort=layer.reasoning_effort,
                temperature=layer.temperature,
            ).completion
        except UnsupportedAgentFeatureError as error:
            raise UnsupportedAgentFeatureError(error.feature, f"Subagent {label!r}: {error.reason}") from error
    overrides = [
        name
        for name, value in (
            ("model", layer.model),
            ("reasoning_effort", layer.reasoning_effort),
            ("temperature", layer.temperature),
        )
        if value is not None
    ]
    if not overrides:
        return None
    inherited = {key: value for key, value in parent.completion.items() if key != "response_format"}
    try:
        parsed = parse_completion_config(inherited)
    except UnsupportedCompletionProviderError:
        parsed = None
    if not isinstance(parsed, (MistralCompletionConfig, OpenAICompletionConfig, AnthropicCompletionConfig)):
        raise UnsupportedAgentFeatureError(
            "completion_provider",
            f"Subagent {label!r} sets {', '.join(overrides)}, which needs a built-in completion provider on its parent",
        )
    if layer.temperature is not None and isinstance(parsed, AnthropicCompletionConfig):
        raise UnsupportedAgentFeatureError(
            "temperature",
            f"Subagent {label!r} sets temperature, which the anthropic provider does not support",
        )
    completion = assemble._with_model_and_reasoning(
        parent.model_copy(update={"completion": inherited}),
        model=layer.model,
        reasoning_effort=layer.reasoning_effort,
    ).completion
    if layer.temperature is not None:
        completion = {**completion, "temperature": layer.temperature}
    return completion


def authored_subagent_layers(
    subagents: Sequence[subagent_authoring.Subagent],
    path: tuple[str, ...] = (),
) -> Iterator[tuple[tuple[str, ...], subagent_authoring.Subagent]]:
    """Yield every ``agents.Subagent`` in the catalog, nested ones included, with its path."""

    for entry in subagents:
        layer_path = (*path, entry.name)
        yield layer_path, entry
        yield from authored_subagent_layers(entry.subagents or (), layer_path)


def authored_mcp_layers(
    mcps: Mapping[str, McpHttpSourceConfiguration],
    subagents: Sequence[subagent_authoring.Subagent],
) -> Iterator[tuple[tuple[str, ...], Mapping[str, McpHttpSourceConfiguration]]]:
    """Yield the root's MCP sources, then each subagent's that declares its own, with its path.

    A subagent that leaves ``mcps`` unset inherits its parent's sources, so it adds no layer.
    """

    yield (), mcps
    for path, layer in authored_subagent_layers(subagents):
        if layer.mcps is not None:
            yield path, layer.mcps


def subagent_tools(
    layer: subagent_authoring.Subagent,
    path: tuple[str, ...],
) -> list[assemble._AuthoredTool] | None:
    """Return the tools a subagent declares, or None when it inherits its parent's."""

    bundled = [tool for hook in layer.hooks or () for tool in hook.tools]
    if layer.tools is None:
        if bundled:
            raise SdkError(
                f"Subagent {'/'.join(path)!r} has Hooks that bring tools "
                f"({', '.join(repr(tool_authoring.tool_name(tool)) for tool in bundled)}) but does not set tools; "
                "an unset tools list is inherited unchanged, so set tools on the subagent as well"
            )
        return None
    tools = cast(list[assemble._AuthoredTool], [*layer.tools, *bundled])
    names: set[str] = set()
    for tool in tools:
        tool_id = tool_authoring.tool_id(tool)
        if tool_id in names:
            raise ValueError(f"duplicate tool ID {tool_id!r} in subagent {'/'.join(path)!r}")
        names.add(tool_id)
    return tools


__all__ = [
    "SubagentHarness",
    "authored_subagent_layers",
    "compile_subagent_catalog",
    "compile_subagents",
    "subagent_tools",
]
