"""S2 browser-worker runtime and its in-process control-plane stub.

Public surface:
  * ``BrowserWorker`` — the runtime; drive it through the eight S2 operations.
  * ``StubControlPlane`` — the in-process Browser Manager stand-in for tests.
  * ``InMemoryTokenAuthority`` — the stub's token issuer + verifier.
  * ``models`` / ``commands`` — the typed S2 wire contract (imported, never re-declared).
"""

from __future__ import annotations

from matrx_scraper.cloud_browser.worker.auth import (
    InMemoryTokenAuthority,
    TokenVerifier,
    WorkerCredential,
)
from matrx_scraper.cloud_browser.worker.errors import (
    WorkerError,
    WorkerProtocolError,
    http_status_for,
    retryable_for,
)
from matrx_scraper.cloud_browser.worker.profile_lock import ProfileLock, ProfileLockError
from matrx_scraper.cloud_browser.worker.runtime import WORKER_VERSION, BrowserWorker
from matrx_scraper.cloud_browser.worker.stub_control_plane import StubControlPlane

__all__ = [
    "BrowserWorker",
    "InMemoryTokenAuthority",
    "ProfileLock",
    "ProfileLockError",
    "StubControlPlane",
    "TokenVerifier",
    "WORKER_VERSION",
    "WorkerCredential",
    "WorkerError",
    "WorkerProtocolError",
    "http_status_for",
    "retryable_for",
]
