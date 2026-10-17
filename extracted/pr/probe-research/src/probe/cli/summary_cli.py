"""`probe summary checkout|push` and `probe visuals options|set`: the summary of
a project or an experiment, and its Metrics-center tables and charts, kept by
whoever records the session (plan writer-owns-summary §3.4, §3.8).

    probe summary checkout --project willow-sft          # -> JSON with the draft's path and the Markdown
    $EDITOR <path>
    probe summary push --project willow-sft              # merges if the page moved; exit 2 on a conflict
    probe summary checkout --experiment b2-decay [--project willow-sft]
    probe visuals options --experiment b2-decay          # the closed set, and a draft of the current list
    probe visuals set --experiment b2-decay --file <path>

THE FILE MODEL IS `notes_file`'s: checkout writes the server's text and records
it as the base; push sends the file and, when the page moved (409
`version_moved`), merges locally with `merge3` against the head the 409 carries
and asks for another push. Two things differ:

1. ONE DRAFT PER SESSION: `<state>/summaries/<kind>/<id>/<session id>.md`, 0600
   (`<session id>.daemon.md` for the daemon recording that session, so the
   agent's own checkout never replaces the daemon's unpushed edits). Two
   sessions sharing one file could both check out a clean copy and overwrite
   each other before either pushed. A session's checkout replaces its own draft;
   only a shell with no session id (a person's terminal) shares the
   entity-addressed `note.md`, which `claim` guards as `probe notes` does.
2. AN ERASURE IS NOT MERGED: 409 `erased_since_checkout` means the base this
   draft grew from held words a session erasure removed; merging from it would
   carry them back. Push refuses (exit 2) and says to check out again. There is
   no `--force`: it would send the current version with the old text and slip
   the erased words past that check.

THE REMINDER (plan §3.5, D11): the first `probe` write of a session that lands
on a project or experiment whose summary that session has not checked out
prints one line on stderr, once per session per entity. The entity is read from
the parsed command's own arguments (never the status line's resolver, which
collapses an experiment to its project), and no server is asked.
"""

from __future__ import annotations

import json
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import typer

from ..sdk import errors

summary_app = typer.Typer(
    no_args_is_help=True,
    help="a project's or experiment's summary (its Overview page) as a Markdown file: checkout, edit, push",
)
visuals_app = typer.Typer(
    no_args_is_help=True,
    help="the tables and charts of a project's or experiment's Metrics center",
)

#: Set on every `probe` call the Probe daemon makes (`daemon/worker.py::probe_env`).
DAEMON_SESSION_ENV = "PROBE_DAEMON_SESSION"
#: The daemon's drafts: `<session id>.daemon.md`, apart from the agent's own.
DAEMON_DRAFT = ".daemon"
#: Set by `probe exec` and the SDK in the job they launch (`write_gate.RUN_ID_ENV`).
RUN_ID_ENV = "PROBE_RUN_ID"
#: The draft's stem when no session id is known: the entity-addressed file.
SHARED_DRAFT = "note"
#: Kinds of summary anchor.
PROJECT = "project"
EXPERIMENT = "experiment"
#: 409 codes a push does not merge (CONTRACT.md).
ERASED_SINCE_CHECKOUT = "erased_since_checkout"
SESSION_ERASED = "session_erased"
VERSION_MOVED = "version_moved"
WRITER_OFF = "summary_writer_off"
#: What `mode` says while the overview lane still writes the team's pages.
MODE_LANE = "lane"
#: The mark a lane-mode refusal or note carries, which the daemon reads
#: (`tools.note_summary_marks`).
LANE_MARK = "(mode lane)"

#: Where this machine keeps the team's summaries mode as a checkout or a push
#: last saw it (`{"mode", "at", "server"}`): the reminder stays quiet while it
#: reads lane, so agents are not sent to summaries the server would refuse.
MODE_FILE = "mode.json"
#: How long a seen mode stands for the reminder: the flip moves it once.
MODE_TTL_S = 24 * 3600

#: The reminder (plan §3.5). `{label}` is the ref as the command named it.
REMINDER = "Summary of {label} not loaded this session - probe summary checkout --{kind} {label}"
#: What a push says when the draft grew from a base an erasure changed.
ERASED_DETAIL = (
    "a session erasure changed this {kind}'s summary since your checkout, so it was not merged; "
    "check out again (`probe summary checkout --{kind} {label}`) and redo your edit"
)
SESSION_ERASED_DETAIL = "this session was erased, so its summary writes are refused"
LANE_NOTE = (
    f"this team's summaries are still written by Probe's overview lane {LANE_MARK}: "
    "`probe summary push` is refused until that changes"
)
#: Checkout's line when the entity carries Metrics-center visuals and none is set
#: (plan 3.8): the reminder rides the object at the moment it is handed over.
VISUALS_HINT = "Tables and charts for {label}: none set - read overview-visuals, then probe visuals options --{kind} {label}"


def _main():
    """`probe.cli.main`, the module (the package re-exports its `main()`
    function under the same name)."""
    import importlib

    return importlib.import_module(f"{__package__}.main")


def _print_json(obj: Any) -> None:
    _main()._print_json(obj)


def _directed(flag: bool) -> bool:
    """`--directed` as this command saw it. `probe`'s own `main` strips the flag
    before the parser runs (`write_gate.split_directed`) and keeps it on the
    connection; a direct `app(...)` call (tests) parses it here."""
    return bool(flag or getattr(_main()._conn, "directed", False))


def session_id() -> str | None:
    """The session whose draft this is: the daemon's (it records that session),
    else the coding agent's own. None in a shell with neither, or one whose id
    is not safe as a file name."""
    from ..sdk import agent_session, session_marker

    sid = os.environ.get(DAEMON_SESSION_ENV) or agent_session.session_id_from_env()
    return sid if sid and session_marker.valid_session_id(sid) else None


@dataclass(frozen=True)
class Target:
    """The project or experiment a summary command names."""

    kind: str  # PROJECT | EXPERIMENT
    id: str
    project_id: str | None  # an experiment: the project it is filed under
    slug: str | None
    label: str  # the ref as typed, for messages

    def anchors(self) -> dict[str, str | None]:
        """The SDK's anchor keywords (`project=` / `experiment=`)."""
        if self.kind == EXPERIMENT:
            return {"project": self.project_id, "experiment": self.id}
        return {"project": self.id}

    def keys(self) -> set[str]:
        """Every spelling a later command may name this entity by: the reminder
        matches on any of them, with no server call."""
        names = {self.id, f"id:{self.id}", self.label}
        if self.slug:
            names.add(self.slug)
        return {f"{self.kind}:{n}" for n in names if n}


def resolve_target(client, project: str | None, experiment: str | None) -> Target:
    """`--experiment E [--project P]` or `--project P`; exactly one entity."""
    from . import refs

    if experiment is not None:
        hint = _main()._project_id(client, project) if project is not None else None
        ref = refs.resolve(client, EXPERIMENT, experiment, project_hint=hint)
        row = ref.row or {}
        parent = row.get("project_id") or row.get("parent_project_id") or hint
        return Target(
            EXPERIMENT, str(ref.id), str(parent) if parent else None, row.get("slug"), experiment
        )
    if project is not None:
        ref = refs.resolve(client, PROJECT, project)
        return Target(PROJECT, str(ref.id), None, (ref.row or {}).get("slug"), project)
    raise typer.BadParameter(
        "pass --project P, or --experiment E (with --project P to save a lookup)"
    )


def draft_paths(settings, target: Target, sid: str | None, *, suffix: str = ""):
    """The draft's three files (`notes_file.paths_for` under `summaries/`)."""
    from . import notes_file

    stem = sid + (DAEMON_DRAFT if os.environ.get(DAEMON_SESSION_ENV) else "") if sid else SHARED_DRAFT
    return notes_file.paths_for(
        settings,
        target.kind,
        target.id,
        root=notes_file.SUMMARIES_ROOT,
        draft=stem + suffix,
    )


def _settings():
    from ..sdk.config import resolve

    return resolve(base_url=_main()._conn.base_url)


def _get_summary(client, anchors: dict) -> dict:
    """`client.get_summary`, with FastAPI's own 404 (a server older than the
    summary routes) said as the writes say it. The SDK read keeps raising
    `NotFoundError` there: the MCP's summary views read that as "cannot say"."""
    from ..sdk.client import _PREDATES_SUMMARIES, _route_absent

    try:
        return client.get_summary(**anchors)
    except errors.NotFoundError as exc:
        if _route_absent(exc):
            raise errors.CapabilityUnavailable("summaries", _PREDATES_SUMMARIES) from exc
        raise


def _mode_file() -> Path:
    from ..version_policy import state_dir

    return state_dir() / "summaries" / MODE_FILE


def _server() -> str:
    """The server this command talks to: `--base-url`, else the active context's
    (`_settings`). The bare flag is empty without `--base-url`, which keyed every
    server's lane mode the same."""
    try:
        return str(_settings().base_url or "")
    except Exception:  # noqa: BLE001 -- no config: the flag, or nothing
        return str(getattr(_main()._conn, "base_url", "") or "")


def record_mode(mode: str | None) -> None:
    """Remember the mode a checkout or a push just saw (never raises)."""
    if mode not in (MODE_LANE, "recorder"):
        return
    try:
        from ..sdk.durable import write_text_atomic

        path = _mode_file()
        path.parent.mkdir(parents=True, exist_ok=True)
        write_text_atomic(path, json.dumps({"mode": mode, "at": time.time(), "server": _server()}), mode=0o600)
    except Exception:  # noqa: BLE001 -- a hint for the reminder, never a failed command
        pass


def _seen_lane() -> bool:
    try:
        seen = json.loads(_mode_file().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return (isinstance(seen, dict) and seen.get("mode") == MODE_LANE and seen.get("server") == _server()
            and time.time() - float(seen.get("at") or 0) < MODE_TTL_S)


def _fail(message: str, code: int = 1) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise typer.Exit(code)


def _code(exc: errors.RosError) -> str | None:
    detail = getattr(exc, "detail", None)
    return detail.get("code") if isinstance(detail, dict) else None


def _message(exc: errors.RosError) -> str:
    detail = getattr(exc, "detail", None)
    if isinstance(detail, dict) and detail.get("message"):
        return str(detail["message"])
    return str(exc)


_PROJECT_OPT = typer.Option(None, "--project", help="project slug (or id:<uuid>)")
_EXPERIMENT_OPT = typer.Option(None, "--experiment", help="experiment slug (or id:<uuid>)")
_DIRECTED_OPT = typer.Option(
    False,
    "--directed",
    help="the researcher asked for this write (the daemon sees it and does not repeat it)",
)


# -- probe summary ------------------------------------------------------------


@summary_app.command("checkout")
def summary_checkout(
    project: str = _PROJECT_OPT,
    experiment: str = _EXPERIMENT_OPT,
    steal: bool = typer.Option(
        False,
        "--steal",
        help="no session id only: take the shared file although it has unpushed edits",
    ),
) -> None:
    """Pull the summary to a Markdown file; edit it, then `probe summary push` with the same flag.

    Prints JSON: `path` (the draft), `version`, `markdown`, `you` and `today`
    (for an entry's `## <date> · <name>`), `edited_by`, `edited_at` and `mode`.
    A person's own blocks show as `<!-- kept: hN -->` ... `<!-- /kept -->`:
    leave them where they are. The draft is this session's own file, in the
    state directory at 0600; checking out again replaces it with the page."""
    from . import notes_file

    with _main()._client() as client:
        target = resolve_target(client, project, experiment)
        row = _get_summary(client, target.anchors())
        visuals = _visuals_state(client, target) if row.get("mode") != MODE_LANE else None
    sid = session_id()
    where = draft_paths(_settings(), target, sid)
    if sid is None:
        refusal = notes_file.claim(where, steal=steal)
        if refusal is not None:
            print(refusal, file=sys.stderr)
            raise typer.Exit(2)
    markdown = row.get("markdown") or ""
    version = int(row.get("version") or 0)
    record_mode(row.get("mode"))
    notes_file.checkout(where, body=markdown, version=version)
    record_loaded(sid, target)
    print(f"checked out {target.kind} summary ({target.label}) v{version}", file=sys.stderr)
    if row.get("mode") == MODE_LANE:
        print(LANE_NOTE, file=sys.stderr)
    if visuals is not None and visuals["eligible"] and not visuals["count"]:
        print(VISUALS_HINT.format(label=target.label, kind=target.kind), file=sys.stderr)
    _print_json(
        {
            "target": target.kind,
            "label": target.label,
            "path": str(where.document),
            "version": version,
            "markdown": markdown,
            "you": row.get("you"),
            "today": row.get("today"),
            "edited_by": row.get("edited_by"),
            "edited_at": row.get("edited_at"),
            "mode": row.get("mode"),
            "visuals": visuals,
        }
    )


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
    from . import note_sync, notes_file

    directed = _directed(directed)
    sid = session_id()
    refused: dict[str, Any] = {}
    sent: dict[str, Any] = {}
    head: dict[str, Any] = {}
    with _main()._client() as client:
        target = resolve_target(client, project, experiment)
        anchors = target.anchors()
        where = draft_paths(_settings(), target, sid)
        again = f"`probe summary checkout --{target.kind} {target.label}`"
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
            sent["text"] = text
            sent["base"] = base_version
            try:
                row = client.put_summary(
                    text,
                    expected_version=base_version,
                    session_id=sid,
                    directed=directed,
                    **anchors,
                )
            except errors.ConflictError as exc:
                code = _code(exc)
                if code in (None, VERSION_MOVED):
                    detail = exc.detail if isinstance(exc.detail, dict) else {}
                    if (
                        isinstance(detail.get("markdown"), str)
                        and detail.get("version") is not None
                    ):
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
            sent["canonical"] = row.get("markdown")
            return int(row.get("version") or 0)

        def fetch() -> tuple[str, int]:
            if "page" in head:  # the 409 carried the head: no second read
                return head.pop("page")
            row = _get_summary(client, anchors)
            return row.get("markdown") or "", int(row.get("version") or 0)

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
        record_mode("recorder")
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


def _adopt_canonical(where, sent: str | None, canonical: str | None, version: int) -> None:
    """After a landed push: when the page's own Markdown (what a fresh GET now
    returns) differs from what was sent -- a person's block expanded from the
    stored page, the renderer's spelling -- it becomes the base, and the draft
    too unless it was edited after the send. The next push then diffs against
    what the server holds."""
    from ..sdk.durable import file_lock
    from .note_sync import commit, read_text

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


# -- probe visuals ------------------------------------------------------------

#: The draft of a visuals list sits beside the summary's: `<session>.visuals.json`.
VISUALS_SUFFIX = ".visuals"


def _visuals_draft(target: Target, sid: str | None) -> Path:
    where = draft_paths(_settings(), target, sid, suffix=VISUALS_SUFFIX)
    return where.document.with_suffix(".json")


def _visuals_version_file(draft: Path) -> Path:
    """Beside the draft: the page version `visuals options` read, which a `set`
    without `--version` sends as its precondition (`.meta.json`, so the daemon's
    shell may not write it). A list someone set since then is a 409, never a
    silent overwrite."""
    return draft.with_name(f"{draft.stem}.meta.json")


def _remember_visuals_version(draft: Path, version: Any, *, only_if=None) -> None:
    """Under the draft's lock, so a `set` and this session's `summary push`
    finishing together cannot interleave a check with a write. `only_if` gets
    the version remembered now and says whether to replace it."""
    from ..sdk.durable import file_lock, write_text_atomic

    try:
        with file_lock(draft.with_name(f"{draft.stem}.lock")):
            if only_if is not None and not only_if(_remembered_visuals_version(draft)):
                return
            write_text_atomic(_visuals_version_file(draft), json.dumps({"version": int(version or 0)}), mode=0o600)
    except (OSError, TypeError, ValueError):
        pass  # `set` falls back to the page's current version


def _remembered_visuals_version(draft: Path) -> int | None:
    try:
        return int(json.loads(_visuals_version_file(draft).read_text(encoding="utf-8"))["version"])
    except (OSError, ValueError, KeyError, TypeError):
        return None


# A summary push and a visuals set bump the same page counter, but each keeps
# the other's half (a push keeps `series.visuals`, a set keeps the body byte for
# byte: `service.write_locked`). So when this session's own write landed on the
# exact version the other half was read at, that half still describes the page
# and moves to the new version: the next write is not refused, or merged, for
# this session's own bump. Any other version means someone else wrote: left as is.


def _visuals_follow_push(target: Target, sid: str | None, before: int | None, after: int) -> None:
    draft = _visuals_draft(target, sid)
    if before is not None and _remembered_visuals_version(draft) == int(before):
        _remember_visuals_version(draft, after, only_if=lambda now: now == int(before))


def _summary_follow_set(target: Target, sid: str | None, before: int, after: int) -> None:
    from ..sdk.durable import file_lock, write_text_atomic
    from .note_sync import read_meta

    where = draft_paths(_settings(), target, sid)
    if not where.meta.exists():
        return
    try:
        with file_lock(where.lock):
            meta = read_meta(where.meta)
            if meta.get("version") is None or int(meta["version"]) != int(before):
                return
            write_text_atomic(where.meta, json.dumps({**meta, "version": int(after)}, indent=2), mode=0o600)
    except (OSError, TypeError, ValueError):
        pass  # the next push merges instead


@visuals_app.command("options")
def visuals_options(project: str = _PROJECT_OPT, experiment: str = _EXPERIMENT_OPT) -> None:
    """What this entity's tables and charts may name (metric keys, configs,
    runs, groups, caps), the current list and the page's version.

    Also writes the current list to a draft file (`path` in the JSON, 0600 in
    the state directory): edit it, then `probe visuals set` with the same flag."""
    from ..sdk.durable import write_text_atomic

    with _main()._client() as client:
        target = resolve_target(client, project, experiment)
        options = client.get_visuals_options(**target.anchors())
    draft = _visuals_draft(target, session_id())
    draft.parent.mkdir(parents=True, exist_ok=True)
    write_text_atomic(draft, json.dumps(options.get("current") or [], indent=2) + "\n", mode=0o600)
    _remember_visuals_version(draft, options.get("version"))
    _print_json({**options, "path": str(draft)})


@visuals_app.command("set")
def visuals_set(
    project: str = _PROJECT_OPT,
    experiment: str = _EXPERIMENT_OPT,
    file: str = typer.Option(
        None,
        "--file",
        help='the visuals JSON (a list, or {"visuals": [...]}); default: the draft `options` wrote',
    ),
    version: int = typer.Option(
        None,
        "--version",
        help="the page version you chose against (default: the one `visuals options` read)",
    ),
    directed: bool = _DIRECTED_OPT,
) -> None:
    """Replace the tables and charts with the list in the file. The server
    checks every name against the closed set (`probe visuals options`) and
    reads the numbers itself.

    Exit 2: the page moved since `--version`, or since `visuals options` read
    it (the current list is printed: choose again). Exit 1: refused (the
    checker's reason) or not sent."""
    directed = _directed(directed)
    with _main()._client() as client:
        target = resolve_target(client, project, experiment)
        draft = _visuals_draft(target, session_id())
        path = Path(file).expanduser() if file else draft
        remembered = _remembered_visuals_version(draft) if version is None else None
        if not file and version is None and remembered is None:
            # The draft's version is what keeps a list someone set since from
            # being overwritten: without it, never the page's current one.
            _fail(
                f"no page version is recorded beside {draft}: "
                f"`probe visuals options --{target.kind} {target.label}` first, or pass --version"
            )
        try:
            raw = sys.stdin.read() if file == "-" else path.read_text(encoding="utf-8")
            data = json.loads(raw)
        except (OSError, UnicodeDecodeError, ValueError) as exc:
            _fail(f"could not read the visuals from {file or path}: {exc}")
        visuals = data.get("visuals") if isinstance(data, dict) else data
        if not isinstance(visuals, list):
            _fail('the file holds a JSON list of visuals, or {"visuals": [...]}')
        anchors = target.anchors()
        try:
            if version is not None:
                expected = int(version)
            elif remembered is not None:
                expected = remembered
            else:
                expected = int(client.get_visuals_options(**anchors).get("version") or 0)
            row = client.put_visuals(
                visuals, expected_version=expected, directed=directed, **anchors
            )
        except errors.ConflictError as exc:
            detail = exc.detail if isinstance(exc.detail, dict) else {}
            _print_json(
                {
                    "target": target.kind,
                    "label": target.label,
                    "set": False,
                    "version": detail.get("version"),
                    "current": detail.get("current"),
                }
            )
            _fail(
                f"{target.label}: the page moved since version {expected}; the current list is above",
                2,
            )
        except errors.RosError as exc:
            if _main()._key_refused(exc):
                raise  # main() says so in the daemon's words
            lane = f" {LANE_MARK}" if _code(exc) == WRITER_OFF else ""
            _fail(f"{target.label}: {_message(exc)}{lane}")
    if not file:  # the draft now holds what the page shows, at this version
        # Never backwards: a push of this session's that landed after this set
        # has already moved the remembered version past it.
        _remember_visuals_version(
            draft, row.get("version"), only_if=lambda now: now is None or now <= int(row.get("version") or 0)
        )
    if row.get("version") is not None and int(row["version"]) != expected:
        _summary_follow_set(target, session_id(), expected, int(row["version"]))
    _print_json({"target": target.kind, "label": target.label, "set": True, **row})
    print(
        f"set {len(visuals)} visuals on {target.kind} {target.label} (v{row.get('version')})",
        file=sys.stderr,
    )


# -- the reminder ---------------------------------------------------------------

#: Command words whose own parameters name the entity a write lands on, by
#: what the parameter IS: `--experiment` / `experiment_id` an experiment,
#: `--project` / `project_id` a project, and a create's new `slug` its own kind.
#: A parameter that may be either (`run move --to`) names nothing here.
_EXPERIMENT_PARAMS = ("experiment", "experiment_id")
_PROJECT_PARAMS = ("project", "project_id")
#: The summary's own commands: a push IS the summary, and both read it first.
_OWN = frozenset({"summary checkout", "summary push"})
_LOADED_DIR = "sessions"


def _loaded_file(sid: str) -> Path:
    from ..version_policy import state_dir

    return state_dir() / "summaries" / _LOADED_DIR / f"{sid}.json"


def _read_loaded(sid: str) -> dict[str, list[str]]:
    try:
        data = json.loads(_loaded_file(sid).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"loaded": [], "reminded": []}
    if not isinstance(data, dict):
        return {"loaded": [], "reminded": []}
    return {
        k: [str(x) for x in data.get(k) or [] if isinstance(x, str)] for k in ("loaded", "reminded")
    }


def _write_loaded(sid: str, update) -> None:
    from ..sdk.durable import file_lock, write_text_atomic

    path = _loaded_file(sid)
    path.parent.mkdir(parents=True, exist_ok=True)
    with file_lock(path.with_suffix(".lock")):
        data = _read_loaded(sid)
        update(data)
        write_text_atomic(path, json.dumps(data), mode=0o600)


def record_loaded(sid: str | None, target: Target) -> None:
    """This session has the summary of `target` (a checkout or a push): no reminder for it."""
    if not sid:
        return
    try:
        _write_loaded(sid, lambda d: d.update(loaded=sorted(set(d["loaded"]) | target.keys())))
    except OSError:
        pass  # a reminder too many, never a failed checkout


def landing(args: list[str]) -> tuple[str, str] | None:
    """`(kind, ref)` of the project or experiment a `probe` write lands on, from
    the CLI's own parse of its arguments; None for a read, an unscoped write, a
    parameter that could be either, or the summary's own commands."""
    from ..sdk import session_marker

    kind, matched = session_marker.classify_probe_args(list(args))
    if kind != "write" or matched.removeprefix("probe ") in _OWN:
        return None
    from probe.daemon import precheck

    try:
        parsed = precheck.parse(list(args))
    except precheck.ParseError:
        return None
    if parsed.path in _OWN:
        return None

    def first(names: tuple[str, ...]) -> str | None:
        for name in names:
            value = next((v for v in precheck._strings(parsed.params.get(name)) if v.strip()), None)
            if value:
                return value
        return None

    if parsed.path == "experiment create":
        slug = first(("slug",))
        return (EXPERIMENT, slug) if slug else None
    if parsed.path == "project create":
        slug = first(("slug",))
        return (PROJECT, slug) if slug else None
    found = first(_EXPERIMENT_PARAMS)
    if found:
        return EXPERIMENT, found
    found = first(_PROJECT_PARAMS)
    return (PROJECT, found) if found else None


def remind(args: list[str]) -> None:
    """After a `probe` write exited 0: print `REMINDER` once per session per
    entity whose summary this session has not checked out. Never raises, never
    asks a server. Not in a session the daemon records for the agent (the
    summary is the daemon's there), not in a shell with no session, and not
    while this machine's last checkout or push saw the team in lane mode
    (`MODE_FILE`, a day): the server would refuse the summary."""
    try:
        sid = session_id()
        if sid is None or os.environ.get(RUN_ID_ENV):
            return  # no session, or a run recording its own data (`probe exec`, the SDK)
        if not os.environ.get(DAEMON_SESSION_ENV):
            from ..sdk import session_marker

            if session_marker.session_state(sid) == session_marker.STATE_DAEMON:
                return
        head = args[: args.index("--")] if "--" in args else list(args)
        if "--help" in head or _seen_lane():
            return  # a lane team's summaries are not the agent's to keep yet
        found = landing(list(args))
        if found is None:
            return
        kind, ref = found
        key = f"{kind}:{ref}"
        state = _read_loaded(sid)
        if key in state["loaded"] or key in state["reminded"]:
            return
        print(REMINDER.format(label=ref, kind=kind), file=sys.stderr)
        _write_loaded(sid, lambda d: d.update(reminded=sorted(set(d["reminded"]) | {key})))
    except Exception:  # noqa: BLE001 -- a reminder, never a failed write
        return
