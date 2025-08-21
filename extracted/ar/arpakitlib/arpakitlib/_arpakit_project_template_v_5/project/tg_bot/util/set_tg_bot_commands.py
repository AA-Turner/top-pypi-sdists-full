import asyncio
import logging

from aiogram.types import BotCommand, BotCommandScopeChat

from arpakitlib.ar_str_util import return_str_if_none
from project.core.settings import get_cached_settings
from project.core.setup_logging import setup_logging
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM
from project.tg_bot.blank.client import get_cached_rus_client_tg_bot_blank
from project.tg_bot.const import ClientTgBotCommands, AdminTgBotCommands
from project.tg_bot.tg_bot import get_cached_tg_bot

_logger = logging.getLogger(__name__)


def get_client_tg_bot_commands_to_set() -> list[BotCommand]:
    res = [
        BotCommand(
            command=ClientTgBotCommands.start,
            description=return_str_if_none(
                get_cached_rus_client_tg_bot_blank().command_to_desc().get(ClientTgBotCommands.start),
                ClientTgBotCommands.start
            )
        ),
        BotCommand(
            command=ClientTgBotCommands.about,
            description=return_str_if_none(
                get_cached_rus_client_tg_bot_blank().command_to_desc().get(ClientTgBotCommands.about),
                ClientTgBotCommands.about
            )
        ),
        BotCommand(
            command=ClientTgBotCommands.support,
            description=return_str_if_none(
                get_cached_rus_client_tg_bot_blank().command_to_desc().get(ClientTgBotCommands.support),
                ClientTgBotCommands.support
            )
        ),
        BotCommand(
            command=ClientTgBotCommands.author,
            description=return_str_if_none(
                get_cached_rus_client_tg_bot_blank().command_to_desc().get(ClientTgBotCommands.author),
                ClientTgBotCommands.author
            )
        )
    ]
    return res


def get_admin_tg_bot_commands_to_set() -> list[BotCommand]:
    res = []
    for command in AdminTgBotCommands.values_list():
        res.append(BotCommand(
            command=command,
            description=command
        ))
    return res


async def set_client_tg_bot_commands():
    _logger.info(f"start")
    await get_cached_tg_bot().set_my_commands(commands=get_client_tg_bot_commands_to_set())
    _logger.info("finish")


async def set_admin_tg_bot_commands():
    _logger.info(f"start")

    user_tg_ids = set()
    for tg_bot_admin_tg_id in get_cached_settings().tg_bot_admin_tg_ids:
        user_tg_ids.add(tg_bot_admin_tg_id)

    if get_cached_sqlalchemy_db() is not None:
        with get_cached_sqlalchemy_db().new_session() as session:
            user_dbms: list[UserDBM] = session.query(UserDBM).filter(UserDBM.roles.any(UserDBM.Roles.admin)).all()
            for user_dbm in user_dbms:
                user_tg_ids.add(user_dbm.tg_id)

    for user_tg_id in user_tg_ids:
        await get_cached_tg_bot().set_my_commands(
            commands=get_client_tg_bot_commands_to_set() + get_admin_tg_bot_commands_to_set(),
            scope=BotCommandScopeChat(chat_id=user_tg_id)
        )

    _logger.info("finish")


async def set_all_tg_bot_commands():
    _logger.info(f"start")
    await set_client_tg_bot_commands()
    await set_admin_tg_bot_commands()
    _logger.info("finish")


async def __async_example():
    setup_logging()
    await set_client_tg_bot_commands()
    await set_admin_tg_bot_commands()
    await get_cached_tg_bot().session.close()


if __name__ == '__main__':
    asyncio.run(__async_example())
