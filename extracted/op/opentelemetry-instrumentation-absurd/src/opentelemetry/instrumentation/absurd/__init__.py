"""OpenTelemetry instrumentation for the Absurd durable-task SDK.

Absurd (`absurd_sdk.AsyncAbsurd`) is a Postgres-backed durable task queue: a producer `spawn()`s a
task and a worker `work_batch()` claims and runs the registered handler, possibly in a different
process. Without instrumentation the two halves live in separate traces, so a task's execution
cannot be linked back to whatever spawned it.

This instrumentor follows the standard producer/consumer span shape for a task queue:

- `AsyncAbsurd.spawn()` is wrapped to open a CLIENT span named after the task and inject the
  current trace context into the task's `headers`. Absurd persists headers on the task row and
  hands them back to the handler via `ctx.headers`.
- `AsyncAbsurd.register_task()` is wrapped so every registered handler runs inside a
  `running:<task>` SERVER span whose parent is extracted from those headers.

The two spans share one trace, so a task's execution is linked back to whatever spawned it.

Usage::

    from opentelemetry.instrumentation.absurd import AbsurdInstrumentor

    AbsurdInstrumentor().instrument()

Install it once per process on both the spawn side and the worker side. Only `AsyncAbsurd` is
instrumented because it is the only client this codebase uses.
"""

from __future__ import annotations

from collections.abc import Callable, Collection, Coroutine
from typing import Any

from absurd_sdk import AsyncAbsurd
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.instrumentation.utils import unwrap
from opentelemetry.propagate import extract, inject
from wrapt import wrap_function_wrapper  # pyright: ignore[reportUnknownVariableType]

from opentelemetry import trace
from opentelemetry.instrumentation.absurd.package import _instruments
from opentelemetry.instrumentation.absurd.version import __version__

__all__ = ['AbsurdInstrumentor', '__version__']

# Task headers are a free-form JSON object shared with the caller, so the trace carrier is nested
# under a single key rather than written as flat top-level headers.
CARRIER_KEYWORD = 'otel.absurd.context'

# `absurd_sdk` types the task handler as `Callable[[Any, AsyncTaskContext], Awaitable[Any]]`; the
# `instance`/`ctx` wrappers below read SDK-private state (`_queue_name`, `_task`) and so are `Any`.
AsyncTaskHandler = Callable[[Any, Any], Coroutine[Any, Any, Any]]


class AbsurdInstrumentor(BaseInstrumentor):
    """Instrument `absurd_sdk.AsyncAbsurd` so spawn and task execution share one distributed trace."""

    def instrumentation_dependencies(self) -> Collection[str]:
        return _instruments

    def _instrument(self, **kwargs: Any) -> None:
        tracer_provider = kwargs.get('tracer_provider')
        tracer = trace.get_tracer(
            __name__,
            __version__,
            tracer_provider=tracer_provider if isinstance(tracer_provider, trace.TracerProvider) else None,
            schema_url='https://opentelemetry.io/schemas/1.11.0',
        )
        wrap_function_wrapper(AsyncAbsurd, 'spawn', _wrap_spawn(tracer))
        wrap_function_wrapper(AsyncAbsurd, 'register_task', _wrap_register_task(tracer))

    def _uninstrument(self, **kwargs: Any) -> None:
        unwrap(AsyncAbsurd, 'spawn')
        unwrap(AsyncAbsurd, 'register_task')


def _wrap_spawn(tracer: trace.Tracer) -> Callable[..., Coroutine[Any, Any, Any]]:
    async def _traced_spawn(
        wrapped: Callable[..., Coroutine[Any, Any, Any]], instance: Any, args: Any, kwargs: Any
    ) -> Any:
        # `task_name` is the first positional argument of `spawn`.
        task_name: str = args[0]
        attributes: dict[str, Any] = {
            'absurd.task.name': task_name,
            'absurd.queue': kwargs.get('queue') or instance._queue_name,
        }
        # OTel drops (and warns on) `None` attribute values, so only set optional ones when present.
        idempotency_key = kwargs.get('idempotency_key')
        if idempotency_key is not None:
            attributes['absurd.task.idempotency_key'] = idempotency_key
        with tracer.start_as_current_span(task_name, kind=trace.SpanKind.CLIENT, attributes=attributes) as span:
            # Inject the current context (this CLIENT span) into a fresh carrier nested under a
            # single header key, so the worker can parent its SERVER span to this span.
            carrier: dict[str, str] = {}
            inject(carrier)
            headers = dict(kwargs.get('headers') or {})
            headers[CARRIER_KEYWORD] = carrier
            kwargs = {**kwargs, 'headers': headers}

            result = await wrapped(*args, **kwargs)

            # The DB mints these as UUIDs; OTel attributes must be primitives, so stringify.
            span.set_attribute('absurd.task.id', str(result['task_id']))
            span.set_attribute('absurd.run.id', str(result['run_id']))
        return result

    return _traced_spawn


def _wrap_register_task(tracer: trace.Tracer) -> Callable[..., Any]:
    def _traced_register_task(
        wrapped: Callable[..., Callable[[AsyncTaskHandler], AsyncTaskHandler]], _instance: Any, args: Any, kwargs: Any
    ) -> Callable[[AsyncTaskHandler], AsyncTaskHandler]:
        # `name` is passed by keyword at every call site (`register_task(name=...)`).
        task_name: str = kwargs['name']
        decorator = wrapped(*args, **kwargs)

        def _traced_decorator(handler: AsyncTaskHandler) -> AsyncTaskHandler:
            return decorator(_trace_handler(tracer, task_name, handler))

        return _traced_decorator

    return _traced_register_task


def _trace_handler(tracer: trace.Tracer, task_name: str, handler: AsyncTaskHandler) -> AsyncTaskHandler:
    """Wrap a task handler so it runs inside a `running:<task>` SERVER span parented to the spawner."""

    async def _traced_handler(params: Any, ctx: Any) -> Any:
        carrier: dict[str, str] = ctx.headers.get(CARRIER_KEYWORD) or {}
        attributes: dict[str, Any] = {
            'absurd.task.name': task_name,
            'absurd.task.id': str(ctx.task_id),
            'absurd.task.attempt': ctx._task.get('attempt'),
            'absurd.queue': ctx._queue_name,
        }
        with tracer.start_as_current_span(
            f'running:{task_name}',
            kind=trace.SpanKind.SERVER,
            context=extract(carrier),
            attributes=attributes,
        ):
            return await handler(params, ctx)

    return _traced_handler
