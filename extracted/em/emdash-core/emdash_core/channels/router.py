"""ChannelRouter — routes outbound messages to the primary channel or stored fallback."""

from __future__ import annotations

import logging
from pathlib import Path

from .base import Channel, ChannelEvent, DeliveryResult
from .stored import StoredChannel

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Module-level singleton so tools / background tasks can reach the router
# without a reference to the FastAPI app.
# ---------------------------------------------------------------------------

_router: ChannelRouter | None = None


def get_channel_router() -> ChannelRouter | None:
    """Return the global ChannelRouter, or *None* if the server hasn't started."""
    return _router


def set_channel_router(router: ChannelRouter) -> None:
    """Set the global ChannelRouter (called once during server lifespan)."""
    global _router
    _router = router


class ChannelRouter:
    """Route outbound events to the user's active channel.

    Falls back to :class:`StoredChannel` when no live channel is available,
    ensuring messages are never lost.

    Channels register programmatically at startup::

        router = ChannelRouter(emdash_dir)
        router.register(telegram_channel)
        router.set_primary("telegram")
    """

    def __init__(self, emdash_dir: Path) -> None:
        self._stored = StoredChannel(emdash_dir)
        self._channels: dict[str, Channel] = {}
        self._primary_name: str | None = None
        self._last_sender: dict[str, str] = {}  # channel_name → last sender_id

    # -- Registration --

    def register(self, channel: Channel) -> None:
        """Register a channel by its ``name``."""
        self._channels[channel.name] = channel

    def unregister(self, name: str) -> None:
        """Remove a previously-registered channel."""
        self._channels.pop(name, None)
        if self._primary_name == name:
            self._primary_name = None

    def set_primary(self, name: str) -> None:
        """Set the primary delivery channel by name."""
        self._primary_name = name

    # -- Delivery --

    def track_sender(self, channel_name: str, sender_id: str) -> None:
        """Record the last sender_id for a channel (called on inbound messages)."""
        self._last_sender[channel_name] = sender_id

    @property
    def last_sender_id(self) -> str | None:
        """Return the sender_id for the primary (active) channel, if known.

        Only returns a sender tracked on the current primary channel so that
        scheduled deliveries never use a sender_id from a different channel
        (e.g. a CLI user id when Telegram is active).
        """
        if self._primary_name and self._primary_name in self._last_sender:
            return self._last_sender[self._primary_name]
        return None

    async def deliver(
        self, event: ChannelEvent, sender_id: str = "default"
    ) -> DeliveryResult:
        """Deliver an event to the primary channel, falling back to stored."""
        if self._primary_name and self._primary_name in self._channels:
            primary = self._channels[self._primary_name]
            try:
                if await primary.is_available():
                    result = await primary.send_event(sender_id, event)
                    if result.success:
                        return result
                    log.warning(
                        "Primary channel %s delivery failed: %s — falling back to stored",
                        self._primary_name,
                        result.error,
                    )
            except Exception as exc:
                log.warning(
                    "Primary channel %s raised %s: %s — falling back to stored",
                    self._primary_name,
                    type(exc).__name__,
                    exc,
                )
        # Fall back to stored channel
        return await self._stored.send_event(sender_id, event)

    # -- Pending messages --

    def get_pending(self) -> list[dict]:
        """Read and clear pending stored messages."""
        return self._stored.get_and_clear()

    # -- Introspection --

    @property
    def channels(self) -> dict[str, Channel]:
        """Return registered channels (read-only view)."""
        return dict(self._channels)

    @property
    def primary(self) -> Channel | None:
        """Return the current primary channel, if any."""
        if self._primary_name:
            return self._channels.get(self._primary_name)
        return None
