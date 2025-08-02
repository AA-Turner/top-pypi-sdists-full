import aiogram.filters
from aiogram.fsm.context import FSMContext

from project.tg_bot.blank.client import get_cached_rus_client_tg_bot_blank
from project.tg_bot.middleware.common import MiddlewareDataTgBot

tg_bot_router = aiogram.Router()


@tg_bot_router.message()
async def _(
        m: aiogram.types.Message,
        state: FSMContext,
        middleware_data_tg_bot: MiddlewareDataTgBot,
        **kwargs
):
    await state.clear()
    await m.answer(text=get_cached_rus_client_tg_bot_blank().raw_message())
