from matrx_scraper.cache import TwoTierCache


def test_two_tier_cache_accepts_legacy_pool_wiring() -> None:
    cache = TwoTierCache(pool=object(), max_size=7, ttl_seconds=11)

    assert cache._memory.maxsize == 7
    assert cache._memory.ttl == 11
