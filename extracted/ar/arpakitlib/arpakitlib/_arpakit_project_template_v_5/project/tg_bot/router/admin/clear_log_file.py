import aiogram
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from arpakitlib.ar_aiogram_util import as_tg_command
from project.core.settings import get_cached_settings
from project.tg_bot.blank.admin import get_cached_eng_admin_tg_bot_blank
from project.tg_bot.const import AdminTgBotCommands
from project.tg_bot.filter_.is_private_chat import IsPrivateChatTgBotFilter
from project.tg_bot.filter_.user_roles_has_admin import UserRolesHasAdminTgBotFilter
from project.tg_bot.middleware.common import MiddlewareDataTgBot

tg_bot_router = Router()


@tg_bot_router.message(
    IsPrivateChatTgBotFilter(),
    UserRolesHasAdminTgBotFilter(),
    aiogram.filters.Command(AdminTgBotCommands.clear_log_file)
)
@as_tg_command(passwd_validator=get_cached_settings().tg_bot_command_passwd)
async def _(
        m: types.Message,
        state: FSMContext,
        middleware_data_tg_bot: MiddlewareDataTgBot,
        **kwargs
):
    await state.clear()

    with open(get_cached_settings().log_filepath, mode="r") as f:
        if not f.read():
            await m.answer(get_cached_eng_admin_tg_bot_blank().good())
            return

    with open(get_cached_settings().log_filepath, mode="w") as f:
        f.write("")

    await m.answer(get_cached_eng_admin_tg_bot_blank().good())
