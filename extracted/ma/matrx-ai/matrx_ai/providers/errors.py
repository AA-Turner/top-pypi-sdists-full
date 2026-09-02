"""
Centralized error handling for AI provider APIs.

Architecture:
    1. Each provider has a top-level classify_<provider>_error() function.
    2. Inside each classifier, individual _handle_<situation>() functions
       handle specific error types. This makes behavior easy to adjust per-error.
    3. RetryableError carries everything the executor and emitter need:
       - error_type / message / status_code for logging and persistence
       - is_retryable + retry_after for the retry loop
       - user_message for the frontend (plain English, actionable)
    4. Recovery philosophy:
       - Transient failures (network, rate limit, 5xx): intelligent retry with backoff
       - Fixable settings errors (e.g., streaming override): fix + warn loudly
       - Unfixable settings errors (e.g., context overflow): fail immediately, never
         silently alter the user's request in a way that changes the task
"""

from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

import httpx
from matrx_utils import vcprint

if TYPE_CHECKING:
    from matrx_ai.config import TokenUsage


# ---------------------------------------------------------------------------
# Core data structure
# ---------------------------------------------------------------------------


@dataclass
class RetryableError:
    error_type: str
    message: str
    status_code: int | None = None
    retry_after: float | None = None
    is_retryable: bool = True
    user_message: str = "The AI service is temporarily unavailable. Retrying..."
    details: dict[str, object] = field(default_factory=dict)
    retry_schedule: tuple[float, ...] | None = None

    def get_backoff_delay(self, attempt: int) -> float:
        if self.retry_schedule:
            if attempt < len(self.retry_schedule):
                return self.retry_schedule[attempt]
            return self.retry_schedule[-1]
        if self.retry_after:
            return self.retry_after
        return min(2**attempt, 30)


# ---------------------------------------------------------------------------
# Billed-usage capture on terminal-failure paths
# ---------------------------------------------------------------------------
# A provider bills us the instant a call starts; the charge stands even when
# the call then FAILS (raised error, ``response.failed``, an incomplete or a
# mid-stream break) or is CANCELLED in-flight. The orchestrator historically
# recorded usage ONLY on a successful provider return, so a failed cx_request
# carried ``cost=0`` while we were really billed — the exact gap that let
# mid-flight API rejections go un-costed (per the cost-tracking incident).
#
# The convention (mirrors the ``error_info`` one): a provider that can see
# billed ``TokenUsage`` on a terminal-failure / cancel path stamps it onto the
# exception with ``attach_billed_usage()``; the orchestrator harvests it with
# ``get_billed_usage()`` on its failure / cancel finalizers and records it via
# ``request.add_usage(...)`` so the failed row carries real cost. Provider-
# agnostic: ANY provider that attaches gets recorded, no orchestrator change.
#
# LAYER 2 — the net for a FORGETFUL provider. All nine providers implement the
# convention above today, but nothing forces the tenth to. Layer 1 is invisible
# when it is simply never called: a provider that raises without ever looking at
# billing is indistinguishable, downstream, from one that genuinely had nothing
# to bill — both produce ``get_billed_usage() is None`` and a $0 failed row.
# So every helper below marks the exception as BILLING-CHECKED, and
# ``UnifiedAIClient.execute`` screams when a wire-engaged failure comes back
# unchecked. Extinction is layered: layer 1 captures the cost, layer 2 makes a
# missing layer-1 loud instead of silent.

_BILLED_USAGE_ATTR = "_matrx_billed_usage"
_BILLING_CHECKED_ATTR = "_matrx_billing_checked"
_COMPLETED_RESPONSE_ATTR = "_matrx_completed_response"


def mark_billing_checked(exc: BaseException) -> None:
    """Record that a provider adapter inspected billing for this exception.

    Set by every attach/accumulate helper — including when there was nothing to
    attach, which is the whole point: "the provider looked and there was no
    billed usage" must be distinguishable from "no provider ever looked."
    Best-effort; an exception that rejects attribute assignment is swallowed.
    """
    try:
        setattr(exc, _BILLING_CHECKED_ATTR, True)
    except Exception:
        pass


def was_billing_checked(exc: BaseException | None) -> bool:
    """True when some provider adapter ran billing capture for this exception."""
    if exc is None:
        return False
    return bool(getattr(exc, _BILLING_CHECKED_ATTR, False))


# Top-level packages whose exceptions can only come from a provider SDK or the
# HTTP client underneath it — i.e. the wire was engaged and we may already have
# been billed. Deliberately an ALLOWLIST: an unknown module means "don't know",
# and layer 2 stays quiet rather than crying wolf on our own pre-flight errors.
_WIRE_EXC_MODULES: frozenset[str] = frozenset(
    {
        "httpx", "httpcore", "aiohttp", "urllib3", "requests", "ssl", "socket",
        "openai", "anthropic", "google", "groq", "together", "cerebras",
        "replicate", "elevenlabs", "huggingface_hub", "xai_sdk",
    }
)


# Statuses the provider returns INSTEAD OF running inference. A 401 or a 400 is
# a rejection, not a charge; alarming on them would put a red line in the log on
# every bad API key and every malformed schema, which is precisely how an alarm
# gets trained into background noise. 429 belongs here too: a rate-limit refusal
# is a pre-inference rejection. 5xx does NOT — a 500 can land after generation.
_PRE_INFERENCE_STATUSES: frozenset[int] = frozenset(
    {400, 401, 402, 403, 404, 405, 409, 413, 422, 429}
)

# Never reached a server, so nothing can have been billed. Note the ORDER of the
# checks in ``wire_was_engaged``: several of these are httpx.HTTPError subclasses,
# so they must be excluded BEFORE the positive httpx test.
_NEVER_SENT_EXC = (
    httpx.ConnectError,
    httpx.ConnectTimeout,
    httpx.UnsupportedProtocol,
    httpx.InvalidURL,
    httpx.TooManyRedirects,
    ConnectionError,
    OSError,  # covers socket.gaierror (DNS) and friends
)


def wire_was_engaged(exc: BaseException) -> bool:
    """True when this exception plausibly means a provider call was BILLED.

    Layer 2 only screams for these, and the bar is deliberately "we may have been
    charged", not "something went wrong at the network layer". A ``ValueError``
    our own capability gate raised, a 401 from a bad key, a DNS failure — none of
    those cost money, and a red alarm on each is how everyone learns to ignore
    the alarm.

    Excluded outright: interpreter-control exceptions (``SystemExit`` carries an
    int ``.code``, which the status-code sniffer would otherwise read as an HTTP
    status), pre-inference rejection statuses, and never-sent transport errors.
    """
    if isinstance(exc, SystemExit | KeyboardInterrupt):
        return False
    # A bare cancel is EXCLUDED, and not because cancels aren't billed — they are,
    # and layer 1 captures them where it can. It is because layer 2 cannot judge
    # them: `stream_with_billed_usage` is an async generator, so when the task is
    # cancelled while the CONSUMER's loop body is awaiting, the CancelledError is
    # raised in the consumer and the generator only ever sees GeneratorExit. The
    # adapter did everything right and still cannot mark that object. Alarming
    # here would fire on every stop-button press on four providers and say the
    # adapter is broken when it isn't. Making cancels markable is real work,
    # filed in FOUND_DEFECTS; until then layer 2 stays silent rather than wrong.
    if isinstance(exc, asyncio.CancelledError):
        return False
    if isinstance(exc, _NEVER_SENT_EXC):
        return False
    # `_extract_status_code` reads the status off the exception itself. Several
    # SDK errors (httpx.HTTPStatusError, and anything modelled on it) instead
    # hang it on `.response`, so check both — missing it here would let a 400 or
    # 401 fall through to the httpx branch below and fire the alarm on a
    # rejection that cost nothing.
    status = _extract_status_code(exc)  # type: ignore[arg-type]
    if status is None:
        status = getattr(getattr(exc, "response", None), "status_code", None)
        if not isinstance(status, int):
            status = None
    if status is not None:
        return status not in _PRE_INFERENCE_STATUSES
    # A read-timeout means we were mid-flight with a live request — the provider
    # may well have generated (and billed) before we gave up.
    if isinstance(exc, TimeoutError | httpx.HTTPError):
        return True
    root = (type(exc).__module__ or "").split(".", 1)[0]
    return root in _WIRE_EXC_MODULES


def attach_billed_usage(exc: BaseException, usage: TokenUsage | None) -> None:
    """Stamp provider-billed ``TokenUsage`` onto a raised/cancelling exception.

    Safe to call unconditionally: a ``None`` usage is a no-op, and a usage with
    no model name (cost can't be computed) is still attached so the token counts
    are not lost. Never overwrites a usage already attached (the innermost
    capture — closest to the wire — wins). Best-effort: a builtin exception with
    ``__slots__`` that rejects attribute assignment is swallowed — cost capture
    must NEVER mask the real error.
    """
    mark_billing_checked(exc)  # the adapter LOOKED — that fact is the layer-2 signal
    if usage is None:
        return
    try:
        if getattr(exc, _BILLED_USAGE_ATTR, None) is not None:
            return
        setattr(exc, _BILLED_USAGE_ATTR, usage)
    except Exception:
        pass


def accumulate_billed_usage(exc: BaseException, usage: TokenUsage | None) -> None:
    """Add a later paid attempt to usage already attached to ``exc``.

    Provider-hosted continuations can make multiple independently billed calls
    before the final one fails. ``attach_billed_usage`` intentionally preserves
    the innermost capture; this explicit primitive is for the narrower case
    where the provider adapter knows both captures belong to one logical turn.
    """
    mark_billing_checked(exc)
    if usage is None:
        return
    try:
        existing = getattr(exc, _BILLED_USAGE_ATTR, None)
        setattr(exc, _BILLED_USAGE_ATTR, existing + usage if existing is not None else usage)
    except Exception:
        pass


def get_billed_usage(exc: BaseException | None) -> TokenUsage | None:
    """Read any provider-billed ``TokenUsage`` stamped on an exception."""
    if exc is None:
        return None
    return getattr(exc, _BILLED_USAGE_ATTR, None)


def attach_completed_response(exc: BaseException, response: Any) -> None:
    try:
        setattr(exc, _COMPLETED_RESPONSE_ATTR, response)
    except Exception:
        pass


def get_completed_response(exc: BaseException | None) -> Any:
    if exc is None:
        return None
    return getattr(exc, _COMPLETED_RESPONSE_ATTR, None)


def report_billed_usage_capture_failure(provider: str, exc: BaseException) -> None:
    """Scream with request correlation when billing evidence cannot be attached.

    NOTE: ``exc`` here is the CAPTURE failure, not the provider exception that is
    propagating — so this deliberately does NOT mark billing-checked. If capture
    blew up before ``attach_billed_usage`` ran, the propagating exception really
    does carry no billing evidence and layer 2 SHOULD also scream about it.
    """
    request_id = conversation_id = None
    try:
        from matrx_ai.context.app_context import try_get_app_context

        ctx = try_get_app_context()
        if ctx is not None:
            request_id = ctx.request_id
            conversation_id = ctx.conversation_id
    except Exception:
        pass
    vcprint(
        {
            "provider": provider,
            "request_id": request_id,
            "conversation_id": conversation_id,
            "exception_type": f"{type(exc).__module__}.{type(exc).__qualname__}",
            "message": str(exc) or type(exc).__name__,
            "impact": "provider usage may be under-recorded",
        },
        "[Provider Billing] Failed to capture billed usage",
        color="red",
        log_level="ERROR",
    )


def attach_openai_billed_usage(
    exc: BaseException, usage_data: Any, *, model: str | None, api: str
) -> None:
    """Attach billed usage from an OpenAI-style streaming usage object (one with
    ``prompt_tokens`` / ``completion_tokens``) onto a raised/cancelling
    exception, so a mid-flight failure on an OpenAI-compatible provider records
    real cost instead of cost=0. No-op when ``usage_data`` is None. Best-effort —
    cost capture must never mask the real error."""
    mark_billing_checked(exc)
    if usage_data is None:
        return
    try:
        from matrx_ai.config import TokenUsage
        from matrx_ai.config.usage_config import serialize_provider_usage

        attach_billed_usage(
            exc,
            TokenUsage(
                input_tokens=getattr(usage_data, "prompt_tokens", 0) or 0,
                output_tokens=getattr(usage_data, "completion_tokens", 0) or 0,
                matrx_model_name=model,
                provider_model_name=model,
                api=api,
                raw_usage=serialize_provider_usage(usage_data),
            ),
        )
    except Exception:
        pass


def report_unbilled_provider_failure(exc: BaseException, *, provider: str, model: str | None) -> bool:
    """LAYER 2. Scream when a wire-engaged provider failure carries no billing evidence.

    Called once, at the single dispatch chokepoint (``UnifiedAIClient.execute``),
    for every provider. Returns True when it fired.

    Silent on the two honest cases: a failure that never reached the wire (it
    cannot have been billed), and a failure some adapter already inspected — even
    if that inspection found nothing to bill. What is left is precisely the gap
    layer 1 cannot see: a provider that raised from the wire without ever running
    billing capture. That is a code defect in the adapter, not a runtime error,
    and it silently under-reports real spend.

    Best-effort and never raises: a cost alarm must not mask the real error.
    """
    try:
        if was_billing_checked(exc) or not wire_was_engaged(exc):
            return False
        mark_billing_checked(exc)  # one alarm per failure, however many frames unwind
        request_id = conversation_id = None
        try:
            from matrx_ai.context.app_context import try_get_app_context

            ctx = try_get_app_context()
            if ctx is not None:
                request_id = ctx.request_id
                conversation_id = ctx.conversation_id
        except Exception:
            pass
        vcprint(
            {
                "provider": provider,
                "model": model,
                "request_id": request_id,
                "conversation_id": conversation_id,
                "exception_type": f"{type(exc).__module__}.{type(exc).__qualname__}",
                "message": str(exc) or type(exc).__name__,
                "impact": (
                    "this failed attempt records cost=0; if the provider billed it, "
                    "real spend is under-reported"
                ),
                "fix": (
                    f"{provider}'s adapter must call attach_billed_usage() / "
                    "stream_with_billed_usage() on its terminal-failure and cancel paths"
                ),
            },
            "[Provider Billing] LAYER 2 — provider failed at the wire with NO billing capture",
            color="red",
            log_level="ERROR",
        )
        return True
    except Exception:
        return False


def openai_stream_usage(chunk: Any) -> Any | None:
    """Return usage from an OpenAI-compatible stream chunk.

    Most compatible APIs put terminal usage on ``chunk.usage``. Moonshot's
    streaming Chat Completions contract instead puts it on ``choice.usage``.
    Centralising both shapes prevents a provider-specific reader from silently
    recording a successful, billable stream as zero-token usage.
    """
    usage = getattr(chunk, "usage", None)
    if usage:
        return usage
    if isinstance(chunk, dict):
        usage = chunk.get("usage")
        if usage:
            return usage
        choices = chunk.get("choices") or []
    else:
        choices = getattr(chunk, "choices", None) or []
    for choice in choices:
        choice_usage = choice.get("usage") if isinstance(choice, dict) else getattr(choice, "usage", None)
        if choice_usage:
            return choice_usage
    return None


async def stream_with_billed_usage(stream: Any, *, model: str | None, api: str) -> Any:
    """Wrap an OpenAI-compatible chat stream so a mid-iteration failure still
    carries cost. Tracks the running ``chunk.usage`` and, if the stream raises
    (safety block mid-stream, network drop, client disconnect → ``CancelledError``,
    shutdown), stamps the last-seen billed usage onto the exception before
    re-raising. Drop-in: ``async for chunk in stream_with_billed_usage(stream,
    model=model, api="groq")`` — the provider's own loop body is unchanged, this
    only adds the failure-path capture so a new provider can't reintroduce the gap.
    Usage may be on either ``chunk.usage`` or ``choice.usage``; both are part
    of the OpenAI-compatible ecosystem."""
    usage_data = None
    try:
        async for chunk in stream:
            u = openai_stream_usage(chunk)
            if u:
                usage_data = u
            yield chunk
    except BaseException as exc:
        attach_openai_billed_usage(exc, usage_data, model=model, api=api)
        raise


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _extract_status_code(exception: Exception) -> int | None:
    for attr in ("status_code", "code", "http_status", "status"):
        val = getattr(exception, attr, None)
        if isinstance(val, int):
            return val
    return None


def _resolve_exc(module, name: str) -> type | None:
    """Resolve an exception class by name on a provider SDK, tolerant of churn.

    Provider SDKs occasionally rearrange their public exception surface — a
    class is present in one minor version, moved to a private submodule the
    next. ``isinstance(exc, sdk.Foo)`` raises ``AttributeError`` mid-classify
    if the name has moved, masking the real provider error and crashing the
    request. This helper looks up the class on the public module first, then
    on the private ``_exceptions`` submodule, then gives up. Callers should
    treat ``None`` as "skip this branch" and let the status-code fallback
    classify by HTTP code.
    """
    cls = getattr(module, name, None)
    if isinstance(cls, type):
        return cls
    private = getattr(module, "_exceptions", None)
    if private is not None:
        cls = getattr(private, name, None)
        if isinstance(cls, type):
            return cls
    return None


def _isinstance_opt(exception: Exception, cls: type | None) -> bool:
    return cls is not None and isinstance(exception, cls)


def _extract_error_body(exception: Exception) -> dict[str, object]:
    """Pull the parsed JSON error body off an SDK exception when available."""
    try:
        body = getattr(exception, "body", None)
        if isinstance(body, dict):
            error_obj = body.get("error", body)
            if isinstance(error_obj, dict):
                return {
                    "type": error_obj.get("type", ""),
                    "message": error_obj.get("message", str(exception)),
                }
            return {"type": "", "message": str(exception)}
        details = getattr(exception, "details", None)
        if isinstance(details, dict):
            return {
                "type": details.get("status", ""),
                "message": details.get("message", str(exception)),
            }
    except Exception:
        pass
    return {"type": "", "message": str(exception)}


def _extract_retry_after(exception: Exception) -> float | None:
    """Parse provider retry/reset duration headers from the response."""
    try:
        response = getattr(exception, "response", None)
        if response is None:
            return None
        headers = getattr(response, "headers", None)
        if headers is None or not hasattr(headers, "get"):
            return None

        retry_ms = headers.get("retry-after-ms")
        if retry_ms:
            try:
                return float(retry_ms) / 1000.0
            except (TypeError, ValueError):
                pass

        retry_s = headers.get("retry-after")
        if retry_s:
            try:
                return float(retry_s)
            except (TypeError, ValueError):
                pass

        # Together reports the time remaining in the current per-second
        # request window as x-ratelimit-reset. It may be a bare seconds value
        # or a compact duration such as "850ms" / "2s".
        reset = headers.get("x-ratelimit-reset")
        if reset:
            value = str(reset).strip().lower()
            multipliers = (("ms", 0.001), ("s", 1.0), ("m", 60.0))
            for suffix, multiplier in multipliers:
                if value.endswith(suffix):
                    try:
                        return float(value[: -len(suffix)]) * multiplier
                    except (TypeError, ValueError):
                        break
            else:
                try:
                    return float(value)
                except (TypeError, ValueError):
                    pass
    except Exception:
        pass

    return None


# ---------------------------------------------------------------------------
# Individual error handlers — one function per distinct situation
# ---------------------------------------------------------------------------

# -- Authentication / authorization ----------------------------------------


def _handle_auth_error(provider: str, message: str, status_code: int) -> RetryableError:
    return RetryableError(
        error_type="auth_error",
        message=message,
        status_code=status_code,
        is_retryable=False,
        user_message=f"{provider} API key is invalid, expired, or missing. Please check your configuration.",
    )


def _handle_permission_error(provider: str, message: str, status_code: int) -> RetryableError:
    return RetryableError(
        error_type="permission_error",
        message=message,
        status_code=status_code,
        is_retryable=False,
        user_message=f"Your {provider} API key does not have permission to access this model or feature.",
    )


# -- Client / request errors (non-retryable, user must fix) ---------------


def _handle_bad_request(provider: str, message: str, body: dict[str, object]) -> RetryableError:
    detail = body.get("message", message)
    return RetryableError(
        error_type="invalid_request",
        message=message,
        status_code=400,
        is_retryable=False,
        user_message=f"{provider} rejected the request: {detail}",
        details=body,
    )


def _handle_not_found(provider: str, message: str) -> RetryableError:
    lowered = message.lower()
    if any(marker in lowered for marker in ("model_archived", "model archived", "is archived", "retired model")):
        return RetryableError(
            error_type="model_retired",
            message=message,
            status_code=404,
            is_retryable=False,
            user_message=(
                f"The configured {provider} model has been retired. "
                "Choose an active catalog model before running this agent again."
            ),
            details={"catalog_drift": True},
        )
    return RetryableError(
        error_type="not_found",
        message=message,
        status_code=404,
        is_retryable=False,
        user_message=f"The requested {provider} model or endpoint was not found. It may have been retired or renamed.",
    )


def _handle_request_too_large(provider: str, message: str) -> RetryableError:
    return RetryableError(
        error_type="request_too_large",
        message=message,
        status_code=413,
        is_retryable=False,
        user_message=(
            f"The request exceeds {provider}'s maximum size limit. "
            "Try shortening the conversation or removing large attachments."
        ),
    )


def _handle_billing_error(
    provider: str, message: str, status_code: int = 402
) -> RetryableError:
    return RetryableError(
        error_type="billing_error",
        message=message,
        status_code=status_code,
        is_retryable=False,
        user_message=f"There is a billing issue with the {provider} account. Please check your plan and payment details.",
    )


def _handle_unprocessable(provider: str, message: str, body: dict[str, object]) -> RetryableError:
    detail = body.get("message", message)
    return RetryableError(
        error_type="unprocessable_request",
        message=message,
        status_code=422,
        is_retryable=False,
        user_message=f"{provider} could not process the request: {detail}",
        details=body,
    )


def _handle_conflict(provider: str, message: str) -> RetryableError:
    return RetryableError(
        error_type="conflict",
        message=message,
        status_code=409,
        is_retryable=False,
        user_message=f"A conflict occurred with the {provider} request. Please try again.",
    )


# -- Rate limiting (retryable with backoff) --------------------------------


def _handle_rate_limit(provider: str, message: str, retry_after: float | None) -> RetryableError:
    # Providers commonly use HTTP 429 for both a transient traffic limit and a
    # permanently exhausted/suspended account. Retrying the latter only burns
    # the request's retry budget and masks the actionable billing failure.
    quota_markers = (
        "insufficient balance",
        "insufficient credit",
        "insufficient quota",
        "exceeded_current_quota",
        "billing hard limit",
        "account is suspended",
        "account suspended",
    )
    if any(marker in message.lower() for marker in quota_markers):
        return RetryableError(
            error_type="billing_error",
            message=message,
            status_code=429,
            is_retryable=False,
            user_message=(
                f"The {provider} account has insufficient balance or is suspended. "
                "Add credits or check the provider plan, then try again."
            ),
        )
    delay = retry_after or 10.0
    return RetryableError(
        error_type="rate_limit",
        message=message,
        status_code=429,
        retry_after=delay,
        is_retryable=True,
        user_message=(f"{provider} rate limit reached. Retrying in {delay:.0f} seconds..."),
    )


def _moonshot_error_details(exception: Exception) -> tuple[int | None, str, str, dict[str, object]]:
    status_code = _extract_status_code(exception)
    body = _extract_error_body(exception)
    provider_type = str(body.get("type") or "").lower()
    provider_message = str(body.get("message") or str(exception))
    return status_code, provider_type, provider_message, {
        "provider": "moonshot",
        "provider_error_type": provider_type or None,
    }


def classify_moonshot_error(exception: Exception) -> RetryableError:
    """Normalize Moonshot's documented `{error: {type, message}}` responses."""
    common = classify_common_error(exception, "Moonshot")
    if common is not None:
        return common

    status_code, provider_type, provider_message, details = _moonshot_error_details(exception)
    retry_after = _extract_retry_after(exception)

    if provider_type == "content_filter":
        result = _handle_content_filter("Moonshot", provider_message)
    elif provider_type in {"invalid_authentication_error", "incorrect_api_key_error"}:
        result = _handle_auth_error("Moonshot", provider_message, 401)
    elif provider_type == "permission_denied_error":
        result = _handle_permission_error("Moonshot", provider_message, 403)
    elif provider_type in {"resource_not_found", "resource_not_found_error"}:
        result = _handle_not_found("Moonshot", provider_message)
    elif provider_type == "exceeded_current_quota_error":
        result = RetryableError(
            error_type="billing_error",
            message=provider_message,
            status_code=429,
            is_retryable=False,
            user_message=(
                "The Moonshot account balance or token quota is exhausted. "
                "Add credit or use another provider."
            ),
        )
    elif provider_type == "rate_limit_reached_error":
        # Moonshot distinguishes a traffic limit from engine overload and
        # quota exhaustion.  Retrying a traffic limit without a provider wait
        # hint just consumes the request retry budget, so wait only when the
        # API explicitly tells us when the next attempt is allowed.
        if retry_after is None:
            result = RetryableError(
                error_type="rate_limit",
                message=provider_message,
                status_code=429,
                is_retryable=False,
                user_message="Moonshot rate limit reached. Please wait and try again.",
            )
        else:
            result = _handle_rate_limit("Moonshot", provider_message, retry_after)
    elif provider_type == "engine_overloaded_error":
        result = _handle_overloaded("Moonshot", provider_message, 429)
    elif provider_type == "client_closed_request" or status_code == 499:
        result = RetryableError(
            error_type="provider_request_cancelled",
            message=provider_message,
            status_code=499,
            is_retryable=False,
            user_message="The provider connection closed before completion. Please try again.",
        )
    elif provider_type == "invalid_request_error" or status_code == 400:
        if any(marker in provider_message.lower() for marker in ("context", "token limit", "too long")):
            result = _handle_context_length_exceeded("Moonshot", provider_message)
        else:
            result = _handle_bad_request("Moonshot", provider_message, {"message": provider_message})
    elif status_code == 401:
        result = _handle_auth_error("Moonshot", provider_message, 401)
    elif status_code == 403:
        result = _handle_permission_error("Moonshot", provider_message, 403)
    elif status_code == 404:
        result = _handle_not_found("Moonshot", provider_message)
    elif status_code == 429:
        # SDK versions do not always expose Moonshot's JSON body. Preserve the
        # billing/suspension recognition available in its message before using
        # the conservative traffic-limit fallback.
        classified_rate_limit = _handle_rate_limit("Moonshot", provider_message, retry_after)
        if classified_rate_limit.error_type == "billing_error":
            result = classified_rate_limit
        elif retry_after is None:
            result = RetryableError(
                error_type="rate_limit",
                message=provider_message,
                status_code=429,
                is_retryable=False,
                user_message="Moonshot rate limit reached. Please wait and try again.",
            )
        else:
            result = classified_rate_limit
    elif status_code == 504:
        result = _handle_timeout("Moonshot", provider_message)
    elif status_code is not None and status_code >= 500:
        result = _handle_server_error("Moonshot", provider_message, status_code)
    else:
        # Unknown Moonshot responses are still a stable provider failure, never
        # an opaque `unknown_error` presented to the user.
        result = RetryableError(
            error_type="provider_error",
            message=provider_message,
            status_code=status_code,
            is_retryable=False,
            user_message="Moonshot could not complete this request. Please try again.",
        )
    result.details.update({key: value for key, value in details.items() if value is not None})
    return result


# -- Server / transient errors (retryable) --------------------------------


def _handle_server_error(provider: str, message: str, status_code: int) -> RetryableError:
    return RetryableError(
        error_type="server_error",
        message=f"{provider} internal server error ({status_code}): {message}",
        status_code=status_code,
        retry_after=5.0,
        is_retryable=True,
        user_message=f"{provider} is experiencing an internal error. Retrying automatically...",
    )


def _handle_overloaded(provider: str, message: str, status_code: int) -> RetryableError:
    schedule = (2.0, 5.0, 10.0, 30.0, 60.0)
    return RetryableError(
        error_type="provider_overloaded",
        message=f"{provider} is temporarily overloaded ({status_code})",
        status_code=status_code,
        retry_after=None,
        is_retryable=True,
        user_message=(
            f"{provider} is temporarily overloaded due to high demand. "
            "We are waiting and retrying automatically."
        ),
        retry_schedule=schedule,
        details={
            "provider": provider.lower(),
            "retry_schedule": list(schedule),
            "retry_strategy": "provider_overload_wait_then_suspend",
        },
    )


def _handle_timeout(provider: str, message: str) -> RetryableError:
    return RetryableError(
        error_type="provider_timeout",
        message=message,
        status_code=504,
        retry_after=10.0,
        is_retryable=True,
        user_message=(
            f"The request to {provider} timed out. "
            "This can happen with very long prompts or high token limits. Retrying..."
        ),
    )


def _handle_connection_error(provider: str, message: str) -> RetryableError:
    return RetryableError(
        error_type="connection_error",
        message=message,
        retry_after=3.0,
        is_retryable=True,
        user_message=f"Could not connect to {provider}. Checking connection and retrying...",
    )


# -- Provider-specific client-side SDK errors (non-retryable) ---------------


def _handle_anthropic_streaming_required(message: str) -> RetryableError:
    return RetryableError(
        error_type="streaming_required",
        message=message,
        is_retryable=False,
        user_message=(
            "The requested output token limit is too high for a non-streaming request. "
            "Please either reduce the max tokens setting or enable streaming."
        ),
    )


def _handle_content_filter(provider: str, message: str) -> RetryableError:
    return RetryableError(
        error_type="content_filtered",
        message=message,
        is_retryable=False,
        user_message=f"{provider} blocked this request due to content policy restrictions.",
    )


def _handle_context_length_exceeded(provider: str, message: str) -> RetryableError:
    return RetryableError(
        error_type="context_length_exceeded",
        message=message,
        is_retryable=False,
        user_message=(
            f"The conversation is too long for the selected {provider} model's context window. "
            "Please shorten the conversation or switch to a model with a larger context window."
        ),
    )


# ---------------------------------------------------------------------------
# Fallback classifiers (string-based, last resort)
# ---------------------------------------------------------------------------

# Bare digit codes MUST be digit-bounded. A naive ``"429" in message`` false-
# positives on timestamps like ``2026-08-04 10:31:17.542904+00`` (microseconds
# contain ``429``), which misclassified a missing ``history.row_versions``
# partition as a Replicate rate limit and retried a paid ``async_run``.
def _has_http_code(text: str, *codes: int) -> bool:
    """True if ``text`` contains any of ``codes`` not embedded in a longer number."""
    if not codes:
        return False
    alternation = "|".join(str(code) for code in codes)
    return re.search(rf"(?<!\d)(?:{alternation})(?!\d)", text) is not None


def _fallback_classify(error_str: str, provider: str) -> RetryableError:
    s = error_str.lower()

    if any(marker in s for marker in ("model_archived", "model archived", "is archived", "retired model")):
        return _handle_not_found(provider, error_str)

    if any(x in s for x in ("context_length_exceeded", "context window", "maximum context")):
        return _handle_context_length_exceeded(provider, error_str)

    if any(x in s for x in ("content_filter", "content_policy", "safety", "blocked")):
        return _handle_content_filter(provider, error_str)

    if _has_http_code(s, 401, 403) or any(
        x in s for x in ("invalid api key", "unauthorized", "forbidden")
    ):
        return _handle_auth_error(provider, error_str, 401)

    if _has_http_code(s, 400) or any(x in s for x in ("invalid request", "bad request")):
        return _handle_bad_request(provider, error_str, {"message": error_str})

    if _has_http_code(s, 429) or any(
        x in s for x in ("rate limit", "quota", "too many requests")
    ):
        return _handle_rate_limit(provider, error_str, retry_after=10.0)

    if any(x in s for x in ("timeout", "timed out", "deadline")):
        return _handle_timeout(provider, error_str)

    if any(x in s for x in ("connection", "network", "dns", "refused")):
        return _handle_connection_error(provider, error_str)

    if "overloaded" in s or _has_http_code(s, 529):
        return _handle_overloaded(provider, error_str, 529)

    # Generic 5xx / transient server failures. Reached only as a last resort
    # (no SDK type or status attribute matched), e.g. a provider error that was
    # re-raised as a bare Exception carrying the HTTP code in its message. These
    # are transient and retryable — without this branch they fell through to
    # ``unknown_error``, mislabelling a routine 503/500 as an unknown failure.
    if _has_http_code(s, 500, 502, 503, 504) or any(
        x in s
        for x in (
            "internal server",
            "server error",
            "service unavailable",
            "unavailable",
            "bad gateway",
            "gateway timeout",
        )
    ):
        if _has_http_code(s, 504) or "gateway timeout" in s:
            return _handle_timeout(provider, error_str)
        status = (
            503
            if (_has_http_code(s, 503) or "unavailable" in s)
            else (502 if (_has_http_code(s, 502) or "bad gateway" in s) else 500)
        )
        return _handle_server_error(provider, error_str, status)

    return RetryableError(
        error_type="unknown_error",
        message=error_str,
        retry_after=5.0,
        is_retryable=True,
        user_message=f"An unexpected {provider} error occurred. Retrying...",
    )


# ---------------------------------------------------------------------------
# Internal-bug guard — our own exception is NEVER a provider error
# ---------------------------------------------------------------------------

# Python built-in exception types that mean OUR OWN code is broken (a defect in
# the matrx stack), never a provider-side condition. A provider SDK raises its own
# typed errors (ClientError / APIError / ...) or an httpx transport error — it does
# NOT raise a bare AttributeError/TypeError from inside our request-building or
# stream-parsing code. When one of these reaches a provider error classifier it is
# because the provider's broad ``except Exception`` caught an exception from OUR
# code and is about to launder it into a retryable ``unknown_error``. That is always
# wrong twice over: the call can never succeed on retry (it is deterministic — we
# burned paid retries for nothing, e.g. the CaptureEmitter ``send_reasoning_state``
# gap), and mislabelling it as ``google.unknown_error`` hides our defect behind the
# provider's name in ops-triage so nobody ever fixes it.
_INTERNAL_BUG_EXCEPTIONS = (
    AttributeError,
    TypeError,
    NameError,
    IndexError,
    KeyError,
    UnboundLocalError,
    ImportError,
    SyntaxError,
    IndentationError,
    RecursionError,
    NotImplementedError,
    AssertionError,
)

# Modules whose exceptions mean OUR INFRASTRUCTURE failed — the database, its
# driver, or the ORM on top of it. Matched by walking the exception class's MRO
# module names, so matrx-ai needs no import of (and no dependency on) matrx-orm,
# asyncpg, or psycopg — the host injects those.
#
# Same laundering hazard as the built-ins above, one layer down and far more
# damaging. A provider call is wrapped in a broad ``except Exception``; an agent
# persisting its result hits a DB failure INSIDE that block; the DB error is
# then reported as "An unexpected Google error occurred. Retrying...". The 2026-08
# outage is the case in point: history.row_versions ran out of partitions, so
# every write to a versioned table raised IntegrityError — and podcast, image,
# and TTS stages all reported it as five different providers being flaky
# simultaneously, while the real message ("no partition of relation
# row_versions found for row") never reached a human. Retrying is also pure
# waste: the DB is down for everyone, and no provider retry can fix it.
_INFRASTRUCTURE_ERROR_MODULES = (
    "matrx_orm",
    "asyncpg",
    "psycopg",
    "psycopg2",
    "sqlalchemy",
)


def _infrastructure_module(exception: Exception) -> str | None:
    for klass in type(exception).__mro__:
        root = (getattr(klass, "__module__", "") or "").split(".", 1)[0]
        if root in _INFRASTRUCTURE_ERROR_MODULES:
            return root
    return None


def classify_internal_error(exception: Exception, provider: str) -> RetryableError | None:
    """Return a NON-retryable internal-bug classification, or None if not ours.

    Called at the top of every provider classifier so an exception from the matrx
    stack is surfaced as our own bug (``matrx_internal_error``, non-retryable)
    instead of being laundered into a retryable provider ``unknown_error``.
    """
    # Message sanitation is a local preflight gate: no provider connection was
    # attempted, and sending the same malformed message list again cannot help.
    # Keep this import local so the provider error module does not participate
    # in config's import graph.
    from matrx_ai.config.message_config import MessageSanitizationError

    if isinstance(exception, MessageSanitizationError):
        return RetryableError(
            error_type="message_sanitization_error",
            message=str(exception) or type(exception).__name__,
            is_retryable=False,
            details={"exception": type(exception).__qualname__},
            user_message=(
                "This agent has no non-empty message to send. Add the required "
                "input and run it again; no AI provider request was attempted."
            ),
        )

    # Catalog routing fails before a provider request can start. It is a
    # deterministic platform configuration error, so retrying cannot help and
    # calling it an ``unknown_error`` hides the exact model/offering defect.
    from matrx_ai.catalog.errors import CatalogRoutingError

    if isinstance(exception, CatalogRoutingError):
        detail = str(exception).strip() or type(exception).__name__
        return RetryableError(
            error_type="matrx_catalog_error",
            message=detail,
            is_retryable=False,
            details={"exception": type(exception).__qualname__},
            user_message=(
                "This AI step is configured with a model route that is no longer "
                f"available. The configuration error has been recorded. {detail}"
            ),
        )

    if isinstance(exception, _INTERNAL_BUG_EXCEPTIONS):
        return RetryableError(
            error_type="matrx_internal_error",
            message=str(exception) or type(exception).__name__,
            is_retryable=False,
            user_message=(
                "An internal error occurred while processing the request "
                f"(a bug in our code, not a {provider} failure). It has been recorded."
            ),
        )

    infra = _infrastructure_module(exception)
    if infra is not None:
        # Preserve the REAL message verbatim — it names the table/constraint and
        # is the only thing that makes the failure diagnosable.
        detail = str(exception).strip() or type(exception).__name__
        return RetryableError(
            error_type="matrx_infrastructure_error",
            message=detail,
            is_retryable=False,
            details={"infrastructure": infra, "exception": type(exception).__qualname__},
            user_message=(
                "Our database is not accepting writes right now, so this step could "
                f"not be saved (this is NOT a {provider} failure). "
                f"Underlying error: {detail}"
            ),
        )
    return None


def classify_common_error(exception: Exception, provider: str) -> RetryableError | None:
    """Classify exceptions that mean the same thing for every provider.

    Raw ``httpx`` transport failures can escape provider SDK wrappers while a
    response stream is being consumed. Their string representation is often
    empty (notably ``httpx.ReadError``), so string-based fallback classification
    used to produce a retryable ``unknown_error`` with a blank message. Preserve
    the typed transport meaning and always provide a useful diagnostic.
    """
    internal = classify_internal_error(exception, provider)
    if internal is not None:
        return internal

    exception_name = f"{type(exception).__module__}.{type(exception).__qualname__}"
    message = str(exception).strip() or type(exception).__name__
    result: RetryableError | None = None
    if isinstance(exception, httpx.TimeoutException | TimeoutError):
        result = _handle_timeout(provider, message)
    elif isinstance(exception, httpx.TransportError | ConnectionError):
        result = _handle_connection_error(provider, message)

    if result is not None:
        result.details.update(
            {
                "provider": provider.lower(),
                "transport_exception": exception_name,
            }
        )
    return result


# ============================================================================
# ANTHROPIC
# ============================================================================


def classify_anthropic_error(exception: Exception) -> RetryableError:
    common = classify_common_error(exception, "Anthropic")
    if common is not None:
        return common

    # SDK client-side ValueError (streaming required)
    if isinstance(exception, ValueError) and "Streaming is required" in str(exception):
        return _handle_anthropic_streaming_required(str(exception))

    # Import Anthropic exception types locally to avoid hard dependency at module level
    try:
        import anthropic
    except ImportError:
        status_code = _extract_status_code(exception)
        if status_code is not None:
            return _classify_anthropic_by_status(status_code, exception)
        return _fallback_classify(str(exception), "Anthropic")

    retry_after = _extract_retry_after(exception)
    body = _extract_error_body(exception)

    if isinstance(exception, anthropic.AuthenticationError):
        return _handle_auth_error("Anthropic", str(exception), 401)

    if isinstance(exception, anthropic.PermissionDeniedError):
        return _handle_permission_error("Anthropic", str(exception), 403)

    if isinstance(exception, anthropic.BadRequestError):
        msg = str(exception)
        if "credit balance is too low" in msg.lower():
            # Anthropic reports exhausted prepaid credit as
            # invalid_request_error/HTTP 400 rather than HTTP 402. It is an
            # account-routing failure, not a malformed user request.
            return _handle_billing_error("Anthropic", msg, 400)
        if "context_length" in msg.lower() or "too many tokens" in msg.lower():
            return _handle_context_length_exceeded("Anthropic", msg)
        return _handle_bad_request("Anthropic", msg, body)

    if isinstance(exception, anthropic.NotFoundError):
        return _handle_not_found("Anthropic", str(exception))

    if _isinstance_opt(exception, _resolve_exc(anthropic, "RequestTooLargeError")):
        return _handle_request_too_large("Anthropic", str(exception))

    if isinstance(exception, anthropic.UnprocessableEntityError):
        return _handle_unprocessable("Anthropic", str(exception), body)

    if isinstance(exception, anthropic.RateLimitError):
        return _handle_rate_limit("Anthropic", str(exception), retry_after)

    if _isinstance_opt(exception, _resolve_exc(anthropic, "OverloadedError")):
        return _handle_overloaded("Anthropic", str(exception), 529)

    if isinstance(exception, anthropic.APITimeoutError):
        return _handle_timeout("Anthropic", str(exception))

    if isinstance(exception, anthropic.APIConnectionError):
        return _handle_connection_error("Anthropic", str(exception))

    if isinstance(exception, anthropic.InternalServerError):
        return _handle_server_error(
            "Anthropic", str(exception), getattr(exception, "status_code", 500)
        )

    if isinstance(exception, anthropic.ConflictError):
        return _handle_conflict("Anthropic", str(exception))

    # DeadlineExceededError (504) — a subclass of APIStatusError
    if isinstance(exception, anthropic.APIStatusError):
        return _classify_anthropic_by_status(exception.status_code, exception)

    return _fallback_classify(str(exception), "Anthropic")


def _classify_anthropic_by_status(status_code: int, exception: Exception) -> RetryableError:
    body = _extract_error_body(exception)
    msg = str(exception)
    retry_after = _extract_retry_after(exception)

    if status_code == 400:
        if "credit balance is too low" in msg.lower():
            return _handle_billing_error("Anthropic", msg, 400)
        return _handle_bad_request("Anthropic", msg, body)
    if status_code == 401:
        return _handle_auth_error("Anthropic", msg, 401)
    if status_code == 402:
        return _handle_billing_error("Anthropic", msg)
    if status_code == 403:
        return _handle_permission_error("Anthropic", msg, 403)
    if status_code == 404:
        return _handle_not_found("Anthropic", msg)
    if status_code == 413:
        return _handle_request_too_large("Anthropic", msg)
    if status_code == 429:
        return _handle_rate_limit("Anthropic", msg, retry_after)
    if status_code == 529:
        return _handle_overloaded("Anthropic", msg, 529)
    if status_code == 504:
        return _handle_timeout("Anthropic", msg)
    if status_code >= 500:
        return _handle_server_error("Anthropic", msg, status_code)

    return _fallback_classify(msg, "Anthropic")


# ============================================================================
# OPENAI
# ============================================================================


def classify_openai_error(exception: Exception) -> RetryableError:
    common = classify_common_error(exception, "OpenAI")
    if common is not None:
        return common

    try:
        import openai
    except ImportError:
        status_code = _extract_status_code(exception)
        if status_code is not None:
            return _classify_openai_by_status(status_code, exception)
        return _fallback_classify(str(exception), "OpenAI")

    retry_after = _extract_retry_after(exception)
    body = _extract_error_body(exception)

    if isinstance(exception, openai.AuthenticationError):
        return _handle_auth_error("OpenAI", str(exception), 401)

    if isinstance(exception, openai.PermissionDeniedError):
        return _handle_permission_error("OpenAI", str(exception), 403)

    if isinstance(exception, openai.BadRequestError):
        msg = str(exception)
        if "context_length" in msg.lower() or "maximum context" in msg.lower():
            return _handle_context_length_exceeded("OpenAI", msg)
        if "content_policy" in msg.lower() or "content_filter" in msg.lower():
            return _handle_content_filter("OpenAI", msg)
        return _handle_bad_request("OpenAI", msg, body)

    if isinstance(exception, openai.NotFoundError):
        return _handle_not_found("OpenAI", str(exception))

    if isinstance(exception, openai.UnprocessableEntityError):
        return _handle_unprocessable("OpenAI", str(exception), body)

    if isinstance(exception, openai.RateLimitError):
        return _handle_rate_limit("OpenAI", str(exception), retry_after)

    if isinstance(exception, openai.APITimeoutError):
        return _handle_timeout("OpenAI", str(exception))

    if isinstance(exception, openai.APIConnectionError):
        return _handle_connection_error("OpenAI", str(exception))

    if isinstance(exception, openai.InternalServerError):
        return _handle_server_error(
            "OpenAI", str(exception), getattr(exception, "status_code", 500)
        )

    if isinstance(exception, openai.ConflictError):
        return _handle_conflict("OpenAI", str(exception))

    # LengthFinishReasonError / ContentFilterFinishReasonError are client-side
    if isinstance(exception, openai.LengthFinishReasonError):
        return RetryableError(
            error_type="truncated_response",
            message=str(exception),
            is_retryable=False,
            user_message="The response was cut off because the model reached its output token limit.",
        )
    if isinstance(exception, openai.ContentFilterFinishReasonError):
        return _handle_content_filter("OpenAI", str(exception))

    if isinstance(exception, openai.APIStatusError):
        return _classify_openai_by_status(exception.status_code, exception)

    return _fallback_classify(str(exception), "OpenAI")


def _classify_openai_by_status(status_code: int, exception: Exception) -> RetryableError:
    body = _extract_error_body(exception)
    msg = str(exception)
    retry_after = _extract_retry_after(exception)

    if status_code == 400:
        return _handle_bad_request("OpenAI", msg, body)
    if status_code == 401:
        return _handle_auth_error("OpenAI", msg, 401)
    if status_code == 403:
        return _handle_permission_error("OpenAI", msg, 403)
    if status_code == 404:
        return _handle_not_found("OpenAI", msg)
    if status_code == 429:
        return _handle_rate_limit("OpenAI", msg, retry_after)
    if status_code == 504:
        return _handle_timeout("OpenAI", msg)
    if status_code >= 500:
        return _handle_server_error("OpenAI", msg, status_code)

    return _fallback_classify(msg, "OpenAI")


# ============================================================================
# GOOGLE (Gemini)
# ============================================================================


def classify_google_error(exception: Exception) -> RetryableError:
    common = classify_common_error(exception, "Google")
    if common is not None:
        return common

    # A bare ValueError on the Google path is client-side SDK validation raised
    # BEFORE any HTTP call (e.g. ``contents are required.`` on an empty request) —
    # a deterministic bad request, never a transient failure to retry.
    if isinstance(exception, ValueError):
        return _handle_bad_request("Google", str(exception), {"message": str(exception)})

    try:
        from google.genai.errors import APIError as GoogleAPIError
        from google.genai.errors import ClientError, ServerError
    except ImportError:
        status_code = _extract_status_code(exception)
        if status_code is not None:
            return _classify_google_by_status(status_code, exception)
        return _fallback_classify(str(exception), "Google")

    if isinstance(exception, ClientError):
        code = getattr(exception, "code", 400)
        status = getattr(exception, "status", "") or ""
        msg = str(exception)

        if code == 401 or "UNAUTHENTICATED" in status:
            return _handle_auth_error("Google", msg, 401)
        if code == 403 or "PERMISSION_DENIED" in status:
            return _handle_permission_error("Google", msg, 403)
        if code == 404 or "NOT_FOUND" in status:
            return _handle_not_found("Google", msg)
        if code == 429 or "RESOURCE_EXHAUSTED" in status:
            retry_after = _extract_retry_after(exception)
            return _handle_rate_limit("Google", msg, retry_after)

        # Google safety blocks come as 400 with specific messages
        msg_lower = msg.lower()
        if any(x in msg_lower for x in ("safety", "blocked", "harm_category")):
            return _handle_content_filter("Google", msg)
        if any(x in msg_lower for x in ("context_length", "too many tokens", "token limit")):
            return _handle_context_length_exceeded("Google", msg)

        return _handle_bad_request("Google", msg, _extract_error_body(exception))

    if isinstance(exception, ServerError):
        code = getattr(exception, "code", 500)
        msg = str(exception)
        status = getattr(exception, "status", "") or ""

        if code == 503 or "UNAVAILABLE" in status:
            return _handle_overloaded("Google", msg, 503)

        return _handle_server_error("Google", msg, code)

    if isinstance(exception, GoogleAPIError):
        code = getattr(exception, "code", None)
        if code is not None:
            return _classify_google_by_status(code, exception)

    # Google function call errors
    try:
        from google.genai.errors import (
            FunctionInvocationError,
            UnknownFunctionCallArgumentError,
            UnsupportedFunctionError,
        )

        if isinstance(
            exception,
            UnknownFunctionCallArgumentError | UnsupportedFunctionError | FunctionInvocationError,
        ):
            return RetryableError(
                error_type="tool_call_error",
                message=str(exception),
                is_retryable=False,
                user_message="A tool call failed due to invalid arguments or an unsupported function.",
            )
    except ImportError:
        pass

    return _fallback_classify(str(exception), "Google")


def _classify_google_by_status(status_code: int, exception: Exception) -> RetryableError:
    msg = str(exception)
    retry_after = _extract_retry_after(exception)

    if status_code == 400:
        return _handle_bad_request("Google", msg, _extract_error_body(exception))
    if status_code == 401:
        return _handle_auth_error("Google", msg, 401)
    if status_code == 403:
        return _handle_permission_error("Google", msg, 403)
    if status_code == 404:
        return _handle_not_found("Google", msg)
    if status_code == 429:
        return _handle_rate_limit("Google", msg, retry_after)
    if status_code == 503:
        return _handle_overloaded("Google", msg, 503)
    if status_code == 504:
        return _handle_timeout("Google", msg)
    if status_code >= 500:
        return _handle_server_error("Google", msg, status_code)

    return _fallback_classify(msg, "Google")


# ============================================================================
# GROQ (Stainless SDK — same exception hierarchy as Anthropic/OpenAI)
# ============================================================================


def classify_groq_error(exception: Exception) -> RetryableError:
    common = classify_common_error(exception, "Groq")
    if common is not None:
        return common

    try:
        import groq
    except ImportError:
        status_code = _extract_status_code(exception)
        if status_code is not None:
            return _classify_stainless_by_status("Groq", status_code, exception)
        return _fallback_classify(str(exception), "Groq")

    return _classify_stainless_provider("Groq", exception, groq)


# ============================================================================
# XAI (OpenAI-compatible SDK)
# ============================================================================


def classify_xai_error(exception: Exception) -> RetryableError:
    common = classify_common_error(exception, "xAI")
    if common is not None:
        return common

    # xAI uses the OpenAI SDK under the hood
    try:
        import openai

        if isinstance(exception, openai.OpenAIError):
            result = classify_openai_error(exception)
            result.user_message = result.user_message.replace("OpenAI", "xAI")
            return result
    except ImportError:
        pass

    status_code = _extract_status_code(exception)
    if status_code is not None:
        return _classify_stainless_by_status("xAI", status_code, exception)
    return _fallback_classify(str(exception), "xAI")


# ============================================================================
# TOGETHER AI (OpenAI-compatible SDK)
# ============================================================================


def classify_together_error(exception: Exception) -> RetryableError:
    common = classify_common_error(exception, "Together AI")
    if common is not None:
        return common

    try:
        import openai

        if isinstance(exception, openai.OpenAIError):
            result = classify_openai_error(exception)
            result.user_message = result.user_message.replace("OpenAI", "Together AI")
            return result
    except ImportError:
        pass

    status_code = _extract_status_code(exception)
    if status_code is not None:
        return _classify_stainless_by_status("Together AI", status_code, exception)
    return _fallback_classify(str(exception), "Together AI")


# ============================================================================
# CEREBRAS
# ============================================================================


def classify_cerebras_error(exception: Exception) -> RetryableError:
    common = classify_common_error(exception, "Cerebras")
    if common is not None:
        return common

    try:
        import openai

        if isinstance(exception, openai.OpenAIError):
            result = classify_openai_error(exception)
            result.user_message = result.user_message.replace("OpenAI", "Cerebras")
            return result
    except ImportError:
        pass

    status_code = _extract_status_code(exception)
    if status_code is not None:
        return _classify_stainless_by_status("Cerebras", status_code, exception)
    return _fallback_classify(str(exception), "Cerebras")


# ============================================================================
# GENERIC OPENAI-COMPATIBLE (HuggingFace, etc.)
# ============================================================================


def classify_generic_openai_error(exception: Exception) -> RetryableError:
    common = classify_common_error(exception, "AI provider")
    if common is not None:
        return common

    try:
        import openai

        if isinstance(exception, openai.OpenAIError):
            result = classify_openai_error(exception)
            result.user_message = result.user_message.replace("OpenAI", "AI provider")
            return result
    except ImportError:
        pass

    status_code = _extract_status_code(exception)
    if status_code is not None:
        return _classify_stainless_by_status("AI provider", status_code, exception)
    return _fallback_classify(str(exception), "AI provider")


# ============================================================================
# ELEVENLABS
# ============================================================================


def classify_elevenlabs_error(exception: Exception) -> RetryableError:
    common = classify_common_error(exception, "ElevenLabs")
    if common is not None:
        return common

    status_code = _extract_status_code(exception)
    msg = str(exception)

    if status_code == 401:
        return _handle_auth_error("ElevenLabs", msg, 401)
    if status_code == 422:
        if "character" in msg.lower() or "limit" in msg.lower():
            return RetryableError(
                error_type="character_limit",
                message=msg,
                status_code=422,
                is_retryable=False,
                user_message="The text exceeds ElevenLabs' character limit for this voice/plan.",
            )
        return _handle_unprocessable("ElevenLabs", msg, _extract_error_body(exception))
    if status_code == 429:
        return _handle_rate_limit("ElevenLabs", msg, _extract_retry_after(exception))
    if status_code is not None and status_code >= 500:
        return _handle_server_error("ElevenLabs", msg, status_code)

    return _fallback_classify(msg, "ElevenLabs")


# ============================================================================
# Shared Stainless-SDK classifier (Groq and any future Stainless-based SDKs)
# ============================================================================


def _classify_stainless_provider(
    provider: str, exception: Exception, sdk_module: object
) -> RetryableError:
    """Classify errors from Stainless-generated SDKs (Groq, etc.) using isinstance."""
    retry_after = _extract_retry_after(exception)
    body = _extract_error_body(exception)

    AuthErr = getattr(sdk_module, "AuthenticationError", None)
    PermErr = getattr(sdk_module, "PermissionDeniedError", None)
    BadReq = getattr(sdk_module, "BadRequestError", None)
    NotFound = getattr(sdk_module, "NotFoundError", None)
    Unprocessable = getattr(sdk_module, "UnprocessableEntityError", None)
    RateLimit = getattr(sdk_module, "RateLimitError", None)
    Timeout = getattr(sdk_module, "APITimeoutError", None)
    ConnErr = getattr(sdk_module, "APIConnectionError", None)
    InternalErr = getattr(sdk_module, "InternalServerError", None)
    StatusErr = getattr(sdk_module, "APIStatusError", None)

    if AuthErr and isinstance(exception, AuthErr):
        return _handle_auth_error(provider, str(exception), 401)
    if PermErr and isinstance(exception, PermErr):
        return _handle_permission_error(provider, str(exception), 403)
    if BadReq and isinstance(exception, BadReq):
        msg = str(exception)
        if "context_length" in msg.lower():
            return _handle_context_length_exceeded(provider, msg)
        return _handle_bad_request(provider, msg, body)
    if NotFound and isinstance(exception, NotFound):
        return _handle_not_found(provider, str(exception))
    if Unprocessable and isinstance(exception, Unprocessable):
        return _handle_unprocessable(provider, str(exception), body)
    if RateLimit and isinstance(exception, RateLimit):
        return _handle_rate_limit(provider, str(exception), retry_after)
    if Timeout and isinstance(exception, Timeout):
        return _handle_timeout(provider, str(exception))
    if ConnErr and isinstance(exception, ConnErr):
        return _handle_connection_error(provider, str(exception))
    if InternalErr and isinstance(exception, InternalErr):
        return _handle_server_error(
            provider, str(exception), getattr(exception, "status_code", 500)
        )
    if StatusErr and isinstance(exception, StatusErr):
        return _classify_stainless_by_status(
            provider, getattr(exception, "status_code", 500), exception
        )

    return _fallback_classify(str(exception), provider)


def _classify_stainless_by_status(
    provider: str, status_code: int, exception: Exception
) -> RetryableError:
    """Status-code dispatch for any Stainless-SDK based provider."""
    body = _extract_error_body(exception)
    msg = str(exception)
    retry_after = _extract_retry_after(exception)

    if status_code == 400:
        return _handle_bad_request(provider, msg, body)
    if status_code == 401:
        return _handle_auth_error(provider, msg, 401)
    if status_code == 402:
        return _handle_billing_error(provider, msg)
    if status_code == 403:
        return _handle_permission_error(provider, msg, 403)
    if status_code == 404:
        return _handle_not_found(provider, msg)
    if status_code == 413:
        return _handle_request_too_large(provider, msg)
    if status_code == 429:
        return _handle_rate_limit(provider, msg, retry_after)
    if status_code == 529:
        return _handle_overloaded(provider, msg, 529)
    if status_code == 504:
        return _handle_timeout(provider, msg)
    if status_code >= 500:
        return _handle_server_error(provider, msg, status_code)

    return _fallback_classify(msg, provider)


# ============================================================================
# UNIVERSAL DISPATCH
# ============================================================================

_PROVIDER_CLASSIFIERS: dict[str, object] = {
    "anthropic": classify_anthropic_error,
    "openai": classify_openai_error,
    "google": classify_google_error,
    "groq": classify_groq_error,
    "xai": classify_xai_error,
    "together": classify_together_error,
    "cerebras": classify_cerebras_error,
    "generic_openai": classify_generic_openai_error,
    "huggingface": classify_generic_openai_error,
    "moonshot": classify_moonshot_error,
    "elevenlabs": classify_elevenlabs_error,
}


def classify_provider_error(provider: str, exception: Exception) -> RetryableError:
    common = classify_common_error(exception, provider)
    if common is not None:
        return common

    classifier = _PROVIDER_CLASSIFIERS.get(provider.lower())
    if classifier:
        return classifier(exception)

    status_code = _extract_status_code(exception)
    if status_code is not None:
        return _classify_stainless_by_status(provider, status_code, exception)
    return _fallback_classify(str(exception), provider)
