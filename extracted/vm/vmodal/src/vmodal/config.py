from typing import List, Dict, Tuple, Optional, Any, Union
from dataclasses import dataclass
import os,sys
import fire


# Current hosted public gateway. The hostname is retained for compatibility
# across the Python, Go, Android, and MCP clients.
PUBLIC_GATEWAY_URL = "https://searchapi-test.v-modal.com"
DEV_GATEWAY_URL = "http://127.0.0.1:3099"


def str_gateway_base_url(base_url: str, mode: str = "") -> str:
    base = str(base_url or "").strip().rstrip("/")
    mode = str(mode or "").strip().lower()
    if not base or mode != "gateway":
        return base
    suffix = "/api/v1/proxy/search_api"
    if base.endswith(suffix):
        return base
    return base + suffix


def str_users_base_url(base_url: str) -> str:
    base = str(base_url or "").strip().rstrip("/")
    suffix = "/api/v1/proxy/search_api"
    if base.endswith(suffix):
        return base[: -len(suffix)]
    return base


@dataclass
class SdkConfig:
    base_url: str
    user_id: str
    tenant_id: str = ""
    email: str = ""
    token: str = ""
    timeout: float = 30
    mode: str = "direct"
    max_retries: int = 1

    def __post_init__(self):
        self.mode = str(self.mode or "direct").strip() or "direct"
        self.base_url = str_gateway_base_url(self.base_url, self.mode)
        self.user_id = str(self.user_id or "").strip()
        self.tenant_id = str(self.tenant_id or "").strip()
        self.email = str(self.email or "").strip()
        self.token = str(self.token or "").strip()
        self.timeout = float(self.timeout or 30)
        self.max_retries = max(0, int(self.max_retries))

    def resolve_identity(self, refresh: bool = False) -> Dict:
        """Resolve and cache identity fields through ``/api/v1/auth/me``."""
        from vmodal.utils_userid import get_save_userinfo

        if self.user_id and not refresh:
            return {"user_id": self.user_id, "tenant_id": self.tenant_id, "email": self.email}
        info = get_save_userinfo(self.token, self.base_url, refresh=refresh)
        self.user_id = str(info.get("user_id", "") or "").strip()
        self.tenant_id = str(info.get("tenant_id", "") or "").strip()
        self.email = str(info.get("email", "") or "").strip()
        return info

    def resolve_user_id(self, refresh: bool = False) -> str:
        """Resolve and cache the token owner through ``/api/v1/auth/me``."""
        self.resolve_identity(refresh=refresh)
        return self.user_id

    @classmethod
    def from_env(cls, **kw):
        resolve_identity = bool(kw.pop("resolve_identity", True))
        env_arg = str(kw.pop("env", "") or "").strip().lower()
        env_raw = str(os.environ.get("VMODAL_ENV", "") or "").strip().lower()
        private = bool(env_arg or env_raw)
        env = env_arg or env_raw or "prd"
        if env not in ("dev", "prd"):
            raise ValueError("VMODAL_ENV must be dev or prd")
        env_url = DEV_GATEWAY_URL if env == "dev" else PUBLIC_GATEWAY_URL
        base_url = env_url
        token = os.environ.get("VMODAL_API_KEY", "")
        timeout = 30
        max_retries = 1
        if private:
            base_url = os.environ.get("VMODAL_BASE_URL", "") or os.environ.get("TEST_CLIENT_SERVER_API_URL", "") or env_url
            token = (
                token
                or os.environ.get("VMODAL_API_TOKEN", "")
                or os.environ.get("TEST_CLIENT_CLERK_USER_API_TOKEN", "")
                or os.environ.get("TEST_CLIENT_USER_TOKEN", "")
            )
            timeout = float(os.environ.get("VMODAL_TIMEOUT", "30") or 30)
            max_retries = int(os.environ.get("VMODAL_MAX_RETRIES", "1") or 1)
        data = {
            "base_url": base_url,
            "user_id": "",
            "tenant_id": "",
            "email": "",
            "token": token,
            "timeout": timeout,
            "mode": "gateway",
            "max_retries": max_retries,
        }
        data.update(kw)
        cfg = cls(**data)
        if not cfg.token:
            raise ValueError("VMODAL_API_KEY is required")
        if resolve_identity:
            cfg.resolve_identity()
        return cfg


if __name__ == "__main__":
    fire.Fire(SdkConfig)
