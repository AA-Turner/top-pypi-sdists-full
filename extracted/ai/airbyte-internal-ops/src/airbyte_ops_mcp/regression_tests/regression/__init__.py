# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Regression test utilities for comparing connector outputs.

This module provides functions for comparing control and target connector
outputs to detect regressions in data integrity.

Based on airbyte-ci implementation:
https://github.com/airbytehq/airbyte/blob/master/airbyte-ci/connectors/live-tests/src/live_tests/regression_tests/test_read.py
"""

from airbyte_ops_mcp.regression_tests.regression.comparators import (
    ComparisonResult,
    RecordDiff,
    StreamComparisonResult,
    compare_all_records,
    compare_primary_keys,
    compare_record_counts,
    compare_record_schemas,
)

__all__ = [
    "ComparisonResult",
    "RecordDiff",
    "StreamComparisonResult",
    "compare_all_records",
    "compare_primary_keys",
    "compare_record_counts",
    "compare_record_schemas",
]
