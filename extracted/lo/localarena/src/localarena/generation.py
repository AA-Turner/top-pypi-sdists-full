"""Provider-neutral request and response records for live model generation."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Literal

_MAX_SAFE_INTEGER = (1 << 53) - 1
_MAX_JSON_DEPTH = 100
_MESSAGE_ROLES = frozenset({"system", "user", "assistant"})
_RESERVED_REQUEST_FIELDS = frozenset(
    {
        "model",
        "messages",
        "stream",
        "max_tokens",
        "max_completion_tokens",
        "temperature",
        "seed",
        "stop",
    }
)

JsonPrimitive = str | int | float | bool | None
JsonValue = JsonPrimitive | list["JsonValue"] | dict[str, "JsonValue"]


def _require_nonempty_string(value: object, *, field_name: str) -> str:
    if type(value) is not str:
        raise TypeError(f"{field_name} must be a string")
    if not value.strip():
        raise ValueError(f"{field_name} must not be empty or whitespace")
    return value


def _normalize_json(
    value: object,
    *,
    path: str,
    active: set[int],
    depth: int,
) -> object:
    if depth > _MAX_JSON_DEPTH:
        raise ValueError(f"{path} exceeds the maximum JSON depth of {_MAX_JSON_DEPTH}")

    if value is None or type(value) is bool or isinstance(value, str):
        return value
    if type(value) is int:
        if abs(value) > _MAX_SAFE_INTEGER:
            raise ValueError(f"{path} exceeds the interoperable JSON integer range")
        return value
    if type(value) is float:
        if not math.isfinite(value):
            raise ValueError(f"{path} must be finite")
        if value.is_integer() and abs(value) > _MAX_SAFE_INTEGER:
            raise ValueError(f"{path} exceeds the interoperable JSON integer range")
        return value

    if isinstance(value, Mapping):
        identity = id(value)
        if identity in active:
            raise ValueError(f"{path} contains a circular reference")
        active.add(identity)
        try:
            normalized: dict[str, object] = {}
            for key, item in value.items():
                if type(key) is not str:
                    raise TypeError(f"{path} keys must be strings")
                normalized[key] = _normalize_json(
                    item,
                    path=f"{path}.{key}",
                    active=active,
                    depth=depth + 1,
                )
            return normalized
        finally:
            active.remove(identity)

    if isinstance(value, (list, tuple)):
        identity = id(value)
        if identity in active:
            raise ValueError(f"{path} contains a circular reference")
        active.add(identity)
        try:
            return [
                _normalize_json(
                    item,
                    path=f"{path}[{index}]",
                    active=active,
                    depth=depth + 1,
                )
                for index, item in enumerate(value)
            ]
        finally:
            active.remove(identity)

    raise TypeError(f"{path} contains a non-JSON value of type {type(value).__name__}")


def _copy_json_object(value: Mapping[str, object], *, field_name: str) -> dict[str, object]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{field_name} must be a mapping")
    normalized = _normalize_json(value, path=field_name, active=set(), depth=0)
    return normalized  # type: ignore[return-value]


def _freeze_json(value: object) -> object:
    if isinstance(value, dict):
        return MappingProxyType(
            {key: _freeze_json(item) for key, item in value.items()}
        )
    if isinstance(value, list):
        return tuple(_freeze_json(item) for item in value)
    return value


def _freeze_json_object(
    value: Mapping[str, object],
    *,
    field_name: str,
) -> Mapping[str, object]:
    return _freeze_json(
        _copy_json_object(value, field_name=field_name)
    )  # type: ignore[return-value]


def _thaw_json(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: _thaw_json(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw_json(item) for item in value]
    return value


def _optional_token_count(value: object, *, field_name: str) -> int | None:
    if value is None:
        return None
    if type(value) is not int:
        raise TypeError(f"{field_name} must be an integer or None")
    if value < 0:
        raise ValueError(f"{field_name} must not be negative")
    if value > _MAX_SAFE_INTEGER:
        raise ValueError(f"{field_name} exceeds the interoperable integer range")
    return value


@dataclass(frozen=True, slots=True)
class ChatMessage:
    """One text message in a provider-neutral chat conversation."""

    role: Literal["system", "user", "assistant"]
    content: str

    def __post_init__(self) -> None:
        if type(self.role) is not str:
            raise TypeError("role must be a string")
        if self.role not in _MESSAGE_ROLES:
            choices = ", ".join(sorted(_MESSAGE_ROLES))
            raise ValueError(f"role must be one of {choices}")
        if type(self.content) is not str:
            raise TypeError("content must be a string")

    def to_dict(self) -> dict[str, str]:
        """Return a detached JSON object accepted by chat-completion APIs."""

        return {"role": self.role, "content": self.content}

    def __deepcopy__(self, memo: dict[int, object]) -> ChatMessage:
        memo[id(self)] = self
        return self


@dataclass(frozen=True, slots=True)
class GenerationRequest:
    """A conservative, interoperable non-streaming generation request."""

    model: str
    messages: Sequence[ChatMessage]
    max_tokens: int | None = 512
    temperature: float | None = None
    seed: int | None = None
    stop: Sequence[str] = ()
    extra_body: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "model",
            _require_nonempty_string(self.model, field_name="model"),
        )

        if isinstance(self.messages, (str, bytes, bytearray)):
            raise TypeError("messages must be a sequence of ChatMessage values")
        messages = tuple(self.messages)
        if not messages:
            raise ValueError("messages must contain at least one message")
        if any(not isinstance(message, ChatMessage) for message in messages):
            raise TypeError("messages must contain only ChatMessage values")
        object.__setattr__(self, "messages", messages)

        if self.max_tokens is not None:
            if type(self.max_tokens) is not int:
                raise TypeError("max_tokens must be an integer or None")
            if self.max_tokens < 1:
                raise ValueError("max_tokens must be greater than zero")
            if self.max_tokens > _MAX_SAFE_INTEGER:
                raise ValueError("max_tokens exceeds the interoperable integer range")

        if self.temperature is not None:
            if type(self.temperature) not in (int, float):
                raise TypeError("temperature must be a number or None")
            temperature = float(self.temperature)
            if not math.isfinite(temperature):
                raise ValueError("temperature must be finite")
            if temperature < 0 or temperature > 2:
                raise ValueError("temperature must be between zero and two")
            object.__setattr__(self, "temperature", temperature)

        if self.seed is not None:
            if type(self.seed) is not int:
                raise TypeError("seed must be an integer or None")
            if abs(self.seed) > _MAX_SAFE_INTEGER:
                raise ValueError("seed exceeds the interoperable integer range")

        if isinstance(self.stop, (str, bytes, bytearray)):
            raise TypeError("stop must be a sequence of strings")
        stops = tuple(self.stop)
        if any(type(item) is not str or not item for item in stops):
            raise ValueError("stop must contain only non-empty strings")
        object.__setattr__(self, "stop", stops)

        extra_body = _copy_json_object(self.extra_body, field_name="extra_body")
        reserved = sorted(_RESERVED_REQUEST_FIELDS.intersection(extra_body))
        if reserved:
            raise ValueError(
                "extra_body must not override reserved fields: "
                + ", ".join(reserved)
            )
        object.__setattr__(
            self,
            "extra_body",
            _freeze_json(extra_body),
        )

    def __deepcopy__(self, memo: dict[int, object]) -> GenerationRequest:
        memo[id(self)] = self
        return self


@dataclass(frozen=True, slots=True)
class TokenUsage:
    """Normalized token accounting from a provider response."""

    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None
    cached_input_tokens: int | None = None
    reasoning_tokens: int | None = None

    def __post_init__(self) -> None:
        for field_name in (
            "input_tokens",
            "output_tokens",
            "total_tokens",
            "cached_input_tokens",
            "reasoning_tokens",
        ):
            object.__setattr__(
                self,
                field_name,
                _optional_token_count(
                    getattr(self, field_name),
                    field_name=field_name,
                ),
            )

    def to_dict(self) -> dict[str, int | None]:
        """Return a detached JSON representation."""

        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "cached_input_tokens": self.cached_input_tokens,
            "reasoning_tokens": self.reasoning_tokens,
        }

    def __deepcopy__(self, memo: dict[int, object]) -> TokenUsage:
        memo[id(self)] = self
        return self


@dataclass(frozen=True, slots=True)
class GenerationResult:
    """Normalized text generation plus safe provenance and usage metadata."""

    text: str
    provider: str
    model: str
    response_model: str | None = None
    finish_reason: str | None = None
    usage: TokenUsage = field(default_factory=TokenUsage)
    latency_seconds: float = 0.0
    attempts: int = 1
    response_id: str | None = None
    metadata: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if type(self.text) is not str:
            raise TypeError("text must be a string")
        object.__setattr__(
            self,
            "provider",
            _require_nonempty_string(self.provider, field_name="provider"),
        )
        object.__setattr__(
            self,
            "model",
            _require_nonempty_string(self.model, field_name="model"),
        )
        for field_name in ("response_model", "finish_reason", "response_id"):
            value = getattr(self, field_name)
            if value is not None and type(value) is not str:
                raise TypeError(f"{field_name} must be a string or None")
        if not isinstance(self.usage, TokenUsage):
            raise TypeError("usage must be a TokenUsage")
        if type(self.latency_seconds) not in (int, float):
            raise TypeError("latency_seconds must be a number")
        latency = float(self.latency_seconds)
        if not math.isfinite(latency) or latency < 0:
            raise ValueError("latency_seconds must be finite and non-negative")
        object.__setattr__(self, "latency_seconds", latency)
        if type(self.attempts) is not int:
            raise TypeError("attempts must be an integer")
        if not 1 <= self.attempts <= _MAX_SAFE_INTEGER:
            raise ValueError(
                "attempts must be a positive interoperable integer"
            )
        object.__setattr__(
            self,
            "metadata",
            _freeze_json_object(self.metadata, field_name="metadata"),
        )

    def to_dict(self) -> dict[str, object]:
        """Return a detached, JSON-compatible representation."""

        return {
            "text": self.text,
            "provider": self.provider,
            "model": self.model,
            "response_model": self.response_model,
            "finish_reason": self.finish_reason,
            "usage": self.usage.to_dict(),
            "latency_seconds": self.latency_seconds,
            "attempts": self.attempts,
            "response_id": self.response_id,
            "metadata": _thaw_json(self.metadata),
        }

    def __deepcopy__(self, memo: dict[int, object]) -> GenerationResult:
        memo[id(self)] = self
        return self


@dataclass(frozen=True, slots=True)
class ModelInfo:
    """A model identifier discovered from one configured provider."""

    id: str
    provider: str
    display_name: str | None = None
    metadata: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "id",
            _require_nonempty_string(self.id, field_name="id"),
        )
        object.__setattr__(
            self,
            "provider",
            _require_nonempty_string(self.provider, field_name="provider"),
        )
        if self.display_name is not None and type(self.display_name) is not str:
            raise TypeError("display_name must be a string or None")
        object.__setattr__(
            self,
            "metadata",
            _freeze_json_object(self.metadata, field_name="metadata"),
        )

    def to_dict(self) -> dict[str, object]:
        """Return a detached, JSON-compatible representation."""

        return {
            "id": self.id,
            "provider": self.provider,
            "display_name": self.display_name,
            "metadata": _thaw_json(self.metadata),
        }

    def __deepcopy__(self, memo: dict[int, object]) -> ModelInfo:
        memo[id(self)] = self
        return self
