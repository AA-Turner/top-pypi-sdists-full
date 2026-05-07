"""Shared CLI update helpers for SAGE.

This module centralizes version checks and self-update behavior so the
terminal backend, standard CLI, and REPL all use the same logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version as package_version
from pathlib import Path
import logging
import os
import shutil
import subprocess
import sys
import sysconfig
import tempfile
import threading
import time

from sage import __version__

logger = logging.getLogger("sage.updater")


@dataclass
class CLIVersion:
    """Version information for the installed CLI."""

    current: str
    latest: str
    update_available: bool


@dataclass
class CLIUpdateResult:
    """Outcome of an update check or update attempt."""

    ok: bool
    updated: bool
    attempted: bool
    current: str
    latest: str
    message: str
    scheduled: bool = False


def build_sage_run_command() -> list[str]:
    """Build the most reliable `sage run` invocation for the current env."""

    executable_dir = Path(sys.executable).resolve().parent
    for name in ("sage", "sage.exe"):
        candidate = executable_dir / name
        if candidate.exists():
            return [str(candidate), "run"]

    sage_cmd = shutil.which("sage")
    if sage_cmd:
        return [sage_cmd, "run"]

    return [
        sys.executable,
        "-c",
        "import sys; sys.argv = ['sage', 'run']; from sage.main import app; app()",
    ]


class CLIAutoUpdater:
    """Handles update checks and in-place upgrades for sage-ai-cli."""

    PACKAGE_NAME = "sage-ai-cli"

    def __init__(self) -> None:
        self._cache_timeout = 300
        self._last_check = 0.0
        self._cached_version: CLIVersion | None = None
        self._lock = threading.Lock()

    def get_current_version(self) -> str:
        """Get the installed package version for the active Python env."""

        try:
            return package_version(self.PACKAGE_NAME)
        except PackageNotFoundError:
            return __version__
        except Exception as exc:
            logger.warning("Failed to read installed SAGE version: %s", exc)
            return __version__

    def get_latest_version(self) -> str:
        """Check pip index for the newest published version."""

        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "index",
                    "versions",
                    self.PACKAGE_NAME,
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0 and "(" in result.stdout:
                return result.stdout.split("(", 1)[1].split(")", 1)[0].strip()
        except Exception as exc:
            logger.warning("Failed to check latest SAGE version: %s", exc)
        return self.get_current_version()

    def check_for_update(self, force: bool = False) -> CLIVersion:
        """Return current and latest version information."""

        now = time.time()
        if not force and self._cached_version and (now - self._last_check) < self._cache_timeout:
            return self._cached_version

        current = self.get_current_version()
        latest = self.get_latest_version()
        update_available = self._compare_versions(current, latest) < 0

        # Check git if update not found on pip
        if not update_available:
            root_dir = Path(__file__).resolve().parent.parent.parent.parent
            if (root_dir / ".git").exists():
                try:
                    subprocess.run(
                        ["git", "fetch"],
                        cwd=str(root_dir),
                        capture_output=True,
                        timeout=30,
                    )
                    result = subprocess.run(
                        ["git", "status", "-uno"],
                        cwd=str(root_dir),
                        capture_output=True,
                        text=True,
                        timeout=30,
                    )
                    if "Your branch is behind" in result.stdout:
                        update_available = True
                        latest = f"{current} (git update available)"
                except Exception:
                    pass

        version = CLIVersion(
            current=current,
            latest=latest,
            update_available=update_available,
        )
        self._cached_version = version
        self._last_check = now
        return version

    def apply_update(self) -> bool | str:
        """Upgrade SAGE in the current environment.

        Returns:
            True  - update applied in-process (Linux/macOS, or git pull on any OS).
            "scheduled" - update was scheduled to run after the current process
                          exits. Used on Windows where the running ``sage.exe``
                          is locked by the OS and pip cannot replace it
                          in-place.
            False - update failed.
        """

        with self._lock:
            # 1. Try git update if running from a git clone (cross-platform safe).
            root_dir = Path(__file__).resolve().parent.parent.parent.parent
            if (root_dir / ".git").exists():
                try:
                    logger.info("Detected git repository, attempting git pull...")
                    result = subprocess.run(
                        ["git", "pull"],
                        cwd=str(root_dir),
                        capture_output=True,
                        text=True,
                        timeout=60,
                    )
                    if result.returncode == 0:
                        if "Already up to date" in result.stdout:
                            logger.info("SAGE is already up to date via git.")
                        else:
                            logger.info("Successfully updated SAGE via git pull.")
                        return True
                    logger.warning("git pull failed: %s", result.stderr.strip())
                except Exception as exc:
                    logger.warning("Failed to update via git: %s", exc)

            # 2. Pip-based upgrade. On Windows the running ``sage.exe`` is
            # locked by the OS, so an in-process ``pip install --upgrade``
            # always fails with WinError 32. Spawn a detached helper that
            # runs after this process exits.
            if sys.platform == "win32":
                if self._schedule_windows_pip_upgrade():
                    return "scheduled"
                return False

            # 3. Linux/macOS: in-process pip upgrade is fine — the executable
            # is loaded into memory and replacing the file on disk does not
            # affect the running process.
            try:
                result = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "pip",
                        "install",
                        "--upgrade",
                        "--disable-pip-version-check",
                        self.PACKAGE_NAME,
                    ],
                    capture_output=True,
                    text=True,
                    timeout=300,
                )
                if result.returncode == 0:
                    self._cached_version = None
                    self._last_check = 0
                    logger.info("Successfully updated %s via pip", self.PACKAGE_NAME)
                    return True
                logger.error("SAGE update failed: %s", result.stderr.strip())
            except Exception as exc:
                logger.error("Failed to apply SAGE update: %s", exc)
        return False

    def _schedule_windows_pip_upgrade(self) -> bool:
        """Spawn a detached batch helper that upgrades SAGE after this process exits.

        On Windows the running ``sage.exe`` console script holds an exclusive
        file lock (the OS does not allow replacing a running executable), so
        ``pip install --upgrade`` fails with WinError 32. The helper:

        * Waits for the parent ``sage.exe`` to release the lock.
        * Cleans up any ``~age-ai-cli`` invalid-distribution directories pip
          left behind from a prior failed install (these emit harmless but
          noisy warnings on every pip invocation).
        * Runs ``python -m pip install --upgrade sage-ai-cli``.
        * Pauses so the user can see the result before the window closes.
        """

        try:
            python_exe = sys.executable
            # Site-packages dir for the running interpreter — that's where
            # the leftover ``~age-ai-cli*`` directories live after a failed
            # update.
            site_packages = sysconfig.get_paths().get("purelib") or ""
            parent_pid = os.getpid()
            log_path = Path(tempfile.gettempdir()) / "sage_update.log"

            # Build the batch script. We use Python's pathlib for the path
            # but write it as a literal Windows path inside the .bat.
            bat_lines = [
                "@echo off",
                "setlocal enableextensions",
                "title SAGE AI Updater",
                "echo.",
                "echo SAGE AI updater - waiting for the previous sage process to exit...",
                "echo.",
                # Wait for the parent sage.exe (PID %parent_pid%) to exit so
                # the executable is no longer locked. ``tasklist`` is a built-in
                # Windows command that ships with every supported version.
                f'set "SAGE_PARENT_PID={parent_pid}"',
                ":wait_loop",
                'tasklist /FI "PID eq %SAGE_PARENT_PID%" 2>nul | find "%SAGE_PARENT_PID%" >nul',
                "if not errorlevel 1 (",
                "  timeout /t 1 /nobreak >nul",
                "  goto wait_loop",
                ")",
                "",
                "echo Cleaning up leftover invalid distributions...",
            ]

            # Best-effort cleanup of any leftover ``~age-ai-cli*`` directories
            # pip didn't finish removing during the previous failed install.
            if site_packages:
                bat_lines.extend(
                    [
                        f'pushd "{site_packages}" 2>nul',
                        "if not errorlevel 1 (",
                        '  for /d %%D in ("~age-ai-cli*") do rmdir /s /q "%%D" 2>nul',
                        '  for /d %%D in ("~age_ai_cli*") do rmdir /s /q "%%D" 2>nul',
                        "  popd",
                        ")",
                    ]
                )

            bat_lines.extend(
                [
                    "",
                    "echo Upgrading SAGE AI...",
                    "echo.",
                    # --force-reinstall + --no-cache-dir: idempotent, safe when
                    # a previous run aborted mid-install and left the package
                    # half-removed (sage.exe present but `import sage` broken).
                    # Without this, pip's "already up to date" short-circuit
                    # would skip the install and leave the user permanently
                    # broken — they had to know to manually pass --force.
                    f'"{python_exe}" -m pip install --force-reinstall --no-cache-dir '
                    f"--disable-pip-version-check {self.PACKAGE_NAME}",
                    "set RC=%ERRORLEVEL%",
                    "echo.",
                    "if %RC%==0 (",
                    # Verify by importing the package, not just running
                    # sage --version (the wrapper script can succeed even
                    # when the package is half-installed in some edge cases).
                    f'  "{python_exe}" -c "import sage; print(\'SAGE AI\', sage.__version__, \'installed.\')"',
                    "  set VRC=%ERRORLEVEL%",
                    "  if not %VRC%==0 (",
                    "    echo.",
                    "    echo WARNING: pip reported success but `import sage` failed.",
                    "    echo Recover with:",
                    f'    echo   "{python_exe}" -m pip install --force-reinstall --no-cache-dir {self.PACKAGE_NAME}',
                    "  )",
                    ") else (",
                    "  echo SAGE AI update FAILED with exit code %RC%.",
                    "  echo Recover by running this command yourself:",
                    f'  echo   "{python_exe}" -m pip install --force-reinstall --no-cache-dir {self.PACKAGE_NAME}',
                    "  echo If sage.exe was still locked, close every sage window first.",
                    ")",
                    "echo.",
                    "echo You can close this window.",
                    "pause",
                    "exit /b %RC%",
                ]
            )

            bat_path = Path(tempfile.gettempdir()) / f"sage_update_{parent_pid}.bat"
            bat_path.write_text("\r\n".join(bat_lines), encoding="utf-8")

            # Spawn the helper in a new console window, fully detached so the
            # parent sage.exe can exit without killing it.
            DETACHED_PROCESS = 0x00000008
            CREATE_NEW_CONSOLE = 0x00000010
            CREATE_NEW_PROCESS_GROUP = 0x00000200
            CREATE_BREAKAWAY_FROM_JOB = 0x01000000

            flags = (
                CREATE_NEW_CONSOLE
                | CREATE_NEW_PROCESS_GROUP
                | CREATE_BREAKAWAY_FROM_JOB
                | DETACHED_PROCESS
            )
            try:
                subprocess.Popen(
                    ["cmd.exe", "/c", str(bat_path)],
                    creationflags=flags,
                    close_fds=True,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except OSError:
                # CREATE_BREAKAWAY_FROM_JOB fails when the parent process is
                # already in a job that disallows breakaway (e.g. some CI
                # runners). Retry without that flag.
                fallback_flags = CREATE_NEW_CONSOLE | CREATE_NEW_PROCESS_GROUP
                subprocess.Popen(
                    ["cmd.exe", "/c", str(bat_path)],
                    creationflags=fallback_flags,
                    close_fds=True,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )

            logger.info(
                "Scheduled SAGE update via detached helper at %s (log: %s)",
                bat_path,
                log_path,
            )
            return True
        except Exception as exc:
            logger.error("Failed to schedule Windows SAGE update: %s", exc)
            return False

    def ensure_latest(self) -> CLIUpdateResult:
        """Check for updates and apply them when available."""

        version = self.check_for_update()
        if not version.update_available:
            return CLIUpdateResult(
                ok=True,
                updated=False,
                attempted=False,
                current=version.current,
                latest=version.latest,
                message=f"SAGE AI is already up to date (v{version.current}).",
            )

        outcome = self.apply_update()

        if outcome == "scheduled":
            return CLIUpdateResult(
                ok=True,
                updated=False,
                attempted=True,
                scheduled=True,
                current=version.current,
                latest=version.latest,
                message=(
                    f"SAGE AI update scheduled (v{version.current} -> v{version.latest}). "
                    "A new window has opened to finish the upgrade after this "
                    "process exits — close any other running sage windows. "
                    "Run `sage --version` once it completes to confirm the upgrade."
                ),
            )

        success = bool(outcome)
        refreshed = self.check_for_update(force=True)
        if success:
            if "git update available" in version.latest:
                return CLIUpdateResult(
                    ok=True,
                    updated=True,
                    attempted=True,
                    current=refreshed.current,
                    latest=refreshed.latest,
                    message=f"Updated SAGE AI via git pull (v{version.current}).",
                )

            if self._compare_versions(refreshed.current, version.current) > 0:
                return CLIUpdateResult(
                    ok=True,
                    updated=True,
                    attempted=True,
                    current=refreshed.current,
                    latest=refreshed.latest,
                    message=(
                        f"Updated SAGE AI from v{version.current} to v{refreshed.current}."
                    ),
                )

            if not refreshed.update_available:
                return CLIUpdateResult(
                    ok=True,
                    updated=False,
                    attempted=True,
                    current=refreshed.current,
                    latest=refreshed.latest,
                    message=f"SAGE AI is already up to date (v{refreshed.current}).",
                )

            return CLIUpdateResult(
                ok=False,
                updated=False,
                attempted=True,
                current=refreshed.current,
                latest=refreshed.latest,
                message=(
                    "SAGE AI update completed, but the installed version did not change. "
                    f"Current version is still v{refreshed.current}."
                ),
            )

        return CLIUpdateResult(
            ok=False,
            updated=False,
            attempted=True,
            current=refreshed.current,
            latest=version.latest,
            message=(
                f"Failed to update SAGE AI from v{version.current} to v{version.latest}."
            ),
        )

    @staticmethod
    def _compare_versions(v1: str, v2: str) -> int:
        """Compare two version strings."""

        def parse(version: str) -> tuple[int, ...]:
            parts: list[int] = []
            for part in version.replace("-", ".").split("."):
                try:
                    parts.append(int(part))
                except ValueError:
                    parts.append(0)
            return tuple(parts)

        p1, p2 = parse(v1), parse(v2)
        if p1 < p2:
            return -1
        if p1 > p2:
            return 1
        return 0
