import logging

import aiogram
from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from arpakitlib.ar_exception_util import exception_to_traceback_str
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from project.sqlalchemy_db_.sqlalchemy_model import StoryLogDBM
from project.tg_bot.blank.client import get_cached_rus_client_tg_bot_blank
from project.tg_bot.middleware.common import MiddlewareDataTgBot

_logger = logging.getLogger(__name__)

tg_bot_router = Router()


@tg_bot_router.error()
async def _(
        error_event: aiogram.types.ErrorEvent,
        state: FSMContext,
        middleware_data_tg_bot: MiddlewareDataTgBot,
        **kwargs
):
    await state.clear()

    need_logging = True
    need_create_story_log = True

    if (
            error_event.update.event_type == "message"
            and isinstance(error_event.update.event, aiogram.types.Message)
    ):
        try:
            await error_event.update.event.answer(
                text=get_cached_rus_client_tg_bot_blank().error()
            )
        except Exception as exception:
            _logger.error(exception)

    if (
            error_event.update.event_type == "callback_query"
            and isinstance(error_event.update.event, aiogram.types.CallbackQuery)
    ):

        if isinstance(error_event.exception, TelegramBadRequest) and (
                error_event.exception.message
                and "message is not modified".lower().strip() in error_event.exception.message.lower().strip()
        ):
            error_linked_with_message_not_modified = True
        else:
            error_linked_with_message_not_modified = False

        if error_linked_with_message_not_modified:
            need_logging = False
            need_create_story_log = False

        try:
            await error_event.update.event.answer()
        except Exception as exception:
            _logger.error(exception)

        if not error_linked_with_message_not_modified:

            try:
                await error_event.update.event.message.edit_reply_markup(reply_markup=None)
            except Exception as exception:
                _logger.error(exception)

            try:
                await error_event.update.event.message.answer(
                    text=get_cached_rus_client_tg_bot_blank().error()
                )
            except Exception as exception:
                _logger.error(exception)

    if need_logging:
        _logger.exception(error_event.exception)

    if need_create_story_log:
        if get_cached_sqlalchemy_db() is not None:
            async with get_cached_sqlalchemy_db().new_async_session() as session:
                story_log_dbm = StoryLogDBM(
                    level=StoryLogDBM.Levels.error,
                    type=StoryLogDBM.Types.error_in_tg_bot,
                    title=f"{type(error_event.exception)}",
                    extra_data={
                        "exception": str(error_event.exception),
                        "exception_traceback": exception_to_traceback_str(exception=error_event.exception)
                    }
                )
                session.add(story_log_dbm)
                await session.commit()
                await session.refresh(story_log_dbm)
