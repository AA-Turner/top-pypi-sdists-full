import aiogram
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from arpakitlib.ar_aiogram_util import as_tg_command
from project.tg_bot.blank.admin import get_cached_eng_admin_tg_bot_blank
from project.tg_bot.const import AdminTgBotCommands
from project.tg_bot.filter_.is_private_chat import IsPrivateChatTgBotFilter
from project.tg_bot.filter_.user_roles_has_admin import UserRolesHasAdminTgBotFilter
from project.tg_bot.middleware.common import MiddlewareDataTgBot

tg_bot_router = Router()


class _CD(CallbackData, prefix=AdminTgBotCommands.kb_with_not_modified):
    pass


@tg_bot_router.message(
    IsPrivateChatTgBotFilter(),
    UserRolesHasAdminTgBotFilter(),
    aiogram.filters.Command(AdminTgBotCommands.kb_with_not_modified, ignore_case=True)
)
@as_tg_command()
async def _(
        m: types.Message,
        state: FSMContext,
        middleware_data_tg_bot: MiddlewareDataTgBot,
        **kwargs
):
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(
        text="Button raises Not Modified",
        callback_data=_CD().pack()
    ))
    await m.answer(
        text=get_cached_eng_admin_tg_bot_blank().good(),
        reply_markup=kb_builder.as_markup()
    )


@tg_bot_router.callback_query(
    IsPrivateChatTgBotFilter(),
    UserRolesHasAdminTgBotFilter(),
    _CD.filter()
)
async def _(
        cq: types.CallbackQuery,
        state: FSMContext,
        middleware_data_tg_bot: MiddlewareDataTgBot,
        **kwargs
):
    await state.clear()
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(
        text="Button raises Not Modified",
        callback_data=_CD().pack()
    ))
    await cq.message.edit_text(
        text=get_cached_eng_admin_tg_bot_blank().good(),
        reply_markup=kb_builder.as_markup()
    )
