from __future__ import annotations

from typing import TYPE_CHECKING

from matrx_utils import vcprint

if TYPE_CHECKING:
    from matrx_connect.context.app_context import AppContext


class ChildSourceContextError(ValueError):
    """Raised when a child agent run is missing required source tracking."""

    error_type = "matrx_validation_gate"


MISSING_SOURCE_TRACKING_KIND = "agent_source_tracking_missing"


class MissingSourceTrackingError(RuntimeError):
    """Durable operational alarm for an agent run with incomplete provenance."""


def _capture_missing_source_tracking(
    *,
    handler: str,
    label: str | None,
    missing: list[str],
) -> None:
    """Best-effort structured capture through the host seam; never blocks a run."""
    try:
        from matrx_ai._ext import get_ext

        record_error = get_ext("record_error")
    except Exception:
        return

    error = MissingSourceTrackingError(
        f"agent source tracking missing {', '.join(missing)} at {handler}"
    )
    try:
        pending = record_error(
            error,
            kind=MISSING_SOURCE_TRACKING_KIND,
            error_type=MISSING_SOURCE_TRACKING_KIND,
            error_text=str(error),
            route=handler,
            payload={"handler": handler, "label": label, "missing": missing},
        )
        import inspect

        if inspect.isawaitable(pending):
            import asyncio

            try:
                asyncio.get_running_loop()
            except RuntimeError:
                pending.close()
                return
            from matrx_utils import detached_task

            detached_task(pending, name=MISSING_SOURCE_TRACKING_KIND)
    except Exception:
        # This is an alarm on a non-blocking compatibility guard. A broken
        # alarm must not turn the warning into a user-facing execution failure.
        return


async def capture_missing_source_tracking(
    ctx: AppContext,
    *,
    handler: str,
    label: str | None = None,
) -> bool:
    """Await the host's structured alarm at an async execution boundary.

    Returns ``True`` when provenance was incomplete, even when the optional
    host seam is unavailable.  Awaiting here lets a host finish the durable
    write before its request lane is drained.
    """
    missing: list[str] = []
    if not (ctx.source_app or "").strip():
        missing.append("source_app")
    if not (ctx.source_feature or "").strip():
        missing.append("source_feature")
    if not missing:
        return False

    try:
        from matrx_ai._ext import get_ext

        record_error = get_ext("record_error")
        error = MissingSourceTrackingError(
            f"agent source tracking missing {', '.join(missing)} at {handler}"
        )
        pending = record_error(
            error,
            kind=MISSING_SOURCE_TRACKING_KIND,
            error_type=MISSING_SOURCE_TRACKING_KIND,
            error_text=str(error),
            route=handler,
            payload={"handler": handler, "label": label, "missing": missing},
        )
        import inspect

        if inspect.isawaitable(pending):
            await pending
    except Exception:
        # The compatibility alarm remains non-blocking. The host boundary
        # awaits the write when available, but telemetry cannot fail a run.
        pass
    return True


def default_child_source_app() -> str:
    from matrx_ai._ext import get_ext, has_ext

    if has_ext("default_child_source_app"):
        return str(get_ext("default_child_source_app")).strip()
    return "matrx-ai"


def resolve_child_source(
    *,
    source_app: str | None,
    source_feature: str | None,
    caller: str,
) -> tuple[str, str]:
    """Resolve and validate (source_app, source_feature) for a child agent run.

    Every ``run_agent`` / direct ``child_agent_context`` path MUST call this
    before forking so the child ``cx_conversation`` is tagged with the
    mechanism that spawned it — never the parent request's feature.

    ``source_app`` may be omitted to use the host default
    (``default_child_source_app`` ext, else ``matrx-ai``).
    ``source_feature`` is required — it names the spawning surface
    (``agent_call``, ``page_summary``, …).
    """
    app = (source_app or "").strip() or default_child_source_app()
    feature = (source_feature or "").strip()
    if feature:
        return app, feature

    vcprint(
        "\n"
        "================================================================\n"
        "  matrx-ai — source_tracking.resolve_child_source\n"
        "  (child-agent source validation gate)\n"
        "----------------------------------------------------------------\n"
        "  My job: require source_feature on every child agent fork so\n"
        "          cx_conversation / usage report the spawning surface,\n"
        "          not the parent HTTP request's feature.\n"
        f"  Caller:  {caller}\n"
        f"  Got:     source_app={app!r} source_feature={feature!r}\n"
        "  Fix:     pass source_feature='...' to run_agent() or\n"
        "           NamedAgent.run(source_feature='...').\n"
        "  See:     matrx_ai.agents.executor.run_agent\n"
        "================================================================",
        color="red",
    )
    raise ChildSourceContextError(
        f"{caller} requires source_feature for child agent source tracking."
    )


def child_source_overrides(
    *,
    source_app: str | None,
    source_feature: str | None,
    caller: str,
) -> dict[str, str]:
    app, feature = resolve_child_source(
        source_app=source_app,
        source_feature=source_feature,
        caller=caller,
    )
    return {"source_app": app, "source_feature": feature}


def stamp_source_context(
    *,
    source_app: str,
    source_feature: str,
    only_if_unset: bool = True,
) -> None:
    from matrx_connect import set_app_context, try_get_app_context

    from matrx_ai.agents.conversation_type import (
        ConversationType,
        derive_conversation_type,
    )

    ctx = try_get_app_context()
    if ctx is None:
        return

    overrides: dict[str, str] = {}
    if only_if_unset:
        has_app = bool((ctx.source_app or "").strip())
        has_feature = bool((ctx.source_feature or "").strip())
        if not has_app:
            overrides["source_app"] = source_app
        if not has_feature:
            overrides["source_feature"] = source_feature
    else:
        overrides["source_app"] = source_app
        overrides["source_feature"] = source_feature

    # Classify the conversation from the source_feature being stamped, but only
    # while conversation_type is still the default. This makes every source
    # stamp ALSO set conversation_type explicitly at the construction site —
    # the same value the gate's derivation fallback would compute, but stamped
    # eagerly so it survives even if source_feature later drifts. An explicitly
    # non-standard type (e.g. a sub-agent fork) is never overwritten here.
    effective_feature = overrides.get("source_feature", ctx.source_feature)
    if (
        ctx.conversation_type or ConversationType.STANDARD.value
    ) == ConversationType.STANDARD.value:
        derived = derive_conversation_type(
            explicit=None,
            is_internal_agent=bool(ctx.is_internal_agent),
            source_feature=effective_feature,
            parent_conversation_id=ctx.parent_conversation_id,
        )
        if derived != ctx.conversation_type:
            overrides["conversation_type"] = derived

    if not overrides:
        return

    set_app_context(ctx.with_overrides(**overrides))


def warn_missing_source_tracking(
    ctx: AppContext,
    *,
    handler: str,
    label: str | None = None,
    capture: bool = True,
) -> None:
    missing: list[str] = []
    if not (ctx.source_app or "").strip():
        missing.append("source_app")
    if not (ctx.source_feature or "").strip():
        missing.append("source_feature")
    if not missing:
        return

    if capture:
        _capture_missing_source_tracking(
            handler=handler,
            label=label,
            missing=missing,
        )

    label_bit = f" label={label!r}" if label else ""
    vcprint(
        "\n"
        "══════════════════════════════════════════════════════════════════════\n"
        "  SOURCE TRACKING WARNING — cx_conversation / usage will be untagged\n"
        "══════════════════════════════════════════════════════════════════════\n"
        f"  handler:  {handler}{label_bit}\n"
        f"  missing:  {', '.join(missing)}\n"
        f"  current:  source_app={ctx.source_app!r} source_feature={ctx.source_feature!r}\n"
        "  fix:      ctx = ctx.with_overrides(source_app='...', source_feature='...')\n"
        "            set_app_context(ctx)  # before prepare_agent_run / run_agent\n"
        "  see:      matrx_ai.agents.executor.run_agent\n"
        "            aidream.services.ai_execution.agent_run.prepare_agent_run\n"
        "══════════════════════════════════════════════════════════════════════",
        color="red",
    )


def warn_missing_agent_attribution(
    ctx: AppContext,
    *,
    handler: str,
    label: str | None = None,
) -> None:
    """Scream LOUDLY when a DB-backed agent executes without agent attribution
    on the request context.

    A ``cx_user_request`` / ``cx_conversation`` written while ``ctx.agent_id`` and
    ``ctx.agent_version_id`` are both unset persists with NULL agent attribution
    — the work succeeds and is billed, but CX Explorer can never attribute the
    conversation, tokens, or cost back to the agent that produced it. This is the
    exact gap that hid every research / podcast / NER programmatic agent run.

    The HTTP ``/agents/{id}`` route stamps attribution in ``prepare_agent_run``;
    the programmatic path stamps it in ``run_agent`` (from ``Agent.source_id``).
    This guard is the tripwire that catches any NEW path that executes a
    DB-backed agent WITHOUT stamping. Loud, non-blocking by design (for now) —
    flip to a hard raise once the codebase is confirmed clean.
    """
    if ctx.agent_id or ctx.agent_version_id:
        return

    label_bit = f" label={label!r}" if label else ""
    vcprint(
        "\n"
        "══════════════════════════════════════════════════════════════════════\n"
        "  AGENT ATTRIBUTION WARNING — cx_* rows will be written with NULL\n"
        "  agent_id / agent_version_id. The run succeeds and is BILLED, but the\n"
        "  conversation, tokens, and cost can NEVER be attributed to the agent.\n"
        "══════════════════════════════════════════════════════════════════════\n"
        f"  handler:  {handler}{label_bit}\n"
        f"  current:  agent_id={ctx.agent_id!r} agent_version_id={ctx.agent_version_id!r}\n"
        f"            source_app={ctx.source_app!r} source_feature={ctx.source_feature!r}\n"
        "  fix:      run the agent through matrx_ai.agents.executor.run_agent\n"
        "            (it stamps attribution from Agent.source_id), OR stamp it\n"
        "            yourself before execute():\n"
        "              ctx = ctx.with_overrides(agent_id='...')          # floating\n"
        "              ctx = ctx.with_overrides(agent_version_id='...')  # pinned\n"
        "              set_app_context(ctx)\n"
        "  see:      matrx_ai.agents.executor.run_agent\n"
        "            aidream.services.ai_execution.agent_run.prepare_agent_run\n"
        "══════════════════════════════════════════════════════════════════════",
        color="red",
    )
