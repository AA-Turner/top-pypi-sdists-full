"""Site data — structured records for hard sites, via Bright Data's Web Scraper API.

The door every caller uses (``read_page``'s route-first lane and the agent
``site_data`` tool):

* ``match(url)`` — the verified, auto-routing catalog entry for a URL, or None.
* ``fetch(url=...)`` / ``fetch(site=key, query=..., inputs=...)`` →
  ``SiteDataResult`` with the records, a bounded markdown rendering an LLM can
  read, and provenance (provider, dataset key, records billed).

The client is INJECTED by the host (``configure_ext(brightdata_client=...)``);
this package never reads a key from the environment. No client = an honest
``status="not_configured"`` answer, never a silent skip.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from matrx_scraper._ext import get_ext, has_ext
from matrx_scraper.vendors.brightdata import (
    BrightDataCapExceeded,
    BrightDataClient,
    BrightDataError,
    BrightDataInputError,
    BrightDataTimeout,
    current_limits,
)
from matrx_scraper.vendors.site_catalog import CatalogEntry, ensure_catalog, get_entry, verified_entries
from matrx_scraper.vendors.site_catalog import match as _catalog_match

EXT_CLIENT = "brightdata_client"
#: Optional host hook: ``async () -> bool`` — the platform knob deciding whether
#: ``read_page`` routes catalog URLs here first. Absent = route (defaults lean open).
EXT_ROUTE_ENABLED = "site_data_route_enabled"
#: Optional host hook: ``async (request: SiteDataTableRequest, progress) -> SiteDataTableSaved`` —
#: fetch the records AND write them into a table the person owns (the host's durable job, metering,
#: limits and table API). Absent = ``fetch_to_table`` answers ``not_configured``; this package
#: never writes a table itself.
EXT_TABLE_WRITER = "site_data_table_writer"

DEFAULT_MAX_RECORDS = 20
#: The ceiling on ``max_records`` is no longer a constant here: it is the host-injected limit
#: (``vendors.brightdata.current_limits()``; aidream = the knob
#: ``knowledge.scraper.site_data_max_records_per_fetch``), package default 100.
DEFAULT_RENDER_CHARS = 24_000
_FIELD_CHARS = 600
_LIST_ITEMS = 8
_TITLE_KEYS = ("name", "title", "job_title", "company_name", "product_name", "business_name",
               "question", "headline", "place_name", "advertiser_name")


@dataclass
class SiteDataResult:
    status: str  # success | not_configured | no_match | input_error | timeout | error | empty
    message: str = ""
    entry_key: str | None = None
    label: str | None = None
    records: list[dict[str, Any]] = field(default_factory=list)
    errors: list[dict[str, Any]] = field(default_factory=list)
    rendering: str = ""
    rendering_truncated: bool = False
    records_billed: int = 0
    snapshot_id: str | None = None
    #: Set only by ``fetch_to_table``: ``{table_id, table_name, rows_created, rows_updated,
    #: records_billed, cost_usd, job_id, limit_applied}``.
    table: dict[str, Any] | None = None

    @property
    def ok(self) -> bool:
        return self.status == "success"

    @property
    def provenance(self) -> dict[str, Any]:
        return {
            "provider": "live_data",
            "engine": "site_data",
            "dataset": self.entry_key,
            "label": self.label,
            "records_billed": self.records_billed,
            "snapshot_id": self.snapshot_id,
            "announcement": f"live data, {self.label}" if self.label else "live data",
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "message": self.message,
            "records": self.records,
            "record_count": len(self.records),
            "errors": self.errors[:10],
            "rendering": self.rendering,
            "rendering_truncated": self.rendering_truncated,
            "provenance": self.provenance,
        }


def match(url: str) -> CatalogEntry | None:
    return _catalog_match(url)


def is_configured() -> bool:
    return has_ext(EXT_CLIENT) and get_ext(EXT_CLIENT) is not None


def covered_sites() -> list[dict[str, Any]]:
    return [
        {"key": e.key, "label": e.label, "input": e.input_kind, "required": list(e.required_fields)}
        for e in verified_entries()
    ]


def _unknown_site(site: str) -> str:
    known = verified_entries()
    shown = ", ".join(e.key for e in known[:60])
    more = f" (and {len(known) - 60} more)" if len(known) > 60 else ""
    return f"Unknown site {site!r}. Verified sources: {shown}{more}."


def _not_configured(entry: CatalogEntry | None) -> SiteDataResult:
    return SiteDataResult(
        status="not_configured",
        message="Live data is not configured on this server (no data client was wired at startup).",
        entry_key=entry.key if entry else None,
        label=entry.label if entry else None,
    )


def build_inputs(entry: CatalogEntry, *, url: str | None, query: str | None, location: str | None,
                  inputs: list[dict[str, Any]] | dict[str, Any] | None, cap: int) -> list[dict[str, Any]]:
    if isinstance(inputs, dict):
        inputs = [inputs]
    rows: list[dict[str, Any]] = [dict(r) for r in (inputs or []) if isinstance(r, dict)]
    if not rows:
        row: dict[str, Any] = {}
        if entry.input_kind == "url" and url:
            row["url"] = url
        if query and entry.query_field:
            row[entry.query_field] = query
        if location and entry.location_field:
            row[entry.location_field] = location
        rows = [row]
    for row in rows:
        for k, v in entry.defaults.items():
            row.setdefault(k, v)
        if entry.limit_field:
            row.setdefault(entry.limit_field, cap)
    return rows


async def fetch(
    *,
    url: str | None = None,
    site: str | None = None,
    query: str | None = None,
    location: str | None = None,
    inputs: list[dict[str, Any]] | dict[str, Any] | None = None,
    max_records: int = DEFAULT_MAX_RECORDS,
    timeout_s: float = 180.0,
    render_chars: int = DEFAULT_RENDER_CHARS,
) -> SiteDataResult:
    entry: CatalogEntry | None
    await ensure_catalog()
    if site:
        entry = get_entry(site)
        if entry is None:
            return SiteDataResult(status="no_match", message=_unknown_site(site))
    elif url:
        entry = match(url)
        if entry is None:
            return SiteDataResult(status="no_match",
                                  message="No site-data dataset covers this URL; read it as a normal page.")
    else:
        return SiteDataResult(status="input_error", message="Pass url, or site plus query/inputs.")

    if not is_configured():
        return _not_configured(entry)
    client: BrightDataClient = get_ext(EXT_CLIENT)

    limits = await current_limits()
    cap = max(1, min(int(max_records or DEFAULT_MAX_RECORDS), limits.max_total_records))
    rows = build_inputs(entry, url=url, query=query, location=location, inputs=inputs, cap=cap)
    missing = sorted({f for r in rows for f in entry.missing(r)})
    if missing:
        return SiteDataResult(
            status="input_error", entry_key=entry.key, label=entry.label,
            message=f"{entry.label} needs: {', '.join(missing)}.",
        )

    if len(rows) > limits.max_inputs or cap * len(rows) > limits.max_total_records:
        return SiteDataResult(
            status="input_error", entry_key=entry.key, label=entry.label,
            message=(f"{entry.label}: {len(rows)} inputs x {cap} records each could return {cap * len(rows)} "
                     f"records; at most {limits.max_inputs} inputs and {limits.max_total_records} records in "
                     "total per call. Send fewer inputs or lower max_records."),
        )

    try:
        res = await client.scrape(
            entry.dataset_id, rows,
            limit=cap,
            discover_by=entry.discover_for(rows[0]) if rows else None,
            timeout_s=timeout_s,
        )
    except BrightDataCapExceeded as exc:
        return SiteDataResult(status="input_error", entry_key=entry.key, label=entry.label, message=str(exc))
    except BrightDataInputError as exc:
        return SiteDataResult(status="input_error", entry_key=entry.key, label=entry.label, message=str(exc))
    except BrightDataTimeout as exc:
        return SiteDataResult(status="timeout", entry_key=entry.key, label=entry.label, message=str(exc),
                              snapshot_id=exc.snapshot_id)
    except BrightDataError as exc:
        return SiteDataResult(status="error", entry_key=entry.key, label=entry.label, message=str(exc))

    records = res.records[:cap]
    out = SiteDataResult(
        status="success" if records else "empty",
        entry_key=entry.key, label=entry.label, records=records, errors=res.errors,
        records_billed=res.records_billed, snapshot_id=res.snapshot_id,
        message=_issue_note(entry) if records else _empty_message(entry, res.errors),
    )
    if limits.notice:
        out.message = f"{out.message} {limits.notice}".strip() if out.message else limits.notice
    out.rendering, out.rendering_truncated = render_records(
        records, label=entry.label, total=len(res.records), limit=render_chars
    )
    return out


@dataclass
class SiteDataTableRequest:
    """What the host writer is asked: a resolved catalog source and its raw inputs."""

    source_key: str
    inputs: list[dict[str, Any]]
    max_records: int
    table_id: str | None = None
    table_name: str | None = None


@dataclass
class SiteDataTableSaved:
    """What the host writer answers: the records plus where they landed."""

    records: list[dict[str, Any]]
    table: dict[str, Any]


class SiteDataTableRefused(Exception):
    """The host refused (or failed) the save: ``code`` is the host's code, ``message`` a sentence."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


#: host refusal code -> the ``SiteDataResult`` status the agent tool already types.
_REFUSAL_STATUS = {
    "usage_limit": "usage_limit", "limit": "input_error", "input_error": "input_error",
    "unknown_source": "no_match", "source_unavailable": "unavailable", "not_configured": "not_configured",
    "still_running": "timeout", "timeout": "timeout", "table_not_found": "input_error",
    "wrong_organization": "input_error", "organization_required": "input_error",
    "not_signed_in": "input_error", "empty": "empty",
}


async def fetch_to_table(
    *,
    url: str | None = None,
    site: str | None = None,
    query: str | None = None,
    location: str | None = None,
    inputs: list[dict[str, Any]] | dict[str, Any] | None = None,
    max_records: int = DEFAULT_MAX_RECORDS,
    table_id: str | None = None,
    table_name: str | None = None,
    progress: Any = None,
    render_chars: int = DEFAULT_RENDER_CHARS,
) -> SiteDataResult:
    """Like ``fetch`` but the records land in a table via the host's writer (one job, one meter).

    ``progress`` is an optional ``async (label: str) -> None``. The result's ``table`` carries
    ``{table_id, table_name, rows_created, rows_updated, records_billed, ...}``.
    """
    entry: CatalogEntry | None
    await ensure_catalog()
    if site:
        entry = get_entry(site)
        if entry is None:
            return SiteDataResult(status="no_match", message=_unknown_site(site))
    elif url:
        entry = match(url)
        if entry is None:
            return SiteDataResult(status="no_match",
                                  message="No site-data dataset covers this URL; read it as a normal page.")
    else:
        return SiteDataResult(status="input_error", message="Pass url, or site plus query/inputs.")
    if not has_ext(EXT_TABLE_WRITER) or get_ext(EXT_TABLE_WRITER) is None:
        return SiteDataResult(
            status="not_configured", entry_key=entry.key, label=entry.label,
            message="Saving live data to a table is not set up on this server, so nothing was fetched or billed.")
    if isinstance(inputs, dict):
        inputs = [inputs]
    raw = [dict(r) for r in (inputs or []) if isinstance(r, dict)]
    if not raw:
        row: dict[str, Any] = {}
        if entry.input_kind == "url" and url:
            row["url"] = url
        if query and entry.query_field:
            row[entry.query_field] = query
        if location and entry.location_field:
            row[entry.location_field] = location
        raw = [row]
    request = SiteDataTableRequest(source_key=entry.key, inputs=raw, max_records=int(max_records or DEFAULT_MAX_RECORDS),
                                   table_id=table_id, table_name=table_name)
    try:
        saved: SiteDataTableSaved = await get_ext(EXT_TABLE_WRITER)(request, progress)
    except SiteDataTableRefused as exc:
        return SiteDataResult(status=_REFUSAL_STATUS.get(exc.code, "error"), entry_key=entry.key,
                              label=entry.label, message=exc.message)
    records = list(saved.records)
    out = SiteDataResult(
        status="success" if records else "empty", entry_key=entry.key, label=entry.label, records=records,
        records_billed=int(saved.table.get("records_billed") or 0), table=dict(saved.table),
        message=_issue_note(entry) if records else "No records came back." + (f" Known issue: {entry.known_issue}" if entry.known_issue else ""),
    )
    out.rendering, out.rendering_truncated = render_records(records, label=entry.label, total=len(records),
                                                            limit=render_chars)
    return out


def _issue_note(entry: CatalogEntry) -> str:
    return f"{entry.label}: {entry.known_issue}" if entry.known_issue else ""


def _empty_message(entry: CatalogEntry, errors: list[dict[str, Any]]) -> str:
    issue = f" Known issue: {entry.known_issue}" if entry.known_issue else ""
    if errors:
        first = errors[0]
        why = first.get("error") or first.get("error_code") or "unknown error"
        return f"{entry.label}: no records came back ({why}).{issue}"
    return f"{entry.label}: no records came back.{issue}"


# ── Rendering ────────────────────────────────────────────────────────────


def _scalar(v: Any) -> str:
    s = str(v).strip().replace("\n", " ")
    return s if len(s) <= _FIELD_CHARS else s[:_FIELD_CHARS] + "…"


def _render_value(v: Any, depth: int) -> str:
    if isinstance(v, dict):
        if depth >= 2:
            return _scalar({k: x for k, x in v.items() if x not in (None, "", [], {})})
        parts = [f"{k}: {_render_value(x, depth + 1)}" for k, x in v.items() if x not in (None, "", [], {})]
        return "; ".join(parts)
    if isinstance(v, list):
        items = [x for x in v if x not in (None, "", [], {})]
        shown = [_render_value(x, depth + 1) for x in items[:_LIST_ITEMS]]
        more = f" (+{len(items) - _LIST_ITEMS} more)" if len(items) > _LIST_ITEMS else ""
        if items and isinstance(items[0], dict):
            return "".join(f"\n  - {s}" for s in shown) + more
        return ", ".join(shown) + more
    return _scalar(v)


def _title(rec: dict[str, Any], i: int) -> str:
    for k in _TITLE_KEYS:
        if rec.get(k):
            return _scalar(rec[k])
    return f"Record {i}"


def render_one(rec: dict[str, Any], i: int) -> str:
    lines = [f"### {i}. {_title(rec, i)}"]
    for k, v in rec.items():
        if v in (None, "", [], {}) or k in ("input", "timestamp", "discovery_input"):
            continue
        lines.append(f"- **{k}**: {_render_value(v, 0)}")
    return "\n".join(lines)


def render_records(records: list[dict[str, Any]], *, label: str, total: int | None = None,
                   limit: int = DEFAULT_RENDER_CHARS) -> tuple[str, bool]:
    """Markdown for an LLM, bounded at ``limit`` chars; the cut is announced in the text."""
    n = len(records)
    header = f"Live data — {label} ({n} record{'s' if n != 1 else ''}"
    header += f" of {total})" if total and total != n else ")"
    out = [header, ""]
    used = len(header) + 1
    for i, rec in enumerate(records, 1):
        block = render_one(rec, i)
        if used + len(block) + 2 > limit:
            if i == 1:  # never render nothing: cut the first record itself
                out.append(block[: max(limit - used - 120, 200)] + "…")
                i += 1
            out.append(f"\n[Rendering stopped at {i - 1} of {n} records ({limit:,}-character limit); "
                       "the full records are in `records`.]")
            return "\n".join(out), True
        out.append(block)
        out.append("")
        used += len(block) + 2
    return "\n".join(out).rstrip() + "\n", False


__all__ = [
    "DEFAULT_MAX_RECORDS",
    "EXT_CLIENT",
    "EXT_ROUTE_ENABLED",
    "EXT_TABLE_WRITER",
    "SiteDataTableRefused",
    "SiteDataTableRequest",
    "SiteDataTableSaved",
    "fetch_to_table",
    "build_inputs",
    "SiteDataResult",
    "covered_sites",
    "fetch",
    "is_configured",
    "match",
    "render_one",
    "render_records",
]
