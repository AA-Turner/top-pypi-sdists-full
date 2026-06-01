import pytest
from opentelemetry import trace, baggage
from aliyun.trace.aliyun_llm_trace import start_as_current_span
from aliyun.trace.aliyun_llm_trace import TRAFFIC_PREFIX, TRAFFIC_ATTRIBUTES_SHADOW
from typing import Optional
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor


@pytest.fixture
def tracer():
    resource = Resource(
        attributes={
            SERVICE_NAME: 'aliyun_llm_dashscope_test',
            SERVICE_VERSION: '0.0.1',
            "source": "python agent",
        }
    )
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)
    return trace.get_tracer(__name__)


def make_context_with_shadow_flag(flag_value: Optional[str]):
    if flag_value is not None:
        return baggage.set_baggage(TRAFFIC_ATTRIBUTES_SHADOW, flag_value)
    else:
        return None


def test_start_as_current_span_with_shadow_1(tracer):
    context = make_context_with_shadow_flag("1")

    with start_as_current_span(
            tracer=tracer,
            name="test_span",
            context=context,
            attributes={"key": "value"}
    ) as span:
        assert span.attributes is not None
        assert "key" not in span.attributes
        assert span.attributes[TRAFFIC_ATTRIBUTES_SHADOW[len(TRAFFIC_PREFIX):]] == "1"


def test_start_as_current_span_with_shadow_0(tracer):
    context = make_context_with_shadow_flag("0")

    with start_as_current_span(
            tracer=tracer,
            name="test_span",
            context=context,
            attributes={"key": "value"}
    ) as span:
        assert span.attributes is not None
        assert span.attributes["key"] == "value"
        assert span.attributes[TRAFFIC_ATTRIBUTES_SHADOW[len(TRAFFIC_PREFIX):]] == "0"


def test_start_as_current_span_with_no_shadow_flag(tracer):
    context = make_context_with_shadow_flag(None)

    with start_as_current_span(
            tracer=tracer,
            name="test_span",
            context=context,
            attributes={"key": "value"}
    ) as span:
        assert span.attributes is not None
        assert span.attributes["key"] == "value"
