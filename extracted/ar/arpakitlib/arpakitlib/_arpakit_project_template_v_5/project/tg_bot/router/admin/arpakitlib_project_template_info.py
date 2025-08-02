import aiogram.filters
from aiogram.fsm.context import FSMContext

from arpakitlib.ar_aiogram_util import as_tg_command
from arpakitlib.ar_json_util import transfer_data_to_json_str
from project.tg_bot.const import AdminTgBotCommands
from project.tg_bot.filter_.is_private_chat import IsPrivateChatTgBotFilter
from project.tg_bot.filter_.user_roles_has_admin import UserRolesHasAdminTgBotFilter
from project.tg_bot.middleware.common import MiddlewareDataTgBot
from project.util.arpakitlib_project_template_util import get_arpakitlib_project_template_info

tg_bot_router = aiogram.Router()


@tg_bot_router.message(
    IsPrivateChatTgBotFilter(),
    UserRolesHasAdminTgBotFilter(),
    aiogram.filters.Command(AdminTgBotCommands.arpakitlib_project_template_info)
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
        text=transfer_data_to_json_str(get_arpakitlib_project_template_info(), beautify=True)
    )
