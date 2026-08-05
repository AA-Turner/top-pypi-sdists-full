# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Comparison functions for regression testing.

This module provides functions for comparing control and target connector
outputs to detect regressions in data integrity.

Schemas are compared as the connector *declares* them, in the spec and in the
discovered catalog, never as inferred from the records that came back: an
inferred schema describes the sample, so a field absent from one run's data
reads as a schema change and a field that changed type between two runs of the
same version reads as a regression.

Based on airbyte-ci implementation:
https://github.com/airbytehq/airbyte/blob/master/airbyte-ci/connectors/live-tests/src/live_tests/regression_tests/test_read.py
"""

from __future__ import annotations

import collections.abc
import contextlib
import hashlib
import json
import logging
import re
from collections import Counter
from collections.abc import Hashable
from dataclasses import dataclass, field
from functools import reduce
from pathlib import Path
from typing import Any

from airbyte_protocol.models import AirbyteMessage
from airbyte_protocol.models import Type as AirbyteMessageType
from deepdiff import DeepDiff
from pydantic import ValidationError

logger = logging.getLogger(__name__)

# Fields to exclude when comparing records (timestamps vary between runs)
EXCLUDE_PATHS = ["emitted_at"]

# Primary keys for a stream, in Airbyte protocol format: a list of field
# paths, where each path is a list of keys for nested traversal
# (e.g. [["id"]] or [["location", "id"], ["date"]]).
PrimaryKeys = list[list[str]]

# Caps on what is embedded in serialized summaries so reports stay readable
# and GITHUB_OUTPUT stays under size limits. The PK example lists are
# generous (5k covers any realistic triage; the *_count fields carry the
# full totals), and the DeepDiff payloads of the kept value-diff examples
# are embedded whole: bounded in number (MAX_EXAMPLE_DIFFS per stream) but
# not in size. Both caps are per stream, so a summary can still outgrow
# GITHUB_OUTPUT's ~1MiB-per-step limit -- `to_dict` enforces
# MAX_SUMMARY_BYTES as a global floor, degrading example payloads in
# stages (never counts or verdicts) only when a summary actually exceeds
# it. The JSON path alone degrades: the in-memory summary the HTML report
# renders is untouched.
MAX_EXAMPLE_PKS = 5_000
MAX_EXAMPLE_DIFFS = 5
# GITHUB_OUTPUT caps a step's outputs at 1MiB; leave headroom for the
# non-comparison keys that share the payload and the file.
MAX_SUMMARY_BYTES = 900_000
# Where the degraded stages land: example lists shrink to this length and
# error/warning lists to this count. The `*_count` fields keep the totals.
DEGRADED_EXAMPLE_CAP = 100
# A dict/list PK component is JSON-encoded to stay hashable; past this size
# the encoding is truncated and suffixed with a digest of the full value --
# a plain prefix truncation would make two distinct oversized values compare
# equal and silently merge their records. The digest keeps equality exact
# while PK examples and report lines stay bounded.
MAX_PK_COMPONENT_CHARS = 500


@dataclass
class RecordDiff:
    """Represents a diff between control and target records.

    The record lists hold capped examples (`MAX_EXAMPLE_DIFFS`) so a
    large-scale regression (e.g. a field added to every record) does not
    hold the whole stream in memory; the `*_count` fields carry the true
    totals. The counts are floored to the example list lengths on init,
    so constructing with just the lists keeps them consistent.
    """

    stream_name: str
    records_with_value_diff: list[dict[str, Any]] = field(default_factory=list)
    records_only_in_control: list[dict[str, Any]] = field(default_factory=list)
    records_only_in_target: list[dict[str, Any]] = field(default_factory=list)
    records_with_value_diff_count: int = 0
    records_only_in_control_count: int = 0
    records_only_in_target_count: int = 0
    # The PK paths the by-PK matching used, so the report can name the
    # identifying fields of each example instead of only their values.
    pk_paths: PrimaryKeys | None = None

    def __post_init__(self) -> None:
        self.records_with_value_diff_count = max(
            self.records_with_value_diff_count, len(self.records_with_value_diff)
        )
        self.records_only_in_control_count = max(
            self.records_only_in_control_count, len(self.records_only_in_control)
        )
        self.records_only_in_target_count = max(
            self.records_only_in_target_count, len(self.records_only_in_target)
        )

    @property
    def has_diff(self) -> bool:
        return bool(
            self.records_with_value_diff_count
            or self.records_only_in_control_count
            or self.records_only_in_target_count
        )


@dataclass
class StreamComparisonResult:
    """Result of comparing a single stream between control and target.

    `records_missing_pk_examples` holds up to `MAX_EXAMPLE_DIFFS` full copies
    of the records counted by `records_missing_pk`, so the report can show
    *which* records lack their declared PK values rather than only how many.

    The PK lists hold capped examples (`MAX_EXAMPLE_PKS`), like
    `RecordDiff`'s record lists: the merged summary of a failing run keeps
    every stream's result alive through report generation, and uncapped
    lists would break the "peak memory is the largest single stream" bound
    exactly on the runs that drop the most records. The `*_pk_count` fields
    carry the exact totals and are floored to the list lengths on init, so
    constructing with just the lists keeps them consistent.
    """

    stream_name: str
    passed: bool
    control_count: int = 0
    target_count: int = 0
    missing_pks: list[Any] = field(default_factory=list)
    extra_pks: list[Any] = field(default_factory=list)
    duplicate_pks: list[Any] = field(default_factory=list)
    missing_pk_count: int = 0
    extra_pk_count: int = 0
    duplicate_pk_count: int = 0
    # Occurrence count per duplicated PK value (always >= 2): how many
    # records shared it, keyed by the same tuples `duplicate_pks` lists.
    duplicate_pk_counts: dict[Any, int] = field(default_factory=dict)
    records_missing_pk: int = 0
    records_missing_pk_examples: list[dict[str, Any]] = field(default_factory=list)
    # The declared PK paths, so the report can say which fields are missing
    # on the example records rather than only that some are.
    pk_paths: PrimaryKeys | None = None
    record_diff: RecordDiff | None = None
    schema_diff: dict[str, Any] | None = None
    message: str = ""

    def __post_init__(self) -> None:
        self.missing_pk_count = max(self.missing_pk_count, len(self.missing_pks))
        self.extra_pk_count = max(self.extra_pk_count, len(self.extra_pks))
        self.duplicate_pk_count = max(self.duplicate_pk_count, len(self.duplicate_pks))


@dataclass
class ComparisonResult:
    """Result of comparing control and target connector outputs.

    `additive_only` says every difference found *adds* something -- a new
    stream, a new field -- and nothing was removed, retyped or re-declared. It
    is false for an unchanged run, which has no differences to classify: the
    caller uses it to decide whether a change is worth blocking a release over,
    and "nothing changed" is not that question.
    """

    passed: bool
    stream_results: dict[str, StreamComparisonResult] = field(default_factory=dict)
    message: str = ""
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    additive_only: bool = False

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
    primary_keys_per_stream: dict[str, PrimaryKeys | None],
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

        # Sorted so re-running the same regression surfaces the same subset
        # once a display cap bites; set iteration order varies per process
        # under hash randomization. `key=repr` because PK tuples can mix
        # types (int vs str vs None), which plain sorting cannot compare.
        # Stored capped (exact totals in the *_pk_count fields): the merged
        # summary keeps every stream's lists alive through report
        # generation, and no surface renders more than the cap anyway.
        missing = sorted(control_pks - target_pks, key=repr)
        extra = sorted(target_pks - control_pks, key=repr)
        missing_pk_count, extra_pk_count = len(missing), len(extra)
        missing_pks = missing[:MAX_EXAMPLE_PKS]
        extra_pks = extra[:MAX_EXAMPLE_PKS]

        passed = missing_pk_count == 0

        message = ""
        if missing_pks:
            # PK values are matched by exact value AND type: 123 and "123"
            # are different PKs. A target version that changes the PK value
            # type therefore reports every control PK as missing — call
            # that possibility out, since the records may all still be
            # there under the differently-typed values.
            message = (
                f"Stream {stream_name} is missing {missing_pk_count} primary "
                "key value(s) in target: records were dropped, or the PK "
                'value type changed between versions (e.g. 123 vs "123"), '
                "which also counts as missing"
            )
            errors.append(message)

        stream_results[stream_name] = StreamComparisonResult(
            stream_name=stream_name,
            passed=passed,
            control_count=len(control_pks),
            target_count=len(target_pks),
            missing_pks=missing_pks,
            extra_pks=extra_pks,
            missing_pk_count=missing_pk_count,
            extra_pk_count=extra_pk_count,
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


def check_pk_uniqueness(
    records_per_stream: dict[str, list[AirbyteMessage]],
    primary_keys_per_stream: dict[str, PrimaryKeys | None],
    version_label: str = "",
) -> ComparisonResult:
    """Check PK integrity of a single version's output, per stream.

    Two failure modes, both hard failures even when present in both
    versions (they indicate a broken primary key declaration or broken
    records, which breaks deduplication on the destination side):

    - Duplicate primary keys: the same PK value appears on more than one
      record, indicating the connector emitted the same entity more than
      once (e.g. broken pagination or slicing).
    - Missing primary key values: a record has no value (absent field or
      null) for one or more of its declared PK fields, indicating the
      catalog declares a primary key that is not actually present on the
      records. Such records are excluded from the duplicate count — they
      are reported through their own error instead.

    This runs on a single version's output; call it separately for control
    and target.

    Args:
        records_per_stream: Records grouped by stream name.
        primary_keys_per_stream: Primary key paths per stream; streams
            without a primary key are skipped.
        version_label: Optional label ("control"/"target") used in messages.
    """
    stream_results: dict[str, StreamComparisonResult] = {}
    errors: list[str] = []
    warnings: list[str] = []
    label = f" in {version_label}" if version_label else ""

    for stream_name, messages in records_per_stream.items():
        pk_paths = primary_keys_per_stream.get(stream_name)
        if not pk_paths:
            warnings.append(
                f"No primary keys defined for stream {stream_name}, "
                "skipping PK uniqueness check"
            )
            stream_results[stream_name] = StreamComparisonResult(
                stream_name=stream_name,
                passed=True,
                message="Skipped - no primary keys defined",
            )
            continue

        records_missing_pk = 0
        # Full copies of the first few offending records, so the report can
        # show what a record without its declared PK actually looks like.
        # Capped like the other example lists; the count stays exact.
        records_missing_pk_examples: list[dict[str, Any]] = []
        pk_counts: Counter[tuple] = Counter()
        for msg in messages:
            if not (msg.record and msg.record.data):
                continue
            pk = _extract_pk_tuple(msg.record.data, pk_paths)
            if _pk_has_missing_values(pk):
                records_missing_pk += 1
                if len(records_missing_pk_examples) < MAX_EXAMPLE_DIFFS:
                    records_missing_pk_examples.append(
                        json.loads(msg.record.model_dump_json())
                    )
            else:
                pk_counts[pk] += 1
        duplicates = {pk: count for pk, count in pk_counts.items() if count > 1}
        duplicate_pk_count = len(duplicates)
        # Capped like the other PK lists; Counter preserves first-seen order,
        # so the kept subset is deterministic.
        duplicate_pk_counts = dict(list(duplicates.items())[:MAX_EXAMPLE_PKS])
        duplicate_pks = list(duplicate_pk_counts)

        stream_errors: list[str] = []
        if duplicate_pks:
            stream_errors.append(
                f"Stream {stream_name} has {duplicate_pk_count} duplicate "
                f"primary key value(s){label}"
            )
        if records_missing_pk:
            stream_errors.append(
                f"Stream {stream_name} has {records_missing_pk} record(s) "
                f"with missing or null primary key value(s){label} — primary "
                f"key {pk_paths} is declared in the catalog but not present "
                "on the record data"
            )
        errors.extend(stream_errors)

        stream_results[stream_name] = StreamComparisonResult(
            stream_name=stream_name,
            passed=not stream_errors,
            duplicate_pks=duplicate_pks,
            duplicate_pk_counts=duplicate_pk_counts,
            duplicate_pk_count=duplicate_pk_count,
            records_missing_pk=records_missing_pk,
            records_missing_pk_examples=records_missing_pk_examples,
            pk_paths=pk_paths,
            message="; ".join(stream_errors),
        )

    all_passed = all(r.passed for r in stream_results.values())
    return ComparisonResult(
        passed=all_passed,
        stream_results=stream_results,
        message=(
            f"All primary keys unique and present{label}"
            if all_passed
            else f"Primary key integrity issues found{label}"
        ),
        errors=errors,
        warnings=warnings,
    )


def compare_all_records(
    control_records: dict[str, list[AirbyteMessage]],
    target_records: dict[str, list[AirbyteMessage]],
    primary_keys_per_stream: dict[str, PrimaryKeys | None] | None = None,
    exclude_paths: list[str] | None = None,
    directional: bool = False,
) -> ComparisonResult:
    """Compare all records between control and target versions.

    This is the strictest level of regression testing - checking that all
    records are identical between control and target (excluding timestamps).

    When `directional` is True, records that exist only in the target are
    not treated as a failure (the target having *more* data than the control
    is acceptable when both runs hit a live API without request caching);
    only value differences on matching records and records missing from the
    target fail the comparison. Directional mode only affects streams with
    primary keys — without a PK there is no way to match records, so the
    without-PK path is unchanged.

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

        if directional and pk_fields:
            passed = not (
                record_diff.records_with_value_diff_count
                or record_diff.records_only_in_control_count
            )
        else:
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


def compare_catalog_schemas(
    control_catalog: Any,
    target_catalog: Any,
) -> ComparisonResult:
    """Compare the discovered catalogs of the two versions, strictly.

    The discovered catalog is the source of truth for what a stream looks like:
    it is the schema the platform normalises and writes against, and it is
    declared by the connector rather than inferred from whichever record
    happened to come first. Any difference in a stream -- its `json_schema`, its
    supported sync modes, its declared primary key or cursor -- fails, including
    a stream that is new in the target: an intentional schema change still has
    to be reviewed before it ships, and the report says which kind it is.

    A missing catalog fails rather than passing vacuously: a `discover` that
    emitted no catalog cannot be shown to be unchanged.

    Streams are keyed by namespace and name, since `users` in two schemas of the
    same database source are two streams, and comparisons are ordered so that
    the most serious finding is the first one a truncated summary shows.

    Args:
        control_catalog: The `AirbyteCatalog` the control version discovered.
        target_catalog: The `AirbyteCatalog` the target version discovered.

    Returns:
        A per-stream result whose `schema_diff` holds the diff for that stream.
    """
    control_streams, control_problems = _streams_by_id(control_catalog)
    target_streams, target_problems = _streams_by_id(target_catalog)

    missing_side = _missing_sides(control_streams, target_streams)
    if missing_side:
        return ComparisonResult(
            passed=False,
            message=f"No discovered catalog to compare ({missing_side})",
            errors=[f"No discovered catalog to compare ({missing_side})"],
        )

    assert control_streams is not None and target_streams is not None

    problems = [
        f"The {side} catalog could not be read: {problem}"
        for side, side_problems in (
            ("control", control_problems),
            ("target", target_problems),
        )
        for problem in side_problems
    ]

    if not control_streams and not target_streams:
        # Two empty catalogs are not a match, they are an absence of evidence:
        # a config scoped to nothing, or a discover that degraded the same way
        # on both sides. Either way nothing about the schema was checked.
        message = "Neither version discovered any stream; nothing was compared"
        return ComparisonResult(
            passed=False, message=message, errors=[message, *problems]
        )

    stream_results: dict[str, StreamComparisonResult] = {}
    findings: list[tuple[int, str]] = [
        (_UNREADABLE_ENTRY, problem) for problem in problems
    ]
    # Counted by kind, because "changed in 3 streams" is a different sentence
    # from "2 new, 1 unreadable" and only one of them is true.
    tally = {_MISSING_STREAM: 0, _CHANGED_STREAM: 0, _NEW_STREAM: 0}
    # A catalog that only grew is still a change worth reporting, but it is not
    # the change a release is blocked over. An entry that could not be read is:
    # nothing is known about it.
    destructive = bool(problems)

    for stream_id in sorted(
        set(control_streams) | set(target_streams),
        # `None` sorts against `str` otherwise; the label is what a reader
        # sees, so order by that.
        key=_stream_label,
    ):
        # Two distinct streams can render the same label -- `public.users`
        # the name beside `users` in the `public` namespace -- and a shared
        # label must not collapse them into one result either.
        label = _unique_label(_stream_label(stream_id), stream_results)
        control_stream = control_streams.get(stream_id)
        target_stream = target_streams.get(stream_id)

        if target_stream is None:
            destructive = True
            rank, message = (
                _MISSING_STREAM,
                f"Stream {label} is missing from the target catalog",
            )
        elif control_stream is None:
            rank, message = _NEW_STREAM, f"Stream {label} is new in the target catalog"
        else:
            # Strictly: no `ignore_order`, because a reordered list in a
            # discovered catalog is a real difference -- `default_cursor_field`
            # and `source_defined_primary_key` are paths, where order is the
            # meaning.
            diff = DeepDiff(control_stream, target_stream)
            if diff and not _is_additive_diff(diff):
                destructive = True
            rank, message = (
                (_CHANGED_STREAM, f"Stream {label} has schema differences")
                if diff
                else (_CHANGED_STREAM, "")
            )
            stream_results[label] = StreamComparisonResult(
                stream_name=label,
                passed=not diff,
                schema_diff=_jsonable_diff(diff) if diff else None,
                message=message,
            )
            if message:
                tally[rank] += 1
                findings.append((rank, message))
            continue

        tally[rank] += 1
        findings.append((rank, message))
        stream_results[label] = StreamComparisonResult(
            stream_name=label,
            passed=False,
            message=message,
        )

    all_passed = not findings and all(
        result.passed for result in stream_results.values()
    )
    # Severity first: a summary that lists only the first few findings must not
    # spend them on three new streams while a changed type waits below.
    errors = [message for _rank, message in sorted(findings, key=lambda f: f[0])]

    return ComparisonResult(
        passed=all_passed,
        stream_results=stream_results,
        message=(
            f"Discovered catalog unchanged across {_count(len(stream_results), 'stream')}"
            if all_passed
            else _catalog_change_message(tally, len(problems))
        ),
        errors=errors,
        additive_only=not all_passed and not destructive,
    )


def normalize_primary_keys(primary_key: list | None) -> PrimaryKeys | None:
    """Normalize a primary key definition to the protocol's nested-path format.

    Accepts both `["id"]` (flat field names) and `[["id"]]` /
    `[["location", "id"]]` (nested paths) and returns the nested form.
    Returns None when no primary key is defined.
    """
    if not primary_key:
        return None
    return [[part] if isinstance(part, str) else list(part) for part in primary_key]


def _extract_pk_tuple(
    record_data: dict[str, Any],
    pk_paths: PrimaryKeys,
) -> tuple:
    """Extract a hashable primary key tuple from record data.

    Each path is traversed through nested dicts; a missing key yields None
    for that component. Unhashable values (lists/dicts) are JSON-encoded so
    the tuple stays usable as a dict/set key; an encoding past
    `MAX_PK_COMPONENT_CHARS` is truncated with a digest of the full value,
    keeping equality exact while the component stays bounded.
    """
    components = []
    for pk_path in pk_paths:
        value: Any = reduce(
            lambda data, key: data.get(key) if isinstance(data, dict) else None,
            pk_path,
            record_data,
        )
        if isinstance(value, (dict, list)):
            value = json.dumps(value, sort_keys=True, default=str)
            if len(value) > MAX_PK_COMPONENT_CHARS:
                digest = hashlib.sha256(value.encode()).hexdigest()[:16]
                value = f"{value[:MAX_PK_COMPONENT_CHARS]}…sha256:{digest}"
        components.append(value)
    return tuple(components)


def _pk_has_missing_values(pk_tuple: tuple) -> bool:
    """Whether any component of an extracted PK tuple is missing/null.

    Such a tuple cannot identify a record: distinct records missing their
    PK collide on the same tuple. Callers exclude these records from
    PK-based matching; `check_pk_uniqueness` reports them as an error.
    """
    return any(component is None for component in pk_tuple)


# The one DeepDiff verdict that only ever means "there is more here than there
# was". Everything else -- a value changed, a type changed, anything removed,
# any list moving -- is a redeclaration of something that already existed.
_ADDITIVE_DIFF_KEY = "dictionary_item_added"

# Where a new field can appear.
_STREAM_FIELDS_PREFIX = "root['json_schema']['properties']"

# A new field is a *direct child* of a field map: `…['properties']['email']`, or
# `…['address']['properties']['zip']` one level down. Anything deeper is a
# keyword landing on a field that already existed -- `['created_at']['format']`,
# an `airbyte_type`, an `enum` -- which redeclares how the platform types that
# column rather than adding anything.
_NEW_FIELD_PATH = re.compile(r"\['properties'\]\['[^']+'\]$")

# A key of the stream itself, e.g. `root['is_file_based']`.
_STREAM_KEY_PATH = re.compile(r"^root\['([^']+)'\]$")

# The stream-level keys whose *appearance* changes how the stream is read or
# where it lands, rather than declaring something new about it. Everything else
# a stream grows is metadata: the CDK adds such keys on a routine base-image
# bump -- `is_file_based` and `is_resumable` are the current examples -- and
# treating each new one as destructive would redden `discover` for every
# certified connector until someone extended a list. Naming the keys that
# matter, rather than the ones that do not, is what makes that self-correcting.
#
# These are the protocol's own snake_case field names, which is what both sides
# of this comparison carry: a catalog read from a connector's `discover`. A
# camelCase catalog -- the Cloud API's shape, `sourceDefinedPrimaryKey` -- would
# slip a behaviour key past the exemption as metadata, so add those spellings
# here if such a catalog ever reaches this function.
_STREAM_BEHAVIOUR_KEYS = frozenset(
    {
        "default_cursor_field",
        "json_schema",
        "name",
        "namespace",
        "source_defined_cursor",
        "source_defined_primary_key",
        "supported_sync_modes",
    }
)


def _is_additive_diff(diff: DeepDiff) -> bool:
    """Whether a stream's diff only adds -- a field, or metadata about itself."""
    if set(diff.keys()) != {_ADDITIVE_DIFF_KEY}:
        return False

    return all(_is_additive_path(str(path)) for path in diff[_ADDITIVE_DIFF_KEY])


def _is_additive_path(path: str) -> bool:
    """Whether one added path is growth rather than a redeclaration."""
    if path.startswith(_STREAM_FIELDS_PREFIX):
        return bool(_NEW_FIELD_PATH.search(path))

    stream_key = _STREAM_KEY_PATH.match(path)

    return bool(stream_key) and stream_key.group(1) not in _STREAM_BEHAVIOUR_KEYS


# How the catalog findings are ordered before anything truncates them. An entry
# that could not be read comes first: not knowing what a stream declares is
# worse than knowing it changed.
_UNREADABLE_ENTRY = 0
_MISSING_STREAM = 1
_CHANGED_STREAM = 2
_NEW_STREAM = 3


def _catalog_change_message(tally: dict[int, int], unreadable: int) -> str:
    """Say what changed, by kind.

    Counting every finding as a changed stream made the sentence lie in two
    directions at once: a stream that is new is not changed, and an entry that
    could not be read is not a stream at all.
    """
    clauses = [
        clause
        for count, clause in (
            (
                tally[_MISSING_STREAM],
                f"{_count(tally[_MISSING_STREAM], 'stream')} missing from the target",
            ),
            (
                tally[_CHANGED_STREAM],
                f"{_count(tally[_CHANGED_STREAM], 'stream')} changed",
            ),
            (
                tally[_NEW_STREAM],
                f"{_count(tally[_NEW_STREAM], 'stream')} new in the target",
            ),
            (
                unreadable,
                "1 unreadable entry"
                if unreadable == 1
                else f"{unreadable} unreadable entries",
            ),
        )
        if count
    ]

    return f"Discovered catalog: {', '.join(clauses)}"


def compare_specs(
    control_spec: Any,
    target_spec: Any,
) -> ComparisonResult:
    """Compare the two versions' specs, allowing backward-compatible additions.

    A spec is the contract with every existing config, so the rule is
    compatibility rather than equality: a new optional property passes, because
    no saved config becomes invalid, while a removed property, a changed type or
    a property that has become required fails, because saved configs do. Purely
    descriptive changes -- a title, a description, an example -- pass and are
    reported as such; a config field *named* `description` is still compared,
    since the exemption is by position, not by name.

    A missing spec fails rather than passing vacuously.

    Args:
        control_spec: The `ConnectorSpecification` the control version emitted.
        target_spec: The `ConnectorSpecification` the target version emitted.

    Returns:
        A result whose `errors` are the breaking changes and whose `warnings`
        are the compatible ones, both as reviewer-readable sentences.
    """
    control = _to_plain_dict(control_spec)
    target = _to_plain_dict(target_spec)

    missing_side = _missing_sides(control, target)
    if missing_side:
        return ComparisonResult(
            passed=False,
            message=f"No spec to compare ({missing_side})",
            errors=[f"No spec to compare ({missing_side})"],
        )

    assert control is not None and target is not None

    if not control.get("connectionSpecification") and not target.get(
        "connectionSpecification"
    ):
        # The same rule the discovered catalog follows: two sides that declare
        # nothing are not a match, they are an absence of evidence. A connector
        # that genuinely takes no config is caught by this too -- deliberately,
        # since a spec command that returns an empty schema is worth a look
        # either way.
        message = "Neither version declared a connection specification"
        return ComparisonResult(passed=False, message=message, errors=[message])

    breaking: list[str] = []
    compatible: list[str] = []
    _diff_spec_node(control, target, "", None, False, breaking, compatible)

    if breaking:
        message = f"Spec has {_count(len(breaking), 'backward-incompatible change')}"
    elif compatible:
        message = f"Spec changed compatibly ({_count(len(compatible), 'change')})"
    else:
        message = "Spec is unchanged"

    return ComparisonResult(
        passed=not breaking,
        message=message,
        errors=breaking,
        warnings=compatible,
    )


# Keys whose value documents a property rather than constraining it. A change
# under one of these cannot invalidate a saved config, so it is reported and not
# failed -- otherwise every reworded description would fail a release.
_SPEC_DOC_KEYS = frozenset(
    {
        "always_show",
        "changelogUrl",
        "description",
        "display_type",
        "documentationUrl",
        "examples",
        "group",
        "order",
        "pattern_descriptor",
        "title",
    }
)

# Keys whose value maps *config field names* to schemas. Their keys are names a
# connector chose, so nothing inside them is a schema keyword: a field called
# `description` is a field, and a field called `properties` has a title of its
# own. Every classification below therefore asks where a key sits, not what it
# is called.
_SPEC_PROPERTY_MAP_KEYS = frozenset(
    {"$defs", "definitions", "patternProperties", "properties"}
)

# Keys that constrain what a config may say. Adding one narrows the set of valid
# configs and breaks the ones outside it; removing one only widens it.
_SPEC_CONSTRAINT_KEYS = frozenset(
    {
        "additionalProperties",
        "const",
        "enum",
        "exclusiveMaximum",
        "exclusiveMinimum",
        "format",
        "maxItems",
        "maxLength",
        "maxProperties",
        "maximum",
        "minItems",
        "minLength",
        "minProperties",
        "minimum",
        "multipleOf",
        "pattern",
        "type",
        "uniqueItems",
    }
)

# Boolean constraints, and the value that is the strict one. `pattern` and
# `format` have no such direction -- a regex is not comparable to another regex
# -- so a change to one stays a failure and the docs say so.
_SPEC_STRICT_BOOLEAN = {"additionalProperties": False, "uniqueItems": True}

# Numeric bounds, and the direction that relaxes them.
_SPEC_BOUNDS_RELAXED_BY_GROWING = frozenset(
    {"exclusiveMaximum", "maxItems", "maxLength", "maxProperties", "maximum"}
)
_SPEC_BOUNDS_RELAXED_BY_SHRINKING = frozenset(
    {"exclusiveMinimum", "minItems", "minLength", "minProperties", "minimum"}
)

# Keys that decide the *shape* of a node rather than constrain a value. One
# appearing or disappearing rewrites what a config for this node looks like.
_SPEC_STRUCTURE_KEYS = frozenset({"$ref", "allOf", "anyOf", "items", "oneOf"})

# Keys whose value is a set of allowed values rather than an ordered sequence.
# Everything else -- `path_in_connector_config`, `predicate_key`, a tuple-form
# `items` -- is positional, where order and length carry meaning. `type` and
# `examples` are set-valued too but never arrive here: one is compared by
# `_diff_type` and the other is documentation, both decided before a list is
# reached.
_SPEC_SET_VALUED_KEYS = frozenset({"enum", "supported_destination_sync_modes"})

# Keys holding alternative shapes for the same node, matched by discriminator
# rather than by position: reordering a connector's auth methods is a no-op the
# platform resolves through the branch's `const`, not through its index.
_SPEC_BRANCH_KEYS = frozenset({"anyOf", "oneOf"})


def _diff_spec_node(
    control: Any,
    target: Any,
    path: str,
    key: str | None,
    is_property_map: bool,
    breaking: list[str],
    compatible: list[str],
) -> None:
    """Walk one node of the spec, recording changes as breaking or compatible.

    Args:
        control: The node as the control version declared it.
        target: The same node as the target version declares it.
        path: Dotted path to the node, for the message a reviewer reads.
        key: The key this node sits under, which decides how a list under it is
            compared. `None` at the root.
        is_property_map: Whether this node maps config field names to schemas
            rather than schema keywords to values.
        breaking: Accumulates the changes that invalidate a saved config.
        compatible: Accumulates the changes that do not.
    """
    if control == target:
        return

    if isinstance(control, dict) and isinstance(target, dict):
        _diff_spec_object(control, target, path, is_property_map, breaking, compatible)
        return

    if isinstance(control, list) and isinstance(target, list):
        _diff_spec_list(control, target, path, key, breaking, compatible)
        return

    breaking.append(
        f"{_label(path)} changed from {_brief(control)} to {_brief(target)}"
    )


def _diff_spec_object(
    control: dict[str, Any],
    target: dict[str, Any],
    path: str,
    is_property_map: bool,
    breaking: list[str],
    compatible: list[str],
) -> None:
    """Compare two schema nodes, or two maps of config fields, key by key."""
    # `required` is compared whether or not the control node had the key: a node
    # that gains its first `required` list has made optional fields mandatory,
    # which is the same break as adding a name to an existing one.
    required_handled = not is_property_map and _diff_required(
        control.get("required"), target.get("required"), path, breaking, compatible
    )

    for key in control:
        if required_handled and key == "required":
            continue

        child_path = _child_path(path, key)

        if key not in target:
            _record_removed_key(key, child_path, is_property_map, breaking, compatible)
            continue

        if control[key] == target[key]:
            continue

        _diff_spec_member(
            key,
            control[key],
            target[key],
            child_path,
            is_property_map,
            breaking,
            compatible,
        )

    for key in target:
        if key in control or (required_handled and key == "required"):
            continue

        _record_added_key(
            key, _child_path(path, key), is_property_map, breaking, compatible
        )


def _record_removed_key(
    key: str,
    child_path: str,
    is_property_map: bool,
    breaking: list[str],
    compatible: list[str],
) -> None:
    """Classify a key the target no longer declares."""
    label = _label(child_path)

    if is_property_map:
        breaking.append(f"{label} was removed")
    elif key in _SPEC_DOC_KEYS:
        compatible.append(f"{label} was removed (documentation)")
    elif key == "default":
        compatible.append(f"{label} was removed (changes behaviour, not validity)")
    elif key in _SPEC_CONSTRAINT_KEYS:
        compatible.append(f"{label} was removed, widening what a config may set")
    else:
        breaking.append(f"{label} was removed")


def _record_added_key(
    key: str,
    child_path: str,
    is_property_map: bool,
    breaking: list[str],
    compatible: list[str],
) -> None:
    """Classify a key only the target declares.

    An added *property* is the additive case the whole rule exists for. An added
    *constraint* is its opposite and used to be waved through here: a node that
    grows an `enum`, a `pattern` or `additionalProperties: false` rejects configs
    it accepted yesterday.
    """
    label = _label(child_path)

    if is_property_map or key in _SPEC_DOC_KEYS or key in _SPEC_PROPERTY_MAP_KEYS:
        compatible.append(f"{label} was added")
    elif key == "default":
        compatible.append(f"{label} was added (changes behaviour, not validity)")
    elif key in _SPEC_CONSTRAINT_KEYS:
        breaking.append(f"{label} was added, narrowing what a config may set")
    elif key in _SPEC_STRUCTURE_KEYS:
        breaking.append(f"{label} was added, changing the shape of this node")
    else:
        compatible.append(f"{label} was added")


def _diff_spec_member(
    key: str,
    control_value: Any,
    target_value: Any,
    child_path: str,
    is_property_map: bool,
    breaking: list[str],
    compatible: list[str],
) -> None:
    """Compare one key both versions declare, differently."""
    label = _label(child_path)

    if not is_property_map:
        if key in _SPEC_DOC_KEYS:
            compatible.append(f"{label} changed (documentation)")
            return

        if key == "default":
            compatible.append(
                f"{label} changed from {_brief(control_value)} to "
                f"{_brief(target_value)} (changes behaviour, not validity)"
            )
            return

        if key == "type":
            _diff_type(control_value, target_value, label, breaking, compatible)
            return

        if isinstance(control_value, bool) and isinstance(target_value, bool):
            switch = _diff_boolean_constraint(key, target_value, label)
            if switch is not None:
                (compatible if switch[0] else breaking).append(switch[1])
                return

        if _is_number(control_value) and _is_number(target_value):
            bound = _diff_bound(key, control_value, target_value, label)
            if bound is not None:
                (compatible if bound[0] else breaking).append(bound[1])
                return

    _diff_spec_node(
        control_value,
        target_value,
        child_path,
        key,
        not is_property_map and key in _SPEC_PROPERTY_MAP_KEYS,
        breaking,
        compatible,
    )


def _diff_type(
    control_value: Any,
    target_value: Any,
    label: str,
    breaking: list[str],
    compatible: list[str],
) -> None:
    """Compare two `type` declarations as the sets of types they allow.

    `"string"` becoming `["null", "string"]` is the shape every CDK-generated
    spec takes when a field becomes nullable, and it accepts strictly more than
    before -- comparing the raw values would call that a break.
    """
    control_types = _as_type_set(control_value)
    target_types = _as_type_set(target_value)

    removed = sorted(control_types - target_types)
    added = sorted(target_types - control_types)

    if removed:
        breaking.append(f"{label} no longer allows {', '.join(removed)}")
    if added:
        compatible.append(f"{label} also allows {', '.join(added)}")


def _as_type_set(value: Any) -> set[str]:
    """A `type` declaration as a set, whether it was given as one or not."""
    if isinstance(value, list):
        return {str(entry) for entry in value}

    return {str(value)}


def _diff_boolean_constraint(
    key: str,
    target_value: bool,
    label: str,
) -> tuple[bool, str] | None:
    """Classify a flipped boolean constraint, or `None` when `key` is not one.

    Returns `(compatible, message)`. Two constraints are booleans with an
    unambiguous strict direction, and both were failing in the relaxing
    direction: unsealing an object (`additionalProperties: false -> true`)
    accepts configs it used to reject, and so does dropping `uniqueItems`.
    Deleting either key was already treated as the relaxation it is; flipping
    the value is the same change written differently.
    """
    strict_value = _SPEC_STRICT_BOOLEAN.get(key)
    if strict_value is None:
        return None

    tightened = target_value == strict_value
    verb = "tightened to" if tightened else "relaxed to"

    return not tightened, f"{label} {verb} {target_value!r}"


def _diff_bound(
    key: str,
    control_value: float,
    target_value: float,
    label: str,
) -> tuple[bool, str] | None:
    """Classify a moved numeric bound, or `None` when `key` is not one.

    Returns `(compatible, message)`. Raising a `maximum` or lowering a `minimum`
    admits configs that were invalid before and cannot break one that was valid.
    """
    if key in _SPEC_BOUNDS_RELAXED_BY_GROWING:
        relaxed = target_value > control_value
    elif key in _SPEC_BOUNDS_RELAXED_BY_SHRINKING:
        relaxed = target_value < control_value
    else:
        return None

    verb = "relaxed" if relaxed else "tightened"

    return relaxed, f"{label} {verb} from {control_value!r} to {target_value!r}"


def _is_number(value: Any) -> bool:
    """Whether a value is a JSON number, excluding `True`/`False`."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _diff_spec_list(
    control: list[Any],
    target: list[Any],
    path: str,
    key: str | None,
    breaking: list[str],
    compatible: list[str],
) -> None:
    """Compare two lists in a spec, by what the list under `key` means.

    `oneOf` holds alternative shapes and is matched by discriminator. An `enum`
    or a `type` union is a set of allowed values, so dropping one narrows what a
    saved config may say and breaks while adding one does not. Everything else
    is positional: in `path_in_connector_config`, `["credentials", "client_id"]`
    is a different location from `["client_id"]`, not a wider one.
    """
    if key in _SPEC_BRANCH_KEYS:
        _diff_spec_branches(control, target, path, breaking, compatible)
        return

    if key in _SPEC_SET_VALUED_KEYS:
        # By membership, not by position, and whatever the entries are: JSON
        # Schema says an `enum` is a set, so an object-valued one widens the same
        # way a string-valued one does. Requiring scalars here made the two read
        # as opposite verdicts on the same change.
        for entry in [entry for entry in control if entry not in target]:
            breaking.append(f"{_label(path)} no longer allows {_brief(entry)}")
        for entry in [entry for entry in target if entry not in control]:
            compatible.append(f"{_label(path)} also allows {_brief(entry)}")
        return

    for index, control_entry in enumerate(control):
        child_path = f"{path}[{index}]"
        if index >= len(target):
            breaking.append(f"{_label(child_path)} was removed")
            continue
        _diff_spec_node(
            control_entry, target[index], child_path, key, False, breaking, compatible
        )

    for index in range(len(control), len(target)):
        breaking.append(
            f"{_label(f'{path}[{index}]')} was added, changing an ordered list"
        )


def _diff_spec_branches(
    control: list[Any],
    target: list[Any],
    path: str,
    breaking: list[str],
    compatible: list[str],
) -> None:
    """Compare `oneOf` branches, matched by what identifies them.

    Promoting OAuth above API-key authentication is one of the most common spec
    edits there is, and it is a no-op: the platform picks the branch by its
    discriminating `const`, not by its index. Compared positionally it reads as
    every field of both branches being replaced by the other's -- red, and
    telling the reviewer that fields were removed which are still there.

    A branch that carries a discriminator and finds no partner is reported as
    removed or added rather than diffed against an unrelated branch. Only
    branches with nothing to identify them fall back to their position. Paths in
    the messages follow the control's ordering, which is the version the
    reviewer is comparing against.
    """
    target_by_key = _branches_by_key(target)
    matched_targets: set[int] = set()
    unkeyed_control: list[tuple[int, Any]] = []

    for index, branch in enumerate(control):
        branch_key = _branch_key(branch)

        if branch_key is None:
            unkeyed_control.append((index, branch))
            continue

        target_index = target_by_key.get(branch_key)
        if target_index is None:
            breaking.append(f"{_label(f'{path}[{index}]')} was removed")
            continue

        matched_targets.add(target_index)
        _diff_spec_node(
            branch,
            target[target_index],
            f"{path}[{index}]",
            None,
            False,
            breaking,
            compatible,
        )

    unkeyed_target: list[tuple[int, Any]] = []
    for index, branch in enumerate(target):
        if index in matched_targets:
            continue
        if _branch_key(branch) is not None:
            compatible.append(f"{_label(f'{path}[{index}]')} was added")
            continue
        unkeyed_target.append((index, branch))

    for (control_index, control_branch), (_, target_branch) in zip(
        unkeyed_control, unkeyed_target
    ):
        _diff_spec_node(
            control_branch,
            target_branch,
            f"{path}[{control_index}]",
            None,
            False,
            breaking,
            compatible,
        )

    for control_index, _ in unkeyed_control[len(unkeyed_target) :]:
        breaking.append(f"{_label(f'{path}[{control_index}]')} was removed")

    for target_index, _ in unkeyed_target[len(unkeyed_control) :]:
        compatible.append(f"{_label(f'{path}[{target_index}]')} was added")


def _branches_by_key(branches: list[Any]) -> dict[tuple[str, Any], int]:
    """Index branches by discriminator, dropping any the index cannot separate."""
    indexed: dict[tuple[str, Any], int] = {}
    duplicated: set[tuple[str, Any]] = set()

    for index, branch in enumerate(branches):
        branch_key = _branch_key(branch)
        if branch_key is None:
            continue
        if branch_key in indexed:
            duplicated.add(branch_key)
            continue
        indexed[branch_key] = index

    for branch_key in duplicated:
        del indexed[branch_key]

    return indexed


def _branch_key(branch: Any) -> tuple[str, Any] | None:
    """What identifies a `oneOf` branch across versions, if anything does.

    A single-valued property -- `auth_type: {const: "oauth2.0"}` -- is what the
    platform itself discriminates on. A title is the next best thing, and a
    branch with neither is left to its position.

    When a branch carries more than one discriminator, the smallest property
    name wins. Taking whichever came first in the dict made the key depend on
    declaration order, so reordering a branch's own properties gave the two
    sides different keys, and a compatible edit read as one auth method removed
    and another added.
    """
    if not isinstance(branch, dict):
        return None

    properties = branch.get("properties")
    if isinstance(properties, dict):
        discriminators = sorted(
            (str(name), value)
            for name, schema in properties.items()
            if isinstance(schema, dict)
            for value in (_single_valued(schema),)
            if value is not None
        )
        if discriminators:
            return discriminators[0]

    title = branch.get("title")

    return ("title", title) if isinstance(title, str) else None


def _single_valued(schema: dict[str, Any]) -> Any | None:
    """The one value a property may take, if its schema pins it to one."""
    value = schema.get("const")
    if value is None:
        enum = schema.get("enum")
        value = enum[0] if isinstance(enum, list) and len(enum) == 1 else None

    return value if isinstance(value, Hashable) else None


def _diff_required(
    control_required: Any,
    target_required: Any,
    path: str,
    breaking: list[str],
    compatible: list[str],
) -> bool:
    """Compare the `required` list of one schema node.

    Requiring a property that was optional invalidates every saved config that
    omitted it, whether the property is new, whether it was already required
    somewhere else, and whether the node had a `required` list at all before.
    Dropping a requirement is a relaxation.

    Returns:
        Whether `required` was compared here. A node whose `required` is not a
        list of names is left to the ordinary comparison, which reports it as
        the malformed spec it is.
    """
    if control_required is None and target_required is None:
        return False

    control_names = [] if control_required is None else control_required
    target_names = [] if target_required is None else target_required

    if not _is_name_list(control_names) or not _is_name_list(target_names):
        return False

    node = _label(path)
    for name in target_names:
        if name not in control_names:
            breaking.append(f"{node}: `{name}` is now required")
    for name in control_names:
        if name not in target_names:
            compatible.append(f"{node}: `{name}` is no longer required")

    return True


def _is_name_list(value: Any) -> bool:
    """Whether a value is a `required`-style list of property names."""
    return isinstance(value, list) and all(isinstance(entry, str) for entry in value)


def _child_path(path: str, key: str) -> str:
    """The dotted path of `key` inside the node at `path`."""
    return f"{path}.{key}" if path else key


def _label(path: str) -> str:
    """The name a reviewer sees for a spec path."""
    return f"`{path}`" if path else "the spec"


# How much of a value a finding quotes. A node that changed shape -- an object
# that became a list -- would otherwise quote both whole subtrees, and a hundred
# of those defeat the payload bound that counts findings but not their length.
_MAX_VALUE_CHARS = 120


def _brief(value: Any) -> str:
    """A value as a finding should quote it: readable, and bounded."""
    text = repr(value)

    return text if len(text) <= _MAX_VALUE_CHARS else f"{text[:_MAX_VALUE_CHARS]}…"


def _count(quantity: int, noun: str) -> str:
    """`1 stream`, `2 streams` -- the messages are read by people."""
    return f"{quantity} {noun}" if quantity == 1 else f"{quantity} {noun}s"


def _missing_sides(control: Any, target: Any) -> str:
    """Name the sides that produced nothing to compare, or `""` if both did."""
    missing = [
        name
        for name, value in (("control", control), ("target", target))
        if value is None
    ]
    if not missing:
        return ""

    return f"missing on the {' and '.join(missing)}"


def _to_plain_dict(value: Any) -> dict[str, Any] | None:
    """Normalise a protocol object to plain JSON-compatible data.

    Accepts the pydantic models an `ExecutionResult` yields as well as the plain
    dicts saved artifacts and tests carry, so a comparator never depends on
    which of the two it was handed.
    """
    if value is None:
        return None

    if isinstance(value, dict):
        return value

    model_dump = getattr(value, "model_dump", None)
    if callable(model_dump):
        return model_dump(mode="json", exclude_none=True)

    raise TypeError(f"Cannot compare a {type(value).__name__} as JSON data")


def _streams_by_id(
    catalog: Any,
) -> tuple[dict[tuple[str | None, str], dict[str, Any]] | None, list[str]]:
    """Index a discovered catalog's streams, and say what could not be indexed.

    The key is `(namespace, name)`, not `name`: a database source discovers
    `public.users` and `reporting.users` as two streams, and indexing on the
    name alone would let one silently shadow the other -- taking a real schema
    change in the shadowed stream with it. It is a pair rather than the
    `namespace.name` string it displays as, so a stream literally named
    `public.users` is not the same key as `users` in the `public` namespace.

    Returns:
        The index and the problems found, or `(None, [])` when there is no
        catalog at all. A stream that cannot be indexed is reported rather than
        dropped: an unreadable entry is not an unchanged one.
    """
    plain = _to_plain_dict(catalog)
    if plain is None:
        return None, []

    indexed: dict[tuple[str | None, str], dict[str, Any]] = {}
    problems: list[str] = []

    for position, stream in enumerate(plain.get("streams") or []):
        if not isinstance(stream, dict):
            problems.append(f"stream at position {position} is not an object")
            continue

        name = stream.get("name")
        if not name:
            problems.append(f"stream at position {position} has no name")
            continue

        namespace = stream.get("namespace")
        stream_id = (str(namespace) if namespace else None, str(name))

        if stream_id in indexed:
            problems.append(
                f"stream {_stream_label(stream_id)} is declared more than once"
            )
            continue

        indexed[stream_id] = stream

    return indexed, problems


def _stream_label(stream_id: tuple[str | None, str]) -> str:
    """How a stream is named in everything a reviewer reads."""
    namespace, name = stream_id

    return f"{namespace}.{name}" if namespace else name


def _unique_label(label: str, taken: dict[str, Any]) -> str:
    """`label`, or a qualified form of it when another stream got there first."""
    if label not in taken:
        return label

    qualified = f"{label} (2)"
    suffix = 2
    while qualified in taken:
        suffix += 1
        qualified = f"{label} ({suffix})"

    return qualified


def _jsonable_diff(diff: DeepDiff) -> dict[str, Any]:
    """A DeepDiff as plain JSON data.

    The diff travels into the run's JSON payload, and `to_dict` keeps DeepDiff's
    own set and tree types, which `json.dumps` refuses. `to_json` is the
    serialiser that knows how to flatten them; a diff it cannot express is
    reported as its text rather than crashing the run that found it.
    """
    try:
        return json.loads(diff.to_json())
    except Exception:
        logger.warning("Could not serialise a schema diff; reporting it as text")
        return {"diff": str(diff)}


def _extract_pk_values(
    messages: list[AirbyteMessage],
    pk_paths: PrimaryKeys,
) -> set[tuple]:
    """Extract primary key values from a list of messages.

    Records with missing/null PK values are excluded — they cannot be
    matched between versions and are surfaced by `check_pk_uniqueness`.
    """
    pk_values: set[tuple] = set()
    for msg in messages:
        if msg.record and msg.record.data:
            pk = _extract_pk_tuple(msg.record.data, pk_paths)
            if not _pk_has_missing_values(pk):
                pk_values.add(pk)
    return pk_values


def _compare_records_with_pk(
    stream_name: str,
    control_msgs: list[AirbyteMessage],
    target_msgs: list[AirbyteMessage],
    pk_fields: PrimaryKeys,
    exclude_paths: list[str],
) -> RecordDiff:
    """Compare records using primary keys for matching.

    Records with missing/null PK values are excluded from the lookup —
    they would otherwise collide on the same key and silently collapse.
    `check_pk_uniqueness` reports them as an error.
    """
    # Build lookup by PK. A duplicated PK keeps its FIRST record, so the
    # example a reader sees for it is stable across runs (check_pk_uniqueness
    # fails the run on the duplicate either way).
    control_by_pk: dict[tuple, dict] = {}
    for msg in control_msgs:
        if msg.record and msg.record.data:
            pk = _extract_pk_tuple(msg.record.data, pk_fields)
            if not _pk_has_missing_values(pk) and pk not in control_by_pk:
                control_by_pk[pk] = json.loads(msg.record.model_dump_json())

    target_by_pk: dict[tuple, dict] = {}
    for msg in target_msgs:
        if msg.record and msg.record.data:
            pk = _extract_pk_tuple(msg.record.data, pk_fields)
            if not _pk_has_missing_values(pk) and pk not in target_by_pk:
                target_by_pk[pk] = json.loads(msg.record.model_dump_json())

    control_pks = set(control_by_pk.keys())
    target_pks = set(target_by_pk.keys())

    only_in_control = control_pks - target_pks
    only_in_target = target_pks - control_pks

    # Records with value differences (same PK, different values). Only the
    # first MAX_EXAMPLE_DIFFS diffs are kept as examples; the count covers
    # all of them.
    records_with_value_diff: list[dict[str, Any]] = []
    value_diff_count = 0
    # Sorted (`key=repr`: PK tuples mix types) so the kept examples are the
    # same ones on every run; set iteration order varies per process.
    for pk in sorted(control_pks & target_pks, key=repr):
        control_record = control_by_pk[pk]
        target_record = target_by_pk[pk]
        # Fast path: equal dicts cannot produce a diff, and DeepDiff with
        # ignore_order=True costs ~500\u00b5s per pair \u2014 which is every pair on
        # a passing run. Plain equality is ~0.9\u00b5s; skipping identical pairs
        # measured 13\u00d7 faster end-to-end on an all-identical stream.
        if {
            key: value
            for key, value in control_record.items()
            if key not in exclude_paths
        } == {
            key: value
            for key, value in target_record.items()
            if key not in exclude_paths
        }:
            continue
        diff = DeepDiff(
            control_record,
            target_record,
            ignore_order=True,
            exclude_paths=[f"root['{p}']" for p in exclude_paths],
        )
        if diff:
            value_diff_count += 1
            if len(records_with_value_diff) < MAX_EXAMPLE_DIFFS:
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
        # Sorted for the same reason as the value-diff examples: which few
        # records survive the example cap must not change run to run.
        records_only_in_control=[
            control_by_pk[pk]
            for pk in sorted(only_in_control, key=repr)[:MAX_EXAMPLE_DIFFS]
        ],
        records_only_in_target=[
            target_by_pk[pk]
            for pk in sorted(only_in_target, key=repr)[:MAX_EXAMPLE_DIFFS]
        ],
        records_with_value_diff_count=value_diff_count,
        records_only_in_control_count=len(only_in_control),
        records_only_in_target_count=len(only_in_target),
        pk_paths=pk_fields,
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


@dataclass
class RecordComparisonSummary:
    """Aggregated result of all record-level comparisons for a read run.

    Produced by `run_record_comparisons`. `passed` is the overall
    verdict folded from every individual check.
    """

    passed: bool
    count_comparison: ComparisonResult
    # True when the comparison itself crashed rather than compared: the run
    # still fails (fail closed), but as inconclusive \u2014 a comparator bug must
    # not tell a connector developer their change caused a regression.
    errored: bool = False
    pk_presence: ComparisonResult | None = None
    control_pk_uniqueness: ComparisonResult | None = None
    target_pk_uniqueness: ComparisonResult | None = None
    field_comparison: ComparisonResult | None = None
    streams_without_pk: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-safe dict for reports and GitHub outputs.

        Example values (missing/duplicate PKs capped at `MAX_EXAMPLE_PKS`,
        record diffs at `MAX_EXAMPLE_DIFFS`) are bounded in number, and the
        DeepDiff payload of each kept example is embedded whole. Those caps
        are per stream, so as a global floor the serialized payload is held
        under `MAX_SUMMARY_BYTES` (GITHUB_OUTPUT rejects a step's outputs
        past ~1MiB -- at the end of the run, losing exactly the failing
        run's signal): an oversized summary degrades in stages -- diff
        payloads to placeholders, then example lists to
        `DEGRADED_EXAMPLE_CAP`, then passing streams' per-stream entries
        (a huge catalog outgrows the budget on per-stream metadata alone),
        then error/warning lists, then failing streams' entries past
        `DEGRADED_EXAMPLE_CAP` per check, and as a last resort everything
        but the verdicts -- each stage recording itself in `warnings`.
        Verdicts and counts are never touched, and full details remain in
        the run artifacts.
        """
        checks: dict[str, Any] = {
            "record_counts": _count_check_to_dict(self.count_comparison),
        }
        if self.pk_presence is not None:
            checks["pk_presence"] = _pk_presence_check_to_dict(self.pk_presence)
        if self.control_pk_uniqueness is not None:
            checks["pk_uniqueness_control"] = _pk_uniqueness_check_to_dict(
                self.control_pk_uniqueness
            )
        if self.target_pk_uniqueness is not None:
            checks["pk_uniqueness_target"] = _pk_uniqueness_check_to_dict(
                self.target_pk_uniqueness
            )
        if self.field_comparison is not None:
            checks["field_values"] = _field_check_to_dict(self.field_comparison)

        payload: dict[str, Any] = json_safe(
            {
                "passed": self.passed,
                "errored": self.errored,
                "errors": self.errors,
                "warnings": self.warnings,
                "streams_without_pk": self.streams_without_pk,
                "checks": checks,
            }
        )

        if _serialized_size(payload) <= MAX_SUMMARY_BYTES:
            return payload
        for degrade in (
            _degrade_diffs_to_placeholders,
            _degrade_example_lists,
            _degrade_passing_stream_entries,
            _degrade_message_lists,
            _degrade_failing_stream_entries,
            _degrade_to_verdict_only,
        ):
            note = degrade(payload)
            if note:
                payload["warnings"].append(
                    f"Summary truncated to fit GITHUB_OUTPUT: {note}; "
                    "full details are in the run artifacts"
                )
            if _serialized_size(payload) <= MAX_SUMMARY_BYTES:
                break
        return payload


def run_record_comparisons(
    control_records: dict[str, list[AirbyteMessage]],
    target_records: dict[str, list[AirbyteMessage]],
    primary_keys_per_stream: dict[str, list | None],
) -> RecordComparisonSummary:
    """Run all record-level comparisons between control and target output.

    Checks, folded into a single pass/fail verdict:

    - Record counts (all streams): directional — the target must produce at
      least as many records as the control. For streams without a primary
      key this is the *only* check (records can't be matched without a PK,
      and live API data may legitimately grow between the two runs).
    - Primary key presence (streams with a PK): every control PK value must
      appear in the target output. Extra PKs in the target are acceptable.
    - Primary key integrity (streams with a PK): each PK value must appear
      at most once per stream, and every record must carry a value for its
      declared PK fields; checked independently on the control and the
      target output. Both fail even when present in both versions — a
      duplicate or missing PK means the declared primary key cannot be
      trusted (and would break deduplication on the destination side),
      regardless of which version introduced it.
    - Field values (streams with a PK): records matched by PK must have
      identical field values (excluding `emitted_at`). Records that exist
      only in the target do not fail the comparison (directional).

    Args:
        control_records: Control run records grouped by stream name.
        target_records: Target run records grouped by stream name.
        primary_keys_per_stream: Primary key definition per stream, either
            flat (`["id"]`) or nested (`[["id"]]`) format; falsy values
            mean the stream has no primary key.
    """
    normalized_pks: dict[str, PrimaryKeys | None] = {
        stream: normalize_primary_keys(pk)
        for stream, pk in primary_keys_per_stream.items()
    }

    all_streams = set(control_records) | set(target_records)
    streams_without_pk = sorted(
        stream for stream in all_streams if not normalized_pks.get(stream)
    )
    has_pk_streams = len(streams_without_pk) < len(all_streams)

    warnings: list[str] = [
        f"Stream {stream} has no primary key; only record counts are compared"
        for stream in streams_without_pk
    ]

    count_comparison = compare_record_counts(control_records, target_records)
    results: list[ComparisonResult] = [count_comparison]

    pk_presence: ComparisonResult | None = None
    control_pk_uniqueness: ComparisonResult | None = None
    target_pk_uniqueness: ComparisonResult | None = None
    field_comparison: ComparisonResult | None = None

    if has_pk_streams:
        control_with_pk = {
            stream: msgs
            for stream, msgs in control_records.items()
            if normalized_pks.get(stream)
        }
        target_with_pk = {
            stream: msgs
            for stream, msgs in target_records.items()
            if normalized_pks.get(stream)
        }

        pk_presence = compare_primary_keys(
            control_with_pk, target_with_pk, normalized_pks
        )
        control_pk_uniqueness = check_pk_uniqueness(
            control_with_pk, normalized_pks, version_label="control"
        )
        target_pk_uniqueness = check_pk_uniqueness(
            target_with_pk, normalized_pks, version_label="target"
        )
        field_comparison = compare_all_records(
            control_with_pk,
            target_with_pk,
            primary_keys_per_stream=normalized_pks,
            directional=True,
        )
        results.extend(
            [pk_presence, control_pk_uniqueness, target_pk_uniqueness, field_comparison]
        )

    errors: list[str] = []
    for result in results:
        errors.extend(result.errors)
        warnings.extend(result.warnings)

    return RecordComparisonSummary(
        passed=all(result.passed for result in results),
        count_comparison=count_comparison,
        pk_presence=pk_presence,
        control_pk_uniqueness=control_pk_uniqueness,
        target_pk_uniqueness=target_pk_uniqueness,
        field_comparison=field_comparison,
        streams_without_pk=streams_without_pk,
        errors=errors,
        warnings=warnings,
    )


def run_record_comparisons_from_files(
    control_record_files: dict[str, Path],
    target_record_files: dict[str, Path],
    primary_keys_per_stream: dict[str, list | None],
) -> RecordComparisonSummary:
    """Run all record-level comparisons from per-stream record files.

    Memory-bounded variant of `run_record_comparisons` for full connector
    outputs: instead of holding every stream of both runs in memory, it
    loads one stream at a time (both versions), runs the full set of
    checks on it, and merges the per-stream results. Peak memory is one
    stream's records rather than the whole sync output. Checks and the
    resulting summary are identical to the in-memory variant.

    Args:
        control_record_files: Control run per-stream record files (jsonl of
            Airbyte RECORD messages), e.g. from `split_records_per_stream`.
        target_record_files: Target run per-stream record files.
        primary_keys_per_stream: Primary key definition per stream, as for
            `run_record_comparisons`.
    """
    chunk_summaries: list[RecordComparisonSummary] = []
    for stream in sorted(set(control_record_files) | set(target_record_files)):
        control_chunk: dict[str, list[AirbyteMessage]] = {}
        if stream in control_record_files:
            control_chunk[stream] = _read_records_file(control_record_files[stream])
        target_chunk: dict[str, list[AirbyteMessage]] = {}
        if stream in target_record_files:
            target_chunk[stream] = _read_records_file(target_record_files[stream])

        chunk_summaries.append(
            run_record_comparisons(
                control_records=control_chunk,
                target_records=target_chunk,
                primary_keys_per_stream=primary_keys_per_stream,
            )
        )

    return _merge_summaries(chunk_summaries)


def _read_records_file(records_path: Path) -> list[AirbyteMessage]:
    """Load the record messages from a single per-stream jsonl file.

    This is the one full protocol validation each record gets: the splitter
    routes lines on a plain JSON parse, so a RECORD-typed line that fails
    protocol validation lands in the stream file (keeping the artifact an
    honest copy of what the connector emitted) and is skipped here.
    """
    records: list[AirbyteMessage] = []
    with records_path.open() as records_file:
        for line in records_file:
            line = line.strip()
            if not line:
                continue
            with contextlib.suppress(ValidationError):
                message = AirbyteMessage.model_validate_json(line)
                if message.type is AirbyteMessageType.RECORD:
                    records.append(message)
    return records


def _merge_comparison_results(
    results: list[ComparisonResult],
    passed_message: str,
    failed_message: str,
) -> ComparisonResult | None:
    """Merge per-stream ComparisonResults into one (streams are disjoint)."""
    if not results:
        return None
    stream_results: dict[str, StreamComparisonResult] = {}
    errors: list[str] = []
    warnings: list[str] = []
    for result in results:
        stream_results.update(result.stream_results)
        errors.extend(result.errors)
        warnings.extend(result.warnings)
    passed = all(result.passed for result in results)
    return ComparisonResult(
        passed=passed,
        stream_results=stream_results,
        message=passed_message if passed else failed_message,
        errors=errors,
        warnings=warnings,
    )


def _merge_summaries(
    chunk_summaries: list[RecordComparisonSummary],
) -> RecordComparisonSummary:
    """Merge single-stream comparison summaries into one overall summary."""

    def merge(
        results: list[ComparisonResult | None],
        passed_message: str,
        failed_message: str,
    ) -> ComparisonResult | None:
        return _merge_comparison_results(
            [r for r in results if r is not None], passed_message, failed_message
        )

    count_comparison = merge(
        [c.count_comparison for c in chunk_summaries],
        "Record counts match",
        "Record count mismatch",
    ) or ComparisonResult(passed=True, message="Record counts match")

    return RecordComparisonSummary(
        passed=all(c.passed for c in chunk_summaries),
        count_comparison=count_comparison,
        pk_presence=merge(
            [c.pk_presence for c in chunk_summaries],
            "All primary keys present",
            "Missing primary keys",
        ),
        control_pk_uniqueness=merge(
            [c.control_pk_uniqueness for c in chunk_summaries],
            "All primary keys unique and present in control",
            "Primary key integrity issues found in control",
        ),
        target_pk_uniqueness=merge(
            [c.target_pk_uniqueness for c in chunk_summaries],
            "All primary keys unique and present in target",
            "Primary key integrity issues found in target",
        ),
        field_comparison=merge(
            [c.field_comparison for c in chunk_summaries],
            "All records match",
            "Record differences found",
        ),
        streams_without_pk=sorted(
            stream for c in chunk_summaries for stream in c.streams_without_pk
        ),
        errors=[error for c in chunk_summaries for error in c.errors],
        warnings=[warning for c in chunk_summaries for warning in c.warnings],
    )


def json_safe(value: Any) -> Any:
    """Recursively convert a value into JSON-serializable builtins.

    The set branch matches `collections.abc.Set` rather than the builtin
    types alone: DeepDiff reports `dictionary_item_added`/`_removed` as its
    own ordered-set classes, and falling through to `str()` would collapse
    the whole collection into one unreadable line instead of a JSON array
    with one path per entry.
    """
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, collections.abc.Set)):
        return [json_safe(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def _serialized_size(payload: dict[str, Any]) -> int:
    """The payload's size as it will land in GITHUB_OUTPUT."""
    return len(json.dumps(payload, separators=(",", ":")))


def _degrade_diffs_to_placeholders(payload: dict[str, Any]) -> str | None:
    """Swap each embedded DeepDiff payload for a placeholder, in place.

    First degradation stage for a summary past `MAX_SUMMARY_BYTES`: the
    diffs are the only entries unbounded in size (a `values_changed` entry
    carries both full field values). The placeholder keeps the example
    identifiable -- its `pk` names the record in the per-stream artifact
    files, `changed_sections` says what kind of change it was.

    Returns a note for the summary's warnings, or None if there was
    nothing to degrade.
    """
    changed = False
    field_values = payload.get("checks", {}).get("field_values", {})
    for stream_info in field_values.get("streams", {}).values():
        for example in stream_info.get("value_diff_examples", []):
            diff = example.get("diff") or {}
            if not diff or diff.get("truncated") is True:
                continue
            example["diff"] = {
                "truncated": True,
                "note": (
                    "diff omitted: the summary exceeded the GITHUB_OUTPUT "
                    "size budget; compare the records for this pk in the "
                    "per-stream files in the run artifacts"
                ),
                "changed_sections": sorted(diff),
            }
            changed = True
    return "value-diff payloads replaced by placeholders" if changed else None


def _degrade_example_lists(payload: dict[str, Any]) -> str | None:
    """Shrink the PK example lists to `DEGRADED_EXAMPLE_CAP`, in place.

    Second degradation stage: the per-stream `MAX_EXAMPLE_PKS` cap is what
    lets a many-streams failure outgrow the global budget. The `*_count`
    fields keep the exact totals.

    Returns a note for the summary's warnings, or None if there was
    nothing to degrade.
    """
    changed = False
    checks = payload.get("checks", {})
    for check_key, list_key in (
        ("pk_presence", "missing_pk_examples"),
        ("pk_uniqueness_control", "duplicate_pk_examples"),
        ("pk_uniqueness_target", "duplicate_pk_examples"),
    ):
        for stream_info in checks.get(check_key, {}).get("streams", {}).values():
            examples = stream_info.get(list_key, [])
            if len(examples) > DEGRADED_EXAMPLE_CAP:
                stream_info[list_key] = examples[:DEGRADED_EXAMPLE_CAP]
                changed = True
    return (
        f"PK example lists capped at {DEGRADED_EXAMPLE_CAP} per stream"
        if changed
        else None
    )


def _degrade_passing_stream_entries(payload: dict[str, Any]) -> str | None:
    """Drop passing streams from each check's per-stream map, in place.

    Third degradation stage, and the only one a huge *passing* catalog
    needs: the per-stream maps carry an entry per stream per check
    regardless of outcome, so thousands of streams outgrow the budget with
    no examples at all. Failing entries -- the ones a reader triages --
    survive; each check records how many passing entries it dropped.

    Returns a note for the summary's warnings, or None if there was
    nothing to degrade.
    """
    changed = False
    for check in payload.get("checks", {}).values():
        streams = check.get("streams", {})
        failing = {
            name: info for name, info in streams.items() if not info.get("passed", True)
        }
        if len(failing) < len(streams):
            check["streams"] = failing
            check["passing_streams_omitted"] = len(streams) - len(failing)
            changed = True
    return "per-stream detail for passing streams omitted" if changed else None


def _degrade_message_lists(payload: dict[str, Any]) -> str | None:
    """Cap the errors/warnings lists at `DEGRADED_EXAMPLE_CAP`, in place.

    These lists carry one line per failing stream per check, so they only
    dominate the budget on colossal catalogs. A capped list ends with how
    much it dropped.

    Returns a note for the summary's warnings, or None if there was
    nothing to degrade.
    """
    changed = False
    for key in ("errors", "warnings"):
        messages = payload.get(key, [])
        if len(messages) > DEGRADED_EXAMPLE_CAP:
            payload[key] = [
                *messages[:DEGRADED_EXAMPLE_CAP],
                f"… and {len(messages) - DEGRADED_EXAMPLE_CAP} more (see run artifacts)",
            ]
            changed = True
    return f"error/warning lists capped at {DEGRADED_EXAMPLE_CAP}" if changed else None


def _degrade_failing_stream_entries(payload: dict[str, Any]) -> str | None:
    """Cap each check's per-stream map at `DEGRADED_EXAMPLE_CAP` entries.

    Nothing before this bounds the number of *failing* streams, and a wide
    database source dropping records across thousands of tables outgrows
    the budget on failing entries alone. The first `DEGRADED_EXAMPLE_CAP`
    streams by name survive (sorted, so re-runs keep the same subset);
    each check records how many failing entries it dropped.

    Returns a note for the summary's warnings, or None if there was
    nothing to degrade.
    """
    changed = False
    for check in payload.get("checks", {}).values():
        streams = check.get("streams", {})
        if len(streams) <= DEGRADED_EXAMPLE_CAP:
            continue
        kept = dict(sorted(streams.items())[:DEGRADED_EXAMPLE_CAP])
        check["failing_streams_omitted"] = (
            len(streams) - len(kept) + check.get("failing_streams_omitted", 0)
        )
        check["streams"] = kept
        changed = True
    return (
        f"per-stream detail capped at {DEGRADED_EXAMPLE_CAP} streams per check"
        if changed
        else None
    )


def _degrade_to_verdict_only(payload: dict[str, Any]) -> str | None:
    """Last resort: keep the verdicts and drop every per-stream payload.

    The stages before this shrink what they can while keeping detail; this
    one exists so `MAX_SUMMARY_BYTES` is a guarantee rather than a hope --
    a pathological payload (huge scalar PK values times many streams) can
    survive every cap above. Verdicts, messages, per-check pass/fail and
    omission counts stay; everything else lives in the run artifacts.
    """
    for check in payload.get("checks", {}).values():
        streams = check.get("streams", {})
        if streams:
            check["failing_streams_omitted"] = len(streams) + check.get(
                "failing_streams_omitted", 0
            )
        check["streams"] = {}
    for key in ("errors", "warnings"):
        payload[key] = [message[:200] for message in payload.get(key, [])[:5]]
    payload["streams_without_pk"] = payload.get("streams_without_pk", [])[:5]

    return "degraded to verdicts only"


def _count_check_to_dict(result: ComparisonResult) -> dict[str, Any]:
    return {
        "passed": result.passed,
        "message": result.message,
        "streams": {
            name: {
                "passed": r.passed,
                "control_count": r.control_count,
                "target_count": r.target_count,
            }
            for name, r in result.stream_results.items()
        },
    }


def _pk_presence_check_to_dict(result: ComparisonResult) -> dict[str, Any]:
    return {
        "passed": result.passed,
        "message": result.message,
        "streams": {
            name: {
                "passed": r.passed,
                "missing_pk_count": r.missing_pk_count,
                "extra_pk_count": r.extra_pk_count,
                "missing_pk_examples": r.missing_pks[:MAX_EXAMPLE_PKS],
            }
            for name, r in result.stream_results.items()
        },
    }


def _pk_uniqueness_check_to_dict(result: ComparisonResult) -> dict[str, Any]:
    return {
        "passed": result.passed,
        "message": result.message,
        "streams": {
            name: {
                "passed": r.passed,
                "duplicate_pk_count": r.duplicate_pk_count,
                # Each example carries how many records shared the PK value,
                # e.g. {"pk": [777], "count": 3} for a PK emitted three times.
                "duplicate_pk_examples": [
                    {"pk": pk, "count": r.duplicate_pk_counts.get(pk)}
                    for pk in r.duplicate_pks[:MAX_EXAMPLE_PKS]
                ],
                "records_missing_pk": r.records_missing_pk,
            }
            for name, r in result.stream_results.items()
        },
    }


def _field_check_to_dict(result: ComparisonResult) -> dict[str, Any]:
    streams: dict[str, Any] = {}
    for name, r in result.stream_results.items():
        diff = r.record_diff
        streams[name] = {
            "passed": r.passed,
            "records_with_value_diff": diff.records_with_value_diff_count
            if diff
            else 0,
            "records_only_in_control": diff.records_only_in_control_count
            if diff
            else 0,
            "records_only_in_target": diff.records_only_in_target_count if diff else 0,
            "value_diff_examples": [
                {
                    "pk": entry.get("pk"),
                    "diff": json_safe(entry.get("diff") or {}),
                }
                for entry in (
                    diff.records_with_value_diff[:MAX_EXAMPLE_DIFFS] if diff else []
                )
            ],
        }
    return {
        "passed": result.passed,
        "message": result.message,
        "streams": streams,
    }
