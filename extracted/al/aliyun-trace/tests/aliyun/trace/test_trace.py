from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter as OTLPSpanHttpExporter
from opentelemetry import trace

from aliyun.trace.aliyun_llm_trace import start_llm_span, start_as_current_span
from aliyun.trace.entities.arms_llm_trace_entity import LLM
from aliyun.trace.entities.arms_llm_trace_entity import add_attribute

resource = Resource(
    attributes={
        SERVICE_NAME: 'aliyun_llm_dashscope_test',
        SERVICE_VERSION: '0.0.1',
        "source": "python agent",
        # "telemetry.sdk.language": "Python",
    }
)
provider = TracerProvider(resource=resource)
provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))  # 在控制台输出Trace
trace.set_tracer_provider(provider)


def mock_start_llm_span():
    print(f"test_start_llm_span")
    tracer_provider = trace.get_tracer_provider()
    _tracer = trace.get_tracer(__name__, tracer_provider=tracer_provider)
    llm = LLM(sub_kind="CHAT", )
    with start_llm_span(tracer=_tracer, llm=llm) as span:
        print(span.attributes)
    # with start_as_current_span(
    #         tracer=_tracer,
    #         name=llm.get_type(),
    #         attributes=llm.get_attributes()) as span:
    #     print(f'span:{span}')


def test_add_attribute():
    attr = {}
    key = "key"
    val = "val"
    add_attribute(attr, key, val)

    add_attribute(attr, key, None)


if __name__ == "__main__":
    mock_start_llm_span()
