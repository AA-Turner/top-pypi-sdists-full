"""probe summary checkout / push: the page to this session's draft and back, merging if it moved, refusing scrubbed text."""

from __future__ import annotations

import json
import sys
from typing import Any

import typer

from ....sdk import errors
from .. import owed
from probe.shared.notes.summary.summary import (
    EXT_BY_FORMAT,
    FORMAT_HTML,
    FORMAT_MARKDOWN,
    LANE_MARK,
    LANE_NOTE,
    MODE_LANE,
    MODE_RECORDER,
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
    _settings,
    chartable_path,
    checked_out,
    compose_draft,
    draft_paths,
    record_mode,
    resolve_target,
    session_id,
)

summary_app = typer.Typer(
    no_args_is_help=True,
    help="a project's or experiment's summary (its Overview page): checkout, edit the file, push; or one-command edit and append",
)
#: 409 codes a push does not merge (CONTRACT.md).
ERASED_SINCE_CHECKOUT = "erased_since_checkout"
SESSION_ERASED = "session_erased"
VERSION_MOVED = "version_moved"
WRITER_OFF = "summary_writer_off"
#: A push the credential scrubber would rewrite: refused before it is sent,
#: because the scrubber's change would land silently (inside a page's code, a
#: broken chart).
SCRUBBED = "scrubbed"
#: The scrubber's whole-value marker.
SCRUB_MARK = "<redacted>"
#: What a push says when the draft grew from a base an erasure changed.
ERASED_DETAIL = (
    "a session erasure changed this {kind}'s summary since your checkout, so it was not merged; "
    "check out again (`probe summary checkout --{kind} {label} --steal`: the draft's edits grew "
    "from the erased text) and redo your edit"
)
#: What a checkout says when the draft holds edits that were never pushed
#: (review of #3034, finding 3): never replaced without `--steal`.
UNPUSHED = (
    "{path} has edits that were never pushed, so it was not replaced. Push them (`probe summary "
    "push --{kind} {label}`), or check out again with --steal to discard them"
)
#: The checkout JSON's `refused` when the draft holds unpushed edits.
REFUSED_UNPUSHED = "unpushed edits"
SESSION_ERASED_DETAIL = "this session was erased, so its summary writes are refused"
#: Checkout's line when the entity carries Metrics-center visuals and none is set
#: (plan 3.8): the reminder rides the object at the moment it is handed over.
VISUALS_HINT = "Tables and charts for {label}: none set - read overview-visuals, then probe visuals options --{kind} {label}"


def _get_summary(client, anchors: dict, *, html: bool = False) -> dict:
    """`client.get_summary`, with FastAPI's own 404 (a server older than the
    summary routes) said as the writes say it. The SDK read keeps raising
    `NotFoundError` there: the MCP's summary views read that as "cannot say".
    `html` asks for the full page (`?format=html`), which an older server
    ignores (`_is_html` reads which one came back)."""
    from ....sdk.client.resources.projects.summaries import _PREDATES_SUMMARIES
    from ....sdk.client.server_features import _route_absent

    try:
        if html:
            return client.get_summary(**anchors, format=FORMAT_HTML)
        return client.get_summary(**anchors)
    except errors.NotFoundError as exc:
        if _route_absent(exc):
            raise errors.CapabilityUnavailable("summaries", _PREDATES_SUMMARIES) from exc
        raise


def _is_html(row: dict) -> bool:
    """Did the server hand over the page as HTML (a server with full pages)?"""
    return row.get("format") == FORMAT_HTML and isinstance(row.get("html"), str)


def _draft_text(row: dict) -> str:
    """The draft a summary read makes: the HTML draft, or the Markdown."""
    if _is_html(row):
        return compose_draft(row.get("html") or "", row.get("series"))
    return row.get("markdown") or ""


# -- probe summary ------------------------------------------------------------


@summary_app.command("checkout")
def summary_checkout(
    project: str = _PROJECT_OPT,
    experiment: str = _EXPERIMENT_OPT,
    steal: bool = typer.Option(
        False,
        "--steal",
        help="replace the draft although it has edits that were never pushed",
    ),
    visuals: bool = typer.Option(
        True,
        "--visuals/--no-visuals",
        hidden=True,
        help="also ask whether the Metrics-center tables are set (the daemon's own loads skip it)",
    ),
) -> None:
    """Pull the summary to a file; edit it, then `probe summary push` with the same flag.

    Prints JSON: `path` (the draft), `version`, `you` and `today` (for an
    entry's `## <date> · <name>`), `edited_by`, `edited_at` and `mode`, and
    the text: `markdown`, or -- from a server with full pages -- `format`:
    `html`, `html` (the draft: a `<script type="application/json"
    data-probe-series>` block of chart declarations, then the page),
    `chartable_path` (the closed set those may name: each run's metric keys
    and point counts) and `chartable` (how many runs and keys it holds). A
    person's own blocks show as `<!-- kept: hN -->` ... `<!-- /kept -->`:
    leave them where they are. The draft is this session's own file, in the
    state directory at 0600; checking out again replaces it with the page,
    unless it holds edits that were never pushed: then exit 2, the JSON names
    the draft (`refused: "unpushed edits"`), and `--steal` replaces it."""
    with _main()._client() as client:
        target = resolve_target(client, project, experiment)
        try:
            payload = checkout_draft(client, target, session_id(), steal=steal, visuals=visuals)
        except DraftDirty as dirty:
            _print_json(dirty.payload())
            print(UNPUSHED.format(path=dirty.where.document, kind=target.kind, label=target.label),
                  file=sys.stderr)
            raise typer.Exit(2) from None
    _print_json(payload)


class DraftDirty(Exception):
    """The draft holds edits that were never pushed: a checkout does not
    replace it without `--steal` (review of #3034, finding 3)."""

    def __init__(self, target: "Target", where, fmt: str) -> None:
        super().__init__(str(where.document))
        self.target, self.where, self.fmt = target, where, fmt

    def payload(self) -> dict:
        from ..sync import read_meta

        try:
            version = int(read_meta(self.where.meta).get("version") or 0)
        except (OSError, TypeError, ValueError):
            version = 0
        return {"target": self.target.kind, "label": self.target.label, "path": str(self.where.document),
                "version": version, "format": self.fmt, "refused": REFUSED_UNPUSHED}


def checkout_draft(client, target: Target, sid: str | None, *, steal: bool = False,
                   visuals: bool = True, quiet: bool = False) -> dict:
    """Check `target`'s summary out to this session's draft and return the
    checkout's JSON (see `summary_checkout`). `visuals` also asks whether
    the entity's Metrics-center tables are set; `quiet` prints nothing on
    stderr. Raises `DraftDirty` -- nothing replaced, nothing read -- when this
    session's draft of `target`, in either format, holds edits its base copy
    lacks, unless `steal`."""
    from .. import notes as notes_file

    if not steal:
        # Whichever format is on disk: a checkout in the other format replaces
        # it too (below), so both are judged before anything is fetched.
        for draft_fmt in EXT_BY_FORMAT:
            existing = draft_paths(_settings(), target, sid, fmt=draft_fmt)
            if existing.document.exists() and notes_file.dirty(existing):
                raise DraftDirty(target, existing, draft_fmt)
    row = _get_summary(client, target.anchors(), html=True)
    state = _visuals_state(client, target) if visuals and row.get("mode") != MODE_LANE else None
    fmt = FORMAT_HTML if _is_html(row) else FORMAT_MARKDOWN
    where = draft_paths(_settings(), target, sid, fmt=fmt)
    text = _draft_text(row)
    version = int(row.get("version") or 0)
    record_mode(row.get("mode"))
    notes_file.checkout(where, body=text, version=version)
    # One stem holds one draft: the other format's document (a checkout from
    # an older server, or before one) is no longer what the base describes.
    for other in (f for f in EXT_BY_FORMAT if f != fmt):
        try:
            draft_paths(_settings(), target, sid, fmt=other).document.unlink()
        except OSError:
            pass
    extra: dict[str, Any] = {}
    if fmt == FORMAT_HTML:
        from ....foundation.durable.durable import write_text_atomic

        chartable = row.get("chartable") if isinstance(row.get("chartable"), dict) else {}
        path = chartable_path(where)
        write_text_atomic(path, json.dumps(chartable, indent=2) + "\n", mode=0o600)
        runs = [e for e in chartable.get("by_run") or [] if isinstance(e, dict)]
        columns = list(chartable.get("columns") or [])
        key_at = columns.index("key") if "key" in columns else -1
        keys = {row_[key_at] for e in runs for row_ in e.get("series") or []
                if key_at >= 0 and isinstance(row_, list) and len(row_) > key_at}
        extra = {
            "format": FORMAT_HTML,
            "html": text,
            "series": len(row.get("series") or []),
            "chartable_path": str(path),
            "chartable": {"runs": len(runs), "metric_keys": len(keys)},
        }
    else:
        try:
            chartable_path(where).unlink()
        except OSError:
            pass
    record_loaded(sid, target)
    if not quiet:
        print(f"checked out {target.kind} summary ({target.label}) v{version}", file=sys.stderr)
        if row.get("mode") == MODE_LANE:
            print(LANE_NOTE, file=sys.stderr)
        if state is not None and state["eligible"] and not state["count"]:
            print(VISUALS_HINT.format(label=target.label, kind=target.kind), file=sys.stderr)
    payload: dict[str, Any] = {
        "target": target.kind,
        "label": target.label,
        "path": str(where.document),
        "version": version,
    }
    if fmt == FORMAT_MARKDOWN:
        payload["markdown"] = text
    payload.update(
        {
            "you": row.get("you"),
            "today": row.get("today"),
            "edited_by": row.get("edited_by"),
            "edited_at": row.get("edited_at"),
            "mode": row.get("mode"),
            "visuals": state,
            **extra,
        }
    )
    return payload


def _visuals_state(client, target: Target) -> dict | None:
    """Whether the entity carries Metrics-center tables and charts, and how many
    are set; None when the server cannot say (an older server, a refused read):
    the checkout never fails on it."""
    try:
        options = client.get_visuals_options(**target.anchors())
    except Exception:  # noqa: BLE001 -- a hint, never a failed checkout
        return None
    return {"eligible": bool(options.get("eligible")), "count": len(options.get("current") or [])}


@summary_app.command("push")
def summary_push(
    project: str = _PROJECT_OPT,
    experiment: str = _EXPERIMENT_OPT,
    directed: bool = _DIRECTED_OPT,
) -> None:
    """Send the checked-out summary, merging if the page moved meanwhile.

    Exit 2: a conflict was written into the file (resolve the markers, push
    again), or an erasure changed the page since your checkout (check out
    again). Exit 1: Probe refused the text (the message says why) or the push
    could not be sent; the file keeps your edits either way."""
    from .. import sync as note_sync, notes as notes_file

    directed = _directed(directed)
    sid = session_id()
    refused: dict[str, Any] = {}
    sent: dict[str, Any] = {}
    head: dict[str, Any] = {}
    with _main()._client() as client:
        target = resolve_target(client, project, experiment)
        anchors = target.anchors()
        where, fmt = checked_out(_settings(), target, sid)
        html = fmt == FORMAT_HTML
        again = f"`probe summary checkout --{target.kind} {target.label} --steal`"
        if not where.document.exists():
            _fail(f"nothing checked out for this session at {where.document}: {again} first")
        if not where.base.exists():
            _fail(f"no base copy beside {where.document}, so no safe merge: {again}, then redo your edit")
        if not note_sync.stamp_matches(where, _read_stamp(where)):
            _fail(
                f"{where.document} was checked out from another Probe server or key; "
                f"{again} here, then redo your edit"
            )

        def send(text: str, base_version: int, op_key: str) -> int:
            field = "html" if html else "markdown"
            stored = _main()._stored_form(field, text)
            if stored != text:
                refused.update(code=SCRUBBED, exit=1, message=scrubbed_message(field, text, stored))
                raise errors.RosError(refused["message"])
            sent["text"] = text
            sent["base"] = base_version
            try:
                # By the draft's extension: an HTML draft goes whole as `html`
                # (the server lifts its series block out), Markdown as before.
                body = {"html": text, "whole_page": True} if html else {"markdown": text}
                row = client.put_summary(
                    **body,
                    expected_version=base_version,
                    session_id=sid,
                    directed=directed,
                    **anchors,
                )
            except errors.ConflictError as exc:
                code = _code(exc)
                if code in (None, VERSION_MOVED):
                    detail = exc.detail if isinstance(exc.detail, dict) else {}
                    if detail.get("version") is not None:
                        if html and isinstance(detail.get("html"), str):
                            head["page"] = (
                                compose_draft(detail["html"], detail.get("series")),
                                int(detail["version"]),
                            )
                        elif not html and isinstance(detail.get("markdown"), str):
                            head["page"] = (detail["markdown"], int(detail["version"]))
                    raise
                # NOT a ConflictError from here on: `notes_file.push` merges those.
                refused.update(code=code, exit=2)
                raise errors.RosError(_message(exc), status=409, detail=exc.detail) from None
            except errors.RosError as exc:
                if _main()._key_refused(exc):
                    refused["key"] = exc  # main() says so in the daemon's words
                refused.update(code=_code(exc), exit=1, message=_message(exc))
                raise
            if html:
                sent["canonical"] = (
                    compose_draft(row["html"], row.get("series")) if isinstance(row.get("html"), str) else None
                )
            else:
                sent["canonical"] = row.get("markdown")
            return int(row.get("version") or 0)

        def fetch() -> tuple[str, int]:
            if "page" in head:  # the 409 carried the head: no second read
                return head.pop("page")
            row = _get_summary(client, anchors, html=html)
            if html and not _is_html(row):
                raise errors.RosError(
                    f"this Probe server no longer serves the summary as html; {again}, then redo your edit"
                )
            return _draft_text(row), int(row.get("version") or 0)

        report = notes_file.push(where, send=send, fetch=fetch, label=f"{target.kind} summary")
    if "key" in refused:
        raise refused["key"]
    detail = report.detail
    if refused.get("code") == ERASED_SINCE_CHECKOUT:
        detail = ERASED_DETAIL.format(kind=target.kind, label=target.label)
    elif refused.get("code") == SESSION_ERASED:
        detail = SESSION_ERASED_DETAIL
    elif refused.get("code") == WRITER_OFF:
        # The server's words, plus the mark the daemon reads (`tools.note_summary_marks`).
        detail = f"{refused.get('message') or LANE_NOTE} {LANE_MARK}"
        record_mode(MODE_LANE)
    elif refused.get("message"):
        detail = refused["message"]
    if report.pushed:
        _adopt_canonical(where, sent.get("text"), sent.get("canonical"), report.version)
        _visuals_follow_push(target, sid, sent.get("base"), report.version)
        record_loaded(sid, target)
        record_mode(MODE_RECORDER)
        owed.settle(owed.SUMMARY, target.keys())
    _print_json(
        {
            "target": target.kind,
            "label": target.label,
            "pushed": report.pushed,
            "merged": report.merged,
            "conflicted": report.conflicted,
            "version": report.version,
            "detail": detail,
        }
    )
    if detail:
        print(f"{target.label}: {detail}", file=sys.stderr)
    if report.pushed:
        print(f"pushed {target.kind} summary ({target.label}) v{report.version}", file=sys.stderr)
        return
    if report.conflicted or refused.get("exit") == 2:
        raise typer.Exit(2)
    if refused or (not report.merged and detail and detail != "no local edits"):
        raise typer.Exit(1)


def scrubbed_message(field: str, text: str, stored: str) -> str:
    """Why a push the credential scrubber would rewrite was refused, naming
    the first place it would change, in the scrubbed text (never echoing the
    credential itself). A page holding a `%XX` / `\\uXXXX` escape is judged
    decoded and blanked whole, so the change is looked for in the decoded page."""
    from ....sdk import redaction

    whole = stored.strip() == SCRUB_MARK and text.strip() != SCRUB_MARK
    if whole:
        text = redaction._decode_escapes(text)
        stored = _main()._stored_form(field, text)
    at = next((i for i, (a, b) in enumerate(zip(text, stored)) if a != b), min(len(text), len(stored)))
    near = " ".join(stored[max(0, at - 30): at + 40].split())
    where = f" near `{near}`" if near and near != SCRUB_MARK else ""
    why = (" (a `%XX` or `\\u` escape in the page, such as a percent-encoded `data:` URI, makes it blank the whole "
           "page; base64-encode the URI)") if whole else ""
    return (f"Probe's credential scrubber would rewrite this page{where}{why}, which would break it silently; "
            "nothing was written. Rename or remove the credential-shaped text (in code, a variable named like a "
            "signature, token, API key or password), then push again.")


def _adopt_canonical(where, sent: str | None, canonical: str | None, version: int) -> None:
    """After a landed push: when the page's own Markdown (what a fresh GET now
    returns) differs from what was sent -- a person's block expanded from the
    stored page, the renderer's spelling -- it becomes the base, and the draft
    too unless it was edited after the send. The next push then diffs against
    what the server holds."""
    from ....foundation.durable.durable import file_lock
    from ..sync import commit, read_text

    if canonical is None or sent is None or canonical == sent:
        return
    with file_lock(where.lock):
        current = read_text(where.document)
        commit(where, body=canonical, version=int(version), write_document=current == sent)


def _read_stamp(where) -> str | None:
    try:
        return where.stamp.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
from probe.shared.notes.summary.first_write import record_loaded  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.notes.summary.visuals import _visuals_follow_push  # noqa: E402 -- pieces need each other; the front door loads this one first
