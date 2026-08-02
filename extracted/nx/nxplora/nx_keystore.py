"""nx_keystore.py — the NON-macOS secret-storage backend (Windows + Linux).

macOS keeps its native `security`/Keychain path INSIDE each caller (nx_channels,
nx_mcp_oauth, nx_key_pool) exactly as before — proven, and never migrated, so existing
installs are untouched and there is zero risk of losing a stored secret. Every caller
branches on sys.platform and only reaches THIS module off-darwin, where it uses the
`keyring` library (a hard dependency): Windows Credential Locker, Linux Secret Service.

Contract mirrors the macOS one — (account, service) -> value:
  · account = the namespace ("nx-channels" for channel/MCP secrets, "nx" for the key
    pool). In keyring terms this is the service_name.
  · service = the per-secret key (a connector slug, a pooled-key slot, …). In keyring
    terms this is the username.
Names are validated with the SAME allowlist the macOS path uses before anything touches
the OS (no injection, bounded length).

Fail-closed and honest: a headless Linux with no Secret Service backend makes keyring
raise; every function returns None / False rather than crashing the CLI, so the caller
simply reports the secret as absent — the same honest outcome as an empty Keychain.
"""
import re

# Same shape/limits as nx_channels._KC_NAME_RE and nx_key_pool._safe_keychain_name.
_NAME_RE = re.compile(r"^[A-Za-z0-9._-]{1,64}$")


def _ok(*names) -> bool:
    return all(bool(n) and bool(_NAME_RE.match(n)) for n in names)


def kr_get(account: str, service: str):
    """Read a secret. Returns the value, or None if absent / invalid / no backend."""
    if not _ok(account, service):
        return None
    try:
        import keyring
        v = keyring.get_password(account, service)
        return v.strip() if isinstance(v, str) and v.strip() else None
    except Exception:
        return None


def kr_set(account: str, service: str, value: str) -> bool:
    """Store a secret (create/update). Never logs the value. False on any failure."""
    if not _ok(account, service) or value is None:
        return False
    try:
        import keyring
        keyring.set_password(account, service, value)
        return True
    except Exception:
        return False


def kr_delete(account: str, service: str) -> bool:
    """Delete a secret. True if removed; False if absent / invalid / no backend."""
    if not _ok(account, service):
        return False
    try:
        import keyring
        keyring.delete_password(account, service)
        return True
    except Exception:
        return False
