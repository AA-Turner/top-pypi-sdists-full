"""The package-side seam for THE PROVIDER-OUTAGE ALARM.

``matrx_ai`` cannot import the host (the package-boundary gate), and the alarm
needs the host's knob registry, the host's ORM models and the host's
organization resolution. So the detector lives in the host
(``aidream/services/provider_outage/detector.py``) and this module is the thin
door matrx-ai calls through — exactly like ``record_error``.

Two facts cross the door:

* a classified provider REFUSAL, from ``matrx_ai.ops.issue_capture`` — the one
  writer every counted provider error already passes through;
* a provider SUCCESS, from the executor, right after
  ``UnifiedAIClient.execute`` returns.

The success side must cost nothing on the hot path, so the executor asks
:func:`outage_watch_active` first — a process-local bool. It is armed whenever
the host reports an open outage row, and it re-arms itself every
:data:`RECHECK_SECONDS` so a process that restarted while a row was open still
finds and closes it (the flag is an accelerator; the DB is the truth).

Nothing here raises: an unconfigured host is a silent no-op (standalone
matrx-ai), and a failing hook is swallowed by the host side, which captures it.
"""

from __future__ import annotations

import time

#: How long a "nothing is open" answer is trusted before the success path asks
#: the host again. Bounds the damage of a restart that inherited an open row:
#: the first successful call after this many seconds re-checks and closes it.
RECHECK_SECONDS = 300.0

_watch_active = False
_last_checked: float | None = None


def reset_outage_watch() -> None:
    """Drop the process-local watch state. For tests only."""
    global _watch_active, _last_checked
    _watch_active = False
    _last_checked = None


def outage_watch_active() -> bool:
    """True when the success path should tell the host about a successful call.

    Sync, allocation-free, and the only thing the hot path touches."""
    if _watch_active:
        return True
    if _last_checked is None:
        return True
    return (time.monotonic() - _last_checked) >= RECHECK_SECONDS


def _remember(any_open: object) -> None:
    global _watch_active, _last_checked
    _watch_active = bool(any_open)
    _last_checked = time.monotonic()


async def note_provider_failure(
    *,
    provider: str | None,
    model: str | None = None,
    error_type: str | None,
    status_code: int | None = None,
    error_text: str | None = None,
    rerouted_to: str | None = None,
) -> None:
    """Tell the host about one classified provider refusal. Never raises."""
    try:
        from matrx_ai._ext import get_ext, has_ext

        if not has_ext("provider_outage_failure"):
            return
        hook = get_ext("provider_outage_failure")
        _remember(
            await hook(
                provider=provider,
                model=model,
                error_type=error_type,
                status_code=status_code,
                error_text=error_text,
                rerouted_to=rerouted_to,
            )
        )
    except Exception:  # noqa: BLE001 — a broken alarm never becomes a failed run
        return


async def note_provider_success(*, provider: str | None, model: str | None = None) -> None:
    """Tell the host a provider answered, so an open outage row can close.

    Callers gate on :func:`outage_watch_active` first; calling unconditionally
    is safe but does a host round-trip per successful call."""
    try:
        from matrx_ai._ext import get_ext, has_ext

        if not has_ext("provider_outage_success"):
            return
        hook = get_ext("provider_outage_success")
        _remember(await hook(provider=provider, model=model))
    except Exception:  # noqa: BLE001 — a broken alarm never becomes a failed run
        return


__all__ = [
    "RECHECK_SECONDS",
    "note_provider_failure",
    "note_provider_success",
    "outage_watch_active",
    "reset_outage_watch",
]
