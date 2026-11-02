from ..base_models.singleton import SingletonMeta
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import os
import atexit

class MongoConnection(metaclass=SingletonMeta):
    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        uri_base: Optional[str] = None,
        instance: Optional[str] = None,
        max_pool_size: Optional[int] = None,
        max_idle_time_ms: Optional[int] = None,
    ):
        self.username = username or os.getenv('MONGO_USERNAME')
        self.password = password or os.getenv('MONGO_PASSWORD')
        self.uri_base = uri_base or os.getenv('MONGO_URI_BASE')
        self.instance = instance or os.getenv('MONGO_INSTANCE_COMPONENT')
        self.max_pool_size = max_pool_size
        self.max_idle_time_ms = max_idle_time_ms

        if not all([self.username, self.password, self.uri_base, self.instance]):
            raise ValueError("Missing required MongoDB connection parameters")

        client_kwargs: dict = {}
        uri = f"{self.uri_base}://{self.username}:{self.password}@{self.instance}.mongodb.net"
        client_kwargs: dict = {}
        if max_pool_size is not None:
            client_kwargs["maxPoolSize"] = max_pool_size
        if max_idle_time_ms is not None:
            client_kwargs["maxIdleTimeMS"] = max_idle_time_ms

        self.client = AsyncIOMotorClient(uri, **client_kwargs)
        atexit.register(self.close)

    async def ping(self) -> bool:
        try:
            await self.client.admin.command('ping')
            return True
        except Exception:
            return False

    def close(self) -> None:
        if hasattr(self, 'client'):
            self.client.close()
