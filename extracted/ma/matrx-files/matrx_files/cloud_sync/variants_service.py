"""VariantsService — idempotent, variant-aware rendering.

The architectural rule (the user's stated vision):

    The server is fully file-aware and variant-aware. If the FE asks for
    a master in 5 sizes and 4 of those variants already exist, render
    only the 1 missing one and return all 5.

The contract:

    Variants are identified by ``(master_file_id, variant_key)``. The key
    wins — if a variant of the master's CURRENT version exists for that pair, we reuse it regardless of
    the requested spec (width/height/format/quality). Callers that want
    different specs MUST use different keys. The renderer logs a warning
    when the requested spec_hash does not match an existing variant so
    drift is auditable.

Variant rows are stamped with::

    metadata.derived_from        # master file_id
    metadata.variant_family      # 'image' | 'vision' | ...
    metadata.variant_key         # 'thumbnail_url' | 'og_url' | ...
    metadata.variant_spec_hash   # sha256(width|height|format|quality|fit)
    metadata.master_version      # the master's current_version it was rendered from (absent = 1)

The catalog is queried via the JSONB index on ``metadata->>derived_from``
(supabase / postgres GIN).

Public surface
--------------

::

    vs = fm.sync_engine.variants
    catalog = await vs.list_existing_async(master_record)
    rendered = await vs.render_async(
        master_record,
        variants_specs=[{"key": "thumbnail_url", "width": 400, ...}, ...],
    )
    # rendered: dict[key, AssetVariant] — existing + freshly rendered
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any

from matrx_utils import stable_hash, vcprint

from matrx_files.derivations import inherit_derived_file_policy

from .variants import _master_version, _variant_matches_master, write_variant_as_its_master

if TYPE_CHECKING:
    from .sync_engine import SyncEngine
    from ..asset_envelope import AssetVariant


def _current_catalog(master_record: dict, rows: list[dict]) -> dict[str, dict]:
    """``variant_key -> row`` for the variants rendered from the master's CURRENT version only. A master
    replaced in place keeps its old variants (an older request may still name them), but a preset is never
    served from them: the variant is rendered again, of the new bytes, on next use (AND-V IMG17 b — the same
    rule as ``render_variant_async``)."""
    version = _master_version(master_record.get("current_version"))
    out: dict[str, dict] = {}
    for row in rows:
        meta = row.get("metadata") or {}
        key = meta.get("variant_key")
        if key and _variant_matches_master(meta, version):
            out[key] = row
    return out


def _versioned_name(name: str, ext: str, master_record: dict) -> str:
    """``{name}.{ext}``, or ``{name}.v{N}.{ext}`` for a master at version N > 1 (``variant_file_path``'s rule):
    a replaced master's variant never overwrites the one an older version's readers hold."""
    version = _master_version(master_record.get("current_version"))
    return f"{name}.v{version}.{ext}" if version > 1 else f"{name}.{ext}"


def _spec_hash(spec: dict[str, Any]) -> str:
    """Deterministic hash of a variant spec for drift detection.

    Hashes over the fields that affect the rendered bytes — width, height,
    format, quality, fit. Excludes 'key' / 'suffix' (the identifier).
    """
    canonical = {
        "width": spec.get("width"),
        "height": spec.get("height"),
        "format": (spec.get("format") or "").upper() or None,
        "quality": spec.get("quality"),
        "fit": spec.get("fit"),
    }
    return stable_hash(canonical, length=16)


class VariantsService:
    """Idempotent variant rendering.

    Composed by :class:`SyncEngine`; access via ``fm.sync_engine.variants``
    or :class:`FileService.variants`.
    """

    def __init__(self, engine: SyncEngine) -> None:
        self._engine = engine

    # ------------------------------------------------------------------
    # Catalog
    # ------------------------------------------------------------------

    def list_existing(self, master_record: dict) -> dict[str, dict]:
        """Map variant_key -> cld_files row for everything derived from this master's CURRENT bytes."""
        return _current_catalog(master_record, self._engine.db.list_variants_by_master(master_record["id"]))

    async def list_existing_async(self, master_record: dict) -> dict[str, dict]:
        rows = await self._engine.db.list_variants_by_master_async(master_record["id"])
        return _current_catalog(master_record, rows)

    async def list_with_older_async(
        self, master_record: dict, *, include_deleted: bool = False
    ) -> tuple[dict[str, dict], dict[str, dict]]:
        """``(current, older)`` from one read: the current-version catalog, and per key the newest variant of an
        EARLIER version of the master. A reader that only shows (a list thumbnail) serves an older one while a
        render of the current bytes is queued — never nothing (CGU-10 AND-V IMG18 F3). ``include_deleted``: a
        trashed master's variants, which may be in the Trash with it."""
        if include_deleted:
            rows = await self._engine.db.list_variants_by_master_async(master_record["id"], include_deleted=True)
        else:
            rows = await self._engine.db.list_variants_by_master_async(master_record["id"])
        current = _current_catalog(master_record, rows)
        older: dict[str, tuple[int, dict]] = {}
        for row in rows:
            meta = row.get("metadata") or {}
            key = meta.get("variant_key")
            if not key or key in current:
                continue
            made_of = _master_version(meta.get("master_version"))
            if key not in older or made_of >= older[key][0]:
                older[key] = (made_of, row)
        return current, {key: row for key, (_, row) in older.items()}

    # ------------------------------------------------------------------
    # Render
    # ------------------------------------------------------------------

    async def render_async(
        self,
        master_record: dict,
        *,
        variants_specs: list[dict[str, Any]],
        master_bytes: bytes | None = None,
        force_rerender: bool = False,
    ) -> dict[str, AssetVariant]:
        """Idempotently materialize each requested variant for ``master_record``.

        For each spec:
        - If ``(master_id, key)`` already exists in cld_files: reuse the row.
          If the existing variant's spec_hash differs from the request, log
          a warning but still return the existing row (key wins).
        - Otherwise: render the bytes via the image handler, persist as
          a new cld_files row under ``{master_dir}/v/{suffix}.{ext}``,
          stamp metadata.

        Returns ``dict[key, AssetVariant]`` containing every requested key,
        whether reused or freshly rendered.
        """
        from ..asset_envelope import AssetVariant

        if not variants_specs:
            return {}

        # 1. Load the existing catalog once (one DB hit).
        catalog = {} if force_rerender else await self.list_existing_async(master_record)

        # 2. Partition specs by reuse vs render.
        to_render: list[dict] = []
        out: dict[str, AssetVariant] = {}

        for spec in variants_specs:
            key = spec.get("key")
            if not key:
                continue
            requested_hash = _spec_hash(spec)

            existing = catalog.get(key)
            if existing:
                existing_hash = (existing.get("metadata") or {}).get("variant_spec_hash")
                if existing_hash and existing_hash != requested_hash:
                    vcprint(
                        f"[variants] {master_record['id']}.{key}: requested "
                        f"spec_hash={requested_hash} differs from existing "
                        f"spec_hash={existing_hash} — key wins, returning "
                        f"existing variant. Use a different key for a "
                        f"different spec.",
                        color="yellow",
                    )
                out[key] = await self._existing_to_asset_variant(existing, spec)
            else:
                to_render.append({**spec, "_spec_hash": requested_hash})

        if not to_render:
            return out

        # 3. Render only the missing ones — single image-handler call.
        if master_bytes is None:
            master_bytes = await self._engine.router.read_async(master_record["storage_uri"])

        fm = self._engine.fm
        rendered = await asyncio.to_thread(
            fm.image_handler._render_variants, master_bytes,
            [{k: v for k, v in s.items() if not k.startswith("_")} for s in to_render],
        )

        # 4. Persist each rendered variant + build AssetVariants.
        # Variants land under the canonical VARIANTS system folder
        # (system-files/variants/<master_file_id>/<suffix>.<ext>) so they:
        #   - never pollute the user-namespace folder of the master
        #   - are scoped to a stable prefix per master (cleanup on master
        #     delete = one S3 ListObjects + DeleteObjects under
        #     system-files/variants/<master_id>/)
        #   - inherit the system-files retention / quota policy
        from ..system_paths import VARIANTS

        owner_id = master_record["owner_id"]

        # Re-map specs by key for spec_hash lookup post-render.
        specs_by_key = {s["key"]: s for s in to_render}

        for key, suffix, fmt, data in rendered:
            ext = "jpg" if fmt.upper() == "JPEG" else fmt.lower()
            mime = "image/jpeg" if ext == "jpg" else f"image/{ext}"
            variant_path = VARIANTS.path(master_record["id"], _versioned_name(suffix, ext, master_record))
            spec = specs_by_key.get(key, {})
            # Inherit the master's access context (web lane, list filter, org, contextual
            # policy tags) — hand-built variant metadata is the defect class
            # that produced the untagged wrong-org vision variant (E-ii).
            access, metadata = inherit_derived_file_policy(
                master_record,
                {
                    "derived_from": master_record["id"],
                    "variant_family": spec.get("variant_family", "image"),
                    "variant_key": key,
                    "variant_spec_hash": spec.get("_spec_hash") or _spec_hash(spec),
                    "master_version": _master_version(master_record.get("current_version")),
                },
            )
            # Phase 1d.3 — stamp the native lineage columns so consumers
            # can identify variant rows by data shape (parent_file_id +
            # derivation_kind) without inspecting JSONB metadata. The
            # metadata still carries the full derivation context for
            # backwards compatibility + the variant_spec_hash drift
            # check; the columns just surface the headline fact.
            result = await write_variant_as_its_master(master_record, lambda: self._engine.managed_write_async(
                variant_path,
                data,
                mime_type=mime,
                pathway="files.variant",  # placement registry: the declared automated pathway
                published_to_web=access.published_to_web,
                shown_to=access.shown_to,
                user_id=owner_id,
                metadata=metadata,
                parent_file_id=master_record["id"],
                derivation_kind="variant",
            ))
            out[key] = AssetVariant(
                key=key,
                file_id=result.file_id,
                file_path=variant_path,
                width=spec.get("width"),
                height=spec.get("height"),
                mime_type=mime,
                size_bytes=result.size_bytes,
                url=result.url,
                cdn_url=result.cdn_url,
                download_url=result.download_url,
                metadata=metadata,
            )
        return out

    # ------------------------------------------------------------------
    # Pre-rendered persistence — for kind-specific variants where the
    # bytes don't come from the image-encoder size pipeline (PDF page-1
    # renders, video poster frames, audio waveforms). Idempotent by
    # ``(master_id, variant_key)`` like ``render_async``.
    # ------------------------------------------------------------------

    async def persist_prerendered_async(
        self,
        master_record: dict,
        *,
        variant_key: str,
        content: bytes,
        mime_type: str,
        variant_family: str = "kind_specific",
        spec_hash: str | None = None,
        force_rerender: bool = False,
    ) -> AssetVariant:
        """Store pre-rendered bytes as a variant row under ``variant_key``.

        Use for variants whose content isn't an image-encoder output
        (PDF page renders, video poster frames, audio waveform PNGs).
        Idempotent: if a row already exists for
        ``(master_record["id"], variant_key)``, returns the existing
        variant without re-uploading.

        Storage layout mirrors ``render_async``: rows land under
        ``system-files/variants/<master_id>/<variant_key>.<ext>`` so
        cleanup-on-master-delete is one S3 prefix scan.
        """
        from ..asset_envelope import AssetVariant
        from ..system_paths import VARIANTS

        # Idempotency check. ``force_rerender=True`` skips the reuse and
        # overwrites the existing variant IN PLACE — same file_path, so the
        # managed write upserts the row and replaces the S3 object.
        catalog = {} if force_rerender else await self.list_existing_async(master_record)
        existing = catalog.get(variant_key)
        if existing:
            urls = await self._engine.build_urls_for_record_async(existing)
            meta = existing.get("metadata") or {}
            return AssetVariant(
                key=variant_key,
                file_id=existing["id"],
                file_path=existing["file_path"],
                mime_type=existing.get("mime_type"),
                size_bytes=existing.get("size_bytes"),
                url=urls.get("url"),
                cdn_url=urls.get("cdn_url"),
                download_url=urls.get("download_url"),
                metadata={
                    "derived_from": meta.get("derived_from"),
                    "variant_family": meta.get("variant_family"),
                    "variant_key": meta.get("variant_key"),
                    "variant_spec_hash": meta.get("variant_spec_hash"),
                },
            )

        # Pick an extension from the supplied mime. Defaults to .bin for
        # anything we don't recognize so the upload still succeeds.
        ext_map = {
            "image/jpeg": "jpg",
            "image/png": "png",
            "image/webp": "webp",
            "image/gif": "gif",
        }
        ext = ext_map.get(mime_type, mime_type.rsplit("/", 1)[-1] or "bin")
        variant_path = VARIANTS.path(master_record["id"], _versioned_name(variant_key, ext, master_record))
        # Inherit the master's access context (see render_async).
        access, metadata = inherit_derived_file_policy(
            master_record,
            {
                "derived_from": master_record["id"],
                "variant_family": variant_family,
                "variant_key": variant_key,
                "variant_spec_hash": spec_hash or _spec_hash({"key": variant_key}),
                "master_version": _master_version(master_record.get("current_version")),
            },
        )
        owner_id = master_record["owner_id"]

        # Phase 1d.3 — stamp the native lineage columns (see comment on
        # the render_async write path for rationale).
        result = await write_variant_as_its_master(master_record, lambda: self._engine.managed_write_async(
            variant_path,
            content,
            mime_type=mime_type,
            pathway="files.variant",  # placement registry: the declared automated pathway
            published_to_web=access.published_to_web,
            shown_to=access.shown_to,
            user_id=owner_id,
            metadata=metadata,
            parent_file_id=master_record["id"],
            derivation_kind="variant",
        ))
        return AssetVariant(
            key=variant_key,
            file_id=result.file_id,
            file_path=variant_path,
            mime_type=mime_type,
            size_bytes=result.size_bytes,
            url=result.url,
            cdn_url=result.cdn_url,
            download_url=result.download_url,
            metadata=metadata,
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    async def _existing_to_asset_variant(self, row: dict, spec: dict) -> AssetVariant:
        from ..asset_envelope import AssetVariant

        urls = await self._engine.build_urls_for_record_async(row)
        meta = row.get("metadata") or {}
        return AssetVariant(
            key=meta.get("variant_key") or spec.get("key", ""),
            file_id=row["id"],
            file_path=row["file_path"],
            width=spec.get("width"),
            height=spec.get("height"),
            mime_type=row.get("mime_type"),
            size_bytes=row.get("size_bytes"),
            url=urls["url"],
            cdn_url=urls["cdn_url"],
            download_url=urls["download_url"],
            metadata={
                "derived_from": meta.get("derived_from"),
                "variant_family": meta.get("variant_family"),
                "variant_key": meta.get("variant_key"),
                "variant_spec_hash": meta.get("variant_spec_hash"),
            },
        )


__all__ = ["VariantsService", "_spec_hash"]
