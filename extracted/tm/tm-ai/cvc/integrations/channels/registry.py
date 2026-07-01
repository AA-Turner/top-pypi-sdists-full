"""
Channel registry for CVC.

The registry is the single source of truth for:

  - which adapters are loaded (from config)
  - which are running
  - the inbound → CVC-commit → agent → outbound pipeline
  - the status each adapter reports (for /api/channels and the dashboard)

Adding a new channel is three lines in the bootstrapper:
    from cvc.integrations.channels.telegram import TelegramAdapter
    registry.register("telegram", TelegramAdapter)
    await registry.start("telegram", config)

The registry also exposes :func:`handle_inbound_message`, the function
the gateway calls when ANY channel pushes a message into CVC. That
function:

  1. Creates a CVC cognitive commit (the "time machine" — even if the
     agent fails afterwards, the user's message is preserved).
  2. Runs the agent on the message via the gateway's chat pipeline.
  3. Returns the agent's reply to the registry, which dispatches it
     back to the originating channel.
"""

from __future__ import annotations

import asyncio
import logging
import time
from typing import Any, Awaitable, Callable, Dict, List, Optional

from .base import (
    BaseChannelAdapter,
    Capability,
    ChannelStatus,
    InboundMessage,
    OutboundMessage,
)


logger = logging.getLogger(__name__)


# Callback the registry calls to run the agent. Returns the agent's
# reply text (the registry wraps it in OutboundMessage + dispatches).
AgentRunner = Callable[[InboundMessage], Awaitable[Optional[str]]]

# Optional callback the registry calls BEFORE the agent runs, so the
# caller can persist the inbound message as a CVC commit. Receives the
# InboundMessage and the would-be agent prompt (a derived string). May
# return a commit hash or any serialisable marker.
CommitHook = Callable[[InboundMessage, str], Awaitable[Optional[str]]]


class ChannelRegistry:
    """Owns every adapter instance and routes messages to/from them."""

    def __init__(
        self,
        agent_runner: Optional[AgentRunner] = None,
        commit_hook: Optional[CommitHook] = None,
    ) -> None:
        self._adapters: Dict[str, BaseChannelAdapter] = {}
        self._agent_runner = agent_runner
        self._commit_hook = commit_hook
        self._lock = asyncio.Lock()

    # ── Registration ────────────────────────────────────────────────

    def register(self, name: str, adapter: BaseChannelAdapter) -> None:
        """Register an already-instantiated adapter.

        If an adapter with the same name is already registered, it is
        stopped first so we never leak background tasks across reloads.
        """
        if name in self._adapters:
            logger.warning("registry: replacing already-registered adapter %r", name)
            old = self._adapters.pop(name)
            try:
                asyncio.create_task(old.stop())
            except RuntimeError:
                pass
        adapter.name = name
        # Wrap the async handler in a plain async closure so the adapter
        # gets the callable signature it expects.
        async def _inbound(msg: InboundMessage) -> Optional[OutboundMessage]:
            return await self._handle_inbound(name, msg)
        adapter.set_inbound_handler(_inbound)
        self._adapters[name] = adapter
        logger.info("registry: registered adapter %r", name)

    def unregister(self, name: str) -> None:
        if name in self._adapters:
            adapter = self._adapters.pop(name)
            try:
                asyncio.create_task(adapter.stop())
            except RuntimeError:
                pass

    # ── Lifecycle ───────────────────────────────────────────────────

    async def start(self, name: str, config: Dict[str, Any]) -> None:
        """Start a registered adapter with the given config.

        The adapter was originally registered with an empty config dict
        (the bootstrapper has no per-user secrets). We need to REPLACE
        that dict with the live config the gateway loaded from disk
        BEFORE we call ``adapter.start()`` — otherwise the adapter
        reads ``self.cfg("bot_token", "")`` and gets the empty default
        instead of the real token. This was the root cause of the
        "config says X but the bot says token is required" mismatch.
        """
        async with self._lock:
            adapter = self._adapters.get(name)
            if adapter is None:
                raise KeyError(f"no adapter registered for {name!r}")
            # Inject the live config. We re-bind the attribute (rather
            # than mutating in place) so any per-adapter "config was
            # already set" assertions in subclasses still see the new
            # dict as a complete replacement.
            adapter.config = dict(config or {})
            await adapter.start()
            adapter._started_at = time.time()

    async def stop(self, name: str) -> None:
        async with self._lock:
            adapter = self._adapters.get(name)
            if adapter is None:
                return
            await adapter.stop()

    async def start_all(self, configs: Dict[str, Dict[str, Any]]) -> None:
        for name, cfg in configs.items():
            if name not in self._adapters:
                logger.warning("registry: skipping unknown adapter %r", name)
                continue
            if not cfg.get("enabled", False):
                logger.info("registry: %r disabled in config, skipping", name)
                continue
            try:
                await self.start(name, cfg)
            except Exception as exc:  # noqa: BLE001
                logger.exception("registry: %r failed to start: %s", name, exc)
                self._adapters[name]._last_error = str(exc)
                self._adapters[name]._healthy = False

    async def stop_all(self) -> None:
        for name in list(self._adapters.keys()):
            try:
                await self.stop(name)
            except Exception as exc:  # noqa: BLE001
                logger.warning("registry: %r stop failed: %s", name, exc)

    # ── Outbound send (called by gateway / dashboard) ───────────────

    async def send(self, channel: str, message: OutboundMessage) -> Dict[str, Any]:
        adapter = self._adapters.get(channel)
        if adapter is None:
            raise KeyError(f"no adapter for channel {channel!r}")
        self._ensure_capability(adapter, message)
        return await adapter.send(message)

    def _ensure_capability(self, adapter: BaseChannelAdapter, message: OutboundMessage) -> None:
        caps = set(adapter.capabilities())
        problems: List[str] = []
        if message.text and Capability.TEXT not in caps:
            problems.append("text")
        if message.media and Capability.MEDIA not in caps:
            problems.append("media")
        if message.inline_keyboard and Capability.INLINE_KEYBOARD not in caps:
            problems.append("inline_keyboard")
        if message.edit_message_id and Capability.EDIT not in caps:
            problems.append("edit")
        if problems:
            raise ValueError(
                f"channel {adapter.name!r} does not support: {', '.join(problems)}"
            )

    # ── Inbound handler (called by adapters) ─────────────────────────

    async def _handle_inbound(self, channel_name: str, msg: InboundMessage) -> Optional[OutboundMessage]:
        # Make sure `msg.channel` matches reality.
        msg.channel = channel_name
        prompt = self._build_prompt(msg)
        # 1) CVC commit hook (time-machine guarantee).
        commit_marker: Optional[str] = None
        if self._commit_hook is not None:
            try:
                commit_marker = await self._commit_hook(msg, prompt)
            except Exception as exc:  # noqa: BLE001
                logger.warning(
                    "registry: commit hook for %s failed: %s", channel_name, exc
                )
        # 2) Run the agent.
        reply: Optional[str] = None
        if self._agent_runner is not None:
            try:
                reply = await self._agent_runner(msg)
            except Exception as exc:  # noqa: BLE001
                logger.exception("registry: agent runner crashed for %s", channel_name)
                reply = f"⚠️ CVC agent error: {exc}"
        # 3) Wrap in OutboundMessage + return to adapter for dispatch.
        if reply is None:
            return None
        return OutboundMessage(
            chat_id=msg.chat_id,
            thread_id=msg.thread_id,
            reply_to_message_id=msg.reply_to_message_id or self._first_message_id(msg),
            text=reply,
            metadata={"cvc_commit": commit_marker} if commit_marker else {},
        )

    @staticmethod
    def _first_message_id(msg: InboundMessage) -> Optional[str]:
        """Best-effort: most channels want replies anchored to the user's
        own message. We pull it from raw if the adapter populated it."""
        if msg.raw is None:
            return None
        # Telegram: raw.message_id. Discord: raw.id. Slack: raw["ts"].
        for attr in ("message_id", "id"):
            v = getattr(msg.raw, attr, None)
            if v is not None:
                return str(v)
        if isinstance(msg.raw, dict) and "ts" in msg.raw:
            return str(msg.raw["ts"])
        return None

    @staticmethod
    def _build_prompt(msg: InboundMessage) -> str:
        """Render the prompt the agent actually sees. Channel metadata
        is folded into a header so the agent knows where the message
        came from (it can use that for routing, persona, etc.)."""
        head_bits = [f"[channel: {msg.channel}]", f"[chat_id: {msg.chat_id}]"]
        if msg.thread_id:
            head_bits.append(f"[thread_id: {msg.thread_id}]")
        if msg.user_name:
            head_bits.append(f"[user: {msg.user_name}]")
        elif msg.user_id:
            head_bits.append(f"[user_id: {msg.user_id}]")
        header = " ".join(head_bits)
        body = msg.text or ""
        media_note = ""
        if msg.media:
            kinds = ", ".join(sorted({m.get("kind", "?") for m in msg.media}))
            media_note = f"\n[attachments: {len(msg.media)} ({kinds})]"
        return f"{header}\n{body}{media_note}".strip()

    # ── Status ──────────────────────────────────────────────────────

    def status(self) -> Dict[str, ChannelStatus]:
        return {name: adapter.status() for name, adapter in self._adapters.items()}

    def list_names(self) -> List[str]:
        return sorted(self._adapters.keys())

    def get(self, name: str) -> Optional[BaseChannelAdapter]:
        return self._adapters.get(name)

    # ── Dependency injection ─────────────────────────────────────────

    def set_agent_runner(self, runner: AgentRunner) -> None:
        self._agent_runner = runner

    def set_commit_hook(self, hook: CommitHook) -> None:
        self._commit_hook = hook
