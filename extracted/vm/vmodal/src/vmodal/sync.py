from typing import List, Dict, Tuple, Optional, Any, Union
from dataclasses import dataclass
import os,sys
import asyncio
import fire
from vmodal.config import SdkConfig


class _SyncProxy:
    def __init__(self, client, prefix: str):
        self.client = client
        self.prefix = prefix

    def __getattr__(self, name: str):
        def runner(*args, **kw):
            return self.client._call(f"{self.prefix}.{name}", *args, **kw)
        return runner


class _SyncAuthProxy(_SyncProxy):
    def __call__(self) -> str:
        profile = self.client._call("auth.me")
        user_id = str(profile.user_id or "").strip()
        return f"VMODAL_API_KEY is valid, authenticated correctly (user_id={user_id})"


class SyncClient:
    def __init__(self, base_url: Union[str, SdkConfig] = "", user_id: str = "", tenant_id: str = "", email: str = "", token: str = "", timeout: float = 30, mode: str = "direct", cfg: Optional[SdkConfig] = None):
        if isinstance(base_url, SdkConfig):
            cfg = base_url
        self.cfg = cfg or SdkConfig(base_url=base_url, user_id=user_id, tenant_id=tenant_id, email=email, token=token, timeout=timeout, mode=mode)
        self.auth = _SyncAuthProxy(self, "auth")
        self.searches = _SyncProxy(self, "searches")
        self.collections = _SyncProxy(self, "collections")
        self.indexes = _SyncProxy(self, "indexes")
        self.admin = _SyncProxy(self, "admin")
        self.gdrive = _SyncProxy(self, "gdrive")
        self.sql = _SyncProxy(self, "sql")
        self.images = _SyncProxy(self, "images")
        self.r2 = _SyncProxy(self, "r2")

    @classmethod
    def from_env(cls, **kw):
        return cls(cfg=SdkConfig.from_env(**kw))

    def _call(self, target: str, *args, **kw):
        async def run_one():
            from vmodal import Client

            async with Client(cfg=self.cfg) as client:
                obj = client
                for part in target.split("."):
                    obj = getattr(obj, part)
                return await obj(*args, **kw)

        return asyncio.run(run_one())

    def health(self):
        return self._call("auth.health")

    def auth_check(self, user_id: str = ""):
        return self._call("auth.auth_check", user_id=user_id)

    def close(self):
        return None


if __name__ == "__main__":
    fire.Fire(SyncClient.from_env())
