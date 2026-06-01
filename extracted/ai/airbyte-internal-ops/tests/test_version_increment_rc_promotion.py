# Copyright (c) 2025 Airbyte, Inc., all rights reserved.

"""Tests for RC version promotion validation in CheckVersionIncrement."""

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


@patch(f"{_VERSION_MODULE}._get_current_connector_version")
@patch(f"{_VERSION_MODULE}._get_master_metadata")
def test_rc_promotion_to_stable_passes(mock_master, mock_current, mock_connector):
    """Promoting an RC to its corresponding stable version should pass."""
    mock_master.return_value = {"dockerImageTag": "5.1.7-rc.1"}
    mock_current.return_value = semver.Version.parse("5.1.7")

    result = CheckVersionIncrement()._run(mock_connector)
    assert result.status == CheckStatus.PASSED


@pytest.mark.parametrize(
    "master_version, current_version, expected_stable",
    [
        pytest.param("5.1.7-rc.1", "5.2.0", "5.1.7", id="skip-to-new-minor"),
        pytest.param("5.1.7-rc.1", "6.0.0", "5.1.7", id="skip-to-new-major"),
        pytest.param("5.1.7-rc.1", "5.1.8", "5.1.7", id="skip-to-new-patch"),
    ],
)
@patch(f"{_VERSION_MODULE}._get_current_connector_version")
@patch(f"{_VERSION_MODULE}._get_master_metadata")
def test_rc_skip_to_different_version_fails(
    mock_master,
    mock_current,
    mock_connector,
    master_version,
    current_version,
    expected_stable,
):
    """Jumping from an RC to any version other than its stable promotion should fail."""
    mock_master.return_value = {"dockerImageTag": master_version}
    mock_current.return_value = semver.Version.parse(current_version)

    result = CheckVersionIncrement()._run(mock_connector)
    assert result.status == CheckStatus.FAILED
    assert "release candidate" in result.message.lower()
    assert expected_stable in result.message
