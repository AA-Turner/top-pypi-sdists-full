"""Completion adapter tests."""

import json

from conftest import FakeChatCompletionAdapter, SDKHarness, histogram_points, metrics_by_name, point_attributes
from mistralai.client.models.assistantmessage import AssistantMessage
from mistralai.client.models.chatcompletionchoice import ChatCompletionChoice
from mistralai.client.models.chatcompletionresponse import ChatCompletionResponse
from mistralai.client.models.usageinfo import UsageInfo

from mistralai.observability.otel import ChatCompletionDetails
from mistralai.observability.otel import semconv_constants as c


def test_operation_records_mistral_completion(harness: SDKHarness) -> None:
    """Mistral completion helper should enrich spans and token metrics."""
    with harness.observability.operation(
        "chat",
        provider="mistral",
        model="mistral-small",
        include_content=True,
    ) as operation:
        operation.mistral_completion(
            ChatCompletionResponse(
                id="cmpl_123",
                object="chat.completion",
                model="mistral-small-2409",
                usage=UsageInfo(prompt_tokens=4, completion_tokens=2),
                created=0,
                choices=[
                    ChatCompletionChoice(
                        index=0,
                        finish_reason="stop",
                        message=AssistantMessage(content="bonjour"),
                    )
                ],
            ),
            messages=[{"role": "user", "content": "hello"}],
        )

    harness.observability.flush()

    assert harness.log_exporter.get_finished_logs() == ()
    span = harness.span_exporter.get_finished_spans()[0]
    span_attributes = dict(span.attributes or {})
    assert span_attributes[c.ATTR_GEN_AI_RESPONSE_MODEL] == "mistral-small-2409"
    assert span_attributes[c.ATTR_GEN_AI_RESPONSE_ID] == "cmpl_123"
    assert span_attributes[c.ATTR_GEN_AI_RESPONSE_FINISH_REASONS] == ("stop",)
    assert span_attributes[c.ATTR_GEN_AI_USAGE_INPUT_TOKENS] == 4
    assert span_attributes[c.ATTR_GEN_AI_USAGE_OUTPUT_TOKENS] == 2
    assert json.loads(str(span_attributes[c.ATTR_GEN_AI_INPUT_MESSAGES])) == [
        {"role": "user", "parts": [{"type": "text", "content": "hello"}]}
    ]
    assert json.loads(str(span_attributes[c.ATTR_GEN_AI_OUTPUT_MESSAGES])) == [
        {
            "role": "assistant",
            "parts": [{"type": "text", "content": "bonjour"}],
            "finish_reason": "stop",
            "mistral.index": 0,
        }
    ]
    collected_metrics = metrics_by_name(harness.metric_reader.get_metrics_data())
    token_points = histogram_points(collected_metrics[c.METRIC_GEN_AI_CLIENT_TOKEN_USAGE])
    assert {point_attributes(point)[c.ATTR_GEN_AI_TOKEN_TYPE]: point.sum for point in token_points} == {
        c.TOKEN_TYPE_INPUT: 4,
        c.TOKEN_TYPE_OUTPUT: 2,
    }
    assert c.METRIC_GEN_AI_CLIENT_OPERATION_DURATION in collected_metrics
    duration_point = histogram_points(collected_metrics[c.METRIC_GEN_AI_CLIENT_OPERATION_DURATION])[0]
    duration_attributes = point_attributes(duration_point)
    assert duration_attributes[c.ATTR_GEN_AI_RESPONSE_MODEL] == "mistral-small-2409"


def test_operation_records_generic_completion_adapter(harness: SDKHarness) -> None:
    """Generic completion adapters should enrich spans and token metrics."""
    with harness.observability.operation(
        "chat",
        provider="test-provider",
        model="request-model",
        include_content=True,
    ) as operation:
        harness.observability.record_completion(operation, FakeChatCompletionAdapter())

    harness.observability.flush()

    assert harness.log_exporter.get_finished_logs() == ()
    span = harness.span_exporter.get_finished_spans()[0]
    span_attributes = dict(span.attributes or {})
    assert span_attributes[c.ATTR_GEN_AI_RESPONSE_MODEL] == "response-model"
    assert span_attributes[c.ATTR_GEN_AI_RESPONSE_ID] == "resp_123"
    assert span_attributes[c.ATTR_GEN_AI_RESPONSE_FINISH_REASONS] == ("stop",)
    assert span_attributes[c.ATTR_GEN_AI_USAGE_INPUT_TOKENS] == 8
    assert span_attributes[c.ATTR_GEN_AI_USAGE_OUTPUT_TOKENS] == 3
    assert json.loads(str(span_attributes[c.ATTR_GEN_AI_INPUT_MESSAGES])) == [{"role": "user", "content": "hello"}]
    assert json.loads(str(span_attributes[c.ATTR_GEN_AI_OUTPUT_MESSAGES])) == [
        {"role": "assistant", "content": "bonjour"}
    ]
    collected_metrics = metrics_by_name(harness.metric_reader.get_metrics_data())
    token_points = histogram_points(collected_metrics[c.METRIC_GEN_AI_CLIENT_TOKEN_USAGE])
    assert {point_attributes(point)[c.ATTR_GEN_AI_TOKEN_TYPE]: point.sum for point in token_points} == {
        c.TOKEN_TYPE_INPUT: 8,
        c.TOKEN_TYPE_OUTPUT: 3,
    }


def test_sdk_records_completion_details_payload(harness: SDKHarness) -> None:
    """Raw completion details should conform to the low-level adapter contract."""
    with harness.observability.operation(
        "chat",
        provider="test-provider",
        model="request-model",
    ) as operation:
        harness.observability.record_completion(
            operation,
            ChatCompletionDetails(
                response_model="response-model",
                response_id="resp_123",
                finish_reasons=["stop"],
                input_tokens=8,
                output_tokens=3,
            ),
        )

    harness.observability.flush()

    span = harness.span_exporter.get_finished_spans()[0]
    span_attributes = dict(span.attributes or {})
    assert span_attributes[c.ATTR_GEN_AI_RESPONSE_MODEL] == "response-model"
    assert span_attributes[c.ATTR_GEN_AI_RESPONSE_ID] == "resp_123"
    assert span_attributes[c.ATTR_GEN_AI_RESPONSE_FINISH_REASONS] == ("stop",)
    collected_metrics = metrics_by_name(harness.metric_reader.get_metrics_data())
    token_points = histogram_points(collected_metrics[c.METRIC_GEN_AI_CLIENT_TOKEN_USAGE])
    assert {point_attributes(point)[c.ATTR_GEN_AI_TOKEN_TYPE]: point.sum for point in token_points} == {
        c.TOKEN_TYPE_INPUT: 8,
        c.TOKEN_TYPE_OUTPUT: 3,
    }


def test_operation_records_completion_details(harness: SDKHarness) -> None:
    """Manual completion details should enrich spans and token metrics."""
    with harness.observability.operation(
        "chat",
        provider="test-provider",
        model="request-model",
        include_content=True,
    ) as operation:
        operation.completion(
            response_model="response-model",
            response_id="resp_123",
            input_messages=[{"role": "user", "parts": [{"type": "text", "content": "hello"}]}],
            output_messages=[{"role": "assistant", "parts": [{"type": "text", "content": "bonjour"}]}],
            finish_reasons=["stop"],
            input_tokens=8,
            output_tokens=3,
        )

    harness.observability.flush()

    assert harness.log_exporter.get_finished_logs() == ()
    span = harness.span_exporter.get_finished_spans()[0]
    span_attributes = dict(span.attributes or {})
    assert span_attributes[c.ATTR_GEN_AI_RESPONSE_MODEL] == "response-model"
    assert span_attributes[c.ATTR_GEN_AI_RESPONSE_ID] == "resp_123"
    assert span_attributes[c.ATTR_GEN_AI_RESPONSE_FINISH_REASONS] == ("stop",)
    assert span_attributes[c.ATTR_GEN_AI_USAGE_INPUT_TOKENS] == 8
    assert span_attributes[c.ATTR_GEN_AI_USAGE_OUTPUT_TOKENS] == 3
    assert json.loads(str(span_attributes[c.ATTR_GEN_AI_INPUT_MESSAGES])) == [
        {"role": "user", "parts": [{"type": "text", "content": "hello"}]}
    ]
    assert json.loads(str(span_attributes[c.ATTR_GEN_AI_OUTPUT_MESSAGES])) == [
        {"role": "assistant", "parts": [{"type": "text", "content": "bonjour"}]}
    ]
    collected_metrics = metrics_by_name(harness.metric_reader.get_metrics_data())
    token_points = histogram_points(collected_metrics[c.METRIC_GEN_AI_CLIENT_TOKEN_USAGE])
    assert {point_attributes(point)[c.ATTR_GEN_AI_TOKEN_TYPE]: point.sum for point in token_points} == {
        c.TOKEN_TYPE_INPUT: 8,
        c.TOKEN_TYPE_OUTPUT: 3,
    }
