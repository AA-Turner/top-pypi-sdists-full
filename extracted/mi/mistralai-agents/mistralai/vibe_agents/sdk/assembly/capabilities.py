"""Resolve Workflow capability bindings without importing Nuage."""

from collections.abc import Callable, Mapping
from dataclasses import dataclass

from mistralai.vibe.harness.runtime.capabilities import (
    CallableRegistration,
    CallbackRegistration,
    CapabilityBindingReference,
    CapabilityRegistration,
    CapabilityRegistrationRegistry,
)
from mistralai.vibe.harness.runtime.hosts.workflows.harness_definition import (
    WorkflowCapabilityDefinition,
    WorkflowHarnessDefinition,
)
from mistralai.vibe_agents.sdk.assembly.stateful import StateMap
from mistralai.vibe_agents.sdk.authoring import connector_selection, contracts
from mistralai.workflows.plugins.mistralai.connectors import decorator as connector_decorator

# A tool builder gets the Session sandbox, for a tool that takes a ToolCallbackContext.
type CallableRegistrationBuilder = Callable[[WorkflowHarnessDefinition, contracts.HookSandbox], CallableRegistration]
# A Hook builder gets the Session's saved values; a stateful Hook reads and updates its own key there.
type HookCallableRegistrationBuilder = Callable[
    [WorkflowHarnessDefinition, contracts.HookSandbox, StateMap], CallableRegistration
]


class CapabilityNotRegisteredError(ValueError):
    """A declared capability has no builder registered under its provider in this worker process."""


class CapabilityRegistrationConflictError(ValueError):
    """A provider already registered a different function under the same binding identifier."""


@dataclass(frozen=True, slots=True)
class RegisteredBuilder[Builder]:
    builder: Builder
    # Compared with ``==`` to tell the same authored function from a different one; ``None``
    # means the caller gave no fingerprint, so only the same builder object counts as the same.
    fingerprint: object | None
    # Where the row keeps its saved value in a ``StateMap``; ``None`` for a row without state.
    state_key: str | None = None


class WorkflowCapabilityResolver:
    """Resolve compiler-registered callables for one Workflow Harness definition."""

    def __init__(self) -> None:
        self._callable_builders: dict[tuple[str, str], RegisteredBuilder[CallableRegistrationBuilder]] = {}
        self._hook_callable_builders: dict[tuple[str, str], RegisteredBuilder[HookCallableRegistrationBuilder]] = {}

    def register_callable(
        self,
        capability_provider_id: str,
        binding_id: str,
        builder: CallableRegistrationBuilder,
        *,
        fingerprint: object | None = None,
    ) -> None:
        """Register one worker-local builder for a stable capability provider.

        Raises ``CapabilityRegistrationConflictError`` when the provider already registered a
        different function under ``binding_id``.
        """

        self.register_provider(capability_provider_id, callables={binding_id: RegisteredBuilder(builder, fingerprint)})

    def register_hook_callable(
        self,
        capability_provider_id: str,
        binding_id: str,
        builder: HookCallableRegistrationBuilder,
        *,
        fingerprint: object | None = None,
    ) -> None:
        """Register one worker-local Hook builder that reaches the session sandbox.

        Raises ``CapabilityRegistrationConflictError`` when the provider already registered a
        different Hook under ``binding_id``.
        """

        self.register_provider(
            capability_provider_id, hook_callables={binding_id: RegisteredBuilder(builder, fingerprint)}
        )

    def register_provider(
        self,
        capability_provider_id: str,
        *,
        callables: Mapping[str, RegisteredBuilder[CallableRegistrationBuilder]] | None = None,
        hook_callables: Mapping[str, RegisteredBuilder[HookCallableRegistrationBuilder]] | None = None,
    ) -> None:
        """Register every builder of one provider, or none of them if any conflicts.

        Registering the same function again under a binding identifier replaces its builder; a
        different function raises ``CapabilityRegistrationConflictError`` before anything changes.
        """

        staged_callables = {
            (capability_provider_id, binding_id): registered for binding_id, registered in (callables or {}).items()
        }
        staged_hooks = {
            (capability_provider_id, binding_id): registered
            for binding_id, registered in (hook_callables or {}).items()
        }
        for key, incoming in staged_callables.items():
            if key in self._hook_callable_builders or not _same_builder(self._callable_builders.get(key), incoming):
                raise _conflict(key)
        for key, incoming_hook in staged_hooks.items():
            if key in self._callable_builders or not _same_builder(
                self._hook_callable_builders.get(key), incoming_hook
            ):
                raise _conflict(key)
        self._callable_builders.update(staged_callables)
        self._hook_callable_builders.update(staged_hooks)

    def unregister_provider(self, capability_provider_id: str) -> None:
        """Drop every builder this provider registered; a provider with none is left as it is."""

        for builders in (self._callable_builders, self._hook_callable_builders):
            for key in [key for key in builders if key[0] == capability_provider_id]:
                del builders[key]

    def build_capability_registrations(
        self,
        definition: WorkflowHarnessDefinition,
        *,
        sandbox: contracts.HookSandbox | None = None,
        values: StateMap | None = None,
    ) -> CapabilityRegistrationRegistry:
        """Build capability registrations for one durable Harness definition.

        ``values`` holds the saved values of the Session's stateful rows; give one map per Session.
        Raises ``CapabilityNotRegisteredError`` when any active row has no builder in this worker.
        """

        active = _active_binding_ids(definition)
        hook_sandbox = sandbox or contracts.HookSandbox()
        session_values = values if values is not None else StateMap()
        return CapabilityRegistrationRegistry(
            [
                self._build_registration(definition, capability, hook_sandbox, session_values)
                for capability in definition.capabilities
                if capability.binding_id in active
            ]
        )

    def build_capability_registration(
        self,
        definition: WorkflowHarnessDefinition,
        binding_id: str,
        *,
        sandbox: contracts.HookSandbox | None = None,
        values: StateMap | None = None,
    ) -> CapabilityRegistration | None:
        """Build the registration of one active capability row, or None when the definition has none.

        Only the requested row is built, so a row whose function this worker lacks cannot fail a
        call to another one. Raises ``CapabilityNotRegisteredError`` when the requested row itself
        has no builder in this worker. A stateful row reads and updates its value in ``values``.
        """

        if binding_id not in _active_binding_ids(definition):
            return None
        for capability in definition.capabilities:
            if capability.binding_id == binding_id:
                return self._build_registration(
                    definition,
                    capability,
                    sandbox or contracts.HookSandbox(),
                    values if values is not None else StateMap(),
                )
        return None

    def state_key(self, definition: WorkflowHarnessDefinition, binding_id: str) -> str | None:
        """Return where the row bound to ``binding_id`` keeps its saved value, or None without state."""

        if definition.capability_provider_id is None:
            return None
        key = (definition.capability_provider_id, binding_id)
        registered = self._hook_callable_builders.get(key) or self._callable_builders.get(key)
        return registered.state_key if registered is not None else None

    def bound_capabilities(self, definition: WorkflowHarnessDefinition) -> tuple[WorkflowCapabilityDefinition, ...]:
        """Return the active capability rows, checking only what the definition itself decides.

        No worker function is built, so a row whose function this worker lacks does not fail the
        Session that binds it: only calls to that row fail, when the capability activity builds it.
        Raises ``ValueError`` for a definition no worker can serve (no capability provider ID, an
        unsupported permission mode).
        """

        active = _active_binding_ids(definition)
        rows = tuple(capability for capability in definition.capabilities if capability.binding_id in active)
        for capability in rows:
            if capability.kind in {"tool", "hook"} and definition.capability_provider_id is None:
                raise _missing_provider_id()
            elif capability.kind not in {"callback", "tool", "hook"}:
                raise AssertionError(f"Unhandled capability kind {capability.kind!r}")
        return rows

    def _build_registration(
        self,
        definition: WorkflowHarnessDefinition,
        capability: WorkflowCapabilityDefinition,
        sandbox: contracts.HookSandbox,
        values: StateMap,
    ) -> CapabilityRegistration:
        if capability.kind == "callback":
            return CallbackRegistration(reference=CapabilityBindingReference(id=capability.binding_id))
        if capability.kind in {"tool", "hook"}:
            return self._build_registered_callable(definition, capability, sandbox, values)
        raise AssertionError(f"Unhandled capability kind {capability.kind!r}")

    def build_connector_slots(
        self,
        definition: WorkflowHarnessDefinition,
    ) -> tuple[connector_decorator.ConnectorSlot, ...]:
        """Build connector slots from their Vibe-owned durable fields."""

        return tuple(
            connector_decorator.connector(
                resource.connector_name,
                run_as=resource.run_as,
                auto_auth=resource.auto_auth,
                credentials_name=resource.credentials_name,
                allow_mcp_ui=resource.allow_mcp_ui,
            )
            for resource in definition.connector_resources
        )

    def build_connector_discovery(
        self,
        definition: WorkflowHarnessDefinition,
    ) -> connector_selection.AllConnectors | None:
        """Build the run-time connector selection from its durable fields."""

        discovery = definition.connector_discovery
        if discovery is None:
            return None
        return connector_selection.AllConnectors(
            exclude=tuple(discovery.exclude),
            max_connectors=discovery.max_connectors,
            auto_auth=discovery.auto_auth,
            allow_mcp_ui=discovery.allow_mcp_ui,
        )

    def _build_registered_callable(
        self,
        definition: WorkflowHarnessDefinition,
        capability: WorkflowCapabilityDefinition,
        sandbox: contracts.HookSandbox,
        values: StateMap,
    ) -> CallableRegistration:
        if definition.capability_provider_id is None:
            raise _missing_provider_id()
        key = (definition.capability_provider_id, capability.binding_id)
        if (hook_builder := self._hook_callable_builders.get(key)) is not None:
            registration = hook_builder.builder(definition, sandbox, values)
        elif (tool_builder := self._callable_builders.get(key)) is not None:
            registration = tool_builder.builder(definition, sandbox)
        else:
            raise CapabilityNotRegisteredError(
                f"Capability {capability.binding_id!r} is not registered for "
                f"provider {definition.capability_provider_id!r} in this worker process"
            )
        if registration.reference.id != capability.binding_id:
            raise ValueError(
                f"Capability builder registered {registration.reference.id!r} for {capability.binding_id!r}"
            )
        return registration


def _active_binding_ids(definition: WorkflowHarnessDefinition) -> set[str]:
    # Rows a layer does not declare belong to other agents of the tree and are never bound here.
    config = definition.agent_config
    return {tool.binding_reference.id for tool in config.tools} | {
        hook.binding_reference.id for hook in (*config.guardrails, *config.hooks)
    }


def _missing_provider_id() -> ValueError:
    return ValueError(
        "Workflow Harness definition has no capability provider ID; "
        "deploy the Workflow again before executing capabilities"
    )


def _same_builder[Builder](known: RegisteredBuilder[Builder] | None, incoming: RegisteredBuilder[Builder]) -> bool:
    if known is None or known.builder is incoming.builder:
        return True
    if known.fingerprint is None or incoming.fingerprint is None:
        return False
    return known.fingerprint == incoming.fingerprint


def _conflict(key: tuple[str, str]) -> CapabilityRegistrationConflictError:
    provider, binding_id = key
    return CapabilityRegistrationConflictError(
        f"Capability provider {provider!r} already registered a different function for {binding_id!r} "
        "in this worker process; give each agent its own Workflow name or rename one of the tools"
    )


workflow_capability_resolver = WorkflowCapabilityResolver()


__all__ = [
    "CapabilityNotRegisteredError",
    "CapabilityRegistrationConflictError",
    "WorkflowCapabilityResolver",
    "workflow_capability_resolver",
]
