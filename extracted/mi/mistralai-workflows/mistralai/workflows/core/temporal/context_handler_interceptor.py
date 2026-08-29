import inspect
import typing
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Callable, NoReturn, Sequence, Tuple, Type

import structlog
import temporalio.client
import temporalio.worker
import temporalio.workflow
from pydantic import TypeAdapter
from pydantic_core import to_json
from temporalio import workflow

from mistralai.workflows.core.execution.child_start_budget import ChildStartBudget, child_start_budget_var
from mistralai.workflows.core.temporal.utils import TEMPORAL_SCHEDULE_ID_SEARCH_KEY
from mistralai.workflows.core.utils.contextvars import reset_contextvar
from mistralai.workflows.core.utils.type_hints import get_type_hints
from mistralai.workflows.models import PayloadWithContext, WorkflowContext

logger = structlog.get_logger(__name__)

workflow_context_var: ContextVar[str | None] = ContextVar("workflow_context", default=None)


def unwrap_contextual_args(args: Sequence[Any]) -> Tuple[WorkflowContext | None, Sequence[Any]]:
    """Unwrap contextual args (PayloadWithContext), return the workflow context and the unwrapped args"""
    workflow_context: WorkflowContext | None = None
    new_args_list = []

    for arg in args:
        if isinstance(arg, PayloadWithContext):
            workflow_context = arg.context
            if not arg.empty:
                new_args_list.append(arg.payload)
        else:
            new_args_list.append(arg)

    return workflow_context, new_args_list


def _validate_activity_args(fn: Callable[..., Any], args: Sequence[Any]) -> Sequence[Any]:
    """Validate activity args against the function's type hints.

    When an activity has optional parameters (defaults), Temporal may receive fewer
    payloads than the function has parameters. In that case, Temporal drops all type
    hints during deserialization, so Pydantic models arrive as plain dicts. This
    function re-validates args using the actual function signature to restore proper types.
    """
    try:
        hints = get_type_hints(fn)
        params = list(inspect.signature(fn).parameters.keys())
    except Exception:
        return args

    if len(args) > len(params):
        logger.warning(
            "Activity args exceed function params, skipping validation for extra args",
            fn=fn,
            num_args=len(args),
            num_params=len(params),
        )

    validated = []
    for i, arg in enumerate(args):
        param_name = params[i] if i < len(params) else None
        type_hint = hints.get(param_name) if param_name else None
        if type_hint is not None and type_hint is not typing.Any:
            try:
                validated.append(TypeAdapter(type_hint).validate_python(arg))
            except Exception:
                validated.append(arg)
        else:
            validated.append(arg)
    return validated


def wrap_result_with_context(result: Any, workflow_context: WorkflowContext | None) -> Any:
    """Wrap result with workflow context if it exists"""
    if workflow_context is None or isinstance(result, PayloadWithContext):
        return result
    return PayloadWithContext(payload=to_json(result), context=workflow_context)


@contextmanager
def define_context(workflow_context: WorkflowContext | None) -> Any:
    """Set workflow context in contextvar for later use"""
    token = workflow_context_var.set(workflow_context.model_dump_json()) if workflow_context else None
    try:
        yield
    finally:
        if token:
            reset_contextvar(workflow_context_var, token)


def retrieve_context() -> WorkflowContext | None:
    """Extract workflow context from contextvar"""
    context_json = workflow_context_var.get()
    if context_json is not None:
        return WorkflowContext.model_validate_json(context_json)
    return None


def create_workflow_context() -> WorkflowContext:
    """Create WorkflowContext from workflow.info() - single source of truth for identity."""
    workflow_info = workflow.info()
    logger.debug(
        "create_workflow_context called",
        workflow_id=workflow_info.workflow_id,
        workflow_type=workflow_info.workflow_type,
        parent_workflow_id=workflow_info.parent.workflow_id if workflow_info.parent else None,
        root_workflow_id=workflow_info.root.workflow_id if workflow_info.root else None,
    )
    on_behalf_of = False
    try:
        with workflow.unsafe.imports_passed_through():
            from mistralai.workflows.core.definition.workflow_definition import is_workflow_on_behalf_of

            on_behalf_of = is_workflow_on_behalf_of(workflow_info.workflow_type)
    except Exception:
        logger.warning(
            "Failed to resolve on_behalf_of flag, defaulting to False", workflow_type=workflow_info.workflow_type
        )

    return WorkflowContext(
        namespace=workflow_info.namespace,
        execution_id=workflow_info.workflow_id,
        root_workflow_exec_id=workflow_info.root.workflow_id if workflow_info.root else None,
        parent_workflow_exec_id=workflow_info.parent.workflow_id if workflow_info.parent else None,
        on_behalf_of=on_behalf_of,
        continued_run_id=workflow_info.continued_run_id,
        first_execution_run_id=workflow_info.first_execution_run_id,
        schedule_id=workflow_info.typed_search_attributes.get(TEMPORAL_SCHEDULE_ID_SEARCH_KEY),
    )


def _create_workflow_context_with_token() -> WorkflowContext:
    ctx = create_workflow_context()
    existing = retrieve_context()
    if existing:
        updates: dict[str, Any] = {}
        if existing.execution_token is not None:
            updates["execution_token"] = existing.execution_token
        if existing.extensions is not None:
            updates["extensions"] = existing.extensions
        if existing.trusted_extensions is not None:
            updates["trusted_extensions"] = existing.trusted_extensions
        if existing.on_behalf_of is not None:
            updates["on_behalf_of"] = existing.on_behalf_of
        if updates:
            ctx = ctx.model_copy(update=updates)
    return ctx


class WorkflowContextWorkflowOutboundInterceptor(temporalio.worker.WorkflowOutboundInterceptor):
    def _contextualize_args(self, args: Sequence[Any], *, include_token: bool = False) -> Sequence[Any]:
        workflow_context = retrieve_context()
        if workflow_context:
            if not include_token:
                workflow_context = workflow_context.model_copy(update={"execution_token": None})
            contextualized_args = []
            for arg in args:
                if isinstance(arg, PayloadWithContext):
                    contextualized_args.append(arg)
                else:
                    contextualized_args.append(PayloadWithContext(payload=to_json(arg), context=workflow_context))
            if len(contextualized_args) == 0:
                contextualized_args.append(PayloadWithContext(payload=b"null", empty=True, context=workflow_context))
            return contextualized_args
        return args

    async def signal_child_workflow(self, input: temporalio.worker.SignalChildWorkflowInput) -> None:
        input.args = self._contextualize_args(input.args)
        await self.next.signal_child_workflow(input)

    async def signal_external_workflow(self, input: temporalio.worker.SignalExternalWorkflowInput) -> None:
        input.args = self._contextualize_args(input.args)
        await self.next.signal_external_workflow(input)

    def start_activity(self, input: temporalio.worker.StartActivityInput) -> temporalio.workflow.ActivityHandle:
        input.args = self._contextualize_args(input.args, include_token=True)
        return self.next.start_activity(input)

    async def start_child_workflow(
        self, input: temporalio.worker.StartChildWorkflowInput
    ) -> temporalio.workflow.ChildWorkflowHandle:
        input.args = self._contextualize_args(input.args)
        return await self.next.start_child_workflow(input)

    def start_local_activity(
        self, input: temporalio.worker.StartLocalActivityInput
    ) -> temporalio.workflow.ActivityHandle:
        input.args = self._contextualize_args(input.args, include_token=True)
        return self.next.start_local_activity(input)

    def continue_as_new(self, input: temporalio.worker.ContinueAsNewInput) -> NoReturn:
        input.args = self._contextualize_args(input.args)
        self.next.continue_as_new(input)


class WorkflowContextWorkflowInboundInterceptor(temporalio.worker.WorkflowInboundInterceptor):
    """Handles context creation and PayloadWithContext wrapping/unwrapping.

    This interceptor:
    1. Creates fresh WorkflowContext for every workflow from workflow.info()
    2. Sets context in contextvar for activities and streaming to access
    3. Wraps/unwraps PayloadWithContext for cross-worker context propagation
    """

    def init(self, outbound: temporalio.worker.WorkflowOutboundInterceptor) -> None:
        self.next.init(WorkflowContextWorkflowOutboundInterceptor(outbound))

    def _get_child_start_budget(self) -> ChildStartBudget:
        # One budget per workflow run, shared across the entrypoint and signal/update
        # handlers. Each handler runs in its own asyncio task with a copied context, so a
        # ContextVar set in execute_workflow would not propagate to handle_signal — store
        # the instance on the interceptor (one per run) and set it into the ContextVar in
        # each handler so execute_workflow's fan-out gate also covers signal/update fan-outs.
        budget = getattr(self, "_child_start_budget", None)
        if budget is None:
            budget = ChildStartBudget()
            self._child_start_budget = budget
        return budget

    async def execute_workflow(self, input: temporalio.worker.ExecuteWorkflowInput) -> Any:
        # Create fresh context from workflow.info() - single source of truth for identity
        workflow_context = create_workflow_context()

        # Unwrap args — preserve execution_token and extensions from incoming context (set by server)
        incoming_context, input.args = unwrap_contextual_args(input.args)
        if incoming_context:
            updates: dict[str, Any] = {}
            if incoming_context.execution_token is not None:
                updates["execution_token"] = incoming_context.execution_token
            if incoming_context.extensions is not None:
                updates["extensions"] = incoming_context.extensions
            if incoming_context.on_behalf_of is not None:
                updates["on_behalf_of"] = incoming_context.on_behalf_of
            if updates:
                workflow_context = workflow_context.model_copy(update=updates)

        logger.debug(
            "Created workflow context",
            workflow_id=workflow_context.execution_id,
            parent_workflow_id=workflow_context.parent_workflow_exec_id,
            root_workflow_id=workflow_context.root_workflow_exec_id,
            is_child_workflow=workflow_context.parent_workflow_exec_id is not None,
            has_execution_token=workflow_context.execution_token is not None,
        )

        # Execute with context set for activities and streaming
        with define_context(workflow_context):
            budget_token = child_start_budget_var.set(self._get_child_start_budget())
            try:
                result = await super().execute_workflow(input)
            finally:
                reset_contextvar(child_start_budget_var, budget_token)
        # Strip token from result context — token should not leak in workflow results
        result_context = workflow_context.model_copy(update={"execution_token": None})
        return wrap_result_with_context(result, result_context)

    async def handle_signal(self, input: temporalio.worker.HandleSignalInput) -> None:
        _, input.args = unwrap_contextual_args(input.args)
        workflow_context = _create_workflow_context_with_token()
        with define_context(workflow_context):
            budget_token = child_start_budget_var.set(self._get_child_start_budget())
            try:
                await self.next.handle_signal(input)
            finally:
                reset_contextvar(child_start_budget_var, budget_token)

    async def handle_query(self, input: temporalio.worker.HandleQueryInput) -> Any:
        _, input.args = unwrap_contextual_args(input.args)
        workflow_context = _create_workflow_context_with_token()
        with define_context(workflow_context):
            result = await self.next.handle_query(input)
        result_context = workflow_context.model_copy(update={"execution_token": None})
        return wrap_result_with_context(result, result_context)

    def handle_update_validator(self, input: temporalio.worker.HandleUpdateInput) -> None:
        _, input.args = unwrap_contextual_args(input.args)
        workflow_context = _create_workflow_context_with_token()
        with define_context(workflow_context):
            self.next.handle_update_validator(input)

    async def handle_update_handler(self, input: temporalio.worker.HandleUpdateInput) -> Any:
        _, input.args = unwrap_contextual_args(input.args)
        workflow_context = _create_workflow_context_with_token()
        with define_context(workflow_context):
            budget_token = child_start_budget_var.set(self._get_child_start_budget())
            try:
                result = await self.next.handle_update_handler(input)
            finally:
                reset_contextvar(child_start_budget_var, budget_token)
        result_context = workflow_context.model_copy(update={"execution_token": None})
        return wrap_result_with_context(result, result_context)


class WorkflowContextActivityInboundInterceptor(temporalio.worker.ActivityInboundInterceptor):
    """Inbound interceptors runs in the workflow context"""

    async def execute_activity(self, input: temporalio.worker.ExecuteActivityInput) -> Any:
        workflow_context, input.args = unwrap_contextual_args(input.args)
        input.args = _validate_activity_args(input.fn, input.args)
        with define_context(workflow_context):
            result = await self.next.execute_activity(input)
        return wrap_result_with_context(result, workflow_context)


class ContextHandlerInterceptor(temporalio.client.Interceptor, temporalio.worker.Interceptor):
    def intercept_client(self, next: temporalio.client.OutboundInterceptor) -> temporalio.client.OutboundInterceptor:
        return next

    def intercept_activity(
        self, next: temporalio.worker.ActivityInboundInterceptor
    ) -> temporalio.worker.ActivityInboundInterceptor:
        return WorkflowContextActivityInboundInterceptor(next)

    def workflow_interceptor_class(
        self, input: temporalio.worker.WorkflowInterceptorClassInput
    ) -> Type[temporalio.worker.WorkflowInboundInterceptor] | None:
        return WorkflowContextWorkflowInboundInterceptor
