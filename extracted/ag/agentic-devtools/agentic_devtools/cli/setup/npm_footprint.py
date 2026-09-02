"""npm/Node.js footprint detection for conditional setup gating.

Provides a pure detection function that checks whether a directory contains
npm/Node.js indicator files, enabling the setup command to skip npm-specific
certificate and configuration work for non-Node repositories.

This module is intentionally side-effect-free and importable by future
consumers (e.g. the doctor command in #2324).
"""

from pathlib import Path

NPM_INDICATOR_FILES: tuple[str, ...] = (
    "package.json",
    ".nvmrc",
    ".node-version",
    "package-lock.json",
    "npm-shrinkwrap.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "bun.lockb",
)
# Filenames whose presence at a directory root indicates an npm/Node.js project.


def detect_npm_footprint(directory: Path) -> bool:
    """Detect whether a directory has an npm/Node.js footprint.

    Checks for indicator files at the given directory root only
    (no subdirectory scanning). Short-circuits on first match.

    Args:
        directory: The directory to check (typically repo root or CWD).

    Returns:
        True if any npm indicator file exists as a file or symlink to a file,
        False otherwise.
    """
    for filename in NPM_INDICATOR_FILES:
        if (directory / filename).is_file():
            return True
    return False
