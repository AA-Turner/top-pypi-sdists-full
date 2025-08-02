import aiogram
from aiogram.fsm.storage.memory import MemoryStorage

from project.tg_bot.event import add_events_to_tg_bot_dispatcher
from project.tg_bot.middleware.uil import register_middlewares_to_tg_bot
from project.tg_bot.router.main_router import main_tg_bot_router


def create_tg_bot_dispatcher() -> aiogram.Dispatcher:
    tg_bot_dispatcher = aiogram.Dispatcher(
        storage=MemoryStorage(),
    )

    add_events_to_tg_bot_dispatcher(tg_bot_dispatcher=tg_bot_dispatcher)

    register_middlewares_to_tg_bot(tg_bot_dispatcher=tg_bot_dispatcher)

    tg_bot_dispatcher.include_router(router=main_tg_bot_router)

    return tg_bot_dispatcher
