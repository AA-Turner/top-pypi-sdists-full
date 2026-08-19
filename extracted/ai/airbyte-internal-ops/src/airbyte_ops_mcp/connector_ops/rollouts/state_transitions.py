# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Rollout state transitions that need business logic on top of the Config API.

The Config API exposes rollout *endpoints*, not rollout *operations*: there is no
unpause endpoint, and a pause is only meaningful with a reason recorded on it. The
functions here own that gap so every caller — Autopilot, the MCP tools, and the Ops
Webapp — performs the same transition the same way, and so no caller has to know
which endpoint implements it or what inputs that endpoint demands.
"""

from __future__ import annotations

from typing import Any

from airbyte.exceptions import PyAirbyteInputError

from airbyte_ops_mcp.cloud_admin import api_client

# The platform rejects a progression that requests neither actor IDs nor a positive
# target percentage, so a rollout with nothing pinned yet resumes at the smallest
# step the API accepts.
MIN_RESUME_PERCENTAGE = 1


def pause_rollout(
    docker_repository: str,
    docker_image_tag: str,
    actor_definition_id: str,
    rollout_id: str,
    updated_by: str,
    paused_reason: str,
    config_api_root: str,
    client_id: str | None = None,
    client_secret: str | None = None,
    bearer_token: str | None = None,
) -> dict[str, Any]:
    """Pause a rollout, holding it in place with its existing pins retained.

    Autopilot skips a `paused` rollout, so this is the reversible way to stop a
    rollout without withdrawing the version: pinned customers stay on the release
    candidate and nobody new is pinned. `paused_reason` is required — an unexplained
    hold gives the next operator nothing to act on, and Autopilot reads the reason to
    tell its own failure-threshold hold apart from an operator's.

    Returns the updated rollout response.
    """
    paused_reason = paused_reason.strip()
    if not paused_reason:
        raise PyAirbyteInputError(
            message="A reason is required to pause a rollout.",
            context={"rollout_id": rollout_id},
        )

    return api_client.pause_connector_rollout(
        docker_repository=docker_repository,
        docker_image_tag=docker_image_tag,
        actor_definition_id=actor_definition_id,
        rollout_id=rollout_id,
        updated_by=updated_by,
        paused_reason=paused_reason,
        config_api_root=config_api_root,
        client_id=client_id,
        client_secret=client_secret,
        bearer_token=bearer_token,
    )


def unpause_rollout(
    docker_repository: str,
    docker_image_tag: str,
    actor_definition_id: str,
    rollout_id: str,
    updated_by: str,
    config_api_root: str,
    client_id: str | None = None,
    client_secret: str | None = None,
    bearer_token: str | None = None,
) -> tuple[int, dict[str, Any]]:
    """Resume a paused rollout and hand it back to Autopilot where it stopped.

    Autopilot advances a rollout again as soon as its state is `in_progress`, and the
    platform has no unpause endpoint: a manual progression accepts a `paused` rollout
    and writes that state. So this submits the smallest progression that performs the
    transition — the percentage the rollout has already reached, which pins nobody new
    because the platform skips pinning once the target is already met. The percentage
    is read from the rollout itself rather than asked of the caller; a rollout with
    nothing pinned yet resumes at `1%`, pinning one customer.

    The progression is submitted as a manual rollout, so the rollout stays
    operator-driven from the platform's perspective.

    Returns the percentage the rollout resumed at, and the updated rollout response.
    """
    rollout = api_client.get_connector_rollout(
        rollout_id=rollout_id,
        config_api_root=config_api_root,
        client_id=client_id,
        client_secret=client_secret,
        bearer_token=bearer_token,
    )
    current_percentage: int = rollout.get("current_target_rollout_pct") or 0
    resume_percentage = max(current_percentage, MIN_RESUME_PERCENTAGE)

    response = api_client.progress_connector_rollout(
        docker_repository=docker_repository,
        docker_image_tag=docker_image_tag,
        actor_definition_id=actor_definition_id,
        rollout_id=rollout_id,
        updated_by=updated_by,
        config_api_root=config_api_root,
        target_percentage=resume_percentage,
        client_id=client_id,
        client_secret=client_secret,
        bearer_token=bearer_token,
    )
    return resume_percentage, response
