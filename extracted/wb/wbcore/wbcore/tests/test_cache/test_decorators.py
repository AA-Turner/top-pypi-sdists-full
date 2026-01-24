import pytest

from wbcore.cache.decorators import cache_table
from wbcore.cache.registry import periodic_cache_registry


@pytest.mark.parametrize(
    "timeout, key_prefix, periodic_caching_view_kwargs, periodic_caching_get_parameters",
    [(2, "Foo", [{"a": "a"}], [{"b": "b"}])],
)
def test_cache_table(timeout, key_prefix, periodic_caching_view_kwargs, periodic_caching_get_parameters):
    @cache_table(
        timeout=timeout,
        key_prefix=key_prefix,
        periodic_caching=True,
        periodic_caching_view_kwargs=periodic_caching_view_kwargs,
        periodic_caching_get_parameters=periodic_caching_get_parameters,
    )
    class CacheTable:
        pass

    assert CacheTable.CACHE_ENABLED is True
    assert CacheTable.CACHE_TIMEOUT == timeout
    assert CacheTable.CACHE_KEY_PREFIX == key_prefix
    cache_entry = periodic_cache_registry.classes[0]
    assert cache_entry.view_class == CacheTable
    assert cache_entry.view_kwargs == periodic_caching_view_kwargs
    assert cache_entry.get_parameters == periodic_caching_get_parameters
