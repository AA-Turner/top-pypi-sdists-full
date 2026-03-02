"""TelegramChannel — Channel implementation backed by the Telegram Bot API."""

from __future__ import annotations

import base64
import logging
import time
from typing import AsyncIterator

from ..base import Channel, ChannelEvent, ChannelMessage, DeliveryResult, ImageAttachment
from .bot import TelegramBot, TelegramAPIError, TelegramMessage
from .config import TelegramConfig, get_config
from .formatter import SSEEventFormatter

log = logging.getLogger(__name__)


class TelegramChannel(Channel):
    """Bidirectional channel that communicates via Telegram Bot API.

    Wraps :class:`TelegramBot` long-polling and the
    :class:`SSEEventFormatter` to satisfy the :class:`Channel` ABC.
    """

    name = "telegram"

    def __init__(self, config: TelegramConfig | None = None) -> None:
        self._config = config or get_config()
        self._bot: TelegramBot | None = None
        self._running = False
        self._formatter = SSEEventFormatter(
            show_thinking=self._config.settings.show_thinking,
            show_tools=self._config.settings.show_tool_calls,
            compact=self._config.settings.compact_mode,
            live_panel=self._config.settings.show_status_panel,
        )
        # Track sent message IDs per chat for edit support
        self._last_message_ids: dict[str, int] = {}
        # Rate-limit typing indicators (sender_id -> monotonic timestamp)
        self._last_typing: dict[str, float] = {}

    # -- Lifecycle -------------------------------------------------------

    async def start(self) -> None:
        if not self._config.bot_token:
            raise ValueError("Telegram bot token not configured")
        self._bot = TelegramBot(self._config.bot_token)
        # Validate token
        me = await self._bot.get_me()
        log.info("Telegram channel started as @%s", me.username or me.first_name)
        self._running = True

    async def stop(self) -> None:
        self._running = False
        if self._bot and self._bot._client:
            await self._bot._client.aclose()
            self._bot._client = None
        self._bot = None

    async def is_available(self) -> bool:
        return self._running and self._bot is not None

    # -- Inbound ---------------------------------------------------------

    async def poll_messages(self) -> AsyncIterator[ChannelMessage]:
        if self._bot is None:
            return

        offset = self._config.state.last_update_id
        async for update in self._bot.poll_updates(offset=offset):
            self._config.state.last_update_id = update.update_id
            msg = update.message
            if msg is None:
                continue

            # Must have text, caption, or media — skip empty updates
            content = msg.effective_text or ""
            if not content and not msg.has_media:
                continue

            # Download images if present
            images: list[ImageAttachment] = []
            if msg.photo and self._bot:
                try:
                    image_data = await self._download_photo(msg)
                    if image_data:
                        images.append(image_data)
                except Exception:
                    log.warning("Failed to download photo from message %s", msg.message_id)

            # Handle voice messages — download and transcribe
            if msg.voice and self._bot:
                try:
                    raw_audio = await self._bot.download_file_by_id(msg.voice.file_id)
                    from .voice import transcribe_voice
                    transcribed = await transcribe_voice(
                        raw_audio, mime_type=msg.voice.mime_type or "audio/ogg"
                    )
                    if transcribed:
                        voice_note = f"[Voice message ({msg.voice.duration}s) transcription]: {transcribed}"
                    else:
                        voice_note = f"[Voice message ({msg.voice.duration}s) — transcription unavailable]"
                except Exception:
                    log.warning("Failed to process voice from message %s", msg.message_id)
                    voice_note = f"[Voice message ({msg.voice.duration}s) — download failed]"
                content = f"{voice_note}\n{content}" if content else voice_note

            # Skip if still no content and no images
            if not content and not images:
                continue

            yield ChannelMessage(
                content=content,
                sender_id=str(msg.chat.id),
                message_id=str(msg.message_id),
                images=images,
                metadata={
                    "chat_type": msg.chat.type,
                    "chat_name": msg.chat.display_name,
                    "from_user": msg.from_user.display_name if msg.from_user else None,
                    "has_voice": bool(msg.voice),
                    "has_photo": bool(msg.photo),
                },
            )

    async def _download_photo(self, msg: TelegramMessage) -> ImageAttachment | None:
        """Download the largest photo variant and return as base64 ImageAttachment."""
        if not msg.photo or not self._bot:
            return None

        # Pick the largest photo (last in the array)
        best = max(msg.photo, key=lambda p: p.file_size or (p.width * p.height))
        raw = await self._bot.download_file_by_id(best.file_id)
        encoded = base64.b64encode(raw).decode("ascii")
        return ImageAttachment(data=encoded, format="jpg")

    async def check_authorization(self, sender_id: str) -> bool:
        try:
            chat_id = int(sender_id)
        except (ValueError, TypeError):
            return False
        return self._config.is_chat_authorized(chat_id)

    # -- Activity indicator ----------------------------------------------

    async def notify_activity(self, sender_id: str) -> None:
        if self._bot is None:
            return
        now = time.monotonic()
        if now - self._last_typing.get(sender_id, 0) < 4.0:
            return
        self._last_typing[sender_id] = now
        try:
            await self._bot.send_chat_action(int(sender_id), "typing")
        except TelegramAPIError:
            pass

    # -- Outbound --------------------------------------------------------

    async def send_event(
        self, sender_id: str, event: ChannelEvent
    ) -> DeliveryResult:
        if self._bot is None:
            return DeliveryResult(success=False, channel=self.name, error="Bot not started")

        try:
            chat_id = int(sender_id)
        except (ValueError, TypeError):
            return DeliveryResult(
                success=False,
                channel=self.name,
                error=f"Invalid chat_id: {sender_id!r} (expected numeric Telegram chat ID)",
            )
        text = event.content
        if not text:
            return DeliveryResult(success=True, channel=self.name)

        try:
            sent = await self._bot.send_message(chat_id, text, parse_mode="Markdown")
            self._last_message_ids[sender_id] = sent.message_id
            return DeliveryResult(
                success=True, channel=self.name, message_id=str(sent.message_id)
            )
        except TelegramAPIError:
            # Markdown failed — retry as plain text
            try:
                sent = await self._bot.send_message(chat_id, text, parse_mode=None)
                self._last_message_ids[sender_id] = sent.message_id
                return DeliveryResult(
                    success=True, channel=self.name, message_id=str(sent.message_id)
                )
            except TelegramAPIError as exc:
                return DeliveryResult(
                    success=False, channel=self.name, error=str(exc)
                )

    async def update_event(
        self, sender_id: str, message_id: str, event: ChannelEvent
    ) -> DeliveryResult:
        if self._bot is None:
            return DeliveryResult(success=False, channel=self.name, error="Bot not started")

        try:
            chat_id = int(sender_id)
        except (ValueError, TypeError):
            return DeliveryResult(
                success=False,
                channel=self.name,
                error=f"Invalid chat_id: {sender_id!r} (expected numeric Telegram chat ID)",
            )
        try:
            edited = await self._bot.edit_message_text(
                chat_id, int(message_id), event.content, parse_mode="Markdown"
            )
            return DeliveryResult(
                success=True, channel=self.name, message_id=str(edited.message_id)
            )
        except TelegramAPIError:
            # Fall back to sending a new message
            return await self.send_event(sender_id, event)

    # -- SSE formatting --------------------------------------------------

    def format_sse_event(
        self, event_type: str, data: dict
    ) -> ChannelEvent | None:
        formatted = self._formatter.format_event(event_type, data)
        if formatted is None:
            return None
        return ChannelEvent(
            type=event_type,
            content=formatted.text,
            is_update=formatted.is_update,
        )
