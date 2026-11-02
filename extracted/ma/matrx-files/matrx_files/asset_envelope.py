"""Asset / AssetVariant wire shape — the canonical response for media uploads.

This is the *one* response shape every media endpoint returns. The host
(or any consumer of matrx-utils) builds Asset envelopes from cld_files
rows via ``FileService.build_asset_envelope`` / the urn-minter primitive.

    Asset
    ├── file_id            master file_id (the cld_files row)
    ├── published_to_web   true = on the web (the only anonymous lane); the bytes sit behind the CDN
    ├── shown_to           list filter (only_me | my_team | everyone | everyone_on_ai_matrx | null)
    ├── folder             logical folder path (entity-aware)
    ├── preset             preset name used at write time (None for raw)
    ├── primary_key        which variant key is the canonical / "main" one
    ├── primary_url        convenience: variants[primary_key].url
    └── variants           dict[key, AssetVariant]

    AssetVariant
    ├── key                "original" | "cover" | "og" | "thumb" | ...
    ├── file_id            cld_files row for THIS variant
    ├── file_path          logical path
    ├── width / height     None for non-image variants
    ├── mime_type
    ├── file_size
    ├── url                inline-render URL — ALWAYS USABLE and DURABLE
    │                      (CDN when public, authenticated
    │                      /files/{id}/download?inline=1 otherwise)
    ├── cdn_url            permanent CDN URL when public
    └── download_url       durable attachment-disposition URL

    🚨 There is NO signed_url on any wire shape. A signed URL is a handoff,
    never an identity (common-docs/systems/files/media-durability/FEATURE.md);
    clients address files by file_id and render via the durable contract.

Lives in matrx-utils so any host (aidream or a third-party) consumes
the same envelope shape end-to-end without re-defining the contract.
"""

from __future__ import annotations

import logging
from typing import Any, Literal

from matrx_utils import VisibilityLiteral
from matrx_utils.row_access import LegacyLevelInput, ShownToLiteral
from pydantic import BaseModel, ConfigDict, Field, JsonValue


# Row-access words (access ladder T-13) are DEFINED ONCE in matrx_utils.row_access:
# ``published_to_web`` (the only anonymous lane) and ``shown_to`` (a list filter).
# ``LegacyLevelInput`` is the retiring single level word, accepted on a REQUEST only
# (transitional wire input) and reconciled by ``reconcile_row_access``; it is echoed on
# a response only as the transitional wire echo the pre-T-13 frontend still reads.



class AssetVariant(BaseModel):
    key: str = Field(..., description="Variant identifier (e.g. 'original', 'cover_url', 'og_url')")
    file_id: str
    file_path: str
    # NOTE: no `file_uri`/`storage_uri` here. The native s3://bucket/key
    # location is a server-only detail — a client can do nothing with it and
    # it must never cross a client boundary. Reference a variant by `file_id`
    # (round-trips as MediaRef.file_id) and render via `url`. Enforced by
    # scripts/audit_api_types.py (FORBIDDEN_WIRE_FIELDS).
    width: int | None = None
    height: int | None = None
    mime_type: str | None = None
    size_bytes: int | None = None
    # Durable URL contract — see SyncEngine.build_urls_for_record_async.
    url: str | None = None
    cdn_url: str | None = None
    download_url: str | None = None
    # Opaque per-variant JSON metadata echoed from the cld_files row. Typed as
    # JsonValue (typed-JSON-by-design), not Any — the shape is genuinely open.
    metadata: dict[str, JsonValue] = Field(default_factory=dict)


class Asset(BaseModel):
    file_id: str = Field(..., description="The master cld_files row id")
    published_to_web: bool = Field(
        default=False,
        description="True when the asset master is published to the web (served from the CDN).",
    )
    shown_to: ShownToLiteral | None = Field(
        default=None, description="List filter of the asset master; null follows the type's default."
    )
    visibility: VisibilityLiteral = "internal"  # T-13 transitional wire echo
    share_token: str | None = None
    share_url: str | None = None
    folder: str = Field(description="Logical folder containing the asset master.")
    preset: str | None = Field(
        default=None, description="Variant preset used when the asset was rendered."
    )
    primary_key: str = Field(
        default="original",
        description="Variant key selected as the asset's canonical representation.",
    )
    primary_url: str | None = Field(
        default=None, description="Always-usable URL for the primary variant."
    )
    variants: dict[str, AssetVariant] = Field(
        default_factory=dict,
        description="Rendered variants keyed by their stable variant identifier.",
    )
    # Metadata convenience — echoes the master row's metadata jsonb (sanitized).
    # JsonValue (typed-JSON-by-design), not Any — genuinely open shape.
    metadata: dict[str, JsonValue] = Field(
        default_factory=dict,
        description="Sanitized JSON metadata copied from the asset master row.",
    )


class FileRef(BaseModel):
    """The ONE lean, client-facing reference to a single stored file.

    This is what any client (frontend, another service, an embedded
    attachment) receives when it needs to *point at* a file — as opposed
    to the richer file-browser row (``FileRecord`` in aidream) or the
    multi-variant ``Asset`` envelope. It carries only what a client can
    actually act on:

      1. ``file_id``  — the ID. From it, everything else is fetchable, and
                        it round-trips straight back as ``MediaRef.file_id``.
      2. ``url``      — ALWAYS renderable and DURABLE (CDN when public,
                        the authenticated /files/{id}/download?inline=1
                        route otherwise). Bind to <img>/<video> directly.
      3. ``cdn_url``  — permanent public CDN URL (public files only).
      4. ``download_url`` — durable attachment-disposition URL (Download btn).
      5. display metadata the client renders: ``file_name``, ``mime_type``,
         ``size_bytes``, ``published_to_web``, ``shown_to``, ``thumbnail_url``.

    🚫 What it DELIBERATELY OMITS — the whole point of this shape:
      - ``storage_uri`` / ``file_uri`` — the native ``s3://bucket/owner/key``
        location. A client can do NOTHING with it; exposing it is pure
        info-disclosure. It is a server-only column and MUST NEVER cross a
        client boundary. Enforced at the DB (column REVOKE + a realtime
        publication that excludes it) and by ``scripts/audit_api_types.py``.
      - ``file_path`` (the virtual folder path) — belongs on the file-browser
        row, not on a bare reference; navigation shapes carry it, refs don't.
      - internals: ``owner_id``, ``checksum``, ``current_version``,
        ``parent_folder_id``, lineage/derivation fields, raw ``metadata``.

    Populate via ``SyncEngine.build_urls_for_record_async`` for the URL
    flavours — never hand-mint URLs. Lives in matrx-utils so every host
    consumes the identical contract.
    """

    file_id: str = Field(..., description="cld_files row id — the only identifier a client needs.")
    published_to_web: bool = False
    shown_to: ShownToLiteral | None = None
    visibility: VisibilityLiteral | None = None  # T-13 transitional wire echo
    file_name: str | None = None
    mime_type: str | None = None
    size_bytes: int | None = None
    url: str | None = Field(
        default=None,
        description=(
            "Always-renderable durable URL (CDN if public, the authenticated "
            "/files/{id}/download?inline=1 route otherwise)."
        ),
    )
    cdn_url: str | None = Field(default=None, description="Permanent CDN URL — public files only.")
    download_url: str | None = Field(
        default=None, description="Durable attachment-disposition URL (Download button)."
    )
    thumbnail_url: str | None = None


class AssetUploadRequest(BaseModel):
    """JSON body when uploading via multipart/form-data is not desired.

    Mostly an internal documentation aid — the endpoint uses
    multipart/form-data so the file can stream. These are the same
    field names callers pass as form fields.
    """

    preset: str = "raw"
    folder: str | None = None
    # Unstated uploads are private; publishing is always explicit.
    published_to_web: bool | None = None
    shown_to: ShownToLiteral | None = None
    visibility: LegacyLevelInput | None = None  # T-13 transitional wire input
    share_with: list[str] | None = None
    include_social_baseline: bool | None = None
    metadata: dict[str, JsonValue] | None = None


class AssetPatchRequest(BaseModel):
    """Mutate an existing asset.

    Use to:
      - publish to / take off the web (also moves the S3 object between buckets)
      - change who it is shown to in lists
      - grant new sharees
    """

    published_to_web: bool | None = None
    shown_to: ShownToLiteral | None = None
    visibility: LegacyLevelInput | None = None  # T-13 transitional wire input
    share_with: list[str] | None = None
    share_level: Literal["read", "write", "admin"] = "read"
    metadata: dict[str, JsonValue] | None = None


class AssetRenderMoreRequest(BaseModel):
    """Render additional variants for an existing asset.

    Accepts either a known preset name OR a list of custom ImageVariant
    dicts. Both paths run through the matrx-utils variants subsystem so
    each rendered variant is an idempotent cld_files row.
    """

    preset: str | None = Field(default=None, description="Known preset name")
    custom_variants: list[dict[str, Any]] | None = Field(
        default=None,
        description=(
            "Optional list of ImageVariant dicts "
            "({key, suffix, width, height, quality, format}). "
            "Merged with the preset's variants, dedup'd by key."
        ),
    )
    include_social_baseline: bool | None = None


class SubOpError(BaseModel):
    """One sub-operation failure in a combined-op response.

    Combined ops (upload+share+permissions+variants, mutate, bulk) use
    best-effort atomicity: the primary op always lands; sub-op failures
    are collected here rather than rolling everything back.
    """

    sub_op: str = Field(
        ...,
        description="Which sub-operation failed: 'share' | 'permissions' | 'variants' | 'copy' | ...",
    )
    message: str
    code: str | None = None


class ShareLinkInfo(BaseModel):
    """Share-link info returned in combined-op envelopes."""

    token: str
    url: str
    expires_at: str | None = None
    max_uses: int | None = None


class CopyInfo(BaseModel):
    """New-file info when a mutate or upload op also performs a copy_to.

    Carries the same URL flavours as AssetVariant so the FE can navigate
    directly to the new file without a second round-trip.
    """

    file_id: str
    file_path: str
    folder: str | None = None
    published_to_web: bool | None = None
    visibility: VisibilityLiteral = "personal"
    url: str | None = None
    cdn_url: str | None = None
    download_url: str | None = None


class AssetCombinedOpResponse(BaseModel):
    """Response envelope for combined-op endpoints (FE-team A.1 / A.2).

    Returned by ``POST /assets`` when ``options_json`` is set, and by
    ``PATCH /files/{id}`` when union-body fields beyond simple rename/publish
    are present. The primary op (upload / patch) always lands; sub-op failures
    appear in ``errors`` rather than aborting the whole request.
    """

    # The wire field is "copy" (FE contract). Attribute is renamed to avoid
    # shadowing BaseModel.copy(); populate-by-name keeps both forms working.
    model_config = ConfigDict(populate_by_name=True)

    asset: Asset
    share_link: ShareLinkInfo | None = None
    copy_info: CopyInfo | None = Field(default=None, alias="copy")
    errors: list[SubOpError] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# POST /assets/preview — Image Studio's no-persist render endpoint.
#
# Full Sharp.js feature parity:
#   - fit: cover | contain | inside
#   - position: 9-anchor names OR continuous focal point {x, y}
#   - background_color: hex (#ffffff / #rrggbb / #rgb / #rrggbbaa) for
#     alpha-flatten on JPEG/AVIF and for contain-fit letterbox padding
#   - format: jpeg | png | webp | avif
#   - quality: 1..100 (ignored for png)
#
# The renderer (ImageHandler.render_studio_variant) honors all of these
# already; these Pydantic models advertise the surface in OpenAPI so the
# FE types are accurate.
# ---------------------------------------------------------------------------


PreviewFit = Literal["cover", "contain", "inside"]
PreviewFormat = Literal["jpeg", "png", "webp", "avif"]
PreviewAnchor = Literal[
    "center",
    "top",
    "bottom",
    "left",
    "right",
    "top-left",
    "top-right",
    "bottom-left",
    "bottom-right",
    "entropy",
    "attention",
]


class FocalPoint(BaseModel):
    """Continuous focal point — normalized [0..1] coordinates from the
    top-left of the source. Used with fit='cover' to crop around a
    user-chosen point of interest rather than a named anchor."""

    x: float = Field(..., ge=0.0, le=1.0, description="0=left, 1=right")
    y: float = Field(..., ge=0.0, le=1.0, description="0=top, 1=bottom")


class PreviewVariantSpec(BaseModel):
    """One target render for POST /assets/preview.

    Mirrors ``ImageHandler.StudioRenderSpec`` — every field is reachable
    by the renderer. The discriminated union on ``position`` lets the FE
    pass either a named anchor (including the smart-crop modes
    ``entropy`` / ``attention``) or a continuous focal point.
    """

    preset_id: str = Field(
        ..., description="Stable id echoed in the response (used as preset_id in render output)"
    )
    width: int = Field(..., gt=0)
    height: int = Field(..., gt=0)
    format: PreviewFormat = "webp"
    quality: int = Field(85, ge=1, le=100, description="Ignored for png")
    fit: PreviewFit = "cover"
    position: PreviewAnchor | FocalPoint = Field(
        default="center",
        description=(
            "Used when fit='cover'. Pass a named anchor string or "
            "{x, y} focal point. 'entropy' / 'attention' are smart-crop "
            "modes (energy-based, face-based)."
        ),
    )
    background_color: str = Field(
        default="#ffffff",
        description=(
            "Hex color (#rgb / #rrggbb / #rrggbbaa). Used to flatten "
            "alpha on jpeg/avif outputs and to pad letterbox when "
            "fit='contain' / 'inside'."
        ),
    )


class PreviewSource(BaseModel):
    """The source bytes for /assets/preview.

    Pass a MediaRef-shaped dict to render bytes already stored in
    cld_files. The multipart variant of the endpoint takes the bytes
    directly as ``file`` and ignores this shape.
    """

    file_id: str | None = None
    url: str | None = None
    file_uri: str | None = None


class AssetPreviewRequest(BaseModel):
    """Request body for POST /assets/preview."""

    source: PreviewSource
    variants: list[PreviewVariantSpec]
    max_inline_bytes: int = Field(
        default=256 * 1024,
        ge=1024,
        description=(
            "Renders below this size return as base64 data_url; larger "
            "renders return a 5-minute ephemeral_url (row-less scratch — "
            "the ONLY lawful expiring URL shape; see render_urls.py)."
        ),
    )


class AssetPreviewVariant(BaseModel):
    """One rendered preview variant in the response.

    Field names mirror ``ImageHandler.StudioRenderResult`` so the wire
    contract is consistent end-to-end.
    """

    preset_id: str = Field(..., description="Echoed from the request spec")
    width: int
    height: int
    format: PreviewFormat
    quality: int | None = Field(default=None, description="None when format='png'")
    size: int = Field(..., description="Encoded byte length")
    fit: PreviewFit | None = None
    position: PreviewAnchor | FocalPoint | None = Field(
        default=None,
        description="Echoed when fit='cover'. None for contain/inside.",
    )
    notes: list[str] = Field(
        default_factory=list,
        description=(
            "Soft warnings (e.g. 'anchor entropy unsupported, used center', "
            "'exif-transpose failed'). Empty when nothing notable."
        ),
    )
    # Exactly one of the next two is populated, gated by max_inline_bytes.
    data_url: str | None = Field(
        default=None, description="base64 data URL when size <= max_inline_bytes"
    )
    ephemeral_url: str | None = Field(
        default=None,
        description=(
            "Short-lived URL for row-less preview scratch when "
            "size > max_inline_bytes. Expires by design (expires_in); "
            "NEVER persist or pass along — re-render instead."
        ),
    )
    expires_in: int | None = Field(
        default=None,
        description="Seconds (with ephemeral_url). 300 = 5-minute TTL.",
    )
    # Optional per-variant error — present instead of size/data_url when render fails.
    error: str | None = None


class AssetPreviewResponse(BaseModel):
    """Response from POST /assets/preview — no-persist variant rendering."""

    variants: list[AssetPreviewVariant]


class AssetPdfCompressResponse(BaseModel):
    """Response from POST /assets/pdf-compress — no-persist compression."""

    original_size: int
    compressed_size: int
    reduction_ratio: float = Field(..., description="0.0..1.0 — fraction of bytes saved")
    mime_type: str = "application/pdf"
    data_url: str | None = None
    ephemeral_url: str | None = Field(
        None,
        description=(
            "Short-lived URL for the row-less compressed output. Expires by "
            "design (expires_in); NEVER persist or pass along."
        ),
    )
    expires_in: int | None = Field(
        None, description="Seconds until ephemeral_url expires (ephemeral mode only)."
    )
    # Tier metadata from the capped compression run — lets callers report
    # which tier actually produced the bytes and whether a max_size cap held.
    level_requested: int | None = None
    level_used: int | None = Field(
        None,
        description="Compression tier that produced the output (may exceed the requested tier when a size cap forces escalation).",
    )
    cap_satisfied: bool | None = Field(
        None,
        description="True when max_size_bytes was met (or no cap given); False when even the max tier exceeded it.",
    )
    strategy_used: str | None = Field(
        None, description='"inplace" or "raster" — which compression path produced the output.'
    )


class PresetVariantSummary(BaseModel):
    """One variant inside a preset, as listed by GET /assets/presets."""

    key: str
    width: int | None = None
    height: int | None = None
    format: str | None = None


class PresetSummary(BaseModel):
    """One preset, as listed by GET /assets/presets."""

    name: str
    primary_key: str
    include_baseline: bool
    variants: list[PresetVariantSummary]


class PresetsResponse(BaseModel):
    """Response from GET /assets/presets — drives the FE preset picker."""

    presets: list[PresetSummary]
    social_baseline: list[PresetVariantSummary]


class BulkOperationResult(BaseModel):
    """One row's result inside a BulkOperationResponse."""

    file_id: str
    success: bool
    error: str | None = None


class BulkOperationResponse(BaseModel):
    """Response from POST /files/bulk (discriminator: move|delete|restore|publish|share)."""

    op: str
    total: int
    succeeded: int
    failed: int
    results: list[BulkOperationResult]


__all__ = [
    "AssetVariant",
    "Asset",
    "AssetUploadRequest",
    "AssetPatchRequest",
    "AssetRenderMoreRequest",
    "SubOpError",
    "ShareLinkInfo",
    "CopyInfo",
    "AssetCombinedOpResponse",
    "AssetPreviewVariant",
    "AssetPreviewResponse",
    "AssetPdfCompressResponse",
    "PresetVariantSummary",
    "PresetSummary",
    "PresetsResponse",
    "BulkOperationResult",
    "BulkOperationResponse",
]
