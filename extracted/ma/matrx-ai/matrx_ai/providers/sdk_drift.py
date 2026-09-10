"""SDK-drift guard — the ONE seam between catalog-resolved request params and a
provider SDK whose Python signature floats (every SDK here is pinned "latest").

Why this exists (2026-09-09, request 5369148e-2a5b-4e70-8d40-1cde54be1dda):
the ``anthropic`` package moved 0.100 → 1.4.0 in the 2026-09-08 lockfile
refresh and ``messages.create`` / ``messages.stream`` dropped ``temperature``
/ ``top_p`` / ``top_k`` from their signatures. The Messages API still accepts
those keys on the non-adaptive models (Sonnet 4.5, Haiku 4.5, the Claude 4 and
3.x lines); the adaptive models return a clean 400 that the DB rules already
prevent with ``supported: false``. Every call that carried one died with
``TypeError: got an unexpected keyword argument`` BEFORE a request was made —
a silent outage class, not one provider's bug: every translator in
``providers/`` forwards a dict blind (``sdk.method(**kwargs)``) into an SDK
that can rename or drop a keyword on any bump.

The rule: a key the DB catalog resolved is a WIRE fact; the SDK's Python
signature is a transport detail. So, per call, against the INSTALLED
signature (never a pinned version):

  * a key the SDK declares → passes through untouched;
  * a key it no longer declares, on an SDK with ``extra_body`` → travels in
    ``extra_body`` (same bytes on the wire), recorded as an EXPECTED
    ``Adjustment(action="mapped")`` — the request is not changed, only carried;
  * a key it no longer declares, on an SDK with no body escape hatch → DROPPED
    with an UNEXPECTED ``Adjustment(action="dropped")``: the client gets the
    ``setting_not_supported`` warning (THE EQUIVALENCE LAW's client half) and
    the drift is captured durably as an ``ops`` issue so the catalog rule that
    emitted the key gets fixed. Never a TypeError, never silent.

A signature that cannot be read, or one that takes ``**kwargs``, means "accepts
anything" and the request passes through unchanged.

Every voice is once per (SDK method, key) per process — an SDK bump is loud
exactly once, not once per request.
"""

from __future__ import annotations

import inspect
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from matrx_utils import vcprint

from matrx_ai.catalog.models import Adjustment

_ACCEPTS_ANYTHING = None

# Keyed by the UNDERLYING function object (a bound method is a fresh object on
# every attribute access, so ``id(bound)`` is recycled and would collide).
_DECLARED_CACHE: dict[Any, frozenset[str] | None] = {}
_ANNOUNCED: set[str] = set()

ISSUE_KEY = "provider.sdk_signature_drift"


def _underlying(fn: Callable[..., Any]) -> Any:
    return getattr(fn, "__func__", fn)


def _qualname(fn: Callable[..., Any]) -> str:
    return str(getattr(fn, "__qualname__", None) or getattr(fn, "__name__", None) or fn)


def declared_parameters(fn: Callable[..., Any]) -> frozenset[str] | None:
    """The keyword names the installed SDK method declares, or ``None`` when it
    accepts anything (unreadable signature or a ``**kwargs`` parameter)."""
    target = _underlying(fn)
    try:
        return _DECLARED_CACHE[target]
    except KeyError:
        pass
    except TypeError:  # unhashable callable — compute without caching
        target = None

    names: frozenset[str] | None
    try:
        params = inspect.signature(fn).parameters
    except (TypeError, ValueError):
        names = _ACCEPTS_ANYTHING
    else:
        if any(p.kind is inspect.Parameter.VAR_KEYWORD for p in params.values()):
            names = _ACCEPTS_ANYTHING
        else:
            names = frozenset(
                n for n, p in params.items() if p.kind in (p.KEYWORD_ONLY, p.POSITIONAL_OR_KEYWORD)
            )
    if target is not None:
        _DECLARED_CACHE[target] = names
    return names


@dataclass(frozen=True)
class SdkKwargsPlan:
    """The pure result of checking a request against an SDK signature."""

    kwargs: dict[str, Any]
    adjustments: tuple[Adjustment, ...]
    routed: tuple[str, ...]  # keys carried via extra_body
    dropped: tuple[str, ...]  # keys the SDK cannot carry at all

    @property
    def changed(self) -> bool:
        return bool(self.routed or self.dropped)


def plan_sdk_kwargs(fn: Callable[..., Any], request: dict[str, Any]) -> SdkKwargsPlan:
    """Pure: never mutates ``request``; never voices anything."""
    declared = declared_parameters(fn)
    if declared is _ACCEPTS_ANYTHING:
        return SdkKwargsPlan(kwargs=dict(request), adjustments=(), routed=(), dropped=())

    kwargs = dict(request)
    adjustments: list[Adjustment] = []
    routed: list[str] = []
    dropped: list[str] = []
    can_route = "extra_body" in declared
    extra = dict(kwargs.get("extra_body") or {})
    method = _qualname(fn)

    for key in list(kwargs.keys()):
        if key in declared:
            continue
        value = kwargs.pop(key)
        if can_route:
            extra[key] = value
            routed.append(key)
            adjustments.append(
                Adjustment(
                    key=key,
                    action="mapped",
                    canonical_value=value,
                    sent_value=value,
                    expected=True,
                    reason=(
                        f"installed SDK no longer declares '{key}' on {method}; "
                        "sent via extra_body (same wire bytes)"
                    ),
                )
            )
        else:
            dropped.append(key)
            adjustments.append(
                Adjustment(
                    key=key,
                    action="dropped",
                    canonical_value=value,
                    sent_value=None,
                    expected=False,
                    reason=(
                        f"installed SDK no longer declares '{key}' on {method} and has "
                        "no extra_body escape hatch — dropped; the catalog rule that "
                        "emitted it must be corrected"
                    ),
                )
            )
    if routed:
        kwargs["extra_body"] = extra
    return SdkKwargsPlan(
        kwargs=kwargs,
        adjustments=tuple(adjustments),
        routed=tuple(routed),
        dropped=tuple(dropped),
    )


def route_undeclared_params(
    fn: Callable[..., Any],
    request: dict[str, Any],
    *,
    provider: str,
    model: Any = None,
) -> dict[str, Any]:
    """Return ``request`` made safe for ``fn(**...)`` against the INSTALLED SDK
    signature, voicing every change. Never mutates the caller's dict."""
    plan = plan_sdk_kwargs(fn, request)
    if plan.changed:
        _voice(plan, fn, provider=provider, model=model or request.get("model") or "?")
    return plan.kwargs


def _voice(plan: SdkKwargsPlan, fn: Callable[..., Any], *, provider: str, model: Any) -> None:
    method = _qualname(fn)
    fresh = [adj for adj in plan.adjustments if f"{provider}:{method}:{adj.key}" not in _ANNOUNCED]
    for adj in fresh:
        _ANNOUNCED.add(f"{provider}:{method}:{adj.key}")
        vcprint(
            f"[sdk-drift] {provider}: {adj.reason}. "
            + (
                "If the API itself rejects it, the DB rule for that model must mark the "
                "setting unsupported."
                if adj.action == "mapped"
                else "The request proceeds WITHOUT it."
            ),
            color="yellow" if adj.action == "mapped" else "red",
        )
    if not fresh:
        return

    # THE EQUIVALENCE LAW's client half: an unexpected drop reaches the user as
    # a warning (mapped keys are expected conversions — silent to the client).
    from matrx_ai.providers.outbound_params import warn_client_about_dropped_settings

    warn_client_about_dropped_settings(list(plan.adjustments), model=model)

    # Durable, once per (method, key) per process: an SDK bump that changed the
    # transport is a catalog-maintenance item, not just a console line.
    try:
        import asyncio

        asyncio.get_running_loop()
    except RuntimeError:
        return  # sync/offline resolution — the console line is the record
    try:
        from matrx_utils import detached_task

        from matrx_ai.ops.issue_capture import capture_issue

        detached_task(
            capture_issue(
                ISSUE_KEY,
                error_type="sdk_signature_drift",
                provider=provider,
                model=str(model),
                is_retryable=False,
                was_recovered=not plan.dropped,
                detail={
                    "sdk_method": method,
                    "routed_via_extra_body": list(plan.routed),
                    "dropped": list(plan.dropped),
                    "reasons": [adj.reason for adj in fresh],
                },
            ),
            name="sdk_drift_capture",
        )
    except Exception as exc:  # noqa: BLE001 — recording drift must never break the run
        vcprint(f"[sdk-drift] could not capture the drift issue ({exc!r})", color="yellow")
