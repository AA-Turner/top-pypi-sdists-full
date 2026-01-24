from typing import Callable

from django.conf import settings

from ..signals.instance_buttons import add_extra_button
from .buttons import add_clear_cache_button
from .registry import periodic_cache_registry


def cache_table(
    timeout: int | Callable | None = None,
    key_prefix: str | Callable | None = None,
    periodic_caching: bool = False,
    periodic_caching_view_kwargs: list[dict[str, str]] | Callable | None = None,
    periodic_caching_get_parameters: list[dict[str, str]] | Callable | None = None,
):
    def _decorator(pandas_view_class):
        pandas_view_class.CACHE_ENABLED = not settings.DEBUG
        pandas_view_class.CACHE_TIMEOUT = timeout
        pandas_view_class.CACHE_KEY_PREFIX = key_prefix
        add_extra_button.connect(add_clear_cache_button, sender=pandas_view_class, weak=False)

        if periodic_caching:
            periodic_cache_registry.add(
                pandas_view_class,
                view_kwargs=periodic_caching_view_kwargs,
                get_parameters=periodic_caching_get_parameters,
            )
        return pandas_view_class

    return _decorator
