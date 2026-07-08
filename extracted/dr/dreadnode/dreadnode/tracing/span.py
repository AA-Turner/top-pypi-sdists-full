from __future__ import annotations

import contextlib
import hashlib
import time
import typing as t
from contextvars import ContextVar, Token
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID, uuid4

import typing_extensions as te
from logfire._internal.json_encoder import logfire_json_dumps as json_dumps
from logfire._internal.json_schema import (
    JsonSchemaProperties,
    attributes_json_schema,
    create_json_schema,
)
from logfire._internal.tracer import OPEN_SPANS
from logfire._internal.utils import uniquify_sequence
from loguru import logger
from opentelemetry import context as context_api
from opentelemetry import propagate
from opentelemetry import trace as trace_api
from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.trace.status import Status, StatusCode

from dreadnode.core.metric import Metric, MetricAggMode, MetricsDict, MetricSeries
from dreadnode.core.object import Object, ObjectRef, ObjectUri, ObjectVal
from dreadnode.core.serialization import Serialized, serialize
from dreadnode.core.types.common import UNSET, AnyDict, Arguments, JsonDict, Unset
from dreadnode.core.util import clean_str
from dreadnode.tracing.constants import (
    EVENT_ATTRIBUTE_LINK_HASH,
    EVENT_ATTRIBUTE_OBJECT_HASH,
    EVENT_ATTRIBUTE_ORIGIN_SPAN_ID,
    EVENT_NAME_OBJECT,
    EVENT_NAME_OBJECT_INPUT,
    EVENT_NAME_OBJECT_LINK,
    EVENT_NAME_OBJECT_METRIC,
    EVENT_NAME_OBJECT_OUTPUT,
    METRIC_ATTRIBUTE_SOURCE_HASH,
    SPAN_ATTRIBUTE_ARTIFACTS,
    SPAN_ATTRIBUTE_INPUTS,
    SPAN_ATTRIBUTE_LABEL,
    SPAN_ATTRIBUTE_LARGE_ATTRIBUTES,
    SPAN_ATTRIBUTE_METRICS,
    SPAN_ATTRIBUTE_OBJECT_SCHEMAS,
    SPAN_ATTRIBUTE_OBJECTS,
    SPAN_ATTRIBUTE_OUTPUTS,
    SPAN_ATTRIBUTE_PARAMS,
    SPAN_ATTRIBUTE_PARENT_TASK_ID,
    SPAN_ATTRIBUTE_PROJECT,
    SPAN_ATTRIBUTE_RUN_ID,
    SPAN_ATTRIBUTE_SCHEMA,
    SPAN_ATTRIBUTE_SESSION_ID,
    SPAN_ATTRIBUTE_TAGS_,
    SPAN_ATTRIBUTE_TYPE,
    SPAN_ATTRIBUTE_VERSION,
    SpanType,
)
from dreadnode.version import VERSION

R = t.TypeVar("R")

if t.TYPE_CHECKING:
    import types

    from opentelemetry.trace import Tracer
    from opentelemetry.util import types as otel_types

    from dreadnode.storage import Storage


current_task_span: ContextVar[TaskSpan[t.Any] | None] = ContextVar(
    "current_task_span",
    default=None,
)
current_session_id: ContextVar[str | None] = ContextVar("current_session_id", default=None)

# The capability (name, version) an agent is running under, if any. Set when an
# agent is created from a capability so runtime tools (e.g. report_item) can
# attribute emitted items to their producer for schema validation.
current_capability: ContextVar[tuple[str, str] | None] = ContextVar(
    "current_capability", default=None
)


@contextlib.contextmanager
def bind_session_id(session_id: str) -> t.Iterator[None]:
    """Bind a session ID to all spans created in the current context."""
    token = current_session_id.set(session_id)
    try:
        yield
    finally:
        current_session_id.reset(token)


@contextlib.contextmanager
def bind_capability(capability: tuple[str, str] | None) -> t.Iterator[None]:
    """Scope ``current_capability`` to a block, resetting it on exit.

    Use the token pattern so capability attribution can't leak from one agent
    run into a later agent that shares the same async context (e.g. a later
    capability-less agent inheriting a stale value).
    """
    token = current_capability.set(capability)
    try:
        yield
    finally:
        current_capability.reset(token)


def _format_status(status: Status) -> str:
    """Format the status for display."""
    if status.status_code == StatusCode.ERROR:
        if status.description is None:
            return "'error'"
        return f"'error - {status.description}'"
    return "'ok'"


class Span(ReadableSpan):
    def __init__(
        self,
        name: str,
        tracer: Tracer,
        *,
        attributes: AnyDict | None = None,
        label: str | None = None,
        type: SpanType = "span",
        tags: t.Sequence[str] | None = None,
    ) -> None:
        self._label = label or ""
        self._span_name = name

        tags = [tags] if isinstance(tags, str) else list(tags or [])
        tags = [clean_str(t) for t in tags]
        self.tags: tuple[str, ...] = uniquify_sequence(tags)

        self._pre_attributes = {
            SPAN_ATTRIBUTE_VERSION: VERSION,
            SPAN_ATTRIBUTE_TYPE: type,
            SPAN_ATTRIBUTE_LABEL: self._label,
            SPAN_ATTRIBUTE_TAGS_: self.tags,
            **(attributes or {}),
        }
        if (session_id := current_session_id.get()) is not None:
            self._pre_attributes.setdefault(SPAN_ATTRIBUTE_SESSION_ID, session_id)
        self._tracer = tracer

        self._schema: JsonSchemaProperties = JsonSchemaProperties({})
        self._token: object | None = None  # trace sdk context
        self._span: trace_api.Span | None = None
        self._exception: BaseException | None = None
        self._traceback: types.TracebackType | None = None

    if not t.TYPE_CHECKING:

        def __getattr__(self, name: str) -> t.Any:
            return getattr(self._span, name)

    def __enter__(self) -> te.Self:
        if self._span is None:
            self._span = self._tracer.start_span(
                name=self._span_name,
                attributes=prepare_otlp_attributes(self._pre_attributes),
            )

        self._span.__enter__()

        OPEN_SPANS.add(self._span)

        if self._token is None:
            self._token = context_api.attach(trace_api.set_span_in_context(self._span))

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> None:
        if self._token is None or self._span is None:
            return

        self._span.set_attribute(
            SPAN_ATTRIBUTE_SCHEMA,
            attributes_json_schema(self._schema) if self._schema else r"{}",
        )
        self._span.set_attribute(SPAN_ATTRIBUTE_TAGS_, self.tags)

        # Avoid recording control-flow exceptions (BaseException) as errors
        if not isinstance(exc_value, Exception):
            exc_value = None
            traceback = None

        if exc_value is not None:
            self.set_exception(exc_value, traceback=traceback)

        self._span.__exit__(exc_type, exc_value, traceback)

        OPEN_SPANS.discard(self._span)

        with contextlib.suppress(ValueError):
            context_api.detach(self._token)
        self._token = None

    @property
    def span_id(self) -> str:
        if self._span is None:
            raise ValueError("Span is not active")
        return trace_api.format_span_id(self._span.get_span_context().span_id)

    @property
    def trace_id(self) -> str:
        if self._span is None:
            raise ValueError("Span is not active")
        return trace_api.format_trace_id(self._span.get_span_context().trace_id)

    @property
    def label(self) -> str:
        """Get the label of the span."""
        return self._label

    @property
    def is_recording(self) -> bool:
        """Check if the span is currently recording."""
        if self._span is None:
            return False
        return self._span.is_recording()

    @property
    def active(self) -> bool:
        """Check if the span is currently active (recording)."""
        return self._span is not None and self._span.is_recording()

    @property
    def failed(self) -> bool:
        """Check if the span has failed."""
        return self._exception is not None or self.status.status_code == StatusCode.ERROR

    @property
    def exception(self) -> BaseException | None:
        """Get the exception recorded in the span, if any."""
        return self._exception

    @property
    def duration(self) -> float:
        """Get the duration of the span in seconds."""
        if self._span is None:
            return 0.0
        end_time = self.end_time or time.time_ns()
        if not self.start_time:
            return 0.0
        return (end_time - self.start_time) / 1e9

    def set_tags(self, tags: t.Sequence[str]) -> None:
        tags = [tags] if isinstance(tags, str) else list(tags)
        tags = [clean_str(t) for t in tags]
        self.tags = uniquify_sequence(tags)

    def add_tags(self, tags: t.Sequence[str]) -> None:
        tags = [tags] if isinstance(tags, str) else list(tags)
        self.set_tags([*self.tags, *tags])

    def set_attribute(
        self,
        key: str,
        value: t.Any,
        *,
        schema: bool = True,
        raw: bool = False,
    ) -> None:
        self._added_attributes = True
        if schema and raw is False:
            self._schema[key] = create_json_schema(value, set())
        otel_value = self._pre_attributes[key] = value if raw else prepare_otlp_attribute(value)
        if self._span is not None:
            self._span.set_attribute(key, otel_value)
        self._pre_attributes[key] = otel_value

    def set_attributes(self, attributes: AnyDict) -> None:
        for key, value in attributes.items():
            self.set_attribute(key, value)

    def get_attributes(self) -> AnyDict:
        if self._span is not None:
            return getattr(self._span, "attributes", {})
        return self._pre_attributes

    def get_attribute(self, key: str, default: t.Any) -> t.Any:
        return self.get_attributes().get(key, default)

    def log_event(
        self,
        name: str,
        attributes: AnyDict | None = None,
    ) -> None:
        if self._span is not None and self._span.is_recording():
            self._span.add_event(
                name,
                attributes=prepare_otlp_attributes(attributes or {}),
            )

    def set_exception(
        self,
        exception: BaseException,
        *,
        attributes: AnyDict | None = None,
        status: Status | None = None,
        traceback: types.TracebackType | None = None,
    ) -> None:
        self._exception = exception
        self._traceback = traceback

        if self._span is None or not self._span.is_recording():
            return

        if status is None:
            status = Status(StatusCode.ERROR, str(exception))

        self._span.set_status(status)
        self._span.record_exception(
            exception,
            attributes=prepare_otlp_attributes(attributes or {}),
        )

    def raise_if_failed(self) -> None:
        if self.exception is not None:
            raise (
                self.exception.with_traceback(self._traceback)
                if self._traceback
                else self.exception
            )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(name='{self._span_name}', id={self.span_id},"
            f"label='{self._label}', status={_format_status(self.status)}, active={self.is_recording})"
        )

    def __str__(self) -> str:
        return f"{self._span_name} ({self._label})" if self._label else self._span_name


class TaskContext(te.TypedDict):
    """Context for transferring and continuing tasks across processes."""

    task_id: str
    task_name: str
    project: str
    trace_context: dict[str, str]


# Backwards compatibility alias
RunContext = TaskContext


class TaskSpan(Span, t.Generic[R]):
    """Self-sufficient task span with object storage, metrics, params, and artifacts.

    TaskSpan is the primary span type for all operations. It manages its own:
    - Object storage (inputs, outputs, arbitrary objects)
    - Metrics tracking
    - Parameters
    - Artifacts
    - Child tasks

    TaskSpans can be nested - a TaskSpan can contain child TaskSpans.
    """

    def __init__(
        self,
        name: str,
        tracer: Tracer,
        *,
        storage: Storage | None = None,
        project: str = "default",
        task_id: str | UUID | None = None,
        type: SpanType = "task",
        attributes: AnyDict | None = None,
        label: str | None = None,
        params: AnyDict | None = None,
        metrics: MetricsDict | None = None,
        tags: t.Sequence[str] | None = None,
        arguments: Arguments | None = None,
    ) -> None:
        # Core identity
        self.project_id = project
        self._task_id = str(task_id or uuid4())

        # Object storage
        self._storage = storage
        self._objects: dict[str, Object] = {}
        self._object_schemas: dict[str, JsonDict] = {}

        # Data tracking
        self._params = params or {}
        self._metrics = metrics or {}
        self._inputs: list[ObjectRef] = []
        self._outputs: list[ObjectRef] = []
        self._artifacts: list[dict[str, t.Any]] = []

        # Task hierarchy
        self._tasks: list[TaskSpan[t.Any]] = []
        self._parent_task: TaskSpan[t.Any] | None = None

        # Function task support
        self._arguments = arguments
        self._output: R | Unset = UNSET

        # Context management
        self._context_token: Token[TaskSpan[t.Any] | None] | None = None
        self._remote_context: dict[str, str] | None = None
        self._remote_token: object | None = None

        # Run ID is set lazily in __enter__ to inherit from parent if applicable
        self._run_id: str | None = None

        attributes = {
            SPAN_ATTRIBUTE_PROJECT: project,
            SPAN_ATTRIBUTE_INPUTS: self._inputs,
            SPAN_ATTRIBUTE_METRICS: self._metrics,
            SPAN_ATTRIBUTE_OUTPUTS: self._outputs,
            **(attributes or {}),
        }
        super().__init__(name, tracer, type=type, attributes=attributes, label=label, tags=tags)

    @classmethod
    def from_context(
        cls,
        context: TaskContext,
        tracer: Tracer,
        storage: Storage | None = None,
    ) -> TaskSpan[t.Any]:
        """Continue a task from captured context on a remote host."""
        task = TaskSpan(
            name=f"task.{context['task_id']}.fragment",
            tracer=tracer,
            storage=storage,
            project=context["project"],
            task_id=context["task_id"],
            type="task_fragment",
        )
        task._remote_context = context["trace_context"]
        return task

    def __enter__(self) -> te.Self:
        # Handle remote context continuation
        if self._remote_context is not None:
            global_propagator = propagate.get_global_textmap()
            if "NoExtract" in type(global_propagator).__name__:
                w3c_propagator = TraceContextTextMapPropagator()
                otel_context = w3c_propagator.extract(carrier=self._remote_context)
            else:
                otel_context = propagate.extract(carrier=self._remote_context)

            span_context = trace_api.get_current_span(otel_context).get_span_context()

            if span_context.trace_id != 0:
                self._remote_token = context_api.attach(otel_context)
            else:
                super().__enter__()
        else:
            super().__enter__()

        # Set up task hierarchy
        self._parent_task = current_task_span.get()
        if self._parent_task is not None:
            self.set_attribute(SPAN_ATTRIBUTE_PARENT_TASK_ID, self._parent_task.span_id)
            self._parent_task._tasks.append(self)
            if self._storage is None:
                self._storage = self._parent_task._storage
            self._run_id = self._parent_task._run_id
        else:
            # Root task - run_id is this task's own ID
            self._run_id = self._task_id

        # Set the run_id attribute for span routing
        self.set_attribute(SPAN_ATTRIBUTE_RUN_ID, self._run_id, raw=True)

        self._context_token = current_task_span.set(self)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> None:
        if self._remote_context is not None:
            super().__enter__()  # Open actual span for remote continuation

        # Store final state as attributes
        self.set_attribute(SPAN_ATTRIBUTE_PARAMS, self._params, schema=False)
        self.set_attribute(SPAN_ATTRIBUTE_INPUTS, self._inputs, schema=False)
        self.set_attribute(SPAN_ATTRIBUTE_OUTPUTS, self._outputs, schema=False)
        self.set_attribute(SPAN_ATTRIBUTE_METRICS, self._metrics, schema=False)
        self.set_attribute(SPAN_ATTRIBUTE_OBJECTS, self._objects, schema=False)
        self.set_attribute(SPAN_ATTRIBUTE_OBJECT_SCHEMAS, self._object_schemas, schema=False)
        self.set_attribute(SPAN_ATTRIBUTE_ARTIFACTS, self._artifacts, schema=False)

        # Mark large attributes
        if self._objects or self._object_schemas:
            self.set_attribute(
                SPAN_ATTRIBUTE_LARGE_ATTRIBUTES,
                [SPAN_ATTRIBUTE_OBJECTS, SPAN_ATTRIBUTE_OBJECT_SCHEMAS],
                raw=True,
            )

        super().__exit__(exc_type, exc_value, traceback)

        # Clean up remote context
        if self._remote_token is not None:
            with contextlib.suppress(ValueError):
                context_api.detach(self._remote_token)

        # Clean up task context
        if self._context_token is not None:
            with contextlib.suppress(ValueError):
                current_task_span.reset(self._context_token)

    # =========================================================================
    # Identity Properties
    # =========================================================================

    @property
    def task_id(self) -> str:
        """Get this task's unique ID."""
        return self._task_id

    @property
    def root_id(self) -> str:
        """Get the root task's ID (for span grouping/routing)."""
        return self._run_id or self._task_id

    @property
    def agent_id(self) -> str | None:
        """Get the ID of the nearest agent span in the parent chain."""
        span = self._find_ancestor_by_type("agent")
        return span.task_id if span else None

    @property
    def eval_id(self) -> str | None:
        """Get the ID of the nearest evaluation span in the parent chain."""
        span = self._find_ancestor_by_type("evaluation")
        return span.task_id if span else None

    @property
    def study_id(self) -> str | None:
        """Get the ID of the nearest study span in the parent chain."""
        span = self._find_ancestor_by_type("study")
        return span.task_id if span else None

    def _find_ancestor_by_type(self, span_type: str) -> TaskSpan[t.Any] | None:
        """Find the nearest ancestor span with the given type."""
        current: TaskSpan[t.Any] | None = self
        while current is not None:
            if current._pre_attributes.get(SPAN_ATTRIBUTE_TYPE) == span_type:
                return current
            current = current.parent_task
        return None

    # Backwards compatibility alias
    @property
    def run_id(self) -> str:
        """Alias for root_id (backwards compatibility)."""
        return self.root_id

    @property
    def parent_task_id(self) -> str:
        """Get the parent task ID if it exists."""
        return str(self.get_attribute(SPAN_ATTRIBUTE_PARENT_TASK_ID, ""))

    @property
    def parent_task(self) -> TaskSpan[t.Any] | None:
        """Get the parent task if it exists."""
        return self._parent_task

    @property
    def tasks(self) -> list[TaskSpan[t.Any]]:
        """Get the list of child tasks."""
        return self._tasks

    @property
    def all_tasks(self) -> list[TaskSpan[t.Any]]:
        """Get all tasks, including nested subtasks."""
        all_tasks = []
        for task in self._tasks:
            all_tasks.append(task)
            all_tasks.extend(task.all_tasks)
        return all_tasks

    # =========================================================================
    # Object Storage
    # =========================================================================

    def log_object(
        self,
        value: t.Any,
        *,
        label: str | None = None,  # noqa: ARG002 - reserved for future event/log integration
        event_name: str = EVENT_NAME_OBJECT,  # noqa: ARG002 - reserved for future event/log integration
        attributes: AnyDict | None = None,  # noqa: ARG002 - reserved for future event/log integration
    ) -> str:
        """Store an object and return its hash. Objects are stored but not logged as span events."""
        serialized = serialize(value)
        data_hash = serialized.data_hash
        schema_hash = serialized.schema_hash

        # Create composite key for data + schema
        hash_input = f"{data_hash}:{schema_hash}"
        composite_hash = hashlib.sha1(hash_input.encode()).hexdigest()[:16]  # noqa: S324

        # Store schema if new
        if schema_hash not in self._object_schemas:
            self._object_schemas[schema_hash] = serialized.schema

        # Store object if new
        if composite_hash not in self._objects:
            obj = self._create_object_by_hash(serialized, composite_hash)
            obj.runtime_value = value
            self._objects[composite_hash] = obj

        return composite_hash

    def _store_file_by_hash(self, data_bytes: bytes, full_path: str) -> str:
        """Store file to remote storage."""
        if self._storage is None:
            raise RuntimeError("Storage is not configured for file storage.")

        filesystem = self._storage._get_filesystem()
        logger.debug(
            "Storing object by hash: path={}, fs_type={}",
            full_path,
            type(filesystem).__name__,
        )
        if not filesystem.exists(full_path):
            with filesystem.open(full_path, "wb") as f:
                f.write(data_bytes)
        return str(filesystem.unstrip_protocol(full_path))

    def _create_object_by_hash(self, serialized: Serialized, object_hash: str) -> Object:
        """Create an ObjectVal or ObjectUri depending on size."""
        data = serialized.data
        data_bytes = serialized.data_bytes
        data_len = serialized.data_len
        data_hash = serialized.data_hash
        schema_hash = serialized.schema_hash

        # Keep small objects inline
        if self._storage is None or data is None or data_bytes is None or data_len <= 10 * 1024:
            return ObjectVal(
                hash=object_hash,
                value=data,
                schema_hash=schema_hash,
            )

        # Offload large objects to remote storage if available, otherwise keep inline
        try:
            bucket = self._storage.remote_bucket
            prefix = self._storage.remote_prefix
            full_path = f"{bucket}/{prefix.rstrip('/')}/{data_hash}"
            object_uri = self._store_file_by_hash(data_bytes, full_path)
            return ObjectUri(
                hash=object_hash,
                uri=object_uri,
                schema_hash=schema_hash,
                size=data_len,
            )
        except Exception:
            logger.debug("Remote object storage failed, keeping object inline", exc_info=True)
            return ObjectVal(
                hash=object_hash,
                value=data,
                schema_hash=schema_hash,
            )

    def get_object(self, hash_: str) -> Object:
        """Get an object by its hash."""
        return self._objects[hash_]

    def link_objects(
        self,
        object_hash: str,
        link_hash: str,
        attributes: AnyDict | None = None,
    ) -> None:
        """Link two objects together."""
        self.log_event(
            name=EVENT_NAME_OBJECT_LINK,
            attributes={
                **(attributes or {}),
                EVENT_ATTRIBUTE_OBJECT_HASH: object_hash,
                EVENT_ATTRIBUTE_LINK_HASH: link_hash,
                EVENT_ATTRIBUTE_ORIGIN_SPAN_ID: trace_api.format_span_id(
                    trace_api.get_current_span().get_span_context().span_id,
                ),
            },
        )

    # =========================================================================
    # Parameters
    # =========================================================================

    @property
    def params(self) -> AnyDict:
        """Get all parameters."""
        return self._params

    def log_param(self, key: str, value: t.Any) -> None:
        """Log a single parameter."""
        self.log_params(**{key: value})

    def log_params(self, **params: t.Any) -> None:
        """Log multiple parameters."""
        for key, value in params.items():
            self._params[key] = value

    # =========================================================================
    # Inputs and Outputs
    # =========================================================================

    @property
    def inputs(self) -> AnyDict:
        """Get all logged inputs."""
        return {
            ref.name: obj.value if (obj := self._objects.get(ref.hash)) is not None else ref.hash
            for ref in self._inputs
        }

    def log_input(
        self,
        name: str,
        value: t.Any,
        *,
        label: str | None = None,
        attributes: AnyDict | None = None,
    ) -> str:
        """Log an input value."""
        label = clean_str(label or name)
        hash_ = self.log_object(value, label=label, event_name=EVENT_NAME_OBJECT_INPUT)
        self._inputs.append(ObjectRef(name, label=label, hash=hash_, attributes=attributes))
        return hash_

    @property
    def outputs(self) -> AnyDict:
        """Get all logged outputs."""
        return {
            ref.name: obj.value if (obj := self._objects.get(ref.hash)) is not None else ref.hash
            for ref in self._outputs
        }

    def log_output(
        self,
        name: str,
        value: t.Any,
        *,
        label: str | None = None,
        attributes: AnyDict | None = None,
    ) -> str:
        """Log an output value."""
        label = clean_str(label or name)
        hash_ = self.log_object(value, label=label, event_name=EVENT_NAME_OBJECT_OUTPUT)
        self._outputs.append(ObjectRef(name, label=label, hash=hash_, attributes=attributes))
        return hash_

    # =========================================================================
    # Metrics
    # =========================================================================

    @property
    def metrics(self) -> MetricsDict:
        """Get all metrics."""
        return self._metrics

    @t.overload
    def log_metric(
        self,
        name: str,
        value: float | bool,
        *,
        step: int = 0,
        origin: t.Any | None = None,
        timestamp: datetime | None = None,
        aggregation: MetricAggMode | None = None,
        prefix: str | None = None,
        attributes: JsonDict | None = None,
    ) -> Metric: ...

    @t.overload
    def log_metric(
        self,
        name: str,
        value: Metric,
        *,
        origin: t.Any | None = None,
        aggregation: MetricAggMode | None = None,
        prefix: str | None = None,
    ) -> Metric: ...

    def log_metric(
        self,
        name: str,
        value: float | bool | Metric,
        *,
        step: int = 0,
        origin: t.Any | None = None,
        timestamp: datetime | None = None,
        aggregation: MetricAggMode | None = None,
        prefix: str | None = None,
        attributes: JsonDict | None = None,
    ) -> Metric:
        """Log a metric value."""
        metric = (
            value
            if isinstance(value, Metric)
            else Metric(
                float(value),
                step,
                timestamp or datetime.now(UTC),
                attributes or {},
            )
        )

        key = clean_str(name)
        if prefix is not None:
            key = f"{prefix}.{key}"

        if origin is not None:
            origin_hash = self.log_object(origin, label=key, event_name=EVENT_NAME_OBJECT_METRIC)
            metric.attributes[METRIC_ATTRIBUTE_SOURCE_HASH] = origin_hash

        if aggregation is not None:
            metric.attributes["aggregation"] = aggregation

        series = self._metrics.setdefault(key, MetricSeries())
        series.append(value=metric.value, step=step)

        return metric

    def get_average_metric_value(self, key: str) -> float:
        """Get the mean of a metric series."""
        series = self._metrics.get(key)
        if series:
            mean = series.mean()
            if mean is not None:
                return mean
        return 0.0

    # =========================================================================
    # Artifacts
    # =========================================================================

    def log_artifact(
        self,
        local_uri: str | Path,
        *,
        name: str | None = None,
    ) -> dict[str, t.Any] | None:
        """Log a file as an artifact."""
        import mimetypes

        if self._storage is None:
            raise RuntimeError("Storage is not configured for artifact logging.")

        local_path = Path(local_uri).expanduser().resolve()
        if not local_path.exists():
            raise FileNotFoundError(f"Artifact not found: {local_path}")

        if local_path.is_dir():
            artifacts = []
            for file_path in local_path.rglob("*"):
                if file_path.is_file():
                    rel_path = file_path.relative_to(local_path)
                    artifact_name = f"{name or local_path.name}/{rel_path}"
                    artifact = self.log_artifact(file_path, name=artifact_name)
                    if artifact:
                        artifacts.append(artifact)
            return {"type": "directory", "name": name or local_path.name, "files": artifacts}

        oid = self._storage.store_artifact(local_path, upload=True)

        mime_type, _ = mimetypes.guess_type(str(local_path))
        artifact_metadata = {
            "task_id": self._task_id,
            "span_id": self.span_id,
            "name": name or local_path.name,
            "oid": oid,
            "path": str(local_path),
            "size": local_path.stat().st_size,
            "mime_type": mime_type,
            "timestamp": datetime.now(UTC).isoformat(),
        }

        self._artifacts.append(artifact_metadata)
        return artifact_metadata

    # =========================================================================
    # Function Task Support
    # =========================================================================

    @property
    def arguments(self) -> Arguments | None:
        """Get the arguments used for this task if created from a function."""
        return self._arguments

    @property
    def output(self) -> R:
        """Get the output of this task if created from a function."""
        self.raise_if_failed()
        if isinstance(self._output, Unset):
            raise TypeError("Task output is not set")
        return self._output

    @output.setter
    def output(self, value: R) -> None:
        self._output = value

    # =========================================================================
    # String Representations
    # =========================================================================

    def __repr__(self) -> str:
        task_id = self._task_id
        parent_task_id = self.parent_task_id
        num_subtasks = len(self._tasks)
        num_inputs = len(self._inputs)
        num_outputs = len(self._outputs)
        num_objects = len(self._objects)

        parent_info = f", parent_task='{parent_task_id}'" if parent_task_id else ""
        return (
            f"TaskSpan(name='{self.name}', id='{task_id}', "
            f"project='{self.project_id}'{parent_info}, status={_format_status(self.status)}, "
            f"active={self.is_recording}, tasks={num_subtasks}, "
            f"inputs={num_inputs}, outputs={num_outputs}, objects={num_objects})"
        )

    def __str__(self) -> str:
        if self._label and self._label != self.name:
            return f"{self.name} ({self._label})"
        return self.name


# =========================================================================
# Utility Functions
# =========================================================================


def prepare_otlp_attributes(
    attributes: AnyDict,
) -> dict[str, otel_types.AttributeValue]:
    return {key: prepare_otlp_attribute(value) for key, value in attributes.items()}


def prepare_otlp_attribute(value: t.Any) -> otel_types.AttributeValue:
    if isinstance(value, str | int | bool | float):
        return value
    return json_dumps(value)


def get_default_tracer() -> Tracer:
    """Get the default tracer from the default Dreadnode instance."""
    from dreadnode import DEFAULT_INSTANCE

    return DEFAULT_INSTANCE.get_tracer()


def get_current_task_span() -> TaskSpan[t.Any] | None:
    """Get the current task span."""
    return current_task_span.get()


# Backwards compatibility alias
def get_current_run_span() -> TaskSpan[t.Any] | None:
    """Get the current task span (backwards compatibility)."""
    return current_task_span.get()


def find_span_by_type(span_type: str) -> TaskSpan[t.Any] | None:
    """Find the nearest ancestor span with the given type.

    Walks up the parent chain from the current task span to find
    a span matching the specified type (e.g., "agent", "evaluation", "study").

    Args:
        span_type: The span type to search for (e.g., "agent", "evaluation", "study").

    Returns:
        The matching TaskSpan or None if not found.
    """
    task = current_task_span.get()
    while task is not None:
        task_type = task._pre_attributes.get(SPAN_ATTRIBUTE_TYPE)
        if task_type == span_type:
            return task
        task = task.parent_task
    return None
