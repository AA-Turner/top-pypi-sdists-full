# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Comparison functions for regression testing.

This module provides functions for comparing control and target connector
outputs to detect regressions in data integrity.

Based on airbyte-ci implementation:
https://github.com/airbytehq/airbyte/blob/master/airbyte-ci/connectors/live-tests/src/live_tests/regression_tests/test_read.py
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from typing import Any

from airbyte_protocol.models import AirbyteMessage
from deepdiff import DeepDiff

logger = logging.getLogger(__name__)

# Fields to exclude when comparing records (timestamps vary between runs)
EXCLUDE_PATHS = ["emitted_at"]


@dataclass
class RecordDiff:
    """Represents a diff between control and target records."""

    stream_name: str
    records_with_value_diff: list[dict[str, Any]] = field(default_factory=list)
    records_only_in_control: list[dict[str, Any]] = field(default_factory=list)
    records_only_in_target: list[dict[str, Any]] = field(default_factory=list)

    @property
    def has_diff(self) -> bool:
        return bool(
            self.records_with_value_diff
            or self.records_only_in_control
            or self.records_only_in_target
        )


@dataclass
class StreamComparisonResult:
    """Result of comparing a single stream between control and target."""

    stream_name: str
    passed: bool
    control_count: int = 0
    target_count: int = 0
    missing_pks: list[Any] = field(default_factory=list)
    extra_pks: list[Any] = field(default_factory=list)
    record_diff: RecordDiff | None = None
    schema_diff: dict[str, Any] | None = None
    message: str = ""


@dataclass
class ComparisonResult:
    """Result of comparing control and target connector outputs."""

    passed: bool
    stream_results: dict[str, StreamComparisonResult] = field(default_factory=dict)
    message: str = ""
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def failed_streams(self) -> list[str]:
        return [
            name for name, result in self.stream_results.items() if not result.passed
        ]


def compare_record_counts(
    control_records: dict[str, list[AirbyteMessage]],
    target_records: dict[str, list[AirbyteMessage]],
) -> ComparisonResult:
    """Compare record counts between control and target versions.

    This is the first level of regression testing - checking that the target
    version produces at least the same number of records as the control.

    Based on airbyte-ci implementation:
    https://github.com/airbytehq/airbyte/blob/master/airbyte-ci/connectors/live-tests/src/live_tests/regression_tests/test_read.py#L100-L131
    """
    stream_results: dict[str, StreamComparisonResult] = {}
    errors: list[str] = []

    all_streams = set(control_records.keys()) | set(target_records.keys())

    for stream_name in all_streams:
        control_count = len(control_records.get(stream_name, []))
        target_count = len(target_records.get(stream_name, []))
        delta = target_count - control_count

        passed = delta >= 0  # Target should have at least as many records

        message = ""
        if delta > 0:
            message = (
                f"Stream {stream_name} has {delta} more records in target "
                f"({target_count} vs {control_count})"
            )
        elif delta < 0:
            message = (
                f"Stream {stream_name} has {-delta} fewer records in target "
                f"({target_count} vs {control_count})"
            )
            errors.append(message)

        stream_results[stream_name] = StreamComparisonResult(
            stream_name=stream_name,
            passed=passed,
            control_count=control_count,
            target_count=target_count,
            message=message,
        )

    all_passed = all(r.passed for r in stream_results.values())
    return ComparisonResult(
        passed=all_passed,
        stream_results=stream_results,
        message="Record counts match" if all_passed else "Record count mismatch",
        errors=errors,
    )


def compare_primary_keys(
    control_records: dict[str, list[AirbyteMessage]],
    target_records: dict[str, list[AirbyteMessage]],
    primary_keys_per_stream: dict[str, list[str] | None],
) -> ComparisonResult:
    """Compare primary keys between control and target versions.

    This checks that all primary key values from the control version are
    present in the target version for each stream.

    Based on airbyte-ci implementation:
    https://github.com/airbytehq/airbyte/blob/master/airbyte-ci/connectors/live-tests/src/live_tests/regression_tests/test_read.py#L37-L98
    """
    stream_results: dict[str, StreamComparisonResult] = {}
    errors: list[str] = []
    warnings: list[str] = []

    for stream_name, control_msgs in control_records.items():
        pk_fields = primary_keys_per_stream.get(stream_name)
        if not pk_fields:
            warnings.append(
                f"No primary keys defined for stream {stream_name}, skipping PK check"
            )
            stream_results[stream_name] = StreamComparisonResult(
                stream_name=stream_name,
                passed=True,
                message="Skipped - no primary keys defined",
            )
            continue

        # Extract primary key values
        control_pks = _extract_pk_values(control_msgs, pk_fields)
        target_msgs = target_records.get(stream_name, [])
        target_pks = _extract_pk_values(target_msgs, pk_fields)

        missing_pks = list(control_pks - target_pks)
        extra_pks = list(target_pks - control_pks)

        passed = len(missing_pks) == 0

        message = ""
        if missing_pks:
            message = f"Stream {stream_name} is missing {len(missing_pks)} primary keys in target"
            errors.append(message)

        stream_results[stream_name] = StreamComparisonResult(
            stream_name=stream_name,
            passed=passed,
            control_count=len(control_pks),
            target_count=len(target_pks),
            missing_pks=missing_pks,
            extra_pks=extra_pks,
            message=message,
        )

    all_passed = all(r.passed for r in stream_results.values())
    return ComparisonResult(
        passed=all_passed,
        stream_results=stream_results,
        message="All primary keys present" if all_passed else "Missing primary keys",
        errors=errors,
        warnings=warnings,
    )


def compare_all_records(
    control_records: dict[str, list[AirbyteMessage]],
    target_records: dict[str, list[AirbyteMessage]],
    primary_keys_per_stream: dict[str, list[str] | None] | None = None,
    exclude_paths: list[str] | None = None,
) -> ComparisonResult:
    """Compare all records between control and target versions.

    This is the strictest level of regression testing - checking that all
    records are identical between control and target (excluding timestamps).

    Based on airbyte-ci implementation:
    https://github.com/airbytehq/airbyte/blob/master/airbyte-ci/connectors/live-tests/src/live_tests/regression_tests/test_read.py#L133-L183
    """
    if exclude_paths is None:
        exclude_paths = EXCLUDE_PATHS

    if primary_keys_per_stream is None:
        primary_keys_per_stream = {}

    stream_results: dict[str, StreamComparisonResult] = {}
    errors: list[str] = []

    all_streams = set(control_records.keys()) | set(target_records.keys())

    for stream_name in all_streams:
        control_msgs = control_records.get(stream_name, [])
        target_msgs = target_records.get(stream_name, [])

        if control_msgs and not target_msgs:
            errors.append(f"Stream {stream_name} is missing in target version")
            stream_results[stream_name] = StreamComparisonResult(
                stream_name=stream_name,
                passed=False,
                control_count=len(control_msgs),
                target_count=0,
                message=f"Stream {stream_name} is missing in target version",
            )
            continue

        pk_fields = primary_keys_per_stream.get(stream_name)
        if pk_fields:
            record_diff = _compare_records_with_pk(
                stream_name=stream_name,
                control_msgs=control_msgs,
                target_msgs=target_msgs,
                pk_fields=pk_fields,
                exclude_paths=exclude_paths,
            )
        else:
            record_diff = _compare_records_without_pk(
                stream_name=stream_name,
                control_msgs=control_msgs,
                target_msgs=target_msgs,
                exclude_paths=exclude_paths,
            )

        passed = not record_diff.has_diff
        message = ""
        if not passed:
            message = f"Stream {stream_name} has record differences"
            errors.append(message)

        stream_results[stream_name] = StreamComparisonResult(
            stream_name=stream_name,
            passed=passed,
            control_count=len(control_msgs),
            target_count=len(target_msgs),
            record_diff=record_diff,
            message=message,
        )

    all_passed = all(r.passed for r in stream_results.values())
    return ComparisonResult(
        passed=all_passed,
        stream_results=stream_results,
        message="All records match" if all_passed else "Record differences found",
        errors=errors,
    )


def compare_record_schemas(
    control_records: dict[str, list[AirbyteMessage]],
    target_records: dict[str, list[AirbyteMessage]],
) -> ComparisonResult:
    """Compare inferred schemas between control and target versions.

    This compares the structure of records (field names and types) between
    control and target versions.

    Based on airbyte-ci implementation:
    https://github.com/airbytehq/airbyte/blob/master/airbyte-ci/connectors/live-tests/src/live_tests/regression_tests/test_read.py#L185-L234
    """
    stream_results: dict[str, StreamComparisonResult] = {}
    errors: list[str] = []
    warnings: list[str] = []

    all_streams = set(control_records.keys()) | set(target_records.keys())

    for stream_name in all_streams:
        control_msgs = control_records.get(stream_name, [])
        target_msgs = target_records.get(stream_name, [])

        if not control_msgs:
            warnings.append(f"Stream {stream_name} has no records in control version")
            continue

        if not target_msgs:
            warnings.append(f"Stream {stream_name} has no records in target version")
            stream_results[stream_name] = StreamComparisonResult(
                stream_name=stream_name,
                passed=False,
                message=f"Stream {stream_name} has no records in target version",
            )
            errors.append(f"Stream {stream_name} has no records in target version")
            continue

        # Infer schema from first record of each
        control_schema = _infer_schema_from_record(control_msgs[0])
        target_schema = _infer_schema_from_record(target_msgs[0])

        diff = DeepDiff(
            control_schema,
            target_schema,
            ignore_order=True,
        )

        passed = not diff
        schema_diff = diff.to_dict() if diff else None

        message = ""
        if not passed:
            message = f"Stream {stream_name} has schema differences"
            errors.append(message)

        stream_results[stream_name] = StreamComparisonResult(
            stream_name=stream_name,
            passed=passed,
            control_count=len(control_msgs),
            target_count=len(target_msgs),
            schema_diff=schema_diff,
            message=message,
        )

    all_passed = all(r.passed for r in stream_results.values())
    return ComparisonResult(
        passed=all_passed,
        stream_results=stream_results,
        message="All schemas match" if all_passed else "Schema differences found",
        errors=errors,
        warnings=warnings,
    )


def _extract_pk_values(
    messages: list[AirbyteMessage],
    pk_fields: list[str],
) -> set[tuple]:
    """Extract primary key values from a list of messages."""
    pk_values: set[tuple] = set()
    for msg in messages:
        if msg.record and msg.record.data:
            pk_tuple = tuple(msg.record.data.get(field) for field in pk_fields)
            pk_values.add(pk_tuple)
    return pk_values


def _compare_records_with_pk(
    stream_name: str,
    control_msgs: list[AirbyteMessage],
    target_msgs: list[AirbyteMessage],
    pk_fields: list[str],
    exclude_paths: list[str],
) -> RecordDiff:
    """Compare records using primary keys for matching."""
    # Build lookup by PK
    control_by_pk: dict[tuple, dict] = {}
    for msg in control_msgs:
        if msg.record and msg.record.data:
            pk = tuple(msg.record.data.get(field) for field in pk_fields)
            control_by_pk[pk] = json.loads(msg.record.model_dump_json())

    target_by_pk: dict[tuple, dict] = {}
    for msg in target_msgs:
        if msg.record and msg.record.data:
            pk = tuple(msg.record.data.get(field) for field in pk_fields)
            target_by_pk[pk] = json.loads(msg.record.model_dump_json())

    control_pks = set(control_by_pk.keys())
    target_pks = set(target_by_pk.keys())

    # Records only in control
    records_only_in_control = [control_by_pk[pk] for pk in (control_pks - target_pks)]

    # Records only in target
    records_only_in_target = [target_by_pk[pk] for pk in (target_pks - control_pks)]

    # Records with value differences (same PK, different values)
    records_with_value_diff = []
    common_pks = control_pks & target_pks
    for pk in common_pks:
        control_record = control_by_pk[pk]
        target_record = target_by_pk[pk]
        diff = DeepDiff(
            control_record,
            target_record,
            ignore_order=True,
            exclude_paths=[f"root['{p}']" for p in exclude_paths],
        )
        if diff:
            records_with_value_diff.append(
                {
                    "pk": pk,
                    "control": control_record,
                    "target": target_record,
                    "diff": diff.to_dict(),
                }
            )

    return RecordDiff(
        stream_name=stream_name,
        records_with_value_diff=records_with_value_diff,
        records_only_in_control=records_only_in_control,
        records_only_in_target=records_only_in_target,
    )


def _compare_records_without_pk(
    stream_name: str,
    control_msgs: list[AirbyteMessage],
    target_msgs: list[AirbyteMessage],
    exclude_paths: list[str],
) -> RecordDiff:
    """Compare records without primary keys (order-independent comparison)."""
    control_records = [
        json.loads(msg.record.model_dump_json()) for msg in control_msgs if msg.record
    ]
    target_records = [
        json.loads(msg.record.model_dump_json()) for msg in target_msgs if msg.record
    ]

    diff = DeepDiff(
        control_records,
        target_records,
        ignore_order=True,
        exclude_paths=[f"root[*]['{p}']" for p in exclude_paths],
    )

    records_with_value_diff = []
    if diff:
        records_with_value_diff.append(
            {
                "diff": diff.to_dict(),
            }
        )

    return RecordDiff(
        stream_name=stream_name,
        records_with_value_diff=records_with_value_diff,
    )


def _infer_schema_from_record(message: AirbyteMessage) -> dict[str, str]:
    """Infer a simple schema (field -> type) from a record."""
    if not message.record or not message.record.data:
        return {}

    schema: dict[str, str] = {}
    for key, value in message.record.data.items():
        schema[key] = type(value).__name__
    return schema
