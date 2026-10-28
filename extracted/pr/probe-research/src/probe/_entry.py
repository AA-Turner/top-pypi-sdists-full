"""Console-script entry points that survive a missing optional dependency.

``probe`` needs ``typer`` and ``questionary``; ``probe-research-mcp`` needs
``mcp``, ``anyio`` and ``tiktoken``. Plan 2.11 moves them into the ``cli`` and
``mcp`` extras (``all`` = both) so a training environment can install the SDK
alone. An install without them used to die in the console-script loader with
a bare ImportError traceback; this prints what is missing and the one command
that fixes it, and exits 1. Imports nothing heavy at module level.
"""

from __future__ import annotations

import sys

#: Which top-level modules each entry point needs, and the extra that brings them.
_CLI_MODULES = ("typer", "questionary", "click")
_MCP_MODULES = ("mcp", "anyio", "tiktoken", "starlette")


def _missing_dependency(exc: ModuleNotFoundError, modules: tuple[str, ...]) -> str | None:
    """The missing module's name when it is one of ``modules``, else None (a
    real bug, which must keep its traceback)."""
    name = (exc.name or "").split(".")[0]
    return name if name in modules else None


def _explain(tool: str, extra: str, module: str) -> int:
    print(
        f"{tool}: this install of probe-research has the Python SDK but not the "
        f"`{extra}` dependencies (missing: {module}).\n"
        f"  Install them:  pip install 'probe-research[all]'\n"
        f"  (a uv tool install:  uv tool install 'probe-research[all]', or "
        f"'probe-research[all,daemon]' where the Probe daemon records)",
        file=sys.stderr,
    )
    return 1


#: How long a `probe` command (an agent's or a person's, read-only ones too)
#: waits out an in-place update before it answers busy: under an agent's own
#: command timeout (Claude Code's Bash tool: 120 s). A machine's first update
#: (the one-time switch to the side-by-side layout) is in place and takes
#: longer than WAIT_S; failing the command there disturbed running agents
#: (release gate, 2026-10-25), waiting does not.
IN_PLACE_WAIT_S = 90.0
#: Set on the fresh interpreter a waited start re-runs in (`_rerun`), with the
#: count of re-runs so far: never more than MAX_RERUNS.
RERUN_ENV = "PROBE_ENTRY_RERUN"
MAX_RERUNS = 3


def _never_waits(args: list[str]) -> bool:
    """A start that must never wait for an update: a hook's (its deadline is
    the agent's turn, plan D12: only while it is live, never a detached job's
    that outlived its hook, `barrier.hook_deadline_live`)."""
    from probe.service import barrier

    return barrier.hook_deadline_live()


def _rerun(argv: list[str] | None) -> int:
    """Run this same command again in a fresh interpreter, on the code the
    update just installed. This process imported `probe.service` (the barrier,
    its paths) before the files were replaced, and the new CLI loaded on top
    of those old modules fails (`module 'probe.service.procid' has no
    attribute 'exists'`, CLI 0.286.0 -> main, release gate 2026-10-25).
    POSIX: exec (same pid, stdin and exit status). Windows: exec does not
    keep the console's wait, so a child whose exit status is returned."""
    import os

    count = int(os.environ.get(RERUN_ENV) or "0") + 1
    env = dict(os.environ, **{RERUN_ENV: str(count)})
    if argv is None:
        command = [sys.executable, *getattr(sys, "orig_argv", [sys.executable, *sys.argv])[1:]]
    else:
        command = [sys.executable, "-m", "probe", *argv]
    if os.name == "nt":
        import subprocess

        return subprocess.call(command, env=env)
    os.execve(sys.executable, command, env)
    return 0  # not reached


def _update_barrier(argv: list[str] | None) -> int | None:
    """While the Probe service updates the CLI's env in place (plan X1), wait
    for it (IN_PLACE_WAIT_S), then run the command again in a fresh
    interpreter on the new code (`_rerun`); still updating after that: the
    busy status. All BEFORE the CLI is imported, so nothing loads from files
    being replaced. An update side by
    side or of the plugins only replaces nothing a `probe` runs from, and a
    process pinned to a version env is never replaced: no wait at all, the
    installed version runs (`barrier._blocks`, plan C6). A hook's call never
    waits: busy at once. One stat when no update
    runs. `probe daemon worker` gets the worker's own come-back-later status,
    which its supervisor answers with a later respawn instead of a crash
    count; it also comes back later while the service is stopping the running
    workers before an update (plan D7), so it never starts on the code about
    to be replaced. A read-only command waits like any other: busy would fail
    an agent's command mid-work."""
    try:
        from probe.service import barrier
    except Exception:  # noqa: BLE001 -- never a reason not to run `probe`
        return None
    args = sys.argv[1:] if argv is None else argv
    worker = args[:2] == ["daemon", "worker"]
    try:
        if worker:
            # `probe uninstall` runs: no worker starts on the files it removes
            # (its supervisor comes back later, by which time it is gone).
            from probe._shared import uninstall_barrier

            if uninstall_barrier.live():
                print("probe: Probe is being uninstalled on this computer; no daemon worker starts.",
                      file=sys.stderr)
                return barrier.WORKER_BUSY_EXIT_CODE
        if worker and barrier.workers_held():
            print(f"probe: {barrier.MESSAGE}.", file=sys.stderr)
            return barrier.WORKER_BUSY_EXIT_CODE
        if barrier.wait(0.0):
            return None  # the common path: no update holds a start back
        if worker or _never_waits(args):
            pass  # a worker comes back later; a hook's call never waits
        else:
            import os

            print("probe: Probe is updating itself on this machine; waiting for it to finish...",
                  file=sys.stderr)
            if barrier.wait(IN_PLACE_WAIT_S):
                if int(os.environ.get(RERUN_ENV) or "0") >= MAX_RERUNS:
                    return None
                return _rerun(argv)
    except Exception:  # noqa: BLE001 -- never a reason not to run `probe`
        return None
    print(f"probe: {barrier.MESSAGE}.", file=sys.stderr)
    return barrier.WORKER_BUSY_EXIT_CODE if worker else barrier.BUSY_EXIT_CODE


def _daemon_worker_proxy(argv: list[str] | None) -> int | None:
    """`probe daemon worker` started by an old tap: its run goes to the Probe
    service's daemon host, this process waits for it (`probe.daemon.proxy`).
    None: no host to reach, the worker runs here as before."""
    args = sys.argv[1:] if argv is None else argv
    if args[:2] != ["daemon", "worker"]:
        return None
    try:
        from probe.daemon import proxy

        return proxy.main(args[2:]) if proxy.eligible() else None
    except Exception:  # noqa: BLE001 -- never a reason not to run the worker
        return None


def main(argv: list[str] | None = None) -> int:
    """``probe``."""
    busy = _update_barrier(argv)
    if busy is not None:
        return busy
    hosted = _daemon_worker_proxy(argv)
    if hosted is not None:
        return hosted
    try:
        import importlib

        from probe.cli import main as cli_main

        # `probe.cli` loads its implementation on first use: load it here, so a
        # missing extra is this message, not a traceback from inside the call.
        importlib.import_module("probe.cli.main")
    except ModuleNotFoundError as exc:
        module = _missing_dependency(exc, _CLI_MODULES)
        if module is None:
            raise
        return _explain("probe", "cli", module)
    return cli_main(argv)


def mcp_main() -> None:
    """``probe-research-mcp``."""
    try:
        from probe.mcp.server import main as server_main
    except ModuleNotFoundError as exc:
        module = _missing_dependency(exc, _MCP_MODULES)
        if module is None:
            raise
        raise SystemExit(_explain("probe-research-mcp", "mcp", module)) from None
    server_main()


def mcp_http_main() -> None:
    """``probe-research-mcp-http``."""
    try:
        from probe.mcp.server import main_http
    except ModuleNotFoundError as exc:
        module = _missing_dependency(exc, _MCP_MODULES + ("uvicorn",))
        if module is None:
            raise
        raise SystemExit(_explain("probe-research-mcp-http", "mcp", module)) from None
    main_http()
