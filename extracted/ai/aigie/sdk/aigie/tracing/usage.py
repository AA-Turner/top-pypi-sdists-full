"""Canonical token/cost usage for span emission.

``Usage`` is the single source of truth for *where* token and cost data live on
the wire. Integrations construct a ``Usage`` from their framework-native usage
object and call ``to_metadata()``; they never hand-build ``prompt_tokens`` /
``completion_tokens`` dicts themselves. This removes the per-integration
decision that previously let an integration place the prompt/completion split
at the payload top level while the ingest mapper read it from metadata, which
silently dropped the split.

The ingest mapper (``aigie.ingest.mapper``) promotes the flat
``prompt_tokens`` / ``completion_tokens`` / cost keys from metadata into the
typed proto fields (and the ``spans`` columns). ``to_metadata`` therefore emits
those flat keys, plus a richer ``token_usage`` object and a ``usage_details``
breakdown (cache / reasoning) that ride along in ``metadata_json``.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

# Keys an upstream framework usage object may use for the same quantity. Order
# matters: the first present, non-None value wins.
_INPUT_KEYS = ("input_tokens", "prompt_tokens")
_OUTPUT_KEYS = ("output_tokens", "completion_tokens")
_CACHE_READ_KEYS = ("cache_read_input_tokens", "cache_read_tokens")
_CACHE_CREATION_KEYS = ("cache_creation_input_tokens", "cache_write_tokens")
_REASONING_KEYS = ("reasoning_tokens",)


def _first_int(source: Mapping[str, object], keys: tuple[str, ...]) -> int:
    """First present key wins. Uses key-presence, not truthiness, so an
    explicit 0 (e.g. a cache-only call with 0 fresh input tokens) is honored
    rather than skipped in favor of a later alias key."""
    for key in keys:
        value = source.get(key)
        if isinstance(value, (int, float)):
            return int(value)
    return 0


@dataclass(frozen=True)
class Usage:
    """Token counts and (optional) costs for one LLM/agent span.

    ``input_tokens`` / ``output_tokens`` are the prompt / completion split.
    ``total_tokens`` defaults to their sum when not supplied explicitly.
    """

    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int | None = None
    cache_read_tokens: int = 0
    cache_creation_tokens: int = 0
    reasoning_tokens: int = 0
    input_cost: float | None = None
    output_cost: float | None = None
    total_cost: float | None = None

    @classmethod
    def from_mapping(
        cls,
        source: Mapping[str, object] | None,
        *,
        cost: Mapping[str, float] | None = None,
    ) -> Usage:
        """Build a ``Usage`` from a framework-native usage dict.

        Accepts either ``input_tokens``/``output_tokens`` (Anthropic / Claude
        Agent SDK) or ``prompt_tokens``/``completion_tokens`` (OpenAI /
        LangChain) naming. ``cost`` may carry ``input_cost`` / ``output_cost`` /
        ``total_cost``.
        """
        source = source or {}
        cost = cost or {}
        total = source.get("total_tokens")
        total_tokens = int(total) if isinstance(total, (int, float)) else None
        return cls(
            input_tokens=_first_int(source, _INPUT_KEYS),
            output_tokens=_first_int(source, _OUTPUT_KEYS),
            total_tokens=total_tokens,
            cache_read_tokens=_first_int(source, _CACHE_READ_KEYS),
            cache_creation_tokens=_first_int(source, _CACHE_CREATION_KEYS),
            reasoning_tokens=_first_int(source, _REASONING_KEYS),
            input_cost=cost.get("input_cost"),
            output_cost=cost.get("output_cost"),
            total_cost=cost.get("total_cost"),
        )

    @property
    def resolved_total_tokens(self) -> int:
        if self.total_tokens is not None:
            return self.total_tokens
        return self.input_tokens + self.output_tokens

    @property
    def has_tokens(self) -> bool:
        return bool(self.input_tokens or self.output_tokens or self.total_tokens)

    def _token_usage(self, total: int) -> dict[str, int | float]:
        token_usage: dict[str, int | float] = {
            "prompt_tokens": self.input_tokens,
            "input_tokens": self.input_tokens,
            "completion_tokens": self.output_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": total,
        }
        if self.input_cost is not None:
            token_usage["input_cost"] = self.input_cost
        if self.output_cost is not None:
            token_usage["output_cost"] = self.output_cost
        if self.total_cost is not None:
            token_usage["estimated_cost"] = self.total_cost
        return token_usage

    def to_metadata(self) -> dict[str, object]:
        """Return the span ``metadata`` fragment carrying this usage.

        The flat ``prompt_tokens`` / ``completion_tokens`` / cost keys are what
        the ingest mapper promotes into the typed proto fields and ``spans``
        columns. ``token_usage`` and ``usage_details`` ride in ``metadata_json``
        for richer downstream reads.

        The token block is emitted only when there are tokens to report, so a
        cost-only or empty ``Usage`` never injects ``prompt_tokens=0`` noise.
        Costs and cache/reasoning detail are emitted independently.
        """
        metadata: dict[str, object] = {}
        if self.has_tokens:
            total = self.resolved_total_tokens
            metadata["prompt_tokens"] = self.input_tokens
            metadata["completion_tokens"] = self.output_tokens
            metadata["total_tokens"] = total
            metadata["token_usage"] = self._token_usage(total)
        if self.input_cost is not None:
            metadata["input_cost"] = self.input_cost
        if self.output_cost is not None:
            metadata["output_cost"] = self.output_cost
        if self.total_cost is not None:
            metadata["total_cost"] = self.total_cost

        if details := self._usage_details():
            metadata["usage_details"] = details
        return metadata

    def _usage_details(self) -> dict[str, int]:
        details: dict[str, int] = {}
        if self.cache_read_tokens:
            details["cache_read_input_tokens"] = self.cache_read_tokens
        if self.cache_creation_tokens:
            details["cache_creation_input_tokens"] = self.cache_creation_tokens
        if self.reasoning_tokens:
            details["reasoning_tokens"] = self.reasoning_tokens
        return details


def llm_span_payload(
    usage: Mapping[str, object] | None,
    *,
    model_id: str | None = None,
    cost: Mapping[str, float] | None = None,
) -> tuple[dict[str, object], dict[str, object]]:
    """``(extras, metadata_updates)`` for an LLM-call span — the one place that
    shapes ``model`` + the prompt/completion/total split onto the wire from a
    framework-normalized usage mapping.

    ``extras`` are top-level wire fields the platform cost enricher prices from;
    ``metadata_updates`` is the canonical :meth:`Usage.to_metadata`. Every
    integration feeds its own usage extraction through here so no integration
    hand-shapes token fields or forgets ``model``.
    """
    extras: dict[str, object] = {}
    if model_id:
        extras["model"] = model_id
    if usage is None:
        return extras, {}
    parsed = Usage.from_mapping(usage, cost=cost)
    extras["prompt_tokens"] = parsed.input_tokens
    extras["completion_tokens"] = parsed.output_tokens
    extras["total_tokens"] = parsed.resolved_total_tokens
    return extras, parsed.to_metadata()
