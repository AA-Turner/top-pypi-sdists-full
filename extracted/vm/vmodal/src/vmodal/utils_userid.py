"""User id / token helpers for the vmodal SDK.

Resolves the auth token (ENV VMODAL_API_KEY or test compatibility aliases,
else VMODAL_AUTH_CACHE_DIR/token) and the user id
(cached encrypted in VMODAL_AUTH_CACHE_DIR/user_info, else fetched from /api/v1/auth/me).
The default is the operating system's per-user cache directory.
"""
from typing import List, Dict, Tuple, Optional, Any, Union
from dataclasses import dataclass
import os, sys, json, base64, hashlib, time
import fire
from cryptography.fernet import Fernet

CACHE_TTL_SECONDS = 5 * 24 * 3600  # 5 days

def os_cache_dir() -> str:
    """Return the platform user-cache directory for vmodal."""
    custom = str(os.environ.get("VMODAL_AUTH_CACHE_DIR", "")).strip()
    if custom:
        return os.path.expanduser(custom)
    if sys.platform == "darwin":
        return os.path.expanduser("~/Library/Caches/vmodal")
    if os.name == "nt":
        base = os.environ.get("LOCALAPPDATA", "") or os.path.expanduser("~")
        return os.path.join(base, "vmodal", "Cache")
    base = os.environ.get("XDG_CACHE_HOME", "") or os.path.expanduser("~/.cache")
    return os.path.join(base, "vmodal")


DIR_VMODAL = os_cache_dir()
TOKEN_FILE = os.path.join(DIR_VMODAL, "token")
INFO_FILE  = os.path.join(DIR_VMODAL, "user_info")
AUTH_PATH  = "/api/v1/auth/me"


def get_token() -> str:
    """Return token from ENV, else from the platform cache token file."""
    tok = str(os.environ.get("VMODAL_API_KEY", "") or "").strip()
    if not tok and os.environ.get("VMODAL_ENV", "").strip():
        tok = str(
            os.environ.get("VMODAL_API_TOKEN", "")
            or os.environ.get("TEST_CLIENT_CLERK_USER_API_TOKEN", "")
            or os.environ.get("TEST_CLIENT_USER_TOKEN", "")
            or ""
        ).strip()
    if tok:
        return tok
    if os.path.isfile(TOKEN_FILE):
        with open(TOKEN_FILE) as f:
            tok = f.read().strip()
    return tok


def _fernet(token: str):
    """Fernet cipher keyed by sha256(token) as a urlsafe base64 key."""
    key = base64.urlsafe_b64encode(hashlib.sha256(token.encode()).digest())
    return Fernet(key)


def _info_save(info: Dict, token: str) -> None:
    """Encrypt user info json with the token-derived key into INFO_FILE."""
    os.makedirs(DIR_VMODAL, exist_ok=True)
    payload = dict(info)
    payload["__saved_at__"] = time.time()
    blob = _fernet(token).encrypt(json.dumps(payload).encode())
    with open(INFO_FILE, "wb") as f:
        f.write(blob if isinstance(blob, bytes) else blob.encode())


def _info_load(token: str) -> Optional[Dict]:
    """Decrypt INFO_FILE with the token-derived key; None on miss/wrong token/expired TTL."""
    if not os.path.isfile(INFO_FILE):
        return None
    try:
        with open(INFO_FILE, "rb") as f:
            raw = f.read()
        data = _fernet(token).decrypt(raw)
        info = json.loads(data.decode())
        if time.time() - info.get("__saved_at__", 0) > CACHE_TTL_SECONDS:
            return None
        return info
    except Exception:
        return None


def _fetch_me(token: str, base_url: str = "") -> Dict:
    """GET /api/v1/auth/me with Bearer token, return the user details json."""
    import httpx
    from vmodal.config import PUBLIC_GATEWAY_URL, str_users_base_url
    from vmodal.errors import AuthError
    base = str(
        base_url
        or os.environ.get("VMODAL_BASE_URL", "")
        or os.environ.get("TEST_CLIENT_SERVER_API_URL", "")
        or PUBLIC_GATEWAY_URL
    ).strip().rstrip("/")
    base = str_users_base_url(base)
    url = base + AUTH_PATH
    res = httpx.get(url, headers={"Authorization": "Bearer " + token}, timeout=30)
    if res.status_code in (401, 403):
        raise AuthError("API key authentication failed", status_code=res.status_code, body=res.text)
    res.raise_for_status()
    return res.json()


def get_save_userid(token: str = "", base_url: str = "", refresh: bool = False) -> str:
    """Return user id for a token, fetching+caching /auth/me on first call.

    Reads the encrypted platform-cache user_info; on miss queries /api/v1/auth/me,
    saves the json encrypted with the token-derived key, returns the user id.
    """
    return str(get_save_userinfo(token, base_url, refresh).get("user_id", "") or "")


def get_save_userinfo(token: str = "", base_url: str = "", refresh: bool = False) -> Dict:
    """Return the token identity, fetching and caching ``/auth/me`` on a miss."""
    token = str(token or "").strip() or get_token()
    if not token:
        raise ValueError("no token: set VMODAL_API_KEY or configure the vmodal token cache")

    info = None if refresh else _info_load(token)
    if not (info and info.get("user_id")):
        info = _fetch_me(token, base_url)
        _info_save(info, token)
    return info


if __name__ == "__main__":
    fire.Fire({"get_token": get_token, "get_save_userid": get_save_userid, "get_save_userinfo": get_save_userinfo})
