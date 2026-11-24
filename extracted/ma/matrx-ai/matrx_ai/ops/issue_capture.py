from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from matrx_utils import vcprint

from matrx_ai._ext import get_ext, has_ext
from matrx_ai.db._registry import get_model


async def _resolve_organization_id(
    user_id: str | None,
    organization_id: str | None,
) -> str:
    if organization_id:
        return organization_id
    if not has_ext("ops_issue_organization_resolver"):
        raise RuntimeError(
            "ops issue capture requires organization_id or the host's "
            "ops_issue_organization_resolver"
        )
    resolver = get_ext("ops_issue_organization_resolver")
    resolved = await resolver(user_id=user_id, organization_id=organization_id)
    if not resolved:
        raise RuntimeError("ops_issue_organization_resolver returned no organization_id")
    return str(resolved)


async def _already_recorded_today(
    OpsIssueEvent: Any,
    issue_class_id: Any,
    model: str | None,
    now: datetime,
    day_key: tuple[str, ...] | None = None,
) -> bool:
    """True when today's (UTC) row for this class and model (and, when given, ``day_key``) already exists.

    ``day_key`` rides in the stored event's ``detail["day_key"]`` (a list), so the match is exact.
    A failed read files anyway."""
    start_of_day = datetime.combine(now.date(), datetime.min.time(), tzinfo=UTC)
    try:
        if day_key is not None:
            wanted = list(day_key)
            rows = await OpsIssueEvent.get_many(
                issue_class_id=issue_class_id, model=model, occurred_at__gte=start_of_day
            )
            return any((getattr(r, "detail", None) or {}).get("day_key") == wanted for r in rows)
        return bool(
            await OpsIssueEvent.exists(
                issue_class_id=issue_class_id, model=model, occurred_at__gte=start_of_day
            )
        )
    except Exception as exc:  # noqa: BLE001 - a failed dedupe read must not lose the finding
        vcprint(f"[OpsIssueCapture] day-dedupe read failed ({exc}); filing anyway", color="yellow")
        return False


async def capture_issue(
    key: str,
    *,
    error_type: str,
    provider: str | None = None,
    model: str | None = None,
    status_code: int | None = None,
    is_retryable: bool = False,
    was_recovered: bool = False,
    retry_count: int = 0,
    user_id: str | None = None,
    organization_id: str | None = None,
    conversation_id: str | None = None,
    request_id: str | None = None,
    detail: dict[str, Any] | None = None,
    severity: str = "medium",
    once_per_day: bool = False,
    day_key: tuple[str, ...] | None = None,
) -> None:
    """Record one issue event. ``severity`` applies when this call is the one
    that auto-registers the class (a class a person already triaged keeps its
    own severity). ``once_per_day`` makes a recovered capability FACT one row per
    (class, model, UTC day) across every process — an in-process guard alone is
    defeated by short-lived workers. ``day_key`` (only with ``once_per_day``) widens the natural
    key to (class, model, day_key, UTC day) — e.g. the agent and schema a finding is about; it is
    stored in ``detail["day_key"]``. Omitted, behaviour is unchanged."""
    try:
        from matrx_connect import try_get_app_context

        ctx = try_get_app_context()
    except Exception:
        ctx = None

    if model:
        # The column is read by people and grouped by model: a config holding the catalog
        # model's ID (a client sent ``ai_model_id``) filed events under a UUID (live 2026-11-19,
        # groq ``9f6c69bc-…`` = openai/gpt-oss-20b, google ``b32f2079-…`` = gemini-3.8-flash).
        # THE naming door, shared with the swap trace; a ref it cannot name is kept as given.
        from matrx_ai.config.unified_config import swap_model_name

        model = swap_model_name(model)

    if ctx is not None:
        user_id = user_id or ctx.user_id or None
        organization_id = organization_id or ctx.organization_id
        conversation_id = conversation_id or ctx.conversation_id
        request_id = request_id or ctx.request_id or None

    from matrx_utils import detached_task

    detached_task(
        _capture_impl(
            key,
            error_type=error_type,
            provider=provider,
            model=model,
            status_code=status_code,
            is_retryable=is_retryable,
            was_recovered=was_recovered,
            retry_count=retry_count,
            user_id=user_id,
            organization_id=organization_id,
            conversation_id=conversation_id,
            request_id=request_id,
            detail=detail or {},
            severity=severity,
            once_per_day=once_per_day,
            day_key=day_key,
        ),
        name=f"ops_issue_capture:{key}",
    )


async def _capture_impl(
    key: str,
    *,
    error_type: str,
    provider: str | None,
    model: str | None,
    status_code: int | None,
    is_retryable: bool,
    was_recovered: bool,
    retry_count: int,
    user_id: str | None,
    organization_id: str | None,
    conversation_id: str | None,
    request_id: str | None,
    detail: dict[str, Any],
    severity: str = "medium",
    once_per_day: bool = False,
    day_key: tuple[str, ...] | None = None,
) -> None:
    # THE PROVIDER-OUTAGE ALARM hangs off this writer because this is the ONE
    # place every classified provider error is counted: hooking the executor
    # instead would mean hooking six call sites and missing the seventh. Its own
    # try/except so neither half can break the other, and it never raises.
    # aidream/services/provider_outage/detector.py carries the law.
    try:
        from matrx_ai.ops.provider_outage import note_provider_failure

        _reroute = detail.get("overload_reroute")
        _to_model = _reroute.get("to_model") if isinstance(_reroute, dict) else None

        await note_provider_failure(
            provider=provider,
            model=model,
            error_type=error_type,
            status_code=status_code,
            error_text=str(detail.get("error") or detail.get("message") or "") or None,
            rerouted_to=str(_to_model) if _to_model else None,
        )
    except Exception as outage_exc:  # noqa: BLE001 — a broken alarm never breaks capture
        vcprint(
            f"[OpsIssueCapture] provider-outage detection failed: {outage_exc}",
            color="yellow",
        )

    try:
        from matrx_ai.ops.issue_registry import auto_register_class, get_issue_class

        issue_class = await get_issue_class(key)

        if issue_class is None:
            category_guess = "provider_error"
            if "rate_limit" in key:
                category_guess = "resource_limit"
            elif "auth" in key or "billing" in key:
                category_guess = "auth"
            elif "connection" in key or "timeout" in key:
                category_guess = "network"
            elif "content" in key or "safety" in key:
                category_guess = "content_policy"
            elif (
                "streaming" in key
                or "context_length" in key
                or "invalid" in key
                or key.startswith("structured_output.")
            ):
                category_guess = "validation"

            issue_class = await auto_register_class(
                key,
                category=category_guess,
                provider=provider,
                severity=severity,
            )
            if issue_class is None:
                return

        # A settled class never hides a recurrence: record the event AND reopen the class, through this
        # package's own OpsIssueClass model (never a host import).
        from matrx_ai.ops.issue_registry import reopen_settled_class

        await reopen_settled_class(
            issue_class,
            message=str(detail.get("error") or detail.get("message") or error_type),
        )

        issue_class_id = issue_class["id"]

        OpsIssueEvent = get_model("OpsIssueEvent")
        now = datetime.now(UTC)
        if once_per_day and day_key is not None:
            detail = {**detail, "day_key": list(day_key)}
        if once_per_day and await _already_recorded_today(OpsIssueEvent, issue_class_id, model, now, day_key):
            return
        organization_id = await _resolve_organization_id(user_id, organization_id)

        await OpsIssueEvent.create(
            id=str(uuid4()),
            issue_class_id=issue_class_id,
            provider=provider,
            model=model,
            error_type=error_type,
            status_code=status_code,
            is_retryable=is_retryable,
            was_recovered=was_recovered,
            retry_count=retry_count,
            user_id=user_id,
            organization_id=organization_id,
            conversation_id=conversation_id,
            request_id=request_id,
            detail=detail,
            occurred_at=now,
            created_at=now,
        )

    except Exception as exc:
        vcprint(
            f"[OpsIssueCapture] Failed to capture issue '{key}': {exc}",
            color="yellow",
        )
        from matrx_connect.streaming.error_capture import capture_error

        await capture_error(
            exc,
            kind="ops_issue_capture_failed",
            route="ops_issue_capture",
            error_type=type(exc).__name__,
            payload={"issue_key": key, "provider": provider, "model": model},
        )
