"""Operation structured-data transformation tests."""

import logging
from collections.abc import Callable, Generator, Mapping, Sequence
from contextlib import contextmanager
from typing import cast

import pytest
from conftest import SDKHarness, histogram_points, metrics_by_name, point_attributes

from mistralai.observability.otel import (
    OperationDataContext,
    OperationDataTransformer,
    OperationDataValue,
)
from mistralai.observability.otel import semconv_constants as c
from mistralai.observability.otel.attributes import normalize_otel_attribute


class ReplaceTextTransformer:
    """Recursively replace text to exercise the transformer contract."""

    def __init__(self, old: str, new: str) -> None:
        """Configure the text replacement."""
        self._old = old
        self._new = new

    def transform(
        self,
        value: OperationDataValue,
        *,
        context: OperationDataContext,
    ) -> OperationDataValue:
        """Replace matching text leaves while preserving structure."""
        del context
        return self._replace(value)

    def _replace(self, value: OperationDataValue) -> OperationDataValue:
        if isinstance(value, str):
            return value.replace(self._old, self._new)
        if isinstance(value, Mapping):
            return {key: self._replace(nested_value) for key, nested_value in value.items()}
        if isinstance(value, Sequence) and not isinstance(value, bytes):
            transformed = [self._replace(nested_value) for nested_value in value]
            return tuple(transformed) if isinstance(value, tuple) else transformed
        return value


class FieldTransformer:
    """Adapt a field-aware callback to the transformer contract for tests."""

    def __init__(self, callback: Callable[[str, OperationDataValue], OperationDataValue | None]) -> None:
        """Configure the field-aware callback."""
        self._callback = callback

    def transform(
        self,
        value: OperationDataValue,
        *,
        context: OperationDataContext,
    ) -> OperationDataValue | None:
        """Transform a value using its field name."""
        return self._callback(context.field, value)


class SelectiveFailureTransformer:
    """Fail on one sensitive field to verify fail-closed omission."""

    def transform(
        self,
        value: OperationDataValue,
        *,
        context: OperationDataContext,
    ) -> OperationDataValue | None:
        """Raise only for tool arguments."""
        if context.field == c.ATTR_GEN_AI_TOOL_CALL_ARGUMENTS:
            message = "transformation failed for sensitive-value"
            raise RuntimeError(message)
        return value


class DropNamesTransformer:
    """Drop names to exercise stable OTel fallbacks."""

    def transform(
        self,
        value: OperationDataValue,
        *,
        context: OperationDataContext,
    ) -> OperationDataValue | None:
        """Drop span and event names while preserving other fields."""
        if context.field in {"span.name", "event.name"}:
            return None
        return value


class InvalidOperationDataValue:
    """Invalid transformer output whose representation contains sensitive data."""

    def __repr__(self) -> str:
        """Return content that must never appear in normalization errors."""
        return "sensitive-value"


@contextmanager
def _configured_sdk(*transformers: OperationDataTransformer) -> Generator[SDKHarness]:
    harness = SDKHarness(operation_data_transformers=transformers)
    try:
        yield harness
    finally:
        harness.shutdown()


def test_span_values_are_transformed_before_recording() -> None:
    """Structured operation and child-span values should be transformed before OTel."""
    transformer = ReplaceTextTransformer("secret", "[TRANSFORMED]")
    with _configured_sdk(transformer) as harness:
        operation = harness.observability.operation("chat-secret", include_content=True)
        operation.system_instructions = {"content": "system-secret"}
        operation.tool_definitions = [{"name": "tool-secret"}]
        operation.tool_call_arguments = {"token": "argument-secret"}
        operation.tool_call_result = {"value": "result-secret"}
        operation.prompt_variables = {"customer": "variable-secret"}

        with operation:
            operation.completion(
                input_messages=[{"role": "user", "content": "input-secret"}],
                output_messages=[{"role": "assistant", "content": "output-secret"}],
            )
            with operation.span("child-secret", attributes={"custom.child": "child-secret"}):
                pass

        harness.observability.flush()
        spans = harness.span_exporter.get_finished_spans()
        operation_span = next(span for span in spans if span.name == "chat-[TRANSFORMED]")
        child_span = next(span for span in spans if span.name == "child-[TRANSFORMED]")
        operation_attributes = dict(operation_span.attributes or {})
        for key in (
            c.ATTR_GEN_AI_SYSTEM_INSTRUCTIONS,
            c.ATTR_GEN_AI_TOOL_DEFINITIONS,
            c.ATTR_GEN_AI_TOOL_CALL_ARGUMENTS,
            c.ATTR_GEN_AI_TOOL_CALL_RESULT,
            c.ATTR_GEN_AI_INPUT_MESSAGES,
            c.ATTR_GEN_AI_OUTPUT_MESSAGES,
            f"{c.ATTR_GEN_AI_PROMPT_VARIABLE}.customer",
        ):
            assert "secret" not in str(operation_attributes[key])
        assert "secret" not in str(dict(child_span.attributes or {}))


def test_structured_transformer_results_are_serialized_at_otel_boundaries() -> None:
    """Transformer output should always become valid OTel span and metric attributes."""

    def structure_custom_attributes(key: str, value: OperationDataValue) -> OperationDataValue:
        if key in {"custom.sequence", "custom.empty_list", "custom.empty_tuple"}:
            return value
        if key == "custom.nested":
            return [["nested"]]
        if key.startswith("custom."):
            return {"value": value}
        return value

    with _configured_sdk(FieldTransformer(structure_custom_attributes)) as harness:
        with harness.observability.operation(
            "chat",
            attributes={"custom.operation": "operation"},
        ) as operation:
            operation.set_attribute("custom.dynamic", "dynamic")
            operation.set_attribute("custom.sequence", ["first", "second"])
            operation.set_attribute("custom.empty_list", [])
            operation.set_attribute("custom.empty_tuple", ())
            operation.set_attribute("custom.nested", "nested")
            operation.token_usage(input_tokens=1, attributes={"custom.metric": "metric"})
            with operation.span("child", attributes={"custom.child": "child"}):
                pass

        harness.observability.flush()
        spans = {span.name: span for span in harness.span_exporter.get_finished_spans()}
        operation_attributes = dict(spans["chat"].attributes or {})
        child_attributes = dict(spans["child"].attributes or {})
        metrics = metrics_by_name(harness.metric_reader.get_metrics_data())
        token_point = histogram_points(metrics[c.METRIC_GEN_AI_CLIENT_TOKEN_USAGE])[0]

        assert operation_attributes["custom.operation"] == '{"value":"operation"}'
        assert operation_attributes["custom.dynamic"] == '{"value":"dynamic"}'
        assert operation_attributes["custom.sequence"] == ("first", "second")
        assert operation_attributes["custom.empty_list"] == ()
        assert operation_attributes["custom.empty_tuple"] == ()
        assert operation_attributes["custom.nested"] == '[["nested"]]'
        assert child_attributes["custom.child"] == '{"value":"child"}'
        assert point_attributes(token_point)["custom.metric"] == '{"value":"metric"}'


def test_invalid_transformed_value_error_does_not_include_value() -> None:
    """Invalid transformer output should report its type without exposing its value."""
    invalid_value = cast("OperationDataValue", InvalidOperationDataValue())

    with pytest.raises(TypeError, match="Unsupported operation data type: InvalidOperationDataValue") as error:
        normalize_otel_attribute(invalid_value)

    assert "sensitive-value" not in str(error.value)


def test_log_values_are_transformed_before_recording() -> None:
    """Log bodies, names, and attributes should be transformed before OTel."""
    transformer = ReplaceTextTransformer("secret", "[TRANSFORMED]")
    with _configured_sdk(transformer) as harness:
        with harness.observability.operation("chat") as operation:
            operation.log({"message": "log-secret"}, attributes={"custom": "attribute-secret"})
            operation.event("event-secret", {"message": "event-secret"})
            operation.inference_details(
                prompt="prompt-secret",
                completion="completion-secret",
            )
            operation.evaluation_result("quality", explanation="explanation-secret")

        harness.observability.flush()
        logs = harness.log_exporter.get_finished_logs()
        assert logs[1].log_record.event_name == "event-[TRANSFORMED]"
        for log in logs:
            assert "secret" not in str(log.log_record.body)
            assert "secret" not in str(dict(log.log_record.attributes or {}))


def test_transformers_compose_in_registration_order() -> None:
    """Configured transformers should run in registration order."""
    transformers = [
        ReplaceTextTransformer("secret", "first"),
        ReplaceTextTransformer("first", "second"),
    ]
    with _configured_sdk(*transformers) as harness:
        with harness.observability.operation("chat") as operation:
            operation.log("secret")

        harness.observability.flush()
        assert harness.log_exporter.get_finished_logs()[0].log_record.body == "second"


def test_transformer_failure_drops_only_the_sensitive_field(caplog: pytest.LogCaptureFixture) -> None:
    """A transformation error should omit its field without losing the span."""
    with (
        caplog.at_level(logging.DEBUG, logger="mistralai.observability.otel.hooks"),
        _configured_sdk(SelectiveFailureTransformer()) as harness,
    ):
        with harness.observability.tool(
            "lookup",
            arguments={"token": "secret"},
            result={"status": "ok"},
        ):
            pass

        harness.observability.flush()
        span_attributes = dict(harness.span_exporter.get_finished_spans()[0].attributes or {})
        assert c.ATTR_GEN_AI_TOOL_CALL_ARGUMENTS not in span_attributes
        assert c.ATTR_GEN_AI_TOOL_CALL_RESULT in span_attributes

    diagnostic = caplog.records[-1].getMessage()
    assert "SelectiveFailureTransformer" in diagnostic
    assert "span" in diagnostic
    assert c.ATTR_GEN_AI_TOOL_CALL_ARGUMENTS in diagnostic
    assert "RuntimeError" in diagnostic
    assert "secret" not in diagnostic
    assert "sensitive-value" not in caplog.text


def test_exception_content_is_transformed_before_recording() -> None:
    """Exception event and status content should never bypass transformation."""
    transformer = ReplaceTextTransformer("secret", "[TRANSFORMED]")
    with _configured_sdk(transformer) as harness:
        with pytest.raises(RuntimeError, match="secret"), harness.observability.operation("chat"):
            message = "request-secret"
            raise RuntimeError(message)

        harness.observability.flush()
        span = harness.span_exporter.get_finished_spans()[0]
        assert span.status.description == "request-[TRANSFORMED]"
        assert len(span.events) == 1
        event_attributes = dict(span.events[0].attributes or {})
        assert "secret" not in str(event_attributes[c.ATTR_EXCEPTION_MESSAGE])
        assert "secret" not in str(event_attributes[c.ATTR_EXCEPTION_STACKTRACE])


@pytest.mark.parametrize(
    ("transformed", "description"),
    [
        ("[TRANSFORMED]", "[TRANSFORMED]"),
        (None, None),
        (123, None),
        ({"redacted": True}, None),
    ],
    ids=["text", "dropped", "number", "mapping"],
)
def test_payload_error_description_uses_status_transformer(
    transformed: OperationDataValue, description: str | None
) -> None:
    """Only string status.description output reaches a returned failure's status."""
    transformer = FieldTransformer(lambda field, value: transformed if field == "status.description" else value)
    with _configured_sdk(transformer) as harness:
        operation = harness.observability.tool("lookup")
        operation.start(set_current_context=False)
        operation.end(error_type="rejected", error_message="sensitive failure")

        harness.observability.flush()
        [span] = harness.span_exporter.get_finished_spans()
        assert span.status.status_code.name == "ERROR"
        assert span.status.description == description
        assert dict(span.attributes or {})[c.ATTR_ERROR_TYPE] == "rejected"
        assert not span.events


def test_dropped_names_use_stable_fallbacks() -> None:
    """Invalid transformed names should use documented internal fallbacks."""
    with _configured_sdk(DropNamesTransformer()) as harness:
        with harness.observability.operation("chat") as operation:
            with operation.span("child"):
                pass
            operation.event("named-event")

        harness.observability.flush()
        spans = harness.span_exporter.get_finished_spans()
        logs = harness.log_exporter.get_finished_logs()

        assert {span.name for span in spans} == {
            c.FALLBACK_OPERATION_SPAN_NAME,
            c.FALLBACK_CHILD_SPAN_NAME,
        }
        assert logs[0].log_record.event_name == c.FALLBACK_OPERATION_EVENT_NAME


def test_user_structured_attribute_override_is_transformed_once() -> None:
    """A user override should replace generated content before transformation."""
    transformed_fields: list[str] = []

    def track_transformations(key: str, value: OperationDataValue) -> OperationDataValue:
        if key == c.ATTR_GEN_AI_SYSTEM_INSTRUCTIONS:
            transformed_fields.append(key)
            return f"transformed:{value}"
        return value

    with _configured_sdk(FieldTransformer(track_transformations)) as harness:
        with harness.observability.create_agent(
            system_instructions="generated",
            attributes={c.ATTR_GEN_AI_SYSTEM_INSTRUCTIONS: "override"},
        ):
            pass

        harness.observability.flush()
        span_attributes = dict(harness.span_exporter.get_finished_spans()[0].attributes or {})

        assert transformed_fields == [c.ATTR_GEN_AI_SYSTEM_INSTRUCTIONS]
        assert span_attributes[c.ATTR_GEN_AI_SYSTEM_INSTRUCTIONS] == "transformed:override"


@pytest.mark.parametrize("recorded", ["at_start", "after_start"])
@pytest.mark.parametrize(
    ("override", "expected"),
    [
        (None, 'transformed:{"value":"result"}'),
        ("override", "transformed:override"),
    ],
)
def test_tool_call_result_is_transformed_once(recorded: str, override: str | None, expected: str) -> None:
    """Tool results set at start or via `tool_result` share one transformation path."""
    transformed_fields: list[str] = []

    def track_transformations(key: str, value: OperationDataValue) -> OperationDataValue:
        # `start()` also offers an absent result (`None`) to transformers; only count real values.
        if key == c.ATTR_GEN_AI_TOOL_CALL_RESULT and value is not None:
            transformed_fields.append(key)
            return f"transformed:{normalize_otel_attribute(value, structured_document=True)}"
        return value

    result = {"value": "result"}
    attributes = None if override is None else {c.ATTR_GEN_AI_TOOL_CALL_RESULT: override}
    with _configured_sdk(FieldTransformer(track_transformations)) as harness:
        if recorded == "at_start":
            with harness.observability.tool("lookup", result=result, attributes=attributes):
                pass
        else:
            with harness.observability.tool("lookup") as operation:
                operation.tool_result(result, attributes=attributes)

        harness.observability.flush()
        span_attributes = dict(harness.span_exporter.get_finished_spans()[0].attributes or {})

        assert transformed_fields == [c.ATTR_GEN_AI_TOOL_CALL_RESULT]
        assert span_attributes[c.ATTR_GEN_AI_TOOL_CALL_RESULT] == expected
