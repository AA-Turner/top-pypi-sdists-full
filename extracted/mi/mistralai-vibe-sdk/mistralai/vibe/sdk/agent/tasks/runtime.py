"""Task configuration, reconstruction, and registry.

Key types for SDK consumers:

- ``TaskConfigBase``: Subclass to define a new serializable task type.
  Subclasses with a ``type`` field auto-register for deserialization.
- ``ModuleTask[ConfigT]``: Base class for tasks backed by a StateModule.
  Provides ``execute()`` / ``run()`` / ``from_config()`` for both
  local and workflow execution paths.
- ``task_from_config(config)``: Reconstruct any task from its config.
- ``TaskExtension``: Install descriptor — binds a config class to its
  task class and optional workflow class.
- ``ModuleTaskRegistry``: Maps config types to task classes and workflow
  bindings for reconstruction and child-workflow dispatch.

Concrete built-in config types currently live in sdk.agent.tasks.agent_task
and sdk.capabilities.adapters.local_function.
"""

import asyncio
import inspect
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import BaseModel, model_validator

from mistralai.vibe.sdk.agent.tasks.core import Card, TaskCallback
from mistralai.vibe.sdk.execution_record.state import TaskState
from mistralai.vibe.sdk.transports.adapters.local import LocalChannel
from mistralai.vibe.sdk.transports.channel import Channel
from mistralai.vibe.sdk.transports.events import (
    DownstreamMessage,
    TaskStateUpdateEvent,
    TaskStateUpdatePayload,
)

if TYPE_CHECKING:
    from mistralai.vibe.sdk.agent.execution.loop import (
        DownstreamWriter,
        EffectExecutor,
        StateModule,
    )

ConfigT = TypeVar("ConfigT", bound=BaseModel)

__all__ = [
    "ModuleTask",
    "ModuleTaskRegistry",
    "QueueDownstreamWriter",
    "TaskConfigBase",
    "TaskExtension",
    "default_registry",
    "extract_impl_configs",
    "task_from_config",
]


# ---------------------------------------------------------------------------
# Open config registry
# ---------------------------------------------------------------------------

_CONFIG_REGISTRY: dict[str, type["TaskConfigBase"]] = {}


def _ensure_builtin_config_types() -> None:
    """Import built-in config types on first validation access."""
    if "agent" not in _CONFIG_REGISTRY:
        from mistralai.vibe.sdk.agent.tasks.agent_task import AgentTaskConfig  # noqa: F401

    if "tool" not in _CONFIG_REGISTRY:
        from mistralai.vibe.sdk.capabilities.adapters.local_function import (  # noqa: F401
            ToolTaskConfig,
        )


class TaskConfigBase(BaseModel):
    """Open base class for all serializable task configs.

    Subclass this and declare a ``type: Literal["my_type"] = "my_type"``
    field to define a new config type. Auto-registered at import time.

    Deserialization: ``TaskConfigBase.model_validate({"type": "agent", ...})``
    dispatches to the correct concrete class automatically.

    Guards:
    - Only direct subclasses of TaskConfigBase can register (no
      grandchild inheritance — subclassing an already-registered config
      raises ``TypeError``).
    - Duplicate ``type`` names raise ``TypeError`` at import time.
    """

    type: str

    def nested_configs(self) -> dict[str, "TaskConfigBase"]:
        """Collect all nested TaskConfigBase values from dict fields.

        Scans this config's fields for dict[str, TaskConfigBase] and
        returns a flat {name: config} mapping. Works for any config
        subclass without override.
        """
        result: dict[str, TaskConfigBase] = {}
        for field_name in type(self).model_fields:
            value = getattr(self, field_name)
            if isinstance(value, dict):
                for k, v in value.items():
                    if isinstance(v, TaskConfigBase):
                        result[k] = v
        return result

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        # Only register if 'type' is directly declared on this class
        if "type" not in cls.__annotations__:
            return
        type_field = cls.model_fields.get("type")
        if type_field is None or type_field.default is None:
            return
        type_name: str = type_field.default
        # Leaf-type rule: durable configs must be direct subclasses of
        # TaskConfigBase. Subclassing an already-registered config creates
        # inheritance-based polymorphism that breaks durable identity.
        for parent in cls.__mro__[1:]:
            if parent is TaskConfigBase:
                break
            parent_declares_type = "type" in inspect.get_annotations(parent)
            if parent_declares_type and parent in _CONFIG_REGISTRY.values():
                msg = (
                    f"Cannot register '{type_name}' as subclass of "
                    f"registered type '{parent.__name__}'. "
                    f"Durable config types must directly subclass TaskConfigBase."
                )
                raise TypeError(msg)
        if type_name in _CONFIG_REGISTRY:
            existing = _CONFIG_REGISTRY[type_name]
            if existing is not cls:
                msg = (
                    f"Duplicate TaskConfig type '{type_name}': "
                    f"{existing.__name__} and {cls.__name__}"
                )
                raise TypeError(msg)
        _CONFIG_REGISTRY[type_name] = cls

    @model_validator(mode="wrap")
    @classmethod
    def _dispatch_config(cls, data: Any, handler: Any) -> "TaskConfigBase":
        """Route dict data to the concrete config subclass.

        Raises ValueError when ``type`` is present but not registered,
        so missing extensions fail fast at deserialization time rather
        than silently stripping extension-specific fields.
        """
        if cls is not TaskConfigBase:
            result: TaskConfigBase = handler(data)
            return result
        _ensure_builtin_config_types()
        if isinstance(data, TaskConfigBase):
            return data
        if isinstance(data, dict):
            type_name = data.get("type")
            if type_name and type_name in _CONFIG_REGISTRY:
                concrete: TaskConfigBase = _CONFIG_REGISTRY[type_name].model_validate(data)
                return concrete
            if type_name:
                msg = (
                    f"Unknown TaskConfig type '{type_name}'. "
                    f"Registered types: {sorted(_CONFIG_REGISTRY)}. "
                    f"Install the extension that provides this type."
                )
                raise ValueError(msg)
        msg = (
            f"Cannot validate TaskConfigBase from {type(data).__name__}: "
            f"expected dict or TaskConfigBase instance"
        )
        raise ValueError(msg)


# ---------------------------------------------------------------------------
# TaskExtension — install descriptor for durable task types
# ---------------------------------------------------------------------------


def _derive_type_name(config_cls: type[TaskConfigBase]) -> str:
    """Derive the type name from a config class's ``type`` field default."""
    type_field = config_cls.model_fields.get("type")
    if type_field is None or type_field.default is None:
        msg = f"{config_cls.__name__} must declare a 'type' field with a default value"
        raise ValueError(msg)
    result: str = type_field.default
    return result


def _derive_workflow_name(workflow_cls: type) -> str:
    """Derive the workflow identifier from a @workflow.define-decorated class.

    Reads ``__temporal_workflow_definition.name`` set by the Mistral
    Workflows SDK ``@workflow.define(name=...)`` decorator. Raises
    ValueError if the attribute is absent — callers must pass a
    properly decorated workflow class, not an arbitrary type.
    """
    defn = getattr(workflow_cls, "__temporal_workflow_definition", None)
    if defn is not None:
        name = getattr(defn, "name", None)
        if isinstance(name, str):
            return name
    msg = (
        f"{workflow_cls.__name__} is not a @workflow.define-decorated class "
        f"(missing __temporal_workflow_definition attribute)"
    )
    raise ValueError(msg)


@dataclass(frozen=True)
class TaskExtension:
    """Install descriptor for a durable task type.

    Metadata is derived at install time, not duplicated:
    - ``type_name`` derived from ``config_cls.type`` default
    - ``workflow_name`` derived from ``workflow_cls`` decorator metadata
    - ``supports_child_dispatch`` defaults to ``True`` when ``workflow_cls``
      is present; explicit ``False`` for rare top-level-only durable tasks
    """

    config_cls: type[TaskConfigBase]
    task_cls: type["ModuleTask[Any]"]
    workflow_cls: type | None = None
    supports_child_dispatch: bool | None = None


# ---------------------------------------------------------------------------
# ModuleTaskRegistry
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _Binding:
    """Resolved install binding. Internal to the registry."""

    type_name: str
    config_cls: type[TaskConfigBase]
    task_cls: type["ModuleTask[Any]"]
    workflow_cls: type | None
    workflow_name: str | None
    supports_child_dispatch: bool


class ModuleTaskRegistry:
    """Registry for durable task reconstruction and workflow routing.

    Public API is ``install(TaskExtension(...))`` for registration and
    lookup methods for reconstruction/routing. Metadata is derived from
    the extension descriptor at install time.

    Config dispatch is a separate concern owned by ``TaskConfigBase``
    (Pydantic ``__pydantic_init_subclass__``). Activity cache stays in
    ``executor.py`` (keyed by module class). These ownership boundaries
    do not overlap.
    """

    def __init__(self) -> None:
        self._bindings: dict[str, _Binding] = {}
        self._builtins_installed = False

    def _ensure_builtins(self) -> None:
        """Lazily install built-in task types on first access."""
        if not self._builtins_installed:
            self._builtins_installed = True
            _install_builtins(self)

    def install(self, ext: TaskExtension) -> None:
        """Install a durable task extension.

        Derives ``type_name`` from ``config_cls``, ``workflow_name``
        from ``workflow_cls``, and defaults ``supports_child_dispatch``
        based on whether a workflow binding exists.

        Rejects duplicate installs. The one permitted upgrade path is
        adding a workflow binding to a type that was installed without
        one (the built-in lazy install pattern).
        """
        type_name = _derive_type_name(ext.config_cls)
        existing = self._bindings.get(type_name)

        if existing is not None:
            self._validate_upgrade(existing, ext, type_name)

        workflow_name: str | None = None
        if ext.workflow_cls is not None:
            workflow_name = _derive_workflow_name(ext.workflow_cls)

        if ext.supports_child_dispatch is not None:
            child_dispatch = ext.supports_child_dispatch
            if child_dispatch and ext.workflow_cls is None:
                msg = (
                    f"Cannot set supports_child_dispatch=True for '{type_name}' "
                    f"without a workflow_cls binding"
                )
                raise ValueError(msg)
        else:
            child_dispatch = ext.workflow_cls is not None

        self._bindings[type_name] = _Binding(
            type_name=type_name,
            config_cls=ext.config_cls,
            task_cls=ext.task_cls,
            workflow_cls=ext.workflow_cls,
            workflow_name=workflow_name,
            supports_child_dispatch=child_dispatch,
        )

    @staticmethod
    def _validate_upgrade(existing: _Binding, ext: TaskExtension, type_name: str) -> None:
        """Validate that a re-install is a legitimate workflow upgrade."""
        if existing.workflow_cls is not None:
            msg = (
                f"Task type '{type_name}' is already installed with "
                f"workflow {existing.workflow_cls.__name__}"
            )
            raise ValueError(msg)
        if ext.workflow_cls is None:
            msg = f"Task type '{type_name}' is already installed"
            raise ValueError(msg)
        if existing.config_cls is not ext.config_cls:
            msg = (
                f"Cannot upgrade '{type_name}': config_cls mismatch "
                f"({existing.config_cls.__name__} vs {ext.config_cls.__name__})"
            )
            raise ValueError(msg)
        if existing.task_cls is not ext.task_cls:
            msg = (
                f"Cannot upgrade '{type_name}': task_cls mismatch "
                f"({existing.task_cls.__name__} vs {ext.task_cls.__name__})"
            )
            raise ValueError(msg)

    def get_binding(self, type_name: str) -> _Binding | None:
        """Look up a resolved binding by config type name."""
        self._ensure_builtins()
        return self._bindings.get(type_name)

    def resolve_workflow_name(self, config: "TaskConfigBase") -> str:
        """Look up the workflow identifier for a config type.

        Returns the derived ``workflow_name``, or raises ValueError
        if no workflow is installed for the given config type.
        """
        self._ensure_builtins()
        binding = self._bindings.get(config.type)
        if binding is None or binding.workflow_name is None:
            msg = f"No workflow installed for config type '{config.type}'"
            raise ValueError(msg)
        return binding.workflow_name

    def task_from_config(self, config: "TaskConfigBase") -> Any:
        """Reconstruct a Task from an already-validated config."""
        self._ensure_builtins()
        binding = self._bindings.get(config.type)
        if binding is None:
            msg = f"No task installed for config type '{config.type}'"
            raise ValueError(msg)
        return binding.task_cls.from_config(config)


def _install_builtins(registry: ModuleTaskRegistry) -> None:
    """Install built-in task types (agent, tool)."""
    # Lazy imports to avoid circular dependencies
    from mistralai.vibe.sdk.agent.tasks.agent_task import AgentTask, AgentTaskConfig
    from mistralai.vibe.sdk.capabilities.adapters.local_function import ToolTask, ToolTaskConfig

    if "agent" not in registry._bindings:
        registry.install(TaskExtension(config_cls=AgentTaskConfig, task_cls=AgentTask))
    if "tool" not in registry._bindings:
        registry.install(TaskExtension(config_cls=ToolTaskConfig, task_cls=ToolTask))


default_registry = ModuleTaskRegistry()


def task_from_config(config: TaskConfigBase) -> Any:
    """Reconstruct a Task from a serializable config.

    Delegates to the default ModuleTaskRegistry.
    """
    return default_registry.task_from_config(config)


# ---------------------------------------------------------------------------
# QueueDownstreamWriter — shared by ModuleTask.run()
# ---------------------------------------------------------------------------


class QueueDownstreamWriter:
    """DownstreamWriter backed by an asyncio.Queue."""

    def __init__(self) -> None:
        self.queue: asyncio.Queue[DownstreamMessage | None] = asyncio.Queue()

    def send_patches(self, task_id: str, patches: list[Any]) -> None:
        self.queue.put_nowait(
            TaskStateUpdateEvent(payload=TaskStateUpdatePayload(task_id=task_id, patches=patches))
        )

    def send(self, message: DownstreamMessage) -> None:
        self.queue.put_nowait(message)

    def close(self) -> None:
        """Signal end-of-stream by pushing the sentinel."""
        self.queue.put_nowait(None)


# ---------------------------------------------------------------------------
# ModuleTask — base class for tasks backed by a StateModule
# ---------------------------------------------------------------------------


def extract_impl_configs(config: TaskConfigBase) -> dict[str, TaskConfigBase]:
    """Extract nested configs for workflow callback resolution."""
    return config.nested_configs()


class ModuleTask[ConfigT: BaseModel](ABC):
    """Base for tasks backed by a StateModule.

    Takes typed config, exposes execute() for workflow injection,
    implements run() for local execution. Satisfies the Task protocol.

    Subclasses must implement:
    - ``create_module()``: returns a fully configured StateModule.
    - ``from_config()``: classmethod to reconstruct from serializable config.
    """

    # Callback resolution — class default. Subclasses set in their own __init__.
    _resolvable_names: frozenset[str] = frozenset()

    def __init__(
        self,
        *,
        name: str = "",
        description: str = "",
        input_schema: dict[str, Any] | None = None,
        output_schema: dict[str, Any] | None = None,
        callbacks: list[TaskCallback] | None = None,
    ) -> None:
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.output_schema = output_schema
        self.callbacks: list[TaskCallback] = callbacks or []

    @property
    def resolvable_names(self) -> frozenset[str]:
        """Names of callbacks this task can resolve locally.

        For AgentTask: keys of tasks dict + keys of callback_implems.
        For ToolTask: empty (tools don't resolve child callbacks).
        """
        return self._resolvable_names

    @property
    def unresolved_callbacks(self) -> dict[str, TaskCallback]:
        """Callbacks this task delegates upstream — schemas keyed by name."""
        return {cb.card.name: cb for cb in self.callbacks}

    @abstractmethod
    def create_module(self) -> "StateModule":
        """Create a fully configured StateModule for this task."""
        ...

    @classmethod
    @abstractmethod
    def from_config(cls, config: Any, **kwargs: Any) -> "ModuleTask[Any]":
        """Reconstruct from serializable config."""
        ...

    @property
    def card(self) -> Card:
        return Card(
            name=self.name,
            description=self.description,
            input_schema=self.input_schema,
            output_schema=self.output_schema,
            callbacks=self.callbacks,
        )

    async def execute(
        self,
        state: TaskState,
        downstream: "DownstreamWriter",
        upstream_queue: asyncio.Queue[Any] | None = None,
        effect_executor: "EffectExecutor | None" = None,
    ) -> TaskState:
        """Run the module loop to completion and return the final TaskState.

        Constructs the StateModule via create_module(), wires up an
        ExecutionLoop, and runs it. Works for both local and workflow paths.
        """
        from mistralai.vibe.sdk.agent.execution.loop import ExecutionLoop

        module = self.create_module()
        loop = ExecutionLoop(state, module, downstream=downstream, effect_executor=effect_executor)
        loop._upstream = upstream_queue
        module.bind_exec_loop(loop, downstream=downstream)
        await loop.run(module.initial_action_type())
        return loop.state

    async def run(self, state: TaskState) -> Channel:
        """Start the task and return a Channel for streaming results.

        Local execution path — creates a queue-backed downstream, runs
        execute() in a background asyncio.Task, and returns a LocalChannel.
        """
        queue_downstream = QueueDownstreamWriter()
        upstream_queue: asyncio.Queue[Any] = asyncio.Queue()

        async def _run_and_close() -> None:
            try:
                await self.execute(state, queue_downstream, upstream_queue)
            finally:
                queue_downstream.close()

        bg_task = asyncio.create_task(_run_and_close())
        return LocalChannel(queue_downstream.queue, upstream_queue, bg_task)
