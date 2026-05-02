"""Filesystem helpers for packaged charter and profile manifests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

PROFILE_MANIFEST_FILENAME = "profile.json"
AEGIS_FILENAME = "AEGIS.md"
PROFILE_BUNDLES_DIRNAME = "profiles"


def profile_manifest_path(profile_dir: Path) -> Path:
    return profile_dir / PROFILE_MANIFEST_FILENAME


def profile_bundle_has_content(bundle_dir: Path) -> bool:
    return profile_manifest_path(bundle_dir).exists()


def write_profile_manifest_file(profile_dir: Path, manifest: Mapping[str, Any]) -> Path:
    path = profile_manifest_path(profile_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dict(manifest), indent=2, sort_keys=True), encoding="utf-8")
    return path
