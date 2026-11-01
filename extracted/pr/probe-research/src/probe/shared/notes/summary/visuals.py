"""probe visuals options / set: the tables and charts list, kept in step with this session's summary draft."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import typer

from ....sdk import errors
from probe.shared.notes.summary.summary import (
    LANE_MARK,
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
    draft_paths,
    resolve_target,
    session_id,
)
visuals_app = typer.Typer(
    no_args_is_help=True,
    help="the tables and charts of a project's or experiment's Metrics center",
)


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
    from ....foundation.durable.durable import file_lock, write_text_atomic

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
    from ....foundation.durable.durable import file_lock, write_text_atomic
    from ..sync import read_meta

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
    from ....foundation.durable.durable import write_text_atomic

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
from probe.shared.notes.summary.checkout_push import WRITER_OFF  # noqa: E402 -- pieces need each other; the front door loads this one first
