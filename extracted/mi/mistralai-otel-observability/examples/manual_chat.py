"""Manual chat telemetry example for local OTLP export."""

from mistralai.observability.otel import ObservabilityConfig, observability
from mistralai.observability.otel import semconv_constants as genai

# Configure an isolated SDK instance. This example points at a local OTLP HTTP
# collector; production code can use `observability.configure_mistral(...)`.
observability.configure(
    ObservabilityConfig(
        service_name="manual-chat-example",
        endpoint="http://localhost:4318",
        protocol="http/protobuf",
    )
)

# The operation context manager creates one GenAI chat span and records its
# duration metric when the block exits.
with observability.operation(
    genai.OPERATION_NAME_CHAT,
    model="mistral-large-latest",
    provider=genai.PROVIDER_NAME_MISTRAL_AI,
    include_content=True,
) as chat:
    # Arbitrary spans are useful for intermediate local work, such as cache
    # lookups. They use the current operation as their parent but do not emit
    # GenAI attributes or metrics.
    with chat.span("cache.lookup", attributes={"cache.hit": False}) as cache_span:
        cache_span.set_attribute("cache.backend", "memory")

    # Completion details enrich the operation span with GenAI response
    # attributes and record token usage metrics. Content is copied to the span
    # because this operation opted in with `include_content=True`.
    chat.completion(
        response_model="mistral-large-latest",
        response_id="manual-chat-response",
        input_messages=[{"role": "user", "content": "Say hello in French"}],
        output_messages=[{"role": "assistant", "content": "Bonjour!"}],
        finish_reasons=["stop"],
        input_tokens=8,
        output_tokens=3,
    )

    # Evaluation results are log events correlated to the operation trace/span.
    chat.evaluation_result(
        "helpfulness",
        score_value=1.0,
        score_label="pass",
        explanation="Short and correct.",
    )

# Shutdown performs a final flush of the owned trace, metric, and log pipelines.
observability.shutdown()
