import logging
from typing import Any, Awaitable, Callable, Dict

import aiogram
import sqlalchemy
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from arpakitlib.ar_datetime_util import now_utc_dt
from project.core.settings import get_cached_settings
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM
from project.tg_bot.middleware.common import MiddlewareDataTgBot

_logger = logging.getLogger(__name__)


class InitUserTgBotMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        _logger.info("start")

        if "middleware_data_tg_bot" in data:
            middleware_data_tg_bot = data["middleware_data_tg_bot"]
        else:
            middleware_data_tg_bot = MiddlewareDataTgBot()
            data["middleware_data_tg_bot"] = middleware_data_tg_bot

        tg_user: aiogram.types.User | None = None
        if event.event_type == "message":
            tg_user = event.message.from_user
        elif event.event_type == "callback_query":
            tg_user = event.callback_query.from_user
        elif event.event_type == "inline_query":
            tg_user = event.inline_query.from_user

        if tg_user is not None:
            middleware_data_tg_bot.additional_data["tg_user_was_found"] = tg_user
            middleware_data_tg_bot.additional_data["found_tg_user_id"] = tg_user.id

        now_utc_dt_ = now_utc_dt()

        if tg_user is not None and get_cached_sqlalchemy_db() is not None:
            async with get_cached_sqlalchemy_db().new_async_session() as async_session:
                middleware_data_tg_bot.current_user_dbm = await async_session.scalar(
                    sqlalchemy.select(UserDBM).filter(UserDBM.tg_id == tg_user.id)
                )
                if middleware_data_tg_bot.current_user_dbm is None:
                    roles = [UserDBM.Roles.client]
                    if tg_user.id in get_cached_settings().tg_bot_admin_tg_ids:
                        roles.append(UserDBM.Roles.admin)
                    middleware_data_tg_bot.current_user_dbm = UserDBM(
                        creation_dt=now_utc_dt_,
                        roles=roles,
                        is_verified=True,
                        tg_id=tg_user.id,
                        tg_data=tg_user.model_dump(mode="json"),
                        tg_bot_last_action_dt=now_utc_dt_
                    )
                    async_session.add(middleware_data_tg_bot.current_user_dbm)
                    await async_session.commit()
                    await async_session.refresh(middleware_data_tg_bot.current_user_dbm)
                    middleware_data_tg_bot.current_user_dbm_just_created = True
                    _logger.info(f"user_dbm was added, {middleware_data_tg_bot.current_user_dbm}")
                else:
                    middleware_data_tg_bot.current_user_dbm.is_verified = True
                    middleware_data_tg_bot.current_user_dbm.tg_data = tg_user.model_dump(mode="json")
                    middleware_data_tg_bot.current_user_dbm.tg_bot_last_action_dt = now_utc_dt_
                    if (
                            tg_user.id in get_cached_settings().tg_bot_admin_tg_ids
                            and UserDBM.Roles.admin not in middleware_data_tg_bot.current_user_dbm.roles
                    ):
                        middleware_data_tg_bot.current_user_dbm.roles = (
                                middleware_data_tg_bot.current_user_dbm.roles + [UserDBM.Roles.admin]
                        )
                    await async_session.commit()
                    await async_session.refresh(middleware_data_tg_bot.current_user_dbm)
                    middleware_data_tg_bot.current_user_dbm_just_created = False

        _logger.info("finish")

        return await handler(event, data)
