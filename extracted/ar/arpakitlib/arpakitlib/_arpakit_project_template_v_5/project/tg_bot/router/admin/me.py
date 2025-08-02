import aiogram.filters
from aiogram.fsm.context import FSMContext

from arpakitlib.ar_aiogram_util import as_tg_command
from project.tg_bot.blank.admin import get_cached_eng_admin_tg_bot_blank
from project.tg_bot.const import AdminTgBotCommands
from project.tg_bot.filter_.is_private_chat import IsPrivateChatTgBotFilter
from project.tg_bot.filter_.user_roles_has_admin import UserRolesHasAdminTgBotFilter
from project.tg_bot.middleware.common import MiddlewareDataTgBot

tg_bot_router = aiogram.Router()


@tg_bot_router.message(
    IsPrivateChatTgBotFilter(),
    UserRolesHasAdminTgBotFilter(),
    aiogram.filters.Command(AdminTgBotCommands.me)
)
@as_tg_command()
async def _(
        m: aiogram.types.Message,
        state: FSMContext,
        middleware_data_tg_bot: MiddlewareDataTgBot,
        **kwargs
):
    await state.clear()
    await m.answer(
        text=get_cached_eng_admin_tg_bot_blank().user_dbm(user_dbm=middleware_data_tg_bot.current_user_dbm)
    )
