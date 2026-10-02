"""The detached half of the CLI's version check.

Three jobs, one entry point, because all of them must happen OUT of the invoking
process:

    (no args)   refresh the cached manifest. The invoking CLI must never make a
                network call -- a 3s timeout on the every-command path would put
                a periodic stall inside training loops.

    --apply     wait for the spawning command to exit, then upgrade. The wait is
                what stops `uv tool upgrade` from replacing the tree while the
                command that triggered it is still lazily importing from it.

    --apply-if-newer
                the RUN-END path. Fetch a fresh manifest, compare it against the
                installed CLI, and only then do what --apply does.

WHY --apply-if-newer EXISTS RATHER THAN REUSING --apply.

The run-end trigger fires whenever a run finishes and no other run is live. It
cannot consult the cached manifest to decide -- after a multi-hour run that cache
is stale, and reading it in the parent is exactly the blocking work the run-end
path refuses to do. So the decision has to happen HERE, on fresh data.

`--apply` cannot make that decision, because `perform_update` does not have one:
it takes `cli_latest(manifest)` -- the latest version, not "is it newer" -- and
calls `upgrade_cli` unconditionally. Spawning it at every run end would run
`uv tool upgrade` plus two `claude plugin` subprocesses forever, on a machine
that is already current, and would overwrite `last_attempt` each time with a
no-op success -- destroying the one record that tells a working auto-updater from
a dead one.

The plugin's SessionStart hook does not need this mode: it compares before it
spawns anything (version_check.py's `_remote_gt_local`).

Run as `python -m probe.cli.version_refresh`, detached via start_new_session so it
outlives the CLI that spawned it. Nothing here prints anywhere a human will see;
the audit record in `autoupdate` is how a detached run reports what happened.
"""

from __future__ import annotations

import os
import sys


def _daemonize() -> bool:
    """Fork so the caller's direct child exits at once. True in the worker.

    Without this the spawning CLI has to either wait for the whole refresh
    (defeating the point) or leave a zombie until it exits -- which for
    `probe exec` means the length of a training run. Forking here lets the CLI
    reap the first stage immediately while init adopts the grandchild.

    Returns False in the stage that should exit. Where fork is unavailable
    (Windows), returns True and the work runs in this process: correct, just not
    reaped as early.
    """
    try:
        if os.fork() > 0:
            os._exit(0)  # first stage: vanish so the parent's wait() returns
    except (AttributeError, OSError):
        return True  # no fork here; carry on inline
    try:
        os.setsid()
    except (AttributeError, OSError):
        pass
    return True


def _refresh() -> None:
    """Fetch and cache the manifest, then release the single-flight claim.

    The claim was taken by the SPAWNER, before this process existed -- otherwise
    eight concurrent invocations would each spawn a refresher and only then
    discover they were racing. It carries the spawner's pid, so releasing it
    means releasing THAT claim, not whatever claim happens to be there now.
    """
    from probe import version_policy
    from probe.sdk.tls import ssl_context

    owner = os.environ.get(version_policy.REFRESH_OWNER_ENV)
    try:
        version_policy.refresh(context=ssl_context())
    finally:
        try:
            version_policy.release_refresh(int(owner) if owner else None)
        except (TypeError, ValueError):
            version_policy.release_refresh()


def _apply() -> None:
    """Wait out the parent, then upgrade.

    `perform_update` does the waiting and re-checks the run lock afterwards; both
    live there because the wizard's own Update action shares this path and must
    behave identically when it is not spawned (no parent pid in the environment,
    so no wait).
    """
    from probe import version_policy
    from probe.cli import autoupdate
    from probe.cli.upgrading import perform_update

    # Single-writer across concurrent sessions. Without it, several Claude Code
    # windows starting at once each run `uv tool upgrade` against one install.
    if not autoupdate.acquire_lock():
        return
    try:
        perform_update(base_url=version_policy.base_url())
    finally:
        autoupdate.release_lock()


def _apply_if_newer() -> None:
    """Fetch, compare, and only then upgrade. The run-end path's entry point.

    The fetch is authoritative rather than cached ON PURPOSE: the parent that
    spawned us could not consult the cache without doing exactly the blocking
    work the run-end trigger exists to avoid, so the freshness lives here.

    A failed fetch means we do NOTHING. That inverts `perform_update`'s posture,
    which upgrades anyway on a failed fetch because "unable to ask what is latest
    is not a reason to refuse to move" -- true when a human asked for an upgrade,
    wrong here, where nobody asked and the next run end will try again.

    The manifest is handed to `perform_update` so it does not fetch a second one;
    a release landing between the two fetches would otherwise mean comparing
    against one version and upgrading toward another.
    """
    from probe import __version__, version_policy
    from probe.cli import autoupdate, updater
    from probe.cli.upgrading import perform_update

    base = version_policy.base_url()

    # THE LOCK COMES FIRST, BEFORE THE FETCH, and that ordering is the whole
    # rate limit on this path.
    #
    # `_apply` can take its lock later because its caller already decided; this
    # mode's entire job is the deciding, and the deciding costs a request. Every
    # run end that clears the parent's gates spawns one of these, so a sweep of
    # short runs -- `for r in $(seq 500); do probe exec r$r -- true; done` --
    # would put 500 manifest requests on the API within seconds, none of which
    # would ever reach the upgrade because the CLI is already current. Nothing
    # else bounds this path: the parent deliberately reads no cache, so there is
    # no TTL upstream to lean on.
    #
    # With the lock first, 500 children make ONE request and 499 exit at this
    # line. That is also why the fetch failure below returns from INSIDE the
    # `finally` -- the lock must be released on every exit, not just the happy one.
    if not autoupdate.acquire_lock():
        return
    try:
        try:
            manifest = updater.fetch_latest(base)
        except Exception:  # noqa: BLE001 -- see docstring: no manifest, no upgrade
            return
        if not updater.cli_update_available(manifest, __version__):
            return
        perform_update(base_url=base, manifest=manifest)
    finally:
        autoupdate.release_lock()


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    # Detach FIRST, before any real work, so the spawning CLI's wait() returns
    # in microseconds no matter how long the work takes. `--no-daemon` keeps the
    # work in this process for tests, which need it synchronous to assert on.
    if "--no-daemon" not in args:
        _daemonize()
    try:
        # Checked BEFORE `--apply`: the flags share a prefix, and `in` on a list
        # matches whole elements, but ordering here keeps the intent obvious to
        # anyone adding a fourth mode.
        if "--apply-if-newer" in args:
            _apply_if_newer()
        elif "--apply" in args:
            _apply()
        else:
            _refresh()
    except Exception:  # noqa: BLE001
        # Detached: there is no terminal to raise into, and a traceback on stderr
        # goes to /dev/null. Failures that matter are in the audit record.
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
