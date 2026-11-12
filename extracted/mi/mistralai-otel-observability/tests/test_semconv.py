"""Semantic convention mapping tests."""

import json

from conftest import SDKHarness, histogram_points, metrics_by_name, point_attributes
from opentelemetry.trace import SpanKind

from mistralai.observability.otel import Operation
from mistralai.observability.otel import semconv_constants as c


def test_explicit_operation_model_exposes_advanced_semconv_fields(harness: SDKHarness) -> None:
    """Advanced Operation fields should map to GenAI span attributes."""
    operation = Operation(
        name="chat",
        request_model="mistral-large-latest",
        request_max_tokens=128,
        request_stream=True,
        response_model="mistral-large-2026-06",
        response_id="resp_123",
        response_time_to_first_chunk=0.12,
        cache_read_input_tokens=3,
        output_type="text",
        conversation_id="conv_123",
        conversation_compacted=True,
        prompt_variables={"language": "French"},
        system_instructions=[{"type": "text", "content": "Be concise."}],
        tool_definitions=[{"type": "function", "name": "lookup"}],
        server_address="api.mistral.ai",
        server_port=443,
    )
    operation.start()
    operation.end()

    harness.observability.flush()
    span = harness.span_exporter.get_finished_spans()[0]
    span_attributes = dict(span.attributes or {})
    assert span_attributes[c.ATTR_GEN_AI_REQUEST_MODEL] == "mistral-large-latest"
    assert span_attributes[c.ATTR_GEN_AI_REQUEST_MAX_TOKENS] == 128
    assert span_attributes[c.ATTR_GEN_AI_REQUEST_STREAM] is True
    assert span_attributes[c.ATTR_GEN_AI_RESPONSE_MODEL] == "mistral-large-2026-06"
    assert span_attributes[c.ATTR_GEN_AI_RESPONSE_ID] == "resp_123"
    assert span_attributes[c.ATTR_GEN_AI_RESPONSE_TIME_TO_FIRST_CHUNK] == 0.12
    assert span_attributes[c.ATTR_GEN_AI_USAGE_CACHE_READ_INPUT_TOKENS] == 3
    assert span_attributes[c.ATTR_GEN_AI_OUTPUT_TYPE] == "text"
    assert span_attributes[c.ATTR_GEN_AI_CONVERSATION_ID] == "conv_123"
    assert span_attributes[c.ATTR_GEN_AI_CONVERSATION_COMPACTED] is True
    assert span_attributes[f"{c.ATTR_GEN_AI_PROMPT_VARIABLE}.language"] == "French"
    assert json.loads(str(span_attributes[c.ATTR_GEN_AI_SYSTEM_INSTRUCTIONS])) == [
        {"type": "text", "content": "Be concise."}
    ]
    assert json.loads(str(span_attributes[c.ATTR_GEN_AI_TOOL_DEFINITIONS])) == [{"type": "function", "name": "lookup"}]
    assert span_attributes["server.address"] == "api.mistral.ai"
    assert span_attributes["server.port"] == 443


def test_agent_tool_and_plan_helpers_record_semconv_spans_and_metrics(harness: SDKHarness) -> None:
    """Agent, tool, and plan helpers should emit semconv spans and metrics."""
    with harness.observability.agent(
        "Support Agent",
        agent_id="agent_123",
        description="Answers support questions",
        version="2026-07-07",
        model="mistral-large",
        provider=c.PROVIDER_NAME_MISTRAL_AI,
    ) as agent:
        with harness.observability.plan("Support Agent", parent=agent):
            pass

        with harness.observability.tool(
            "lookup_customer",
            parent=agent,
            call_id="call_123",
            description="Lookup customer metadata",
            tool_type=c.TOOL_TYPE_FUNCTION,
            arguments={"customer_id": "cus_123"},
            result={"tier": "enterprise"},
            agent_name="Support Agent",
        ):
            pass

    harness.observability.flush()

    spans_by_name = {span.name: span for span in harness.span_exporter.get_finished_spans()}
    agent_span = spans_by_name["invoke_agent Support Agent"]
    plan_span = spans_by_name["plan Support Agent"]
    tool_span = spans_by_name["execute_tool lookup_customer"]
    assert agent_span.kind is SpanKind.INTERNAL
    assert plan_span.kind is SpanKind.INTERNAL
    assert tool_span.kind is SpanKind.INTERNAL

    agent_attributes = dict(agent_span.attributes or {})
    assert agent_attributes[c.ATTR_GEN_AI_OPERATION_NAME] == c.OPERATION_NAME_INVOKE_AGENT
    assert agent_attributes[c.ATTR_GEN_AI_AGENT_ID] == "agent_123"
    assert agent_attributes[c.ATTR_GEN_AI_AGENT_NAME] == "Support Agent"
    assert agent_attributes[c.ATTR_GEN_AI_AGENT_DESCRIPTION] == "Answers support questions"
    assert agent_attributes[c.ATTR_GEN_AI_AGENT_VERSION] == "2026-07-07"
    assert agent_attributes[c.ATTR_GEN_AI_PROVIDER_NAME] == c.PROVIDER_NAME_MISTRAL_AI
    assert agent_attributes[c.ATTR_GEN_AI_REQUEST_MODEL] == "mistral-large"

    plan_attributes = dict(plan_span.attributes or {})
    assert plan_span.parent is not None
    assert agent_span.context is not None
    assert plan_span.parent.span_id == agent_span.context.span_id
    assert plan_attributes[c.ATTR_GEN_AI_OPERATION_NAME] == c.OPERATION_NAME_PLAN
    assert plan_attributes[c.ATTR_GEN_AI_AGENT_NAME] == "Support Agent"

    tool_attributes = dict(tool_span.attributes or {})
    assert tool_span.parent is not None
    assert tool_span.parent.span_id == agent_span.context.span_id
    assert tool_attributes[c.ATTR_GEN_AI_OPERATION_NAME] == c.OPERATION_NAME_EXECUTE_TOOL
    assert tool_attributes[c.ATTR_GEN_AI_TOOL_NAME] == "lookup_customer"
    assert tool_attributes[c.ATTR_GEN_AI_TOOL_CALL_ID] == "call_123"
    assert tool_attributes[c.ATTR_GEN_AI_TOOL_DESCRIPTION] == "Lookup customer metadata"
    assert tool_attributes[c.ATTR_GEN_AI_TOOL_TYPE] == c.TOOL_TYPE_FUNCTION
    assert tool_attributes[c.ATTR_GEN_AI_AGENT_NAME] == "Support Agent"
    assert json.loads(str(tool_attributes[c.ATTR_GEN_AI_TOOL_CALL_ARGUMENTS])) == {"customer_id": "cus_123"}
    assert json.loads(str(tool_attributes[c.ATTR_GEN_AI_TOOL_CALL_RESULT])) == {"tier": "enterprise"}

    collected_metrics = metrics_by_name(harness.metric_reader.get_metrics_data())
    assert c.METRIC_GEN_AI_INVOKE_AGENT_DURATION in collected_metrics
    assert c.METRIC_GEN_AI_EXECUTE_TOOL_DURATION in collected_metrics
    assert c.METRIC_GEN_AI_CLIENT_OPERATION_DURATION not in collected_metrics
    assert len(histogram_points(collected_metrics[c.METRIC_GEN_AI_INVOKE_AGENT_DURATION])) == 1
    assert len(histogram_points(collected_metrics[c.METRIC_GEN_AI_EXECUTE_TOOL_DURATION])) == 1


def test_create_agent_helper_records_client_agent_creation_span(harness: SDKHarness) -> None:
    """Create-agent helper should emit a client span and duration metric."""
    with harness.observability.create_agent(
        "Support Agent",
        agent_id="agent_123",
        model="mistral-large",
        provider=c.PROVIDER_NAME_MISTRAL_AI,
        system_instructions=[{"type": "text", "content": "Be helpful."}],
        server_address="api.mistral.ai",
        server_port=443,
    ):
        pass

    harness.observability.flush()
    span = harness.span_exporter.get_finished_spans()[0]
    span_attributes = dict(span.attributes or {})
    assert span.name == "create_agent Support Agent"
    assert span.kind is SpanKind.CLIENT
    assert span_attributes[c.ATTR_GEN_AI_OPERATION_NAME] == c.OPERATION_NAME_CREATE_AGENT
    assert span_attributes[c.ATTR_GEN_AI_AGENT_ID] == "agent_123"
    assert span_attributes[c.ATTR_GEN_AI_AGENT_NAME] == "Support Agent"
    assert json.loads(str(span_attributes[c.ATTR_GEN_AI_SYSTEM_INSTRUCTIONS])) == [
        {"type": "text", "content": "Be helpful."}
    ]
    collected_metrics = metrics_by_name(harness.metric_reader.get_metrics_data())
    duration_point = histogram_points(collected_metrics[c.METRIC_GEN_AI_CLIENT_OPERATION_DURATION])[0]
    duration_attributes = point_attributes(duration_point)
    assert duration_attributes[c.ATTR_GEN_AI_OPERATION_NAME] == c.OPERATION_NAME_CREATE_AGENT
    assert duration_attributes[c.ATTR_SERVER_ADDRESS] == "api.mistral.ai"
    assert duration_attributes[c.ATTR_SERVER_PORT] == 443


def test_tool_span_keeps_non_ascii_arguments_and_result_readable(harness: SDKHarness) -> None:
    """Structured tool data should store non-ASCII text as is, not as ``\\uXXXX`` escapes."""
    with harness.observability.tool(
        "search_station",
        arguments={"query": "서울역", "note": "café"},
        result={"name": "東京駅"},
    ):
        pass

    harness.observability.flush()

    (tool_span,) = harness.span_exporter.get_finished_spans()
    tool_attributes = dict(tool_span.attributes or {})
    assert tool_attributes[c.ATTR_GEN_AI_TOOL_CALL_ARGUMENTS] == '{"note":"café","query":"서울역"}'
    assert tool_attributes[c.ATTR_GEN_AI_TOOL_CALL_RESULT] == '{"name":"東京駅"}'


def test_tool_span_drops_lone_surrogates_so_the_span_still_exports(harness: SDKHarness) -> None:
    """A truncated emoji must not leave a lone surrogate that UTF-8 cannot encode."""
    with harness.observability.tool("lookup", arguments={"query\ud83d": "역 \ud83d"}):
        pass

    harness.observability.flush()

    (tool_span,) = harness.span_exporter.get_finished_spans()
    arguments = str(dict(tool_span.attributes or {})[c.ATTR_GEN_AI_TOOL_CALL_ARGUMENTS])
    assert arguments == '{"query":"역 "}'
    arguments.encode()
