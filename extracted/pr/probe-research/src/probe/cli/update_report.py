"""Tell the server how each auto-update went, so a machine left behind says why.

WHY THIS EXISTS. An auto-update records its outcome on the machine it ran on
(`autoupdate.json`, printed by `probe doctor`) and nowhere else. In production
that left a fleet where machines with auto-update ON kept the CLI current while
their transcript tap sat at 0.9.3 and their plugin at 0.112.0, and nothing could
say whether `claude` was missing from the detached updater's PATH, the tap was
installed under a retired id, the marketplace refresh failed, or a run held the
lock. This module turns each attempt, and each recorded skip, into one small
report (`POST /v1/client/update-reports`, wire v1) that names, per component
(cli, plugin, tap), where it ended and why.

IT OBSERVES AND NEVER STEERS. Nothing here changes what the updater installs or
whether it runs; a legacy tap id is reported, not migrated.

IT NEVER COSTS THE CALLER ANYTHING THAT MATTERS.

  * attempts: `perform_update` queues the report (one small file) and sends it
    at once, after the update is done, within `SEND_TIMEOUT_S` of wall-clock
    time in all: the send runs on a daemon thread that is abandoned at the
    deadline, so a hung DNS lookup or TLS handshake costs no more than any
    other dead link. A failure is silent and the report stays queued.
  * skips: NOT sent where they are recorded. `autoupdate.record_skip` runs on
    the every-command path, inside training loops, so it only writes the local
    `last_skip` it always wrote; `flush` sends that record from the next
    detached manifest refresh (`version_refresh`) or update. Zero added cost on
    the hot path, and every skip call site is covered without touching it.

ONE REPORT PER UPDATE RUN. `probe wizard --action update` updates every coding
agent on the machine in turn (Claude Code, Codex, Kimi Code, pi), one
`perform_update` pass each, and the server keeps ONE row per machine. Sent pass
by pass, the last agent's report overwrote the rest: a machine whose Claude Code
tap was current read "tap: not installed" because Kimi Code ran last with no
Probe plugins. So the wizard runs its passes inside `merged_run`, which holds
them and sends one report when the run ends: per component, the pass with the
most informative result (`RESULT_PRIORITY`), with the agent it came from -- a
failed pass's own failure first, so a failed run always names what failed.

Offline, signed out, an old server (404) or a refused body: dropped or kept for
later, silently. A report is telemetry; nothing waits on it.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import threading
import time
from collections.abc import Iterator
from contextlib import contextmanager

import httpx

from probe import version_policy
from probe._compat import StrEnum
from probe._shared import scrub
from probe.cli import autoupdate, updater, versions
from probe.cli.capabilities import tracking_plugin_name
from probe.client_headers import client_version_headers, device_headers
from probe.sdk.config import resolve
from probe.sdk.device_identity import device_instance_id
from probe.sdk.surface import SURFACE_HEADER, Surface
from probe.sdk.tls import ssl_context

ROUTE = "/v1/client/update-reports"
SCHEMA_VERSION = 1
#: The queued attempt, beside `autoupdate.json`.
PENDING_FILENAME = "update-report.json"
#: The whole send, in wall-clock seconds, both reports included: every network
#: step (DNS, connect, TLS, request, answer) runs on a thread `flush` stops
#: waiting for at this deadline. The update it describes is already done; this
#: only bounds how long a person at the wizard waits on a dead link.
SEND_TIMEOUT_S = 3.0
#: httpx's own per-step bounds inside that, so an abandoned thread does not
#: linger long either.
CONNECT_TIMEOUT_S = 2.0
#: A report older than this is history, not news: dropped instead of sent.
MAX_PENDING_AGE_S = 7 * 24 * 3600
#: The server's own bound on every free-text field.
DETAIL_MAX_CHARS = 200
#: Set by whoever spawns a detached update (`main._spawn_update`), so the run
#: says what asked for it.
TRIGGER_ENV = autoupdate.TRIGGER_ENV


#: What asked for an update: one definition, in the stdlib-only module the
#: every-command path can import.
Trigger = autoupdate.Trigger


class Outcome(StrEnum):
    OK = "ok"
    FAILED = "failed"
    SKIPPED = "skipped"


class Result(StrEnum):
    """Where one component ended. The server's `ComponentResult`, verbatim."""

    UPDATED = "updated"
    CURRENT = "current"
    BEHIND = "behind"
    NOT_INSTALLED = "not_installed"
    LEGACY_INSTALLED = "legacy_installed"
    NOT_FOUND_ON_PATH = "not_found_on_path"
    REFRESH_FAILED = "refresh_failed"
    ERROR = "error"


class PiStep(StrEnum):
    """Which way pi's package step (`upgrading._update_pi_package`) ended."""

    NOT_INSTALLED = "not_installed"
    #: Another update holds the package's lock.
    LOCKED = "locked"
    #: pi itself is gone: nothing to update with.
    UNREACHABLE = "unreachable"
    FAILED = "failed"
    UPDATED = "updated"
    CURRENT = "current"


#: Where each pi step lands on the wire. A locked step is BEHIND: the package
#: was not moved, and the detail says why.
_PI_RESULTS = {
    PiStep.NOT_INSTALLED: Result.NOT_INSTALLED,
    PiStep.UNREACHABLE: Result.NOT_FOUND_ON_PATH,
    PiStep.UPDATED: Result.UPDATED,
    PiStep.CURRENT: Result.CURRENT,
    PiStep.FAILED: Result.ERROR,
    PiStep.LOCKED: Result.BEHIND,
}

#: The local skip sentences, as the wire's codes. A reason added here later and
#: not mapped still reaches the server, as `other`, rather than failing the
#: report the server would refuse.
_SKIP_CODES = {
    autoupdate.SKIP_RUN_IN_FLIGHT: "run_in_flight",
    autoupdate.SKIP_NOT_A_TTY: "not_a_tty",
    autoupdate.SKIP_HOT_PATH_COMMAND: "hot_path_command",
    autoupdate.SKIP_LIVENESS_UNPROVABLE: "liveness_unprovable",
}
_OK_RESULTS = (Result.UPDATED, Result.CURRENT)
#: The results that say a component did not end where the update meant it to.
#: A FAILED attempt always carries one of these, with its detail, on the
#: component that failed it -- the report's whole point is to name it. Not every
#: one of them fails an attempt: an agent not on PATH (`not_found_on_path`), a
#: CLI the updater refuses to touch or a pi package another update holds
#: (`behind`) are each a skip, not a failure.
FAILING_RESULTS = frozenset(
    (Result.ERROR, Result.REFRESH_FAILED, Result.NOT_FOUND_ON_PATH, Result.BEHIND)
)

#: Which result a merged run reports for a component when its agents disagree
#: (after a failed pass's own failure, `merge_passes`), most informative first: a failure beats a cause beats "behind" beats a
#: success, and "not installed" -- which says only that THIS agent lacks it --
#: loses to everything. So a Kimi Code pass with no Probe plugins can no longer
#: hide a Claude Code tap that is current, and a Codex tap left behind is not
#: hidden by a Claude Code tap that moved. Every `Result` appears exactly once
#: (pinned by a test).
RESULT_PRIORITY: tuple[Result, ...] = (
    Result.ERROR,
    Result.REFRESH_FAILED,
    Result.NOT_FOUND_ON_PATH,
    Result.LEGACY_INSTALLED,
    Result.BEHIND,
    Result.UPDATED,
    Result.CURRENT,
    Result.NOT_INSTALLED,
)
#: The server's version shape. Anything else is sent as unknown (None): one odd
#: value must not get the whole report refused.
_VERSION = re.compile(r"^[0-9][0-9A-Za-z.+-]{0,63}$")
_HARNESS = re.compile(r"^[a-z][a-z0-9_]{0,31}$")


def trigger_from_env(default: Trigger) -> Trigger:
    """The trigger a spawner named in `TRIGGER_ENV`, else `default`."""
    try:
        return Trigger(os.environ.get(TRIGGER_ENV, ""))
    except ValueError:
        return default


# ---------------------------------------------------------------------------
# Building a report
# ---------------------------------------------------------------------------


def _version(value: str | None) -> str | None:
    if not isinstance(value, str):
        return None
    value = value.strip()
    return value if _VERSION.match(value) else None


def _detail(text: str | None) -> str:
    """One scrubbed line, clipped. This machine's own home and login name go
    first, then every home-shaped path and credential (`probe._shared.scrub`,
    shared with the diagnostic reports). The server strips home directories
    again: it does not trust this."""
    if not text:
        return ""
    try:
        flat = " ".join(scrub.scrub(text).split())
    except Exception:  # noqa: BLE001 - withhold, never fail the report
        return "detail withheld: it could not be scrubbed"
    if len(flat) > DETAIL_MAX_CHARS:
        flat = flat[: DETAIL_MAX_CHARS - 1].rstrip() + "…"
    return flat


def _component(
    before: str | None,
    after: str | None,
    target: str | None,
    result: Result,
    detail: str = "",
    *,
    note: str = "",
) -> dict:
    """`note` is the one thing a component that ended where it should may
    still say (sessions still running an older tap): kept whatever the result."""
    return {
        "before": _version(before),
        "after": _version(after),
        "target": _version(target),
        "result": result.value,
        # Nothing to explain on a component that ended where it should.
        "detail": _detail(note) if note else "" if result in _OK_RESULTS else _detail(detail),
    }


def cli_component(
    res: updater.CliResult | None,
    *,
    current: str,
    target: str | None,
    refused: str = "",
) -> dict:
    """The CLI's half. `res` is None when nothing ran: an install the updater
    refuses to touch (`refused` says why: editable, managed, unknown), or a
    temporary npx/uvx run whose installed copy was already current."""
    if res is None:
        if refused:
            behind = updater.is_newer(target, current)
            return _component(
                current, current, target, Result.BEHIND if behind else Result.CURRENT, refused
            )
        installed = versions.cli_version()
        return _component(current, installed, target, Result.CURRENT)
    if res.ok:
        return _component(
            res.before, res.after, target, Result.UPDATED if res.changed else Result.CURRENT
        )
    if res.missing_binary:
        result = Result.NOT_FOUND_ON_PATH  # `uv` / `pipx` missing from this PATH
    elif res.after and target and updater.is_newer(target, res.after):
        result = Result.BEHIND
    else:
        result = Result.ERROR
    return _component(res.before, res.after, target, result, res.message)


def plugin_component(
    pres: updater.PluginResult | None, *, target: str | None, source: str
) -> dict | None:
    """The tracking plugin's half (Claude Code, Codex or Kimi Code)."""
    if pres is None:
        return None
    name = tracking_plugin_name(source)
    before = updater.listed_version(pres.before, name)
    after = updater.listed_version(pres.after, name)
    if not pres.attempted:
        result = Result.NOT_FOUND_ON_PATH if pres.missing_binary else Result.NOT_INSTALLED
    elif pres.confirmed:
        result = Result.UPDATED if pres.changed else Result.CURRENT
    elif updater.nothing_installed(pres, source):
        # None of Probe's plugins in the agent's own list, before or after: the
        # update had nothing to move (its command failing then is the
        # consequence). The outcome reads the same rule, so this is no failure.
        result = Result.NOT_INSTALLED
    elif pres.refresh_failed:
        result = Result.REFRESH_FAILED
    elif pres.command_failed:
        result = Result.ERROR
    elif after and target and updater.is_newer(target, after):
        result = Result.BEHIND  # the command succeeded and nothing moved
    else:
        result = Result.ERROR
    return _component(before, after, target, result, pres.message)


def tap_component(pres: updater.PluginResult | None, *, target: str | None) -> dict | None:
    """The transcript tap's half -- where `tap_verdict` says only "skipped" for a
    tap it cannot see, this says WHICH of the reasons it was."""
    if pres is None:
        return None
    before, after = pres.tap_before, pres.tap_after
    legacy = updater.legacy_tap_ids(pres.legacy_ids)
    detail = pres.tap_detail
    if not pres.attempted:
        result = Result.NOT_FOUND_ON_PATH if pres.missing_binary else Result.NOT_INSTALLED
        detail = pres.message
    elif not after:
        if before:
            # It was there before the update and is not now: a failed update
            # (`tap_verdict`). Its own failure if a command said one, else what
            # happened -- the no-op sentences ("did not advance") are not it.
            result = Result.ERROR
            if not detail or detail in (updater.TAP_NOOP, updater.CODEX_TAP_NOOP):
                seen = "could not be confirmed" if pres.list_unreadable else "is not there"
                detail = f"tap {before} was installed before the update and {seen} after it"
        elif legacy:
            result = Result.LEGACY_INSTALLED
            detail = f"installed only as {', '.join(legacy)}, which this update does not move"
        else:
            result = Result.NOT_INSTALLED
    elif not target or not updater.is_newer(target, after):
        result = Result.UPDATED if updater.is_newer(after, before) else Result.CURRENT
        # The installed tap is current, and sessions started before it may
        # still run an older one -- the tap this machine reports (the server
        # keeps a machine's OLDEST live tap). The result stays what the update
        # did; the reason the machine still reads the old tap rides in detail.
        return _component(
            before, after, target, result, note=updater.running_stale_note(pres)
        )
    elif pres.refresh_failed:
        result = Result.REFRESH_FAILED
    elif detail and detail not in (updater.TAP_NOOP, updater.CODEX_TAP_NOOP):
        result = Result.ERROR  # its own update command failed
    else:
        result = Result.BEHIND
        # It moved, but not far enough: no command failed and no no-op is
        # named, so say what the local line says rather than nothing.
        detail = detail or f"still {after} after the update, behind the latest {target}"
    return _component(before, after, target, result, detail)


def pi_component(step, *, target: str | None, harness: str | None = None) -> dict | None:
    """pi's package, which is the plugin half on pi (`upgrading._PiUpdate`).
    `harness` names pi on a pass run for another agent (`plugin_half`); the
    report's own harness is used otherwise."""
    if step is None:
        return None
    result = _PI_RESULTS.get(step.code, Result.BEHIND)
    detail = step.detail or (step.lines[-1].strip() if step.lines else "")
    component = _component(step.before, step.after, target, result, detail)
    if _harness(harness):
        component["harness"] = harness
    return component


def plugin_half(plugin: dict | None, package: dict | None) -> dict | None:
    """The plugin slot of a pass for a marketplace agent (Claude Code, Codex,
    Kimi Code), which also moves pi's package (`upgrading._update_pi_package`).

    `package` is pi's package component when its step FAILED (the caller passes
    None otherwise), and that failure fails the pass. Its plugin slot used to carry
    the marketplace plugin alone, which had moved: a report that read updated
    across the board and failed. The more informative of the two by
    `RESULT_PRIORITY`, the plugin's own on a tie -- so a failed pi package is
    named unless the plugin failed too."""
    candidates = [c for c in (plugin, package) if c is not None]
    return min(candidates, key=_rank) if candidates else None


def _harness(source: str | None) -> str | None:
    return source if isinstance(source, str) and _HARNESS.match(source) else None


def attempt_report(
    *,
    trigger: Trigger,
    ok: bool,
    at: int,
    source: str | None,
    cli: dict | None,
    plugin: dict | None,
    tap: dict | None,
    legacy_ids: tuple[str, ...] = (),
) -> dict:
    """One attempt, as wire v1. The harness flags are read HERE, in the
    updater's own process, because the question is whether THIS process --
    often a detached one, with whatever PATH its spawner had -- can find them.

    `at` is when the attempt ran (unix seconds): a report kept for a later send
    must not read as an attempt made when it finally landed. Each component
    names the agent (`harness`) whose pass produced it, which is what tells a
    merged run's components apart (`merge_passes`)."""
    harness = _harness(source)
    return {
        "schema_version": SCHEMA_VERSION,
        "trigger": trigger.value,
        "outcome": (Outcome.OK if ok else Outcome.FAILED).value,
        "attempted_at": int(at),
        "harness": harness,
        "cli": _from_harness(cli, harness),
        "plugin": _from_harness(plugin, harness),
        "tap": _from_harness(tap, harness),
        "claude_found": shutil.which("claude") is not None,
        "codex_found": shutil.which("codex") is not None,  # harness-literal-ok: the wire field's own name
        "legacy_plugin_ids": list(dict.fromkeys(legacy_ids))[:8],
    }


def _from_harness(component: dict | None, harness: str | None) -> dict | None:
    """`component` tagged with the pass's agent, unless it names its own (pi's
    package on another agent's pass, `plugin_half`)."""
    return None if component is None else {"harness": harness, **component}


def _rank(component: dict) -> int:
    try:
        return RESULT_PRIORITY.index(Result(component.get("result")))
    except ValueError:
        return len(RESULT_PRIORITY)


def _named_failure(report: dict, component: dict) -> bool:
    """`component` is what failed `report`'s pass: a failing result on a
    failed pass."""
    try:
        failing = Result(component.get("result")) in FAILING_RESULTS
    except ValueError:
        failing = False
    return failing and report.get("outcome") == Outcome.FAILED


def merge_passes(reports: list[dict]) -> dict:
    """One report for a run made of several agents' passes.

    Per component, the pass with the most informative result
    (`RESULT_PRIORITY`; on a tie, the earlier pass) -- its versions, detail and
    agent travel with it, never mixed with another pass's. EXCEPT that a failed
    pass's failing result comes first: the run failed because of it, and an
    agent missing from PATH (`not_found_on_path`) or a tap under a retired id
    (`legacy_installed`) on a pass that did NOT fail outranked a tap left
    `behind` by the pass that did, so the merged report failed naming nothing
    that failed. The run failed if any pass failed; it is dated by its first
    pass; the plugin ids found under a retired id are the union. The top-level
    `harness` is the first pass's (the one that ran the CLI upgrade); each
    component carries its own."""
    if len(reports) == 1:
        return reports[0]
    merged = dict(reports[0])
    merged["outcome"] = (
        Outcome.FAILED if any(r.get("outcome") == Outcome.FAILED for r in reports) else Outcome.OK
    ).value
    times = [r["attempted_at"] for r in reports if isinstance(r.get("attempted_at"), int)]
    if times:
        merged["attempted_at"] = min(times)
    for name in ("cli", "plugin", "tap"):
        candidates = [(r, r[name]) for r in reports if r.get(name)]
        merged[name] = (
            min(candidates, key=lambda c: (not _named_failure(*c), _rank(c[1])))[1]
            if candidates
            else None
        )
    for flag in ("claude_found", "codex_found"):
        merged[flag] = any(r.get(flag) for r in reports)
    merged["legacy_plugin_ids"] = list(
        dict.fromkeys(i for r in reports for i in r.get("legacy_plugin_ids") or ())
    )[:8]
    return merged


#: The passes of the run `merged_run` is holding, or None outside one.
_run_passes: list[tuple[dict, str | None]] | None = None


@contextmanager
def merged_run() -> Iterator[None]:
    """Hold every attempt reported inside, and send ONE merged report on exit.

    For an update that runs one `perform_update` pass per coding agent (the
    wizard's Update). Nested runs belong to the outermost one. Never raises on
    its own account: a merge or send failure costs the report, not the run."""
    global _run_passes
    if _run_passes is not None:
        yield
        return
    _run_passes = []
    started = time.time()
    try:
        # The local record (`probe doctor`) merges the same passes.
        with autoupdate.merged_attempts():
            try:
                yield
            except SystemExit as exc:
                _stopped_pass(exc, started)
                raise
    finally:
        passes, _run_passes = _run_passes, None
        if passes:
            try:
                _send(merge_passes([report for report, _base in passes]), passes[-1][1])
            except Exception:  # noqa: BLE001 - telemetry must never break its caller
                pass


#: `probe.core.events._stop`'s exit statuses (128 + the signal): SIGTERM or
#: SIGHUP ended the run wherever it was.
_STOP_SIGNALS = ("SIGTERM", "SIGHUP")


def _stopped_pass(exc: SystemExit, started: float) -> None:
    """A run SIGTERM or SIGHUP ended (the Probe service stops an update past
    its time limit, `probe.service.updater.UPDATE_TIMEOUT_S`) fails, and its
    report and local record say so: one more failed pass, its CLI half the
    stop. The passes it finished keep their own results; without this a run
    stopped in its first pass sent nothing, and one stopped later sent what
    the finished passes said, success included. Never raises."""
    try:
        import signal

        name = next(
            (n for n in _STOP_SIGNALS if hasattr(signal, n) and exc.code == 128 + int(getattr(signal, n))), None
        )
        if name is None or _run_passes is None:
            return
        from probe import __version__

        ran = time.time() - started
        took = f"{ran / 60:.0f} min" if ran >= 120 else f"{ran:.0f} s"
        detail = f"stopped by {name} after {took}, before the update finished"
        now = int(time.time())
        autoupdate.record_attempt(
            autoupdate.Attempt(at=now, ok=False, detail=detail, from_version=__version__)
        )
        report = attempt_report(
            trigger=trigger_from_env(Trigger.MANUAL),
            ok=False,
            at=now,
            source=None,
            cli=_component(__version__, versions.cli_version(), None, Result.ERROR, detail),
            plugin=None,
            tap=None,
        )
        _run_passes.append((report, _run_passes[-1][1] if _run_passes else None))
    except Exception:  # noqa: BLE001 - telemetry must never break its caller
        pass


def skip_report(skip: autoupdate.Skip) -> dict:
    """A recorded skip, as wire v1. Carries no components: the server keeps the
    last attempt's, which is the explanation a skip does not have."""
    try:
        trigger = Trigger(skip.trigger)
    except ValueError:
        trigger = Trigger.CLI
    return {
        "schema_version": SCHEMA_VERSION,
        "trigger": trigger.value,
        "outcome": Outcome.SKIPPED.value,
        "skip_reason": _SKIP_CODES.get(skip.reason, "other"),
        "skip_count": max(1, int(skip.count)),
    }


# ---------------------------------------------------------------------------
# Queueing and sending
# ---------------------------------------------------------------------------


def pending_path():
    return version_policy.state_dir() / PENDING_FILENAME


def _read_pending() -> dict:
    try:
        loaded = json.loads(pending_path().read_text())
    except (OSError, ValueError):
        return {}
    return loaded if isinstance(loaded, dict) else {}


def queue_attempt(report: dict, *, now: int | None = None) -> None:
    """Keep `report` until it is delivered. Only the newest attempt is kept: the
    server stores one per machine, so an older one could only be overwritten."""
    try:
        with autoupdate._state_write_lock():
            pending = _read_pending()
            pending["attempt"] = {"at": int(time.time()) if now is None else now, "body": report}
            version_policy.atomic_write_json(pending_path(), pending)
    except Exception:  # noqa: BLE001 - a report must never fail an update
        pass


def _skip_marker(skip: autoupdate.Skip) -> list:
    return [skip.at, skip.reason, skip.count, skip.trigger]


def _due(now: float) -> list[tuple[str, int, dict, object]]:
    """What is waiting to be sent, oldest first: the queued attempt, and the
    local `last_skip` when it changed since it was last sent."""
    pending = _read_pending()
    jobs: list[tuple[str, int, dict, object]] = []
    attempt = pending.get("attempt")
    if isinstance(attempt, dict) and isinstance(attempt.get("body"), dict):
        at = attempt.get("at")
        if isinstance(at, int) and now - at <= MAX_PENDING_AGE_S:
            jobs.append(("attempt", at, attempt["body"], attempt))
    skip = autoupdate.load().last_skip
    if (
        skip is not None
        and now - skip.at <= MAX_PENDING_AGE_S
        and pending.get("skip_sent") != _skip_marker(skip)
    ):
        jobs.append(("skip", skip.at, skip_report(skip), _skip_marker(skip)))
    jobs.sort(key=lambda job: job[1])
    return jobs


def _settle(kind: str, sent: object) -> None:
    """Never send `sent` again: drop the attempt (unless a newer one replaced
    it meanwhile), or remember the skip as sent."""
    with autoupdate._state_write_lock():
        pending = _read_pending()
        if kind == "attempt":
            if pending.get("attempt") != sent:
                return
            pending.pop("attempt", None)
        else:
            pending["skip_sent"] = sent
        version_policy.atomic_write_json(pending_path(), pending)


def _headers(token: str) -> dict[str, str]:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        SURFACE_HEADER: Surface.CLI.value,
        # The version INSTALLED now, not the one this process imported: after an
        # upgrade they differ, and the old one would be recorded as current.
        **client_version_headers(Surface.CLI.value, versions.cli_version()),
    }
    try:
        headers.update(device_headers(device_instance_id()))
    except Exception:  # noqa: BLE001 - no machine identity: the token's own machine
        pass
    return headers


def _deliver_within(
    base_url: str, headers: dict[str, str], body: dict, budget: float
) -> int | None:
    """`_deliver`, given at most `budget` seconds of WALL-CLOCK time.

    httpx's timeouts bound each step separately (DNS is not bounded at all,
    connect is per resolved address, then TLS, then the read), so their sum is
    not a deadline. The send runs on a daemon thread instead, and at the
    deadline it is abandoned: the answer is None, so the report stays queued for
    the next flush (a late success then lands as a harmless repeat)."""
    answer: list[int | None] = []

    def _send() -> None:
        try:
            answer.append(_deliver(base_url, headers, body, budget))
        except Exception:  # noqa: BLE001 - on this thread nothing else would catch it
            answer.append(None)

    sender = threading.Thread(target=_send, name="probe-update-report", daemon=True)
    sender.start()
    sender.join(budget)
    return answer[0] if answer and not sender.is_alive() else None


def _deliver(base_url: str, headers: dict[str, str], body: dict, timeout: float) -> int | None:
    """POST one report. The HTTP status, or None when it never got an answer.

    THE ONE PLACE THIS MODULE TOUCHES THE NETWORK, which is why the test suite
    replaces exactly this (agent/tests/conftest.py)."""
    try:
        with httpx.Client(
            base_url=base_url,
            timeout=httpx.Timeout(timeout, connect=min(timeout, CONNECT_TIMEOUT_S)),
            verify=ssl_context(),
        ) as client:
            return client.post(ROUTE, json=body, headers=headers).status_code
    except Exception:  # noqa: BLE001 - offline, DNS, TLS, timeout: all the same here
        return None


def flush(base_url: str | None = None, *, timeout: float = SEND_TIMEOUT_S) -> None:
    """Send whatever is waiting, within `timeout` seconds of wall-clock time in
    all (`_deliver_within`). Never raises.

    A delivered report, or one the server refused for good (a 4xx: an old
    server without the route, a token without `write`), is never sent again.
    No answer, a 429 or a 5xx keeps it for the next flush. Signed out: nothing
    is sent and nothing is lost. Nothing waiting: nothing is read beyond the
    two small state files -- no machine identity is touched or minted.
    """
    try:
        deadline = time.monotonic() + timeout
        settings = resolve(base_url=base_url) if base_url else resolve()
        if not settings.token:
            return
        jobs = _due(time.time())
        if not jobs:
            return
        headers = _headers(settings.token)
        for kind, _at, body, sent in jobs:
            left = deadline - time.monotonic()
            if left <= 0.2:
                return
            status = _deliver_within(settings.base_url, headers, body, left)
            if status is None or status == 429 or status >= 500:
                return  # unreachable or struggling: keep everything for later
            _settle(kind, sent)
    except Exception:  # noqa: BLE001 - telemetry must never break its caller
        return


def submit_attempt(report: dict, *, base_url: str | None = None) -> None:
    """Queue `report` and send it now (with any skip still waiting) -- or, inside
    `merged_run`, hold it for the run's one merged report."""
    if _run_passes is not None:
        _run_passes.append((report, base_url))
        return
    _send(report, base_url)


def _send(report: dict, base_url: str | None) -> None:
    queue_attempt(report)
    flush(base_url)
