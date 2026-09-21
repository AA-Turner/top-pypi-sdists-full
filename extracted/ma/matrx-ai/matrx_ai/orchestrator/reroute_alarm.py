"""THE PROVIDER-SUBSTITUTION ALARM — a model swap is an operator alarm, not a log line.

WHY THIS EXISTS
---------------
When a provider refuses a call before doing the work (429 / 529 / 503, or a
``billing_error`` — "Your credit balance is too low to access the Anthropic
API"), the executor reroutes: first to a sibling ``ai.offering`` of the SAME
model, then to the model row's ``retry_fallback_id``, which is a DIFFERENT
model and usually a different vendor
(``matrx_ai.orchestrator.overload_reroute``). That is the right runtime
behaviour — a user's request continues — but it is also the platform quietly
spending on, and answering with, a model nobody chose.

Before 2026-09-12 the whole record of that was: a red terminal block, an
``info`` stream event the workflow surfaces never showed, a note in the request
metadata nothing read back, and an ``ops.ops_issue_event`` row filed under the
provider's error class. Nothing named the SUBSTITUTION itself, so nobody was
alarmed when the Anthropic account ran out of credit and three live medical
workup runs (843d5847…, 94d48d9c…, 339bb4bf…) authored ``claude-sonnet-5`` and
ran end to end on ``gpt-4.1-2025-04-14``.

This writes the missing row, through the host's own ``record_error`` door (the
one seam ``matrx_ai`` has for ``ops.system_error``), so an exhausted or
throttled provider becomes a named alarm on the error surfaces an operator
already watches — alongside the per-occurrence counting ``capture_issue``
already does.

It NEVER raises: a broken alarm must not become a failed run.
"""

from __future__ import annotations

import inspect
from typing import Any

#: ``system_error.kind`` when a DIFFERENT MODEL answered the call.
PROVIDER_MODEL_SUBSTITUTED_KIND = "provider_model_substituted"

#: ``system_error.kind`` when the SAME model was re-dialed through another
#: endpoint/api route. Cheaper than a substitution — the author's model still
#: ran — but it still means a route we sell is refusing calls.
PROVIDER_OFFERING_REROUTED_KIND = "provider_offering_rerouted"

#: The ``source_app`` these findings are filed under.
REROUTE_SOURCE_APP = "ai-routing"

#: The ``source_feature`` these findings are filed under — the SMALLER half of
#: the one two-level categorization, so a reroute filters apart from every other
#: routing failure under the same app.
REROUTE_SOURCE_FEATURE = "reroute"

#: (kind, from_model, to_model, error_type) already filed in this process.
#: One row per class per process — ``ops.ops_issue_event`` carries the
#: per-occurrence count, so repeating the row would only bury the alarm.
_REPORTED: set[tuple[str, str, str, str]] = set()


class ProviderModelSubstituted(RuntimeError):
    """The platform answered on a model the caller did not name.

    An exception type only because the host's ``record_error`` door captures
    exceptions. Nothing raises it.
    """


def reset_reported_reroutes() -> None:
    """Clear the per-process dedupe. For tests only."""
    _REPORTED.clear()


def _context() -> Any | None:
    try:
        from matrx_connect.context.app_context import try_get_app_context

        return try_get_app_context()
    except Exception:  # noqa: BLE001 — no context is a normal state, not a failure
        return None


def record_provider_reroute(
    note: dict[str, Any] | None,
    *,
    spec_type: str | None = None,
    mandate_key: str | None = None,
) -> str | None:
    """File ONE ``ops.system_error`` row naming a reroute that just happened.

    ``note`` is a :class:`~matrx_ai.orchestrator.overload_reroute.RerouteNote`
    dumped to a dict. Returns the ``kind`` it filed (or would have filed), or
    ``None`` when there is nothing to report — so a caller and a test can see
    the decision without reaching into the host.
    """
    if not isinstance(note, dict) or not note:
        return None
    scope = str(note.get("scope") or "model")
    from_model = str(note.get("from_model") or "")
    to_model = str(note.get("to_model") or "")
    error_type = str(note.get("error_type") or "")
    kind = (
        PROVIDER_OFFERING_REROUTED_KIND
        if scope == "offering"
        else PROVIDER_MODEL_SUBSTITUTED_KIND
    )

    signature = (kind, from_model, to_model, error_type)
    if signature in _REPORTED:
        return kind
    _REPORTED.add(signature)

    reason_text = note.get("reason") or "not recorded"
    from_offering = note.get("from_offering_id") or "preferred"
    to_offering = note.get("to_offering_id") or "unknown"
    status_code = note.get("status_code")
    status_text = f", HTTP {status_code}" if status_code else ""
    if kind == PROVIDER_MODEL_SUBSTITUTED_KIND:
        text = (
            f"A provider refused the call ({error_type or 'unknown error'}"
            f"{status_text}) and the "
            f"request was ANSWERED BY A DIFFERENT MODEL: '{from_model}' → '{to_model}'. "
            f"The caller named '{from_model}'; the answer, its cost and its usage row belong to "
            f"'{to_model}'. Fix the named model's provider (the reason below says how) or change "
            f"its ai.model_definition.retry_fallback_id. Reason: {reason_text}"
        )
    else:
        text = (
            f"An ai.offering refused the call ({error_type or 'unknown error'}"
            f"{status_text}) and the "
            f"request was re-dialed through a SIBLING OFFERING of the same model '{from_model}': "
            f"offering '{from_offering}' → "
            f"'{to_offering}'. The named model still ran, but a route "
            f"we sell is refusing calls. Reason: {reason_text}"
        )

    try:
        from matrx_ai._ext import get_ext, has_ext

        if not has_ext("record_error"):
            return kind
        record_error = get_ext("record_error")
    except Exception:  # noqa: BLE001 — no host wiring is a normal standalone state
        return kind

    try:
        ctx = _context()
        pending = record_error(
            ProviderModelSubstituted(text),
            kind=kind,
            error_type=error_type or kind,
            error_text=text,
            source_app=REROUTE_SOURCE_APP,
            source_feature=REROUTE_SOURCE_FEATURE,
            route=spec_type or "ai.execute",
            user_id=getattr(ctx, "user_id", None) or None,  # orm-getattr-ok: AppContext
            organization_id=getattr(ctx, "organization_id", None),  # orm-getattr-ok: AppContext
            conversation_id=getattr(ctx, "conversation_id", None),  # orm-getattr-ok: AppContext
            request_id=getattr(ctx, "request_id", None) or None,  # orm-getattr-ok: AppContext
            payload={
                "reroute": dict(note),
                "spec_type": spec_type,
                "mandate_key": mandate_key,
            },
        )
        if inspect.isawaitable(pending):
            import asyncio

            try:
                asyncio.get_running_loop()
            except RuntimeError:
                pending.close()
                return kind
            from matrx_utils import detached_task

            detached_task(pending, name=kind)
    except Exception:  # noqa: BLE001 — a broken alarm never becomes a failed run
        return kind
    return kind


__all__ = [
    "PROVIDER_MODEL_SUBSTITUTED_KIND",
    "PROVIDER_OFFERING_REROUTED_KIND",
    "REROUTE_SOURCE_APP",
    "REROUTE_SOURCE_FEATURE",
    "ProviderModelSubstituted",
    "record_provider_reroute",
    "reset_reported_reroutes",
]
