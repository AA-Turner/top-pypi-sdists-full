import logging

from aiogram import Router, types
from aiogram.exceptions import AiogramError
from aiogram.fsm.context import FSMContext

from project.tg_bot.callback_data_.client import RemoveMessageClientCD
from project.tg_bot.middleware.common import MiddlewareDataTgBot

_logger = logging.getLogger(__name__)
tg_bot_router = Router()


@tg_bot_router.callback_query(
    RemoveMessageClientCD.filter(),
)
async def _(
        cq: types.CallbackQuery,
        state: FSMContext,
        middleware_data_tg_bot: MiddlewareDataTgBot,
        **kwargs
):
    try:
        await cq.message.delete()
    except AiogramError as exception:
        _logger.error(exception)
        try:
            await cq.answer()
        except AiogramError as exception:
            _logger.error(exception)
