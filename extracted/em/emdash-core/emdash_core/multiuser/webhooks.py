"""Webhook registry and dispatcher for project/task events.

Core holds in-memory state and business logic. When mutations happen,
core fires webhooks to registered consumers. The consumer persists
to whatever backend it chooses (Firebase, SQLite, etc.).

Flow:
    1. Consumer registers:  POST /api/multiuser/webhooks/register
       { "url": "http://localhost:9100/hooks", "events": ["project.*", "task.*"] }

    2. Core mutates state (create project, assign task, etc.)

    3. Core fires webhook to all matching consumers:
       POST http://localhost:9100/hooks
       { "event": "project.created", "data": { ... }, "timestamp": "..." }

    4. Consumer receives webhook and persists however it wants

Webhook delivery is async and non-blocking — core doesn't wait for
the consumer to finish persisting. If the consumer is down, the event
is logged and skipped (consumer can resync via the sync endpoint).
"""

import asyncio
import fnmatch
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

import httpx

log = logging.getLogger(__name__)


@dataclass
class WebhookRegistration:
    """A registered webhook endpoint."""

    hook_id: str
    url: str
    events: list[str]  # glob patterns: "project.*", "task.assigned", "*"
    secret: Optional[str] = None  # optional shared secret for verification
    created_at: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def matches(self, event_name: str) -> bool:
        """Check if this hook should fire for the given event."""
        return any(fnmatch.fnmatch(event_name, pattern) for pattern in self.events)

    def to_dict(self) -> dict[str, Any]:
        return {
            "hook_id": self.hook_id,
            "url": self.url,
            "events": self.events,
            "created_at": self.created_at,
            "metadata": self.metadata,
        }


@dataclass
class WebhookEvent:
    """An event payload sent to webhook consumers."""

    event: str  # e.g. "project.created", "task.assigned"
    data: dict[str, Any]  # the full object dict
    timestamp: str
    event_id: str = ""

    def __post_init__(self):
        if not self.event_id:
            self.event_id = str(uuid.uuid4())
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event": self.event,
            "data": self.data,
            "timestamp": self.timestamp,
        }


class WebhookRegistry:
    """Manages webhook registrations and dispatches events.

    Usage:
        registry = WebhookRegistry()

        # Consumer registers
        hook_id = registry.register(
            url="http://localhost:9100/hooks",
            events=["project.*", "task.*"],
        )

        # Core fires event after a mutation
        await registry.dispatch("project.created", project.to_dict())

        # Consumer unregisters
        registry.unregister(hook_id)
    """

    def __init__(self, timeout: float = 5.0, max_retries: int = 0):
        self._hooks: dict[str, WebhookRegistration] = {}
        self._timeout = timeout
        self._max_retries = max_retries
        self._client: Optional[httpx.AsyncClient] = None

    def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self._timeout)
        return self._client

    def register(
        self,
        url: str,
        events: list[str],
        secret: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> str:
        """Register a webhook endpoint.

        Args:
            url: HTTP endpoint to POST events to
            events: List of event glob patterns to match
                    e.g. ["project.*"] matches project.created, project.updated, etc.
                    e.g. ["*"] matches everything
                    e.g. ["task.assigned", "task.status_changed"] matches only those
            secret: Optional shared secret (sent in X-Webhook-Secret header)
            metadata: Optional metadata about the consumer

        Returns:
            hook_id for unregistering
        """
        hook_id = str(uuid.uuid4())
        hook = WebhookRegistration(
            hook_id=hook_id,
            url=url,
            events=events,
            secret=secret,
            created_at=datetime.utcnow().isoformat(),
            metadata=metadata or {},
        )
        self._hooks[hook_id] = hook
        log.info(f"Registered webhook {hook_id} → {url} for events {events}")
        return hook_id

    def unregister(self, hook_id: str) -> bool:
        """Unregister a webhook endpoint."""
        if hook_id in self._hooks:
            hook = self._hooks.pop(hook_id)
            log.info(f"Unregistered webhook {hook_id} → {hook.url}")
            return True
        return False

    def list_hooks(self) -> list[dict[str, Any]]:
        """List all registered webhooks."""
        return [h.to_dict() for h in self._hooks.values()]

    async def dispatch(
        self,
        event_name: str,
        data: dict[str, Any],
        origin_user_id: Optional[str] = None,
    ) -> None:
        """Fire an event to all matching webhook consumers.

        This is async and non-blocking. Failed deliveries are logged
        but don't raise — the consumer can resync later.

        Args:
            event_name: Event name, e.g. "project.created", "task.assigned"
            data: The full object dict (project.to_dict(), task.to_dict(), etc.)
            origin_user_id: Who triggered this mutation (for echo loop prevention)
        """
        webhook_event = WebhookEvent(
            event=event_name,
            data={**data, "_origin": origin_user_id} if origin_user_id else data,
            timestamp=datetime.utcnow().isoformat(),
        )
        payload = webhook_event.to_dict()

        # Find all matching hooks
        matching = [h for h in self._hooks.values() if h.matches(event_name)]
        if not matching:
            return

        # Fire all in parallel, don't block
        tasks = [self._deliver(hook, payload) for hook in matching]
        await asyncio.gather(*tasks, return_exceptions=True)

    async def _deliver(
        self, hook: WebhookRegistration, payload: dict[str, Any]
    ) -> None:
        """Deliver a webhook event to a single consumer."""
        headers = {"Content-Type": "application/json"}
        if hook.secret:
            headers["X-Webhook-Secret"] = hook.secret

        client = self._get_client()
        for attempt in range(1 + self._max_retries):
            try:
                resp = await client.post(hook.url, json=payload, headers=headers)
                if resp.status_code < 400:
                    log.debug(
                        f"Webhook {hook.hook_id} delivered {payload['event']} "
                        f"→ {hook.url} ({resp.status_code})"
                    )
                    return
                log.warning(
                    f"Webhook {hook.hook_id} got {resp.status_code} from {hook.url}"
                )
            except Exception as e:
                log.warning(
                    f"Webhook {hook.hook_id} delivery failed (attempt {attempt + 1}): {e}"
                )
            if attempt < self._max_retries:
                await asyncio.sleep(1 * (attempt + 1))

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None


# ─────────────────────────────────────────────────────────────
# Global Instance
# ─────────────────────────────────────────────────────────────

_webhook_registry: Optional[WebhookRegistry] = None


def get_webhook_registry() -> WebhookRegistry:
    """Get the global WebhookRegistry instance."""
    global _webhook_registry
    if _webhook_registry is None:
        _webhook_registry = WebhookRegistry()
    return _webhook_registry


def set_webhook_registry(registry: WebhookRegistry) -> None:
    """Set the global WebhookRegistry instance."""
    global _webhook_registry
    _webhook_registry = registry
