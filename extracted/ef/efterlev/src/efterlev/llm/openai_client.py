"""OpenAI Chat Completions adapter for `LLMClient`.

Mirrors `anthropic_client.py` exactly — same call shape, same retry +
fallback discipline, same on_chunk streaming semantics — so swapping the
backend never changes the agent layer above. Differences are SDK-specific:

  - calls `openai.OpenAI().chat.completions.create(..., stream=True,
    stream_options={"include_usage": True})`,
  - serializes the prompt as `[{role:"system",...},{role:"user",...}]`
    instead of system + messages,
  - uses `max_completion_tokens` (the forward-compatible name for
    GPT-5-family models; the SDK accepts it on older models too),
  - classifies retry-vs-permanent against `openai.*` exception types.

**Status: experimental (v0.1.211).** Quality not yet maintainer-validated
on the 60-KSI eval-harness sweep (the other backends are at 99-100% on
the 5-fixture harness). See LIMITATIONS.md "OpenAI backend: unvalidated"
for the graduation plan. Backend wiring is feature-complete; what's
unproven is whether a given OpenAI model classifies KSIs at parity with
Claude on the labeled fixtures.

Optional dep: install with `pipx install 'efterlev[openai]'`. The SDK is
imported lazily so importing this module is cheap when the dep is absent.
"""

from __future__ import annotations

import hashlib
import logging
import random
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from efterlev.errors import AgentError
from efterlev.llm.base import LLMMessage, LLMResponse

if TYPE_CHECKING:  # pragma: no cover
    from openai import OpenAI

log = logging.getLogger(__name__)


# Match AnthropicClient's budget so swapping backends doesn't change the
# transient-error envelope users experience.
_MAX_RETRIES = 3
_INITIAL_DELAY_SECONDS = 1.0
_MAX_DELAY_SECONDS = 60.0


@dataclass
class OpenAIClient:
    """`LLMClient`-shaped wrapper over the OpenAI Python SDK."""

    api_key: str | None = None
    # Fallback model after primary-model retries are exhausted. `None`
    # disables fallback — same posture as AnthropicClient.
    fallback_model: str | None = None
    sleeper: Callable[[float], None] = field(default=time.sleep, repr=False)
    _sdk: Any = field(default=None, init=False, repr=False)

    def _client(self) -> OpenAI:
        if self._sdk is None:
            try:
                from openai import OpenAI
            except ImportError as e:  # pragma: no cover - guard
                raise AgentError(
                    "openai SDK not installed; install with "
                    "`pipx install 'efterlev[openai]'` or inject a StubLLMClient"
                ) from e
            # Resolution order: explicit param → env var → credentials file
            # (what the shell `/setup` OpenAI path writes). Mirrors
            # AnthropicClient's resolve_anthropic_api_key fallback.
            from efterlev.shell.credentials import resolve_openai_api_key

            key = self.api_key or resolve_openai_api_key()
            if not key:
                raise AgentError(
                    "OPENAI_API_KEY is not set. Export it, run /setup in the "
                    "efterlev shell, or inject a StubLLMClient. (For the "
                    "Anthropic backend, set ANTHROPIC_API_KEY instead.)"
                )
            self._sdk = OpenAI(api_key=key)
        return self._sdk  # type: ignore[no-any-return]

    def complete(
        self,
        *,
        system: str,
        messages: list[LLMMessage],
        model: str,
        max_tokens: int = 4096,
        on_chunk: Callable[[str], None] | None = None,
    ) -> LLMResponse:
        joined = system + "\n".join(m.content for m in messages)
        prompt_hash = hashlib.sha256(joined.encode("utf-8")).hexdigest()

        last_error: Exception | None = None
        for attempt in range(_MAX_RETRIES):
            try:
                return self._one_call(
                    system=system,
                    messages=messages,
                    model=model,
                    max_tokens=max_tokens,
                    prompt_hash=prompt_hash,
                    on_chunk=on_chunk,
                )
            except Exception as e:
                last_error = e
                if not _is_retryable(e):
                    raise AgentError(f"openai completion failed: {e}") from e
                if attempt < _MAX_RETRIES - 1:
                    delay = _backoff_delay(attempt)
                    log.warning(
                        "openai %s attempt %d/%d failed (%s); retrying in %.2fs",
                        model,
                        attempt + 1,
                        _MAX_RETRIES,
                        type(e).__name__,
                        delay,
                    )
                    self.sleeper(delay)
                else:
                    log.warning(
                        "openai %s exhausted %d retries (%s)",
                        model,
                        _MAX_RETRIES,
                        type(e).__name__,
                    )

        if self.fallback_model and self.fallback_model != model:
            log.warning(
                "openai falling back from %s to %s after %d failed attempts",
                model,
                self.fallback_model,
                _MAX_RETRIES,
            )
            try:
                return self._one_call(
                    system=system,
                    messages=messages,
                    model=self.fallback_model,
                    max_tokens=max_tokens,
                    prompt_hash=prompt_hash,
                    on_chunk=on_chunk,
                )
            except Exception as e:
                raise AgentError(
                    f"openai completion failed on primary ({model}) AND fallback "
                    f"({self.fallback_model}): {e}"
                ) from e

        raise AgentError(
            f"openai completion failed after {_MAX_RETRIES} attempts on {model}: {last_error}"
        )

    def _one_call(
        self,
        *,
        system: str,
        messages: list[LLMMessage],
        model: str,
        max_tokens: int,
        prompt_hash: str,
        on_chunk: Callable[[str], None] | None = None,
    ) -> LLMResponse:
        """Single SDK call + response validation.

        Streams unconditionally (`stream=True` + `stream_options=include_usage`)
        to match the AnthropicClient discipline + receive token usage on the
        final chunk. `max_completion_tokens` is the forward-compatible name
        OpenAI introduced with GPT-5; older models accept it too via SDK alias.
        No `temperature` parameter — same rationale as AnthropicClient (newer
        OpenAI reasoning models reject it; downstream pydantic strict-validates
        JSON output).
        """
        client = self._client()
        sdk_messages = [{"role": "system", "content": system}]
        sdk_messages.extend({"role": "user", "content": m.content} for m in messages)

        # SDK overloads constrain `messages` to discriminated TypedDicts keyed by
        # role literals; our untyped dict shape carries the same payload but trips
        # mypy. The shape is checked by tests + the SDK itself at call time.
        stream = client.chat.completions.create(  # type: ignore[call-overload]
            model=model,
            messages=sdk_messages,
            max_completion_tokens=max_tokens,
            stream=True,
            stream_options={"include_usage": True},
        )

        parts: list[str] = []
        input_tokens = 0
        output_tokens = 0
        served_model = model
        finish_reason: str | None = None
        cumulative = ""
        for chunk in stream:
            # Usage is delivered on a terminal "usage chunk" (choices may be []).
            usage = getattr(chunk, "usage", None)
            if usage is not None:
                input_tokens = int(getattr(usage, "prompt_tokens", 0) or 0)
                output_tokens = int(getattr(usage, "completion_tokens", 0) or 0)
            # Model + finish_reason come on regular choice chunks.
            if getattr(chunk, "model", None):
                served_model = chunk.model
            if chunk.choices:
                choice = chunk.choices[0]
                delta = getattr(choice, "delta", None)
                text = getattr(delta, "content", None) if delta is not None else None
                if text:
                    parts.append(text)
                    if on_chunk is not None:
                        cumulative += text
                        on_chunk(cumulative)
                if getattr(choice, "finish_reason", None):
                    finish_reason = choice.finish_reason

        if not parts:
            raise AgentError(
                f"openai response had no text content (finish_reason={finish_reason!r})"
            )

        # Truncation surfaces as `finish_reason == "length"` on OpenAI (matches
        # Anthropic's `stop_reason == "max_tokens"`). Same rationale: agents
        # parse JSON downstream; a truncated response is almost certainly
        # invalid JSON, and surfacing the real cause beats a misleading
        # parser error.
        if finish_reason == "length":
            raise AgentError(
                f"openai response truncated at max_completion_tokens={max_tokens}. "
                "Increase the max_tokens argument the agent passes to _invoke_llm."
            )

        return LLMResponse(
            text="".join(parts),
            model=served_model,
            prompt_hash=prompt_hash,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )


def _is_retryable(error: Exception) -> bool:
    """Transient errors → retry; permanent errors → bypass retry loop.

    Mirrors the Anthropic classifier: rate limits / timeouts / connection
    errors / 5xx are retryable; auth / bad-request / not-found are not.
    Agent-level errors (truncated output, no text blocks) are never retryable.
    """
    if isinstance(error, AgentError):
        return False
    try:
        import openai
    except ImportError:  # pragma: no cover
        return False
    retryable_types: tuple[type[Exception], ...] = (
        openai.RateLimitError,
        openai.APITimeoutError,
        openai.APIConnectionError,
        openai.InternalServerError,
    )
    return isinstance(error, retryable_types)


def _backoff_delay(attempt: int) -> float:
    """Same exponential-backoff-with-full-jitter as the Anthropic client."""
    cap = min(_MAX_DELAY_SECONDS, _INITIAL_DELAY_SECONDS * (2**attempt))
    return random.uniform(0, cap)
