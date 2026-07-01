"""
Telegram adapter for CVC — Hermes-parity v1.

Powered by the official ``python-telegram-bot`` library (already a CVC
core dep). Feature checklist vs the Hermes vendored reference:

  [x] MarkdownV2 send with full escape
  [x] GFM table rewrite to row groups (Telegram doesn't render tables)
  [x] Long-message split at paragraph / line / space boundaries
  [x] Media: photo / audio / voice / video / document / sticker
  [x] Inline keyboard buttons + callback-query handling
  [x] Slash commands + BotCommand menu
  [x] Topics / threads (message_thread_id)
  [x] Allowlist of user IDs (DMs) and chat IDs (groups)
  [x] Reply-to-anchor (replies to the user's own message)
  [x] Optional streaming: edit one message as the agent thinks
  [x] Channel-paired log of all messages for the dashboard
  [ ] Photo-as-document fallback for files >10 MB (Hermes does this)
  [ ] Sticker-cache (Hermes has; CVC defers to v1.1)
  [ ] DM-topic helper (Hermes has a /topic command; v1.1)

Compared to Hermes: we are shorter (≈600 LOC vs 6,056), but the
contract is the same — Hermes users moving to CVC should see the same
behaviour they had, minus the sticker cache and DM-topic helper which
are nice-to-haves, not core UX.

Architecture note: this file does NOT import from
``cvc.agent._vendor.hermes.*``. It depends only on CVC's own
``cvc.integrations.*`` plus the ``telegram`` and ``httpx`` libraries.
"""

from __future__ import annotations

import asyncio
import io
import logging
import mimetypes
import os
import re
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx

from .base import (
    BaseChannelAdapter,
    Capability,
    InboundMessage,
    OutboundMessage,
)


logger = logging.getLogger(__name__)


# Lazy import — python-telegram-bot is a heavy dep with side effects on
# import (logging, asyncio policy on older versions). Keeping the import
# lazy means a CVC user who never enables Telegram never pays the cost.
_telegram_import_error: Optional[Exception] = None
try:
    from telegram import (
        Update,
        Bot,
        Message,
        InlineKeyboardButton,
        InlineKeyboardMarkup,
        InputFile,
        ReplyParameters,
        BotCommand,
    )
    from telegram.constants import ParseMode, ChatAction
    from telegram.ext import (
        Application,
        ApplicationBuilder,
        CallbackQueryHandler,
        CommandHandler,
        ContextTypes,
        MessageHandler as PTBMessageHandler,
        filters,
    )
    _TELEGRAM_AVAILABLE = True
except Exception as _exc:  # noqa: BLE001
    _TELEGRAM_AVAILABLE = False
    _telegram_import_error = _exc
    # Provide minimal stand-ins so module import never fails.
    Update = Any  # type: ignore
    Bot = Any  # type: ignore
    Message = Any  # type: ignore
    InlineKeyboardButton = Any  # type: ignore
    InlineKeyboardMarkup = Any  # type: ignore
    InputFile = Any  # type: ignore
    ReplyParameters = Any  # type: ignore
    BotCommand = Any  # type: ignore
    ParseMode = Any  # type: ignore
    ChatAction = Any  # type: ignore
    Application = Any  # type: ignore
    ApplicationBuilder = Any  # type: ignore
    CallbackQueryHandler = Any  # type: ignore
    CommandHandler = Any  # type: ignore
    ContextTypes = Any  # type: ignore
    PTBMessageHandler = Any  # type: ignore
    filters = None  # type: ignore


from ..formatting.markdown import (  # noqa: E402  (after the lazy import guard)
    escape_mdv2,
    wrap_markdown_tables,
    split_message,
    markdown_to_mdv2,
    markdown_to_plain,
)


# C6: spine channel capture — fired at the channel boundary (inbound + outbound + errors).
try:
    from cvc.events.channel_capture import (
        capture_message_in,
        capture_message_out,
        capture_message_error,
        capture_message_skipped,
    )
    _CHANNEL_CAPTURE_OK = True
except Exception:  # noqa: BLE001 — never break the bot for telemetry
    _CHANNEL_CAPTURE_OK = False
    def capture_message_in(*_a, **_kw): return None  # type: ignore
    def capture_message_out(*_a, **_kw): return None  # type: ignore
    def capture_message_error(*_a, **_kw): return None  # type: ignore
    def capture_message_skipped(*_a, **_kw): return None  # type: ignore


# Module-level import so ``_stream_via_drafts`` / ``_stream_via_edits``
# (called from ``_handle_streaming``) can see the symbol without relying
# on function-local scoping. The earlier "import inside _handle_streaming"
# pattern caused ``NameError: name 'run_chat_turn_streaming' is not
# defined`` to leak into the warning log every time streaming fired and
# silently fell back to the non-streaming reply path.
try:
    from cvc.gateway.chat import run_chat_turn_streaming  # noqa: E402
    _RUN_CHAT_TURN_STREAMING_AVAILABLE = True
except Exception as _rcts_exc:  # noqa: BLE001
    run_chat_turn_streaming = None  # type: ignore
    _RUN_CHAT_TURN_STREAMING_AVAILABLE = False
    logger.warning(
        "telegram: run_chat_turn_streaming import failed at module load: %s. "
        "Streaming will fall back to the non-streaming reply path.",
        _rcts_exc,
    )


_TG_MAX_TEXT = 4000  # leave headroom under Telegram's 4096 cap


# ─────────────────────────────────────────────────────────────────────────────
# Helpers — formatting + media download
# ─────────────────────────────────────────────────────────────────────────────


def _to_mdv2(text: str) -> List[str]:
    """Apply table rewrite → MarkdownV2 conversion → split pipeline,
    returning the list of ready-to-send chunks.

    The conversion is markdown-aware: ``**bold**`` / ``*italic*`` /
    ``__underline__`` / ``~~strike~~`` / ``[text](url)`` / ``# heading``
    become proper MarkdownV2 markup, and ```inline code``` / ```fenced
    blocks``` / ```pre``` are preserved verbatim. Characters that are
    NOT part of any markup construct get escaped with a single
    backslash, as MarkdownV2 requires.
    """
    rewritten = wrap_markdown_tables(text)
    converted = markdown_to_mdv2(rewritten)
    return split_message(converted, _TG_MAX_TEXT)


def _is_authorized(allowlist: List[str], user_id: int, chat_id: int) -> bool:
    """True if *user_id* or *chat_id* appears in the allowlist.

    Allowlist entries are bare integers (user or chat) or ``-100…``
    chat IDs for groups. Empty allowlist = reject all (safe default).
    """
    if not allowlist:
        return False
    targets = {str(user_id), str(chat_id), str(chat_id).removeprefix("-")}
    return bool(targets & set(allowlist))


async def _download_telegram_file(bot: "Bot", file_id: str) -> Optional[bytes]:
    """Download a Telegram file by id and return raw bytes."""
    try:
        tg_file = await bot.get_file(file_id)
        if tg_file.file_path is None:
            return None
        # python-telegram-bot exposes async download_as_bytearray on v20+.
        bio = io.BytesIO()
        await tg_file.download_to_memory(out=bio)
        return bio.getvalue()
    except Exception as exc:  # noqa: BLE001
        logger.warning("telegram: file download failed for %s: %s", file_id, exc)
        return None


# ─────────────────────────────────────────────────────────────────────────────
# Adapter
# ─────────────────────────────────────────────────────────────────────────────


class TelegramAdapter(BaseChannelAdapter):
    """CVC ↔ Telegram adapter. See module docstring for the feature list."""

    name = "telegram"
    display_name = "Telegram Bot"
    description = (
        "Bidirectional Telegram bot via the Bot API. Talk to CVC from your phone "
        "or a group chat. Matches Hermes Telegram parity (MarkdownV2, GFM tables, "
        "media, inline keyboards, topics, streaming edits, slash commands)."
    )
    config_schema = [
        {
            "key": "bot_token",
            "label": "Bot token",
            "help": (
                "Get one from @BotFather on Telegram:\n"
                "  1. Open @BotFather → /newbot\n"
                "  2. Copy the HTTP API token (looks like 123456789:AA...)\n"
                "  3. Paste it here. The wizard will verify it's live with getMe()."
            ),
            "secret": True,
            "required": True,
            "kind": "str",
        },
        {
            "key": "allowlist",
            "label": "Allowed user IDs / chat IDs (comma-separated)",
            "help": (
                "Your NUMERIC Telegram user_id — NOT your @username.\n"
                "Quickest way to find it:\n"
                "  • Open @userinfobot on Telegram, send /start, copy the Id\n"
                "  • Or send /start to @RawDataBot and look for \"id\"\n"
                "For group chats, prepend the chat ID with -100.\n"
                "Tip: run `cvc doctor telegram --fix` anytime to set this later."
            ),
            "required": True,
            "kind": "list[str]",
        },
        {
            "key": "parse_mode",
            "label": "Markdown parse mode",
            "help": "Telegram MarkdownV2 is the safe default.",
            "default": "markdownv2",
            "kind": "str",
            "choices": ["markdownv2", "html", "markdown"],
        },
        {
            "key": "stream_edits",
            "label": "Stream edits",
            "help": "Edit one message in-place as the agent thinks (recommended).",
            "default": True,
            "kind": "bool",
        },
        {
            "key": "webhook_url",
            "label": "Webhook URL (optional)",
            "help": "If set, the bot uses webhooks instead of long polling.",
            "required": False,
            "kind": "str",
        },
    ]


    # ── Capabilities ────────────────────────────────────────────────

    def capabilities(self) -> List[Capability]:
        return [
            Capability.TEXT,
            Capability.MEDIA,
            Capability.INLINE_KEYBOARD,
            Capability.THREADS,
            Capability.EDIT,
            Capability.REACTIONS,
            Capability.STREAMING,
            Capability.VOICE,
        ]

    # ── Lifecycle ──────────────────────────────────────────────────

    async def start(self) -> None:
        if not _TELEGRAM_AVAILABLE:
            raise RuntimeError(
                "python-telegram-bot is not installed. "
                "Run `pip install 'python-telegram-bot[webhooks]>=22.0'`."
            ) from _telegram_import_error

        token = self.cfg("bot_token", "")
        if not token:
            raise RuntimeError("telegram: bot_token is required in config")

        self._allowlist = self.cfg_list("allowlist")
        self._default_parse_mode = self.cfg("parse_mode", "markdownv2")
        self._stream_edits = self.cfg_bool("stream_edits", True)
        self._streaming_edit_interval_ms = int(self.cfg("streaming_edit_interval_ms", 350))

        builder = ApplicationBuilder().token(token)
        builder = builder.read_timeout(30).write_timeout(30).connect_timeout(15)
        # Disable the noisy per-message INFO log from PTB.
        builder = builder.http_version("1.1")
        app = builder.build()
        self._app: Application = app  # type: ignore[assignment]
        self._bot: Bot = app.bot  # type: ignore[assignment]

        # Slash commands visible in the Telegram command menu.
        await self._register_bot_commands()

        # Register handlers. Order matters: callback queries first so
        # button presses never lose to a stale message handler.
        app.add_handler(CallbackQueryHandler(self._on_callback_query))
        app.add_handler(CommandHandler("help", self._on_help))
        app.add_handler(CommandHandler("status", self._on_status))
        app.add_handler(CommandHandler("cancel", self._on_cancel))
        app.add_handler(CommandHandler("commit", self._on_commit))
        app.add_handler(CommandHandler("branches", self._on_branches))
        app.add_handler(CommandHandler("checkout", self._on_checkout))
        app.add_handler(CommandHandler("search", self._on_search))
        app.add_handler(CommandHandler("clear", self._on_clear))
        app.add_handler(PTBMessageHandler(filters.TEXT & ~filters.COMMAND, self._on_text))
        app.add_handler(PTBMessageHandler(filters.PHOTO, self._on_photo))
        app.add_handler(PTBMessageHandler(filters.AUDIO, self._on_audio))
        app.add_handler(PTBMessageHandler(filters.VOICE, self._on_voice))
        app.add_handler(PTBMessageHandler(filters.VIDEO, self._on_video))
        app.add_handler(PTBMessageHandler(filters.Document.ALL, self._on_document))
        app.add_handler(PTBMessageHandler(filters.Sticker.ALL, self._on_sticker))

        # Initialize + start the bot. We poll by default; webhook mode is
        # opt-in via config (set `webhook_url` to enable).
        #
        # CVC_PASSTHROUGH_BOT env var: when set to "1" or "true", skip
        # starting the local bot polling entirely — useful when the
        # SAME Telegram token is also being polled by another CVC
        # instance (e.g. Mac gateway + Windows gateway). Set this on
        # whichever side should NOT answer messages so the other side
        # owns the polling slot cleanly.
        import os as _os
        if _os.environ.get("CVC_PASSTHROUGH_BOT", "").lower() in ("1", "true", "yes"):
            logger.info(
                "telegram: CVC_PASSTHROUGH_BOT=1 — skipping local polling. "
                "Another bot instance owns this token. The local gateway "
                "stays up so the dashboard, SSE, voice transcription, "
                "and other channels keep working."
            )
            self._healthy = True  # adapter is "up" but passive
            self._passthrough = True
            # Still register handlers so the bot object exists for any
            # direct API calls (send_message, etc.). We just don't poll.
            await app.initialize()
            return

        await app.initialize()
        webhook_url = self.cfg("webhook_url", "").strip()
        if webhook_url:
            await app.bot.set_webhook(url=webhook_url)
            self._healthy = True
            logger.info("telegram: webhook set to %s", webhook_url)
        else:
            # ── Phase 1A: gateway-side getMe() backstop ────────────────
            #
            # Before we start polling (or any other long-running ops),
            # prove the bot_token actually works with a live Bot API
            # ``get_me()`` call. This catches the silent-failure class
            # of bugs that the in-wizard validator can't catch:
            #
            #   * The user edited ~/.cvc/channels/telegram.yaml by hand
            #     and pasted a typo / revoked token.
            #   * The token was rotated via @BotFather/revoke and the
            #     channels yaml went stale.
            #   * The user restored a backup of the channels yaml from
            #     an old machine where the token is no longer valid.
            #
            # Without this check, PTB's polling would either (a) spin
            # forever returning 401s from Telegram or (b) crash on the
            # first message and spam the gateway errlog. With it, we
            # mark the adapter ``healthy=False`` with a precise reason
            # and the dashboard + ``cvc doctor telegram`` both show
            # the exact problem. This is the bottom layer of the
            # "three layers of validation" architecture:
            #   layer 1: wizard's live getMe() (catches typos at save)
            #   layer 2: gateway startup getMe() (this — catches drift)
            #   layer 3: cvc doctor telegram (catches all of the above
            #            plus 5 other common issues)
            try:
                me = await app.bot.get_me()
                username = getattr(me, "username", None) or "?"
                self._bot_username = username
                self._bot_id = getattr(me, "id", None)
                logger.info(
                    "telegram: getMe() ok — bot is @%s (id %s)",
                    username,
                    self._bot_id,
                )
            except Exception as getme_exc:  # noqa: BLE001
                # Capture the exact Telegram error message — it's
                # already user-friendly (e.g. "Unauthorized: bot was
                # blocked by the user", "Invalid token", "Bot was
                # deleted"). Mark unhealthy so the dashboard shows it.
                err = str(getme_exc).strip() or getme_exc.__class__.__name__
                self._healthy = False
                self._last_error = (
                    f"getMe() failed: {err}. "
                    "Run `cvc channel-setup telegram --reset` and paste a fresh token. "
                    "Get a new one from @BotFather on Telegram (/revoke → /token)."
                )
                logger.error(
                    "telegram: %s. Adapter marked unhealthy. Fix with "
                    "`cvc channel-setup telegram --reset`.",
                    self._last_error,
                )
                # Still shut down the partial app we initialized so
                # resources don't leak. We return early — never try
                # to poll with a dead token.
                try:
                    await app.shutdown()
                except Exception:
                    pass
                return

            try:
                await app.start()
                await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)  # type: ignore[union-attr]
                self._healthy = True
                logger.info("telegram: polling started")
            except Exception as start_exc:  # noqa: BLE001
                # TelegramConflictError on start: another bot is already
                # polling. Log loudly and disable this adapter so it
                # doesn't spam conflicts forever.
                err_str = str(start_exc).lower()
                if "conflict" in err_str or "terminated by other getupdates" in err_str:
                    logger.warning(
                        "telegram: ANOTHER BOT is already polling this token. "
                        "CVC's local adapter is disabling itself — "
                        "the other instance will handle messages. "
                        "To fix: stop one of the two daemons "
                        "(`cvc gateway stop` on the other machine), then "
                        "restart this one so it can claim the polling slot. "
                        "Underlying error: %s",
                        start_exc,
                    )
                    self._healthy = False
                    self._conflict = True
                    return
                raise
        self._started_at = time.time()

    async def stop(self) -> None:
        app: Optional[Application] = getattr(self, "_app", None)  # type: ignore[assignment]
        if app is None:
            return
        try:
            await app.updater.stop()  # type: ignore[union-attr]
        except Exception:
            pass
        try:
            await app.stop()
        except Exception:
            pass
        try:
            await app.shutdown()
        except Exception:
            pass
        self._healthy = False
        logger.info("telegram: stopped")

    # ── Outbound send ──────────────────────────────────────────────

    async def send(self, message: OutboundMessage) -> Dict[str, Any]:
        bot: Bot = self._bot
        chat_id = int(message.chat_id)
        thread_id = int(message.thread_id) if message.thread_id else None
        reply_to = int(message.reply_to_message_id) if message.reply_to_message_id else None

        results: List[Dict[str, Any]] = []

        # --- text / streaming edit ------------------------------------
        text = message.text or ""
        if text:
            if (
                message.edit_message_id
                and message.metadata.get("__streaming")
                and self._stream_edits
            ):
                # Streaming edit path — the registry sets edit_message_id
                # + __streaming on intermediate updates.
                try:
                    edited = await bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=int(message.edit_message_id),
                        text=text[: _TG_MAX_TEXT],
                        parse_mode=ParseMode.MARKDOWN_V2,
                    )
                    results.append({"message_id": str(edited.message_id)})
                    return results[-1]
                except Exception as exc:  # noqa: BLE001
                    logger.debug("telegram: streaming edit failed, falling back to send: %s", exc)
                    # Fall through to fresh send.

            chunks = _to_mdv2(text)
            for i, chunk in enumerate(chunks):
                kwargs: Dict[str, Any] = {
                    "chat_id": chat_id,
                    "text": chunk,
                    "parse_mode": ParseMode.MARKDOWN_V2,
                    "disable_web_page_preview": True,
                }
                if thread_id is not None:
                    kwargs["message_thread_id"] = thread_id
                if reply_to is not None and i == 0:
                    kwargs["reply_parameters"] = ReplyParameters(
                        message_id=reply_to,
                        allow_sending_without_reply=True,
                    )
                if message.inline_keyboard and i == len(chunks) - 1:
                    keyboard = self._build_inline_keyboard(message.inline_keyboard)
                    if keyboard:
                        kwargs["reply_markup"] = keyboard
                sent = await bot.send_message(**kwargs)
                results.append({"message_id": str(sent.message_id)})

        # --- media attachments ---------------------------------------
        for idx, m in enumerate(message.media or []):
            url = m.get("url", "")
            kind = m.get("kind", "document")
            caption = m.get("caption", "")
            if not url:
                continue
            media_result = await self._send_media(
                bot=bot,
                chat_id=chat_id,
                thread_id=thread_id,
                url=url,
                kind=kind,
                caption=caption,
                send_kwarg_only=(idx == 0 and not text),
            )
            if media_result:
                results.append(media_result)

        # C6: capture the outbound event after successful sends.
        # We capture ONCE per send() call, regardless of how many chunks
        # / media pieces were sent — one "CVC replied" event per reply.
        try:
            session_id = f"cvc_ch_{self.name}_{chat_id}_{thread_id or ''}".rstrip("_")
            capture_message_out(
                channel=self.name,
                actor="bot",
                session_id=session_id,
                summary=(text[:140] if text else f"[media] {len(message.media or [])} item(s)"),
                data={
                    "chat_id": str(chat_id),
                    "thread_id": str(thread_id) if thread_id else None,
                    "reply_to": str(reply_to) if reply_to else None,
                    "message_ids": [r.get("message_id") for r in results if r.get("message_id")],
                    "text_length": len(text or ""),
                    "media_count": len(message.media or []),
                    "streaming": bool(message.metadata.get("__streaming")),
                    "edit_message_id": str(message.edit_message_id) if message.edit_message_id else None,
                },
            )
        except Exception:
            pass

        return results[-1] if results else {}

    async def _send_media(
        self,
        bot: Bot,
        chat_id: int,
        thread_id: Optional[int],
        url: str,
        kind: str,
        caption: str,
        send_kwarg_only: bool,
    ) -> Optional[Dict[str, Any]]:
        """Download *url* and forward to Telegram via the right method."""
        try:
            async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:
                resp = await client.get(url)
                resp.raise_for_status()
                data = resp.content
                content_type = resp.headers.get("content-type", "application/octet-stream")
        except Exception as exc:  # noqa: BLE001
            logger.warning("telegram: failed to fetch media %s: %s", url, exc)
            return None

        ext = mimetypes.guess_extension(content_type.split(";")[0].strip()) or ""
        if kind in {"photo", "image"} or content_type.startswith("image/"):
            method = "send_photo"
            filename = f"image{ext or '.jpg'}"
            attach = data
        elif kind == "voice" or content_type.startswith("audio/ogg"):
            method = "send_voice"
            filename = f"voice{ext or '.ogg'}"
            attach = data
        elif kind == "audio" or content_type.startswith("audio/"):
            method = "send_audio"
            filename = f"audio{ext or '.mp3'}"
            attach = data
        elif kind == "video" or content_type.startswith("video/"):
            method = "send_video"
            filename = f"video{ext or '.mp4'}"
            attach = data
        else:
            method = "send_document"
            filename = mangle_filename(url, content_type, ext)
            attach = data

        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(filename).suffix) as tmp:
            tmp.write(attach)
            tmp_path = tmp.name
        try:
            with open(tmp_path, "rb") as fh:
                send_fn = getattr(bot, method)
                kwargs: Dict[str, Any] = {
                    "chat_id": chat_id,
                    "caption": escape_mdv2(caption)[: 1024] if caption else None,
                    "parse_mode": ParseMode.MARKDOWN_V2 if caption else None,
                }
                if thread_id is not None:
                    kwargs["message_thread_id"] = thread_id
                if method == "send_photo":
                    kwargs["photo"] = InputFile(fh, filename=filename)
                elif method == "send_voice":
                    kwargs["voice"] = InputFile(fh, filename=filename)
                elif method == "send_audio":
                    kwargs["audio"] = InputFile(fh, filename=filename)
                    kwargs["title"] = filename
                elif method == "send_video":
                    kwargs["video"] = InputFile(fh, filename=filename)
                else:
                    kwargs["document"] = InputFile(fh, filename=filename)
                sent = await send_fn(**{k: v for k, v in kwargs.items() if v is not None})
                return {"message_id": str(sent.message_id)}
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

    def _build_inline_keyboard(
        self, kb: List[List[Dict[str, str]]]
    ) -> Optional[InlineKeyboardMarkup]:
        rows: List[List[InlineKeyboardButton]] = []
        for row in kb:
            buttons: List[InlineKeyboardButton] = []
            for b in row:
                text = b.get("text", "")
                if "callback_data" in b:
                    buttons.append(
                        InlineKeyboardButton(text=text, callback_data=b["callback_data"])
                    )
                elif "url" in b:
                    buttons.append(InlineKeyboardButton(text=text, url=b["url"]))
            if buttons:
                rows.append(buttons)
        if not rows:
            return None
        return InlineKeyboardMarkup(rows)

    # ── Bot command menu ───────────────────────────────────────────

    async def _register_bot_commands(self) -> None:
        """Register ALL available CVC slash commands + skills with BotFather.

        Discovers:
        1. Core agent commands from ``SLASH_COMMANDS`` (renderer.py) — the
           same list the CLI REPL uses for tab completion.
        2. Available skills (from skill discovery) — each becomes a command
           the user can invoke with ``/skill_name``.

        Telegram limits to 100 commands; each name ≤32 chars, lowercase
        letters + digits + underscores only.
        """
        commands: list = []  # list[BotCommand]
        seen: set[str] = set()

        def _add(name: str, desc: str) -> None:
            # Telegram command rules: 1-32 chars, [a-z0-9_], must start
            # with a letter.
            clean = name.lstrip("/").lower().replace("-", "_")[:32]
            if not clean or not clean[0].isalpha():
                return
            if clean in seen:
                return
            seen.add(clean)
            commands.append(BotCommand(clean, desc[:256] if desc else clean))

        # 1. Core commands — always present.
        _add("help", "Show what CVC can do here")
        _add("status", "Agent + workspace status")
        _add("cancel", "Cancel the current turn")

        # 2. All CVC slash commands from the agent's command registry.
        try:
            from cvc.agent.renderer import SLASH_COMMANDS
            for cmd in SLASH_COMMANDS:
                _add(cmd, f"CVC command: {cmd.lstrip('/')}")
        except Exception:
            pass

        # 3. Skills — each becomes a command.
        try:
            from cvc.agent.skills import discover_skills
            from pathlib import Path
            skills = discover_skills(Path.home())
            for skill in skills:
                _add(skill.name, skill.description or f"Skill: {skill.name}")
        except Exception:
            pass

        # Telegram hard limit: 100 commands.
        commands = commands[:100]

        try:
            await self._bot.set_my_commands(commands)
            logger.info("telegram: registered %d bot commands (%d skills discovered)",
                        len(commands), len(seen))
        except Exception as exc:  # noqa: BLE001
            logger.debug("telegram: set_my_commands failed: %s", exc)

    # ── Inbound handlers ───────────────────────────────────────────

    async def _on_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self._handle_message(update, text_override=update.message.text or "")

    async def _on_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self._handle_media(update, kind="photo")

    async def _on_audio(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self._handle_media(update, kind="audio")

    async def _on_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Voice messages — download, transcribe, then run as a normal
        text message.

        Flow (mirrors Hermes's QQ Bot + Discord voice pipeline):
        1. Show typing indicator
        2. Download the .ogg from Telegram
        3. POST to ``/api/voice/transcribe`` on the gateway
           (tries local Whisper → Groq → OpenAI → Gemini in order)
        4. Inject the transcript as ``inbound.text``
        5. Run the normal agent pipeline (with the streaming UX)

        If transcription fails, we tell the user instead of silently
        dropping the voice note — Hermes does the same.
        """
        msg = update.message
        if msg is None or msg.voice is None or msg.from_user is None:
            return
        user = msg.from_user
        chat = msg.chat

        if not _is_authorized(self._allowlist, user.id, chat.id):
            logger.info("telegram: rejecting voice from user_id=%s chat_id=%s",
                        user.id, chat.id)
            return

        # ── Silent transcription (no "processing voice" sticker) ───────
        # Customer should NOT see internal processing state. The only
        # thing the customer ever sees is the final agent response —
        # streamed live, word-by-word, in the same way the dashboard
        # streams it. If transcription fails, we surface ONE clean error
        # message and stop.
        #
        # We still send the typing indicator (Telegram-native, lives in
        # the chat header, never appears as a message) so the user
        # understands their voice was received while we work.
        try:
            await self._bot.send_chat_action(chat_id=chat.id, action=ChatAction.TYPING)
        except Exception:
            pass

        voice_msg = msg.voice
        duration = voice_msg.duration or 0

        # Download the .ogg audio bytes.
        try:
            tg_file = await self._bot.get_file(voice_msg.file_id)
            if tg_file.file_path is None:
                raise RuntimeError("Telegram returned no file_path")
            bio = io.BytesIO()
            await tg_file.download_to_memory(out=bio)
            audio_bytes = bio.getvalue()
        except Exception as exc:
            logger.warning("telegram: voice download failed: %s", exc)
            await self._bot.send_message(
                chat_id=chat.id,
                text="⚠️ _Failed to download voice note\\._",
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_to_message_id=msg.message_id,
            )
            return

        if not audio_bytes:
            await self._bot.send_message(
                chat_id=chat.id,
                text="⚠️ _Voice note is empty\\._",
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_to_message_id=msg.message_id,
            )
            return

        # Transcribe via the gateway's STT endpoint.
        transcript, provider = await self._transcribe_audio(
            audio_bytes=audio_bytes,
            filename="voice.ogg",
            content_type="audio/ogg",
        )

        if not transcript or not transcript.strip():
            await self._bot.send_message(
                chat_id=chat.id,
                text=(
                    "⚠️ _Could not transcribe the voice note\\. "
                    "No speech\\-to\\-text provider is configured\\._\n\n"
                    "_Fix: run `cvc voice install` to add free local Whisper, "
                    "or set `GROQ_API_KEY` / `OPENAI_API_KEY` / `GOOGLE_API_KEY`\\._"
                ),
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_to_message_id=msg.message_id,
            )
            return

        # No transcript preview sticker — customer should not see
        # internal state. Just inject the transcript into the inbound
        # and let streaming take over. The agent's response IS the
        # first message the customer sees.
        text = transcript
        thread_id = str(msg.message_thread_id) if msg.message_thread_id else None
        inbound = InboundMessage(
            channel=self.name,
            chat_id=str(chat.id),
            user_id=str(user.id),
            user_name=user.full_name or user.username or "",
            text=text,
            thread_id=thread_id,
            reply_to_message_id=str(msg.message_id),
            media=[{
                "kind": "voice",
                "transcript": transcript,
                "provider": provider,
                "duration": duration,
                "mime": "audio/ogg",
                "size": len(audio_bytes),
            }],
            is_command=text.lstrip().startswith("/"),
            command=(text.split(maxsplit=1)[0].lstrip("/").lower() or None) if text.lstrip().startswith("/") else None,
            command_args=(text.split(maxsplit=1)[1] if text.lstrip().startswith("/") and " " in text else None),
            raw=msg,
        )

        # Run through the same handler path as a typed message —
        # slash commands, streaming, all apply. No cloud placeholder,
        # no transcript preview — the customer's first sight of our
        # reply is the live-streamed agent response.
        await self._handle_message(update, text_override=text)

    async def _transcribe_audio(
        self,
        audio_bytes: bytes,
        filename: str = "voice.ogg",
        content_type: str = "audio/ogg",
    ) -> tuple[Optional[str], Optional[str]]:
        """POST audio bytes to the gateway's /api/voice/transcribe endpoint.

        The legacy endpoint (``cvc.gateway_legacy:voice_transcribe``) uses
        ``UploadFile`` named ``audio`` — so we send the multipart field as
        ``audio``, not ``file``.

        Returns ``(transcript, provider)`` — both ``None`` if all providers
        fail or none are configured.
        """
        try:
            async with httpx.AsyncClient(timeout=90.0) as client:
                # NOTE: field name is ``audio`` — that's what the legacy
                # FastAPI route binds via ``UploadFile = File(...)``.
                files = {"audio": (filename, audio_bytes, content_type)}
                r = await client.post(
                    "http://localhost:13421/api/voice/transcribe",
                    files=files,
                )
                if r.status_code >= 400:
                    logger.warning(
                        "telegram: /api/voice/transcribe returned %s: %s",
                        r.status_code, r.text[:200],
                    )
                    return None, None
                data = r.json()
                text = (data.get("text") or "").strip()
                provider = data.get("provider") or "unknown"
                if text:
                    logger.info(
                        "telegram: voice transcribed (%d chars, %s): %r…",
                        len(text), provider, text[:60],
                    )
                return (text or None), provider
        except Exception as exc:
            logger.warning("telegram: STT endpoint call failed: %s", exc)
            return None, None

    async def _on_video(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self._handle_media(update, kind="video")

    async def _on_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self._handle_media(update, kind="document")

    async def _on_sticker(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # Stickers are decoded into a single media entry of kind "sticker".
        msg = update.message
        if msg is None or msg.sticker is None:
            return
        await self._handle_message(update, media_override=[{
            "kind": "sticker",
            "file_id": msg.sticker.file_id,
            "emoji": msg.sticker.emoji or "",
        }])

    async def _on_callback_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Callback queries: pressed inline buttons come back here.

        Two kinds of callbacks:
        - ``pick:*``  → our picker flow (model, branch, persona). Handled
          by ``_handle_picker_callback`` which edits the message.
        - anything else → forwarded as a synthetic inbound to the agent
          so the cognitive-commit trail stays unbroken.
        """
        cq = update.callback_query
        if cq is None:
            return
        data = cq.data or ""

        # Picker flow — handled inline (don't fall through to streaming).
        if data.startswith("pick:"):
            await self._handle_picker_callback(cq)
            return

        # Generic callback → forward to agent.
        await cq.answer()  # dismiss the spinner
        synthetic = Update(
            update_id=update.update_id,
            message=cq.message,
        )
        await self._handle_message(
            synthetic,
            text_override=f"[button: {data}]",
        )

    # ── Slash commands ─────────────────────────────────────────────

    async def _on_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self._reply(update, (
            "*🤖 CVC — Time Machine for AI Agents*\n\n"
            "Send any message and CVC will respond with full cognitive context.\n"
            "All messages are committed to your CVC Merkle DAG — CVC never forgets.\n\n"
            "*Slash commands:*\n"
            "• `/status` — agent + workspace status\n"
            "• `/cancel` — cancel the running turn\n"
            "• `/commit [msg]` — commit current workspace\n"
            "• `/branches` — list cognitive branches\n"
            "• `/checkout <name>` — switch branch\n"
            "• `/search <query>` — search workspace\n"
            "• `/clear` — clear chat-scoped transient context\n"
        ))

    async def _on_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # The agent_runner handles rich status; here we just show channel health.
        await self._reply(update, (
            f"*CVC channel status*\n"
            f"• Telegram: healthy={self._healthy}\n"
            f"• Started: {self._started_at and time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self._started_at))}\n"
            f"• Last activity: {self._last_activity_at and time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self._last_activity_at))}"
        ))

    async def _on_cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self._reply(update, "_Cancellation requested. The current turn will stop on the next WS frame._")

    async def _on_commit(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # Surface as a normal message — the commit hook + agent runner handle the rest.
        msg = update.message.text or "/commit"
        await self._handle_message(update, text_override=msg)

    async def _on_branches(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self._handle_message(update, text_override="/branches")

    async def _on_checkout(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self._handle_message(update, text_override=update.message.text or "/checkout")

    async def _on_search(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self._handle_message(update, text_override=update.message.text or "/search")

    async def _on_clear(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self._reply(update, "_Chat transient context cleared. CVC cognitive history is preserved._")

    # ── Inbound pipeline ───────────────────────────────────────────

    async def _handle_message(
        self,
        update: Update,
        text_override: Optional[str] = None,
        media_override: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        msg = update.message or update.edited_message
        if msg is None or msg.from_user is None:
            return
        user = msg.from_user
        chat = msg.chat

        if not _is_authorized(self._allowlist, user.id, chat.id):
            # C6: capture the rejection — it's still observable activity.
            try:
                capture_message_skipped(
                    channel=self.name,
                    actor=str(user.id),
                    summary=f"telegram: user {user.id} not in allowlist (chat {chat.id})",
                    data={
                        "chat_id": str(chat.id),
                        "reason": "not_in_allowlist",
                        "is_edit": bool(update.edited_message),
                    },
                )
            except Exception:
                pass
            logger.info("telegram: rejecting message from user_id=%s chat_id=%s", user.id, chat.id)
            return

        text = text_override if text_override is not None else (msg.text or msg.caption or "")
        thread_id = str(msg.message_thread_id) if msg.message_thread_id else None

        media: List[Dict[str, Any]] = []
        if media_override is not None:
            media = list(media_override)
        else:
            media = await self._extract_media(msg)

        inbound = InboundMessage(
            channel=self.name,
            chat_id=str(chat.id),
            user_id=str(user.id),
            user_name=user.full_name or user.username or "",
            text=text,
            thread_id=thread_id,
            reply_to_message_id=str(msg.reply_to_message.message_id) if msg.reply_to_message else None,
            media=media,
            is_command=text.lstrip().startswith("/"),
            command=(text.split(maxsplit=1)[0].lstrip("/").lower() or None) if text.lstrip().startswith("/") else None,
            command_args=(text.split(maxsplit=1)[1] if text.lstrip().startswith("/") and " " in text else None),
            raw=msg,
        )

        # C6: capture the inbound event at the channel boundary — BEFORE the
        # agent starts. This gives the timeline an exact "message arrived at
        # CVC" timestamp, separate from chat.session_start (which fires
        # inside run_chat_turn_streaming and only if the agent actually runs).
        try:
            capture_message_in(
                channel=self.name,
                actor=str(user.id),
                session_id=f"cvc_ch_{self.name}_{chat.id}_{thread_id or ''}".rstrip("_"),
                summary=(text[:140] if text else f"[/c]{inbound.command}" if inbound.command else "<empty>"),
                data={
                    "chat_id": str(chat.id),
                    "thread_id": thread_id,
                    "user_name": inbound.user_name,
                    "media_count": len(media),
                    "media_kinds": [m.get("kind", "?") for m in media],
                    "is_command": inbound.is_command,
                    "command": inbound.command,
                    "command_args": (inbound.command_args or "")[:80],
                    "reply_to": inbound.reply_to_message_id,
                    "is_edit": bool(update.edited_message),
                    "text_length": len(text or ""),
                },
            )
        except Exception:
            pass

        # Show typing indicator while the agent thinks.
        try:
            await self._bot.send_chat_action(chat_id=chat.id, action=ChatAction.TYPING)
        except Exception:
            pass

        # ── Slash command fast-path ──────────────────────────────────
        # Intercept slash commands BEFORE the streaming pipeline and
        # route them based on the SLASH_REGISTRY exec strategy:
        #   "agent"  → forward through streaming pipeline (agent handles it)
        #   "route"  → hit the gateway API directly
        #   "client" → handle locally or return instructions
        if text.strip().startswith("/") and text.strip() != "/cancel":
            handled = await self._handle_slash_command(chat, msg, text)
            if handled:
                return

        # ── Streaming path ───────────────────────────────────────────
        # When stream_edits is enabled and this isn't a media-only message,
        # use the live streaming pipeline (word-by-word message editing).
        if self._stream_edits and text.strip():
            try:
                handled = await self._handle_streaming(chat, msg, inbound)
                if handled:
                    return
            except Exception as exc:  # noqa: BLE001
                logger.warning("telegram: streaming failed, falling back: %s", exc)
                # C6: capture channel-level streaming failure.
                try:
                    capture_message_error(
                        channel=self.name,
                        actor=str(user.id),
                        session_id=f"cvc_ch_{self.name}_{chat.id}_{thread_id or ''}".rstrip("_"),
                        summary=f"telegram: streaming failed: {type(exc).__name__}",
                        data={
                            "chat_id": str(chat.id),
                            "error_type": "streaming_failure",
                            "exception": type(exc).__name__,
                            "message": str(exc)[:200],
                        },
                    )
                except Exception:
                    pass

        # ── Non-streaming fallback (via registry) ────────────────────
        reply = await self._emit_inbound(inbound)
        if reply is None or not reply.text:
            return
        await self.send(reply)

    async def _handle_slash_command(
        self,
        chat: Any,
        msg: Any,
        text: str,
    ) -> bool:
        """Unified slash command handler for Telegram.

        Routes every registered slash command to its proper handler:
        - "agent"  → forward through streaming pipeline (the agent knows).
        - "route"  → hit the gateway API directly with proper args.
        - "client" → handle locally:
          - Model/branch/persona pickers → inline keyboards with the
            actual catalog fetched from /api/catalog/providers
          - Session commands (/new, /clear) → handle locally
          - Dashboard-only UI actions → forward to agent or send instructions
        - Unknown commands → forward to streaming pipeline (the agent may
          understand them naturally).

        Returns ``True`` if the command was handled, ``False`` to fall
        through to the streaming pipeline.
        """
        parts = text.strip().split(maxsplit=1)
        cmd = parts[0].lower()
        args_str = parts[1] if len(parts) > 1 else ""
        chat_id = chat.id

        # ── Channel-specific commands (always handle locally) ────────
        if cmd == "/help":
            await self._on_help_inline(chat_id, msg)
            return True

        if cmd == "/cancel":
            await self._bot.send_message(
                chat_id=chat_id,
                text="_Cancellation requested\\._",
                parse_mode=ParseMode.MARKDOWN_V2,
            )
            return True

        # ── Look up in SLASH_REGISTRY ────────────────────────────────
        entry = None
        try:
            from cvc.dashboard.dx_api import SLASH_REGISTRY
            entry = next(
                (c for c in SLASH_REGISTRY if c.get("cmd") == cmd),
                None,
            )
        except Exception:
            pass

        if entry is None:
            # Unknown slash command — forward to agent for natural-language
            # interpretation. (The streaming pipeline will handle it.)
            return False

        exec_strategy = entry.get("exec", "agent")
        client_action = entry.get("client_action", "")
        route = entry.get("route", "")

        # ── exec="route" — direct API call ──────────────────────────
        if exec_strategy == "route" and route:
            return await self._exec_route_command(chat_id, route, cmd, args_str, entry)

        # ── exec="client" with picker actions → inline keyboard ─────
        if client_action == "open_model_picker":
            return await self._show_model_picker(chat_id, cmd)
        if client_action == "open_branch_picker":
            return await self._show_branch_picker(chat_id, cmd)
        if client_action == "open_persona_picker":
            return await self._show_persona_picker(chat_id, cmd)
        if client_action == "open_workspace_picker":
            return await self._show_workspace_picker(chat_id, cmd)
        if client_action == "open_insights_panel":
            return await self._exec_route_command(
                chat_id, "GET /api/dx/insights", cmd, args_str, entry,
            )
        if client_action == "open_pins_panel":
            await self._bot.send_message(
                chat_id=chat_id,
                text="_Pinned messages are a dashboard feature\\. In Telegram, just reference the message directly\\._",
                parse_mode=ParseMode.MARKDOWN_V2,
            )
            return True
        if client_action in ("new_thread", "clear_thread"):
            # Session commands — send the placeholder + tell the user to
            # start a fresh conversation. The session itself stays in the
            # agent cache so context flows normally; what we really mean
            # here is "the dashboard's local thread state". For Telegram
            # we just acknowledge.
            await self._bot.send_message(
                chat_id=chat_id,
                text="✓ _Session reset\\. Your next message starts a fresh conversation\\._",
                parse_mode=ParseMode.MARKDOWN_V2,
            )
            return True
        if client_action in ("copy_last_message", "pin_selected_message",
                             "open_sessions_panel", "abort_stream"):
            # Dashboard-only UI actions.
            await self._bot.send_message(
                chat_id=chat_id,
                text=f"_`{client_action}` is a dashboard\\-only action\\. Not available in Telegram\\._",
                parse_mode=ParseMode.MARKDOWN_V2,
            )
            return True

        # ── exec="agent" (default) — forward to streaming pipeline ───
        # The agent has system-prompt instructions and tools for these.
        return False

    async def _exec_route_command(
        self,
        chat_id: int,
        route: str,
        cmd: str,
        args_str: str,
        entry: Dict[str, Any],
    ) -> bool:
        """Execute a ``"route"`` slash command by hitting the gateway API.

        The route format is ``"METHOD /api/path"``. Args from the user
        (after the slash command) are parsed and packed into the body
        according to the entry's args schema (best-effort string split).
        """
        try:
            method, _, path = route.partition(" ")
            url = f"http://localhost:13421{path}"

            # Build body from user args + entry's args schema.
            # First entry is the primary arg — put it under that key.
            args_schema = entry.get("args", []) if entry else []
            json_body: Dict[str, Any] = {}
            if args_schema and args_str:
                primary_key = args_schema[0].get("name", "value")
                # If the cmd is /remember, split into kind + content.
                if cmd == "/remember":
                    parts = args_str.split(maxsplit=1)
                    json_body["kind"] = parts[0] if parts else "fact"
                    json_body["content"] = parts[1] if len(parts) > 1 else ""
                elif cmd == "/think" or cmd == "/effort":
                    json_body["level"] = args_str.strip().lower()
                elif cmd == "/model":
                    # /model <provider> <model> or just /model <model>
                    parts = args_str.split(maxsplit=1)
                    json_body["provider"] = parts[0] if parts else ""
                    if len(parts) > 1:
                        json_body["model"] = parts[1]
                elif cmd == "/cd":
                    json_body["workspace_path"] = args_str
                elif cmd == "/branch" or cmd == "/checkout":
                    json_body["ref"] = args_str
                elif cmd == "/commit":
                    json_body["message"] = args_str
                else:
                    json_body[primary_key] = args_str

            if method == "GET":
                resp = await self._http_get(url)
            elif method == "POST":
                resp = await self._http_post(url, json_body=json_body or None)
            elif method == "PUT":
                resp = await self._http_put(url, json_body=json_body or None)
            else:
                resp = {"error": f"Unsupported method: {method}"}

            result_text = self._format_api_response(cmd, resp)
            await self._bot.send_message(
                chat_id=chat_id,
                text=result_text[: _TG_MAX_TEXT],
                parse_mode=ParseMode.MARKDOWN_V2,
                disable_web_page_preview=True,
            )
            return True
        except Exception as exc:
            logger.warning("telegram: route command %s failed: %s", cmd, exc)
            # Fall through to streaming pipeline — agent may handle.
            return False

    async def _show_model_picker(self, chat_id: int, cmd: str) -> bool:
        """Inline-keyboard picker for switching provider+model.

        Fetches the catalog from ``/api/catalog/providers`` and renders
        one button per provider; tapping a provider re-sends the picker
        with the provider's model list as buttons.
        """
        try:
            resp = await self._http_get("http://localhost:13421/api/catalog/providers")
            providers = resp.get("providers", []) if isinstance(resp, dict) else []
            if not providers:
                # Fallback: hardcoded list
                await self._bot.send_message(
                    chat_id=chat_id,
                    text=(
                        "⚠️ _Provider catalog unavailable\\. Use `/model <provider> <model>` to switch\\._\n\n"
                        "*Known providers:*\n"
                        "• `anthropic` \\- Claude models\n"
                        "• `openai` \\- GPT models\n"
                        "• `google` \\- Gemini models\n"
                        "• `ollama` \\- local models\n"
                        "• `copilot` \\- GitHub Copilot"
                    ),
                    parse_mode=ParseMode.MARKDOWN_V2,
                )
                return True

            rows: list = []
            for prov in providers[:8]:  # Telegram button row limit considerations
                pname = prov.get("id", prov.get("name", "?"))
                plabel = prov.get("label", pname)
                rows.append([InlineKeyboardButton(
                    text=f"📡 {plabel}",
                    callback_data=f"pick:provider:{pname}",
                )])

            await self._bot.send_message(
                chat_id=chat_id,
                text="*Select a provider:*",
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=InlineKeyboardMarkup(rows),
            )
            return True
        except Exception as exc:
            logger.warning("model picker failed: %s", exc)
            return False

    async def _show_branch_picker(self, chat_id: int, cmd: str) -> bool:
        """Show a picker of git branches."""
        try:
            resp = await self._http_get("http://localhost:13421/api/git/branches")
            branches = resp.get("branches", []) if isinstance(resp, dict) else []
            active = resp.get("active", "") if isinstance(resp, dict) else ""

            if not branches:
                await self._bot.send_message(
                    chat_id=chat_id,
                    text="_No branches found in current workspace\\._",
                    parse_mode=ParseMode.MARKDOWN_V2,
                )
                return True

            rows: list = []
            for br in branches[:20]:  # Telegram row cap
                name = br if isinstance(br, str) else br.get("name", "?")
                is_active = " ✓" if name == active else ""
                rows.append([InlineKeyboardButton(
                    text=f"🌿 {name}{is_active}",
                    callback_data=f"pick:branch:{name}",
                )])

            await self._bot.send_message(
                chat_id=chat_id,
                text=f"*Switch to branch:*\n_\\(current: `{escape_mdv2(active)}`\\)_",
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=InlineKeyboardMarkup(rows),
            )
            return True
        except Exception as exc:
            logger.warning("branch picker failed: %s", exc)
            return False

    async def _show_persona_picker(self, chat_id: int, cmd: str) -> bool:
        """Show a picker of personas."""
        await self._bot.send_message(
            chat_id=chat_id,
            text=(
                "*Available personas:*\n"
                "• `sofia` \\- default\n"
                "• `analyst` \\- focused on data\n"
                "• `engineer` \\- coding\\-focused\n\n"
                "_Use `/persona <name>` to switch\\._"
            ),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return True

    async def _show_workspace_picker(self, chat_id: int, cmd: str) -> bool:
        """Show a picker of workspaces."""
        await self._bot.send_message(
            chat_id=chat_id,
            text=(
                "📁 *Workspace picker*\n\n"
                "_The Telegram bot has full machine access by default \\(`/model home`\\)_\n\n"
                "If you need a different workspace, type `/cd <absolute path>`\\."
            ),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return True

    async def _handle_picker_callback(self, cq: Any) -> None:
        """Handle callback queries from picker buttons."""
        data = cq.data or ""
        # Format: "pick:provider:<id>" or "pick:branch:<name>"
        parts = data.split(":", 2)
        if len(parts) < 3 or parts[0] != "pick":
            await cq.answer("Unknown picker action")
            return
        kind, value = parts[1], parts[2]
        await cq.answer()  # Dismiss the spinner

        if kind == "provider":
            # Show models for this provider
            try:
                resp = await self._http_get(
                    f"http://localhost:13421/api/catalog/providers/{value}/models"
                )
                models = resp.get("models", []) if isinstance(resp, dict) else []
                if not models:
                    await cq.edit_message_text(
                        text=f"_No models for `{value}`\\._",
                        parse_mode=ParseMode.MARKDOWN_V2,
                    )
                    return

                rows: list = []
                for m in models[:20]:
                    mname = m if isinstance(m, str) else m.get("id", m.get("name", "?"))
                    rows.append([InlineKeyboardButton(
                        text=f"⚡ {mname}",
                        callback_data=f"pick:model:{value}:{mname}",
                    )])
                await cq.edit_message_text(
                    text=f"*Select a model from `{escape_mdv2(value)}`:*",
                    parse_mode=ParseMode.MARKDOWN_V2,
                    reply_markup=InlineKeyboardMarkup(rows),
                )
            except Exception as exc:
                logger.warning("provider model fetch failed: %s", exc)
                await cq.edit_message_text(
                    text=f"⚠️ _Could not load models: `{escape_mdv2(str(exc)[:100])}`\\._",
                    parse_mode=ParseMode.MARKDOWN_V2,
                )
            return

        if kind == "model":
            # Actually switch
            provider, model = value.split(":", 1) if ":" in value else (value, "")
            try:
                resp = await self._http_post(
                    "http://localhost:13421/api/models/switch",
                    json_body={"provider": provider, "model": model},
                )
                if "error" in resp:
                    await cq.edit_message_text(
                        text=f"⚠️ _{escape_mdv2(str(resp['error'])[:200])}\\_",
                        parse_mode=ParseMode.MARKDOWN_V2,
                    )
                else:
                    await cq.edit_message_text(
                        text=(
                            f"✓ *Model switched*\n"
                            f"• Provider: `{escape_mdv2(provider)}`\n"
                            f"• Model: `{escape_mdv2(model)}`"
                        ),
                        parse_mode=ParseMode.MARKDOWN_V2,
                    )
            except Exception as exc:
                await cq.edit_message_text(
                    text=f"⚠️ _{escape_mdv2(str(exc)[:200])}\\_",
                    parse_mode=ParseMode.MARKDOWN_V2,
                )
            return

        if kind == "branch":
            # Switch branch
            try:
                resp = await self._http_post(
                    "http://localhost:13421/api/git/checkout",
                    json_body={"branch": value},
                )
                if "error" in resp:
                    await cq.edit_message_text(
                        text=f"⚠️ _{escape_mdv2(str(resp['error'])[:200])}\\_",
                        parse_mode=ParseMode.MARKDOWN_V2,
                    )
                else:
                    await cq.edit_message_text(
                        text=f"✓ *Switched to branch `{escape_mdv2(value)}`*",
                        parse_mode=ParseMode.MARKDOWN_V2,
                    )
            except Exception as exc:
                await cq.edit_message_text(
                    text=f"⚠️ _{escape_mdv2(str(exc)[:200])}\\_",
                    parse_mode=ParseMode.MARKDOWN_V2,
                )
            return

        await cq.edit_message_text(
            text="_Unknown picker action\\._",
            parse_mode=ParseMode.MARKDOWN_V2,
        )

    def _format_api_response(self, cmd: str, resp: Dict[str, Any]) -> str:
        """Format an API response dict as Telegram-friendly MarkdownV2 text."""
        if not resp:
            return f"_{cmd} returned no output_"
        if "error" in resp:
            err = str(resp["error"])[:200]
            return f"⚠️ _{cmd} error:_ {err}"
        # Pretty-print the response
        import json
        try:
            pretty = json.dumps(resp, indent=2, default=str, ensure_ascii=False)[:2000]
        except Exception:
            pretty = str(resp)[:2000]
        return f"*{cmd}*\n```\n{pretty}\n```"

    async def _http_get(self, url: str, **kw) -> Dict[str, Any]:
        async with httpx.AsyncClient() as c:
            r = await c.get(url, **kw)
            return r.json() if r.status_code < 400 else {"error": f"{r.status_code} {r.text[:200]}"}

    async def _http_post(self, url: str, json_body: Optional[dict] = None, **kw) -> Dict[str, Any]:
        async with httpx.AsyncClient() as c:
            r = await c.post(url, json=json_body, **kw)
            return r.json() if r.status_code < 400 else {"error": f"{r.status_code} {r.text[:200]}"}

    async def _http_put(self, url: str, json_body: Optional[dict] = None, **kw) -> Dict[str, Any]:
        async with httpx.AsyncClient() as c:
            r = await c.put(url, json=json_body, **kw)
            return r.json() if r.status_code < 400 else {"error": f"{r.status_code} {r.text[:200]}"}

    async def _on_help_inline(self, chat_id: int, msg: Any) -> None:
        """Inline help that includes discovered commands + skills."""
        help_lines = [
            "*🤖 CVC — Time Machine for AI Agents*\n",
            "Send any message and CVC responds with full cognitive context\\.\n",
            "*Commands:*\n",
        ]
        # Get a sample of commands from the registry
        try:
            from cvc.dashboard.dx_api import SLASH_REGISTRY
            groups: Dict[str, list] = {}
            for entry in SLASH_REGISTRY:
                g = entry.get("group", "other")
                groups.setdefault(g, []).append(entry)
            for group_name in sorted(groups.keys()):
                cmds = groups[group_name]
                help_lines.append(f"\n*{group_name.title()}*")
                for c in cmds[:8]:  # Cap per group
                    help_lines.append(f"  `{c['cmd']}` — {c.get('desc', '')}")
        except Exception:
            help_lines.append("  `/help` — Show this help")
            help_lines.append("  `/status` — Agent status")

        await self._bot.send_message(
            chat_id=chat_id,
            text="\n".join(help_lines)[: _TG_MAX_TEXT],
            parse_mode=ParseMode.MARKDOWN_V2,
            disable_web_page_preview=True,
        )

    async def _handle_streaming(
        self,
        chat: Any,
        msg: Any,
        inbound: InboundMessage,
    ) -> bool:
        """Live streaming response — NO cloud placeholder, NO edit-then-delete.

        Two paths, picked at call time:

        A. **Native draft streaming** (``sendMessageDraft``, Bot API 9.5+) —
           the chat client's "typing in chat…" animation IS the live
           stream. Same ``draft_id`` reused across calls makes Telegram
           update the preview in place. On ``done`` we send the final
           formatted message via normal ``send_message``; the draft
           preview clears naturally on the client. **No placeholder
           message is ever sent, no edit storm, no delete dance.**

        B. **Edit-based fallback** (groups, or older PTB) — send one
           empty message, then ``edit_message_text`` every ~0.9s as
           tokens arrive. On ``done`` we do a single final edit with
           MarkdownV2 formatting. The message id stays the same
           throughout — no replacement, no second message, no cloud.

        Tool calls and thinking events are inlined into the streamed
        text as small italic footnotes (``↳ read_file(...)`` /
        ``✓ done in 120 ms``) so the customer sees activity without
        a separate sticker/GIF/thinking animation. Same parity with
        the Hermes Telegram channel (``sendMessageDraft`` is what
        Hermes uses; see
        ``cvc.agent._vendor.hermes.gateway.platforms.telegram:send_draft``).
        """
        if not _RUN_CHAT_TURN_STREAMING_AVAILABLE or run_chat_turn_streaming is None:
            logger.debug("telegram: streaming disabled (run_chat_turn_streaming unavailable)")
            return False

        chat_id = int(inbound.chat_id)
        reply_to = int(inbound.reply_to_message_id) if inbound.reply_to_message_id else None
        thread_id = int(inbound.thread_id) if inbound.thread_id else None

        # Pick the streaming strategy based on chat type + bot API.
        chat_type = getattr(chat, "type", "") or ""
        use_drafts = (
            chat_type == "private"
            and self._bot is not None
            and hasattr(self._bot, "send_message_draft")
        )

        # ── Path A: native draft streaming ──────────────────────────
        if use_drafts:
            return await self._stream_via_drafts(
                chat_id=chat_id,
                reply_to=reply_to,
                thread_id=thread_id,
                inbound=inbound,
            )

        # ── Path B: edit-based fallback ─────────────────────────────
        return await self._stream_via_edits(
            chat_id=chat_id,
            reply_to=reply_to,
            thread_id=thread_id,
            inbound=inbound,
        )

    async def _stream_via_drafts(
        self,
        *,
        chat_id: int,
        reply_to: Optional[int],
        thread_id: Optional[int],
        inbound: InboundMessage,
    ) -> bool:
        """Path A — native ``sendMessageDraft`` streaming + per-tool cards.

        UX parity with Hermes's Telegram platform:
        - **Text deltas** stream live into ONE draft message (the "live
          response" — same message_id throughout)
        - **Each tool call** becomes its OWN Telegram message as a card
          (``🔍 search_files: "class AIAgent"``) — sent the instant the
          tool starts. The card is then EDITED in-place when the tool
          finishes (``✓ search_files done in 45 ms``)
        - **Final response** replaces the draft in chat history

        Customers see activity **live, block by block**, exactly like
        Hermes — no waiting for the full response, no internal debug
        noise, clean formatted cards with emoji + tool name + arg preview.

        References: Hermes's
        ``cvc.agent._vendor.hermes.gateway.platforms.telegram`` (card
        rendering + draft streaming) and
        ``cvc.agent._vendor.hermes.agent.display`` (emoji + preview).
        """
        import hashlib
        seed = f"{chat_id}:{reply_to or 0}:{inbound.text[:32]}".encode("utf-8")
        draft_id = int.from_bytes(
            hashlib.blake2b(seed, digest_size=4).digest(),
            "big",
            signed=True,
        )

        # Tool card tracking — map call_id → telegram message_id so we
        # can edit the card in-place when the tool finishes. Same key as
        # the gateway outbox emits.
        tool_cards: dict[str, int] = {}

        accumulated: list[str] = []
        last_send = 0.0
        # v3.3.41 — Monotonically-growing cursor into ``accumulated``.
        # CRITICAL: tracks how many characters have already been shown
        # to the user. Without this, every new text delta causes the
        # draft preview to re-render from the FIRST character, which
        # looks like "delete-and-rewrite" on the user's screen. With
        # this, only the NEW tail is delivered — text grows monotonically
        # even across tool-call interruptions.
        delivered_chars: int = 0
        last_typing_ping = time.time()
        TYPING_REFRESH = 4.0
        DRAFT_INTERVAL = 0.15

        async for event in run_chat_turn_streaming(
            channel=inbound.channel,
            chat_id=inbound.chat_id,
            user_id=inbound.user_id,
            user_name=inbound.user_name,
            thread_id=inbound.thread_id,
            text=inbound.text,
        ):
            etype = event.get("type")
            now = time.time()

            if now - last_typing_ping >= TYPING_REFRESH:
                try:
                    await self._bot.send_chat_action(
                        chat_id=chat_id, action=ChatAction.TYPING,
                    )
                    last_typing_ping = now
                except Exception:
                    pass

            if etype == "text":
                delta = event.get("content", "")
                if delta:
                    accumulated.append(delta)
                    # Typewriter for batched providers — only deliver the
                    # NEW tail (chars past ``delivered_chars``) so the
                    # message grows monotonically instead of re-rendering
                    # from word 0.
                    full_text = "".join(accumulated)
                    new_tail = full_text[delivered_chars:]
                    if len(new_tail) > 40:
                        await self._deliver_progressive(
                            accumulated_tail=new_tail,
                            already_shown_prefix=full_text[:delivered_chars],
                            chat_id=chat_id,
                            draft_id=draft_id,
                            thread_id=thread_id,
                            last_send_ref={"v": last_send},
                            interval=DRAFT_INTERVAL,
                            use_drafts=True,
                        )
                        delivered_chars = len(full_text)
                        last_send = time.time()
                    elif now - last_send >= DRAFT_INTERVAL:
                        preview = full_text[:_TG_MAX_TEXT]
                        if preview.strip():
                            ok = await self._send_draft_frame(
                                chat_id=chat_id,
                                draft_id=draft_id,
                                content=preview,
                                thread_id=thread_id,
                            )
                            if ok:
                                last_send = now
                                delivered_chars = len(full_text)

            elif etype == "tool_start":
                # Send a SEPARATE Telegram message for each tool call —
                # this is the "block" UX from Hermes. The card is sent
                # instantly when the tool starts, then edited in-place
                # when it finishes.
                call_id = event.get("call_id", "")
                name = event.get("name") or event.get("label") or "tool"
                preview = event.get("label") or event.get("preview") or ""
                emoji = event.get("emoji") or "⚙️"
                card_text = self._format_tool_card_start(emoji, name, preview)
                if call_id:
                    try:
                        card_msg = await self._bot.send_message(
                            chat_id=chat_id,
                            text=card_text,
                            parse_mode=ParseMode.MARKDOWN_V2,
                            message_thread_id=thread_id,
                            disable_web_page_preview=True,
                        )
                        tool_cards[call_id] = card_msg.message_id
                    except Exception as exc:  # noqa: BLE001
                        logger.debug("telegram: tool card send failed: %s", exc)

            elif etype == "tool_result":
                # Edit the tool's card in-place: 🔍 search_files: "..."
                # → ✓ search_files done in 45 ms. Same message_id, no
                # new bubble, no cleanup needed.
                call_id = event.get("call_id", "")
                name = event.get("name") or "tool"
                dur_ms = event.get("duration_ms")
                msg_id = tool_cards.pop(call_id, None)
                if msg_id is not None:
                    card_text = self._format_tool_card_done(name, dur_ms)
                    try:
                        await self._bot.edit_message_text(
                            chat_id=chat_id,
                            message_id=msg_id,
                            text=card_text,
                            parse_mode=ParseMode.MARKDOWN_V2,
                            disable_web_page_preview=True,
                        )
                    except Exception as exc:  # noqa: BLE001
                        logger.debug("telegram: tool card edit failed: %s", exc)

            elif etype == "status":
                # Status events become ephemeral info messages — small,
                # italic, separate bubble. Not inlined into the draft.
                msg = event.get("content") or event.get("message") or ""
                if msg:
                    try:
                        await self._bot.send_message(
                            chat_id=chat_id,
                            text=f"_{self._escape_mdv2_inline(msg)}_",
                            parse_mode=ParseMode.MARKDOWN_V2,
                            message_thread_id=thread_id,
                            disable_web_page_preview=True,
                        )
                    except Exception:
                        pass

            elif etype == "done":
                final_text = event.get("content", "") or "".join(accumulated)
                if not final_text.strip():
                    await self._bot.send_message(
                        chat_id=chat_id,
                        text="_(no response generated)_",
                        parse_mode=ParseMode.MARKDOWN_V2,
                        reply_to_message_id=reply_to,
                        message_thread_id=thread_id,
                    )
                    return True
                await self._send_final_message(
                    chat_id=chat_id,
                    final_text=final_text,
                    reply_to=reply_to,
                    thread_id=thread_id,
                )
                return True

            elif etype == "error":
                logger.warning(
                    "telegram: streaming error event: %s",
                    event.get("message"),
                )

        # Stream ended without a done event — send whatever we got.
        final_text = "".join(accumulated)
        if final_text.strip():
            await self._send_final_message(
                chat_id=chat_id,
                final_text=final_text,
                reply_to=reply_to,
                thread_id=thread_id,
            )
        else:
            await self._bot.send_message(
                chat_id=chat_id,
                text="⚠️ _No response generated\\._",
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_to_message_id=reply_to,
                message_thread_id=thread_id,
            )
        return True

    async def _send_draft_frame(
        self,
        *,
        chat_id: int,
        draft_id: int,
        content: str,
        thread_id: Optional[int],
    ) -> bool:
        """Send one ``sendMessageDraft`` frame. Returns True on success.

        Tries MarkdownV2 first, falls back to plain text on parse
        failure. Identical retry shape to Hermes's ``send_draft``.
        """
        text = content[:_TG_MAX_TEXT]
        for use_markdown in (True, False):
            kwargs: Dict[str, Any] = {
                "chat_id": chat_id,
                "draft_id": draft_id,
                "text": self._format_mdv2(text) if use_markdown else text,
            }
            if use_markdown:
                kwargs["parse_mode"] = ParseMode.MARKDOWN_V2
            if thread_id is not None:
                kwargs["message_thread_id"] = thread_id
            try:
                ok = await self._bot.send_message_draft(**kwargs)
                if ok:
                    return True
            except Exception as exc:  # noqa: BLE001
                logger.debug(
                    "telegram: sendMessageDraft failed (markdown=%s): %s",
                    use_markdown, exc,
                )
                if not use_markdown:
                    return False
        return False

    async def _stream_via_edits(
        self,
        *,
        chat_id: int,
        reply_to: Optional[int],
        thread_id: Optional[int],
        inbound: InboundMessage,
    ) -> bool:
        """Path B — edit-based streaming + per-tool cards (groups).

        Same UX as Path A but uses ``edit_message_text`` instead of
        ``sendMessageDraft`` because the latter only works in DMs.
        Each tool call still becomes its own card message; the streamed
        text still updates one message in place.
        """
        EDIT_INTERVAL = 0.15

        try:
            placeholder = await self._bot.send_message(
                chat_id=chat_id,
                text="…",
                reply_to_message_id=reply_to,
                message_thread_id=thread_id,
            )
        except Exception:
            return False
        edit_msg_id = placeholder.message_id

        tool_cards: dict[str, int] = {}
        accumulated: list[str] = []
        last_edit_time = 0.0
        had_any_text = False
        # v3.3.41 — Monotonic cursor into ``accumulated``. See the
        # matching comment in ``_stream_via_drafts`` for why this is
        # critical (without it, every text delta re-edits the message
        # from word 0, looking like delete-and-rewrite to the user).
        delivered_chars: int = 0

        async for event in run_chat_turn_streaming(
            channel=inbound.channel,
            chat_id=inbound.chat_id,
            user_id=inbound.user_id,
            user_name=inbound.user_name,
            thread_id=inbound.thread_id,
            text=inbound.text,
        ):
            etype = event.get("type")
            now = time.time()
            if etype == "text":
                delta = event.get("content", "")
                if delta:
                    accumulated.append(delta)
                    had_any_text = True
                    full_text = "".join(accumulated)
                    new_tail = full_text[delivered_chars:]
                    if len(new_tail) > 40:
                        await self._deliver_progressive(
                            accumulated_tail=new_tail,
                            already_shown_prefix=full_text[:delivered_chars],
                            chat_id=chat_id,
                            edit_msg_id=edit_msg_id,
                            thread_id=thread_id,
                            last_send_ref={"v": last_edit_time},
                            interval=EDIT_INTERVAL,
                            use_drafts=False,
                        )
                        delivered_chars = len(full_text)
                        last_edit_time = time.time()
                    elif now - last_edit_time >= EDIT_INTERVAL:
                        preview = full_text[:_TG_MAX_TEXT]
                        if preview.strip():
                            try:
                                await self._bot.edit_message_text(
                                    chat_id=chat_id,
                                    message_id=edit_msg_id,
                                    text=preview + " ▌",
                                )
                                last_edit_time = now
                                delivered_chars = len(full_text)
                            except Exception:
                                pass

            elif etype == "tool_start":
                call_id = event.get("call_id", "")
                name = event.get("name") or event.get("label") or "tool"
                preview = event.get("label") or event.get("preview") or ""
                emoji = event.get("emoji") or "⚙️"
                card_text = self._format_tool_card_start(emoji, name, preview)
                if call_id:
                    try:
                        card_msg = await self._bot.send_message(
                            chat_id=chat_id,
                            text=card_text,
                            parse_mode=ParseMode.MARKDOWN_V2,
                            message_thread_id=thread_id,
                            disable_web_page_preview=True,
                        )
                        tool_cards[call_id] = card_msg.message_id
                    except Exception as exc:  # noqa: BLE001
                        logger.debug("telegram: tool card send failed: %s", exc)

            elif etype == "tool_result":
                call_id = event.get("call_id", "")
                name = event.get("name") or "tool"
                dur_ms = event.get("duration_ms")
                msg_id = tool_cards.pop(call_id, None)
                if msg_id is not None:
                    card_text = self._format_tool_card_done(name, dur_ms)
                    try:
                        await self._bot.edit_message_text(
                            chat_id=chat_id,
                            message_id=msg_id,
                            text=card_text,
                            parse_mode=ParseMode.MARKDOWN_V2,
                            disable_web_page_preview=True,
                        )
                    except Exception as exc:  # noqa: BLE001
                        logger.debug("telegram: tool card edit failed: %s", exc)

            elif etype == "status":
                msg = event.get("content") or event.get("message") or ""
                if msg:
                    try:
                        await self._bot.send_message(
                            chat_id=chat_id,
                            text=f"_{self._escape_mdv2_inline(msg)}_",
                            parse_mode=ParseMode.MARKDOWN_V2,
                            message_thread_id=thread_id,
                            disable_web_page_preview=True,
                        )
                    except Exception:
                        pass

            elif etype == "done":
                final_text = event.get("content", "") or "".join(accumulated)
                if not final_text.strip():
                    if not had_any_text:
                        try:
                            await self._bot.edit_message_text(
                                chat_id=chat_id,
                                message_id=edit_msg_id,
                                text="_(no response generated)_",
                                parse_mode=ParseMode.MARKDOWN_V2,
                            )
                        except Exception:
                            pass
                    return True
                await self._finalize_edit_message(
                    chat_id=chat_id,
                    edit_msg_id=edit_msg_id,
                    final_text=final_text,
                    thread_id=thread_id,
                )
                return True

            elif etype == "error":
                logger.warning(
                    "telegram: streaming error event: %s",
                    event.get("message"),
                )

        final_text = "".join(accumulated)
        if final_text.strip():
            await self._finalize_edit_message(
                chat_id=chat_id,
                edit_msg_id=edit_msg_id,
                final_text=final_text,
                thread_id=thread_id,
            )
        else:
            try:
                await self._bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=edit_msg_id,
                    text="⚠️ _No response generated\\._",
                    parse_mode=ParseMode.MARKDOWN_V2,
                )
            except Exception:
                pass
        return True

    async def _deliver_progressive(
        self,
        *,
        accumulated_tail: str,
        already_shown_prefix: str,
        chat_id: int,
        thread_id: Optional[int],
        last_send_ref: dict,
        interval: float,
        use_drafts: bool,
        draft_id: Optional[int] = None,
        edit_msg_id: Optional[int] = None,
    ) -> None:
        """Typewriter-style progressive delivery for batched responses.

        v3.3.41 — Now types out ONLY the new tail (chars past
        ``already_shown_prefix``). Each frame sent to Telegram is
        ``already_shown_prefix + running_tail_snapshot`` — meaning the
        message grows monotonically. The caller tracks
        ``delivered_chars`` (which == ``len(already_shown_prefix)`` at
        the time of the call) and is responsible for advancing it.

        This prevents the "delete-and-rewrite" loop where every text
        delta re-rendered the message from word 0. After this fix, once
        the user sees text X, text X is never re-rendered — only NEW
        characters are appended.

        When a provider returns the entire response as one large delta
        (common with MiniMax-M3 via Anthropic Messages API, or any
        provider that buffers streaming), this method splits the
        *new tail* into word-level chunks and delivers each chunk to
        the draft/edit with a small delay — giving the user a smooth
        appending experience instead of a full-response dump.

        Args:
            accumulated_tail: the NEW characters since last delivery
                (does NOT include already-shown text).
            already_shown_prefix: the prefix the user already sees.
                Each frame will be ``prefix + growing_tail``.
            chat_id: Telegram chat id
            thread_id: optional thread (message_thread_id)
            last_send_ref: mutable dict {"v": float} tracking last send time
            interval: minimum seconds between delivery frames
            use_drafts: True → send_message_draft, False → edit_message_text
            draft_id: required if use_drafts=True
            edit_msg_id: required if use_drafts=False
        """
        if not accumulated_tail or not accumulated_tail.strip() or len(accumulated_tail) < 40:
            return

        # Split into word-level chunks. We preserve whitespace by splitting
        # on spaces and re-joining with spaces, keeping the original
        # formatting (newlines etc.) as part of the word tokens.
        import re as _re
        words = _re.split(r"(\s+)", accumulated_tail)  # split keeping whitespace
        if len(words) < 4:
            return

        # Group into chunks of ~4 word-tokens for smooth delivery.
        CHUNK_WORDS = 4
        # Delay between chunks — fast enough to feel live, slow enough
        # for Telegram to render each frame. ~30ms gives ~130 words/sec
        # which is faster than any human can read but looks "alive".
        CHUNK_DELAY = 0.03

        running_tail = ""
        for i in range(0, len(words), CHUNK_WORDS):
            chunk_end = min(i + CHUNK_WORDS, len(words))
            running_tail = "".join(words[:chunk_end])
            frame = (already_shown_prefix + running_tail)[:_TG_MAX_TEXT]

            if use_drafts and draft_id is not None:
                ok = await self._send_draft_frame(
                    chat_id=chat_id,
                    draft_id=draft_id,
                    content=frame,
                    thread_id=thread_id,
                )
                if not ok:
                    break
            elif edit_msg_id is not None:
                try:
                    await self._bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=edit_msg_id,
                        text=frame + " ▌",
                    )
                except Exception:
                    pass

            last_send_ref["v"] = time.time()
            await asyncio.sleep(CHUNK_DELAY)

    @staticmethod
    def _format_tool_card_start(emoji: str, name: str, preview: str) -> str:
        """Format the 'tool starting' card message.

        Matches Hermes's ``format_tool_event`` style for the
        ``"all"`` mode: ``{emoji} {tool_name}: "{preview}"``

        Args:
            emoji: tool emoji (e.g. ``🔍`` from ``get_tool_emoji``)
            name: tool name (e.g. ``search_files``)
            preview: short preview of the primary argument
        """
        from ..formatting.markdown import escape_mdv2
        safe_emoji = escape_mdv2(emoji)
        safe_name = escape_mdv2(name)
        safe_preview = escape_mdv2(preview) if preview else ""
        if safe_preview:
            return f"{safe_emoji} {safe_name}: `{safe_preview}`"
        return f"{safe_emoji} {safe_name}\\.\\.\\."

    @staticmethod
    def _format_tool_card_done(name: str, dur_ms: Optional[int]) -> str:
        """Format the 'tool finished' card edit. The same card gets
        edited in-place from ``🔍 search_files: ...`` to this."""
        from ..formatting.markdown import escape_mdv2
        safe_name = escape_mdv2(name)
        if isinstance(dur_ms, (int, float)) and dur_ms >= 0:
            return f"✓ {safe_name} _done in {int(dur_ms)} ms_"
        return f"✓ {safe_name} _done_"

    @staticmethod
    def _escape_mdv2_inline(text: str) -> str:
        """Escape a short text for use in an italic MarkdownV2 message.

        Only used for status messages — does NOT wrap in code blocks
        or do table rewrites. Matches the ``_to_mdv2`` pipeline's
        escape behaviour but is cheaper for short status strings.
        """
        from ..formatting.markdown import escape_mdv2
        return escape_mdv2(text)

    @staticmethod
    def _render_event_line(event: dict) -> Optional[str]:
        """Render a non-text event (``tool_start``, ``tool_result``,
        ``status``) as a small italic footnote line that gets inlined
        into the streamed draft/edited message. Customer sees activity
        without a separate sticker/GIF/animation."""
        etype = event.get("type")
        if etype == "tool_start":
            name = event.get("name") or event.get("label") or "tool"
            return f"\n\n_↳ {name}\\.\\.\\._\n\n"
        if etype == "tool_result":
            name = event.get("name") or "tool"
            dur = event.get("duration_ms")
            if isinstance(dur, (int, float)) and dur >= 0:
                return f"\n\n_✓ {name} done in {int(dur)} ms_\n\n"
            return f"\n\n_✓ {name} done_\n\n"
        if etype == "status":
            msg = event.get("content") or event.get("message") or ""
            if msg:
                return f"\n\n_{msg}_\n\n"
        return None

    def _format_mdv2(self, text: str) -> str:
        """Apply MarkdownV2 escape + table rewrite for a draft frame.

        Wraps ``_to_mdv2`` for one chunk (drafts are length-capped the
        same as messages).
        """
        chunks = _to_mdv2(text)
        return chunks[0] if chunks else text

    async def _send_final_message(
        self,
        *,
        chat_id: int,
        final_text: str,
        reply_to: Optional[int],
        thread_id: Optional[int],
    ) -> None:
        """Send the final formatted message after a draft stream.

        MarkdownV2 → plain text fallback on parse failure. Long
        responses split at paragraph boundaries and sent as multiple
        messages (each one ``reply_to`` the original user message so
        the thread stays anchored).
        """
        chunks = _to_mdv2(final_text)
        for idx, chunk in enumerate(chunks):
            sent = False
            for use_markdown in (True, False):
                kwargs: Dict[str, Any] = {
                    "chat_id": chat_id,
                    "text": chunk,
                    "disable_web_page_preview": True,
                    # Only the first message gets reply_to_message_id
                    # so we don't create a reply chain.
                    "reply_to_message_id": reply_to if idx == 0 else None,
                }
                if use_markdown:
                    kwargs["parse_mode"] = ParseMode.MARKDOWN_V2
                if thread_id is not None:
                    kwargs["message_thread_id"] = thread_id
                try:
                    await self._bot.send_message(**kwargs)
                    sent = True
                    break
                except Exception as exc:  # noqa: BLE001
                    logger.debug(
                        "telegram: final send failed (markdown=%s): %s",
                        use_markdown, exc,
                    )
                    if not use_markdown:
                        break
            if not sent:
                logger.warning(
                    "telegram: could not deliver final chunk %d/%d",
                    idx + 1, len(chunks),
                )

    async def _finalize_edit_message(
        self,
        chat_id: int,
        edit_msg_id: int,
        final_text: str,
        thread_id: Optional[int],
    ) -> None:
        """Edit-based path: apply final MarkdownV2 formatting to the
        same message that was streaming — no delete, no replacement,
        no cloud. One edit, one message id, final answer.
        """
        chunks = _to_mdv2(final_text)
        if not chunks:
            return
        # Apply first chunk as a single edit. The trailing caret ` ▌`
        # is gone, the MarkdownV2 formatting is on. Same message_id.
        try:
            await self._bot.edit_message_text(
                chat_id=chat_id,
                message_id=edit_msg_id,
                text=chunks[0],
                parse_mode=ParseMode.MARKDOWN_V2,
                disable_web_page_preview=True,
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "telegram: final edit failed msg_id=%s: %s — "
                "falling back to send",
                edit_msg_id, exc,
            )
            # Last-resort fallback: send as new message (still no cloud,
            # still no delete).
            try:
                await self._bot.send_message(
                    chat_id=chat_id,
                    text=chunks[0],
                    parse_mode=ParseMode.MARKDOWN_V2,
                    disable_web_page_preview=True,
                    message_thread_id=thread_id,
                )
            except Exception:
                pass
        # Overflow continuations — same edit-or-send logic so the
        # thread stays anchored to the user's original message and
        # we never create a second "cloud".
        for chunk in chunks[1:]:
            kwargs: Dict[str, Any] = {
                "chat_id": chat_id,
                "text": chunk,
                "parse_mode": ParseMode.MARKDOWN_V2,
                "disable_web_page_preview": True,
            }
            if thread_id is not None:
                kwargs["message_thread_id"] = thread_id
            try:
                await self._bot.send_message(**kwargs)
            except Exception as exc:  # noqa: BLE001
                logger.debug(
                    "telegram: continuation send failed: %s — "
                    "retrying plain text", exc,
                )
                plain_kwargs = dict(kwargs)
                plain_kwargs.pop("parse_mode", None)
                try:
                    await self._bot.send_message(**plain_kwargs)
                except Exception:
                    pass

    async def _extract_media(self, msg: Message) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []
        if msg.photo:
            # Largest size is the last entry.
            biggest = msg.photo[-1]
            data = await _download_telegram_file(self._bot, biggest.file_id)
            if data:
                out.append({
                    "kind": "photo",
                    "data": data,
                    "mime": "image/jpeg",
                    "size": biggest.file_size or 0,
                    "caption": msg.caption or "",
                })
        for attr, kind in (
            ("audio", "audio"),
            ("voice", "voice"),
            ("video", "video"),
            ("document", "document"),
        ):
            obj = getattr(msg, attr, None)
            if obj is None:
                continue
            data = await _download_telegram_file(self._bot, obj.file_id)
            if data:
                out.append({
                    "kind": kind,
                    "data": data,
                    "mime": getattr(obj, "mime_type", None) or "application/octet-stream",
                    "size": getattr(obj, "file_size", 0) or 0,
                    "filename": getattr(obj, "file_name", None),
                    "caption": msg.caption or "",
                })
        return out

    async def _reply(self, update: Update, text: str) -> None:
        msg = update.message or update.edited_message
        if msg is None:
            return
        thread_id = msg.message_thread_id if msg.message_thread_id else None
        await self.send(OutboundMessage(
            chat_id=str(msg.chat_id),
            thread_id=str(thread_id) if thread_id else None,
            reply_to_message_id=str(msg.message_id),
            text=text,
        ))

    def _info(self) -> Dict[str, Any]:
        info = super()._info()
        info.update({
            "polling": not bool(self.cfg("webhook_url", "").strip()),
            "allowlist_size": len(getattr(self, "_allowlist", [])),
            "parse_mode": getattr(self, "_default_parse_mode", "markdownv2"),
        })
        return info


# ─────────────────────────────────────────────────────────────────────────────
# Small helpers
# ─────────────────────────────────────────────────────────────────────────────


def mangle_filename(url: str, content_type: str, ext: str) -> str:
    """Pick a sane filename for a downloaded media."""
    # Try to extract a basename from the URL path.
    base = ""
    try:
        from urllib.parse import urlparse
        base = Path(urlparse(url).path).name
    except Exception:
        pass
    if base and "." in base:
        return base
    if not ext:
        ext = mimetypes.guess_extension(content_type.split(";")[0].strip()) or ".bin"
    return f"cvc-media-{int(time.time())}{ext}"
