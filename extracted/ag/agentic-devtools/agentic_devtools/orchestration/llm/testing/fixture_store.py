"""Fixture store for deterministic test mode."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agentic_devtools.orchestration.llm.errors import (
    FixtureVersionMismatchError,
    NoFixtureFoundError,
)

CURRENT_FIXTURE_VERSION = 1
INVALID_FILENAME_CHARS = frozenset('<>:"/\\|?*')
WINDOWS_RESERVED_BASENAMES = frozenset(
    {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "COM5",
        "COM6",
        "COM7",
        "COM8",
        "COM9",
        "LPT1",
        "LPT2",
        "LPT3",
        "LPT4",
        "LPT5",
        "LPT6",
        "LPT7",
        "LPT8",
        "LPT9",
    }
)


def _validate_fixture_key(key: str) -> None:
    """Validate that a fixture key is a safe filename component.

    Raises:
        ValueError: If the key contains path separators that could enable path traversal.
    """
    if "/" in key or "\\" in key:
        raise ValueError(f"Invalid fixture key {key!r}: must not contain path separators")
    if not key:
        raise ValueError("Invalid fixture key: must not be empty")
    if key != key.strip():
        raise ValueError(f"Invalid fixture key {key!r}: must not contain leading/trailing whitespace")
    if key in {".", ".."}:
        raise ValueError(f"Invalid fixture key {key!r}: reserved relative path segment")
    if any(ord(ch) < 32 for ch in key):
        raise ValueError(f"Invalid fixture key {key!r}: must not contain control characters")
    if key.endswith("."):
        raise ValueError(f"Invalid fixture key {key!r}: must not end with a dot")
    invalid_char = next((ch for ch in key if ch in INVALID_FILENAME_CHARS), None)
    if invalid_char is not None:
        raise ValueError(f"Invalid fixture key {key!r}: invalid filename character {invalid_char!r}")
    base_name = key.split(".", 1)[0].upper()
    if base_name in WINDOWS_RESERVED_BASENAMES:
        raise ValueError(f"Invalid fixture key {key!r}: reserved Windows filename")


class FixtureStore:
    """Manages fixture files for deterministic LLM test mode."""

    def __init__(self, fixture_dir: str | Path) -> None:
        self._fixture_dir = Path(fixture_dir)

    @property
    def fixture_dir(self) -> Path:
        """Return the fixture directory path."""
        return self._fixture_dir

    def exists(self, key: str) -> bool:
        """Check if a fixture exists for the given key."""
        _validate_fixture_key(key)
        override = self._fixture_dir / f"{key}.override.json"
        if override.exists():
            return True
        return (self._fixture_dir / f"{key}.json").exists()

    def load(self, key: str) -> dict[str, Any]:
        """Load a fixture by key.

        Override files (<key>.override.json) take precedence.

        Args:
            key: Fixture key (SHA-256 hash or explicit name).

        Returns:
            Fixture record dict with fixture_version, request, response.

        Raises:
            NoFixtureFoundError: If no fixture found.
            FixtureVersionMismatchError: If fixture version doesn't match.
        """
        return load_fixture(key, fixture_dir=self._fixture_dir)

    def save(self, key: str, request: dict[str, Any], response: dict[str, Any]) -> Path:
        """Save a fixture record.

        Args:
            key: Fixture key.
            request: Canonical request payload.
            response: Provider response metadata and content.

        Returns:
            Path to saved fixture file.
        """
        return save_fixture(key, request=request, response=response, fixture_dir=self._fixture_dir)


def load_fixture(
    key: str,
    *,
    fixture_dir: str | Path,
    expected_version: int = CURRENT_FIXTURE_VERSION,
) -> dict[str, Any]:
    """Load a fixture by key from the fixture directory.

    Args:
        key: Fixture key (SHA-256 hash or explicit name).
        fixture_dir: Directory containing fixture files.
        expected_version: Expected fixture version.

    Returns:
        Fixture record dict.

    Raises:
        NoFixtureFoundError: If no fixture found.
        FixtureVersionMismatchError: If version doesn't match.
    """
    dir_path = Path(fixture_dir)

    _validate_fixture_key(key)

    # Override files take precedence
    override_path = dir_path / f"{key}.override.json"
    fixture_path = dir_path / f"{key}.json"

    path = override_path if override_path.exists() else fixture_path

    if not path.exists():
        raise NoFixtureFoundError(
            f"No fixture found for key: {key}",
            fixture_key=key,
            fixture_dir=str(dir_path),
        )

    with open(path, encoding="utf-8") as f:
        record = json.load(f)

    actual_version = record.get("fixture_version", 0)
    if actual_version != expected_version:
        raise FixtureVersionMismatchError(
            f"Fixture version {actual_version} != expected {expected_version}",
            expected_version=expected_version,
            actual_version=actual_version,
            fixture_path=str(path),
        )

    return record


def save_fixture(
    key: str,
    *,
    request: dict[str, Any],
    response: dict[str, Any],
    fixture_dir: str | Path,
) -> Path:
    """Save a fixture record to the fixture directory.

    Args:
        key: Fixture key.
        request: Canonical request payload.
        response: Provider response metadata and content.
        fixture_dir: Directory to save fixture files.

    Returns:
        Path to saved fixture file.
    """
    dir_path = Path(fixture_dir)
    dir_path.mkdir(parents=True, exist_ok=True)

    _validate_fixture_key(key)

    record = {
        "fixture_version": CURRENT_FIXTURE_VERSION,
        "request": request,
        "response": response,
    }

    path = dir_path / f"{key}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, sort_keys=True, ensure_ascii=False)

    return path
