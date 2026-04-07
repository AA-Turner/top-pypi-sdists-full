import json
import logging

logger = logging.getLogger(__name__)

KWARGS_TO_CAPTURE = [
    "cache_control",
    "container",
    "inference_geo",
    "max_tokens",
    "metadata",
    "output_config",
    "service_tier",
    "stop_sequences",
    "stream",
    "system",
    "temperature",
    "thinking",
    "tool_choice",
    "tools",
    "top_k",
    "top_p",
]

USAGE_METADATA_KEYS = {
    "cache_creation_input_tokens": "cacheCreationInputTokens",
    "cache_read_input_tokens": "cacheReadInputTokens",
    "inference_geo": "inferenceGeo",
    "service_tier": "serviceTier",
}


class AnthropicUtils:
    @staticmethod
    def get_property(obj, key, default=None):
        if isinstance(obj, dict):
            return obj.get(key, default)
        return getattr(obj, key, default)

    @staticmethod
    def serialize_value(value):
        if value is None or isinstance(value, (str, int, float, bool)):
            return value

        if isinstance(value, list):
            return [AnthropicUtils.serialize_value(item) for item in value]

        if isinstance(value, tuple):
            return [AnthropicUtils.serialize_value(item) for item in value]

        if isinstance(value, dict):
            return {
                key: AnthropicUtils.serialize_value(item)
                for key, item in value.items()
                if item is not None
            }

        if hasattr(value, "model_dump"):
            try:
                dumped = value.model_dump(exclude_none=True)
            except TypeError:
                dumped = value.model_dump()
            return AnthropicUtils.serialize_value(dumped)

        if hasattr(value, "model_dump_json"):
            try:
                return AnthropicUtils.serialize_value(
                    json.loads(value.model_dump_json(exclude_none=True))
                )
            except TypeError:
                return AnthropicUtils.serialize_value(json.loads(value.model_dump_json()))
            except Exception:
                logger.exception("Error serializing Anthropic value via model_dump_json")

        if hasattr(value, "dict"):
            try:
                return AnthropicUtils.serialize_value(value.dict())
            except Exception:
                logger.exception("Error serializing Anthropic value via dict()")

        if hasattr(value, "__dict__"):
            return AnthropicUtils.serialize_value(
                {
                    key: item
                    for key, item in vars(value).items()
                    if not key.startswith("_") and item is not None
                }
            )

        return value

    @staticmethod
    def normalize_content(content):
        if isinstance(content, str) or content is None:
            return content
        return AnthropicUtils.serialize_value(content)

    @staticmethod
    def parse_usage(usage):
        if usage is None:
            return None

        tokens_usage = {}

        prompt_tokens = AnthropicUtils.get_property(usage, "input_tokens")
        completion_tokens = AnthropicUtils.get_property(usage, "output_tokens")
        cache_creation_input_tokens = AnthropicUtils.get_property(
            usage, "cache_creation_input_tokens"
        )
        cache_read_input_tokens = AnthropicUtils.get_property(
            usage, "cache_read_input_tokens"
        )

        if prompt_tokens is not None:
            tokens_usage["prompt"] = prompt_tokens

        if completion_tokens is not None:
            tokens_usage["completion"] = completion_tokens

        if (
            cache_creation_input_tokens is not None
            or cache_read_input_tokens is not None
        ):
            tokens_usage["promptCached"] = (
                cache_creation_input_tokens or 0
            ) + (cache_read_input_tokens or 0)

        return tokens_usage or None

    @staticmethod
    def build_metadata(message):
        metadata = {}

        for key, target_key in {
            "id": "messageId",
            "model": "model",
            "stop_reason": "stopReason",
            "stop_sequence": "stopSequence",
        }.items():
            value = AnthropicUtils.get_property(message, key)
            if value is not None:
                metadata[target_key] = value

        usage = AnthropicUtils.get_property(message, "usage")
        if usage is not None:
            for key, target_key in USAGE_METADATA_KEYS.items():
                value = AnthropicUtils.get_property(usage, key)
                if value is not None:
                    metadata[target_key] = value

        return metadata or None

    @staticmethod
    def parse_message(message):
        parsed_message = {
            "role": AnthropicUtils.get_property(message, "role"),
            "content": AnthropicUtils.normalize_content(
                AnthropicUtils.get_property(message, "content")
            ),
        }

        refusal = AnthropicUtils.get_property(message, "refusal")
        if refusal is not None:
            parsed_message["refusal"] = refusal

        name = AnthropicUtils.get_property(message, "name")
        if name is not None:
            parsed_message["name"] = name

        tool_call_id = AnthropicUtils.get_property(message, "tool_call_id")
        if tool_call_id is not None:
            parsed_message["tool_call_id"] = tool_call_id

        message_id = AnthropicUtils.get_property(message, "id")
        if message_id is not None:
            parsed_message["id"] = message_id

        model = AnthropicUtils.get_property(message, "model")
        if model is not None:
            parsed_message["model"] = model

        stop_reason = AnthropicUtils.get_property(message, "stop_reason")
        if stop_reason is not None:
            parsed_message["stop_reason"] = stop_reason

        stop_sequence = AnthropicUtils.get_property(message, "stop_sequence")
        if stop_sequence is not None:
            parsed_message["stop_sequence"] = stop_sequence

        return parsed_message

    @staticmethod
    def parse_input(*args, **kwargs):
        try:
            messages = [
                AnthropicUtils.parse_message(message)
                for message in kwargs.get("messages", [])
            ]
            system = kwargs.get("system")
            if system is not None:
                messages = [
                    {
                        "role": "system",
                        "content": AnthropicUtils.normalize_content(system),
                    }
                ] + messages

            name = kwargs.get("model")
            extra = {
                key: AnthropicUtils.serialize_value(kwargs[key])
                for key in KWARGS_TO_CAPTURE
                if key in kwargs
            }

            return {"name": name, "input": messages, "extra": extra}
        except Exception:
            logger.exception("Error parsing Anthropic input")
            return {"name": kwargs.get("model"), "input": None, "extra": {}}

    @staticmethod
    def parse_output(message, stream=False):
        try:
            parsed_output = {
                "output": AnthropicUtils.parse_message(message),
                "tokensUsage": AnthropicUtils.parse_usage(
                    AnthropicUtils.get_property(message, "usage")
                ),
                "metadata": AnthropicUtils.build_metadata(message),
            }
            return parsed_output
        except Exception:
            logger.exception("Error parsing Anthropic output")
            return {
                "output": AnthropicUtils.serialize_value(message),
                "tokensUsage": None,
                "metadata": None,
            }
