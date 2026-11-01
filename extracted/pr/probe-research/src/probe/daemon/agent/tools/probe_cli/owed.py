"""what a run owes before it ends: summaries, notes and visuals its own commands left unpushed; the team's summaries mode."""

from __future__ import annotations

import asyncio
import json
import time
from typing import Any
from probe.shared.command_rules import command_rules as precheck



#: The run's tally (`Deps.ledger_from`, the visuals sets and the flags), kept
#: in the store until the run's end stands (`tally_settled`): a run paused after
#: ROUNDS_BEFORE_YIELD carries on in the next bite with new Deps, and still owes.
SUMMARY_TALLY = "summary_tally"
_TALLY_SETS = ("concluded", "visuals_landed")
_TALLY_FLAGS = ("summaries_off", "summaries_owed_asked", "notes_owed_asked", "visuals_owed_asked")


def _tally(deps: Deps) -> None:
    """Read the stored tally into `deps`, once per Deps."""
    if deps.tally_loaded:
        return
    deps.tally_loaded = True
    saved = deps.store.fact(SUMMARY_TALLY)
    if not isinstance(saved, dict):
        return
    for name in _TALLY_SETS:
        getattr(deps, name).update(str(x) for x in saved.get(name) or [] if isinstance(x, str))
    for name in _TALLY_FLAGS:
        setattr(deps, name, getattr(deps, name) or bool(saved.get(name)))
    state = saved.get("visuals_state")
    if isinstance(state, dict):
        deps.visuals_state.update({k: v for k, v in state.items() if isinstance(v, dict) and k not in deps.visuals_state})
    if isinstance(saved.get("ledger_from"), int):
        deps.ledger_from = max(deps.ledger_from, saved["ledger_from"])


#: The team's summaries mode as last seen (`{"mode", "at"}`): a checkout's JSON,
#: a refused push or set (lane), a landed push (recorder), or
#: `summaries_mode`'s read. The writer is sent back for a summary only in
#: recorder mode: in lane mode the push is refused, and asking costs rounds.
SUMMARIES_MODE = "summaries_mode"
#: How long a seen mode stands: the global flip moves it once, and a stale
#: `lane` only skips a nudge.
SUMMARIES_MODE_TTL_S = 1800


#: The commands that keep a summary and its tables: in lane mode the server
#: refuses the writes, and the bench's lane replays spent a quarter more on them
#: (12 checkouts, 3 pushes, 12 visuals calls a session). Once a checkout or a
#: refusal said lane, they are not run until the seen mode expires.
SUMMARY_COMMANDS = frozenset({"summary checkout", "summary push", "visuals options", "visuals set"})
LANE_SKIP = ("not run: Probe's overview lane still writes this team's summaries and tables (mode lane), so "
             "`probe summary` and `probe visuals` wait until it hands them over. Record everything else as usual.")


def _mode_seen(deps: Deps) -> str | None:
    """The stored mode while fresh (`SUMMARIES_MODE`), else None; asks nobody."""
    saved = deps.store.fact(SUMMARIES_MODE)
    if isinstance(saved, dict) and time.time() - float(saved.get("at") or 0) < SUMMARIES_MODE_TTL_S:
        return saved.get("mode")
    return None


def _note_mode(deps: Deps, mode: str) -> None:
    deps.store.set_fact(SUMMARIES_MODE, {"mode": mode, "at": time.time()})


async def summaries_mode(deps: Deps, owed: str) -> str | None:
    """`lane` | `recorder` | None (unknown: the server could not say). The
    stored mode while fresh, else one summary read of `owed` (`kind ref`)."""
    from probe.daemon.session import probe_api

    seen = _mode_seen(deps)
    if seen in probe_api.SUMMARIES_MODES:
        return seen
    kind, _, ref = owed.partition(" ")
    try:
        mode = await asyncio.wait_for(probe_api.summaries_mode(deps.probe_env, kind, ref), probe_api.SCOPE_TIMEOUT_S)
    except probe_api.KeyRefused:
        _mark_key_refused(deps)  # the worker hands recording back, as for any refused key
        return None
    except Exception:  # noqa: BLE001 -- unknown: no nudge
        return None
    if mode:
        _note_mode(deps, mode)
    return mode


def tally_save(deps: Deps) -> None:
    deps.store.set_fact(SUMMARY_TALLY, {
        **{name: sorted(getattr(deps, name)) for name in _TALLY_SETS},
        **{name: bool(getattr(deps, name)) for name in _TALLY_FLAGS},
        "visuals_state": deps.visuals_state,
        "ledger_from": deps.ledger_from,
    })


def tally_settled(deps: Deps) -> None:
    """The run's end stands: the next run starts owing nothing (it reads the
    ledger from here on). What the last checkouts said about tables
    (`visuals_state`) stays for the session."""
    from probe.shared.notes import owed

    deps.store.set_fact(SUMMARY_TALLY, {"visuals_state": deps.visuals_state,
                                        "ledger_from": owed.read(deps.session_id)["seq"]})


def _flag_key(parsed: Any) -> str | None:
    """`kind:ref` from a summary or visuals command's own `--experiment` /
    `--project` flags."""
    from probe.shared.notes import summary as summary_cli

    experiment = next(iter(precheck._strings(parsed.params.get("experiment"))), None)
    if experiment:
        return f"{summary_cli.EXPERIMENT}:{experiment}"
    project = next(iter(precheck._strings(parsed.params.get("project"))), None)
    return f"{summary_cli.PROJECT}:{project}" if project else None


def _json(stdout: str) -> dict | None:
    try:
        payload = json.loads(stdout or "")
    except ValueError:
        return None
    return payload if isinstance(payload, dict) else None


def _lane_said(parsed: Any, stdout: str, stderr: str) -> bool:
    """Did this summary or visuals command say the team's summaries are the
    lane's? A checkout's JSON `mode`; a refused push's JSON `detail`, or a
    refused `visuals set`'s error line, ending in `summary_cli.LANE_MARK`.
    Never free text: a page, a chart title in a 409's list, any other
    command's output could hold the same words."""
    from probe.shared.notes import summary as summary_cli

    payload = _json(stdout)
    if parsed.path == "summary checkout":
        return bool(payload) and payload.get("mode") == summary_cli.MODE_LANE
    if parsed.path == "summary push":
        detail = payload.get("detail") if payload else None
        return isinstance(detail, str) and detail.endswith(summary_cli.LANE_MARK)
    if parsed.path == "visuals set":
        return any(line.startswith("error: ") and line.rstrip().endswith(summary_cli.LANE_MARK)
                   for line in (stderr or "").splitlines())
    return False


def note_summary_marks(deps: Deps, parsed: Any, argv: list[str], stdout: str = "", stderr: str = "") -> None:
    """Keep the run's lane mode and visuals tally (saved to the store; plain
    code, never raises into the write it follows). What a summary or a note
    owes is the CLI's own ledger (`probe.shared.notes.owed`), which the command itself
    kept: a push settles a summary there only when it landed."""
    try:
        _tally(deps)
        from probe.shared.notes import summary as summary_cli

        if _lane_said(parsed, stdout, stderr):
            deps.summaries_off = True
            _note_mode(deps, summary_cli.MODE_LANE)
        elif parsed.path == "summary push":
            payload = _json(stdout)
            if payload and payload.get("pushed"):
                _note_mode(deps, "recorder")
        elif parsed.path == "summary checkout":
            key = _flag_key(parsed)
            payload = _json(stdout)
            visuals = payload.get("visuals") if payload else None
            if key and isinstance(visuals, dict):
                deps.visuals_state[key] = visuals
            if payload and payload.get("mode") == "recorder":
                _note_mode(deps, "recorder")
        elif parsed.path == "visuals set":
            key = _flag_key(parsed)
            if key and _json(stdout) and _json(stdout).get("set"):
                deps.visuals_landed.add(key)
        else:
            conclusion = precheck._strings(parsed.params.get("conclusion"))
            if not (parsed.path == "experiment set" and any(c.strip() for c in conclusion)):
                return
            found = summary_cli.landing(list(argv))
            if found is None:
                return
            deps.concluded.add(f"{found[0]}:{found[1]}")
        tally_save(deps)
    except Exception:  # noqa: BLE001 -- bookkeeping, never a failed write
        return


def _owed(deps: Deps, why: str) -> list[str]:
    """`kind ref` for each `why` the ledger says this run's own commands left
    owed (`probe.shared.notes.owed`), sorted."""
    from probe.shared.notes import owed

    _tally(deps)
    try:
        items = owed.owed(deps.session_id, by=owed.BY_DAEMON, since=deps.ledger_from, why=why)
    except Exception:  # noqa: BLE001 -- an unreadable ledger owes nothing
        return []
    return sorted(f"{i['kind']} {i['ref']}" for i in items)


def summaries_owed(deps: Deps) -> list[str]:
    """`kind ref` for each summary this run owes and did not push; [] when the
    team's summaries are the lane's."""
    from probe.shared.notes import owed

    return [] if deps.summaries_off else _owed(deps, owed.SUMMARY)


def notes_owed(deps: Deps) -> list[str]:
    """`run ref` for each run this run tagged invalid with no note since."""
    from probe.shared.notes import owed

    return _owed(deps, owed.NOTE)


def visuals_owed(deps: Deps) -> list[str]:
    """`kind ref` for each experiment this run concluded whose checkout said it
    carries Metrics-center tables and charts and has none, with no `visuals set`
    since; [] when the team's summaries are the lane's."""
    _tally(deps)
    if deps.summaries_off:
        return []
    owed = [key for key in deps.concluded
            if (deps.visuals_state.get(key) or {}).get("eligible") and not deps.visuals_state[key].get("count")
            and key not in deps.visuals_landed]
    return [key.replace(":", " ", 1) for key in sorted(owed)]
from probe.daemon.agent.tools.probe_cli.process import _mark_key_refused  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.tools import Deps  # noqa: E402 -- pieces need each other; the front door loads this one first
