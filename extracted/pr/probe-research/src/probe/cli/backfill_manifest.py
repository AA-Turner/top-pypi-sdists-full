"""Validate the exact file set assigned to one backfill worker.

The manifest is agent output, not a completion receipt. Keep independently
valid rows usable while retaining every omission or invalid row as a failure.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path, PurePosixPath


MAX_MANIFEST_BYTES = 32 * 1024 * 1024
MAX_ROW_BYTES = 256 * 1024
_FIELDS = frozenset({"path", "name", "notes", "reference", "allow_missing"})


@dataclass(frozen=True)
class ManifestCheck:
    rows: tuple[dict, ...]
    missing: tuple[str, ...]
    errors: tuple[str, ...]

    @property
    def complete(self) -> bool:
        return not self.missing and not self.errors

    def describe(self) -> str:
        parts = list(self.errors[:3])
        if self.missing:
            sample = ", ".join(self.missing[:3])
            parts.append(f"{len(self.missing)} assigned file(s) missing: {sample}")
        return "; ".join(parts)


def validate_manifest(manifest: Path, paths: tuple[str, ...], *, root: Path) -> ManifestCheck:
    """Read bounded JSONL and reconcile unique, confined, schema-valid paths."""
    expected = set(paths)
    valid: dict[str, dict] = {}
    seen: set[str] = set()
    errors: list[str] = []
    resolved_root = root.resolve()
    try:
        if manifest.stat().st_size > MAX_MANIFEST_BYTES:
            raise ValueError("manifest exceeds the 32 MiB limit")
        with manifest.open("rb") as source:
            lineno = 0
            total_bytes = 0
            while raw := source.readline(MAX_ROW_BYTES + 1):
                lineno += 1
                total_bytes += len(raw)
                if total_bytes > MAX_MANIFEST_BYTES or lineno > max(1024, len(paths) * 2 + 16):
                    errors.append("manifest exceeds the bounded row/byte budget")
                    break
                if len(raw) > MAX_ROW_BYTES:
                    errors.append(f"line {lineno}: manifest row exceeds 256 KiB")
                    while raw and not raw.endswith(b"\n"):
                        raw = source.readline(MAX_ROW_BYTES + 1)
                        total_bytes += len(raw)
                        if total_bytes > MAX_MANIFEST_BYTES:
                            errors.append("manifest exceeds the bounded byte budget")
                            break
                    if total_bytes > MAX_MANIFEST_BYTES:
                        break
                    continue
                if not raw.strip():
                    continue
                try:
                    row = json.loads(raw)
                    if not isinstance(row, dict):
                        raise ValueError("expected a JSON object")
                    path = row.get("path")
                    if not isinstance(path, str) or not path or "\x00" in path:
                        raise ValueError("path must be a nonempty string")
                    rel = PurePosixPath(path)
                    if rel.is_absolute() or ".." in rel.parts or str(rel) != path:
                        raise ValueError("path must be the exact assigned relative path")
                    if path not in expected:
                        raise ValueError(f"path is outside this unit: {path}")
                    if path in seen:
                        valid.pop(path, None)
                        raise ValueError(f"duplicate path: {path}")
                    seen.add(path)
                    unknown = row.keys() - _FIELDS
                    if unknown:
                        raise ValueError(f"unknown fields: {', '.join(sorted(unknown))}")
                    if "name" in row and row["name"] != path:
                        raise ValueError("name must preserve the exact source path")
                    if "notes" in row and not isinstance(row["notes"], str):
                        raise ValueError("notes must be a string")
                    for key in ("reference", "allow_missing"):
                        if key in row and not isinstance(row[key], bool):
                            raise ValueError(f"{key} must be true or false")
                    resolved = (resolved_root / path).resolve()
                    if not resolved.is_relative_to(resolved_root):
                        raise ValueError(f"path resolves outside the imported folder: {path}")
                    valid[path] = row
                except (ValueError, UnicodeError, OSError, RuntimeError) as exc:
                    errors.append(f"line {lineno}: {str(exc)[:512]}")
    except (OSError, ValueError) as exc:
        errors.append(f"no manifest could be read: {exc}")
    return ManifestCheck(
        rows=tuple(valid[path] for path in paths if path in valid),
        missing=tuple(sorted(expected - valid.keys())),
        errors=tuple(errors),
    )
