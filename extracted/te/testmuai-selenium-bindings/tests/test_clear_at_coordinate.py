"""Tests for testmu_selenium._helpers.clear_at_coordinate.

Coordinate-based clear: move to (x, y), click, select-all (Ctrl+A), delete.
Thin wrapper over _clear_coord_runner, the proven gesture used by V2 canvas-coordinate
clear path. Driver-level helper (no element to heal).

Ported from the V2 Selenium coordinate-clear implementation (canvas branch).
"""
from unittest.mock import MagicMock, patch
import testmu_selenium


def test_clear_at_coordinate_is_public_export():
    """clear_at_coordinate is exported at the top level."""
    assert hasattr(testmu_selenium, "clear_at_coordinate")
    assert "clear_at_coordinate" in testmu_selenium.__all__


@patch("testmu_selenium._helpers.clear_at_coordinate._clear_coord_runner")
def test_clear_at_coordinate_delegates_to_coord_runner(mock_runner):
    """clear_at_coordinate delegates to _clear_coord_runner with (driver, x, y, ctx)."""
    driver = MagicMock()
    testmu_selenium.clear_at_coordinate(driver, 11, 22)

    mock_runner.assert_called_once()
    args, kwargs = mock_runner.call_args
    # Check positional args contain driver, x, y
    assert driver in args
    assert 11 in args and 22 in args
