import aiogram.filters
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from arpakitlib.ar_aiogram_util import as_tg_command
from project.tg_bot.callback_data_.common import BaseCD
from project.tg_bot.const import AdminTgBotCommands
from project.tg_bot.filter_.is_private_chat import IsPrivateChatTgBotFilter
from project.tg_bot.filter_.user_roles_has_admin import UserRolesHasAdminTgBotFilter
from project.tg_bot.middleware.common import MiddlewareDataTgBot

tg_bot_router = aiogram.Router()


class _CD(BaseCD, prefix=AdminTgBotCommands.kb_with_old_cd):
    pass


@tg_bot_router.message(
    IsPrivateChatTgBotFilter(),
    UserRolesHasAdminTgBotFilter(),
    aiogram.filters.Command(AdminTgBotCommands.kb_with_old_cd, ignore_case=True)
)
@as_tg_command()
async def _(
        m: aiogram.types.Message,
        state: FSMContext,
        middleware_data_tg_bot: MiddlewareDataTgBot,
        **kwargs
):
    await state.clear()
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(
        text="Button with old data",
        callback_data=_CD().pack()
    ))
    await m.answer(
        text="Old data",
        reply_markup=kb_builder.as_markup()
    )
