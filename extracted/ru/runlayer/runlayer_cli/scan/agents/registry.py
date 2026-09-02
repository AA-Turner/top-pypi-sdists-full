"""Declarative signature registry.

The framework knowledge base lives entirely in ``signatures.json`` (data, not
code): adding or tuning a framework is a data-only edit. This module loads and
validates that file into typed :class:`FrameworkSignature` records.

Standard-library only. The data file is resolved in both source checkouts and
the frozen ``aiwatch`` onedir/onefile bundle.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# Default evidence weights. ``signatures.json`` may override any of these via a
# top-level ``weights`` object; unknown keys are ignored.
DEFAULT_WEIGHTS: dict[str, int] = {
    "package_dep": 3,
    "import": 2,
    "symbol": 1,
    "shared_dep": 1,
}

# Fields a framework entry must declare. The signature list fields default to
# empty when omitted, but identity + manifest fields are mandatory.
_REQUIRED_FIELDS = ("framework_id", "display_name", "language", "manifest_files")


class RegistryError(ValueError):
    """Raised when ``signatures.json`` is missing or structurally invalid."""


@dataclass(frozen=True)
class FrameworkSignature:
    """One framework's detection signature (a single ``signatures.json`` entry)."""

    framework_id: str
    display_name: str
    language: str
    manifest_files: tuple[str, ...]
    package_deps: tuple[str, ...] = ()
    shared_deps: tuple[str, ...] = ()
    imports: tuple[str, ...] = ()
    symbols: tuple[str, ...] = ()


@dataclass(frozen=True)
class Registry:
    """The loaded, validated knowledge base."""

    weights: dict[str, int]
    frameworks: tuple[FrameworkSignature, ...]

    @property
    def framework_ids(self) -> tuple[str, ...]:
        return tuple(fw.framework_id for fw in self.frameworks)


def signatures_path() -> Path:
    """Locate ``signatures.json`` in both source and frozen-bundle layouts.

    Resolution order: PyInstaller's ``sys._MEIPASS`` (onedir + onefile), then a
    path next to the executable (py2exe and other freezers ship data there),
    then the module-relative file (source checkouts).
    """
    relative = Path("runlayer_cli", "scan", "agents", "signatures.json")
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        bundled = Path(meipass) / relative
        if bundled.is_file():
            return bundled
    if getattr(sys, "frozen", False):
        near_exe = Path(sys.executable).resolve().parent / relative
        if near_exe.is_file():
            return near_exe
    return Path(__file__).resolve().parent / "signatures.json"


def _as_str_tuple(value: Any, *, field: str, framework_id: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
        raise RegistryError(
            f"framework {framework_id!r}: field {field!r} must be a list of strings"
        )
    return tuple(value)


def _build_framework(entry: Any) -> FrameworkSignature:
    if not isinstance(entry, dict):
        raise RegistryError(f"framework entry must be an object, got {type(entry)}")
    framework_id = entry.get("framework_id")
    if not isinstance(framework_id, str) or not framework_id:
        raise RegistryError("framework entry missing a string 'framework_id'")
    for field in _REQUIRED_FIELDS:
        if field not in entry:
            raise RegistryError(f"framework {framework_id!r} missing field {field!r}")
    manifest_files = _as_str_tuple(
        entry.get("manifest_files"), field="manifest_files", framework_id=framework_id
    )
    if not manifest_files:
        raise RegistryError(
            f"framework {framework_id!r}: 'manifest_files' must be non-empty"
        )
    display_name = entry.get("display_name")
    language = entry.get("language")
    if not isinstance(display_name, str) or not isinstance(language, str):
        raise RegistryError(
            f"framework {framework_id!r}: 'display_name' and 'language' must be strings"
        )
    return FrameworkSignature(
        framework_id=framework_id,
        display_name=display_name,
        language=language,
        manifest_files=manifest_files,
        package_deps=_as_str_tuple(
            entry.get("package_deps"), field="package_deps", framework_id=framework_id
        ),
        shared_deps=_as_str_tuple(
            entry.get("shared_deps"), field="shared_deps", framework_id=framework_id
        ),
        imports=_as_str_tuple(
            entry.get("imports"), field="imports", framework_id=framework_id
        ),
        symbols=_as_str_tuple(
            entry.get("symbols"), field="symbols", framework_id=framework_id
        ),
    )


def load_registry(path: str | Path | None = None) -> Registry:
    """Load and validate the signature registry.

    Raises :class:`RegistryError` if the file is missing, not valid JSON, or any
    framework entry is malformed -- a single bad edit fails loudly rather than
    silently dropping a framework.
    """
    resolved = Path(path) if path is not None else signatures_path()
    try:
        raw = json.loads(resolved.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RegistryError(f"signatures file not found: {resolved}") from exc
    except json.JSONDecodeError as exc:
        raise RegistryError(f"signatures file is not valid JSON: {exc}") from exc

    if not isinstance(raw, dict):
        raise RegistryError("signatures file must be a JSON object")

    entries = raw.get("frameworks")
    if not isinstance(entries, list) or not entries:
        raise RegistryError(
            "signatures file must declare a non-empty 'frameworks' list"
        )

    frameworks = tuple(_build_framework(entry) for entry in entries)

    seen: set[str] = set()
    for fw in frameworks:
        if fw.framework_id in seen:
            raise RegistryError(f"duplicate framework_id {fw.framework_id!r}")
        seen.add(fw.framework_id)

    weights = dict(DEFAULT_WEIGHTS)
    overrides = raw.get("weights")
    if isinstance(overrides, dict):
        for key, value in overrides.items():
            if key in DEFAULT_WEIGHTS and isinstance(value, (int, float)):
                weights[key] = int(value)

    return Registry(weights=weights, frameworks=frameworks)
