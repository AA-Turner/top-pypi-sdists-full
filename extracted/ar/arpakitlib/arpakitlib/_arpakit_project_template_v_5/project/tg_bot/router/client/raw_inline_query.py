import aiogram.filters
from aiogram.fsm.context import FSMContext

from project.tg_bot.middleware.common import MiddlewareDataTgBot

tg_bot_router = aiogram.Router()


@tg_bot_router.inline_query()
async def _(
        iq: aiogram.types.InlineQuery,
        state: FSMContext,
        middleware_data_tg_bot: MiddlewareDataTgBot,
        **kwargs
):
    pass
