# type: ignore
import json
from typing import Any, Dict, Optional

try:
    from agents.tracing import (
        Span as OpenAISpan,
        ResponseSpanData as OpenAIResponseSpanData,
    )
except ImportError:
    OpenAISpan = Any
    OpenAIResponseSpanData = Any


def sgp_span_name(openai_span: "OpenAISpan") -> str:
    span_data = openai_span.span_data
    if span_data is None:
        return "Unnamed Span"
    default_name = str(type(span_data).__name__).replace("SpanData", "")

    return span_data.export().get("name", default_name)


def extract_response(openai_span: "OpenAISpan") -> Optional[Dict[str, Any]]:
    span_data = openai_span.span_data
    if not isinstance(span_data, OpenAIResponseSpanData):
        return None

    return {} if span_data.response is None else span_data.response.model_dump()


def parse_metadata(openai_span: "OpenAISpan") -> Dict[str, Any]:
    """Extracts and formats metadata from an OpenAI span."""
    if not openai_span.span_data:
        return {}

    excluded_fields = ("output", "input")
    exported_span_data: dict = openai_span.span_data.export()
    exported_span_data["openai_span_id"] = openai_span.span_id

    filtered_span_data: dict = {
        k: v for k, v in exported_span_data.items() if k not in excluded_fields
    }
    response = extract_response(openai_span)
    if response is not None:
        filtered_span_data["openai_response"] = response
    return {"openai_metadata": filtered_span_data}


def parse_input_output(openai_span: "OpenAISpan", key: str) -> Dict[str, Any]:
    """
    Safely extracts and parses input/output data from a span.
    The openai-agents SDK sometimes returns this data as a JSON string.
    """
    span_data = openai_span.span_data
    if not span_data:
        return {}
    exported_span_data: dict = span_data.export()
    value: Optional[Any] = exported_span_data.get(key)
    if value is None:
        return {}

    if isinstance(value, str):
        try:
            value = json.loads(value)
            if isinstance(value, dict):
                return value
        except (json.JSONDecodeError, TypeError):
            return {key: value}
    return {key: value}
