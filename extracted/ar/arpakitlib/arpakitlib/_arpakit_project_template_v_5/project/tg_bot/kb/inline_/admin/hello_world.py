from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from project.tg_bot.blank.admin import get_cached_eng_admin_tg_bot_blank
from project.tg_bot.callback_data_.admin import HelloWorldAdminCD


def hello_world_admin_inline_kb_tg_bot() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(
        text=get_cached_eng_admin_tg_bot_blank().but_hello_world(),
        callback_data=HelloWorldAdminCD(hello_world=True).pack()
    ))

    return kb_builder.as_markup()
