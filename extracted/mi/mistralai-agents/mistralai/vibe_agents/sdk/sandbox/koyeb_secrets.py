"""Per-worker cache of Koyeb sandbox secrets.

A sandbox secret plus the sandbox URL is enough to run any command in the sandbox, and any
workspace member can read a Session's Workflow history. So the secret never travels through
Workflow payloads: the worker that creates a sandbox caches it, and any other worker looks it
up from Koyeb by service ID. Every activity reconnects to the sandbox and a lookup costs two to
three Koyeb API calls, hence the cache. A service's secret never changes, so entries only leave
when the sandbox is deleted or the cache is full.
"""

from typing import Protocol

from cachetools import LRUCache
from pydantic import SecretStr


class SandboxSecretMissingError(RuntimeError):
    """Koyeb returned a sandbox without its secret.

    koyeb-sdk 1.5.2 `get_from_id` logs and swallows a failed deployment read, then returns a
    sandbox whose secret is None. Every exec would then fail authentication, so callers fail the
    activity instead and let it retry.
    """


class KoyebSandboxWithSecret(Protocol):
    @property
    def service_id(self) -> str: ...

    @property
    def sandbox_secret(self) -> str | None: ...


_MAX_ENTRIES = 1024
_secrets: LRUCache[str, SecretStr] = LRUCache(maxsize=_MAX_ENTRIES)


def get(service_id: str) -> SecretStr | None:
    return _secrets.get(service_id)


def put(sandbox: KoyebSandboxWithSecret) -> SecretStr:
    """Cache the secret of a sandbox that was just created or looked up."""
    if not sandbox.sandbox_secret:
        raise SandboxSecretMissingError("Koyeb sandbox lookup returned no secret")
    secret = SecretStr(sandbox.sandbox_secret)
    _secrets[sandbox.service_id] = secret
    return secret


def evict(service_id: str) -> None:
    _secrets.pop(service_id, None)


def clear() -> None:
    _secrets.clear()
