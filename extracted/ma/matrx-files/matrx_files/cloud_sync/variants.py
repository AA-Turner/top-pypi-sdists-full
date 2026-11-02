"""Generic, encoder-injected variant primitive.

A "variant" is a derived file produced from a master ``cld_files`` row by
running an encoder over the master's bytes. Variants are themselves
``cld_files`` rows under a deterministic path so they get share links,
permissions, CDN URLs, checksum cache-busting, lifecycle policy — every
existing platform feature applies for free.

This module is intentionally encoder-agnostic. The host (or a sibling
package like matrx-ai) registers an encoder for a *family* (e.g.
``"vision"``) and a *variant key* (e.g. ``"anthropic_opus_hires"``).
matrx-utils never imports matrx-ai.

Wire shape
----------

A master file lives at::

    {master.file_path}                       (e.g. screenshots/<uuid>/master.jpg)

Its variants live alongside under a deterministic, **master-scoped** ``v/``
subfolder — the master's own ``file_id`` is part of the path so two DIFFERENT
masters that happen to share a directory can NEVER collide on one variant::

    {master_dir}/v/{master_file_id}/{variant_key}.{ext}
    (e.g. screenshots/<uuid>/v/<master_file_id>/anthropic_opus_hires.jpg)

The variant's ``cld_files.metadata`` carries::

    {
        "derived_from": "<master_file_id>",
        "variant_family": "vision",
        "variant_key": "anthropic_opus_hires",
    }

.. warning::

    The path MUST stay master-scoped. An earlier scheme keyed the variant on
    ``{master_dir}/v/{variant_key}.{ext}`` (no master identity), so every file
    sharing a directory resolved to ONE variant file. That silently served the
    FIRST master's bytes for every sibling — e.g. the Education handwriting
    grader uploads every photo into one ``system-files/image-grade/responses/``
    folder, so all their ``gemini25_default`` variants collapsed onto a single
    file and every distinct submission was graded as the first image. Keep the
    ``master_file_id`` segment, and keep the ``derived_from`` verification in
    :func:`render_variant_async` as the loud second layer.

Idempotency
-----------

``render_variant_async`` short-circuits when a variant row already exists
for the given (master_file_id, variant_key) pair. The encoder is invoked
exactly once per master+key tuple per process — re-runs are free.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable, Callable
from posixpath import dirname
from typing import TYPE_CHECKING, Any

from matrx_files.derivations import FileDerivationKind, inherit_derived_file_policy

logger = logging.getLogger(__name__)


# Encoder signature: receives master bytes + variant key, returns
# (encoded_bytes, mime_type). Encoders are pure — no I/O, no DB.
VariantEncoder = Callable[[bytes, str], "Awaitable[tuple[bytes, str]] | tuple[bytes, str]"]


# Process-level registry: family -> encoder. Hosts call register_variant_encoder()
# at startup. Lookups happen inside render_variant_async().
_ENCODERS: dict[str, VariantEncoder] = {}


def register_variant_encoder(family: str, encoder: VariantEncoder) -> None:
    """Register an encoder for a variant family.

    A "family" is a top-level namespace like ``"vision"`` (used for LLM
    image re-encoding) or ``"thumbnail"``. The encoder receives the
    master bytes plus the specific variant key and returns the encoded
    bytes plus their mime_type.

    Calling this with the same ``family`` replaces the previous encoder.
    """
    if not callable(encoder):
        raise TypeError(f"encoder for family {family!r} must be callable")
    _ENCODERS[family] = encoder
    logger.info("[variants] registered encoder for family=%s", family)


def get_variant_encoder(family: str) -> VariantEncoder | None:
    return _ENCODERS.get(family)


def has_variant_encoder(family: str) -> bool:
    return family in _ENCODERS


# ---------------------------------------------------------------------------
# Path / filename helpers
# ---------------------------------------------------------------------------

# Map common image mime_types to file extensions for variant filenames.
_MIME_TO_EXT: dict[str, str] = {
    "image/jpeg": "jpg",
    "image/jpg": "jpg",
    "image/png": "png",
    "image/webp": "webp",
    "image/gif": "gif",
    "image/heic": "heic",
}


def _ext_for_mime(mime: str) -> str:
    if not mime:
        return "bin"
    norm = mime.lower().split(";", 1)[0].strip()
    if norm in _MIME_TO_EXT:
        return _MIME_TO_EXT[norm]
    if "/" in norm:
        return norm.split("/", 1)[1]
    return "bin"


def variant_file_path(
    master_file_path: str, variant_key: str, ext: str, master_file_id: str
) -> str:
    """Build the deterministic, **master-scoped** logical path for a variant.

    Master:  ``a/b/master.jpg``  (id ``M``)
    Variant: ``a/b/v/{M}/{variant_key}.{ext}``

    For a master with no parent folder (just ``master.jpg``), the variant
    is placed at ``v/{M}/{variant_key}.{ext}``.

    ``master_file_id`` is REQUIRED and part of the path: it makes the variant
    identity globally unique per master, so two different masters that share a
    directory (e.g. many photos uploaded into one folder) can never collide on
    the same variant file. Dropping it silently serves the first master's bytes
    for every sibling — see the module docstring's warning.
    """
    master_dir = dirname(master_file_path)
    name = f"{variant_key}.{ext}"
    scoped = f"v/{master_file_id}/{name}"
    return f"{master_dir}/{scoped}" if master_dir else scoped


# ---------------------------------------------------------------------------
# Render entry points
# ---------------------------------------------------------------------------

if TYPE_CHECKING:
    from ..file_manager import FileManager


async def render_variant_async(
    fm: FileManager,
    master_file_id: str,
    *,
    variant_key: str,
    family: str = "vision",
    encoder: VariantEncoder | None = None,
) -> dict[str, Any]:
    """Resolve (or render and persist) a variant for ``master_file_id``.

    Parameters
    ----------
    fm
        A FileManager with cloud_sync configured.
    master_file_id
        The cld_files UUID for the master file.
    variant_key
        The variant identifier within the family (e.g. ``"anthropic_opus_hires"``).
    family
        The encoder family. Defaults to ``"vision"``.
    encoder
        Optional override; falls back to the family-registered encoder.

    Returns
    -------
    A dict with the resolved variant's cld_files-style fields:

        {
            "file_id": <uuid>,
            "storage_uri": "s3://...",
            "file_path": "...",
            "mime_type": "image/jpeg",
            "size_bytes": 12345,
            "url": "<signed url>",   # may be None if the router can't sign
            "is_new": False,         # True iff this call rendered the variant
            "metadata": {...},
        }

    Raises
    ------
    RuntimeError
        When no encoder is registered for ``family`` and ``encoder`` is None.
    FileNotFoundError
        When the master record cannot be found.
    """
    se = fm._require_sync_engine()
    db = se.db
    router = se.router

    master = await db.get_file_async(master_file_id)
    if not master:
        raise FileNotFoundError(f"master file_id {master_file_id} not found")

    enc = encoder or get_variant_encoder(family)
    if enc is None:
        raise RuntimeError(
            f"no variant encoder registered for family={family!r}; "
            f"call register_variant_encoder({family!r}, encoder) at startup."
        )

    master_path: str = master["file_path"]
    owner_id: str = master["owner_id"]

    # Cache probe by METADATA, not by guessing filename extensions — the old
    # 4-extension path probe (jpg/png/webp/bin) silently missed every variant
    # whose encoder produced any other extension (gif, heic, avif, tiff, ...)
    # and re-ran the encoder on each call. ``list_variants_by_master_async``
    # queries ``metadata.derived_from == master_file_id`` directly, so a hit
    # ALWAYS belongs to this master by construction (no collision check
    # needed) and the extension never matters.
    for row in await db.list_variants_by_master_async(master_file_id):
        row_meta = row.get("metadata") or {}
        if row_meta.get("variant_key") != variant_key:
            continue
        row_family = row_meta.get("variant_family")
        if row_family is not None and row_family != family:
            continue
        urls = await se.build_urls_for_record_async(row)
        return {
            "file_id": row["id"],
            "storage_uri": row["storage_uri"],
            "file_path": row["file_path"],
            "mime_type": row.get("mime_type"),
            "size_bytes": row.get("size_bytes"),
            "url": urls["url"],
            "cdn_url": urls["cdn_url"],
            "download_url": urls["download_url"],
            "is_new": False,
            "metadata": row_meta,
        }

    # Cache miss — read master bytes, run encoder, write variant row.
    master_bytes = await router.read_async(master["storage_uri"])

    # Encoders are image/PDF transforms and may be CPU-bound.  Calling a
    # synchronous encoder here used to freeze the server event loop (Pillow's
    # LANCZOS resize was observed blocking every request for >1 second).
    # Async encoders still work: invoking one in the worker returns its
    # coroutine, which is then awaited on this loop.
    raw = await asyncio.to_thread(enc, master_bytes, variant_key)
    if hasattr(raw, "__await__"):
        encoded_bytes, encoded_mime = await raw  # type: ignore[misc]
    else:
        encoded_bytes, encoded_mime = raw  # type: ignore[misc]

    ext = _ext_for_mime(encoded_mime)
    variant_path = variant_file_path(master_path, variant_key, ext, master_file_id)

    # A variant inherits the master's ACCESS CONTEXT — web lane, list filter, org, and
    # the contextual policy tags (system_artifact / artifact_domain /
    # web_site_id / …). Hand-built metadata here is what created the untagged,
    # wrong-org vision variant of a crawl screenshot (FOUND_DEFECTS E-ii).
    access, metadata = inherit_derived_file_policy(
        master,
        {
            "derived_from": master_file_id,
            "variant_family": family,
            "variant_key": variant_key,
        },
    )

    result = await se.managed_write_async(
        variant_path,
        encoded_bytes,
        mime_type=encoded_mime,
        published_to_web=access.published_to_web,
        shown_to=access.shown_to,
        user_id=owner_id,
        metadata=metadata,
        parent_file_id=master_file_id,
        derivation_kind=FileDerivationKind.VARIANT.value,
    )

    return {
        "file_id": result.file_id,
        "storage_uri": result.storage_uri,
        "file_path": variant_path,
        "mime_type": encoded_mime,
        "size_bytes": len(encoded_bytes),
        "url": result.url,
        "cdn_url": result.cdn_url,
        "download_url": result.download_url,
        "is_new": result.is_new,
        "metadata": metadata,
    }


__all__ = [
    "VariantEncoder",
    "register_variant_encoder",
    "get_variant_encoder",
    "has_variant_encoder",
    "variant_file_path",
    "render_variant_async",
]
