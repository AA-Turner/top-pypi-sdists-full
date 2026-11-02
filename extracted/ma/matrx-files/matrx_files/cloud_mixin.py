"""CloudMixin — injects cloud storage capabilities into any FileHandler subclass.

Every handler that extends FileHandler (PDFHandler, ImageHandler, etc.) automatically
inherits this mixin. Cloud access is only active when FileManager constructs the handler
and calls set_cloud_router(), which passes the shared BackendRouter instance.

Handlers used standalone (in scripts, tests, or outside FileManager) keep
self._cloud as None. Any cloud method call in that state raises a descriptive
RuntimeError rather than silently doing nothing.

Usage inside a handler method:
    # sync (scripts/tests, or when you know the context isn't async)
    raw   = self.cloud_read_url(url_from_client)
    ok    = self.cloud_write("s3://bucket/output.json", json_bytes)
    url   = self.cloud_ensure_url(old_url, expires_in=3600)

    # async (FastAPI routes, pipelines — always prefer these)
    raw   = await self.cloud_read_async("s3://bucket/file.pdf")
    ok    = await self.cloud_write_async("s3://bucket/result.txt", content)
    url   = await self.cloud_ensure_url_async(old_url)
    b64   = await self.get_for_llm_async(url, mode="base64")
    ok    = await self.push_from_llm_async(b64_data, "s3://bucket/out.png")
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from matrx_files.backends.router import BackendRouter
    from matrx_files.backends.llm_helpers import LLMInputMode, LLMOutputFormat


class CloudMixin:
    """Mixin that gives every FileHandler subclass a full cloud I/O API.

    Sits between BaseHandler and FileHandler in the MRO:
        BaseHandler → CloudMixin → FileHandler → specific handlers
    """

    _cloud: "BackendRouter | None" = None

    # ------------------------------------------------------------------
    # Router wiring — called by FileManager, not by app code
    # ------------------------------------------------------------------

    def set_cloud_router(self, router: "BackendRouter") -> None:
        """Attach the shared BackendRouter. Called by FileManager after construction."""
        self._cloud = router

    def _require_cloud(self) -> "BackendRouter":
        if self._cloud is None:
            raise RuntimeError(
                f"{self.__class__.__name__} has no cloud router attached. "
                "Construct this handler through FileManager, or call "
                "handler.set_cloud_router(router) before using cloud methods."
            )
        return self._cloud

    # ------------------------------------------------------------------
    # Sync cloud API
    # ------------------------------------------------------------------

    def cloud_read(self, uri: str) -> bytes:
        """Read raw bytes from a cloud URI (s3:// or server://)."""
        return self._require_cloud().read(uri)

    def cloud_write(self, uri: str, content: bytes | str, **kwargs) -> bool:
        """Write content to a cloud URI."""
        return self._require_cloud().write(uri, content, **kwargs)

    def cloud_append(self, uri: str, content: bytes | str) -> bool:
        """Append content to a cloud object."""
        return self._require_cloud().append(uri, content)

    def cloud_delete(self, uri: str) -> bool:
        """Delete a cloud object."""
        return self._require_cloud().delete(uri)

    def cloud_get_url(self, uri: str, expires_in: int = 3600) -> str:
        """Return a time-limited signed/presigned URL for a cloud object."""
        return self._require_cloud().get_url(uri, expires_in=expires_in)

    def cloud_list_files(self, uri_prefix: str) -> list[str]:
        """List cloud objects under a URI prefix."""
        return self._require_cloud().list_files(uri_prefix)

    def cloud_read_url(self, url: str) -> bytes:
        """Read bytes from any URL format the client might send.

        Accepts native URIs, public HTTPS, signed, or expired signed URLs.
        Reads via server-side credentials — token expiry is irrelevant.
        """
        return self._require_cloud().read_url(url)

    def cloud_ensure_url(self, url: str, expires_in: int = 3600) -> str:
        """Return a guaranteed-valid URL, refreshing only if expired.

        Reads S3 expiry from the URL itself — zero network calls when the URL
        is still fresh.
        """
        return self._require_cloud().ensure_url(url, expires_in=expires_in)

    # ------------------------------------------------------------------
    # Async cloud API — always prefer these in FastAPI routes
    # ------------------------------------------------------------------

    async def cloud_read_async(self, uri: str) -> bytes:
        """Non-blocking read from a cloud URI."""
        return await self._require_cloud().read_async(uri)

    async def cloud_write_async(self, uri: str, content: bytes | str, **kwargs) -> bool:
        """Non-blocking write to a cloud URI."""
        return await self._require_cloud().write_async(uri, content, **kwargs)

    async def cloud_append_async(self, uri: str, content: bytes | str) -> bool:
        """Non-blocking append to a cloud object."""
        return await self._require_cloud().append_async(uri, content)

    async def cloud_delete_async(self, uri: str) -> bool:
        """Non-blocking delete of a cloud object."""
        return await self._require_cloud().delete_async(uri)

    async def cloud_get_url_async(self, uri: str, expires_in: int = 3600) -> str:
        """Non-blocking signed/presigned URL generation."""
        return await self._require_cloud().get_url_async(uri, expires_in=expires_in)

    async def cloud_get_public_url_async(self, uri: str) -> str:
        """Return the permanent public URL for a cloud object (bucket must be public)."""
        return await self._require_cloud().get_public_url_async(uri)

    def cloud_get_public_url(self, uri: str) -> str:
        """Return the permanent public URL for a cloud object (bucket must be public)."""
        return self._require_cloud().get_public_url(uri)

    async def cloud_list_files_async(self, uri_prefix: str) -> list[str]:
        """Non-blocking file listing under a URI prefix."""
        return await self._require_cloud().list_files_async(uri_prefix)

    async def cloud_read_url_async(self, url: str) -> bytes:
        """Non-blocking read from any URL format a client might send."""
        return await self._require_cloud().read_url_async(url)

    async def cloud_ensure_url_async(self, url: str, expires_in: int = 3600) -> str:
        """Non-blocking ensure_url — refreshes only if expired."""
        return await self._require_cloud().ensure_url_async(url, expires_in=expires_in)

    # ------------------------------------------------------------------
    # LLM helpers
    # ------------------------------------------------------------------

    def get_for_llm(
        self,
        url: str,
        mode: "LLMInputMode" = "base64",
        expires_in: int = 300,
    ) -> str | bytes:
        """Return a cloud file in the format an LLM provider needs.

        mode="url"    → fresh signed URL (for providers that fetch directly)
        mode="base64" → base64-encoded string (for inline data providers)
        mode="bytes"  → raw bytes
        """
        from matrx_files.backends.llm_helpers import get_for_llm
        return get_for_llm(url, self._require_cloud(), mode=mode, expires_in=expires_in)

    async def get_for_llm_async(
        self,
        url: str,
        mode: "LLMInputMode" = "base64",
        expires_in: int = 300,
    ) -> str | bytes:
        """Async version of get_for_llm()."""
        from matrx_files.backends.llm_helpers import get_for_llm_async
        return await get_for_llm_async(url, self._require_cloud(), mode=mode, expires_in=expires_in)

    def push_from_llm(
        self,
        data: str | bytes,
        dest_uri: str,
        source_format: "LLMOutputFormat" = "base64",
        **kwargs,
    ) -> bool:
        """Write LLM-generated content to cloud storage.

        source_format="base64" → decode then write (OpenAI, Stability AI, etc.)
        source_format="url"    → download then write (DALL-E URLs, Gemini, etc.)
        source_format="bytes"  → write directly
        """
        from matrx_files.backends.llm_helpers import push_from_llm
        return push_from_llm(data, dest_uri, self._require_cloud(), source_format=source_format, **kwargs)

    async def push_from_llm_async(
        self,
        data: str | bytes,
        dest_uri: str,
        source_format: "LLMOutputFormat" = "base64",
        **kwargs,
    ) -> bool:
        """Async version of push_from_llm()."""
        from matrx_files.backends.llm_helpers import push_from_llm_async
        return await push_from_llm_async(data, dest_uri, self._require_cloud(), source_format=source_format, **kwargs)
