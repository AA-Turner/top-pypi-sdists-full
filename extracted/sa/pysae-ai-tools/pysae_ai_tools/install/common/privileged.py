"""Run a command through ``sudo`` without ever hiding its password prompt.

``subprocess.run(["sudo", ...], capture_output=True)`` is a trap: when sudo has
no cached credential it writes ``[sudo] password for <user>:`` to the captured
stream and waits. The user sees a frozen command and no question — the install
hangs forever with no timeout and no clue.

So the decision is made *before* running:

- already root → no sudo needed at all;
- sudo credential cached (``sudo -n true`` succeeds) → no prompt can appear, so
  the output is safe to capture;
- a password will be asked and a terminal is attached → announce it, then run
  **without capturing**, so the prompt reaches the user;
- a password will be asked and there is no terminal (CI, pipe) → fail with that
  as the reason, rather than hanging.
"""

import os
import shutil
import subprocess
from dataclasses import dataclass

import typer

# Long enough for a package install over a slow link, short enough that a
# genuinely stuck command eventually returns instead of hanging the install.
DEFAULT_TIMEOUT = 900


@dataclass
class PrivilegedResult:
    """Outcome of a privileged run. ``output`` is empty when the command ran
    attached to the terminal (nothing was captured — the user saw it live)."""

    returncode: int
    output: str = ""
    error: str = ""

    @property
    def ok(self) -> bool:
        return self.returncode == 0 and not self.error


def is_root() -> bool:
    return hasattr(os, "geteuid") and os.geteuid() == 0


def sudo_available() -> bool:
    return shutil.which("sudo") is not None


def sudo_credential_cached() -> bool:
    """True when sudo can run right now without asking for a password."""
    if not sudo_available():
        return False
    try:
        probe = subprocess.run(
            ["sudo", "-n", "true"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return probe.returncode == 0


def run_privileged(
    args: list[str],
    *,
    what: str,
    timeout: int = DEFAULT_TIMEOUT,
) -> PrivilegedResult:
    """Run ``args`` with root privileges, never hiding a password prompt.

    ``args`` is the command **without** ``sudo`` — this decides whether to add
    it. ``what`` names the operation in the announcement the user sees when a
    password is about to be requested.
    """
    from .checklist import is_interactive

    if is_root():
        return _run_captured(args, timeout=timeout)

    if not sudo_available():
        return PrivilegedResult(returncode=1, error="root privileges required but `sudo` is not installed")

    sudo_args = ["sudo", *args]

    if sudo_credential_cached():
        return _run_captured(sudo_args, timeout=timeout)

    if not is_interactive():
        return PrivilegedResult(
            returncode=1,
            error=(
                f"{what} needs root and sudo would ask for a password, but this run has no terminal — "
                "run it once interactively, or grant passwordless sudo"
            ),
        )

    typer.echo("", err=True)
    typer.secho(f"  🔑 {what} requires root — sudo will ask for your password below.", fg=typer.colors.YELLOW, err=True)
    typer.echo("", err=True)
    return _run_attached(sudo_args, timeout=timeout)


def _run_captured(args: list[str], *, timeout: int) -> PrivilegedResult:
    try:
        proc = subprocess.run(
            args,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
            stdin=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        return PrivilegedResult(returncode=127, error=f"command not found: {args[0]}")
    except subprocess.TimeoutExpired:
        return PrivilegedResult(returncode=124, error=f"timed out after {timeout}s")
    detail = (proc.stderr or "").strip() or (proc.stdout or "").strip()
    return PrivilegedResult(
        returncode=proc.returncode,
        output=(proc.stdout or "").strip(),
        error="" if proc.returncode == 0 else detail,
    )


def _run_attached(args: list[str], *, timeout: int) -> PrivilegedResult:
    """Run with stdio inherited, so the sudo prompt is visible and answerable."""
    try:
        proc = subprocess.run(args, check=False, timeout=timeout)
    except FileNotFoundError:
        return PrivilegedResult(returncode=127, error=f"command not found: {args[0]}")
    except subprocess.TimeoutExpired:
        return PrivilegedResult(returncode=124, error=f"timed out after {timeout}s")
    return PrivilegedResult(
        returncode=proc.returncode,
        error="" if proc.returncode == 0 else f"`{' '.join(args)}` exited {proc.returncode}",
    )
