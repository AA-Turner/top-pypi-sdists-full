"""Read and validate the shared quality baseline."""

from __future__ import annotations

import json
from pathlib import Path


def read_quality_baseline(
    repo_root: str | Path,
) -> tuple[dict[str, int], dict[str, str], str | None]:
    """Return validated file-length and complexity entries, or a readable error."""
    path = Path(repo_root) / "quality-baseline.json"
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}, {}, "ERROR: quality-baseline.json is missing."
    except (OSError, UnicodeError) as exc:
        return {}, {}, f"ERROR: Could not read quality-baseline.json: {exc}"

    try:
        baseline = json.loads(text)
    except json.JSONDecodeError as exc:
        return {}, {}, f"ERROR: Invalid quality baseline JSON: {exc}"

    return _validate_baseline(baseline)


def _validate_baseline(
    baseline: object,
) -> tuple[dict[str, int], dict[str, str], str | None]:
    if not isinstance(baseline, dict):
        return {}, {}, "ERROR: Invalid quality baseline: expected an object."

    version = baseline.get("schema_version")
    if isinstance(version, bool) or not isinstance(version, int) or version != 1:
        return {}, {}, f"ERROR: Invalid quality baseline schema_version: {version!r}."

    raw_file_lengths = baseline.get("file_length")
    if not isinstance(raw_file_lengths, dict):
        return {}, {}, "ERROR: Invalid quality baseline: file_length must be an object."
    raw_complexity = baseline.get("complexity")
    if not isinstance(raw_complexity, dict):
        return {}, {}, "ERROR: Invalid quality baseline: complexity must be an object."

    file_lengths, error = _validate_file_lengths(raw_file_lengths)
    if error is not None:
        return {}, {}, error
    complexity, error = _validate_complexity(raw_complexity)
    if error is not None:
        return {}, {}, error
    return file_lengths, complexity, None


def _validate_file_lengths(raw_file_lengths: dict[object, object]) -> tuple[dict[str, int], str | None]:
    file_lengths: dict[str, int] = {}
    for relative_path, line_count in raw_file_lengths.items():
        if (
            not isinstance(relative_path, str)
            or not isinstance(line_count, int)
            or isinstance(line_count, bool)
            or line_count < 0
        ):
            return {}, f"ERROR: Invalid quality baseline line count for {relative_path!r}."
        file_lengths[relative_path] = line_count
    return file_lengths, None


def _validate_complexity(raw_complexity: dict[object, object]) -> tuple[dict[str, str], str | None]:
    complexity: dict[str, str] = {}
    for identifier, message in raw_complexity.items():
        if not isinstance(identifier, str) or not identifier or not isinstance(message, str) or not message:
            return {}, f"ERROR: Invalid quality baseline complexity entry: {identifier!r}."
        complexity[identifier] = message
    return complexity, None
