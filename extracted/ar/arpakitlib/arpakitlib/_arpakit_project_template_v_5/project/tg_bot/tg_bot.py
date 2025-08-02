from functools import lru_cache

import aiogram
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

from project.core.settings import get_cached_settings


def create_tg_bot() -> aiogram.Bot:
    session: AiohttpSession | None = None
    if get_cached_settings().tg_bot_proxy_url is not None:
        session = AiohttpSession(proxy=get_cached_settings().tg_bot_proxy_url)

    tg_bot = aiogram.Bot(
        token=get_cached_settings().tg_bot_token,
        session=session,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            disable_notification=False,
            link_preview_is_disabled=True
        )
    )

    return tg_bot


@lru_cache()
def get_cached_tg_bot() -> aiogram.Bot:
    return create_tg_bot()
