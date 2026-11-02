"""Internal implementation of FileManager.resolve_media + resolve_media_async.

Kept in its own module so ``file_manager.py`` stays focused on file I/O.
The public entry points are ``FileManager.resolve_media`` and
``FileManager.resolve_media_async``; the functions here are imported
lazily from those methods.

Resolution order (the same for sync + async):

  1. ``ref.is_resolved`` → return immediately. Idempotency guarantee.
  2. ``ref.file_id`` set → DB lookup → byte-cache check → S3 read or
     presigned URL mint.
  3. ``ref.url`` set → URL classification → if ours: DB → cache → S3;
     if external: pass through (caller fetches if needed).
  4. ``ref.file_uri`` set → if it's an S3 URI we own, treat like (3);
     otherwise leave as-is for provider-native handling.

Always sets ``ref.is_resolved = True`` on a successful pass.
On failure, sets ``ref.resolver_error`` and leaves the rest untouched
so the caller can decide whether to fail loudly or fall back.
"""

from __future__ import annotations

import base64
import logging
import mimetypes
import re
from typing import TYPE_CHECKING

from .byte_cache import get_byte_cache
from .url_resolver import classify_url, resolve_file_url, resolve_file_url_async


# External-URL pre-fetch policy. We mirror what every LLM provider would
# accept inline, with hard limits that prevent a malicious / oversized
# URL from chewing up worker memory or wall time. Fetched bytes go onto
# the MediaRef as base64; this is the only way to keep the per-provider
# serialisers fully sync (no I/O) and the event loop unblocked.
_EXTERNAL_FETCH_TIMEOUT_SECONDS: float = 30.0
_EXTERNAL_FETCH_MAX_BYTES: int = 50 * 1024 * 1024  # 50 MB

if TYPE_CHECKING:
    from ..file_manager import FileManager
    from .media_ref import MediaRef


logger = logging.getLogger(__name__)


def _guess_mime(path_or_url: str | None) -> str | None:
    if not path_or_url:
        return None
    return mimetypes.guess_type(path_or_url)[0]


def _is_short_circuit(ref: "MediaRef") -> bool:
    """Return True iff the ref is already resolved or has no identifier."""
    if ref.is_resolved:
        return True
    if not ref.has_identifier():
        ref.resolver_error = "no_identifier"
        return True
    return False


def _populate_from_resolved_file(ref: "MediaRef", rec) -> None:
    """Copy canonical metadata from a ResolvedFile onto the MediaRef."""
    if rec.file_id:
        ref.file_id = rec.file_id
    if rec.owner_id:
        ref.owner_id = rec.owner_id
    if rec.file_size is not None:
        ref.file_size = rec.file_size
    if rec.mime_type:
        ref.mime_type = rec.mime_type   # canonical; client claim is overruled
    if rec.is_ours:
        ref.is_ours = True


# =============================================================================
# THE ACCESS GATE — the single place file access is authorized on the media path
# =============================================================================
#
# resolve_media is the one funnel every media reference (chat attachments,
# preview sources, tool media, agent media) passes through to become bytes.
# Enforcement lives HERE so no caller can forget it:
#
#   * The requesting user is read from the ambient request context
#     (``get_active_user_id`` — aidream wires it to AppContext). A user cannot
#     "forget" to pass it; it rides the request.
#   * With a user present, the file must be OWNED by them, PUBLIC, or SHARED
#     with them (owner → public → grant → folder inheritance, via the same
#     PermissionsManager the /files/{id} download path uses).
#   * A valid SHARE TOKEN is itself the authorization (capability-based) — the
#     URL resolver already validated it, so we trust ``is_share_link``.
#   * A raw user-supplied native cloud path is REFUSED — users
#     reference files by id, never by raw storage location.
#   * NO request context at all ⇒ an internal/background job (RAG, thumbnails,
#     cron) — but it is trusted ONLY when it declares itself with the explicit
#     marker ``matrx_utils.ctx.system_file_access("<reason>")``. Without the
#     marker the gate is fail-CLOSED: it DENIES with a loud self-identifying
#     banner (matrx_validation_gate style) so a missed internal call site
#     SCREAMS instead of silently getting an unscoped read. (2026-07-09)
#   * A request context that carries NO user (an ANONYMOUS HTTP request — no JWT,
#     no fingerprint) is DENIED. It has no identity, so it may not read an
#     owned file by id. This closes the fail-open where an anonymous caller hit
#     a media-accepting route (e.g. /pdf/*) with another user's file_id and the
#     "no user ⇒ trusted" bypass served the bytes. (2026-07-09)
#
# Returns a resolver_error string to stamp on the ref when denied, else None.

# Sentinel: get_active_context() returned None ⇒ there is NO request in flight
# ⇒ internal/background job. Distinct from "context present but user_id empty"
# (anonymous HTTP request), which must be DENIED.
_TRUSTED_INTERNAL = object()


def _authorized_actor_uid_or_deny():
    """Resolve the requesting identity for the access gate.

    Returns ``_TRUSTED_INTERNAL`` when there is no active request context at all
    (an internal/background job — trusted); otherwise the request's ``user_id``
    (``""`` for an anonymous request, which the gate denies for owned files)."""
    from matrx_utils.ctx import get_active_context

    ctx = get_active_context()
    if ctx is None:
        return _TRUSTED_INTERNAL
    return getattr(ctx, "user_id", None) or ""


def _no_context_system_or_deny(ref: MediaRef) -> str | None:
    """No request context at all: allow ONLY with the explicit system marker."""
    from matrx_utils.ctx import get_system_file_access_reason

    reason = get_system_file_access_reason()
    if reason:
        logger.debug(
            "resolve_media access gate: system access '%s' (file_id=%s)",
            reason, ref.file_id,
        )
        return None

    banner = (
        "\n" + "=" * 78 + "\n"
        "🚨 MATRX VALIDATION GATE — resolve_media ACCESS GATE (fail-closed)\n"
        + "=" * 78 + "\n"
        f"A media resolution reached the access gate with NO request context and NO\n"
        f"explicit system-access marker (file_id={ref.file_id!r},\n"
        f"url={getattr(ref, 'url', None)!r}, file_uri={getattr(ref, 'file_uri', None)!r}).\n"
        "The server bypasses RLS, so an unmarked no-user read would be an UNSCOPED\n"
        "read of any user's file. DENYING (resolver_error='access_denied_no_actor').\n\n"
        "How to fix:\n"
        "  * Request path: the AppContext was lost — restore it (set_app_context\n"
        "    after with_overrides; see aidream/CLAUDE.md 'Request context').\n"
        "  * Genuinely-internal job resolving a SERVER-constructed ref: wrap the call —\n"
        "        from matrx_utils.ctx import system_file_access\n"
        "        with system_file_access('<job-name>'):\n"
        "            await fm.resolve_media_async(ref, ...)\n"
        "Contract: packages/matrx-utils/matrx_utils/file_handling/FEATURE.md\n"
        + "=" * 78
    )
    try:
        from matrx_utils import vcprint
        vcprint(banner, color="red")
    except Exception:
        pass
    logger.error(
        "matrx_validation_gate: resolve_media denied — no request context and no "
        "system_file_access marker (file_id=%s)", ref.file_id,
    )
    return "access_denied_no_actor"


def _authorized_or_error_sync(fm: "FileManager", ref: "MediaRef", *, is_share_link: bool) -> str | None:
    if is_share_link:
        return None  # a valid share token IS the authorization (even anonymous)
    actor_uid = _authorized_actor_uid_or_deny()
    if actor_uid is _TRUSTED_INTERNAL:
        return _no_context_system_or_deny(ref)  # fail-CLOSED unless explicitly marked
    if not actor_uid:
        return "access_denied"  # request context but NO user = anonymous HTTP → deny
    if ref.file_id:
        try:
            fm._sync_engine.permissions.require("file", ref.file_id, "read", actor_uid)
            return None
        except PermissionError:
            return "access_denied"
    return "access_denied_raw_uri"  # user handed us a raw storage path — never allowed


async def _authorized_or_error_async(fm: "FileManager", ref: "MediaRef", *, is_share_link: bool) -> str | None:
    if is_share_link:
        return None  # a valid share token IS the authorization (even anonymous)
    actor_uid = _authorized_actor_uid_or_deny()
    if actor_uid is _TRUSTED_INTERNAL:
        return _no_context_system_or_deny(ref)  # fail-CLOSED unless explicitly marked
    if not actor_uid:
        return "access_denied"  # request context but NO user = anonymous HTTP → deny
    if ref.file_id:
        try:
            await fm._sync_engine.permissions.require_async("file", ref.file_id, "read", actor_uid)
            return None
        except PermissionError:
            return "access_denied"
    return "access_denied_raw_uri"  # user handed us a raw storage path — never allowed


# =============================================================================
# Sync
# =============================================================================


def _carry_file_name(ref: "MediaRef", rec: dict) -> None:
    """Keep the file's own name beside its bytes (``metadata.file_name``).

    A model reading five attachments must be able to tell which block is which
    file; provider serializers title documents from it and conversion notices
    name it (real test PB-05, 2026-10-18). First write wins, so a later variant
    re-resolve never renames the original.
    """
    name = rec.get("file_name")
    if not isinstance(name, str) or not name.strip():
        return
    try:
        if not (ref.metadata or {}).get("file_name"):
            ref.metadata = {**(ref.metadata or {}), "file_name": name}
    except Exception:  # noqa: BLE001 — a name is a courtesy; never fail resolution over it
        return


def _resolve_media_sync(fm: "FileManager", ref: "MediaRef", *, needs_bytes: bool,
                        presigned_ttl_seconds: int) -> "MediaRef":
    if _is_short_circuit(ref):
        return ref
    if fm._sync_engine is None:
        ref.resolver_error = "cloud_sync_unavailable"
        return ref

    cache = get_byte_cache()
    row_version = row_size = row_file_id = None
    db = fm._sync_engine.db
    router = fm._sync_engine._router

    storage_uri: str | None = ref.file_uri if (ref.file_uri or "").startswith("s3://") else None
    is_share_link = False  # set true only when the ref resolved via a valid /share/<token>

    # ------------------------------------------------------------------
    # 1. file_id path: direct DB lookup
    # ------------------------------------------------------------------
    if ref.file_id:
        try:
            rec = db.get_file(ref.file_id)
        except Exception as e:
            ref.resolver_error = f"db_lookup_failed: {type(e).__name__}: {e}"
            return ref
        if not rec:
            ref.resolver_error = "file_not_found"
            return ref
        ref.is_ours = True
        ref.owner_id = rec.get("owner_id")
        if rec.get("mime_type"):
            ref.mime_type = rec["mime_type"]
        ref.file_size = rec.get("size_bytes")
        storage_uri = rec.get("storage_uri")
        _carry_file_name(ref, rec)
        row_version, row_size = rec.get("current_version"), rec.get("size_bytes")
        row_file_id = ref.file_id

    # ------------------------------------------------------------------
    # 2. url path: classify + DB lookup
    # ------------------------------------------------------------------
    elif ref.url and not storage_uri:
        info = classify_url(ref.url)
        if info.get("is_ours"):
            resolved = resolve_file_url(ref.url, db)
            if resolved.error:
                ref.resolver_error = resolved.error
                # Still mark is_ours so downstream doesn't try a blind fetch.
                ref.is_ours = True
                return ref
            _populate_from_resolved_file(ref, resolved)
            storage_uri = resolved.storage_uri
            is_share_link = resolved.is_share_link
        else:
            # External URL — leave alone; provider will fetch if it can.
            ref.is_resolved = True
            return ref

    # ------------------------------------------------------------------
    # 2b. ACCESS GATE — authorize before any cache hit / byte read / presign.
    # ------------------------------------------------------------------
    if ref.file_id or storage_uri:
        _deny = _authorized_or_error_sync(fm, ref, is_share_link=is_share_link)
        if _deny:
            ref.resolver_error = _deny
            return ref

    # ------------------------------------------------------------------
    # 3. Cache hit?
    # ------------------------------------------------------------------
    if needs_bytes and ref.file_id:
        same_row = ref.file_id == row_file_id
        cached = cache.get(
            ref.file_id,
            version=row_version if same_row else None,
            size_bytes=row_size if same_row else None,
        )
        if cached is not None:
            ref.base64_data = base64.b64encode(cached.bytes_).decode("ascii")
            if cached.mime_type and not ref.mime_type:
                ref.mime_type = cached.mime_type
            ref.file_size = cached.file_size
            ref.is_resolved = True
            logger.info("resolve_media: cache hit file_id=%s mime=%s bytes=%d",
                        ref.file_id, ref.mime_type, cached.file_size)
            return ref

    # ------------------------------------------------------------------
    # 4. Bytes via cloud_sync read
    # ------------------------------------------------------------------
    if needs_bytes and storage_uri:
        try:
            content = router.read(storage_uri)
        except Exception as e:
            ref.resolver_error = f"cloud_read_failed: {type(e).__name__}: {e}"
            return ref
        ref.base64_data = base64.b64encode(content).decode("ascii")
        if not ref.mime_type:
            ref.mime_type = _guess_mime(ref.file_id) or "application/octet-stream"
        ref.file_size = len(content)
        ref.is_resolved = True
        cache.put(ref.file_id, bytes_=content, mime_type=ref.mime_type,
                  owner_id=ref.owner_id, file_path=None,
                  version=row_version if ref.file_id == row_file_id else None)
        logger.info("resolve_media: cloud read file_id=%s mime=%s bytes=%d",
                    ref.file_id, ref.mime_type, len(content))
        return ref

    # ------------------------------------------------------------------
    # 5. URL form: mint a fresh presigned URL
    # ------------------------------------------------------------------
    if storage_uri:
        try:
            presigned = router.get_url(storage_uri, expires_in=presigned_ttl_seconds)
            ref.resolved_url = presigned
            ref.is_resolved = True
            return ref
        except Exception as e:
            ref.resolver_error = f"presign_failed: {type(e).__name__}: {e}"
            return ref

    # No storage_uri and we don't need bytes — leave the ref as-is.
    ref.is_resolved = True
    return ref


# =============================================================================
# Async
# =============================================================================


async def _resolve_media_async_impl(fm: "FileManager", ref: "MediaRef", *,
                                     needs_bytes: bool, presigned_ttl_seconds: int) -> "MediaRef":
    if _is_short_circuit(ref):
        return ref
    if fm._sync_engine is None:
        ref.resolver_error = "cloud_sync_unavailable"
        return ref

    cache = get_byte_cache()
    row_version = row_size = row_file_id = None
    db = fm._sync_engine.db
    router = fm._sync_engine._router

    storage_uri: str | None = ref.file_uri if (ref.file_uri or "").startswith("s3://") else None
    is_share_link = False  # set true only when the ref resolved via a valid /share/<token>

    if ref.file_id:
        try:
            rec = await db.get_file_async(ref.file_id)
        except Exception as e:
            ref.resolver_error = f"db_lookup_failed: {type(e).__name__}: {e}"
            return ref
        if not rec:
            ref.resolver_error = "file_not_found"
            return ref
        ref.is_ours = True
        ref.owner_id = rec.get("owner_id")
        if rec.get("mime_type"):
            ref.mime_type = rec["mime_type"]
        ref.file_size = rec.get("size_bytes")
        storage_uri = rec.get("storage_uri")
        _carry_file_name(ref, rec)
        row_version, row_size = rec.get("current_version"), rec.get("size_bytes")
        row_file_id = ref.file_id

    elif ref.url and not storage_uri:
        info = classify_url(ref.url)
        if info.get("is_ours"):
            # Async DB lookup — no thread-pool dispatch, loop never blocks.
            resolved = await resolve_file_url_async(ref.url, db)
            if resolved.error:
                ref.resolver_error = resolved.error
                ref.is_ours = True
                return ref
            _populate_from_resolved_file(ref, resolved)
            storage_uri = resolved.storage_uri
            is_share_link = resolved.is_share_link
        else:
            # External URL — pre-fetch bytes here when the caller wants
            # bytes, so per-provider serialisers stay sync-only and the
            # event loop never blocks on a downstream HTTP fetch. The
            # resolved bytes also go into the byte cache (keyed by URL
            # hash) so repeated requests within ~10 minutes hit memory.
            if needs_bytes:
                await _fetch_external_url_into_ref(ref)
                # _fetch_external_url_into_ref always sets is_resolved
                # (success → with bytes; failure → with resolver_error).
            else:
                ref.is_resolved = True
            return ref

    # ------------------------------------------------------------------
    # ACCESS GATE — authorize before variant render / cache hit / byte read /
    # presign. (Placed before the variant pivot so we never render a variant
    # of a file the requesting user isn't allowed to touch.)
    # ------------------------------------------------------------------
    if ref.file_id or storage_uri:
        _deny = await _authorized_or_error_async(fm, ref, is_share_link=is_share_link)
        if _deny:
            ref.resolver_error = _deny
            return ref

    # ------------------------------------------------------------------
    # Variant pivot: when ``ref.vision_class`` is set AND we resolved a
    # master cld_files row, swap ``storage_uri`` / ``file_id`` /
    # ``mime_type`` / ``file_size`` to the variant. The cache + read
    # paths below then operate on the variant's bytes, not the master.
    # No-op if no encoder for the family is registered (matrx-utils used
    # standalone, e.g.) — falls back to serving the master.
    # ------------------------------------------------------------------
    vision_class = getattr(ref, "vision_class", None)
    if vision_class and ref.file_id and storage_uri:
        from .variants import has_variant_encoder, render_variant_async
        if has_variant_encoder("vision"):
            try:
                variant_info = await render_variant_async(
                    fm, ref.file_id,
                    variant_key=vision_class,
                    family="vision",
                )
            except Exception as e:
                ref.resolver_error = f"variant_render_failed: {type(e).__name__}: {e}"
                return ref
            ref.file_id = variant_info["file_id"]
            storage_uri = variant_info["storage_uri"]
            if variant_info.get("mime_type"):
                ref.mime_type = variant_info["mime_type"]
            if variant_info.get("size_bytes") is not None:
                ref.file_size = variant_info["size_bytes"]
        else:
            logger.warning(
                "resolve_media_async: vision_class=%s set but no encoder "
                "registered for family='vision'; serving master bytes.",
                vision_class,
            )

    if needs_bytes and ref.file_id:
        same_row = ref.file_id == row_file_id
        cached = cache.get(
            ref.file_id,
            version=row_version if same_row else None,
            size_bytes=row_size if same_row else None,
        )
        if cached is not None:
            ref.base64_data = base64.b64encode(cached.bytes_).decode("ascii")
            if cached.mime_type and not ref.mime_type:
                ref.mime_type = cached.mime_type
            ref.file_size = cached.file_size
            ref.is_resolved = True
            logger.info("resolve_media_async: cache hit file_id=%s mime=%s bytes=%d",
                        ref.file_id, ref.mime_type, cached.file_size)
            return ref

    if needs_bytes and storage_uri:
        try:
            content = await router.read_async(storage_uri)
        except Exception as e:
            ref.resolver_error = f"cloud_read_failed: {type(e).__name__}: {e}"
            return ref
        ref.base64_data = base64.b64encode(content).decode("ascii")
        if not ref.mime_type:
            ref.mime_type = _guess_mime(ref.file_id) or "application/octet-stream"
        ref.file_size = len(content)
        ref.is_resolved = True
        cache.put(ref.file_id, bytes_=content, mime_type=ref.mime_type,
                  owner_id=ref.owner_id, file_path=None,
                  version=row_version if ref.file_id == row_file_id else None)
        logger.info("resolve_media_async: cloud read file_id=%s mime=%s bytes=%d",
                    ref.file_id, ref.mime_type, len(content))
        return ref

    if storage_uri:
        try:
            presigned = await router.get_url_async(storage_uri, expires_in=presigned_ttl_seconds)
            ref.resolved_url = presigned
            ref.is_resolved = True
            return ref
        except Exception as e:
            ref.resolver_error = f"presign_failed: {type(e).__name__}: {e}"
            return ref

    ref.is_resolved = True
    return ref


# =============================================================================
# External URL pre-fetch (async, non-blocking)
# =============================================================================
#
# Why this exists:
#   1. Per-provider serialisers in matrx-ai (DocumentContent.to_google et al.)
#      MUST stay sync — they're called from inside the async provider client
#      and any sync I/O there blocks the event loop for the duration of the
#      HTTP fetch (often seconds).
#   2. The boundary normalizer is the ONE place where we can do this fetch
#      without blocking, so we do it here. After this call, every MediaRef
#      with an external URL has either base64_data set (success) or
#      resolver_error set (failure with a clear reason).
#   3. Pre-fetching also gives us:
#        - Consistent caching (URL-hash key in the byte cache)
#        - Token / size insight upfront
#        - Resilience: a 404 surfaces at our boundary, not at provider time
#        - Predictable behavior across providers (Google REQUIRES bytes;
#          OpenAI / Anthropic accept URLs natively, but bytes always work).


async def _fetch_external_url_into_ref(ref: "MediaRef") -> None:
    """Download an external URL into ``ref.base64_data``.

    Sets ``ref.is_resolved`` on every exit path. On failure, also sets
    ``ref.resolver_error`` with a short reason string. Never raises.

    Cache key for external URLs is ``url:<sha256(url)[:32]>`` so we can
    use the existing byte cache without colliding with file_id keys.
    """
    from matrx_utils import hash_text

    cache = get_byte_cache()
    url_key = "url:" + hash_text(ref.url, length=32)

    cached = cache.get(url_key)
    if cached is not None:
        ref.base64_data = base64.b64encode(cached.bytes_).decode("ascii")
        if cached.mime_type and not ref.mime_type:
            ref.mime_type = cached.mime_type
        ref.file_size = cached.file_size
        ref.is_resolved = True
        logger.info("resolve_media_async: external cache hit url=%s mime=%s bytes=%d",
                    ref.url[:80], ref.mime_type, cached.file_size)
        return

    try:
        import httpx
    except ImportError:
        ref.resolver_error = "external_fetch_unavailable: httpx not installed"
        ref.is_resolved = True
        return

    from matrx_utils.outbound_guard import OutboundUrlRefused, public_only_client

    try:
        # A genuinely external URL (ours never reach here — they are read from
        # storage): every hop must be a public address, pinned to the checked IP.
        async with public_only_client(
            timeout=_EXTERNAL_FETCH_TIMEOUT_SECONDS,
            follow_redirects=True,
            headers={"User-Agent": "matrx-utils/cloud-sync (+https://aimatrx.com)"},
        ) as client:
            # Stream the response so we can enforce the size cap without
            # buffering an oversized download in memory first.
            async with client.stream("GET", ref.url) as resp:
                if resp.status_code >= 400:
                    ref.resolver_error = (
                        f"external_fetch_http_{resp.status_code}: "
                        f"{resp.reason_phrase or 'request failed'}"
                    )
                    ref.is_resolved = True
                    return

                # Server-declared content-type wins over the client hint when
                # we're fetching from an external URL we don't control.
                ctype = resp.headers.get("content-type", "")
                if ctype:
                    # Strip "; charset=utf-8" tails.
                    ref.mime_type = ctype.split(";", 1)[0].strip().lower()

                chunks: list[bytes] = []
                received = 0
                async for chunk in resp.aiter_bytes(chunk_size=64 * 1024):
                    received += len(chunk)
                    if received > _EXTERNAL_FETCH_MAX_BYTES:
                        ref.resolver_error = (
                            f"external_fetch_too_large: > "
                            f"{_EXTERNAL_FETCH_MAX_BYTES // (1024 * 1024)} MB"
                        )
                        ref.is_resolved = True
                        return
                    chunks.append(chunk)

                content = b"".join(chunks)
    except OutboundUrlRefused as e:
        ref.resolver_error = f"external_fetch_refused: {e}"
        ref.is_resolved = True
        logger.warning("resolve_media_async: external fetch REFUSED url=%s: %s", ref.url[:80], e)
        return
    except httpx.TimeoutException:
        ref.resolver_error = (
            f"external_fetch_timeout: > {_EXTERNAL_FETCH_TIMEOUT_SECONDS}s"
        )
        ref.is_resolved = True
        return
    except httpx.HTTPError as e:
        ref.resolver_error = f"external_fetch_failed: {type(e).__name__}: {e}"
        ref.is_resolved = True
        return
    except Exception as e:
        # Defensive — never let a fetch bug propagate up to the request.
        ref.resolver_error = f"external_fetch_unexpected: {type(e).__name__}: {e}"
        ref.is_resolved = True
        return

    ref.base64_data = base64.b64encode(content).decode("ascii")
    if not ref.mime_type:
        ref.mime_type = _guess_mime(ref.url) or "application/octet-stream"
    ref.file_size = len(content)
    ref.is_resolved = True

    # Cache by URL hash so a second reference within TTL hits memory.
    cache.put(
        url_key,
        bytes_=content,
        mime_type=ref.mime_type,
        owner_id=None,
        file_path=None,
    )
    logger.info("resolve_media_async: external fetch url=%s mime=%s bytes=%d",
                ref.url[:80], ref.mime_type, len(content))


__all__ = ["_resolve_media_sync", "_resolve_media_async_impl"]
