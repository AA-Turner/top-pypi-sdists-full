from typing import List, Dict, Tuple, Optional, Any, Union
from dataclasses import dataclass
import os,sys
import fire
from vmodal.config import SdkConfig
from vmodal.http import Http
from vmodal.resources import AuthResource, SearchesResource, CollectionsResource, IndexesResource, AdminResource, GDriveResource, SqlResource, ImagesResource, R2Resource
from vmodal.sync import SyncClient

__version__ = "1.0.0"


class Client:
    def __init__(self, base_url: Union[str, SdkConfig] = "", user_id: str = "", tenant_id: str = "", email: str = "", token: str = "", timeout: float = 30, mode: str = "direct", cfg: Optional[SdkConfig] = None):
        if isinstance(base_url, SdkConfig):
            cfg = base_url
        cfg = cfg or SdkConfig(base_url=base_url, user_id=user_id, tenant_id=tenant_id, email=email, token=token, timeout=timeout, mode=mode)
        self.cfg = cfg
        self.http = Http(cfg)
        self.auth = AuthResource(self.http)
        self.searches = SearchesResource(self.http)
        self.collections = CollectionsResource(self.http)
        self.indexes = IndexesResource(self.http)
        self.admin = AdminResource(self.http)
        self.gdrive = GDriveResource(self.http)
        self.sql = SqlResource(self.http)
        self.images = ImagesResource(self.http)
        self.r2 = R2Resource(self.http)

    @classmethod
    def from_env(cls, **kw):
        return cls(cfg=SdkConfig.from_env(**kw))

    async def health(self):
        return await self.auth.health()

    async def auth_check(self, user_id: str = ""):
        return await self.auth.auth_check(user_id=user_id)

    async def aclose(self):
        await self.http.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.aclose()


__all__ = ["Client", "SyncClient", "SdkConfig", "__version__"]


if __name__ == "__main__":
    fire.Fire()
