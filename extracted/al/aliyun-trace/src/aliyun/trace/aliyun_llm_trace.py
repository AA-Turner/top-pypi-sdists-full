import contextlib

from aliyun.trace.entities.arms_llm_trace_entity import (
    LLM,
    Chain,
    Retriever,
    ReRanker,
    Embeddings,
    Tool,
    Agent,
    Task
)
from opentelemetry.baggage import get_all
from opentelemetry import trace as otel_trace
from opentelemetry.trace.status import Status, StatusCode
from opentelemetry.trace import Span
from typing import Optional, Sequence
from opentelemetry.util import types
from opentelemetry.propagate import extract
from opentelemetry.context import attach

TRAFFIC_PREFIX = "traffic.llm_sdk."

TRAFFIC_ATTRIBUTES_SHADOW = TRAFFIC_PREFIX + "attributes.shadow"


@contextlib.contextmanager
def start_as_current_span(
        tracer: otel_trace.Tracer,
        name: str,
        context: Optional[otel_trace.Context] = None,
        kind: otel_trace.SpanKind = otel_trace.SpanKind.INTERNAL,
        attributes: types.Attributes = None,
        links: Optional[Sequence[otel_trace.Link]] = (),
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        record_exception: bool = True,
        set_status_on_exception: bool = True,
):
    span = None
    final_attributes = attributes
    try:
        attrs = get_all(context=context)
        if len(attrs) > 0:
            shadow_flag = attrs.get(TRAFFIC_ATTRIBUTES_SHADOW)
            if str(shadow_flag) == "1":
                # do shadow
                final_attributes = None
        with tracer.start_as_current_span(
                name,
                context,
                kind,
                final_attributes,
                links,
                start_time,
                record_exception,
                set_status_on_exception,
                end_on_exit=False,
        ) as span:
            setattr(span, "__should_end", True)
            if len(attrs) > 0:
                for key in attrs:
                    if key.startswith(TRAFFIC_PREFIX):
                        new_key = key[len(TRAFFIC_PREFIX):]
                        span.set_attribute(new_key, attrs[key])
            yield span
    except BaseException as e:
        handler_span_exception(span, e)
        raise
    finally:
        if span is not None and getattr(span, "__should_end", False):
            span.end(end_time=end_time)


def handler_span_exception(span, e):
    if isinstance(span, Span) and span.is_recording():
        # Record the exception as an event
        span.record_exception(e)
        # Records status as error
        span.set_status(
            Status(
                status_code=StatusCode.ERROR,
                description=f"{type(e).__name__}: {str(e)}",
            )
        )


@contextlib.contextmanager
def start_llm_span(
        tracer: otel_trace.Tracer,
        llm: LLM,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None):
    with start_as_current_span(
            tracer=tracer,
            name=llm.get_type(),
            attributes=llm.get_attributes(),
            start_time=start_time,
            end_time=end_time,
    ) as span:
        yield span


@contextlib.contextmanager
def start_task_span(tracer: otel_trace.Tracer, task: Task,
                    start_time: Optional[int] = None,
                    end_time: Optional[int] = None):
    with start_as_current_span(
            tracer=tracer,
            name=task.get_type(),
            attributes=task.get_attributes(),
            start_time=start_time,
            end_time=end_time,
    ) as span:
        yield span


@contextlib.contextmanager
def start_chain_span(tracer: otel_trace.Tracer, chain: Chain,
                     start_time: Optional[int] = None,
                     end_time: Optional[int] = None):
    with start_as_current_span(
            tracer=tracer,
            name=chain.get_type(),
            attributes=chain.get_attributes(),
            start_time=start_time,
            end_time=end_time,
    ) as span:
        yield span


@contextlib.contextmanager
def start_retriever_span(tracer: otel_trace.Tracer, retriever: Retriever
                         , start_time: Optional[int] = None,
                         end_time: Optional[int] = None):
    with start_as_current_span(
            tracer=tracer,
            name=retriever.get_type(),
            attributes=retriever.get_attributes(),
            start_time=start_time,
            end_time=end_time,
    ) as span:
        yield span


@contextlib.contextmanager
def start_rerank_span(tracer: otel_trace.Tracer, rerank: ReRanker, start_time: Optional[int] = None,
                      end_time: Optional[int] = None):
    with start_as_current_span(
            tracer=tracer,
            name=rerank.get_type(),
            attributes=rerank.get_attributes(),
            start_time=start_time,
            end_time=end_time,
    ) as span:
        yield span


@contextlib.contextmanager
def start_embedding_span(tracer: otel_trace.Tracer, embedding: Embeddings, start_time: Optional[int] = None,
                         end_time: Optional[int] = None):
    with start_as_current_span(
            tracer=tracer,
            name=embedding.get_type(),
            attributes=embedding.get_attributes(),
            start_time=start_time,
            end_time=end_time,
    ) as span:
        yield span


@contextlib.contextmanager
def start_tool_span(tracer: otel_trace.Tracer, tool: Tool, start_time: Optional[int] = None,
                    end_time: Optional[int] = None):
    with start_as_current_span(
            tracer=tracer,
            name=tool.get_type(),
            attributes=tool.get_attributes(),
            start_time=start_time,
            end_time=end_time,
    ) as span:
        yield span


@contextlib.contextmanager
def start_agent_span(tracer: otel_trace.Tracer, agent: Agent, start_time: Optional[int] = None,
                     end_time: Optional[int] = None):
    with start_as_current_span(
            tracer=tracer,
            name=agent.get_type(),
            attributes=agent.get_attributes(),
            start_time=start_time,
            end_time=end_time
    ) as span:
        yield span


def extract_from_remote(source: dict):
    context = extract(source)
    attach(context)
