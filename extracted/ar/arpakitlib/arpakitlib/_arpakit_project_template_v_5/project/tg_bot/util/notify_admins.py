import asyncio
import logging
from datetime import timedelta

import sqlalchemy
from aiogram.exceptions import AiogramError
from emoji import emojize

from arpakitlib.ar_str_util import remove_tags_and_html
from project.core.settings import get_cached_settings
from project.core.setup_logging import setup_logging
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM
from project.tg_bot.tg_bot import get_cached_tg_bot

_logger = logging.getLogger(__name__)


async def notify_admins(text: str):
    text = emojize(
        f"<b>Notification for admin</b>"
        f"\n\n"
        f"{text.strip()}"
    )

    admin_tg_ids = set()

    if get_cached_sqlalchemy_db() is not None:
        async with get_cached_sqlalchemy_db().new_async_session() as async_session:
            admin_user_dbms: list[UserDBM] = (await async_session.scalars(
                sqlalchemy.select(UserDBM).filter(UserDBM.roles.any(UserDBM.Roles.admin))
            )).all()
        for admin_user_dbm in admin_user_dbms:
            admin_tg_ids.add(admin_user_dbm.tg_id)

    for tg_id in get_cached_settings().tg_bot_admin_tg_ids:
        admin_tg_ids.add(tg_id)

    for admin_tg_id in admin_tg_ids:
        try:
            await get_cached_tg_bot().send_message(
                chat_id=admin_tg_id,
                text=text,
                request_timeout=int(timedelta(seconds=3).total_seconds())
            )
        except AiogramError as exception:
            _logger.error(exception)
            try:
                await get_cached_tg_bot().send_message(
                    chat_id=admin_tg_id,
                    text=remove_tags_and_html(text),
                    request_timeout=int(timedelta(seconds=3).total_seconds())
                )
            except AiogramError as exception:
                _logger.error(exception)


async def __async_example():
    setup_logging()
    await notify_admins("Hello world")
    await get_cached_tg_bot().session.close()


if __name__ == '__main__':
    asyncio.run(__async_example())
