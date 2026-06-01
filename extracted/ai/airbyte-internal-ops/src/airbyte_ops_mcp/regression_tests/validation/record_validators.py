# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Record validation functions for connector read output.

Based on airbyte-ci validation tests:
https://github.com/airbytehq/airbyte/blob/master/airbyte-ci/connectors/live-tests/src/live_tests/validation_tests/test_read.py
"""

from __future__ import annotations

from collections import defaultdict
from functools import reduce
from typing import TYPE_CHECKING, Any

import jsonschema
from airbyte_protocol.models import AirbyteMessage, AirbyteStateType
from airbyte_protocol.models import Type as AirbyteMessageType

from airbyte_ops_mcp.regression_tests.validation.catalog_validators import (
    ValidationResult,
)

if TYPE_CHECKING:
    from airbyte_ops_mcp.regression_tests.models import ExecutionResult


def validate_records_conform_to_schema(
    execution_result: ExecutionResult,
) -> ValidationResult:
    """Validate that all records conform to their stream schemas.

    Args:
        execution_result: The execution result containing records and catalog.

    Returns:
        ValidationResult indicating success or failure.
    """
    if not execution_result.configured_catalog:
        return ValidationResult.failure(
            "No configured catalog available for schema validation"
        )

    errors = []
    stream_schemas = {
        stream.stream.name: stream.stream.json_schema
        for stream in execution_result.configured_catalog.streams
    }

    for record in execution_result.get_records():
        stream_name = record.record.stream
        if stream_name not in stream_schemas:
            errors.append(f"Record for unknown stream '{stream_name}'")
            continue

        schema = stream_schemas[stream_name]
        try:
            jsonschema.validate(instance=record.record.data, schema=schema)
        except jsonschema.exceptions.ValidationError as e:
            errors.append(
                f"Record in stream '{stream_name}' does not conform to schema: "
                f"{e.message}"
            )

    if errors:
        return ValidationResult.failure(
            "Some records do not conform to their schemas",
            errors=errors[:10],  # Limit to first 10 errors
        )
    return ValidationResult.success("All records conform to their schemas")


def _extract_primary_key_value(
    record: dict[str, Any],
    primary_key: list[list[str]],
) -> dict[tuple[str, ...], Any]:
    """Extract primary key values from a record.

    Args:
        record: The record data.
        primary_key: List of primary key paths.

    Returns:
        Dictionary mapping primary key paths to their values.
    """
    pk_values = {}
    for pk_path in primary_key:
        pk_value: Any = reduce(
            lambda data, key: data.get(key) if isinstance(data, dict) else None,
            pk_path,
            record,
        )
        pk_values[tuple(pk_path)] = pk_value
    return pk_values


def validate_primary_keys_in_records(
    execution_result: ExecutionResult,
) -> ValidationResult:
    """Validate that all records have non-null primary key values.

    Args:
        execution_result: The execution result containing records and catalog.

    Returns:
        ValidationResult indicating success or failure.
    """
    if not execution_result.configured_catalog:
        return ValidationResult.failure(
            "No configured catalog available for primary key validation"
        )

    errors = []
    stream_pks: dict[str, list[list[str]]] = {}
    for stream in execution_result.configured_catalog.streams:
        if stream.primary_key:
            stream_pks[stream.stream.name] = stream.primary_key

    for record in execution_result.get_records():
        stream_name = record.record.stream
        if stream_name not in stream_pks:
            continue

        pk = stream_pks[stream_name]
        pk_values = _extract_primary_key_value(record.record.data, pk)

        for pk_path, value in pk_values.items():
            if value is None:
                errors.append(
                    f"Stream '{stream_name}': primary key {pk_path} has null value"
                )

    if errors:
        return ValidationResult.failure(
            "Some records have null primary key values",
            errors=errors[:10],  # Limit to first 10 errors
        )
    return ValidationResult.success("All records have valid primary key values")


def validate_state_messages_emitted(
    execution_result: ExecutionResult,
) -> ValidationResult:
    """Validate that state messages are emitted for each stream.

    Args:
        execution_result: The execution result containing messages.

    Returns:
        ValidationResult indicating success or failure.
    """
    if not execution_result.configured_catalog:
        return ValidationResult.failure(
            "No configured catalog available for state validation"
        )

    errors = []
    warnings = []

    configured_streams = {
        stream.stream.name for stream in execution_result.configured_catalog.streams
    }

    state_messages_per_stream: dict[str, list[AirbyteMessage]] = defaultdict(list)
    for message in execution_result.airbyte_messages:
        if (
            message.type == AirbyteMessageType.STATE
            and message.state.stream
            and message.state.stream.stream_descriptor
        ):
            stream_name = message.state.stream.stream_descriptor.name
            state_messages_per_stream[stream_name].append(message)

    for stream_name in configured_streams:
        if stream_name not in state_messages_per_stream:
            errors.append(f"No state messages emitted for stream '{stream_name}'")
            continue

        state_messages = state_messages_per_stream[stream_name]
        for state_msg in state_messages:
            if state_msg.state.type == AirbyteStateType.LEGACY:
                warnings.append(
                    f"Stream '{stream_name}' uses deprecated LEGACY state type"
                )

    result = ValidationResult(
        passed=len(errors) == 0,
        message=(
            "State messages validation completed"
            if len(errors) == 0
            else "Some streams are missing state messages"
        ),
        errors=errors,
        warnings=warnings,
    )
    return result


def validate_has_records(execution_result: ExecutionResult) -> ValidationResult:
    """Validate that at least one record was read.

    Args:
        execution_result: The execution result containing messages.

    Returns:
        ValidationResult indicating success or failure.
    """
    record_count = sum(1 for _ in execution_result.get_records())
    if record_count == 0:
        return ValidationResult.failure(
            "No records were read",
            errors=["At least one record should be read using the provided catalog"],
        )
    return ValidationResult.success(f"Read {record_count} records")


def validate_read_output(execution_result: ExecutionResult) -> list[ValidationResult]:
    """Run all read output validations.

    Args:
        execution_result: The execution result to validate.

    Returns:
        List of ValidationResult objects.
    """
    return [
        validate_has_records(execution_result),
        validate_records_conform_to_schema(execution_result),
        validate_primary_keys_in_records(execution_result),
        validate_state_messages_emitted(execution_result),
    ]
