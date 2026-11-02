"""LLM file I/O helpers.

Two directions:
    get_for_llm  — cloud file → whatever an LLM provider needs
    push_from_llm — whatever an LLM returns → cloud storage

Both directions have sync and async variants.

get_for_llm modes
-----------------
    "url"     — return a fresh signed URL the provider can fetch directly.
                Expired signed URLs are automatically refreshed (no network
                call if still valid).
    "base64"  — read bytes via credentials, return base64-encoded string.
                Use for providers that require inline data (Anthropic, etc.).
    "bytes"   — read raw bytes. Use when you need to do your own encoding
                or when piping to another process.

push_from_llm source_format
---------------------------
    "base64"  — decode and write. Standard for OpenAI image generation, etc.
    "url"     — download via HTTP (uses open_any_file which handles auth
                headers if needed) and write to storage. Handles temporary
                provider URLs (DALL-E, Gemini, etc.).
    "bytes"   — write directly.

All methods accept any URL format (native URI, public HTTPS, signed HTTPS).
"""

from __future__ import annotations

import base64
from typing import Literal

LLMInputMode = Literal["url", "base64", "bytes"]
LLMOutputFormat = Literal["base64", "url", "bytes"]


# ---------------------------------------------------------------------------
# Sync API
# ---------------------------------------------------------------------------

def get_for_llm(
    url: str,
    router,
    mode: LLMInputMode = "base64",
    expires_in: int = 300,
) -> str | bytes:
    """Return the file at *url* in the format *mode* specifies.

    Parameters
    ----------
    url:
        Any cloud storage URL or native URI.
    router:
        The BackendRouter instance (passed by FileManager).
    mode:
        "url"    → fresh signed URL (auto-refreshed if expired)
        "base64" → bytes read via credentials, base64-encoded string
        "bytes"  → raw bytes
    expires_in:
        Expiry for generated signed URLs (seconds). Default 300 s.

    Returns
    -------
    str  when mode is "url" or "base64"
    bytes when mode is "bytes"
    """
    if mode == "url":
        return router.ensure_url(url, expires_in=expires_in)

    raw: bytes = router.read_url(url)

    if mode == "base64":
        return base64.b64encode(raw).decode()

    return raw  # mode == "bytes"


def push_from_llm(
    data: str | bytes,
    dest_uri: str,
    router,
    source_format: LLMOutputFormat = "base64",
    **write_kwargs,
) -> bool:
    """Write *data* (LLM output) to *dest_uri* in cloud storage.

    Parameters
    ----------
    data:
        The LLM's output — base64 string, a URL, or raw bytes.
    dest_uri:
        Cloud storage destination, e.g. "s3://bucket/users/id/output.png"
    router:
        The BackendRouter instance.
    source_format:
        "base64" → decode then write
        "url"    → download then write (handles any HTTP URL)
        "bytes"  → write directly
    write_kwargs:
        Extra keyword arguments forwarded to backend.write() (e.g. acl="public-read").
    """
    raw: bytes

    if source_format == "base64":
        if isinstance(data, str):
            raw = base64.b64decode(data)
        else:
            raw = base64.b64decode(data.decode() if isinstance(data, bytes) else data)

    elif source_format == "url":
        if not isinstance(data, str):
            raise TypeError(f"source_format='url' requires a str URL, got {type(data)}")
        # open_any_file handles HTTP downloads cleanly
        from matrx_files.local_files import open_any_file
        filename, file_obj = open_any_file(data)
        try:
            raw = file_obj.read()
        finally:
            file_obj.close()

    elif source_format == "bytes":
        if isinstance(data, str):
            raw = data.encode()
        else:
            raw = data

    else:
        raise ValueError(f"Unknown source_format: {source_format!r}")

    return router.write(dest_uri, raw, **write_kwargs)


# ---------------------------------------------------------------------------
# Async API
# ---------------------------------------------------------------------------

async def get_for_llm_async(
    url: str,
    router,
    mode: LLMInputMode = "base64",
    expires_in: int = 300,
) -> str | bytes:
    """Async version of get_for_llm()."""
    if mode == "url":
        return await router.ensure_url_async(url, expires_in=expires_in)

    raw: bytes = await router.read_url_async(url)

    if mode == "base64":
        return base64.b64encode(raw).decode()

    return raw


async def push_from_llm_async(
    data: str | bytes,
    dest_uri: str,
    router,
    source_format: LLMOutputFormat = "base64",
    **write_kwargs,
) -> bool:
    """Async version of push_from_llm()."""
    import asyncio

    raw: bytes

    if source_format == "base64":
        b64: str = data if isinstance(data, str) else data.decode()
        raw = base64.b64decode(b64)

    elif source_format == "url":
        if not isinstance(data, str):
            raise TypeError(f"source_format='url' requires a str URL, got {type(data)}")
        # The URL came from a model: never an address inside our network.
        from matrx_utils.outbound_guard import public_only_client

        async with public_only_client(timeout=60, follow_redirects=True) as client:
            response = await client.get(data)
            response.raise_for_status()
            raw = response.content

    elif source_format == "bytes":
        raw = data if isinstance(data, bytes) else data.encode()  # type: ignore[union-attr]

    else:
        raise ValueError(f"Unknown source_format: {source_format!r}")

    return await router.write_async(dest_uri, raw, **write_kwargs)
