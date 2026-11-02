from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any
import uuid

from .file_handler import FileHandler
from .specific_handlers.html_handler import HtmlHandler
from .specific_handlers.json_handler import JsonHandler
from .specific_handlers.markdown_handler import MarkdownHandler
from .specific_handlers.text_handler import TextHandler
from .specific_handlers.image_handler import (
    ImageHandler,
    ImageVariant,
    PODCAST_VARIANTS,
    SOCIAL_VARIANTS,
    WEB_VARIANTS,
    EMAIL_VARIANTS,
    LOGO_VARIANTS,
    AVATAR_VARIANTS,
    FAVICON_VARIANTS,
    SOCIAL_BASELINE,
    ALL_VARIANTS,
)
from .specific_handlers.video_handler import VideoHandler
from .batch_handler import BatchHandler
from .backends import (
    BackendRouter,
    is_cloud_uri,
    parse_storage_url,
    is_storage_url,
    get_for_llm,
    get_for_llm_async,
    push_from_llm,
    push_from_llm_async,
    LLMInputMode,
    LLMOutputFormat,
)

if TYPE_CHECKING:
    from .cloud_sync.config import CloudSyncConfig
    from .cloud_sync.sync_engine import SyncEngine
    from .cloud_sync.models import SyncResult

_logger = logging.getLogger(__name__)


class FileManager:
    _instances = {}
    _log_intro = "[MATRX FILE MANAGER]"

    def __init__(
        self,
        app_name,
        new_instance=False,
        batch_print=False,
        print_errors=True,
        batch_handler=None,
        cloud_sync: CloudSyncConfig | None = None,
    ):
        self.app_name = app_name
        self.batch_print = batch_print
        self.print_errors = print_errors
        self.batch_handler = batch_handler or BatchHandler.get_instance(enable_batch=batch_print)

        self.file_handler = FileHandler.get_instance(app_name, new_instance, batch_print, print_errors, self.batch_handler)
        self.text_handler = TextHandler(app_name, batch_print=batch_print)
        self.json_handler = JsonHandler(app_name, batch_print=batch_print)
        self.html_handler = HtmlHandler(app_name, batch_print=batch_print)
        self.image_handler = ImageHandler(app_name, batch_print=batch_print)
        self.markdown_handler = MarkdownHandler(app_name, batch_print=batch_print)
        self.video_handler = VideoHandler(app_name, batch_print=batch_print)
        self.cloud = BackendRouter()

        # Inject the shared router into every handler so they can call
        # cloud methods (self.cloud_read, self.cloud_write_async, etc.)
        # without constructing their own BackendRouter.
        for _handler in (
            self.file_handler,
            self.text_handler,
            self.json_handler,
            self.html_handler,
            self.image_handler,
            self.markdown_handler,
            self.video_handler,
        ):
            _handler.set_cloud_router(self.cloud)

        # Cloud sync engine — None when not configured.
        self._sync_engine: SyncEngine | None = None
        if cloud_sync is not None:
            from .cloud_sync.sync_engine import SyncEngine as _SE
            self._sync_engine = _SE(cloud_sync, self.cloud)
            # Back-pointer so VariantsService can reach fm.image_handler.
            self._sync_engine._fm_ref = self

    @property
    def sync_engine(self) -> SyncEngine | None:
        """The cloud sync engine, or None if cloud_sync is not configured."""
        return self._sync_engine

    @classmethod
    def get_instance(
        cls,
        app_name,
        new_instance=False,
        batch_print=False,
        print_errors=True,
        batch_handler=None,
        cloud_sync: CloudSyncConfig | None = None,
    ):
        key = (app_name, batch_print, print_errors, id(batch_handler))
        if not new_instance and key in cls._instances:
            existing = cls._instances[key]
            if cloud_sync is not None and existing._sync_engine is None:
                from .cloud_sync.sync_engine import SyncEngine as _SE
                existing._sync_engine = _SE(cloud_sync, existing.cloud)
            return existing

        instance = cls(app_name, new_instance, batch_print, print_errors, batch_handler, cloud_sync)
        if not new_instance:
            cls._instances[key] = instance
        return instance

    # ------------------------------------------------------------------
    # Internal sync helpers
    # ------------------------------------------------------------------

    def _require_sync_engine(self) -> SyncEngine:
        if self._sync_engine is None:
            raise RuntimeError(
                "Cloud sync is not configured. Pass a CloudSyncConfig to FileManager."
            )
        return self._sync_engine

    # ==================================================================
    # MEDIA REFERENCE RESOLUTION — the single public entry point.
    #
    # Every package and every consumer that takes a user-supplied media
    # reference resolves it through one of these two methods. Idempotent
    # (checks ``ref.is_resolved``) so defense-in-depth calls cost nothing.
    # Cache-first so the typical "upload then chat" flow is a memory hit.
    # ==================================================================

    def resolve_media(self, ref, *, needs_bytes: bool = False,
                      presigned_ttl_seconds: int = 3600):
        """Resolve a ``MediaRef`` in place (sync). Returns the same ref.

        ``needs_bytes=True`` produces ``ref.base64_data``; otherwise we
        prefer a fresh presigned URL and only fall back to bytes when no
        URL form is available.

        If ``ref.is_resolved`` is already True, this is a no-op.
        """
        from .cloud_sync.media_ref import MediaRef
        from .cloud_sync._media_resolution import _resolve_media_sync
        if not isinstance(ref, MediaRef):
            raise TypeError(f"resolve_media expects MediaRef, got {type(ref).__name__}")
        return _resolve_media_sync(self, ref, needs_bytes=needs_bytes,
                                    presigned_ttl_seconds=presigned_ttl_seconds)

    async def resolve_media_async(self, ref, *, needs_bytes: bool = False,
                                   presigned_ttl_seconds: int = 3600):
        """Async variant. Same idempotency + caching guarantees."""
        from .cloud_sync.media_ref import MediaRef
        from .cloud_sync._media_resolution import _resolve_media_async_impl
        if not isinstance(ref, MediaRef):
            raise TypeError(f"resolve_media_async expects MediaRef, got {type(ref).__name__}")
        return await _resolve_media_async_impl(self, ref, needs_bytes=needs_bytes,
                                                presigned_ttl_seconds=presigned_ttl_seconds)

    # ==================================================================
    # VARIANTS — derived files written to cld_files alongside the master.
    #
    # ``resolve_variant_async(master_id, variant_key=...)`` is idempotent;
    # second call hits the existing variant row without re-encoding.
    # See ``cloud_sync/variants.py`` for the full design notes.
    # ==================================================================

    async def resolve_variant_async(
        self,
        master_file_id: str,
        *,
        variant_key: str,
        family: str = "vision",
        encoder=None,
    ) -> dict:
        """Resolve (or render and persist) a variant of a master file.

        Returns a dict with the variant's ``file_id``, ``storage_uri``,
        ``mime_type``, ``file_size``, ``url``, ``is_new``, ``metadata``.
        """
        from .cloud_sync.variants import render_variant_async
        return await render_variant_async(
            self,
            master_file_id,
            variant_key=variant_key,
            family=family,
            encoder=encoder,
        )

    def _should_sync(self, override: bool | None) -> bool:
        if override is not None:
            return override
        return self._sync_engine is not None and self._sync_engine.auto_sync

    def _background_sync_write(
        self, path: str, content, mime_type: str | None = None
    ) -> None:
        if self._sync_engine:
            self._sync_engine.fire_and_forget_write(path, content, mime_type=mime_type)

    def _background_sync_delete(self, path: str) -> None:
        if self._sync_engine:
            self._sync_engine.fire_and_forget_delete(path)

    def read(self, root, path=None, file_type='text'):
        """Read a file from local storage or a cloud URI.

        Local usage (unchanged):
            fm.read("base", "report.json", file_type="json")

        Cloud usage — pass a full URI as the first argument:
            fm.read("s3://bucket/report.json")
            fm.read("s3://bucket/avatar.png")
            fm.read("server://uploads/data.csv")
        """
        if is_cloud_uri(root):
            return self.cloud.read(root)
        handler = getattr(self, f"{file_type}_handler")
        return getattr(handler, f"read_{file_type}")(root, path)

    def write(self, root, path=None, content=None, file_type='text', clean=True, *, cloud_sync=None, **kwargs):
        """Write content to local storage or a cloud URI.

        Local usage (unchanged):
            fm.write("base", "report.json", data, file_type="json")

        Cloud usage — pass a full URI as the first argument:
            fm.write("s3://bucket/report.json", content=data)
            fm.write("s3://bucket/avatar.png", content=image_bytes)
            fm.write("server://uploads/data.csv", content=csv_text)

        When cloud_sync is configured, local writes automatically sync
        to cloud storage and record metadata in the database (background).
        Pass ``cloud_sync=False`` to skip sync for this call.
        """
        if is_cloud_uri(root):
            if content is None:
                raise ValueError("write() requires 'content' when using a cloud URI.")
            return self.cloud.write(root, content, **kwargs)
        handler = getattr(self, f"{file_type}_handler")
        result = getattr(handler, f"write_{file_type}")(root, path, content, clean=clean)
        if result and path and self._should_sync(cloud_sync):
            self._background_sync_write(path, content)
        return result

    def append(self, root, path=None, content=None, file_type='text', **kwargs):
        """Append to a file in local storage or a cloud URI.

        Cloud usage:
            fm.append("s3://bucket/log.txt", content=new_lines)
        """
        if is_cloud_uri(root):
            if content is None:
                raise ValueError("append() requires 'content' when using a cloud URI.")
            return self.cloud.append(root, content)
        handler = getattr(self, f"{file_type}_handler")
        append_method = getattr(handler, f"append_{file_type}", None)
        if append_method is None:
            raise NotImplementedError(
                f"append() is not implemented for file_type='{file_type}'."
            )
        return append_method(root, path, content)

    def delete(self, root, path=None, file_type='text', *, cloud_sync=None):
        """Delete a file from local storage or a cloud URI.

        Cloud usage:
            fm.delete("s3://bucket/old-report.json")
        """
        if is_cloud_uri(root):
            return self.cloud.delete(root)
        handler = getattr(self, f"{file_type}_handler")
        result = handler.delete_file(root, path)
        if path and self._should_sync(cloud_sync):
            self._background_sync_delete(path)
        return result

    def file_exists(self, root, path, file_type='text'):
        handler = getattr(self, f"{file_type}_handler")
        return handler.file_exists(root, path)

    def delete_file(self, root, path, file_type='text'):
        handler = getattr(self, f"{file_type}_handler")
        return handler.delete_file(root, path)

    def list_files(self, root, path="", file_type='text'):
        """List files in local storage or a cloud URI prefix.

        Cloud usage:
            fm.list_files("s3://bucket/reports/")
            fm.list_files("s3://bucket/avatars/")
        """
        if is_cloud_uri(root):
            return self.cloud.list_files(root)
        handler = getattr(self, f"{file_type}_handler")
        return handler.list_files(root, path)

    def get_url(self, uri: str, expires_in: int = 3600) -> str:
        """Return a time-limited URL for a cloud-stored file.

        Usage:
            url = fm.get_url("s3://bucket/report.pdf", expires_in=600)
            url = fm.get_url("s3://bucket/avatars/user1.png")
            url = fm.get_url("server://uploads/document.pdf")
        """
        if not is_cloud_uri(uri):
            raise ValueError(
                f"get_url() requires a cloud URI (s3:// or server://). Got: '{uri}'"
            )
        return self.cloud.get_url(uri, expires_in=expires_in)

    def read_url(self, url: str) -> bytes:
        """Read bytes from any URL format a client (React/mobile) might send.

        This is the recommended entry point for FastAPI route handlers that
        receive a file URL from the frontend. It accepts every URL format —
        public, signed/presigned, expired signed, or native storage URI —
        and reads the file via server-side credentials, making token expiry
        and URL format completely irrelevant.

        Supported inputs
        ----------------
            # Native storage URIs
            fm.read_url("s3://bucket/users/user-id/report.pdf")
            fm.read_url("s3://bucket/uploads/image.png")

            # S3 HTTPS URLs (with or without presigned query params)
            fm.read_url("https://bucket.s3.us-east-2.amazonaws.com/key")
            fm.read_url("https://bucket.s3.us-east-2.amazonaws.com/key?X-Amz-Signature=...")

        Raises
        ------
        ValueError
            If the URL cannot be recognized as a supported storage URL.
        RuntimeError
            If the relevant backend is not configured (missing credentials).
        """
        return self.cloud.read_url(url)

    def parse_url(self, url: str):
        """Parse any cloud storage URL and return a ParsedStorageUrl.

        Useful when you need to inspect what backend and path a URL refers to
        before deciding whether to read it.

        Returns a ParsedStorageUrl with .scheme, .storage_path, .to_native_uri()
        """
        return parse_storage_url(url)

    def is_storage_url(self, url: str) -> bool:
        """Return True if *url* is a recognizable cloud storage URL."""
        return is_storage_url(url)

    def configured_backends(self) -> list[str]:
        """Return the names of all cloud backends that have valid credentials."""
        return self.cloud.configured_backends()

    # ------------------------------------------------------------------
    # Async cloud API — use these in FastAPI routes
    # ------------------------------------------------------------------

    async def read_async(self, uri: str) -> bytes:
        """Non-blocking read. Always use this inside FastAPI routes."""
        return await self.cloud.read_async(uri)

    async def write_async(self, uri: str, content: bytes | str, **kwargs) -> bool:
        """Non-blocking write."""
        return await self.cloud.write_async(uri, content, **kwargs)

    async def append_async(self, uri: str, content: bytes | str) -> bool:
        """Non-blocking append."""
        return await self.cloud.append_async(uri, content)

    async def delete_async(self, uri: str) -> bool:
        """Non-blocking delete."""
        return await self.cloud.delete_async(uri)

    async def get_url_async(self, uri: str, expires_in: int = 3600) -> str:
        """Non-blocking signed/presigned URL generation."""
        return await self.cloud.get_url_async(uri, expires_in=expires_in)

    async def list_files_async(self, uri_prefix: str) -> list[str]:
        """Non-blocking file listing."""
        return await self.cloud.list_files_async(uri_prefix)

    async def read_url_async(self, url: str) -> bytes:
        """Non-blocking read from any URL format a client might send."""
        return await self.cloud.read_url_async(url)

    # ------------------------------------------------------------------
    # ensure_url — smart URL refresh (sync + async)
    # ------------------------------------------------------------------

    def ensure_url(self, url: str, expires_in: int = 3600) -> str:
        """Return a guaranteed-valid URL for a cloud file.

        Reads expiry from the URL itself (no network call) and only
        regenerates the URL if it has expired or has < 60 s remaining.

        Works with:
        - Native URIs (s3://)          → always generates fresh URL
        - expired signed URLs (JWT token in ?token) → checks 'exp' claim
        - S3 presigned URLs (X-Amz-Date/Expires)    → checks query params
        - Public HTTPS URLs (no expiry info)         → returned as-is

        Usage in a FastAPI route (sync helper version):
            url = fm.ensure_url(url_from_client, expires_in=3600)
            response = openai.chat(..., image_url=url)
        """
        return self.cloud.ensure_url(url, expires_in=expires_in)

    async def ensure_url_async(self, url: str, expires_in: int = 3600) -> str:
        """Async version of ensure_url(). Use this in FastAPI routes."""
        return await self.cloud.ensure_url_async(url, expires_in=expires_in)

    # ------------------------------------------------------------------
    # LLM helpers — get_for_llm / push_from_llm (sync + async)
    # ------------------------------------------------------------------

    def get_for_llm(
        self,
        url: str,
        mode: LLMInputMode = "base64",
        expires_in: int = 300,
    ) -> str | bytes:
        """Return a cloud file in the format an LLM provider needs.

        Parameters
        ----------
        url:
            Any cloud URL or URI (public, signed, presigned, native).
        mode:
            "url"    → fresh signed URL (auto-refreshed if expired).
                       Use for providers that fetch files directly
                       (OpenAI vision, Gemini file API, etc.)
            "base64" → raw bytes encoded as base64 string.
                       Use for providers that require inline data
                       (Anthropic, most multi-modal APIs).
            "bytes"  → raw bytes. Use when you encode yourself.
        expires_in:
            Expiry for generated signed URLs in seconds (default 300).

        Examples
        --------
            # Provider fetches URL directly
            url = fm.get_for_llm(file_url, mode="url")
            openai.chat(messages=[{"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": url}}
            ]}])

            # Provider needs inline base64
            b64 = fm.get_for_llm(file_url, mode="base64")
            anthropic.messages.create(messages=[{"role": "user", "content": [
                {"type": "image", "source": {"type": "base64",
                 "media_type": "image/png", "data": b64}}
            ]}])
        """
        return get_for_llm(url, self.cloud, mode=mode, expires_in=expires_in)

    async def get_for_llm_async(
        self,
        url: str,
        mode: LLMInputMode = "base64",
        expires_in: int = 300,
    ) -> str | bytes:
        """Async version of get_for_llm(). Use this in FastAPI routes."""
        return await get_for_llm_async(url, self.cloud, mode=mode, expires_in=expires_in)

    def push_from_llm(
        self,
        data: str | bytes,
        dest_uri: str,
        source_format: LLMOutputFormat = "base64",
        **write_kwargs,
    ) -> bool:
        """Write LLM-generated content directly to cloud storage.

        Parameters
        ----------
        data:
            The LLM's output — base64 string, a URL, or raw bytes.
        dest_uri:
            Destination in cloud storage.
            e.g. "s3://bucket/users/{user_id}/output.png"
            e.g. "s3://bucket/generated/image.png"
        source_format:
            "base64" → decode and write (OpenAI, Stability AI, etc.)
            "url"    → download then write (DALL-E response URLs, Gemini, etc.)
            "bytes"  → write directly

        Examples
        --------
            # OpenAI image generation → S3
            result = openai.images.generate(...)
            fm.push_from_llm(
                result.data[0].b64_json,
                "s3://bucket/users/123/avatar.png",
                source_format="base64",
            )

            # DALL-E URL → S3
            fm.push_from_llm(
                result.data[0].url,
                "s3://bucket/generated/image.png",
                source_format="url",
            )
        """
        return push_from_llm(data, dest_uri, self.cloud, source_format=source_format, **write_kwargs)

    async def push_from_llm_async(
        self,
        data: str | bytes,
        dest_uri: str,
        source_format: LLMOutputFormat = "base64",
        **write_kwargs,
    ) -> bool:
        """Async version of push_from_llm(). Use this in FastAPI routes."""
        return await push_from_llm_async(
            data, dest_uri, self.cloud, source_format=source_format, **write_kwargs
        )

    def print_batch(self):
        self.file_handler.print_batch()

    def read_json(self, root, path):
        return self.json_handler.read_json(root, path)

    def write_json(self, root, path, data, clean=True):
        return self.json_handler.write_json(root=root, path=path, data=data, clean=clean)

    def append_json(self, root, path, data, clean=True):
        return self.json_handler.append_json(root=root, path=path, data=data, clean=clean)

    def read_temp_json(self, path):
        return self.json_handler.read_json(root="temp", path=path)

    def write_temp_json(self, path, data, clean=True):
        return self.json_handler.write_json(root="temp", path=path, data=data, clean=clean)

    def get_config_json(self, path):
        return self.json_handler.read_json(root="config", path=path)

    def read_text(self, root, path):
        return self.text_handler.read_text(root, path)

    def write_text(self, root, path, data, clean=True):
        return self.text_handler.write_text(root=root, path=path, content=data, clean=clean)

    def read_temp_text(self, path):
        return self.text_handler.read_text(root="temp", path=path)

    def write_temp_text(self, path, data, clean=True):
        return self.text_handler.write_text(root="temp", path=path, content=data, clean=clean)

    # HTML specific methods
    def read_html(self, root, path):
        return self.html_handler.read_html(root, path)

    def write_html(self, root, path, data, clean=True):
        return self.html_handler.write_html(root=root, path=path, content=data, clean=clean)

    def read_temp_html(self, path):
        return self.html_handler.read_html(root="temp", path=path)

    def write_temp_html(self, path, data, clean=True):
        return self.html_handler.write_html(root="temp", path=path, content=data, clean=clean)

    # Markdown specific methods
    def read_markdown(self, root, path):
        return self.markdown_handler.read_markdown(root, path)

    def write_markdown(self, root, path, data, clean=True):
        return self.markdown_handler.write_markdown(root=root, path=path, content=data, clean=clean)

    def read_temp_markdown(self, path):
        return self.markdown_handler.read_markdown(root="temp", path=path)

    def write_temp_markdown(self, path, data, clean=True):
        return self.markdown_handler.write_markdown(root="temp", path=path, content=data, clean=clean)

    def read_markdown_lines(self, root, path):
        return self.markdown_handler.read_lines(root, path)

    def write_markdown_lines(self, root, path, data, clean=True):
        return self.markdown_handler.write_lines(root, path, lines=data, clean=clean)


    # Image specific
    def read_image(self, root, path):
        return self.image_handler.read_image(root, path)

    def write_image(self, root, path, data):
        return self.image_handler.write_image(root=root, path=path, image=data)

    def read_temp_image(self, path):
        return self.image_handler.read_image(root="temp", path=path)

    def write_temp_image(self, path, data, clean=True):
        return self.image_handler.write_image(root="temp", path=path, image=data)

    def generate_filename(self, extension, sub_dir="", prefix="", suffix="", random=False):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sub_dir = f"{sub_dir}/" if sub_dir else ""
        prefix = f"{prefix}_" if prefix else ""
        suffix = f"_{suffix}" if suffix else ""

        if random:
            return f"{sub_dir}{prefix}{str(uuid.uuid4())}{suffix}.{extension}"

        return f"{sub_dir}{prefix}{timestamp}{suffix}.{extension}"

    def generate_directoryname(self, sub_dir="", prefix="", suffix="", random=False):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sub_dir = f"{sub_dir}/" if sub_dir else ""
        prefix = f"{prefix}_" if prefix else ""
        suffix = f"_{suffix}" if suffix else ""

        if random:
            return f"{sub_dir}{prefix}{str(uuid.uuid4())}{suffix}"

        return f"{sub_dir}{prefix}{timestamp}{suffix}"

    def add_to_batch(self, full_path=None, message=None, color=None):
        self.file_handler.add_to_batch(full_path, message, color)

    def get_full_path_from_base(self, root, path):
        return self.file_handler.public_get_full_path(root, path)

    # ------------------------------------------------------------------
    # Media processing convenience methods
    # ------------------------------------------------------------------

    async def process_image_variants_async(
        self,
        image_bytes: bytes,
        variants: "list[ImageVariant]",
        folder_uri: str,
    ) -> "dict[str, str]":
        """Resize image to all variants, upload each to cloud, return public URLs.

        Delegates to ImageHandler.process_variants_async(). CPU work runs in a
        thread executor; uploads are fully async.

        Parameters
        ----------
        image_bytes:
            Raw bytes of the source image.
        variants:
            List of ImageVariant dicts. Use PODCAST_VARIANTS, SOCIAL_VARIANTS,
            WEB_VARIANTS, EMAIL_VARIANTS, or a custom list.
        folder_uri:
            Cloud folder URI, e.g. ``"s3://bucket/{user_id}/{uuid}"``.

        Returns
        -------
        dict[str, str]
            Variant key → permanent public URL.
        """
        return await self.image_handler.process_variants_async(image_bytes, variants, folder_uri)

    async def extract_video_frame_async(
        self, video_bytes: bytes, position: float = 0.10
    ) -> bytes:
        """Extract a JPEG frame from *video_bytes* at *position* (0.0–1.0).

        Delegates to VideoHandler.extract_frame_at_async(). Runs in a thread
        executor — never blocks the event loop.

        Returns JPEG bytes of the extracted frame.
        """
        return await self.video_handler.extract_frame_at_async(video_bytes, position)

    async def upload_video_async(
        self,
        video_bytes: bytes,
        dest_uri: str,
        content_type: str = "video/mp4",
    ) -> str:
        """Upload video bytes to cloud storage and return the permanent public URL.

        Delegates to VideoHandler.upload_video_async(). Uses the S3 backend's
        600-second timeout, which safely handles large podcast video files.

        Parameters
        ----------
        video_bytes:
            Raw bytes of the video file.
        dest_uri:
            Full cloud storage URI including filename.
            e.g. ``"s3://bucket/{user_id}/{uuid}/video.mp4"``
        content_type:
            MIME type. Defaults to ``"video/mp4"``.

        Returns
        -------
        str
            Permanent public URL of the uploaded video.
        """
        return await self.video_handler.upload_video_async(video_bytes, dest_uri, content_type)

    # ------------------------------------------------------------------
    # Managed cloud operations — full control with permissions + versioning
    # ------------------------------------------------------------------

    def managed_write(
        self,
        file_path: str,
        content: bytes | str | dict | list,
        *,
        mime_type: str | None = None,
        published_to_web: bool | None = None,
        shown_to: str | None = None,
        visibility: str | None = None,
        share_with: list[str] | None = None,
        share_level: str = "read",
        change_summary: str | None = None,
        user_id: str | None = None,
        metadata: dict | None = None,
    ) -> SyncResult:
        """Write a file to cloud with full metadata, versioning, and permissions."""
        return self._require_sync_engine().managed_write(
            file_path, content,
            mime_type=mime_type,
            published_to_web=published_to_web,
            shown_to=shown_to,
            visibility=visibility,
            share_with=share_with,
            share_level=share_level,
            change_summary=change_summary,
            user_id=user_id,
            metadata=metadata,
        )

    async def managed_write_async(
        self,
        file_path: str,
        content: bytes | str | dict | list,
        *,
        mime_type: str | None = None,
        published_to_web: bool | None = None,
        shown_to: str | None = None,
        visibility: str | None = None,
        share_with: list[str] | None = None,
        share_level: str = "read",
        change_summary: str | None = None,
        user_id: str | None = None,
        metadata: dict | None = None,
        file_id: str | None = None,
        parent_file_id: str | None = None,
        derivation_kind: str | None = None,
        derivation_metadata: dict[str, Any] | None = None,
        duplicate_of_file_id: str | None = None,
    ) -> SyncResult:
        """Async version of managed_write(). Use this in FastAPI routes."""
        return await self._require_sync_engine().managed_write_async(
            file_path, content,
            mime_type=mime_type,
            published_to_web=published_to_web,
            shown_to=shown_to,
            visibility=visibility,
            share_with=share_with,
            share_level=share_level,
            change_summary=change_summary,
            user_id=user_id,
            metadata=metadata,
            file_id=file_id,
            parent_file_id=parent_file_id,
            derivation_kind=derivation_kind,
            derivation_metadata=derivation_metadata,
            duplicate_of_file_id=duplicate_of_file_id,
        )

    def managed_read(
        self,
        file_path: str,
        *,
        user_id: str | None = None,
        version: int | None = None,
    ) -> bytes:
        """Read a cloud-managed file with permission checking."""
        return self._require_sync_engine().managed_read(
            file_path, user_id=user_id, version=version
        )

    async def managed_read_async(
        self,
        file_path: str,
        *,
        user_id: str | None = None,
        version: int | None = None,
    ) -> bytes:
        """Async version of managed_read()."""
        return await self._require_sync_engine().managed_read_async(
            file_path, user_id=user_id, version=version
        )

    def managed_delete(
        self,
        file_path: str,
        *,
        user_id: str | None = None,
        hard_delete: bool = False,
        allow_system_purge: bool = False,
    ) -> bool:
        """Delete a cloud-managed file (soft delete by default)."""
        return self._require_sync_engine().managed_delete(
            file_path,
            user_id=user_id,
            hard_delete=hard_delete,
            allow_system_purge=allow_system_purge,
        )

    async def managed_delete_async(
        self,
        file_path: str,
        *,
        user_id: str | None = None,
        hard_delete: bool = False,
        allow_system_purge: bool = False,
    ) -> bool:
        """Async version of managed_delete()."""
        return await self._require_sync_engine().managed_delete_async(
            file_path,
            user_id=user_id,
            hard_delete=hard_delete,
            allow_system_purge=allow_system_purge,
        )

    def managed_list_files(
        self,
        folder_path: str | None = None,
        *,
        user_id: str | None = None,
    ) -> list[dict]:
        """List cloud-managed files, optionally filtered by folder."""
        return self._require_sync_engine().list_files(
            folder_path=folder_path, user_id=user_id
        )

    async def managed_list_files_async(
        self,
        folder_path: str | None = None,
        *,
        user_id: str | None = None,
    ) -> list[dict]:
        """Async version of managed_list_files()."""
        return await self._require_sync_engine().list_files_async(
            folder_path=folder_path, user_id=user_id
        )

    def managed_get_url(
        self,
        file_path: str,
        *,
        user_id: str | None = None,
    ) -> str:
        """Durable render URL for a managed file, with permission check."""
        return self._require_sync_engine().get_file_url(file_path, user_id=user_id)

    async def managed_get_url_async(
        self,
        file_path: str,
        *,
        user_id: str | None = None,
    ) -> str:
        """Async version of managed_get_url()."""
        return await self._require_sync_engine().get_file_url_async(file_path, user_id=user_id)

    def set_sync_user(self, user_id: str) -> None:
        """Switch the active user for cloud sync (call per-request in FastAPI)."""
        self._require_sync_engine().set_user(user_id)
