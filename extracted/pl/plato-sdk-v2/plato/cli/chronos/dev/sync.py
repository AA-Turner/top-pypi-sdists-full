"""Sync utilities for hot reload in dev mode."""

from __future__ import annotations

import asyncio
import logging
import subprocess
import time
from collections.abc import Callable
from pathlib import Path
from time import perf_counter

from pydantic import BaseModel, Field

from plato.cli.chronos.dev.ssh import build_ssh_command_string, ensure_master_connection

logger = logging.getLogger(__name__)


def parse_gitignore(gitignore_path: Path) -> list[str]:
    """Parse .gitignore file and return list of patterns for rsync --exclude.

    Args:
        gitignore_path: Path to .gitignore file

    Returns:
        List of exclude patterns (always includes .git)
    """
    patterns = [
        ".git",
        "__pycache__",
        "*.pyc",
        ".venv",
        "node_modules",
        ".mypy_cache",
        ".pytest_cache",
        "dist",
        ".next",
        "plato-fuse/target",
        "*.log",
    ]

    if not gitignore_path.exists():
        return patterns

    with open(gitignore_path) as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue
            # Skip negation patterns (rsync doesn't support them the same way)
            if line.startswith("!"):
                continue
            patterns.append(line)

    return patterns


def check_fswatch() -> bool:
    """Check if fswatch is installed."""
    try:
        subprocess.run(["fswatch", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def _glob_to_regex(pattern: str) -> str:
    """Convert a gitignore-style glob pattern to a regex for fswatch -e.

    Args:
        pattern: A gitignore glob pattern (e.g. '*.pyc', '.git', 'node_modules')

    Returns:
        A POSIX extended regex string suitable for fswatch -e
    """
    # Strip trailing slashes (directory markers in gitignore)
    pattern = pattern.rstrip("/")

    # Only escape chars that are special in POSIX extended regex.
    # Do NOT use re.escape — it escapes chars like '-' that POSIX ERE
    # doesn't recognise as escape sequences, causing fswatch to error.
    _POSIX_ERE_SPECIAL = set(r"\.^$+{}()|[]")
    result = []
    i = 0
    while i < len(pattern):
        c = pattern[i]
        if c == "*":
            # Check for **
            if i + 1 < len(pattern) and pattern[i + 1] == "*":
                result.append(".*")
                i += 2
                continue
            result.append("[^/]*")
        elif c == "?":
            result.append("[^/]")
        elif c in _POSIX_ERE_SPECIAL:
            result.append(f"\\{c}")
        else:
            result.append(c)
        i += 1
    return "".join(result)


class SyncTarget(BaseModel):
    """A local->remote sync target."""

    local_path: Path
    remote_path: str
    job_id: str
    excludes: list[str] = Field(default_factory=list)


class SyncManager:
    """Manages rsync and fswatch for hot reload.

    Syncs local directories to VMs and watches for changes.

    Example:
        sync = SyncManager(ssh_key_path)
        sync.add_target(Path("./world"), "/world", "job-123")
        sync.add_target(Path("./agent"), "/agents/coder", "job-123")

        await sync.initial_sync()  # Sync all once
        await sync.watch()  # Watch and sync on changes
    """

    def __init__(self, ssh_key_path: Path, verbose: bool = False):
        """Initialize the sync manager.

        Args:
            ssh_key_path: Path to SSH private key for VM access
            verbose: Print sync status messages
        """
        self.ssh_key_path = ssh_key_path
        self.verbose = verbose
        self.targets: list[SyncTarget] = []
        self._fswatch_proc: subprocess.Popen | None = None
        self._watch_task: asyncio.Task | None = None
        self._running = False

    def add_target(
        self,
        local_path: Path,
        remote_path: str,
        job_id: str,
        excludes: list[str] | None = None,
    ) -> None:
        """Add a sync target.

        Args:
            local_path: Local directory to sync
            remote_path: Remote path on VM
            job_id: VM job ID
            excludes: Additional exclude patterns (gitignore is auto-parsed)
        """
        # Parse gitignore from local path
        gitignore_excludes = parse_gitignore(local_path / ".gitignore")

        # Combine with additional excludes
        all_excludes = gitignore_excludes + (excludes or [])

        self.targets.append(
            SyncTarget(
                local_path=local_path.resolve(),
                remote_path=remote_path,
                job_id=job_id,
                excludes=all_excludes,
            )
        )

    def _build_rsync_cmd(self, target: SyncTarget) -> list[str]:
        """Build rsync command for a target."""
        ssh_cmd = build_ssh_command_string(target.job_id, self.ssh_key_path)

        # Use --rsync-path to create parent directories on remote before sync
        mkdir_cmd = f"mkdir -p {target.remote_path} && rsync"

        cmd = ["rsync", "-az", "--delete", "--stats", "--rsync-path", mkdir_cmd]

        for pattern in target.excludes:
            cmd.extend(["--exclude", pattern])

        cmd.extend(
            [
                "-e",
                ssh_cmd,
                f"{target.local_path}/",
                f"root@{target.job_id}.plato:{target.remote_path}/",
            ]
        )

        return cmd

    @staticmethod
    def _format_bytes(raw: str) -> str:
        """Convert a raw byte string (e.g. '7314070') to human-readable MB/KB."""
        try:
            n = int(raw.strip().split()[0])
        except (ValueError, IndexError):
            return raw
        if n >= 1_000_000:
            return f"{n / 1_048_576:.1f} MB"
        if n >= 1_000:
            return f"{n / 1_024:.1f} KB"
        return f"{n} B"

    @staticmethod
    def _parse_rsync_stats(output: str) -> str:
        """Extract a one-line summary from rsync --stats output."""
        files_transferred = ""
        total_size_raw = ""
        bytes_sent_raw = ""
        for line in output.splitlines():
            line = line.strip()
            # Linux rsync uses "regular files transferred", macOS uses "files transferred"
            if "files transferred:" in line and "regular" not in line.split("transferred")[0]:
                files_transferred = line.split(":", 1)[1].strip()
            elif line.startswith("Number of regular files transferred:"):
                files_transferred = line.split(":", 1)[1].strip()
            elif line.startswith("Total transferred file size:"):
                total_size_raw = line.split(":", 1)[1].strip()
            elif line.startswith("Total bytes sent:"):
                bytes_sent_raw = line.split(":", 1)[1].strip()
        parts: list[str] = []
        if files_transferred:
            parts.append(f"{files_transferred} files")
        if total_size_raw:
            parts.append(SyncManager._format_bytes(total_size_raw))
        if bytes_sent_raw:
            parts.append(f"sent {SyncManager._format_bytes(bytes_sent_raw)}")
        return ", ".join(parts)

    def _sync_target(self, target: SyncTarget, max_retries: int = 3, retry_delay: float = 5.0) -> tuple[bool, str]:
        """Sync a single target with retries. Returns (success, stats_summary)."""
        cmd = self._build_rsync_cmd(target)
        last_error = ""
        for attempt in range(1, max_retries + 1):
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=300,
                )
                if result.returncode == 0:
                    stats = self._parse_rsync_stats(result.stdout)
                    return True, stats
                last_error = result.stderr
            except subprocess.TimeoutExpired:
                last_error = "timed out"
            except Exception as e:
                last_error = str(e)

            if attempt < max_retries:
                logger.warning(
                    "Rsync failed for %s (attempt %d/%d), retrying in %.0fs: %s",
                    target.local_path,
                    attempt,
                    max_retries,
                    retry_delay,
                    last_error.strip(),
                )
                time.sleep(retry_delay)

        logger.warning(f"Rsync failed for {target.local_path} after {max_retries} attempts: {last_error}")
        return False, ""

    async def initial_sync(self, on_synced: Callable[[SyncTarget, float], None] | None = None) -> int:
        """Sync all targets in parallel.

        Args:
            on_synced: Optional callback invoked after each target finishes syncing,
                with (target, elapsed_seconds).

        Returns:
            Number of successful syncs
        """
        loop = asyncio.get_event_loop()
        logger.info(
            "Syncing %d target(s): %s",
            len(self.targets),
            ", ".join(f"{t.local_path.name} -> {t.remote_path}" for t in self.targets),
        )

        # Pre-establish SSH master so parallel rsyncs multiplex over it
        if self.targets:
            target = self.targets[0]
            await loop.run_in_executor(None, ensure_master_connection, target.job_id, self.ssh_key_path)

        async def _sync_one(target: SyncTarget) -> bool:
            logger.info(
                "Syncing %s -> %s (%d excludes)",
                target.local_path,
                target.remote_path,
                len(target.excludes),
            )
            started = perf_counter()
            success, stats = await loop.run_in_executor(None, self._sync_target, target)
            elapsed = perf_counter() - started
            if success:
                stats_msg = f" ({stats})" if stats else ""
                logger.info(
                    "Synced %s -> %s in %.1fs%s",
                    target.local_path.name,
                    target.remote_path,
                    elapsed,
                    stats_msg,
                )
            else:
                logger.warning(f"Failed to sync {target.local_path.name} after {elapsed:.1f}s")
            if on_synced:
                on_synced(target, elapsed)
            return success

        results = await asyncio.gather(*[_sync_one(t) for t in self.targets])
        return sum(results)

    async def watch(self) -> None:
        """Watch for changes and sync continuously.

        Runs until stopped or cancelled.
        """
        if not check_fswatch():
            logger.warning("fswatch not installed, hot reload disabled")
            logger.info("Install: brew install fswatch (macOS) or apt install fswatch (Linux)")
            return

        self._running = True

        # Build fswatch command
        fswatch_cmd = ["fswatch", "-o", "--latency", "0.5", "-r"]

        # Add exclude patterns from all targets
        all_excludes: set[str] = set()
        for target in self.targets:
            all_excludes.update(target.excludes)
        for pattern in sorted(all_excludes):
            fswatch_cmd.extend(["-e", _glob_to_regex(pattern)])

        # Add all local paths to watch
        for target in self.targets:
            fswatch_cmd.append(str(target.local_path))

        logger.debug(f"Watching {len(self.targets)} path(s) for changes...")

        self._fswatch_proc = subprocess.Popen(
            fswatch_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        loop = asyncio.get_event_loop()

        try:
            while self._running:
                if not self._fswatch_proc or not self._fswatch_proc.stdout:
                    break
                # Wait for fswatch to report a change
                line = await loop.run_in_executor(None, self._fswatch_proc.stdout.readline)
                if not line:
                    stderr_output = ""
                    if self._fswatch_proc and self._fswatch_proc.stderr:
                        stderr_output = self._fswatch_proc.stderr.read().decode(errors="replace").strip()
                    if stderr_output:
                        logger.warning(f"fswatch exited with error: {stderr_output}")
                    else:
                        logger.warning("fswatch process exited, stopping file watcher")
                    break

                # Sync all targets (initial_sync already logs the count)
                await self.initial_sync()

        except asyncio.CancelledError:
            pass
        finally:
            self.stop()

    def stop(self) -> None:
        """Stop watching for changes."""
        self._running = False
        if self._fswatch_proc:
            self._fswatch_proc.terminate()
            try:
                self._fswatch_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._fswatch_proc.kill()
            self._fswatch_proc = None
