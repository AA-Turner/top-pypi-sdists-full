"""Disk-backed cache for runtime sandbox tokens at ~/.dreadnode/runtimes.json."""

from __future__ import annotations

import contextlib
import json
import os
import tempfile
import typing as t
from datetime import UTC, datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse, urlunparse

from loguru import logger

_DEFAULT_PATH = Path.home() / ".dreadnode" / "runtimes.json"
_MAX_AGE = timedelta(days=7)


class RuntimeTokenCache:
    """Read/write runtime connection tokens, keyed by runtime ID."""

    def __init__(self, path: Path | None = None) -> None:
        self._path = path or _DEFAULT_PATH

    def get(self, runtime_id: str) -> dict[str, t.Any] | None:
        store = self._read()
        entry = store.get(runtime_id)
        if entry is None:
            return None

        cached_at = entry.get("cached_at")
        if cached_at:
            try:
                ts = datetime.fromisoformat(cached_at)
                if ts.tzinfo is None:
                    ts = ts.replace(tzinfo=UTC)
                if datetime.now(tz=UTC) - ts > _MAX_AGE:
                    self.remove(runtime_id)
                    return None
            except (ValueError, TypeError):
                pass

        return entry

    def put(
        self,
        runtime_id: str,
        *,
        sandbox_url: str,
        token: str,
        provider_sandbox_id: str,
    ) -> None:
        store = self._read()
        store[runtime_id] = {
            "sandbox_url": self._strip_path(sandbox_url),
            "token": token,
            "provider_sandbox_id": provider_sandbox_id,
            "cached_at": datetime.now(tz=UTC).isoformat(),
        }
        self._write(store)

    def remove(self, runtime_id: str) -> None:
        store = self._read()
        if runtime_id in store:
            del store[runtime_id]
            self._write(store)

    def _read(self) -> dict[str, t.Any]:
        if not self._path.exists():
            return {}
        try:
            return json.loads(self._path.read_text())
        except (json.JSONDecodeError, OSError):
            logger.warning("Corrupt runtime cache at {}, starting fresh", self._path)
            return {}

    def _write(self, store: dict[str, t.Any]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        # Atomic write: write to temp file, fsync, then rename
        fd, tmp_path = tempfile.mkstemp(dir=self._path.parent, suffix=".tmp")
        try:
            with os.fdopen(fd, "w") as f:
                json.dump(store, f, indent=2)
                f.flush()
                os.fsync(f.fileno())
            Path(tmp_path).chmod(0o600)
            Path(tmp_path).replace(self._path)
        except BaseException:
            with contextlib.suppress(OSError):
                Path(tmp_path).unlink()
            raise

    @staticmethod
    def _strip_path(url: str) -> str:
        parsed = urlparse(url)
        return urlunparse((parsed.scheme, parsed.netloc, "", "", "", ""))
