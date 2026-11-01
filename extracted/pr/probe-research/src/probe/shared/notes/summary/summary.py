"""`probe summary checkout|push|edit|append` and `probe visuals options|set`: the
summary of a project or an experiment, and its Metrics-center tables and charts,
kept by whoever records the session (plan writer-owns-summary §3.4, §3.8).

    probe summary checkout --project willow-sft          # -> JSON with the draft's path and its text
    $EDITOR <path>
    probe summary push --project willow-sft              # merges if the page moved; exit 2 on a conflict
    probe summary checkout --experiment b2-decay [--project willow-sft]
    probe summary edit --project willow-sft --old '<p>Yes.</p>' --new '<p>Yes, by 2.1.</p>'  # no draft
    probe summary append --project willow-sft --html '<p>Next: seeds.</p>'                  # no draft
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

FULL PAGES (ARTIFACT-PAGES P1). Checkout asks for the page as HTML
(`?format=html`); a server that offers it hands over the page, its chart
declarations and the closed set they may name, and the draft is `<sid>.html`
(`<sid>.daemon.html`): ONE file holding the declarations as a
`<script type="application/json" data-probe-series>` block ahead of the page
(`compose_draft`), so one edit and one three-way merge cover both, with the
closed set beside it (`<sid>.chartable.json`, `chartable_path` in the JSON).
Push sends the draft by its extension: `.html` as `html` (the server lifts the
series block out), `.md` as `markdown`. A server older than full pages ignores
the parameter and the draft is Markdown, as before.

LOADING ON THE FIRST WRITE (plan §3.5, D11; ARTIFACT-PAGES P3): the first
`probe` write of a session that lands on a project or experiment whose summary
that session has not checked out checks it out itself and prints the draft's
path on stderr, once per session per entity (`remind`). The entity is read from
the parsed command's own arguments (never the status line's resolver, which
collapses an experiment to its project). When the checkout cannot be made (no
network, a refused read, unpushed edits in the draft) it prints the reminder
line instead, and the write it follows never fails. Under the daemon the
reminder stays a line: the daemon's worker loads its writer's summaries itself.
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

from ....sdk import errors, session_marker

#: Set on every `probe` call the Probe daemon makes (`daemon/worker/worker.py::probe_env`).
DAEMON_SESSION_ENV = "PROBE_DAEMON_SESSION"
#: The daemon's drafts: `<session id>.daemon.md`, apart from the agent's own.
DAEMON_DRAFT = ".daemon"
#: The draft's stem when no session id is known: the entity-addressed file.
SHARED_DRAFT = "note"
#: Kinds of summary anchor.
PROJECT = "project"
EXPERIMENT = "experiment"
#: What `mode` says while the overview lane still writes the team's pages, and
#: once the recorders write them.
MODE_LANE = "lane"
MODE_RECORDER = "recorder"
#: The mark a lane-mode refusal or note carries, which the daemon reads
#: (`tools.note_summary_marks`).
LANE_MARK = "(mode lane)"

#: Where this machine keeps the team's summaries mode as a checkout or a push
#: last saw it (`{"mode", "at", "server"}`): the reminder stays quiet while it
#: reads lane, so agents are not sent to summaries the server would refuse.
MODE_FILE = session_marker.SUMMARIES_MODE_FILE[-1]
#: How long a seen mode stands for the reminder: the flip moves it once.
MODE_TTL_S = session_marker.SUMMARIES_MODE_TTL_S
#: `GET .../summary?format=html` (ARTIFACT-PAGES P1): the page as HTML.
FORMAT_HTML = "html"
FORMAT_MARKDOWN = "markdown"
#: A draft's extension says what push sends.
EXT_BY_FORMAT = {FORMAT_MARKDOWN: ".md", FORMAT_HTML: ".html"}
#: The draft's block of chart declarations, ahead of the page; the server
#: lifts it out (`app/overviews/summary_html.py` `SERIES_BLOCK_ATTR`).
SERIES_ATTR = "data-probe-series"
#: Beside an HTML draft: the closed set its series may name.
CHARTABLE_SUFFIX = ".chartable.json"
#: The server's `summary_writer_off` words (app/overviews/summary.py
#: WRITER_OFF_MESSAGE): since writer-owns-summary R2 no lane writes a `lane`
#: team's summaries, so the door is closed until Probe switches the team.
LANE_NOTE = (
    f"this team's summary door is closed (summaries_by=lane) {LANE_MARK}: "
    "`probe summary push` is refused until Probe switches the team to recorder; "
    "ask Probe (support@prbe.ai) to switch it"
)


def _main():
    """`probe.cli.main`, the module (the package re-exports its `main()`
    function under the same name)."""
    import importlib

    return importlib.import_module("probe.cli.main")  # by name: this file left probe/cli/ (agent:12)


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
    from ....sdk import agent_session, session_marker

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
    from ....cli import refs

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


def draft_paths(settings, target: Target, sid: str | None, *, suffix: str = "", fmt: str = FORMAT_MARKDOWN):
    """The draft's three files (`notes_file.paths_for` under `summaries/`): the
    document is `.md`, or `.html` for a page checked out as HTML (`fmt`)."""
    from .. import notes as notes_file

    stem = sid + (DAEMON_DRAFT if os.environ.get(DAEMON_SESSION_ENV) else "") if sid else SHARED_DRAFT
    return notes_file.paths_for(
        settings,
        target.kind,
        target.id,
        root=notes_file.SUMMARIES_ROOT,
        draft=stem + suffix,
        ext=EXT_BY_FORMAT[fmt],
    )


def checked_out(settings, target: Target, sid: str | None):
    """`(paths, format)` of this session's draft of `target`: the one on disk
    (the newer, should both formats be there), else the Markdown paths."""
    found = []
    for fmt in (FORMAT_HTML, FORMAT_MARKDOWN):
        where = draft_paths(settings, target, sid, fmt=fmt)
        try:
            found.append((where.document.stat().st_mtime, fmt, where))
        except OSError:
            continue
    if not found:
        return draft_paths(settings, target, sid), FORMAT_MARKDOWN
    _mtime, fmt, where = max(found, key=lambda f: f[0])
    return where, fmt


def compose_draft(html: str, series: list | None) -> str:
    """An HTML draft: the page's chart declarations as one JSON block, then the
    page. `</` inside the JSON is written `<\\/`, so a title cannot end the block."""
    body = json.dumps(series or [], indent=2, ensure_ascii=False).replace("</", "<\\/")
    tail = "" if not html or html.endswith("\n") else "\n"
    return f'<script type="application/json" {SERIES_ATTR}>\n{body}\n</script>\n{html}{tail}'


def chartable_path(where) -> Path:
    return where.document.with_suffix(CHARTABLE_SUFFIX)


def _settings():
    from ....sdk.settings.settings import resolve

    return resolve(base_url=_main()._conn.base_url)


def _mode_file() -> Path:
    from ...updates.version_policy import state_dir

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
    if mode not in (MODE_LANE, MODE_RECORDER):
        return
    try:
        from ....foundation.durable.durable import write_text_atomic

        path = _mode_file()
        path.parent.mkdir(parents=True, exist_ok=True)
        write_text_atomic(path, json.dumps({"mode": mode, "at": time.time(), "server": _server()}), mode=0o600)
    except Exception:  # noqa: BLE001 -- a hint for the reminder, never a failed command
        pass


def seen_mode() -> str | None:
    """The mode this machine's last checkout or push saw on this server, within
    MODE_TTL_S; None when unknown."""
    try:
        seen = json.loads(_mode_file().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not (isinstance(seen, dict) and seen.get("server") == _server()
            and time.time() - float(seen.get("at") or 0) < MODE_TTL_S):
        return None
    return seen.get("mode") if seen.get("mode") in (MODE_LANE, MODE_RECORDER) else None


def _seen_lane() -> bool:
    return seen_mode() == MODE_LANE


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
