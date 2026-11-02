"""probe notes status: the team-wide fullness sweep of every notes document."""

from __future__ import annotations
import math
import sys

import typer
from probe.cli.commands.notes.notes import notes_app


#: One sweep reads at most this many pages of the catalog. 100 is the route's
#: per-page maximum, so this is 2,000 documents -- far above the largest tenant
#: today (52) and bounded on purpose: an unbounded walk is a command that gets
#: slower every month without anyone deciding it should. When the cap is reached
#: the report SAYS so, because a truncated sweep that reads as complete is worse
#: than no sweep -- "nothing is near full" would be a claim it never checked.
_NOTES_STATUS_MAX_PAGES = 20
_NOTES_STATUS_PAGE_SIZE = 100


def _is_count(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _notes_status_row(item: dict) -> dict | None:
    """One catalog item as a fullness row, or None if its fullness is unknown.

    Fullness is TOKENS against the token cap (`tokens` / `limit_tokens`), the
    limit a write is refused at. A row without a token count cannot be ranked:
    the server has not counted it yet (`tokens: null` until its backfill
    reaches the row), or the backend predates token caps. Dropped rather than
    defaulted to zero, which would sort a document of unknown size to the
    bottom of a report whose whole job is finding the full ones -- and never
    ranked by its `chars`, which measure the character backstop, not the cap.
    The caller counts what it dropped and says so.

    `chars` / `limit` / `remaining` keep the character meaning they always had
    (the backstop now), beside the token numbers.
    """
    tokens, limit = item.get("tokens"), item.get("limit_tokens")
    if not _is_count(tokens) or not _is_count(limit) or limit <= 0:
        return None
    ancestors = [a.get("title") or "" for a in item.get("ancestors") or []]
    row = {
        "kind": item.get("kind"),
        "id": item.get("id"),
        "title": item.get("title"),
        "path": " / ".join([*ancestors, item.get("title") or ""]),
        "tokens": tokens,
        "limit_tokens": limit,
        "remaining_tokens": max(0, limit - tokens),
        # floor, matching probe.sdk.reads.notes_cap: never print 100% for a document that
        # still accepts a write.
        "percent": math.floor(100 * tokens / limit),
        "updated_at": item.get("updated_at"),
    }
    chars, limit_chars = item.get("chars"), item.get("limit_chars")
    if _is_count(chars) and _is_count(limit_chars):
        row.update({"chars": chars, "limit": limit_chars, "remaining": max(0, limit_chars - chars)})
    return row


@notes_app.command("status")
def notes_status(
    above: float = typer.Option(
        0.0, "--above", min=0.0, max=100.0, help="only report documents at least this % full"
    ),
) -> None:
    """How full every notes document in this team is -- the fullness sweep.

    TENANT-WIDE, and deliberately without the --project/--experiment/--run flags
    the other `notes` verbs take. One entity's headroom already rides on that
    entity's own read (`notes_remaining_tokens` and `notes_limit_tokens` on the
    project, experiment and run responses), so the question only this
    command can answer is the cross-entity one: WHICH documents are close to
    refusing writes. Answering it used to mean one API fetch per entity, which is
    why nobody did it -- and why a project sat at 99,992 of its then
    100,000-character cap, refusing every append, for a day.

    Documents are listed fullest first, in TOKENS against each one's token cap.
    Writes are refused AT the cap, not near it, so a document at 100% is one
    that has already been losing writes. A document the server has not counted
    yet is not ranked, and the summary says how many there were.
    """
    from ....sdk.reads.notes_cap import NOTES_WARN_FRACTION

    rows: list[dict] = []
    unmeasured = 0
    cursor: str | None = None
    is_truncated = False
    with _client() as c:
        for page_number in range(_NOTES_STATUS_MAX_PAGES):
            # The limit is what selects the FLAT listing over the dashboard's
            # lazy tree; without it this would sweep root branches only. See
            # Client.list_notes.
            page = c.list_notes(
                cursor=cursor,
                limit=_NOTES_STATUS_PAGE_SIZE,
                # A sub-note can refuse writes at ITS cap while every main note
                # has room; a sweep that cannot see them reports "nothing is
                # near full" about the very documents losing writes.
                include_sub_notes=True,
            )
            for item in page.get("items") or []:
                row = _notes_status_row(item)
                if row is not None:
                    rows.append(row)
                else:
                    unmeasured += 1
            cursor = page.get("next_cursor")
            if not cursor:
                break
            is_truncated = page_number == _NOTES_STATUS_MAX_PAGES - 1

    rows.sort(key=lambda r: (-r["percent"], -r["tokens"]))
    warn_at = 100 * (1 - NOTES_WARN_FRACTION)
    near_full = [r for r in rows if r["percent"] >= warn_at]
    shown = [r for r in rows if r["percent"] >= above]

    for row in shown:
        mark = "!" if row["percent"] >= warn_at else " "
        print(
            f"{mark} {row['percent']:3d}%  {row['tokens']:>6,}/{row['limit_tokens']:<6,} tokens  "
            f"{row['kind']:<10} {row['path']}",
            file=sys.stderr,
        )
    summary = f"{len(rows)} notes documents, {len(near_full)} at or above {warn_at:.0f}% full"
    if unmeasured:
        # Not "nothing is near full" about documents it could not measure.
        summary += f"; {unmeasured} not counted in tokens yet, so not ranked"
    if is_truncated:
        summary += (
            f" -- STOPPED after {_NOTES_STATUS_MAX_PAGES * _NOTES_STATUS_PAGE_SIZE} documents; "
            "more exist and were not read"
        )
    print(summary, file=sys.stderr)
    _print_json(
        {
            "scanned": len(rows),
            "unmeasured": unmeasured,
            "truncated": is_truncated,
            "warn_at_percent": warn_at,
            "near_full": len(near_full),
            "documents": shown,
        }
    )
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _client  # noqa: E402 -- pieces need each other; the front door loads this one first
