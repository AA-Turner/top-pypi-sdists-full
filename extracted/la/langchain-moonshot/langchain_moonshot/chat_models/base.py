"""Moonshot chat model integration."""

from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from typing import Any, Literal, cast

import openai
from langchain_core.language_models import (
    LangSmithParams,
    LanguageModelInput,
    ModelProfile,
    ModelProfileRegistry,
)
from langchain_core.messages import AIMessage, AIMessageChunk
from langchain_core.outputs import ChatGenerationChunk, ChatResult
from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool
from langchain_core.utils import from_env, secret_from_env
from langchain_openai.chat_models.base import (
    BaseChatOpenAI,
    _create_usage_metadata,
)
from pydantic import ConfigDict, Field, SecretStr, model_validator
from typing_extensions import Self

from langchain_moonshot.data._profiles import _PROFILES

DEFAULT_API_BASE = "https://api.moonshot.ai/v1"
DEFAULT_API_BASE_CN = "https://api.moonshot.cn/v1"
_SERIALIZED_CLASS_PATH = ("langchain", "chat_models", "moonshot", "ChatMoonshot")
_IMPORT_CLASS_PATH = ("langchain_moonshot", "chat_models", "base", "ChatMoonshot")

_MODEL_PROFILES = cast("ModelProfileRegistry", _PROFILES)


def _get_default_model_profile(model_name: str) -> ModelProfile | None:
    default = _MODEL_PROFILES.get(model_name)
    return default.copy() if default is not None else None


def _is_close_to(value: float | int | None, expected: float) -> bool:
    return value is not None and math.isclose(
        float(value),
        expected,
        rel_tol=0.0,
        abs_tol=1e-9,
    )


def _normalize_token_usage(token_usage: dict[str, Any] | None) -> dict[str, Any] | None:
    if token_usage is None:
        return None
    normalized = dict(token_usage)
    cached_tokens = normalized.get("cached_tokens")
    if cached_tokens is not None:
        prompt_details = dict(normalized.get("prompt_tokens_details") or {})
        prompt_details.setdefault("cached_tokens", cached_tokens)
        normalized["prompt_tokens_details"] = prompt_details
    return normalized


def _register_serializable_mapping() -> None:
    from langchain_core.load.load import (
        ALL_SERIALIZABLE_MAPPINGS,
        DEFAULT_NAMESPACES,
        _default_class_paths_cache,
    )
    from langchain_core.load.mapping import SERIALIZABLE_MAPPING

    SERIALIZABLE_MAPPING[_SERIALIZED_CLASS_PATH] = _IMPORT_CLASS_PATH
    ALL_SERIALIZABLE_MAPPINGS[_SERIALIZED_CLASS_PATH] = _IMPORT_CLASS_PATH
    if "langchain_moonshot" not in DEFAULT_NAMESPACES:
        DEFAULT_NAMESPACES.append("langchain_moonshot")
    _default_class_paths_cache.clear()


_register_serializable_mapping()


class ChatMoonshot(BaseChatOpenAI):
    """Moonshot chat model integration."""

    model_name: str = Field(alias="model")
    api_key: SecretStr | None = Field(
        default_factory=secret_from_env("MOONSHOT_API_KEY", default=None),
    )
    api_base: str = Field(
        alias="base_url",
        default_factory=from_env("MOONSHOT_API_BASE", default=DEFAULT_API_BASE),
    )
    thinking: bool | None = None
    prompt_cache_key: str | None = None
    safety_identifier: str | None = None
    max_completion_tokens: int | None = None

    model_config = ConfigDict(populate_by_name=True)

    @property
    def _llm_type(self) -> str:
        return "chat-moonshot"

    @property
    def lc_secrets(self) -> dict[str, str]:
        return {
            "api_key": "MOONSHOT_API_KEY",
            "openai_api_key": "MOONSHOT_API_KEY",
        }

    @classmethod
    def get_lc_namespace(cls) -> list[str]:
        return list(_SERIALIZED_CLASS_PATH[:-1])

    @property
    def lc_attributes(self) -> dict[str, Any]:
        attributes = super().lc_attributes
        if self.api_base not in {DEFAULT_API_BASE, DEFAULT_API_BASE_CN}:
            attributes["openai_api_base"] = self.api_base
        return attributes

    @classmethod
    def is_lc_serializable(cls) -> bool:
        return True

    def _resolve_model_profile(self) -> ModelProfile | None:
        return _get_default_model_profile(self.model_name)

    def _get_ls_params(
        self,
        stop: list[str] | None = None,
        **kwargs: Any,
    ) -> LangSmithParams:
        ls_params = super()._get_ls_params(stop=stop, **kwargs)
        ls_params["ls_provider"] = "moonshot"
        return ls_params

    @model_validator(mode="after")
    def validate_environment(self) -> Self:
        if (
            self.api_base in {DEFAULT_API_BASE, DEFAULT_API_BASE_CN}
            and not self.api_key
        ):
            msg = "If using default api base, MOONSHOT_API_KEY must be set."
            raise ValueError(msg)

        client_params: dict[str, Any] = {
            key: value
            for key, value in {
                "api_key": self.api_key.get_secret_value() if self.api_key else None,
                "base_url": self.api_base,
                "timeout": self.request_timeout,
                "max_retries": self.max_retries,
                "default_headers": self.default_headers,
                "default_query": self.default_query,
            }.items()
            if value is not None
        }

        if not self.client:
            sync_specific: dict[str, Any] = {"http_client": self.http_client}
            self.root_client = openai.OpenAI(
                **client_params,
                **sync_specific,
            )
            self.client = self.root_client.chat.completions
        if not self.async_client:
            async_specific: dict[str, Any] = {"http_client": self.http_async_client}
            self.root_async_client = openai.AsyncOpenAI(
                **client_params,
                **async_specific,
            )
            self.async_client = self.root_async_client.chat.completions
        return self

    def _thinking_is_enabled(self, thinking: bool | None) -> bool:
        return thinking is not False

    def _is_kimi_k2_5_model(self, model_name: str | None = None) -> bool:
        return (model_name or self.model_name).lower().startswith("kimi-k2.5")

    def _validate_kimi_k2_5_request(
        self,
        payload: dict[str, Any],
        thinking: bool | None,
    ) -> None:
        if not self._is_kimi_k2_5_model(payload.get("model")):
            return

        effective_thinking = self._thinking_is_enabled(thinking)
        expected_temperature = 1.0 if effective_thinking else 0.6

        if "temperature" in payload and payload["temperature"] is not None:
            if not _is_close_to(payload["temperature"], expected_temperature):
                msg = (
                    "kimi-k2.5 only supports temperature=1.0 when thinking is enabled "
                    "and temperature=0.6 when thinking is disabled."
                )
                raise ValueError(msg)
        if (
            "top_p" in payload
            and payload["top_p"] is not None
            and not _is_close_to(payload["top_p"], 0.95)
        ):
            raise ValueError("kimi-k2.5 only supports top_p=0.95.")
        if "n" in payload and payload["n"] is not None and payload["n"] != 1:
            raise ValueError("kimi-k2.5 only supports n=1.")
        if (
            "presence_penalty" in payload
            and payload["presence_penalty"] is not None
            and not _is_close_to(payload["presence_penalty"], 0.0)
        ):
            raise ValueError("kimi-k2.5 only supports presence_penalty=0.0.")
        if (
            "frequency_penalty" in payload
            and payload["frequency_penalty"] is not None
            and not _is_close_to(payload["frequency_penalty"], 0.0)
        ):
            raise ValueError("kimi-k2.5 only supports frequency_penalty=0.0.")

        tools = cast(list[dict[str, Any]], payload.get("tools") or [])
        if tools and effective_thinking:
            tool_choice = payload.get("tool_choice")
            if tool_choice not in (None, "auto", "none"):
                msg = (
                    "kimi-k2.5 with thinking enabled only supports "
                    "tool_choice='auto' or 'none'."
                )
                raise ValueError(msg)
            if any(
                tool.get("type") == "builtin_function"
                and tool.get("function", {}).get("name") == "$web_search"
                for tool in tools
            ):
                raise ValueError(
                    "Moonshot builtin $web_search is not supported when "
                    "thinking is enabled."
                )

    def _get_request_payload(
        self,
        input_: LanguageModelInput,
        *,
        stop: list[str] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        thinking = kwargs.pop("thinking", self.thinking)
        prompt_cache_key = kwargs.pop("prompt_cache_key", self.prompt_cache_key)
        safety_identifier = kwargs.pop("safety_identifier", self.safety_identifier)
        max_completion_tokens = kwargs.pop(
            "max_completion_tokens",
            self.max_completion_tokens,
        )

        payload = super()._get_request_payload(input_, stop=stop, **kwargs)
        messages = self._convert_input(input_).to_messages()

        for source_message, payload_message in zip(
            messages,
            payload.get("messages", []),
            strict=False,
        ):
            if not isinstance(source_message, AIMessage):
                continue
            reasoning_content = source_message.additional_kwargs.get(
                "reasoning_content"
            )
            if reasoning_content is not None:
                payload_message["reasoning_content"] = reasoning_content
            if source_message.additional_kwargs.get("partial"):
                payload_message["partial"] = True

        extra_body = dict(payload.get("extra_body") or {})
        if thinking is not None:
            extra_body["thinking"] = {
                "type": "enabled" if self._thinking_is_enabled(thinking) else "disabled"
            }
        if prompt_cache_key is not None:
            extra_body["prompt_cache_key"] = prompt_cache_key
        if safety_identifier is not None:
            extra_body["safety_identifier"] = safety_identifier
        if extra_body:
            payload["extra_body"] = extra_body

        if max_completion_tokens is not None:
            payload_max_tokens = payload.get("max_tokens")
            if (
                payload_max_tokens is not None
                and payload_max_tokens != max_completion_tokens
            ):
                msg = "Specify at most one of `max_tokens` and `max_completion_tokens`."
                raise ValueError(msg)
            payload.pop("max_tokens", None)
            payload["max_completion_tokens"] = max_completion_tokens

        self._validate_kimi_k2_5_request(payload, thinking)
        return payload

    def _create_chat_result(
        self,
        response: dict[str, Any] | openai.BaseModel,
        generation_info: dict[str, Any] | None = None,
    ) -> ChatResult:
        response_dict = (
            dict(response)
            if isinstance(response, dict)
            else response.model_dump(
                exclude={"choices": {"__all__": {"message": {"parsed"}}}}
            )
        )
        normalized_usage = _normalize_token_usage(
            cast(dict[str, Any] | None, response_dict.get("usage"))
        )
        if normalized_usage is not None:
            response_dict["usage"] = normalized_usage

        result = super()._create_chat_result(response_dict, generation_info)
        service_tier = cast(str | None, response_dict.get("service_tier"))

        for generation, choice in zip(
            result.generations,
            response_dict.get("choices", []),
            strict=False,
        ):
            if generation.message.response_metadata is None:
                generation.message.response_metadata = {}
            generation.message.response_metadata["model_provider"] = "moonshot"

            message = choice.get("message", {})
            if isinstance(message, dict):
                reasoning_content = message.get("reasoning_content")
                if reasoning_content is not None:
                    generation.message.additional_kwargs["reasoning_content"] = (
                        reasoning_content
                    )

            if normalized_usage is not None and isinstance(
                generation.message,
                AIMessage,
            ):
                generation.message.usage_metadata = _create_usage_metadata(
                    normalized_usage,
                    service_tier,
                )

        if result.llm_output is not None:
            result.llm_output["model_provider"] = "moonshot"
            if normalized_usage is not None:
                result.llm_output["token_usage"] = normalized_usage

        return result

    def _convert_chunk_to_generation_chunk(
        self,
        chunk: dict[str, Any],
        default_chunk_class: type,
        base_generation_info: dict[str, Any] | None,
    ) -> ChatGenerationChunk | None:
        normalized_chunk = dict(chunk)
        choices = normalized_chunk.get("choices") or normalized_chunk.get(
            "chunk",
            {},
        ).get("choices", [])
        if normalized_chunk.get("usage") is None and choices:
            choice_usage = choices[0].get("usage")
            if choice_usage is not None:
                normalized_chunk["usage"] = choice_usage
        if normalized_chunk.get("usage") is not None:
            normalized_chunk["usage"] = _normalize_token_usage(
                normalized_chunk["usage"]
            )

        generation_chunk = super()._convert_chunk_to_generation_chunk(
            normalized_chunk,
            default_chunk_class,
            base_generation_info,
        )
        if not generation_chunk:
            return None

        if isinstance(generation_chunk.message, AIMessageChunk):
            generation_chunk.message.response_metadata = {
                **generation_chunk.message.response_metadata,
                "model_provider": "moonshot",
            }
            if choices:
                reasoning_content = choices[0].get("delta", {}).get(
                    "reasoning_content"
                )
                if reasoning_content is not None:
                    generation_chunk.message.additional_kwargs["reasoning_content"] = (
                        reasoning_content
                    )

        return generation_chunk

    def bind_tools(
        self,
        tools: Sequence[dict[str, Any] | type | Callable[..., Any] | BaseTool],
        *,
        tool_choice: dict[str, Any] | str | bool | None = None,
        strict: bool | None = None,
        parallel_tool_calls: bool | None = None,
        **kwargs: Any,
    ) -> Runnable[LanguageModelInput, AIMessage]:
        if self._is_kimi_k2_5_model() and self._thinking_is_enabled(self.thinking):
            if tool_choice not in (None, False, "auto", "none"):
                msg = (
                    "kimi-k2.5 with thinking enabled only supports "
                    "tool_choice='auto' or 'none'."
                )
                raise ValueError(msg)

        return super().bind_tools(
            tools,
            tool_choice=tool_choice,
            strict=strict,
            parallel_tool_calls=parallel_tool_calls,
            **kwargs,
        )

    def with_structured_output(
        self,
        schema: dict[str, Any] | type | None = None,
        *,
        method: Literal[
            "function_calling",
            "json_mode",
            "json_schema",
        ] = "function_calling",
        include_raw: bool = False,
        strict: bool | None = None,
        **kwargs: Any,
    ) -> Runnable[LanguageModelInput, Any]:
        if method == "json_schema":
            method = "function_calling"
        return super().with_structured_output(
            schema,
            method=method,
            include_raw=include_raw,
            strict=strict,
            **kwargs,
        )
