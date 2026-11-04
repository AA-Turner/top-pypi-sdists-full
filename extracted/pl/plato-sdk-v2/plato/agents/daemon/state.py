"""Daemon runtime state and filesystem layout."""

from __future__ import annotations

import hmac
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path


@dataclass
class DaemonContext:
    """Shared state handed to every service at registration time."""

    state_dir: Path
    token: str
    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    capabilities: list[str] = field(default_factory=list)
    # Set by the pool service's reclaim endpoint: once True, every /v1 call
    # except reclaim/handshake gets a typed RECLAIMED error so in-flight and
    # new callers see a semantic state instead of a dropped connection.
    reclaimed: bool = False

    @property
    def jobs_dir(self) -> Path:
        return self.state_dir / "jobs"

    def ensure_dirs(self) -> None:
        self.state_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.jobs_dir.mkdir(parents=True, exist_ok=True, mode=0o700)

    def token_matches(self, presented: str) -> bool:
        return hmac.compare_digest(self.token.encode(), presented.encode())


def read_token_file(path: Path) -> str:
    token = path.read_text().strip()
    if not token:
        raise ValueError(f"Token file {path} is empty")
    return token
