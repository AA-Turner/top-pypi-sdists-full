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
import hashlib
import json
import locale
import logging
import re
from array import array
from collections import Counter
from collections.abc import Callable, Hashable, Iterator, Mapping, Sequence
from collections.abc import Set as AbstractSet
from dataclasses import dataclass, field, replace
from functools import reduce
from pathlib import Path
from typing import Any

from airbyte_protocol.models import AirbyteMessage
from airbyte_protocol.models import Type as AirbyteMessageType
from deepdiff import DeepDiff
from pydantic import ValidationError

from airbyte_ops_mcp.regression_tests.normalization import (
    stream_label,
    to_plain_dict,
    to_stream_id,
    unique_label,
)

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
# A duplicated PK's value-diff example shows at most this many records per
# side, and its DeepDiff compares only those: a PK whose thousands of records
# all differ (a mis-declared PK on a target that adds a field) would otherwise
# diff, store and render every one of them. The example's note keeps the
# full counts.
MAX_GROUP_EXAMPLE_RECORDS = 20


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
    # More identical copies the target emits under PK values the control
    # already duplicates (`_record_group_diff`): a warning, never a value
    # diff. Exact totals; `added_copy_pks` maps a capped, sorted set of those
    # PK values (`MAX_EXAMPLE_PKS`) to their extra copies.
    added_copy_count: int = 0
    added_copy_pk_count: int = 0
    added_copy_pks: dict[Any, int] = field(default_factory=dict)
    # On a stopped-early read (`partial`), the differences found on PK values
    # with more than one record on either side: a cap or a deadline can cut
    # such a group on one side, so they are reported and never fail. Kept
    # apart from `records_with_value_diff`, which then holds only the strict
    # findings -- PK values both sides emitted once -- with their own capped
    # examples (`MAX_EXAMPLE_DIFFS`). Empty on a complete read, where every
    # finding is strict.
    partial_group_diffs: list[dict[str, Any]] = field(default_factory=list)
    partial_group_diff_count: int = 0

    def __post_init__(self) -> None:
        self.records_with_value_diff_count = max(
            self.records_with_value_diff_count, len(self.records_with_value_diff)
        )
        self.partial_group_diff_count = max(
            self.partial_group_diff_count, len(self.partial_group_diffs)
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
    lists would break the comparison's per-stream memory bound exactly on
    the runs that drop the most records. The `*_pk_count` fields
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
    # The stream's duplicated PK values classified against the other
    # version's output: duplicated in both versions, in the target only, in
    # the control only with every record still in the target (fixed), in
    # the control only with records the target dropped or changed (the
    # `lost_*` fields, named for the records rather than the PK). Set by the
    # comparison and identical on both versions' results; zero on a
    # single-version check. On a stopped-early read fixed and lost are zero
    # too: a cut can make either look true, so the control's duplicates that
    # are not pre-existing stay unclassified
    # (`_unclassified_duplicate_pk_count`). The counts are exact;
    # `lost_duplicate_pks` is capped like the other PK lists.
    pre_existing_duplicate_pk_count: int = 0
    new_duplicate_pk_count: int = 0
    fixed_duplicate_pk_count: int = 0
    lost_duplicate_pk_count: int = 0
    lost_duplicate_pks: list[Any] = field(default_factory=list)
    # Records beyond the first of each duplicated PK value, sum(count - 1):
    # how many fewer records the version would emit without its duplicates.
    # Exact, like the split; the record-count check allows for the ones the
    # target no longer emits.
    duplicate_row_count: int = 0
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

    `value_only` is the same kind of flag for the state comparison: every
    difference found is a scalar value under an identical shape, a cursor that
    moved rather than a state that was restructured. Until HTTP replay lands
    (airbyte-internal-issues#16837) the two versions call the live API in
    separate runs, so a timestamp cursor can legitimately advance between them;
    failing on that would redden every incremental read. Like `additive_only`,
    it is false for a run with no differences at all.

    `inconclusive` says the comparison had nothing to compare -- not a pass, and
    not a difference either. It is a separate flag from `value_only` because the
    two answer different questions: `value_only` classifies differences that were
    found, so reporting "nothing was compared" through it would say every
    difference was benign drift when there were no differences at all. Both make
    a `passed=False` non-gating, and only one of them can be true.
    """

    passed: bool
    stream_results: dict[str, StreamComparisonResult] = field(default_factory=dict)
    message: str = ""
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    additive_only: bool = False
    value_only: bool = False
    inconclusive: bool = False

    @property
    def failed_streams(self) -> list[str]:
        return [
            name for name, result in self.stream_results.items() if not result.passed
        ]


def compare_record_counts(
    control_records: Mapping[str, Sequence[AirbyteMessage]],
    target_records: Mapping[str, Sequence[AirbyteMessage]],
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

    return ComparisonResult(
        passed=all(r.passed for r in stream_results.values()),
        stream_results=stream_results,
        message=_record_count_message(stream_results),
        errors=errors,
    )


def _record_count_message(stream_results: dict[str, StreamComparisonResult]) -> str:
    """The count check's message, shared with the merge of per-stream results.

    A passing stream with fewer target records is one the duplicate-row
    allowance passed (`_allow_dropped_duplicate_rows`). The message claims
    only the arithmetic: whether the dropped rows were copies is the field
    values' call.
    """
    if not all(r.passed for r in stream_results.values()):
        return "Record count mismatch"
    if any(r.target_count < r.control_count for r in stream_results.values()):
        return "Record counts match once duplicate rows are left out"
    return "Record counts match"


def _allow_dropped_duplicate_rows(
    count_comparison: ComparisonResult,
    control_pk_uniqueness: ComparisonResult,
    target_pk_uniqueness: ComparisonResult,
) -> None:
    """Pass, with a warning, a count shortfall within the drop in duplicate rows.

    A target that stops emitting a duplicated PK's extra copies has fewer
    records, and the directional count would fail it on the very fix the
    PK-integrity check reports as "fixed in target". So a failing stream
    passes when its shortfall is no larger than the control's duplicate rows
    minus the target's: the target has at least as many records once each
    side's duplicate rows are left out. Updated in place, warning instead of
    error; a passing stream with fewer target records is always this case.

    Safe only together with the field-value rule for duplicated PKs
    (`_record_group_diff`): a dropped row that was not a copy of a record the
    target still emits is a lost record and fails the field values, and a
    dropped PK fails PK presence. The count itself cannot tell copies from
    lost records, so its message states the arithmetic and leaves that to the
    field values.

    Not applied to a stopped-early read (`run_record_comparisons`): its
    counts never decide the verdict there, and a target cut short would only
    widen the allowance.
    """
    for stream, result in count_comparison.stream_results.items():
        if result.passed:
            continue
        control_rows = _duplicate_row_count(control_pk_uniqueness, stream)
        target_rows = _duplicate_row_count(target_pk_uniqueness, stream)
        shortfall = result.control_count - result.target_count
        if shortfall > control_rows - target_rows:
            continue
        count_comparison.errors.remove(result.message)
        result.passed = True
        records = "record" if shortfall == 1 else "records"
        result.message = (
            f"Stream {stream} has {shortfall} fewer {records} in target, within "
            "the duplicate rows the target dropped "
            f"({control_rows} in control, {target_rows} in target); field values "
            "check that the dropped rows were copies"
        )
        count_comparison.warnings.append(result.message)
    count_comparison.passed = all(
        r.passed for r in count_comparison.stream_results.values()
    )
    count_comparison.message = _record_count_message(count_comparison.stream_results)


def _duplicate_row_count(pk_uniqueness: ComparisonResult, stream: str) -> int:
    result = pk_uniqueness.stream_results.get(stream)
    return result.duplicate_row_count if result is not None else 0


def compare_primary_keys(
    control_records: Mapping[str, Sequence[AirbyteMessage]],
    target_records: Mapping[str, Sequence[AirbyteMessage]],
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


@dataclass
class _PkIntegrityScan:
    """One version's PK integrity findings on one stream, before any verdict.

    `duplicates` is the full occurrence count per duplicated PK value. The
    result keeps a capped copy; the full map is what the comparison needs to
    classify the duplicates against the other version's, and it lives only
    as long as that stream is being compared.
    """

    pk_paths: PrimaryKeys
    duplicates: dict[tuple, int]
    records_missing_pk: int
    records_missing_pk_examples: list[dict[str, Any]]


@dataclass(frozen=True)
class _DuplicatePkSplit:
    """One stream's duplicated PK values, classified against the other version.

    `pre_existing` are duplicated in both versions, `new` in the target only.
    A value duplicated in the control only is `fixed` when every one of its
    control records still has an equal record in the target -- the target
    collapsed copies -- and `lost` otherwise: the target dropped or changed a
    record of it, which the field values (or PK presence, for a value the
    target no longer emits at all) fail on. The control's duplicates are
    `pre_existing + fixed + lost`, the target's `pre_existing + new`.
    `lost_pks` is the sorted, capped list of those values.

    On a stopped-early read neither `fixed` nor `lost` is decided: a cap or a
    deadline can cut either side, so a control-only duplicate may be one the
    target had not reached yet, or one the control read further into. Both
    stay 0, and the control's duplicates are then `pre_existing` plus the
    ones not duplicated in the target (partial read).
    """

    pre_existing: int = 0
    new: int = 0
    fixed: int = 0
    lost: int = 0
    lost_pks: tuple[Any, ...] = ()


def _scan_pk_integrity(
    messages: Sequence[AirbyteMessage], pk_paths: PrimaryKeys
) -> _PkIntegrityScan:
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
    return _PkIntegrityScan(
        pk_paths=pk_paths,
        duplicates={pk: count for pk, count in pk_counts.items() if count > 1},
        records_missing_pk=records_missing_pk,
        records_missing_pk_examples=records_missing_pk_examples,
    )


def _scan_pk_integrity_per_stream(
    records_per_stream: Mapping[str, Sequence[AirbyteMessage]],
    primary_keys_per_stream: dict[str, PrimaryKeys | None],
) -> dict[str, _PkIntegrityScan | None]:
    """Scan every stream; `None` stands for a stream without a primary key."""
    scans: dict[str, _PkIntegrityScan | None] = {}
    for stream_name, messages in records_per_stream.items():
        pk_paths = primary_keys_per_stream.get(stream_name)
        scans[stream_name] = (
            _scan_pk_integrity(messages, pk_paths) if pk_paths else None
        )
    return scans


def _split_duplicate_pks(
    control: _PkIntegrityScan | None,
    target: _PkIntegrityScan | None,
    control_messages: Sequence[AirbyteMessage],
    target_messages: Sequence[AirbyteMessage],
    partial: bool = False,
) -> _DuplicatePkSplit:
    control_pks = (control.duplicates if control else {}).keys()
    target_pks = (target.duplicates if target else {}).keys()
    pre_existing = len(control_pks & target_pks)
    new = len(target_pks - control_pks)
    if partial:
        return _DuplicatePkSplit(pre_existing=pre_existing, new=new)
    control_only = control_pks - target_pks
    lost = (
        _lost_duplicate_pks(
            control_only, control.pk_paths, control_messages, target_messages
        )
        if control is not None and control_only
        else []
    )
    return _DuplicatePkSplit(
        pre_existing=pre_existing,
        new=new,
        fixed=len(control_only) - len(lost),
        lost=len(lost),
        lost_pks=tuple(lost[:MAX_EXAMPLE_PKS]),
    )


def _lost_duplicate_pks(
    control_only: AbstractSet[tuple],
    pk_paths: PrimaryKeys,
    control_messages: Sequence[AirbyteMessage],
    target_messages: Sequence[AirbyteMessage],
) -> list[tuple]:
    """The control-only duplicated PK values the target did not just collapse.

    The target emits such a value at most once. It was fixed only when every
    control record of it equals that one target record (`_canonical_record`
    with `EXCLUDE_PATHS`, the field values' matching); otherwise the target
    dropped or changed a record of it, or dropped the value entirely. Sorted
    (`key=repr`), exact.

    One pass over each side, reading only the records of these values. The
    target's one record per value is kept as a 16-byte blake2b digest of its
    key rather than the key itself, and each control record is compared as it
    is read, so what is held does not grow with the records' size. On a read
    from disk (`_RecordsFile`) that is one more pass over each file, which
    `_split_duplicate_pks` makes only for a stream with control-only
    duplicates on a complete read.
    """

    def keyed(
        messages: Sequence[AirbyteMessage],
    ) -> Iterator[tuple[tuple, AirbyteMessage]]:
        for message in messages:
            if not (message.record and message.record.data):
                continue
            pk = _extract_pk_tuple(message.record.data, pk_paths)
            if pk in control_only:
                yield pk, message

    target_digests = {
        pk: _record_digest(message) for pk, message in keyed(target_messages)
    }
    lost: set[tuple] = set()
    for pk, message in keyed(control_messages):
        if pk not in lost and target_digests.get(pk) != _record_digest(message):
            lost.add(pk)
    return sorted(lost, key=repr)


def _record_digest(message: AirbyteMessage) -> bytes:
    """A blake2b digest of a record's `_canonical_record` on `EXCLUDE_PATHS`."""
    key = _canonical_record(_record_dict(message), EXCLUDE_PATHS)
    return hashlib.blake2b(key.encode(), digest_size=16).digest()


def check_pk_uniqueness(
    records_per_stream: dict[str, list[AirbyteMessage]],
    primary_keys_per_stream: dict[str, PrimaryKeys | None],
    version_label: str = "",
) -> ComparisonResult:
    """Check PK integrity of a single version's output, per stream.

    Two failure modes, both hard failures on a version checked alone (they
    indicate a broken primary key declaration or broken records, which
    breaks deduplication on the destination side):

    - Duplicate primary keys: the same PK value appears on more than one
      record, indicating the connector emitted the same entity more than
      once (e.g. broken pagination or slicing).
    - Missing primary key values: a record has no value (absent field or
      null) for one or more of its declared PK fields, indicating the
      catalog declares a primary key that is not actually present on the
      records. Such records are excluded from the duplicate count — they
      are reported through their own error instead.

    This runs on a single version's output. The comparison goes through
    `_compare_pk_integrity` instead, which classifies each stream's
    duplicates against the other version's and fails only on the ones the
    target introduced.

    Args:
        records_per_stream: Records grouped by stream name.
        primary_keys_per_stream: Primary key paths per stream; streams
            without a primary key are skipped.
        version_label: Optional label ("control"/"target") used in messages.
    """
    scans = _scan_pk_integrity_per_stream(records_per_stream, primary_keys_per_stream)
    return _pk_uniqueness_result(scans, version_label)


def _compare_pk_integrity(
    control_records: Mapping[str, Sequence[AirbyteMessage]],
    target_records: Mapping[str, Sequence[AirbyteMessage]],
    primary_keys_per_stream: dict[str, PrimaryKeys | None],
    partial: bool = False,
) -> tuple[ComparisonResult, ComparisonResult]:
    """Both versions' PK integrity results, control first.

    Each stream's duplicated PK values are classified against the other
    version's (`_DuplicatePkSplit`) and the split is recorded on both
    versions' stream results. Only the target's new duplicates fail: a PK
    value duplicated in both versions is pre-existing and warns, and one
    duplicated in the control alone warns as fixed by the target -- or, when
    the target dropped or changed records of it, warns that the field values
    or PK presence fail on it, without failing a second time here. On a
    `partial` read the target's new duplicates warn too, since the control
    may have stopped before the second record of the group, and a
    control-only duplicate is neither fixed nor lost: it warns as "not
    duplicated in target (partial read)". A record missing its PK value
    fails on either version, as when checked alone.
    """
    control_scans = _scan_pk_integrity_per_stream(
        control_records, primary_keys_per_stream
    )
    target_scans = _scan_pk_integrity_per_stream(
        target_records, primary_keys_per_stream
    )
    splits = {
        stream: _split_duplicate_pks(
            control_scans.get(stream),
            target_scans.get(stream),
            control_records.get(stream, []),
            target_records.get(stream, []),
            partial=partial,
        )
        for stream in set(control_scans) | set(target_scans)
    }
    return (
        _pk_uniqueness_result(control_scans, "control", splits, partial=partial),
        _pk_uniqueness_result(
            target_scans,
            "target",
            splits,
            partial=partial,
            control_streams_with_records={
                name for name, records in control_records.items() if records
            },
        ),
    )


def _pk_uniqueness_result(
    scans: dict[str, _PkIntegrityScan | None],
    version_label: str = "",
    splits: dict[str, _DuplicatePkSplit] | None = None,
    partial: bool = False,
    control_streams_with_records: set[str] | None = None,
) -> ComparisonResult:
    """Build one version's PK integrity result from its per-stream scans.

    `splits` is the comparison's classification of each stream's duplicates
    (see `_compare_pk_integrity`), with `version_label` naming which version
    this is: the target's new duplicates are errors, everything else warns.
    On a `partial` read the target's new duplicates warn as well, and the
    control's own duplicates are named neutrally, as "not duplicated in
    target (partial read)", since the split decides neither fixed nor lost
    there. Without `splits`, a version checked alone fails on every
    duplicate.

    The shared duplicates are reported once, as the control's warning; the
    target's stream message names them too, so its own row can say why it
    warns.
    """
    stream_results: dict[str, StreamComparisonResult] = {}
    errors: list[str] = []
    warnings: list[str] = []
    label = f" in {version_label}" if version_label else ""

    for stream_name, scan in scans.items():
        if scan is None:
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

        duplicate_pk_count = len(scan.duplicates)
        # Capped like the other PK lists; Counter preserves first-seen order,
        # so the kept subset is deterministic.
        duplicate_pk_counts = dict(list(scan.duplicates.items())[:MAX_EXAMPLE_PKS])
        duplicate_pks = list(duplicate_pk_counts)
        split = (splits or {}).get(stream_name, _DuplicatePkSplit())

        stream_errors: list[str] = []
        stream_warnings: list[str] = []
        stream_notes: list[str] = []
        if splits is None:
            if duplicate_pks:
                stream_errors.append(
                    f"Stream {stream_name} has {duplicate_pk_count} duplicate "
                    f"primary key value(s){label}"
                )
        else:
            pre_existing = (
                f"Stream {stream_name} has {split.pre_existing} pre-existing "
                "duplicate primary key value(s), unchanged between control and "
                "target"
            )
            if version_label == "target":
                control_note = (
                    "(stream not read by control)"
                    if control_streams_with_records is not None
                    and stream_name not in control_streams_with_records
                    else "(not duplicated in control)"
                )
                new = (
                    f"Stream {stream_name} has {split.new} new duplicate "
                    f"primary key value(s) in target {control_note}"
                )
                if split.new and partial:
                    stream_warnings.append(
                        f"{new}, inconclusive on a stopped-early read: the "
                        "control may have stopped before the duplicate"
                    )
                elif split.new:
                    stream_errors.append(new)
                if split.pre_existing:
                    stream_notes.append(pre_existing)
            else:
                if split.pre_existing:
                    stream_warnings.append(pre_existing)
                control_only = duplicate_pk_count - split.pre_existing
                if partial and control_only:
                    stream_warnings.append(
                        f"Stream {stream_name} has {control_only} duplicate "
                        "primary key value(s) in control not duplicated in target "
                        "(partial read): a cap or deadline can cut either side, so "
                        "they are neither fixed nor lost"
                    )
                if split.fixed:
                    stream_warnings.append(
                        f"Stream {stream_name} has {split.fixed} duplicate primary "
                        "key value(s) in control fixed in target"
                    )
                if split.lost:
                    stream_warnings.append(
                        f"Stream {stream_name} has {split.lost} duplicate primary "
                        "key value(s) in control not duplicated in target, with "
                        "records the target dropped or changed; field values or "
                        "PK presence fail on them"
                    )
        if scan.records_missing_pk:
            stream_errors.append(
                f"Stream {stream_name} has {scan.records_missing_pk} record(s) "
                f"with missing or null primary key value(s){label} — primary "
                f"key {scan.pk_paths} is declared in the catalog but not present "
                "on the record data"
            )
        errors.extend(stream_errors)
        warnings.extend(stream_warnings)

        stream_results[stream_name] = StreamComparisonResult(
            stream_name=stream_name,
            passed=not stream_errors,
            duplicate_pks=duplicate_pks,
            duplicate_pk_counts=duplicate_pk_counts,
            duplicate_pk_count=duplicate_pk_count,
            pre_existing_duplicate_pk_count=split.pre_existing,
            new_duplicate_pk_count=split.new,
            fixed_duplicate_pk_count=split.fixed,
            lost_duplicate_pk_count=split.lost,
            lost_duplicate_pks=list(split.lost_pks),
            duplicate_row_count=sum(count - 1 for count in scan.duplicates.values()),
            records_missing_pk=scan.records_missing_pk,
            records_missing_pk_examples=scan.records_missing_pk_examples,
            pk_paths=scan.pk_paths,
            message="; ".join([*stream_errors, *stream_warnings, *stream_notes]),
        )

    return ComparisonResult(
        passed=all(r.passed for r in stream_results.values()),
        stream_results=stream_results,
        message=_pk_uniqueness_message(
            stream_results,
            version_label,
            new_inconclusive=partial and version_label == "target",
        ),
        errors=errors,
        warnings=warnings,
    )


def _pk_uniqueness_message(
    stream_results: dict[str, StreamComparisonResult],
    version_label: str = "",
    new_inconclusive: bool = False,
) -> str:
    """The check-level message, shared with the merge of per-stream results.

    A passing check's duplicates are named from the split the stream results
    carry: pre-existing ones are in both versions' output; fixed and lost
    ones only in the control's -- the target emits them once at most, so its
    row does not mention them. "Fixed" is said only of values whose records
    all reached the target; values with records the target dropped or
    changed are named apart, as a pointer to the checks that fail on them.

    `new_inconclusive` marks the target's result on a partial read, where new
    duplicates warn rather than fail. Both versions' results carry the same
    split, so the control's must not pass it. The control's duplicates that
    are none of pre-existing, fixed or lost are the ones a partial read does
    not classify (`_unclassified_duplicate_pk_count`); they are named as not
    duplicated in the target.
    """
    label = f" in {version_label}" if version_label else ""
    if not all(r.passed for r in stream_results.values()):
        return f"Primary key integrity issues found{label}"
    results = stream_results.values()
    if new_inconclusive and any(r.new_duplicate_pk_count for r in results):
        return (
            f"New duplicate primary keys{label} (inconclusive on a stopped-early read)"
        )
    pre_existing = any(r.pre_existing_duplicate_pk_count for r in results)
    in_control = version_label == "control"
    fixed = in_control and any(r.fixed_duplicate_pk_count for r in results)
    lost = in_control and any(r.lost_duplicate_pk_count for r in results)
    unclassified = in_control and any(
        _unclassified_duplicate_pk_count(r) for r in results
    )
    if pre_existing and fixed:
        message = (
            f"Pre-existing duplicate primary keys{label}, and others fixed in "
            "target (not a regression)"
        )
    elif pre_existing:
        message = f"Pre-existing duplicate primary keys{label} (not a regression)"
    elif fixed:
        message = "Duplicate primary keys in control fixed in target (not a regression)"
    else:
        message = ""
    if unclassified:
        unclassified_message = "not duplicated in target (partial read)"
        if message:
            return f"{message}; others {unclassified_message}"
        return f"Duplicate primary keys in control {unclassified_message}"
    if lost:
        lost_message = (
            "with records the target dropped or changed (field values or PK "
            "presence fail on them)"
        )
        if message:
            return f"{message}; others {lost_message}"
        return f"Duplicate primary keys in control {lost_message}"
    return message or f"All primary keys unique and present{label}"


def _unclassified_duplicate_pk_count(result: StreamComparisonResult) -> int:
    """The control's duplicates a partial read leaves neither fixed nor lost.

    A complete read classifies every control duplicate as pre-existing,
    fixed or lost, so this is 0 there; on a partial read fixed and lost stay
    0 and the control-only duplicates are what is left.
    """
    return max(
        0,
        result.duplicate_pk_count
        - result.pre_existing_duplicate_pk_count
        - result.fixed_duplicate_pk_count
        - result.lost_duplicate_pk_count,
    )


def compare_all_records(
    control_records: Mapping[str, Sequence[AirbyteMessage]],
    target_records: Mapping[str, Sequence[AirbyteMessage]],
    primary_keys_per_stream: dict[str, PrimaryKeys | None] | None = None,
    exclude_paths: list[str] | None = None,
    directional: bool = False,
    partial: bool = False,
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

    When `partial` is True (a side was stopped early), a difference on a PK
    value with more than one record on either side is reported and does not
    fail, and no added copies are counted: a cap or a deadline can cut such a
    group on one side (`RecordDiff.partial_group_diffs`). A PK value both
    sides emitted once is still compared strictly.

    Based on airbyte-ci implementation:
    https://github.com/airbytehq/airbyte/blob/master/airbyte-ci/connectors/live-tests/src/live_tests/regression_tests/test_read.py#L133-L183
    """
    if exclude_paths is None:
        exclude_paths = EXCLUDE_PATHS

    if primary_keys_per_stream is None:
        primary_keys_per_stream = {}

    stream_results: dict[str, StreamComparisonResult] = {}
    errors: list[str] = []
    warnings: list[str] = []

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
                partial=partial,
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
        messages: list[str] = []
        if not passed:
            messages.append(f"Stream {stream_name} has record differences")
            errors.append(messages[-1])
        stream_warnings = _record_diff_warnings(stream_name, record_diff)
        messages.extend(stream_warnings)
        warnings.extend(stream_warnings)

        stream_results[stream_name] = StreamComparisonResult(
            stream_name=stream_name,
            passed=passed,
            control_count=len(control_msgs),
            target_count=len(target_msgs),
            record_diff=record_diff,
            message="; ".join(messages),
        )

    return ComparisonResult(
        passed=all(r.passed for r in stream_results.values()),
        stream_results=stream_results,
        message=_field_values_message(stream_results),
        errors=errors,
        warnings=warnings,
    )


def _record_diff_warnings(stream_name: str, record_diff: RecordDiff) -> list[str]:
    """A stream's field-value findings that warn rather than fail."""
    warnings: list[str] = []
    if record_diff.added_copy_count:
        copies = "copy" if record_diff.added_copy_count == 1 else "copies"
        warnings.append(
            f"Stream {stream_name}: {record_diff.added_copy_pk_count:,} "
            f"duplicated PK value(s) emit {record_diff.added_copy_count:,} "
            f"more identical {copies} in target than in control"
        )
    if record_diff.partial_group_diff_count:
        warnings.append(
            f"Stream {stream_name}: {record_diff.partial_group_diff_count:,} "
            "duplicated PK value(s) whose records differ, inconclusive on a "
            "stopped-early read: a cap or deadline can cut a PK's records on "
            "one side"
        )
    return warnings


def _field_values_message(stream_results: dict[str, StreamComparisonResult]) -> str:
    """The field check's message, shared with the merge of per-stream results."""
    if not all(r.passed for r in stream_results.values()):
        return "Record differences found"
    if any(
        r.record_diff and r.record_diff.partial_group_diff_count
        for r in stream_results.values()
    ):
        return (
            "All records match, apart from duplicated PK values that are "
            "inconclusive on a stopped-early read"
        )
    if any(
        r.record_diff and r.record_diff.added_copy_count
        for r in stream_results.values()
    ):
        return "All records match, apart from identical copies the target added"
    return "All records match"


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
        # sees, so order by that -- with the identity as a tie-breaker, because
        # two streams can render the same label and the label alone leaves their
        # order to set iteration, which string hashing randomises per process.
        # Which of the two then got the bare label and which got `(2)` would
        # change between runs of the same comparison.
        #
        # Namespace before name in the tie-break, matching the order
        # `compare_final_states` sorts by, so a collision is qualified the same
        # way on both surfaces. Breaking the tie by name instead would agree with
        # it only where the combined label happens to sort like the bare name:
        # for a stream `z.a` beside `a` in namespace `z`, name-first hands the
        # bare `z.a` to the namespaced stream while the state comparison hands it
        # to the other, so one report's two tables would point at each other's
        # stream. Colliding ids tie on the label, so this orders exactly as the
        # state comparison does.
        key=lambda stream_id: (
            stream_label(*stream_id),
            stream_id[0] or "",
            stream_id[1],
            stream_id[0] is not None,
        ),
    ):
        # Two distinct streams can render the same label -- `public.users`
        # the name beside `users` in the `public` namespace -- and a shared
        # label must not collapse them into one result either.
        label = unique_label(stream_label(*stream_id), stream_results)
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
            # `ignore_private_variables=False` for the reason
            # `compare_final_states` passes it: DeepDiff's default drops every
            # key beginning with `__`, and a connector's own `__`-prefixed
            # field -- `__v` on a Mongo-shaped source, `__typename` passed
            # through from a GraphQL API -- is data it declared, not a Python
            # private. On the default a stream that added, removed or retyped
            # such a field would compare equal and the check would report the
            # schema unchanged.
            diff = DeepDiff(
                control_stream, target_stream, ignore_private_variables=False
            )
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


def compare_final_states(
    control_states: dict[tuple[str | None, str], Any] | None,
    target_states: dict[tuple[str | None, str], Any] | None,
) -> ComparisonResult:
    """Compare the last state each version emitted per stream.

    The state a `read` leaves behind is what the next incremental sync resumes
    from, and nothing else in the run checks it: a target version that drops a
    cursor key, renames it or changes its type exits 0 like any other, and the
    damage only shows up as missed or duplicated records on a customer's next
    sync.

    The verdict is deliberately two-tiered:

    - A *structural* difference -- a stream with state on only one side, or a
      key or type added or removed inside the state blob -- fails. The shape of
      a state blob is a contract between a version and its own future runs.
    - A *value-only* difference under an identical shape is reported and does
      not gate, via `value_only`. Until HTTP replay lands
      (airbyte-internal-issues#16837) the two versions hit the live API in
      separate runs, so a timestamp cursor legitimately advances between them;
      failing on that would redden every incremental read and train reviewers to
      click past the check.

    Args:
        control_states: The control version's final state per stream identity,
            as `ExecutionResult.get_final_state_per_stream` returns it -- keyed
            by `(namespace, name)`, not by the label it displays as, so two
            streams that render the same label stay two streams here.
        target_states: The same, for the target version.

    Returns:
        A per-stream result whose `schema_diff` holds the diff for that stream.
    """
    control = control_states or {}
    target = target_states or {}

    if not control and not target:
        # Not a pass, and not a failure either. Emitting no state at all is
        # unusual rather than impossible -- note it is *not* what a
        # full-refresh-only read does, since the Python CDK emits a terminal
        # sentinel state per stream even there -- but a connector old enough to
        # predate that, or one that died before its first checkpoint, has
        # nothing here through no fault of the target version. So this cannot
        # hard-fail the way a `discover` with no catalog does, while a check
        # that went green over something it never looked at is how a silent
        # state regression ships. The message is the whole finding, so it is
        # not repeated as an error the summary would print twice.
        return ComparisonResult(
            passed=False,
            message="Neither version emitted any state; nothing was compared",
            inconclusive=True,
        )

    stream_results: dict[str, StreamComparisonResult] = {}
    findings: list[tuple[int, str]] = []
    warnings: list[str] = []
    tally = {_MISSING_STATE: 0, _CHANGED_STATE: 0}
    value_changes = 0
    structural = False

    for stream_id in sorted(
        set(control) | set(target),
        # By identity, not by the label: `None` sorts against `str` otherwise,
        # and two streams can render the same label -- ordering by that would
        # let emission order decide which of them is labelled first, so the two
        # sides could disagree about which stream a label refers to. The third
        # component keeps the order total where the first two tie, which is how
        # a stream named `(shared)` sorts against the shared-state key: without
        # it the tie would fall to set iteration order, and which of the two got
        # the unqualified label would change between runs.
        key=lambda stream_id: (
            stream_id[0] or "",
            stream_id[1],
            stream_id[0] is not None,
        ),
    ):
        # A shared label must not collapse two streams into one result, for the
        # reason the catalog comparison qualifies its own: `public.users` the
        # name beside `users` in the `public` namespace.
        label = unique_label(stream_label(*stream_id), stream_results)

        if stream_id not in control or stream_id not in target:
            structural = True
            side = "control" if stream_id in target else "target"
            message = f"State for {label} is missing on the {side}"
            tally[_MISSING_STATE] += 1
            findings.append((_MISSING_STATE, message))
            stream_results[label] = StreamComparisonResult(
                stream_name=label, passed=False, message=message
            )
            continue

        # No `ignore_order`, for the same reason the catalog comparison uses
        # none: a reordered list is a difference worth seeing, not noise to
        # normalise away. It does not *gate*, though -- DeepDiff encodes a pure
        # reorder of same-shaped elements as `values_changed`, which the
        # classifier treats as value-only, so a reorder warns rather than fails.
        # That is deliberate: a substream's partition list can legitimately come
        # back in a different order from two live-API runs, and failing on it
        # would redden those runs exactly the way failing on a moved cursor
        # would. Without `ignore_order` it is at least visible as a change; with
        # it the reorder would vanish entirely.
        #
        # `ignore_private_variables=False` because DeepDiff defaults it to
        # True, which drops every key beginning with `__` -- and the terminal
        # state of a full-refresh stream is nothing but such a key:
        # `{"__ab_no_cursor_state_message": true}` for a plain full refresh,
        # `{"__ab_full_refresh_sync_complete": true}` once the stream is
        # resumable. On the default, every full-refresh stream's state
        # normalises to `{}` on both sides and the check reports "unchanged"
        # over a state it never looked at -- including a swap from one sentinel
        # to the other, which is a real change to what the next sync resumes
        # from. These are the connector's own keys, not Python privates.
        diff = DeepDiff(
            control[stream_id], target[stream_id], ignore_private_variables=False
        )
        if not diff:
            stream_results[label] = StreamComparisonResult(
                stream_name=label, passed=True
            )
            continue

        if _is_value_only_diff(diff):
            value_changes += 1
            message = f"State for {label} changed value"
            warnings.append(message)
        else:
            structural = True
            message = f"State for {label} changed shape"
            tally[_CHANGED_STATE] += 1
            findings.append((_CHANGED_STATE, message))

        stream_results[label] = StreamComparisonResult(
            stream_name=label,
            passed=False,
            schema_diff=_jsonable_diff(diff),
            message=message,
        )

    all_passed = all(result.passed for result in stream_results.values())
    # Severity first: a summary that names only the first few findings must not
    # spend them on a moved cursor while a dropped state key waits below.
    errors = [message for _rank, message in sorted(findings, key=lambda f: f[0])]

    return ComparisonResult(
        passed=all_passed,
        stream_results=stream_results,
        message=(
            f"Final state unchanged across {_count(len(stream_results), 'stream')}"
            if all_passed
            else _final_state_change_message(tally, value_changes)
        ),
        errors=errors,
        warnings=warnings,
        value_only=not all_passed and not structural,
    )


# How the final-state findings are ordered before anything truncates them. A
# stream whose state exists on only one side comes first: the next sync has
# nothing to resume from, or resumes from something the other version never had.
_MISSING_STATE = 0
_CHANGED_STATE = 1

# The one DeepDiff verdict that means "the same shape holds a different scalar".
# Every other verdict -- `dictionary_item_added`, `dictionary_item_removed`,
# `type_changes`, `iterable_item_added`, `iterable_item_removed`, and anything
# DeepDiff grows later -- restructures the blob, so the check fails closed on
# keys it does not recognise rather than waving them through as drift.
_VALUE_DIFF_KEY = "values_changed"

# A masked value, as `masking.mask_value` writes it: the type it had, its
# length where it has one, and a truncated hash.
_TOKEN = re.compile(
    r"^(string|integer|number|boolean|null|array|object|unknown)(_len-\d+)?_[0-9a-f]{16}$"
)


def _token_type(value: Any) -> str | None:
    """The type a masked value's token carries, or `None` for a raw value."""
    if not isinstance(value, str):
        return None
    match = _TOKEN.match(value)
    return match.group(1) if match else None


def _is_token_type_change(change: Any) -> bool:
    """Whether a `values_changed` entry is two tokens of different types.

    Under masking both sides of a retyped cursor are strings, so DeepDiff
    files the change as a moved value rather than a `type_changes`. The token
    still carries the type, and a type that moved is the shape of the state
    changing, exactly as it is for raw values.
    """
    if not isinstance(change, dict):
        return False
    old_type = _token_type(change.get("old_value"))
    new_type = _token_type(change.get("new_value"))
    return old_type is not None and new_type is not None and old_type != new_type


def _is_value_only_diff(diff: DeepDiff) -> bool:
    """Whether a state's diff is a cursor that moved, not a state redeclared."""
    if set(diff.keys()) != {_VALUE_DIFF_KEY}:
        return False
    changes = diff[_VALUE_DIFF_KEY]
    if not isinstance(changes, dict):
        return True
    return not any(_is_token_type_change(change) for change in changes.values())


def _final_state_change_message(tally: dict[int, int], value_changes: int) -> str:
    """Say what moved in the state, by kind.

    A moved cursor and a dropped cursor key are one sentence apart and several
    severities apart, so the summary never calls them both "changed".
    """
    clauses = [
        clause
        for count, clause in (
            (
                tally[_MISSING_STATE],
                f"{_count(tally[_MISSING_STATE], 'stream')} with state on one side only",
            ),
            (
                tally[_CHANGED_STATE],
                f"{_count(tally[_CHANGED_STATE], 'stream')} whose state changed shape",
            ),
            (
                value_changes,
                f"{_count(value_changes, 'stream')} whose state changed value",
            ),
        )
        if count
    ]

    return f"Final state: {', '.join(clauses)}"


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
    control = to_plain_dict(control_spec)
    target = to_plain_dict(target_spec)

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
    The state comparison keys streams the same way, so both agree on what a
    stream is.

    Returns:
        The index and the problems found, or `(None, [])` when there is no
        catalog at all. A stream that cannot be indexed is reported rather than
        dropped: an unreadable entry is not an unchanged one.
    """
    plain = to_plain_dict(catalog)
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

        stream_id = to_stream_id(stream.get("namespace"), name)

        if stream_id in indexed:
            problems.append(
                f"stream {stream_label(*stream_id)} is declared more than once"
            )
            continue

        indexed[stream_id] = stream

    return indexed, problems


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
    messages: Sequence[AirbyteMessage],
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
    control_msgs: Sequence[AirbyteMessage],
    target_msgs: Sequence[AirbyteMessage],
    pk_fields: PrimaryKeys,
    exclude_paths: list[str],
    partial: bool = False,
) -> RecordDiff:
    """Compare records using primary keys for matching.

    Records with missing/null PK values are excluded from the lookup —
    they would otherwise collide on the same key and silently collapse.
    `check_pk_uniqueness` reports them as an error.

    A PK emitted more than once keeps every one of its records, and the two
    versions' groups for it are compared as multisets (`_record_group_diff`):
    a pre-existing duplicate no longer fails the run, so the comparison has
    to be right about it, and the same rows in a different emission order
    are not a change. On a `partial` read such a PK's findings are reported
    apart and never fail (`_ValueDiffTally`).

    A stream read from disk (`_RecordsFile`) goes through
    `_compare_records_with_pk_by_fingerprint` instead, which returns the same
    result without holding either side's records.
    """
    if isinstance(control_msgs, _RecordsFile) or isinstance(target_msgs, _RecordsFile):
        return _compare_records_with_pk_by_fingerprint(
            stream_name, control_msgs, target_msgs, pk_fields, exclude_paths, partial
        )

    control_by_pk = _group_records_by_pk(control_msgs, pk_fields)
    target_by_pk = _group_records_by_pk(target_msgs, pk_fields)

    control_pks = set(control_by_pk.keys())
    target_pks = set(target_by_pk.keys())

    only_in_control = control_pks - target_pks
    only_in_target = target_pks - control_pks

    tally = _ValueDiffTally(partial=partial)
    # Sorted (`key=repr`: PK tuples mix types) so the kept examples are the
    # same ones on every run; set iteration order varies per process.
    for pk in sorted(control_pks & target_pks, key=repr):
        control_group = control_by_pk[pk]
        target_group = target_by_pk[pk]
        tally.add(
            pk,
            len(control_group),
            len(target_group),
            *_pk_group_diff(control_group, target_group, exclude_paths),
        )

    return RecordDiff(
        stream_name=stream_name,
        # Sorted for the same reason as the value-diff examples: which few
        # records survive the example cap must not change run to run.
        records_only_in_control=[
            control_by_pk[pk][0]
            for pk in sorted(only_in_control, key=repr)[:MAX_EXAMPLE_DIFFS]
        ],
        records_only_in_target=[
            target_by_pk[pk][0]
            for pk in sorted(only_in_target, key=repr)[:MAX_EXAMPLE_DIFFS]
        ],
        records_only_in_control_count=len(only_in_control),
        records_only_in_target_count=len(only_in_target),
        pk_paths=pk_fields,
        **tally.fields(),
    )


@dataclass
class _ValueDiffTally:
    """The value-diff findings on one stream's shared PK values, as found.

    Only the first `MAX_EXAMPLE_DIFFS` findings of each kind are kept as
    examples; the counts cover all of them. Shared by the in-memory and the
    fingerprint comparison, so the two count the same way.

    On a `partial` read a PK value with more than one record on either side
    is judged apart: a cap or a deadline can cut its records on one side, so
    a lost record, records left on both sides and a capped group may only
    say where each side stopped. Its difference goes to
    `partial_group_diffs` and never fails, and its added copies are not
    counted, since the control may have stopped before them. A PK value both
    sides emitted once keeps the strict rule.
    """

    partial: bool
    value_diffs: list[dict[str, Any]] = field(default_factory=list)
    value_diff_count: int = 0
    partial_group_diffs: list[dict[str, Any]] = field(default_factory=list)
    partial_group_diff_count: int = 0
    added_copy_count: int = 0
    added_copy_pk_count: int = 0
    added_copy_pks: dict[Any, int] = field(default_factory=dict)

    def add(
        self,
        pk: tuple,
        control_size: int,
        target_size: int,
        example: dict[str, Any] | None,
        added_copies: int,
    ) -> None:
        """Count one shared PK value's example (or None) and its added copies."""
        if self.partial and (control_size > 1 or target_size > 1):
            if example is not None:
                self.partial_group_diff_count += 1
                if len(self.partial_group_diffs) < MAX_EXAMPLE_DIFFS:
                    self.partial_group_diffs.append({"pk": pk, **example})
            return
        if added_copies:
            self.added_copy_count += added_copies
            self.added_copy_pk_count += 1
            if len(self.added_copy_pks) < MAX_EXAMPLE_PKS:
                self.added_copy_pks[pk] = added_copies
        if example is not None:
            self.value_diff_count += 1
            if len(self.value_diffs) < MAX_EXAMPLE_DIFFS:
                self.value_diffs.append({"pk": pk, **example})

    def fields(self) -> dict[str, Any]:
        """The `RecordDiff` fields this tally fills."""
        return {
            "records_with_value_diff": self.value_diffs,
            "records_with_value_diff_count": self.value_diff_count,
            "partial_group_diffs": self.partial_group_diffs,
            "partial_group_diff_count": self.partial_group_diff_count,
            "added_copy_count": self.added_copy_count,
            "added_copy_pk_count": self.added_copy_pk_count,
            "added_copy_pks": self.added_copy_pks,
        }


def _group_records_by_pk(
    messages: list[AirbyteMessage], pk_fields: PrimaryKeys
) -> dict[tuple, list[dict[str, Any]]]:
    """Every record of each PK value, in emission order; missing-PK records skipped."""
    by_pk: dict[tuple, list[dict[str, Any]]] = {}
    for msg in messages:
        if msg.record and msg.record.data:
            pk = _extract_pk_tuple(msg.record.data, pk_fields)
            if not _pk_has_missing_values(pk):
                by_pk.setdefault(pk, []).append(
                    json.loads(msg.record.model_dump_json())
                )
    return by_pk


# One record's entry in a fingerprint index: its position in the stream and
# `_record_fingerprint` of it.
_FingerprintEntry = tuple[int, bytes | None]


def _compare_records_with_pk_by_fingerprint(
    stream_name: str,
    control_msgs: Sequence[AirbyteMessage],
    target_msgs: Sequence[AirbyteMessage],
    pk_fields: PrimaryKeys,
    exclude_paths: list[str],
    partial: bool = False,
) -> RecordDiff:
    """`_compare_records_with_pk` for streams read from disk, record by record.

    Each side keeps only the position and fingerprint of its records, per PK.
    A PK whose fingerprints match on both sides has nothing the full
    comparison would report, so it is skipped; the records of every other
    shared PK are loaded back and diffed by the same `_pk_group_diff`, and the
    one-sided examples are loaded the same way. The result is the one
    `_compare_records_with_pk` returns for the same records held in lists.
    """
    control_by_pk = _fingerprint_records_by_pk(control_msgs, pk_fields, exclude_paths)
    target_by_pk = _fingerprint_records_by_pk(target_msgs, pk_fields, exclude_paths)

    def load(
        messages: Sequence[AirbyteMessage], entries: list[_FingerprintEntry]
    ) -> list[dict[str, Any]]:
        return [_record_dict(messages[position]) for position, _ in entries]

    # The same set operations and sort as the in-memory comparison, so the
    # same PK spelling (`1` or `1.0`) reaches the examples in the same order.
    control_pks = set(control_by_pk.keys())
    target_pks = set(target_by_pk.keys())
    only_in_control = control_pks - target_pks
    only_in_target = target_pks - control_pks

    tally = _ValueDiffTally(partial=partial)
    for pk in sorted(control_pks & target_pks, key=repr):
        control_group = control_by_pk[pk]
        target_group = target_by_pk[pk]
        # The same multiset of fingerprints leaves nothing unmatched on either
        # side, so no difference and no added copies.
        if _fingerprints_match(control_group, target_group):
            continue
        tally.add(
            pk,
            len(control_group),
            len(target_group),
            *_pk_group_diff(
                load(control_msgs, control_group),
                load(target_msgs, target_group),
                exclude_paths,
            ),
        )

    return RecordDiff(
        stream_name=stream_name,
        records_only_in_control=[
            _record_dict(control_msgs[control_by_pk[pk][0][0]])
            for pk in sorted(only_in_control, key=repr)[:MAX_EXAMPLE_DIFFS]
        ],
        records_only_in_target=[
            _record_dict(target_msgs[target_by_pk[pk][0][0]])
            for pk in sorted(only_in_target, key=repr)[:MAX_EXAMPLE_DIFFS]
        ],
        records_only_in_control_count=len(only_in_control),
        records_only_in_target_count=len(only_in_target),
        pk_paths=pk_fields,
        **tally.fields(),
    )


def _fingerprint_records_by_pk(
    messages: Sequence[AirbyteMessage],
    pk_fields: PrimaryKeys,
    exclude_paths: list[str],
) -> dict[tuple, list[_FingerprintEntry]]:
    """`_group_records_by_pk` with each record's position and fingerprint in its place."""
    by_pk: dict[tuple, list[_FingerprintEntry]] = {}
    for position, msg in enumerate(messages):
        if msg.record and msg.record.data:
            pk = _extract_pk_tuple(msg.record.data, pk_fields)
            if not _pk_has_missing_values(pk):
                fingerprint = _record_fingerprint(_record_dict(msg), exclude_paths)
                by_pk.setdefault(pk, []).append((position, fingerprint))
    return by_pk


def _record_fingerprint(
    record: dict[str, Any], exclude_paths: list[str]
) -> bytes | None:
    """A digest of the record's `_canonical_record`, or None to compare it in full.

    Equal canonical keys mean records the single-pair comparison finds no
    difference between (`_canonical_record`), and the group matching pairs
    records on that same key. NaN and infinity are the exception:
    `_normalized_value` leaves them as floats, and NaN is spelled one way but
    never equal to itself. Pydantic writes both as null, so they do not reach
    a record dict today; a record that has one gets no fingerprint
    (`allow_nan=False` raises) rather than one that could hide a difference.
    """
    try:
        canonical = _canonical_record(record, exclude_paths, allow_nan=False)
    except ValueError:
        return None
    return hashlib.blake2b(canonical.encode(), digest_size=16).digest()


def _fingerprints_match(
    control_group: list[_FingerprintEntry], target_group: list[_FingerprintEntry]
) -> bool:
    """Whether one PK's records are the same multiset of fingerprints on both sides.

    True only where `_pk_group_diff` would find nothing: the fingerprint is a
    digest of `_canonical_record`, so `1`, `1.0` and `True`, and the same list
    in another order, give the same fingerprint, as they give the same key to
    the group matching and to `_single_record_diff`. False is not a
    difference in itself: lists that differ only in how often an item
    repeats fingerprint apart while DeepDiff calls them equal, and a record
    holding NaN or infinity has no fingerprint, so those records are loaded
    and diffed in full.
    """
    control = [fingerprint for _, fingerprint in control_group]
    target = [fingerprint for _, fingerprint in target_group]
    if None in control or None in target:
        return False
    return sorted(control) == sorted(target)


def _record_dict(message: AirbyteMessage) -> dict[str, Any]:
    """A record message as the plain dict the field comparison diffs."""
    return json.loads(message.record.model_dump_json())


def _compared_fields(
    record: dict[str, Any], exclude_paths: list[str]
) -> dict[str, Any]:
    return {key: value for key, value in record.items() if key not in exclude_paths}


def _canonical_record(
    record: dict[str, Any], exclude_paths: list[str], *, allow_nan: bool = True
) -> str:
    """The compared fields as sorted-key JSON: a hashable key for matching.

    Two records get the same key when the single-pair comparison would find
    no difference between them, so one keyed pass matches a group. That
    comparison treats `1`, `1.0` and `True` as one value (`==`) and ignores
    list order (DeepDiff `ignore_order=True`), so `_normalized_value` writes
    each bool and whole float as its int and sorts every list, at any depth.
    The record fingerprints of the comparison from disk
    (`_record_fingerprint`) are digests of this key, so they ignore list
    order too. The key still tells apart lists that differ only in how often
    an item repeats, which DeepDiff ignores: such records are left over, and
    `_record_group_diff` judges them.

    The protocol models write NaN and infinity as null, so they do not reach
    here today. `_normalized_value` leaves them as floats, so with
    `allow_nan=False` a record holding one still raises `ValueError`, which
    is how `_record_fingerprint` falls back to comparing it in full.
    """
    return json.dumps(
        _normalized_value(_compared_fields(record, exclude_paths)),
        sort_keys=True,
        default=str,
        allow_nan=allow_nan,
    )


def _normalized_value(value: Any) -> Any:
    """`value` with each bool and whole float as its int, and lists sorted.

    A list's items are normalized first, then sorted (`_list_item_order`).
    """
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, dict):
        return {key: _normalized_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return sorted((_normalized_value(item) for item in value), key=_list_item_order)
    return value


def _list_item_order(item: Any) -> tuple[int, Any]:
    """A sort key for normalized list items of any mix of types.

    Scalars sort by value within their kind, so a list of numbers or strings
    needs no JSON per item; containers sort by their sorted-key JSON. Two
    items with equal keys are equal, so the order is the same for any two
    lists holding the same items.
    """
    if item is None:
        return (0, 0)
    if isinstance(item, (int, float)):
        return (1, item)
    if isinstance(item, str):
        return (2, item)
    return (3, json.dumps(item, sort_keys=True, default=str))


def _pk_group_diff(
    control_group: list[dict[str, Any]],
    target_group: list[dict[str, Any]],
    exclude_paths: list[str],
) -> tuple[dict[str, Any] | None, int]:
    """One PK's value-diff example (or None) and the identical copies added.

    A single pair has no copies to add, so its count is always 0; a PK with
    more than one record on either side goes through `_record_group_diff`.
    """
    if len(control_group) == 1 and len(target_group) == 1:
        return (
            _single_record_diff(control_group[0], target_group[0], exclude_paths),
            0,
        )
    return _record_group_diff(control_group, target_group, exclude_paths)


def _single_record_diff(
    control_record: dict[str, Any],
    target_record: dict[str, Any],
    exclude_paths: list[str],
) -> dict[str, Any] | None:
    """The value-diff example for one PK-matched pair, or None when equal."""
    # Fast path: equal dicts cannot produce a diff, and DeepDiff with
    # ignore_order=True costs ~500\u00b5s per pair \u2014 which is every pair on
    # a passing run. Plain equality is ~0.9\u00b5s; skipping identical pairs
    # measured 13\u00d7 faster end-to-end on an all-identical stream.
    if _compared_fields(control_record, exclude_paths) == _compared_fields(
        target_record, exclude_paths
    ):
        return None
    # Equal keys are records the group matching pairs up and the comparison
    # from disk skips by fingerprint (`1`, `1.0` and `True` as one value, list
    # order ignored), so a single pair is judged the same way: on its own,
    # DeepDiff calls a bool beside an int in a reordered list a type change.
    if _canonical_record(control_record, exclude_paths) == _canonical_record(
        target_record, exclude_paths
    ):
        return None
    # `ignore_private_variables=False`: see `compare_catalog_schemas`. Note
    # the fast path above uses plain equality, so a pair differing only in a
    # `__`-prefixed field does reach here -- and on DeepDiff's default it
    # comes back empty, so the difference is silently not counted.
    diff = DeepDiff(
        control_record,
        target_record,
        ignore_order=True,
        ignore_private_variables=False,
        exclude_paths=[f"root['{p}']" for p in exclude_paths],
    )
    if not diff:
        return None
    return {"control": control_record, "target": target_record, "diff": diff.to_dict()}


def _record_group_diff(
    control_group: list[dict[str, Any]],
    target_group: list[dict[str, Any]],
    exclude_paths: list[str],
) -> tuple[dict[str, Any] | None, int]:
    """The value-diff example for a PK emitted more than once, and added copies.

    Returns the example (None when the group has no difference) and how many
    more identical copies the target emits than the control.

    The two groups are matched as multisets (`_unmatched_records`): each
    control record pairs with a target record equal to it on the compared
    fields (`exclude_paths` left out, as for a single pair), whatever the
    emission order -- a hold and a release row that come out swapped between
    two reads are the same records. A *copy* is a record equal, in that same
    sense, to another one. What is left unmatched decides:

    - Both sides have records left: the PK's records changed. A difference,
      listing the target's unmatched records against the control's lost ones
      -- leftovers that are not copies of a matched record -- or against all
      of the control's leftovers when each of them is a copy. The exception
      is when every leftover on both sides is a copy: the control's of a
      matched record, the target's of a matched or earlier leftover record.
      That is a collapsed copy next to an added copy, not a change, so it is
      no difference and the target's copies count as added copies.
    - Only the control has records left: one that is a copy of a matched
      record is a collapsed copy -- the target fixed a duplicate, and that
      passes. Any other is a lost record, a difference: the target no longer
      emits it.
    - Only the target has records left, under a PK the control already emits
      more than once: one that is a copy of a matched record, or of an
      earlier leftover target record, is an added copy. It is not a
      difference: it is counted and warns, because a live read with offset
      pagination can return the same row twice. Any other leftover is an
      added record and passes, like an extra PK. When the control emits the
      PK once, the leftovers are left to the PK-integrity check, which
      already fails them as a new duplicate.

    The rule is directional, like the rest of the record comparison: every
    control record must reach the target, and the target may add records.
    It is also what lets the record count allow for collapsed copies
    (`_allow_dropped_duplicate_rows`): a dropped row that was not a copy
    fails here. A lost record carries a `note` saying so, next to `pk`,
    `control`, `target` and `diff`.

    Each side of the example, and the DeepDiff, holds at most
    `MAX_GROUP_EXAMPLE_RECORDS` records, the first ones in canonical order; a
    capped example's note gives the full counts. Because the verdict on a
    capped group cannot rest on a diff of part of it, a capped group with
    leftovers on both sides is a difference even when that diff is empty.
    """
    key = _cached_record_key(exclude_paths)
    control_left, target_left = _unmatched_records(
        control_group, target_group, exclude_paths, key=key
    )
    if not control_left and not target_left:
        return None, 0

    def shown(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return sorted(records, key=key)[:MAX_GROUP_EXAMPLE_RECORDS]

    def compared(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [_compared_fields(record, exclude_paths) for record in records]

    if control_left and target_left:
        matched = _without_records(control_group, control_left)
        _collapsed, lost = _split_copies(control_left, matched, exclude_paths, key=key)
        added_copies, added = _split_copies(
            target_left,
            _without_records(target_group, target_left),
            exclude_paths,
            chained=True,
            key=key,
        )
        if not lost and not added:
            # Only copies on both sides: the target collapsed one copy and
            # repeated another record ({A, A, B} against {A, B, B}), as an
            # offset-pagination repeat that moved to another row does.
            # Collapsed copies pass and added copies warn.
            return None, len(added_copies)
        # Collapsed copies among the control's leftovers are not part of the
        # change, so the example shows the lost records against the target's
        # leftovers. When every leftover is a copy ({a, a} against {a, x}),
        # there is nothing else to show them against, so all of them stay.
        control_side = lost or control_left
        control_shown, target_shown = shown(control_side), shown(target_left)
        diff = DeepDiff(
            compared(control_shown),
            compared(target_shown),
            ignore_order=True,
            ignore_private_variables=False,
        )
        capped = max(len(control_side), len(target_left)) > MAX_GROUP_EXAMPLE_RECORDS
        # Uncapped, the diff covers every leftover, and an empty one means
        # they differ only in list item repetition, which the single-pair path
        # ignores too. Capped, it covers the shown ones only, so the group
        # fails closed: the keys already say the records do not match.
        if not diff and not capped:
            return None, 0
        example = {
            "control": control_shown,
            "target": target_shown,
            "diff": diff.to_dict(),
        }
        if capped:
            example["note"] = (
                f"{len(control_side):,} control and {len(target_left):,} target "
                "records of this PK do not match (first "
                f"{MAX_GROUP_EXAMPLE_RECORDS} of each shown)"
            )
            if not diff:
                example["note"] += (
                    "; the shown ones differ only in repeated list items, which "
                    "the diff ignores, so the difference may be past them"
                )
        return example, 0

    if control_left:
        matched = _without_records(control_group, control_left)
        _collapsed, lost = _split_copies(control_left, matched, exclude_paths, key=key)
        if not lost:
            return None, 0
        lost_shown = shown(lost)
        # One side is empty, so there is no order to ignore; without
        # `ignore_order` DeepDiff lists every record rather than one per value.
        diff = DeepDiff(compared(lost_shown), [], ignore_private_variables=False)
        return {
            "control": lost_shown,
            "target": [],
            "diff": diff.to_dict(),
            "note": (
                f"the target no longer emits {_records_text(len(lost))} of this PK"
                f"{_shown_text(len(lost))}"
            ),
        }, 0

    if len(control_group) == 1:
        return None, 0
    matched = _without_records(target_group, target_left)
    added_copies, _added = _split_copies(
        target_left, matched, exclude_paths, chained=True, key=key
    )
    return None, len(added_copies)


def _records_text(count: int) -> str:
    """`1 record`, `1,234 records`."""
    return f"{count:,} record" if count == 1 else f"{count:,} records"


def _shown_text(count: int) -> str:
    """` (first 20 shown)` when an example list was capped, else nothing."""
    if count <= MAX_GROUP_EXAMPLE_RECORDS:
        return ""
    return f" (first {MAX_GROUP_EXAMPLE_RECORDS} shown)"


def _cached_record_key(exclude_paths: list[str]) -> Callable[[dict[str, Any]], str]:
    """`_canonical_record` that computes each record's key once.

    A group needs a record's key for the matching, the copy split and the
    example order; with lists sorted at every depth the key is the costly
    part. Cached by identity, so the records must outlive the cache, as a
    group's records do.
    """
    keys: dict[int, str] = {}

    def key(record: dict[str, Any]) -> str:
        found = keys.get(id(record))
        if found is None:
            found = keys[id(record)] = _canonical_record(record, exclude_paths)
        return found

    return key


def _without_records(
    group: list[dict[str, Any]], records: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """`group` minus the given records, by identity: what was matched."""
    left_out = {id(record) for record in records}
    return [record for record in group if id(record) not in left_out]


def _split_copies(
    records: list[dict[str, Any]],
    originals: list[dict[str, Any]],
    exclude_paths: list[str],
    chained: bool = False,
    key: Callable[[dict[str, Any]], str] | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Split `records` into copies of an original and the rest, in that order.

    A copy equals an original on the compared fields, tested by canonical key
    (`key`, `_canonical_record` by default) the way `_unmatched_records`
    matches. With `chained`, a record that is not a copy becomes an original
    for the records after it, so the second of two new equal records is a
    copy.
    """
    key = key or (lambda record: _canonical_record(record, exclude_paths))
    keys = {key(record) for record in originals}
    copies: list[dict[str, Any]] = []
    rest: list[dict[str, Any]] = []
    for record in records:
        record_key = key(record)
        if record_key in keys:
            copies.append(record)
            continue
        rest.append(record)
        if chained:
            keys.add(record_key)
    return copies, rest


def _unmatched_records(
    control_group: list[dict[str, Any]],
    target_group: list[dict[str, Any]],
    exclude_paths: list[str],
    key: Callable[[dict[str, Any]], str] | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Each side's records with no equal record on the other side.

    One keyed pass on `_canonical_record` (or `key`), which agrees with the
    single-pair comparison (`1` and `1.0` match, list order is ignored), so
    a PK duplicated thousands of times stays linear even when nothing
    matches.
    """
    key = key or (lambda record: _canonical_record(record, exclude_paths))
    target_pool: dict[str, list[dict[str, Any]]] = {}
    for record in target_group:
        target_pool.setdefault(key(record), []).append(record)
    control_left: list[dict[str, Any]] = []
    for record in control_group:
        bucket = target_pool.get(key(record))
        if bucket:
            bucket.pop()
        else:
            control_left.append(record)
    target_left = [record for bucket in target_pool.values() for record in bucket]
    return control_left, target_left


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

    # `ignore_private_variables=False`: see `compare_catalog_schemas`.
    diff = DeepDiff(
        control_records,
        target_records,
        ignore_order=True,
        ignore_private_variables=False,
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
    # True when a side was stopped early (deadline or record cap), so the two
    # outputs end at different points. Record counts, PK presence, the
    # target's new duplicate PKs and the field values of duplicated PK values
    # are then reported rather than folded, and `passed` is decided by records
    # missing their PK and the field values of PK values both sides emitted
    # once. The fixed/lost split, added copies and the count allowance are not
    # computed: their counts stay 0.
    partial: bool = False
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
                "partial": self.partial,
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
    control_records: Mapping[str, Sequence[AirbyteMessage]],
    target_records: Mapping[str, Sequence[AirbyteMessage]],
    primary_keys_per_stream: dict[str, list | None],
    partial: bool = False,
) -> RecordComparisonSummary:
    """Run all record-level comparisons between control and target output.

    Checks, folded into a single pass/fail verdict:

    - Record counts (all streams): directional — the target must produce at
      least as many records as the control. For streams without a primary
      key this is the *only* check (records can't be matched without a PK,
      and live API data may legitimately grow between the two runs). On a
      stream with a PK, a shortfall within the drop in duplicate rows warns
      instead (`_allow_dropped_duplicate_rows`); the field values check that
      the dropped rows were copies.
    - Primary key presence (streams with a PK): every control PK value must
      appear in the target output. Extra PKs in the target are acceptable.
    - Primary key integrity (streams with a PK): each PK value must appear
      at most once per stream, and every record must carry a value for its
      declared PK fields; checked independently on the control and the
      target output. A missing PK value fails on either version — the
      declared primary key cannot be trusted regardless of which version
      introduced it. Duplicates are classified against the other version:
      a PK value duplicated in both is pre-existing and only warns, one
      duplicated in the target alone is new and fails (warns on a partial
      read), one duplicated in the control alone was fixed by the target and
      warns. Both versions' results carry the split.
    - Field values (streams with a PK): records matched by PK must have
      identical field values (excluding `emitted_at`). Records that exist
      only in the target do not fail the comparison (directional). A
      duplicated PK's records are matched as multisets: a record the target
      no longer emits fails, and extra identical copies under a PK the
      control already duplicates warn (`_record_group_diff`).

    Args:
        control_records: Control run records grouped by stream name.
        target_records: Target run records grouped by stream name.
        primary_keys_per_stream: Primary key definition per stream, either
            flat (`["id"]`) or nested (`[["id"]]`) format; falsy values
            mean the stream has no primary key.
        partial: Whether a side was stopped early, so the two outputs end at
            different points. A count drop or a PK the target never reached
            is then expected rather than a regression: record counts and PK
            presence are still computed and reported, but do not decide
            `passed`, and the field comparison judges only the records both
            sides emitted. A cap or a deadline can also cut a duplicated PK
            value's records on one side, so everything that rests on a whole
            group is reported, not failed, or not computed: a duplicate PK
            new in the target only warns; the field values of a PK value
            with more than one record on either side are reported apart
            (`RecordDiff.partial_group_diffs`); a control-only duplicate is
            neither fixed nor lost; no added copies are counted; and the
            record count gets no duplicate-row allowance, as it does not
            decide `passed` anyway. A PK value both sides emitted once is
            still compared strictly, and a record missing its declared PK
            value still fails -- that is wrong however much of the stream
            was read.
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
        control_pk_uniqueness, target_pk_uniqueness = _compare_pk_integrity(
            control_with_pk, target_with_pk, normalized_pks, partial=partial
        )
        # On a partial read the counts are diagnostic whatever they show, and
        # a cut target would only inflate the allowance.
        if not partial:
            _allow_dropped_duplicate_rows(
                count_comparison, control_pk_uniqueness, target_pk_uniqueness
            )
        field_comparison = compare_all_records(
            control_with_pk,
            target_with_pk,
            primary_keys_per_stream=normalized_pks,
            directional=True,
            partial=partial,
        )
        if partial:
            field_comparison = _matched_records_only(field_comparison)
        results.extend(
            [pk_presence, control_pk_uniqueness, target_pk_uniqueness, field_comparison]
        )

    def is_diagnostic(result: ComparisonResult) -> bool:
        return partial and (result is count_comparison or result is pk_presence)

    errors: list[str] = []
    for result in results:
        if is_diagnostic(result):
            warnings.extend(result.errors)
        else:
            errors.extend(result.errors)
        warnings.extend(result.warnings)

    return RecordComparisonSummary(
        passed=all(result.passed for result in results if not is_diagnostic(result)),
        partial=partial,
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
    partial: bool = False,
) -> RecordComparisonSummary:
    """Run all record-level comparisons from per-stream record files.

    Memory-bounded variant of `run_record_comparisons` for full connector
    outputs: it compares one stream at a time (both versions), runs the full
    set of checks on it, and merges the per-stream results. A stream is never
    loaded whole either: each check reads its records from the file
    (`_RecordsFile`), and the field comparison keeps only a position and a
    fingerprint per record, loading back the records whose fingerprints
    differ. Peak memory is the PK indexes of the largest stream -- a few
    hundred bytes per record -- rather than its records. Checks and the
    resulting summary are identical to the in-memory variant.

    Args:
        control_record_files: Control run per-stream record files (jsonl of
            Airbyte RECORD messages), e.g. from `split_records_per_stream`.
        target_record_files: Target run per-stream record files.
        primary_keys_per_stream: Primary key definition per stream, as for
            `run_record_comparisons`.
        partial: As for `run_record_comparisons`.
    """
    chunk_summaries: list[RecordComparisonSummary] = []
    for stream in sorted(set(control_record_files) | set(target_record_files)):
        control_chunk: dict[str, Sequence[AirbyteMessage]] = {}
        if stream in control_record_files:
            control_chunk[stream] = _read_records_file(control_record_files[stream])
        target_chunk: dict[str, Sequence[AirbyteMessage]] = {}
        if stream in target_record_files:
            target_chunk[stream] = _read_records_file(target_record_files[stream])

        chunk_summaries.append(
            run_record_comparisons(
                control_records=control_chunk,
                target_records=target_chunk,
                primary_keys_per_stream=primary_keys_per_stream,
                partial=partial,
            )
        )

    return _merge_summaries(chunk_summaries, partial=partial)


def _matched_records_only(result: ComparisonResult) -> ComparisonResult:
    """Re-judge a field comparison on the records both sides emitted.

    On a stopped-early read the sides end at different points, so a record
    only the control reached says nothing about the target version. A value
    that differs on a PK value both sides emitted once still does, and still
    fails: `records_with_value_diff_count` counts only those on a partial
    read, since the comparison already set apart the duplicated PK values
    (`RecordDiff.partial_group_diff_count`), which keep their warning.
    """
    stream_results: dict[str, StreamComparisonResult] = {}
    errors: list[str] = []
    for name, stream in result.stream_results.items():
        diff = stream.record_diff
        passed = diff is None or not diff.records_with_value_diff_count
        messages = [] if passed else [f"Stream {name} has record differences"]
        errors.extend(messages)
        if diff is not None:
            messages.extend(_record_diff_warnings(name, diff))
        stream_results[name] = replace(
            stream, passed=passed, message="; ".join(messages)
        )

    return ComparisonResult(
        passed=all(stream.passed for stream in stream_results.values()),
        stream_results=stream_results,
        message=_field_values_message(stream_results),
        errors=errors,
        warnings=result.warnings,
    )


def _read_records_file(records_path: Path) -> Sequence[AirbyteMessage]:
    """The record messages of a single per-stream jsonl file, read lazily.

    Full protocol validation happens here, not in the splitter: the splitter
    routes lines on a plain JSON parse, so a RECORD-typed line that fails
    protocol validation lands in the stream file (keeping the artifact an
    honest copy of what the connector emitted) and is skipped here.
    """
    return _RecordsFile(records_path)


class _RecordsFile(Sequence[AirbyteMessage]):
    """One stream's RECORD messages, read from its jsonl file when needed.

    Held as parsed messages, a large stream costs over ten times its size on
    disk, and a check only ever needs one record at a time. Construction reads
    the file once to note where each valid record starts; iterating reads and
    validates it again, and indexing seeks to the one record. The lines are
    those a text-mode read would see -- split on newlines, decoded as `open()`
    decodes, stripped -- so this holds exactly the records a list read from
    the file would. Positions only: there is no slicing.
    """

    def __init__(self, path: Path) -> None:
        self._path = path
        # What a text-mode `open()` decodes with, and so what the splitter
        # wrote the file in.
        self._encoding = locale.getpreferredencoding(False)
        self._offsets = array("q", (offset for offset, _ in self._scan()))

    def _scan(self) -> Iterator[tuple[int, AirbyteMessage]]:
        offset = 0
        with self._path.open("rb") as records_file:
            for raw_line in records_file:
                message = self._parse(raw_line)
                if message is not None:
                    yield offset, message
                offset += len(raw_line)

    def _parse(self, raw_line: bytes) -> AirbyteMessage | None:
        line = raw_line.decode(self._encoding).strip()
        if not line:
            return None
        try:
            message = AirbyteMessage.model_validate_json(line)
        except ValidationError:
            return None
        return message if message.type is AirbyteMessageType.RECORD else None

    def __len__(self) -> int:
        return len(self._offsets)

    def __iter__(self) -> Iterator[AirbyteMessage]:
        return (message for _, message in self._scan())

    def __getitem__(self, position: int) -> AirbyteMessage:
        with self._path.open("rb") as records_file:
            records_file.seek(self._offsets[position])
            message = self._parse(records_file.readline())
        if message is None:
            # IndexError, as a sequence's `__getitem__` raises: the record
            # this position was noted for is no longer there.
            raise IndexError(
                f"{self._path} changed while it was being compared: no record "
                f"at position {position}"
            )
        return message


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
    partial: bool = False,
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

    def merge_pk_uniqueness(
        results: list[ComparisonResult | None], version_label: str
    ) -> ComparisonResult | None:
        merged = merge(results, "", "")
        if merged is not None:
            merged.message = _pk_uniqueness_message(
                merged.stream_results,
                version_label,
                new_inconclusive=partial and version_label == "target",
            )
        return merged

    def merge_field_values(
        results: list[ComparisonResult | None],
    ) -> ComparisonResult | None:
        merged = merge(results, "", "")
        if merged is not None:
            merged.message = _field_values_message(merged.stream_results)
        return merged

    count_comparison = merge(
        [c.count_comparison for c in chunk_summaries], "", ""
    ) or ComparisonResult(passed=True)
    count_comparison.message = _record_count_message(count_comparison.stream_results)

    return RecordComparisonSummary(
        passed=all(c.passed for c in chunk_summaries),
        partial=partial,
        count_comparison=count_comparison,
        pk_presence=merge(
            [c.pk_presence for c in chunk_summaries],
            "All primary keys present",
            "Missing primary keys",
        ),
        control_pk_uniqueness=merge_pk_uniqueness(
            [c.control_pk_uniqueness for c in chunk_summaries], "control"
        ),
        target_pk_uniqueness=merge_pk_uniqueness(
            [c.target_pk_uniqueness for c in chunk_summaries], "target"
        ),
        field_comparison=merge_field_values(
            [c.field_comparison for c in chunk_summaries]
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
        for example in (
            *stream_info.get("value_diff_examples", []),
            *stream_info.get("partial_group_diff_examples", []),
        ):
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
                "pre_existing_duplicate_pk_count": r.pre_existing_duplicate_pk_count,
                "new_duplicate_pk_count": r.new_duplicate_pk_count,
                "fixed_duplicate_pk_count": r.fixed_duplicate_pk_count,
                "lost_duplicate_pk_count": r.lost_duplicate_pk_count,
                "duplicate_row_count": r.duplicate_row_count,
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


def _value_diff_examples_to_dict(
    examples: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    return [
        {
            "pk": entry.get("pk"),
            "diff": json_safe(entry.get("diff") or {}),
            # Set on a lost record inside a duplicated PK, or on a capped
            # group example (`_record_group_diff`).
            **({"note": entry["note"]} if entry.get("note") else {}),
        }
        for entry in examples[:MAX_EXAMPLE_DIFFS]
    ]


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
            "added_copy_count": diff.added_copy_count if diff else 0,
            "added_copy_pk_count": diff.added_copy_pk_count if diff else 0,
            "value_diff_examples": _value_diff_examples_to_dict(
                diff.records_with_value_diff if diff else []
            ),
            # Stopped-early reads only: duplicated PK values whose records
            # differ, reported and not failed. 0 and [] on a complete read.
            "partial_group_diff_count": diff.partial_group_diff_count if diff else 0,
            "partial_group_diff_examples": _value_diff_examples_to_dict(
                diff.partial_group_diffs if diff else []
            ),
        }
    return {
        "passed": result.passed,
        "message": result.message,
        "streams": streams,
    }
