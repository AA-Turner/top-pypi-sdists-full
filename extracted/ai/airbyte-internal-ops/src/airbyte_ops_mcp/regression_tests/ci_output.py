# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""CI-friendly output helpers for GitHub Actions integration.

This module provides utilities for writing structured output to GitHub Actions
environment files (GITHUB_OUTPUT and GITHUB_STEP_SUMMARY), and for generating
regression test reports modeled on the legacy connector_live_tests HTML reports.
"""

from __future__ import annotations

import datetime
import json
import os
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from airbyte_ops_mcp.regression_tests.models import StreamError

if TYPE_CHECKING:
    from airbyte_ops_mcp.regression_tests.repro_case import ReproductionVerdict


def is_ci() -> bool:
    """Check if running in a CI environment."""
    return bool(os.getenv("CI"))


def is_github_actions() -> bool:
    """Check if running in GitHub Actions."""
    return bool(os.getenv("GITHUB_ACTIONS"))


def write_github_output(key: str, value: str | int | bool | None) -> None:
    """Write a single key-value pair to GITHUB_OUTPUT.

    Args:
        key: The output variable name.
        value: The value to write. None values are skipped.
    """
    if value is None:
        return

    github_output = os.getenv("GITHUB_OUTPUT")
    if not github_output:
        return

    with open(github_output, "a", encoding="utf-8") as f:
        if isinstance(value, bool):
            value = str(value).lower()
        f.write(f"{key}={value}\n")


def write_github_outputs(outputs: dict[str, Any]) -> None:
    """Write multiple key-value pairs to GITHUB_OUTPUT.

    Args:
        outputs: Dictionary of output variables. None values are skipped.
    """
    for key, value in outputs.items():
        write_github_output(key, value)


def write_github_summary(content: str) -> None:
    """Write content to GITHUB_STEP_SUMMARY.

    Args:
        content: Markdown content to append to the step summary.
    """
    github_summary = os.getenv("GITHUB_STEP_SUMMARY")
    if not github_summary:
        return

    with open(github_summary, "a", encoding="utf-8") as f:
        f.write(content)
        if not content.endswith("\n"):
            f.write("\n")


def write_test_summary(
    connector_image: str,
    test_type: str,
    success: bool,
    results: dict[str, Any],
    details: str | None = None,
) -> None:
    """Write a formatted test summary to GITHUB_STEP_SUMMARY.

    Generic plumbing for any test type. The regression-test path no longer uses
    it: it emits the richer concise summary built by
    `airbyte_ops_mcp.regression_tests.report.render_inline_summary` instead.

    Args:
        connector_image: The connector image being tested.
        test_type: Type of test (e.g., "live-test", "regression-test").
        success: Whether the test passed.
        results: Dictionary of test results to display.
        details: Optional additional details in markdown format.
    """
    status_emoji = "✅" if success else "❌"
    status_text = "PASSED" if success else "FAILED"

    summary = f"""## {status_emoji} {test_type.title()} Results

**Connector:** `{connector_image}`
**Status:** {status_text}

### Results

| Metric | Value |
|--------|-------|
"""

    for key, value in results.items():
        display_key = key.replace("_", " ").title()
        summary += f"| {display_key} | {value} |\n"

    if details:
        summary += f"\n### Details\n\n{details}\n"

    write_github_summary(summary)


def write_json_output(key: str, data: dict[str, Any] | list[Any]) -> None:
    """Write JSON data to GITHUB_OUTPUT using multiline format.

    For complex data structures, GitHub Actions requires multiline output format.

    Args:
        key: The output variable name.
        data: The data to serialize as JSON.
    """
    github_output = os.getenv("GITHUB_OUTPUT")
    if not github_output:
        return

    json_str = json.dumps(data, separators=(",", ":"))

    with open(github_output, "a", encoding="utf-8") as f:
        delimiter = "EOF"
        f.write(f"{key}<<{delimiter}\n")
        f.write(json_str)
        f.write(f"\n{delimiter}\n")


ARTIFACT_NAME_PREFIX = "regression-test-artifacts"
ARTIFACT_NAME_ENV_VAR = "REGRESSION_TEST_ARTIFACT_NAME"


def github_artifact_name(command: str) -> str:
    """Name of the artifact this command's output is uploaded under.

    The single source of truth for the artifact naming contract shared with
    `.github/workflows/connector-regression-test.yml`, whose per-command
    `actions/upload-artifact` steps use exactly this shape. Outside GitHub
    Actions there is no run id, so the bare per-command name is returned.

    `sandbox-case-run.yml` uploads a single artifact under a name its caller
    chooses and passes it in `REGRESSION_TEST_ARTIFACT_NAME`, which then wins.
    """
    override = os.getenv(ARTIFACT_NAME_ENV_VAR, "")
    if override:
        return override

    run_id = os.getenv("GITHUB_RUN_ID", "")
    if run_id:
        return f"{ARTIFACT_NAME_PREFIX}-{command}-{run_id}"

    return f"{ARTIFACT_NAME_PREFIX}-{command}"


def _format_delta(delta: int) -> str:
    """Format a delta value with +/- prefix and highlight if non-zero."""
    if delta > 0:
        return f"**+{delta}**"
    elif delta < 0:
        return f"**{delta}**"
    return "0"


def github_run_url() -> str | None:
    """Get the URL to the current GitHub Actions workflow run.

    Returns:
        The workflow run URL, or None if not running in GitHub Actions.
    """
    server_url = os.getenv("GITHUB_SERVER_URL")
    repository = os.getenv("GITHUB_REPOSITORY")
    run_id = os.getenv("GITHUB_RUN_ID")

    if not all([server_url, repository, run_id]):
        return None

    return f"{server_url}/{repository}/actions/runs/{run_id}"


def github_artifacts_url() -> str | None:
    """Get the URL to the artifacts section of the current workflow run.

    GitHub offers no URL that deep-links to a file inside an artifact, so this
    is the closest a report link can get: the reviewer downloads the artifact
    from here and opens `report.html` locally.

    Returns:
        The artifacts section URL, or None if not running in GitHub Actions.
    """
    run_url = github_run_url()
    if not run_url:
        return None

    return f"{run_url}#artifacts"


# What an unmeasured metric reads as, and the distinction the HTTP table turns
# on. A proxy that never ran and a connector that never reported are both *not
# measured*, and neither may render as `0` or as `0.00%`: a reviewer reading a
# zero cache-hit ratio concludes the version broke its caching, when in fact
# nobody looked. `not reported` is also what a Java connector, a connector using
# its own `requests.Session`, and a connector on a CDK predating the counters all
# render as -- see docs/regression-tests.md.
_NOT_CAPTURED = "not captured"
_NOT_REPORTED = "not reported"

# One name per HTTP metric, shared by `report.md` and the HTML report's table,
# keyed by the `http_metrics` JSON key. "Flow" is mitmproxy's word; a reviewer
# is counting requests, and the same number must not read as `Requests` on one
# surface and `Flow Count` on the next.
HTTP_METRIC_LABELS: dict[str, str] = {
    "flow_count": "Requests",
    "duplicate_flow_count": "Repeated URLs",
    "replayed_flow_count": "Replayed",
    "live_flow_count": "Live",
    "unreplayable_flow_count": "Unreplayable",
    "replay_hit_ratio": "Replay hit ratio",
    "connector_request_count": "Connector requests",
    "connector_cache_hits_count": "Cache hits",
    "connector_cache_hit_ratio": "Cache hit ratio",
}

# The proxy-derived columns, and the connector-derived ones. Split because the
# two sides of the table go missing independently: a run whose proxy never
# started has the connector's numbers and none of the proxy's. The connector's
# own request count gets a column of its own because it is the denominator of
# `Cache hit ratio` -- the proxy's `Requests` is not: a cache hit is served
# inside `Session.send()` and never reaches the proxy.
_PROXY_HTTP_COLUMNS = (
    "flow_count",
    "duplicate_flow_count",
    "replayed_flow_count",
    "live_flow_count",
    "replay_hit_ratio",
)
_CONNECTOR_HTTP_COLUMNS = (
    "connector_request_count",
    "connector_cache_hits_count",
    "connector_cache_hit_ratio",
)


def _http_metrics_row(version: str, http_metrics: dict[str, Any]) -> str:
    """One version's row of the HTTP table, with unmeasured sides named as such."""
    cells = [
        str(http_metrics.get(key, _NOT_CAPTURED)) for key in _PROXY_HTTP_COLUMNS
    ] + [str(http_metrics.get(key, _NOT_REPORTED)) for key in _CONNECTOR_HTTP_COLUMNS]
    return f"| {version} | " + " | ".join(cells) + " |"


def _pk_integrity_cell(
    uniqueness_info: dict[str, Any], side: str, partial: bool = False
) -> str:
    """Render one version's PK integrity as a table cell.

    Shows the duplicate PK count split into what the target did not introduce
    (pre-existing in both versions, or fixed in the target: a warning) and
    what it did (new: a failure, or a warning on a stopped-early read), plus
    the number of records missing their declared PK values when there are any
    (a failure on either side). The control's own duplicates the target
    dropped or changed records of are named apart ("with dropped or changed
    records"): the field values or PK presence fail on them, so this cell only
    warns. The glyph follows the comparison's `passed`, which already applies
    the stopped-early rule, so the cell cannot disagree with the stream's
    result or the Result line. The status closes the cell, after every
    finding, so it reads as the verdict on all of them: `1 (pre-existing), 1
    missing PK ❌`.

    On a `partial` read the comparison calls no control duplicate fixed or
    lost (both counts are 0), so the control's own duplicates are the rest of
    its count, named "not duplicated in target (partial read)".
    """
    duplicate_count = uniqueness_info.get("duplicate_pk_count", 0)
    pre_existing = uniqueness_info.get("pre_existing_duplicate_pk_count", 0)
    if side == "target":
        own = [(uniqueness_info.get("new_duplicate_pk_count", 0), "new")]
    else:
        fixed = uniqueness_info.get("fixed_duplicate_pk_count", 0)
        lost = uniqueness_info.get("lost_duplicate_pk_count", 0)
        unclassified = (
            max(0, duplicate_count - pre_existing - fixed - lost) if partial else 0
        )
        own = [
            (fixed, "fixed in target"),
            (lost, "with dropped or changed records"),
            (unclassified, "not duplicated in target (partial read)"),
        ]
    own = [(count, label) for count, label in own if count]

    if pre_existing and not own:
        cell = f"{pre_existing} (pre-existing)"
    elif own and not pre_existing and len(own) == 1:
        cell = f"{own[0][0]} {own[0][1]}"
    elif own:
        parts = [f"{pre_existing} pre-existing"] if pre_existing else []
        parts += [f"{count} {label}" for count, label in own]
        cell = f"{duplicate_count} ({', '.join(parts)})"
    else:
        cell = str(duplicate_count)
    records_missing_pk = uniqueness_info.get("records_missing_pk", 0)
    if records_missing_pk:
        cell += f", {records_missing_pk} missing PK"
    if not uniqueness_info.get("passed", True):
        cell += " ❌"
    elif duplicate_count:
        cell += " ⚠️"
    else:
        cell += " ✅"
    return cell


def _render_record_comparison_section(
    record_comparison: dict[str, Any],
) -> list[str]:
    """Render the record comparison results as markdown lines.

    Takes a serialized RecordComparisonSummary (`to_dict()` output) and
    produces a per-stream table covering all record-level checks plus the
    aggregated error/warning lists.
    """
    checks = record_comparison.get("checks", {})
    counts = checks.get("record_counts", {}).get("streams", {})
    pk_presence = checks.get("pk_presence", {}).get("streams", {})
    uniqueness_control = checks.get("pk_uniqueness_control", {}).get("streams", {})
    uniqueness_target = checks.get("pk_uniqueness_target", {}).get("streams", {})
    field_values = checks.get("field_values", {}).get("streams", {})
    streams_without_pk = set(record_comparison.get("streams_without_pk", []))

    passed = record_comparison.get("passed", False)
    partial = bool(record_comparison.get("partial"))
    status = "✅ PASSED" if passed else "❌ FAILED"

    lines: list[str] = [
        "### Record Comparison",
        "",
        f"**Status:** {status}",
        "",
        (
            "Checks: directional record counts (target ≥ control), primary key "
            + "presence (all control PKs must appear in target), PK integrity "
            + "(per version: no records missing their declared PK values, and "
            + "no duplicate PK values the target introduced — duplicates present "
            + "in both versions are pre-existing and only warn), and field-value "
            + "equality on PK-matched records. Streams without a primary key "
            + "fall back to count comparison only."
        ),
        "",
        *(
            [
                (
                    "This read was stopped early, so the two outputs end at different "
                    + "points: record counts and primary key presence are inconclusive "
                    + "here (⚠️ whatever they show — under a cap equal counts are what "
                    + "the cap guarantees). A cap or deadline can also cut a duplicated "
                    + "PK value's records on one side, so duplicate PKs new in the "
                    + "target, the field values of PK values with more than one record "
                    + "on either side, and control duplicates the target does not repeat "
                    + "are reported, not judged; no added copies or count allowance are "
                    + "computed. Only records missing their declared PK values and the "
                    + "field values of PK values both sides emitted once decide the "
                    + "status."
                ),
                "",
            ]
            if partial
            else []
        ),
        "| Stream | Count (C → T) | Missing PKs | Dup PKs (control) | Dup PKs (target) | Value Diffs | Result |",
        "|--------|---------------|-------------|-------------------|------------------|-------------|--------|",
    ]

    all_streams = sorted(
        set(counts)
        | set(pk_presence)
        | set(uniqueness_control)
        | set(uniqueness_target)
        | set(field_values)
    )

    # On a partial read the count and presence cells are inconclusive whatever
    # they show, and they never decide the stream's result.
    def glyph(info_passed: bool) -> str:
        if partial:
            return "⚠️"
        return "✅" if info_passed else "❌"

    for stream in all_streams:
        count_info = counts.get(stream, {})
        count_pass = count_info.get("passed", True)
        control_count = count_info.get("control_count", 0)
        target_count = count_info.get("target_count", 0)
        # A count that passes with fewer target records passed on the
        # duplicate-row allowance: the shortfall is within the duplicate rows
        # the target dropped. On a partial read the cell is inconclusive
        # whatever it shows.
        count_warned = count_pass and target_count < control_count
        if partial:
            count_status = glyph(count_pass)
        elif not count_pass:
            count_status = "❌"
        elif count_warned:
            count_status = "⚠️"
        else:
            count_status = "✅"
        count_cell = f"{control_count} → {target_count} {count_status}"

        if stream in streams_without_pk:
            missing_cell = dup_control_cell = dup_target_cell = diff_cell = "—"
            stream_passed = count_pass or partial
            stream_warned = partial or count_warned
        else:
            presence_info = pk_presence.get(stream, {})
            missing = presence_info.get("missing_pk_count", 0)
            missing_cell = f"{missing} {glyph(presence_info.get('passed', True))}"

            dup_control = uniqueness_control.get(stream, {})
            dup_control_cell = _pk_integrity_cell(dup_control, "control", partial)

            dup_target = uniqueness_target.get(stream, {})
            dup_target_cell = _pk_integrity_cell(dup_target, "target", partial)

            field_info = field_values.get(stream, {})
            diff_count = field_info.get("records_with_value_diff", 0)
            # Identical copies the target added under an already-duplicated
            # PK warn; they are not value diffs. Neither are the duplicated
            # PK values a stopped-early read could not judge.
            added_copies = field_info.get("added_copy_count", 0)
            partial_groups = field_info.get("partial_group_diff_count", 0)
            diff_cell = str(diff_count)
            if added_copies:
                copies = "copy" if added_copies == 1 else "copies"
                diff_cell += f", {added_copies} added {copies}"
            if partial_groups:
                diff_cell += f", {partial_groups} duplicated PK(s) inconclusive"
            if not field_info.get("passed", True):
                diff_cell += " ❌"
            elif added_copies or partial_groups:
                diff_cell += " ⚠️"
            else:
                diff_cell += " ✅"

            deciding = (
                (dup_control, dup_target, field_info)
                if partial
                else (count_info, presence_info, dup_control, dup_target, field_info)
            )
            stream_passed = all(info.get("passed", True) for info in deciding)
            stream_warned = (
                partial
                or count_warned
                or bool(added_copies)
                or any(
                    info.get("duplicate_pk_count", 0)
                    for info in (dup_control, dup_target)
                )
            )

        if not stream_passed:
            result_cell = "❌"
        elif stream_warned:
            result_cell = "⚠️"
        else:
            result_cell = "✅"
        # Stream names are connector-controlled: a `|` would split the row
        # into extra columns and a newline would end the table entirely.
        stream_cell = " ".join(stream.split()).replace("|", "\\|")
        lines.append(
            f"| {stream_cell} | {count_cell} | {missing_cell} | {dup_control_cell} "
            f"| {dup_target_cell} | {diff_cell} | {result_cell} |"
        )

    lines.append("")

    errors = record_comparison.get("errors", [])
    if errors:
        lines.extend(["#### Comparison Errors", ""])
        lines.extend(f"- ❌ {error}" for error in errors[:20])
        if len(errors) > 20:
            lines.append(f"- … and {len(errors) - 20} more (see run artifacts)")
        lines.append("")

    warnings = record_comparison.get("warnings", [])
    if warnings:
        lines.extend(["#### Comparison Warnings", ""])
        lines.extend(f"- ⚠️ {warning}" for warning in warnings[:20])
        if len(warnings) > 20:
            lines.append(f"- … and {len(warnings) - 20} more (see run artifacts)")
        lines.append("")

    return lines


@dataclass(frozen=True)
class ComparisonOutcome:
    """The derived outcome of comparing target and control results.

    Exactly one of `both_succeeded`, `regression_detected`, `both_failed` and
    `control_failed_only` is true. `check_improvement` is a sub-case of
    `control_failed_only` and is the only way a run that is not
    `both_succeeded` can still be a pass.
    """

    success: bool
    regression_detected: bool
    both_failed: bool
    control_failed_only: bool
    check_improvement: bool
    both_succeeded: bool


def command_result_succeeded(command: str, result: dict[str, Any]) -> bool:
    """Whether a single connector run passed the given command.

    The run must always exit cleanly. For `check` it must additionally report
    `connectionStatus: SUCCEEDED`: the CDK exits 0 even when a check fails, so
    the exit code alone would call a failed check a pass. A `check` run that
    reports no status at all fails closed -- we cannot call that a pass.

    This is the single per-version rule shared by comparison mode
    (`evaluate_comparison_outcome`) and single-version mode.
    """
    if not result["success"]:
        return False

    if command == "check":
        return result.get("connection_status") == "SUCCEEDED"

    return True


def _describe_run(command: str, result: dict[str, Any]) -> str:
    """Describe what one side of a comparison actually did, for the report.

    Never asserts a `connectionStatus` the run did not report: for `check` the
    verdict also depends on the exit code, so a run that reports SUCCEEDED and
    then exits nonzero is a failure that must not be described as
    "connectionStatus FAILED".
    """
    exit_code = result["exit_code"]

    if command != "check":
        return "succeeded" if result["success"] else f"failed (exit {exit_code})"

    status = result.get("connection_status")

    if not result["success"]:
        if status:
            return f"exited {exit_code} after reporting connectionStatus {status}"
        return f"exited {exit_code} with no connectionStatus"

    if status is None:
        return "exited 0 but reported no connectionStatus"

    return f"connectionStatus {status}"


def stopped_early_sides(
    *sides: tuple[str, dict[str, Any]],
) -> tuple[tuple[str, dict[str, Any]], ...]:
    """The sides the harness stopped, as `(role, stopped_early)` pairs.

    `stopped_early` is the per-side dict `_run_connector_command` emits --
    `reason`, `records_seen`, `elapsed_s` -- and is `None` on a side that ran
    to completion, which is left out here.
    """
    return tuple(
        (role, result["stopped_early"])
        for role, result in sides
        if result.get("stopped_early")
    )


def describe_stopped_early(
    stopped: Sequence[tuple[str, dict[str, Any]]], side_count: int
) -> str:
    """The Result line's account of a run that was stopped early.

    One clause when both sides stopped with the same count, and both counts
    when they did not: under a cap the two sides hold the same number of
    records, under a deadline they rarely do, and that difference is what a
    reader needs before reading the count table. Equal counts are not the
    same records: a connector that reads slices concurrently can stop each
    side at different records.
    """
    reasons = sorted({entry["reason"] for _role, entry in stopped})
    reason = (
        reasons[0]
        if len(reasons) == 1
        else ", ".join(f"{role}: {entry['reason']}" for role, entry in stopped)
    )
    counts = [entry["records_seen"] for _role, entry in stopped]
    if side_count == 1:
        return f"stopped early ({reason}) after {counts[0]:,} records"
    if len(stopped) < side_count:
        role = stopped[0][0]
        other = "control" if role == "target" else "target"
        return (
            f"{role} stopped early ({reason}) after {counts[0]:,} records; "
            f"{other} ran to completion"
        )
    if len(set(counts)) == 1:
        return f"stopped early ({reason}) after {counts[0]:,} records per side"
    both = " / ".join(f"{entry['records_seen']:,} ({role})" for role, entry in stopped)

    return f"stopped early ({reason}) after {both} records"


def stopped_early_notes(
    stopped: Sequence[tuple[str, dict[str, Any]]],
) -> tuple[str, ...]:
    """One line per stopped side, for the context block of every surface.

    A read's deadline is its share of `--read-timeout`, so a side stopped at
    its deadline carries `share_s` and `budget_s`, and its line names the
    share: the deadline falls before the budget's end (well before it for a
    comparison's control), and a bare elapsed time would read as the whole
    budget. A share of 0 is a side that never started.
    """
    notes: list[str] = []
    for role, entry in stopped:
        note = (
            f"{'Run' if role == 'single' else role.capitalize()}: stopped early "
            f"({entry['reason']}) after {entry['records_seen']:,} records "
            f"in {entry['elapsed_s']:,.0f} s"
        )
        share_s = entry.get("share_s")
        budget_s = entry.get("budget_s")
        if share_s is not None and budget_s is not None:
            budget = f"the {_duration_adjective(budget_s)} read budget"
            note += (
                f", without starting: nothing was left of {budget}"
                if share_s == 0
                else f", at the end of its {_duration_adjective(share_s)} share "
                f"of {budget}"
            )
        notes.append(note)
    return tuple(notes)


LEGACY_NOT_FOUND_MESSAGE = (
    "A stream listed in your configuration was not found in the source. "
    "Please check the logs for more details."
)
_CDK_AGGREGATE_ERROR_PREFIX = (
    "During the sync, the following streams did not sync successfully"
)


def not_exercised_streams(
    target_only_streams: Sequence[str],
    target_counts: Mapping[str, int],
    excluded_streams: Sequence[str] = (),
) -> tuple[str, ...]:
    """The target-only streams the target read nothing from.

    A stream configured for the target but not for the control -- typically one
    the connector PR adds -- has no control side to compare against, so the
    record comparison cannot fail it. Zero records there means the PR's new
    code path was never run, and the rule that catches it is this one. Empty
    whenever the two sides read the same catalog, which keeps the verdict of
    such a run exactly as it was.
    """
    return tuple(
        stream
        for stream in target_only_streams
        if stream not in excluded_streams and not target_counts.get(stream, 0)
    )


def undefined_streams(
    target_only_streams: Sequence[str],
    statuses: Mapping[str, Sequence[str]],
    record_counts: Mapping[str, int],
    errors: Mapping[str | None, Sequence[StreamError]],
) -> tuple[str, ...]:
    """Target-only streams the target connector does not define."""
    result = []
    for stream in target_only_streams:
        stream_errors = errors.get(stream, ())
        incomplete_only = (
            statuses.get(stream, ()) == ["INCOMPLETE"]
            and record_counts.get(stream, 0) == 0
            and not stream_errors
        )
        legacy_not_found = any(
            error.message == LEGACY_NOT_FOUND_MESSAGE for error in stream_errors
        )
        if incomplete_only or legacy_not_found:
            result.append(stream)
    return tuple(result)


def config_error_streams(
    target_only_streams: Sequence[str],
    errors: Mapping[str | None, Sequence[StreamError]],
) -> tuple[str, ...]:
    """Target-only streams with an attributed, non-legacy config error."""
    return tuple(
        stream
        for stream in target_only_streams
        if any(
            error.failure_type == "config_error"
            and error.message != LEGACY_NOT_FOUND_MESSAGE
            for error in errors.get(stream, ())
        )
    )


def could_not_test(
    target_only_streams: Sequence[str],
    errors: Mapping[str | None, Sequence[StreamError]],
) -> bool:
    """Whether every read error prevents testing a target-only config."""
    target_only = set(target_only_streams)
    has_target_config_error = False
    for stream, stream_errors in errors.items():
        for error in stream_errors:
            if stream is None:
                if not (error.message or "").startswith(_CDK_AGGREGATE_ERROR_PREFIX):
                    return False
                continue
            if (
                stream in target_only
                and error.failure_type == "config_error"
                and error.message != LEGACY_NOT_FOUND_MESSAGE
            ):
                has_target_config_error = True
                continue
            return False
    return has_target_config_error


def target_errors_only_from(
    target_only_streams: Sequence[str],
    errors: Mapping[str | None, Sequence[StreamError]],
) -> bool:
    """Whether every recorded error is target-only or a CDK aggregate."""
    target_only = set(target_only_streams)
    return all(
        (
            stream in target_only
            if stream is not None
            else all(
                (error.message or "").startswith(_CDK_AGGREGATE_ERROR_PREFIX)
                for error in stream_errors
            )
        )
        for stream, stream_errors in errors.items()
    )


def describe_setup_error(streams: Sequence[str]) -> str:
    return (
        f"{len(streams)} stream(s) the control did not read are not defined by "
        "the target (lone INCOMPLETE status, no records, no error): "
        f"{', '.join(streams)}"
    )


def describe_could_not_test(
    streams: Sequence[str],
    errors: Mapping[str | None, Sequence[StreamError]],
) -> str:
    details = []
    for stream in streams:
        error = next(
            (
                error
                for error in errors.get(stream, ())
                if error.failure_type == "config_error"
                and error.message != LEGACY_NOT_FOUND_MESSAGE
            ),
            None,
        )
        details.append(
            f"{stream}: {error.message if error and error.message else 'no message provided'}"
        )
    return (
        f"{len(streams)} stream(s) the control did not read failed with a config "
        "error (often a missing permission or scope): " + "; ".join(details)
    )


def describe_not_exercised(streams: Sequence[str]) -> str:
    """The Result line's account of a read that proved nothing about a stream."""
    return (
        f"{len(streams)} stream(s) the control did not read returned no "
        f"records: {', '.join(streams)}"
    )


def not_exercised_note(streams: Sequence[str]) -> str | None:
    """The context-block line of a run with unexercised streams, or `None`."""
    return f"Not exercised: {describe_not_exercised(streams)}" if streams else None


def new_stream_verdict_label(
    *,
    stopped: bool,
    setup_error: bool,
    strict_failed: bool,
    regression: bool,
    both_failed: bool,
    comparison_errored: bool,
    could_not_test: bool,
    not_exercised: bool,
) -> str | None:
    """Choose the label for a run with a target-only stream verdict reason.

    Returns `None` when no incomplete, setup, config-error, comparison-error, or
    unexercised-stream reason needs to override the existing pass/fail path.
    """
    if stopped:
        return "INCOMPLETE"
    if setup_error:
        return "SETUP ERROR"
    if not (could_not_test or not_exercised or comparison_errored):
        return None
    if strict_failed and not comparison_errored:
        return "FAIL (regression)"
    if regression and not could_not_test:
        return "FAIL (regression)"
    if both_failed or comparison_errored:
        return "FAIL (inconclusive)"
    if could_not_test:
        return "COULD NOT TEST (config error)"
    return "NOT EXERCISED"


def _duration_adjective(seconds: int) -> str:
    """`96-minute`, or `45-second` for under ten minutes that are not whole."""
    if seconds % 60 == 0 or seconds >= 600:
        return f"{seconds / 60:,.0f}-minute"
    return f"{seconds:,}-second"


def run_output_mode(*results: dict[str, Any]) -> str | None:
    """How the run's output was written, from the first side that says."""
    for result in results:
        mode = result.get("output_mode")
        if mode:
            return str(mode)
    return None


def run_readable_fields(*results: dict[str, Any]) -> dict[str, Any] | None:
    """What a masked run left readable per stream, from the first side that says.

    The shape is `MaskPolicy.streams` serialised: stream name to `cursor`,
    `readable`, `declared` and `reason`. `None` for a raw run, or a result
    that predates the key.
    """
    for result in results:
        fields = result.get("readable_fields")
        if isinstance(fields, dict):
            return fields
    return None


def readable_cursor_counts(readable_fields: Mapping[str, Any]) -> tuple[int, int]:
    """Streams whose cursor stayed readable, out of those that declare one."""
    with_cursor = [
        entry
        for entry in readable_fields.values()
        if isinstance(entry, dict) and entry.get("cursor")
    ]
    return sum(bool(entry.get("readable")) for entry in with_cursor), len(with_cursor)


def describe_readable_cursors(readable_fields: Mapping[str, Any]) -> str:
    """The one-line count every surface shows; `report.html` has the table."""
    readable, total = readable_cursor_counts(readable_fields)
    return (
        f"cursor readable on {readable} of {total} streams "
        "(integer, date, date-time only)"
    )


def describe_masking(
    output_mode: str | None, readable_fields: Mapping[str, Any] | None = None
) -> str | None:
    """One line on what the run's artifacts hold, for every surface."""
    if output_mode == "masked":
        cursors = (
            describe_readable_cursors(readable_fields)
            if readable_fields is not None
            else "a cursor is readable only when its declared type is an integer or a date"
        )
        return (
            "masked — record values are type-and-length tokens; primary keys "
            f"masked; {cursors}; debug logs off, and DEBUG, TRACE, ERROR and FATAL "
            "log messages, stack traces, error internals and stderr lines keep "
            "only their length"
        )
    if output_mode == "raw":
        return (
            "raw — records, HTTP bodies and logs are unmasked; treat the "
            "artifacts as sensitive"
        )
    return None


def evaluate_comparison_outcome(
    command: str,
    target_result: dict[str, Any],
    control_result: dict[str, Any],
) -> ComparisonOutcome:
    """Evaluate the pass/fail outcome for a target and control comparison.

    Any failure on either side fails the test. A run where both versions failed
    is inconclusive rather than a pass, and so is a run where only the control
    failed: there is nothing left to compare the target against. The single
    exception is `check`, where a target that connects while the control
    cleanly reports FAILED is an improvement, not a failure.
    """
    target_ok = command_result_succeeded(command, target_result)
    control_ok = command_result_succeeded(command, control_result)
    check_improvement = False

    if command == "check":
        # An improvement requires the control to have run cleanly and reported
        # FAILED. A control with no status is inconclusive, not an improvement.
        check_improvement = (
            target_ok
            and control_result.get("connection_status") == "FAILED"
            and bool(control_result["success"])
        )

    return ComparisonOutcome(
        success=target_ok and (control_ok or check_improvement),
        regression_detected=not target_ok and control_ok,
        both_failed=not target_ok and not control_ok,
        control_failed_only=target_ok and not control_ok,
        check_improvement=check_improvement,
        both_succeeded=target_ok and control_ok,
    )


def generate_action_test_comparison_report(
    target_image: str,
    control_image: str,
    command: str,
    target_result: dict[str, Any],
    control_result: dict[str, Any],
    output_dir: Path,
    record_comparison: dict[str, Any] | None = None,
    comparison_findings: Sequence[tuple[str, str]] = (),
    reproduction: ReproductionVerdict | None = None,
    target_only_streams: Sequence[str] = (),
    inconclusive_findings: Sequence[str] = (),
) -> Path:
    """Generate a markdown comparison report for a single action (command).

    This creates a comprehensive report with context, message counts comparison,
    and record counts per stream (for read commands). The report starts with an
    L2 header containing the command name, making it easy to consolidate multiple
    command reports into a single document.

    Args:
        target_image: The target (new version) connector image.
        control_image: The control (baseline version) connector image.
        command: The Airbyte command that was run (e.g., "spec", "check", "discover", "read").
        target_result: Results dict from running target connector.
        control_result: Results dict from running control connector.
        output_dir: Directory to write the report to.
        record_comparison: Optional serialized RecordComparisonSummary
            (from `RecordComparisonSummary.to_dict()`) for read commands.
        comparison_findings: What comparing the two versions' output found, as
            `(status, sentence)` pairs where status is `"fail"` or `"warn"`.
            `ComparisonOutcome` describes how the *commands* went, so without
            these this report would announce "no regression" over a spec that
            dropped a field. Warnings are listed without changing the verdict:
            they do not gate a release, but a reader of this file should not
            have to open the HTML report to learn the catalog grew.
        inconclusive_findings: Failed findings that represent checks that could
            not complete, rather than evidence of a regression. They remain
            visible as failed findings in the report.
        reproduction: The reproduction-case verdict, when the run used one. It
            replaces the command-outcome verdict: in case mode a failing control
            is the expected evidence, not an inconclusive run.
        target_only_streams: The streams configured for the target but not for
            the control. One that returned no records makes the verdict NOT
            EXERCISED, never a pass (see `not_exercised_streams`).

    Returns:
        Path to the generated report.md file.
    """
    outcome = evaluate_comparison_outcome(command, target_result, control_result)

    record_comparison_failed = (
        record_comparison is not None and not record_comparison.get("passed", True)
    )

    target_counts = target_result.get("message_counts", {})
    control_counts = control_result.get("message_counts", {})
    target_record_counts = target_result.get("record_counts_per_stream", {})
    control_record_counts = control_result.get("record_counts_per_stream", {})

    # Extract version tags for the summary table
    target_version = (
        target_image.rsplit(":", 1)[-1] if ":" in target_image else "unknown"
    )
    control_version = (
        control_image.rsplit(":", 1)[-1] if ":" in control_image else "unknown"
    )

    # Start with L2 header containing the command name (no L1 header)
    # This allows multiple command reports to be concatenated into a single document
    # Note: Context block (connector, versions, workflow links) is added at the workflow level
    lines: list[str] = [
        f"## `{command.upper()}` Test Results",
        "",
    ]

    # Describe what each side actually did rather than restating the verdict: for
    # `check` the verdict folds in the exit code as well as connectionStatus, so a
    # fixed "connectionStatus FAILED" would contradict the table below whenever a
    # side reports SUCCEEDED and then exits nonzero.
    sides = (
        f"Target {_describe_run(command, target_result)}, "
        f"control {_describe_run(command, control_result)}"
    )

    failures = [text for status, text in comparison_findings if status == "fail"]
    inconclusive_failure_texts = set(inconclusive_findings)
    inconclusive_failures = [
        text for text in failures if text in inconclusive_failure_texts
    ]
    strict_failures = [
        text for text in failures if text not in inconclusive_failure_texts
    ]

    stopped = stopped_early_sides(
        ("control", control_result), ("target", target_result)
    )
    not_exercised = not_exercised_streams(
        target_only_streams,
        target_result.get("record_counts_per_stream", {}),
        excluded_streams=target_result.get("excluded_not_exercised_streams", ()),
    )
    setup_error = bool(target_result.get("setup_error"))
    setup_error_clears_regression = bool(
        target_result.get("setup_error_clears_regression")
    )
    could_not_test_result = bool(target_result.get("could_not_test"))
    record_comparison_errored = bool(
        record_comparison is not None and record_comparison.get("errored")
    )
    strict_problems = len(strict_failures) + (
        1
        if outcome.both_succeeded
        and record_comparison_failed
        and not record_comparison_errored
        else 0
    )
    comparison_errored = (
        (record_comparison_errored or bool(inconclusive_failures))
        and not strict_problems
        and not outcome.regression_detected
    )
    verdict_label = new_stream_verdict_label(
        stopped=bool(stopped),
        setup_error=setup_error,
        strict_failed=bool(strict_problems),
        regression=outcome.regression_detected,
        both_failed=outcome.both_failed,
        comparison_errored=comparison_errored,
        could_not_test=could_not_test_result,
        not_exercised=bool(not_exercised),
    )
    if (
        comparison_errored
        and not outcome.both_failed
        and not_exercised
        and verdict_label == "FAIL (inconclusive)"
    ):
        verdict_label = "NOT EXERCISED"

    if verdict_label is not None:
        # Never a pass: the comparison saw part of what each side would have
        # emitted, or nothing at all of a stream only the target read. A strict
        # failure inside what it saw is still a regression. A stop outranks an
        # unexercised stream, which then goes in the notes below the line.
        if verdict_label == "INCOMPLETE":
            detail = describe_stopped_early(stopped, side_count=2)
        elif verdict_label == "SETUP ERROR":
            detail = target_result.get("setup_error_detail", "Target setup failed.")
            if outcome.regression_detected and not setup_error_clears_regression:
                detail += f"; {sides}"
        elif could_not_test_result and verdict_label == "COULD NOT TEST (config error)":
            detail = target_result.get(
                "could_not_test_detail", "A target config error prevented the read."
            )
        elif could_not_test_result or verdict_label.startswith("FAIL"):
            detail = sides
        else:
            detail = describe_not_exercised(not_exercised)
        if (
            not outcome.success
            and not (setup_error or could_not_test_result)
            and not verdict_label.startswith("FAIL")
        ):
            detail += f"; {sides[0].lower()}{sides[1:]}"
        if setup_error or could_not_test_result:
            if setup_error and verdict_label != "SETUP ERROR":
                detail += "; " + target_result.get("setup_error_detail", "")
            if (
                could_not_test_result
                and verdict_label != "COULD NOT TEST (config error)"
            ):
                detail += "; " + target_result.get("could_not_test_detail", "")
        if not_exercised and verdict_label != "NOT EXERCISED":
            detail += "; " + describe_not_exercised(not_exercised)
        if strict_problems:
            plural = "s" if strict_problems > 1 else ""
            detail += f", and the comparison found {strict_problems} problem{plural}"
        if comparison_errored:
            detail += "; the record comparison errored, so it is inconclusive"
        line = f"**Result:** {verdict_label} — {detail}"
        if strict_problems or (
            outcome.regression_detected
            and not (
                setup_error_clears_regression
                or could_not_test_result
                or comparison_errored
            )
        ):
            line += " — **REGRESSION DETECTED**"
        lines.append(line)
        lines.extend(f"- {note}" for note in stopped_early_notes(stopped))
        if stopped and not_exercised:
            lines.append(f"- {not_exercised_note(not_exercised)}")
    elif reproduction is not None:
        lines.append(f"**Result:** {reproduction.detail} — **{reproduction.label}**")
        lines.extend(f"- {finding}" for finding in reproduction.details)
    elif strict_failures:
        # Only reachable when both commands ran cleanly, so this is the one
        # verdict the exit codes could not have produced.
        plural = "s" if len(strict_failures) > 1 else ""
        lines.append(
            f"**Result:** {sides}, and the comparison found "
            f"{len(strict_failures)} problem{plural} — **REGRESSION DETECTED**"
        )
    elif outcome.check_improvement:
        lines.append(f"**Result:** {sides} — improvement, not a regression")
    elif outcome.regression_detected:
        lines.append(f"**Result:** {sides} — **REGRESSION DETECTED**")
    elif outcome.both_succeeded and record_comparison_failed:
        lines.append(
            "**Result:** Both versions succeeded, but record comparison "
            "failed (**REGRESSION DETECTED**)"
        )
    elif outcome.both_succeeded:
        # A pass requires a clean exit on both sides (plus SUCCEEDED for `check`),
        # so this line cannot disagree with the per-version rows.
        lines.append("**Result:** Both versions succeeded (no regression)")
    elif outcome.both_failed:
        lines.append(
            f"**Result:** {sides} — **TEST FAILED** (inconclusive, cannot rule out "
            "a regression)"
        )
    else:
        lines.append(
            f"**Result:** {sides} — **TEST FAILED** (inconclusive, nothing to "
            "compare the target against)"
        )

    masking = describe_masking(
        run_output_mode(target_result, control_result),
        run_readable_fields(target_result, control_result),
    )
    if masking:
        lines.append(f"- Output mode: {masking}")

    # Use emojis for better scanability. The Result column comes from the shared
    # per-version rule rather than a local re-derivation, so it agrees with the
    # verdict for every combination of exit code and connectionStatus -- including
    # a `check` that exits 0 without reporting a status, which fails closed.
    control_emoji = "✅" if command_result_succeeded(command, control_result) else "❌"
    target_emoji = "✅" if command_result_succeeded(command, target_result) else "❌"

    # For CHECK, show connectionStatus alongside the exit code: connectionStatus
    # is the real signal (the CDK exits 0 even when a check fails), but a version
    # only passes when it also exited cleanly.
    if command == "check":
        target_conn = target_result.get("connection_status")
        control_conn = control_result.get("connection_status")
        # "—" in the connectionStatus column means no status was reported; the
        # Result column above already treats that as a failure.
        conn_control_emoji = (
            "✅" if control_conn == "SUCCEEDED" else "❌" if control_conn else "—"
        )
        conn_target_emoji = (
            "✅" if target_conn == "SUCCEEDED" else "❌" if target_conn else "—"
        )
        lines.extend(
            [
                "",
                "| Version | Exit Code | connectionStatus | Result |",
                "|---------|-----------|------------------|--------|",
                f"| Control (`{control_version}`) | {control_result['exit_code']} | {control_conn or 'N/A'} {conn_control_emoji} | {control_emoji} |",
                f"| Target (`{target_version}`) | {target_result['exit_code']} | {target_conn or 'N/A'} {conn_target_emoji} | {target_emoji} |",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "",
                "| Version | Exit Code | Result |",
                "|---------|-----------|--------|",
                f"| Control (`{control_version}`) | {control_result['exit_code']} | {control_emoji} |",
                f"| Target (`{target_version}`) | {target_result['exit_code']} | {target_emoji} |",
                "",
            ]
        )

    if comparison_findings:
        lines.extend(
            [
                "### Comparison Findings",
                "",
                *(
                    f"- {'❌' if status == 'fail' else '⚠️'} {text}"
                    for status, text in comparison_findings
                ),
                "",
            ]
        )

    lines.extend(
        [
            "### Command Execution Metrics",
            "",
        ]
    )

    if target_counts or control_counts:
        lines.extend(
            [
                "#### Message Types",
                "",
                "| Type | Control | Target | Delta |",
                "|------|---------|--------|-------|",
            ]
        )
        all_types = sorted(set(target_counts) | set(control_counts))
        for msg_type in all_types:
            control_count = control_counts.get(msg_type, 0)
            target_count = target_counts.get(msg_type, 0)
            delta = target_count - control_count
            lines.append(
                f"| `{msg_type}` | {control_count} | {target_count} | {_format_delta(delta)} |"
            )
        lines.append("")

    if target_record_counts or control_record_counts:
        lines.extend(
            [
                "#### Record Count per Stream",
                "",
                "| Stream | Control | Target | Delta |",
                "|--------|---------|--------|-------|",
            ]
        )
        all_streams = sorted(set(target_record_counts) | set(control_record_counts))
        total_control = 0
        total_target = 0
        for stream in all_streams:
            control_count = control_record_counts.get(stream, 0)
            target_count = target_record_counts.get(stream, 0)
            total_control += control_count
            total_target += target_count
            delta = target_count - control_count
            lines.append(
                f"| {stream} | {control_count} | {target_count} | {_format_delta(delta)} |"
            )
        total_delta = total_target - total_control
        lines.append(
            f"| **Total** | **{total_control}** | **{total_target}** | {_format_delta(total_delta)} |"
        )
        lines.append("")

    control_http = control_result.get("http_metrics") or {}
    target_http = target_result.get("http_metrics") or {}
    # Counts only when something was actually measured. A payload holding just
    # `replay_skipped_reason` describes a proxy that never ran, and an all-zero
    # table -- `spec`, and `check` on plenty of connectors -- is noise either
    # way. The skip reason still prints below, outside the table.
    #
    # `connector_request_count` and not `flow_count` alone: the connector's own
    # cache needs no proxy to be measured, so a run whose proxy never started
    # still has half a table to show, and gating on the proxy would hide it.
    if any(
        side.get(key)
        for side in (control_http, target_http)
        for key in ("flow_count", "connector_request_count")
    ):
        lines.extend(
            [
                "#### HTTP Metrics",
                "",
                # The first five columns are the harness's view through the
                # proxy; the last three are the connector's report on its own
                # `requests_cache`, which no proxy can see. Two different
                # measurements of two different things -- see the docs.
                "| Version | "
                + " | ".join(
                    HTTP_METRIC_LABELS[key]
                    for key in (*_PROXY_HTTP_COLUMNS, *_CONNECTOR_HTTP_COLUMNS)
                )
                + " |",
                "|---" * (1 + len(_PROXY_HTTP_COLUMNS) + len(_CONNECTOR_HTTP_COLUMNS))
                + "|",
                _http_metrics_row("Control", control_http),
                _http_metrics_row("Target", target_http),
                "",
            ]
        )
        if control_http.get("unreplayable_flow_count") or target_http.get(
            "unreplayable_flow_count"
        ):
            # Out of the table rather than a ninth column, but never dropped:
            # this is the usual reason replay coverage is poor, and the fix
            # (`--http-replay-max-body`) is only findable if the number is.
            lines.extend(
                [
                    f"Flows excluded from the replay corpus as unreplayable: "
                    f"control {control_http.get('unreplayable_flow_count', 0)}, "
                    f"target {target_http.get('unreplayable_flow_count', 0)}. "
                    "Raise `--http-replay-max-body` if this is a large share of "
                    "the requests.",
                    "",
                ]
            )

    # Outside the table: the reason is the whole story when the proxy never ran,
    # and there are no counts to hang it off.
    if target_http.get("replay_skipped_reason"):
        lines.extend(
            [
                "HTTP replay was requested and skipped: "
                f"{target_http['replay_skipped_reason']}. The target ran "
                "against live data.",
                "",
            ]
        )
    for role, http in (("control", control_http), ("target", target_http)):
        if http.get("capture_skipped_reason"):
            lines.extend(
                [
                    f"HTTP traffic was not captured on the {role}: "
                    f"{http['capture_skipped_reason']}.",
                    "",
                ]
            )

    if record_comparison is not None:
        lines.extend(_render_record_comparison_section(record_comparison))

    # Note: Execution Details section removed as redundant with Summary table

    report_content = "\n".join(lines)
    report_path = output_dir / "report.md"
    report_path.write_text(report_content)

    return report_path


# Backwards-compatible alias for the old function name
generate_regression_report = generate_action_test_comparison_report


def generate_single_version_report(
    connector_image: str,
    command: str,
    result: dict[str, Any],
    output_dir: Path,
) -> Path:
    """Generate a markdown report for a single-version regression test.

    This creates a report with message counts and record counts per stream for a single
    connector run. The report starts with an L2 header containing the command name,
    making it easy to consolidate multiple command reports.

    Args:
        connector_image: The connector image that was tested.
        command: The Airbyte command that was run (e.g., "spec", "check", "discover", "read").
        result: Results dict from running the connector.
        output_dir: Directory to write the report to.

    Returns:
        Path to the generated report.md file.
    """
    message_counts = result.get("message_counts", {})
    record_counts = result.get("record_counts_per_stream", {})

    artifact_name = github_artifact_name(command)

    version = (
        connector_image.rsplit(":", 1)[-1] if ":" in connector_image else "unknown"
    )
    connector_name = (
        connector_image.rsplit(":", 1)[0] if ":" in connector_image else connector_image
    )

    run_url = github_run_url()
    artifacts_url = github_artifacts_url()

    # Get tester identity from environment (GitHub Actions sets GITHUB_ACTOR)
    tester = os.getenv("GITHUB_ACTOR") or os.getenv("USER") or "unknown"

    # Start with L2 header containing the command name (no L1 header)
    lines: list[str] = [
        f"## `{command.upper()}` Test Results",
        "",
        "### Context",
        "",
        f"- **Test Date:** {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"- **Tester:** `{tester}`",
        f"- **Connector:** `{connector_name}`",
        f"- **Version:** `{version}`",
        f"- **Command:** `{command.upper()}`",
    ]

    if run_url:
        lines.append(f"- **Workflow Run:** [View Execution]({run_url})")
    if artifacts_url:
        lines.append(f"- **Artifacts:** [Download `{artifact_name}`]({artifacts_url})")
    else:
        lines.append(f"- **Artifacts:** `{artifact_name}`")

    masking = describe_masking(run_output_mode(result), run_readable_fields(result))
    if masking:
        lines.append(f"- **Output mode:** {masking}")

    # Single-version mode uses the same per-version rule as comparison mode, so a
    # `check` that exits 0 with connectionStatus FAILED is a FAIL, not a pass.
    succeeded = command_result_succeeded(command, result)
    stopped = stopped_early_sides(("single", result))
    if stopped:
        verdict = f"INCOMPLETE — {describe_stopped_early(stopped, side_count=1)}"
    else:
        verdict = "PASS" if succeeded else "FAIL"

    lines.extend(
        [
            "",
            "### Summary",
            "",
            f"**Result:** {verdict}",
            *(f"- {note}" for note in stopped_early_notes(stopped)),
            "",
            f"- **Exit Code:** {result['exit_code']}",
        ]
    )

    if command == "check":
        lines.append(
            f"- **connectionStatus:** {result.get('connection_status') or 'N/A'}"
        )

    lines.extend(
        [
            f"- **Success:** {succeeded}",
            "",
        ]
    )

    if message_counts:
        lines.extend(
            [
                "### Message Types",
                "",
                "| Type | Count |",
                "|------|-------|",
            ]
        )
        for msg_type in sorted(message_counts.keys()):
            count = message_counts[msg_type]
            lines.append(f"| `{msg_type}` | {count} |")
        lines.append("")

    if record_counts:
        lines.extend(
            [
                "### Record Count per Stream",
                "",
                "| Stream | Count |",
                "|--------|-------|",
            ]
        )
        total = 0
        for stream in sorted(record_counts.keys()):
            count = record_counts[stream]
            total += count
            lines.append(f"| {stream} | {count} |")
        lines.append(f"| **Total** | **{total}** |")
        lines.append("")

    lines.extend(
        [
            "### Execution Details",
            "",
            f"- **Image:** `{connector_image}`",
            f"- **Stdout:** `{result.get('stdout_file', 'N/A')}`",
            f"- **Stderr:** `{result.get('stderr_file', 'N/A')}`",
            "",
        ]
    )

    report_content = "\n".join(lines)
    report_path = output_dir / "report.md"
    report_path.write_text(report_content)

    return report_path
