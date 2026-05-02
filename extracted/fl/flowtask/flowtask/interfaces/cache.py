from abc import ABC
from collections.abc import Callable
import redis
from redis import asyncio as aioredis
from redis.exceptions import RedisError, ResponseError, ReadOnlyError
from navconfig.logging import logging
from ..exceptions import FlowTaskError
from ..conf import REDIS_URL


class CacheSupport(ABC):
    """
    Very Basic Cache Support using Redis
    """

    params: dict = {
        "encoding": "utf-8",
        "decode_responses": True,
        "max_connections": 10,
    }

    def __init__(self, *args, **kwargs):
        self.redis_url = kwargs.get('redis_url', REDIS_URL)
        self._redis: Callable = None
        self.expiration = self.parse_duration(kwargs.pop("every", "60m"))
        super().__init__(
            *args, **kwargs
        )

    async def __aenter__(self):
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    def parse_duration(self, duration: str) -> int:
        """
        Parse a duration string and return its value in seconds.

        Supported formats:
        - "Xs" for seconds
        - "Xm" for minutes
        - "Xh" for hours
        """
        if duration is None:
            return None
        value = int(duration[:-1])
        unit = duration[-1]

        if unit == "s":
            return value
        elif unit == "m":
            return value * 60
        elif unit == "h":
            return value * 3600
        else:
            raise ValueError(f"Unsupported duration unit: {unit}")

    def set(self, key, value):
        try:
            return self._redis.set(key, value)
        except ReadOnlyError as err:
            raise FlowTaskError(f"Redis is Read Only: {err}") from err
        except Exception as err:
            raise FlowTaskError(f"Redis Error: {err}") from err

    def delete(self, key: str) -> None:
        try:
            self._redis.delete(key)
        except RedisError as err:
            raise FlowTaskError(f"Error deleting key {key}: {err}") from err

    def exists(self, key, *keys):
        try:
            return bool(self._redis.exists(key, *keys))
        except ResponseError as err:
            raise FlowTaskError(f"Bad Response: {err}") from err
        except RedisError as err:
            raise FlowTaskError(f"Redis Error: {err}") from err
        except Exception as err:
            raise FlowTaskError(f"Redis Exception: {err}") from err

    def get(self, key):
        try:
            return self._redis.get(key)
        except ResponseError as err:
            raise FlowTaskError(f"Bad Response: {err}") from err
        except RedisError as err:
            raise FlowTaskError(f"Redis Error: {err}") from err
        except Exception as err:
            raise FlowTaskError(f"Redis Exception: {err}") from err

    def setexp(self, key, value, timeout: str = None):
        """
        setexp
           Set the value and expiration of a Key
           params:
            key: key Name
            value: value of the key
            timeout: expiration time in seconds
        """
        if timeout is None:
            timeout = self.expiration
        elif isinstance(timeout, str):
            timeout = self.parse_duration(timeout)
        else:
            try:
                timeout = self.parse_duration(timeout)
            except TypeError:
                timeout = self.expiration
        if timeout is None:
            return
        try:
            logging.debug(
                f"Cache: Set Cache {key} with expiration {timeout} secs"
            )
            self._redis.setex(key, timeout, value)
        except ReadOnlyError as err:
            raise FlowTaskError(f"Redis is Read Only: {err}") from err
        except ResponseError as err:
            raise FlowTaskError(f"Bad Response: {err}") from err
        except RedisError as err:
            raise FlowTaskError(f"Redis Error: {err}") from err
        except Exception as err:
            raise FlowTaskError(f"Unknown Redis Error: {err}") from err

    async def setex(self, key, value, timeout: str = None):
        """
        setex
           Set the value and expiration of a Key
           params:
            key: key Name
            value: value of the key
            timeout: expiration time in seconds
        """
        if timeout is None:
            timeout = self.expiration
        elif isinstance(timeout, str):
            timeout = self.parse_duration(timeout)
        else:
            try:
                timeout = self.parse_duration(timeout)
            except TypeError:
                timeout = self.expiration
        if timeout is None:
            return
        try:
            logging.debug(
                f"Cache: Set Cache {key} with expiration {timeout} secs"
            )
            await self._redis.setex(key, timeout, value)
        except ReadOnlyError as err:
            raise FlowTaskError(f"Redis is Read Only: {err}") from err
        except ResponseError as err:
            raise FlowTaskError(f"Bad Response: {err}") from err
        except RedisError as err:
            raise FlowTaskError(f"Redis Error: {err}") from err
        except Exception as err:
            raise FlowTaskError(f"Unknown Redis Error: {err}") from err

    async def open(self, url: str = None):
        if not url:
            url = self.redis_url
        self._redis = await aioredis.from_url(
            url, encoding="utf-8", decode_responses=True
        )
        return self

    async def close(self):
        try:
            await self._redis.close()
            await self._redis.connection_pool.disconnect()
        except Exception:
            pass

    def connect(self):
        try:
            self._redis = redis.from_url(url=self.redis_url, **self.params)
        except TimeoutError as err:
            raise FlowTaskError(f"Redis Config: Redis Timeout: {err}") from err
        except (RedisError, ConnectionError) as err:
            raise FlowTaskError(
                f"Redis Config: Unable to connect to Redis: {err}"
            ) from err
        except Exception as err:
            logging.exception(err)
            raise FlowTaskError(f"Redis Error: {err}") from err

    def disconnect(self):
        try:
            self._redis.close()
        except Exception as err:  # pylint: disable=W0703
            logging.error(err)
