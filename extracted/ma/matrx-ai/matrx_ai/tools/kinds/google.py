"""Kinds for the two Google agent tools — ``google_workspace`` · ``google_marketing``.

ONE union kind per tool, the ``cms_*`` / ``topical_map`` precedent: an
action-dispatched tool returns one shape whose branch-only keys are optional,
and every branch validates against it before the result leaves the tool
(a key the kind does not declare is a TOOL DEFECT, never an untyped
pass-through).

* ``google_workspace_result`` — Docs, Sheets, the prepared (never sent) email,
  and the read/import halves of Calendar, Contacts and Tasks. Promoted from the
  placeholder tier on 2026-09-17 when the tool was rebuilt to the convention
  (``common-docs/projects/google-native/PLAN.md`` §5.8): every mutating action
  gained ``dry_run``, so the kind now declares the PREVIEW branches too — the
  block an append would land and where, the cells a write would replace, the
  fields an import would mint, the field map a contact import would apply, and
  which of a task set is already here.
* ``google_marketing_result`` — the six read-only marketing reads. Every branch
  carries ``source`` (persisted vs live Google), the ``bounds`` it was asked
  for, and the truthful truncation trio, because a marketing number read
  without its bounds is how a partial window becomes a reported total.

The models live HERE, not in aidream, because ``TOOL_RESULT_KINDS`` may never
import aidream (``scripts/check_package_boundaries.py``) and the tool
implementations import these models to validate with.

Publish: ``scripts/publish_kind_catalog.py matrx_ai.tools.kinds.google --apply``.
"""

from __future__ import annotations

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind
from pydantic import JsonValue

# ---------------------------------------------------------------------------
# google_workspace_result
# ---------------------------------------------------------------------------


@kind(
    "google_workspace_result",
    label="Google Workspace Result",
    family="google_workspace",
    example={
        "action": "append_document",
        "dry_run": True,
        "file_id": "1AbC",
        "title": "Q3 Plan",
        "would_append": {
            "position": "end_of_document",
            "heading": "## 2026-09-17",
            "text": "Three risks remain open.",
            "after_char": 4211,
        },
        "note": "Nothing was written. Re-run without dry_run to append exactly this block.",
        "open_in_google": "https://docs.google.com/document/d/1AbC",
    },
)
class GoogleWorkspaceResult(KindModel):
    #: Every result names the action that produced it (the union's own label).
    action: str = ""
    #: Which connected Google account answered. Present on every live read.
    google_account: str | None = None
    note: str | None = None

    # ── list_resources: the files AI Matrx can reach + the health of the
    # accounts behind them (what `google_read.list_capabilities` used to answer).
    resources: list[dict] | None = None
    count: int | None = None
    accounts: list[dict] | None = None

    # ── create receipts (Doc or Sheet).
    created: bool | None = None
    file_id: str | None = None
    name: str | None = None
    kind: str | None = None
    open_in_google: str | None = None

    # ── document read / append window.
    title: str | None = None
    text: str | None = None
    total_chars: int | None = None
    showing_chars: str | None = None
    has_more: bool | None = None
    next_start_char: int | None = None
    appended: bool | None = None

    # ── sheet read / write window.
    tab: str | None = None
    range: str | None = None
    rows: list[list[JsonValue]] | None = None
    row_count: int | None = None
    sheet_size: str | None = None
    next_range_a1: str | None = None
    written: bool | None = None

    # ── dry_run previews. `dry_run: true` means NOTHING was written; each
    # preview is the exact change the same call without dry_run would make.
    dry_run: bool | None = None
    #: append_document — the block and where it lands.
    would_append: dict | None = None
    #: write_sheet — the cells that would be replaced and what would replace them.
    would_write: dict | None = None
    #: create_document / create_sheet — the file that would be created.
    would_create: dict | None = None

    # ── import_sheet_as_table.
    #: One field per header-row column, with the column letter it came from.
    fields: list[dict] | None = None
    header_row: int | None = None
    #: A step only the browser can take, named exactly. Never a fake success.
    needs_client: dict | None = None

    # ── prepare_email — a draft for the HUMAN send step; never sent here.
    sent: bool | None = None
    draft: dict | None = None
    from_email: str | None = None
    next_step: str | None = None

    # ── read_calendar.
    events: list[dict] | None = None
    window_start: str | None = None
    window_end: str | None = None

    # ── read_contacts / import_contact.
    contacts: list[dict] | None = None
    #: import_contact — per Person field, where the value came from.
    field_map: list[dict] | None = None
    person: dict | None = None
    imported: bool | None = None
    matched_by: str | None = None

    # ── read_tasks / import_tasks.
    task_lists: list[dict] | None = None
    tasks: list[dict] | None = None
    #: import_tasks — what landed, what was already here, what was skipped.
    imported_tasks: list[dict] | None = None
    already_imported: list[dict] | None = None
    skipped: list[dict] | None = None

    # ── the human-in-the-loop branch. An organization can require a person to
    # approve a write or an import before it happens (the ``hitl.google.*``
    # knobs). When it does, the tool runs its OWN dry run, queues that exact
    # preview in the one approval queue, and returns the preview WITH these two
    # keys set — so the model is told, in the result rather than in prose, that
    # nothing was written and where the change is waiting.
    #: True when the change was PROPOSED, not made. Never present otherwise.
    awaiting_approval: bool | None = None
    #: The queue item: ``approval_id``, the ``mode`` it runs in, the ``knob``
    #: that decided, whether the run was ``attended``, and who it waits with.
    approval: dict | None = None

    # ── the honesty trio every bounded read carries.
    bounds: dict | None = None
    truncated: bool | None = None
    limit_note: str | None = None


# ---------------------------------------------------------------------------
# google_marketing_result
# ---------------------------------------------------------------------------


@kind(
    "google_marketing_result",
    label="Google Marketing Result",
    family="google_marketing",
    example={
        "action": "read_search_console",
        "source": "persisted",
        "site_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "bounds": {"start_date": "2026-08-01", "end_date": "2026-08-28", "limit": 1000},
        "returned_count": 412,
        "count_unit": "rows",
        "truncated": False,
        "completeness": "complete_within_requested_bound",
        "limit_note": "Persisted Search Console rows are bounded by the requested limit.",
        "data": {"rows": []},
    },
)
class GoogleMarketingResult(KindModel):
    action: str = ""
    #: `persisted` = our own stored facts (no hidden sync); `live_google` = a
    #: bounded call to Google made for this request. Never absent.
    source: str = ""
    #: Which connected Google account answered a live read.
    google_account: str | None = None
    site_id: str | None = None
    channel_id: str | None = None

    #: What was ASKED for — the window, the limit, the profile.
    bounds: dict | None = None
    returned_count: int | None = None
    count_unit: str | None = None
    #: True/False when the provider or our own cap says so; null when unknowable.
    truncated: bool | None = None
    completeness: str | None = None
    limit_note: str | None = None
    #: How old the numbers are, in words, when the source lags (GSC ~3 days).
    freshness: str | None = None
    note: str | None = None

    #: The read's payload, under the shape the underlying reader returns.
    data: JsonValue | None = None

    # ── tracking_health: the plain-English verdict, the three graded checks, and
    # what the read could not see. The check shape and the three booleans are the
    # SAME vocabulary the stored snapshot declares (`web.tag_manager_snapshot`
    # findings → `tag_manager_findings`, migration 0763), so this answer can be
    # persisted verbatim rather than translated into a second set of words.
    verdict: str | None = None
    checks: list[dict] | None = None
    has_ga4: bool | None = None
    has_conversion_tag: bool | None = None
    has_consent: bool | None = None
    caveats: list[str] | None = None
    containers: list[dict] | None = None


GOOGLE_TOOL_RESULT_KINDS: dict[str, type[KindModel]] = {
    "google_workspace": GoogleWorkspaceResult,
    "google_marketing": GoogleMarketingResult,
}


__all__ = [
    "GOOGLE_TOOL_RESULT_KINDS",
    "GoogleMarketingResult",
    "GoogleWorkspaceResult",
]
