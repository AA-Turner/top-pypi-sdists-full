"""Tests for validation of backend-resolved update targets."""

from __future__ import annotations

import pytest

from runlayer_cli.update_contract import (
    Artifact,
    MAX_INSTALLER_SIZE_BYTES,
    TargetRelease,
    UpdateContractError,
    parse_target,
)


def _payload(
    *,
    size_bytes: int = 42,
    artifact_format: str = "pkg",
    filename: str = "agent.pkg",
    variant: str | None = None,
) -> dict[str, object]:
    artifact: dict[str, object] = {
        "platform": "macos",
        "arch": "arm64",
        "filename": filename,
        "sha256": "A" * 64,
        "size_bytes": size_bytes,
        "format": artifact_format,
    }
    if variant is not None:
        artifact["variant"] = variant
    return {
        "data": [
            {
                "package": "ai-watch",
                "resolved_target": {
                    "version": "2.0.0",
                    "artifacts": [artifact],
                },
            }
        ]
    }


def test_parses_and_normalizes_resolved_target() -> None:
    assert parse_target(_payload(), "ai-watch") == TargetRelease(
        version="2.0.0",
        artifacts=(Artifact("macos", "arm64", "agent.pkg", "a" * 64, 42, "pkg"),),
    )


def test_rejects_missing_resolved_target_contract() -> None:
    payload = {"data": [{"package": "ai-watch"}]}

    with pytest.raises(UpdateContractError, match="resolved_target"):
        parse_target(payload, "ai-watch")


def test_accepts_explicit_null_resolved_target() -> None:
    payload = {"data": [{"package": "ai-watch", "resolved_target": None}]}

    assert parse_target(payload, "ai-watch") is None


def test_absent_variant_parses_as_standard_artifact() -> None:
    target = parse_target(_payload(), "ai-watch")

    assert target is not None
    assert target.artifacts[0].variant is None


def test_parses_variant_artifact() -> None:
    target = parse_target(_payload(variant="glibc2.17"), "ai-watch")

    assert target is not None
    assert target.artifacts[0].variant == "glibc2.17"


def test_explicit_null_variant_parses_as_standard_artifact() -> None:
    payload = _payload()
    resolved = payload["data"][0]["resolved_target"]  # type: ignore[index]
    resolved["artifacts"][0]["variant"] = None

    target = parse_target(payload, "ai-watch")

    assert target is not None
    assert target.artifacts[0].variant is None


@pytest.mark.parametrize("variant", ["", 17])
def test_rejects_non_string_or_empty_variant(variant: object) -> None:
    payload = _payload()
    resolved = payload["data"][0]["resolved_target"]  # type: ignore[index]
    resolved["artifacts"][0]["variant"] = variant

    with pytest.raises(UpdateContractError, match="variant"):
        parse_target(payload, "ai-watch")


def test_rejects_unsupported_artifact_format() -> None:
    with pytest.raises(UpdateContractError, match="format"):
        parse_target(_payload(artifact_format="exe"), "ai-watch")


def test_rejects_parent_directory_artifact_filename() -> None:
    with pytest.raises(UpdateContractError, match="basename"):
        parse_target(_payload(filename=".."), "ai-watch")


def test_rejects_oversized_resolved_target_contract() -> None:
    with pytest.raises(UpdateContractError, match="maximum"):
        parse_target(
            _payload(size_bytes=MAX_INSTALLER_SIZE_BYTES + 1),
            "ai-watch",
        )
