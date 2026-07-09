from abc import ABC, abstractmethod
from typing import Optional
from urllib.parse import urlsplit, urlunsplit

import requests

from abstra_internals import environment
from abstra_internals.services.clamav import ScanResult, ScanVerdict
from abstra_internals.threaded import threaded
from abstra_internals.utils.env import is_dev_env, is_test_env


def _sanitize_url(url: Optional[str]) -> Optional[str]:
    """Drop query string and fragment before persisting a URL"""
    if not url:
        return url
    try:
        parts = urlsplit(url)
        return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))
    except Exception:
        return None


def _current_execution_id() -> Optional[str]:
    try:
        from abstra_internals.execution import get_execution_id

        return get_execution_id()
    except Exception:
        return None


class AuditEvent(ABC):
    """Base for a fire-and-forget audit event.

    Subclasses set :attr:`endpoint` (the path segment under ``/apps/audit/``) and
    implement :meth:`payload`. Override :meth:`should_emit` to skip in some states.
    """

    endpoint: str

    def should_emit(self) -> bool:
        return True

    @abstractmethod
    def payload(self) -> dict: ...

    @threaded
    def register(self) -> None:
        """Record this event in cloud-api. Spawns a thread and returns immediately, so
        nothing audit-related runs in the caller's thread; all errors are swallowed so
        auditing never affects the audited operation."""
        try:
            if not self.should_emit():
                return
            if is_test_env() or is_dev_env():
                return
            if (
                not environment.CLOUD_API_PROD_URL
                or not environment.CLOUD_API_PROD_SHARED_TOKEN
            ):
                return

            requests.post(
                f"{environment.CLOUD_API_PROD_URL}/audit/{self.endpoint}",
                headers=environment.CLOUD_API_PROD_HEADERS,
                json=self.payload(),
                timeout=environment.REQUEST_TIMEOUT,
            )
        except Exception:
            pass


class FileScanAuditEvent(AuditEvent):
    """One ClamAV scan of a downloaded file."""

    endpoint = "file-scan"

    def __init__(
        self,
        result: ScanResult,
        *,
        source_url: Optional[str] = None,
        filename: Optional[str] = None,
        file_size_bytes: Optional[int] = None,
        scan_duration_ms: Optional[int] = None,
    ):
        self.result = result
        self.source_url = source_url
        self.filename = filename
        self.file_size_bytes = file_size_bytes
        self.scan_duration_ms = scan_duration_ms
        self.execution_id = _current_execution_id()

    def should_emit(self) -> bool:
        return self.result.verdict is not ScanVerdict.SKIPPED

    def payload(self) -> dict:
        return {
            "executionId": self.execution_id,
            "verdict": self.result.verdict.value,
            "engine": self.result.engine.value,
            "signature": self.result.signature,
            "fileSizeBytes": self.file_size_bytes,
            "filename": self.filename,
            "sourceUrl": _sanitize_url(self.source_url),
            "scanDurationMs": self.scan_duration_ms,
            "environment": "editor"
            if environment.EDITOR_MODE == "web"
            else "production",
        }
