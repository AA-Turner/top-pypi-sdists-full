from configurations import values


class Cache:
    CACHE_REDIS_URL = values.Value(None, environ_prefix=None)
    CACHE_TIMEOUT = values.IntegerValue(
        10 * 24 * 3600, environ_prefix=None
    )  # The default (10 days) timeout in seconds

    @property
    def CACHES(self):  # noqa
        if self.CACHE_REDIS_URL:
            return {
                "default": {
                    "BACKEND": "django.core.cache.backends.redis.RedisCache",
                    "LOCATION": self.CACHE_REDIS_URL,
                    "TIMEOUT": self.CACHE_TIMEOUT,
                }
            }
        return {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache", "TIMEOUT": self.CACHE_TIMEOUT}}
