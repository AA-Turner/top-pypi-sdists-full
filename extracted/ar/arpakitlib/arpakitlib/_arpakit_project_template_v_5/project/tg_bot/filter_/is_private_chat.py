import aiogram.types
from aiogram.filters import Filter


class IsPrivateChatTgBotFilter(Filter):
    async def __call__(self, update: aiogram.types.Message | aiogram.types.CallbackQuery) -> bool:
        if isinstance(update, aiogram.types.Message):
            return update.chat.type == aiogram.enums.ChatType.PRIVATE
        elif isinstance(update, aiogram.types.CallbackQuery):
            return update.message.chat.type == aiogram.enums.ChatType.PRIVATE
        else:
            return False
