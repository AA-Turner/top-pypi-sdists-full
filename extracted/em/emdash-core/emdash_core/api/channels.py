"""REST API for channel management (Telegram, etc.).

The TUI calls these endpoints to check status, configure, connect,
and disconnect communication channels during the startup wizard.
"""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/channels", tags=["channels"])


# -- Models ----------------------------------------------------------------

class ChannelStatus(BaseModel):
    configured: bool
    connected: bool
    bot_username: str | None = None


class SetupRequest(BaseModel):
    bot_token: str


class SetupResponse(BaseModel):
    success: bool
    bot_username: str | None = None
    error: str | None = None


class ConnectRequest(BaseModel):
    agent_type: str = "open"


# -- Endpoints -------------------------------------------------------------

@router.get("/telegram/status", response_model=ChannelStatus)
async def telegram_status() -> ChannelStatus:
    """Check whether Telegram is configured and/or connected."""
    from ..agent.tools.channel import get_telegram_channel_status

    info = get_telegram_channel_status()
    bot_username = info.get("bot_username")

    # If configured but bot_username isn't cached yet, fetch it from Telegram
    if info["configured"] and not bot_username:
        from ..channels.telegram.bot import verify_token
        from ..channels.telegram.config import get_config, save_config

        tg_config = get_config()
        if tg_config.bot_token:
            try:
                bot_user = await verify_token(tg_config.bot_token)
                if bot_user and bot_user.username:
                    bot_username = bot_user.username
                    tg_config.state.bot_username = bot_username
                    save_config(tg_config)
            except Exception:
                pass

    return ChannelStatus(
        configured=info["configured"],
        connected=info["connected"],
        bot_username=bot_username,
    )


@router.post("/telegram/setup", response_model=SetupResponse)
async def telegram_setup(req: SetupRequest) -> SetupResponse:
    """Verify a bot token with the Telegram API and save it."""
    from ..channels.telegram.bot import verify_token
    from ..channels.telegram.config import get_config, save_config

    bot_user = await verify_token(req.bot_token)
    if bot_user is None:
        return SetupResponse(success=False, error="Invalid bot token — Telegram API rejected it.")

    tg_config = get_config()
    tg_config.bot_token = req.bot_token
    tg_config.state.enabled = True
    tg_config.state.bot_username = bot_user.username
    save_config(tg_config)

    return SetupResponse(success=True, bot_username=bot_user.username)


@router.post("/telegram/connect")
async def telegram_connect(req: ConnectRequest | None = None) -> dict:
    """Start the Telegram channel loop."""
    from ..agent.tools.channel import start_telegram_channel

    agent_type = (req.agent_type if req else None) or "open"
    result = await start_telegram_channel(
        agent_options={"agent_type": agent_type},
    )
    if "error" in result:
        return {"status": "error", "error": result["error"]}
    return {"status": "connected"}


@router.post("/telegram/disconnect")
async def telegram_disconnect() -> dict:
    """Stop the Telegram channel loop."""
    from ..agent.tools.channel import stop_telegram_channel

    result = await stop_telegram_channel()
    if "error" in result:
        return {"status": "error", "error": result["error"]}
    return {"status": "disconnected"}
