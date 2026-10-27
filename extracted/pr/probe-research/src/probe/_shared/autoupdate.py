"""Background auto-update: settings, the safe triggers, and the audit record.

THE TRIGGER BOUNDARY IS THE WHOLE POINT.

`probe update` replaces the installed tree in place (see updater.py's H8 note on
why its whole call graph is imported eagerly). That is fine when a human types
the command. It is NOT fine from an arbitrary CLI invocation, because `probe log`
runs inside training loops -- upgrading the package under hour nine of a run is a
confusing failure landing in the middle of somebody's experiment.

So auto-update fires from exactly TWO places, and each carries the gates its own
hazard needs:

  * the plugin's SessionStart hook. A human is at the keyboard by definition, so
    `enabled` is the only gate before the spawn.
  * the CLI's root callback (`main.py:_version_notice`), which exists because a
    box that never starts a Claude Code session would otherwise never update at
    all. Reaching an arbitrary invocation is the whole point of that trigger and
    also its whole danger, so it gates on a denylist of the run-scoped commands
    a training loop makes and on the run lock (for a day at most:
    `defer_for_run`) -- and records every refusal, because a box correctly
    deferring all week must not look like a dead updater. Off a terminal it
    starts the detached update at most once per window (`main._claim_window`):
    it used to refuse there altogether, and a machine whose only `probe` calls
    come from hooks never updated (plan C3). Where the Probe service is the
    updater (POSIX), neither trigger applies anything itself: both ask the
    service, which records its own deferrals here, and the CLI's gates and
    their records stay with the fallback updater (`main._version_notice`).

Both are spawned DETACHED, and `perform_update` re-checks the run lock for both
(see upgrading.py -- that check is unconditional precisely because the hook does
not pre-check anything). The hook is synchronous by contract (its systemMessage
cannot come from a background process) and the upgrade timeout is 300s, so
applying inline would let a Claude Code session hang for up to five minutes
before you could type. Nothing is lost by deferring: a plugin update only takes
effect on restart anyway.

Because a detached process cannot report failure through the hook, every attempt
is RECORDED. Without that, an auto-updater that silently fails forever looks
exactly like one that works. `probe doctor` prints it.

stdlib only, and it stays that way: `probe.version_policy` -- which owns the paths
and constants this module and the plugin hook share -- is stdlib-only for the
hook's benefit, and a dependency here would defeat that.

(This docstring used to claim the hook imported THIS module. It never did: the
hook re-implemented the state read instead, which is the duplication
`version_policy` now removes.)
"""

from __future__ import annotations

import os
import time
from contextlib import contextmanager
from dataclasses import dataclass

from probe import version_policy
from probe._compat import StrEnum

STATE_DIRNAME = version_policy.STATE_DIRNAME
STATE_FILENAME = version_policy.STATE_FILENAME
LOCK_FILENAME = version_policy.LOCK_FILENAME

#: A lock older than this is treated as abandoned. Comfortably longer than the
#: 300s upgrade timeout so a slow-but-live upgrade is never stolen from.
#:
#: Age is the right reaper for THIS lock -- an upgrade that outlives 900s is
#: genuinely stuck. It is the wrong reaper for the run lock in run_lock.py, where
#: a twenty-hour holder is the normal case; that one proves liveness instead.
STALE_LOCK_SECONDS = 900


# There was a `stable` channel here, meant as a legible promise that a new CLI
# would not land on a researcher mid-experiment. It was stored, passed on the
# command line and validated -- and never read by anything. `cli_latest()` always
# returned `manifest["cli"]["latest"]`, and the manifest has no `stable` key, so
# choosing it behaved exactly like `latest`. A setting that does nothing is worse
# than an absent one: it answers a real worry with a promise nothing keeps.
#
# If the worry needs answering, it needs a `stable` field in the manifest and a
# `cli_latest(manifest, channel)` that reads it -- not an enum.


@dataclass(frozen=True)
class Attempt:
    """The outcome of one auto-update run, for `probe doctor` to print.

    BOTH halves, because an auto-update is two upgrades. The plugin's outcome
    used to live only in the printed lines, which a detached run sends to
    /dev/null -- so a plugin that had silently stopped updating looked exactly
    like one that worked. That is the failure mode this record exists to
    prevent, one layer down.
    """

    at: int
    ok: bool
    detail: str = ""
    from_version: str | None = None
    to_version: str | None = None
    #: True when the plugin half has nothing to report -- it succeeded, or there
    #: was no Claude Code to update. A missing `claude` is a legitimate state for
    #: a CLI-only user, not an auto-update failure.
    plugin_ok: bool = True
    plugin_detail: str = ""
    plugin_version: str | None = None

    @property
    def succeeded(self) -> bool:
        return self.ok and self.plugin_ok

    def summary(self) -> str:
        """Timestamp and overall status for the wizard's device summary."""
        when = time.strftime("%Y-%m-%d %H:%M", time.localtime(self.at))
        return f"{when} · {'success' if self.succeeded else 'fail'}"

    def describe(self) -> str:
        when = time.strftime("%Y-%m-%d %H:%M", time.localtime(self.at))
        landed = ", ".join(
            part
            for part in (
                f"CLI {self.to_version}" if self.to_version else "",
                f"plugin {self.plugin_version}" if self.plugin_version else "",
            )
            if part
        )
        notes = "; ".join(
            note
            for note in (
                "" if self.ok else (self.detail or "unknown error"),
                f"plugin: {self.plugin_detail}" if self.plugin_detail else "",
            )
            if note
        )
        if self.succeeded:
            out = f"success -> {landed} ({when})" if landed else f"success ({when})"
            return f"{out}: {notes}" if notes else out
        # On a failure the versions are where things are STUCK, not where they
        # landed -- "FAILED -> plugin 0.1.0" reads like 0.1.0 was the goal.
        out = f"FAILED ({when})"
        if notes:
            out += f": {notes}"
        return f"{out} — still at {landed}" if landed else out


class Trigger(StrEnum):
    """What asked for an update (or for the skip of one). Here, in the
    stdlib-only module, because the every-command path names it without
    importing an HTTP client; `update_report` reports it."""

    #: A coding agent's session start: the plugin's SessionStart hook, pi's start.
    SESSION_START = "session_start"
    #: The CLI on its own: the every-command check, or a run's end.
    CLI = "cli"
    #: A person chose Update in `probe wizard` (or `probe update`) at a terminal.
    MANUAL = "manual"
    #: The lifeboat, outside every release, rescued this machine (plan
    #: fool-proof-updates B5): the hand-off it ran names it (`PROBE_HANDOFF_TRIGGER`).
    LIFEBOAT = "lifeboat"


#: Why an eligible upgrade was not applied. These are NOT failures -- each one is
#: the system working correctly -- but they are indistinguishable from a dead
#: auto-updater unless they are recorded, which is the whole point of `Skip`.
SKIP_RUN_IN_FLIGHT = "run in flight"
SKIP_NOT_A_TTY = "not an interactive terminal"
SKIP_HOT_PATH_COMMAND = "hot-path command"
SKIP_LIVENESS_UNPROVABLE = "run liveness unprovable on this platform"
#: Another `probe wizard` (a terminal, or the desktop app) holds the device
#: (`wizard_lock`). Reaches the server as `other` until it learns this code.
SKIP_SETUP_RUNNING = "another Probe setup is running"
#: A Probe daemon worker is recording a session on this machine: the Probe
#: service updates only while none is (plan X1; phase 2 pauses them instead).
#: Reaches the server as `other` until it learns this code.
SKIP_DAEMON_RECORDING = "a Probe daemon is recording"


@dataclass(frozen=True)
class Skip:
    """The last time an available upgrade was deliberately NOT applied.

    A SIBLING of `last_attempt`, never a replacement for it. "We skipped 214
    times because this box has been training all week" and "the last real upgrade
    succeeded on Tuesday" are different facts, and `probe doctor` needs both: with
    only the second, a machine that is correctly idle for six days is
    byte-identical to one whose auto-updater died.

    `count` accumulates while the reason is unchanged, so a fortnight-long sweep
    reads as one durable state rather than as the most recent of many.
    """

    at: int
    reason: str
    count: int = 1
    available: str | None = None  # the version we would have moved to
    #: What asked for the update that was skipped (a `Trigger` value). Absent on
    #: records written before it existed, which were all the every-command
    #: check's or the spawned updater's own run-lock recheck: `cli`. A plain
    #: string, not the enum: a newer CLI may have written a value this one lacks.
    trigger: str = Trigger.CLI.value

    def describe(self) -> str:
        when = time.strftime("%Y-%m-%d %H:%M", time.localtime(self.at))
        times = "once" if self.count == 1 else f"{self.count}x"
        target = f" -> {self.available}" if self.available else ""
        return f"skipped {times}{target} — {self.reason} (last: {when})"


@dataclass(frozen=True)
class Settings:
    enabled: bool = False
    last_attempt: Attempt | None = None
    last_skip: Skip | None = None
    #: `enabled` is the managed CLI's default (no choice on record), not a
    #: person's (`version_policy.autoupdate_state`): never evidence that anyone
    #: set this machine up (`Capabilities.configured`).
    by_default: bool = False


# One definition, shared with the plugin hook. See version_policy's docstring for
# why the hook cannot simply import this module.
state_dir = version_policy.state_dir
state_path = version_policy.state_path
lock_path = version_policy.lock_path
_read = version_policy.read_state


def _attempt_from(attempt_raw: object) -> Attempt | None:
    """The `last_attempt` record as an `Attempt`, or None (absent or unreadable)."""
    if not isinstance(attempt_raw, dict):
        return None
    try:
        return Attempt(
            at=int(attempt_raw["at"]),
            ok=bool(attempt_raw["ok"]),
            detail=str(attempt_raw.get("detail", "")),
            from_version=attempt_raw.get("from_version"),
            to_version=attempt_raw.get("to_version"),
            # Absent on records written before the plugin half was tracked.
            # Defaulting to True keeps an old success reading as a success.
            plugin_ok=bool(attempt_raw.get("plugin_ok", True)),
            plugin_detail=str(attempt_raw.get("plugin_detail", "")),
            plugin_version=attempt_raw.get("plugin_version"),
        )
    except (KeyError, TypeError, ValueError):
        return None


def load() -> Settings:
    """Current settings. Fail-soft: unreadable or corrupt state reads as no
    choice, which is the default (`version_policy.autoupdate_state`): ON for
    the machine's managed CLI, OFF for any other install. A `false` in any
    known state folder is off."""
    raw = _read()
    attempt = _attempt_from(raw.get("last_attempt"))
    skip_raw = raw.get("last_skip")
    skip = None
    if isinstance(skip_raw, dict):
        try:
            skip = Skip(
                at=int(skip_raw["at"]),
                reason=str(skip_raw["reason"]),
                # Absent on records written before counting existed. One is the
                # reading that preserves the old meaning: we saw exactly this.
                count=int(skip_raw.get("count", 1)),
                available=skip_raw.get("available"),
                trigger=str(skip_raw.get("trigger") or Trigger.CLI.value),
            )
        except (KeyError, TypeError, ValueError):
            skip = None
    # A `channel` key written by an older CLI is ignored, not migrated away: the
    # state file is also read by the plugin hook, which may be older than us.
    # That tolerance is the forward-compatibility rule stated in version_policy:
    # additive keys only, unknown keys ignored, missing keys defaulted to the
    # reading that preserves old behaviour.
    enabled, by_default = version_policy.autoupdate_state(raw)
    return Settings(
        enabled=enabled,
        last_attempt=attempt,
        last_skip=skip,
        by_default=by_default,
    )


def _write(payload: dict) -> None:
    # Atomic replace via a UNIQUE temp name. A half-written state file read by a
    # concurrent SessionStart parses as "off" and silently stops auto-updating --
    # and the old fixed `autoupdate.json.tmp` was SHARED by every writer here, so
    # two of them racing could produce exactly that. With skip records added
    # there are now three writers, which is what made the fix load-bearing.
    version_policy.atomic_write_json(state_path(), payload)


#: Serializes read-modify-write over the state file: `save()`,
#: `record_attempt()`, `record_skip()` (`version_policy.state_write_lock`).
_state_write_lock = version_policy.state_write_lock


def save(*, enabled: bool) -> Settings:
    """A person's choice, the only thing that writes `enabled` (the managed
    CLI's default is never written: `version_policy.autoupdate_state`). Saved
    in every known state folder: one saved under XDG_STATE_HOME alone is
    invisible to the Probe service, which reads the default folder.

    Raises OSError, naming the files, when one could not be written (every
    folder is tried first): the wizard must not say "off" while the service
    reads on."""
    failed: list[str] = []
    for folder in version_policy.known_state_dirs():
        path = folder / STATE_FILENAME
        try:
            with _state_write_lock(folder=folder):
                raw = _read(folder)
                raw["enabled"] = bool(enabled)
                if not version_policy.atomic_write_json(path, raw):
                    failed.append(str(path))
        except OSError:
            failed.append(str(path))
    # Before raising: the lifeboat must hear an off even when one folder failed.
    _tell_lifeboat(bool(enabled))
    if failed:
        raise OSError(f"could not save the automatic-updates setting in {', '.join(failed)}")
    return load()


def _tell_lifeboat(enabled: bool) -> None:
    """The lifeboat reads the setting from its own env.json (it runs outside
    every release): kept in step at every save, so updates turned off stop it
    at its next run, not at the next service start (plan fool-proof-updates).
    Never raises."""
    try:
        from probe.service import lifeboat

        lifeboat.note_auto_update(enabled)
    except Exception:  # noqa: BLE001 -- the next service start writes it anyway
        pass


def forget() -> None:
    """Drop this device's auto-update record entirely. Uninstall only.

    `save(enabled=False)` turns the setting off but KEEPS `last_attempt`, and
    `Capabilities.configured` reads that field as evidence this machine has been
    set up -- so a fully removed device could never look fresh again, and the
    next install offered "everything currently off" where it should offer the
    defaults. An absent file reads as no choice (see `load`): OFF for most
    installs, and for a managed CLI left behind its default, ON -- that CLI
    keeps itself current, and a default is never evidence of a setup. A
    person's explicit `false` is KEPT, alone (`{"enabled": false}`, no evidence
    of a setup either: `Capabilities.configured` counts only on): removing
    Probe is no reason to start updating what they froze. In every known state
    folder, as `save` writes.
    """
    # Fail-soft all the way down, like every other writer here. This runs in
    # the middle of an uninstall on a machine whose plugins are already gone: a
    # state file we cannot remove leaves the device reading as configured, which
    # is a cosmetic loss. A traceback there is not.
    for folder in version_policy.known_state_dirs():
        path = folder / STATE_FILENAME
        if not path.exists():
            continue
        try:
            with _state_write_lock(folder=folder):
                if _read(folder).get("enabled") is False:
                    version_policy.atomic_write_json(path, {"enabled": False})
                else:
                    path.unlink(missing_ok=True)
        except OSError:
            pass


#: The passes of the Update run `merged_attempts` is holding, each with the
#: agent it ran for; None outside one.
_held_attempts: list[tuple[str | None, Attempt]] | None = None


@contextmanager
def merged_attempts():
    """Hold every attempt recorded inside, and record ONE merged attempt on exit.

    For an update that runs one pass per coding agent (the wizard's Update, see
    `update_report.merged_run`, which enters this). Each pass used to overwrite
    `last_attempt`, so the LAST agent's result was all `probe doctor` showed:
    a sandboxed Update whose Claude Code pass could not update its plugin
    recorded success, because pi ran last with nothing to update (2026-10-07).
    Nested runs belong to the outermost one. Never raises on its own account.
    """
    global _held_attempts
    if _held_attempts is not None:
        yield
        return
    _held_attempts = []
    try:
        yield
    finally:
        held, _held_attempts = _held_attempts, None
        if held:
            try:
                _write_attempt(merge_attempts(held))
            except Exception:  # noqa: BLE001 - a diagnostic must never break the run
                pass


def merge_attempts(passes: list[tuple[str | None, Attempt]]) -> Attempt:
    """One record for an Update run made of several agents' passes.

    The server report's rule (`update_report.merge_passes`, `RESULT_PRIORITY`)
    on this record's booleans: a failure beats a success, and a pass with
    nothing to update -- an agent with no Probe plugins -- never hides one that
    failed. The CLI half is the first pass that failed, else the first pass
    (the one that ran the upgrade); the plugin half fails if any pass's did,
    and its detail names each agent that failed (in a success, each agent
    with a plugin that has a note). Dated by the first pass."""
    if len(passes) == 1:
        return passes[0][1]
    attempts = [attempt for _agent, attempt in passes]
    first = attempts[0]
    cli = next((attempt for attempt in attempts if not attempt.ok), first)
    failed = [(agent, attempt) for agent, attempt in passes if not attempt.plugin_ok]
    # In a success, only an agent that HAS a plugin has news (sessions still on
    # an older tap); "no Probe plugins installed in Kimi Code" is not news.
    noted = failed or [
        (agent, attempt) for agent, attempt in passes if attempt.plugin_detail and attempt.plugin_version
    ]
    detail = "; ".join(
        f"{agent}: {attempt.plugin_detail}" if agent else attempt.plugin_detail
        for agent, attempt in noted
        if attempt.plugin_detail
    )
    versions = [attempt.plugin_version for _agent, attempt in failed or passes]
    return Attempt(
        at=min(attempt.at for attempt in attempts),
        ok=cli.ok,
        detail=cli.detail,
        from_version=first.from_version,
        to_version=cli.to_version,
        plugin_ok=not failed,
        plugin_detail=detail,
        plugin_version=next((version for version in versions if version), None),
    )


def record_attempt(attempt: Attempt, *, agent: str | None = None) -> None:
    """Persist the outcome of one run. This is the ONLY way a detached upgrade
    can tell anyone what happened. Inside `merged_attempts`, held for the run's
    one merged record instead; `agent` names the coding agent the pass was for."""
    if _held_attempts is not None:
        _held_attempts.append((agent, attempt))
        return
    _write_attempt(attempt)


def _write_attempt(attempt: Attempt) -> None:
    with _state_write_lock():
        raw = _read()
        _put_attempt(raw, attempt)
        _write(raw)


def _put_attempt(raw: dict, attempt: Attempt) -> None:
    raw["last_attempt"] = {
        "at": attempt.at,
        "ok": attempt.ok,
        "detail": attempt.detail,
        "from_version": attempt.from_version,
        "to_version": attempt.to_version,
        "plugin_ok": attempt.plugin_ok,
        "plugin_detail": attempt.plugin_detail,
        "plugin_version": attempt.plugin_version,
    }
    # A real attempt CLEARS the skip record. Leaving a week-old "skipped, run
    # in flight" beside a fresh success would read as though we were blocked.
    raw.pop("last_skip", None)
    # And ends a run's hold on it: the next run's day starts with that run.
    raw.pop(RUN_DEFERRED_SINCE_KEY, None)
    raw.pop(RUN_DEFERRED_LAST_KEY, None)


def amend_attempt(change, *, wait: bool = True) -> bool:
    """`last_attempt` replaced by `change(the current one, or None)`, read and
    written under one hold of the state lock. `wait=False`: never waits for
    it, and writes nothing (False) while another writer holds it -- the Probe
    service recording an update it stopped, which a process that would not
    stop may still hold the lock for. Whether it was written."""
    with _state_write_lock(wait=wait) as free:
        if not free:
            return False
        raw = _read()
        _put_attempt(raw, change(_attempt_from(raw.get("last_attempt"))))
        _write(raw)
    return True


def record_skip(
    reason: str,
    *,
    available: str | None = None,
    now: int | None = None,
    trigger: Trigger = Trigger.CLI,
) -> None:
    """Note that an available upgrade was deliberately not applied.

    Writes to `last_skip`, NEVER to `last_attempt`: the two answer different
    questions and doctor prints both. Consecutive skips for the same reason
    increment a counter instead of appending, so a fortnight-long sweep costs one
    small field rather than an unbounded log nothing prunes.

    This record is also what the SERVER hears about a skip: `update_report.flush`
    sends `last_skip` when it changed since it last sent one. Nothing is sent
    from here -- this runs inside training loops -- so a skip costs exactly the
    one local write it always did, and reaches the server from the next
    detached manifest refresh or update instead.

    Never raises. This runs on the CLI's every-command path, and a diagnostic
    that can break `probe log` is worse than no diagnostic.
    """
    try:
        stamp = int(time.time()) if now is None else now
        with _state_write_lock():
            raw = _read()
            _put_skip(raw, reason, available=available, stamp=stamp, trigger=trigger)
            _write(raw)
    except Exception:  # noqa: BLE001 -- see docstring
        pass


def _put_skip(raw: dict, reason: str, *, available: str | None, stamp: int, trigger) -> None:
    previous = raw.get("last_skip")
    count = 1
    if isinstance(previous, dict) and previous.get("reason") == reason:
        try:
            count = int(previous.get("count", 1)) + 1
        except (TypeError, ValueError):
            count = 1
    raw["last_skip"] = {
        "at": stamp,
        "reason": reason,
        "count": count,
        "available": available,
        "trigger": str(trigger),
    }


#: Where the CLI's own updater runs (no Probe service: pip and pipx installs,
#: Windows, no runtime interpreter), a live run holds an update off this long
#: without a break, at most; then the update goes on past it, as the Probe
#: service's does after DEFER_LIMIT_S (plan D33, C3).
RUN_DEFER_LIMIT_S = 24 * 3600
#: Deferrals further apart than this are not one hold "without a break": the
#: machine was idle in between, and the run found now may be minutes old.
RUN_DEFER_GAP_S = 2 * 3600
#: `autoupdate.json`: since when live runs have held the CLI's own update off,
#: and when one last did.
RUN_DEFERRED_SINCE_KEY = "run_deferred_since"
RUN_DEFERRED_LAST_KEY = "run_deferred_last"


def _number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def defer_for_run(
    *,
    available: str | None = None,
    trigger: Trigger | str = Trigger.CLI,
    now: float | None = None,
) -> bool:
    """A live run holds an update off: defer it (True) or, once runs have held
    it off for RUN_DEFER_LIMIT_S without a break, go on past them (False).

    Deferring is a skip (`record_skip`'s record, `run in flight`) and keeps the
    time of the first deferral of the hold and of the latest, so a machine that
    trains without a break still updates within a day. The hold starts again
    -- its day counted from now -- when the latest deferral is more than
    RUN_DEFER_GAP_S old (idle in between: never update in place under a run
    that started minutes ago), when a check found no live run
    (`clear_run_deferral`), after a real attempt (`_put_attempt`), or when the
    clock went back. Never raises: a state that cannot be read or written
    defers, as before the cap."""
    try:
        moment = time.time() if now is None else now
        with _state_write_lock():
            raw = _read()
            since, last = raw.get(RUN_DEFERRED_SINCE_KEY), raw.get(RUN_DEFERRED_LAST_KEY)
            if (
                not _number(since) or not _number(last)
                or since > moment or last > moment or moment - last > RUN_DEFER_GAP_S
            ):
                since = moment
            raw[RUN_DEFERRED_SINCE_KEY] = since
            raw[RUN_DEFERRED_LAST_KEY] = moment
            if moment - since >= RUN_DEFER_LIMIT_S:
                # The hold goes on (a run is still live): an update turned away
                # now for some other reason must not start a fresh day of it.
                _write(raw)
                return False
            _put_skip(raw, SKIP_RUN_IN_FLIGHT, available=available, stamp=int(moment), trigger=trigger)
            _write(raw)
    except Exception:  # noqa: BLE001 -- see docstring
        pass
    return True


def clear_run_deferral() -> None:
    """A check found no live run: the next run's hold starts with it
    (`defer_for_run`). Writes only when there is a hold to end. Never raises."""
    try:
        held = _read()
        if RUN_DEFERRED_SINCE_KEY not in held and RUN_DEFERRED_LAST_KEY not in held:
            return
        with _state_write_lock():
            raw = _read()
            raw.pop(RUN_DEFERRED_SINCE_KEY, None)
            raw.pop(RUN_DEFERRED_LAST_KEY, None)
            _write(raw)
    except Exception:  # noqa: BLE001
        pass


#: The spawner puts its own pid here so the detached child can wait for it.
WAIT_FOR_PID_ENV = "PROBE_AUTOUPDATE_WAIT_PID"
#: What asked for a spawned update (`update_report.Trigger`): `cli` or
#: `session_start`. Here, not in update_report, because the spawn runs on the
#: every-command path and must not import an HTTP client to name an env var.
TRIGGER_ENV = "PROBE_AUTOUPDATE_TRIGGER"

#: Set while pi's package update is owed: set before `pi update` runs, so an
#: update killed partway is owed too, and kept when it fails. Without it the
#: only retry was the NEXT CLI release, since every trigger fires on "the CLI is
#: behind". pi's session start and a run's end retry it, CLI current or not,
#: once `PI_UPDATE_RETRY_S` has passed (`pi_update_due`).
PI_UPDATE_PENDING_FILENAME = "pi-update-pending"
#: What this CLI writes in the marker. An EMPTY marker is an older CLI's: it
#: touched one whenever it held the update back for a running pi, which is
#: not a failure to wait out.
PI_UPDATE_PENDING_MARK = "owed\n"
#: Between owed retries. Every pi session start and every run end asks, and a
#: `pi update` that keeps failing (offline, an npm install past its timeout)
#: would otherwise run again on each one. Each attempt rewrites the marker.
PI_UPDATE_RETRY_S = 10 * 60


def pi_update_pending() -> bool:
    try:
        return (version_policy.state_dir() / PI_UPDATE_PENDING_FILENAME).exists()
    except OSError:
        return False


def pi_update_due() -> bool:
    """An owed pi update whose last attempt is `PI_UPDATE_RETRY_S` old, or one
    an older CLI held back (an empty marker: due now). A marker dated in the
    future (a clock that moved back) is due too, rather than waiting it out."""
    path = version_policy.state_dir() / PI_UPDATE_PENDING_FILENAME
    try:
        if not path.read_text().strip():
            return True
        age = time.time() - path.stat().st_mtime
    except OSError:
        return False
    return age < 0 or age >= PI_UPDATE_RETRY_S


def mark_pi_update_pending(pending: bool) -> None:
    """Fail-soft: a marker that cannot be written costs one retry, not an update."""
    try:
        path = version_policy.state_dir() / PI_UPDATE_PENDING_FILENAME
        if pending:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(PI_UPDATE_PENDING_MARK)
        else:
            path.unlink(missing_ok=True)
    except OSError:
        pass

#: Upper bound on that wait. The parent is the CLI invocation that spawned us,
#: which is short-lived -- the one long-running command, `probe exec`, is on the
#: denylist and never spawns. The bound only matters if that ever stops being
#: true, and the run-lock recheck after the wait is the real backstop.
WAIT_FOR_PID_TIMEOUT = 1800


def pid_is_alive(pid: int) -> bool:
    """Signal 0 probes for existence without delivering anything. On Windows
    `os.kill(pid, 0)` answers nothing (a dead pid included), so a spawned update
    waited out its whole WAIT_FOR_PID_TIMEOUT there: `oscompat.probe_pid` asks
    the process table instead."""
    from probe._shared import oscompat

    try:
        oscompat.probe_pid(pid)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True  # exists, owned by someone else
    except OSError:
        return True  # unknown -> assume alive, which delays rather than clobbers
    return True


def wait_for_pid_exit(pid: int, *, timeout: float = WAIT_FOR_PID_TIMEOUT) -> bool:
    """Block until `pid` exits. True if it did, False on timeout.

    THIS IS WHY IT EXISTS. The version check runs in Typer's root callback, which
    fires BEFORE the command is dispatched, and this CLI imports lazily all over
    the place -- `from ..sdk.run import Run` inside a function, and many more. So
    a naive spawn has `uv tool upgrade` replacing files on disk while the command
    that triggered it is still reaching for them, producing a `ModuleNotFoundError`
    from a command that has worked every day for a year. Once, unreproducibly, and
    only in the minutes after a release.

    The updater already protects ITSELF from this by importing its whole call
    graph eagerly. That protects the wrong process; this protects the parent.
    """
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if not pid_is_alive(pid):
            return True
        time.sleep(0.25)
    return not pid_is_alive(pid)


#: Set (to this pid) by a holder about to exec the newest release in its
#: place (`version_refresh._hand_off`): the run after the exec holds the lock.
LOCK_HELD_ENV = "PROBE_AUTOUPDATE_LOCK_HELD"


def acquire_lock() -> bool:
    """Single writer across concurrent Claude Code sessions.

    Several sessions starting at once would otherwise each spawn `uv tool
    upgrade` against the same install. O_EXCL is the whole mechanism; a lock
    older than STALE_LOCK_SECONDS is treated as abandoned so a crashed upgrade
    cannot wedge auto-update permanently. A lock handed across an exec is
    taken over once: the update hand-off execs the newest release in the same
    process (`probe.core.adopt`), and the `--apply` run it starts finds
    LOCK_HELD_ENV naming this pid, as the lock file does.
    """
    path = lock_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        age = time.time() - path.stat().st_mtime
        if age > STALE_LOCK_SECONDS:
            path.unlink(missing_ok=True)
    except OSError:
        pass
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        if os.environ.pop(LOCK_HELD_ENV, "") != str(os.getpid()):
            return False
        try:
            return path.read_text(encoding="utf-8").strip() == str(os.getpid())
        except OSError:
            return False
    except OSError:
        return False
    os.write(fd, str(os.getpid()).encode())
    os.close(fd)
    return True


def release_lock() -> None:
    try:
        lock_path().unlink(missing_ok=True)
    except OSError:
        pass
