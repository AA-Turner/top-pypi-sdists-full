from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from project.tg_bot.blank.admin import get_cached_eng_admin_tg_bot_blank


def hello_world_admin_static_kb_tg_bot() -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()

    kb_builder.row(KeyboardButton(
        text=get_cached_eng_admin_tg_bot_blank().but_hello_world()
    ))

    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=False)
