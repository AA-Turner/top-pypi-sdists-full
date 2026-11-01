"""probe summary edit / append: change the page in place (exact replace outside kept spans, or append before its article closes), version-pinned."""

from __future__ import annotations
import re
import sys
from typing import Any

import typer

from ....sdk import errors
from .. import owed
from probe.shared.notes.summary.checkout_push import (
    ERASED_SINCE_CHECKOUT,
    SESSION_ERASED,
    SESSION_ERASED_DETAIL,
    VERSION_MOVED,
    WRITER_OFF,
    _get_summary,
    _is_html,
    summary_app,
)
from probe.shared.notes.summary.summary import (
    LANE_MARK,
    LANE_NOTE,
    MODE_LANE,
    Target,
    _DIRECTED_OPT,
    _EXPERIMENT_OPT,
    _PROJECT_OPT,
    _code,
    _directed,
    _fail,
    _main,
    _message,
    _print_json,
    compose_draft,
    record_mode,
    resolve_target,
    session_id,
)


# -- probe summary edit | append ----------------------------------------------
#
# One command, no draft: read the page as HTML, change it, write it back pinned
# to the version read. For a caller whose files do not outlive one command (the
# dashboard assistant runs each command in a temporary HOME) and for a small
# change anyone wants without a checkout. HTML only: the Markdown door rebuilds
# every element but figures, style and charts from Markdown, so a recorder
# page's layout would flatten on every edit. A person's block is theirs: an
# edit that reaches into one is refused here, because the server would put the
# stored bytes back and report the write a success.

#: How many times one edit re-applies itself to a page that moved under it.
EDIT_ATTEMPTS = 5
#: A person's block as the HTML read hands it over (`summary_html._KEPT`).
_KEPT_SPAN = re.compile(r"<!--\s*kept:\s*h\d+\s*-->.*?<!--\s*/kept\s*-->", re.S)
#: A kept marker alone: the overview read shows the page without them.
_KEPT_MARKER = re.compile(r"<!--\s*/?kept(?::\s*h\d+)?\s*-->")
#: Text no tag inside counts: a stylesheet, a script, a comment.
_OPAQUE = re.compile(r"<(style|script)\b[^>]*>.*?</\1\s*>|<!--.*?-->", re.S | re.I)
#: The page's own article (overview-contract: `<article class="ov-page">`).
_PAGE_ARTICLE = re.compile(r"""<article\b[^>]*\bclass\s*=\s*["'][^"']*\bov-page\b""", re.I)
_ARTICLE_TAG = re.compile(r"<(/?)article\b[^>]*>", re.I)
#: What an edit says when a session erasure moved the page since the text was read.
ERASED_EDIT = (
    "a session erasure changed this {kind}'s summary since the page your text came from, so "
    "nothing was written; read the page again and redo the change from what it says now"
)
#: What an edit or append says to a write that changed nothing.
UNCHANGED = "the page already said that; nothing changed"


def _kept_spans(page: str) -> list[tuple[int, int]]:
    return [(m.start(), m.end()) for m in _KEPT_SPAN.finditer(page)]


def _touches(spans: list[tuple[int, int]], start: int, end: int) -> bool:
    return any(start < e and s < end for s, e in spans)


def _occurrences(page: str, old: str) -> list[int]:
    """Every position `old` starts at, overlapping ones included: `x x` sits
    twice in `x x x`, and an edit must not pick one of them silently."""
    found, at = [], page.find(old)
    while at >= 0:
        found.append(at)
        at = page.find(old, at + 1)
    return found


def _refuse_kept(what: str) -> None:
    _fail(
        f"{what} falls inside a block a person wrote (<!-- kept: hN --> ... <!-- /kept -->); "
        "only they can change it, with the dashboard's edit pencil. Nothing was written."
    )


def _replace_once(old: str, new: str, target: Target):
    """The change `summary edit` makes: `old` must sit exactly once outside a
    person's block. A match inside one, or across its edge, is refused: the
    server would put the person's bytes back and report a change."""

    def change(page: str) -> str:
        kept = _kept_spans(page)
        found = _occurrences(page, old)
        outside = [at for at in found if not _touches(kept, at, at + len(old))]
        if len(outside) == 1:
            at = outside[0]
            return page[:at] + new + page[at + len(old):]
        if len(outside) > 1:
            _fail(f"--old matches {len(outside)} places in the {target.kind} summary ({target.label}); "
                  "nothing was written. Add surrounding text until it matches once.")
        if found or old in _KEPT_MARKER.sub("", page):
            _refuse_kept("--old")
        _fail(f"--old matches nothing in the {target.kind} summary ({target.label}); nothing was "
              "written. Copy it exactly from the page's HTML, not its Markdown: the `html` of the "
              "entity's overview view, or `probe summary checkout`.")
        raise AssertionError("unreachable")  # _fail raises

    return change


def _page_article_close(page: str) -> int | None:
    """Where the page's own `<article class="ov-page">` closes: its matching
    `</article>`, nested articles counted, tags inside a stylesheet, script or
    comment ignored. None when the page has no such article."""
    opaque = [(m.start(), m.end()) for m in _OPAQUE.finditer(page)]
    start = next((m for m in _PAGE_ARTICLE.finditer(page) if not _touches(opaque, m.start(), m.end())), None)
    if start is None:
        return None
    depth = 0
    for tag in _ARTICLE_TAG.finditer(page, start.start()):
        if _touches(opaque, tag.start(), tag.end()):
            continue
        depth += -1 if tag.group(1) else 1
        if depth == 0:
            return tag.start()
    return None


def _append_html(text: str, target: Target):
    def change(page: str) -> str:
        if not page.strip():
            _fail(f"the {target.kind} summary ({target.label}) has no page yet, so there is nothing "
                  "to add to; nothing was written. Its first page is written by the daemon or an "
                  "agent with `probe summary checkout` and `push`.")
        at = _page_article_close(page)
        if at is None:
            _fail(f"the {target.kind} summary ({target.label}) has no <article class=\"ov-page\"> to "
                  "add to (an older page); nothing was written. Use `probe summary edit` to put the "
                  "text next to a sentence it already has.")
        if _touches(_kept_spans(page), at, at + 1):
            _refuse_kept("the end of the page")
        before = page[:at]
        sep = "" if before.endswith("\n") else "\n"
        return f"{before}{sep}{text.strip()}\n{page[at:]}"

    return change


def rewrite_summary(client, target: Target, change, *, directed: bool, version: int | None = None) -> dict:
    """Read `target`'s page as HTML, `change` it, write it pinned to the version
    read; the written row. `change(page)` returns the new page or refuses by
    raising. A page that moved (409 `version_moved`) is changed again from the
    head the 409 carries, so a concurrent writer's words are kept, never
    overwritten. `version` is the page version the caller's text was written
    from (the overview read's): the first write is pinned to it, so a session
    erasure since then is refused (`ERASED_EDIT`, exit 2) rather than its words
    written back; without it the version this command read stands in. Every
    write passes the credential scrubber, so a page holding text it would
    rewrite is refused, and so is a change that brings some. A reply that does
    not confirm the write is settled by reading the page, never by sending it
    again (`main._settle_unconfirmed`)."""
    main = _main()
    anchors = target.anchors()
    what = f"{target.kind} summary ({target.label})"
    shown = f"probe summary checkout --{target.kind} {target.label}"
    head: dict[str, tuple[str, Any, Any]] = {}
    pinned = version

    def read() -> tuple[dict, str, object]:
        row = _get_summary(client, anchors, html=True)
        if not isinstance(row, dict):
            raise ValueError(f"the reply was not a {target.kind} summary")
        if not _is_html(row):
            _fail(f"this Probe server does not hand the {what} over as HTML, so it cannot be "
                  f"changed here without flattening the page; nothing was written. Use `{shown}`, "
                  "edit the draft, then `probe summary push`.")
        # Stripped: the server stores the page stripped, and a lost reply is
        # settled by comparing what it holds with what was sent.
        return row, (row.get("html") or "").strip(), row.get("version")

    for _ in range(EDIT_ATTEMPTS):
        if "page" in head:  # the 409 carried the head: no second read
            page, series, read_version = head.pop("page")
        else:
            try:
                row, page, read_version = read()
            except ValueError:
                _fail(f"reading the {what} did not return Probe's answer; nothing was written.")
            series = row.get("series")
        if not main._is_version(read_version):
            _fail(f"Probe did not say which version of the {what} it read, so a write could "
                  "overwrite someone else's; nothing was written.")
        expected = int(pinned) if pinned is not None else int(read_version)
        pinned = None  # only the first write: a retry follows the page that moved
        before = compose_draft(page, series)
        if main._stored_form("html", before) != before:
            _fail(f"the {what} holds text Probe's credential scrubber would rewrite, and saving the "
                  f"page would rewrite it; nothing was written. Review it with `{shown}`, then "
                  "`probe summary push`.")
        new_page = change(page).strip()
        text = compose_draft(new_page, series)
        if main._stored_form("html", text) != text:
            _fail("the new text holds something Probe's credential scrubber would rewrite; nothing "
                  "was written. Leave the credential-shaped text out.")
        try:
            row = client.put_summary(
                html=text,
                expected_version=expected,
                session_id=session_id(),
                directed=directed,
                **anchors,
            )
        except errors.ConflictError as exc:
            code = _code(exc)
            detail = exc.detail if isinstance(exc.detail, dict) else {}
            if code == ERASED_SINCE_CHECKOUT:
                _fail(ERASED_EDIT.format(kind=target.kind), 2)
            if code == SESSION_ERASED:
                _fail(SESSION_ERASED_DETAIL, 2)
            if code in (None, VERSION_MOVED):
                if isinstance(detail.get("html"), str) and main._is_version(detail.get("version")):
                    head["page"] = (detail["html"].strip(), detail.get("series"), detail["version"])
                continue
            raise errors.RosError(_message(exc), status=409, detail=exc.detail) from None
        except errors.RosError as exc:
            if _code(exc) == WRITER_OFF:  # the team's door is closed: nothing to retry
                record_mode(MODE_LANE)
                _fail(f"{_message(exc) or LANE_NOTE} {LANE_MARK}")
            why = main._unconfirmed_reason(exc)
            if why is None:
                raise
            return main._settle_unconfirmed(read, int(read_version), new_page, what, why=why, shown=shown)
        except ValueError:  # a 200 that is not Probe's JSON: it may hold the write
            return main._settle_unconfirmed(
                read, int(read_version), new_page, what, why=main._NO_VERSION_REPLY, shown=shown
            )
        if not (isinstance(row, dict) and main._is_version(row.get("version"))):
            return main._settle_unconfirmed(
                read, int(read_version), new_page, what, why=main._NO_VERSION_REPLY, shown=shown
            )
        return row
    _fail(f"the {what} kept changing while this wrote; nothing was written. Run it again.")
    raise AssertionError("unreachable")  # _fail raises


_VERSION_OPT = typer.Option(
    None,
    "--version",
    min=0,
    help="the page version your text was written from (the overview read's `version`): a session "
    "erasure since then is refused instead of written back",
)


def _report(target: Target, row: dict, payload: dict, done: str) -> None:
    changed = row.get("changed") is not False
    _print_json({"target": target.kind, "label": target.label, **payload, "changed": changed,
                 "version": row.get("version")})
    if changed:
        owed.settle(owed.SUMMARY, target.keys())
        print(f"{done} {target.kind} summary ({target.label}) v{row.get('version')}", file=sys.stderr)
    else:
        print(f"{target.kind} summary ({target.label}): {UNCHANGED}", file=sys.stderr)


@summary_app.command("edit")
def summary_edit(
    old: str = typer.Option(..., "--old", help="the exact HTML to replace; must match once"),
    new: str = typer.Option(..., "--new", help="the HTML that replaces it ('' deletes it)"),
    project: str = _PROJECT_OPT,
    experiment: str = _EXPERIMENT_OPT,
    version: int = _VERSION_OPT,
    directed: bool = _DIRECTED_OPT,
) -> None:
    """Replace one exact piece of the summary page, with no checkout.

    `--old` is the page's HTML (the `html` of the entity's overview view, or
    the draft `probe summary checkout` writes), character for character, and
    must appear exactly once outside a person's block; a match inside or across
    one is refused, as is no match or several. Nothing is written then. Both
    values are literal text (no @file, no stdin). Exit 2: a session erasure
    changed the page since `--version` (or since this read): read it again."""
    if not old:
        raise typer.BadParameter("--old is empty")
    with _main()._client() as client:
        target = resolve_target(client, project, experiment)
        row = rewrite_summary(client, target, _replace_once(old, new, target),
                              directed=_directed(directed), version=version)
    _report(target, row, {"removed": len(old), "added": len(new)}, "edited")


@summary_app.command("append")
def summary_append(
    html: str = typer.Option(..., "--html", help="the HTML to add at the end of the page"),
    project: str = _PROJECT_OPT,
    experiment: str = _EXPERIMENT_OPT,
    version: int = _VERSION_OPT,
    directed: bool = _DIRECTED_OPT,
) -> None:
    """Add HTML at the end of the summary page (before its article's close),
    with no checkout. A page with nothing on it yet, or an older page with no
    `<article class="ov-page">`, is refused: its first page is written with
    checkout and push. Literal text (no @file, no stdin). Exit 2: a session
    erasure changed the page since `--version` (or since this read)."""
    if not html.strip():
        raise typer.BadParameter("--html is empty")
    with _main()._client() as client:
        target = resolve_target(client, project, experiment)
        row = rewrite_summary(client, target, _append_html(html, target),
                              directed=_directed(directed), version=version)
    _report(target, row, {"added": len(html.strip())}, "added to")
