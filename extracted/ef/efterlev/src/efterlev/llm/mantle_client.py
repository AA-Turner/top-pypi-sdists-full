"""OpenAI-on-Bedrock adapter for `LLMClient` (the `bedrock-mantle` endpoint).

AWS Bedrock serves OpenAI models (GPT-5.4, GPT-5.5; launched 2026-06-01) on a
dedicated `bedrock-mantle` endpoint that speaks the **OpenAI Responses API**
(`client.responses.create(...)`), NOT the Chat Completions API the direct
`OpenAIClient` uses, and NOT the Bedrock Converse API the Anthropic
`AnthropicBedrockClient` uses. So this is a third client shape:

  - the OpenAI Python SDK, pointed at `https://bedrock-mantle.{region}.api.aws/openai/v1`,
  - authenticated with a **Bedrock API key** (env `AWS_BEARER_TOKEN_BEDROCK`),
  - calling `responses.create(model="openai.gpt-5.4", instructions=system,
    input=user, max_output_tokens=...)`,
  - reading `response.output_text` + `response.usage.{input_tokens,output_tokens}`.

Why a separate backend (`bedrock_openai`) rather than folding into `bedrock`
or `openai`: the transport (Responses API + Mantle base URL + Bedrock key +
region) shares nothing with the Converse path and differs from direct-OpenAI
on auth, base URL, and API surface. Keeping it explicit avoids magic dispatch
on model-ID prefixes.

**Status: wiring shipped at v0.1.216; live accuracy NOT yet maintainer-validated.**
Two things need a real Bedrock key to confirm (the endpoint is brand new and
this environment has none): (1) the exact base-URL path the SDK expects — the
AWS model card lists the operation URL as `.../openai/v1/responses`; the SDK
appends `/responses` to its `base_url`, so we set `.../openai/v1` and leave it
overridable via `EFTERLEV_MANTLE_BASE_URL`; (2) whether gpt-5.4 passes the gap
agent's citation discipline — gpt-5.4 (regular) reliably fabricated empty
`evidence_ids` via direct OpenAI in v0.1.213, and that's a model behavior, not
a transport one, so the same failure is expected here until a tuned prompt
lands. See LIMITATIONS.md "OpenAI on Bedrock (bedrock_openai)".

Non-streaming: the Responses API supports streaming, but since this can't be
verified live yet, we make one blocking call and fire `on_chunk` once with the
final text — the uniform-contract / per-backend-granularity pattern the
Bedrock Converse client already uses (see `llm/base.py`). Streaming is a
follow-up once the transport is validated.

Optional dep: install with `pipx install 'efterlev[openai]'` (the SDK is the
same `openai` package; imported lazily so importing this module is cheap when
the dep is absent).
"""

from __future__ import annotations

import hashlib
import logging
import os
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

# Match the other clients' transient-error envelope so swapping backends
# doesn't change the retry behavior users experience.
_MAX_RETRIES = 3
_INITIAL_DELAY_SECONDS = 1.0
_MAX_DELAY_SECONDS = 60.0


def mantle_base_url(region: str) -> str:
    """Return the `bedrock-mantle` OpenAI base URL for a region.

    The OpenAI SDK appends the operation path (`/responses`) to its
    `base_url`, so we return `.../openai/v1` (the model card lists the full
    operation URL `.../openai/v1/responses`). `EFTERLEV_MANTLE_BASE_URL`
    overrides this entirely — kept so the exact path can be corrected at
    dispatch time without a code change while the endpoint is new.
    """
    override = os.environ.get("EFTERLEV_MANTLE_BASE_URL", "").strip()
    if override:
        return override
    return f"https://bedrock-mantle.{region}.api.aws/openai/v1"


@dataclass
class BedrockOpenAIClient:
    """`LLMClient`-shaped wrapper over OpenAI models on the Bedrock Mantle endpoint."""

    region: str
    api_key: str | None = None
    # Fallback after primary-model retries are exhausted. `None` disables it
    # (same posture as the other clients). Must be a Mantle-served model id.
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
            # A Bedrock API key (long-term, from the Bedrock console). The
            # AWS-standard env var is AWS_BEARER_TOKEN_BEDROCK; accept the
            # explicit param first for tests/injection.
            key = self.api_key or os.environ.get("AWS_BEARER_TOKEN_BEDROCK", "").strip()
            if not key:
                raise AgentError(
                    "AWS_BEARER_TOKEN_BEDROCK is not set. The bedrock_openai backend "
                    "needs a Bedrock API key (generate one in the Bedrock console: "
                    "console.aws.amazon.com/bedrock/home#/api-keys). Export it as "
                    "AWS_BEARER_TOKEN_BEDROCK, or inject a StubLLMClient."
                )
            self._sdk = OpenAI(api_key=key, base_url=mantle_base_url(self.region))
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
                    raise AgentError(f"bedrock_openai (mantle) completion failed: {e}") from e
                if attempt < _MAX_RETRIES - 1:
                    delay = _backoff_delay(attempt)
                    log.warning(
                        "bedrock_openai %s attempt %d/%d failed (%s); retrying in %.2fs",
                        model,
                        attempt + 1,
                        _MAX_RETRIES,
                        type(e).__name__,
                        delay,
                    )
                    self.sleeper(delay)
                else:
                    log.warning(
                        "bedrock_openai %s exhausted %d retries (%s)",
                        model,
                        _MAX_RETRIES,
                        type(e).__name__,
                    )

        if self.fallback_model and self.fallback_model != model:
            log.warning(
                "bedrock_openai falling back from %s to %s after %d failed attempts",
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
                    f"bedrock_openai completion failed on primary ({model}) AND fallback "
                    f"({self.fallback_model}): {e}"
                ) from e

        raise AgentError(
            f"bedrock_openai completion failed after {_MAX_RETRIES} attempts on {model}: "
            f"{last_error}"
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
        """Single Responses-API call + response validation.

        The Responses API takes the system prompt as `instructions` and the
        user content as `input`, caps output via `max_output_tokens`, and
        returns `output_text` (a convenience aggregation of the output items)
        plus `usage.{input_tokens,output_tokens}`. No `temperature` — the
        GPT-5 reasoning family rejects it (same rationale as the other clients).
        """
        client = self._client()
        user_text = "\n".join(m.content for m in messages)

        response = client.responses.create(  # type: ignore[call-overload]
            model=model,
            instructions=system,
            input=user_text,
            max_output_tokens=max_tokens,
        )

        text = _extract_output_text(response)
        served_model = getattr(response, "model", None) or model

        usage = getattr(response, "usage", None)
        input_tokens = int(getattr(usage, "input_tokens", 0) or 0) if usage else 0
        output_tokens = int(getattr(usage, "output_tokens", 0) or 0) if usage else 0

        # Truncation surfaces as status="incomplete" with reason
        # "max_output_tokens" on the Responses API (the analog of OpenAI Chat
        # Completions' finish_reason=="length" / Anthropic's "max_tokens").
        status = getattr(response, "status", None)
        if status == "incomplete":
            details = getattr(response, "incomplete_details", None)
            reason = getattr(details, "reason", None) if details else None
            if reason == "max_output_tokens":
                raise AgentError(
                    f"bedrock_openai response truncated at max_output_tokens={max_tokens}. "
                    "Increase the max_tokens argument the agent passes to _invoke_llm."
                )

        if not text:
            item_types = [
                getattr(i, "type", "?") for i in (getattr(response, "output", None) or [])
            ]
            raise AgentError(
                f"bedrock_openai response had no text content (status={status!r}; "
                f"output item types={item_types}). If the model returned only reasoning "
                "items, the request may need a higher max_tokens or a prompt that elicits "
                "a final message."
            )

        if on_chunk is not None:
            on_chunk(text)

        return LLMResponse(
            text=text,
            model=served_model,
            prompt_hash=prompt_hash,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )


def _extract_output_text(response: Any) -> str:
    """Pull the assistant text out of a Responses-API response.

    `response.output_text` is the SDK's convenience aggregation, but in
    practice it can come back empty even on a `status="completed"` response
    (observed with gpt-5.5 on the Bedrock Mantle endpoint, 2026-06-03) while
    the text is actually present in the structured `output` items. So: prefer
    `output_text`, then fall back to walking `output[].content[].text` for the
    message items. Returns "" if no text is found anywhere (the caller raises a
    diagnostic error listing the output item types).
    """
    direct = getattr(response, "output_text", None)
    if direct:
        return str(direct)

    parts: list[str] = []
    for item in getattr(response, "output", None) or []:
        # Message items carry the user-visible text; reasoning items don't.
        if getattr(item, "type", None) not in (None, "message"):
            continue
        for content in getattr(item, "content", None) or []:
            piece = getattr(content, "text", None)
            if piece:
                parts.append(str(piece))
    return "".join(parts)


def _is_retryable(error: Exception) -> bool:
    """Transient errors → retry; permanent errors → bypass. Mirrors OpenAIClient."""
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
    """Same exponential-backoff-with-full-jitter as the other clients."""
    cap = min(_MAX_DELAY_SECONDS, _INITIAL_DELAY_SECONDS * (2**attempt))
    return random.uniform(0, cap)
