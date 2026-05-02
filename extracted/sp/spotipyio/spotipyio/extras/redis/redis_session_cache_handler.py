import json
from typing import Optional, Dict

from redis import Redis

from spotipyio.auth import ISessionCacheHandler


class RedisSessionCacheHandler(ISessionCacheHandler):
    def __init__(self, key: str, redis: Redis):
        self._key = key
        self._redis = redis

    def get(self) -> Optional[Dict[str, str]]:
        encoded_response = self._redis.get(self._key)

        if encoded_response is not None:
            return json.loads(encoded_response)

    def set(self, response: Dict[str, str]) -> None:
        encoded_response = json.dumps(response)
        self._redis.set(name=self._key, value=encoded_response)
