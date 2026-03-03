"""Sync utilities for hot reload in dev mode."""

from __future__ import annotations

import asyncio
import logging
import subprocess
from collections.abc import Callable
from pathlib import Path
from time import perf_counter

from pydantic import BaseModel, Field

from plato.cli.chronos.dev.ssh import build_ssh_command_string

logger = logging.getLogger(__name__)


def parse_gitignore(gitignore_path: Path) -> list[str]:
    """Parse .gitignore file and return list of patterns for rsync --exclude.

    Args:
        gitignore_path: Path to .gitignore file

    Returns:
        List of exclude patterns (always includes .git)
    """
    patterns = [".git", "__pycache__", "*.pyc", ".venv", "node_modules", ".mypy_cache", ".pytest_cache"]

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

        cmd = ["rsync", "-az", "--delete", "--rsync-path", mkdir_cmd]

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

    def _sync_target(self, target: SyncTarget) -> bool:
        """Sync a single target. Returns True on success."""
        try:
            cmd = self._build_rsync_cmd(target)
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
            )
            if result.returncode != 0:
                logger.warning(f"Rsync failed for {target.local_path}: {result.stderr}")
                return False
            return True
        except subprocess.TimeoutExpired:
            logger.warning(f"Rsync timed out for {target.local_path}")
            return False
        except Exception as e:
            logger.warning(f"Rsync error for {target.local_path}: {e}")
            return False

    async def initial_sync(self, on_synced: Callable[[SyncTarget, float], None] | None = None) -> int:
        """Sync all targets in parallel.

        Args:
            on_synced: Optional callback invoked after each target finishes syncing,
                with (target, elapsed_seconds).

        Returns:
            Number of successful syncs
        """
        loop = asyncio.get_event_loop()

        async def _sync_one(target: SyncTarget) -> bool:
            logger.debug(f"Syncing {target.local_path} -> {target.remote_path}")
            started = perf_counter()
            success = await loop.run_in_executor(None, self._sync_target, target)
            elapsed = perf_counter() - started
            if not success:
                logger.warning(f"Failed to sync {target.local_path.name}")
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
