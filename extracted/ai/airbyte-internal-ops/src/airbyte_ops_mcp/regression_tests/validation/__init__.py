# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Validation functions for connector output.

This module provides validation functions for verifying connector output
conforms to the Airbyte protocol and best practices.

Based on airbyte-ci validation tests:
https://github.com/airbytehq/airbyte/tree/master/airbyte-ci/connectors/live-tests/src/live_tests/validation_tests
"""

from airbyte_ops_mcp.regression_tests.validation.catalog_validators import (
    ValidationResult,
    validate_additional_properties_is_true,
    validate_catalog,
    validate_catalog_has_streams,
    validate_cursors_exist_in_schema,
    validate_no_duplicate_stream_names,
    validate_no_unresolved_refs,
    validate_primary_keys_exist_in_schema,
    validate_schemas_are_valid_json_schema,
    validate_streams_have_sync_modes,
)
from airbyte_ops_mcp.regression_tests.validation.record_validators import (
    validate_primary_keys_in_records,
    validate_records_conform_to_schema,
    validate_state_messages_emitted,
)

__all__ = [
    "ValidationResult",
    "validate_additional_properties_is_true",
    "validate_catalog",
    "validate_catalog_has_streams",
    "validate_cursors_exist_in_schema",
    "validate_no_duplicate_stream_names",
    "validate_no_unresolved_refs",
    "validate_primary_keys_exist_in_schema",
    "validate_primary_keys_in_records",
    "validate_records_conform_to_schema",
    "validate_schemas_are_valid_json_schema",
    "validate_state_messages_emitted",
    "validate_streams_have_sync_modes",
]
