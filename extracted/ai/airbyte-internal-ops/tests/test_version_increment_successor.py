# Copyright (c) 2025 Airbyte, Inc., all rights reserved.

"""Tests for direct successor validation in CheckVersionIncrement."""

from unittest.mock import MagicMock, patch

import pytest
import semver

from airbyte_ops_mcp.connector_qa.checks.version import CheckVersionIncrement
from airbyte_ops_mcp.connector_qa.models import CheckStatus

_VERSION_MODULE = "airbyte_ops_mcp.connector_qa.checks.version.CheckVersionIncrement"


@pytest.fixture
def mock_connector(tmp_path):
    return MagicMock(
        code_directory=str(tmp_path),
        technical_name="mock-connector",
        metadata={"dockerImageTag": "1.0.0"},
    )


@pytest.mark.parametrize(
    "master_version, current_version",
    [
        pytest.param("6.0.2", "6.0.3", id="patch"),
        pytest.param("6.0.2", "6.1.0", id="minor"),
        pytest.param("6.0.2", "7.0.0", id="major"),
        pytest.param("6.0.2", "6.0.3-rc.1", id="patch-rc"),
        pytest.param("6.0.2", "6.1.0-rc.1", id="minor-rc"),
        pytest.param("6.0.2", "7.0.0-rc.1", id="major-rc"),
        pytest.param("5.1.7-rc.1", "5.1.7-rc.2", id="next-rc"),
        pytest.param("5.1.7-rc.1", "5.1.7", id="rc-promotion"),
        pytest.param(None, "3.4.5", id="new-connector"),
    ],
)
@patch(f"{_VERSION_MODULE}._get_current_connector_version")
@patch(f"{_VERSION_MODULE}._get_master_metadata")
def test_direct_successor_versions_pass(
    mock_master, mock_current, mock_connector, master_version, current_version
):
    """Direct successor versions and new connector versions should pass."""
    mock_master.return_value = (
        {"dockerImageTag": master_version} if master_version is not None else None
    )
    mock_current.return_value = semver.Version.parse(current_version)

    result = CheckVersionIncrement()._run(mock_connector)

    assert result.status == CheckStatus.PASSED


@pytest.mark.parametrize(
    "master_version, current_version, expected_versions",
    [
        pytest.param(
            "6.0.2",
            "6.0.4",
            "6.0.3, 6.1.0, 7.0.0, 6.0.3-rc.1, 6.1.0-rc.1, 7.0.0-rc.1",
            id="skipped-patch",
        ),
        pytest.param(
            "6.0.2",
            "6.1.1",
            "6.0.3, 6.1.0, 7.0.0, 6.0.3-rc.1, 6.1.0-rc.1, 7.0.0-rc.1",
            id="minor-with-patch",
        ),
        pytest.param(
            "6.0.2",
            "6.2.0",
            "6.0.3, 6.1.0, 7.0.0, 6.0.3-rc.1, 6.1.0-rc.1, 7.0.0-rc.1",
            id="skipped-minor",
        ),
        pytest.param(
            "6.0.2",
            "7.0.1",
            "6.0.3, 6.1.0, 7.0.0, 6.0.3-rc.1, 6.1.0-rc.1, 7.0.0-rc.1",
            id="major-with-patch",
        ),
        pytest.param(
            "6.0.2",
            "8.0.0",
            "6.0.3, 6.1.0, 7.0.0, 6.0.3-rc.1, 6.1.0-rc.1, 7.0.0-rc.1",
            id="skipped-major",
        ),
        pytest.param(
            "6.0.2",
            "6.0.3-rc.2",
            "6.0.3, 6.1.0, 7.0.0, 6.0.3-rc.1, 6.1.0-rc.1, 7.0.0-rc.1",
            id="later-first-rc",
        ),
        pytest.param(
            "5.1.7-rc.1",
            "5.1.7-rc.3",
            "5.1.7-rc.2, 5.1.7",
            id="skipped-rc",
        ),
    ],
)
@patch(f"{_VERSION_MODULE}._get_current_connector_version")
@patch(f"{_VERSION_MODULE}._get_master_metadata")
def test_skipped_successor_versions_fail(
    mock_master,
    mock_current,
    mock_connector,
    master_version,
    current_version,
    expected_versions,
):
    """Versions that skip a direct successor should fail with the options."""
    mock_master.return_value = {"dockerImageTag": master_version}
    mock_current.return_value = semver.Version.parse(current_version)

    result = CheckVersionIncrement()._run(mock_connector)

    assert result.status == CheckStatus.FAILED
    assert "skips a version" in result.message
    assert f"The next version must be one of: {expected_versions}" in result.message
