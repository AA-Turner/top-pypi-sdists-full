"""Collect, check and bind the Session inputs that tools, hooks and sandbox hooks declare."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import cast

from pydantic import JsonValue

from mistralai.vibe.harness.app_server.session import AgentConfig
from mistralai.vibe.harness.runtime.capabilities import HookInvocationBase
from mistralai.vibe.harness.runtime.configuration import (
    validate_session_input_declarations,
    validate_session_input_schema_isolation,
)
from mistralai.vibe.harness.runtime.hosts.workflows.harness_definition import WorkflowHookPoint
from mistralai.vibe_agents.sdk.authoring import contracts, session_input
from mistralai.vibe_agents.sdk.authoring import tool as tool_authoring
from mistralai.vibe_agents.sdk.authoring.errors import SdkError

from . import sandbox as sandbox_assembly


def hook_declarations(hook: contracts.Hook, point: WorkflowHookPoint) -> Mapping[str, type[session_input.SessionInput]]:
    """Map each Session input parameter of a Hook method to its class."""

    return session_input.method_session_inputs(contracts.Hook, hook, point)


def rebuild_hook_session_inputs(
    hook: contracts.Hook,
    point: WorkflowHookPoint,
    invocation: HookInvocationBase,
) -> dict[str, object]:
    """Rebuild a Hook method's declared Session inputs from its invocation."""

    return session_input.rebuild_session_inputs(
        f"Hook {_hook_name(hook, point)}",
        hook_declarations(hook, point),
        invocation.injected_session_inputs,
    )


def collect_input_classes(
    tools: Sequence[contracts.HarnessTool],
    hooks: Sequence[tuple[contracts.Hook, WorkflowHookPoint]],
    sandbox: contracts.Sandbox,
) -> dict[str, type[session_input.SessionInput]]:
    """Map each input ID the consumers declare to its class, rejecting two classes that claim one ID.

    An input ID keys exactly one value per Session, rebuilt into the declaring class
    on delivery: two classes sharing an ID would rebuild one value into both shapes.
    """

    consumers: list[tuple[str, Mapping[str, type[session_input.SessionInput]]]] = [
        *((f"tool {tool_authoring.tool_name(tool)!r}", tool.session_inputs) for tool in tools),
        *((f"hook {_hook_name(hook, point)}", hook_declarations(hook, point)) for hook, point in hooks),
        *sandbox_assembly.sandbox_hook_session_input_consumers(sandbox),
    ]
    classes: dict[str, type[session_input.SessionInput]] = {}
    declared_by: dict[str, str] = {}
    for consumer, declarations in consumers:
        for input_class in declarations.values():
            input_id = session_input.require_input_id(input_class)
            known = classes.setdefault(input_id, input_class)
            if known is not input_class:
                raise SdkError(
                    f"Session input {input_id!r} is declared by two classes: "
                    f"{known.__module__}.{known.__qualname__} ({declared_by[input_id]}) and "
                    f"{input_class.__module__}.{input_class.__qualname__} ({consumer})"
                )
            declared_by.setdefault(input_id, consumer)
    return classes


def _hook_name(hook: contracts.Hook, point: WorkflowHookPoint) -> str:
    return f"{type(hook).__name__}.{point}"


def bind_session_inputs(
    config: AgentConfig,
    sandbox: sandbox_assembly.AgentsSdkSandbox,
    session_inputs: Mapping[str, JsonValue],
    *,
    sandbox_is_live: bool,
) -> None:
    """Check a Session's inputs against every declaration, then bind them for its sandbox hooks.

    Call before the sandbox is provisioned; raises ``ValueError`` when an input is
    missing, unusable, or collides with a model-visible tool argument. A live
    sandbox skips the sandbox hook check.
    """

    validate_session_input_declarations(config, session_inputs)
    validate_session_input_schema_isolation(config)
    sandbox.bind_session_inputs(session_inputs, sandbox_is_live=sandbox_is_live)


def serialize_session_inputs(
    inputs: Mapping[str, contracts.SessionInput] | None,
    *,
    declared_classes: Mapping[str, type[session_input.SessionInput]] | None = None,
) -> dict[str, JsonValue]:
    """Validate caller-supplied Session inputs and serialize them to JSON.

    Each dictionary key must equal its value class's ``input_id`` so a caller
    cannot mistype one. When the Agent's declared classes are known, a value
    must be an instance of the class declared for its ID: another class that
    merely shares the ID would be rebuilt into the wrong shape on delivery.
    """

    if not inputs:
        return {}
    serialized: dict[str, JsonValue] = {}
    for key, value in inputs.items():
        if not isinstance(value, contracts.SessionInput):
            raise SdkError(f"Session input {key!r} must be an agents.SessionInput instance")
        input_id = session_input.require_input_id(type(value))
        if key != input_id:
            raise SdkError(f"Session input key {key!r} must equal its value's input_id {input_id!r}")
        declared_class = (declared_classes or {}).get(input_id)
        if declared_class is not None and not isinstance(value, declared_class):
            raise SdkError(
                f"Session input {input_id!r} is a {type(value).__module__}.{type(value).__qualname__}, "
                f"but this Agent declares {declared_class.__module__}.{declared_class.__qualname__} for it"
            )
        serialized[input_id] = cast(JsonValue, value.model_dump(mode="json"))
    return serialized


def with_omitted_optional_inputs(
    input_classes: Mapping[str, type[session_input.SessionInput]],
    supplied: Mapping[str, JsonValue],
) -> dict[str, JsonValue]:
    """Return ``supplied`` plus an empty value for each omitted input whose fields all have defaults.

    A caller may omit such an input, as the control plane accepts: its consumers then
    receive the class's defaults.
    """

    omitted: dict[str, JsonValue] = {
        input_id: {}
        for input_id, input_class in input_classes.items()
        if input_id not in supplied and not any(field.is_required() for field in input_class.model_fields.values())
    }
    return {**omitted, **supplied}


__all__ = [
    "bind_session_inputs",
    "collect_input_classes",
    "hook_declarations",
    "rebuild_hook_session_inputs",
    "serialize_session_inputs",
    "with_omitted_optional_inputs",
]
