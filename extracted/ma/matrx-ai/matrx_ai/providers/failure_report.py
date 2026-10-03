"""THE one door a provider failure takes to the operator.

Every paid provider call — chat, image, video, speech, transcription,
embeddings, research — classifies its failure through
``matrx_ai.providers.errors`` and reports it HERE. The shared dispatch seam
(``UnifiedAIClient._dispatch_with_billing_net``) calls it for everything that
rides it — chat, media, extraction, STT, Google embeddings, decisions, Cohere
rerank; a runtime that cannot hand its call to the seam (matrx-rag's injected
admission, a token-broker mint or relay, matrx-batch's injected
``failure_reporter``, the Google Live/Lyria sessions, Meet's STT, a
browser-held session reported to ``POST /broker/provider-failures``) calls
``report_dispatch_failure`` / ``report_provider_failure`` from its own
``except`` block. The orchestrator calls it again as a second layer; the exception is
marked once reported, so every layer may call it and the operator still gets
exactly one row.

It files two classes. ``provider_setting_rejected`` (Settings Translation R1,
K10): the provider refused one of our SETTINGS — the typed ``invalid_setting``
record a routine can fix from. And ``provider_account_out_of_credit`` — the
platform's account with a provider cannot pay for calls (2026-10-01: OpenAI
"You have no credits remaining" was retried 3x as ``unknown_error`` and no
operator surface named it). A new operator-worthy provider condition is added
here, never at one call site.

Never raises: a broken alarm must not replace the provider's exception.
"""

from __future__ import annotations

import time
from typing import Any

from matrx_ai.providers.errors import RetryableError, classify_provider_error
from matrx_ai.providers.setting_rejection import SETTING_REJECTION_ERROR_TYPE

#: ``system_error.kind`` for a provider refusing because the PLATFORM's account
#: has no credit (or is suspended). Its own kind so the collapsed error
#: surfaces raise it as one named class, whether or not a reroute then rescued
#: the request.
PROVIDER_OUT_OF_CREDIT_KIND = "provider_account_out_of_credit"

_REPORTED_ATTR = "_matrx_provider_failure_reported"


def classify_for_report(exc: BaseException, provider: str) -> RetryableError | None:
    """The failure's classification: the adapter's own when attached, else the shared classifier."""
    attached = getattr(exc, "error_info", None)
    if isinstance(attached, RetryableError):
        return attached
    if not isinstance(exc, Exception):
        return None  # cancellation / shutdown — not a provider failure
    try:
        return classify_provider_error(provider or "unknown", exc)
    except Exception:  # noqa: BLE001 — classification must never replace the failure
        return None


def _ambient_identity() -> dict[str, Any]:
    try:
        from matrx_connect.context.app_context import try_get_app_context

        ctx = try_get_app_context()
    except Exception:  # noqa: BLE001 — no context is a normal state for a worker
        ctx = None
    if ctx is None:
        return {}
    return {
        "request_id": getattr(ctx, "request_id", None) or None,  # orm-getattr-ok: AppContext
        "user_id": getattr(ctx, "user_id", None) or None,  # orm-getattr-ok: AppContext
        "conversation_id": getattr(ctx, "conversation_id", None) or None,  # orm-getattr-ok: AppContext
    }


# One out-of-credit row per (provider, request) — and, for work with no request,
# per provider per minute. Once-per-EXCEPTION is not enough: a batched embed
# over an exhausted account gathers ~50 batches, each raising its OWN exception,
# and filed ~50 identical rows for one person's one action (review of
# d022ab9953). The account is either out of credit or it is not; one row per
# request is the whole signal, and the collapsed surfaces count requests.
_ALARM_WINDOW_WITH_REQUEST_SECONDS = 600.0
_ALARM_WINDOW_WITHOUT_REQUEST_SECONDS = 60.0
_ALARM_MEMORY_MAX = 4096
_alarmed: dict[tuple[str, str], float] = {}


def _already_alarmed(provider_key: str, request_id: Any) -> bool:
    now = time.monotonic()
    key = (provider_key, str(request_id or ""))
    window = (
        _ALARM_WINDOW_WITH_REQUEST_SECONDS if request_id else _ALARM_WINDOW_WITHOUT_REQUEST_SECONDS
    )
    last = _alarmed.get(key)
    if last is not None and now - last < window:
        return True
    if len(_alarmed) >= _ALARM_MEMORY_MAX:
        cutoff = now - _ALARM_WINDOW_WITH_REQUEST_SECONDS
        for stale in [k for k, t in _alarmed.items() if t < cutoff]:
            del _alarmed[stale]
        if len(_alarmed) >= _ALARM_MEMORY_MAX:
            _alarmed.clear()
    _alarmed[key] = now
    return False


def reset_alarm_memory() -> None:
    """Forget which alarms were filed. For tests only."""
    _alarmed.clear()


async def report_provider_failure(
    exc: BaseException,
    *,
    provider: str,
    model: str | None = None,
    route: str = "providers/dispatch",
    error_info: RetryableError | None = None,
    payload: dict[str, Any] | None = None,
    setting_context: dict[str, Any] | None = None,
    **identity: Any,
) -> RetryableError | None:
    """Classify ``exc`` and file the operator alarm it calls for — once per exception.

    ``identity`` (request_id / user_id / conversation_id) overrides the ambient
    AppContext when the caller knows better. Returns the classification.
    """
    info = error_info or classify_for_report(exc, provider)
    if info is not None and info.error_type == SETTING_REJECTION_ERROR_TYPE:
        await report_setting_rejection(
            exc,
            info,
            provider=provider,
            model=model,
            route=route,
            payload=payload,
            setting_context=setting_context,
            **identity,
        )
        return info
    if info is None or info.error_type != "billing_error":
        return info
    if getattr(exc, _REPORTED_ATTR, False):
        return info
    try:
        setattr(exc, _REPORTED_ATTR, True)
    except Exception:  # noqa: BLE001 — an immutable exception still gets its row
        pass

    provider_key = str((info.details or {}).get("provider") or provider or "unknown").lower()
    fields: dict[str, Any] = {**_ambient_identity(), **{k: v for k, v in identity.items() if v}}
    if _already_alarmed(provider_key, fields.get("request_id")):
        return info
    try:
        from matrx_connect.streaming.error_capture import capture_error

        await capture_error(
            exc,
            kind=PROVIDER_OUT_OF_CREDIT_KIND,
            route=route,
            error_type=f"{provider_key}.billing_error",
            payload={
                "provider": provider_key,
                "model": model,
                "status_code": info.status_code,
                "provider_error_type": (info.details or {}).get("provider_error_type"),
                "provider_message": info.message,
                **(payload or {}),
            },
            **fields,
        )
    except Exception:  # noqa: BLE001 — the alarm never replaces the provider's exception
        pass
    return info


def _ambient_setting_context() -> dict[str, Any]:
    """What the running turn knows about the call that just failed.

    The ExecutionState holds the wire body the provider captured just before the
    SDK call, the pre-allocated failure snapshot id, and the canonical config of
    the request in flight. Absent outside an orchestrated turn (a bare media
    call) — the caller's explicit context and the exception's attached wire
    payload cover that.
    """
    try:
        from matrx_ai.orchestrator.execution_state import try_get_execution_state

        state = try_get_execution_state()
    except Exception:  # noqa: BLE001
        state = None
    if state is None:
        return {}
    current = getattr(state, "current_request", None)
    return {
        "wire_payload": getattr(state, "snapshot_payload", None),
        "request_snapshot_id": getattr(state, "failure_snapshot_id", None),
        "config": getattr(current, "config", None) if current is not None else None,
        "adjustments": getattr(state, "adjustments", None),
    }


async def report_setting_rejection(
    exc: BaseException,
    info: RetryableError,
    *,
    provider: str,
    model: str | None = None,
    route: str = "providers/dispatch",
    payload: dict[str, Any] | None = None,
    setting_context: dict[str, Any] | None = None,
    **identity: Any,
) -> None:
    """File THE record of a settings rejection (K10) — once per exception and request.

    ONE ``ops.system_error`` row, kind ``provider_setting_rejected``, error_type
    ``<provider>.invalid_setting``, payload = the K10 record with
    ``lifecycle: "new"``. The orchestrator's generic ``provider_request_failed``
    row is NOT also written for this class, and the browser's copy of the same
    stream error is kept local (matrx-frontend captureStreamError) — the request
    id on this row is the dedupe key. Never raises.
    """
    if getattr(exc, _REPORTED_ATTR, False):
        return
    try:
        setattr(exc, _REPORTED_ATTR, True)
    except Exception:  # noqa: BLE001
        pass
    try:
        from matrx_ai.providers.setting_rejection import (
            PROVIDER_SETTING_REJECTED_KIND,
            attached_wire_payload,
            build_record,
        )

        ctx: dict[str, Any] = {k: v for k, v in _ambient_setting_context().items() if v is not None}
        ctx.update({k: v for k, v in (setting_context or {}).items() if v is not None})
        wire = ctx.get("wire_payload")
        if wire is None:
            wire = attached_wire_payload(exc)
        record = build_record(
            info,
            model=model,
            profile=ctx.get("profile"),
            config=ctx.get("config"),
            wire_payload=wire,
            request_snapshot_id=ctx.get("request_snapshot_id"),
            modality=ctx.get("modality"),
            adjustments=ctx.get("adjustments"),
        )
        fields: dict[str, Any] = {**_ambient_identity(), **{k: v for k, v in identity.items() if v}}
        # One record per (request, refused field); with no request, per print.
        dedupe = (
            f"setting:{record['provider']}:{record['provider_param'] or '?'}"
            if fields.get("request_id")
            else f"setting:{record['fingerprint']}"
        )
        if _already_alarmed(dedupe, fields.get("request_id")):
            return
        from matrx_connect.streaming.error_capture import capture_error

        await capture_error(
            exc,
            kind=PROVIDER_SETTING_REJECTED_KIND,
            route=route,
            error_type=f"{record['provider']}.{SETTING_REJECTION_ERROR_TYPE}",
            error_text=(
                f"{record['provider']} rejected setting "
                f"{record['provider_param'] or '(unnamed)'}: {record['provider_message']}"
            )[:2000],
            payload={**record, **(payload or {})},
            **fields,
        )
    except Exception:  # noqa: BLE001 — the record never replaces the provider's exception
        pass


PROVIDER_BILLING_CAPTURE_MISSING_KIND = "provider_billing_capture_missing"


async def report_dispatch_failure(
    exc: BaseException,
    *,
    provider: str,
    model: str | None = None,
    route: str = "providers/dispatch",
    profile: Any = None,
    config: Any = None,
    modality: str | None = None,
    defer_setting_rejection: bool = False,
) -> None:
    """Everything the shared dispatch seam does with a failed provider call.

    ``UnifiedAIClient._dispatch_with_billing_net`` calls this from its
    ``except``; a runtime that cannot hand its call to the seam as a callable
    (matrx-rag's injected admission context manager) calls it from its own,
    so both take the same pipe: the operator alarm door, then LAYER 2 — a
    wire-engaged failure no adapter inspected for billing files
    ``provider_billing_capture_missing``. Never raises.
    """
    from matrx_ai.providers.errors import report_unbilled_provider_failure

    # ``defer_setting_rejection``: the caller (the dispatch seam's settings
    # self-heal, R2) files the K10 record itself once the repair's outcome is
    # known — ``self_healed`` true/false — so it is not filed here first.
    deferred = False
    if defer_setting_rejection:
        info = classify_for_report(exc, provider)
        deferred = info is not None and info.error_type == SETTING_REJECTION_ERROR_TYPE
    if not deferred:
        await report_provider_failure(
            exc,
            provider=provider,
            model=model,
            route=route,
            setting_context={"profile": profile, "config": config, "modality": modality},
        )
    if not report_unbilled_provider_failure(exc, provider=provider, model=model):
        return
    try:
        from matrx_connect.streaming.error_capture import capture_error

        await capture_error(
            exc,
            kind=PROVIDER_BILLING_CAPTURE_MISSING_KIND,
            route=route,
            error_type=f"{type(exc).__module__}.{type(exc).__qualname__}",
            payload={"provider": provider, "model": model},
        )
    except Exception:  # noqa: BLE001 — accounting alarms never replace the provider exception
        pass


__all__ = [
    "PROVIDER_BILLING_CAPTURE_MISSING_KIND",
    "report_setting_rejection",
    "PROVIDER_OUT_OF_CREDIT_KIND",
    "classify_for_report",
    "report_dispatch_failure",
    "report_provider_failure",
]
