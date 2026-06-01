# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for the bump_base_image module."""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from airbyte_ops_mcp.airbyte_repo.bump_base_image import (
    BaseImageError,
    NoBaseImageInMetadataError,
    _extract_docker_repo_from_base_image,
    _extract_major_from_base_image,
    _find_latest_stable_tag,
    _parse_stable_tags,
    bump_base_image,
)

# ---------------------------------------------------------------------------
# _extract_major_from_base_image
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "address,expected",
    [
        pytest.param(
            "docker.io/airbyte/python-connector-base:2.7.3@sha256:abc123",
            2,
            id="standard_digested_address",
        ),
        pytest.param(
            "docker.io/airbyte/python-connector-base:1.0.0",
            1,
            id="no_digest",
        ),
        pytest.param(
            "docker.io/airbyte/java-connector-base:0.44.5@sha256:def456",
            0,
            id="zero_major",
        ),
        pytest.param(
            "docker.io/repo:latest",
            None,
            id="non_semver_tag",
        ),
        pytest.param(
            "docker.io/repo:2.0",
            None,
            id="incomplete_semver",
        ),
    ],
)
def test_extract_major_from_base_image(address: str, expected: int | None):
    assert _extract_major_from_base_image(address) == expected


# ---------------------------------------------------------------------------
# _find_latest_stable_tag
# ---------------------------------------------------------------------------

SAMPLE_TAGS = {
    "1.0.0": "sha256:aaa",
    "1.2.3": "sha256:bbb",
    "2.0.0": "sha256:ccc",
    "2.1.0-rc.1": "sha256:ddd",  # prerelease — should be skipped
    "2.1.0": "sha256:eee",
    "latest": "sha256:fff",  # non-semver — should be skipped
}


@pytest.mark.unit
def test_find_latest_stable_tag_unconstrained():
    result = _find_latest_stable_tag(SAMPLE_TAGS)
    assert result is not None
    tag, digest = result
    assert tag == "2.1.0"
    assert digest == "sha256:eee"


@pytest.mark.unit
def test_find_latest_stable_tag_constrained_to_major_1():
    result = _find_latest_stable_tag(SAMPLE_TAGS, major=1)
    assert result is not None
    tag, _ = result
    assert tag == "1.2.3"


@pytest.mark.unit
def test_find_latest_stable_tag_no_match():
    result = _find_latest_stable_tag(SAMPLE_TAGS, major=99)
    assert result is None


# ---------------------------------------------------------------------------
# _parse_stable_tags
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_parse_stable_tags_filters_prerelease_and_non_semver():
    tags = {
        "1.0.0": "sha256:a",
        "2.0.0-beta.1": "sha256:b",
        "latest": "sha256:c",
        "3.0.0": "",  # empty digest — should be skipped
    }
    result = _parse_stable_tags(tags)
    assert len(result) == 1
    assert result[0][1] == "1.0.0"


# ---------------------------------------------------------------------------
# _extract_docker_repo_from_base_image
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "address,expected",
    [
        pytest.param(
            "docker.io/airbyte/python-connector-base:2.7.3@sha256:abc123",
            "airbyte/python-connector-base",
            id="standard_digested_address",
        ),
        pytest.param(
            "docker.io/airbyte/source-declarative-manifest:1.0.0",
            "airbyte/source-declarative-manifest",
            id="no_digest",
        ),
        pytest.param(
            "docker.io/airbyte/java-connector-base:0.44.5@sha256:def456",
            "airbyte/java-connector-base",
            id="java_base",
        ),
    ],
)
def test_extract_docker_repo_from_base_image(address: str, expected: str):
    assert _extract_docker_repo_from_base_image(address) == expected


# ---------------------------------------------------------------------------
# bump_base_image (integration-style with mocked DockerHub)
# ---------------------------------------------------------------------------


def _make_connector(tmpdir: str, connector_name: str, metadata_yaml: str) -> Path:
    """Helper to create a minimal connector directory."""
    connector_dir = (
        Path(tmpdir) / "airbyte-integrations" / "connectors" / connector_name
    )
    connector_dir.mkdir(parents=True)
    (connector_dir / "metadata.yaml").write_text(metadata_yaml)
    return connector_dir


METADATA_WITH_BASE_IMAGE = """\
data:
  connectorBuildOptions:
    baseImage: "docker.io/airbyte/python-connector-base:1.0.0@sha256:old"
  connectorType: source
"""

MOCK_TAGS = {
    "1.0.0": "sha256:old",
    "1.2.0": "sha256:new",
    "2.0.0": "sha256:v2",
}


@pytest.mark.unit
@patch("airbyte_ops_mcp.airbyte_repo.bump_base_image.get_docker_hub_tags_and_digests")
def test_bump_base_image_default_stays_within_major(mock_tags):
    mock_tags.return_value = MOCK_TAGS

    with tempfile.TemporaryDirectory() as tmpdir:
        _make_connector(tmpdir, "source-test", METADATA_WITH_BASE_IMAGE)
        result = bump_base_image(tmpdir, "source-test")

    assert result.updated is True
    assert "1.2.0" in result.new_base_image
    assert "2.0.0" not in result.new_base_image


@pytest.mark.unit
@patch("airbyte_ops_mcp.airbyte_repo.bump_base_image.get_docker_hub_tags_and_digests")
def test_bump_base_image_force_latest_crosses_major(mock_tags):
    mock_tags.return_value = MOCK_TAGS

    with tempfile.TemporaryDirectory() as tmpdir:
        _make_connector(tmpdir, "source-test", METADATA_WITH_BASE_IMAGE)
        result = bump_base_image(tmpdir, "source-test", force_latest=True)

    assert result.updated is True
    assert "2.0.0" in result.new_base_image


@pytest.mark.unit
def test_bump_base_image_no_base_image_raises():
    metadata = "data:\n  connectorType: source\n"

    with tempfile.TemporaryDirectory() as tmpdir:
        _make_connector(tmpdir, "source-test", metadata)
        with pytest.raises(NoBaseImageInMetadataError):
            bump_base_image(tmpdir, "source-test")


@pytest.mark.unit
@patch("airbyte_ops_mcp.airbyte_repo.bump_base_image.get_docker_hub_tags_and_digests")
def test_bump_base_image_unparseable_tag_raises_in_default_mode(mock_tags):
    """Default mode raises BaseImageError when current tag isn't valid semver."""
    mock_tags.return_value = MOCK_TAGS
    metadata = """\
data:
  connectorBuildOptions:
    baseImage: "docker.io/airbyte/python-connector-base:latest"
  connectorType: source
"""

    with tempfile.TemporaryDirectory() as tmpdir:
        _make_connector(tmpdir, "source-test", metadata)
        with pytest.raises(BaseImageError, match="Use --force-latest"):
            bump_base_image(tmpdir, "source-test")
