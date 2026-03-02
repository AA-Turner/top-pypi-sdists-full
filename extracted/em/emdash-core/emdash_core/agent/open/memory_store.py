"""MemoryStore — Safe filesystem layer for the OpenClaw-style memory system.

Markdown files on disk are the source of truth. This module provides safe,
validated filesystem operations for reading and writing memory files.

Allowed paths:
- MEMORY.md (long-term curated memory)
- memory/*.md (daily logs)
"""

import logging
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Pattern for valid daily log filenames
_DAILY_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")


class MemoryStore:
    """Safe filesystem operations for the memory system.

    All memory is stored as markdown files on disk:
    - ``<workspace>/MEMORY.md`` — long-term curated memory
    - ``<workspace>/memory/YYYY-MM-DD.md`` — daily rolling logs

    Path validation ensures no traversal or access outside allowed paths.
    """

    def __init__(self, workspace_dir: Path) -> None:
        self._workspace = Path(workspace_dir).resolve()
        self._memory_dir = self._workspace / "memory"
        self._memory_md = self._workspace / "MEMORY.md"
        self._ensure_dirs()

    @property
    def workspace_dir(self) -> Path:
        return self._workspace

    @property
    def memory_dir(self) -> Path:
        return self._memory_dir

    @property
    def memory_md_path(self) -> Path:
        return self._memory_md

    # ------------------------------------------------------------------
    # Directory setup
    # ------------------------------------------------------------------

    def _ensure_dirs(self) -> None:
        """Ensure the memory/ directory exists."""
        try:
            self._memory_dir.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            logger.warning("Could not create memory directory %s: %s", self._memory_dir, exc)

    # ------------------------------------------------------------------
    # Path validation
    # ------------------------------------------------------------------

    def _validate_path(self, path: str) -> Path:
        """Validate that *path* is within the allowed memory set.

        Allowed:
        - ``MEMORY.md``
        - ``memory/<name>.md`` where <name> matches YYYY-MM-DD or other .md

        Raises :class:`ValueError` on invalid paths.
        """
        # Reject obvious traversal attempts
        if ".." in path:
            raise ValueError(f"Path traversal not allowed: {path}")

        # Normalise to a relative path (strip leading ./ or /)
        clean = path.lstrip("./")

        # Check against allowed patterns
        if clean == "MEMORY.md":
            return self._memory_md

        # memory/*.md or memory/**/*.md
        if clean.startswith("memory/") and clean.endswith(".md"):
            resolved = (self._workspace / clean).resolve()
            # Ensure it stays within workspace
            if not str(resolved).startswith(str(self._workspace)):
                raise ValueError(f"Path escapes workspace: {path}")
            return resolved

        raise ValueError(
            f"Path not allowed: {path}. "
            "Only MEMORY.md and memory/**/*.md are accessible."
        )

    # ------------------------------------------------------------------
    # Daily log operations
    # ------------------------------------------------------------------

    def append_daily(self, text: str, heading: Optional[str] = None) -> Path:
        """Append a block to today's daily log.

        Creates the file with a title header if it doesn't exist yet.
        Each append goes under a timestamped ``##`` heading.

        Args:
            text: Markdown text to append.
            heading: Optional heading. Defaults to ``"HH:MM"``.

        Returns:
            Path to the daily log file.
        """
        today = datetime.now().strftime("%Y-%m-%d")
        log_path = self._memory_dir / f"{today}.md"

        if heading is None:
            heading = datetime.now().strftime("%H:%M")

        block = f"\n## {heading}\n\n{text.strip()}\n"

        if not log_path.exists():
            block = f"# Daily Log — {today}\n{block}"

        with open(log_path, "a", encoding="utf-8") as f:
            f.write(block)

        return log_path

    def read_daily(self, date: str) -> Optional[str]:
        """Read a specific daily log file.

        Args:
            date: Date string in ``YYYY-MM-DD`` format.

        Returns:
            File contents, or *None* if the file doesn't exist.
        """
        log_path = self._memory_dir / f"{date}.md"
        if not log_path.exists():
            return None
        try:
            return log_path.read_text(encoding="utf-8")
        except OSError as exc:
            logger.warning("Could not read daily log %s: %s", log_path, exc)
            return None

    def read_today(self) -> Optional[str]:
        """Read today's daily log."""
        return self.read_daily(datetime.now().strftime("%Y-%m-%d"))

    def read_yesterday(self) -> Optional[str]:
        """Read yesterday's daily log."""
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        return self.read_daily(yesterday)

    # ------------------------------------------------------------------
    # Long-term memory (MEMORY.md) operations
    # ------------------------------------------------------------------

    def append_long_term(self, text: str, heading: Optional[str] = None) -> None:
        """Append a block to MEMORY.md.

        Creates the file with a title header if it doesn't exist yet.

        Args:
            text: Markdown text to append.
            heading: Optional ``##`` heading for this block.
        """
        if heading is None:
            heading = datetime.now().strftime("Added %Y-%m-%d %H:%M")

        block = f"\n## {heading}\n\n{text.strip()}\n"

        if not self._memory_md.exists():
            block = f"# Long-Term Memory\n{block}"

        with open(self._memory_md, "a", encoding="utf-8") as f:
            f.write(block)

    def read_long_term(self) -> Optional[str]:
        """Read MEMORY.md.

        Returns:
            File contents, or *None* if the file doesn't exist.
        """
        if not self._memory_md.exists():
            return None
        try:
            return self._memory_md.read_text(encoding="utf-8")
        except OSError as exc:
            logger.warning("Could not read MEMORY.md: %s", exc)
            return None

    # ------------------------------------------------------------------
    # Generic range read (for memory_get tool)
    # ------------------------------------------------------------------

    def read_range(
        self,
        path: str,
        start_line: int = 0,
        n_lines: int = 0,
    ) -> str:
        """Read a line range from a validated memory file.

        Args:
            path: Relative path (e.g. ``"MEMORY.md"`` or ``"memory/2026-02-18.md"``).
            start_line: 0-based line offset. 0 = beginning.
            n_lines: Number of lines to return. 0 = all remaining.

        Returns:
            The requested content.

        Raises:
            ValueError: If *path* is not within the allowed set.
            FileNotFoundError: If the file doesn't exist.
        """
        resolved = self._validate_path(path)
        if not resolved.exists():
            raise FileNotFoundError(f"Memory file not found: {path}")

        lines = resolved.read_text(encoding="utf-8").splitlines(keepends=True)

        if start_line > 0:
            lines = lines[start_line:]

        if n_lines > 0:
            lines = lines[:n_lines]

        return "".join(lines)

    # ------------------------------------------------------------------
    # Listing
    # ------------------------------------------------------------------

    def list_daily_logs(self) -> list[str]:
        """List all daily log dates (sorted newest first).

        Returns:
            List of date strings like ``["2026-02-18", "2026-02-17", ...]``.
        """
        dates: list[str] = []
        if not self._memory_dir.exists():
            return dates

        for f in self._memory_dir.iterdir():
            if f.is_file() and _DAILY_PATTERN.match(f.name):
                dates.append(f.stem)  # "2026-02-18"

        dates.sort(reverse=True)
        return dates
