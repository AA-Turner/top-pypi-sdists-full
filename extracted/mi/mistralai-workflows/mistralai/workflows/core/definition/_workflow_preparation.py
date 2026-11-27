from collections.abc import Iterator, Sequence
from contextlib import ExitStack, contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from threading import Lock
from typing import Type, TypeVar

import temporalio.workflow
from temporalio.common import VersioningBehavior

from mistralai.workflows.core._logger import get_logger
from mistralai.workflows.core.config.config import (
    AppConfig,
    WorkerConfig,
    WorkerVersioningConfig,
    WorkflowDecoratorConfig,
    _use_workflow_config,
    resolve_worker_config,
    use_config,
)
from mistralai.workflows.core.definition.workflow_definition import (
    get_workflow_definition,
    mount_workflow,
    set_workflow_definition,
)
from mistralai.workflows.exceptions import ErrorCode, WorkflowsException
from mistralai.workflows.models import WorkflowSpec

logger = get_logger(__name__)

ClassType = TypeVar("ClassType", bound=Type)


@dataclass(frozen=True)
class WorkflowDecoratorMetadata:
    name: str
    enforce_determinism: bool | None


@dataclass(frozen=True)
class RegisteredIdentity:
    name: str
    enforce_determinism: bool


def registered_identity(
    metadata: WorkflowDecoratorMetadata, worker_config: WorkerConfig | WorkflowDecoratorConfig
) -> RegisteredIdentity:
    """Return the name and determinism setting a worker registers for a decorated workflow."""
    return RegisteredIdentity(
        name=f"{worker_config.workflow_name_prefix}{metadata.name}",
        enforce_determinism=metadata.enforce_determinism
        if metadata.enforce_determinism is not None
        else worker_config.default_enforce_determinism,
    )


@dataclass(frozen=True)
class _TemporalWorkflowDefinitionConfig:
    name: str
    sandboxed: bool
    versioning_behavior: VersioningBehavior


_TEMPORAL_DEFINITION_CONFIG_ATTR = "__workflows_temporal_definition_config"
_temporal_definition_lock = Lock()
_active_preparation_config: ContextVar[AppConfig | None] = ContextVar(
    "mistral_workflows_active_preparation_config",
    default=None,
)


def _keep_context_arg_for_parameterless_entrypoint(workflow_type: ClassType) -> None:
    # temporalio>=1.31 truncates decoded workflow args to len(arg_types), so an empty list drops the
    # PayloadWithContext the SDK always sends; None makes it decode every payload untyped.
    defn = temporalio.workflow._Definition.must_from_class(workflow_type)
    if defn.arg_types == []:
        object.__setattr__(defn, "arg_types", None)


def build_temporal_definition_config(
    name: str,
    sandboxed: bool,
    versioning: WorkerVersioningConfig,
) -> _TemporalWorkflowDefinitionConfig:
    versioning_behavior = (
        VersioningBehavior.PINNED
        if versioning.enabled and versioning.deployment_name and versioning.build_id
        else VersioningBehavior.UNSPECIFIED
    )
    return _TemporalWorkflowDefinitionConfig(
        name=name,
        sandboxed=sandboxed,
        versioning_behavior=versioning_behavior,
    )


def ensure_temporal_workflow_definition(
    workflow_type: ClassType,
    requested: _TemporalWorkflowDefinitionConfig,
) -> None:
    """Apply Temporal's public decorator once, rejecting later incompatible worker configs."""
    with _temporal_definition_lock:
        _ensure_temporal_workflow_definition_locked(workflow_type, requested)


def _check_temporal_workflow_definition_locked(
    workflow_type: ClassType,
    requested: _TemporalWorkflowDefinitionConfig,
) -> bool:
    """Return whether Temporal's decorator still has to be applied, rejecting incompatible configs."""
    existing = getattr(workflow_type, _TEMPORAL_DEFINITION_CONFIG_ATTR, None)
    if existing is None:
        return True
    if existing != requested:
        raise WorkflowsException(
            code=ErrorCode.WORKFLOW_DEFINITION_ERROR,
            message=(
                f"Workflow class {workflow_type.__name__!r} is already configured for Temporal with "
                f"{existing}. It cannot be reused in the same process with {requested}. "
                "Use the same workflow definition settings for every worker or run differently configured "
                "workers in separate processes."
            ),
        )
    return False


def _ensure_temporal_workflow_definition_locked(
    workflow_type: ClassType,
    requested: _TemporalWorkflowDefinitionConfig,
) -> None:
    if _check_temporal_workflow_definition_locked(workflow_type, requested):
        _apply_temporal_workflow_definition_locked(workflow_type, requested)


def _apply_temporal_workflow_definition_locked(
    workflow_type: ClassType,
    requested: _TemporalWorkflowDefinitionConfig,
) -> None:
    if not requested.sandboxed:
        logger.warning(
            "Workflow registered with determinism enforcement disabled. "
            "This may lead to non-deterministic behavior and replay failures.",
            workflow_name=requested.name,
        )

    temporalio.workflow.defn(
        name=requested.name,
        sandboxed=requested.sandboxed,
        versioning_behavior=requested.versioning_behavior,
    )(workflow_type)
    _keep_context_arg_for_parameterless_entrypoint(workflow_type)
    setattr(workflow_type, _TEMPORAL_DEFINITION_CONFIG_ATTR, requested)

    if requested.versioning_behavior == VersioningBehavior.PINNED:
        logger.info("Workflow registered with PINNED versioning behavior", workflow_name=requested.name)
    else:
        logger.info("Workflow registered WITHOUT versioning behavior", workflow_name=requested.name)


def configure_workflow_for_worker(
    workflow_type: ClassType,
    config: AppConfig,
    mounts: ExitStack,
    *,
    replay_namespace: str | None = None,
) -> None:
    """Resolve definition-time settings immediately before constructing a worker."""
    configure_workflows_for_worker([workflow_type], config, mounts, replay_namespace=replay_namespace)


def configure_workflows_for_worker(
    workflow_types: Sequence[ClassType],
    config: AppConfig,
    mounts: ExitStack,
    *,
    replay_namespace: str | None = None,
) -> None:
    """Resolve definition-time settings for a complete worker workflow set.

    Each workflow is mounted under its configured name on ``mounts`` and stays mounted until that
    stack closes. While a worker mounts a name, another workflow class cannot use it. Replay
    preparation, given its ``replay_namespace``, mounts only within that namespace.
    """
    with _temporal_definition_lock, ExitStack() as pending_mounts:
        # First mount and validate the complete set, so a conflict changes nothing: no name stays
        # mounted, and no Temporal or SDK definition is applied to any class.
        prepared: list[tuple[ClassType, _TemporalWorkflowDefinitionConfig | None, WorkflowSpec]] = []
        for workflow_type in workflow_types:
            metadata = getattr(workflow_type, "__workflows_decorator_metadata", None)
            if not isinstance(metadata, WorkflowDecoratorMetadata):
                continue

            workflow_definition = get_workflow_definition(workflow_type)
            identity = registered_identity(metadata, config.worker)
            actual_name = identity.name
            pending_mounts.enter_context(
                mount_workflow(
                    actual_name,
                    workflow_type,
                    replay_namespace=replay_namespace,
                    namespace=None if replay_namespace is not None else config.temporal.namespace,
                )
            )
            enforce_determinism = identity.enforce_determinism
            temporal_config = build_temporal_definition_config(
                actual_name, enforce_determinism, config.worker.versioning
            )
            needs_temporal_definition = _check_temporal_workflow_definition_locked(workflow_type, temporal_config)
            prepared.append(
                (
                    workflow_type,
                    temporal_config if needs_temporal_definition else None,
                    WorkflowSpec.model_validate(
                        {
                            **workflow_definition.model_dump(),
                            "name": actual_name,
                            "enforce_determinism": enforce_determinism,
                        }
                    ),
                )
            )

        for workflow_type, pending_temporal_config, definition in prepared:
            # A class listed twice is decorated on its first occurrence only.
            if pending_temporal_config is not None and _check_temporal_workflow_definition_locked(
                workflow_type, pending_temporal_config
            ):
                _apply_temporal_workflow_definition_locked(workflow_type, pending_temporal_config)
            set_workflow_definition(workflow_type, definition)
        mounts.enter_context(pending_mounts.pop_all())


@contextmanager
def _use_workflow_config_for_worker(
    workflow_type: ClassType,
    config: AppConfig,
    task_queue: str,
    *,
    replay_namespace: str | None = None,
    deployment_version_override: tuple[str, str] | None = None,
) -> Iterator[None]:
    with _use_workflow_config(
        get_workflow_definition(workflow_type).name,
        task_queue,
        config,
        replay_namespace=replay_namespace,
        deployment_version_override=deployment_version_override,
    ):
        yield


@contextmanager
def prepare_workflows(
    workflows: Sequence[ClassType],
    config: AppConfig | None = None,
    *,
    replay_only: bool = False,
    replay_namespace: str = "ReplayNamespace",
) -> Iterator[list[ClassType]]:
    """Prepare Mistral workflow classes for direct use with Temporal.

    Keep this context open while constructing and running a Temporal ``Worker`` or
    ``Replayer`` so Temporal sandbox imports use the same resolved configuration.
    Preparations with different configurations cannot be nested in the same execution
    context. Run concurrently configured workers in separate async tasks or processes.

    Args:
        workflows: Workflow classes decorated with :meth:`workflow.define`.
        config: Explicit SDK configuration. When omitted, environment configuration is
            resolved when this context is entered.
        replay_only: Skip worker startup validation when preparing workflows exclusively
            for a Temporal ``Replayer``. Do not enable this for a Temporal ``Worker``.
        replay_namespace: Namespace configured on the Temporal ``Replayer``. The default
            matches Temporal's default replay namespace. Ignored unless ``replay_only``
            is enabled.

    Yields:
        The prepared workflow classes, ready for Temporal's ``Worker`` or ``Replayer``.
    """
    resolved_config = resolve_worker_config(config)
    if not replay_only:
        resolved_config.validate_for_worker_startup()
    active_preparation_config = _active_preparation_config.get()
    if active_preparation_config is not None and active_preparation_config.model_dump(
        round_trip=True
    ) != resolved_config.model_dump(round_trip=True):
        raise WorkflowsException(
            code=ErrorCode.WORKFLOW_DEFINITION_ERROR,
            message=(
                "prepare_workflows() cannot be nested with a different configuration in the same execution "
                "context. Run each worker in its own async task or process and keep its preparation context "
                "open for the worker lifetime."
            ),
        )
    prepared_workflows = list(workflows)
    preparation_token = _active_preparation_config.set(resolved_config)
    try:
        with use_config(resolved_config), ExitStack() as registrations:
            configure_workflows_for_worker(
                prepared_workflows,
                resolved_config,
                registrations,
                replay_namespace=replay_namespace if replay_only else None,
            )
            for workflow_type in prepared_workflows:
                registrations.enter_context(
                    _use_workflow_config_for_worker(
                        workflow_type,
                        resolved_config,
                        resolved_config.get_effective_task_queue(),
                        replay_namespace=replay_namespace if replay_only else None,
                    )
                )
            yield prepared_workflows
    finally:
        _active_preparation_config.reset(preparation_token)
