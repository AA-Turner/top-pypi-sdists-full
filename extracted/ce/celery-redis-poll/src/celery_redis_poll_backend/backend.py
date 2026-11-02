from celery.backends.redis import RedisBackend
from typing import Any
import celery
from celery_redis_cluster_backend import RedisClusterBackend


def choose_backend(scheme, *args, **kwargs):
    url = kwargs.get("url", "")

    def patch_url(additional):
        nonlocal url
        kwargs["url"] = url.replace(additional, scheme, 1)

    if url.startswith("poll"):
        patch_url("poll")
        return PollingRedisBackend(*args, **kwargs)
    elif url.startswith("cluster_poll"):
        patch_url("cluster_poll")
        return PollingRedisClusterBackend(*args, **kwargs)
    else:
        return RedisBackend(*args, **kwargs)


def choose_redis_backend(*args, **kwargs):
    return choose_backend("redis", *args, **kwargs)


def choose_rediss_backend(*args, **kwargs):
    return choose_backend("rediss", *args, **kwargs)


class PollingRedisBackend(celery.backends.base.SyncBackendMixin, RedisBackend):
    """
    Disables pub/sub for getting task results and instead uses polling.
    """

    def _set(self, key: str, value: str) -> None:
        """
        Simply set value in Redis, do not publish.
        :param key:
        :param value:
        :return:
        """
        if self.expires:
            self.client.setex(key, self.expires, value)
        else:
            self.client.set(key, value)

    def on_task_call(self, *args: Any, **kwargs: Any) -> None:
        pass


class PollingRedisClusterBackend(PollingRedisBackend, RedisClusterBackend):
    """
    Same as PollingRedisBackend but with ReidsCluster for client.
    """

    pass
