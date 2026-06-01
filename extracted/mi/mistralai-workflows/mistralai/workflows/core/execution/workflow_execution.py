import inspect
from datetime import timedelta
from types import NoneType
from typing import TYPE_CHECKING, Any, Literal, Type, overload

import structlog
import temporalio.workflow
from pydantic import BaseModel
from temporalio.workflow import ChildWorkflowHandle as TemporalChildWorkflowHandle
from temporalio.workflow import ParentClosePolicy

from mistralai.workflows.core.definition.validation._validator import get_function_signature_type_hints
from mistralai.workflows.core.definition.workflow_definition import (
    _get_workflow_entrypoint_method,
    get_workflow_definition,
)
from mistralai.workflows.core.utils.contextvars import unwrap_contextual_result
from mistralai.workflows.exceptions import ErrorCode, WorkflowsException

if TYPE_CHECKING:
    from typing import NoReturn

    from typing_extensions import deprecated

    class ChildWorkflowHandle(TemporalChildWorkflowHandle):
        """Typing-only subclass that hides Temporal-internal attributes."""

        @property
        @deprecated("temporal internal")
        def first_execution_run_id(self) -> NoReturn: ...


logger = structlog.get_logger(__name__)


def _coerce_workflow_result(return_value: Any, entrypoint_method: Any) -> Any:
    """Coerce a raw workflow result based on the entrypoint's return-type annotation.

    Handles two cases:
    - BaseModel return types are validated via model_validate
    - Primitive return types are extracted from the {"result": ...} Temporal wrapper
    """
    original_func = getattr(entrypoint_method, "__wrapped__", None)
    if original_func:
        _, return_type, _ = get_function_signature_type_hints(original_func, is_method=True)
    else:
        return_type = None

    if return_type and return_type != NoneType:
        try:
            is_base_model = inspect.isclass(return_type) and issubclass(return_type, BaseModel)
        except TypeError:
            is_base_model = False

        if is_base_model:
            return return_type.model_validate(return_value)
        elif isinstance(return_value, dict) and "result" in return_value:
            return return_value["result"]

    return return_value


_HIDDEN_ATTRS = frozenset({"first_execution_run_id"})


def _patch_child_workflow_handle(
    handle: TemporalChildWorkflowHandle,
    entrypoint_method: Any,
) -> None:
    """Patch a Temporal ChildWorkflowHandle in-place:

    1. Monkey-patch ``_resolve_success`` so that ``await handle`` returns the
       same unwrapped + coerced value as the ``wait=True`` path.
    2. Monkey-patch ``__getattribute__`` to hide Temporal-internal attributes
       (e.g. ``first_execution_run_id``) from consumers.

    NOTE: Relies on Temporal's private ``_resolve_success`` method.
    """
    original_resolve = handle._resolve_success  # type: ignore[attr-defined]

    def _coercing_resolve(result: Any) -> None:
        _, unwrapped = unwrap_contextual_result(result)
        original_resolve(_coerce_workflow_result(unwrapped, entrypoint_method))

    handle._resolve_success = _coercing_resolve  # type: ignore[attr-defined]

    original_getattribute = type(handle).__getattribute__

    def _guarded_getattribute(self: Any, name: str) -> Any:
        if name in _HIDDEN_ATTRS:
            raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")
        return original_getattribute(self, name)

    handle.__class__ = type(
        handle.__class__.__name__,
        (handle.__class__,),
        {"__getattribute__": _guarded_getattribute},
    )


def get_execution_id() -> str | None:
    if temporalio.workflow.in_workflow():
        return temporalio.workflow.info().workflow_id
    else:
        return None


@overload
async def execute_workflow(
    workflow: Type,
    params: BaseModel,
    execution_timeout: timedelta = ...,
    execution_id: str | None = ...,
    wait: Literal[True] = ...,
    parent_close_policy: ParentClosePolicy | None = ...,
) -> Any: ...


@overload
async def execute_workflow(
    workflow: Type,
    params: BaseModel,
    execution_timeout: timedelta = ...,
    execution_id: str | None = ...,
    wait: Literal[False] = ...,
    parent_close_policy: ParentClosePolicy | None = ...,
) -> "ChildWorkflowHandle": ...


@overload
async def execute_workflow(
    workflow: Type,
    params: BaseModel,
    execution_timeout: timedelta = ...,
    execution_id: str | None = ...,
    wait: bool = ...,
    parent_close_policy: ParentClosePolicy | None = ...,
) -> Any: ...


async def execute_workflow(
    workflow: Type,
    params: BaseModel,
    execution_timeout: timedelta = timedelta(hours=1),
    execution_id: str | None = None,
    wait: bool = True,
    parent_close_policy: ParentClosePolicy | None = None,
) -> Any:
    """Execute a workflow. If called from within a workflow, it will execute the workflow as a child workflow.

    Args:
        workflow (Type): The workflow class to execute. (must be decorated with @define)
        params (BaseModel): The parameters to pass to the workflow. (must be a BaseModel)
        execution_timeout (timedelta, optional): The maximum time the workflow can run.
                                                 Defaults to timedelta(hours=1).
        execution_id (str | None, optional): The workflow id to use. If None, a random id will be generated.
        wait (bool, optional): If True (default), wait for the child workflow to complete and return the result.
                               If False, return a ChildWorkflowHandle immediately (only inside a workflow).
        parent_close_policy (ParentClosePolicy | None, optional): Policy for the child when the parent closes.
                             Defaults to TERMINATE when wait=True, ABANDON when wait=False.

    Returns:
        Any: The return value of the workflow (wait=True), or a ChildWorkflowHandle (wait=False).
    """
    if not wait and not temporalio.workflow.in_workflow():
        raise WorkflowsException(
            code=ErrorCode.WORKFLOW_DEFINITION_ERROR,
            message="execute_workflow with wait=False can only be called from within a workflow",
        )

    workflow_definition = get_workflow_definition(workflow)
    if not workflow_definition:
        raise WorkflowsException(
            code=ErrorCode.WORKFLOW_DEFINITION_ERROR,
            message=f"{workflow} class must be decorated with @workflow.define",
        )

    entrypoint_method = _get_workflow_entrypoint_method(workflow)
    if not entrypoint_method:
        raise WorkflowsException(
            code=ErrorCode.WORKFLOW_DEFINITION_ERROR,
            message=f"{workflow} class must have an entrypoint method decorated with @workflow.entrypoint",
        )

    if parent_close_policy is None:
        parent_close_policy = ParentClosePolicy.TERMINATE if wait else ParentClosePolicy.ABANDON

    if temporalio.workflow.in_workflow():
        if not wait:
            handle = await temporalio.workflow.start_child_workflow(
                workflow_definition.name,
                params.model_dump(),
                execution_timeout=execution_timeout,
                result_type=dict,
                id=execution_id,
                parent_close_policy=parent_close_policy,
            )
            _patch_child_workflow_handle(handle, entrypoint_method)
            return handle

        return_value = await temporalio.workflow.execute_child_workflow(
            workflow_definition.name,
            params.model_dump(),
            execution_timeout=execution_timeout,
            result_type=dict,
            id=execution_id,
            parent_close_policy=parent_close_policy,
        )

        _, return_value = unwrap_contextual_result(return_value)
    else:
        workflow_instance = workflow()
        params_dict = params.model_dump()
        return_value = await entrypoint_method(workflow_instance, params_dict)

    return _coerce_workflow_result(return_value, entrypoint_method)
