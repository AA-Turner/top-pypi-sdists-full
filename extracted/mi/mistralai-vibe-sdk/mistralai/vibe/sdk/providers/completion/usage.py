"""Token usage accounting shared by completion adapters and history entries."""

from collections.abc import Callable, Mapping
from typing import Any

from pydantic import BaseModel

_TokenReader = Callable[[Any, str], int | None]


class TokenUsage(BaseModel):
    """Provider-reported token usage for an LLM response."""

    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0
    reasoning_tokens: int = 0
    total_tokens: int | None = None

    @classmethod
    def from_provider_usage(
        cls,
        raw_usage: Any,
        *,
        read: _TokenReader,
        input_aliases: tuple[str, ...] = ("input_tokens", "prompt_tokens"),
        output_aliases: tuple[str, ...] = ("output_tokens", "completion_tokens"),
        cache_read_aliases: tuple[str, ...] = (
            "cache_read_tokens",
            "cached_input_tokens",
            "cached_tokens",
        ),
        cache_write_aliases: tuple[str, ...] = ("cache_write_tokens",),
        reasoning_aliases: tuple[str, ...] = ("reasoning_tokens",),
        total_aliases: tuple[str, ...] = ("total_tokens",),
    ) -> "TokenUsage | None":
        """Normalize provider-specific usage payloads into TokenUsage."""
        if raw_usage is None:
            return None

        usage = cls(
            input_tokens=_read_first(raw_usage, read, input_aliases) or 0,
            output_tokens=_read_first(raw_usage, read, output_aliases) or 0,
            cache_read_tokens=_read_first(raw_usage, read, cache_read_aliases) or 0,
            cache_write_tokens=_read_first(raw_usage, read, cache_write_aliases) or 0,
            reasoning_tokens=_read_first(raw_usage, read, reasoning_aliases) or 0,
            total_tokens=_read_first(raw_usage, read, total_aliases),
        )
        if usage.is_empty:
            return None
        return usage

    @classmethod
    def from_mapping_usage(
        cls,
        raw_usage: Any,
        *,
        nested_aliases: Mapping[str, tuple[str, ...]] | None = None,
    ) -> "TokenUsage | None":
        """Normalize a dict-like provider usage payload."""

        def read(usage: Any, name: str) -> int | None:
            if not isinstance(usage, Mapping):
                return None
            if nested_aliases is not None and (path := nested_aliases.get(name)) is not None:
                obj: Any = usage
                for part in path:
                    if not isinstance(obj, Mapping):
                        break
                    obj = obj.get(part)
                else:
                    if isinstance(obj, int):
                        return obj
            value = usage.get(name)
            return value if isinstance(value, int) else None

        return cls.from_provider_usage(raw_usage, read=read)

    @classmethod
    def from_attribute_usage(
        cls,
        raw_usage: Any,
        *,
        nested_aliases: Mapping[str, tuple[str, ...]] | None = None,
    ) -> "TokenUsage | None":
        """Normalize an object-style provider usage payload."""

        def read(usage: Any, name: str) -> int | None:
            if nested_aliases is not None and (path := nested_aliases.get(name)) is not None:
                obj: Any = usage
                for part in path:
                    obj = obj.get(part) if isinstance(obj, Mapping) else getattr(obj, part, None)
                if isinstance(obj, int):
                    return obj
            value = getattr(usage, name, None)
            return value if isinstance(value, int) else None

        return cls.from_provider_usage(raw_usage, read=read)

    @property
    def is_empty(self) -> bool:
        return (
            self.input_tokens == 0
            and self.output_tokens == 0
            and self.cache_read_tokens == 0
            and self.cache_write_tokens == 0
            and self.reasoning_tokens == 0
            and self.total_tokens is None
        )

    @property
    def context_tokens(self) -> int:
        """Return the context pressure represented by this usage payload."""
        if self.total_tokens is not None:
            return self.total_tokens
        return self.input_tokens + self.output_tokens

    def annotation(
        self,
        *,
        provider: str | None = None,
        model: str | None = None,
    ) -> dict[str, Any]:
        """Serialize usage into a history annotation payload."""
        annotation = self.model_dump(exclude_none=True)
        annotation["context_tokens"] = self.context_tokens
        if provider is not None:
            annotation["provider"] = provider
        if model is not None:
            annotation["model"] = model
        return annotation


def _read_first(
    raw_usage: Any,
    read: _TokenReader,
    aliases: tuple[str, ...],
) -> int | None:
    for alias in aliases:
        value = read(raw_usage, alias)
        if isinstance(value, int):
            return value
    return None
