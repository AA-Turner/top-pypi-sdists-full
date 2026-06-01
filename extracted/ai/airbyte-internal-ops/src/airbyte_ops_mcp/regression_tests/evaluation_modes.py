# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Test evaluation modes for live tests.

This module provides evaluation modes that control how test failures are handled.

Based on airbyte-ci implementation:
https://github.com/airbytehq/airbyte/blob/master/airbyte-ci/connectors/live-tests/src/live_tests/commons/evaluation_modes.py
"""

from __future__ import annotations

from enum import Enum


class TestEvaluationMode(Enum):
    """Test evaluation modes.

    Tests may be run in "diagnostic" mode or "strict" mode.

    When run in "diagnostic" mode, validation failures won't fail the overall
    test run, but errors will still be surfaced in the test report.

    In "strict" mode, tests pass/fail as usual.

    Diagnostic mode is useful for tests that don't affect the overall
    functionality of the connector but test an ideal state.
    """

    DIAGNOSTIC = "diagnostic"
    STRICT = "strict"

    @classmethod
    def from_string(
        cls,
        value: str,
    ) -> TestEvaluationMode:
        """Parse evaluation mode from string."""
        value_lower = value.lower()
        if value_lower == "diagnostic":
            return cls.DIAGNOSTIC
        if value_lower == "strict":
            return cls.STRICT
        raise ValueError(
            f"Unknown evaluation mode: {value}. Must be 'diagnostic' or 'strict'."
        )
