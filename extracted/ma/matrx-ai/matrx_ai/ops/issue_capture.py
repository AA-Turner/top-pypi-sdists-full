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
) -> None:
    try:
        from matrx_connect import try_get_app_context

        ctx = try_get_app_context()
    except Exception:
        ctx = None

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
) -> None:
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
            elif "streaming" in key or "context_length" in key or "invalid" in key:
                category_guess = "validation"

            issue_class = await auto_register_class(
                key,
                category=category_guess,
                provider=provider,
                severity="medium",
            )
            if issue_class is None:
                return

        if not issue_class.get("is_active", True):
            return

        issue_class_id = issue_class["id"]

        OpsIssueEvent = get_model("OpsIssueEvent")
        now = datetime.now(UTC)
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
