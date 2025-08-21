import aiogram
import telebot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

from project.core.settings import get_cached_settings
from project.core.setup_logging import setup_logging


def create_async_tg_bot_notifier() -> aiogram.Bot | None:
    if get_cached_settings().tg_bot_notifier_token is None:
        return None
    session: AiohttpSession | None = None
    if get_cached_settings().tg_bot_notifier_proxy_url:
        session = AiohttpSession(proxy=get_cached_settings().tg_bot_notifier_proxy_url)
    tg_bot = aiogram.Bot(
        token=get_cached_settings().tg_bot_notifier_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            disable_notification=False,
            link_preview_is_disabled=True
        ),
        session=session
    )
    return tg_bot


def create_tg_bot_notifier() -> telebot.TeleBot | None:
    if not get_cached_settings().tg_bot_notifier_token:
        return None

    if get_cached_settings().tg_bot_notifier_proxy_url is not None:
        telebot.apihelper.proxy = {
            "https": get_cached_settings().tg_bot_notifier_proxy_url,
            "http": get_cached_settings().tg_bot_notifier_proxy_url
        }

    return telebot.TeleBot(get_cached_settings().tg_bot_notifier_token, parse_mode="HTML")


def __example():
    setup_logging()
    create_tg_bot_notifier().send_message(chat_id=269870432, text="Hello world")


if __name__ == '__main__':
    __example()
