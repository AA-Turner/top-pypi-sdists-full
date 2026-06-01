# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for the existing-pin guard in cloud_admin.version_guard."""

from __future__ import annotations

import pytest

from airbyte_ops_mcp.cloud_admin.version_guard import (
    _check_major_version_crossing,
    _validate_not_already_pinned,
)

# ---------------------------------------------------------------------------
# _validate_not_already_pinned
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("is_pinned", "pinned_version", "pin_scope", "force", "expected_error"),
    [
        # Not pinned — should always pass
        pytest.param(False, None, None, False, None, id="not-pinned"),
        pytest.param(False, None, None, True, None, id="not-pinned-forced"),
        pytest.param(False, "1.0.0", None, False, None, id="not-pinned-with-version"),
        pytest.param(False, None, "actor", False, None, id="not-pinned-with-scope"),
        # Pinned without force — should reject
        pytest.param(True, None, None, False, "already pinned", id="pinned-basic"),
        pytest.param(
            True,
            "3.5.2",
            None,
            False,
            "version 3.5.2",
            id="pinned-with-version",
        ),
        pytest.param(
            True,
            None,
            "actor",
            False,
            "at actor scope",
            id="pinned-with-scope",
        ),
        pytest.param(
            True,
            "2.1.0",
            "workspace",
            False,
            "version 2.1.0",
            id="pinned-workspace-scope",
        ),
        pytest.param(
            True,
            "1.0.0",
            "organization",
            False,
            "at organization scope",
            id="pinned-org-scope",
        ),
        pytest.param(
            True,
            "3.5.2",
            "actor",
            False,
            "force=True",
            id="pinned-includes-force-hint",
        ),
        # Pinned with force — should pass
        pytest.param(True, None, None, True, None, id="pinned-forced"),
        pytest.param(True, "3.5.2", None, True, None, id="pinned-forced-with-version"),
        pytest.param(True, None, "actor", True, None, id="pinned-forced-with-scope"),
        pytest.param(
            True,
            "2.1.0",
            "workspace",
            True,
            None,
            id="pinned-forced-workspace",
        ),
        pytest.param(
            True,
            "1.0.0",
            "organization",
            True,
            None,
            id="pinned-forced-org",
        ),
    ],
)
def test__validate_not_already_pinned(
    is_pinned: bool,
    pinned_version: str | None,
    pin_scope: str | None,
    force: bool,
    expected_error: str | None,
) -> None:
    result = _validate_not_already_pinned(
        is_pinned=is_pinned,
        pinned_version=pinned_version,
        pin_scope=pin_scope,
        force=force,
    )
    if expected_error is None:
        assert result is None
    else:
        assert result is not None
        assert expected_error in result


def test__validate_not_already_pinned_full_message() -> None:
    """Verify the complete error message structure."""
    result = _validate_not_already_pinned(
        is_pinned=True,
        pinned_version="3.5.2",
        pin_scope="actor",
        force=False,
    )
    assert result is not None
    assert "Version override rejected" in result
    assert "already pinned" in result
    assert "version 3.5.2" in result
    assert "at actor scope" in result
    assert "ongoing rollout" in result
    assert "breaking-change migration" in result
    assert "force=True" in result


def test__validate_not_already_pinned_minimal_message() -> None:
    """Verify error message when no version or scope is provided."""
    result = _validate_not_already_pinned(
        is_pinned=True,
        pinned_version=None,
        pin_scope=None,
        force=False,
    )
    assert result is not None
    assert "already pinned" in result
    assert "force=True" in result


def test__validate_not_already_pinned_blocking_includes_major_version_note() -> None:
    """Verify blocking message includes note that major-version crossings are also blocked."""
    result = _validate_not_already_pinned(
        is_pinned=True,
        pinned_version="2.5.0",
        pin_scope="actor",
        force=False,
        target_version="3.0.0",
    )
    assert result is not None
    assert "already pinned" in result
    assert "force=True" in result
    # Should include note that even force=True would be blocked for major crossing
    assert "Even with force=True" in result
    assert "v2 -> v3" in result
    assert "breaking changes" in result


def test__validate_not_already_pinned_blocking_no_warning_same_major() -> None:
    """Verify blocking message does NOT include warning when same major."""
    result = _validate_not_already_pinned(
        is_pinned=True,
        pinned_version="2.5.0",
        pin_scope="actor",
        force=False,
        target_version="2.8.0",
    )
    assert result is not None
    assert "already pinned" in result
    assert "WARNING" not in result


def test__validate_not_already_pinned_blocking_no_warning_without_target() -> None:
    """Verify blocking message does NOT include warning when no target_version."""
    result = _validate_not_already_pinned(
        is_pinned=True,
        pinned_version="2.5.0",
        pin_scope="actor",
        force=False,
    )
    assert result is not None
    assert "already pinned" in result
    assert "WARNING" not in result


def test__validate_not_already_pinned_blocking_no_warning_without_pinned_version() -> (
    None
):
    """Verify no warning when pinned_version is None (can't compare)."""
    result = _validate_not_already_pinned(
        is_pinned=True,
        pinned_version=None,
        pin_scope="actor",
        force=False,
        target_version="3.0.0",
    )
    assert result is not None
    assert "already pinned" in result
    assert "WARNING" not in result


# ---------------------------------------------------------------------------
# _check_major_version_crossing (hard blocker — no override)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("existing_pinned_version", "target_version", "expected_error"),
    [
        # Same major — no error
        pytest.param("1.2.3", "1.5.0", None, id="same-major-upgrade"),
        pytest.param("2.0.0", "2.1.0", None, id="same-major-minor"),
        pytest.param("3.0.0", "3.0.1", None, id="same-major-patch"),
        pytest.param("0.1.0", "0.99.0", None, id="same-major-zero"),
        # Cross-major — should block
        pytest.param("1.2.3", "2.0.0", "v1 -> v2", id="cross-major-1-to-2"),
        pytest.param("2.5.0", "3.0.0", "v2 -> v3", id="cross-major-2-to-3"),
        pytest.param("0.1.0", "1.0.0", "v0 -> v1", id="cross-major-0-to-1"),
        pytest.param("3.0.0", "1.0.0", "v3 -> v1", id="cross-major-downgrade"),
        # Pre-release versions
        pytest.param("1.2.0-rc.1", "1.3.0-rc.2", None, id="rc-same-major"),
        pytest.param("1.2.0-rc.1", "2.0.0-rc.1", "v1 -> v2", id="rc-cross-major"),
        pytest.param(
            "1.2.0-dev.abc123",
            "2.0.0-dev.def456",
            "v1 -> v2",
            id="dev-cross-major",
        ),
        # Unparseable versions — no error (graceful)
        pytest.param("not-a-version", "1.0.0", None, id="unparseable-existing"),
        pytest.param("1.0.0", "not-a-version", None, id="unparseable-target"),
        pytest.param("garbage", "also-garbage", None, id="both-unparseable"),
        # None existing version — no error
        pytest.param(None, "2.0.0", None, id="none-existing"),
    ],
)
def test__check_major_version_crossing(
    existing_pinned_version: str | None,
    target_version: str,
    expected_error: str | None,
) -> None:
    result = _check_major_version_crossing(
        existing_pinned_version=existing_pinned_version,
        target_version=target_version,
    )
    if expected_error is None:
        assert result is None
    else:
        assert result is not None
        assert expected_error in result
        assert "blocked" in result
        assert "breaking changes" in result


def test__check_major_version_crossing_full_message() -> None:
    """Verify the complete error message structure."""
    result = _check_major_version_crossing(
        existing_pinned_version="2.5.0",
        target_version="3.0.0",
    )
    assert result is not None
    assert "blocked" in result
    assert "major version" in result
    assert "v2 -> v3" in result
    assert "breaking changes" in result
    assert "schema changes" in result
    assert "cannot be overridden" in result
