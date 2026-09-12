"""THE RUNTIME MANDATE-CARRIER GATE — every AI call names its Holder, or screams.

THE BLIND SPOT THIS CLOSES (2026-09-11)
---------------------------------------
The ruling was never missing. ``/systems/mandates/ROLLOUT.md`` lines 45-50 rule
that code reaching ``llm_to_text``, ``llm_to_pydantic``, ``UnifiedAIClient`` or
``execute_ai_request`` without first resolving a Mandate is a BYPASS under the
Universal Law, and worklist row **A10** (ROLLOUT.md:197-210) has named these
exact files since 2026-08-18 under the heading *"Mandate guard cannot see this
class"*. No guard was ever built for it. This is that guard.

The static scanner (``matrx-mandate-scan``) answers "who calls a mandate?" by
finding raw provider SDK imports and declared mandate carriers. It is blind, BY
CONSTRUCTION, to our own executor: a call that goes through
``execute_ai_request`` imports no provider SDK and names no mandate, so a code
path carrying nothing but a model id read out of a node's config looked exactly
like a fully governed mandate run to every guard we had.

Measured that morning: every AI step node in ``matrx_ai.graph_nodes`` (extract,
llm, chat, image, video, the agent loop, the strict-JSON funnel) reached the
provider with a bare model id and no Holder of any kind — one of them with
``"gpt-4o-mini"`` hard-coded in code as its default, which is itself a PINS LAW
violation (``/systems/mandates/RUNTIME.md`` § THE PINS LAW: code never
references a model). Nothing anywhere said so.

WHAT A CARRIER IS
-----------------
A carrier is a DECLARED way the Holder of this call reaches the executor. There
are four, in precedence order, and they are the ones the platform already
writes — this module invented none of them:

1. ``execute_ai_request(..., mandate_key="...")`` — the explicit parameter,
   added 2026-09-11. The funnel had NO mandate parameter at all before that
   (audit census, ``docs/handoffs/mandate-guard-gap-2026-09-11.md``): 14 of 17
   call sites reached the model with no mandate identity of any kind.
2. ``metadata["mandate_key"]`` passed to :func:`execute_ai_request`, and
   ``ctx.metadata["mandate_key"]`` — what
   ``aidream.services.ai_execution.agent_run.prepare_agent_run`` stamps from
   ``request._mandate_key`` for every mandated chat/agent start.
3. ``ctx.source_feature`` beginning ``"mandate:"`` — what
   ``aidream.services.mandates.service.run_mandate`` stamps on the agent lane.
4. ``ctx.agent_id`` / ``ctx.agent_version_id`` — an authored Holder from the
   database is running. Not a mandate key, but a named, findable Holder; a raw
   agent id is its own D20 fix-list row, tracked by the hardcoded-agent guards,
   not a runtime blind spot.

Anything else is a **mandate bypass**: intelligence running with no Holder.

WHAT HAPPENS THEN — AND WHY IT IS NEVER A RAISE
-----------------------------------------------
`D20 </systems/mandates/DECISIONS.md>`_ (Arman, 2026-09-09): intelligence
outside a Mandate "is not okay… we absolutely will not create new ones. But for
now, we'll live with the ones we've got until we have time to fix them." A
bypass is therefore a DEFECT ROW, never a refusal — turning today's inventory
into 500s would take the platform down to enforce a list we already agreed to
work off.

**D23** is the rule this follows in code: checks "scream loud and red and
REPORT… but without blocking", and "things can be found and reported through our
error system so that they can then be handled by automated agents". So a bypass
here is: a red terminal scream naming the caller, a structured logger line,
``metadata["mandate_bypass"]`` stamped onto the request the persistence layer
already writes, and ONE ``ops.system_error`` row of kind
``mandate_bypass_runtime`` under ``source_app='mandate-scan'`` — the same door
and the same source_app ``matrx_mandate_scan.transport`` and the 4-hourly
``mandate_reference_patrol`` already use, so the existing reconciliation and the
references board pick it up with zero new surface. It never raises, and there is no
strictness knob: D20 and D23 together leave exactly one behavior, so a knob here
would be an invented opinion (`the ten laws` § 6 — knobs are for behavioral
choices organizations get to make, and this is not one).

`D21 </systems/mandates/DECISIONS.md>`_ is why the row is written even for a
path nobody can reach today: unreachable is a red flag, never a filter.

ONE ROW PER CODE PATH PER PROCESS. The signature is (caller site, model). A
workflow running ten thousand extract steps produces one row, not ten thousand —
the fact being reported is "this code path has no Holder", which is true once.

Guards: ``uv run pytest packages/matrx-ai/tests/test_mandate_carrier_guard.py``
(runtime) and ``python scripts/check_mandate_call_sites.py`` (the static ratchet
over the whole funnel vocabulary ROLLOUT.md:45-48 names).
"""

from __future__ import annotations

import inspect
import logging
from pathlib import Path
from typing import Any

from matrx_utils import vcprint

logger = logging.getLogger(__name__)

#: The ``system_error.kind`` written when an AI call reaches the executor with
#: no Holder of any kind. Named once, here; the census script and the admin
#: queue read this same string.
MANDATE_BYPASS_KIND = "mandate_bypass_runtime"

#: The metadata key that carries a mandate through the executor. Already the
#: platform's convention (``agent_run.prepare_agent_run`` writes it); named here
#: so a caller can import it instead of retyping the string.
MANDATE_KEY_METADATA_KEY = "mandate_key"

#: The metadata key the bypass record is stamped under, so a persisted request
#: carries the fact that nothing held it.
MANDATE_BYPASS_METADATA_KEY = "mandate_bypass"

#: ``source_feature`` prefix ``run_mandate`` stamps on the agent lane.
MANDATE_SOURCE_FEATURE_PREFIX = "mandate:"

#: The ``source_app`` every mandate-scan finding is filed under — shared with
#: ``matrx_mandate_scan.transport`` and ``mandates.reference_patrol`` so the
#: existing reconciliation sweep and the references board see these rows too.
MANDATE_SCAN_SOURCE_APP = "mandate-scan"

#: Signatures already reported in this process. See ONE ROW PER CODE PATH above.
_REPORTED: set[tuple[str, str]] = set()

#: Frames that are this gate or the executor itself — never the caller.
_OWN_MODULES = (
    "matrx_ai/orchestrator/mandate_carrier.py",
    "matrx_ai/orchestrator/executor.py",
)


class MandateBypassAtRuntime(RuntimeError):
    """An AI call reached the executor with no Holder. Recorded, never raised.

    It is an exception type only because ``record_error`` captures exceptions —
    the platform's one door for a ``system_error`` row. Nothing raises it.
    """


def _stack_caller() -> str:
    """The first frame outside this gate and the executor — file:line in func.

    Derived, never declared: a caller that had to name itself would be one more
    thing to forget, and the sites this exists to catch are exactly the ones
    nobody remembered to annotate.
    """
    try:
        for frame_info in inspect.stack()[1:]:
            filename = frame_info.filename.replace("\\", "/")
            if any(own in filename for own in _OWN_MODULES):
                continue
            if "/importlib/" in filename or filename.startswith("<"):
                continue
            parts = Path(filename).parts
            short = "/".join(parts[-3:]) if len(parts) >= 3 else filename
            return f"{short}:{frame_info.lineno} in {frame_info.function}"
    except Exception:  # noqa: BLE001 — a broken stack walk must not break a run
        pass
    return "unknown"


def _context() -> Any | None:
    try:
        from matrx_connect.context.app_context import try_get_app_context

        return try_get_app_context()
    except Exception:  # noqa: BLE001 — no context is a normal state, not a failure
        return None


def carrier_for(
    metadata: dict[str, Any] | None = None,
    ctx: Any | None = None,
    *,
    mandate_key: str | None = None,
) -> tuple[str, str] | None:
    """The Holder carrier for this call, as ``(carrier_name, value)``, or None.

    The four declared carriers, in precedence order — see the module docstring.
    """
    if isinstance(mandate_key, str) and mandate_key.strip():
        return ("mandate_key", mandate_key.strip())

    if isinstance(metadata, dict):
        explicit = metadata.get(MANDATE_KEY_METADATA_KEY)
        if isinstance(explicit, str) and explicit.strip():
            return ("metadata.mandate_key", explicit.strip())

    if ctx is None:
        ctx = _context()
    if ctx is None:
        return None

    ctx_metadata = getattr(ctx, "metadata", None)  # orm-getattr-ok: AppContext
    if isinstance(ctx_metadata, dict):
        inherited = ctx_metadata.get(MANDATE_KEY_METADATA_KEY)
        if isinstance(inherited, str) and inherited.strip():
            return ("context.metadata.mandate_key", inherited.strip())

    source_feature = getattr(ctx, "source_feature", "") or ""  # orm-getattr-ok: AppContext
    if isinstance(source_feature, str) and source_feature.startswith(
        MANDATE_SOURCE_FEATURE_PREFIX
    ):
        return (
            "context.source_feature",
            source_feature[len(MANDATE_SOURCE_FEATURE_PREFIX) :].strip() or source_feature,
        )

    for attribute, name in (
        ("agent_id", "context.agent_id"),
        ("agent_version_id", "context.agent_version_id"),
    ):
        value = getattr(ctx, attribute, None)  # orm-getattr-ok: AppContext
        if isinstance(value, str) and value.strip():
            return (name, value.strip())

    return None


def _record(
    *,
    caller: str,
    model: str,
    spec_type: str | None,
    ctx: Any | None,
) -> None:
    """Write the ``system_error`` row through the host's own door. Never raises."""
    try:
        from matrx_ai._ext import get_ext, has_ext

        if not has_ext("record_error"):
            return
        record_error = get_ext("record_error")
    except Exception:  # noqa: BLE001 — no host wiring is a normal standalone state
        return

    error = MandateBypassAtRuntime(
        f"AI call with no mandate Holder at {caller} (model={model or 'unset'}"
        + (f", spec_type={spec_type}" if spec_type else "")
        + ")"
    )
    try:
        pending = record_error(
            error,
            kind=MANDATE_BYPASS_KIND,
            error_type=MANDATE_BYPASS_KIND,
            error_text=str(error),
            source_app=MANDATE_SCAN_SOURCE_APP,
            route=caller,
            user_id=getattr(ctx, "user_id", None) or None,  # orm-getattr-ok: AppContext
            organization_id=getattr(ctx, "organization_id", None),  # orm-getattr-ok: AppContext
            conversation_id=getattr(ctx, "conversation_id", None),  # orm-getattr-ok: AppContext
            request_id=getattr(ctx, "request_id", None) or None,  # orm-getattr-ok: AppContext
            payload={
                "caller": caller,
                "model": model,
                "spec_type": spec_type,
                "source_app": getattr(ctx, "source_app", None),  # orm-getattr-ok: AppContext
                "source_feature": getattr(ctx, "source_feature", None),  # orm-getattr-ok: AppContext
                "carriers_checked": [
                    "metadata.mandate_key",
                    "context.metadata.mandate_key",
                    "context.source_feature",
                    "context.agent_id",
                ],
            },
        )
        if inspect.isawaitable(pending):
            import asyncio

            try:
                asyncio.get_running_loop()
            except RuntimeError:
                pending.close()
                return
            from matrx_utils import detached_task

            detached_task(pending, name=MANDATE_BYPASS_KIND)
    except Exception:  # noqa: BLE001 — a broken alarm never becomes a failed run
        return


def note_mandate_carrier(
    config: Any,
    metadata: dict[str, Any] | None = None,
    *,
    mandate_key: str | None = None,
) -> dict[str, Any] | None:
    """Entry gate: name the Holder of this AI call, or record the bypass.

    Returns the bypass record (``{"reason", "caller", "model", "spec_type"}``)
    when nothing holds the call, so the executor can stamp it onto the request
    metadata the persistence layer already writes; returns ``None`` when the
    call is held.

    NEVER raises and NEVER refuses — D20 (the inventory is a fix list, not a
    licence) and D23 (scream and report, never block) together.
    """
    try:
        ctx = _context()
        if carrier_for(metadata, ctx, mandate_key=mandate_key) is not None:
            return None

        model = ""
        try:
            model = str(getattr(config, "model", "") or "")  # orm-getattr-ok: UnifiedConfig
        except Exception:  # noqa: BLE001
            model = ""

        spec_type = None
        for source in (metadata, getattr(ctx, "metadata", None)):  # orm-getattr-ok: AppContext
            if isinstance(source, dict):
                candidate = source.get("spec_type") or source.get("node_type")
                if isinstance(candidate, str) and candidate.strip():
                    spec_type = candidate.strip()
                    break

        caller = _stack_caller()
        record = {
            "reason": "no_mandate_carrier",
            "caller": caller,
            "model": model,
            "spec_type": spec_type,
        }

        signature = (caller, model)
        if signature in _REPORTED:
            return record
        _REPORTED.add(signature)

        vcprint(
            "\n"
            "================================================================\n"
            "  MANDATE BYPASS AT RUNTIME — an AI call with no Holder\n"
            "----------------------------------------------------------------\n"
            f"  Caller:    {caller}\n"
            f"  Model:     {model or '(unset)'}\n"
            f"  Step type: {spec_type or '(none)'}\n"
            "  Why it matters: no Mandate holds this call, so nobody can\n"
            "          rebind it, price it, version it, or find it. Ruled a\n"
            "          bypass by ROLLOUT.md:45-50, inventoried as row A10.\n"
            "  Fix:     pass mandate_key=<declared key> to execute_ai_request,\n"
            "           or run it through run_mandate.\n"
            f"  Recorded: ops.system_error kind={MANDATE_BYPASS_KIND} "
            f"source_app={MANDATE_SCAN_SOURCE_APP}\n"
            "================================================================",
            color="red",
        )
        logger.error(
            "[mandates] mandate_bypass_runtime: AI call with no Holder at %s (model=%s, "
            "spec_type=%s)",
            caller,
            model or "unset",
            spec_type or "none",
        )
        _record(caller=caller, model=model, spec_type=spec_type, ctx=ctx)
        return record
    except Exception:  # noqa: BLE001 — the gate can never fail a real AI request
        return None


def reset_reported_signatures() -> None:
    """Clear the per-process dedupe. For tests only."""
    _REPORTED.clear()


# ── The declared pass-through ───────────────────────────────────────────────


def mandate_carrier_passthrough(reason: str):
    """DECLARE that this function's Holder is supplied by its caller.

    The static half of the same idea ``aidream.services.mandates.carriers``
    already carries for mandate keys: some ``execute_ai_request`` callers are
    generic funnels (``llm_messages_to_pydantic``, ``Agent.execute``, the chat
    task body, the parallel executor). Their Holder legitimately arrives as
    DATA — on the metadata they were handed, or on the AppContext their caller
    stamped — so no literal at that line could ever be honest.

    Declaring it does three things a silent pass-through does not: it names the
    reason in the code, it lets
    ``scripts/check_runtime_mandate_carriers.py`` tell "declared pass-through"
    apart from "nobody thought about it", and it keeps the runtime gate above
    as the real check — a declared pass-through that is handed NOTHING still
    records ``mandate_bypass_runtime``, naming the caller that forgot.

    Inert at runtime: it returns the function unchanged with one attribute set.
    """
    if not reason or not reason.strip():
        raise ValueError(
            "mandate_carrier_passthrough requires a reason naming WHO supplies "
            "the Holder at this call site"
        )

    def decorate(func):
        func.__mandate_carrier_passthrough__ = reason.strip()
        return func

    return decorate
