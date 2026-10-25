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


#: Commands that only read: during an in-place update (the one kind that still
#: holds a start back) they answer busy at once instead of waiting.
_READ_ONLY = frozenset({("version",), ("status",), ("doctor",), ("help",), ("session", "status"),
                        ("service", "status")})
_READ_ONLY_FLAGS = frozenset({"--version", "-V", "--help", "-h"})


def _never_waits(args: list[str]) -> bool:
    """A start that must never wait for an update: a hook's (its deadline is
    the agent's turn, plan D12: only while it is live, never a detached job's
    that outlived its hook, `barrier.hook_deadline_live`) and a read-only
    command's."""
    from probe.service import barrier

    if barrier.hook_deadline_live():
        return True
    if _READ_ONLY_FLAGS.intersection(args):
        return True
    words = [a for a in args if not a.startswith("-")]
    return tuple(words[:1]) in _READ_ONLY or tuple(words[:2]) in _READ_ONLY


def _update_barrier(argv: list[str] | None) -> int | None:
    """While the Probe service updates the CLI's env in place (plan X1), wait
    up to 10 s for it, else end here with the busy status: BEFORE the CLI is
    imported, so nothing loads from files being replaced. An update side by
    side or of the plugins only replaces nothing a `probe` runs from, and a
    process pinned to a version env is never replaced: no wait at all, the
    installed version runs (`barrier._blocks`, plan C6). A hook's call or a
    read-only command never waits: busy at once. One stat when no update
    runs. `probe daemon worker` gets the worker's own come-back-later status,
    which its supervisor answers with a later respawn instead of a crash
    count; it also comes back later while the service is stopping the running
    workers before an update (plan D7), so it never starts on the code about
    to be replaced."""
    try:
        from probe.service import barrier
    except Exception:  # noqa: BLE001 -- never a reason not to run `probe`
        return None
    args = sys.argv[1:] if argv is None else argv
    worker = args[:2] == ["daemon", "worker"]
    try:
        if worker and barrier.workers_held():
            print(f"probe: {barrier.MESSAGE}.", file=sys.stderr)
            return barrier.WORKER_BUSY_EXIT_CODE
        if barrier.wait(0.0 if _never_waits(args) else None):
            return None
    except Exception:  # noqa: BLE001 -- never a reason not to run `probe`
        return None
    print(f"probe: {barrier.MESSAGE}.", file=sys.stderr)
    return barrier.WORKER_BUSY_EXIT_CODE if worker else barrier.BUSY_EXIT_CODE


def main(argv: list[str] | None = None) -> int:
    """``probe``."""
    busy = _update_barrier(argv)
    if busy is not None:
        return busy
    try:
        from probe.cli import main as cli_main
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
