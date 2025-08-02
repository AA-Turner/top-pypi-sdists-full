from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from project.tg_bot.blank.client import get_cached_rus_client_tg_bot_blank


def support_client_inline_kb_tg_bot() -> InlineKeyboardMarkup:
    return InlineKeyboardBuilder(markup=[
        [
            InlineKeyboardButton(
                text=get_cached_rus_client_tg_bot_blank().but_support(),
                url="https://t.me/arpakit"
            )
        ]
    ]).as_markup()
