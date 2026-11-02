"""hand an update off without blocking the command: a detached child, the Probe service, or the moment a run ends."""

from __future__ import annotations
import os
import subprocess
import sys

#: Where the Probe service is the updater, the every-command check hands it an
#: available update at most this often: the service's own `update.check_now`
#: cooldown (`probe.service.updater.settings.CHECK_NOW_COOLDOWN_S`), inside which it
#: answers `recent` anyway. A coding agent's hooks and the daemon run `probe`
#: off a terminal dozens of times an hour (Bucket's laptop: 293 in three hours,
#: 2026-10-23), so this is one asking process per window, not one per command.
_SERVICE_ASK_EVERY_S = 15 * 60
#: Its stamp (one byte once an ask is claimed; its mtime is the last ask), beside
#: `autoupdate.json`.
_SERVICE_ASK_STAMP = "service-update-ask"


def _spawn_detached(argv: list[str], env: dict[str, str]) -> None:
    """Launch `argv` fully detached, leaving NO child of ours behind.

    `start_new_session=True` detaches the session but does NOT reparent: the
    process stays our child, so if we never wait for it, its exit status sits in
    the table as a zombie until we exit. That is invisible for `probe ls` and
    real for `probe exec`, which can own a training process for hours.

    So the target daemonizes -- it forks and its first stage exits immediately
    (see version_refresh.main) -- and we reap that first stage right here. The
    real work is carried by the grandchild, which init adopts.

    Windows has no fork, so the child does its work inline and there is no
    first stage to reap (nor a zombie to leave): return at once. A `--apply`
    child waits for THIS process to exit, so waiting on it here held every
    command that found an update for the full 10 s. `start_new_session` means
    nothing there: a new process group with no console window keeps the child
    out of the terminal's Ctrl-C (an upgrade killed halfway) and shows nothing.
    """
    windows = os.name == "nt"
    child = subprocess.Popen(  # noqa: S603 -- our own interpreter, our own module
        argv,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        close_fds=True,
        env=env,
        # CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW, as the Probe service's own start
        **({"creationflags": 0x00000200 | 0x08000000} if windows else {"start_new_session": True}),
    )
    if windows:
        return
    try:
        # The first stage forks and exits at once, so this returns immediately.
        # The timeout is a backstop, not a wait: if the fork ever fails and the
        # process runs its work inline, we abandon it rather than block a command.
        child.wait(timeout=10)
    except subprocess.TimeoutExpired:
        pass


def _spawn_version_refresh() -> None:
    """Refresh the manifest in a DETACHED child; never fetch inline.

    The invoking process must not make a network call. `PROBE_VERSION_TIMEOUT` is
    3s, so an inline fetch means one `probe log` in every TTL blocking for up to
    three seconds inside somebody's training loop -- a periodic step-time spike
    that correlates with nothing in their code. This repo has been here before:
    every run-anchored CLI write used to make a network call before the write,
    and it had to be removed.

    The cost is that this invocation compares against the OLD manifest and the
    nudge lands on the NEXT one. That is how update-notifier behaves, for the
    same reason.

    Where a Probe service answers, it refreshes instead (`manifest.refresh`:
    one child of its own per context, the same refresh and update reports
    this child would run) and this command goes on without spawning; it never
    waits for the fetch. The claim then simply ages out (REFRESH_CLAIM_SECONDS),
    long after the service's child has written a fresh cache: the commands
    meanwhile skip at the claim, as they do while a detached child fetches. No
    service, an older one, Windows, a `PROBE_VERSION_CACHE` it cannot be told,
    a caller in a sandbox, or a service refresh that did not land (`recent`
    with this cache still stale): the detached child, as before.
    """
    from probe.shared.updates import version_policy

    if not version_policy.claim_refresh():
        return  # somebody is already fetching; a burst of 8 runs makes 1 request
    try:
        from probe.cli.lifecycle import service_calls

        if service_calls.refresh_manifest():
            return
    except Exception:  # noqa: BLE001 -- the detached child is never worse than none
        pass
    env = dict(os.environ)
    env[version_policy.REFRESH_OWNER_ENV] = str(os.getpid())
    try:
        _spawn_detached([sys.executable, "-m", "probe.cli.version_refresh"], env)
    except Exception:  # noqa: BLE001
        version_policy.release_refresh()


def _spawn_update(flag: str, *, trigger: str | None = None, available: str | None = None) -> None:
    """Launch version_refresh detached, naming OURSELVES as the pid to outlive.

    The wait is the whole point, and it is why both update triggers share this
    rather than each building the env themselves. The CLI imports lazily
    throughout, so a child that starts replacing the installed tree before this
    process exits would break the very command that spawned it.

    Raises whatever `_spawn_detached` raises; both callers are fail-open and
    swallow it, for different reasons documented at their own sites.
    `available`: the version the caller found, for a skip's record.
    """
    from probe.shared.updates import autoupdate

    if _service_owns_updates():
        # The service's words: a harness's session start is `session`.
        _ask_service_to_update("session" if trigger == autoupdate.Trigger.SESSION_START.value else "cli")
        return
    # The CLI's own updater lands in place, so nothing may run from the CLI's
    # files: never from a command a Probe daemon runs, nor while a daemon worker
    # holds its lock -- whichever trigger asked (every command, a run's end, pi's
    # session start, a remote ask). Off a terminal (C3) most callers are those.
    from probe.sdk.agent_session import DAEMON_SESSION_ENV

    if os.environ.get(DAEMON_SESSION_ENV):
        return
    from probe.service.updater.quiet.workers import daemon_worker_running

    if daemon_worker_running():
        autoupdate.record_skip(
            autoupdate.SKIP_DAEMON_RECORDING, available=available, trigger=trigger or autoupdate.Trigger.CLI.value
        )
        return
    env = dict(os.environ)
    env[autoupdate.WAIT_FOR_PID_ENV] = str(os.getpid())
    # What asked, for the server's update report: a harness's session start
    # when named; else the CLI's own trigger.
    env[autoupdate.TRIGGER_ENV] = trigger or autoupdate.Trigger.CLI.value
    _spawn_detached([sys.executable, "-m", "probe.cli.version_refresh", flag], env)


def _service_owns_updates() -> bool:
    """Is the Probe service this machine's updater? Always, on POSIX (it has no
    switch): nothing else spawns one (plan Q4), since the service applies
    updates only on a quiet machine and its own child outlives no CLI command."""
    if not hasattr(os, "fork"):
        return False
    try:
        from probe.foundation import service_api as service_client
    except Exception:  # noqa: BLE001 -- the old path is never worse than none
        return False
    # A service needs an interpreter to start with (runtime.json, else the uv
    # tool env's): a pip or pipx install without either keeps the old updater,
    # or its updates would be dropped.
    try:
        return service_client.runtime_python() is not None
    except Exception:  # noqa: BLE001
        return False


def _ask_service_to_update(trigger: str) -> None:
    """`ensure` the service and send it `update.check_now`, from a detached
    process (`python -m probe.service.client check-now`): starting the service
    can take a moment, and this command must not wait for it. That process
    first waits for THIS one to exit (`--wait-for-pid`, as `WAIT_FOR_PID_ENV`
    does for the old spawn): the service's quiet check and barrier cannot see
    a plain command, which is still importing from the env an update replaces.
    `-I`: the researcher's working folder (a `probe/` package, a `json.py`)
    never shadows ours."""
    subprocess.Popen(  # noqa: S603 -- our own interpreter, our own module
        [
            sys.executable,
            "-I",
            "-m",
            "probe.service.client",
            "check-now",
            "--trigger",
            trigger,
            "--wait-for-pid",
            str(os.getpid()),
        ],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
        close_fds=True,
    )


def _hand_update_to_service(command: str | None) -> None:
    """The every-command check's update, where the Probe service is the
    updater: ask it (`_ask_service_to_update`, trigger `cli`) at most once per
    `_SERVICE_ASK_EVERY_S`, from any command, terminal or not, a run live or
    not -- the service decides, and records why when it waits. Records nothing.

    Not from `probe service` (it talks to the service itself), nor from a
    run-scoped command (`_UPDATE_HOT_PATH_COMMANDS`) inside a run: no process
    is started from inside a training loop. `artifact`, `run` and `outbox`
    outside one ask as any command does (`_ASK_OUTSIDE_A_RUN`,
    `_inside_a_run`); `log`, `span` and `exec` never do. Machines that only
    run those still update on the service's own schedule, the keeper's and at
    each coding agent's session start. Nor from a command
    the service itself runs (`paths.SERVICE_CHILD_ENV`: its team-note sync):
    the service is the updater, and an ask from its first command would land
    while the rest of that job still runs from the CLI's files.

    The window is claimed under an exclusive, non-blocking lock on the stamp,
    so a burst of commands starting together asks once; a command that finds
    the lock taken leaves the ask to its holder. A stamp that cannot be opened
    or locked asks nothing: one asking process per command is worse than none.
    Never raises."""
    exempt = command in _UPDATE_HOT_PATH_COMMANDS and command not in _ASK_OUTSIDE_A_RUN
    if command == _SERVICE_COMMAND or exempt:
        return
    try:
        # `paths`, not `children`: loaded already by `_service_owns_updates`,
        # where `children` would import asyncio on every command (~7 ms).
        from probe.foundation.service_api.paths import SERVICE_CHILD_ENV

        if os.environ.get(SERVICE_CHILD_ENV):
            return
        if command in _ASK_OUTSIDE_A_RUN and _inside_a_run():
            return
        if _claim_window(_SERVICE_ASK_STAMP, _SERVICE_ASK_EVERY_S):
            _ask_service_to_update("cli")
    except Exception:  # noqa: BLE001 -- the check never breaks the command it runs before
        pass


def _spawn_session_start_update() -> None:
    """Apply an update found at an extension harness's session start (pi's), NOW.

    Nothing waits for pi: neither the CLI nor pi's package (`pi update` runs
    under a running pi, which keeps what it loaded until `/reload`; see
    `upgrading._update_pi_package`). Waiting for that pi held both back: a pi
    process lives for days, and strand-ai's pi-only laptop sat on CLI 0.219.0
    through a day of pi session starts (2026-10-07), then on an old pi package
    with pi agents running around the clock (2026-10-15).
    `--apply-if-newer` re-checks on a fresh manifest under the update lock, so
    several pi sessions starting at once update once.
    """
    from probe.shared.updates import autoupdate

    try:
        _spawn_update("--apply-if-newer", trigger=autoupdate.Trigger.SESSION_START.value)
    except Exception:  # noqa: BLE001 -- fail-open: never block the command
        pass


def _spawn_autoupdate(available: str | None = None) -> None:
    """Apply the upgrade from the root callback, where an update was found
    (`available`, the version the cache names).

    `--apply` rather than `--apply-if-newer`: this path only runs after
    `_version_notice` already compared against the cached manifest, so a second
    comparison in the child would be redundant.
    """
    try:
        _spawn_update("--apply", available=available)
    except Exception:  # noqa: BLE001 -- fail-open: never block the command
        pass


def _apply_deferred_update() -> None:
    """Apply an update at the moment a run provably ended. Never raises.

    WHY THIS EXISTS. `_version_notice` finds the update and then refuses it,
    because every command a run-scoped researcher types is on
    `_UPDATE_HOT_PATH_COMMANDS`. That refusal is correct and terminal: nothing
    revisited it, so a researcher who installs via the wizard and never opens a
    new agent session never updated at all. This is the revisit.

    THE GATES, and what each one is actually for:

        enabled?      one small state-file read. On for the managed CLI unless
                      turned off; an install that is not it and never opted in
                      touches one file and stops.
        any_live()?   the only real safety check here. It is what stops an
                      upgrade landing on a run in ANOTHER process -- an SDK
                      training script holds an flock for its whole life.

    No TTY test, deliberately. `probe exec python train.py > train.log` has a
    non-tty stdout, and that is the shape this fix exists to reach; the TTY gate
    `_version_notice` had then would have defeated it silently. Nothing is lost:
    the hazard the TTY test proxies for is a live run, which `any_live()` answers
    directly, and `perform_update` re-checks it again in the child.

    No cache read and no comparison, also deliberately. After a multi-hour run
    the cached manifest is always stale, and refreshing it here would mean
    blocking the command. The child fetches and decides instead
    (`version_refresh --apply-if-newer`).

    THE GUARD IS NOT DECORATION. The exec call site is inside a `finally`, so an
    exception raised here replaces whatever was already propagating -- turning a
    clean run into a traceback, or masking the KeyboardInterrupt from a Ctrl-C'd
    training run. `probe exec` exists to hand back its child's exit code.
    """
    try:
        from probe.shared.updates import version_policy

        if not version_policy.autoupdate_enabled():
            return

        from probe.foundation.durable import run_lock

        if run_lock.any_live():
            return

        _spawn_update("--apply-if-newer")
    except Exception:  # noqa: BLE001 -- see docstring: must never break the command
        pass
from probe.cli.lifecycle.lifecycle import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _ASK_OUTSIDE_A_RUN,
    _SERVICE_COMMAND,
    _UPDATE_HOT_PATH_COMMANDS,
    _claim_window,
    _inside_a_run,
)
