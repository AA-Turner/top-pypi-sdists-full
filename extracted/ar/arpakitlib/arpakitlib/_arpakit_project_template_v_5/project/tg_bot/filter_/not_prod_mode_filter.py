from aiogram.filters import Filter

from project.core.settings import get_cached_settings


class NotProdModeTgBotFilter(Filter):
    async def __call__(self, *args, **kwargs) -> bool:
        return not get_cached_settings().prod_mode
