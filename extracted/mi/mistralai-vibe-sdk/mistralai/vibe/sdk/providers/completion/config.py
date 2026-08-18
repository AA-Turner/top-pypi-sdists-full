"""Serializable completion configuration for built-in and extension providers."""

import os
from typing import TYPE_CHECKING, Annotated, Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

if TYPE_CHECKING:
    from mistralai.vibe.sdk.providers.completion.port import CompletionModel


class CompletionConfigBase(BaseModel):
    """Open base class for serializable completion configs.

    Subclass this and declare a ``type: Literal["my_provider"] = "my_provider"``
    field to define a new completion provider. Subclasses auto-register at
    import time and ``CompletionConfigBase.model_validate(...)`` dispatches by
    ``type``.
    """

    model_config = ConfigDict(extra="allow")
    _registry: ClassVar[dict[str, type["CompletionConfigBase"]]] = {}

    type: Any
    model: str

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        if "type" not in cls.__annotations__:
            return
        type_field = cls.model_fields.get("type")
        if type_field is None or not isinstance(type_field.default, str):
            return
        type_name: str = type_field.default
        existing = CompletionConfigBase._registry.get(type_name)
        if existing is not None and existing is not cls:
            msg = (
                f"Duplicate CompletionConfig type '{type_name}': "
                f"{existing.__name__} and {cls.__name__}"
            )
            raise TypeError(msg)
        CompletionConfigBase._registry[type_name] = cls

    @model_validator(mode="wrap")
    @classmethod
    def _dispatch_config(cls, data: Any, handler: Any) -> "CompletionConfigBase":
        """Route dict data to the concrete completion config subclass."""
        if cls is not CompletionConfigBase:
            result: CompletionConfigBase = handler(data)
            return result
        if isinstance(data, CompletionConfigBase):
            return data
        if isinstance(data, dict):
            type_name = data.get("type")
            if type_name and type_name in CompletionConfigBase._registry:
                concrete = CompletionConfigBase._registry[type_name].model_validate(data)
                return concrete
            if type_name:
                msg = (
                    f"Unknown CompletionConfig type '{type_name}'. "
                    f"Registered types: {sorted(CompletionConfigBase._registry)}. "
                    f"Import the extension that provides this type."
                )
                raise ValueError(msg)
        msg = (
            f"Cannot validate CompletionConfigBase from {type(data).__name__}: "
            f"expected dict or CompletionConfigBase instance"
        )
        raise ValueError(msg)

    def to_completion(self) -> "CompletionModel":
        """Build the runtime completion adapter."""
        raise NotImplementedError


CompletionConfig = CompletionConfigBase


class MistralCompletionConfig(CompletionConfigBase):
    """Serializable config for the Mistral completion adapter."""

    model_config = ConfigDict(extra="forbid")

    type: Literal["mistral"] = "mistral"
    model: str = "mistral-small-latest"
    api_key_env_var: str = "MISTRAL_CLIENT_API_KEY"
    prompt_cache_key: str | None = None
    base_url: Annotated[str, StringConstraints(strip_whitespace=True)] | None = None
    reasoning_effort: str | None = None

    def to_completion(self) -> "CompletionModel":
        """Build the runtime Mistral completion adapter."""
        api_key = os.environ.get(self.api_key_env_var, "").strip()
        if not api_key:
            msg = f"Required environment variable is not set: {self.api_key_env_var}"
            raise KeyError(msg)

        from mistralai.vibe.sdk.providers.completion.adapters.mistral import (
            MistralCompletion,
        )

        return MistralCompletion(
            api_key=api_key,
            model=self.model,
            prompt_cache_key=self.prompt_cache_key,
            reasoning_effort=self.reasoning_effort,
            server_url=self.base_url,
        )


class OpenAICompletionConfig(CompletionConfigBase):
    """Serializable config for the OpenAI completion-like adapter."""

    model_config = ConfigDict(extra="forbid")

    type: Literal["openai"] = "openai"
    model: str = "gpt-4.1"
    api_key_env_var: str = "OPENAI_API_KEY"
    base_url: Annotated[str, StringConstraints(strip_whitespace=True)] | None = None
    reasoning_effort: str | None = None
    timeout: Annotated[
        float,
        Field(gt=0, description="OpenAI-compatible HTTP timeout in seconds."),
    ] = 60.0
    temperature: (
        Annotated[
            float,
            Field(ge=0, le=2, description="Optional OpenAI-compatible sampling temperature."),
        ]
        | None
    ) = None

    def to_completion(self) -> "CompletionModel":
        """Build the runtime OpenAI completion adapter."""
        api_key = os.environ.get(self.api_key_env_var, "").strip()
        if not api_key:
            msg = f"Required environment variable is not set: {self.api_key_env_var}"
            raise KeyError(msg)

        from mistralai.vibe.sdk.providers.completion.adapters.openai import (
            OpenAICompletion,
        )

        kwargs: dict[str, Any] = {}
        if self.base_url:
            kwargs["base_url"] = self.base_url
        return OpenAICompletion(
            api_key=api_key,
            model=self.model,
            reasoning_effort=self.reasoning_effort,
            timeout=self.timeout,
            temperature=self.temperature,
            **kwargs,
        )


class OpenAIResponsesCompletionConfig(CompletionConfigBase):
    """Serializable config for the OpenAI Responses API adapter."""

    model_config = ConfigDict(extra="forbid")

    type: Literal["openai_responses"] = "openai_responses"
    model: str = "gpt-4.1"
    api_key_env_var: str = "OPENAI_API_KEY"
    base_url: Annotated[str, StringConstraints(strip_whitespace=True)] | None = None
    reasoning_effort: str | None = None
    reasoning_summary: str | None = "auto"
    timeout: Annotated[
        float,
        Field(gt=0, description="OpenAI Responses HTTP timeout in seconds."),
    ] = 60.0
    temperature: (
        Annotated[
            float,
            Field(ge=0, le=2, description="Optional OpenAI Responses sampling temperature."),
        ]
        | None
    ) = None

    def to_completion(self) -> "CompletionModel":
        """Build the runtime OpenAI Responses adapter."""
        api_key = os.environ.get(self.api_key_env_var, "").strip()
        if not api_key:
            msg = f"Required environment variable is not set: {self.api_key_env_var}"
            raise KeyError(msg)

        from mistralai.vibe.sdk.providers.completion.adapters.openai_responses import (
            OpenAIResponsesCompletion,
        )

        kwargs: dict[str, Any] = {}
        if self.base_url:
            kwargs["base_url"] = self.base_url
        return OpenAIResponsesCompletion(
            api_key=api_key,
            model=self.model,
            reasoning_effort=self.reasoning_effort,
            reasoning_summary=self.reasoning_summary,
            timeout=self.timeout,
            temperature=self.temperature,
            **kwargs,
        )


class OllamaCompletionConfig(CompletionConfigBase):
    """Serializable config for the Ollama native API adapter."""

    model_config = ConfigDict(extra="forbid")

    type: Literal["ollama"] = "ollama"
    model: str
    base_url: Annotated[str, StringConstraints(strip_whitespace=True)] = "http://localhost:11434"
    timeout: Annotated[
        float,
        Field(gt=0, description="Ollama HTTP timeout in seconds."),
    ] = 120.0
    temperature: (
        Annotated[
            float,
            Field(ge=0, le=2, description="Optional sampling temperature."),
        ]
        | None
    ) = None
    think: bool | Literal["low", "medium", "high", "max"] | None = None

    def to_completion(self) -> "CompletionModel":
        """Build the runtime Ollama completion adapter."""
        from mistralai.vibe.sdk.providers.completion.adapters.ollama import (
            OllamaCompletion,
        )

        return OllamaCompletion(
            model=self.model,
            base_url=self.base_url,
            timeout=self.timeout,
            temperature=self.temperature,
            think=self.think,
        )


class AnthropicCompletionConfig(CompletionConfigBase):
    """Serializable config for the Anthropic Messages API adapter."""

    model_config = ConfigDict(extra="forbid")

    type: Literal["anthropic"] = "anthropic"
    model: str = "claude-sonnet-4-5"
    api_key_env_var: str = "ANTHROPIC_API_KEY"
    max_tokens: int = 4096
    thinking: Literal["off", "low", "medium", "high", "max"] = "off"
    base_url: Annotated[str, StringConstraints(strip_whitespace=True)] | None = None

    def to_completion(self) -> "CompletionModel":
        """Build the runtime Anthropic completion adapter."""
        from mistralai.vibe.sdk.providers.completion.adapters.anthropic import (
            AnthropicCompletion,
        )

        api_key = os.environ.get(self.api_key_env_var, "").strip()
        if not api_key:
            msg = f"Required environment variable is not set: {self.api_key_env_var}"
            raise KeyError(msg)

        kwargs: dict[str, Any] = {}
        if self.base_url:
            kwargs["base_url"] = self.base_url
        return AnthropicCompletion(
            api_key=api_key,
            model=self.model,
            max_tokens=self.max_tokens,
            thinking=self.thinking,
            **kwargs,
        )


def completion_config_from_obj(config: CompletionConfig | dict[str, Any]) -> CompletionConfig:
    """Validate provider config into a registered completion config subclass."""
    return CompletionConfigBase.model_validate(config)


def completion_from_config(config: CompletionConfig) -> "CompletionModel":
    """Build a runtime ``CompletionModel`` from serializable provider config."""
    return config.to_completion()


__all__ = [
    "AnthropicCompletionConfig",
    "CompletionConfig",
    "CompletionConfigBase",
    "MistralCompletionConfig",
    "OllamaCompletionConfig",
    "OpenAICompletionConfig",
    "OpenAIResponsesCompletionConfig",
    "completion_config_from_obj",
    "completion_from_config",
]
