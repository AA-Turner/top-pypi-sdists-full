import inspect
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from threading import Lock
from typing import Callable, Type, cast

import temporalio.exceptions
import temporalio.workflow
from pydantic import BaseModel

from mistralai.workflows.exceptions import ErrorCode, WorkflowsException
from mistralai.workflows.models import WorkflowSpec

_SEARCH_KEY_INFO_ATTR = "__workflows_search_key_info"


@dataclass(frozen=True)
class _SearchKeyInfo:
    search_keys: tuple[str, ...]
    entrypoint_param_names: tuple[str, ...]
    input_model: type[BaseModel]


@dataclass
class _MountedWorkflow:
    workflow_type: type
    reference_count: int = 0
    # Temporal namespaces of the workers holding this mount, with their reference counts.
    namespaces: dict[str, int] = field(default_factory=dict)


# Runtime code only knows a workflow by the name Temporal reports. This index maps that name to
# the class a worker or `prepare_workflows()` is serving, so per-workflow metadata is read from
# the class itself and two classes never share it. Names are mounted for the lifetime of their
# scope only, so another class can reuse a name once every scope using it has closed.
_mounted_workflows: dict[str, _MountedWorkflow] = {}
# A Replayer runs under its own namespace, so replay preparations are indexed by that namespace.
# A replay of one class then never reads the metadata of a live worker serving the same name.
_replay_mounted_workflows: dict[tuple[str, str], _MountedWorkflow] = {}
_mounted_workflows_lock = Lock()


def _get_workflow_entrypoint_method(cls_type: Type) -> Callable | None:
    for _, method in inspect.getmembers(cls_type, predicate=inspect.isfunction):
        if hasattr(method, "__workflows_workflow_entrypoint"):
            return method
    return None


def get_workflow_definition(workflow: Type | Callable) -> WorkflowSpec:
    definition = getattr(workflow, "__workflows_workflow_def", None)
    if definition is None:
        raise ValueError(f"Cannot get definition from {workflow}. Make sure it was decorated with @define")
    return cast(WorkflowSpec, definition)


def set_workflow_definition(workflow: Type | Callable, definition: WorkflowSpec) -> None:
    setattr(workflow, "__workflows_workflow_def", definition)


def replace_workflow_definition(workflow: Type | Callable, definition: WorkflowSpec) -> None:
    set_workflow_definition(workflow, definition)


def set_workflow_search_key_info(
    workflow: Type,
    search_keys: tuple[str, ...],
    entrypoint_param_names: tuple[str, ...],
    input_model: type[BaseModel],
) -> None:
    setattr(workflow, _SEARCH_KEY_INFO_ATTR, _SearchKeyInfo(search_keys, entrypoint_param_names, input_model))


def get_class_search_key_info(workflow: Type) -> _SearchKeyInfo:
    info = getattr(workflow, _SEARCH_KEY_INFO_ATTR, None)
    if info is None:
        raise KeyError(getattr(workflow, "__name__", repr(workflow)))
    return cast(_SearchKeyInfo, info)


def _reserved_error(name: str, owner: type, workflow_type: type, scope: str) -> WorkflowsException:
    return WorkflowsException(
        code=ErrorCode.WORKFLOW_DEFINITION_ERROR,
        message=(
            f"Workflow type {name!r} is already reserved by workflow class {owner.__name__!r}{scope}. "
            f"It cannot be used by workflow class {workflow_type.__name__!r} while that workflow is "
            "prepared in the same process. Stop the other worker first, replay under another namespace, "
            "or use a unique workflow name."
        ),
    )


@contextmanager
def mount_workflow(
    name: str,
    workflow_type: Type,
    *,
    replay_namespace: str | None = None,
    namespace: str | None = None,
) -> Iterator[None]:
    """Serve ``workflow_type`` under ``name`` until the context exits.

    While mounted, a different class cannot use the same name. With ``replay_namespace``, the
    mount only applies to workflows replayed under that namespace, so a replay never blocks a
    worker, nor reads the metadata of the class a worker serves. ``namespace`` is the Temporal
    namespace a worker polls: a replay of another class under that same namespace is rejected,
    because the two could not be told apart at runtime.
    """
    replaying = replay_namespace is not None
    index: dict = _replay_mounted_workflows if replaying else _mounted_workflows
    key: str | tuple[str, str] = name if replay_namespace is None else (name, replay_namespace)
    with _mounted_workflows_lock:
        if replay_namespace is not None:
            worker = _mounted_workflows.get(name)
            if (
                worker is not None
                and worker.workflow_type is not workflow_type
                and worker.namespaces.get(replay_namespace)
            ):
                raise _reserved_error(name, worker.workflow_type, workflow_type, f" in namespace {replay_namespace!r}")
        elif namespace is not None:
            replay = _replay_mounted_workflows.get((name, namespace))
            if replay is not None and replay.workflow_type is not workflow_type:
                raise _reserved_error(name, replay.workflow_type, workflow_type, f" in replay namespace {namespace!r}")
        mounted = index.get(key)
        if mounted is None:
            mounted = _MountedWorkflow(workflow_type)
            index[key] = mounted
        elif mounted.workflow_type is not workflow_type:
            scope = f" in replay namespace {replay_namespace!r}" if replaying else ""
            raise _reserved_error(name, mounted.workflow_type, workflow_type, scope)
        mounted.reference_count += 1
        if namespace is not None and not replaying:
            mounted.namespaces[namespace] = mounted.namespaces.get(namespace, 0) + 1
    try:
        yield
    finally:
        with _mounted_workflows_lock:
            mounted.reference_count -= 1
            if namespace is not None and not replaying:
                remaining = mounted.namespaces[namespace] - 1
                if remaining:
                    mounted.namespaces[namespace] = remaining
                else:
                    del mounted.namespaces[namespace]
            if not mounted.reference_count and index.get(key) is mounted:
                del index[key]


def _current_workflow_namespace() -> str | None:
    if not temporalio.workflow.in_workflow():
        return None
    try:
        return temporalio.workflow.info().namespace
    except (RuntimeError, temporalio.exceptions.TemporalError):
        return None


def get_mounted_workflow(name: str) -> Type | None:
    namespace = _current_workflow_namespace()
    if namespace is not None:
        replay_mount = _replay_mounted_workflows.get((name, namespace))
        if replay_mount is not None:
            return replay_mount.workflow_type
    mounted = _mounted_workflows.get(name)
    return mounted.workflow_type if mounted is not None else None


def is_workflow_on_behalf_of(workflow_name: str) -> bool:
    workflow_type = get_mounted_workflow(workflow_name)
    if workflow_type is None:
        return False
    return get_workflow_definition(workflow_type).on_behalf_of


def get_workflow_search_key_info(workflow_name: str) -> _SearchKeyInfo:
    workflow_type = get_mounted_workflow(workflow_name)
    if workflow_type is None:
        raise KeyError(workflow_name)
    return get_class_search_key_info(workflow_type)


def set_workflow_entrypoint(method: Callable) -> None:
    setattr(method, "__workflows_workflow_entrypoint", True)
