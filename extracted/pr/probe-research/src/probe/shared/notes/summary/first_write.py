"""a session's first write to an entity: remind it to load that entity's summary, or load it, once per session."""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import typer

#: Set by `probe exec` and the SDK in the job they launch (`write_gate.RUN_ID_ENV`).
RUN_ID_ENV = "PROBE_RUN_ID"

#: The reminder (plan §3.5). `{label}` is the ref as the command named it.
REMINDER = "Summary of {label} not loaded this session - probe summary checkout --{kind} {label}"
#: What the first write's own checkout says (ARTIFACT-PAGES P3), in the
#: reminder's place. Wording PROPOSED.
LOADED = ("Summary of {label} checked out for this session (v{version}): {path} - "
          "edit it, then probe summary push --{kind} {label}")
#: The first write's own checkout (`_load_on_first_write`) gets this long for
#: every request it makes, with no retry.
FIRST_WRITE_LOAD_S = 5.0


# -- the reminder ---------------------------------------------------------------

#: Command words whose own parameters name the entity a write lands on, by
#: what the parameter IS: `--experiment` / `experiment_id` an experiment,
#: `--project` / `project_id` a project, and a create's new `slug` its own kind.
#: A parameter that may be either (`run move --to`) names nothing here.
_EXPERIMENT_PARAMS = ("experiment", "experiment_id")
_PROJECT_PARAMS = ("project", "project_id")
#: The summary's own commands: each reads the summary first, and the writes ARE the summary.
_OWN = frozenset({"summary checkout", "summary push", "summary edit", "summary append"})
_LOADED_DIR = "sessions"


def _loaded_file(sid: str) -> Path:
    from ...updates.version_policy import state_dir

    return state_dir() / "summaries" / _LOADED_DIR / f"{sid}.json"


#: What `_loaded_file` keeps: summaries checked out, reminders given, and the
#: entities whose note the first write printed (`first_touch`, key `writer:kind:ref`).
_LOADED_KEYS = ("loaded", "reminded", "noted")


def _read_loaded(sid: str) -> dict[str, list[str]]:
    try:
        data = json.loads(_loaded_file(sid).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        data = {}
    if not isinstance(data, dict):
        data = {}
    return {k: [str(x) for x in data.get(k) or [] if isinstance(x, str)] for k in _LOADED_KEYS}


def _write_loaded(sid: str, update) -> None:
    from ....foundation.durable.durable import file_lock, write_text_atomic

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
    from ....sdk import session_marker

    kind, matched = session_marker.classify_probe_args(list(args))
    if kind != "write" or matched.removeprefix("probe ") in _OWN:
        return None
    from probe.shared.command_rules import command_rules as precheck

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
    """After a `probe` write exited 0, once per session per entity whose
    summary this session has not checked out: check it out and print `LOADED`
    (ARTIFACT-PAGES P3), or -- under the daemon (its worker loads the
    writer's summaries), or when the checkout cannot be made -- print
    `REMINDER`. Never raises. Not in a session the daemon records for the
    agent (the summary is the daemon's there), not in a shell with no session,
    and not while this machine's last checkout or push saw the team in lane
    mode (`MODE_FILE`, a day): the server would refuse the summary."""
    try:
        sid = session_id()
        if sid is None or os.environ.get(RUN_ID_ENV):
            return  # no session, or a run recording its own data (`probe exec`, the SDK)
        if not os.environ.get(DAEMON_SESSION_ENV):
            from ....sdk import session_marker

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
        loaded = None if os.environ.get(DAEMON_SESSION_ENV) else _load_on_first_write(sid, kind, ref)
        print(loaded or REMINDER.format(label=ref, kind=kind), file=sys.stderr)
        _write_loaded(sid, lambda d: d.update(reminded=sorted(set(d["reminded"]) | {key})))
    except Exception:  # noqa: BLE001 -- a reminder, never a failed write
        return


def _load_on_first_write(sid: str, kind: str, ref: str) -> str | None:
    """ARTIFACT-PAGES P3: check the summary out for this session and say where
    it went (`LOADED`); None -- the caller prints the reminder -- when that
    cannot be done: no server answer, a refused read, or a draft of this
    session's for the entity that holds unpushed edits (never replaced).
    Bounded: one attempt per request, `FIRST_WRITE_LOAD_S` for all of them
    (review of #3034, finding 6) -- the write it follows has already landed,
    and a slow server must not hold the agent's command."""
    from ....sdk.delivery.transport.deadlines import deadline_scope

    try:
        with deadline_scope(time.monotonic() + FIRST_WRITE_LOAD_S), _main()._client() as client:
            transport = getattr(client, "transport", None)
            if transport is not None:
                transport.max_retries = 0
                transport.timeout = min(float(getattr(transport, "timeout", FIRST_WRITE_LOAD_S)),
                                        FIRST_WRITE_LOAD_S)
            target = resolve_target(
                client, ref if kind == PROJECT else None, ref if kind == EXPERIMENT else None
            )
            payload = checkout_draft(client, target, sid, visuals=False, quiet=True)
    except (Exception, typer.Exit):  # noqa: BLE001 -- DraftDirty, no answer: the reminder, never a failed write
        return None
    return LOADED.format(label=ref, kind=kind, path=payload["path"], version=payload["version"])
from probe.shared.notes.summary.checkout_push import checkout_draft  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.notes.summary.summary import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    DAEMON_SESSION_ENV,
    EXPERIMENT,
    PROJECT,
    Target,
    _main,
    _seen_lane,
    resolve_target,
    session_id,
)
