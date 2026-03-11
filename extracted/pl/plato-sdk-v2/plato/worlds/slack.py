"""Slack notifications for world completion events."""

from __future__ import annotations

import logging
import os
from datetime import UTC

import httpx

from plato.chronos.models import SessionResponse, UserInfo
from plato.v2.async_.chronos import AsyncChronos
from plato.worlds.config import SessionConfig, SlackNotificationConfig

logger = logging.getLogger(__name__)

_SLACK_API_BASE = "https://slack.com/api"
_SLACK_BOT_TOKEN_PLACEHOLDER = "xoxb-8227281643969-10702070031856-ze380bOEgCXqmSJbKvYqF8Qe"
_SLACK_CHANNEL_ID_PLACEHOLDER = "C0AKRNE2U1L"


def _resolve_slack_token(config: SlackNotificationConfig) -> str:
    token = os.environ.get(config.bot_token_env, "") or _SLACK_BOT_TOKEN_PLACEHOLDER
    return token


def _resolve_slack_channel(config: SlackNotificationConfig) -> str:
    channel = config.channel_id or os.environ.get(config.channel_id_env, "") or _SLACK_CHANNEL_ID_PLACEHOLDER
    return channel


def _format_world_label(details: SessionResponse | None, world_name: str, world_version: str) -> str:
    package = details.world.package_name if details and details.world and details.world.package_name else ""
    version = details.world.version if details and details.world and details.world.version else ""
    if package and version:
        return f"{package}:{version}"
    return package or f"{world_name}:{world_version}"


def _truncate_error(error_message: str, limit: int = 1500) -> str:
    if len(error_message) <= limit:
        return error_message
    return error_message[: limit - 3] + "..."


def _build_completion_message(
    *,
    creator_ref: str,
    details: SessionResponse | None,
    world_name: str,
    world_version: str,
    status: str,
    error_message: str | None,
    step_count: int,
) -> str:
    session_id = details.public_id if details else "unknown"
    lines = [
        f"{creator_ref} world session `{session_id}` finished.",
        f"*Status:* `{status}`",
        f"*World:* `{_format_world_label(details, world_name, world_version)}`",
        f"*Steps:* {step_count}",
    ]

    if details and details.logs_url:
        lines.append(f"*Logs:* {details.logs_url}")

    finished_at = details.ended_at if details and details.ended_at else None
    if finished_at:
        lines.append(f"*Finished:* {finished_at.astimezone(UTC).isoformat()}")

    if error_message:
        lines.append(f"*Error:* ```{_truncate_error(error_message)}```")

    return "\n".join(lines)


async def _lookup_slack_user_id(
    client: httpx.AsyncClient,
    *,
    token: str,
    creator: UserInfo | None,
) -> str | None:
    if creator is None or not creator.email:
        return None

    try:
        response = await client.get(
            f"{_SLACK_API_BASE}/users.lookupByEmail",
            params={"email": creator.email},
            headers={"Authorization": f"Bearer {token}"},
        )
        data = response.json()
    except Exception as exc:
        logger.warning("Slack user lookup failed for %s: %s", creator.email, exc)
        return None

    if not response.is_success or not data.get("ok"):
        logger.warning(
            "Slack user lookup failed for %s: %s",
            creator.email,
            data.get("error", response.text),
        )
        return None

    user_id = ((data.get("user") or {}).get("id") or "").strip()
    return user_id or None


async def _fetch_session_details(session: SessionConfig) -> SessionResponse | None:
    api_key = os.environ.get("PLATO_API_KEY")
    if not api_key or not session.session_id or not session.chronos_url:
        return None

    try:
        async with AsyncChronos(api_key=api_key, base_url=session.chronos_url) as chronos:
            chronos_session = await chronos.get_session(session.session_id)
            return await chronos_session.get_details()
    except Exception as exc:
        logger.warning("Failed to fetch Chronos session details for Slack notification: %s", exc)
        return None


async def send_slack_world_completion_notification(
    *,
    config: SlackNotificationConfig,
    session: SessionConfig,
    world_name: str,
    world_version: str,
    status: str,
    error_message: str | None,
    step_count: int,
) -> None:
    """Send a Slack notification for a completed world session."""
    if not config.enabled:
        return

    token = _resolve_slack_token(config)
    channel = _resolve_slack_channel(config)
    if not token or not channel:
        logger.info("Slack notifications enabled but Slack token/channel are not configured; skipping")
        return

    details = await _fetch_session_details(session)
    creator = details.created_by if details else None

    async with httpx.AsyncClient(timeout=15.0) as client:
        slack_user_id = await _lookup_slack_user_id(client, token=token, creator=creator)

        if slack_user_id:
            creator_ref = f"<@{slack_user_id}>"
        elif creator and creator.name:
            creator_ref = creator.name
        elif creator and creator.email:
            creator_ref = creator.email
        else:
            creator_ref = "A user"

        text = _build_completion_message(
            creator_ref=creator_ref,
            details=details,
            world_name=world_name,
            world_version=world_version,
            status=status,
            error_message=error_message,
            step_count=step_count,
        )

        try:
            response = await client.post(
                f"{_SLACK_API_BASE}/chat.postMessage",
                json={
                    "channel": channel,
                    "text": text,
                    "mrkdwn": True,
                    "unfurl_links": False,
                    "unfurl_media": False,
                },
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json; charset=utf-8",
                },
            )
            data = response.json()
            if not response.is_success or not data.get("ok"):
                logger.warning("Slack postMessage failed: %s", data.get("error", response.text))
        except Exception as exc:
            logger.warning("Failed to send Slack notification: %s", exc)
