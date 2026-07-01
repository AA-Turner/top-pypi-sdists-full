"""
Base adapter interface for CVC's external messaging channels.

Every channel CVC supports (Telegram, Discord, Slack, WhatsApp,
Matrix, Signal, Email, Webhook, …) implements :class:`BaseChannelAdapter`.
The base class enforces a single contract: receive inbound messages
into the CVC agent loop, send agent output back, and emit status.

Design principles (CVC-specific, distinct from Hermes):

  1. **Self-contained.** The base class lives entirely under
     ``cvc/integrations/``. It does NOT import from
     ``cvc.agent._vendor.hermes.*``. CVC users on any machine get the
     full channel stack on install — no ``pip install hermes-agent``.

  2. **CVC-commit-bound.** Every inbound message flows through
     :meth:`BaseChannelAdapter.handle_inbound`, which (when wired to a
     :class:`ChannelRegistry`) is responsible for creating a cognitive
     commit BEFORE running the agent. This is CVC's "time machine"
     guarantee — the message is preserved as part of the Merkle DAG
     before the agent ever touches it, so even if the agent crashes
     or lies, the conversation is durable.

  3. **Async-first.** Adapters are coroutines. The registry schedules
     them as background asyncio tasks.

  4. **Capability-flagged.** Adapters declare which capabilities they
     support (text, media, inline keyboards, threads, edits). The
     registry refuses to send a capability the adapter doesn't have.

  5. **Pluggable.** Adding a new channel is a single subclass and a
     single ``register(telegram, TelegramAdapter())`` line in the
     bootstrapper. The dashboard, gateway API, and CLI pick it up
     automatically.
"""

from __future__ import annotations

import abc
import asyncio
import dataclasses
import enum
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, Dict, List, Optional


logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Capability flags
# ─────────────────────────────────────────────────────────────────────────────


class Capability(str, enum.Enum):
    """Features a channel can support.

    These are coarse-grained on purpose — the goal is for the registry
    to refuse impossible sends, not to fully model each platform's
    edge cases.
    """

    TEXT = "text"                       # Plain or formatted text
    MEDIA = "media"                     # Photo, audio, video, document, sticker
    INLINE_KEYBOARD = "inline_keyboard"  # Buttons under a message
    THREADS = "threads"                 # Reply in a topic / thread
    EDIT = "edit"                       # Edit a previously sent message
    REACTIONS = "reactions"             # React with emoji
    STREAMING = "streaming"             # Edit-as-you-stream the response
    VOICE = "voice"                     # Native voice-note delivery


# ─────────────────────────────────────────────────────────────────────────────
# Inbound + outbound message dataclasses
# ─────────────────────────────────────────────────────────────────────────────


@dataclass
class InboundMessage:
    """A message arriving from an external channel into CVC.

    Captures everything an adapter knows about the inbound message.
    Adapters fill these in and hand them to the registry, which then
    runs the agent and gets an :class:`OutboundMessage` back to send.
    """

    channel: str                       # "telegram" / "discord" / …
    chat_id: str                       # Platform-native chat/conversation id
    user_id: str                       # Platform-native user id (may be "" for groups)
    user_name: str                     # Human display name (best-effort)
    text: str                          # User-typed message ("" if media-only)
    thread_id: Optional[str] = None    # Platform-native thread/topic id
    reply_to_message_id: Optional[str] = None
    media: List[Dict[str, Any]] = field(default_factory=list)
    # ^ Each entry: {"kind": "photo"|"audio"|"voice"|"video"|"document"|"sticker",
    #                "url": str, "mime": str, "size": int, "caption": str}
    is_command: bool = False           # True if message starts with /
    command: Optional[str] = None      # The slash command without "/"
    command_args: Optional[str] = None # Everything after the command
    raw: Any = None                    # Platform-native object (rarely needed)
    timestamp: float = field(default_factory=time.time)


@dataclass
class OutboundMessage:
    """A message being sent FROM CVC to an external channel."""

    chat_id: str
    text: str = ""
    thread_id: Optional[str] = None
    reply_to_message_id: Optional[str] = None
    media: List[Dict[str, Any]] = field(default_factory=list)
    inline_keyboard: Optional[List[List[Dict[str, str]]]] = None
    # ^ Each button: {"text": "Approve", "callback_data": "approve:42"}
    parse_mode: Optional[str] = None    # "markdown" | "html" | None
    edit_message_id: Optional[str] = None  # If set, edit this message instead of sending
    silent: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ChannelStatus:
    """Live status of one channel adapter, surfaced via the gateway API."""

    name: str
    enabled: bool
    healthy: bool
    capabilities: List[Capability]
    started_at: Optional[float] = None
    last_activity_at: Optional[float] = None
    last_error: Optional[str] = None
    config_keys: List[str] = field(default_factory=list)
    info: Dict[str, Any] = field(default_factory=dict)


# ─────────────────────────────────────────────────────────────────────────────
# Adapter ABC
# ─────────────────────────────────────────────────────────────────────────────


class BaseChannelAdapter(abc.ABC):
    """Base class every CVC channel adapter inherits from.

    Lifecycle:
      1. ``__init__(config)`` — adapter reads its config dict.
      2. ``start()`` — adapter spins up its polling/webhook coroutine.
      3. For each inbound message, adapter builds an
         :class:`InboundMessage` and calls ``self.on_inbound(msg)``.
         The registry has registered ``on_inbound`` to enqueue a CVC
         commit + run the agent.
      4. After the agent produces output, the registry calls
         :meth:`send` with an :class:`OutboundMessage`.
      5. ``stop()`` — adapter shuts down its background tasks.

    Adapters MUST be idempotent across start/stop cycles. They MUST NOT
    import anything from ``cvc.agent._vendor.hermes.*``.
    """

    #: Channel id used everywhere (config keys, API paths, dashboard).
    name: str = "base"

    #: Human-readable label for the CLI setup wizard + dashboard.
    display_name: str = "Channel"

    #: One-paragraph description shown in the CLI/dashboard.
    description: str = ""

    #: Structured config schema consumed by :func:`setup_wizard.suggest_prompts`
    #: and the dashboard's per-channel "Configure" panel. Each entry is a
    #: dict with keys:
    #:
    #:   ``key``       (str, required) — config-key name
    #:   ``label``     (str, required) — prompt label shown to the user
    #:   ``help``      (str, optional) — one-line help text under the prompt
    #:   ``secret``    (bool, optional) — hide input while typing
    #:   ``default``   (any, optional) — default value if user presses Enter
    #:   ``required``  (bool, optional) — block save if empty (default True)
    #:   ``kind``      (str, optional) — "str"|"int"|"list[str]"|"bool"|"json"
    #:   ``choices``   (list, optional) — restrict to these values
    #:
    #: Subclasses override this attribute to declare what they need.
    #: The CLI / dashboard introspect it to render the right prompts.
    config_schema: List[Dict[str, Any]] = []

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config or {}
        self._on_inbound: Optional[Callable[[InboundMessage], Awaitable[Optional[OutboundMessage]]]] = None
        self._started_at: Optional[float] = None
        self._last_activity_at: Optional[float] = None
        self._last_error: Optional[str] = None
        self._healthy: bool = False
        self._tasks: List[asyncio.Task] = []

    # ── Abstract surface ───────────────────────────────────────────────

    @abc.abstractmethod
    def capabilities(self) -> List[Capability]:
        """Declare which features this adapter supports."""
        ...

    @abc.abstractmethod
    async def start(self) -> None:
        """Spin up polling/webhook. Must be idempotent."""
        ...

    @abc.abstractmethod
    async def stop(self) -> None:
        """Tear down. Must be idempotent."""
        ...

    @abc.abstractmethod
    async def send(self, message: OutboundMessage) -> Dict[str, Any]:
        """Send an outbound message. Returns platform-native metadata
        (e.g. Telegram ``message_id``) for downstream use (edits,
        reactions)."""
        ...

    # ── Concrete helpers ───────────────────────────────────────────────

    def set_inbound_handler(
        self,
        handler: Callable[[InboundMessage], Awaitable[Optional[OutboundMessage]]],
    ) -> None:
        """The registry calls this once at startup. The adapter calls
        it indirectly via :meth:`_emit_inbound` whenever a real message
        arrives."""
        self._on_inbound = handler

    async def _emit_inbound(self, msg: InboundMessage) -> Optional[OutboundMessage]:
        """Called by the adapter for each inbound message. Forwards to
        the registered handler if any, and records activity."""
        self._last_activity_at = time.time()
        if self._on_inbound is None:
            logger.warning("[%s] inbound message but no handler registered", self.name)
            return None
        try:
            return await self._on_inbound(msg)
        except Exception as exc:  # noqa: BLE001
            self._last_error = f"handler: {exc}"
            logger.exception("[%s] inbound handler crashed", self.name)
            return None

    def status(self) -> ChannelStatus:
        """Return the current status snapshot for the gateway API."""
        return ChannelStatus(
            name=self.name,
            enabled=self.config.get("enabled", False),
            healthy=self._healthy,
            capabilities=self.capabilities(),
            started_at=self._started_at,
            last_activity_at=self._last_activity_at,
            last_error=self._last_error,
            config_keys=sorted(self.config.keys()),
            info=self._info(),
        )

    def _info(self) -> Dict[str, Any]:
        """Optional: subclasses can override to expose diagnostic info."""
        return {}

    # ── Config helpers (subclasses use these) ──────────────────────────

    def cfg(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def cfg_bool(self, key: str, default: bool = False) -> bool:
        v = self.config.get(key, default)
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            return v.strip().lower() in {"1", "true", "yes", "on"}
        return bool(v)

    def cfg_list(self, key: str) -> List[str]:
        v = self.config.get(key, [])
        if isinstance(v, list):
            return [str(x) for x in v]
        if isinstance(v, str):
            return [x.strip() for x in v.split(",") if x.strip()]
        return []

    def cfg_dict(self, key: str) -> Dict[str, Any]:
        v = self.config.get(key, {})
        return dict(v) if isinstance(v, dict) else {}
