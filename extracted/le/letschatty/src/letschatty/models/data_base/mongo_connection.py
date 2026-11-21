from ..base_models.singleton import SingletonMeta
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import os
import atexit


def _pymongo_tiene_zstd() -> bool:
    """Si el pymongo instalado puede comprimir con zstd.

    Se le pregunta a pymongo y no a una librería: hasta 4.15 usa `zstandard` y desde 4.16
    `backports.zstd` (o `compression.zstd` en 3.14). Instalar la equivocada no da error: pymongo
    avisa con un warning y cae a zlib. La dependencia correcta es el extra `pymongo[zstd]`.
    """
    try:
        from pymongo.compression_support import _have_zstd
    except ImportError:
        return False
    return _have_zstd()


def compresores_de_mongo() -> dict:
    """Compresión del protocolo con Atlas, como kwargs del cliente.

    Atlas cobra cada GB que sale del cluster hacia nosotros (~USD 270/mes en sep-2026, casi todo
    lectura) y sin esto viaja en BSON crudo. Medido contra dev el 2026-11-20: zstd manda 9× menos
    bytes y zlib 5,5×. zstd primero porque también le cuesta menos CPU al cluster; si `zstandard`
    no está instalado, zlib (viene con Python), sin el warning de pymongo.
    `MONGO_COMPRESSORS` lo pisa sin deploy: vacío apaga la compresión.
    """
    configurado = os.getenv("MONGO_COMPRESSORS")
    if configurado is None:
        configurado = "zstd,zlib" if _pymongo_tiene_zstd() else "zlib"
    # "zstd, zlib" con espacio: pymongo descartaría " zlib" y quedaría sin compresión.
    configurado = ",".join(parte.strip() for parte in configurado.split(",") if parte.strip())
    return {"compressors": configurado} if configurado else {}


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

        uri = f"{self.uri_base}://{self.username}:{self.password}@{self.instance}.mongodb.net"
        client_kwargs: dict = compresores_de_mongo()
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
