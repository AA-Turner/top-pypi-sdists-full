import logging

import aiogram.filters
from aiogram import Router
from aiogram.fsm.context import FSMContext

from project.tg_bot.blank.client import get_cached_rus_client_tg_bot_blank
from project.tg_bot.middleware.common import MiddlewareDataTgBot

tg_bot_router = Router()
_logger = logging.getLogger(__name__)


@tg_bot_router.message(aiogram.F.content_type == aiogram.enums.ContentType.VOICE)
async def _(
        m: aiogram.types.Message,
        state: FSMContext,
        middleware_data_tg_bot: MiddlewareDataTgBot,
        **kwargs
):
    await state.clear()
    await m.answer(text=get_cached_rus_client_tg_bot_blank().raw_message())
