from collections.abc import Iterable, Iterator, Mapping
from typing import Any, Dict
import jsonpickle
from pydantic import BaseModel, Field



def default_input_parser(*args, **kwargs):
    def serialize(args, kwargs):
        if not args and not kwargs:
            return None

        if len(args) == 1 and not kwargs:
            return args[0]

        input = list(args)
        if kwargs:
            input.append(kwargs)

        return input

    return {"input": serialize(args, kwargs)}

def method_input_parser(*args, **kwargs):
    def serialize(args, kwargs):
        args = args[1:]

        if not args and not kwargs:
            return None

        if len(args) == 1 and not kwargs:
            return args[0]

        input_list = list(args)
        if kwargs:
            input_list.append(kwargs)

        return input_list

    return {"input": serialize(args, kwargs)}


def default_output_parser(output, *args, **kwargs):
    return {"output": getattr(output, "content", output), "tokensUsage": None}

class PydanticHandler(jsonpickle.handlers.BaseHandler):
    def flatten(self, obj, data):
        """Convert Pydantic model to a JSON-friendly dict using model_dump_json()"""
        return jsonpickle.loads(obj.model_dump_json(), safe=True)

PARAMS_TO_CAPTURE = [
  "cache_control",
  "container",
  "context_management",
  "betas",
  "frequency_penalty",
  "function_call", 
  "functions",
  "inference_geo",
  "logit_bias",
  "logprobs",
  "max_tokens",
  "max_completion_tokens",
  "mcp_servers",
  "n",
  "output_config",
  "output_format",
  "presence_penalty", 
  "response_format",
  "seed",
  "service_tier",
  "speed",
  "stop",
  "stop_sequences",
  "stream",
  "audio",
  "modalities",
  "temperature",
  "thinking",
  "tool_choice",
  "tools",
  "tool_calls",
  "top_p",
  "top_k",
  "top_logprobs",
  "prediction",
  "service_tier",
  "parallel_tool_calls",
  "reasoning_effort",
  "verbosity",
  "stream_options",
  "store",
  "user",
  "safety_identifier",
  "prompt_cache_key",
  "prompt_cache_retention",
  # Additional params
  "extra_headers",
  "extraHeaders",
  "extra_query", 
  "extra_body",
  "timeout"
]

REDACTED_HEADER_VALUE = "[REDACTED]"
EXTRA_HEADERS_KEYS = {"extra_headers", "extraHeaders"}
EXTRA_BODY_KEYS = {"extra_body", "extraBody"}
JSON_SCHEMA_NAME_MAP_KEYS = {
    "$defs",
    "definitions",
    "dependencies",
    "dependentRequired",
    "dependentSchemas",
    "patternProperties",
    "properties",
}


def is_openai_omitted(value: Any) -> bool:
    """Recognize OpenAI omission sentinels without importing the SDK."""
    value_type = type(value)
    return (
        value_type.__module__.split(".")[0] == "openai"
        and value_type.__name__ in {"NotGiven", "Omit"}
    )


def unavailable_iterable_snapshot(value: Any) -> Dict[str, str]:
    """Describe an iterable without consuming the provider-owned object."""
    value_type = type(value)
    reason = getattr(value, "_lunary_capture_unavailable_reason", None)
    return {
        "type": "capture_unavailable",
        "reason": (
            reason
            or (
                "one_shot_iterable"
                if isinstance(value, Iterator)
                else "non_materialized_iterable"
            )
        ),
        "value_type": f"{value_type.__module__}.{value_type.__name__}",
    }


def redact_extra_headers(
    value: Any, *, _schema_name_map: bool = False, _depth: int = 0
) -> Any:
    """Redact transport headers while keeping root provider bodies opaque."""
    if isinstance(value, Mapping):
        redacted = {}
        for key, item in value.items():
            if key in EXTRA_HEADERS_KEYS and not _schema_name_map:
                redacted[key] = (
                    {
                        header_name: REDACTED_HEADER_VALUE
                        for header_name in item
                    }
                    if isinstance(item, Mapping)
                    else REDACTED_HEADER_VALUE
                )
            elif (
                key in EXTRA_BODY_KEYS
                and _depth == 0
                and not _schema_name_map
            ):
                redacted[key] = serialize_param_value(item)
            else:
                redacted[key] = redact_extra_headers(
                    item,
                    _schema_name_map=key in JSON_SCHEMA_NAME_MAP_KEYS,
                    _depth=_depth + 1,
                )
        return redacted

    if isinstance(value, (list, tuple)):
        return [
            redact_extra_headers(item, _depth=_depth + 1)
            for item in value
        ]

    return value


def filter_params(params: Dict[str, Any]) -> Dict[str, Any]:
    redacted_params = redact_extra_headers(params)
    filtered_params = {
        key: serialize_param_value(value)
        for key, value in redacted_params.items()
        if key in PARAMS_TO_CAPTURE and not is_openai_omitted(value)
    }
    return redact_extra_headers(filtered_params)


def serialize_param_value(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value

    if isinstance(value, list):
        return [
            serialize_param_value(item)
            for item in value
            if not is_openai_omitted(item)
        ]

    if isinstance(value, tuple):
        return [
            serialize_param_value(item)
            for item in value
            if not is_openai_omitted(item)
        ]

    if isinstance(value, dict):
        return {
            key: serialize_param_value(item)
            for key, item in value.items()
            if not is_openai_omitted(item)
        }

    if isinstance(value, type):
        if issubclass(value, BaseModel):
            return {
                "type": "pydantic_model",
                "class_name": value.__name__,
                "schema": serialize_param_value(value.model_json_schema()),
            }

        return value.__name__

    if isinstance(value, BaseModel):
        return serialize_param_value(jsonpickle.loads(value.model_dump_json(), safe=True))

    if hasattr(value, "model_dump"):
        try:
            return serialize_param_value(value.model_dump(exclude_none=True))
        except TypeError:
            return serialize_param_value(value.model_dump())

    if hasattr(value, "model_dump_json"):
        try:
            return serialize_param_value(
                jsonpickle.loads(value.model_dump_json(exclude_none=True), safe=True)
            )
        except TypeError:
            return serialize_param_value(
                jsonpickle.loads(value.model_dump_json(), safe=True)
            )

    if hasattr(value, "dict"):
        return serialize_param_value(value.dict())

    if isinstance(value, Iterable):
        return unavailable_iterable_snapshot(value)

    if hasattr(value, "__dict__"):
        return serialize_param_value(
            {
                key: item
                for key, item in vars(value).items()
                if not key.startswith("_") and item is not None
            }
        )

    return value
