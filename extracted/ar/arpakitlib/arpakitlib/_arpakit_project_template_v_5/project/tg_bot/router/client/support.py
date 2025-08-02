import logging

import aiogram
from aiogram import Router
from aiogram.filters import Command, or_f
from aiogram.fsm.context import FSMContext

from project.tg_bot.blank.client import get_cached_rus_client_tg_bot_blank
from project.tg_bot.const import ClientTgBotCommands
from project.tg_bot.filter_.message_text import MessageTextTgBotFilter
from project.tg_bot.kb.inline_.client.support import support_client_inline_kb_tg_bot
from project.tg_bot.middleware.common import MiddlewareDataTgBot

tg_bot_router = Router()
_logger = logging.getLogger(__name__)


@tg_bot_router.message(
    or_f(
        Command(ClientTgBotCommands.support),
        MessageTextTgBotFilter([
            ClientTgBotCommands.support,
            "поддержка"
        ], ignore_case=True)
    )
)
async def _(
        m: aiogram.types.Message,
        state: FSMContext,
        middleware_data_tg_bot: MiddlewareDataTgBot,
        **kwargs
):
    await state.clear()
    await m.answer(
        text=get_cached_rus_client_tg_bot_blank().support(),
        reply_markup=support_client_inline_kb_tg_bot()
    )
