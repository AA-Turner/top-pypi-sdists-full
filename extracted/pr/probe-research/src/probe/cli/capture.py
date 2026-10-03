"""Turning session capture OFF, as a verified postcondition.

"Off" is not "delete the paired token file". Two independent things keep capture
alive after a naive revoke:

1. THE CREDENTIAL. The uploader resolves its token from three places -- the
   paired `.token`, `PROBE_INGEST_TOKEN`, and the probe CLI config's
   `ingest_token` (which `probe login --ingest-token` writes). Clearing only the
   first lets capture silently resume at the next session start while the menu
   reports it as off.

2. THE PROCESS. The uploader is a detached daemon spawned at session start. It
   already holds its bearer in memory and has a queue to drain, so deleting
   files does not stop it.

For a feature whose entire justification is honest consent, "we told you it was
off and it wasn't" is the worst available bug. So off is defined as a
postcondition and VERIFIED before it is reported.

THE CONFIG CREDENTIAL IS MACHINE-WIDE, NOT PER-SOURCE. Unlike the paired
`.token` and the killswitch -- both scoped by `tap_plugin_dir()`, which is
different per agent source -- the probe CLI config's `ingest_token` is ONE
file shared by every source's tap (see `capture_token_sources()`'s
PROBE_CONFIG branch). Clearing it unconditionally, the moment ANY source ran
`turn_off`, meant "an uninstall only uninstalls from the coding agents we
select" was false for exactly this credential: `probe wizard --agent pi
--no-capture --uninstall` silently broke Claude Code capture on the same
machine, because both sources read the same config file. Proven live
2026-08-28 (project note 18).

So the clear is now conditional on the shared state, not just this source's
own: last one out turns off the lights. Before dropping `ingest_token`,
`turn_off` asks `_other_sources_with_capture_installed()` whether any OTHER
source still has its tap plugin/package entry installed. If none do, this is
the last source and the config credential is cleared exactly as before. If
one does, the credential is deliberately left in place -- clearing it would
strand that source's own capture -- and `TurnOffResult.preserved_for` records
who it was kept for. This is not a verification failure: what "off" promises
FOR THIS SOURCE is that no session of it can use the credential, and the
killswitch this teardown already set is what guarantees that, independent of
whether the file on disk still has a token in it.

Since D3, only Claude Code reads that credential (`consumes_cli_capture_token`):
pi and Codex resolve their own paired token or nothing. So Codex or pi turning
off never sees it in their sources, and the "kept for" list only names agents
that read it, which today is nobody but Claude Code itself.

The wizard offers two shapes of off, mirroring a distinction the product already
draws (the pairing modal separates `tap revoke`, which keeps the plugin, from
`/plugin uninstall`). Both run the full teardown; UNINSTALL additionally removes
the plugin.
"""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass, field
from probe._compat import StrEnum
from pathlib import Path

from probe.cli import pi_config, plugin_cli
from probe.cli.capabilities import (
    revoke_capture_device,
    MARKETPLACE,
    TokenSource,
    agent_source,
    capture_plugin_name,
    capture_token_sources,
    consumes_cli_capture_token,
    installed_plugins,
    probe_config_path,
    tap_plugin_dir,
    tap_token_env,
)

#: Display name per capture source, for the shared-credential summary line
#: (`TurnOffResult.summary()`). Deliberately duplicated from
#: `setup.py::AGENT_LABELS` rather than imported: setup.py imports `turn_off`
#: FROM this module (`from probe.cli.capture import OffMode, clear_killswitch,
#: turn_off`), so the reverse import would be circular. Keep the two in sync
#: by hand -- same shape as `capabilities.py`'s `_TAP_TOKEN_ENV_BY_SOURCE`,
#: which hand-mirrors the tap plugin's own table for the identical reason.
_SOURCE_LABELS: dict[str, str] = {
    "claude_code": "Claude Code",
    "codex": "Codex",
    "pi": "pi",
}


def _source_label(source: str) -> str:
    return _SOURCE_LABELS.get(source, source)


class OffMode(StrEnum):
    DISABLE = "disable"
    """Stop capturing; leave the plugin installed so it is one keystroke back."""

    UNINSTALL = "uninstall"
    """Stop capturing and remove the plugin entirely."""


@dataclass
class TurnOffResult:
    """What actually happened, so the caller can tell the truth about it."""

    cleared: list[TokenSource] = field(default_factory=list)
    remaining: list[TokenSource] = field(default_factory=list)
    killswitch_set: bool = False
    daemon_stopped: bool = False
    plugin_removed: bool = False

    #: Did the server accept the revoke? True = revoked, False = nothing live
    #: to revoke, None = we could not ask (offline, or no credential resolved).
    #: Tri-state on purpose: "we did not tell it" and "it had nothing to tell"
    #: are different, and only the first is worth a warning.
    server_revoked: bool | None = None
    warnings: list[str] = field(default_factory=list)

    #: The agent source this teardown ran for (e.g. "pi"), set by `turn_off`.
    #: Only used to label the shared-credential line in `summary()`.
    source: str = ""

    #: Display names of OTHER sources whose tap is still installed, and for
    #: whose sake the shared `ingest_token` in the probe CLI config was
    #: deliberately left in place rather than cleared. Empty means either the
    #: token was cleared (this was the last source) or there was never one to
    #: preserve. See the module docstring's "THE CONFIG CREDENTIAL IS
    #: MACHINE-WIDE" section.
    preserved_for: list[str] = field(default_factory=list)

    @property
    def verified(self) -> bool:
        """Off means ALL THREE, not just the credentials.

        Capture needs a credential, a live daemon, and no killswitch. Checking
        only the credential would report "off" while a surviving uploader keeps
        draining its queue with a bearer it already holds in memory, or while a
        failed killswitch write lets the next session respawn it.

        A deliberately-PRESERVED shared credential (`preserved_for` non-empty)
        is not a failure of this postcondition even though it still shows up
        in `remaining` via PROBE_CONFIG: what "off" promises for THIS source is
        that no session of it can use the credential, and the killswitch this
        teardown already set is what guarantees that. Only PROBE_CONFIG gets
        this pass, and only when `preserved_for` says the leftover was
        deliberate -- an unexplained PROBE_CONFIG (clearing attempted and
        failed, or `preserved_for` empty for any other reason) still blocks
        verification exactly as before.
        """
        unexplained = [
            source
            for source in self.remaining
            if not (source is TokenSource.PROBE_CONFIG and self.preserved_for)
        ]
        return not unexplained and self.killswitch_set and self.daemon_stopped

    def summary(self) -> str:
        if self.verified:
            if self.preserved_for:
                who = ", ".join(self.preserved_for)
                return (
                    f"Session capture is off for {_source_label(self.source)}. "
                    f"The shared capture credential remains for: {who}."
                )
            if self.source:
                # Name the agent: another agent's own credential (Claude Code's
                # shared token, say) may well still be there, and its capture on.
                return (
                    f"Session capture is off for {_source_label(self.source)}: "
                    "none of its credentials resolves on this device."
                )
            return "Session capture is off. No credential resolves on this device."
        blockers: list[str] = [
            source.value
            for source in self.remaining
            if not (source is TokenSource.PROBE_CONFIG and self.preserved_for)
        ]
        if not self.killswitch_set:
            blockers.append("killswitch not set")
        if not self.daemon_stopped:
            blockers.append("uploader still running")
        return f"Session capture is NOT fully off — {', '.join(blockers)}"


def _clear_paired_token() -> bool:
    path = tap_plugin_dir() / ".token"
    try:
        path.unlink(missing_ok=True)
    except OSError:
        return False
    return True


def _clear_probe_config_token() -> bool:
    """Drop `ingest_token` from the CLI config, preserving everything else."""
    import json

    path = probe_config_path()
    try:
        raw = json.loads(path.read_text())
    except (OSError, ValueError):
        return True  # nothing there to clear
    if not isinstance(raw, dict):
        return True
    changed = raw.pop("ingest_token", None) is not None
    for context in (raw.get("contexts") or {}).values():
        if isinstance(context, dict) and context.pop("ingest_token", None) is not None:
            changed = True
    if not changed:
        return True
    try:
        tmp = path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(raw, indent=2, sort_keys=True))
        tmp.replace(path)
    except OSError:
        return False
    return True


def _other_sources_with_capture_installed(current: str) -> list[str]:
    """Every OTHER agent source on this machine whose capture is still
    installed, in a fixed order.

    Backs the "last one out" decision in `turn_off` for the shared
    `ingest_token` (see the module docstring). "Installed" here means the
    tap plugin/package entry is present -- NOT whether that source's capture
    is currently on -- because DISABLE deliberately leaves the plugin in
    place ("one keystroke back"), and a source sitting behind its own
    killswitch still needs the config credential to fall back to if it is
    ever re-enabled without re-pairing.

    claude_code/codex answer through `installed_plugins()`, which already
    shells out to that source's marketplace CLI and already fails soft to
    "not installed" (empty names, unverified) when the binary is absent --
    `claude_cli.run`/`plugin_cli.run` catch the missing-binary case and never
    raise it. pi has no marketplace CLI at all; `pi_config.package_entry_installed()`
    reads its settings.json entry directly, no subprocess involved. Either
    way, an unreadable signal collapses to "not installed" rather than
    raising -- this runs on the turn_off path, and a diagnostic failure here
    must not block the teardown it is trying to protect.
    """
    others: list[str] = []
    for source in ("claude_code", "codex", "pi"):
        if source == current:
            continue
        try:
            if source == "pi":
                installed = pi_config.package_entry_installed()
            else:
                installed = capture_plugin_name(source) in installed_plugins(source=source)
        except Exception:  # noqa: BLE001 - an unknown answer must read as "not installed"
            installed = False
        if installed:
            others.append(source)
    return others


def _set_killswitch() -> bool:
    """Write `.disabled`, which `hooks/session-start.sh` already checks BEFORE
    doing any work. This is what stops the next session from respawning the
    daemon, and it is why we do not need to invent a new mechanism."""
    try:
        directory = tap_plugin_dir()
        directory.mkdir(parents=True, exist_ok=True)
        (directory / ".disabled").write_text("disabled by the Probe Research wizard\n")
    except OSError:
        return False
    return True


#: What a sign-in writes into a capture source it minted a token for but whose
#: install is not confirmed yet (`setup.authorize`): a consent barrier, so an
#: installed hook never uploads with a token the person has not confirmed.
AWAITING_CONFIRMATION = "Awaiting confirmation in the Probe install wizard.\n"


def clear_stray_pi_killswitch() -> bool:
    """Remove pi's leftover sign-in marker, and only that (decision D4, narrowed).

    Before D3 every fresh Claude Code sign-in wrote `AWAITING_CONFIRMATION`
    into pi's tap folder, pi installed or not, because pi could fall back to
    Claude Code's token. Nothing ever removed it, so pi capture -- and with it
    the Probe daemon, which only the tap starts -- was off from the day pi was
    installed. The marker is a real consent barrier only while pi HOLDS a token
    of its own that the person has not confirmed; with no pi token there is
    nothing for it to protect. Every other agent's marker, and the deliberate
    off (`_set_killswitch`'s text), is never touched.
    """
    marker = tap_plugin_dir("pi") / ".disabled"
    try:
        if marker.read_text(encoding="utf-8") != AWAITING_CONFIRMATION:
            return False
    except OSError:
        return False
    if capture_token_sources("pi"):
        return False
    try:
        marker.unlink()
    except OSError:
        return False
    return True


def clear_killswitch() -> None:
    """Remove `.disabled` so capture can be turned back on from the menu."""
    try:
        (tap_plugin_dir() / ".disabled").unlink(missing_ok=True)
    except OSError:
        pass


# --- stop-daemon forensics ---------------------------------------------------
#
# A tap daemon has repeatedly been found dead with its pid file unlinked and NO
# shutdown sentinel — a signature only _stop_daemon() below produces
# (session-end.sh touches the sentinel; a crash leaves the pid file behind).
# macOS cannot tell the dying process who signalled it, so attribution has to
# be written by the KILLER: every invocation of _stop_daemon() is journalled
# here before any signal is sent. A daemon death with no matching entry
# exonerates this code path — which is itself the answer.

_STOP_LOG_MAX_BYTES = 256 * 1024
_STOP_LOG_KEEP_LINES = 200


def stop_log_path() -> Path:
    """The killer-side journal, in the tap state dir both sides already share
    (env overrides and the codex flavor included, via tap_plugin_dir())."""
    return tap_plugin_dir() / "logs" / "stop-daemon.jsonl"


def _append_stop_log(record: dict) -> None:
    """Append one invocation record. May raise; the call site suppresses.

    Rotation is deliberately crude: past _STOP_LOG_MAX_BYTES, keep the newest
    _STOP_LOG_KEEP_LINES lines. Precision is not the point — surviving years
    of wizard runs without eating the disk is.
    """
    import json

    path = stop_log_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        oversized = path.stat().st_size > _STOP_LOG_MAX_BYTES
    except OSError:
        oversized = False
    if oversized:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        path.write_text("\n".join(lines[-_STOP_LOG_KEEP_LINES:]) + "\n", encoding="utf-8")
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, separators=(",", ":")) + "\n")


def last_stop_event() -> dict | None:
    """The newest parseable journal record, or None. Fail-soft throughout:
    `probe doctor` reads this, and a diagnostic must never crash."""
    import json

    try:
        lines = stop_log_path().read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None
    for raw in reversed(lines):
        raw = raw.strip()
        if not raw:
            continue
        try:
            record = json.loads(raw)
        except ValueError:
            continue
        if isinstance(record, dict):
            return record
    return None


def describe_last_stop() -> str | None:
    """One doctor-ready line: when, which command, how many daemons signalled."""
    event = last_stop_event()
    if event is None:
        return None
    from datetime import datetime, timezone

    ts = event.get("ts")
    when = (
        datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        if isinstance(ts, (int, float))
        else "unknown time"
    )
    argv = event.get("argv")
    cmd = " ".join(str(a) for a in argv) if isinstance(argv, list) and argv else "unknown command"
    signalled = event.get("signalled")
    count = len(signalled) if isinstance(signalled, list) else 0
    plural = "" if count == 1 else "s"
    return f"{when} by `{cmd}` (pid {event.get('pid')}), {count} daemon{plural} signalled"


def _looks_like_the_uploader(pid: int) -> bool:
    """Confirm a PID really is the tap before signalling it.

    /tmp is world-writable and the PID files live there, so an unprivileged
    local process can plant `probe-research-tap-watcher-<anything>.pid`
    containing any number it likes. Signalling on the strength of a filename
    would let it aim SIGTERM at an arbitrary process running as this user. PID
    reuse causes the same accident without anyone being malicious.

    So: ask the OS what the process actually is, and only proceed if it names
    the tap.
    """
    try:
        completed = subprocess.run(  # noqa: S603 - fixed binary, no shell
            ["/bin/ps", "-ww", "-p", str(pid), "-o", "command="],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return capture_plugin_name() in completed.stdout or "tap" in completed.stdout.split()


#: Overrides where `_stop_daemon()` looks for pid files. The tap's hooks always
#: write them to `/tmp` (session-start.sh, `capture_state.pid_file`), so this
#: exists ONLY so a test suite can aim the stop away from the machine's real
#: uploaders: the glob matches EVERY live session's daemon, and tests calling
#: `turn_off()` SIGTERMed all of them on a shared box (2026-09-28).
#: `agent/tests/conftest.py` sets it for every test.
PID_DIR_ENV = "PROBE_TEST_TAP_PID_DIR"


def _pid_dir() -> str:
    return os.environ.get(PID_DIR_ENV) or "/tmp"


def _stop_daemon() -> tuple[bool, list[str]]:
    """Ask the running uploader to stop, and confirm it did.

    Returns (stopped, warnings). `stopped` is False if any uploader is still
    alive afterwards, which must stop the caller claiming capture is off: a
    daemon that ignored SIGTERM still holds its bearer in memory and still has
    a queue to drain.

    Every invocation is journalled to stop_log_path() BEFORE any signal goes
    out, so a daemon that dies by this hand has a matching record even if this
    process dies mid-stop. The journal is strictly best-effort: a logging
    failure must never prevent or delay the stop.
    """
    warnings: list[str] = []
    import glob
    import signal
    import sys
    import time

    survivors: list[int] = []
    from probe.cli.capture_state import watcher_prefix

    prefix = watcher_prefix(agent_source())
    targets: list[tuple[int, str]] = []
    for pid_file in glob.glob(f"{glob.escape(_pid_dir())}/{prefix}-watcher-*.pid"):
        try:
            stat = os.stat(pid_file)
            if stat.st_uid != os.getuid():
                warnings.append(f"ignoring {pid_file}: not owned by this user")
                continue
            pid = int(open(pid_file).read().strip())  # noqa: SIM115
        except (OSError, ValueError):
            continue
        if pid <= 1 or not _looks_like_the_uploader(pid):
            # Stale file or an impostor. Do not signal it.
            continue
        targets.append((pid, pid_file))

    try:
        _append_stop_log(
            {
                "ts": time.time(),
                "pid": os.getpid(),
                "argv": list(sys.argv),
                "signalled": [{"pid": pid, "pid_file": pid_file} for pid, pid_file in targets],
            }
        )
    except Exception:  # noqa: BLE001 - forensics must never block the stop
        pass

    for pid, pid_file in targets:
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass  # already gone: the desired state
        except OSError as exc:
            warnings.append(f"could not stop uploader pid {pid}: {exc}")
            survivors.append(pid)
            continue
        # Wait for it, rather than assuming. An uploader mid-flush can take a
        # moment, and reporting "off" while it is still draining is the lie.
        for _ in range(20):
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                break
            except OSError:
                break
            time.sleep(0.1)
        else:
            survivors.append(pid)
            warnings.append(f"uploader pid {pid} is still running after SIGTERM")
            continue
        try:
            os.unlink(pid_file)
        except OSError:
            pass
    return (not survivors), warnings


def _uninstall_plugin() -> tuple[bool, list[str]]:
    selected = agent_source()
    if selected == "pi":
        # pi has no marketplace: its "plugin" is the settings.json packages
        # entry pi_config owns. Branch BEFORE plugin_cli -- this function
        # used to fall straight through to plugin_cli.uninstall, which
        # resolved pi's binary as "claude" and ran the uninstall against the
        # user's real Claude Code (the audited bug class; binary_name now
        # raises on pi so a regression here fails loud instead of silently).
        removal = pi_config.remove_package_entry()
        if not removal.ok:
            return False, [f"pi package-entry removal failed: {removal.detail}"]
        return True, []
    result = plugin_cli.uninstall(selected, f"{capture_plugin_name(selected)}@{MARKETPLACE}")
    if not result.reachable:
        return False, [
            f"`{plugin_cli.binary_name(selected)}` not found, so the plugin was left installed"
        ]
    if not result.ok:
        return False, [f"plugin uninstall failed: {result.detail}"]
    return True, []


def turn_off(mode: OffMode = OffMode.DISABLE) -> TurnOffResult:
    """Turn capture off and PROVE it, rather than assuming.

    Order matters: set the killswitch before clearing credentials, so a session
    starting mid-teardown finds the daemon already disabled rather than racing a
    half-cleared credential set.
    """
    result = TurnOffResult()
    result.source = agent_source()
    before = capture_token_sources()

    # SERVER FIRST, while the bearer still exists. `_clear_paired_token` below
    # deletes the very `.token` this authenticates with, so past that point the
    # device can never be revoked server-side -- not here, and not by a later
    # `python -m tap revoke`, which reads the same file and skips its server
    # call when it finds nothing. Leaving it unrevoked keeps the row at
    # `revoked_at IS NULL` forever: the machine lingers in the dashboard's
    # device list and its capture credential stays valid on a token nobody
    # holds any more.
    #
    # BEST EFFORT, DELIBERATELY. "Off" is a promise about THIS machine, and the
    # local teardown below is what keeps it. An unreachable server must never
    # be the reason someone cannot turn capture off.
    result.server_revoked = revoke_capture_device()
    if result.server_revoked is None and TokenSource.PAIRED_FILE in before:
        result.warnings.append(
            "could not tell the server this device is gone; it may linger in "
            "your dashboard's Devices list -- disconnect it there"
        )

    result.killswitch_set = _set_killswitch()
    if not result.killswitch_set:
        result.warnings.append("could not write the killswitch marker")

    if TokenSource.PAIRED_FILE in before and _clear_paired_token():
        result.cleared.append(TokenSource.PAIRED_FILE)
    if TokenSource.PROBE_CONFIG in before:
        # Machine-wide, not source-scoped -- see the module docstring. Clear
        # it only if this is the last source still holding capture installed;
        # otherwise leave it for whoever else needs it and say so.
        other_sources = [
            source
            for source in _other_sources_with_capture_installed(result.source)
            if consumes_cli_capture_token(source)
        ]
        if other_sources:
            result.preserved_for = [_source_label(source) for source in other_sources]
        elif _clear_probe_config_token():
            result.cleared.append(TokenSource.PROBE_CONFIG)

    stopped, stop_warnings = _stop_daemon()
    result.daemon_stopped = stopped
    result.warnings.extend(stop_warnings)

    if mode is OffMode.UNINSTALL:
        removed, warnings = _uninstall_plugin()
        result.plugin_removed = removed
        result.warnings.extend(warnings)

    # THE VERIFICATION. Re-resolve from scratch rather than trusting the
    # bookkeeping above.
    result.remaining = list(capture_token_sources())
    if TokenSource.ENVIRONMENT in result.remaining:
        # The one source the wizard genuinely cannot fix: it cannot unset a
        # variable in the parent shell. Saying so is the only honest option --
        # reporting "off" here would be the exact lie this module exists to
        # prevent.
        token_env = tap_token_env()
        result.warnings.append(
            f"{token_env} is set in your shell environment. This process "
            f"cannot unset it for you. Run `unset {token_env}` and remove "
            "it from your shell profile, or capture will resume in new sessions."
        )
    return result
    (agent_source,)
    (capture_plugin_name,)
