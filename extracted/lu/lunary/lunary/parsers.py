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
  # Additional params
  "extra_headers",
  "extra_query", 
  "extra_body",
  "timeout"
]

def filter_params(params: Dict[str, Any]) -> Dict[str, Any]:
    filtered_params = {
        key: serialize_param_value(value)
        for key, value in params.items()
        if key in PARAMS_TO_CAPTURE
    }
    return filtered_params


def serialize_param_value(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value

    if isinstance(value, list):
        return [serialize_param_value(item) for item in value]

    if isinstance(value, tuple):
        return [serialize_param_value(item) for item in value]

    if isinstance(value, dict):
        return {
            key: serialize_param_value(item)
            for key, item in value.items()
            if item is not None
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

    if hasattr(value, "__dict__"):
        return serialize_param_value(
            {
                key: item
                for key, item in vars(value).items()
                if not key.startswith("_") and item is not None
            }
        )

    return value
