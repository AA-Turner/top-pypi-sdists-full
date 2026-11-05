"""Compile SDK-owned authoring into Unified Harness definitions and callbacks."""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Literal, NamedTuple, cast

from pydantic import BaseModel, JsonValue

from mistralai.vibe.harness.app_server.session import (
    AgentConfig,
    BuiltinsConfig,
    ConnectorAllowlistSelection,
    ConnectorAllSelection,
    ConnectorSelection,
    HookDefinition,
    McpHttpSourceConfiguration,
    MistralConnectorConfiguration,
    SubagentConfig,
    ToolDefinition,
)
from mistralai.vibe.harness.app_server.session import (
    PermissionPolicy as SessionPermissionPolicy,
)
from mistralai.vibe.harness.app_server.session import (
    ToolAnnotations as SessionToolAnnotations,
)
from mistralai.vibe.harness.app_server.session.models.configuration import (
    RegistrySkillSourceConfiguration,
    SkillSourceConfiguration,
)
from mistralai.vibe.harness.core import protocol as core_protocol
from mistralai.vibe.harness.runtime.capabilities import (
    CallableRegistration,
    CallbackRegistration,
    CapabilityBindingReference,
    CapabilityInvocationFailed,
    CapabilityRegistration,
    CapabilityRegistrationRegistry,
    HookInvocationBase,
    PostAgentTurnHookAccept,
    PostAgentTurnHookInvocation,
    PostLlmCallHookAccept,
    PostLlmCallHookInvocation,
    PostLlmCallHookReject,
    PostLlmCallHookRetry,
    PostToolCallHookContinue,
    PostToolCallHookInvocation,
    PreAgentTurnHookContinue,
    PreAgentTurnHookInvocation,
    PreAgentTurnHookSkip,
    PreLlmCallHookContinue,
    PreLlmCallHookInvocation,
    PreLlmCallHookSkip,
    PreToolCallHookContinue,
    PreToolCallHookInvocation,
    PreToolCallHookSkip,
    current_provided_tool_invocation,
)
from mistralai.vibe.harness.runtime.completion import (
    CompletionConfig,
    CompletionConfigBase,
    RetryConfig,
    UnsupportedCompletionProviderError,
    parse_completion_config,
    serialize_completion_config,
    structured_output,
)
from mistralai.vibe.harness.runtime.completion.profile import WireFormat, parse_reasoning
from mistralai.vibe.harness.runtime.completion.providers.anthropic import AnthropicCompletionConfig
from mistralai.vibe.harness.runtime.completion.providers.mistral import MistralCompletionConfig
from mistralai.vibe.harness.runtime.completion.providers.openai import OpenAICompletionConfig
from mistralai.vibe.harness.runtime.configuration import validate_permission_policy_tools
from mistralai.vibe.harness.runtime.hosts.workflows.harness_definition import (
    WorkflowCapabilityDefinition,
    WorkflowConnectorDefinition,
    WorkflowConnectorDiscovery,
    WorkflowHarnessDefinition,
    WorkflowHookPoint,
)
from mistralai.vibe.harness.runtime.session.definition import SessionSubagentConnectors
from mistralai.vibe_agents import session_workflow as wire
from mistralai.vibe_agents.sdk.app import config as app_config
from mistralai.vibe_agents.sdk.authoring import connector_selection, contracts, mcp_sources, session_input
from mistralai.vibe_agents.sdk.authoring import hooks as hook_authoring
from mistralai.vibe_agents.sdk.authoring import subagent as subagent_authoring
from mistralai.vibe_agents.sdk.authoring import tool as tool_authoring
from mistralai.vibe_agents.sdk.authoring import types as authoring_types
from mistralai.vibe_agents.sdk.authoring.errors import SdkError, UnsupportedAgentFeatureError
from mistralai.vibe_agents.sdk.authoring.skills import AllRegistrySkills, RegistrySkill, SandboxWorkspaceSkills
from mistralai.vibe_agents.sdk.authoring.tool_definition import ToolAnnotations
from mistralai.vibe_agents.sdk.authoring.tool_errors import (
    DEFAULT_TOOL_ERRORS,
    ToolCodeError,
    ToolError,
    ToolErrors,
    ToolFunctionError,
    call_is_cancelling,
    failed_tool_result,
)
from mistralai.workflows.plugins.mistralai.connectors import decorator as connector_decorator

from . import capabilities, sandbox_skills, stateful_hooks, tool_results
from . import sandbox as sandbox_assembly
from . import session_inputs as session_input_assembly
from . import subagents as subagent_assembly
from .stateful import StatefulRow, StateMap, snapshot

logger = logging.getLogger(__name__)

_HOOK_POINTS: tuple[WorkflowHookPoint, ...] = (
    "pre_agent_turn",
    "pre_llm_call",
    "post_llm_call",
    "post_agent_turn",
    "pre_tool_call",
    "post_tool_call",
)
type _AuthoredTool = tool_authoring.PythonTool[..., Any] | tool_authoring.ClientToolDefinition[BaseModel]
type AuthoredSubagent = subagent_authoring.Subagent


def _with_model_and_reasoning(
    config: AgentConfig,
    *,
    model: str | None,
    reasoning_effort: authoring_types.ReasoningEffort | None,
    feature: str = "completion_provider",
) -> AgentConfig:
    if model is None and reasoning_effort is None:
        return config
    try:
        completion = parse_completion_config(config.completion)
    except UnsupportedCompletionProviderError as error:
        raise UnsupportedAgentFeatureError(
            feature, "model and reasoning_effort overrides require a built-in completion provider"
        ) from error
    if isinstance(completion, CompletionConfigBase):
        raise UnsupportedAgentFeatureError(
            feature, "model and reasoning_effort overrides require a built-in completion provider"
        )
    if not isinstance(completion, (MistralCompletionConfig, OpenAICompletionConfig, AnthropicCompletionConfig)):
        raise UnsupportedAgentFeatureError(
            feature,
            f"model and reasoning_effort overrides are not supported with the {completion.type!r} completion "
            "config; set them on the completion config itself",
        )

    completion = completion.model_copy(deep=True)
    if model is not None:
        completion.model = model
    if reasoning_effort is not None:
        # OpenAI's names (none, minimal) become standard settings; each provider sends its own.
        setting = parse_reasoning(reasoning_effort, WireFormat.OPENAI_RESPONSES)
        if isinstance(completion, AnthropicCompletionConfig):
            completion.thinking = setting
        else:
            completion.reasoning_effort = setting

    serialized = serialize_completion_config(completion)
    return config.model_copy(
        update={
            "completion": {key: value for key, value in serialized.items() if key in completion.model_fields_set},
        }
    )


def with_session_agent_customization(config: AgentConfig, customization: wire.SessionAgentCustomization) -> AgentConfig:
    return _with_model_and_reasoning(
        config.model_copy(update={"instructions": customization.apply_to_instructions(config.instructions)}),
        model=customization.model,
        reasoning_effort=customization.reasoning_effort,
    )


@dataclass(frozen=True, slots=True)
class SandboxFileSkills:
    """The sandbox serves explicit bundles and discovered Registry skills for the agent tree.

    The root's explicit skills are written under ``/skills`` before the root starts. ``subagents`` holds the
    skills each child configuration declares; a child writes its own into a folder of its own when
    it starts, and a child that inherits reads its parent's. ``workspace`` says where the root finds
    the skills already in the sandbox. ``discovery`` lists metadata for accessible Registry skills;
    their files are downloaded on first skill-tool use.
    """

    skills: tuple[contracts.HarnessSkill, ...]
    subagents: tuple[tuple[contracts.HarnessSkill, ...], ...] = ()
    workspace: tuple[SandboxWorkspaceSkills, ...] = ()
    discovery: AllRegistrySkills | None = None


@dataclass(frozen=True, slots=True)
class AgentAssembly:
    """Portable Agent Configuration plus Host-owned live registrations."""

    config: AgentConfig
    registrations: CapabilityRegistrationRegistry
    sandbox: sandbox_assembly.AgentsSdkSandbox
    connector_slots: tuple[connector_decorator.ConnectorSlot, ...]
    connector_discovery: connector_selection.AllConnectors | None
    harness_definition: WorkflowHarnessDefinition
    hook_sandbox: contracts.HookSandbox
    # The one Session input class each declared input ID resolves to.
    session_input_classes: Mapping[str, type[session_input.SessionInput]]
    skills: SandboxFileSkills | None = None


CallbackContext = contracts.CallbackContext
HookCallbackContext = contracts.HookCallbackContext
ToolCallbackContext = contracts.ToolCallbackContext
CallbackSession = contracts.CallbackSession
KeepCallbackOpen = contracts.KeepCallbackOpen
Hook = contracts.Hook


def _serialize_completion(completion: CompletionConfig) -> dict[str, JsonValue]:
    if not isinstance(completion, MistralCompletionConfig):
        return serialize_completion_config(completion)
    settings = app_config.get_app_settings()
    if (server_url := settings.completion_gateway_server_url) is not None:
        completion = completion.with_gateway(
            base_url=server_url, api_key_env_var=settings.completion_gateway_api_key_env_var
        )
    return serialize_completion_config(completion)


def build_completion_http_headers(principal: wire.Principal, *, correlation_id: str | None = None) -> dict[str, str]:
    """Map a caller Principal to the completion gateway's identity headers.

    The band is always the lowest: the gateway places a request without one above every banded
    caller, and each completion replaces it with the customer's band from Albe.
    """

    headers = {
        "x-internal-key-scope": "vibe",
        "x-internal-org-tier": wire.DEFAULT_ORG_TIER,
        "x-consumer-custom-id": str(principal.customer_id),
        "x-organization-id": str(principal.organization_id),
        "x-workspace-id": str(principal.workspace_id),
    }
    if principal.user_id is not None:
        headers["x-user-id"] = str(principal.user_id)
    if (known := wire.known_correlation_id(correlation_id)) is not None:
        headers["x-internal-correlation-id"] = known
    return headers


def _completion_response_format(completion: CompletionConfig, response_format: type[BaseModel]) -> JsonValue:
    # A built-in config carries response_format like the config the SDK builds without completion=,
    # so an Agent can use structured output and still set a field the Agent has no option for
    # (base_url, api_timeout). A custom provider has no such field to honour. Among the built-in
    # configs, the structured-output builder decides which providers have a verified mapping.
    if isinstance(completion, CompletionConfigBase):
        raise UnsupportedAgentFeatureError(
            "structured_output",
            "structured_output is not supported together with a custom completion provider",
        )
    # Two formats would leave the Agent parsing one answer while the model is held to the other.
    if completion.response_format is not None:
        raise UnsupportedAgentFeatureError(
            "structured_output",
            "the completion config already sets response_format; pass output_type= on the Agent (or to run()) "
            "or on the completion config, not both",
        )
    return _structured_output_payload(response_format, provider=completion.type)


def _with_temperature(completion: CompletionConfig, temperature: float | None) -> CompletionConfig:
    if temperature is None:
        return completion
    if "temperature" not in type(completion).model_fields:
        raise UnsupportedAgentFeatureError(
            "temperature", f"the {type(completion).__name__} completion config has no temperature field"
        )
    return completion.model_copy(update={"temperature": temperature})


def _structured_output_payload(response_format: type[BaseModel], *, provider: str) -> JsonValue:
    try:
        payload = structured_output.build_structured_output_response_format(response_format, provider=provider)
    except structured_output.UnsupportedStructuredOutputProviderError as error:
        raise UnsupportedAgentFeatureError("structured_output", f"{error} on this backend") from error
    return cast(JsonValue, payload)


def build_agent_config(
    *,
    model: str,
    provider: str,
    name: str,
    instructions: str | None,
    max_iterations: int | None,
    auto_compact_threshold: int | None,
    builtins: BuiltinsConfig | None = None,
    completion: CompletionConfig | None = None,
    response_format: type[BaseModel] | None = None,
    reasoning_effort: authoring_types.ReasoningEffort | None = None,
    temperature: float | None = None,
    first_output_timeout_seconds: float | None = None,
    permission_policy: SessionPermissionPolicy | None = None,
) -> AgentConfig:
    """Compile the portable part of Agents SDK authoring into Harness data.

    `provider="mistral"` compiles to `MistralCompletionConfig(model=model)`, so it produces the same payload
    as a caller-supplied default `MistralCompletionConfig`. Both route through the configured completion
    gateway when they name no `base_url`. Any other caller-supplied `completion` (a built-in provider's
    config, or a custom provider's `mistralai.vibe.harness.runtime.completion.CompletionConfigBase` subclass)
    is serialized verbatim: it owns its own transport and credentials end to end.
    ``response_format`` is set on a built-in provider's config as it is on the default one; a custom provider
    refuses it. ``temperature`` and ``reasoning_effort`` replace the config's own value, and fail on a config
    that has no field for them.
    """

    completion_payload: dict[str, JsonValue]
    if completion is not None:
        completion_response_format = (
            None if response_format is None else _completion_response_format(completion, response_format)
        )
        completion_payload = _serialize_completion(_with_temperature(completion, temperature))
        if completion_response_format is not None:
            completion_payload["response_format"] = completion_response_format
    else:
        if provider not in {member.value for member in authoring_types.LLMProvider}:
            raise UnsupportedAgentFeatureError(
                "completion_provider",
                f"provider {provider!r} is not supported",
            )
        # Anthropic's Messages API has no sampling-temperature field; its runtime config rejects
        # unknown keys, so emitting it would fail provider construction.
        if temperature is not None and provider == authoring_types.LLMProvider.ANTHROPIC:
            raise UnsupportedAgentFeatureError(
                "temperature",
                "temperature is not supported by the anthropic provider; "
                "pass completion= with your own provider config to control anthropic sampling",
            )
        response_format_payload = (
            None if response_format is None else _structured_output_payload(response_format, provider=provider)
        )
        if provider == authoring_types.LLMProvider.MISTRAL:
            completion_payload = _serialize_completion(
                MistralCompletionConfig(
                    model=model,
                    temperature=temperature,
                    response_format=cast(dict[str, object] | None, response_format_payload),
                )
            )
        else:
            completion_payload = {
                "type": provider,
                "model": model,
                "retry": RetryConfig().model_dump(mode="json"),
            }
            if temperature is not None:
                completion_payload["temperature"] = temperature
            if response_format_payload is not None:
                completion_payload["response_format"] = response_format_payload
    agent_config = AgentConfig(
        completion=completion_payload,
        name=name,
        instructions=instructions or "",
        max_iterations=max_iterations,
        first_output_timeout_seconds=first_output_timeout_seconds,
        builtins=BuiltinsConfig() if builtins is None else builtins,
        auto_compact_threshold=auto_compact_threshold,
        permission_policy=permission_policy,
    )
    return _with_model_and_reasoning(
        agent_config, model=None, reasoning_effort=reasoning_effort, feature="reasoning_effort"
    )


def check_permission_policy_tools(
    config: AgentConfig,
    authored_harness: contracts.Harness,
    subagents: Sequence[AuthoredSubagent],
) -> None:
    """Reject a permission pattern that names a namespace of the tree's tools but none of them.

    Computed without compiling the tree, so a deploy can fail before it uploads anything. The
    check reads the tools and MCP sources of the whole tree, so every one the tree declares is
    listed on the root here: the root's, those its guardrails and Hooks bring, and every
    subagent's. Each MCP source is keyed by its position and keeps its own namespace.
    """

    layer_mcps = [
        authored_harness.mcps,
        *(layer.mcps or {} for _path, layer in subagent_assembly.authored_subagent_layers(subagents)),
    ]
    sources = [
        source.model_copy(update={"namespace": source.namespace or key})
        for mcps_of_layer in layer_mcps
        for key, source in mcps_of_layer.items()
    ]
    mcps = {str(index): source for index, source in enumerate(sources)}
    tools = [
        *authored_harness.tools,
        *(tool for guardrail in authored_harness.guardrails for tool in guardrail.tools),
        *(tool for hook in authored_harness.hooks for tool in hook.tools),
        *(
            tool
            for path, layer in subagent_assembly.authored_subagent_layers(subagents)
            for tool in subagent_assembly.subagent_tools(layer, path) or ()
        ),
    ]
    _validate_permission_policy_tools(
        config.model_copy(update={"tools": [_build_tool_definition(tool) for tool in tools], "mcps": mcps})
    )


def _validate_permission_policy_tools(config: AgentConfig) -> None:
    try:
        validate_permission_policy_tools(config, is_subagent=False)
    except ValueError as error:
        raise SdkError(str(error)) from error


def assemble_agent(
    config: AgentConfig,
    authored_harness: contracts.Harness,
    *,
    permission_mode: authoring_types.PermissionMode,
    subagents: Sequence[AuthoredSubagent] = (),
    session_id: str | None = None,
    capability_provider_id: str | None = None,
    capability_resolver: capabilities.WorkflowCapabilityResolver = (capabilities.workflow_capability_resolver),
    customization: wire.SessionAgentCustomization | None = None,
    tool_errors: ToolErrors = DEFAULT_TOOL_ERRORS,
) -> AgentAssembly:
    """Compile Unified Harness SDK capabilities into Harness definitions.

    ``subagents`` is the authored catalog ``config.subagents`` was compiled from. Each child is
    compiled again here, once, with the tool, MCP and sandbox access the Harness gives it.
    ``customization`` changes the root only: children keep the completion they derive from
    ``config``. Every function in the whole agent tree, the root's and each
    ``agents.Subagent``'s, gets one capability row in the root definition and one registration
    under ``capability_provider_id``; every subagent definition inherits that table unchanged.
    ``tool_errors`` is the root's ``Agent(tool_errors=...)``, for every Python tool of the tree.
    """

    if config.permission_policy is not None:
        config = config.model_copy(
            update={"permission_policy": SessionPermissionPolicy.model_validate(config.permission_policy.model_dump())}
        )

    connector_slots = tuple(authored_harness.connectors)
    connector_discovery = authored_harness.connector_discovery
    connector_config = _build_connector_configuration(connector_slots, connector_discovery)
    definitions: list[ToolDefinition] = []
    compiled_tools: list[tuple[_AuthoredTool, ToolDefinition]] = []
    table = _CapabilityTable(tool_errors=tool_errors)
    tools = [
        *authored_harness.tools,
        *(tool for guardrail in authored_harness.guardrails for tool in guardrail.tools),
        *(tool for hook in authored_harness.hooks for tool in hook.tools),
    ]
    names: set[str] = set()
    for tool in tools:
        tool_id = tool_authoring.tool_id(tool)
        if tool_id in names:
            raise SdkError(f"duplicate tool ID {tool_id!r}")
        names.add(tool_id)
        definition = _build_tool_definition(tool, programmatic=config.builtins.programmatic_enabled)
        definitions.append(definition)
        compiled_tools.append((tool, definition))
        table.add_tool(_tool_capability(tool, definition), tool, owner=())
    mcp_sources.refuse_tool_namespaces(tools, authored_harness.mcps)

    compiled_guardrails = [
        (guardrail, compiled)
        for index, guardrail in enumerate(authored_harness.guardrails)
        for compiled in _compile_hook(
            index,
            guardrail,
            namespace="guardrail",
        )
    ]
    compiled_authored_hooks = [
        (hook, compiled) for index, hook in enumerate(authored_harness.hooks) for compiled in _compile_hook(index, hook)
    ]
    guardrail_definitions = [compiled.definition for _hook, compiled in compiled_guardrails]
    hook_definitions = [compiled.definition for _hook, compiled in compiled_authored_hooks]
    compiled_hooks = [*compiled_guardrails, *compiled_authored_hooks]
    for hook, compiled in compiled_hooks:
        table.add_hook(compiled.capability, hook, owner=(), state_key=compiled.state_key)

    subagent_tools: list[_AuthoredTool] = []
    subagent_hooks: list[tuple[contracts.Hook, WorkflowHookPoint]] = []
    for path, layer in subagent_assembly.authored_subagent_layers(subagents):
        for tool in subagent_assembly.subagent_tools(layer, path) or ():
            table.add_tool(_tool_capability(tool, _build_tool_definition(tool)), tool, owner=path)
            subagent_tools.append(tool)
        for index, hook in enumerate(layer.hooks or ()):
            for compiled in _compile_hook(index, hook, scope=path):
                table.add_hook(compiled.capability, hook, owner=path, state_key=compiled.state_key)
                subagent_hooks.append((hook, compiled.point))
    stateful_hooks.check_hooks_rebuildable(
        [
            ((), (*authored_harness.guardrails, *authored_harness.hooks)),
            *((path, layer.hooks or ()) for path, layer in subagent_assembly.authored_subagent_layers(subagents)),
        ]
    )

    session_input_classes = session_input_assembly.collect_input_classes(
        [*(tool for tool, _definition in compiled_tools), *subagent_tools],
        [*((hook, compiled.point) for hook, compiled in compiled_hooks), *subagent_hooks],
        authored_harness.sandbox,
    )

    capability_definitions = list(table.rows)
    permission_policy = config.permission_policy
    if permission_mode in ("ask", "deny"):
        permission_policy = SessionPermissionPolicy(default=permission_mode)

    subagent_catalog = {
        **config.subagents,
        **subagent_assembly.compile_subagent_catalog(
            # The parent ``_to_agent_config`` compiled the catalog against.
            config.model_copy(update={"subagents": {}, "subagent_policy": None}),
            subagents,
            harness=subagent_assembly.SubagentHarness(
                tools=tools, mcps=authored_harness.mcps, sandbox=authored_harness.sandbox
            ),
        ),
    }
    if customization is not None:
        config = with_session_agent_customization(config, customization)
    sandbox = sandbox_assembly.compile_sandbox(authored_harness.sandbox, session_id=session_id)
    mcps = _resolve_mcp_model_access(authored_harness.mcps, programmatic=config.builtins.programmatic_enabled)
    mcp_sources.check_mcp_sources(mcps, programmatic=config.builtins.programmatic_enabled)
    skills = _skill_delivery(authored_harness, subagent_catalog, subagents)
    # Revalidate rather than copy so authored subagent layers are checked against the compiled
    # parent configuration they inherit from.
    compiled_config = AgentConfig.model_validate(
        {
            **{name: getattr(config, name) for name in AgentConfig.model_fields},
            "tools": definitions,
            "guardrails": guardrail_definitions,
            "hooks": hook_definitions,
            "mcps": mcps,
            "connectors": connector_config,
            # The sandbox holds skill files itself, so the Harness skill pipeline gets no source.
            "skill_sources": [],
            "permission_policy": permission_policy,
            # The access level is authored on the sandbox, but the Harness reads it from the agent:
            # the Session replaces agent_config.sandbox with the runtime sandbox.
            "sandbox_access": authored_harness.sandbox.access,
            "subagents": subagent_catalog,
        },
    ).model_copy(deep=True)
    _validate_permission_policy_tools(compiled_config)
    _require_subagent_capabilities_in_tree(
        compiled_config.subagents, {capability.binding_id for capability in capability_definitions}
    )
    # Register only once the whole tree has compiled, so a rejected tree leaves no stale entry.
    if capability_provider_id is not None:
        table.register(capability_resolver, capability_provider_id)
    sandbox_config = sandbox.config
    harness_definition = WorkflowHarnessDefinition(
        capability_provider_id=capability_provider_id,
        agent_config=compiled_config.model_copy(update={"sandbox": sandbox_config}, deep=True),
        sandbox=sandbox_config,
        capabilities=tuple(capability_definitions),
        mcps=mcps,
        connectors=connector_config,
        connector_resources=_connector_definitions(connector_slots),
        connector_discovery=_connector_discovery_definition(connector_discovery),
        subagent_connectors=_subagent_connector_records(subagents),
        session_id=session_id,
    )
    hook_sandbox = contracts.HookSandbox()
    # The saved values of this assembly's one Session, for the registrations built here.
    values = StateMap()
    registrations: list[CapabilityRegistration] = [
        *(
            _build_tool_registration(
                tool, definition, session_id=session_id, sandbox=hook_sandbox, tool_errors=tool_errors
            )
            for tool, definition in compiled_tools
        ),
        *(
            _build_hook_registration(
                StatefulRow(compiled.state_key, hook),
                compiled.point,
                compiled.definition,
                harness=harness_definition,
                session_id=session_id,
                sandbox=hook_sandbox,
                values=values,
            )
            for hook, compiled in compiled_hooks
        ),
    ]
    return AgentAssembly(
        config=compiled_config,
        registrations=CapabilityRegistrationRegistry(registrations),
        sandbox=sandbox,
        connector_slots=connector_slots,
        connector_discovery=connector_discovery,
        harness_definition=harness_definition,
        hook_sandbox=hook_sandbox,
        session_input_classes=session_input_classes,
        skills=skills,
    )


def declared_session_input_classes(
    config: AgentConfig,
    authored_harness: contracts.Harness,
    *,
    subagents: Sequence[AuthoredSubagent] = (),
) -> dict[str, type[session_input.SessionInput]]:
    """Map each Session input ID the agent tree's tools, hooks and sandbox hooks declare to its class.

    Computed without a Session or a Sandbox, from the same consumers
    ``assemble_agent`` compiles, so a worker can report its declarations before
    any Session exists.
    """

    tools = [
        *authored_harness.tools,
        *(tool for guardrail in authored_harness.guardrails for tool in guardrail.tools),
        *(tool for hook in authored_harness.hooks for tool in hook.tools),
    ]
    hooks = [
        *(
            (guardrail, compiled.point)
            for index, guardrail in enumerate(authored_harness.guardrails)
            for compiled in _compile_hook(
                index,
                guardrail,
                namespace="guardrail",
            )
        ),
        *(
            (hook, compiled.point)
            for index, hook in enumerate(authored_harness.hooks)
            for compiled in _compile_hook(index, hook)
        ),
    ]
    for path, layer in subagent_assembly.authored_subagent_layers(subagents):
        tools.extend(subagent_assembly.subagent_tools(layer, path) or ())
        hooks.extend(
            (hook, compiled.point)
            for index, hook in enumerate(layer.hooks or ())
            for compiled in _compile_hook(index, hook, scope=path)
        )
    return session_input_assembly.collect_input_classes(tools, hooks, authored_harness.sandbox)


def compile_harness_definition(
    config: AgentConfig,
    authored_harness: contracts.Harness,
    *,
    permission_mode: authoring_types.PermissionMode,
    subagents: Sequence[AuthoredSubagent] = (),
    session_id: str | None = None,
    capability_provider_id: str,
    capability_resolver: capabilities.WorkflowCapabilityResolver = (capabilities.workflow_capability_resolver),
) -> WorkflowHarnessDefinition:
    """Compile Unified Harness SDK authoring into a Vibe-owned Harness definition."""

    if not capability_provider_id.strip():
        raise ValueError("capability_provider_id must not be blank")
    return assemble_agent(
        config,
        authored_harness,
        permission_mode=permission_mode,
        subagents=subagents,
        session_id=session_id,
        capability_provider_id=capability_provider_id,
        capability_resolver=capability_resolver,
    ).harness_definition


def _skill_delivery(
    authored_harness: contracts.Harness,
    catalog: Mapping[str, SubagentConfig],
    subagents: Sequence[AuthoredSubagent],
) -> SandboxFileSkills | None:
    """Collect the skills of the whole tree, which its Sessions serve as files of one shared sandbox."""

    sandbox = authored_harness.sandbox
    skills = tuple(authored_harness.skills)
    workspace = tuple(authored_harness.workspace_skills)
    discovery = authored_harness.skill_discovery
    if workspace and not (sandbox._supports_files() and sandbox._supports_python):
        raise UnsupportedAgentFeatureError(
            "skills",
            "SandboxWorkspaceSkills finds skills with a Python program in the sandbox; use a sandbox that runs "
            "Python, such as environment=MistralSandbox()",
        )
    _check_skill_sandbox(skills, sandbox, owner=None, discovery=discovery)
    authored = {
        sandbox_skills.skill_sources_key(sandbox_skills.skill_sources(layer.skills)): tuple(layer.skills)
        for _path, layer in subagent_assembly.authored_subagent_layers(subagents)
        if layer.skills
    }
    declared: dict[str, tuple[contracts.HarnessSkill, ...]] = {}
    for path, layer in _subagent_config_layers(catalog):
        if not layer.skill_sources:
            continue
        key = sandbox_skills.skill_sources_key(layer.skill_sources)
        # A SubagentConfig carries no executable bits; an agents.Subagent keeps the bundles it was given.
        layer_skills = authored.get(key) or _skills_from_sources(layer.skill_sources)
        _check_skill_sandbox(layer_skills, sandbox, owner=f"Subagent {'/'.join(path)!r}")
        declared[key] = layer_skills
    if not (skills or declared or workspace or discovery is not None):
        return None
    return SandboxFileSkills(
        skills=skills, subagents=tuple(declared.values()), workspace=workspace, discovery=discovery
    )


def _subagent_config_layers(
    layers: Mapping[str, SubagentConfig], path: tuple[str, ...] = ()
) -> Iterator[tuple[tuple[str, ...], SubagentConfig]]:
    for name, layer in layers.items():
        layer_path = (*path, name)
        yield layer_path, layer
        yield from _subagent_config_layers(_nested_configs(layer), layer_path)


def _nested_configs(layer: SubagentConfig) -> Mapping[str, SubagentConfig]:
    return {} if layer.subagents is None else layer.subagents


def _skills_from_sources(sources: Sequence[SkillSourceConfiguration]) -> tuple[contracts.HarnessSkill, ...]:
    return tuple(
        RegistrySkill(id=source.id, version=source.version)
        if isinstance(source, RegistrySkillSourceConfiguration)
        else contracts.LocalSkillBundle(
            files=[
                contracts.LocalSkillFile(path=file.path, content_base64=file.content_base64) for file in source.files
            ]
        )
        for source in sources
    )


def _check_skill_sandbox(
    skills: Sequence[contracts.HarnessSkill],
    sandbox: contracts.Sandbox,
    *,
    owner: str | None,
    discovery: AllRegistrySkills | None = None,
) -> None:
    if not skills and discovery is None:
        return
    prefix = f"{owner} sets skills: " if owner is not None else ""
    if not sandbox._supports_files():
        raise UnsupportedAgentFeatureError(
            "skills",
            f"{prefix}skills are served as sandbox files and {type(sandbox).__name__}() cannot hold files; use a "
            "sandbox that holds files, such as environment=BashkitSandbox()",
        )
    unpinned = [str(skill.id) for skill in skills if isinstance(skill, RegistrySkill) and skill.version is None]
    if unpinned:
        raise UnsupportedAgentFeatureError(
            "skills",
            f"{prefix}registry skill {', '.join(unpinned)} has no version; sandbox files serve one exact "
            "version, so set RegistrySkill(version=...)",
        )


def _build_connector_configuration(
    slots: tuple[connector_decorator.ConnectorSlot, ...],
    discovery: connector_selection.AllConnectors | None = None,
) -> MistralConnectorConfiguration | None:
    if not slots and discovery is None:
        return None
    connector_decorator.raise_if_duplicate_connector_names(slots)

    authentication_modes = {slot.auto_auth for slot in slots}
    execution_identities = {slot.run_as.value for slot in slots}
    if discovery is not None:
        authentication_modes.add(discovery.auto_auth)
        # A discovered set is resolved against the Session user, so it fixes the
        # identity for the whole Session rather than agreeing with an authored one.
        execution_identities.add("auto")
    if len(authentication_modes) != 1:
        raise ValueError("All connectors on one Harness Session must use the same auto_auth value")
    if len(execution_identities) != 1:
        if discovery is not None:
            raise ValueError(
                "all_connectors() resolves the connector set on behalf of the Session user, so it "
                "cannot be combined with run_as='deployment' connectors"
            )
        raise ValueError("All connectors on one Harness Session must use the same run_as identity")

    selection: ConnectorSelection
    if discovery is not None:
        selection = ConnectorAllSelection()
    else:
        selection = ConnectorAllowlistSelection(connector_ids=[slot.connector_name for slot in slots])
    return MistralConnectorConfiguration(
        selection=selection,
        credential_names={
            slot.connector_name: slot.credentials_name for slot in slots if slot.credentials_name is not None
        },
        authentication=("interactive" if next(iter(authentication_modes)) else "existing_only"),
        execution_identity=cast(
            Literal["auto", "deployment"],
            next(iter(execution_identities)),
        ),
    )


def _connector_definitions(
    slots: Sequence[connector_decorator.ConnectorSlot],
) -> tuple[WorkflowConnectorDefinition, ...]:
    return tuple(
        WorkflowConnectorDefinition(
            connector_name=slot.connector_name,
            run_as=slot.run_as.value if slot.run_as_explicit else None,
            auto_auth=slot.auto_auth,
            credentials_name=slot.credentials_name,
            allow_mcp_ui=slot.allow_mcp_ui,
        )
        for slot in slots
    )


def _connector_discovery_definition(
    discovery: connector_selection.AllConnectors | None,
) -> WorkflowConnectorDiscovery | None:
    if discovery is None:
        return None
    return WorkflowConnectorDiscovery(
        exclude=discovery.exclude,
        max_connectors=discovery.max_connectors,
        auto_auth=discovery.auto_auth,
        allow_mcp_ui=discovery.allow_mcp_ui,
    )


def _subagent_connector_records(
    subagents: Sequence[AuthoredSubagent] | None,
) -> dict[str, SessionSubagentConnectors]:
    """Keep each child's connector slots and discovery filters, which its compiled layer cannot hold."""

    records: dict[str, SessionSubagentConnectors] = {}
    for layer in subagents or ():
        nested = _subagent_connector_records(layer.subagents)
        if layer.connectors is None and not nested:
            continue
        records[layer.name] = SessionSubagentConnectors(
            resources=_connector_definitions(layer.connectors or ()),
            discovery=_connector_discovery_definition(layer.connector_discovery),
            subagents=nested,
        )
    return records


def _build_tool_definition(tool: _AuthoredTool, *, programmatic: bool = True) -> ToolDefinition:
    if isinstance(tool, tool_authoring.PythonTool):
        described = tool.tool_definition
        name, description, input_schema = described.name, described.description, described.input_schema
        output_schema = described.output_schema or {}
    else:
        name, description, input_schema = tool.name, tool.description, tool.input_schema
        output_schema = tool.output_json_schema or {}
    return ToolDefinition(
        # The Harness reads no namespace as the default one. Leaving it unset keeps the binding IDs
        # that tools without a namespace had before namespace= existed.
        namespace=None if tool.namespace == tool_authoring.DEFAULT_TOOL_NAMESPACE else tool.namespace,
        name=name,
        description=description,
        input_schema=input_schema,
        output_schema=output_schema,
        model_access=tool_authoring.resolved_model_access(tool, programmatic=programmatic),
        required_session_input_ids=tool.required_input_ids,
        annotations=_declared_annotations(tool.annotations),
    )


def _declared_annotations(annotations: ToolAnnotations) -> SessionToolAnnotations | None:
    """The hints the tool declares, for the Harness to put on its approvals; None when it declares none.

    A hint left out stays off the wire, and every approver reads it with MCP's default.
    """

    declared = annotations.model_dump(include=annotations.model_fields_set)
    return SessionToolAnnotations(**declared) if declared else None


def _resolve_mcp_model_access(
    mcps: Mapping[str, McpHttpSourceConfiguration], *, programmatic: bool
) -> dict[str, McpHttpSourceConfiguration]:
    """The Harness sources for authored ``mcps``, direct when ``model_access`` is unset and the agent has no programs.

    This matches authored tools: an explicit ``"programmatic"`` is kept, so the Harness rejects it.
    Each source becomes the Harness model itself, never the stricter ``RemoteMCP`` subclass, so a
    definition compares equal to one read back from the wire.
    """

    resolved: dict[str, McpHttpSourceConfiguration] = {}
    for name, source in mcps.items():
        declared = source.model_dump(exclude_unset=True, by_alias=False)
        if not programmatic and "model_access" not in declared:
            declared["model_access"] = "direct"
        resolved[name] = McpHttpSourceConfiguration.model_validate(declared)
    return resolved


def _tool_context(
    definition: ToolDefinition, *, session_id: str | None, sandbox: contracts.HookSandbox | None
) -> contracts.ToolCallbackContext:
    """The context of the tool call running now: the Session, its sandbox and the call's ID."""

    invocation = current_provided_tool_invocation()
    if invocation is None:
        raise RuntimeError(f"Tool {definition.name!r} takes a ToolCallbackContext but runs outside a tool call")
    if session_id is None:
        raise RuntimeError(f"Tool {definition.name!r} takes a ToolCallbackContext but has no Session id")
    return contracts.ToolCallbackContext(
        contracts.CallbackSession(id=session_id, turn_id=invocation.turn_id),
        sandbox,
        tool_call_id=invocation.call_id,
    )


def _build_tool_registration(
    tool: _AuthoredTool,
    definition: ToolDefinition,
    *,
    session_id: str | None = None,
    sandbox: contracts.HookSandbox | None = None,
    tool_errors: ToolErrors = DEFAULT_TOOL_ERRORS,
) -> CapabilityRegistration:
    handler = getattr(tool, "handler", None)
    if handler is None:
        return CallbackRegistration(reference=CapabilityBindingReference(id=definition.binding_reference.id))

    async def invoke(**arguments: JsonValue) -> tool_results.ProvidedToolResult | CapabilityInvocationFailed:
        # The Harness passes injected_session_inputs only to tools that declare
        # inputs; for any other tool the name belongs to the model's arguments.
        injected_session_inputs = (
            cast(dict[str, JsonValue] | None, arguments.pop("injected_session_inputs", None))
            if tool.required_input_ids
            else None
        )
        try:
            if isinstance(tool, tool_authoring.PythonTool):
                if injected_session_inputs is not None:
                    arguments["injected_session_inputs"] = injected_session_inputs
                context = (
                    _tool_context(definition, session_id=session_id, sandbox=sandbox)
                    if tool_authoring.takes_context(tool)
                    else None
                )
                result = await tool._invoke_unconverted(context, dict(arguments))
            else:
                parsed = tool.input_model.model_validate(arguments)
                handler_kwargs: dict[str, object] = {"args": parsed}
                handler_kwargs.update(
                    session_input.rebuild_session_inputs(
                        f"Tool {definition.name!r}", tool.session_inputs, injected_session_inputs
                    )
                )
                try:
                    result = await tool_authoring.call_handler(handler, **handler_kwargs)
                except asyncio.CancelledError as error:
                    if call_is_cancelling():
                        raise
                    raise ToolFunctionError(error) from error
                except Exception as error:
                    raise ToolFunctionError(error) from error
        except ToolFunctionError as raised:
            return _tool_raised(raised.error, tool_name=definition.name, tool_errors=tool_errors)
        # The `output_schema=` model the result must match; a return annotation alone is not checked.
        result_schema = tool._output_model if isinstance(tool, tool_authoring.PythonTool) else tool.output_schema
        try:
            return tool_results.to_provided_tool_result(result, result_schema=result_schema)
        except tool_results.OutputSchemaMismatch as mismatch:
            return _output_schema_mismatch(mismatch, tool_name=definition.name, tool_errors=tool_errors)
        except Exception as error:  # noqa: BLE001 - a returned value that cannot be sent follows tool_errors
            return _tool_raised(error, tool_name=definition.name, tool_errors=tool_errors)

    return CallableRegistration(
        reference=CapabilityBindingReference(id=definition.binding_reference.id),
        callable=invoke,
    )


def _tool_raised(
    error: ToolCodeError, *, tool_name: str, tool_errors: ToolErrors
) -> tool_results.ProvidedToolResult | CapabilityInvocationFailed:
    """The result of a Python tool, by ``tool_errors``, whose function raised ``error`` or returned a value
    that cannot be sent (``error`` says why)."""

    if tool_errors == "raise" and not isinstance(error, ToolError):
        logger.error("Tool %s raised %s; the turn fails", tool_name, type(error).__name__, exc_info=error)
        # fail_turn: the Runtime ends the turn Failed with this error, instead of a failed call.
        # The message leaves the exception's text out: a subagent's failed turn goes to its parent's
        # model, which reads the tool's name and the exception's type only.
        return CapabilityInvocationFailed(
            error=core_protocol.ProtocolError(
                code="tool_raised",
                message=f"Tool {tool_name!r} raised {type(error).__name__}",
                retryable=False,
                details=None,
            ),
            fail_turn=True,
        )
    failed = failed_tool_result(error, tool_errors=tool_errors, tool_id=tool_name)
    return tool_results.to_provided_tool_result(failed, result_schema=None)


def _output_schema_mismatch(
    mismatch: tool_results.OutputSchemaMismatch, *, tool_name: str, tool_errors: ToolErrors
) -> tool_results.ProvidedToolResult | CapabilityInvocationFailed:
    """A Python tool's result that does not match its ``output_schema=``. Always logged; with ``"raise"``
    the turn fails, with ``"hide"`` and ``"show"`` the call fails and the model reads why."""

    logger.warning("Tool %s: %s", tool_name, mismatch.summary)
    if tool_errors != "raise":
        return mismatch.result
    return CapabilityInvocationFailed(
        error=core_protocol.ProtocolError(
            code="tool_output_schema_mismatch",
            message=f"Tool {tool_name!r}: {mismatch.summary}",
            retryable=False,
            details=None,
        ),
        fail_turn=True,
    )


class _CompiledHook(NamedTuple):
    definition: HookDefinition
    point: WorkflowHookPoint
    capability: WorkflowCapabilityDefinition
    # Every Hook point of one authored Hook shares this key, so they share one saved value.
    state_key: str


def _compile_hook(
    index: int,
    hook: contracts.Hook,
    *,
    scope: tuple[str, ...] = (),
    namespace: Literal["guardrail"] | None = None,
) -> list[_CompiledHook]:
    # A subagent's Hook names carry the subagent's path, so its Hook at index 0 never takes the
    # binding of the root's Hook at index 0. The model sees a Hook name only when a tool Hook
    # fails: the tool result then names the Hook that failed.
    prefix = "agents-sdk" if namespace is None else f"agents-sdk:{namespace}"
    if scope:
        prefix = f"{prefix}:subagent:{'/'.join(scope)}"
    state_key = f"{prefix}:{index}:{type(hook).__name__}"
    compiled: list[_CompiledHook] = []
    for point in _HOOK_POINTS:
        if getattr(type(hook), point) is getattr(contracts.Hook, point):
            continue
        name = f"{state_key}:{point}"
        definition = HookDefinition(
            type=cast(object, point),
            name=name,
            required_session_input_ids=session_input.required_input_ids(
                session_input_assembly.hook_declarations(hook, point)
            ),
        )
        compiled.append(
            _CompiledHook(
                definition,
                point,
                WorkflowCapabilityDefinition(
                    binding_id=definition.binding_reference.id,
                    kind="hook",
                    hook_key=_authored_hook_key(hook),
                    hook_point=point,
                ),
                state_key,
            )
        )
    return compiled


def _build_hook_registration(
    row: StatefulRow[contracts.Hook],
    point: WorkflowHookPoint,
    definition: HookDefinition,
    *,
    harness: WorkflowHarnessDefinition,
    session_id: str | None,
    sandbox: contracts.HookSandbox | None = None,
    values: StateMap,
) -> CallableRegistration:
    async def invoke(invocation: object) -> object:
        async def run(hook: contracts.Hook) -> object:
            return await _invoke_hook(
                hook,
                point,
                invocation,
                harness=harness,
                session_id=session_id,
                sandbox=sandbox,
            )

        return await row.call(values, run)

    return CallableRegistration(
        reference=CapabilityBindingReference(id=definition.binding_reference.id),
        callable=invoke,
    )


async def _invoke_hook(
    hook: contracts.Hook,
    point: WorkflowHookPoint,
    invocation: object,
    *,
    harness: WorkflowHarnessDefinition | None = None,
    session_id: str | None,
    sandbox: contracts.HookSandbox | None = None,
) -> _HookResult | CapabilityInvocationFailed:
    if session_id is None:
        raise RuntimeError("Harness Hook context requires a Session id")
    if not isinstance(invocation, HookInvocationBase):
        return _unsupported_hook_invocation(hook, invocation)
    context = HookCallbackContext(
        session=CallbackSession(id=session_id, turn_id=getattr(invocation, "turn_id", "")),
        sandbox=sandbox,
        _max_iterations=harness.agent_config.max_iterations if harness is not None else None,
    )
    session_inputs = session_input_assembly.rebuild_hook_session_inputs(hook, point, invocation)
    # ``None`` continues unchanged, as the base class does, and a decision becomes the point's result
    # of that kind. Each point names its result apart, so each keeps its own type.
    if point == "pre_agent_turn" and isinstance(invocation, PreAgentTurnHookInvocation):
        request = hook_authoring.pre_agent_turn_view(invocation)
        match turn_start := await hook.pre_agent_turn(context, request, **session_inputs):
            case None:
                # From the view, not the invocation: a Hook may have edited it in place. Blocks it
                # did not change come back as the originals.
                return PreAgentTurnHookContinue(user_content=request.user_content)
            case hook_authoring.HookDecision(kind="skip", message=message):
                return PreAgentTurnHookSkip(reason=_text(message))
            case PreAgentTurnHookContinue() | PreAgentTurnHookSkip():
                return turn_start
        raise _unexpected_result(hook, point, turn_start, accepted=("skip",))
    if point == "pre_llm_call" and isinstance(invocation, PreLlmCallHookInvocation):
        llm_call = hook_authoring.pre_llm_call_view(invocation)
        match llm_start := await hook.pre_llm_call(context, llm_call, **session_inputs):
            case None:
                return PreLlmCallHookContinue()
            case hook_authoring.HookDecision(kind="skip", message=message):
                return PreLlmCallHookSkip(reason=_text(message))
            case PreLlmCallHookContinue() | PreLlmCallHookSkip():
                return llm_start
        raise _unexpected_result(hook, point, llm_start, accepted=("skip",))
    if point == "post_llm_call" and isinstance(invocation, PostLlmCallHookInvocation):
        reply = hook_authoring.model_reply_view(hook_authoring.PostLlmCall, invocation)
        match llm_end := await hook.post_llm_call(context, reply, **session_inputs):
            case None:
                return PostLlmCallHookAccept()
            case hook_authoring.HookDecision(kind="retry", message=message):
                return PostLlmCallHookRetry(feedback=_text(message))
            case hook_authoring.HookDecision(kind="reject", message=message):
                return PostLlmCallHookReject(reason=_text(message))
            case PostLlmCallHookAccept() | PostLlmCallHookRetry() | PostLlmCallHookReject():
                return llm_end
        raise _unexpected_result(hook, point, llm_end, accepted=("retry", "reject"))
    if point == "post_agent_turn" and isinstance(invocation, PostAgentTurnHookInvocation):
        answer = hook_authoring.model_reply_view(hook_authoring.PostAgentTurn, invocation)
        match turn_end := await hook.post_agent_turn(context, answer, **session_inputs):
            case None:
                return PostAgentTurnHookAccept()
            case PostAgentTurnHookAccept():
                return turn_end
        raise _unexpected_result(hook, point, turn_end, accepted=())
    if point == "pre_tool_call" and isinstance(invocation, PreToolCallHookInvocation):
        pre_call = hook_authoring.pre_tool_call_view(invocation)
        match tool_start := await hook.pre_tool_call(context, pre_call, **session_inputs):
            case None:
                return PreToolCallHookContinue(effective_arguments=invocation.tool_call.call.arguments)
            case hook_authoring.HookDecision(kind="skip", message=message):
                return PreToolCallHookSkip(reason=_text(message))
            case PreToolCallHookContinue() | PreToolCallHookSkip():
                return tool_start
        raise _unexpected_result(hook, point, tool_start, accepted=("skip",))
    if point == "post_tool_call" and isinstance(invocation, PostToolCallHookInvocation):
        post_call = hook_authoring.post_tool_call_view(invocation)
        match tool_end := await hook.post_tool_call(context, post_call, **session_inputs):
            case None:
                # From the view, as for ``pre_agent_turn``; an unchanged result is the original.
                return PostToolCallHookContinue(
                    tool_result=hook_authoring.to_core_tool_result(post_call.tool_result, invocation.tool_result)
                )
            case hook_authoring.PostToolCallHookContinue(tool_result=tool_result):
                return PostToolCallHookContinue(
                    tool_result=hook_authoring.to_core_tool_result(tool_result, invocation.tool_result)
                )
            case PostToolCallHookContinue():
                # The Runtime's own result, with Runtime content: kept for code written against it.
                return tool_end
        raise _unexpected_result(hook, point, tool_end, accepted=())
    return _unsupported_hook_invocation(hook, invocation)


# Every result a Hook point hands back to the runtime.
type _HookResult = (
    PreAgentTurnHookContinue
    | PreAgentTurnHookSkip
    | PreLlmCallHookContinue
    | PreLlmCallHookSkip
    | PostLlmCallHookAccept
    | PostLlmCallHookRetry
    | PostLlmCallHookReject
    | PreToolCallHookContinue
    | PreToolCallHookSkip
    | PostToolCallHookContinue
    | PostAgentTurnHookAccept
)


def _text(message: str) -> list[core_protocol.ContentBlock]:
    return [core_protocol.TextContentBlock(text=message)]


def _unexpected_result(
    hook: contracts.Hook,
    point: WorkflowHookPoint,
    result: object,
    *,
    accepted: Sequence[hook_authoring.HookDecisionKind],
) -> SdkError:
    returned = (
        f"agents.{result.kind}(...)" if isinstance(result, hook_authoring.HookDecision) else type(result).__name__
    )
    decisions = f"agents.{' or agents.'.join(accepted)}" if accepted else "no decision"
    return SdkError(
        f"Hook {type(hook).__name__}.{point} returned {returned}, but {point} accepts None, its own result "
        f"type, or {decisions}"
    )


def _unsupported_hook_invocation(hook: contracts.Hook, invocation: object) -> CapabilityInvocationFailed:
    return CapabilityInvocationFailed(
        error=core_protocol.ProtocolError(
            code="unsupported_hook_invocation",
            message=f"Hook {type(hook).__name__} cannot handle {type(invocation).__name__}",
            retryable=False,
            details=None,
        )
    )


def _authored_tool_builder(
    capability: WorkflowCapabilityDefinition,
    tool: _AuthoredTool,
    *,
    tool_errors: ToolErrors,
) -> capabilities.CallableRegistrationBuilder:
    if capability.tool_name is None:
        raise ValueError(f"Tool capability {capability.binding_id!r} has no tool name")

    def build(definition: WorkflowHarnessDefinition, sandbox: contracts.HookSandbox) -> CallableRegistration:
        registration = _build_tool_registration(
            tool,
            _find_tool_definition(definition, capability.binding_id),
            session_id=definition.session_id,
            sandbox=sandbox,
            tool_errors=tool_errors,
        )
        if not isinstance(registration, CallableRegistration):
            raise ValueError(f"Tool {tool_authoring.tool_name(tool)!r} no longer has its registered worker callable")
        return registration

    return build


def _authored_hook_key(hook: contracts.Hook) -> str:
    return f"{type(hook).__module__}:{type(hook).__qualname__}"


def _authored_hook_builder(
    capability: WorkflowCapabilityDefinition,
    row: StatefulRow[contracts.Hook],
) -> capabilities.HookCallableRegistrationBuilder:
    if capability.hook_key is None:
        raise ValueError(f"Hook capability {capability.binding_id!r} has no hook key")
    if capability.hook_point is None:
        raise ValueError(f"Hook capability {capability.binding_id!r} has no hook point")
    point = capability.hook_point

    def build(
        definition: WorkflowHarnessDefinition,
        sandbox: contracts.HookSandbox,
        values: StateMap,
    ) -> CallableRegistration:
        return _build_hook_registration(
            row,
            point,
            _find_hook_definition(definition, capability.binding_id),
            harness=definition,
            session_id=definition.session_id,
            sandbox=sandbox,
            values=values,
        )

    return build


def _tool_capability(tool: _AuthoredTool, definition: ToolDefinition) -> WorkflowCapabilityDefinition:
    callback_backed = isinstance(tool, tool_authoring.ClientToolDefinition) and tool.handler is None
    return WorkflowCapabilityDefinition(
        binding_id=definition.binding_reference.id,
        kind="callback" if callback_backed else "tool",
        tool_name=tool_authoring.tool_name(tool),
    )


@dataclass(frozen=True, slots=True)
class _TableEntry:
    capability: WorkflowCapabilityDefinition
    function: _AuthoredTool | contracts.Hook
    owner: tuple[str, ...]
    state_key: str | None = None


class _CapabilityTable:
    """One capability row per binding identifier for a whole agent tree.

    A tree shares one registry keyed by binding identifier, so the same function may appear in
    several agents of the tree, but two different functions may not share one identifier.
    """

    def __init__(self, *, tool_errors: ToolErrors = DEFAULT_TOOL_ERRORS) -> None:
        self._entries: dict[str, _TableEntry] = {}
        self._tool_errors = tool_errors

    @property
    def rows(self) -> tuple[WorkflowCapabilityDefinition, ...]:
        return tuple(entry.capability for entry in self._entries.values())

    def add_tool(
        self,
        capability: WorkflowCapabilityDefinition,
        tool: _AuthoredTool,
        *,
        owner: tuple[str, ...],
    ) -> None:
        known = self._entries.get(capability.binding_id)
        if known is None:
            self._entries[capability.binding_id] = _TableEntry(capability, tool, owner)
            return
        if isinstance(known.function, contracts.Hook) or not _same_tool(known.function, tool):
            raise SdkError(
                f"Tool {tool_authoring.tool_id(tool)!r} is bound to two different functions in one agent tree: "
                f"{_function_label(known.function)} on {_owner_label(known.owner)} and "
                f"{_function_label(tool)} on {_owner_label(owner)}. Every agent in a tree shares one "
                "tool registry keyed by tool ID, so rename one of them or move it to another namespace, "
                "for example with @agents.tool(name=...) or @agents.tool(namespace=...)"
            )

    def add_hook(
        self,
        capability: WorkflowCapabilityDefinition,
        hook: contracts.Hook,
        *,
        owner: tuple[str, ...],
        state_key: str,
    ) -> None:
        known = self._entries.get(capability.binding_id)
        if known is None:
            self._entries[capability.binding_id] = _TableEntry(capability, hook, owner, state_key)
            return
        if not isinstance(known.function, contracts.Hook) or not _same_hook(known.function, hook):
            raise SdkError(
                f"Hook binding {capability.binding_id!r} is bound to two different Hooks in one agent tree: "
                f"{_function_label(known.function)} on {_owner_label(known.owner)} and "
                f"{_function_label(hook)} on {_owner_label(owner)}"
            )

    def register(
        self,
        capability_resolver: capabilities.WorkflowCapabilityResolver,
        capability_provider_id: str,
    ) -> None:
        callables: dict[str, capabilities.RegisteredBuilder[capabilities.CallableRegistrationBuilder]] = {}
        hook_callables: dict[str, capabilities.RegisteredBuilder[capabilities.HookCallableRegistrationBuilder]] = {}
        for binding_id, entry in self._entries.items():
            if isinstance(entry.function, contracts.Hook):
                if entry.state_key is None:
                    raise AssertionError(f"Hook binding {binding_id!r} has no state key")
                row = StatefulRow(entry.state_key, entry.function)
                hook_callables[binding_id] = capabilities.RegisteredBuilder(
                    _authored_hook_builder(entry.capability, row),
                    (entry.capability.hook_point, _hook_fingerprint(entry.function)),
                    state_key=row.key if row.has_state else None,
                )
            elif entry.capability.kind == "tool":
                callables[binding_id] = capabilities.RegisteredBuilder(
                    _authored_tool_builder(entry.capability, entry.function, tool_errors=self._tool_errors),
                    _tool_fingerprint(entry.function),
                )
        capability_resolver.register_provider(
            capability_provider_id, callables=callables, hook_callables=hook_callables
        )


def _tool_function(tool: _AuthoredTool) -> object:
    # A Python tool adapts its function to the handler it calls; compare the authored function.
    if isinstance(tool, tool_authoring.PythonTool):
        return tool.__wrapped__
    return tool.handler


# Authored tool attributes that shape what the one shared registration of a binding does. The
# description and the model access are not among them: each agent's own tool definition carries
# its model-visible text and how its model may call the tool.
_TOOL_BEHAVIOUR_ATTRIBUTES = (
    "input_model",
    "output_schema",
    "output_json_schema",
    "_context_parameter",
    "session_inputs",
)
_PER_AGENT_TOOL_FIELDS = {"description", "model_access"}


def _tool_fingerprint(tool: _AuthoredTool) -> object:
    """Everything about an authored tool that a shared binding depends on, minus per-agent fields."""

    definition = _build_tool_definition(tool).model_dump(mode="json", exclude=_PER_AGENT_TOOL_FIELDS)
    return (
        type(tool),
        _tool_function(tool),
        definition,
        tuple(getattr(tool, name, None) for name in _TOOL_BEHAVIOUR_ATTRIBUTES),
    )


def _hook_fingerprint(hook: contracts.Hook) -> object:
    if not type(hook).model_fields:
        # A Hook's settings are its fields, so a Hook without fields is told apart by its class only.
        return _authored_hook_key(hook)
    return snapshot(hook)


def _same_tool(known: _AuthoredTool | contracts.Hook, tool: _AuthoredTool) -> bool:
    if known is tool:
        return True
    if type(known) is not type(tool):
        return False
    known_tool = cast(_AuthoredTool, known)
    if _tool_function(tool) is None:
        # Two client callbacks of one name both route to the client that answers the callback.
        return _tool_function(known_tool) is None
    return _tool_fingerprint(known_tool) == _tool_fingerprint(tool)


def _same_hook(known: contracts.Hook, hook: contracts.Hook) -> bool:
    return known is hook or (type(known) is type(hook) and _hook_fingerprint(known) == _hook_fingerprint(hook))


def _function_label(function: _AuthoredTool | contracts.Hook) -> str:
    if isinstance(function, contracts.Hook):
        return f"Hook {type(function).__module__}.{type(function).__qualname__}"
    handler = _tool_function(function)
    if handler is None:
        return f"client tool {tool_authoring.tool_name(function)!r}"
    module = getattr(handler, "__module__", None)
    qualname = getattr(handler, "__qualname__", None) or type(handler).__qualname__
    return f"{module}.{qualname}" if module else qualname


def _owner_label(owner: tuple[str, ...]) -> str:
    return "the root agent" if not owner else f"subagent {'/'.join(owner)!r}"


def _require_subagent_capabilities_in_tree(
    layers: Mapping[str, SubagentConfig],
    bound: set[str],
    path: tuple[str, ...] = (),
) -> None:
    """Reject a subagent layer that declares a tool or Hook no function in the tree provides.

    Every agent in a tree binds the tree's one capability table, so a declaration without a row
    would otherwise fail only when that subagent starts. A layer that omits ``tools`` or
    ``hooks`` inherits declarations its parent was checked for, and the table does not depend
    on which layer spawns it, so checking what each authored layer sets covers every layer
    reachable through ``agents.spawn``, inherited catalogs included.
    """

    for name, layer in layers.items():
        layer_path = (*path, name)
        tools = [_tool_label(tool) for tool in layer.tools or () if tool.binding_reference.id not in bound]
        hooks = [hook.name for hook in layer.hooks or () if hook.binding_reference.id not in bound]
        if tools or hooks:
            raise SdkError(_unbound_subagent_capabilities_message(layer_path, tools, hooks))
        _require_subagent_capabilities_in_tree(_nested_configs(layer), bound, layer_path)


def _tool_label(tool: ToolDefinition) -> str:
    return tool.name if tool.namespace is None else f"{tool.namespace}.{tool.name}"


def _unbound_subagent_capabilities_message(path: tuple[str, ...], tools: list[str], hooks: list[str]) -> str:
    declared = " and ".join(
        part
        for part in (
            f"tools {', '.join(repr(name) for name in tools)}" if tools else "",
            f"Hooks {', '.join(repr(name) for name in hooks)}" if hooks else "",
        )
        if part
    )
    return (
        f"Subagent {'/'.join(path)!r} declares {declared} that no agent in this tree provides a function for. "
        "Give the subagent the function itself with agents.Subagent(tools=[...], hooks=[...]); a "
        "SubagentConfig built by hand only names tools and Hooks, so it can use only those another agent in the tree "
        "provides. "
        "Built-in tools are not declared in tools; select them with agents.Builtins and the sandbox access level"
    )


def _find_tool_definition(
    harness_definition: WorkflowHarnessDefinition,
    binding_id: str,
) -> ToolDefinition:
    for definition in harness_definition.agent_config.tools:
        if definition.binding_reference.id == binding_id:
            return definition
    raise ValueError(f"Harness definition has no tool definition for {binding_id!r}")


def _find_hook_definition(
    harness_definition: WorkflowHarnessDefinition,
    binding_id: str,
) -> HookDefinition:
    for definition in (
        *harness_definition.agent_config.guardrails,
        *harness_definition.agent_config.hooks,
    ):
        if definition.binding_reference.id == binding_id:
            return definition
    raise ValueError(f"Harness definition has no Hook definition for {binding_id!r}")


def to_json_value(value: object) -> JsonValue:
    # Models, also inside lists and dicts, by alias: a tool's output schema names their fields by alias.
    return tool_results.to_json_value(value)


__all__ = [
    "AgentAssembly",
    "CallbackContext",
    "CallbackSession",
    "Hook",
    "HookCallbackContext",
    "SandboxFileSkills",
    "ToolCallbackContext",
    "UnsupportedAgentFeatureError",
    "assemble_agent",
    "build_agent_config",
    "build_completion_http_headers",
    "compile_harness_definition",
]
