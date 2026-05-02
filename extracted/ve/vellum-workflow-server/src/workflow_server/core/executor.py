from datetime import datetime, timezone
from io import StringIO
import logging
from multiprocessing import Process, Queue
import os
import random
import string
import sys
from threading import Event as ThreadingEvent
import time
from traceback import format_exc
from uuid import UUID, uuid4
from typing import Any, Callable, Generator, Iterator, Optional, Tuple

import orjson
from pydantic_core import PydanticSerializationError
from vellum_ee.workflows.display.utils.events import event_enricher
from vellum_ee.workflows.display.utils.expressions import base_descriptor_validator
from vellum_ee.workflows.server.virtual_file_loader import VirtualFileFinder

from vellum.workflows import BaseWorkflow
from vellum.workflows.context import execution_context
from vellum.workflows.emitters.base import BaseWorkflowEmitter
from vellum.workflows.emitters.vellum_emitter import VellumEmitter
from vellum.workflows.errors import WorkflowError, WorkflowErrorCode
from vellum.workflows.events.exception_handling import stream_initialization_exception
from vellum.workflows.events.node import NodeExecutionRejectedBody, NodeExecutionRejectedEvent
from vellum.workflows.events.types import BaseEvent
from vellum.workflows.events.workflow import (
    WorkflowEvent,
    WorkflowExecutionInitiatedBody,
    WorkflowExecutionInitiatedEvent,
    WorkflowExecutionRejectedBody,
    WorkflowExecutionRejectedEvent,
)
from vellum.workflows.exceptions import WorkflowInitializationException
from vellum.workflows.inputs import BaseInputs
from vellum.workflows.nodes import BaseNode
from vellum.workflows.nodes.mocks import MockNodeExecution
from vellum.workflows.resolvers.base import BaseWorkflowResolver
from vellum.workflows.resolvers.resolver import VellumResolver
from vellum.workflows.state.context import WorkflowContext
from vellum.workflows.state.store import EmptyStore
from vellum.workflows.triggers import BaseTrigger
from vellum.workflows.types import CancelSignal
from vellum.workflows.workflows.event_filters import (
    all_workflow_event_filter,
    root_workflow_event_filter,
    workflow_event_filter,
    workflow_sandbox_event_filter,
)
from workflow_server.config import LOCAL_DEPLOYMENT, LOCAL_WORKFLOW_MODULE
from workflow_server.core.cancel_workflow import CancelWorkflowWatcherThread
from workflow_server.core.events import (
    SPAN_ID_EVENT,
    STREAM_FINISHED_EVENT,
    VembdaExecutionFulfilledBody,
    VembdaExecutionFulfilledEvent,
)
from workflow_server.core.utils import (
    create_vembda_rejected_event,
    is_events_emitting_enabled,
    serialize_vembda_rejected_event,
)
from workflow_server.core.workflow_executor_context import (
    BaseExecutorContext,
    EventFilterType,
    NodeExecutorContext,
    WorkflowExecutorContext,
)
from workflow_server.utils.log_proxy import redirect_log
from workflow_server.utils.system_utils import get_memory_in_use_mb
from workflow_server.utils.utils import get_version

logger = logging.getLogger(__name__)

EVENT_FILTER_MAP: dict[EventFilterType, Callable[[type["BaseWorkflow"], "WorkflowEvent"], bool]] = {
    "ROOT_WORKFLOW_ONLY": workflow_event_filter,
    "ROOT_WORKFLOW_AND_ROOT_NODE": root_workflow_event_filter,
    "EXCLUDE_NESTED_SNAPSHOTTED": workflow_sandbox_event_filter,
    "ALL": all_workflow_event_filter,
}


def _get_event_filter(
    filter_type: Optional[EventFilterType],
) -> Callable[[type["BaseWorkflow"], "WorkflowEvent"], bool]:
    """
    Get the event filter function based on the filter type.
    Defaults to workflow_sandbox_event_filter if no filter type is specified.
    """
    if filter_type is None:
        return workflow_sandbox_event_filter
    return EVENT_FILTER_MAP.get(filter_type, workflow_sandbox_event_filter)


def stream_node_process_timeout(
    executor_context: NodeExecutorContext,
    queue: Queue,
) -> Process:
    node_process = Process(
        target=_stream_node_wrapper,
        args=(executor_context, queue),
    )
    node_process.start()

    if node_process.exitcode is not None:
        queue.put(create_vembda_rejected_event(executor_context, "Internal Server Error", timed_out=True))

    return node_process


def _stream_node_wrapper(executor_context: NodeExecutorContext, queue: Queue) -> None:
    try:
        for event in stream_node(executor_context=executor_context):
            queue.put(event)
    except WorkflowInitializationException as e:
        queue.put(create_vembda_rejected_event(executor_context, e.message))
    except Exception as e:
        logger.exception(e)
        queue.put(create_vembda_rejected_event(executor_context, "Internal Server Error"))


def _stream_workflow_wrapper(
    executor_context: WorkflowExecutorContext,
    queue: Queue,
    cancel_signal: CancelSignal,
    timeout_signal: CancelSignal,
) -> None:
    span_id_emitted = False
    try:
        stream_iterator, span_id = stream_workflow(
            executor_context=executor_context,
            cancel_signal=cancel_signal,
            timeout_signal=timeout_signal,
        )

        queue.put(f"{SPAN_ID_EVENT}:{span_id}")
        span_id_emitted = True

        for event in stream_iterator:
            queue.put(orjson.dumps(event).decode("utf-8"))

    except Exception as e:
        if not span_id_emitted:
            queue.put(f"{SPAN_ID_EVENT}:{uuid4()}")

        logger.exception(e)
        queue.put(serialize_vembda_rejected_event(executor_context, "Internal Server Error"))

    queue.put(STREAM_FINISHED_EVENT)

    exit(0)


def stream_workflow_process_timeout(
    executor_context: WorkflowExecutorContext,
    queue: Queue,
    cancel_signal: CancelSignal,
    timeout_signal: CancelSignal,
) -> Process:
    workflow_process = Process(
        target=_stream_workflow_wrapper,
        args=(
            executor_context,
            queue,
            cancel_signal,
            timeout_signal,
        ),
    )
    workflow_process.start()

    if workflow_process.exitcode is not None:
        queue.put(create_vembda_rejected_event(executor_context, "Internal Server Error", timed_out=True))

    return workflow_process


def stream_workflow(
    executor_context: WorkflowExecutorContext,
    timeout_signal: CancelSignal,
    cancel_signal: CancelSignal,
    disable_redirect: bool = True,
) -> tuple[Iterator[dict], UUID]:
    cancel_watcher_kill_switch = ThreadingEvent()
    workflow: Optional[BaseWorkflow] = None
    try:
        workflow, namespace = _create_workflow(executor_context)

        trigger_id = executor_context.trigger_id

        inputs_or_trigger = workflow.deserialize_trigger(
            trigger_id=trigger_id,
            inputs=executor_context.inputs,
            dataset_row=executor_context.dataset_row,
        )

        # Determine whether we have inputs or a trigger
        if isinstance(inputs_or_trigger, BaseInputs):
            workflow_inputs = inputs_or_trigger
            trigger = None
        elif isinstance(inputs_or_trigger, BaseTrigger):
            workflow_inputs = None
            trigger = inputs_or_trigger
        else:
            workflow_inputs = None
            trigger = None

        workflow_state = (
            workflow.deserialize_state(
                executor_context.state,
                workflow_inputs=workflow_inputs or BaseInputs(),
            )
            if executor_context.state
            else None
        )
        node_output_mocks = MockNodeExecution.validate_all(
            executor_context.node_output_mocks,
            workflow.__class__,
            descriptor_validator=base_descriptor_validator,
        )

        cancel_signal = cancel_signal or ThreadingEvent()

        stream = workflow.stream(
            inputs=workflow_inputs,
            state=workflow_state,
            node_output_mocks=node_output_mocks,
            event_filter=_get_event_filter(executor_context.event_filter),
            cancel_signal=cancel_signal,
            entrypoint_nodes=[executor_context.node_id] if executor_context.node_id else None,
            previous_execution_id=executor_context.previous_execution_id,
            timeout=executor_context.timeout,
            trigger=trigger,
            execution_id=executor_context.workflow_span_id,
            event_max_size=executor_context.event_max_size,
        )
    except WorkflowInitializationException as e:
        cancel_watcher_kill_switch.set()

        with execution_context(
            parent_context=executor_context.execution_context.parent_context,
            trace_id=executor_context.execution_context.trace_id,
        ):
            initialization_exception_stream = stream_initialization_exception(e)

        def _stream_generator() -> Generator[dict[str, Any], Any, None]:
            for event in initialization_exception_stream:
                if workflow:
                    for emitter in workflow.emitters:
                        emitter.emit_event(event)

                yield _dump_event(
                    event=event,
                    executor_context=executor_context,
                )

            if workflow:
                workflow.join()

        return (
            _call_stream(
                executor_context=executor_context,
                stream_generator=_stream_generator,
                disable_redirect=disable_redirect,
                timeout_signal=timeout_signal,
            ),
            initialization_exception_stream.span_id,
        )
    except Exception:
        cancel_watcher_kill_switch.set()
        logger.exception("Failed to generate Workflow Stream")

        parent = executor_context.execution_context.parent_context
        trace_id = executor_context.execution_context.trace_id
        span_id = uuid4()
        workflow_definition = workflow.__class__ if workflow is not None else BaseWorkflow

        def _stream_generator() -> Generator[dict[str, Any], Any, None]:
            initiated_event: WorkflowEvent = WorkflowExecutionInitiatedEvent(
                trace_id=trace_id,
                span_id=span_id,
                body=WorkflowExecutionInitiatedBody(
                    workflow_definition=workflow_definition,
                    inputs=BaseInputs(),
                    initial_state=None,
                ),
                parent=parent,
            )
            yield _dump_event(
                event=initiated_event,
                executor_context=executor_context,
            )

            rejected_event = WorkflowExecutionRejectedEvent(
                trace_id=trace_id,
                span_id=span_id,
                body=WorkflowExecutionRejectedBody(
                    workflow_definition=workflow_definition,
                    error=WorkflowError(
                        code=WorkflowErrorCode.INTERNAL_ERROR,
                        message="Failed to generate Workflow Stream",
                    ),
                    stacktrace=format_exc(),
                ),
                parent=parent,
            )
            yield _dump_event(
                event=rejected_event,
                executor_context=executor_context,
            )

        return (
            _call_stream(
                executor_context=executor_context,
                stream_generator=_stream_generator,
                disable_redirect=disable_redirect,
                timeout_signal=timeout_signal,
            ),
            span_id,
        )

    cancel_watcher = CancelWorkflowWatcherThread(
        kill_switch=cancel_watcher_kill_switch,
        execution_id=stream.span_id,
        timeout_seconds=executor_context.timeout,
        vembda_public_url=executor_context.vembda_public_url,
        cancel_signal=cancel_signal,
    )

    try:
        if executor_context.vembda_public_url:
            cancel_watcher.start()
    except Exception:
        logger.exception("Failed to start cancel watcher")

    def call_workflow() -> Generator[dict[str, Any], Any, None]:
        try:
            first = True
            for event in stream:
                if first:
                    executor_context.stream_start_time = time.time_ns()
                    first = False

                try:
                    yield _dump_event(
                        event=event,
                        executor_context=executor_context,
                    )
                except PydanticSerializationError:
                    logger.exception(
                        "Failed to serialize event from Workflow Stream",
                        extra={"event_name": event.name, "event_span_id": str(event.span_id)},
                    )
                    # Skip this event and continue processing the rest of the stream
        except Exception as e:
            logger.exception("Failed to generate event from Workflow Stream")
            raise e
        finally:
            cancel_watcher_kill_switch.set()

        if workflow is not None:
            workflow.join()

    return (
        _call_stream(
            executor_context=executor_context,
            stream_generator=call_workflow,
            disable_redirect=disable_redirect,
            timeout_signal=timeout_signal,
        ),
        stream.span_id,
    )


def stream_node(
    executor_context: NodeExecutorContext,
    disable_redirect: bool = True,
) -> Iterator[dict]:
    workflow, namespace = _create_workflow(executor_context)

    def call_node() -> Generator[dict[str, Any], Any, None]:
        executor_context.stream_start_time = time.time_ns()

        for event in workflow.run_node(executor_context.node_ref, inputs=executor_context.inputs):
            yield event.model_dump(mode="json")

    return _call_stream(
        executor_context=executor_context,
        stream_generator=call_node,
        disable_redirect=disable_redirect,
        timeout_signal=ThreadingEvent(),
    )


def _call_stream(
    executor_context: BaseExecutorContext,
    stream_generator: Callable[[], Generator[dict[str, Any], Any, None]],
    timeout_signal: CancelSignal,
    disable_redirect: bool = True,
) -> Iterator[dict]:
    log_redirect: Optional[StringIO] = None

    if not disable_redirect:
        log_redirect = redirect_log()

    try:
        yield from stream_generator()

        if not executor_context.exclude_vembda_events:
            vembda_fulfilled_event = VembdaExecutionFulfilledEvent(
                id=uuid4(),
                timestamp=datetime.now(),
                trace_id=executor_context.trace_id,
                span_id=executor_context.execution_id,
                body=VembdaExecutionFulfilledBody(
                    exit_code=0,
                    log=log_redirect.getvalue() if log_redirect else "",
                    stderr="",
                    container_overhead_latency=executor_context.container_overhead_latency,
                    timed_out=timeout_signal.is_set(),
                ),
                parent=None,
            )
            yield vembda_fulfilled_event.model_dump(mode="json")

    except Exception:
        if not executor_context.exclude_vembda_events:
            vembda_fulfilled_event = VembdaExecutionFulfilledEvent(
                id=uuid4(),
                timestamp=datetime.now(),
                trace_id=executor_context.trace_id,
                span_id=executor_context.execution_id,
                body=VembdaExecutionFulfilledBody(
                    exit_code=-1,
                    log=log_redirect.getvalue() if log_redirect else "",
                    stderr=format_exc(),
                    container_overhead_latency=executor_context.container_overhead_latency,
                ),
                parent=None,
            )
            yield vembda_fulfilled_event.model_dump(mode="json")
        else:
            parent = executor_context.execution_context.parent_context if executor_context.execution_context else None
            if isinstance(executor_context, NodeExecutorContext):
                rejected_event: BaseEvent = NodeExecutionRejectedEvent(
                    trace_id=executor_context.trace_id,
                    span_id=executor_context.execution_id,
                    body=NodeExecutionRejectedBody(
                        node_definition=BaseNode,
                        error=WorkflowError(
                            code=WorkflowErrorCode.INTERNAL_ERROR,
                            message="Node execution failed",
                        ),
                        stacktrace=format_exc(),
                    ),
                    parent=parent,
                )
            else:
                rejected_event = WorkflowExecutionRejectedEvent(
                    trace_id=executor_context.trace_id,
                    span_id=executor_context.execution_id,
                    body=WorkflowExecutionRejectedBody(
                        workflow_definition=BaseWorkflow,
                        error=WorkflowError(
                            code=WorkflowErrorCode.INTERNAL_ERROR,
                            message="Workflow execution failed",
                        ),
                        stacktrace=format_exc(),
                    ),
                    parent=parent,
                )
            yield _dump_event(
                event=rejected_event,
                executor_context=executor_context,
            )


def _create_workflow(executor_context: BaseExecutorContext) -> Tuple[BaseWorkflow, str]:
    namespace = _get_file_namespace(executor_context)
    if namespace != LOCAL_WORKFLOW_MODULE:
        sys.meta_path.append(
            VirtualFileFinder(executor_context.files, namespace, source_module=executor_context.module)
        )

    workflow_context = _create_workflow_context(executor_context)
    Workflow = BaseWorkflow.load_from_module(namespace)
    VembdaExecutionFulfilledEvent.model_rebuild(
        # Not sure why this is needed, but it is required for the VembdaExecutionFulfilledEvent to be
        # properly rebuilt with the recursive types.
        # use flag here to determine which emitter to use
        _types_namespace={
            "BaseWorkflow": BaseWorkflow,
            "BaseNode": BaseNode,
        },
    )

    # Determine whether to enable the Vellum Emitter for event publishing
    use_vellum_emitter = is_events_emitting_enabled(executor_context)
    emitters: list["BaseWorkflowEmitter"] = []
    if use_vellum_emitter:
        emitters = [VellumEmitter()]

    use_vellum_resolver = executor_context.previous_execution_id is not None
    resolvers: list["BaseWorkflowResolver"] = []
    if use_vellum_resolver:
        resolvers = [VellumResolver()]

    # Explicit constructor call to satisfy typing
    workflow = Workflow(
        context=workflow_context,
        store=EmptyStore(),
        emitters=emitters,
        resolvers=resolvers,
    )

    return workflow, namespace


def _create_workflow_context(executor_context: BaseExecutorContext) -> WorkflowContext:
    if executor_context.environment_variables:
        os.environ.update(executor_context.environment_variables)

    namespace = _get_file_namespace(executor_context)

    return WorkflowContext(
        vellum_client=executor_context.vellum_client,
        execution_context=executor_context.execution_context,
        generated_files=executor_context.files,
        namespace=namespace,
    )


def _get_file_namespace(executor_context: BaseExecutorContext) -> str:
    if (
        LOCAL_WORKFLOW_MODULE
        and hasattr(executor_context.execution_context.parent_context, "deployment_name")
        and LOCAL_DEPLOYMENT == executor_context.execution_context.parent_context.deployment_name  # type: ignore
    ):
        return LOCAL_WORKFLOW_MODULE

    if executor_context.execution_id:
        return str(executor_context.execution_id)

    return get_random_namespace()


def get_random_namespace() -> str:
    return "workflow_tmp_" + "".join(random.choice(string.ascii_letters + string.digits) for i in range(14))


def _enrich_event(event: WorkflowEvent, executor_context: Optional[BaseExecutorContext] = None) -> WorkflowEvent:
    """
    Enrich an event with metadata based on the event type.

    For initiated events, include server and SDK versions.
    For fulfilled events with WORKFLOW_DEPLOYMENT parent, include memory usage.
    """
    metadata: Optional[dict] = None

    try:
        is_deployment = event.parent and event.parent.type in ("WORKFLOW_DEPLOYMENT", "EXTERNAL")

        if event.name == "workflow.execution.initiated" and is_deployment:
            metadata = {
                **get_version(),
            }

            memory_mb = get_memory_in_use_mb()
            if memory_mb is not None:
                metadata["memory_usage_mb"] = memory_mb

            if executor_context is not None:
                metadata["is_new_server"] = executor_context.is_new_server

                if executor_context.vembda_service_initiated_timestamp is not None and event.timestamp is not None:
                    event_ts = event.timestamp
                    if event_ts.tzinfo is None:
                        event_ts = event_ts.replace(tzinfo=timezone.utc)
                    event_ts_ns = int(event_ts.timestamp() * 1_000_000_000)
                    initiated_latency = event_ts_ns - executor_context.vembda_service_initiated_timestamp
                    metadata["initiated_latency"] = initiated_latency
        elif event.name == "workflow.execution.fulfilled" and is_deployment:
            metadata = {}
            memory_mb = get_memory_in_use_mb()
            if memory_mb is not None:
                metadata["memory_usage_mb"] = memory_mb
    except Exception:
        pass

    vellum_client = executor_context.vellum_client if executor_context else None
    return event_enricher(event, vellum_client, metadata=metadata)


def _dump_event(event: BaseEvent, executor_context: BaseExecutorContext) -> dict:
    module_base = executor_context.module.split(".")

    dump = event.model_dump(
        mode="json",
        context={"event_enricher": lambda event: _enrich_event(event, executor_context)},
    )
    if dump["name"] in {
        "workflow.execution.initiated",
        "workflow.execution.fulfilled",
        "workflow.execution.rejected",
        "workflow.execution.streaming",
        "workflow.execution.paused",
        "workflow.execution.resumed",
    }:
        dump["body"]["workflow_definition"]["module"] = module_base + dump["body"]["workflow_definition"]["module"][1:]
    elif dump["name"] in {
        "node.execution.initiated",
        "node.execution.fulfilled",
        "node.execution.rejected",
        "node.execution.streaming",
        "node.execution.paused",
        "node.execution.resumed",
    }:
        dump["body"]["node_definition"]["module"] = module_base + dump["body"]["node_definition"]["module"][1:]

    return dump
