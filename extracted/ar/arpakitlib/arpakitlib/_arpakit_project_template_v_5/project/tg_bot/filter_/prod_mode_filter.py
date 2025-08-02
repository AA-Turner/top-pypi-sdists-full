from aiogram.filters import Filter

from project.core.settings import get_cached_settings


class ProdModeTgBotFilter(Filter):
    async def __call__(self, *args, **kwargs) -> bool:
        return get_cached_settings().prod_mode
