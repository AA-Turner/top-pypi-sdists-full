import asyncio

from project.core.util import setup_logging
from project.tg_bot.tg_bot import get_cached_tg_bot
from project.tg_bot.util.set_tg_bot_commands import set_client_tg_bot_commands, set_admin_tg_bot_commands


async def __async_command():
    setup_logging()
    await set_client_tg_bot_commands()
    await set_admin_tg_bot_commands()
    await get_cached_tg_bot().session.close()


if __name__ == '__main__':
    asyncio.run(__async_command())
