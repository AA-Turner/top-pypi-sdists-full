"""ChannelTool — lets the LLM agent connect/disconnect/check communication channels."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from .base import BaseTool, ToolCategory, ToolResult

log = logging.getLogger(__name__)

# Background tasks keyed by channel name so disconnect can cancel them.
_channel_tasks: dict[str, asyncio.Task] = {}


# ---------------------------------------------------------------------------
# Shared helpers — reusable by both ChannelTool and the REST API
# ---------------------------------------------------------------------------


async def start_telegram_channel(
    server_url: str | None = None,
    agent_options: dict | None = None,
) -> dict:
    """Start the Telegram channel loop. Returns a status dict.

    Reusable by both ChannelTool and the channels REST API.

    Args:
        server_url: Base URL of the emdash-core server.
        agent_options: Options forwarded to ``/api/agent/chat`` (e.g.
            ``{"agent_type": "open"}``).
    """
    from ...channels.router import get_channel_router
    from ...channels.telegram import TelegramChannel
    from ...channels.telegram.config import get_config as get_tg_config
    from ...config import get_config as get_server_config

    router = get_channel_router()
    if router is None:
        return {"error": "Channel router not initialized (server not started?)."}

    if "telegram" in _channel_tasks and not _channel_tasks["telegram"].done():
        return {"error": "Telegram channel is already connected."}

    tg_config = get_tg_config()
    if not tg_config.is_configured():
        return {"error": "Telegram bot token not configured."}

    channel = TelegramChannel(tg_config)
    router.register(channel)
    router.set_primary(channel.name)

    if server_url is None:
        srv = get_server_config()
        server_url = f"http://{srv.host}:{srv.port}"

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return {"error": "No running event loop — cannot start channel."}

    import httpx

    # Use generous timeouts: agent responses can stream for minutes.
    # read timeout = time between chunks (SSE pings every 15s, so 120s is safe).
    timeout = httpx.Timeout(connect=30, read=120, write=30, pool=30)

    # Event set by the task once channel.start() succeeds (or fails).
    started = asyncio.Event()
    startup_error: list[str] = []

    async def _run_loop():
        _RECONNECT_DELAYS = [5, 10, 30, 60, 120]  # seconds
        consecutive_failures = 0
        first_start = True

        async with httpx.AsyncClient(timeout=timeout) as client:
            while True:
                # (Re)create channel instance on reconnect so internal state
                # (bot client, running flag) is fresh.
                nonlocal channel
                if not first_start:
                    channel = TelegramChannel(tg_config)
                    router.register(channel)
                    router.set_primary(channel.name)

                try:
                    await channel.start()
                    if first_start:
                        started.set()
                        first_start = False
                    consecutive_failures = 0
                    log.info("Telegram channel connected (polling)")
                    try:
                        async for message in channel.poll_messages():
                            if not await channel.check_authorization(message.sender_id):
                                from ...channels.base import ChannelEvent
                                await channel.send_event(
                                    message.sender_id,
                                    ChannelEvent("error", "Not authorized"),
                                )
                                continue
                            if await channel.route_message(message):
                                continue
                            session_id = channel.get_session_id(message.sender_id)
                            from ...channels.loop import _process_agent_stream
                            await _process_agent_stream(
                                channel, client, server_url, message, session_id, agent_options,
                            )
                    finally:
                        await channel.stop()

                except asyncio.CancelledError:
                    log.info("Telegram channel loop cancelled")
                    break  # intentional shutdown — no reconnect

                except Exception as exc:
                    from ...channels.telegram.bot import TelegramAPIError

                    if isinstance(exc, TelegramAPIError) and exc.error_code == 409:
                        msg = (
                            "Another bot instance is already polling with this token. "
                            "Stop the other process (e.g. run_telegram_bot.py) and try again."
                        )
                        log.error(msg)
                        if first_start:
                            startup_error.append(msg)
                            started.set()
                        break  # 409 is permanent — no reconnect

                    # Transient failure — reconnect with backoff
                    if first_start:
                        startup_error.append(str(exc))
                        started.set()
                        break  # fail fast on first start

                    idx = min(consecutive_failures, len(_RECONNECT_DELAYS) - 1)
                    delay = _RECONNECT_DELAYS[idx]
                    consecutive_failures += 1
                    log.warning(
                        "Telegram channel disconnected (%s), reconnecting in %ds",
                        exc, delay,
                    )
                    await asyncio.sleep(delay)
                    continue  # retry

            router.unregister("telegram")

    task = loop.create_task(_run_loop(), name="channel_loop:telegram")
    _channel_tasks["telegram"] = task

    # Wait up to 10s for the task to actually start (validates token, etc.)
    try:
        await asyncio.wait_for(started.wait(), timeout=10)
    except asyncio.TimeoutError:
        pass  # proceed anyway — polling might just be slow

    if startup_error:
        task.cancel()
        _channel_tasks.pop("telegram", None)
        return {"error": f"Telegram channel failed to start: {startup_error[0]}"}

    bot_username = tg_config.state.bot_username or None
    return {
        "channel": "telegram",
        "status": "connected",
        "bot_username": bot_username,
        "message": "Telegram channel connected and polling for messages.",
    }


async def stop_telegram_channel() -> dict:
    """Stop the Telegram channel loop. Returns a status dict."""
    from ...channels.router import get_channel_router

    task = _channel_tasks.pop("telegram", None)
    if task is not None and not task.done():
        task.cancel()

    router = get_channel_router()
    if router is not None:
        router.unregister("telegram")

    return {"channel": "telegram", "status": "disconnected", "message": "Telegram channel disconnected."}


def get_telegram_channel_status() -> dict:
    """Get current Telegram channel status. Returns a status dict."""
    from ...channels.telegram.config import get_config as get_tg_config

    tg_config = get_tg_config()
    task = _channel_tasks.get("telegram")
    connected = task is not None and not task.done() if task else False

    return {
        "configured": tg_config.is_configured(),
        "connected": connected,
        "bot_username": tg_config.state.bot_username,
    }


class ChannelTool(BaseTool):
    """Manage external communication channels (e.g. Telegram).

    Actions:
      - **connect**  — start receiving/sending messages on a channel
      - **disconnect** — stop an active channel
      - **status** — list registered channels and their availability
      - **setup** — save configuration (e.g. bot token) for a channel
    """

    name = "manage_channel"
    description = (
        "Connect, disconnect, or check the status of communication channels "
        "(e.g. Telegram). Use action='setup' to save a bot token, "
        "action='connect' to start, action='disconnect' to stop, "
        "action='status' to inspect."
    )
    category = ToolCategory.COMMUNICATION

    def __init__(self, connection=None):
        super().__init__(connection=False)

    # -- Schema ----------------------------------------------------------

    def get_schema(self) -> dict:
        return self._make_schema(
            {
                "action": {
                    "type": "string",
                    "enum": ["connect", "disconnect", "status", "setup"],
                    "description": "Action to perform on the channel.",
                },
                "channel_type": {
                    "type": "string",
                    "enum": ["telegram"],
                    "description": "Which channel to act on (default: telegram).",
                },
                "config": {
                    "type": "object",
                    "description": (
                        "Configuration dict for 'setup' action. "
                        "For telegram: {\"bot_token\": \"...\"}."
                    ),
                },
            },
            required=["action"],
        )

    # -- Execute ---------------------------------------------------------

    def execute(
        self,
        action: str,
        channel_type: str = "telegram",
        config: dict[str, Any] | None = None,
        **kwargs,
    ) -> ToolResult:
        if channel_type != "telegram":
            return ToolResult.error_result(
                f"Unsupported channel type: {channel_type}",
                suggestions=["Currently only 'telegram' is supported."],
            )

        dispatch = {
            "connect": self._connect,
            "disconnect": self._disconnect,
            "status": self._status,
            "setup": self._setup,
        }
        handler = dispatch.get(action)
        if handler is None:
            return ToolResult.error_result(
                f"Unknown action: {action}",
                suggestions=["Use one of: connect, disconnect, status, setup"],
            )
        return handler(channel_type, config or {})

    # -- Actions ---------------------------------------------------------

    def _connect(self, channel_type: str, config: dict) -> ToolResult:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return ToolResult.error_result("No running event loop — cannot start channel.")

        import concurrent.futures
        future: concurrent.futures.Future = concurrent.futures.Future()

        async def _do():
            try:
                future.set_result(await start_telegram_channel())
            except Exception as exc:
                future.set_exception(exc)

        loop.call_soon_threadsafe(asyncio.ensure_future, _do())
        result = future.result(timeout=15)

        if "error" in result:
            return ToolResult.error_result(result["error"])
        return ToolResult.success_result(data=result)

    def _disconnect(self, channel_type: str, config: dict) -> ToolResult:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return ToolResult.error_result("No running event loop.")

        import concurrent.futures
        future: concurrent.futures.Future = concurrent.futures.Future()

        async def _do():
            try:
                future.set_result(await stop_telegram_channel())
            except Exception as exc:
                future.set_exception(exc)

        loop.call_soon_threadsafe(asyncio.ensure_future, _do())
        result = future.result(timeout=15)

        if "error" in result:
            return ToolResult.error_result(result["error"])
        return ToolResult.success_result(data=result)

    def _status(self, channel_type: str, config: dict) -> ToolResult:
        from ...channels.router import get_channel_router

        router = get_channel_router()
        if router is None:
            return ToolResult.success_result(data={"channels": [], "primary": None})

        channels_info = []
        for name, ch in router.channels.items():
            task = _channel_tasks.get(name)
            channels_info.append({
                "name": name,
                "running": task is not None and not task.done() if task else False,
                "is_primary": router.primary is ch,
            })

        return ToolResult.success_result(
            data={
                "channels": channels_info,
                "primary": router.primary.name if router.primary else None,
            }
        )

    def _setup(self, channel_type: str, config: dict) -> ToolResult:
        from ...channels.telegram.config import get_config as get_tg_config, save_config
        from ...channels.telegram.bot import verify_token

        bot_token = config.get("bot_token")
        if not bot_token:
            return ToolResult.error_result(
                "Missing 'bot_token' in config.",
                suggestions=["Provide config={\"bot_token\": \"123456:ABC-DEF...\"}"],
            )

        # Verify token with Telegram API
        import asyncio

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop is not None:
            import concurrent.futures
            # We're inside an event loop (tool likely called from async context).
            # verify_token is async so we need to run it properly.
            # Use loop.create_task if already in async, but execute() is sync.
            # Schedule a coroutine and wait for the result via a Future.
            future: concurrent.futures.Future = concurrent.futures.Future()

            async def _verify():
                try:
                    result = await verify_token(bot_token)
                    future.set_result(result)
                except Exception as exc:
                    future.set_exception(exc)

            loop.call_soon_threadsafe(asyncio.ensure_future, _verify())
            try:
                bot_user = future.result(timeout=15)
            except Exception:
                bot_user = None
        else:
            try:
                bot_user = asyncio.run(verify_token(bot_token))
            except Exception:
                bot_user = None

        if bot_user is None:
            return ToolResult.error_result(
                "Invalid bot token — Telegram API rejected it.",
                suggestions=["Double-check the token from @BotFather."],
            )

        tg_config = get_tg_config()
        tg_config.bot_token = bot_token
        tg_config.state.enabled = True
        tg_config.state.bot_username = bot_user.username
        save_config(tg_config)

        return ToolResult.success_result(
            data={
                "channel": channel_type,
                "bot_username": bot_user.username,
                "bot_name": bot_user.first_name,
                "message": f"Telegram bot @{bot_user.username} configured. Use action='connect' to start.",
            }
        )
