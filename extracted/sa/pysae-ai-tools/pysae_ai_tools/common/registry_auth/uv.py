"""Pose the credential for the Python ecosystem — uv and pip.

``uv auth login`` writes uv's default credential store, which pip also benefits
from when the index is reached through uv. The credential is registered against
the **host root**: uv matches stored credentials by URL prefix, so one entry
covers every GitLab PyPI index below it (project- or group-scoped) while a
request to a public index finds nothing.

Unlike Docker, the token cannot be piped: ``uv auth login`` requires
``--token`` (or ``--password``) as an argument and errors out without one, so it
is briefly visible in this process's argv. Accepted for this ecosystem — the
credential is read-only on the registries, and uv owns the store format, which
we would otherwise have to reproduce by hand.
"""

import subprocess
import tomllib
from pathlib import Path

from .consumer import ApplyResult, ConsumerState, RegistryConsumer
from .targets import RegistryTargets

_STORE_FILE = "credentials.toml"


def _run_uv(*args: str, timeout: int = 60) -> subprocess.CompletedProcess[str] | None:
    """Run ``uv <args>``; ``None`` when uv is absent or the call times out."""
    try:
        return subprocess.run(
            ["uv", *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None


def credentials_store() -> Path | None:
    """Path of uv's credential store, as uv itself resolves it."""
    result = _run_uv("auth", "dir", timeout=15)
    if result is None or result.returncode != 0:
        return None
    directory = (result.stdout or "").strip()
    return Path(directory) / _STORE_FILE if directory else None


def _stored_services() -> tuple[str, ...]:
    """Services the store holds a credential for. Never returns any password."""
    store = credentials_store()
    if store is None or not store.exists():
        return ()
    try:
        data = tomllib.loads(store.read_text(encoding="utf-8", errors="replace"))
    except (OSError, tomllib.TOMLDecodeError):
        return ()
    entries = data.get("credential")
    if not isinstance(entries, list):
        return ()
    return tuple(
        str(entry["service"]) for entry in entries if isinstance(entry, dict) and isinstance(entry.get("service"), str)
    )


def _same_service(stored: str, wanted: str) -> bool:
    return stored.rstrip("/") == wanted.rstrip("/")


class PythonIndexConsumer(RegistryConsumer):
    name = "uv"

    def state(self, targets: RegistryTargets) -> ConsumerState:
        service = targets.python_service
        stored = any(_same_service(entry, service) for entry in _stored_services())
        store = credentials_store()
        return ConsumerState(
            name=self.name,
            configured=stored,
            locations=(str(store),) if stored and store is not None else (),
            detail="" if stored else "no credential registered for the GitLab host",
        )

    def apply(self, token: str, targets: RegistryTargets) -> ApplyResult:
        service = targets.python_service
        result = _run_uv("auth", "login", service, "--token", token)
        if result is None:
            return ApplyResult(error="uv is not installed or not in PATH")
        if result.returncode != 0:
            detail = (result.stderr or result.stdout or "").strip().splitlines()
            return ApplyResult(error=f"uv auth login failed: {detail[-1] if detail else 'unknown error'}")
        store = credentials_store()
        return ApplyResult(changed=True, locations=(str(store),) if store is not None else ())

    def remove(self, targets: RegistryTargets) -> tuple[str, ...]:
        service = targets.python_service
        if not any(_same_service(entry, service) for entry in _stored_services()):
            return ()
        result = _run_uv("auth", "logout", service, timeout=30)
        if result is None or result.returncode != 0:
            return ()
        store = credentials_store()
        return (str(store),) if store is not None else (service,)


consumer = PythonIndexConsumer()
