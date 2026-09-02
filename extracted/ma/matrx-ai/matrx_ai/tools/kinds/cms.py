"""Kinds for the ``cms_*`` tool results (the agent-facing CMS surface).

Ledger rows: `cms_asset` `cms_collection` `cms_component` `cms_data`
`cms_find_page` `cms_inspect` `cms_page` `cms_site` (KIND_TOOL_LEDGER,
agent ``lead-w2a``). NOT here: `html_page` and `cms_verify` — unclaimed rows.

WHY THESE LIVE IN THE PACKAGE WHEN THE IMPLEMENTATIONS LIVE IN AIDREAM
----------------------------------------------------------------------
The `cms_*` implementations are `aidream/tools/cms_*_tool.py`, but the ONE
declaration map (``TOOL_RESULT_KINDS``) lives here and a package may never
import aidream — so the models live here and aidream imports them (the legal
direction). Same law as the rest of this package, applied from the other side.

THE SHAPE LAW FOR A MULTIPLEXED TOOL
------------------------------------
Every `cms_*` tool is a discriminated-union dispatcher: 5–13 actions, each
with its own success payload (an entity read, a paged listing, a dry-run stub,
a delete receipt, a versions view…). One tool still gets ONE result kind — the
UNION of every action's top-level keys, everything action-specific optional —
because the tool's callers receive exactly one of these shapes per call and
``additionalProperties:false`` means a missed branch key is a validation
failure on the busy day (the trace batch's cap-keys finding, again: the cap
keys `truncated`/`truncation_notice`/`results_omitted`/… ARE part of the
shape). Placeholder tier: entity rows (site/page/component/collection/item/
asset dumps) stay opaque ``dict``s — distilling the CMS DTOs is a Stage A run,
not a stub's job.

One real type union survives honestly: `cms_page`'s single-create dry-run stub
returns ``would_create: True`` (bool) while the `create_many` batch report
returns ``would_create: <int>`` — both branches are live code, so the field is
``bool | int``.
"""

from __future__ import annotations

from pydantic import JsonValue

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind


@kind(
    "cms_asset_result",
    label="CMS Asset Result",
    family="cms",
    example={
        "asset": {"id": "a-1", "file_name": "hero.webp", "url": "https://cdn.example/x.webp"},
        "reference_url": "https://cdn.example/x.webp",
        "note": "Reference this asset in page HTML by its durable `url` above.",
    },
    # PLACEHOLDER — the outer union of the upload/list/get/update/usage/
    # versions/delete actions; the asset row itself stays an opaque dump.
    maturity="placeholder",
)
class CmsAssetResult(KindModel):
    #: Single-entity actions (upload/get/update).
    asset: dict | None = None
    #: `upload` — the durable CDN URL to reference in page HTML.
    reference_url: str | None = None
    note: str | None = None
    #: `list`.
    assets: list[dict] | None = None
    count: int | None = None
    #: `usage`, and `delete(dry_run=true)`'s live scan.
    usage: dict | None = None
    #: `versions` — summary list, or one snapshot with `version_number`.
    versions: list[dict] | None = None
    version: dict | None = None
    #: `delete` receipt (service-authored).
    success: bool | None = None
    deleted_id: str | None = None
    forced: bool | None = None
    was_in_use: bool | None = None
    #: dry-run stubs.
    dry_run: bool | None = None
    would_upload: bool | None = None
    would_update: bool | None = None
    would_delete: bool | None = None
    site_id: str | None = None
    #: `upload(dry_run)` echo of the one media reference.
    source: dict | None = None
    asset_id: str | None = None
    fields: list[str] | None = None


@kind(
    "cms_collection_result",
    label="CMS Collection Result",
    family="cms",
    example={"collection": {"id": "c-1", "slug": "contact-form"}},
    maturity="placeholder",
)
class CmsCollectionResult(KindModel):
    collection: dict | None = None
    #: `list` — page + self-cap state (`total` is pre-cap; `truncated` means
    #: rows or jsonb fields were dropped to fit the output budget).
    collections: list[dict] | None = None
    count: int | None = None
    total: int | None = None
    truncated: bool | None = None
    truncation_notice: str | None = None
    #: `versions`.
    versions: list[dict] | None = None
    version: dict | None = None
    #: `delete` receipt — soft delete, cascaded to items.
    success: bool | None = None
    deleted_id: str | None = None
    items_soft_deleted: int | None = None
    #: `restore`.
    restored: bool | None = None
    restored_from_version: int | None = None
    new_version: int | None = None
    #: `rotate_site_key`.
    rotated: bool | None = None
    site: dict | None = None
    #: dry-run stubs.
    dry_run: bool | None = None
    would_create: bool | None = None
    would_update: bool | None = None
    would_archive: bool | None = None
    would_delete: bool | None = None
    would_restore: bool | None = None
    would_rotate_site_key: bool | None = None
    site_id: str | None = None
    slug: str | None = None
    collection_id: str | None = None
    version_number: int | None = None
    fields: list[str] | None = None


@kind(
    "cms_component_result",
    label="CMS Component Result",
    family="cms",
    example={"component": {"id": "cp-1", "name": "Header", "component_type": "header"}},
    maturity="placeholder",
)
class CmsComponentResult(KindModel):
    component: dict | None = None
    components: list[dict] | None = None
    count: int | None = None
    #: `patch` — which field was patched and the hunk stats; a dry-run patch
    #: also carries the validation report (None when validation didn't run).
    field: str | None = None
    diff_stats: dict | None = None
    validation_report: dict | None = None
    #: `versions`.
    versions: list[dict] | None = None
    version: dict | None = None
    #: `delete` receipt.
    success: bool | None = None
    deleted_id: str | None = None
    #: dry-run stubs.
    dry_run: bool | None = None
    would_create: bool | None = None
    would_update: bool | None = None
    would_apply: bool | None = None
    would_delete: bool | None = None
    site_id: str | None = None
    name: str | None = None
    component_id: str | None = None
    fields: list[str] | None = None


@kind(
    "cms_data_result",
    label="CMS Data Result",
    family="cms",
    example={
        "items": [{"id": "i-1", "data": {"email": "a@b.c"}}],
        "count": 1,
        "total": 1,
        "limit": 50,
        "offset": 0,
    },
    maturity="placeholder",
)
class CmsDataResult(KindModel):
    #: `list`/`query` — one page, self-capped (`total` is the pre-cap count).
    items: list[dict] | None = None
    item: dict | None = None
    count: int | None = None
    total: int | None = None
    limit: int | None = None
    offset: int | None = None
    truncated: bool | None = None
    truncation_notice: str | None = None
    #: `delete` receipt (soft delete).
    success: bool | None = None
    deleted_id: str | None = None
    #: `stats`.
    stats: dict | None = None
    collection_id: str | None = None
    #: `export` — jsonl comes back as native rows, csv as capped text.
    format: str | None = None
    row_count: int | None = None
    byte_size: int | None = None
    rows: list[dict] | None = None
    rows_returned: int | None = None
    content: str | None = None
    content_chars: int | None = None
    content_truncated: bool | None = None
    #: dry-run stubs.
    dry_run: bool | None = None
    would_create: bool | None = None
    would_update: bool | None = None
    would_set_flags: bool | None = None
    would_delete: bool | None = None
    data_keys: list[str] | None = None
    item_id: str | None = None
    flags: dict | None = None


@kind(
    "cms_page_candidates",
    label="CMS Page Candidates",
    family="cms",
    example={
        "candidates": [{"page_id": "p-1", "route": "/pricing", "score": 0.92}],
        "count": 1,
    },
    # PLACEHOLDER — `cms_find_page`'s one action: ranked candidates, never a
    # silent best-guess.
    maturity="placeholder",
)
class CmsPageCandidates(KindModel):
    candidates: list[dict] = []
    count: int = 0


@kind(
    "cms_inspect_report",
    label="CMS Inspect Report",
    family="cms",
    example={"policy": {"default": {"profile": "default"}}, "conventions": {}},
    maturity="placeholder",
)
class CmsInspectReport(KindModel):
    #: `site` overview — the site row plus its pages and components.
    site: dict | None = None
    pages: list[dict] | None = None
    components: list[dict] | None = None
    #: `cascade` — the resolved CSS cascade report for one page.
    cascade: dict | None = None
    #: `rules` — the content-guard policy description plus the CMS conventions.
    policy: dict | None = None
    conventions: dict | None = None


@kind(
    "cms_page_result",
    label="CMS Page Result",
    family="cms",
    example={"page": {"id": "p-1", "slug": "pricing", "route": "/pricing"}},
    maturity="placeholder",
)
class CmsPageResult(KindModel):
    page: dict | None = None
    pages: list[dict] | None = None
    count: int | None = None
    #: `patch` — which field was patched and the hunk stats; a dry-run patch
    #: also carries the validation report (None when validation didn't run).
    field: str | None = None
    diff_stats: dict | None = None
    validation_report: dict | None = None
    #: `versions`.
    versions: list[dict] | None = None
    version: dict | None = None
    #: `delete` receipt.
    success: bool | None = None
    deleted_id: str | None = None
    #: `submit_exception` — the PENDING approvals-queue row.
    exception: dict | None = None
    note: str | None = None
    #: `create_many` / `publish_many` batch reports (PageBatchResult /
    #: PublishBatchResult dumps + the failed-rows-first cap keys).
    site_id: str | None = None
    site_slug: str | None = None
    requested: int | None = None
    created: int | None = None
    skipped_exists: int | None = None
    failed: int | None = None
    published: int | None = None
    would_publish: int | None = None
    skipped_no_changes: int | None = None
    remaining_candidates: int | None = None
    results: list[dict] | None = None
    results_truncated: bool | None = None
    results_omitted: int | None = None
    omitted_slugs_by_status: dict | None = None
    results_truncation_note: str | None = None
    #: dry-run stubs. `would_create` is True (bool) on the single-create stub
    #: and an int count on the batch report — both branches are live code.
    dry_run: bool | None = None
    would_create: bool | int | None = None
    would_update: bool | None = None
    would_apply: bool | None = None
    would_save_draft: bool | None = None
    #: lifecycle stubs: which transition would run (publish/discard_draft/
    #: rollback/delete).
    would_transition: str | None = None
    page_id: str | None = None
    slug: str | None = None
    fields: list[str] | None = None


@kind(
    "cms_site_result",
    label="CMS Site Result",
    family="cms",
    example={"site": {"id": "s-1", "slug": "dev-website", "name": "Dev Website"}},
    maturity="placeholder",
)
class CmsSiteResult(KindModel):
    site: dict | None = None
    sites: list[dict] | None = None
    count: int | None = None
    #: `versions`.
    versions: list[dict] | None = None
    version: dict | None = None
    #: `delete` receipt — pages are deleted with the site.
    success: bool | None = None
    deleted_id: str | None = None
    deleted_pages: int | None = None
    #: `starter_kit` (StarterKitResult dump; components are summarized to
    #: char counts + nav-token presence rather than full markup).
    site_id: str | None = None
    site_slug: str | None = None
    forced: bool | None = None
    operation: str | None = None
    global_css_chars: int | None = None
    global_css_written: bool | None = None
    global_css_replaced_chars: int | None = None
    navigation_seeded: bool | None = None
    navigation: list[dict] | None = None
    components: list[dict] | None = None
    replaced_component_ids: list[str] | None = None
    rejected_theme_properties: list[str] | None = None
    nav_token: str | None = None
    notes: list[str] | None = None
    #: `redirects` sub-actions: the ledger listing, the DB-function receipt of
    #: `redirect_record`, and the removed row from `redirect_delete`.
    redirects: list[dict] | None = None
    result: dict | None = None
    deleted: dict | None = None
    #: dry-run stubs.
    dry_run: bool | None = None
    would_create: bool | None = None
    would_update: bool | None = None
    would_delete: bool | None = None
    would_record: bool | None = None
    slug: str | None = None
    force: bool | None = None
    fields: list[str] | None = None
    from_route: str | None = None
    to_route: str | None = None
    redirect_id: str | None = None


@kind(
    "cms_html_page_result",
    label="HTML Page Result",
    family="cms",
    example={"page": {"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "title": "Landing"}, "reused": False},
    # PLACEHOLDER — the html_page quick-publish dispatcher (lead-w2f):
    # list/get/create/update/patch/promote/versions/delete, dry-run previews
    # included (the cap-keys rule — every branch key declared, optional).
    maturity="placeholder",
)
class CmsHtmlPageResult(KindModel):
    #: `list`.
    pages: list[dict] | None = None
    count: int | None = None
    total: int | None = None
    #: `get` / `create` / `update` / `patch` — the page row (content-heavy
    #: columns already stripped by the tool where they would be huge).
    page: dict | None = None
    reused: bool | None = None
    diff_stats: dict | None = None
    #: dry-run previews.
    dry_run: bool | None = None
    would_create: bool | None = None
    would_update: bool | None = None
    would_apply: bool | None = None
    would_delete: bool | None = None
    page_id: str | None = None
    fields: list[str] | None = None
    validation_report: JsonValue | None = None
    preview: dict | None = None
    #: `promote` — the W2-A bridge receipt.
    promoted: bool | None = None
    source: dict | None = None
    conversion_warnings: list[str] | None = None
    was_full_document: bool | None = None
    preview_url: str | None = None
    original_url: str | None = None
    #: `versions`.
    version: dict | None = None
    versions: list[dict] | None = None
    #: `delete`.
    deleted: bool | None = None


#: tool name → model, merged into ``TOOL_RESULT_KINDS`` by the package init.
CMS_TOOL_RESULT_KINDS: dict[str, type[KindModel]] = {
    "cms_asset": CmsAssetResult,
    "cms_collection": CmsCollectionResult,
    "cms_component": CmsComponentResult,
    "cms_data": CmsDataResult,
    "cms_find_page": CmsPageCandidates,
    "cms_inspect": CmsInspectReport,
    "cms_page": CmsPageResult,
    "cms_site": CmsSiteResult,
    "html_page": CmsHtmlPageResult,
}
