import os
import redis

from typing import Any

REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = int(os.environ["REDIS_PORT"])
REDIS_DB = int(os.getenv("REDIS_DB", 0))

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


def k(*parts: str) -> str:
    return ":".join(parts)


def get_redis(*args: str) -> Any:
    value = redis_client.get(k(*args))
    if value:
        return value.decode("utf-8")
    return None


def set_redis(*args) -> None:
    value = args[-1]
    redis_client.set(k(*args[:-1]), value)


if __name__ == "__main__":
    set_redis("ping", "pong")
    print(get_redis(("ping")))
