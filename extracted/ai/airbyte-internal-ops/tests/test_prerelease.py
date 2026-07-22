# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for the prerelease module."""

from __future__ import annotations

import pytest

from airbyte_ops_mcp.airbyte_repo.bump_version import InvalidVersionError
from airbyte_ops_mcp.mcp.connector_versions import (
    PRERELEASE_SHA_LENGTH,
    PRERELEASE_TAG_PREFIX,
    compute_prerelease_docker_image_tag,
)


@pytest.mark.parametrize(
    "base_version,sha,expected,expected_exception",
    [
        pytest.param(
            "1.2.3",
            "abcdef1234567890",
            "1.2.3-preview.abcdef1",
            None,
            id="standard_version_long_sha",
        ),
        pytest.param(
            "0.1.0",
            "1234567",
            "0.1.0-preview.1234567",
            None,
            id="short_version_exact_sha_length",
        ),
        pytest.param(
            "10.20.30",
            "abc1234",
            "10.20.30-preview.abc1234",
            None,
            id="large_version_numbers",
        ),
        pytest.param(
            "0.0.1",
            "deadbeef12345678901234567890",
            "0.0.1-preview.deadbee",
            None,
            id="very_long_sha_truncated",
        ),
        pytest.param(
            "2.0.0",
            "a6370d9275abc123",
            "2.0.0-preview.a6370d9",
            None,
            id="real_world_sha_example",
        ),
        pytest.param(
            "2.23.16-rc.1",
            "abcdef1234567890",
            "2.23.16-preview.abcdef1",
            None,
            id="rc_version_stripped_to_preview",
        ),
        pytest.param(
            "1.3.0-rc.5",
            "deadbeef12345678",
            "1.3.0-preview.deadbee",
            None,
            id="rc_high_number_stripped_to_preview",
        ),
        pytest.param(
            "0.1.0-rc.1",
            "abc1234",
            "0.1.0-preview.abc1234",
            None,
            id="rc_zero_major_stripped_to_preview",
        ),
        pytest.param(
            "not-a-version",
            "abcdef1234567890",
            None,
            InvalidVersionError,
            id="invalid_version_raises_error",
        ),
    ],
)
def test_compute_prerelease_docker_image_tag(
    base_version: str,
    sha: str,
    expected: str | None,
    expected_exception: type[Exception] | None,
) -> None:
    """Test that compute_prerelease_docker_image_tag produces correct version tags."""
    if expected_exception is not None:
        with pytest.raises(expected_exception):
            compute_prerelease_docker_image_tag(base_version, sha)
    else:
        result = compute_prerelease_docker_image_tag(base_version, sha)
        assert result == expected


def test_prerelease_constants() -> None:
    """Test that prerelease constants have expected values."""
    assert PRERELEASE_TAG_PREFIX == "preview"
    assert PRERELEASE_SHA_LENGTH == 7


def test_compute_prerelease_docker_image_tag_uses_constants() -> None:
    """Test that the function uses the defined constants for consistency."""
    base_version = "1.0.0"
    sha = "abcdefghijklmnop"

    result = compute_prerelease_docker_image_tag(base_version, sha)

    assert f"-{PRERELEASE_TAG_PREFIX}." in result
    assert result.endswith(sha[:PRERELEASE_SHA_LENGTH])
