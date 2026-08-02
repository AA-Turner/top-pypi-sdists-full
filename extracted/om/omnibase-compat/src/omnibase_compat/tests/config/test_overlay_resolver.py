# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Resolution-equivalence + fail-closed tests for the compat overlay resolver.

These tests pin the OMN-13564 migration invariant: the endpoint URL and the
autowire strict-mode flag resolve from the contract/overlay surface and produce
behavior identical to the pre-migration hardcoded literal / bare env read,
while failing **closed** on a missing/invalid overlay or missing field.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
from pydantic import ValidationError

from omnibase_compat.config.overlay_resolver import (
    ModelCompatRuntimeOverlay,
    OverlayResolutionError,
    load_overlay,
    resolve_autowire_strict_raw,
    resolve_endpoint_url,
)

# The exact URL the pre-migration ``_LINEAR_API_URL`` literal produced.
# This constant lives in a test file (out of scan scope for url-authority) and
# is the equivalence oracle for the migration.
_PRE_MIGRATION_LINEAR_URL = "https://api.linear.app/graphql"  # url-authority-ok: test oracle


@pytest.mark.unit
def test_packaged_overlay_validates() -> None:
    """The shipped overlay parses into the typed model with no extra keys."""
    overlay = load_overlay()
    assert isinstance(overlay, ModelCompatRuntimeOverlay)
    assert overlay.schema_version == "1.0.0"
    assert "project_tracker_linear" in overlay.endpoints


@pytest.mark.unit
def test_endpoint_resolution_equivalence() -> None:
    """Resolved Linear endpoint equals the pre-migration literal exactly."""
    resolved = resolve_endpoint_url("project_tracker_linear")
    assert resolved == _PRE_MIGRATION_LINEAR_URL


@pytest.mark.unit
def test_unknown_endpoint_fails_closed() -> None:
    """An unknown endpoint name raises rather than returning a default."""
    with pytest.raises(OverlayResolutionError):
        resolve_endpoint_url("does_not_exist")


@pytest.mark.unit
def test_missing_overlay_file_fails_closed(tmp_path: Path) -> None:
    """A missing overlay file fails closed (no silent default)."""
    with pytest.raises(OverlayResolutionError):
        resolve_endpoint_url(
            "project_tracker_linear",
            overlay_path=tmp_path / "nonexistent.json",
        )


@pytest.mark.unit
def test_invalid_json_fails_closed(tmp_path: Path) -> None:
    """An unparseable overlay fails closed."""
    bad = tmp_path / "overlay.json"
    bad.write_text("{not json", encoding="utf-8")
    with pytest.raises(OverlayResolutionError):
        load_overlay(bad)


@pytest.mark.unit
def test_unknown_top_level_key_fails_closed(tmp_path: Path) -> None:
    """extra='forbid' makes an unknown overlay key fail at parse time."""
    doc = {
        "schema_version": "1.0.0",
        "endpoints": {"project_tracker_linear": {"url": _PRE_MIGRATION_LINEAR_URL}},
        "autowire": {"strict_mode_raw": None},
        "surprise_key": "boom",
    }
    overlay_file = tmp_path / "overlay.json"
    overlay_file.write_text(json.dumps(doc), encoding="utf-8")
    with pytest.raises(ValidationError):
        load_overlay(overlay_file)


@pytest.mark.unit
@pytest.mark.parametrize(
    ("env_value", "expected_raw"),
    [
        (None, None),
        ("", ""),
        ("0", "0"),
        ("1", "1"),
        ("true", "true"),
        ("1 ", "1 "),
    ],
)
def test_autowire_strict_interpolation_equivalence(
    monkeypatch: pytest.MonkeyPatch,
    env_value: str | None,
    expected_raw: str | None,
) -> None:
    """${env.AUTOWIRE_STRICT} resolves to exactly what os.environ.get would return."""
    if env_value is None:
        monkeypatch.delenv("AUTOWIRE_STRICT", raising=False)
    else:
        monkeypatch.setenv("AUTOWIRE_STRICT", env_value)
    assert resolve_autowire_strict_raw() == expected_raw
    # Direct oracle: the resolved raw value matches the raw env read it replaced.
    assert resolve_autowire_strict_raw() == os.environ.get("AUTOWIRE_STRICT")


@pytest.mark.unit
def test_endpoint_env_override(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """An endpoint declared as ${env.VAR} resolves from the environment."""
    doc = {
        "schema_version": "1.0.0",
        "endpoints": {"project_tracker_linear": {"url": "${env.LINEAR_OVERRIDE_URL}"}},
        "autowire": {"strict_mode_raw": None},
    }
    overlay_file = tmp_path / "overlay.json"
    overlay_file.write_text(json.dumps(doc), encoding="utf-8")
    monkeypatch.setenv("LINEAR_OVERRIDE_URL", "https://linear.example.test/graphql")
    resolved = resolve_endpoint_url("project_tracker_linear", overlay_path=overlay_file)
    assert resolved == "https://linear.example.test/graphql"  # url-authority-ok: test
