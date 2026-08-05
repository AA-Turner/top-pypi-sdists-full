# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for the regression-test report model and its two renderers."""

import re
from dataclasses import replace
from pathlib import Path

import pytest
from airbyte_protocol.models import AirbyteMessage, AirbyteRecordMessage
from airbyte_protocol.models import Type as AirbyteMessageType

from airbyte_ops_mcp.regression_tests.ci_output import (
    ARTIFACT_NAME_PREFIX,
    evaluate_comparison_outcome,
    github_artifact_name,
)
from airbyte_ops_mcp.regression_tests.regression import (
    ComparisonResult,
    RecordComparisonSummary,
    run_record_comparisons,
)
from airbyte_ops_mcp.regression_tests.report import (
    HTML_REPORT_FILENAME,
    INLINE_STREAM_TABLE_COLLAPSE_THRESHOLD,
    MAX_DIFF_LINES_PER_BLOCK,
    MAX_INLINE_FINDINGS,
    MAX_INLINE_STREAM_ROWS,
    MAX_LABEL_CHARS,
    MAX_LINE_CHARS,
    MAX_OUTPUT_TAIL_BYTES,
    MAX_STREAM_SECTIONS,
    META_MARKER,
    RECORD_COUNTS_TABLE,
    CheckResult,
    DiffLine,
    SplitDiffRow,
    build_comparison_report_model,
    build_diff_block,
    build_json_block,
    build_single_version_report_model,
    build_split_diff_block,
    consolidate_reports,
    extract_report_part,
    render_html_report,
    render_inline_summary,
    write_html_report,
)

pytestmark = pytest.mark.unit

TARGET_IMAGE = "airbyte/source-faker:6.3.0"
CONTROL_IMAGE = "airbyte/source-faker:6.2.0"


def _run_result(success: bool, **extra) -> dict:
    """Build a minimal run-result dict of the shape the builders expect."""
    return {"success": success, "exit_code": 0 if success else 1, **extra}


def _comparison(command: str, target: dict, control: dict, **kwargs):
    """Build a comparison model from two run results."""
    return build_comparison_report_model(
        target_image=TARGET_IMAGE,
        control_image=CONTROL_IMAGE,
        command=command,
        target_result=target,
        control_result=control,
        **kwargs,
    )


# --------------------------------------------------------------------------
# Verdict parity: the model must never disagree with the shared verdict rules
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "command,target_result,control_result",
    [
        pytest.param("read", _run_result(True), _run_result(True), id="both-succeed"),
        pytest.param("read", _run_result(False), _run_result(True), id="regression"),
        pytest.param("read", _run_result(False), _run_result(False), id="both-failed"),
        pytest.param(
            "read", _run_result(True), _run_result(False), id="control-only-failure"
        ),
        pytest.param(
            "check",
            _run_result(True, connection_status="SUCCEEDED"),
            _run_result(True, connection_status="FAILED"),
            id="check-improvement",
        ),
        pytest.param(
            "check",
            _run_result(True, connection_status="FAILED"),
            _run_result(True, connection_status="SUCCEEDED"),
            id="check-regression",
        ),
        pytest.param(
            "check",
            _run_result(True),
            _run_result(True, connection_status="SUCCEEDED"),
            id="check-target-missing-status-fails-closed",
        ),
    ],
)
def test_comparison_verdict_matches_the_shared_rule(
    command, target_result, control_result
):
    """`passed` is the shared outcome, not a re-derivation, and the check agrees."""
    outcome = evaluate_comparison_outcome(command, target_result, control_result)
    model = _comparison(command, target_result, control_result)

    assert model.passed is outcome.success
    assert model.checks[0].passed is outcome.success
    assert model.verdict_label.startswith("PASS" if outcome.success else "FAIL")


def test_comparison_reuses_a_supplied_outcome():
    """A caller's already-evaluated outcome is used rather than recomputed."""
    target, control = _run_result(True), _run_result(True)
    outcome = evaluate_comparison_outcome("read", target, control)

    model = build_comparison_report_model(
        target_image=TARGET_IMAGE,
        control_image=CONTROL_IMAGE,
        command="read",
        target_result=target,
        control_result=control,
        outcome=outcome,
    )

    assert model.outcome is outcome


@pytest.mark.parametrize(
    "command,result,expected_passed",
    [
        pytest.param("spec", _run_result(True), True, id="spec-clean-exit-passes"),
        pytest.param("spec", _run_result(False), False, id="spec-failure-fails"),
        pytest.param(
            "check",
            _run_result(True, connection_status="SUCCEEDED"),
            True,
            id="check-succeeded-passes",
        ),
        pytest.param(
            "check",
            _run_result(True, connection_status="FAILED"),
            False,
            id="check-failed-status-fails-despite-clean-exit",
        ),
        pytest.param(
            "check", _run_result(True), False, id="check-missing-status-fails-closed"
        ),
    ],
)
def test_single_version_verdict_matches_the_shared_rule(
    command, result, expected_passed
):
    """Single-version mode uses the same per-version rule as comparison mode."""
    model = build_single_version_report_model(
        connector_image=TARGET_IMAGE, command=command, result=result
    )

    assert model.passed is expected_passed
    assert model.checks[0].passed is expected_passed


def test_record_counts_do_not_decide_the_verdict():
    """A count drop is reported but does not fail the run.

    Directional record comparison belongs to the record-comparison work; this
    report must not pre-empt it with a verdict of its own.
    """
    model = _comparison(
        "read",
        _run_result(True, record_counts_per_stream={"users": 1}),
        _run_result(True, record_counts_per_stream={"users": 100}),
    )

    assert model.passed is True
    assert [section.status for section in model.stream_sections] == ["info"]


# --------------------------------------------------------------------------
# Model shape
# --------------------------------------------------------------------------


def test_single_check_is_emitted_today():
    """Exactly one check exists until the comparison checks are wired in."""
    model = _comparison("read", _run_result(True), _run_result(True))

    assert [check.name for check in model.checks] == ["Command execution"]
    assert model.checks[0].severity == "strict"


# --------------------------------------------------------------------------
# The check seam: appending a check must move the verdict, on both surfaces
# --------------------------------------------------------------------------


def test_a_failing_strict_check_fails_a_run_whose_commands_both_succeeded():
    """This is the seam's whole promise: append a check and the verdict follows.

    Without the fold the banner would read PASS directly above a table row
    saying the data differs.
    """
    model = _comparison(
        "read",
        _run_result(True),
        _run_result(True),
        extra_checks=(
            CheckResult(name="Record counts", passed=False, summary="51 fewer records"),
        ),
    )

    assert model.passed is False
    assert model.verdict_label == "FAIL (regression)"
    assert "1 check failed: record counts" in model.verdict_detail
    assert "❌ FAIL (regression)" in render_inline_summary(model)
    assert "verdict--fail" in render_html_report(model)


def test_a_failing_diagnostic_check_warns_without_failing_the_run():
    """Diagnostics are worth seeing and not worth failing a release over."""
    model = _comparison(
        "read",
        _run_result(True),
        _run_result(True),
        extra_checks=(
            CheckResult(
                name="Schema",
                passed=False,
                severity="diagnostic",
                summary="a field widened from integer to number",
            ),
        ),
    )

    assert model.passed is True
    assert model.verdict_label == "PASS"
    assert model.checks[1].status == "warn"


def test_an_unrecognised_severity_fails_closed():
    """A typo must not downgrade a real failure to a warning."""
    model = _comparison(
        "read",
        _run_result(True),
        _run_result(True),
        extra_checks=(CheckResult(name="Typo", passed=False, severity="diagnostics"),),
    )

    assert model.checks[1].status == "fail"
    assert model.passed is False


def test_a_failing_check_does_not_overwrite_a_command_failure_verdict():
    """A command that failed stays the headline; checks cannot soften it."""
    model = _comparison(
        "read",
        _run_result(False),
        _run_result(True),
        extra_checks=(CheckResult(name="Record counts", passed=False),),
    )

    assert model.passed is False
    assert model.verdict_label == "FAIL (regression)"
    assert "check failed" not in model.verdict_detail


def test_a_folded_failure_stops_claiming_there_was_no_regression():
    """No surface may report a clean run and a failed check in one breath.

    The wording is written from the command outcome, which for two clean runs
    says "no regression" -- exactly what the failing check denies. Both the
    banner and the check table are pinned here: fixing only the banner left the
    contradiction on the row a reviewer actually scans.
    """
    model = _comparison(
        "spec",
        _run_result(True),
        _run_result(True),
        extra_checks=(CheckResult(name="Spec compatibility", passed=False),),
    )
    html = render_html_report(model)
    summary = render_inline_summary(model)

    assert model.passed is False
    assert model.verdict_detail == (
        "Both versions succeeded, but 1 check failed: spec compatibility"
    )
    assert "no regression" not in html
    assert "no regression" not in summary


def test_a_passing_run_still_says_there_was_no_regression():
    """The parenthetical is dropped because a check denied it, not by default."""
    model = _comparison("spec", _run_result(True), _run_result(True))

    assert model.verdict_detail == "Both versions succeeded (no regression)"


def test_the_step_summary_lists_what_a_failing_check_found():
    """Most readers never download the artifact, so the names ship with the run.

    The diff itself stays in the report; this is the list that tells a reviewer
    whether opening it is worth the click.
    """
    model = _comparison(
        "discover",
        _run_result(True),
        _run_result(True),
        extra_checks=(
            CheckResult(
                name="Catalog schema",
                passed=False,
                summary="Discovered catalog changed in 2 streams",
                details=(
                    "Stream users has schema differences",
                    "Stream gone is missing",
                ),
            ),
        ),
    )
    summary = render_inline_summary(model)

    assert "<details><summary>What the comparison found (2)</summary>" in summary
    assert "- Stream users has schema differences" in summary
    assert "- Stream gone is missing" in summary
    # The HTML report carries the same list, under the check row, so the
    # summary's "and N more, in the report" pointer is true.
    html = render_html_report(model)
    assert "All 2 findings" in html
    assert "Stream users has schema differences" in html
    assert "Stream gone is missing" in html


def test_the_step_summary_caps_the_findings_it_lists():
    """A 200-stream catalog change must not push the run's other steps off screen."""
    model = _comparison(
        "discover",
        _run_result(True),
        _run_result(True),
        extra_checks=(
            CheckResult(
                name="Catalog schema",
                passed=False,
                details=tuple(f"Stream s{index} changed" for index in range(40)),
            ),
        ),
    )
    summary = render_inline_summary(model)

    assert summary.count("\n- Stream ") == MAX_INLINE_FINDINGS
    assert f"… and {40 - MAX_INLINE_FINDINGS} more, in the report" in summary


def test_a_passing_check_does_not_list_findings():
    """A green run stays short: there is nothing for a reviewer to decide."""
    model = _comparison(
        "spec",
        _run_result(True),
        _run_result(True),
        extra_checks=(CheckResult(name="Spec compatibility", passed=True),),
    )

    assert "What the comparison found" not in render_inline_summary(model)


def test_comparison_diff_blocks_are_rendered_above_the_failure_output():
    """A check row has one line; the reviewer's next question is always "what?"."""
    model = _comparison(
        "discover",
        _run_result(True),
        _run_result(True),
        extra_checks=(CheckResult(name="Catalog schema", passed=False),),
        extra_diff_blocks=(
            build_json_block("Schema diff — users", '{"type_changes": {"id": 1}}'),
        ),
    )
    html = render_html_report(model)

    assert "Schema diff — users" in html
    assert "type_changes" in html


def test_both_surfaces_classify_a_check_the_same_way():
    """`status` is the single classification, so no surface can disagree."""
    model = _comparison(
        "read",
        _run_result(True),
        _run_result(True),
        extra_checks=(
            CheckResult(name="Warned", passed=False, severity="diagnostic"),
            CheckResult(name="Passed check", passed=True),
        ),
    )
    html = render_html_report(model)
    summary = render_inline_summary(model)

    assert '<td class="status--warn">WARN</td>' in html
    assert "| Warned | ⚠️ |" in summary
    assert '<td class="status--pass">PASS</td>' in html
    assert "| Passed check | ✅ |" in summary


def test_metric_tables_carry_sorted_rows_deltas_and_totals():
    """Rows are sorted, deltas are signed, and the total matches the columns."""
    model = _comparison(
        "read",
        _run_result(
            True,
            message_counts={"RECORD": 300, "STATE": 2},
            record_counts_per_stream={"users": 88, "events": 200},
        ),
        _run_result(
            True,
            message_counts={"RECORD": 312, "STATE": 2},
            record_counts_per_stream={"users": 100, "events": 200},
        ),
    )
    tables = {table.title: table for table in model.metric_tables}

    assert [row.label for row in tables["Message Types"].rows] == ["RECORD", "STATE"]
    assert tables["Message Types"].rows[0].delta == -12
    assert tables["Message Types"].rows[1].changed is False

    records = tables["Record Count per Stream"]
    assert [row.label for row in records.rows] == ["events", "users"]
    assert records.total.control == 300
    assert records.total.target == 288
    assert records.total.delta == -12


def test_empty_counts_produce_no_tables():
    """A command with no messages renders no empty metric tables."""
    model = _comparison("spec", _run_result(True), _run_result(True))

    assert model.metric_tables == ()
    assert model.stream_sections == ()


def test_a_control_that_emitted_nothing_is_still_compared():
    """An empty control is a comparison with zero counts, not a single-version run."""
    model = _comparison(
        "read",
        _run_result(True, record_counts_per_stream={"users": 5}),
        _run_result(True, record_counts_per_stream={}),
    )

    assert model.stream_sections[0].metrics[0].control == 0
    assert model.stream_sections[0].metrics[0].delta == 5
    assert "0 → 5 records (+5)" in model.stream_sections[0].headline


def test_http_metrics_table_only_appears_when_recorded():
    """The HTTP table is absent without `--enable-http-metrics`."""
    without = _comparison("read", _run_result(True), _run_result(True))
    with_metrics = _comparison(
        "read",
        _run_result(True, http_metrics={"flow_count": 12, "duplicate_flow_count": 1}),
        _run_result(True, http_metrics={"flow_count": 12, "duplicate_flow_count": 0}),
    )

    assert all(table.title != "HTTP Traffic" for table in without.metric_tables)
    assert any(table.title == "HTTP Traffic" for table in with_metrics.metric_tables)


def test_optional_result_keys_are_not_required():
    """A result dict carrying only counts and exit status still builds."""
    model = build_single_version_report_model(
        connector_image=TARGET_IMAGE,
        command="read",
        result={"success": True, "exit_code": 0},
    )

    assert model.sides[0].stdout_file is None
    assert model.sides[0].http_metrics is None
    assert "<!DOCTYPE html>" in render_html_report(model)


def test_stream_sections_are_capped_and_the_remainder_is_counted():
    """Beyond the cap, streams are dropped and both surfaces say how many."""
    counts = {f"stream_{index:04d}": index for index in range(MAX_STREAM_SECTIONS + 50)}
    model = _comparison(
        "read",
        _run_result(True, record_counts_per_stream=counts),
        _run_result(True, record_counts_per_stream=counts),
    )

    assert len(model.stream_sections) == MAX_STREAM_SECTIONS
    assert model.omitted_stream_count == 50
    # The HTML report is where the inline summary sends the reader, so a drop
    # there must be stated rather than silent.
    assert "50 more stream(s) omitted" in render_html_report(model)


def test_the_collapsed_stream_table_states_the_true_stream_count():
    """The header must not report the capped count it happens to have sections for."""
    counts = {f"stream_{index:04d}": index for index in range(MAX_STREAM_SECTIONS + 50)}
    summary = render_inline_summary(
        _comparison(
            "read",
            _run_result(True, record_counts_per_stream=counts),
            _run_result(True, record_counts_per_stream=counts),
        )
    )

    assert f"({MAX_STREAM_SECTIONS + 50} streams)" in summary


def test_diff_blocks_are_truncated_by_line_count_and_line_length():
    """Diff content is capped so a report stays openable."""
    block = build_diff_block(
        "huge",
        [DiffLine("ctx", "x" * (MAX_LINE_CHARS + 500))]
        * (MAX_DIFF_LINES_PER_BLOCK + 7),
    )

    assert len(block.lines) == MAX_DIFF_LINES_PER_BLOCK
    assert block.truncated_line_count == 7
    assert len(block.lines[0].text) == MAX_LINE_CHARS + 2


# --------------------------------------------------------------------------
# HTML rendering
# --------------------------------------------------------------------------


def _html_with_streams(status: str = "fail"):
    """Render HTML for a two-stream read, with a diff block on the `users` stream.

    Exercises the extension seam the comparison checks will use, so this test
    file also proves the template renders content nothing populates yet.
    """
    model = _comparison(
        "read",
        _run_result(True, record_counts_per_stream={"users": 88, "events": 200}),
        _run_result(True, record_counts_per_stream={"users": 100, "events": 200}),
    )
    diff_block = build_diff_block(
        "users record 1",
        [
            DiffLine("meta", "@@ record pk (1,) @@"),
            DiffLine("del", 'data.name: "a"'),
            DiffLine("add", 'data.name: "b"'),
            DiffLine("ctx", "data.id: 1"),
        ],
    )
    sections = tuple(
        replace(section, status=status, diff_blocks=(diff_block,))
        if section.stream == "users"
        else section
        for section in model.stream_sections
    )

    return render_html_report(replace(model, stream_sections=sections))


@pytest.mark.parametrize(
    "build_model",
    [
        pytest.param(
            lambda: _comparison("read", _run_result(True), _run_result(True)),
            id="comparison",
        ),
        pytest.param(
            lambda: build_single_version_report_model(
                connector_image=TARGET_IMAGE, command="spec", result=_run_result(True)
            ),
            id="single-version",
        ),
    ],
)
def test_html_is_a_complete_document(build_model):
    """Both modes render a full HTML document."""
    model = build_model()
    html = render_html_report(model)

    assert html.startswith("<!DOCTYPE html>")
    assert html.rstrip().endswith("</html>")
    assert model.verdict_label in html


def test_html_is_self_contained(monkeypatch):
    """No scripts and no network assets: the report is read from `file://`.

    Rendered with the GitHub environment set, because that is when the report
    grows links: a hyperlink to the run is fine, an asset that has to be fetched
    is not.
    """
    monkeypatch.setenv("GITHUB_SERVER_URL", "https://github.com")
    monkeypatch.setenv("GITHUB_REPOSITORY", "airbytehq/airbyte-ops-mcp")
    monkeypatch.setenv("GITHUB_RUN_ID", "1234")
    html = _html_with_streams()

    for tag in ("<script", "<link", "<img", "<iframe", "<object", "<embed"):
        assert tag not in html
    assert "cdn" not in html.lower()
    assert "@import" not in html
    # The run link is expected, and proves the assertion above is not vacuous.
    assert (
        'href="https://github.com/airbytehq/airbyte-ops-mcp/actions/runs/1234"' in html
    )


def test_html_supports_dark_mode():
    """The report follows the reader's OS theme."""
    assert "prefers-color-scheme: dark" in _html_with_streams()


def test_html_escapes_connector_supplied_strings():
    """Stream names and diff text are connector-controlled, so they are escaped.

    Guards the `select_autoescape` extension list: its default does not match
    `.html.j2`, which would leave this template unescaped.
    """
    model = _comparison(
        "read",
        _run_result(True, record_counts_per_stream={"<img src=x onerror=alert(1)>": 1}),
        _run_result(True, record_counts_per_stream={"<img src=x onerror=alert(1)>": 1}),
    )
    injected = replace(
        model.stream_sections[0],
        diff_blocks=(
            build_diff_block(
                "</pre><script>alert(1)</script>",
                [DiffLine("add", "</pre><script>alert(1)</script>")],
            ),
        ),
    )
    html = render_html_report(replace(model, stream_sections=(injected,)))

    assert "<script" not in html
    assert "<img src=x" not in html
    assert "&lt;img src=x onerror=alert(1)&gt;" in html


def test_html_renders_collapsible_stream_sections_and_diff_tokens():
    """Streams collapse natively, failures start expanded, diff lines are tokenized."""
    html = _html_with_streams()

    # Only the stream that has a body is a disclosure widget; `events` carries
    # nothing but its record count and renders as a plain row.
    assert html.count('<details class="stream') == 1
    assert '<details class="stream stream--fail" open>' in html
    assert '<summary><span class="mono">users</span>' in html
    assert 'stream--plain"><span class="mono">events</span>' in html
    for kind in ("meta", "del", "add", "ctx"):
        assert f'class="ln ln--{kind}"' in html


def test_a_stream_with_nothing_to_show_is_not_a_disclosure_widget():
    """A widget that expands to nothing is worse than no widget.

    Every stream in a report built today has exactly one metric row, which the
    headline already states, so none of them should be collapsible.
    """
    model = _comparison(
        "read",
        _run_result(True, record_counts_per_stream={"users": 88, "events": 200}),
        _run_result(True, record_counts_per_stream={"users": 100, "events": 200}),
    )
    html = render_html_report(model)

    assert '<details class="stream' not in html
    assert html.count('stream--plain"><span class="mono">') == 2
    assert "100 → 88 records (-12)" in html


def test_html_report_is_written_to_the_artifact_directory(tmp_path):
    """The report lands next to the run's other artifacts."""
    model = _comparison("spec", _run_result(True), _run_result(True))

    path = write_html_report(model, tmp_path)

    assert path == tmp_path / HTML_REPORT_FILENAME
    assert path.read_text().startswith("<!DOCTYPE html>")


# --------------------------------------------------------------------------
# Inline (step summary) rendering
# --------------------------------------------------------------------------


def test_inline_summary_is_concise_and_starts_at_an_l2_heading():
    """The workflow owns the H1 and context block, so the summary omits both."""
    summary = render_inline_summary(
        _comparison(
            "read",
            _run_result(
                True,
                record_counts_per_stream={"users": 88},
                stdout_file="/tmp/target/stdout.txt",
                http_metrics={"flow_count": 12, "duplicate_flow_count": 0},
            ),
            _run_result(
                True,
                record_counts_per_stream={"users": 100},
                stdout_file="/tmp/control/stdout.txt",
            ),
        )
    )

    assert summary.startswith("## `READ` Test Results")
    assert "\n# " not in summary
    assert "Test Date" not in summary
    assert "| Check | Result | Details |" in summary
    assert "| `users` | 100 | 88 | **-12** |" in summary
    assert "| **Total** | **100** | **88** | **-12** |" in summary
    assert HTML_REPORT_FILENAME in summary
    # Detail belongs to the HTML report, not to the step summary.
    assert "stdout.txt" not in summary
    assert "Flow Count" not in summary


def test_inline_summary_uses_a_count_column_in_single_version_mode():
    """There is no control to compare against, so no delta column."""
    summary = render_inline_summary(
        build_single_version_report_model(
            connector_image=TARGET_IMAGE,
            command="read",
            result=_run_result(True, record_counts_per_stream={"users": 100}),
        )
    )

    assert "| Stream | Count |" in summary
    assert "| `users` | 100 |" in summary
    assert "Delta" not in summary


def test_inline_summary_escapes_pipes_in_stream_names():
    """A stream name is connector-controlled and must not break the table."""
    summary = render_inline_summary(
        build_single_version_report_model(
            connector_image=TARGET_IMAGE,
            command="read",
            result=_run_result(True, record_counts_per_stream={"a|b": 1}),
        )
    )

    assert "| `a\\|b` | 1 |" in summary


def test_a_stream_name_cannot_inject_markdown_into_the_step_summary():
    """The step summary has no escaping to fall back on, unlike the HTML report.

    A newline in a connector-supplied stream name would end the table row and
    let everything after it render as top-level markdown -- including a forged
    verdict line on a run that actually failed.
    """
    forged = (
        "users\n\n**Result:** ✅ PASS — Both versions succeeded (no regression)\n\n"
        "[Download the fixed connector](https://evil.example/pwn)\n\n<!--"
    )
    summary = render_inline_summary(
        _comparison(
            "read",
            _run_result(False, record_counts_per_stream={forged: 1}),
            _run_result(True, record_counts_per_stream={forged: 1}),
        )
    )

    lines = summary.splitlines()

    # The payload may appear -- inert, inside its own cell -- but it must not
    # start a line, which is what would make it render as top-level markdown.
    assert [line for line in lines if line.startswith("**Result:**")] == [
        "**Result:** ❌ FAIL (regression) — Target failed (exit 1), "
        "control succeeded — regression detected"
    ]
    assert not [line for line in lines if line.startswith("[Download")]
    assert not [line for line in lines if line.startswith("<!--")]
    # Every table row stays a single row, so no cell is blanked.
    assert all(line.count("|") == 5 for line in lines if line.startswith("| `"))


def test_a_pathological_stream_name_cannot_blow_the_summary_size_limit():
    """`GITHUB_STEP_SUMMARY` is dropped whole past 1 MiB, verdict included."""
    counts = {f"{'x' * 60_000}-{index}": index for index in range(25)}
    summary = render_inline_summary(
        build_single_version_report_model(
            connector_image=TARGET_IMAGE,
            command="read",
            result=_run_result(True, record_counts_per_stream=counts),
        )
    )

    assert len(summary) < 100_000
    assert max(len(line) for line in summary.splitlines()) < MAX_LABEL_CHARS + 100


def test_a_check_summary_cannot_inject_markdown():
    """Check summaries will be built from connector-supplied names by P0.2."""
    summary = render_inline_summary(
        _comparison(
            "read",
            _run_result(True),
            _run_result(True),
            extra_checks=(
                CheckResult(
                    name="Record counts",
                    passed=False,
                    summary="a | b\n\n**Result:** ✅ PASS",
                ),
            ),
        )
    )

    lines = summary.splitlines()

    # Contained in its Details cell: it neither starts a line nor splits the row.
    assert len([line for line in lines if line.startswith("**Result:**")]) == 1
    assert "| Record counts | ❌ | a \\| b **Result:** ✅ PASS |" in summary


def test_inline_summary_collapses_a_long_stream_table():
    """Past the threshold the table is wrapped so the summary stays scannable."""
    counts = {
        f"stream_{index}": index
        for index in range(INLINE_STREAM_TABLE_COLLAPSE_THRESHOLD + 1)
    }
    summary = render_inline_summary(
        build_single_version_report_model(
            connector_image=TARGET_IMAGE,
            command="read",
            result=_run_result(True, record_counts_per_stream=counts),
        )
    )

    assert "<details><summary>Record counts per stream" in summary
    assert "</details>" in summary


def test_inline_summary_caps_stream_rows_and_keeps_the_largest_deltas():
    """The step summary is size-limited, so a wide read is truncated on purpose."""
    control = {f"stream_{index:03d}": 10 for index in range(300)}
    target = dict(control)
    target["stream_299"] = 0  # the only non-zero delta

    summary = render_inline_summary(
        _comparison(
            "read",
            _run_result(True, record_counts_per_stream=target),
            _run_result(True, record_counts_per_stream=control),
        )
    )
    data_rows = [
        line
        for line in summary.splitlines()
        if line.startswith("| `stream_") or line.startswith("| **Total**")
    ]

    assert len(data_rows) <= MAX_INLINE_STREAM_ROWS + 1
    assert "| `stream_299` | 10 | 0 | **-10** |" in summary
    assert "more stream(s) omitted" in summary


@pytest.mark.parametrize(
    "build_model",
    [
        pytest.param(
            lambda: _comparison("read", _run_result(True), _run_result(True)), id="pass"
        ),
        pytest.param(
            lambda: _comparison("read", _run_result(False), _run_result(True)),
            id="regression",
        ),
        pytest.param(
            lambda: _comparison("read", _run_result(False), _run_result(False)),
            id="both-failed",
        ),
        pytest.param(
            lambda: _comparison(
                "check",
                _run_result(True, connection_status="SUCCEEDED"),
                _run_result(True, connection_status="FAILED"),
            ),
            id="check-improvement",
        ),
        pytest.param(
            lambda: _comparison(
                "read",
                _run_result(True),
                _run_result(True),
                extra_checks=(
                    CheckResult(name="Record counts", passed=False, summary="differs"),
                    CheckResult(name="Schema", passed=False, severity="diagnostic"),
                ),
            ),
            id="checks-folded",
        ),
        pytest.param(
            lambda: build_single_version_report_model(
                connector_image=TARGET_IMAGE, command="check", result=_run_result(True)
            ),
            id="single-version",
        ),
    ],
)
def test_both_surfaces_state_the_same_verdict(build_model):
    """The HTML report and the step summary cannot disagree about a run."""
    model = build_model()
    html = render_html_report(model)
    summary = render_inline_summary(model)

    assert model.verdict_label in html
    assert model.verdict_label in summary

    glyphs = {"pass": "✅", "warn": "⚠️", "fail": "❌"}
    for check in model.checks:
        assert check.name in html
        assert check.name in summary
        assert f"status--{check.status}" in html
        assert f"| {check.name} | {glyphs[check.status]} |" in summary


# --------------------------------------------------------------------------
# Coverage: a configured stream that emitted nothing must still be visible
# --------------------------------------------------------------------------


def test_a_configured_stream_that_emitted_nothing_is_shown_as_zero():
    """Counts come from records, so this stream would otherwise be missing.

    A green PASS must not read the same whether the read covered every stream
    or only the ones that happened to return data.
    """
    model = _comparison(
        "read",
        _run_result(True, record_counts_per_stream={"users": 100}),
        _run_result(True, record_counts_per_stream={"users": 100}),
        configured_streams=("users", "shipments"),
    )
    summary = render_inline_summary(model)
    table = next(t for t in model.metric_tables if t.title == RECORD_COUNTS_TABLE)

    assert [section.stream for section in model.stream_sections] == [
        "shipments",
        "users",
    ]
    assert [row.label for row in table.rows] == ["shipments", "users"]
    assert "| `shipments` | 0 | 0 | 0 |" in summary
    assert "no records emitted" in render_html_report(model)
    # Filling the zero must not move the total.
    assert table.total.target == 100


def test_an_empty_stream_warns_without_failing_the_run():
    """It is worth seeing and it is not a regression of the version under test."""
    model = _comparison(
        "read",
        _run_result(True, record_counts_per_stream={"users": 100}),
        _run_result(True, record_counts_per_stream={"users": 100}),
        configured_streams=("users", "shipments"),
    )
    coverage = next(check for check in model.checks if check.name == "Stream coverage")

    assert model.passed is True
    assert coverage.status == "warn"
    assert "no records from shipments" in coverage.summary


def test_full_coverage_reports_a_passing_check():
    """The check is worth showing even when nothing is wrong: it states coverage."""
    model = _comparison(
        "read",
        _run_result(True, record_counts_per_stream={"users": 100}),
        _run_result(True, record_counts_per_stream={"users": 100}),
        configured_streams=("users",),
    )
    coverage = next(check for check in model.checks if check.name == "Stream coverage")

    assert coverage.passed is True
    # "on any version" only in a comparison, where a ✅ beside a failed target
    # would otherwise read as if the target were the one that emitted records.
    assert (
        coverage.summary == "1 of 1 configured stream(s) emitted records on any version"
    )


def test_coverage_wording_does_not_claim_the_target_emitted_records():
    """A ✅ next to a failed target must not read as target coverage."""
    comparison = _comparison(
        "read",
        _run_result(False, record_counts_per_stream={}),
        _run_result(True, record_counts_per_stream={"users": 100}),
        configured_streams=("users",),
    )
    single = build_single_version_report_model(
        connector_image=TARGET_IMAGE,
        command="read",
        result=_run_result(True, record_counts_per_stream={"users": 100}),
        configured_streams=("users",),
    )

    comparison_check = next(
        check for check in comparison.checks if check.name == "Stream coverage"
    )
    single_check = next(
        check for check in single.checks if check.name == "Stream coverage"
    )

    assert comparison_check.summary.endswith("emitted records on any version")
    # Nothing to disambiguate when there is only one version.
    assert single_check.summary.endswith("emitted records")


def test_coverage_counts_streams_past_the_display_cap():
    """The count must come from the records, not from the sections shown.

    Sections are capped for display; deriving coverage from them would report
    every stream past the cap as covered -- overstating coverage on exactly the
    wide catalogs where it is hardest to notice.
    """
    configured = tuple(
        f"stream_{index:04d}" for index in range(MAX_STREAM_SECTIONS + 50)
    )
    model = _comparison(
        "read",
        _run_result(True, record_counts_per_stream={}),
        _run_result(True, record_counts_per_stream={}),
        configured_streams=configured,
    )
    coverage = next(check for check in model.checks if check.name == "Stream coverage")

    assert coverage.summary.startswith("0 of 250 configured stream(s) emitted records")
    # The names are capped for readability, and say how many were left out.
    assert "and 240 more" in coverage.summary


def test_no_coverage_check_without_a_configured_catalog():
    """`spec` and `check` have no catalog; the report must not invent coverage."""
    model = _comparison("spec", _run_result(True), _run_result(True))

    assert [check.name for check in model.checks] == ["Command execution"]


# --------------------------------------------------------------------------
# Failure output and connection objects
# --------------------------------------------------------------------------


def test_a_failing_side_gets_its_output_tail_inlined(tmp_path):
    """A path into an artifact does not answer "why did the target crash"."""
    stderr = tmp_path / "stderr.txt"
    stderr.write_text(
        "\n".join([f"noise {index}" for index in range(500)] + ["RuntimeError: boom"])
    )
    model = _comparison(
        "read",
        _run_result(False, stderr_file=str(stderr)),
        _run_result(True),
    )
    block = model.diff_blocks[0]

    assert block.title == "Target stderr — last 60 line(s)"
    assert block.lines[-1].text == "RuntimeError: boom"
    assert len(block.lines) == 60
    assert "RuntimeError: boom" in render_html_report(model)


def test_the_output_tail_does_not_read_the_whole_file(tmp_path):
    """A failed `read` can leave a `stdout.txt` holding every record it emitted.

    Only the end of it is wanted, so only the end of it is read.
    """
    stderr = tmp_path / "stderr.txt"
    stderr.write_text("x" * 5_000_000 + "\nRuntimeError: boom\n")
    reads: list[int] = []
    real_open = Path.open

    def _counting_open(self, *args, **kwargs):
        handle = real_open(self, *args, **kwargs)
        real_read = handle.read

        def _read(*read_args):
            data = real_read(*read_args)
            reads.append(len(data))
            return data

        handle.read = _read
        return handle

    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(Path, "open", _counting_open)
        model = _comparison(
            "read", _run_result(False, stderr_file=str(stderr)), _run_result(True)
        )

    assert model.diff_blocks[0].lines[-1].text == "RuntimeError: boom"
    assert max(reads) <= MAX_OUTPUT_TAIL_BYTES


@pytest.mark.parametrize(
    "image,expected_name,expected_version",
    [
        pytest.param(
            "airbyte/source-faker:6.3.0", "airbyte/source-faker", "6.3.0", id="tagged"
        ),
        pytest.param(
            "localhost:5000/my-connector",
            "localhost:5000/my-connector",
            "unknown",
            id="registry-port-without-a-tag",
        ),
        pytest.param(
            "localhost:5000/my-connector:1.2.3",
            "localhost:5000/my-connector",
            "1.2.3",
            id="registry-port-with-a-tag",
        ),
        pytest.param("source-faker", "source-faker", "unknown", id="no-tag"),
    ],
)
def test_image_names_and_tags_are_split_at_the_right_colon(
    image, expected_name, expected_version
):
    """A colon before the last `/` is a registry port, not a tag delimiter."""
    model = build_single_version_report_model(
        connector_image=image, command="spec", result=_run_result(True)
    )

    assert model.context.connector_name == expected_name
    assert model.context.target_version == expected_version


def test_stdout_is_the_fallback_when_stderr_is_empty(tmp_path):
    """A connector that logs as Airbyte messages leaves stderr empty."""
    stderr, stdout = tmp_path / "stderr.txt", tmp_path / "stdout.txt"
    stderr.write_text("")
    stdout.write_text('{"type":"LOG","log":{"message":"died"}}')
    model = _comparison(
        "read",
        _run_result(False, stderr_file=str(stderr), stdout_file=str(stdout)),
        _run_result(True),
    )

    assert [block.title for block in model.diff_blocks] == [
        "Target stdout — last 1 line(s)"
    ]


def test_a_passing_run_inlines_no_output(tmp_path):
    """The tail is for diagnosing a failure, not a wall of logs on every run."""
    stderr = tmp_path / "stderr.txt"
    stderr.write_text("all good")
    model = _comparison(
        "read", _run_result(True, stderr_file=str(stderr)), _run_result(True)
    )

    assert model.diff_blocks == ()


def test_missing_output_files_are_skipped():
    """The report must render on a machine that never had those paths."""
    model = _comparison(
        "read",
        _run_result(False, stderr_file="/nonexistent/stderr.txt"),
        _run_result(True),
    )

    assert model.diff_blocks == ()
    assert render_html_report(model).startswith("<!DOCTYPE html>")


def test_connection_objects_render_as_pretty_printed_json():
    """ "Which catalog did this run with" should not need a second file."""
    model = _comparison(
        "read",
        _run_result(True),
        _run_result(True),
        connection_objects=(
            build_json_block(
                "Configured catalog (input)", '{"streams":[{"b":2,"a":1}]}'
            ),
        ),
    )
    html = render_html_report(model)

    assert "Connection objects" in html
    assert "Configured catalog (input)" in html
    # Pretty-printed and key-sorted, so two runs' catalogs can be eyeballed.
    # Quotes arrive escaped, which is the autoescaping doing its job.
    assert "&#34;a&#34;: 1" in html
    assert html.index("&#34;a&#34;") < html.index("&#34;b&#34;")


def test_a_malformed_connection_object_is_shown_rather_than_swallowed():
    """A broken file is itself the answer to why a run behaved oddly."""
    block = build_json_block("Configured catalog (input)", "{not json")

    assert [line.text for line in block.lines] == ["{not json"]


# --------------------------------------------------------------------------
# Consolidation: one page per run, folded from the per-command reports
# --------------------------------------------------------------------------


def _write_command_reports(directory, commands=("spec", "check", "discover", "read")):
    """Write one per-command report per command, as a real run would."""
    for command in commands:
        target = _run_result(command != "read")
        model = _comparison(command, target, _run_result(True))
        (directory / command).mkdir(parents=True, exist_ok=True)
        write_html_report(model, directory / command)

    return [directory / command / HTML_REPORT_FILENAME for command in commands]


def test_a_run_is_consolidated_into_one_page(tmp_path):
    """Every command's report is inlined, in order, under a run-level verdict."""
    paths = _write_command_reports(tmp_path)

    html = consolidate_reports(paths)

    assert html.startswith("<!DOCTYPE html>")
    for command in ("spec", "check", "discover", "read"):
        assert f'id="command-{command}"' in html
        assert f'href="#command-{command}"' in html
    # One command failed, so the run failed.
    assert "verdict--fail" in html
    # The bodies are really inlined, not just linked.
    assert html.count("Command execution") == 4
    # The shared stylesheet appears once per document, not once per command.
    assert html.count("prefers-color-scheme: dark") == 1


def test_consolidated_element_ids_are_unique(tmp_path):
    """Inlining four documents must not produce four `id="checks"`.

    Duplicate ids are invalid HTML and make every in-page link resolve to the
    first command, which defeats the jump list the page is built around.
    """
    html = consolidate_reports(_write_command_reports(tmp_path))
    ids = re.findall(r'id="([^"]+)"', html)

    assert len(ids) == len(set(ids)), sorted(
        {value for value in ids if ids.count(value) > 1}
    )
    assert 'id="read-checks"' in html


def test_the_consolidated_page_puts_commands_side_by_side(tmp_path):
    """The one view a per-command report cannot give.

    A CLI process only ever sees one command, so the metric tables travel in the
    report's own header and are pivoted here.
    """
    for command, counts in (("discover", {"CATALOG": 1}), ("read", {"RECORD": 100})):
        (tmp_path / command).mkdir()
        write_html_report(
            _comparison(
                command,
                _run_result(True, message_counts=counts),
                _run_result(True, message_counts=counts),
            ),
            tmp_path / command,
        )

    html = consolidate_reports(
        [tmp_path / c / HTML_REPORT_FILENAME for c in ("discover", "read")]
    )

    assert "Metrics across commands" in html
    assert html.count('colspan="3"') == 2  # one column group per command
    # A metric a command does not report is blank, not zero: `discover` emits no
    # records, which is not the same as emitting none.
    assert "—" in html


def test_the_cross_command_view_survives_a_report_without_a_header(tmp_path):
    """A report from another version costs the matrix, not the page."""
    (tmp_path / "read").mkdir()
    path = tmp_path / "read" / HTML_REPORT_FILENAME
    write_html_report(
        _comparison("read", _run_result(True), _run_result(True)), tmp_path / "read"
    )
    # Strip the metric tables out of the header, as an older writer would.
    path.write_text(
        re.sub(r'"metric_tables":\[.*?\]', '"metric_tables":0', path.read_text())
    )

    html = consolidate_reports([path])

    assert html is not None
    assert "Metrics across commands" not in html
    assert 'id="command-read"' in html


def test_consolidation_is_self_contained(tmp_path):
    """Same constraint as the per-command report: opened from `file://`."""
    html = consolidate_reports(_write_command_reports(tmp_path))

    for tag in ("<script", "<link", "<img", "<iframe", "<object", "<embed"):
        assert tag not in html
    assert "@import" not in html


def test_consolidation_preserves_the_escaping_of_the_reports_it_inlines(tmp_path):
    """Bodies are inlined unescaped, so their own escaping must have held.

    This is the assertion that justifies `|safe` in the consolidated template:
    connector-supplied content was escaped when its report was rendered, and
    inlining must not resurrect it.
    """
    hostile = "<img src=x onerror=alert(1)>"
    model = _comparison(
        "read",
        _run_result(True, record_counts_per_stream={hostile: 1}),
        _run_result(True, record_counts_per_stream={hostile: 1}),
    )
    (tmp_path / "read").mkdir()
    write_html_report(model, tmp_path / "read")

    html = consolidate_reports([tmp_path / "read" / HTML_REPORT_FILENAME])

    assert "<img src=x" not in html
    assert "&lt;img src=x onerror=alert(1)&gt;" in html


def test_consolidation_skips_missing_and_unreadable_reports(tmp_path):
    """A crashed or cancelled command must not cost the reader the others."""
    paths = _write_command_reports(tmp_path, commands=("spec",))
    (tmp_path / "check").mkdir()
    truncated = tmp_path / "check" / HTML_REPORT_FILENAME
    truncated.write_text("<!DOCTYPE html>\n<html><body>upload cut short")
    # An upload cut mid-write can leave bytes that are not even valid UTF-8, so
    # the read has to fail as softly as the parse.
    (tmp_path / "discover").mkdir()
    binary = tmp_path / "discover" / HTML_REPORT_FILENAME
    binary.write_bytes(b"<!DOCTYPE html>\n\xff\xfe\x00truncated")

    html = consolidate_reports(
        [*paths, truncated, binary, tmp_path / "read" / "report.html"]
    )

    assert 'id="command-spec"' in html
    assert 'id="command-check"' not in html
    assert 'id="command-discover"' not in html
    assert "upload cut short" not in html


def test_consolidation_returns_none_when_nothing_is_readable(tmp_path):
    """Nothing to upload beats uploading an empty page."""
    assert consolidate_reports([tmp_path / "absent" / "report.html"]) is None


def test_a_hostile_verdict_string_cannot_escape_the_metadata_comment(tmp_path):
    """The metadata header is inserted unescaped, so it must be inert.

    A `-->` reaching the comment would end it early and dump the rest of the
    JSON into the page as markup.
    """
    model = _comparison(
        "read",
        _run_result(True),
        _run_result(True),
        extra_checks=(
            CheckResult(
                name="--> <script>alert(1)</script>",
                passed=False,
                # Findings name connector-derived streams and fields, and are
                # rendered as list items in the check table.
                details=("Stream <script>alert(2)</script> changed",),
            ),
        ),
    )
    (tmp_path / "read").mkdir()
    html = write_html_report(model, tmp_path / "read").read_text()

    meta_line = next(line for line in html.splitlines() if META_MARKER in line)
    assert meta_line.endswith("-->")
    assert meta_line.count("-->") == 1
    assert "<script" not in html
    # The header still round-trips into the consolidated page.
    part = extract_report_part(html)
    assert part is not None
    assert part.command == "read"
    assert part.passed is False


# --------------------------------------------------------------------------
# Artifact naming: the contract shared with the workflow's upload steps
# --------------------------------------------------------------------------


@pytest.mark.parametrize("command", ["spec", "check", "discover", "read"])
def test_artifact_name_includes_the_command_and_run_id(command, monkeypatch):
    """The name must match the workflow's `upload-artifact` names exactly."""
    monkeypatch.setenv("GITHUB_RUN_ID", "1234")

    assert github_artifact_name(command) == f"{ARTIFACT_NAME_PREFIX}-{command}-1234"


def test_artifact_name_omits_the_run_id_outside_github_actions(monkeypatch):
    """Locally there is no run, so the name stays meaningful without an id."""
    monkeypatch.delenv("GITHUB_RUN_ID", raising=False)

    assert github_artifact_name("read") == f"{ARTIFACT_NAME_PREFIX}-read"


# --------------------------------------------------------------------------
# Record comparison: the read-run checks folded into the verdict, and the
# per-stream detail blocks the HTML report renders for them
# --------------------------------------------------------------------------


def _msg(stream: str, data: dict) -> AirbyteMessage:
    return AirbyteMessage(
        type=AirbyteMessageType.RECORD,
        record=AirbyteRecordMessage(stream=stream, data=data, emitted_at=1),
    )


def _comparison_with_records(
    control: dict[str, list[dict]],
    target: dict[str, list[dict]],
    primary_keys: dict[str, list | None],
):
    """A read comparison model built from actual records, end to end.

    Runs the real comparison rather than hand-building a summary, so these
    tests exercise the same objects the CLI hands the report builder.
    """
    summary = run_record_comparisons(
        control_records={
            stream: [_msg(stream, data) for data in rows]
            for stream, rows in control.items()
        },
        target_records={
            stream: [_msg(stream, data) for data in rows]
            for stream, rows in target.items()
        },
        primary_keys_per_stream=primary_keys,
    )

    return _comparison(
        "read",
        _run_result(
            True,
            record_counts_per_stream={s: len(r) for s, r in target.items()},
        ),
        _run_result(
            True,
            record_counts_per_stream={s: len(r) for s, r in control.items()},
        ),
        record_comparison=summary,
    )


def _flat_blocks(section):
    """A section's diff blocks with their children, one flat iterable."""
    for block in section.diff_blocks:
        yield block
        yield from block.children


def test_a_passing_comparison_adds_passing_checks_and_green_streams():
    rows = [{"id": 1, "name": "a"}, {"id": 2, "name": "b"}]
    model = _comparison_with_records(
        {"users": rows}, {"users": rows}, {"users": [["id"]]}
    )

    assert model.passed is True
    check_names = [check.name for check in model.checks]
    assert "Record counts" in check_names
    assert "Primary key presence" in check_names
    assert "Primary key integrity (control)" in check_names
    assert "Primary key integrity (target)" in check_names
    assert "Field values" in check_names
    assert all(check.status == "pass" for check in model.checks)

    (section,) = model.stream_sections
    assert section.status == "pass"
    assert section.diff_blocks == ()


def test_a_dropped_record_fails_the_verdict_as_a_regression():
    """Both commands succeeded, so only the folded comparison can fail this."""
    model = _comparison_with_records(
        {"users": [{"id": 1}, {"id": 2}]},
        {"users": [{"id": 1}]},
        {"users": [["id"]]},
    )

    assert model.passed is False
    assert model.verdict_label == "FAIL (regression)"
    assert model.outcome is not None and model.outcome.success is True
    failed = {check.name for check in model.checks if check.status == "fail"}
    assert "Record counts" in failed
    assert "Primary key presence" in failed


def test_a_failing_check_summary_names_the_failing_streams():
    model = _comparison_with_records(
        {"users": [{"id": 1}, {"id": 2}]},
        {"users": [{"id": 1}]},
        {"users": [["id"]]},
    )

    presence = next(c for c in model.checks if c.name == "Primary key presence")
    assert "users" in presence.summary

    summary = render_inline_summary(model)
    assert "| Primary key presence | ❌" in summary


def test_a_missing_pk_renders_the_pk_list_and_the_dropped_records():
    model = _comparison_with_records(
        {"users": [{"id": 1, "name": "kept"}, {"id": 7, "name": "dropped"}]},
        {"users": [{"id": 1, "name": "kept"}]},
        {"users": [["id"]]},
    )

    (section,) = model.stream_sections
    assert section.status == "fail"
    assert "1 missing PK(s)" in section.headline
    titles = [block.title for block in _flat_blocks(section)]
    assert any(
        title.startswith("Missing primary keys — 1 in target") for title in titles
    )
    assert any(
        title.startswith("Missing in target — 1 PK value(s)") for title in titles
    )
    assert any(
        title.startswith("Records from control missing in target") for title in titles
    )

    html = render_html_report(model)
    # The missing PK value and the full dropped record are both on the page.
    assert "[7]" in html
    assert "dropped" in html


def test_a_mutated_field_renders_a_side_by_side_record_diff():
    model = _comparison_with_records(
        {"users": [{"id": 1, "name": "before"}]},
        {"users": [{"id": 1, "name": "after"}]},
        {"users": [["id"]]},
    )

    (section,) = model.stream_sections
    assert "1 record(s) with value diffs" in section.headline
    block = next(
        b for b in section.diff_blocks if b.title.startswith("Field value diffs")
    )
    assert "1 record(s) differ (showing 1)" in block.title
    assert not block.lines
    assert any("pk = [1]" in row.header for row in block.split_rows)
    # The changed field sits on ONE row: control on the left, target on the
    # right — that alignment is the point of the split layout.
    changed = next(
        row
        for row in block.split_rows
        if row.left is not None and "before" in row.left.text
    )
    assert changed.left is not None and changed.left.kind == "del"
    assert changed.right is not None and changed.right.kind == "add"
    assert "after" in changed.right.text
    # Unchanged lines sit on both sides of their row as context.
    assert any(
        row.left is not None
        and row.right is not None
        and row.left.kind == row.right.kind == "ctx"
        and row.left.text == row.right.text
        for row in block.split_rows
    )
    # The comparison excluded emitted_at, so the diff must not present it.
    assert not any(
        "emitted_at" in cell.text
        for row in block.split_rows
        for cell in (row.left, row.right)
        if cell is not None
    )


def test_a_long_unchanged_run_collapses_into_a_gap_divider():
    wide = {f"field_{i:02d}": i for i in range(30)}
    model = _comparison_with_records(
        {"users": [{"id": 1, **wide, "name": "before"}]},
        {"users": [{"id": 1, **wide, "name": "after"}]},
        {"users": [["id"]]},
    )

    (section,) = model.stream_sections
    block = next(
        b for b in section.diff_blocks if b.title.startswith("Field value diffs")
    )
    assert any("unchanged line(s)" in row.header for row in block.split_rows)


def test_duplicate_pks_are_listed_per_version():
    model = _comparison_with_records(
        {"users": [{"id": 1, "n": "a"}]},
        {"users": [{"id": 1, "n": "a"}, {"id": 1, "n": "a"}]},
        {"users": [["id"]]},
    )

    (section,) = model.stream_sections
    assert section.status == "fail"
    assert "1 duplicate PK(s) in target" in section.headline
    # One check-level block whose title summarizes the test, with one child
    # per version that actually has duplicates: no control child exists.
    group = next(
        b
        for b in section.diff_blocks
        if b.title == "Duplicate primary keys — 1 in target"
    )
    assert not group.split_rows
    (child,) = group.children
    assert child.title == "In target — 1 PK value(s)"
    assert [line.text for line in child.lines] == ["[1] \u00d72"]


def test_records_without_their_declared_pk_are_reported():
    model = _comparison_with_records(
        {"users": [{"id": 1, "n": "a"}, {"n": "no-pk-value"}]},
        {"users": [{"id": 1, "n": "a"}, {"n": "no-pk-value"}]},
        {"users": [["id"]]},
    )

    (section,) = model.stream_sections
    assert section.status == "fail"
    assert "record(s) without PK values in control" in section.headline
    assert "record(s) without PK values in target" in section.headline
    # One check-level block with one single-column child per version, each
    # showing that version's own offending records.
    group = next(
        b
        for b in section.diff_blocks
        if b.title
        == "Records with missing or null primary key values — 1 in control, 1 in target"
    )
    assert [child.title for child in group.children] == [
        "In control — 1 record(s)",
        "In target — 1 record(s)",
    ]
    for child in group.children:
        assert not child.split_rows
        assert any("no-pk-value" in line.text for line in child.lines)
        # Nothing was cut, so no truncation note.
        assert not any("truncated" in line.text for line in child.lines)


def test_missing_pk_value_records_beyond_the_cap_get_a_truncation_note():
    """The example copies are capped; the report must say so, not just stop."""
    bad_records = [{"n": f"no-pk-{i}"} for i in range(8)]
    model = _comparison_with_records(
        {"users": [{"id": 1, "n": "a"}, *bad_records]},
        {"users": [{"id": 1, "n": "a"}, *bad_records]},
        {"users": [["id"]]},
    )

    (section,) = model.stream_sections
    group = next(
        b
        for b in section.diff_blocks
        if b.title
        == "Records with missing or null primary key values — 8 in control, 8 in target"
    )
    for version, child in zip(("control", "target"), group.children):
        assert child.title == f"In {version} — 8 record(s)"
        meta = [line.text for line in child.lines if line.kind == "meta"]
        shown = sum(1 for t in meta if t.startswith("record "))
        assert shown == 5  # MAX_EXAMPLE_DIFFS at the comparison layer
        note = next(t for t in meta if "truncated" in t)
        assert f"3 more such record(s) in {version}" in note
        assert "run artifacts" in note


def test_a_stream_without_pk_is_count_only_and_says_so():
    model = _comparison_with_records(
        {"events": [{"a": 1}, {"a": 2}]},
        {"events": [{"a": 1}]},
        {"events": None},
    )

    (section,) = model.stream_sections
    assert section.status == "fail"
    assert "no primary key: count comparison only" in section.headline
    assert "1 fewer record(s) in target" in section.headline
    # No PK detail can exist without a PK.
    assert section.diff_blocks == ()


def test_a_stream_the_comparison_never_saw_stays_info():
    """A configured stream with no records on either side is coverage's job."""
    model = build_comparison_report_model(
        target_image=TARGET_IMAGE,
        control_image=CONTROL_IMAGE,
        command="read",
        target_result=_run_result(True, record_counts_per_stream={"users": 1}),
        control_result=_run_result(True, record_counts_per_stream={"users": 1}),
        record_comparison=run_record_comparisons(
            control_records={"users": [_msg("users", {"id": 1})]},
            target_records={"users": [_msg("users", {"id": 1})]},
            primary_keys_per_stream={"users": [["id"]]},
        ),
        configured_streams=("users", "silent"),
    )

    by_name = {section.stream: section for section in model.stream_sections}
    assert by_name["users"].status == "pass"
    assert by_name["silent"].status == "info"


def test_connector_controlled_pk_values_cannot_inject_html():
    hostile = "<script>alert(1)</script>"
    model = _comparison_with_records(
        {"users": [{"id": hostile, "n": "a"}, {"id": "2", "n": "b"}]},
        {"users": [{"id": "2", "n": "b"}]},
        {"users": [["id"]]},
    )

    html = render_html_report(model)
    assert "<script>alert(1)</script>" not in html
    assert "alert(1)" in html  # escaped, not swallowed


def test_check_summaries_cap_the_failing_stream_names():
    streams = {f"s{i:02d}": [{"id": 1}, {"id": 2}] for i in range(8)}
    model = _comparison_with_records(
        streams,
        {name: [{"id": 1}] for name in streams},
        {name: [["id"]] for name in streams},
    )

    counts = next(c for c in model.checks if c.name == "Record counts")
    assert "8 streams failed" in counts.summary
    assert "and 3 more" in counts.summary


def test_both_surfaces_state_the_comparison_verdict_identically():
    model = _comparison_with_records(
        {"users": [{"id": 1, "v": "x"}]},
        {"users": [{"id": 1, "v": "y"}]},
        {"users": [["id"]]},
    )

    html = render_html_report(model)
    summary = render_inline_summary(model)
    assert model.passed is False
    assert "FAIL (regression)" in html
    assert "FAIL (regression)" in summary
    assert "field values" in model.verdict_detail


def test_the_split_diff_renders_as_a_two_column_table():
    model = _comparison_with_records(
        {"users": [{"id": 1, "name": "before"}]},
        {"users": [{"id": 1, "name": "after"}]},
        {"users": [["id"]]},
    )

    html = render_html_report(model)
    assert '<table class="splitdiff">' in html
    assert "<th>Control</th>" in html
    assert "<th>Target</th>" in html
    assert 'class="cell--del"' in html
    assert 'class="cell--add"' in html


def test_dropped_records_render_as_a_single_column_list():
    """One-sided by construction: a split view here would carry a permanently
    empty target column, which reads as if there were something to compare."""
    model = _comparison_with_records(
        {"users": [{"id": 1, "n": "kept"}, {"id": 7, "n": "dropped"}]},
        {"users": [{"id": 1, "n": "kept"}]},
        {"users": [["id"]]},
    )

    (section,) = model.stream_sections
    block = next(
        b
        for b in section.diff_blocks
        if b.title.startswith("Records from control missing in target")
    )
    assert not block.split_rows
    assert "showing 1 of 1" in block.title
    # Each record opens with its pinned PK fields, like the value diffs.
    texts = [line.text for line in block.lines]
    assert "pk id = 7" in texts
    assert any("dropped" in t for t in texts)


def test_split_diff_blocks_truncate_rows_and_cells_like_line_blocks():
    rows = [
        SplitDiffRow(
            left=DiffLine(kind="del", text="x" * (MAX_LINE_CHARS + 50)),
            right=DiffLine(kind="add", text="y"),
        )
        for _ in range(MAX_DIFF_LINES_PER_BLOCK + 7)
    ]

    block = build_split_diff_block("Example", rows)

    assert len(block.split_rows) == MAX_DIFF_LINES_PER_BLOCK
    assert block.truncated_line_count == 7
    first_left = block.split_rows[0].left
    assert first_left is not None
    assert len(first_left.text) == MAX_LINE_CHARS + len(" …")
    html_block = render_html_report(
        replace(
            _comparison_with_records(
                {"users": [{"id": 1}]}, {"users": [{"id": 1}]}, {"users": [["id"]]}
            ),
            diff_blocks=(block,),
        )
    )
    assert "more row(s) omitted" in html_block


def test_the_raw_deepdiff_payload_is_on_the_page_next_to_the_visual_diff():
    """The same payload the JSON output carries, but untruncated."""
    model = _comparison_with_records(
        {"users": [{"id": 1, "name": "before"}]},
        {"users": [{"id": 1, "name": "after"}]},
        {"users": [["id"]]},
    )

    (section,) = model.stream_sections
    block = next(b for b in section.diff_blocks if "raw DeepDiff payload" in b.title)
    assert block.language == "json"
    assert any("pk = [1]" in line.text for line in block.lines if line.kind == "meta")
    payload = "\n".join(line.text for line in block.lines)
    assert "values_changed" in payload
    assert "before" in payload
    assert "after" in payload

    html = render_html_report(model)
    assert "values_changed" in html


def test_the_raw_deepdiff_payload_is_not_clipped_at_the_generic_limit():
    """A huge field value is one JSON line; the generic 2k clip must not cut
    it (the block has its own far-larger bound, MAX_DEEPDIFF_LINE_CHARS)."""
    model = _comparison_with_records(
        {"users": [{"id": 1, "blob": "x" * (MAX_LINE_CHARS + 500)}]},
        {"users": [{"id": 1, "blob": "y" * (MAX_LINE_CHARS + 500)}]},
        {"users": [["id"]]},
    )

    (section,) = model.stream_sections
    block = next(b for b in section.diff_blocks if "raw DeepDiff payload" in b.title)
    assert any("y" * (MAX_LINE_CHARS + 500) in line.text for line in block.lines), (
        "the full new value must survive into the block"
    )


def test_value_diff_examples_pin_the_pk_fields_above_the_diff():
    """On a wide record the PK field can fall past the row cap or inside a
    collapsed gap; the pinned row keeps the record identifiable regardless."""
    model = _comparison_with_records(
        {"users": [{"id": 132, "name": "before"}]},
        {"users": [{"id": 132, "name": "after"}]},
        {"users": [["id"]]},
    )

    (section,) = model.stream_sections
    block = next(
        b for b in section.diff_blocks if b.title.startswith("Field value diffs")
    )
    divider = next(
        i for i, row in enumerate(block.split_rows) if "pk = [132]" in row.header
    )
    pinned = block.split_rows[divider + 1]
    assert pinned.left is not None and pinned.left.text == "pk id = 132"
    assert pinned.right is not None and pinned.right.text == "pk id = 132"


def test_missing_pk_records_name_the_missing_fields():
    model = _comparison_with_records(
        {"users": [{"id": 1, "n": "a"}]},
        {"users": [{"id": 1, "n": "a"}, {"n": "absent"}, {"id": None, "n": "null"}]},
        {"users": [["id"]]},
    )

    (section,) = model.stream_sections
    group = next(
        b
        for b in section.diff_blocks
        if b.title == "Records with missing or null primary key values — 2 in target"
    )
    # Control emitted none, so the group has a target child only.
    (child,) = group.children
    assert child.title == "In target — 2 record(s)"
    texts = [line.text for line in child.lines]
    # An absent field and a null field are different bugs; say which it is.
    assert "pk id = <field missing>" in texts
    assert "pk id = null" in texts


def test_composite_pk_fields_are_each_pinned():
    model = _comparison_with_records(
        {"orders": [{"location": {"id": 7}, "date": "2026-01-01", "v": "x"}]},
        {"orders": [{"location": {"id": 7}, "date": "2026-01-01", "v": "y"}]},
        {"orders": [["location", "id"], ["date"]]},
    )

    (section,) = model.stream_sections
    block = next(
        b for b in section.diff_blocks if b.title.startswith("Field value diffs")
    )
    texts = [row.left.text for row in block.split_rows if row.left is not None]
    assert "pk location.id = 7" in texts
    assert 'pk date = "2026-01-01"' in texts


def test_extra_target_pks_are_listed_as_context_when_presence_fails():
    """PKs only in target don't fail (directional), but when the presence
    check already failed, the other direction is listed for context."""
    model = _comparison_with_records(
        {"users": [{"id": 1, "n": "a"}, {"id": 2, "n": "b"}]},
        {"users": [{"id": 2, "n": "b"}, {"id": 3, "n": "new"}]},
        {"users": [["id"]]},
    )

    (section,) = model.stream_sections
    group = next(
        b
        for b in section.diff_blocks
        if b.title == "Missing primary keys — 1 in target, 1 in control"
    )
    missing, extra = group.children
    assert missing.title.startswith("Missing in target — 1 PK value(s)")
    assert "(present in control, not in target)" in missing.title
    assert any(line.kind == "del" and line.text == "[1]" for line in missing.lines)
    assert extra.title.startswith("Missing in control — 1 PK value(s)")
    assert "(present in target, not in control)" in extra.title
    assert any(line.kind == "add" and line.text == "[3]" for line in extra.lines)
    assert "NOT fail" in extra.lines[0].text


def test_deepdiff_set_containers_render_as_arrays_not_one_line_strings():
    """`dictionary_item_added/_removed` are DeepDiff's own set classes; they
    must pretty-print as JSON arrays with one path per line, not collapse
    into a single stringified line."""
    model = _comparison_with_records(
        {"users": [{"id": 1, "old_field": "x", "kept": "same"}]},
        {"users": [{"id": 1, "new_field": "y", "kept": "same"}]},
        {"users": [["id"]]},
    )

    (section,) = model.stream_sections
    block = next(b for b in section.diff_blocks if "raw DeepDiff payload" in b.title)
    texts = [line.text for line in block.lines]
    # One path per line inside a JSON array...
    assert any(t.strip() == "\"root['data']['new_field']\"" for t in texts)
    assert any(t.strip() == "\"root['data']['old_field']\"" for t in texts)
    # ...never the whole container collapsed into one quoted string.
    assert not any("[root[" in t for t in texts)


def test_an_errored_comparison_fails_the_verdict_with_its_message():
    """The CLI degrades an unexpected comparison error to a FAILED summary
    with no per-stream results; the check row must carry the message alone,
    not claim "0 streams failed"."""
    errored = RecordComparisonSummary(
        passed=False,
        count_comparison=ComparisonResult(
            passed=False, message="Record comparison errored"
        ),
        errors=["Record comparison errored: OSError('Too many open files')"],
    )
    model = _comparison(
        "read",
        _run_result(True),
        _run_result(True),
        record_comparison=errored,
    )

    assert model.passed is False
    assert model.verdict_label == "FAIL (regression)"
    counts_check = next(c for c in model.checks if c.name == "Record counts")
    assert counts_check.status == "fail"
    assert counts_check.summary == "Record comparison errored"
    assert "stream" not in counts_check.summary

    html = render_html_report(model)
    assert "FAIL (regression)" in html
    assert "Record comparison errored" in html


def test_the_run_check_row_never_claims_no_regression():
    """The command-execution row states facts about the commands; the
    "(no regression)" claim belongs to the folded verdict and must appear
    only when every comparison check passed."""
    failing = _comparison(
        "read",
        _run_result(True),
        _run_result(True),
        extra_checks=(
            CheckResult(name="Record counts", passed=False, summary="51 fewer"),
        ),
    )
    run_check = next(c for c in failing.checks if c.name == "Command execution")
    assert run_check.summary == "Both versions succeeded"
    assert "(no regression)" not in failing.verdict_detail

    passing = _comparison("read", _run_result(True), _run_result(True))
    assert passing.verdict_detail == "Both versions succeeded (no regression)"


def test_failing_streams_are_never_pushed_past_the_section_cap(monkeypatch):
    """Sections sort failing streams first: detail blocks attach per section,
    so a failing stream past the cap would lose its detail entirely behind
    alphabetically-earlier passing streams."""
    monkeypatch.setattr(
        "airbyte_ops_mcp.regression_tests.report.MAX_STREAM_SECTIONS", 2
    )
    rows = [{"id": 1, "n": "a"}, {"id": 2, "n": "b"}]
    model = _comparison_with_records(
        {"aaa": rows, "bbb": rows, "zzz": rows},
        {"aaa": rows, "bbb": rows, "zzz": rows[:1]},
        {"aaa": [["id"]], "bbb": [["id"]], "zzz": [["id"]]},
    )

    sections = model.stream_sections
    assert len(sections) == 2
    assert model.omitted_stream_count == 1
    # The failing stream leads despite sorting last alphabetically.
    assert sections[0].stream == "zzz"
    assert sections[0].status == "fail"
    assert sections[0].diff_blocks


def test_an_errored_comparison_reports_fail_inconclusive():
    """A comparator crash is a tooling failure: the banner must not claim a
    regression the way a real comparison failure does."""
    from airbyte_ops_mcp.regression_tests.regression import (
        ComparisonResult,
        RecordComparisonSummary,
    )

    errored = RecordComparisonSummary(
        passed=False,
        errored=True,
        count_comparison=ComparisonResult(
            passed=False, message="Record comparison errored"
        ),
        errors=["Record comparison errored: OSError('boom')"],
    )
    model = _comparison(
        "read",
        _run_result(True),
        _run_result(True),
        record_comparison=errored,
    )

    assert model.passed is False
    assert model.verdict_label == "FAIL (inconclusive)"
    assert "FAIL (inconclusive)" in render_inline_summary(model)
