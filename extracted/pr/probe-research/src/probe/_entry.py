"""Console-script entry points that survive a missing optional dependency.

``probe`` is a stdlib-only shim (service-only T7): it hands the command to the Probe service,
which runs it in a child of its warm CLI host with this terminal (`probe.foundation.cli_shim`;
the in-child entry is `probe.service.commands.child`). ``probe-research-mcp`` needs ``mcp``,
``anyio`` and ``tiktoken``. Plan 2.11 moved them into the ``cli`` and ``mcp`` extras (``all`` =
both) so a training environment can install the SDK alone: an install without them prints what
is missing and the one command that fixes it, and exits 1. Imports nothing heavy at module level.
"""

from __future__ import annotations

import sys

#: Which top-level modules each entry point needs, and the extra that brings them.
CLI_MODULES = ("typer", "questionary", "click")
_MCP_MODULES = ("mcp", "anyio", "tiktoken", "starlette")


def find_missing_dependency(exc: ModuleNotFoundError, modules: tuple[str, ...]) -> str | None:
    """The missing module's name when it is one of ``modules``, else None (a
    real bug, which must keep its traceback)."""
    name = (exc.name or "").split(".")[0]
    return name if name in modules else None


def explain_missing_extra(tool: str, extra: str, module: str) -> int:
    print(
        f"{tool}: this install of probe-research has the Python SDK but not the "
        f"`{extra}` dependencies (missing: {module}).\n"
        f"  Install them:  pip install 'probe-research[all]'\n"
        f"  (a uv tool install:  uv tool install 'probe-research[all]', or "
        f"'probe-research[all,daemon]' where the Probe daemon records)",
        file=sys.stderr,
    )
    return 1


#: The private package the CLI, daemon and service ship in (agent/packaging/private).
CLI_DIST = "probe-research-cli"


def is_cli_missing() -> bool:
    """`probe.cli` is not installed (probe-research without its `cli` extra), or only an empty
    folder is left of it (files a Python wrote under `probe/cli/` outlive an uninstall)."""
    from importlib.util import find_spec

    try:
        spec = find_spec("probe.cli")
    except (ImportError, ValueError):
        return True
    return spec is None or spec.origin is None


def explain_no_cli() -> int:
    print(
        "probe: this install of probe-research has the Python SDK but not the CLI "
        f"(the {CLI_DIST} package).\n"
        "  Install it:  pip install 'probe-research[all]'\n"
        "  (a uv tool install:  uv tool install 'probe-research[all]', or "
        "'probe-research[all,daemon]' where the Probe daemon records)",
        file=sys.stderr,
    )
    return 1


def find_version_mismatch() -> tuple[str, str] | None:
    """(CLI, SDK) versions when the folder `probe` loads from holds the two wheels at different
    releases, else None (a source or editable tree holds neither). Upgrading one with pip only warns,
    and the CLI then reads SDK fields that moved (`DrainReport.superseded`: a 0.545 CLI on a 0.550 SDK, 11-13)."""
    import os

    import probe
    from probe.foundation.version.version import read_installed_version

    site = [os.path.dirname(os.path.dirname(os.path.abspath(probe.__file__)))]  # `probe.cli` loads from here too
    cli, sdk = read_installed_version(CLI_DIST, site), read_installed_version(paths=site)
    return (cli, sdk) if cli and sdk and cli != sdk else None


def explain_version_mismatch(cli: str, sdk: str) -> int:
    print(
        f"probe: the CLI ({CLI_DIST} {cli}) and the Python SDK (probe-research {sdk}) are different "
        "releases, and the CLI runs only on the SDK release it was built with.\n"
        f"  Match them:  pip install '{CLI_DIST}=={sdk}'\n"
        "  (a uv tool install:  uv tool install 'probe-research[all]')",
        file=sys.stderr,
    )
    return 1


def main(argv: list[str] | None = None) -> int:
    """``probe``: the command runs in the Probe service; this process passes its terminal and waits."""
    if is_cli_missing():
        return explain_no_cli()
    mismatch = find_version_mismatch()
    if mismatch:
        return explain_version_mismatch(*mismatch)
    from probe import __version__
    from probe.foundation.cli_shim import run_command

    return run_command(sys.argv[1:] if argv is None else list(argv), __version__)


def mcp_main() -> None:
    """``probe-research-mcp``."""
    try:
        from probe.mcp.server.server import main as server_main
    except ModuleNotFoundError as exc:
        module = find_missing_dependency(exc, _MCP_MODULES)
        if module is None:
            raise
        raise SystemExit(explain_missing_extra("probe-research-mcp", "mcp", module)) from None
    server_main()


def mcp_http_main() -> None:
    """``probe-research-mcp-http``."""
    try:
        from probe.mcp.server.http import main_http
    except ModuleNotFoundError as exc:
        module = find_missing_dependency(exc, _MCP_MODULES + ("uvicorn",))
        if module is None:
            raise
        raise SystemExit(explain_missing_extra("probe-research-mcp-http", "mcp", module)) from None
    main_http()
