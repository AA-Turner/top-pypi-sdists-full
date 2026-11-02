"""Custom HTTP file-server backend.

Auto-configures from environment variables (or a matrx_utils settings object):

    FILE_SERVER_BASE_URL — required (e.g. https://files.myapp.com)
    FILE_SERVER_API_KEY  — required (sent as "Authorization: Bearer <key>")
    FILE_SERVER_TIMEOUT  — optional, seconds (default: 30)

Expected REST conventions on the server side:

    GET    /files/{path}         → 200 + raw bytes body
    PUT    /files/{path}         → 200/201 on success
    DELETE /files/{path}         → 200/204 on success
    GET    /files?prefix={p}     → 200 + JSON array of path strings
    GET    /files/{path}?url=1   → 200 + JSON {"url": "..."} (signed/direct URL)
    PATCH  /files/{path}?append=1 → 200/201 (server-side append, optional)

All paths are relative — the base URL prefix is prepended automatically.
"""

from __future__ import annotations

import json
from typing import Any

import requests

from .base_backend import StorageBackend
from ..content_headers import resolve_object_headers


_DEFAULT_TIMEOUT = 30


class ServerBackend(StorageBackend):
    def __init__(self) -> None:
        self._base_url: str = ""
        self._api_key: str = ""
        self._timeout: int = _DEFAULT_TIMEOUT
        self._configured: bool = False
        self._session: requests.Session | None = None
        self._init_from_settings()

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def _init_from_settings(self) -> None:
        try:
            from matrx_utils.conf import settings

            base_url = self._safe_get(settings, "FILE_SERVER_BASE_URL")
            api_key = self._safe_get(settings, "FILE_SERVER_API_KEY")
            if not base_url or not api_key:
                return

            self._base_url = base_url.rstrip("/")
            self._api_key = api_key

            timeout_raw = self._safe_get(settings, "FILE_SERVER_TIMEOUT")
            if timeout_raw:
                try:
                    self._timeout = int(timeout_raw)
                except ValueError:
                    self._timeout = _DEFAULT_TIMEOUT

            self._configured = True
        except Exception:
            return

    @staticmethod
    def _safe_get(settings_obj: object, name: str) -> str:
        try:
            val = getattr(settings_obj, name, None)
            return val if isinstance(val, str) and val.strip() else ""
        except Exception:
            return ""

    def _get_session(self) -> requests.Session:
        if self._session is None:
            session = requests.Session()
            session.headers.update({
                "Authorization": f"Bearer {self._api_key}",
                "Accept": "application/octet-stream",
            })
            self._session = session
        return self._session

    def is_configured(self) -> bool:
        return self._configured

    # ------------------------------------------------------------------
    # URL builder
    # ------------------------------------------------------------------

    def _file_url(self, path: str) -> str:
        return f"{self._base_url}/files/{path.lstrip('/')}"

    # ------------------------------------------------------------------
    # Core CRUD
    # ------------------------------------------------------------------

    def read(self, path: str) -> bytes:
        self._require_configured()
        url = self._file_url(path)
        response = self._get_session().get(url, timeout=self._timeout)
        self._raise_for_status(response, f"read '{path}'")
        return response.content

    def write(self, path: str, content: bytes | str, content_type: str | None = None) -> bool:
        self._require_configured()
        if isinstance(content, str):
            content = content.encode()

        url = self._file_url(path)
        session = self._get_session()
        resolved = resolve_object_headers(mime_type=content_type, file_name=path)
        headers = {"Content-Type": resolved.content_type}
        response = session.put(url, data=content, headers=headers, timeout=self._timeout)
        self._raise_for_status(response, f"write '{path}'")
        return True

    def append(self, path: str, content: bytes | str) -> bool:
        """Append to a file on the server.

        Tries a server-side PATCH ?append=1 first. Falls back to a
        read-modify-write cycle if the server returns 404 or 405.
        """
        self._require_configured()
        if isinstance(content, str):
            content = content.encode()

        url = self._file_url(path)
        session = self._get_session()
        headers = {"Content-Type": "application/octet-stream"}

        # Attempt server-side append
        response = session.patch(
            url,
            params={"append": "1"},
            data=content,
            headers=headers,
            timeout=self._timeout,
        )
        if response.status_code in (200, 201, 204):
            return True

        # Fall back: read → concat → write
        try:
            existing = self.read(path)
        except Exception:
            existing = b""
        return self.write(path, existing + content)

    def delete(self, path: str) -> bool:
        self._require_configured()
        url = self._file_url(path)
        response = self._get_session().delete(url, timeout=self._timeout)
        self._raise_for_status(response, f"delete '{path}'")
        return True

    # ------------------------------------------------------------------
    # URL generation
    # ------------------------------------------------------------------

    def get_url(
        self,
        path: str,
        expires_in: int = 3600,
        *,
        response_content_disposition: str | None = None,
        response_content_type: str | None = None,
    ) -> str:
        """Request a signed/direct URL from the server.

        Calls GET /files/{path}?url=1&expires={expires_in}.
        If the server doesn't support this convention the direct endpoint
        URL is returned instead. Response-header override kwargs are
        accepted for signature parity but not forwarded to the remote
        server endpoint.
        """
        self._require_configured()
        url = self._file_url(path)
        session = self._get_session()
        response = session.get(
            url,
            params={"url": "1", "expires": str(expires_in)},
            headers={"Accept": "application/json"},
            timeout=self._timeout,
        )
        if response.status_code == 200:
            try:
                data: Any = response.json()
                if isinstance(data, dict):
                    return data.get("url") or data.get("signedUrl") or url
            except (json.JSONDecodeError, ValueError):
                pass
        return url

    # ------------------------------------------------------------------
    # Listing
    # ------------------------------------------------------------------

    def list_files(self, prefix: str = "") -> list[str]:
        self._require_configured()
        base = f"{self._base_url}/files"
        params: dict[str, str] = {}
        if prefix:
            params["prefix"] = prefix

        response = self._get_session().get(
            base,
            params=params,
            headers={"Accept": "application/json"},
            timeout=self._timeout,
        )
        self._raise_for_status(response, f"list_files prefix='{prefix}'")

        data = response.json()
        if isinstance(data, list):
            return [str(item) for item in data]
        if isinstance(data, dict):
            return [str(item) for item in data.get("files", data.get("items", []))]
        return []

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _raise_for_status(response: requests.Response, context: str) -> None:
        if not response.ok:
            raise RuntimeError(
                f"ServerBackend {context} failed with HTTP {response.status_code}: "
                f"{response.text[:200]}"
            )

    def health_check(self) -> bool:
        """Return True if the file server is reachable and returns 200."""
        try:
            self._require_configured()
            response = self._get_session().get(
                f"{self._base_url}/health",
                timeout=self._timeout,
            )
            return response.ok
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Asynchronous API — httpx.AsyncClient
    # ------------------------------------------------------------------

    def _async_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Accept": "application/octet-stream",
        }

    async def read_async(self, path: str) -> bytes:
        self._require_configured()
        import httpx
        async with httpx.AsyncClient(headers=self._async_headers(), timeout=self._timeout) as client:
            response = await client.get(self._file_url(path))
            self._raise_for_status(response, f"read_async '{path}'")  # type: ignore[arg-type]
            return response.content

    async def write_async(self, path: str, content: bytes | str, content_type: str | None = None) -> bool:
        self._require_configured()
        if isinstance(content, str):
            content = content.encode()
        import httpx
        resolved = resolve_object_headers(mime_type=content_type, file_name=path)
        headers = {**self._async_headers(), "Content-Type": resolved.content_type}
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.put(self._file_url(path), content=content, headers=headers)
            self._raise_for_status(response, f"write_async '{path}'")  # type: ignore[arg-type]
            return True

    async def append_async(self, path: str, content: bytes | str) -> bool:
        self._require_configured()
        if isinstance(content, str):
            content = content.encode()
        import httpx
        headers = {**self._async_headers(), "Content-Type": "application/octet-stream"}
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            # Try server-side append first
            response = await client.patch(
                self._file_url(path),
                params={"append": "1"},
                content=content,
                headers=headers,
            )
            if response.status_code in (200, 201, 204):
                return True
        # Fall back: read → concat → write
        try:
            existing = await self.read_async(path)
        except Exception:
            existing = b""
        return await self.write_async(path, existing + content)

    async def delete_async(self, path: str) -> bool:
        self._require_configured()
        import httpx
        async with httpx.AsyncClient(headers=self._async_headers(), timeout=self._timeout) as client:
            response = await client.delete(self._file_url(path))
            self._raise_for_status(response, f"delete_async '{path}'")  # type: ignore[arg-type]
            return True

    async def get_url_async(
        self,
        path: str,
        expires_in: int = 3600,
        *,
        response_content_disposition: str | None = None,
        response_content_type: str | None = None,
    ) -> str:
        self._require_configured()
        import httpx, json as _json
        url = self._file_url(path)
        headers = {**self._async_headers(), "Accept": "application/json"}
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.get(url, params={"url": "1", "expires": str(expires_in)}, headers=headers)
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, dict):
                        return data.get("url") or data.get("signedUrl") or url
                except (_json.JSONDecodeError, ValueError):
                    pass
        return url

    async def list_files_async(self, prefix: str = "") -> list[str]:
        self._require_configured()
        import httpx
        base = f"{self._base_url}/files"
        params: dict[str, str] = {"prefix": prefix} if prefix else {}
        headers = {**self._async_headers(), "Accept": "application/json"}
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.get(base, params=params, headers=headers)
            self._raise_for_status(response, f"list_files_async prefix='{prefix}'")  # type: ignore[arg-type]
            data = response.json()
            if isinstance(data, list):
                return [str(item) for item in data]
            if isinstance(data, dict):
                return [str(item) for item in data.get("files", data.get("items", []))]
            return []

    async def health_check_async(self) -> bool:
        try:
            self._require_configured()
            import httpx
            async with httpx.AsyncClient(headers=self._async_headers(), timeout=self._timeout) as client:
                response = await client.get(f"{self._base_url}/health")
                return response.is_success
        except Exception:
            return False
