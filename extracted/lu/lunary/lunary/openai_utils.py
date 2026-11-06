import copy
import json
import logging

from .parsers import (
    is_openai_omitted,
    redact_extra_headers,
    serialize_param_value,
    unavailable_iterable_snapshot,
)

logger = logging.getLogger(__name__)

MONITORED_KEYS = [
    "frequency_penalty",
    "functions",
    "logit_bias",
    "max_tokens",
    "max_completion_tokens",
    "n",
    "presence_penalty",
    "response_format",
    "seed",
    "stop",
    "stream",
    "audio",
    "modalities",
    "temperature",
    "tool_choice",
    "tools",
    "tool_calls",
    "top_p",
    "top_k",
    "top_logprobs",
    "logprobs",
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
    "metadata",
    "web_search_options",
]

_DEFAULT_NONE_TRANSPORT_KEYS = (
    "extra_headers",
    "extra_query",
    "extra_body",
)


def _default_none_transport_keys(kwargs):
    return [
        key
        for key in _DEFAULT_NONE_TRANSPORT_KEYS
        if key in kwargs and kwargs[key] is None
    ]


def _serialize_chat_response_format(value):
    if not isinstance(value, type):
        return OpenAIUtils.serialize_value(value)

    try:
        from openai.lib._parsing._completions import (
            type_to_response_format_param,
        )

        return OpenAIUtils.serialize_value(
            type_to_response_format_param(value)
        )
    except (ImportError, TypeError, ValueError):
        return serialize_param_value(value)


def _serialize_responses_text_format(value):
    if not isinstance(value, type):
        return OpenAIUtils.serialize_value(value)

    try:
        from openai.resources.responses.responses import (
            _type_to_text_format_param,
        )

        return OpenAIUtils.serialize_value(_type_to_text_format_param(value))
    except (ImportError, TypeError, ValueError):
        return serialize_param_value(value)


class OpenAIUtils:
    @staticmethod
    def parse_role(role):
        if role == "assistant":
            return "ai"
        else:
            return role

    @staticmethod
    def has_property(object, property):
        if isinstance(object, dict):
            return property in object

        fields_set = getattr(object, "model_fields_set", None)
        if fields_set is not None:
            return property in fields_set

        return hasattr(object, property)

    @staticmethod
    def get_property(object, property, default=None):
        if isinstance(object, dict):
            return object[property] if property in object else default
        return getattr(object, property, default)

    @staticmethod
    def serialize_value(value):
        if value is None or isinstance(value, (str, int, float, bool)):
            return value
        if isinstance(value, type):
            return serialize_param_value(value)
        if isinstance(value, list):
            return [
                OpenAIUtils.serialize_value(item)
                for item in value
                if not is_openai_omitted(item)
            ]
        if isinstance(value, tuple):
            return [
                OpenAIUtils.serialize_value(item)
                for item in value
                if not is_openai_omitted(item)
            ]
        if isinstance(value, dict):
            return {
                key: OpenAIUtils.serialize_value(item)
                for key, item in value.items()
                if not is_openai_omitted(item)
            }
        if hasattr(value, "model_dump"):
            try:
                dumped = value.model_dump(mode="json", exclude_unset=True)
            except TypeError:
                dumped = value.model_dump(exclude_unset=True)
            return OpenAIUtils.serialize_value(dumped)
        if hasattr(value, "model_dump_json"):
            return json.loads(value.model_dump_json(exclude_unset=True))
        if hasattr(value, "__dict__"):
            return {
                key: OpenAIUtils.serialize_value(item)
                for key, item in vars(value).items()
                if not key.startswith("_")
            }
        return serialize_param_value(value)

    @staticmethod
    def parse_message(message):
        parsed_message = {}
        for key in (
            "role",
            "content",
            "name",
            "refusal",
            "audio",
            "function_call",
            "tool_calls",
            "tool_call_id",
            "annotations",
        ):
            if OpenAIUtils.has_property(message, key):
                parsed_message[key] = OpenAIUtils.serialize_value(
                    OpenAIUtils.get_property(message, key)
                )
        return parsed_message

    @staticmethod
    def parse_input(*args, **kwargs):
        provider_messages = kwargs["messages"]
        if isinstance(provider_messages, (list, tuple)):
            messages = [
                OpenAIUtils.parse_message(message)
                for message in provider_messages
            ]
        else:
            messages = unavailable_iterable_snapshot(provider_messages)
        name = (
            kwargs.get("model", None)
            or kwargs.get("engine", None)
            or kwargs.get("deployment_id", None)
        )
        extra = {}
        param_overrides = {}
        for key in MONITORED_KEYS:
            if key not in kwargs or is_openai_omitted(kwargs[key]):
                continue
            serialized = (
                _serialize_chat_response_format(kwargs[key])
                if key == "response_format"
                else OpenAIUtils.serialize_value(kwargs[key])
            )
            extra[key] = serialized
            if key == "response_format":
                param_overrides[key] = serialized
        extra["api_mode"] = "chat_completions"
        if name is not None:
            extra["model"] = name

        return {
            "name": name,
            "input": messages,
            "extra": extra,
            "param_overrides": param_overrides,
            "param_omissions": _default_none_transport_keys(kwargs),
        }

    @staticmethod
    def parse_output(output, stream=False):
        try:
            usage = OpenAIUtils.get_property(output, "usage")
            tokens_usage = None
            if usage is not None:
                tokens_usage = {
                    "completion": OpenAIUtils.get_property(
                        usage, "completion_tokens"
                    ),
                    "prompt": OpenAIUtils.get_property(usage, "prompt_tokens"),
                    "promptCached": OpenAIUtils.get_property(
                        OpenAIUtils.get_property(usage, "prompt_tokens_details"),
                        "cached_tokens",
                    ),
                }
            choices = OpenAIUtils.get_property(output, "choices", []) or []
            parsed_choices = []
            for choice in choices:
                parsed_choice = {}
                for key in ("index", "finish_reason", "logprobs"):
                    if OpenAIUtils.has_property(choice, key):
                        parsed_choice[key] = OpenAIUtils.serialize_value(
                            OpenAIUtils.get_property(choice, key)
                        )
                parsed_choice["message"] = OpenAIUtils.parse_message(
                    OpenAIUtils.get_property(choice, "message")
                )
                parsed_choices.append(parsed_choice)
            parsed_output = {"choices": parsed_choices}

            return {"output": parsed_output, "tokensUsage": tokens_usage}
        except Exception:
            logger.exception("Error parsing openai output")


class OpenAIChatStreamAccumulator:
    def __init__(self, expected_choice_count=1):
        self._expected_choice_count = (
            expected_choice_count
            if isinstance(expected_choice_count, int)
            and not isinstance(expected_choice_count, bool)
            and expected_choice_count > 0
            else 1
        )
        self._choices = {}
        self._choice_metadata = {}
        self.prompt_tokens = None
        self.completion_tokens = None
        self._chunks_with_choices = 0

    @staticmethod
    def _append_fragment(target, key, fragment):
        if fragment is None:
            return
        if isinstance(fragment, str):
            target[key] = f"{target.get(key, '')}{fragment}"
        else:
            target[key] = OpenAIUtils.serialize_value(fragment)

    @staticmethod
    def _merge_object(target, fragment):
        serialized = OpenAIUtils.serialize_value(fragment)
        if not isinstance(serialized, dict):
            return
        for key, value in serialized.items():
            if value is None:
                if key not in target:
                    target[key] = None
            elif isinstance(value, str):
                OpenAIChatStreamAccumulator._append_fragment(target, key, value)
            elif isinstance(value, dict):
                nested = target.setdefault(key, {})
                if isinstance(nested, dict):
                    OpenAIChatStreamAccumulator._merge_object(nested, value)
                else:
                    target[key] = copy.deepcopy(value)
            else:
                target[key] = copy.deepcopy(value)

    def _message(self, choice_index):
        return self._choices.setdefault(choice_index, {})

    @staticmethod
    def _merge_choice_logprobs(metadata, fragment):
        serialized = OpenAIUtils.serialize_value(fragment)
        if serialized is None:
            metadata.setdefault("logprobs", None)
            return
        if not isinstance(serialized, dict):
            metadata["logprobs"] = serialized
            return

        existing = metadata.get("logprobs")
        if not isinstance(existing, dict):
            existing = {}
            metadata["logprobs"] = existing
        for key, value in serialized.items():
            if isinstance(value, list):
                target = existing.setdefault(key, [])
                if isinstance(target, list):
                    target.extend(copy.deepcopy(value))
                else:
                    existing[key] = copy.deepcopy(value)
            else:
                existing[key] = copy.deepcopy(value)

    def _merge_tool_call(self, message, tool_call):
        call_index = OpenAIUtils.get_property(tool_call, "index", 0)
        if call_index is None:
            call_index = 0
        calls = message.setdefault("_tool_calls_by_index", {})
        existing = calls.setdefault(call_index, {})

        for key in ("id", "type"):
            if OpenAIUtils.has_property(tool_call, key):
                value = OpenAIUtils.get_property(tool_call, key)
                if value is not None:
                    existing[key] = value

        if OpenAIUtils.has_property(tool_call, "function"):
            function_fragment = OpenAIUtils.get_property(tool_call, "function")
            if function_fragment is None:
                existing["function"] = None
            else:
                function = existing.get("function")
                if not isinstance(function, dict):
                    function = {}
                    existing["function"] = function
                self._merge_object(function, function_fragment)

    def add_chunk(self, chunk):
        usage = OpenAIUtils.get_property(chunk, "usage")
        if usage is not None:
            prompt = OpenAIUtils.get_property(usage, "prompt_tokens")
            completion = OpenAIUtils.get_property(usage, "completion_tokens")
            if prompt is not None:
                self.prompt_tokens = prompt
            if completion is not None:
                self.completion_tokens = completion

        choices = OpenAIUtils.get_property(chunk, "choices", []) or []
        if choices:
            self._chunks_with_choices += 1

        for choice in choices:
            choice_index = OpenAIUtils.get_property(choice, "index", 0) or 0
            delta = OpenAIUtils.get_property(choice, "delta", {}) or {}
            message = self._message(choice_index)
            metadata = self._choice_metadata.setdefault(
                choice_index, {"index": choice_index}
            )

            if OpenAIUtils.has_property(choice, "finish_reason"):
                finish_reason = OpenAIUtils.get_property(
                    choice, "finish_reason"
                )
                if finish_reason is not None or "finish_reason" not in metadata:
                    metadata["finish_reason"] = OpenAIUtils.serialize_value(
                        finish_reason
                    )
            if OpenAIUtils.has_property(choice, "logprobs"):
                self._merge_choice_logprobs(
                    metadata, OpenAIUtils.get_property(choice, "logprobs")
                )

            for key in ("role", "content", "refusal"):
                if OpenAIUtils.has_property(delta, key):
                    value = OpenAIUtils.get_property(delta, key)
                    if key == "role":
                        if value is not None:
                            message[key] = value
                    elif value is not None:
                        self._append_fragment(message, key, value)

            if OpenAIUtils.has_property(delta, "audio"):
                audio_fragment = OpenAIUtils.get_property(delta, "audio")
                if audio_fragment is None:
                    message["audio"] = None
                else:
                    audio = message.get("audio")
                    if not isinstance(audio, dict):
                        audio = {}
                        message["audio"] = audio
                    self._merge_object(audio, audio_fragment)

            if OpenAIUtils.has_property(delta, "function_call"):
                function_fragment = OpenAIUtils.get_property(
                    delta, "function_call"
                )
                if function_fragment is None:
                    message["function_call"] = None
                else:
                    function_call = message.get("function_call")
                    if not isinstance(function_call, dict):
                        function_call = {}
                        message["function_call"] = function_call
                    self._merge_object(function_call, function_fragment)

            tool_calls = OpenAIUtils.get_property(delta, "tool_calls", []) or []
            for tool_call in tool_calls:
                self._merge_tool_call(message, tool_call)

    def message(self, choice_index=None):
        if not self._choices:
            return {"role": "assistant", "content": ""}
        if choice_index is None:
            choice_index = min(self._choices)
        message = copy.deepcopy(self._choices[choice_index])
        indexed_calls = message.pop("_tool_calls_by_index", {})
        if indexed_calls:
            message["tool_calls"] = [
                indexed_calls[index] for index in sorted(indexed_calls)
            ]
        message.setdefault("role", "assistant")
        return OpenAIUtils.parse_message(message)

    def output(self):
        return {
            "choices": [
                {
                    **copy.deepcopy(
                        self._choice_metadata.get(index, {"index": index})
                    ),
                    "message": self.message(index),
                }
                for index in sorted(self._choices)
            ]
        }

    def has_terminal_choice_state(self):
        expected_indices = set(range(self._expected_choice_count))
        observed_indices = set(self._choices)
        return expected_indices.issubset(observed_indices) and all(
            self._choice_metadata.get(index, {}).get("finish_reason")
            is not None
            for index in observed_indices
        )

    def token_usage(self):
        return {
            "completion": (
                self.completion_tokens
                if self.completion_tokens is not None
                else self._chunks_with_choices
            ),
            "prompt": self.prompt_tokens,
        }


class OpenAIResponsesUtils:
    @staticmethod
    def parse_input(*args, **kwargs):
        text_format = kwargs.get("text_format") if kwargs else None
        param_omissions = _default_none_transport_keys(kwargs)
        if kwargs:
            request = redact_extra_headers(OpenAIUtils.serialize_value(kwargs))
        elif len(args) == 1:
            request = redact_extra_headers(OpenAIUtils.serialize_value(args[0]))
        else:
            request = redact_extra_headers(
                OpenAIUtils.serialize_value(list(args))
            )

        if isinstance(request, dict):
            for key in param_omissions:
                request.pop(key, None)

        if isinstance(request, dict) and "text_format" in request:
            request.pop("text_format")
            text = request.get("text")
            if not isinstance(text, dict):
                text = {}
                request["text"] = text
            text.setdefault(
                "format", _serialize_responses_text_format(text_format)
            )

        model = kwargs.get("model") if kwargs else None
        if model is None and isinstance(request, dict):
            model = request.get("model")
        extra = {"api_mode": "responses"}
        if model is not None:
            extra["model"] = model
        return {
            "name": model,
            "input": request,
            "extra": extra,
            "param_omissions": param_omissions,
        }

    @staticmethod
    def parse_retrieve_input(*args, **kwargs):
        param_omissions = _default_none_transport_keys(kwargs)
        request = {
            key: OpenAIUtils.serialize_value(value)
            for key, value in kwargs.items()
            if not is_openai_omitted(value) and key not in param_omissions
        }
        if args and "response_id" not in request:
            request["response_id"] = OpenAIUtils.serialize_value(args[0])
        return {
            "name": None,
            "input": redact_extra_headers(request),
            "extra": {"api_mode": "responses"},
            "param_omissions": param_omissions,
        }

    @staticmethod
    def parse_output(output, stream=False):
        serialized = OpenAIUtils.serialize_value(output)
        usage = OpenAIUtils.get_property(output, "usage")
        tokens_usage = None
        if usage is not None:
            input_details = OpenAIUtils.get_property(
                usage, "input_tokens_details"
            )
            tokens_usage = {
                "prompt": OpenAIUtils.get_property(usage, "input_tokens"),
                "completion": OpenAIUtils.get_property(
                    usage, "output_tokens"
                ),
                "promptCached": OpenAIUtils.get_property(
                    input_details, "cached_tokens"
                ),
            }
        return {"output": serialized, "tokensUsage": tokens_usage}


class OpenAIResponsesStreamAccumulator:
    _TERMINAL_EVENT_TYPES = {
        "response.completed",
        "response.incomplete",
        "response.failed",
    }

    def __init__(self):
        self._terminal_response = None
        self._stream_error = None
        self._observed_event_types = []

    def add_event(self, event):
        event_type = OpenAIUtils.get_property(event, "type")
        if isinstance(event_type, str):
            self._observed_event_types.append(event_type)
        if event_type == "error":
            self._stream_error = OpenAIUtils.serialize_value(event)
        if event_type in self._TERMINAL_EVENT_TYPES:
            response = OpenAIUtils.get_property(event, "response")
            if response is not None:
                self._terminal_response = response

    def output(self):
        if self._terminal_response is not None:
            return OpenAIUtils.serialize_value(self._terminal_response)
        if self._stream_error is not None:
            return copy.deepcopy(self._stream_error)
        return {
            "type": "responses_stream_capture_incomplete",
            "event_types": self._observed_event_types,
        }

    def has_terminal_response(self):
        return self._terminal_response is not None

    def is_completed(self):
        return (
            self._terminal_response is not None
            and OpenAIUtils.get_property(self._terminal_response, "status")
            == "completed"
        )

    def should_emit_end(self):
        if self._terminal_response is None or self._stream_error is not None:
            return False
        return OpenAIUtils.get_property(
            self._terminal_response, "status"
        ) in {"completed", "incomplete"}

    def error(self, *, eof=False):
        if self._stream_error is not None:
            return {
                "code": self._stream_error.get("code")
                or "responses_stream_error",
                "message": self._stream_error.get("message")
                or "OpenAI Responses stream reported an error",
            }

        if self._terminal_response is not None:
            status = OpenAIUtils.get_property(
                self._terminal_response, "status"
            )
            if status == "failed":
                provider_error = OpenAIUtils.serialize_value(
                    OpenAIUtils.get_property(self._terminal_response, "error")
                )
                if not isinstance(provider_error, dict):
                    provider_error = {}
                return {
                    "code": provider_error.get("code") or "response_failed",
                    "message": provider_error.get("message")
                    or "OpenAI Responses stream failed",
                }
            if status == "incomplete":
                details = OpenAIUtils.serialize_value(
                    OpenAIUtils.get_property(
                        self._terminal_response, "incomplete_details"
                    )
                )
                reason = details.get("reason") if isinstance(details, dict) else None
                return {
                    "code": "response_incomplete",
                    "message": (
                        f"OpenAI Responses stream was incomplete: {reason}"
                        if reason
                        else "OpenAI Responses stream was incomplete"
                    ),
                }
            return {
                "code": "response_not_completed",
                "message": f"OpenAI Responses stream ended with status {status!r}",
            }

        return {
            "code": (
                "responses_stream_incomplete"
                if eof
                else "stream_cancelled"
            ),
            "message": (
                "OpenAI Responses stream ended without a terminal response"
                if eof
                else "OpenAI Responses stream closed before completion"
            ),
        }

    def token_usage(self):
        if self._terminal_response is None:
            return None
        return OpenAIResponsesUtils.parse_output(self._terminal_response)[
            "tokensUsage"
        ]
