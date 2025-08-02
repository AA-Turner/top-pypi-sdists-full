import aiogram.types
from aiogram.filters import Filter

from project.tg_bot.middleware.common import MiddlewareDataTgBot


class UserRolesHasAdminTgBotFilter(Filter):

    async def __call__(
            self,
            update: aiogram.types.Message | aiogram.types.CallbackQuery | aiogram.types.TelegramObject,
            middleware_data_tg_bot: MiddlewareDataTgBot,
            **kwargs
    ) -> bool:
        if middleware_data_tg_bot.current_user_dbm is not None:
            if middleware_data_tg_bot.current_user_dbm.roles_has_admin:
                return True
        return False
