import asyncio

import aiohttp
import aiohttp.web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from project.core.settings import get_cached_settings
from project.core.util import setup_logging
from project.tg_bot.tg_bot import get_cached_tg_bot
from project.tg_bot.tg_bot_dispatcher import create_tg_bot_dispatcher


def start_tg_bot():
    setup_logging()

    tg_bot = get_cached_tg_bot()

    tg_bot_dispatcher = create_tg_bot_dispatcher()

    if not get_cached_settings().tg_bot_webhook_enabled:
        asyncio.run(tg_bot_dispatcher.start_polling(tg_bot))
    else:
        app = aiohttp.web.Application()
        simple_requests_handler = SimpleRequestHandler(
            dispatcher=tg_bot_dispatcher,
            bot=tg_bot,
            secret_token=get_cached_settings().tg_bot_webhook_secret
        )
        simple_requests_handler.register(app, path=get_cached_settings().tg_bot_webhook_path)
        setup_application(app, tg_bot_dispatcher, bot=tg_bot)
        aiohttp.web.run_app(
            app=app,
            host=get_cached_settings().tg_bot_webhook_server_hostname,
            port=get_cached_settings().tg_bot_webhook_server_port
        )


if __name__ == '__main__':
    start_tg_bot()
