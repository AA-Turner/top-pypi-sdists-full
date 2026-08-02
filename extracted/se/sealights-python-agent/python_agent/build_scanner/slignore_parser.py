"""
Parser for .slignore files.

The .slignore file defines patterns for files/directories to exclude from scanning.
It works similarly to .gitignore - if the file exists in the workspace root,
it takes precedence over CLI --exclude/--include parameters.

Supported syntax:
- One pattern per line (shell-style wildcards: *, ?, [seq])
- Lines starting with # are comments
- Blank lines are ignored

Example .slignore file:
    # Ignore virtual environments
    *venv*
    .venv/

    # Ignore test directories
    *tests*
    test_*.py

    # Ignore cache and build artifacts
    __pycache__
    *.pyc
    dist/
    build/
"""

import logging
import os

from python_agent.common.constants import SLIGNORE_FILENAME

log = logging.getLogger(__name__)


class SLIgnoreParser:
    """
    Parser for .slignore files.

    Usage:
        parser = SLIgnoreParser("/path/to/workspace")
        if parser.exists():
            exclude_patterns = parser.parse()
    """

    def __init__(self, workspace_path: str):
        """
        Initialize the parser.

        Args:
            workspace_path: Path to the workspace root where .slignore should be located.
        """
        self.workspace_path = workspace_path
        self.slignore_path = os.path.join(workspace_path, SLIGNORE_FILENAME)

    def exists(self) -> bool:
        """
        Check if .slignore file exists in the workspace.

        Returns:
            True if .slignore file exists, False otherwise.
        """
        return os.path.isfile(self.slignore_path)

    def parse(self) -> list:
        """
        Parse the .slignore file and return list of exclude patterns.

        Returns:
            List of exclude patterns. Empty list if file doesn't exist or is empty.
        """
        if not self.exists():
            log.debug(f"No {SLIGNORE_FILENAME} file found at {self.slignore_path}")
            return []

        patterns = []
        try:
            with open(self.slignore_path, "r", encoding="utf-8") as f:
                for line_number, line in enumerate(f, start=1):
                    pattern = self._parse_line(line)
                    if pattern:
                        patterns.append(pattern)
                        log.debug(f"Parsed pattern from line {line_number}: {pattern}")

            log.info(
                f"Loaded {len(patterns)} exclude pattern(s) from {SLIGNORE_FILENAME}"
            )
        except IOError as e:
            log.error(f"Failed to read {SLIGNORE_FILENAME}: {e}")
        except Exception as e:
            log.error(f"Unexpected error parsing {SLIGNORE_FILENAME}: {e}")

        return patterns

    def _parse_line(self, line: str) -> str:
        """
        Parse a single line from the .slignore file.

        Args:
            line: A single line from the file.

        Returns:
            The pattern string, or None if line is a comment or blank.
        """
        # Strip whitespace from both ends
        line = line.strip()

        # Skip empty lines
        if not line:
            return None

        # Skip comments (lines starting with #)
        if line.startswith("#"):
            return None

        return line
