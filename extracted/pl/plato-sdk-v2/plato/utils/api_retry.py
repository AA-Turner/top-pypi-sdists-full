"""Shared retry logic for rate-limited (HTTP 429) provider API calls.

Moved from ``computer_use_agent.providers.retry`` so SDK consumers (e.g.
``plato.computer_use.remote_computer``) can share it; the agent module
re-exports from here for backward compatibility. Provider-SDK imports are all
deferred, so only the SDKs actually installed need to be present.
"""

from __future__ import annotations

import errno
import json
import logging

from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential_jitter,
)

_log = logging.getLogger(__name__)


# OpenRouter routes each request across multiple upstream providers. When the
# routed attempt fails, it surfaces the upstream failure as an HTTP 400
# "Provider returned error" (openai.BadRequestError) whose error.metadata embeds
# the real upstream errors — including plain rate limits. Retrying re-routes,
# usually to a different provider, so the wrapper is transient whenever any
# embedded upstream error is itself transient (429/5xx or a rate-limit message).
_TRANSIENT_UPSTREAM_CODES = {429, 500, 502, 503, 504, 520, 522, 524}


def _is_transient_openrouter_provider_error(exc: BaseException) -> bool:
    body = getattr(exc, "body", None)
    if not isinstance(body, dict):
        return False
    err = body.get("error", body)
    if not isinstance(err, dict):
        return False
    metadata = err.get("metadata")
    if not isinstance(metadata, dict):
        return False
    upstream = [e for e in metadata.get("previous_errors") or [] if isinstance(e, dict)]
    # The final (routed-to) provider's error lives at the top level: its code on
    # the error object, its raw payload on the metadata.
    upstream.append({"code": err.get("code"), "raw": metadata.get("raw")})
    for e in upstream:
        try:
            code = int(e.get("code"))
        except (TypeError, ValueError):
            code = None
        if code in _TRANSIENT_UPSTREAM_CODES:
            return True
        raw = e.get("raw")
        if isinstance(raw, str) and ("rate limit" in raw.lower() or "rate-limit" in raw.lower()):
            return True
    return False


def is_retryable_error(exc: BaseException) -> bool:
    """Return True if *exc* is a retryable API error (429 or 5xx).

    Each provider SDK surfaces errors differently, so we check for all
    known exception types.  Imports are deferred so that only the SDKs
    actually installed need to be present.
    """
    # Anthropic SDK
    try:
        from anthropic import (
            InternalServerError as AnthropicInternal,
        )
        from anthropic import (
            RateLimitError as AnthropicRateLimit,
        )

        if isinstance(exc, (AnthropicRateLimit, AnthropicInternal)):
            return True
    except ImportError:
        pass

    # OpenAI SDK (also used by ByteDance/OpenRouter via the openai package)
    try:
        from openai import (
            APIStatusError,
        )
        from openai import (
            InternalServerError as OpenAIInternal,
        )
        from openai import (
            RateLimitError as OpenAIRateLimit,
        )

        if isinstance(exc, (OpenAIRateLimit, OpenAIInternal)):
            return True
        # OpenRouter "Provider returned error" 400s that wrap a transient
        # upstream failure (rate limit / 5xx) — retrying re-routes.
        if isinstance(exc, APIStatusError) and _is_transient_openrouter_provider_error(exc):
            return True
    except ImportError:
        pass

    # Google genai SDK — raises ClientError with .code == 429 or 5xx
    try:
        from google.genai.errors import ClientError as GenaiClientError

        if isinstance(exc, GenaiClientError) and exc.code in (429, 500, 502, 503):
            return True
    except ImportError:
        pass

    # Google genai SDK — also raises ServerError for 5xx
    try:
        from google.genai.errors import ServerError as GenaiServerError

        if isinstance(exc, GenaiServerError):
            return True
    except ImportError:
        pass

    # Raw requests (used by the OpenAI provider's _create_response helper)
    if isinstance(exc, RuntimeError) and (
        "429" in str(exc) or "500" in str(exc) or "502" in str(exc) or "503" in str(exc)
    ):
        return True

    # Malformed HTTP-200 body. OpenRouter pads long non-streaming requests with
    # whitespace keep-alives; when the upstream model dies mid-generation the
    # connection closes with a whitespace-only body, and the openai SDK's
    # response.json() raises JSONDecodeError instead of an APIError. The status
    # was 200, so neither the SDK nor the 429/5xx checks above retry it.
    if isinstance(exc, json.JSONDecodeError):
        return True

    # Plato VM SDK — desktop-agent calls through the sims proxy. A 502/503 means
    # the proxy could not reach the agent process on the VM (briefly pegged or
    # restarting): the request never executed, so replaying is safe for ALL
    # actions including type/click. Deliberately NOT 504/timeouts — those can
    # mean the action DID execute, and a blind replay would double-type.
    try:
        from plato.sims.ubuntu_vm.errors import APIError as VMAPIError

        if isinstance(exc, VMAPIError) and getattr(exc, "status_code", None) in (
            502,
            503,
        ):
            return True
    except ImportError:
        pass

    # Transient socket-layer failures from the agent VM. Use errno module
    # constants — the integer values differ across platforms (Linux vs macOS).
    #   ENETUNREACH — agent VM briefly lost route to the API host
    #   ECONNRESET  — peer reset mid-request
    #   ETIMEDOUT   — connect/read timeout from the kernel
    # All three are recoverable by retrying through tenacity's backoff
    # (bounded at 6 attempts, no infinite loop).
    _RETRYABLE_OS_ERRNOS = {errno.ENETUNREACH, errno.ECONNRESET, errno.ETIMEDOUT}
    if isinstance(exc, OSError) and getattr(exc, "errno", None) in _RETRYABLE_OS_ERRNOS:
        return True

    return False


# Keep backward-compatible alias
is_rate_limit_error = is_retryable_error


api_retry = retry(
    retry=retry_if_exception(is_retryable_error),
    wait=wait_exponential_jitter(initial=1, max=60, jitter=5),
    stop=stop_after_attempt(6),
    before_sleep=before_sleep_log(_log, logging.WARNING),
    reraise=True,
)
