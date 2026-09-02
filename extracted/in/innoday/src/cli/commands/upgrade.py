"""
InnoDay CLI ``upgrade`` command.

``innoday upgrade [VERSION] [--refresh] [--dry-run]`` self-reinstalls the CLI
from PyPI and, optionally, re-onboards the current project workspace.

Why a dedicated command (and why ``--reinstall`` is mandatory): ``uv tool
upgrade innoday`` alone can pin to a stale, higher-numbered release under real
PEP 440 ordering (see ``docs/VERSION_MANAGEMENT.md`` "Reset history" and the
CLAUDE.md "stale MCP server" note). ``uv tool install innoday --reinstall``
bypasses uv's version comparison and forces the exact requested (or latest)
release, which is the only reliable way to actually move the installed binary.

The reinstall shells out **synchronously** via :func:`subprocess.run` even
though :meth:`UpgradeCommands.execute` is ``async`` (async only for signature
consistency with the other command groups). PyPI's "latest" is fetched
synchronously with ``requests`` following the exact pattern in
``scripts/verify_pypi_latest.py``; a PyPI failure degrades gracefully (skip the
"already latest?" optimization, still reinstall) rather than aborting.
"""

import argparse
import re
import subprocess
from typing import List, Optional

import requests
from packaging.version import InvalidVersion, Version
from rich.console import Console

from src.cli.commands.workspace import WorkspaceCommands
from src.cli.utils.formatters import (
    format_error,
    format_info,
    format_success,
    format_warning,
)
from src.cli.utils.project_context import find_project_yml
from src.version import get_version

console = Console()

# Same endpoint scripts/verify_pypi_latest.py uses.
_PYPI_JSON_URL = "https://pypi.org/pypi/innoday/json"
# uv install can take a while on a cold cache / slow network; cap it so a hung
# subprocess can't wedge the command indefinitely.
_REINSTALL_TIMEOUT_SECONDS = 300


def _fetch_pypi_latest() -> Optional[str]:
    """Return the ``info.version`` PyPI reports for ``innoday``, or ``None``.

    Copies ``scripts/verify_pypi_latest.py``'s pattern: a transient network/HTTP
    error returns ``None`` (never raises) so a PyPI hiccup can't abort the
    upgrade -- the caller just skips the "already on latest?" optimization and
    reinstalls anyway. Factored out as a module-level helper so tests can patch
    it directly.
    """
    try:
        response = requests.get(_PYPI_JSON_URL, timeout=10)
        response.raise_for_status()
        return response.json()["info"]["version"]
    except requests.exceptions.RequestException:
        return None


def _versions_equal(installed: str, latest: str) -> bool:
    """True if ``installed`` and ``latest`` are the same PEP 440 release.

    Compares parsed :class:`packaging.version.Version` objects, NOT strings:
    this repo spells its own version ``0.1.0-beta`` while PyPI reports the
    normalized ``0.1.0b0`` -- the same release, which ``Version`` parses
    identically but a string compare would wrongly flag as different. A
    malformed version on either side is treated as "not equal" so the command
    falls through to a reinstall rather than crashing.
    """
    try:
        return Version(installed) == Version(latest)
    except InvalidVersion:
        return False


class UpgradeCommands:
    """``innoday upgrade`` -- self-reinstall + optional project refresh."""

    @staticmethod
    def setup_parser(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "version",
            nargs="?",
            default=None,
            metavar="VERSION",
            help="Specific version to install (e.g. 0.1.5-beta). "
            "Omit to install the latest release from PyPI.",
        )
        parser.add_argument(
            "--refresh",
            action="store_true",
            help="After a successful reinstall, re-onboard the current project "
            "workspace (pull repos, rewrite .innoday/project.yml) if you're "
            "inside one.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Print the exact command(s) that would run (and whether a "
            "refresh would follow) without executing anything.",
        )

    @staticmethod
    async def execute(args: argparse.Namespace, config) -> int:
        requested_version: Optional[str] = getattr(args, "version", None)
        refresh: bool = getattr(args, "refresh", False)
        dry_run: bool = getattr(args, "dry_run", False)

        cmd = _build_reinstall_command(requested_version)

        # --dry-run must be side-effect-free: short-circuit BEFORE any network
        # call (_fetch_pypi_latest) and before the already-latest check so the
        # user always sees the plan they asked to preview -- even when they're
        # already on latest. get_version() is local/free, so it's fine to show.
        if dry_run:
            console.print(format_info(f"Installed version: {get_version()}"))
            console.print(format_info(f"[dry run] Would run: {' '.join(cmd)}"))
            if refresh:
                console.print(
                    format_info(
                        "[dry run] Would then refresh the current project "
                        "workspace (if inside one)."
                    )
                )
            return 0

        # Capture the currently-installed version BEFORE reinstalling so the
        # "was X, now reinstalled" reporting reflects the pre-upgrade state.
        installed = get_version()
        latest = _fetch_pypi_latest()

        console.print(format_info(f"Installed version: {installed}"))
        if latest is not None:
            console.print(format_info(f"PyPI latest: {latest}"))
        else:
            console.print(
                format_warning(
                    "Could not resolve latest version from PyPI "
                    "(continuing with reinstall)."
                )
            )

        # Skip the reinstall only when we can prove we're already on latest AND
        # the caller didn't ask for a specific version. An explicit VERSION
        # always reinstalls (e.g. deliberately pinning/downgrading).
        if (
            requested_version is None
            and latest is not None
            and _versions_equal(installed, latest)
        ):
            console.print(
                format_success(
                    f"Already on the latest version ({installed}); skipping reinstall."
                )
            )
            # The binary didn't change, but --refresh does independently useful
            # work (git pull each repo + rewrite .innoday/project.yml), so still
            # run it when asked -- it doesn't depend on a fresh reinstall.
            if refresh:
                return await UpgradeCommands._maybe_refresh(args, config)
            return 0

        reinstall_result = _run_reinstall(cmd)
        if reinstall_result != 0:
            return reinstall_result

        landed = installed_version_from_uv(_LAST_INSTALL.get("output", ""))
        expected = requested_version or latest
        if landed is None:
            # uv's summary did not name a version. Not a failure -- its output
            # format is not a contract, and warning on a working upgrade every
            # time that format shifts is worse than saying nothing.
            console.print(format_success("Reinstall complete."))
        elif expected is not None and not _versions_equal(landed, expected):
            # **The reason this check exists.** "Reinstall complete" was printed
            # unconditionally, so a reinstall that landed on the version already
            # present -- uv resolving from a stale index -- reported success
            # while changing nothing, and the next bug report was about a fix
            # that "did not ship".
            console.print(
                format_warning(
                    f"Reinstalled {landed}, but {expected} was expected. "
                    "uv may have resolved from a cached index; re-run "
                    "`innoday upgrade` or `uv tool install innoday "
                    "--reinstall --refresh`."
                )
            )
        else:
            console.print(format_success(f"Reinstall complete — now on {landed}."))

        # Stamp the version we just installed, not the one running.
        #
        # This process IS the old binary -- it is replacing itself -- so
        # save()'s automatic stamp would record the version being retired and
        # leave the config permanently one release behind after every upgrade.
        # The version uv was told to install is the right value -- an explicit
        # VERSION argument when given, otherwise PyPI's latest. A failure here
        # must not fail the upgrade: the binary is already
        # in place, and the next config write corrects the stamp anyway.
        installed_now = requested_version or latest
        if installed_now:
            try:
                config.set_written_by_version(installed_now)
            except Exception as e:  # noqa: BLE001
                console.print(
                    format_info(f"Could not record the config version stamp: {e}")
                )

        if refresh:
            return await UpgradeCommands._maybe_refresh(args, config)

        return 0

    @staticmethod
    async def _maybe_refresh(args: argparse.Namespace, config) -> int:
        """Re-onboard the current workspace after a successful reinstall.

        Only runs when inside a project workspace. ``execute_refresh`` reads
        ``args.no_clone``/``args.no_hooks``, which the upgrade parser doesn't
        define -- inject safe defaults before delegating.
        """
        if find_project_yml() is None:
            console.print(
                format_warning(
                    "--refresh requested but not inside a project workspace "
                    "(no .innoday/project.yml found); skipping refresh."
                )
            )
            return 0

        if not hasattr(args, "no_clone"):
            args.no_clone = False
        if not hasattr(args, "no_hooks"):
            args.no_hooks = False

        return await WorkspaceCommands.execute_refresh(args, config)


def _build_reinstall_command(requested_version: Optional[str]) -> List[str]:
    """Build the ``uv tool install ... --reinstall --refresh`` argv.

    ``--reinstall`` is mandatory: uv's own version comparison can otherwise pin
    to a stale, higher-numbered release, so a plain ``uv tool upgrade`` may not
    actually move the binary.

    **uv's own ``--refresh`` is what makes ``--reinstall`` mean anything** (not
    to be confused with this command's ``--refresh``, which re-onboards the
    workspace and never reaches uv). ``--reinstall``
    rebuilds the environment; it does not re-ask PyPI what exists. uv answers
    that from its cached index, so a release published minutes ago is invisible
    and the command cheerfully reinstalls the version already present. Measured
    2026-08-27: ``0.1.326b0`` had been on PyPI for some minutes, ``innoday
    upgrade`` printed "Reinstall complete", and the binary was still
    ``0.1.325b0``.
    """
    target = f"innoday=={requested_version}" if requested_version else "innoday"
    return ["uv", "tool", "install", target, "--reinstall", "--refresh"]


#: `~ innoday==0.1.326b0` / `+ innoday==0.1.326b0` in uv's install summary --
#: the only statement of what was actually installed. `get_version()` cannot
#: answer it: this process *is* the binary being replaced, so it reports the
#: version on its way out.
_INSTALLED_VERSION = re.compile(r"^\s*[+~]\s*innoday==(\S+)\s*$", re.MULTILINE)


def installed_version_from_uv(output: str) -> Optional[str]:
    """What uv says it installed, or `None` if its summary did not say.

    `None` is "could not tell", never "failed" -- uv's output format is not a
    contract, and a parser that guessed would turn a working upgrade into a
    warning the next time that format changed.
    """
    match = _INSTALLED_VERSION.search(output or "")
    return match.group(1) if match else None


def _run_reinstall(cmd: List[str]) -> int:
    """Run the reinstall subprocess synchronously; 0 on success, 1 on failure.

    Handles the three ways this can go wrong distinctly: uv missing from PATH
    (``FileNotFoundError``), a hung install (``TimeoutExpired``), and a non-zero
    exit (surface stderr). None of these raise out of this function -- callers
    get a clean return code.
    """
    console.print(format_info(f"Running: {' '.join(cmd)}"))
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=_REINSTALL_TIMEOUT_SECONDS,
        )
    except FileNotFoundError:
        console.print(
            format_error(
                "`uv` was not found on PATH. Install uv "
                "(https://docs.astral.sh/uv/) and try again."
            )
        )
        return 1
    except subprocess.TimeoutExpired:
        console.print(
            format_error(f"Reinstall timed out after {_REINSTALL_TIMEOUT_SECONDS}s.")
        )
        return 1

    if result.returncode != 0:
        console.print(format_error("Reinstall failed."))
        stderr = (result.stderr or "").strip()
        if stderr:
            console.print(f"[dim]{stderr}[/dim]")
        return 1

    # uv writes its install summary to stderr.
    _LAST_INSTALL["output"] = f"{result.stdout or ''}\n{result.stderr or ''}"
    return 0


#: Where `_run_reinstall` leaves uv's output for the caller to check what landed.
#: A module-level slot rather than a return value because `_run_reinstall`'s
#: contract is an exit code that three call sites already branch on.
_LAST_INSTALL: dict = {"output": ""}
