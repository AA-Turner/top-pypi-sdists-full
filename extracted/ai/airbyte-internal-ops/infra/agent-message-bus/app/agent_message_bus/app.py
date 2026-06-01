# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""FastAPI application for the GitHub Subscriptions webhook relay service.

This is the main entry point for the Cloud Run service. It exposes:
- POST /github/webhook — GitHub org-level webhook receiver
- POST /slack/webhook — Slack Block Kit interaction receiver
- POST /zendesk/webhook — Zendesk ticket webhook receiver
- CRUD /subscriptions/* — Subscription management API
- GET /health — Health check
"""

from __future__ import annotations

import hmac
import json
import logging
import os
import urllib.parse
from typing import Any

from fastapi import (
    BackgroundTasks,
    Depends,
    FastAPI,
    Header,
    HTTPException,
    Request,
    Response,
)

from agent_message_bus.firestore_client import SubscriptionStore
from agent_message_bus.github_handler import (
    handle_github_webhook,
    verify_github_signature,
)
from agent_message_bus.models import (
    CreateSubscriptionRequest,
    DeleteSubscriptionResponse,
    SubscriptionResponse,
)
from agent_message_bus.slack_handler import (
    handle_slack_interaction,
    verify_slack_signature,
)
from agent_message_bus.zendesk_handler import (
    handle_zendesk_webhook,
    verify_zendesk_signature,
)

# Configure root logger so all app loggers emit at INFO level
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s: %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="GitHub Subscriptions Webhook Relay",
    description=(
        "Receives GitHub, Slack, and Zendesk webhooks and relays notifications to Devin sessions."
    ),
    version="0.1.0",
)

# Lazily-initialized singleton store
_store: SubscriptionStore | None = None


def _get_store() -> SubscriptionStore:
    """Get or create the Firestore subscription store singleton."""
    global _store
    if _store is None:
        gcp_project = os.environ.get("GCP_PROJECT") or os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not gcp_project:
            raise ValueError(
                "GCP project is not configured. Set GCP_PROJECT or GOOGLE_CLOUD_PROJECT."
            )
        _store = SubscriptionStore(project=gcp_project)
    return _store


def _get_github_webhook_secret() -> str:
    """Retrieve the GitHub webhook secret from environment."""
    secret = os.environ.get("GITHUB_WEBHOOK_SECRET")
    if not secret:
        raise ValueError("GITHUB_WEBHOOK_SECRET environment variable is not set")
    return secret


def _get_slack_signing_secret() -> str:
    """Retrieve the Slack signing secret from environment."""
    secret = os.environ.get("SLACK_SIGNING_SECRET")
    if not secret:
        raise ValueError("SLACK_SIGNING_SECRET environment variable is not set")
    return secret


def _get_bearer_token() -> str:
    """Retrieve the expected bearer token from environment."""
    token = os.environ.get("SUBSCRIPTION_API_BEARER_TOKEN")
    if not token:
        raise ValueError("SUBSCRIPTION_API_BEARER_TOKEN environment variable is not set")
    return token


def _verify_bearer_token(authorization: str | None = Header(default=None)) -> None:
    """Dependency that verifies the bearer token on subscription endpoints."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    if not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")

    token = authorization[7:].strip()
    expected = _get_bearer_token()

    if not hmac.compare_digest(token, expected):
        raise HTTPException(status_code=403, detail="Invalid bearer token")


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------


@app.get("/health")
def health_check() -> dict[str, str]:
    """Simple health check endpoint."""
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# GitHub webhook endpoint
# ---------------------------------------------------------------------------


def _process_github_event(event_type: str, payload: dict[str, Any]) -> None:
    """Process a GitHub webhook event in a background task.

    This runs in a thread pool so synchronous Firestore + HTTP calls
    don't block the async event loop.
    """
    store = _get_store()
    result = handle_github_webhook(event_type=event_type, payload=payload, store=store)
    logger.info("GitHub webhook result: %s", result)


def _parse_webhook_body(body: bytes, content_type: str) -> dict[str, Any]:
    """Parse the webhook body, handling both JSON and form-encoded payloads.

    GitHub webhooks may send payloads as either `application/json` or
    `application/x-www-form-urlencoded` (with the JSON nested inside a
    `payload` form field), depending on how the webhook was registered.
    """
    if "application/x-www-form-urlencoded" in content_type:
        parsed = urllib.parse.parse_qs(body.decode("utf-8"))
        payload_str = parsed.get("payload", [""])[0]
        return json.loads(payload_str)
    return json.loads(body)


@app.post("/github/webhook")
async def github_webhook(request: Request, background_tasks: BackgroundTasks) -> dict[str, Any]:
    """Receive and process GitHub webhook events.

    Validates the webhook signature, then dispatches to a background task
    which matches events against Firestore subscriptions.
    """
    body = await request.body()
    signature = request.headers.get("X-Hub-Signature-256", "")
    event_type = request.headers.get("X-GitHub-Event", "")

    logger.info("GitHub webhook: event=%s, body_length=%d", event_type or "(empty)", len(body))

    if not event_type:
        raise HTTPException(status_code=400, detail="Missing X-GitHub-Event header")

    # Verify webhook signature
    try:
        secret = _get_github_webhook_secret()
    except ValueError as e:
        logger.error("GitHub webhook secret not configured: %s", e)
        raise HTTPException(status_code=500, detail="Webhook secret not configured") from e

    if not verify_github_signature(body, signature, secret):
        logger.warning("Webhook signature mismatch for event=%s", event_type)
        raise HTTPException(status_code=403, detail="Invalid webhook signature")

    # Parse payload — GitHub can send JSON or form-encoded depending on webhook config
    content_type = request.headers.get("content-type", "")
    try:
        payload = _parse_webhook_body(body, content_type)
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        logger.error("Invalid payload (content_type=%s): %s", content_type, str(e)[:200])
        raise HTTPException(status_code=400, detail="Invalid JSON payload") from e

    # Handle ping event (sent when webhook is first registered)
    if event_type == "ping":
        return {"status": "pong", "zen": payload.get("zen", "")}

    # Process in background so we respond quickly and don't block the event loop
    # with synchronous Firestore/HTTP calls
    background_tasks.add_task(_process_github_event, event_type, payload)
    return {"status": "accepted"}


# ---------------------------------------------------------------------------
# Slack webhook endpoint
# ---------------------------------------------------------------------------


def _process_slack_interaction(payload: dict[str, Any]) -> None:
    """Process a Slack interaction in a background task.

    This runs in a thread pool so the synchronous Devin API call
    doesn't block the response to Slack (which must be < 3 seconds).
    """
    result = handle_slack_interaction(payload)
    logger.info("Slack interaction result: %s", result)


@app.post("/slack/webhook")
async def slack_webhook(request: Request, background_tasks: BackgroundTasks) -> Response:
    """Receive and process Slack interactive component events.

    Validates the Slack signature, parses the interaction payload,
    and dispatches to a background task. Returns an empty 200 immediately
    (Slack requires a response within 3 seconds).
    """
    body = await request.body()
    timestamp = request.headers.get("X-Slack-Request-Timestamp", "")
    signature = request.headers.get("X-Slack-Signature", "")

    # Verify Slack signature
    try:
        signing_secret = _get_slack_signing_secret()
    except ValueError as e:
        logger.error("Slack signing secret not configured: %s", e)
        raise HTTPException(status_code=500, detail="Signing secret not configured") from e

    if not verify_slack_signature(body, timestamp, signature, signing_secret):
        raise HTTPException(status_code=403, detail="Invalid Slack signature")

    # Slack sends interaction payloads as form-encoded with a 'payload' field
    form_data = await request.form()
    payload_str = form_data.get("payload", "")
    if not payload_str:
        raise HTTPException(status_code=400, detail="Missing payload field")

    try:
        payload = json.loads(str(payload_str))
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail="Invalid JSON in payload field") from e

    # Process in background — acknowledge Slack immediately
    background_tasks.add_task(_process_slack_interaction, payload)

    # Slack expects an empty 200 response for acknowledgement
    return Response(status_code=200)


# ---------------------------------------------------------------------------
# Zendesk webhook endpoint
# ---------------------------------------------------------------------------


def _get_zendesk_signing_secret() -> str:
    """Retrieve the Zendesk webhook signing secret from environment."""
    secret = os.environ.get("ZENDESK_WEBHOOK_SIGNING_SECRET")
    if not secret:
        raise ValueError("ZENDESK_WEBHOOK_SIGNING_SECRET environment variable is not set")
    return secret


def _process_zendesk_event(payload: dict[str, Any]) -> None:
    """Process a Zendesk webhook event in a background task.

    This runs in a thread pool so the synchronous Devin API call
    doesn't block the async event loop.
    """
    result = handle_zendesk_webhook(payload)
    logger.info("Zendesk webhook result: %s", result)


@app.post("/zendesk/webhook")
async def zendesk_webhook(request: Request, background_tasks: BackgroundTasks) -> dict[str, Any]:
    """Receive and process Zendesk webhook events.

    Validates the Zendesk webhook signature, then dispatches to a
    background task which triggers the Devin triage playbook.
    """
    body = await request.body()
    signature = request.headers.get("X-Zendesk-Webhook-Signature", "")
    timestamp = request.headers.get("X-Zendesk-Webhook-Signature-Timestamp", "")

    logger.info("Zendesk webhook: body_length=%d", len(body))

    # Verify webhook signature
    try:
        signing_secret = _get_zendesk_signing_secret()
    except ValueError as e:
        logger.error("Zendesk webhook signing secret not configured: %s", e)
        raise HTTPException(status_code=500, detail="Webhook signing secret not configured") from e

    if not verify_zendesk_signature(body, signature, timestamp, signing_secret):
        logger.warning("Zendesk webhook signature mismatch")
        raise HTTPException(status_code=403, detail="Invalid webhook signature")

    # Parse JSON payload
    try:
        payload = json.loads(body)
    except json.JSONDecodeError as e:
        logger.error("Invalid Zendesk payload: %s", str(e)[:200])
        raise HTTPException(status_code=400, detail="Invalid JSON payload") from e

    # Process in background so we respond quickly
    background_tasks.add_task(_process_zendesk_event, payload)
    return {"status": "accepted"}


# ---------------------------------------------------------------------------
# Subscription CRUD endpoints
# ---------------------------------------------------------------------------


@app.post(
    "/subscriptions",
    response_model=SubscriptionResponse,
    dependencies=[Depends(_verify_bearer_token)],
)
def create_subscription(
    request: CreateSubscriptionRequest,
) -> SubscriptionResponse:
    """Create or upsert a subscription.

    If a subscription already exists for the same session + issue/PR,
    it is updated (TTL extended, watch_events merged).
    """
    store = _get_store()
    sub = store.create_or_update(request)
    return SubscriptionResponse(
        id=sub.id,
        github_url=sub.github_url,
        session_url=sub.session_url,
        owner=sub.owner,
        repo=sub.repo,
        number=sub.number,
        type=sub.type,
        watch_events=sub.watch_events,
        expires_at=sub.expires_at,
        created_at=sub.created_at,
    )


@app.get(
    "/subscriptions",
    response_model=list[SubscriptionResponse],
    dependencies=[Depends(_verify_bearer_token)],
)
def list_subscriptions(session_url: str) -> list[SubscriptionResponse]:
    """List active subscriptions for a Devin session."""
    store = _get_store()
    subs = store.find_by_session(session_url)
    return [
        SubscriptionResponse(
            id=sub.id,
            github_url=sub.github_url,
            session_url=sub.session_url,
            owner=sub.owner,
            repo=sub.repo,
            number=sub.number,
            type=sub.type,
            watch_events=sub.watch_events,
            expires_at=sub.expires_at,
            created_at=sub.created_at,
        )
        for sub in subs
    ]


@app.delete(
    "/subscriptions/{subscription_id}",
    response_model=DeleteSubscriptionResponse,
    dependencies=[Depends(_verify_bearer_token)],
)
def delete_subscription(subscription_id: str) -> DeleteSubscriptionResponse:
    """Delete a subscription by its ID."""
    store = _get_store()
    deleted = store.delete_by_id(subscription_id)
    count = 1 if deleted else 0
    return DeleteSubscriptionResponse(
        deleted_count=count,
        message=f"Deleted {count} subscription(s).",
    )


@app.delete(
    "/subscriptions",
    response_model=DeleteSubscriptionResponse,
    dependencies=[Depends(_verify_bearer_token)],
)
def delete_subscriptions_by_match(
    session_url: str,
    github_url: str | None = None,
) -> DeleteSubscriptionResponse:
    """Delete subscriptions matching session URL and optionally GitHub URL."""
    store = _get_store()
    count = store.delete_by_match(session_url=session_url, github_url=github_url)
    return DeleteSubscriptionResponse(
        deleted_count=count,
        message=f"Deleted {count} subscription(s).",
    )
