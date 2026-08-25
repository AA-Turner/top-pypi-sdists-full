# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Regression-test report model and its two renderers.

A regression test surfaces its results in two places, and they must never
disagree:

- **`report.html`** in the run artifacts -- the detailed surface, with
  collapsible per-stream sections and diff blocks.
- **A concise markdown block** appended to `GITHUB_STEP_SUMMARY` -- the verdict,
  a per-check pass/fail table, per-stream record-count deltas, and a link to the
  HTML artifact, so the short story is readable without downloading anything.

Both render from one `RegressionReportModel`. Every verdict and every truncation
decision is made once, in the builders below; the renderers only lay out what
they are given. That is the mechanism that keeps the two surfaces consistent.

## Extension seams

The record-level comparison is wired in: `build_comparison_report_model` takes
the `RecordComparisonSummary` of a read run, folds one `CheckResult` per
comparison check into the verdict, and attaches per-stream detail blocks
(missing/duplicate PKs, field-value diffs) to the stream sections. The schema-,
state- and spec-level comparisons are not wired into the CLI yet. When they
are, they surface in **both** places without touching
`templates/report.html.j2`:

- Append a `CheckResult` per new check -- it becomes a row of the per-check
  table in both the HTML report and the step summary.
- Append `DiffBlock`s to the relevant `StreamSection.diff_blocks` -- each one
  renders as a labelled, collapsible, syntax-highlighted block inside that
  stream's section in the HTML report.

`DiffLine.kind` selects a CSS class, so a new token type is a CSS-only change.
Highlighting is done by pre-tokenizing here rather than with a client-side
highlighter: the report is a GitHub Actions artifact, opened from `file://` with
no network, so it has to be a single self-contained file.
"""

from __future__ import annotations

import datetime
import difflib
import json
import os
import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, replace
from itertools import zip_longest
from pathlib import Path
from typing import Any

from jinja2 import Environment, PackageLoader, select_autoescape
from markupsafe import Markup

from airbyte_ops_mcp.regression_tests.ci_output import (
    ComparisonOutcome,
    _describe_run,
    _format_delta,
    command_result_succeeded,
    evaluate_comparison_outcome,
    github_artifact_name,
    github_artifacts_url,
    github_run_url,
)
from airbyte_ops_mcp.regression_tests.regression.comparators import (
    EXCLUDE_PATHS,
    ComparisonResult,
    RecordComparisonSummary,
    RecordDiff,
    StreamComparisonResult,
    json_safe,
)

TEMPLATE_NAME = "report.html.j2"
CONSOLIDATED_TEMPLATE_NAME = "consolidated.html.j2"
HTML_REPORT_FILENAME = "report.html"
CONSOLIDATED_REPORT_FILENAME = "report.html"

# The contract between a per-command report and the consolidated one. Each
# report carries a JSON header and wraps its own body in markers, so the whole
# run can be folded into one page without re-running anything or persisting a
# second copy of the model. Comments, so they cannot affect rendering.
META_MARKER = "airbyte-regression-report-meta"
BODY_START_MARKER = "airbyte-regression-report-body:start"
BODY_END_MARKER = "airbyte-regression-report-body:end"

# Metric table titles. Named because the inline summary picks the record-count
# table out of the list by title.
MESSAGE_TYPES_TABLE = "Message Types"
RECORD_COUNTS_TABLE = "Record Count per Stream"
HTTP_TRAFFIC_TABLE = "HTTP Traffic"

# Caps applied by the builders, so both surfaces truncate identically and report
# the same "N omitted" numbers. `GITHUB_STEP_SUMMARY` is capped at 1 MiB per
# step, which is what bounds the inline table on a many-stream read.
MAX_DIFF_LINES_PER_BLOCK = 200
MAX_LINE_CHARS = 2_000
MAX_STREAM_SECTIONS = 200
MAX_INLINE_STREAM_ROWS = 25
INLINE_STREAM_TABLE_COLLAPSE_THRESHOLD = 10
# Stream names and check summaries are connector-derived and unbounded in the
# protocol, so any single markdown cell is clamped as well as the row count. A
# label is an identifier; a summary is a sentence, so they get different bounds.
MAX_LABEL_CHARS = 120
MAX_SUMMARY_CHARS = 400
# Lines of a failing side's output to inline. Enough to carry a traceback and
# the log lines around it, without turning the report into a log viewer. The
# byte window bounds the read itself: a failed `read` can leave a multi-gigabyte
# `stdout.txt`, and only its end is wanted.
MAX_OUTPUT_TAIL_LINES = 60
MAX_OUTPUT_TAIL_BYTES = 256_000
# Empty streams named in the coverage check before it says "and N more".
MAX_EMPTY_STREAMS_LISTED = 10
# Failing streams named in a record-comparison check summary before it says
# "and N more". The per-stream sections carry the full list either way.
MAX_FAILING_STREAMS_NAMED = 5
# Unchanged lines kept on each side of a change in a side-by-side record
# diff; longer unchanged runs collapse into a "N unchanged lines" divider.
SPLIT_DIFF_CONTEXT_LINES = 2
# Per-line cap for the raw DeepDiff block: far past any value a reader
# scrolls through, but a bound — 200 lines of connector-controlled blob
# columns must not produce an unboundedly large report.html.
MAX_DEEPDIFF_LINE_CHARS = 100_000
# Findings a failing check lists in the step summary before pointing at the
# report. A check's `summary` cell names the first few inline; this is the rest
# of the answer to "what changed", for the reader who never opens the artifact.
MAX_INLINE_FINDINGS = 15
# Share of a replaying target run's requests that may still hit the live API
# before the comparison stops being a comparison against identical data.
#
# 20% is the plan's deliberately loose starting value, chosen while replay is
# experimental and the check is diagnostic: the point today is to make poor
# coverage visible without warning on every run that refreshes a token. It is
# *not* the acceptance criterion, which is `live_flow_count` at or near zero --
# on a 2,000-flow read, 20% is 400 live requests, easily enough upstream drift
# to produce the false regression this whole feature exists to remove.
#
# Tighten it, most likely to a small absolute allowance rather than a ratio,
# before this check is ever promoted from diagnostic to strict.
MAX_LIVE_FLOW_RATIO = 0.2
# Unmatched URLs a failing coverage check names inline. Enough to see whether the
# shortfall is one shape of request -- a per-run job id, a clock-derived window --
# with the rest of the list left in the run's `http_metrics` payload.
MAX_LIVE_URLS_NAMED = 5

_TRUNCATION_SUFFIX = " …"

# The one check every run has: did the command itself succeed. Named because the
# verdict fold treats it as already accounted for.
_RUN_CHECK = "Command execution"
# Reported whenever the target run was asked to replay the control run's traffic.
_REPLAY_CHECK = "HTTP replay coverage"

# Glyphs for the inline summary, keyed by `CheckResult.status` so the step
# summary and the HTML report classify a check identically.
_CHECK_GLYPHS = {"pass": "✅", "warn": "⚠️", "fail": "❌"}


@dataclass(frozen=True)
class MetricRow:
    """One row of a metric table: a label plus one or two counts.

    `control` is `None` in single-version mode, where there is nothing to
    compare against and no delta to show.
    """

    label: str
    target: int
    control: int | None = None

    @property
    def delta(self) -> int | None:
        """Target minus control, or `None` in single-version mode."""
        if self.control is None:
            return None

        return self.target - self.control

    @property
    def changed(self) -> bool:
        """Whether the delta is non-zero, i.e. worth highlighting."""
        return bool(self.delta)


@dataclass(frozen=True)
class MetricTable:
    """A titled table of `MetricRow`s, with an optional bold total row."""

    title: str
    label_header: str
    rows: tuple[MetricRow, ...]
    total: MetricRow | None = None


@dataclass(frozen=True)
class DiffLine:
    """One pre-tokenized line of a diff or code block.

    `kind` selects a CSS class in the template (`add`, `del`, `ctx`, `meta`),
    which is how the HTML report gets highlighting with no highlighter
    dependency and no JavaScript. Adding a kind is a CSS-only change.

    `text` carries no leading `+`/`-` marker: the marker is drawn by CSS, so
    copying a block out of the report yields clean content.
    """

    kind: str
    text: str


@dataclass(frozen=True)
class SplitDiffRow:
    """One row of a side-by-side (control | target) diff table.

    `left` is the control side and `right` the target side; `None` means the
    row has no content on that side -- a record the target never produced has
    an empty right column, which is the point of the layout. A row with
    `header` set instead renders as a single full-width divider (an example
    label, or a "N unchanged lines" gap marker).
    """

    left: DiffLine | None = None
    right: DiffLine | None = None
    header: str = ""


@dataclass(frozen=True)
class DiffBlock:
    """A labelled, collapsible code block inside a stream section.

    Carries either `lines` (a single-column listing: output tails, connection
    objects) or `split_rows` (a side-by-side control-versus-target table,
    which is how the record comparison renders its detail). Extension seam:
    the schema, spec and state comparisons each append blocks here too and
    the template renders them without modification.
    """

    title: str
    language: str = "diff"
    lines: tuple[DiffLine, ...] = ()
    split_rows: tuple[SplitDiffRow, ...] = ()
    truncated_line_count: int = 0
    empty_message: str | None = None
    # One level of nesting: a check-level block summarizes its test in the
    # title and carries one child block per version with findings.
    children: tuple[DiffBlock, ...] = ()


@dataclass(frozen=True)
class StreamSection:
    """One collapsible section for a single stream.

    `status` drives the section's colour and whether it starts expanded:
    `pass`, `fail`, or `info` for a section that carries data but asserts
    nothing. Sections start as `info`; when the record comparison ran,
    `_apply_record_comparison` re-marks every compared stream `pass` or
    `fail` and attaches the failure detail as diff blocks.
    """

    stream: str
    status: str = "info"
    headline: str = ""
    metrics: tuple[MetricRow, ...] = ()
    diff_blocks: tuple[DiffBlock, ...] = ()


@dataclass(frozen=True)
class CheckResult:
    """One named pass/fail check -- a row of the per-check table in both surfaces.

    Extension seam: exactly one check is emitted today ("Command execution",
    derived from `command_result_succeeded`). Appending a check is enough to
    surface it in both places, and a failing `strict` check flips the run's
    verdict -- pass it to a builder as `extra_checks`, which folds it in.

    A failing `diagnostic` check is a warning instead: it is reported on both
    surfaces but does not affect the verdict. Use it for observations that are
    worth seeing and not worth failing a release over.

    `summary` may be connector-derived (a stream or field name), so the inline
    renderer passes it through `_inline_text`; do not pre-escape it here.

    `details` is everything the check found, where `summary` has room for the
    first few. A failing check lists them in the step summary, so the reader who
    never downloads the artifact still learns what changed rather than only that
    something did.
    """

    name: str
    passed: bool
    severity: str = "strict"
    summary: str = ""
    details: tuple[str, ...] = ()

    @property
    def status(self) -> str:
        """`pass`, `warn` or `fail` -- the one source both renderers agree on.

        An unrecognised severity is treated as strict, so a typo fails closed
        rather than quietly downgrading a real failure to a warning.
        """
        if self.passed:
            return "pass"
        if self.severity == "diagnostic":
            return "warn"

        return "fail"


@dataclass(frozen=True)
class ReportContext:
    """Everything needed to say which run produced a report.

    Carried in the HTML so a downloaded artifact is self-describing; the step
    summary gets this once from the workflow instead.
    """

    connector_name: str
    tester: str
    test_date: str
    command: str
    target_image: str
    target_version: str
    control_image: str | None = None
    control_version: str | None = None
    run_url: str | None = None
    artifact_name: str = ""
    artifact_url: str | None = None


@dataclass(frozen=True)
class RunSide:
    """One side of a report: the target, the control, or a lone single run.

    `exited_cleanly` is the container exit status and `passed` is the verdict.
    They differ for `check`, where the CDK exits 0 even when the connection
    fails.
    """

    role: str
    image: str
    version: str
    exit_code: int
    exited_cleanly: bool
    passed: bool
    description: str
    connection_status: str | None = None
    connection_status_message: str | None = None
    stdout_file: str | None = None
    stderr_file: str | None = None
    http_metrics: dict[str, Any] | None = None


@dataclass(frozen=True)
class RegressionReportModel:
    """The single model both report surfaces render from.

    `passed` is the authoritative verdict and is derived from the same helpers
    the markdown report and the CLI's GitHub outputs use, so no surface can
    state a different one.
    """

    mode: str
    command: str
    passed: bool
    verdict_label: str
    verdict_detail: str
    context: ReportContext
    sides: tuple[RunSide, ...]
    checks: tuple[CheckResult, ...]
    metric_tables: tuple[MetricTable, ...]
    stream_sections: tuple[StreamSection, ...] = ()
    omitted_stream_count: int = 0
    outcome: ComparisonOutcome | None = None
    # Extension seam for diffs that belong to the run rather than to one stream
    # -- a spec diff, for instance. Rendered above the per-stream sections.
    diff_blocks: tuple[DiffBlock, ...] = ()
    # The objects the run was given or discovered: configured catalog, input
    # state, discovered catalog. "Which catalog did this actually run with" is
    # the first question when a record count looks wrong.
    connection_objects: tuple[DiffBlock, ...] = ()

    @property
    def is_comparison(self) -> bool:
        """Whether this report compares two versions."""
        return self.mode == "comparison"


def _split_image(image: str) -> tuple[str, str]:
    """Split a connector image into its repository and its tag.

    A colon only introduces a tag when it comes after the last `/`: in
    `localhost:5000/my-connector` it is a registry port, and splitting on it
    would report the version as `5000/my-connector`.

    Returns:
        The repository, and the tag or `unknown` when the image carries none.
    """
    repository, separator, tag = image.rpartition(":")
    if not separator or "/" in tag:
        return image, "unknown"

    return repository, tag


def _image_version(image: str) -> str:
    """The tag of a connector image, or `unknown` when it carries none."""
    return _split_image(image)[1]


def _image_name(image: str) -> str:
    """The repository part of a connector image, without its tag."""
    return _split_image(image)[0]


def _truncate(text: str, limit: int = MAX_LINE_CHARS) -> str:
    """Clip one line to `limit` characters, marking it when clipped."""
    if len(text) <= limit:
        return text

    return text[:limit] + _TRUNCATION_SUFFIX


def build_diff_block(
    title: str,
    lines: list[DiffLine],
    language: str = "diff",
    empty_message: str | None = None,
    max_line_chars: int | None = MAX_LINE_CHARS,
) -> DiffBlock:
    """Build a `DiffBlock`, applying the shared per-block truncation caps.

    Extension seam: use this rather than constructing `DiffBlock` directly, so
    every producer of diff content truncates the same way and the HTML report
    can always say how much it dropped.

    The caps here are per block -- lines per block, characters per line. Nothing
    yet bounds how many blocks a report may hold, because nothing yet produces
    any: the first producer of diff content should add a per-section and
    report-wide budget, since only it can decide which blocks to drop first.
    """
    kept = [
        DiffLine(
            kind=line.kind,
            text=_truncate(line.text, max_line_chars)
            if max_line_chars is not None
            else line.text,
        )
        for line in lines
    ]
    truncated = max(0, len(kept) - MAX_DIFF_LINES_PER_BLOCK)

    return DiffBlock(
        title=title,
        language=language,
        lines=tuple(kept[:MAX_DIFF_LINES_PER_BLOCK]),
        truncated_line_count=truncated,
        empty_message=empty_message,
    )


def build_split_diff_block(
    title: str,
    rows: list[SplitDiffRow],
    empty_message: str | None = None,
) -> DiffBlock:
    """Build a side-by-side `DiffBlock`, applying the shared truncation caps.

    The same caps as `build_diff_block`, applied per row and per cell, so a
    split block and a single-column block truncate identically and state the
    same "N omitted" numbers.
    """
    kept = [
        SplitDiffRow(
            left=DiffLine(row.left.kind, _truncate(row.left.text))
            if row.left
            else None,
            right=DiffLine(row.right.kind, _truncate(row.right.text))
            if row.right
            else None,
            header=_truncate(row.header),
        )
        for row in rows[:MAX_DIFF_LINES_PER_BLOCK]
    ]
    truncated = max(0, len(rows) - MAX_DIFF_LINES_PER_BLOCK)

    return DiffBlock(
        title=title,
        split_rows=tuple(kept),
        truncated_line_count=truncated,
        empty_message=empty_message,
    )


def build_json_block(title: str, payload: str) -> DiffBlock:
    """Render a JSON document as a collapsible, capped code block.

    Used for the connection objects and for any other whole-document payload.
    The text is pretty-printed when it parses, and left as-is when it does not,
    so a malformed file is still shown rather than swallowed.
    """
    try:
        text = json.dumps(json.loads(payload), indent=2, sort_keys=True)
    except (json.JSONDecodeError, TypeError):
        text = payload

    return build_diff_block(
        title,
        [DiffLine(kind="ctx", text=line) for line in text.splitlines()],
        language="json",
        empty_message="Empty.",
    )


def _build_context(
    command: str,
    target_image: str,
    control_image: str | None,
) -> ReportContext:
    """Assemble the context block from the environment and the images under test."""
    artifact_name = github_artifact_name(command)

    return ReportContext(
        connector_name=_image_name(target_image),
        tester=os.getenv("GITHUB_ACTOR") or os.getenv("USER") or "unknown",
        test_date=datetime.datetime.now(datetime.timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S UTC"
        ),
        command=command,
        target_image=target_image,
        target_version=_image_version(target_image),
        control_image=control_image,
        control_version=_image_version(control_image) if control_image else None,
        run_url=github_run_url(),
        artifact_name=artifact_name,
        artifact_url=github_artifacts_url(),
    )


def _build_side(
    role: str,
    command: str,
    image: str,
    result: dict[str, Any],
) -> RunSide:
    """Describe one run for the report.

    Reads `result["success"]` as the container exit status and derives the
    verdict with `command_result_succeeded`, so the caller must pass the
    unannotated run result (see `_annotate_run_verdict` in `cli/cloud.py`).
    """
    return RunSide(
        role=role,
        image=image,
        version=_image_version(image),
        exit_code=result["exit_code"],
        exited_cleanly=bool(result["success"]),
        passed=command_result_succeeded(command, result),
        description=_describe_run(command, result),
        connection_status=result.get("connection_status"),
        connection_status_message=result.get("connection_status_message"),
        stdout_file=result.get("stdout_file"),
        stderr_file=result.get("stderr_file"),
        http_metrics=result.get("http_metrics") or None,
    )


def _comparison_metric_table(
    title: str,
    label_header: str,
    control_counts: dict[str, int],
    target_counts: dict[str, int],
    with_total: bool = False,
) -> MetricTable | None:
    """Build a control/target/delta table, or `None` when there is nothing to show."""
    if not control_counts and not target_counts:
        return None

    rows = tuple(
        MetricRow(
            label=label,
            control=control_counts.get(label, 0),
            target=target_counts.get(label, 0),
        )
        for label in sorted(set(control_counts) | set(target_counts))
    )
    total = (
        MetricRow(
            label="Total",
            control=sum(control_counts.values()),
            target=sum(target_counts.values()),
        )
        if with_total
        else None
    )

    return MetricTable(title=title, label_header=label_header, rows=rows, total=total)


def _single_metric_table(
    title: str,
    label_header: str,
    counts: dict[str, int],
    with_total: bool = False,
) -> MetricTable | None:
    """Build a single-count table, or `None` when there is nothing to show."""
    if not counts:
        return None

    rows = tuple(
        MetricRow(label=label, target=counts[label]) for label in sorted(counts)
    )
    total = (
        MetricRow(label="Total", target=sum(counts.values())) if with_total else None
    )

    return MetricTable(title=title, label_header=label_header, rows=rows, total=total)


def _format_count(value: int) -> str:
    """Render a count with thousands separators."""
    return f"{value:,}"


def _with_configured_streams(
    counts: dict[str, int], configured_streams: tuple[str, ...]
) -> dict[str, int]:
    """Fill in a zero for every configured stream that emitted no records.

    Counts are derived from the records themselves, so a stream that returned
    nothing is simply absent. Both surfaces read this dict, so filling it here
    is what makes a zero-record stream visible in the tables as well as in the
    per-stream sections -- and it cannot change a total.
    """
    return dict.fromkeys(configured_streams, 0) | counts


def _build_stream_sections(
    control_counts: dict[str, int] | None,
    target_counts: dict[str, int],
    configured_streams: tuple[str, ...] = (),
    failing_streams: frozenset[str] = frozenset(),
) -> tuple[tuple[StreamSection, ...], int]:
    """Build one section per stream, capped at `MAX_STREAM_SECTIONS`.

    Sections are `info`, never `pass`/`fail`: a record-count delta is reported
    here but does not decide anything yet. Returns the sections plus how many
    streams were omitted by the cap.

    Args:
        control_counts: The control side's per-stream counts, or `None` in
            single-version mode. An empty dict is a control run that emitted no
            records at all, which still gets compared.
        target_counts: The target side's per-stream counts.
        configured_streams: Every stream the run was configured to read. Counts
            come from the records themselves, so a stream that emitted nothing
            has no entry -- without this it would be missing from the report
            entirely rather than shown as zero.
        failing_streams: Streams the record comparison failed. Sorted to the
            front so the section cap can never hide a failing stream behind
            200 alphabetically-earlier passing ones -- the detail blocks are
            attached per section, so a failing stream past the cap would
            lose its detail entirely.
    """
    every_stream = (
        set(control_counts or {}) | set(target_counts) | set(configured_streams or ())
    )
    all_streams = sorted(every_stream & failing_streams) + sorted(
        every_stream - failing_streams
    )
    omitted = max(0, len(all_streams) - MAX_STREAM_SECTIONS)

    sections: list[StreamSection] = []
    for stream in all_streams[:MAX_STREAM_SECTIONS]:
        target_count = target_counts.get(stream, 0)
        if control_counts is not None:
            control_count = control_counts.get(stream, 0)
            row = MetricRow(label=stream, control=control_count, target=target_count)
            if row.changed:
                headline = (
                    f"{_format_count(control_count)} → "
                    f"{_format_count(target_count)} records ({row.delta:+d})"
                )
            elif not target_count:
                headline = "no records emitted"
            else:
                headline = f"{_format_count(target_count)} records (unchanged)"
        else:
            row = MetricRow(label=stream, target=target_count)
            headline = (
                f"{_format_count(target_count)} records"
                if target_count
                else "no records emitted"
            )

        sections.append(
            StreamSection(
                stream=stream,
                status="info",
                headline=headline,
                metrics=(row,),
            )
        )

    return tuple(sections), omitted


def _tail_lines(path_text: str | None, limit: int = MAX_OUTPUT_TAIL_LINES) -> list[str]:
    """Read the last `limit` lines of a file, or nothing when it is unreadable.

    Reads a bounded window from the end rather than the whole file: this runs on
    a failed run, and a failed `read` leaves a `stdout.txt` holding every record
    it managed to emit, which can be gigabytes.

    Best effort by design: the report must render even when the container never
    produced the file, or the path belongs to a machine this is not running on.
    """
    if not path_text:
        return []

    try:
        with Path(path_text).open("rb") as handle:
            handle.seek(0, os.SEEK_END)
            size = handle.tell()
            handle.seek(max(0, size - MAX_OUTPUT_TAIL_BYTES))
            window = handle.read()
    except OSError:
        return []

    lines = window.decode("utf-8", errors="replace").splitlines()
    if size > MAX_OUTPUT_TAIL_BYTES and lines:
        # The window almost certainly starts mid-line; a half line is misleading.
        del lines[0]

    return lines[-limit:]


def build_failure_output_blocks(sides: tuple[RunSide, ...]) -> tuple[DiffBlock, ...]:
    """Attach the tail of each failing side's output to the report.

    "Why did the target crash" is the most common reason to open the report, and
    a path into an artifact the reader has not downloaded does not answer it.
    `stderr` first: a connector that died usually says why there. `stdout` is
    the fallback, since a connector that logs everything as Airbyte messages
    leaves `stderr` empty.

    Note for obfuscation work: this puts raw connector output on the page, so it
    must be scrubbed by whatever scrubs `stdout.txt` and `stderr.txt`.
    """
    blocks: list[DiffBlock] = []
    for side in sides:
        if side.passed:
            continue

        for label, path_text in (
            ("stderr", side.stderr_file),
            ("stdout", side.stdout_file),
        ):
            tail = _tail_lines(path_text)
            if not tail:
                continue

            blocks.append(
                build_diff_block(
                    f"{side.role.capitalize()} {label} — last {len(tail)} line(s)",
                    [DiffLine(kind="ctx", text=line) for line in tail],
                    language="text",
                )
            )
            break

    return tuple(blocks)


def _stream_coverage_check(
    configured_streams: tuple[str, ...],
    *counts_per_side: dict[str, int],
) -> CheckResult | None:
    """Warn about configured streams that produced no records at all.

    A stream that emitted nothing on **both** versions is the one failure a
    record comparison cannot catch: a directional count check passes 0 >= 0, and
    a table keyed on emitted records cannot list it. It is usually a stream that
    broke before the baseline was cut, or whose credentials expired -- worth
    seeing, but not a regression of the version under test, so it is diagnostic.

    The caller decides which commands get this: `configured_streams` must be
    empty for anything that cannot emit records, or `spec` and `check` would
    each carry a warning that no stream returned anything.

    Args:
        configured_streams: Every stream the run was configured to read.
        counts_per_side: Each side's **untruncated** per-stream counts. Counting
            from the report's stream sections instead would miss every stream
            past the display cap and report it as covered, which overstates
            coverage on exactly the wide catalogs where it matters.

    Returns:
        The check, or `None` when there is no configured catalog to compare
        against.
    """
    if not configured_streams:
        return None

    empty = sorted(
        stream
        for stream in configured_streams
        if not any(counts.get(stream, 0) for counts in counts_per_side)
    )
    covered = len(configured_streams) - len(empty)
    # "on any version" is load-bearing in a comparison: a stream that emitted on
    # control and nothing on target is covered by this check and caught by the
    # record-count comparison, and a bare "emitted records" next to a failed
    # target reads as if the target produced them.
    scope = " on any version" if len(counts_per_side) > 1 else ""
    summary = (
        f"{covered} of {len(configured_streams)} configured "
        f"stream(s) emitted records{scope}"
    )
    if not empty:
        return CheckResult(name="Stream coverage", passed=True, summary=summary)

    shown = empty[:MAX_EMPTY_STREAMS_LISTED]
    listed = ", ".join(shown)
    if len(empty) > len(shown):
        listed += f" and {len(empty) - len(shown)} more"

    return CheckResult(
        name="Stream coverage",
        passed=False,
        severity="diagnostic",
        summary=f"{summary}; no records from {listed}",
    )


def _http_metrics_table(
    control_result: dict[str, Any],
    target_result: dict[str, Any],
) -> MetricTable | None:
    """Build the HTTP traffic table when either side recorded metrics.

    Only populated with `--enable-http-metrics`, hence the `None` return.
    """
    control_http = control_result.get("http_metrics") or {}
    target_http = target_result.get("http_metrics") or {}
    # Only when a capture actually recorded something. Two ways it does not:
    # a payload holding just `replay_skipped_reason`, which describes a proxy
    # that never ran, and a command that made no requests -- `spec`, and
    # `check` on plenty of connectors. A table of zeroes reads as "no traffic"
    # in the first case and is noise in the second; the reason, where there is
    # one, surfaces as a check instead.
    if not control_http.get("flow_count") and not target_http.get("flow_count"):
        return None

    # Counts only: the ratios and `replay_source` are formatted strings rather
    # than numbers, so they are shown per side under Execution details, where
    # they sit next to the counts they are derived from.
    keys = (
        "flow_count",
        "duplicate_flow_count",
        "cache_hits_count",
        "replayed_flow_count",
        "live_flow_count",
        "unreplayable_flow_count",
    )
    rows = tuple(
        MetricRow(
            label=key.replace("_", " ").title(),
            control=int(control_http.get(key, 0) or 0),
            target=int(target_http.get(key, 0) or 0),
        )
        for key in keys
    )

    return MetricTable(title=HTTP_TRAFFIC_TABLE, label_header="Metric", rows=rows)


def _pk_text(pk: Any) -> str:
    """Render one primary-key value for a diff line.

    PKs are tuples of scalars (composite PKs have several components); JSON is
    the one rendering that keeps the type visible -- `123` and `"123"` are
    different PK values, and the missing-PK check treats them as such.
    """
    components = list(pk) if isinstance(pk, (tuple, list)) else [pk]

    return json.dumps(components, default=str)


def _comparison_check(
    name: str, result: ComparisonResult, note: str = ""
) -> CheckResult:
    """One record-comparison check as a row of the per-check table.

    A failing check names the failing streams (capped at
    `MAX_FAILING_STREAMS_NAMED`); the full detail lives in that stream's
    section, so the summary only has to say where to look. A failing check
    with no per-stream results (the comparison errored before producing
    any) has only its message to show.
    """
    if result.passed or not result.failed_streams:
        summary = result.message
    else:
        failing = sorted(result.failed_streams)
        shown = ", ".join(failing[:MAX_FAILING_STREAMS_NAMED])
        if len(failing) > MAX_FAILING_STREAMS_NAMED:
            shown += f" and {len(failing) - MAX_FAILING_STREAMS_NAMED} more"
        plural = "s" if len(failing) > 1 else ""
        summary = f"{result.message} — {len(failing)} stream{plural} failed: {shown}"

    if note:
        summary += f" ({note})"

    return CheckResult(name=name, passed=result.passed, summary=summary)


def _comparison_failing_streams(
    summary: RecordComparisonSummary | None,
) -> frozenset[str]:
    """Every stream at least one record-comparison check failed on."""
    if summary is None:
        return frozenset()

    checks = (
        summary.count_comparison,
        summary.pk_presence,
        summary.control_pk_uniqueness,
        summary.target_pk_uniqueness,
        summary.field_comparison,
    )

    return frozenset(
        name
        for check in checks
        if check is not None
        for name, result in check.stream_results.items()
        if not result.passed
    )


def build_record_comparison_checks(
    summary: RecordComparisonSummary,
) -> tuple[CheckResult, ...]:
    """One `CheckResult` per record-comparison check that actually ran.

    These are `strict` checks: folding them into the verdict is what makes a
    dropped record or a mutated field value fail a run whose containers both
    exited cleanly -- the same rule `record_comparison_passed` applies to the
    CLI's GitHub outputs, so the two surfaces cannot disagree.

    The PK-dependent checks are `None` on a catalog with no keyed streams and
    are omitted rather than shown as trivially passing.
    """
    no_pk_note = ""
    if summary.streams_without_pk:
        no_pk_note = (
            f"{len(summary.streams_without_pk)} stream(s) have no primary key: "
            "count comparison only"
        )

    named_results: tuple[tuple[str, ComparisonResult | None, str], ...] = (
        ("Record counts", summary.count_comparison, no_pk_note),
        ("Primary key presence", summary.pk_presence, ""),
        ("Primary key integrity (control)", summary.control_pk_uniqueness, ""),
        ("Primary key integrity (target)", summary.target_pk_uniqueness, ""),
        ("Field values", summary.field_comparison, ""),
    )

    return tuple(
        _comparison_check(name, result, note)
        for name, result, note in named_results
        if result is not None
    )


def _missing_pk_block(result: StreamComparisonResult) -> DiffBlock:
    """PK values present in control but missing from the target output."""
    lines = [
        DiffLine(
            kind="meta",
            text=(
                "These records were dropped, or their PK value type changed "
                'between versions (e.g. 123 vs "123"), which also counts as '
                "missing. This direction FAILS the test."
            ),
        ),
        *(DiffLine(kind="del", text=_pk_text(pk)) for pk in result.missing_pks),
    ]

    block = build_diff_block(
        f"Missing in target \u2014 {result.missing_pk_count:,} PK value(s) "
        "(present in control, not in target)",
        lines,
    )
    # The stored list is itself capped (MAX_EXAMPLE_PKS); fold anything the
    # cap dropped into the omitted count so the block never under-reports.
    return replace(
        block,
        truncated_line_count=block.truncated_line_count
        + (result.missing_pk_count - len(result.missing_pks)),
    )


def _extra_pk_block(result: StreamComparisonResult) -> DiffBlock:
    """PK values present in target but not in control -- informational."""
    lines = [
        DiffLine(
            kind="meta",
            text=(
                "Typically records created upstream between the two live "
                "runs (the control version runs first). This direction does "
                "NOT fail the test; it is listed for context."
            ),
        ),
        *(DiffLine(kind="add", text=_pk_text(pk)) for pk in result.extra_pks),
    ]

    block = build_diff_block(
        f"Missing in control \u2014 {result.extra_pk_count:,} PK value(s) "
        "(present in target, not in control)",
        lines,
    )
    return replace(
        block,
        truncated_line_count=block.truncated_line_count
        + (result.extra_pk_count - len(result.extra_pks)),
    )


def _pk_presence_group(result: StreamComparisonResult) -> DiffBlock:
    """The PK presence check, one child block per direction.

    A single check-level block whose title summarizes both directions;
    the failing direction (missing in target) always has a child, and the
    informational one (missing in control) only when it has values.
    """
    children = [_missing_pk_block(result)]
    parts = [f"{result.missing_pk_count:,} in target"]
    if result.extra_pks:
        children.append(_extra_pk_block(result))
        parts.append(f"{result.extra_pk_count:,} in control")

    return DiffBlock(
        title=f"Missing primary keys \u2014 {', '.join(parts)}",
        lines=(
            DiffLine(
                kind="meta",
                text=(
                    "PK values one version produced and the other did not, "
                    "listed per direction below. Only \u201cmissing in "
                    "target\u201d fails the test \u2014 the comparison is "
                    "directional because both runs hit the live API and the "
                    "control version runs first."
                ),
            ),
        ),
        children=tuple(children),
    )


def _duplicate_pk_block(version: str, result: StreamComparisonResult) -> DiffBlock:
    """One version's duplicated PK values, with occurrence counts."""
    counts = result.duplicate_pk_counts
    lines = [
        DiffLine(kind="del", text=f"{_pk_text(pk)} \u00d7{count:,}")
        for pk, count in counts.items()
    ]

    block = build_diff_block(
        f"In {version} \u2014 {result.duplicate_pk_count:,} PK value(s)", lines
    )
    return replace(
        block,
        truncated_line_count=block.truncated_line_count
        + (result.duplicate_pk_count - len(counts)),
    )


def _duplicate_pk_group(
    control_result: StreamComparisonResult | None,
    target_result: StreamComparisonResult | None,
) -> DiffBlock:
    """The PK uniqueness findings, one child block per version.

    A single check-level block; a version only gets a child when it actually
    emitted duplicates, so nothing renders as an empty half. A PK seen 3
    times reads `[777] \u00d73`, because "duplicated twice" and "duplicated
    three hundred times" point at different bugs.
    """
    children: list[DiffBlock] = []
    parts: list[str] = []
    for version, result in (("control", control_result), ("target", target_result)):
        if result is not None and result.duplicate_pks:
            children.append(_duplicate_pk_block(version, result))
            parts.append(f"{result.duplicate_pk_count:,} in {version}")

    return DiffBlock(
        title=f"Duplicate primary keys \u2014 {', '.join(parts)}",
        lines=(
            DiffLine(
                kind="meta",
                text=(
                    "PK values emitted on more than one record within a "
                    "single version's output (\u00d7N = how many records shared "
                    "the value) \u2014 the same entity was read more than once "
                    "(e.g. broken pagination or slicing), which breaks "
                    "destination-side dedup. Each version's duplicates are "
                    "its own finding; both fail the test."
                ),
            ),
        ),
        children=tuple(children),
    )


def _records_missing_pk_block(
    version: str, result: StreamComparisonResult
) -> DiffBlock:
    """One version's records that carry no value for their declared PK."""
    lines: list[DiffLine] = []
    for index, record in enumerate(result.records_missing_pk_examples):
        lines.append(DiffLine(kind="meta", text=f"record {index + 1}"))
        # Name the missing fields before dumping the record: the record
        # body cannot show a field it does not have.
        lines.extend(
            DiffLine(kind="del", text=_pk_field_text(record, pk_path))
            for pk_path in result.pk_paths or []
        )
        lines.extend(DiffLine(kind="del", text=line) for line in _record_json(record))

    omitted = result.records_missing_pk - len(result.records_missing_pk_examples)
    if omitted:
        lines.append(
            DiffLine(
                kind="meta",
                text=(
                    f"\u22ef truncated: {omitted:,} more such record(s) in "
                    f"{version} \u2014 the full records are in the per-stream "
                    "files in the run artifacts"
                ),
            )
        )

    return build_diff_block(
        f"In {version} \u2014 {result.records_missing_pk:,} record(s)", lines
    )


def _records_missing_pk_group(
    control_result: StreamComparisonResult | None,
    target_result: StreamComparisonResult | None,
) -> DiffBlock:
    """The missing-PK-value findings, one child block per version.

    Same shape as the duplicate-PK group: a check-level block whose children
    are the versions that actually emitted such records. Each record opens
    with its pinned PK fields saying which field is missing or null.
    """
    children: list[DiffBlock] = []
    parts: list[str] = []
    for version, result in (("control", control_result), ("target", target_result)):
        if result is not None and result.records_missing_pk:
            children.append(_records_missing_pk_block(version, result))
            parts.append(f"{result.records_missing_pk:,} in {version}")

    return DiffBlock(
        title=(
            f"Records with missing or null primary key values \u2014 {', '.join(parts)}"
        ),
        lines=(
            DiffLine(
                kind="meta",
                text=(
                    "Records emitted without a value for their declared "
                    "primary key (field absent or null); they cannot be "
                    "matched between versions and are excluded from the PK "
                    "checks above. Each version's records are its own "
                    "finding; both fail the test."
                ),
            ),
        ),
        children=tuple(children),
    )


def _pk_field_text(record: dict[str, Any], pk_path: list[str]) -> str:
    """One pinned `pk <field> = <value>` line for a record.

    Traverses the record's `data` along the PK path; an absent field reads
    `<field missing>` so a record that is missing its PK says so explicitly
    rather than looking like a null.
    """
    missing = object()
    value: Any = record.get("data") or {}
    for key in pk_path:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            value = missing
            break

    label = ".".join(pk_path)
    if value is missing:
        return f"pk {label} = <field missing>"

    return f"pk {label} = {json.dumps(value, default=str)}"


def _record_json(record: dict[str, Any]) -> list[str]:
    """Pretty-print one record for a side of a split diff."""
    return json.dumps(record, indent=2, sort_keys=True, default=str).splitlines()


def _split_record_rows(
    control_lines: list[str], target_lines: list[str]
) -> list[SplitDiffRow]:
    """Align two records' JSON lines into side-by-side rows.

    Equal lines sit on both sides of the same row; a changed run pairs the
    control lines with the target lines row by row; a line present on one
    side only leaves the other cell empty. Unchanged runs longer than the
    context window collapse into a "N unchanged lines" divider, so a wide
    record does not bury its one changed field.
    """
    matcher = difflib.SequenceMatcher(a=control_lines, b=target_lines, autojunk=False)
    rows: list[SplitDiffRow] = []
    for (
        tag,
        control_start,
        control_end,
        target_start,
        target_end,
    ) in matcher.get_opcodes():
        if tag == "equal":
            indices = range(control_start, control_end)
            hidden = len(indices) - 2 * SPLIT_DIFF_CONTEXT_LINES
            if hidden > 1:
                indices = [
                    *range(control_start, control_start + SPLIT_DIFF_CONTEXT_LINES),
                    None,
                    *range(control_end - SPLIT_DIFF_CONTEXT_LINES, control_end),
                ]
            for index in indices:
                if index is None:
                    rows.append(SplitDiffRow(header=f"⋯ {hidden} unchanged line(s)"))
                else:
                    line = DiffLine(kind="ctx", text=control_lines[index])
                    rows.append(SplitDiffRow(left=line, right=line))
        else:
            # replace, delete and insert are all "left changed into right";
            # zip pads the shorter side with empty cells.
            rows.extend(
                SplitDiffRow(
                    left=DiffLine(kind="del", text=control_line)
                    if control_line is not None
                    else None,
                    right=DiffLine(kind="add", text=target_line)
                    if target_line is not None
                    else None,
                )
                for control_line, target_line in zip_longest(
                    control_lines[control_start:control_end],
                    target_lines[target_start:target_end],
                )
            )

    return rows


def _value_diff_rows(example: dict[str, Any]) -> list[SplitDiffRow]:
    """Side-by-side rows for one PK-matched record pair.

    Diffs the full records rather than reprinting the DeepDiff payload: the
    reader gets the changed fields in context, with the surrounding fields
    visible. `emitted_at` is dropped from both sides because the comparison
    excluded it -- showing it would present a passing field as a diff.

    Falls back to the raw DeepDiff dict when an example carries no record
    copies, so a malformed example still shows *what* changed.
    """
    control = {
        key: value
        for key, value in (example.get("control") or {}).items()
        if key not in EXCLUDE_PATHS
    }
    target = {
        key: value
        for key, value in (example.get("target") or {}).items()
        if key not in EXCLUDE_PATHS
    }
    if not control and not target:
        text = json.dumps(json_safe(example.get("diff") or {}), indent=2, default=str)

        return [
            SplitDiffRow(left=DiffLine(kind="ctx", text=line))
            for line in text.splitlines()
        ]

    return _split_record_rows(_record_json(control), _record_json(target))


def _value_diff_block(diff: RecordDiff) -> DiffBlock:
    """Side-by-side control-versus-target diffs for the kept value-diff examples.

    The examples are already capped at the comparison layer
    (`MAX_EXAMPLE_DIFFS`); the title carries the true total so a reader knows
    how much the cap hid. The full records of both runs stay in the
    per-stream files in the run artifacts.
    """
    rows: list[SplitDiffRow] = []
    for example in diff.records_with_value_diff:
        pk = example.get("pk")
        rows.append(
            SplitDiffRow(
                header=f"record pk = {_pk_text(pk)}" if pk is not None else "record",
            )
        )
        # Pin the identifying fields above the diff: on a wide record the PK
        # field itself can land past the row cap or inside a collapsed gap,
        # and the reader must never have to hunt for which record this is.
        for pk_path in diff.pk_paths or []:
            rows.append(
                SplitDiffRow(
                    left=DiffLine(
                        kind="ctx",
                        text=_pk_field_text(example.get("control") or {}, pk_path),
                    ),
                    right=DiffLine(
                        kind="ctx",
                        text=_pk_field_text(example.get("target") or {}, pk_path),
                    ),
                )
            )
        rows.extend(_value_diff_rows(example))

    return build_split_diff_block(
        f"Field value diffs — {diff.records_with_value_diff_count:,} record(s) "
        f"differ (showing {len(diff.records_with_value_diff)})",
        rows,
    )


def _value_diff_deepdiff_block(diff: RecordDiff) -> DiffBlock:
    """The raw DeepDiff payload of each kept example, verbatim.

    The same payload the JSON output carries in `value_diff_examples`. It
    complements the side-by-side view: DeepDiff names exactly which paths
    changed (`values_changed`, `type_changes`, ...), which is greppable and
    machine-ish where the record diff is visual.
    """
    lines: list[DiffLine] = []
    for example in diff.records_with_value_diff:
        pk = example.get("pk")
        lines.append(
            DiffLine(
                kind="meta",
                text=f"record pk = {_pk_text(pk)}" if pk is not None else "record",
            )
        )
        # Through `json_safe` first: DeepDiff's own set containers are not
        # JSON-serializable, and the `default=str` fallback alone would
        # collapse each one into a single unreadable line.
        text = json.dumps(
            json_safe(example.get("diff") or {}),
            indent=2,
            sort_keys=True,
            default=str,
        )
        lines.extend(DiffLine(kind="ctx", text=line) for line in text.splitlines())

    return build_diff_block(
        f"Field value diffs \u2014 raw DeepDiff payload "
        f"(showing {len(diff.records_with_value_diff)})",
        lines,
        language="json",
        # A huge field value is one JSON line, and the generic 2k clip would
        # cut exactly the values this block exists to show — but the line
        # COUNT cap does not bound line SIZE, and 200 lines of
        # connector-controlled blobs would bloat the artifact. A generous
        # cap keeps the intent while keeping report.html bounded.
        max_line_chars=MAX_DEEPDIFF_LINE_CHARS,
    )


def _records_only_in_control_block(diff: RecordDiff) -> DiffBlock:
    """Full example records that the target failed to produce.

    A single-column list on purpose: every record here comes from the
    control output (records only in the target are tolerated by the
    directional comparison and never rendered), so a split view would
    carry a permanently empty target column. Each record opens with its
    pinned PK fields, like the value-diff examples.
    """
    lines: list[DiffLine] = []
    for index, record in enumerate(diff.records_only_in_control):
        lines.append(DiffLine(kind="meta", text=f"record {index + 1}"))
        lines.extend(
            DiffLine(kind="del", text=_pk_field_text(record, pk_path))
            for pk_path in diff.pk_paths or []
        )
        lines.extend(DiffLine(kind="del", text=line) for line in _record_json(record))

    return build_diff_block(
        f"Records from control missing in target — showing "
        f"{len(diff.records_only_in_control)} of "
        f"{diff.records_only_in_control_count:,} full record(s)",
        lines,
    )


def _stream_comparison_detail(
    stream: str,
    summary: RecordComparisonSummary,
) -> tuple[bool, list[str], tuple[DiffBlock, ...]] | None:
    """One stream's comparison verdict, headline fragments and detail blocks.

    Returns `None` for a stream the comparison never saw -- a configured
    stream that emitted nothing on either side, which the coverage check
    reports instead.

    Detail blocks are built only for the sub-checks that failed: a passing
    stream's section stays a single line, and the report's weight goes where
    the failures are.
    """

    def result_for(check: ComparisonResult | None) -> StreamComparisonResult | None:
        return check.stream_results.get(stream) if check is not None else None

    count_result = summary.count_comparison.stream_results.get(stream)
    presence_result = result_for(summary.pk_presence)
    control_uniqueness = result_for(summary.control_pk_uniqueness)
    target_uniqueness = result_for(summary.target_pk_uniqueness)
    field_result = result_for(summary.field_comparison)

    results = [
        result
        for result in (
            count_result,
            presence_result,
            control_uniqueness,
            target_uniqueness,
            field_result,
        )
        if result is not None
    ]
    if not results:
        return None

    fragments: list[str] = []
    blocks: list[DiffBlock] = []

    if count_result is not None and not count_result.passed:
        fewer = count_result.control_count - count_result.target_count
        fragments.append(f"{fewer:,} fewer record(s) in target")

    if presence_result is not None and not presence_result.passed:
        fragments.append(f"{presence_result.missing_pk_count:,} missing PK(s)")
        blocks.append(_pk_presence_group(presence_result))

    has_duplicates = False
    has_records_missing_pk = False
    for version, uniqueness in (
        ("control", control_uniqueness),
        ("target", target_uniqueness),
    ):
        if uniqueness is None or uniqueness.passed:
            continue
        if uniqueness.duplicate_pks:
            fragments.append(
                f"{uniqueness.duplicate_pk_count:,} duplicate PK(s) in {version}"
            )
            has_duplicates = True
        if uniqueness.records_missing_pk:
            fragments.append(
                f"{uniqueness.records_missing_pk:,} record(s) without PK "
                f"values in {version}"
            )
            has_records_missing_pk = True
    if has_duplicates:
        blocks.append(_duplicate_pk_group(control_uniqueness, target_uniqueness))
    if has_records_missing_pk:
        blocks.append(_records_missing_pk_group(control_uniqueness, target_uniqueness))

    if (
        field_result is not None
        and not field_result.passed
        and field_result.record_diff is not None
    ):
        record_diff = field_result.record_diff
        if record_diff.records_with_value_diff_count:
            fragments.append(
                f"{record_diff.records_with_value_diff_count:,} record(s) "
                "with value diffs"
            )
            blocks.append(_value_diff_block(record_diff))
            blocks.append(_value_diff_deepdiff_block(record_diff))
        if record_diff.records_only_in_control:
            # The PK list above is exhaustive; these are the full records for
            # the first few, which is what makes a drop diagnosable.
            blocks.append(_records_only_in_control_block(record_diff))

    return all(result.passed for result in results), fragments, tuple(blocks)


def _apply_record_comparison(
    sections: tuple[StreamSection, ...],
    summary: RecordComparisonSummary,
) -> tuple[StreamSection, ...]:
    """Fold the record comparison into the per-stream sections.

    Every compared stream is re-marked `pass` or `fail` -- the comparison is
    part of the verdict now, so its sections assert rather than inform -- and
    a failing stream's headline says in one line what went wrong, with the
    detail attached as collapsible diff blocks. Streams the comparison never
    saw stay `info`.
    """
    updated: list[StreamSection] = []
    for section in sections:
        detail = _stream_comparison_detail(section.stream, summary)
        if detail is None:
            updated.append(section)
            continue

        passed, fragments, blocks = detail
        headline = section.headline
        if section.stream in summary.streams_without_pk:
            headline += " — no primary key: count comparison only"
        if fragments:
            headline += " — " + "; ".join(fragments)

        updated.append(
            replace(
                section,
                status="pass" if passed else "fail",
                headline=headline,
                diff_blocks=section.diff_blocks + blocks,
            )
        )

    return tuple(updated)


def _live_url_detail(http_metrics: dict[str, Any]) -> str:
    """The URLs a replaying run fetched live, for a failing coverage check.

    The counts alone say a shortfall happened and nothing about why. These are
    the requests the corpus could not answer, and the recorded dumps are kept out
    of the uploaded artifacts on purpose -- so if the check does not name them,
    nothing does, and the run has to be re-run to be diagnosed.
    """
    live_urls = http_metrics.get("live_urls") or []
    if not live_urls:
        return ""

    shown = [str(entry.get("url")) for entry in live_urls[:MAX_LIVE_URLS_NAMED]]
    total = int(http_metrics.get("live_unique_url_count", len(live_urls)) or 0)
    detail = "; unmatched: " + ", ".join(shown)
    if total > len(shown):
        detail += f" and {total - len(shown)} more"

    return detail


def _replay_coverage_check(
    target_result: dict[str, Any],
    control_result: dict[str, Any],
) -> CheckResult | None:
    """Report how much of a replaying target run still hit the live API.

    The epic's rule is that an inconclusive run must never read as a pass. A
    target that was supposed to replay the control run's traffic and instead
    fetched a large share of it live was compared against *different* upstream
    data, so a record difference cannot be attributed to the version under test.

    Diagnostic on purpose, and re-argued now that replay is the default -- the
    old reasoning was that replay was opt-in, which no longer holds. Every way
    this check fires is a property of the environment or the data rather than
    of the version under test: no `mitmdump` on the runner, a corpus over the
    memory cap, a control run that captured nothing, a proxy killed before it
    flushed its dump, or bodies deliberately excluded by
    `--http-replay-max-body` and refetched live. Failing the verdict
    on any of those would block a connector PR for a reason unrelated to its
    code -- and would fail every local run made without the `live-tests`
    dependency group. So it explains a record difference rather than
    independently causing a failure.

    That leaves it as the main signal that the acceptance criterion held, which
    is why it has to be prominent and accurate even while it is advisory.
    Promoting it to strict wants a threshold grounded in real numbers first --
    see `MAX_LIVE_FLOW_RATIO`.

    Both sides' metrics are read, because either run's proxy can be killed
    before it flushed. A short *control* dump is the worse of the two: the flows
    it lost are the ones the target then refetches live, so the check would
    otherwise report the drift it causes -- and name the URLs that went live --
    with nothing saying the recording was short. That is exactly the
    misattribution `metrics_incomplete` exists to prevent, and the per-side
    execution details are not where anyone looks after reading a red check.

    Args:
        target_result: The target run's payload, whose counts the check reads.
        control_result: The control run's payload, for its `metrics_incomplete`
            marker only -- the recording the target replayed from came from it.

    Returns:
        The check, or `None` when the run was not replaying at all.
    """
    http_metrics = target_result.get("http_metrics") or {}

    # A run that made no HTTP requests has nothing to replay and no upstream to
    # drift: `spec` never calls out at all, so its control run records an empty
    # dump, the target finds nothing to replay from, and every stage of every
    # run would otherwise carry a failed diagnostic whose reasoning is vacuous.
    # That is how a check gets ignored on `read`, where it does carry meaning.
    #
    # Keyed on the *target* having recorded no traffic rather than on the
    # control having captured none: control capturing nothing while the target
    # calls out is the asymmetry worth shouting about, and silencing on the
    # control alone would hide it. A missing `flow_count` is not zero traffic --
    # it means no capture happened at all (see the mitmproxy-unavailable path),
    # which is the one thing this check exists to surface.
    if http_metrics.get("flow_count") == 0:
        return None

    skipped_reason = http_metrics.get("replay_skipped_reason")
    if skipped_reason:
        return CheckResult(
            name=_REPLAY_CHECK,
            passed=False,
            severity="diagnostic",
            summary=(
                f"HTTP replay was requested and skipped ({skipped_reason}); the "
                "target ran against live data, so upstream drift is not ruled out"
            ),
        )

    if not http_metrics.get("replay_source"):
        return None

    flow_count = int(http_metrics.get("flow_count", 0) or 0)
    if not flow_count:
        return None

    live = int(http_metrics.get("live_flow_count", 0) or 0)
    replayed = flow_count - live
    summary = (
        f"{replayed} of {flow_count} target request(s) served from the control "
        f"run's recording; {live} went live"
    )

    # Named per side: a killed control means a short *recording*, so the live
    # count it produces is real drift with a known cause, while a killed target
    # means the counts themselves are short. Pointing at the wrong one sends the
    # reader after the wrong fix.
    incomplete = "; ".join(
        f"{side} run: {reason}"
        for side, reason in (
            (
                "control",
                (control_result.get("http_metrics") or {}).get("metrics_incomplete"),
            ),
            ("target", http_metrics.get("metrics_incomplete")),
        )
        if reason
    )
    if incomplete:
        # The counts are a lower bound, and short in the direction that flatters
        # the run: a killed shutdown loses the flows mitmproxy had not flushed,
        # which can only lower `live_flow_count` on the target and can only
        # shrink the corpus the control recorded. Below the ratio it would
        # otherwise read as a clean replayed run.
        return CheckResult(
            name=_REPLAY_CHECK,
            passed=False,
            severity="diagnostic",
            summary=(
                f"{summary} -- HTTP metrics are incomplete ({incomplete}), so "
                "replay coverage cannot be read as exact"
            ),
        )

    if live / flow_count <= MAX_LIVE_FLOW_RATIO:
        return CheckResult(name=_REPLAY_CHECK, passed=True, summary=summary)

    return CheckResult(
        name=_REPLAY_CHECK,
        passed=False,
        severity="diagnostic",
        summary=(
            f"{summary} ({live / flow_count:.0%}, above "
            f"{MAX_LIVE_FLOW_RATIO:.0%}) -- the two versions did not see the "
            f"same upstream data{_live_url_detail(http_metrics)}"
        ),
    )


def build_comparison_report_model(
    *,
    target_image: str,
    control_image: str,
    command: str,
    target_result: dict[str, Any],
    control_result: dict[str, Any],
    outcome: ComparisonOutcome | None = None,
    record_comparison: RecordComparisonSummary | None = None,
    extra_checks: tuple[CheckResult, ...] = (),
    extra_diff_blocks: tuple[DiffBlock, ...] = (),
    configured_streams: tuple[str, ...] = (),
    connection_objects: tuple[DiffBlock, ...] = (),
) -> RegressionReportModel:
    """Build the report model for a target-versus-control run.

    Pass the **unannotated** run results: `result["success"]` is read as the
    container exit status and the per-version verdict is derived here with
    `command_result_succeeded`, the same rule the markdown report and the CLI's
    GitHub outputs use. Handing this the annotated copies produced by
    `_annotate_run_verdict` would misdescribe every `check` run.

    Args:
        target_image: The target (new version) connector image.
        control_image: The control (baseline version) connector image.
        command: The Airbyte command that was run.
        target_result: Unannotated results dict from the target run.
        control_result: Unannotated results dict from the control run.
        outcome: The already-evaluated outcome, so a run is only evaluated once.
            Recomputed from the results when omitted.
        record_comparison: The record-comparison summary of a read run, when it
            ran. Folded into the verdict as one check per comparison (the rule
            that keeps this model consistent with the CLI's
            `record_comparison_passed` output), and rendered as per-stream
            detail blocks in the HTML report.
        extra_checks: Comparison checks to fold into the verdict and show on both
            surfaces. Supply them here rather than appending to the returned
            model, which would leave `passed` stale.
        extra_diff_blocks: What a failing check found, shown above the failure
            output. A check row has one line to say "this stream's schema
            changed"; the reviewer's next question is always which field.

    Returns:
        The model to render as `report.html` and as the inline summary.
    """
    outcome = outcome or evaluate_comparison_outcome(
        command, target_result, control_result
    )

    sides = (
        _build_side("control", command, control_image, control_result),
        _build_side("target", command, target_image, target_result),
    )
    verdict_detail = _comparison_verdict_detail(outcome, sides)

    control_counts = _with_configured_streams(
        control_result.get("record_counts_per_stream", {}), configured_streams
    )
    target_counts = _with_configured_streams(
        target_result.get("record_counts_per_stream", {}), configured_streams
    )
    stream_sections, omitted = _build_stream_sections(
        control_counts,
        target_counts,
        configured_streams,
        failing_streams=_comparison_failing_streams(record_comparison),
    )
    if record_comparison is not None:
        stream_sections = _apply_record_comparison(stream_sections, record_comparison)
    coverage = _stream_coverage_check(configured_streams, control_counts, target_counts)
    comparison_checks = (
        build_record_comparison_checks(record_comparison)
        if record_comparison is not None
        else ()
    )
    replay_coverage = _replay_coverage_check(target_result, control_result)

    metric_tables = tuple(
        table
        for table in (
            _comparison_metric_table(
                MESSAGE_TYPES_TABLE,
                "Type",
                control_result.get("message_counts", {}),
                target_result.get("message_counts", {}),
            ),
            _comparison_metric_table(
                RECORD_COUNTS_TABLE,
                "Stream",
                control_counts,
                target_counts,
                with_total=True,
            ),
            _http_metrics_table(control_result, target_result),
        )
        if table is not None
    )

    checks = (
        CheckResult(
            name=_RUN_CHECK,
            passed=outcome.success,
            summary=verdict_detail,
        ),
        *([coverage] if coverage is not None else []),
        *comparison_checks,
        # Diagnostic, so deliberately not folded into the verdict below.
        *([replay_coverage] if replay_coverage is not None else []),
        *extra_checks,
    )
    passed, verdict_label, verdict_detail = _fold_check_results(
        (*comparison_checks, *extra_checks),
        outcome.success,
        _comparison_verdict_label(outcome),
        verdict_detail,
        # An errored comparison fails the run as INCONCLUSIVE: a comparator
        # crash is a tooling failure, not evidence the connector regressed.
        failed_label="FAIL (inconclusive)"
        if record_comparison is not None and record_comparison.errored
        else "FAIL (regression)",
    )
    if passed and outcome.both_succeeded:
        # The claim belongs to the folded verdict, not the command outcome:
        # every comparison check passed, so "no regression" is now earned.
        verdict_detail += " (no regression)"

    return RegressionReportModel(
        mode="comparison",
        command=command,
        passed=passed,
        verdict_label=verdict_label,
        verdict_detail=verdict_detail,
        context=_build_context(command, target_image, control_image),
        sides=sides,
        checks=checks,
        metric_tables=metric_tables,
        stream_sections=stream_sections,
        omitted_stream_count=omitted,
        outcome=outcome,
        diff_blocks=(*extra_diff_blocks, *build_failure_output_blocks(sides)),
        connection_objects=connection_objects,
    )


def _comparison_verdict_label(outcome: ComparisonOutcome) -> str:
    """The short verdict shown in the banner and the `Result:` line."""
    if outcome.check_improvement:
        return "PASS (improvement)"
    if outcome.success:
        return "PASS"
    if outcome.regression_detected:
        return "FAIL (regression)"

    return "FAIL (inconclusive)"


def failed_checks(checks: Sequence[CheckResult]) -> tuple[CheckResult, ...]:
    """The checks that fail the run, by the one rule every surface uses.

    A `diagnostic` check is a warning and is not in here. Callers that decide a
    verdict before a report model exists -- the CLI's GitHub outputs, its logged
    payload -- read this rather than testing `passed`, so they cannot disagree
    with the banner the reviewer ends up reading.
    """
    return tuple(check for check in checks if check.status == "fail")


def _fold_check_results(
    checks: tuple[CheckResult, ...],
    passed: bool,
    verdict_label: str,
    verdict_detail: str,
    failed_label: str = "FAIL",
) -> tuple[bool, str, str]:
    """Fold the checks into the run's verdict.

    A failing `strict` check fails the run even when both commands ran cleanly:
    that is the whole point of comparing output, and without this the banner
    would read PASS above a table of failed checks. The wording has to be
    replaced too -- `ComparisonOutcome` describes how the *commands* went and has
    no vocabulary for "they both ran fine and the data differs".

    Args:
        checks: The comparison checks only. The command-execution check is
            already accounted for by `passed`, so folding it again would restate
            a command failure as a check failure.
        passed: The verdict before folding, from the command outcome.
        verdict_label: The label before folding.
        verdict_detail: The sentence before folding.
        failed_label: The label to use when a strict check fails a run whose
            commands both succeeded.

    Returns:
        The folded `(passed, verdict_label, verdict_detail)`.
    """
    failed = failed_checks(checks)
    if not failed or not passed:
        return passed, verdict_label, verdict_detail

    names = ", ".join(check.name.lower() for check in failed)
    plural = "s" if len(failed) > 1 else ""

    return (
        False,
        failed_label,
        f"{verdict_detail}, but {len(failed)} check{plural} failed: {names}",
    )


def _comparison_verdict_detail(
    outcome: ComparisonOutcome,
    sides: tuple[RunSide, ...],
) -> str:
    """The one-sentence verdict, in the same terms `report.md` uses.

    Describes what each side actually did rather than restating the verdict, so
    it cannot contradict the per-version table: for `check` the verdict folds in
    the exit code as well as `connectionStatus`. The per-side clauses come from
    the same `_describe_run` the markdown report uses, so they are identical; the
    emphasis `report.md` puts on its verdict is carried by `verdict_label` here.

    """
    control, target = sides[0], sides[1]
    both = f"Target {target.description}, control {control.description}"

    if outcome.check_improvement:
        return f"{both} — improvement, not a regression"
    if outcome.regression_detected:
        return f"{both} — regression detected"
    if outcome.both_succeeded:
        # Just the facts: "(no regression)" is a claim about the comparison
        # checks, so `build_comparison_report_model` appends it only after
        # the fold confirms every check passed.
        return "Both versions succeeded"

    if outcome.both_failed:
        return f"{both} — inconclusive, cannot rule out a regression"

    return f"{both} — inconclusive, nothing to compare the target against"


def build_single_version_report_model(
    *,
    connector_image: str,
    command: str,
    result: dict[str, Any],
    extra_checks: tuple[CheckResult, ...] = (),
    configured_streams: tuple[str, ...] = (),
    connection_objects: tuple[DiffBlock, ...] = (),
) -> RegressionReportModel:
    """Build the report model for a single-version (`--skip-compare`) run.

    Pass the **unannotated** run result, for the reason given in
    `build_comparison_report_model`.

    Args:
        connector_image: The connector image that was tested.
        command: The Airbyte command that was run.
        result: Unannotated results dict from the run.
        extra_checks: Validation checks to fold into the verdict and show on both
            surfaces. Supply them here rather than appending to the returned
            model, which would leave `passed` stale.

    Returns:
        The model to render as `report.html` and as the inline summary.
    """
    side = _build_side("single", command, connector_image, result)
    verdict_detail = f"{connector_image} {side.description}"

    counts = _with_configured_streams(
        result.get("record_counts_per_stream", {}), configured_streams
    )
    stream_sections, omitted = _build_stream_sections(None, counts, configured_streams)
    coverage = _stream_coverage_check(configured_streams, counts)

    metric_tables = tuple(
        table
        for table in (
            _single_metric_table(
                MESSAGE_TYPES_TABLE, "Type", result.get("message_counts", {})
            ),
            _single_metric_table(
                RECORD_COUNTS_TABLE, "Stream", counts, with_total=True
            ),
        )
        if table is not None
    )

    checks = (
        CheckResult(
            name=_RUN_CHECK,
            passed=side.passed,
            summary=verdict_detail,
        ),
        *([coverage] if coverage is not None else []),
        *extra_checks,
    )
    passed, verdict_label, verdict_detail = _fold_check_results(
        extra_checks, side.passed, "PASS" if side.passed else "FAIL", verdict_detail
    )

    return RegressionReportModel(
        mode="single_version",
        command=command,
        passed=passed,
        verdict_label=verdict_label,
        verdict_detail=verdict_detail,
        context=_build_context(command, connector_image, None),
        sides=(side,),
        checks=checks,
        metric_tables=metric_tables,
        stream_sections=stream_sections,
        omitted_stream_count=omitted,
        diff_blocks=build_failure_output_blocks((side,)),
        connection_objects=connection_objects,
    )


def _jinja_environment() -> Environment:
    """The Jinja environment used to render the HTML report.

    `enabled_extensions` must name `html.j2` explicitly: `select_autoescape`
    matches extensions with `endswith`, so its default
    `("html", "htm", "xml")` leaves a `.html.j2` template **unescaped** and
    would inject connector-controlled strings (stream names, and record values
    once diff blocks are populated) straight into the page.
    """
    environment = Environment(
        loader=PackageLoader("airbyte_ops_mcp.regression_tests", "templates"),
        autoescape=select_autoescape(
            enabled_extensions=("html", "htm", "xml", "html.j2")
        ),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    # Counts read as thousands-separated everywhere, including the stream
    # headlines the builders format, so a six-figure record count is legible.
    environment.filters["number"] = _format_count

    return environment


def _json_for_html_comment(data: dict[str, Any]) -> Markup:
    """Encode a dict as JSON that is safe inside an HTML comment.

    Two hazards, one encoding. Autoescaping would turn the quotes into entities
    and make the header unparseable, so this is marked safe -- which means the
    payload itself must not be able to close the comment. Escaping `<`, `>` and
    `&` as JSON unicode escapes removes that possibility (no `-->` can survive)
    while `json.loads` still decodes them back verbatim.
    """
    encoded = (
        json.dumps(data, separators=(",", ":"))
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
    )

    # Safe by construction: no `<`, `>` or `&` can remain in `encoded`.
    return Markup(encoded)


def render_html_report(model: RegressionReportModel) -> str:
    """Render the detailed HTML report for one command's run.

    The result is a single self-contained document: no scripts, no stylesheets,
    no fonts or images loaded over the network, because it is read from a
    downloaded artifact with no network available.

    The document also carries the machine-readable header and body markers that
    `consolidate_reports` needs to fold a whole run's commands into one page.
    """
    template = _jinja_environment().get_template(TEMPLATE_NAME)
    meta: dict[str, Any] = {
        "command": model.command,
        "mode": model.mode,
        "passed": model.passed,
        "verdict_label": model.verdict_label,
        "verdict_detail": model.verdict_detail,
        "connector": model.context.connector_name,
        "target_version": model.context.target_version,
        "control_version": model.context.control_version,
        "artifact_name": model.context.artifact_name,
        # Carried so the consolidated page can put commands side by side. A CLI
        # process only ever sees one command, so this header is the only channel
        # across that boundary.
        "metric_tables": [
            {
                "title": table.title,
                "rows": [
                    {"label": row.label, "control": row.control, "target": row.target}
                    for row in table.rows
                ],
            }
            for table in model.metric_tables
        ],
    }

    return template.render(
        model=model,
        context=model.context,
        meta_marker=META_MARKER,
        meta_json=_json_for_html_comment(meta),
        body_start_marker=BODY_START_MARKER,
        body_end_marker=BODY_END_MARKER,
    )


def write_html_report(model: RegressionReportModel, output_dir: Path) -> Path:
    """Write the HTML report into a run's artifact directory.

    Args:
        model: The report model to render.
        output_dir: The run's `--output-dir`, which the workflow uploads whole.

    Returns:
        Path to the generated `report.html`.
    """
    report_path = output_dir / HTML_REPORT_FILENAME
    report_path.write_text(render_html_report(model))

    return report_path


@dataclass(frozen=True)
class ReportPart:
    """One command's report, ready to be inlined into the consolidated page.

    `body` is HTML that `render_html_report` already produced, which is why the
    consolidated template may insert it unescaped: everything connector-supplied
    inside it was escaped when that report was rendered. It is read back from
    disk rather than re-rendered because each command runs in its own process.
    """

    command: str
    passed: bool
    verdict_label: str
    verdict_detail: str
    artifact_name: str
    body: str
    metric_tables: tuple[MetricTable, ...] = ()

    @property
    def anchor(self) -> str:
        """The consolidated page's in-document anchor for this command."""
        return f"command-{self.command}"


@dataclass(frozen=True)
class MatrixCell:
    """One command's control/target pair for one metric row."""

    command: str
    row: MetricRow | None


@dataclass(frozen=True)
class MatrixRow:
    """One metric across every command in a run."""

    label: str
    cells: tuple[MatrixCell, ...]


@dataclass(frozen=True)
class CommandMatrix:
    """A metric table pivoted so commands sit side by side.

    This is the view a per-command report cannot give: whether the TRACE
    messages the target emitted during `read` also appeared during `discover`,
    or whether a count moved everywhere or in one place.
    """

    title: str
    label_header: str
    commands: tuple[str, ...]
    rows: tuple[MatrixRow, ...]


def _build_command_matrices(parts: tuple[ReportPart, ...]) -> tuple[CommandMatrix, ...]:
    """Pivot every part's metric tables into one table per title.

    A metric absent from a command renders as an empty cell rather than a zero:
    `spec` emits no records, which is not the same as emitting none.
    """
    titles = [
        title
        for title in (MESSAGE_TYPES_TABLE, RECORD_COUNTS_TABLE, HTTP_TRAFFIC_TABLE)
        if any(table.title == title for part in parts for table in part.metric_tables)
    ]

    matrices: list[CommandMatrix] = []
    for title in titles:
        by_command = {
            part.command: {
                row.label: row
                for table in part.metric_tables
                if table.title == title
                for row in table.rows
            }
            for part in parts
        }
        commands = tuple(part.command for part in parts if by_command.get(part.command))
        labels = sorted({label for rows in by_command.values() for label in rows})
        if not commands or not labels:
            continue

        matrices.append(
            CommandMatrix(
                title=title,
                label_header="Stream" if title == RECORD_COUNTS_TABLE else "Metric",
                commands=commands,
                rows=tuple(
                    MatrixRow(
                        label=label,
                        cells=tuple(
                            MatrixCell(
                                command=command, row=by_command[command].get(label)
                            )
                            for command in commands
                        ),
                    )
                    for label in labels
                ),
            )
        )

    return tuple(matrices)


def extract_report_part(html: str) -> ReportPart | None:
    """Read one per-command report back into its consolidatable pieces.

    Returns:
        The part, or `None` when the file is not a report this version wrote --
        a truncated upload, or a report from a future layout. A run must still
        produce a consolidated page for the commands that did work, so an
        unreadable input is skipped rather than fatal.
    """
    if not html.lstrip().startswith("<!DOCTYPE html>"):
        return None

    meta_match = re.search(rf"<!--{re.escape(META_MARKER)} (\{{.*?\}})-->", html)
    start_comment = f"<!--{BODY_START_MARKER}-->"
    start = html.find(start_comment)
    end = html.find(f"<!--{BODY_END_MARKER}-->")
    if meta_match is None or start == -1 or end == -1 or end < start:
        return None

    try:
        meta = json.loads(meta_match.group(1))
    except json.JSONDecodeError:
        return None

    return ReportPart(
        command=str(meta.get("command", "unknown")),
        passed=bool(meta.get("passed")),
        verdict_label=str(meta.get("verdict_label", "")),
        verdict_detail=str(meta.get("verdict_detail", "")),
        artifact_name=str(meta.get("artifact_name", "")),
        body=html[start + len(start_comment) : end],
        metric_tables=_metric_tables_from_meta(meta.get("metric_tables")),
    )


def _metric_tables_from_meta(payload: Any) -> tuple[MetricTable, ...]:
    """Rebuild the metric tables a report carried in its header.

    Tolerant on purpose: the header is read from a file another process wrote,
    possibly by an older version of this code, and a malformed one must cost the
    cross-command view rather than the whole page.
    """
    if not isinstance(payload, list):
        return ()

    tables: list[MetricTable] = []
    for table in payload:
        if not isinstance(table, dict):
            continue

        rows = tuple(
            MetricRow(
                label=str(row.get("label", "")),
                target=int(row.get("target") or 0),
                control=None if row.get("control") is None else int(row["control"]),
            )
            for row in table.get("rows", [])
            if isinstance(row, dict)
        )
        if rows:
            tables.append(
                MetricTable(
                    title=str(table.get("title", "")), label_header="", rows=rows
                )
            )

    return tuple(tables)


def _read_report_part(path: Path) -> ReportPart | None:
    """Read one report off disk, tolerating anything a broken upload can leave.

    The read has to fail as softly as the parse: an artifact that was truncated
    mid-upload can be unreadable *or* invalid UTF-8, and either one costing the
    whole run's consolidated page would defeat the point of skipping it.
    """
    try:
        html = path.read_text(errors="replace")
    except OSError:
        return None

    return extract_report_part(html)


def consolidate_reports(report_paths: Iterable[Path]) -> str | None:
    """Fold one run's per-command reports into a single self-contained page.

    The workflow runs the CLI once per command, so each command writes its own
    `report.html` into its own artifact. This produces the run-level view: a
    verdict table across commands, a jump list, and every command's full report
    inlined in order.

    Args:
        report_paths: Per-command `report.html` paths, in the order to present
            them. Missing and unreadable files are skipped.

    Returns:
        The consolidated HTML, or `None` when no input was readable -- there is
        nothing useful to upload in that case.
    """
    parts = [part for part in map(_read_report_part, report_paths) if part is not None]
    if not parts:
        return None

    template = _jinja_environment().get_template(CONSOLIDATED_TEMPLATE_NAME)

    return template.render(
        parts=parts,
        matrices=_build_command_matrices(tuple(parts)),
        passed=all(part.passed for part in parts),
        run_url=github_run_url(),
        generated_at=datetime.datetime.now(datetime.timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S UTC"
        ),
    )


def _status_emoji(passed: bool) -> str:
    """Pass/fail emoji, for scanability in the step summary."""
    return "✅" if passed else "❌"


def _inline_text(text: str, limit: int = MAX_SUMMARY_CHARS) -> str:
    """Make a connector-derived string safe to interpolate into markdown.

    The step summary is markdown, so unlike the HTML report it has no escaping
    to fall back on: a newline ends the current construct and everything after
    it renders as top-level markdown. A stream name or a check summary built
    from one is connector-controlled, so without this a connector could append a
    forged verdict line to the summary of a run it failed. Collapsing all
    whitespace removes that channel; escaping `|` keeps table rows intact.

    Length is clamped as well, because `MAX_INLINE_STREAM_ROWS` caps the row
    count but not the width of any one cell, and the step summary is dropped
    whole once it exceeds GitHub's 1 MiB per-step limit.
    """
    flattened = " ".join(text.split())
    if len(flattened) > limit:
        flattened = flattened[:limit] + _TRUNCATION_SUFFIX

    return flattened.replace("|", "\\|")


def _inline_label(label: str) -> str:
    """Render a connector-supplied label as a markdown table cell.

    Backticks make the cell read as an identifier and keep its content inert;
    `_inline_text` does the load-bearing part. A label is an identifier rather
    than prose, so it gets the tighter bound.
    """
    return "`" + _inline_text(label, limit=MAX_LABEL_CHARS).replace("`", "'") + "`"


def _inline_row_priority(row: MetricRow) -> tuple[int, str]:
    """Sort key that puts the rows worth showing inline first.

    A comparison ranks by the size of the change; a single-version run has no
    delta, so the only signal it has is the count itself.
    """
    magnitude = abs(row.delta) if row.delta is not None else row.target

    return (-magnitude, row.label)


def _inline_stream_rows(model: RegressionReportModel) -> list[str]:
    """Render the per-stream record-count table for the step summary.

    Capped at `MAX_INLINE_STREAM_ROWS` rows -- the step summary is limited to
    1 MiB per step, and a wide read can have hundreds of streams. When the cap
    bites, the rows that carry the most signal are kept -- the largest deltas in
    comparison mode, the largest counts in single-version mode, where there is no
    delta -- and the omitted count is stated. `report.html` carries every stream.
    """
    table = next(
        (t for t in model.metric_tables if t.title == RECORD_COUNTS_TABLE),
        None,
    )
    if table is None:
        return []

    rows = list(table.rows)
    omitted = max(0, len(rows) - MAX_INLINE_STREAM_ROWS)
    if omitted:
        rows.sort(key=_inline_row_priority)
        rows = rows[:MAX_INLINE_STREAM_ROWS]
        # Restore the reading order of the HTML table for the rows that survived.
        rows.sort(key=lambda row: row.label)

    lines: list[str] = []
    if model.is_comparison:
        lines.extend(
            [
                "| Stream | Control | Target | Delta |",
                "|--------|---------|--------|-------|",
            ]
        )
        lines.extend(
            f"| {_inline_label(row.label)} | {row.control} | {row.target} "
            f"| {_format_delta(row.delta or 0)} |"
            for row in rows
        )
        if table.total is not None:
            lines.append(
                f"| **Total** | **{table.total.control}** | "
                f"**{table.total.target}** | {_format_delta(table.total.delta or 0)} |"
            )
    else:
        lines.extend(["| Stream | Count |", "|--------|-------|"])
        lines.extend(f"| {_inline_label(row.label)} | {row.target} |" for row in rows)
        if table.total is not None:
            lines.append(f"| **Total** | **{table.total.target}** |")

    if omitted:
        lines.extend(["", f"_… {omitted} more stream(s) omitted — see `report.html`._"])

    return lines


def _inline_finding_lines(model: RegressionReportModel) -> list[str]:
    """What each failing check found, for the reader who stops at the summary.

    Collapsed, because the answer to "what changed" is a list and the summary is
    read next to every other step of the run. The report holds the diff itself;
    this holds the names, which is what a reviewer needs to decide whether the
    diff is worth opening.
    """
    # Warnings list their findings too: an additive-only schema change does not
    # gate the release, and "which streams were added" is exactly what the
    # reviewer who sees the warning wants to know.
    flagged = [check for check in model.checks if check.status in {"fail", "warn"}]
    findings = [(check, check.details) for check in flagged if check.details]
    if not findings:
        return []

    total = sum(len(details) for _check, details in findings)
    lines = [
        f"<details><summary>What the comparison found ({total})</summary>",
        "",
    ]

    for check, details in findings:
        shown = details[:MAX_INLINE_FINDINGS]
        lines.extend(
            [
                f"**{_inline_label(check.name)}**",
                "",
                *(f"- {_inline_text(detail)}" for detail in shown),
            ]
        )
        remaining = len(details) - len(shown)
        if remaining:
            lines.append(f"- … and {remaining} more, in the report")
        lines.append("")

    lines.extend(["</details>", ""])

    return lines


def _artifact_pointer(context: ReportContext) -> str:
    """One line telling the reader where the detailed report lives.

    GitHub cannot deep-link to a file inside an artifact, so this points at the
    run's Artifacts section and names the file to open after downloading.
    """
    if context.artifact_url:
        return (
            f"📄 Full report: `{HTML_REPORT_FILENAME}` in artifact "
            f"[`{context.artifact_name}`]({context.artifact_url})"
        )

    return (
        f"📄 Full report: `{HTML_REPORT_FILENAME}` in artifact "
        f"`{context.artifact_name}`"
    )


def render_inline_summary(model: RegressionReportModel) -> str:
    """Render the concise markdown block for `GITHUB_STEP_SUMMARY`.

    Deliberately short: the verdict, the per-check table, per-stream record
    counts and a pointer to `report.html`. Execution details, HTTP metrics and
    diff blocks belong to the HTML report only -- that split is the point of
    having two surfaces.

    Starts at an L2 heading and carries no context block: the workflow writes the
    report's H1 and context once per run, so repeating them per command would be
    noise. (It writes them after the first command, so they land below that
    command's block -- a pre-existing quirk of the workflow, not of this block.)
    """
    lines: list[str] = [
        f"## `{model.command.upper()}` Test Results",
        "",
        f"**Result:** {_status_emoji(model.passed)} {model.verdict_label} — "
        f"{_inline_text(model.verdict_detail)}",
        "",
        "| Check | Result | Details |",
        "|-------|--------|---------|",
    ]
    lines.extend(
        f"| {check.name} | {_CHECK_GLYPHS[check.status]} "
        f"| {_inline_text(check.summary)} |"
        for check in model.checks
    )
    lines.append("")
    lines.extend(_inline_finding_lines(model))

    stream_rows = _inline_stream_rows(model)
    if stream_rows:
        # The true count, not the number of sections: `stream_sections` is capped
        # and the omitted note below states the difference.
        stream_count = len(model.stream_sections) + model.omitted_stream_count
        if stream_count > INLINE_STREAM_TABLE_COLLAPSE_THRESHOLD:
            # Blank lines around the table are required for GitHub to render
            # markdown inside an HTML block.
            lines.extend(
                [
                    f"<details><summary>Record counts per stream "
                    f"({stream_count} streams)</summary>",
                    "",
                    *stream_rows,
                    "",
                    "</details>",
                    "",
                ]
            )
        else:
            lines.extend([*stream_rows, ""])

    lines.extend([_artifact_pointer(model.context), ""])

    return "\n".join(lines)
