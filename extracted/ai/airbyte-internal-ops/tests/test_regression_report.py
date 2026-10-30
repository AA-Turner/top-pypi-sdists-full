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
    generate_action_test_comparison_report,
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
    build_record_comparison_checks,
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


def test_a_list_valued_http_metric_is_rendered_as_a_list_not_a_repr():
    """`live_urls` is a list of dicts, and Execution details renders every key.

    The blanket loop over `http_metrics` predates any list-valued key, so the
    page showed a Python repr -- `[{'url': ..., 'count': 8}]` -- where a reader
    expects the URLs.
    """
    model = _comparison(
        "read",
        _run_result(
            True,
            http_metrics={
                "flow_count": 12,
                "live_urls": [
                    {"url": "https://api.example.com/report/9001", "count": 8}
                ],
            },
        ),
        _run_result(True, http_metrics={"flow_count": 12}),
    )

    html = render_html_report(model)

    assert "<li>url https://api.example.com/report/9001 · count 8</li>" in html
    assert "&#39;url&#39;" not in html


def test_a_mapping_valued_http_metric_keeps_its_values():
    """Jinja's `sequence` test is true for a dict, and iterating one drops values.

    No `http_metrics` key is a mapping today, but a mapping is the other shape
    that would otherwise render as a Python repr -- and taking the list branch
    renders its keys alone, which is worse than the repr.
    """
    model = _comparison(
        "read",
        _run_result(
            True,
            http_metrics={"per_host_flow_count": {"api.example.com": 8, "cdn": 2}},
        ),
        _run_result(True, http_metrics={"flow_count": 10}),
    )

    html = render_html_report(model)

    assert "<li>api.example.com 8</li>" in html
    assert "<li>cdn 2</li>" in html


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
    # Detail belongs to the HTML report, not to the step summary: the request
    # totals are the one line of the HTTP table the summary carries.
    assert "stdout.txt" not in summary
    assert "Repeated URLs" not in summary
    assert (
        "**HTTP requests:** control not captured · target 12 (0 to a repeated URL)"
        in summary
    )


def test_the_inline_summary_carries_per_version_request_totals():
    """Numbers only, never a verdict.

    A request count that moved between versions is what tells a reviewer
    whether a record difference came with a change in how the connector called
    the API; no threshold turns it into a pass or a fail, so it is a line rather
    than a row of the check table.
    """
    summary = render_inline_summary(
        _comparison(
            "read",
            _run_result(
                True,
                record_counts_per_stream={"users": 5},
                http_metrics={"flow_count": 118, "duplicate_flow_count": 7},
            ),
            _run_result(
                True,
                record_counts_per_stream={"users": 5},
                http_metrics={"flow_count": 120, "duplicate_flow_count": 8},
            ),
        )
    )

    assert (
        "**HTTP requests:** control 120 (8 to a repeated URL) "
        "· target 118 (7 to a repeated URL)" in summary
    )
    # It sits between the check table and the stream table, so it reads as
    # context for both rather than as a check of its own.
    assert summary.index("| Check |") < summary.index("**HTTP requests:**")
    assert summary.index("**HTTP requests:**") < summary.index("| Stream |")


@pytest.mark.parametrize(
    ("target_http", "control_http"),
    [
        pytest.param(None, None, id="no-capture"),
        pytest.param(
            {"flow_count": 0, "duplicate_flow_count": 0},
            {"flow_count": 0, "duplicate_flow_count": 0},
            id="no-traffic",
        ),
        pytest.param(
            {"replay_skipped_reason": "mitmproxy is unavailable"},
            None,
            id="proxy-never-ran",
        ),
    ],
)
def test_the_request_line_is_omitted_when_nothing_was_recorded(
    target_http, control_http
):
    """`spec` never calls out; a line of zeroes on every command is noise."""
    summary = render_inline_summary(
        _comparison(
            "spec",
            _run_result(True, http_metrics=target_http),
            _run_result(True, http_metrics=control_http),
        )
    )

    assert "HTTP requests" not in summary


def test_a_single_version_summary_has_no_request_line():
    """There is no proxy in single-version mode, and nothing to compare against."""
    summary = render_inline_summary(
        build_single_version_report_model(
            connector_image=TARGET_IMAGE,
            command="read",
            result=_run_result(
                True, http_metrics={"flow_count": 12, "duplicate_flow_count": 0}
            ),
        )
    )

    assert "HTTP requests" not in summary


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


def test_an_artifact_name_override_wins(monkeypatch):
    """`sandbox-case-run.yml` uploads one artifact under a name its caller picks."""
    monkeypatch.setenv("GITHUB_RUN_ID", "1234")
    monkeypatch.setenv("REGRESSION_TEST_ARTIFACT_NAME", "sandbox-case-result-1")

    assert github_artifact_name("read") == "sandbox-case-result-1"


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

    assert model.passed is False
    target_check = next(
        c for c in model.checks if c.name == "Primary key integrity (target)"
    )
    assert target_check.status == "fail"
    (section,) = model.stream_sections
    assert section.status == "fail"
    assert "1 new duplicate PK(s) in target" in section.headline
    # One check-level block whose title summarizes the test, with one child
    # per version that actually has duplicates: no control child exists.
    group = next(
        b
        for b in section.diff_blocks
        if b.title == "Duplicate primary keys — 1 in target (1 new in target)"
    )
    assert not group.split_rows
    (child,) = group.children
    assert child.title == "In target — 1 PK value(s)"
    assert [(line.kind, line.text) for line in child.lines] == [
        ("del", "[1] \u00d72 (new in target)")
    ]


def test_pre_existing_duplicate_pks_warn_without_failing_the_run():
    """Duplicates both versions emit are a finding about the connector, not
    about the change under test: every surface shows them as a warning."""
    rows = [{"id": 1, "n": "a"}, {"id": 1, "n": "a"}, {"id": 2, "n": "b"}]
    model = _comparison_with_records(
        {"users": rows}, {"users": rows}, {"users": [["id"]]}
    )

    assert model.passed is True
    assert model.verdict_label == "PASS"
    statuses = {check.name: check.status for check in model.checks}
    assert statuses["Primary key integrity (control)"] == "warn"
    assert statuses["Primary key integrity (target)"] == "warn"
    assert statuses["Record counts"] == "pass"
    control_check = next(
        c for c in model.checks if c.name == "Primary key integrity (control)"
    )
    assert control_check.summary == (
        "Pre-existing duplicate primary keys in control (not a regression) — "
        "1 stream: users"
    )
    assert control_check.details == (
        "Stream users has 1 pre-existing duplicate primary key value(s), "
        "unchanged between control and target",
    )

    (section,) = model.stream_sections
    assert section.status == "warn"
    assert section.headline.endswith("— 1 pre-existing duplicate PK(s), unchanged")
    group = next(
        b
        for b in section.diff_blocks
        if b.title
        == "Duplicate primary keys — 1 in control, 1 in target (1 pre-existing)"
    )
    assert [child.title for child in group.children] == [
        "In control — 1 PK value(s)",
        "In target — 1 PK value(s)",
    ]
    for child in group.children:
        assert [(line.kind, line.text) for line in child.lines] == [
            ("ctx", "[1] \u00d72 (pre-existing)")
        ]

    summary = render_inline_summary(model)
    assert "| Primary key integrity (control) | ⚠️" in summary
    assert "| Primary key integrity (target) | ⚠️" in summary
    assert "✅ PASS" in summary
    html = render_html_report(model)
    assert 'class="stream stream--warn"' in html


def test_a_duplicate_with_lost_records_is_not_called_fixed_on_any_surface():
    """Control `7: hold, release` + `1`, target `7: hold` + `1` + `2`."""
    model = _comparison_with_records(
        {
            "users": [
                {"id": 7, "event": "T1110"},
                {"id": 7, "event": "T1111"},
                {"id": 1},
            ]
        },
        {"users": [{"id": 7, "event": "T1110"}, {"id": 1}, {"id": 2}]},
        {"users": [["id"]]},
    )

    assert model.passed is False
    statuses = {check.name: check.status for check in model.checks}
    assert statuses["Primary key integrity (control)"] == "warn"
    assert statuses["Field values"] == "fail"
    control_check = next(
        c for c in model.checks if c.name == "Primary key integrity (control)"
    )
    assert control_check.summary.startswith(
        "Duplicate primary keys in control with records the target dropped or changed"
    )

    (section,) = model.stream_sections
    assert section.status == "fail"
    assert "1 duplicate PK(s) in control with records dropped or changed in target" in (
        section.headline
    )
    assert "fixed in target" not in section.headline
    group = next(
        b for b in section.diff_blocks if b.title.startswith("Duplicate primary keys")
    )
    assert group.title == (
        "Duplicate primary keys — 1 in control (1 with records dropped or changed "
        "in target)"
    )
    (child,) = group.children
    assert [(line.kind, line.text) for line in child.lines] == [
        ("del", "[7] \u00d72 (records dropped or changed in target)")
    ]
    summary = render_inline_summary(model)
    assert "| Primary key integrity (control) | ⚠️ |" in summary
    assert "| Field values | ❌ |" in summary


def test_a_control_value_is_called_fixed_only_while_the_lost_list_is_complete():
    """The dropped-or-changed list is capped; past the cap a value missing
    from it may still belong there, so it is not labelled fixed."""
    from airbyte_ops_mcp.regression_tests.regression.comparators import (
        StreamComparisonResult,
    )
    from airbyte_ops_mcp.regression_tests.report import _duplicate_pk_block

    def control_lines(lost_count: int) -> list[str]:
        result = StreamComparisonResult(
            stream_name="users",
            passed=True,
            duplicate_pks=[(1,), (2,), (3,)],
            duplicate_pk_counts={(1,): 2, (2,): 2, (3,): 2},
            fixed_duplicate_pk_count=3 - lost_count,
            lost_duplicate_pk_count=lost_count,
            lost_duplicate_pks=[(2,)],
        )
        block = _duplicate_pk_block("control", result, None)
        return [line.text for line in block.lines]

    assert control_lines(1) == [
        "[1] \u00d72 (fixed in target)",
        "[2] \u00d72 (records dropped or changed in target)",
        "[3] \u00d72 (fixed in target)",
    ]
    # Two values dropped or changed, one listed: 1 and 3 cannot be told apart.
    assert control_lines(2) == [
        "[1] \u00d72 (not duplicated in target)",
        "[2] \u00d72 (records dropped or changed in target)",
        "[3] \u00d72 (not duplicated in target)",
    ]


def test_one_added_copy_reads_in_the_singular():
    a, b = {"id": 7, "c": "A"}, {"id": 7, "c": "B"}
    model = _comparison_with_records(
        {"users": [a, a, b]}, {"users": [a, b, b]}, {"users": [["id"]]}
    )

    assert model.passed is True
    (section,) = model.stream_sections
    assert "1 more identical copy in target under 1 duplicated PK(s)" in (
        section.headline
    )


def test_duplicate_pks_the_target_fixed_warn_on_the_control_row():
    model = _comparison_with_records(
        {"users": [{"id": 1, "n": "a"}, {"id": 1, "n": "a"}, {"id": 2, "n": "b"}]},
        {"users": [{"id": 1, "n": "a"}, {"id": 2, "n": "b"}, {"id": 3, "n": "c"}]},
        {"users": [["id"]]},
    )

    assert model.passed is True
    statuses = {check.name: check.status for check in model.checks}
    assert statuses["Primary key integrity (control)"] == "warn"
    assert statuses["Primary key integrity (target)"] == "pass"
    control_check = next(
        c for c in model.checks if c.name == "Primary key integrity (control)"
    )
    assert control_check.summary == (
        "Duplicate primary keys in control fixed in target (not a regression) — "
        "1 stream: users"
    )

    (section,) = model.stream_sections
    assert section.status == "warn"
    assert "1 duplicate PK(s) in control fixed in target" in section.headline
    group = next(
        b
        for b in section.diff_blocks
        if b.title == "Duplicate primary keys — 1 in control (1 fixed in target)"
    )
    (child,) = group.children
    assert [(line.kind, line.text) for line in child.lines] == [
        ("del", "[1] \u00d72 (fixed in target)")
    ]


def test_dropped_duplicate_rows_warn_on_the_record_counts_row():
    """A target that stops emitting a duplicated PK's extra copies has fewer
    records; the count allows for them and every surface shows a warning."""
    model = _comparison_with_records(
        {"users": [{"id": 1, "n": "a"}] * 3 + [{"id": 2, "n": "b"}]},
        {"users": [{"id": 1, "n": "a"}, {"id": 2, "n": "b"}]},
        {"users": [["id"]]},
    )

    assert model.passed is True
    assert model.verdict_label == "PASS"
    statuses = {check.name: check.status for check in model.checks}
    assert statuses["Record counts"] == "warn"
    assert statuses["Primary key integrity (control)"] == "warn"
    assert statuses["Field values"] == "pass"
    counts_check = next(c for c in model.checks if c.name == "Record counts")
    assert counts_check.summary == (
        "Record counts match once duplicate rows are left out — 1 stream: users"
    )
    assert counts_check.details == (
        "Stream users has 2 fewer records in target, within the duplicate rows "
        "the target dropped (2 in control, 0 in target); field values check that "
        "the dropped rows were copies",
    )

    (section,) = model.stream_sections
    assert section.status == "warn"
    assert (
        "2 fewer record(s) in target, within the duplicate rows it dropped"
        in section.headline
    )

    summary = render_inline_summary(model)
    assert "| Record counts | ⚠️ |" in summary
    assert "within the duplicate rows the target dropped" in summary
    assert 'class="stream stream--warn"' in render_html_report(model)


def test_a_count_shortfall_that_is_not_duplicate_rows_still_fails():
    model = _comparison_with_records(
        {"users": [{"id": 1, "n": "a"}] * 2 + [{"id": 2, "n": "b"}]},
        {"users": [{"id": 1, "n": "a"}]},
        {"users": [["id"]]},
    )

    assert model.passed is False
    statuses = {check.name: check.status for check in model.checks}
    assert statuses["Record counts"] == "fail"
    (section,) = model.stream_sections
    assert section.status == "fail"
    assert "2 fewer record(s) in target" in section.headline
    assert "within the duplicate rows" not in section.headline


def test_a_lost_record_warns_on_the_count_and_fails_on_the_field_values():
    """3 distinct rows to 2: the shortfall is within the duplicate rows dropped,
    so the count only warns, and the field values fail on the lost row."""
    model = _comparison_with_records(
        {"users": [{"id": 7, "c": "a"}, {"id": 7, "c": "b"}, {"id": 7, "c": "c"}]},
        {"users": [{"id": 7, "c": "a"}, {"id": 7, "c": "b"}]},
        {"users": [["id"]]},
    )

    assert model.passed is False
    statuses = {check.name: check.status for check in model.checks}
    assert statuses["Record counts"] == "warn"
    assert statuses["Field values"] == "fail"
    (section,) = model.stream_sections
    assert section.status == "fail"
    assert (
        "1 fewer record(s) in target, within the duplicate rows it dropped"
        in section.headline
    )
    summary = render_inline_summary(model)
    assert "| Record counts | ⚠️ |" in summary
    assert "| Field values | ❌ |" in summary


def test_a_new_duplicate_pk_next_to_pre_existing_ones_fails_the_run():
    model = _comparison_with_records(
        {"users": [{"id": 1}, {"id": 1}, {"id": 2}]},
        {"users": [{"id": 1}, {"id": 1}, {"id": 2}, {"id": 2}]},
        {"users": [["id"]]},
    )

    assert model.passed is False
    assert model.verdict_label == "FAIL (regression)"
    statuses = {check.name: check.status for check in model.checks}
    assert statuses["Primary key integrity (control)"] == "warn"
    assert statuses["Primary key integrity (target)"] == "fail"
    target_check = next(
        c for c in model.checks if c.name == "Primary key integrity (target)"
    )
    assert target_check.details == (
        "Stream users has 1 new duplicate primary key value(s) in target (not "
        "duplicated in control); Stream users has 1 pre-existing duplicate "
        "primary key value(s), unchanged between control and target",
    )
    summary = render_inline_summary(model)
    assert "- Stream users has 1 new duplicate primary key value(s) in target" in (
        summary
    )

    (section,) = model.stream_sections
    assert section.status == "fail"
    assert (
        "1 new duplicate PK(s) in target; 1 pre-existing duplicate PK(s), unchanged"
        in (section.headline)
    )
    group = next(
        b for b in section.diff_blocks if b.title.startswith("Duplicate primary keys")
    )
    assert group.title == (
        "Duplicate primary keys — 1 in control, 2 in target (1 pre-existing, 1 new in target)"
    )
    target_child = next(c for c in group.children if c.title.startswith("In target"))
    assert [(line.kind, line.text) for line in target_child.lines] == [
        ("ctx", "[1] \u00d72 (pre-existing)"),
        ("del", "[2] \u00d72 (new in target)"),
    ]


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


def test_a_differing_duplicate_pk_group_renders_both_sides_unmatched_records():
    """A PK emitted twice carries lists of records in its example; the block
    still pins the PK and diffs the two sides."""
    model = _comparison_with_records(
        {
            "users": [
                {"id": 7, "code": "T1110", "amount": 5},
                {"id": 7, "code": "T1111", "amount": 5},
            ]
        },
        {
            "users": [
                {"id": 7, "code": "T1111", "amount": 5},
                {"id": 7, "code": "T1110", "amount": 500},
            ]
        },
        {"users": [["id"]]},
    )

    assert model.passed is False
    (section,) = model.stream_sections
    assert section.status == "fail"
    assert "1 record(s) with value diffs" in section.headline
    block = next(
        b for b in section.diff_blocks if b.title.startswith("Field value diffs")
    )
    divider = next(
        i for i, row in enumerate(block.split_rows) if "pk = [7]" in row.header
    )
    pinned = block.split_rows[divider + 1]
    assert pinned.left is not None and pinned.left.text == "pk id = 7"
    assert pinned.right is not None and pinned.right.text == "pk id = 7"
    left_text = " ".join(row.left.text for row in block.split_rows if row.left)
    right_text = " ".join(row.right.text for row in block.split_rows if row.right)
    assert '"amount": 5' in left_text and '"amount": 500' in right_text
    # The matching T1111 rows are not part of the example.
    assert "T1111" not in left_text and "T1111" not in right_text
    assert "emitted_at" not in left_text

    html = render_html_report(model)
    assert "500" in html


def test_a_record_lost_inside_a_duplicated_pk_renders_with_an_empty_target_side():
    """A lost record has no target records to show: the target column stays
    empty rather than claiming a missing PK field or printing `[]`, and the
    note says what happened."""
    model = _comparison_with_records(
        {"users": [{"id": 7, "code": "T1110"}, {"id": 7, "code": "T1111"}]},
        {"users": [{"id": 7, "code": "T1110"}, {"id": 8, "code": "T1110"}]},
        {"users": [["id"]]},
    )

    assert model.passed is False
    (section,) = model.stream_sections
    block = next(
        b for b in section.diff_blocks if b.title.startswith("Field value diffs —")
    )
    header = next(row for row in block.split_rows if row.header)
    assert header.header == (
        "record pk = [7] — the target no longer emits 1 record of this PK"
    )
    pinned = block.split_rows[block.split_rows.index(header) + 1]
    assert pinned.left is not None and pinned.left.text == "pk id = 7"
    assert pinned.right is None
    body = block.split_rows[block.split_rows.index(header) + 2 :]
    assert all(row.right is None for row in body)
    assert all(row.left is not None and row.left.kind == "del" for row in body)
    assert '"T1111"' in " ".join(row.left.text for row in body if row.left)

    raw = next(
        b
        for b in section.diff_blocks
        if b.title.startswith("Field value diffs \u2014 raw")
    )
    assert raw.lines[0] == DiffLine(
        kind="meta",
        text="record pk = [7] — the target no longer emits 1 record of this PK",
    )
    assert "the target no longer emits 1 record of this PK" in render_html_report(model)


def test_a_lost_record_under_a_nested_composite_pk_pins_every_pk_field():
    def reading(code):
        return {"location": {"id": "a"}, "day": "d1", "code": code}

    model = _comparison_with_records(
        {"readings": [reading("T1110"), reading("T1111")]},
        {"readings": [reading("T1110")]},
        {"readings": [["location", "id"], ["day"]]},
    )

    (section,) = model.stream_sections
    block = next(
        b for b in section.diff_blocks if b.title.startswith("Field value diffs —")
    )
    header = next(row for row in block.split_rows if row.header)
    assert header.header == (
        'record pk = ["a", "d1"] — the target no longer emits 1 record of this PK'
    )
    start = block.split_rows.index(header) + 1
    pinned = block.split_rows[start : start + 2]
    assert [row.left.text for row in pinned if row.left] == [
        'pk location.id = "a"',
        'pk day = "d1"',
    ]
    assert all(row.right is None for row in pinned)


def test_a_capped_group_example_renders_a_bounded_block():
    """Hundreds of differing records under one PK render only the capped
    example, so the report stays small and quick to build."""
    model = _comparison_with_records(
        {"users": [{"id": 7, "seq": i} for i in range(500)]},
        {"users": [{"id": 7, "seq": i, "new": 1} for i in range(500)]},
        {"users": [["id"]]},
    )

    (section,) = model.stream_sections
    block = next(
        b for b in section.diff_blocks if b.title.startswith("Field value diffs —")
    )
    header = next(row for row in block.split_rows if row.header)
    assert header.header.endswith(
        "500 control and 500 target records of this PK do not match "
        "(first 20 of each shown)"
    )
    # 20 records a side, not the 33 or so the 200-row block cap would let in.
    assert sum('"seq":' in row.left.text for row in block.split_rows if row.left) == 20


def test_added_copies_warn_on_the_field_values_row():
    """Control `7: A, B`, target `(A, B) x 50`: a warning on every surface,
    with the PK and its extra copies listed, and the run passes."""
    rows = [{"id": 7, "event": "A"}, {"id": 7, "event": "B"}]
    model = _comparison_with_records(
        {"users": rows}, {"users": rows * 50}, {"users": [["id"]]}
    )

    assert model.passed is True
    statuses = {check.name: check.status for check in model.checks}
    assert statuses["Field values"] == "warn"
    field_check = next(c for c in model.checks if c.name == "Field values")
    assert field_check.summary == (
        "All records match, apart from identical copies the target added "
        "— 1 stream: users"
    )
    assert field_check.details == (
        "Stream users: 1 duplicated PK value(s) emit 98 more identical copies in "
        "target than in control",
    )

    (section,) = model.stream_sections
    assert section.status == "warn"
    assert "98 more identical copies in target under 1 duplicated PK(s)" in (
        section.headline
    )
    block = next(
        b for b in section.diff_blocks if b.title.startswith("Identical copies added")
    )
    assert block.title == (
        "Identical copies added in target — 98 more under 1 PK value(s)"
    )
    assert [line.text for line in block.lines if line.kind == "add"] == ["[7] +98"]
    assert not any(b.title.startswith("Field value diffs") for b in section.diff_blocks)

    summary = render_inline_summary(model)
    assert "| Field values | ⚠️ |" in summary
    assert "✅ PASS" in summary
    assert 'class="stream stream--warn"' in render_html_report(model)


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


def test_warning_streams_cannot_push_a_failing_stream_past_the_section_cap(
    monkeypatch,
):
    """Failing streams first, then warning ones, then passing ones, by name
    within each group: alphabetically-earlier warnings must not take the
    failing stream's place under the cap."""
    monkeypatch.setattr(
        "airbyte_ops_mcp.regression_tests.report.MAX_STREAM_SECTIONS", 3
    )
    rows = [{"id": 1, "n": "a"}, {"id": 2, "n": "b"}]
    duplicated = [{"id": 1, "n": "a"}, {"id": 1, "n": "a"}, {"id": 2, "n": "b"}]
    pks = {name: [["id"]] for name in ("aaa", "bbb", "ccc", "yyy", "zzz")}
    model = _comparison_with_records(
        {
            "aaa": duplicated,
            "bbb": duplicated,
            "ccc": rows,
            "yyy": rows,
            "zzz": rows,
        },
        {
            "aaa": duplicated,
            "bbb": duplicated,
            "ccc": rows,
            "yyy": rows[:1],
            "zzz": rows[:1],
        },
        pks,
    )

    assert [(s.stream, s.status) for s in model.stream_sections] == [
        ("yyy", "fail"),
        ("zzz", "fail"),
        ("aaa", "warn"),
    ]
    assert model.omitted_stream_count == 2
    assert all(section.diff_blocks for section in model.stream_sections)


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


# HTTP replay coverage: a target compared against partly-live data is not a
# comparison against identical data, and the report has to say so
# --------------------------------------------------------------------------


def _replaying_target(flow_count: int, live_flow_count: int, **extra) -> dict:
    return _run_result(
        True,
        record_counts_per_stream={"users": 5},
        http_metrics={
            "flow_count": flow_count,
            "duplicate_flow_count": 0,
            "replayed_flow_count": flow_count - live_flow_count,
            "live_flow_count": live_flow_count,
            "replay_source": "/tmp/target/http_replay_corpus.mitm",
            **extra,
        },
    )


def _replay_check(model) -> CheckResult | None:
    return next(
        (check for check in model.checks if check.name == "HTTP replay coverage"), None
    )


def test_a_fully_replayed_target_reports_clean_replay_coverage():
    model = _comparison("read", _replaying_target(20, 0), _run_result(True))

    check = _replay_check(model)
    assert check is not None
    assert check.status == "pass"
    assert "20 of 20" in check.summary


def test_a_mostly_live_target_run_is_flagged_as_not_the_same_data():
    model = _comparison("read", _replaying_target(20, 10), _run_result(True))

    check = _replay_check(model)
    assert check is not None
    assert check.status == "warn"
    assert "did not see the same upstream data" in check.summary
    # Diagnostic for now: it reports without flipping the verdict, which waits
    # on strict record comparison.
    assert model.passed is True


def test_a_shortfall_names_the_urls_that_matched_nothing():
    """The counts say a shortfall happened, never why.

    Diagnosing one needs the requests the corpus could not answer, and the dumps
    holding them are excluded from the uploaded artifacts on purpose -- so if the
    check does not name them the run has to be repeated to be understood.
    """
    model = _comparison(
        "read",
        _replaying_target(
            20,
            10,
            live_urls=[
                {"url": "https://graph.example.com/report/9001", "count": 6},
                {"url": "https://graph.example.com/report/9002", "count": 4},
            ],
            live_unique_url_count=7,
        ),
        _run_result(True),
    )

    check = _replay_check(model)
    assert check is not None
    assert "https://graph.example.com/report/9001" in check.summary
    assert "and 5 more" in check.summary


def test_a_clean_replay_run_does_not_list_urls():
    """Nothing went live, so there is nothing to explain."""
    model = _comparison("read", _replaying_target(20, 0), _run_result(True))

    check = _replay_check(model)
    assert check is not None
    assert "unmatched" not in check.summary


def test_counts_shortened_by_a_killed_shutdown_do_not_read_as_clean_coverage():
    """A `SIGKILL`ed mitmproxy loses the flows it had not flushed.

    The loss can only lower `live_flow_count`, so an incomplete dump flatters the
    replay acceptance criterion -- below the ratio it would otherwise read as a
    fully replayed run.
    """
    model = _comparison(
        "read",
        _replaying_target(
            20,
            0,
            metrics_incomplete=(
                "mitmproxy did not shut down within 30s and was killed, so the "
                "flows it had not flushed are missing from its dump"
            ),
        ),
        _run_result(True),
    )

    check = _replay_check(model)
    assert check is not None
    assert check.status == "warn"
    assert "HTTP metrics are incomplete" in check.summary
    assert "target run:" in check.summary


def test_a_control_run_killed_before_it_flushed_is_named_by_the_coverage_check():
    """The kill can happen on either side, and the control's is the worse one.

    A control killed before it flushed loses exactly the flows the target then
    refetches live, so reading only the target's marker leaves the check
    reporting the drift -- and naming the URLs -- with nothing saying the
    recording was short. That is the misattribution the marker exists to
    prevent, and per-side execution details are not where a reader goes after a
    red check.
    """
    model = _comparison(
        "read",
        _replaying_target(
            900,
            400,
            live_urls=[{"url": "https://api.example.com/v1/a", "count": 40}],
            live_unique_url_count=40,
        ),
        _run_result(
            True,
            http_metrics={
                "flow_count": 900,
                "metrics_incomplete": (
                    "mitmproxy did not shut down within 30s and was killed, so "
                    "the flows it had not flushed are missing from its dump"
                ),
            },
        ),
    )

    check = _replay_check(model)
    assert check is not None
    assert check.status == "warn"
    assert "control run:" in check.summary
    assert "was killed" in check.summary
    # The cause, not only its consequence: the ratio wording must not be what
    # the reader is left with.
    assert "did not see the same upstream data" not in check.summary


def test_both_sides_being_incomplete_names_both():
    """Neither marker may be swallowed by the other."""
    model = _comparison(
        "read",
        _replaying_target(20, 0, metrics_incomplete="target proxy was killed"),
        _run_result(
            True,
            http_metrics={
                "flow_count": 20,
                "metrics_incomplete": "control proxy was killed",
            },
        ),
    )

    check = _replay_check(model)
    assert check is not None
    assert "control run: control proxy was killed" in check.summary
    assert "target run: target proxy was killed" in check.summary


def test_skipped_replay_is_reported_rather_than_passing_silently():
    """Tripping the dump-size cap must not look like a clean replayed run."""
    target = _run_result(
        True,
        record_counts_per_stream={"users": 5},
        http_metrics={
            "flow_count": 20,
            "duplicate_flow_count": 0,
            "replayed_flow_count": 0,
            "live_flow_count": 20,
            "replay_skipped_reason": "replay corpus is 400 MB (cap 256 MB)",
        },
    )
    model = _comparison("read", target, _run_result(True))

    check = _replay_check(model)
    assert check is not None
    assert check.status == "warn"
    assert "400 MB" in check.summary


def test_a_run_that_was_not_replaying_gets_no_replay_check():
    """`--enable-http-metrics` alone must not grow a replay row."""
    target = _run_result(
        True, http_metrics={"flow_count": 12, "duplicate_flow_count": 1}
    )
    model = _comparison("read", target, _run_result(True))

    assert _replay_check(model) is None


def test_the_http_table_carries_the_replay_counts():
    model = _comparison(
        "read", _replaying_target(20, 3, unreplayable_flow_count=4), _run_result(True)
    )

    table = next(
        table for table in model.metric_tables if table.title == "HTTP Traffic"
    )
    rows = {row.label: row for row in table.rows}
    assert rows["Replayed"].target == 17
    assert rows["Live"].target == 3
    assert rows["Unreplayable"].target == 4


def test_every_flow_unreplayable_still_reports_the_dropped_count():
    """The run whose count matters most used to report zero.

    `unreplayable_flow_count` was keyed on a surviving corpus, but when every
    recorded flow is unreplayable there is no corpus -- so the number that
    explains why nothing replayed was dropped exactly when it was the answer.
    """
    target = _run_result(
        True,
        record_counts_per_stream={"users": 5},
        http_metrics={
            "flow_count": 1,
            "duplicate_flow_count": 0,
            "replayed_flow_count": 0,
            "live_flow_count": 1,
            "unreplayable_flow_count": 1,
            "replay_skipped_reason": "replay source holds no replayable flows",
        },
    )
    model = _comparison("read", target, _run_result(True))

    table = next(
        table for table in model.metric_tables if table.title == "HTTP Traffic"
    )
    rows = {row.label: row for row in table.rows}
    assert rows["Unreplayable"].target == 1


def test_a_proxy_that_never_ran_reports_the_reason_and_no_zero_table():
    """A payload with only a reason means nothing was measured, not zero traffic."""
    target = _run_result(
        True,
        record_counts_per_stream={"users": 5},
        http_metrics={
            "replay_skipped_reason": "mitmproxy is unavailable, so nothing "
            "could be replayed"
        },
    )
    model = _comparison("read", target, _run_result(True))

    assert all(table.title != "HTTP Traffic" for table in model.metric_tables)
    check = _replay_check(model)
    assert check is not None
    assert check.status == "warn"
    assert "mitmproxy is unavailable" in check.summary


def test_a_command_that_makes_no_requests_gets_no_replay_diagnostic():
    """`spec` calls nothing upstream, so it has nothing to replay and no drift.

    Its control run records an empty dump, the target finds nothing to replay
    from, and the skip is real but the reasoning is vacuous. Left alone, every
    connector run would carry a failed check on `spec` -- and usually `check`
    too -- permanently and by construction, which is how a reader learns to
    ignore it on `read`, the one stage where it means something.
    """
    target = _run_result(
        True,
        http_metrics={
            "flow_count": 0,
            "duplicate_flow_count": 0,
            "replayed_flow_count": 0,
            "live_flow_count": 0,
            "replay_skipped_reason": "replay source is missing or empty",
        },
    )
    model = _comparison("spec", target, _run_result(True))

    assert _replay_check(model) is None
    # And no all-zero traffic table alongside it.
    assert all(table.title != "HTTP Traffic" for table in model.metric_tables)


def test_a_target_that_called_out_is_still_reported_when_the_control_did_not():
    """The asymmetry worth shouting about, and the reason for keying on target.

    Control capturing nothing while the target reaches the API is what a broken
    capture looks like. Silencing on the *control* having no flows -- the
    obvious reading of "nothing was recorded" -- would hide exactly that.
    """
    target = _run_result(
        True,
        http_metrics={
            "flow_count": 8,
            "duplicate_flow_count": 0,
            "replayed_flow_count": 0,
            "live_flow_count": 8,
            "replay_skipped_reason": "replay source is missing or empty",
        },
    )
    model = _comparison("read", target, _run_result(True))

    check = _replay_check(model)
    assert check is not None
    assert check.status == "warn"


def test_a_proxy_that_never_ran_is_not_mistaken_for_a_quiet_command():
    """No `flow_count` at all means nothing was measured, not zero traffic."""
    target = _run_result(
        True,
        http_metrics={"replay_skipped_reason": "mitmproxy is unavailable"},
    )
    model = _comparison("read", target, _run_result(True))

    check = _replay_check(model)
    assert check is not None
    assert check.status == "warn"


# --------------------------------------------------------------------------
# Stopped-early reads: INCOMPLETE on every surface
# --------------------------------------------------------------------------

_STOPPED = {"reason": "timeout", "records_seen": 1234, "elapsed_s": 10200.0}


def _stopped(**overrides) -> dict:
    return _run_result(True, stopped_early={**_STOPPED, **overrides})


def _partial_summary(records_in_target: int = 2) -> RecordComparisonSummary:
    """A stopped read: the control holds three records, the target this many."""

    def record(data: dict) -> AirbyteMessage:
        return AirbyteMessage(
            type=AirbyteMessageType.RECORD,
            record=AirbyteRecordMessage(stream="users", data=data, emitted_at=1),
        )

    return run_record_comparisons(
        {"users": [record({"id": 1}), record({"id": 2}), record({"id": 3})]},
        {"users": [record({"id": index}) for index in range(1, records_in_target + 1)]},
        {"users": [["id"]]},
        partial=True,
    )


def test_a_stopped_side_makes_the_verdict_incomplete_never_pass():
    model = _comparison("read", _stopped(), _stopped())

    assert model.passed is False
    assert model.verdict_label == "INCOMPLETE"
    assert (
        model.verdict_detail == "stopped early (timeout) after 1,234 records per side"
    )
    assert model.context.stopped_early_notes == (
        "Control: stopped early (timeout) after 1,234 records in 10,200 s",
        "Target: stopped early (timeout) after 1,234 records in 10,200 s",
    )

    summary = render_inline_summary(model)
    assert (
        "**Result:** ❌ INCOMPLETE — stopped early (timeout) after 1,234 records "
        "per side" in summary
    )
    assert (
        "- Control: stopped early (timeout) after 1,234 records in 10,200 s" in summary
    )
    assert (
        "- Target: stopped early (timeout) after 1,234 records in 10,200 s" in summary
    )

    html = render_html_report(model)
    assert "verdict--fail" in html
    assert "INCOMPLETE" in html
    assert "<dt>Stopped early</dt>" in html
    assert "Target: stopped early (timeout) after 1,234 records in 10,200 s" in html


READABLE_FIELDS = {
    "users": {
        "cursor": ["updated_at"],
        "readable": True,
        "declared": "string/date-time",
        "reason": "readable (string/date-time)",
    },
    "tokens": {
        "cursor": ["token"],
        "readable": False,
        "declared": "string",
        "reason": "masked: type string",
    },
    "events": {
        "cursor": None,
        "readable": False,
        "declared": None,
        "reason": "no cursor",
    },
}


def test_the_context_says_how_the_output_was_masked():
    """A downloaded report must say whether its artifacts hold raw data."""
    model = _comparison(
        "read",
        _run_result(True, output_mode="masked"),
        _run_result(True, output_mode="masked"),
    )

    assert model.context.output_mode == "masked"
    assert model.context.masking is not None
    assert model.context.masking.startswith("masked — ")
    assert "primary keys masked" in model.context.masking
    # A result without the per-stream key states the rule instead of a count.
    assert "integer or a date" in model.context.masking
    assert model.context.readable_fields == ()
    assert model.context.readable_summary is None

    html = render_html_report(model)
    assert "<dt>Output mode</dt>" in html
    assert "primary keys masked" in html
    assert "Readable fields" not in html


def test_a_masked_report_lists_what_stayed_readable_per_stream():
    """The context line carries the count; the table under it says, per
    stream, which cursor stayed readable and why the others did not."""
    model = _comparison(
        "read",
        _run_result(True, output_mode="masked", readable_fields=READABLE_FIELDS),
        _run_result(True, output_mode="masked"),
    )

    assert model.context.masking is not None
    assert "cursor readable on 1 of 2 streams" in model.context.masking
    assert model.context.readable_summary == (
        "cursor readable on 1 of 2 streams (integer, date, date-time only)"
    )
    assert [
        (row.stream, row.cursor, row.readable, row.detail)
        for row in model.context.readable_fields
    ] == [
        ("events", None, False, "no cursor"),
        ("tokens", "token", False, "masked: type string"),
        ("users", "updated_at", True, "string/date-time"),
    ]

    html = render_html_report(model)
    assert "<h3>Readable fields</h3>" in html
    assert (
        "<td><code>users</code></td><td><code>updated_at</code></td><td>yes</td><td>string/date-time</td>"
        in html
    )
    assert (
        "<td><code>tokens</code></td><td><code>token</code></td><td>no</td><td>masked: type string</td>"
        in html
    )
    assert "<td><code>events</code></td><td>—</td><td>no</td><td>no cursor</td>" in html


def test_the_step_summary_carries_the_readable_count_but_not_the_table():
    model = build_single_version_report_model(
        connector_image=TARGET_IMAGE,
        command="read",
        result=_run_result(True, output_mode="masked", readable_fields=READABLE_FIELDS),
    )

    summary = render_inline_summary(model)

    assert (
        "- Readable fields: cursor readable on 1 of 2 streams "
        "(integer, date, date-time only)"
    ) in summary
    assert "updated_at" not in summary
    assert "masked: type string" not in summary


def test_a_raw_run_has_no_readable_fields_table():
    model = _comparison(
        "read",
        _run_result(True, output_mode="raw", readable_fields=READABLE_FIELDS),
        _run_result(True, output_mode="raw"),
    )

    # The rows are built from the key when present; the summary and the
    # masked wording are not, and the page says the run is raw.
    assert model.context.readable_summary is None
    assert "Readable fields" not in render_inline_summary(model)
    assert model.context.masking is not None
    assert model.context.masking.startswith("raw — ")


def test_a_raw_run_is_labelled_as_sensitive():
    model = build_single_version_report_model(
        connector_image=TARGET_IMAGE,
        command="read",
        result=_run_result(True, output_mode="raw"),
    )

    assert model.context.output_mode == "raw"
    assert model.context.masking is not None
    assert model.context.masking.startswith("raw — ")
    assert "treat the artifacts as sensitive" in render_html_report(model)


def test_a_result_without_a_mode_renders_no_masking_row():
    model = _comparison("read", _run_result(True), _run_result(True))

    assert model.context.output_mode is None
    assert model.context.masking is None
    assert "<dt>Output mode</dt>" not in render_html_report(model)


def test_sides_that_stopped_at_different_points_show_both_counts():
    model = _comparison("read", _stopped(records_seen=987), _stopped())

    assert model.verdict_detail == (
        "stopped early (timeout) after 1,234 (control) / 987 (target) records"
    )


def test_one_stopped_side_is_named_and_the_other_is_not_blamed():
    model = _comparison("read", _stopped(reason="cap"), _run_result(True))

    assert model.verdict_label == "INCOMPLETE"
    assert model.verdict_detail == (
        "target stopped early (cap) after 1,234 records; control ran to completion"
    )
    assert model.context.stopped_early_notes == (
        "Target: stopped early (cap) after 1,234 records in 10,200 s",
    )


def test_a_side_stopped_at_its_share_of_the_budget_says_so_on_every_surface():
    """A target that never started reads as one, not as an empty read."""
    model = _comparison(
        "read",
        _stopped(records_seen=0, elapsed_s=0.0, share_s=0, budget_s=10_200),
        _stopped(elapsed_s=5760.0, share_s=5760, budget_s=10_200),
    )

    assert model.passed is False
    assert model.verdict_label == "INCOMPLETE"
    assert model.verdict_detail == (
        "stopped early (timeout) after 1,234 (control) / 0 (target) records"
    )
    control_note = (
        "Control: stopped early (timeout) after 1,234 records in 5,760 s, at the "
        "end of its 96-minute share of the 170-minute read budget"
    )
    target_note = (
        "Target: stopped early (timeout) after 0 records in 0 s, without "
        "starting: nothing was left of the 170-minute read budget"
    )
    assert model.context.stopped_early_notes == (control_note, target_note)
    summary = render_inline_summary(model)
    assert f"- {control_note}" in summary
    assert f"- {target_note}" in summary
    html = render_html_report(model)
    assert control_note in html
    assert target_note in html


def test_a_strict_failure_on_a_stopped_read_is_still_a_regression():
    model = _comparison(
        "read",
        _stopped(),
        _stopped(),
        extra_checks=(
            CheckResult(name="Field values", passed=False, summary="1 record differs"),
        ),
    )

    assert model.passed is False
    assert model.verdict_label == "INCOMPLETE"
    assert model.verdict_detail == (
        "stopped early (timeout) after 1,234 records per side, but 1 check "
        "failed: field values — REGRESSION DETECTED"
    )


def test_a_diagnostic_failure_on_a_stopped_read_claims_no_regression():
    model = _comparison(
        "read",
        _stopped(),
        _stopped(),
        extra_checks=(
            CheckResult(
                name="Record counts",
                passed=False,
                severity="diagnostic",
                summary="1 fewer record",
            ),
        ),
    )

    assert model.verdict_label == "INCOMPLETE"
    assert "REGRESSION DETECTED" not in model.verdict_detail
    assert "check failed" not in model.verdict_detail


def test_an_errored_comparison_on_a_stopped_read_claims_no_regression():
    """A comparator crash is a tooling failure on a stopped read too, as the
    CLI's `regression_detected` treats it."""
    errored = RecordComparisonSummary(
        passed=False,
        errored=True,
        count_comparison=ComparisonResult(
            passed=False, message="Record comparison errored"
        ),
        errors=["Record comparison errored: OSError('boom')"],
    )
    model = _comparison("read", _stopped(), _stopped(), record_comparison=errored)

    assert model.passed is False
    assert model.verdict_label == "INCOMPLETE"
    assert model.verdict_detail == (
        "stopped early (timeout) after 1,234 records per side; the record "
        "comparison errored, so it is inconclusive"
    )


def test_a_stopped_side_beside_a_crashed_target_is_incomplete_and_a_regression():
    model = _comparison("read", _run_result(False), _stopped())

    assert model.verdict_label == "INCOMPLETE"
    assert model.verdict_detail == (
        "control stopped early (timeout) after 1,234 records; target ran to "
        "completion; target failed (exit 1), control succeeded — regression "
        "detected — REGRESSION DETECTED"
    )


def test_partial_record_comparison_checks_downgrade_counts_and_presence():
    """On a partial read the strict rows are PK integrity and field values."""
    summary = _partial_summary()

    checks = {check.name: check for check in build_record_comparison_checks(summary)}

    assert checks["Record counts"].status == "warn"
    assert "inconclusive on a stopped-early read" in checks["Record counts"].summary
    assert checks["Primary key presence"].status == "warn"
    assert checks["Primary key integrity (control)"].severity == "strict"
    assert checks["Primary key integrity (target)"].severity == "strict"
    assert checks["Field values"].severity == "strict"
    assert checks["Field values"].status == "pass"


def test_partial_read_counts_that_agree_are_still_inconclusive():
    """Under a cap equal counts are what the cap guarantees, not evidence."""
    summary = _partial_summary(records_in_target=3)
    assert summary.count_comparison.passed is True

    checks = {check.name: check for check in build_record_comparison_checks(summary)}

    assert checks["Record counts"].status == "warn"
    assert checks["Record counts"].summary == (
        "Record counts match (inconclusive on a stopped-early read)"
    )
    assert checks["Primary key presence"].status == "warn"
    assert checks["Field values"].status == "pass"
    model = _comparison(
        "read",
        _run_result(
            True, stopped_early=_STOPPED, record_counts_per_stream={"users": 3}
        ),
        _run_result(
            True, stopped_early=_STOPPED, record_counts_per_stream={"users": 3}
        ),
        record_comparison=summary,
    )
    assert [section.status for section in model.stream_sections] == ["warn"]
    assert "| Record counts | ⚠️ |" in render_inline_summary(model)


def test_a_partial_reads_stream_section_warns_on_a_diagnostic_finding_alone():
    """A count drop on a partial read is reported as a warning, never a failure."""
    model = _comparison(
        "read",
        _run_result(
            True, stopped_early=_STOPPED, record_counts_per_stream={"users": 2}
        ),
        _run_result(
            True, stopped_early=_STOPPED, record_counts_per_stream={"users": 3}
        ),
        record_comparison=_partial_summary(),
    )

    assert [section.status for section in model.stream_sections] == ["warn"]
    assert "1 fewer record(s) in target" in model.stream_sections[0].headline
    assert model.verdict_label == "INCOMPLETE"
    assert "REGRESSION DETECTED" not in model.verdict_detail


def test_a_partial_read_warns_on_a_duplicate_pk_new_in_the_target():
    """Where the cap cut each side decides whether a duplicate looks new."""

    def record(data: dict) -> AirbyteMessage:
        return AirbyteMessage(
            type=AirbyteMessageType.RECORD,
            record=AirbyteRecordMessage(stream="users", data=data, emitted_at=1),
        )

    summary = run_record_comparisons(
        {"users": [record({"id": 1}), record({"id": 2})]},
        {"users": [record({"id": 1}), record({"id": 1}), record({"id": 2})]},
        {"users": [["id"]]},
        partial=True,
    )

    checks = {check.name: check for check in build_record_comparison_checks(summary)}
    assert checks["Primary key integrity (target)"].status == "warn"
    assert checks["Primary key integrity (target)"].summary == (
        "New duplicate primary keys in target (inconclusive on a stopped-early "
        "read) — 1 stream: users"
    )

    model = _comparison(
        "read",
        _run_result(
            True, stopped_early=_STOPPED, record_counts_per_stream={"users": 3}
        ),
        _run_result(
            True, stopped_early=_STOPPED, record_counts_per_stream={"users": 2}
        ),
        record_comparison=summary,
    )
    assert [section.status for section in model.stream_sections] == ["warn"]
    assert (
        "1 new duplicate PK(s) in target (inconclusive on a stopped-early read)"
        in model.stream_sections[0].headline
    )
    assert model.verdict_label == "INCOMPLETE"
    assert "REGRESSION DETECTED" not in model.verdict_detail


def _ledger_record(transaction_id: str, event: str) -> AirbyteMessage:
    return AirbyteMessage(
        type=AirbyteMessageType.RECORD,
        record=AirbyteRecordMessage(
            stream="transactions",
            data={"transaction_id": transaction_id, "event": event},
            emitted_at=1,
        ),
    )


def test_a_partial_read_reports_duplicated_pk_groups_without_failing():
    """A cut can split a duplicated PK's records; its rows and section warn."""
    summary = run_record_comparisons(
        {
            "transactions": [
                _ledger_record("T7", "sale"),
                _ledger_record("T7", "hold"),
                _ledger_record("T8", "sale"),
                _ledger_record("T8", "sale"),
            ]
        },
        {
            "transactions": [
                _ledger_record("T7", "sale"),
                _ledger_record("T7", "release"),
                _ledger_record("T8", "sale"),
            ]
        },
        {"transactions": [["transaction_id"]]},
        partial=True,
    )

    checks = {check.name: check for check in build_record_comparison_checks(summary)}
    assert checks["Field values"].status == "warn"
    assert checks["Field values"].summary == (
        "All records match, apart from duplicated PK values that are inconclusive "
        "on a stopped-early read — 1 stream: transactions"
    )
    # The count row is the inconclusive one, never the duplicate-row allowance:
    # a complete read would pass this shortfall as collapsed copies.
    assert checks["Record counts"].status == "warn"
    assert checks["Record counts"].summary == (
        "Record count mismatch — 1 stream failed: transactions (inconclusive on a "
        "stopped-early read)"
    )
    assert checks["Primary key integrity (control)"].summary == (
        "Pre-existing duplicate primary keys in control (not a regression); others "
        "not duplicated in target (partial read) — 1 stream: transactions"
    )

    model = _comparison(
        "read",
        _run_result(
            True, stopped_early=_STOPPED, record_counts_per_stream={"transactions": 3}
        ),
        _run_result(
            True, stopped_early=_STOPPED, record_counts_per_stream={"transactions": 4}
        ),
        record_comparison=summary,
    )
    assert model.verdict_label == "INCOMPLETE"
    assert "REGRESSION DETECTED" not in model.verdict_detail
    [section] = model.stream_sections
    assert section.status == "warn"
    assert (
        "1 duplicated PK(s) whose records differ (inconclusive on a stopped-early "
        "read)" in section.headline
    )
    assert (
        "1 duplicate PK(s) in control not duplicated in target (partial read)"
        in section.headline
    )
    assert "fixed in target" not in section.headline
    titles = [block.title for block in section.diff_blocks]
    assert any(
        title.startswith("Duplicated PK values whose records differ, inconclusive")
        for title in titles
    )
    assert not any(title.startswith("Field value diffs") for title in titles)
    html = render_html_report(model)
    assert "not duplicated in target (partial read)" in html
    assert "fixed in target" not in html


def test_a_single_version_stopped_read_is_incomplete():
    model = build_single_version_report_model(
        connector_image=TARGET_IMAGE, command="read", result=_stopped()
    )

    assert model.passed is False
    assert model.verdict_label == "INCOMPLETE"
    assert model.verdict_detail == "stopped early (timeout) after 1,234 records"
    assert model.context.stopped_early_notes == (
        "Run: stopped early (timeout) after 1,234 records in 10,200 s",
    )
    assert "❌ INCOMPLETE" in render_inline_summary(model)


# The connector's own cache: a metric no proxy can observe, and the diagnostic
# that turns it into a regression signal
# --------------------------------------------------------------------------


def _connector_cache(requests: int, hits: int) -> dict:
    """The connector-reported half of an `http_metrics` payload."""
    ratio = "N/A" if not requests else f"{(hits / requests) * 100:.2f}%"
    return {
        "connector_request_count": requests,
        "connector_cache_hits_count": hits,
        "connector_cache_hit_ratio": ratio,
    }


def _cache_check(model) -> CheckResult | None:
    return next(
        (check for check in model.checks if check.name == "Connector cache hit ratio"),
        None,
    )


def _http_table(model):
    return next(
        (table for table in model.metric_tables if table.title == "HTTP Traffic"),
        None,
    )


def test_the_http_table_no_longer_carries_the_duplicate_url_heuristic():
    """`Cache Hits Count` used to be the duplicate count wearing a cache label."""
    model = _comparison(
        "read",
        _run_result(True, http_metrics={"flow_count": 12, "duplicate_flow_count": 5}),
        _run_result(True, http_metrics={"flow_count": 12, "duplicate_flow_count": 5}),
    )

    table = _http_table(model)
    assert table is not None
    labels = {row.label for row in table.rows}
    assert "Cache Hits Count" not in labels
    assert "Cache hits" not in labels
    # The duplicate count itself stays -- it is a real number, just not that one,
    # and it carries the name `report.md` gives it, not mitmproxy's.
    assert "Repeated URLs" in labels
    assert "Duplicate Flow Count" not in labels


def test_the_http_table_carries_the_connector_reported_counts():
    model = _comparison(
        "read",
        _run_result(
            True,
            http_metrics={
                "flow_count": 12,
                "duplicate_flow_count": 0,
                **_connector_cache(40, 10),
            },
        ),
        _run_result(
            True,
            http_metrics={
                "flow_count": 12,
                "duplicate_flow_count": 0,
                **_connector_cache(40, 12),
            },
        ),
    )

    rows = {row.label: row for row in _http_table(model).rows}
    assert rows["Connector requests"].target == 40
    assert rows["Cache hits"].target == 10
    assert rows["Cache hits"].control == 12


def test_the_http_table_appears_for_a_connector_only_run():
    """No proxy at all: the connector's cache is measurable without one.

    Gating the table on `flow_count` would hide every connector cache metric on
    a run made without `--enable-http-metrics`.
    """
    model = _comparison(
        "read",
        _run_result(True, http_metrics=_connector_cache(40, 10)),
        _run_result(True, http_metrics=_connector_cache(40, 10)),
    )

    table = _http_table(model)
    assert table is not None
    labels = {row.label for row in table.rows}
    assert labels == {"Connector requests", "Cache hits"}
    # No proxy rows at all rather than a column of zeroes: nothing was captured.
    assert "Requests" not in labels


def test_a_side_that_did_not_report_is_unknown_rather_than_zero():
    """The failure mode most likely to mislead a reviewer.

    A target on a CDK predating the counters reports nothing while the control
    reports plenty. A `0` in the target column would read as caching that broke;
    `None` renders as an em dash and suppresses the delta.
    """
    model = _comparison(
        "read",
        _run_result(True, http_metrics={"flow_count": 12, "duplicate_flow_count": 0}),
        _run_result(
            True,
            http_metrics={
                "flow_count": 12,
                "duplicate_flow_count": 0,
                **_connector_cache(40, 10),
            },
        ),
    )

    rows = {row.label: row for row in _http_table(model).rows}
    assert rows["Cache hits"].control == 10
    assert rows["Cache hits"].target is None
    assert rows["Cache hits"].delta is None
    assert rows["Cache hits"].changed is False


def test_a_captured_side_with_no_requests_is_a_zero_not_an_unknown():
    """`flow_count: 0` is a proxy that ran and saw nothing; absent is one that never ran.

    A target that made no requests beside a control that made 120 is the
    finding the request totals exist for, and an em dash there reads as
    "nobody looked" when somebody did.
    """
    model = _comparison(
        "read",
        _run_result(True, http_metrics={"flow_count": 0, "duplicate_flow_count": 0}),
        _run_result(True, http_metrics={"flow_count": 120, "duplicate_flow_count": 8}),
    )

    rows = {row.label: row for row in _http_table(model).rows}
    assert rows["Requests"].control == 120
    assert rows["Requests"].target == 0
    assert rows["Requests"].delta == -120
    assert rows["Repeated URLs"].target == 0


def test_a_side_whose_proxy_never_ran_is_an_unknown_not_a_zero():
    model = _comparison(
        "read",
        _run_result(True),
        _run_result(True, http_metrics={"flow_count": 120, "duplicate_flow_count": 8}),
    )

    rows = {row.label: row for row in _http_table(model).rows}
    assert rows["Requests"].control == 120
    assert rows["Requests"].target is None
    assert rows["Requests"].delta is None


def test_two_captured_sides_that_made_no_requests_get_no_table():
    """`spec` on both sides: measured, and nothing worth a table of zeroes."""
    model = _comparison(
        "spec",
        _run_result(True, http_metrics={"flow_count": 0, "duplicate_flow_count": 0}),
        _run_result(True, http_metrics={"flow_count": 0, "duplicate_flow_count": 0}),
    )

    assert _http_table(model) is None


def test_a_target_whose_caching_regressed_is_reported():
    """The payoff of the whole metric.

    A version that drops `use_cache` from a requester makes strictly more
    upstream requests for the same data. The proxy sees more flows and cannot say
    why; this says exactly why.
    """
    model = _comparison(
        "read",
        _run_result(True, http_metrics=_connector_cache(60, 6)),
        _run_result(True, http_metrics=_connector_cache(40, 20)),
    )

    check = _cache_check(model)
    assert check is not None
    assert check.status == "warn"
    assert "Caching regressed" in check.summary
    assert "a drop of 40.0 point(s), above 10" in check.summary
    assert "use_cache" in check.summary


@pytest.mark.parametrize(
    ("control", "target"),
    [
        pytest.param((5, 4), (10, 7), id="80-to-70-with-different-denominators"),
        pytest.param((100, 20), (100, 10), id="20-to-10"),
        pytest.param((3, 1), (30, 7), id="one-third-to-23-and-a-third"),
    ],
)
def test_a_drop_of_exactly_the_threshold_passes(control, target):
    """The threshold is a comparison of two ratios, and it has to be exact.

    `4/5 - 7/10` in floats is a hair over a tenth, so the boundary case warned
    with "a drop of 10 point(s), above 10" while `20/100 - 10/100` passed. The
    comparison is done on fractions, where both are exactly a tenth.
    """
    model = _comparison(
        "read",
        _run_result(True, http_metrics=_connector_cache(*target)),
        _run_result(True, http_metrics=_connector_cache(*control)),
    )

    check = _cache_check(model)
    assert check is not None
    assert check.status == "pass"


def test_a_drop_just_over_the_threshold_is_printed_with_its_decimal():
    """10.4 points used to print as "10 point(s), above 10"."""
    model = _comparison(
        "read",
        _run_result(True, http_metrics=_connector_cache(1000, 200)),
        _run_result(True, http_metrics=_connector_cache(1000, 304)),
    )

    check = _cache_check(model)
    assert check is not None
    assert check.status == "warn"
    assert "a drop of 10.4 point(s), above 10" in check.summary


def test_a_target_whose_cache_served_nothing_is_warned_about_under_the_threshold():
    """8% to 0% is a drop of 8 points: under the threshold, and a cache that is gone.

    The absolute threshold is right for a cache that served a lot; a cache that
    only ever served a little can lose all of it under the threshold, and a
    target reporting no hits where the control reported some is the shape of a
    requester that lost `use_cache` at any ratio.
    """
    model = _comparison(
        "read",
        _run_result(True, http_metrics=_connector_cache(50, 0)),
        _run_result(True, http_metrics=_connector_cache(50, 4)),
    )

    check = _cache_check(model)
    assert check is not None
    assert check.status == "warn"
    assert "Caching lost" in check.summary
    assert "0 of 50" in check.summary
    assert "4 of 50" in check.summary
    assert "use_cache" in check.summary
    assert model.passed is True


def test_the_cache_diagnostic_never_flips_the_verdict():
    """Diagnostic by design: a ratio moves for reasons that are not regressions.

    A differently ordered read warms the cache in a different place, and a
    version that legitimately stopped fetching a stream twice looks identical
    here. Failing a connector PR on that would be wrong.
    """
    model = _comparison(
        "read",
        _run_result(True, http_metrics=_connector_cache(60, 0)),
        _run_result(True, http_metrics=_connector_cache(40, 20)),
    )

    assert _cache_check(model).status == "warn"
    assert model.passed is True
    assert "regression" not in model.verdict_label.lower()


def test_a_steady_cache_hit_ratio_passes():
    model = _comparison(
        "read",
        _run_result(True, http_metrics=_connector_cache(40, 19)),
        _run_result(True, http_metrics=_connector_cache(40, 20)),
    )

    check = _cache_check(model)
    assert check is not None
    assert check.status == "pass"
    assert "19 of 40" in check.summary


def test_a_target_that_started_caching_is_not_warned_about():
    """An improvement, and a control with no hits has none to lose."""
    model = _comparison(
        "read",
        _run_result(True, http_metrics=_connector_cache(40, 20)),
        _run_result(True, http_metrics=_connector_cache(40, 0)),
    )

    assert _cache_check(model) is None


@pytest.mark.parametrize(
    ("control_http", "target_http"),
    [
        pytest.param({}, {}, id="neither-reported"),
        pytest.param(_connector_cache(40, 20), {}, id="target-silent"),
        pytest.param({}, _connector_cache(40, 20), id="control-silent"),
        pytest.param(
            _connector_cache(0, 0), _connector_cache(40, 20), id="control-no-requests"
        ),
    ],
)
def test_the_cache_diagnostic_is_silent_when_a_side_did_not_report(
    control_http, target_http
):
    """Every connector outside the Python CDK's `HttpClient` looks like this.

    A one-sided comparison is not a comparison, and warning on it would fire on
    every Java connector and every connector on an older CDK.
    """
    model = _comparison(
        "read",
        _run_result(True, http_metrics=target_http or None),
        _run_result(True, http_metrics=control_http or None),
    )

    assert _cache_check(model) is None


def test_the_connector_cache_ratio_surfaces_under_execution_details():
    """The per-side `dl` iterates `http_metrics`, so both ratios show up there."""
    model = _comparison(
        "read",
        _run_result(
            True,
            http_metrics={
                "flow_count": 12,
                "replay_hit_ratio": "100.00%",
                **_connector_cache(40, 10),
            },
        ),
        _run_result(True, http_metrics=_connector_cache(40, 10)),
    )
    html = render_html_report(model)

    assert "<dt>Cache hit ratio</dt>" in html
    assert "<dt>Replay hit ratio</dt>" in html
    assert "25.00%" in html


def test_execution_details_name_the_http_metrics_like_the_table_does():
    """One name per metric on every surface, the per-side list included.

    The `dl` used to label raw keys -- `Flow count`, `Connector request count`
    -- beside a table that says `Requests` and `Connector requests` for the
    same numbers. Keys without a row keep a readable form of the key.
    """
    model = _comparison(
        "read",
        _run_result(
            True,
            http_metrics={
                "flow_count": 12,
                "duplicate_flow_count": 3,
                "replay_source": "control",
                **_connector_cache(40, 10),
            },
        ),
        _run_result(True, http_metrics={"flow_count": 12}),
    )
    html = render_html_report(model)

    assert "<dt>Requests</dt>" in html
    assert "<dt>Repeated URLs</dt>" in html
    assert "<dt>Connector requests</dt>" in html
    assert "<dt>Replay source</dt>" in html
    assert "<dt>Flow count</dt>" not in html
    assert "<dt>Duplicate flow count</dt>" not in html
    assert "<dt>Connector request count</dt>" not in html


# --------------------------------------------------------------------------
# Not-exercised reads: a target-only stream with no records is never a pass
# --------------------------------------------------------------------------

_NOT_EXERCISED_DETAIL = (
    "1 stream(s) the control did not read returned no records: audit_logs"
)


def _read_result(counts: dict[str, int], **extra) -> dict:
    return _run_result(True, record_counts_per_stream=counts, **extra)


def test_a_target_only_stream_with_no_records_makes_the_verdict_not_exercised():
    """The comparison cannot fail a stream the control never read, so a zero
    there is the one way a PR's new stream passes untested."""
    model = _comparison(
        "read",
        _read_result({"users": 3}),
        _read_result({"users": 3}),
        configured_streams=("audit_logs", "users"),
        target_only_streams=("audit_logs",),
    )

    assert model.passed is False
    assert model.not_exercised is True
    assert model.verdict_label == "NOT EXERCISED"
    assert model.verdict_detail == _NOT_EXERCISED_DETAIL
    assert model.context.not_exercised_note is None
    assert model.outcome is not None
    assert model.outcome.regression_detected is False

    summary = render_inline_summary(model)
    assert f"**Result:** ❌ NOT EXERCISED — {_NOT_EXERCISED_DETAIL}" in summary
    assert "- Not exercised:" not in summary

    html = render_html_report(model)
    assert "verdict--fail" in html
    assert "NOT EXERCISED" in html
    assert "<dt>Not exercised</dt>" not in html


def test_every_unexercised_stream_is_counted_and_named():
    model = _comparison(
        "read",
        _read_result({"users": 3, "orders": 2}),
        _read_result({"users": 3}),
        target_only_streams=("audit_logs", "invoices", "orders"),
    )

    assert model.verdict_label == "NOT EXERCISED"
    assert model.verdict_detail == (
        "2 stream(s) the control did not read returned no records: audit_logs, invoices"
    )


def test_an_errored_comparison_beside_an_unexercised_stream_claims_no_regression():
    """A comparator crash is a tooling failure on a NOT EXERCISED read too, as
    on a stopped one and as the step summary words it."""
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
        _read_result({"users": 3}),
        _read_result({"users": 3}),
        target_only_streams=("audit_logs",),
        record_comparison=errored,
    )

    assert model.passed is False
    assert model.verdict_label == "NOT EXERCISED"
    assert model.verdict_detail == (
        f"{_NOT_EXERCISED_DETAIL}; the record comparison errored, so it is inconclusive"
    )


def test_the_strict_checks_keep_their_own_verdict_beside_an_unexercised_stream():
    """A regression in the streams both sides read is still named, and the
    record comparison's own verdict is not rewritten by the stream it never
    saw."""

    def record(data: dict) -> AirbyteMessage:
        return AirbyteMessage(
            type=AirbyteMessageType.RECORD,
            record=AirbyteRecordMessage(stream="users", data=data, emitted_at=1),
        )

    clean = run_record_comparisons(
        {"users": [record({"id": 1}), record({"id": 2})]},
        {"users": [record({"id": 1}), record({"id": 2})]},
        {"users": [["id"]]},
    )
    model = _comparison(
        "read",
        _read_result({"users": 2}),
        _read_result({"users": 2}),
        record_comparison=clean,
        target_only_streams=("audit_logs",),
    )
    assert clean.passed is True
    assert model.verdict_label == "NOT EXERCISED"
    assert "REGRESSION DETECTED" not in model.verdict_detail

    dropped = run_record_comparisons(
        {"users": [record({"id": 1}), record({"id": 2})]},
        {"users": [record({"id": 1})]},
        {"users": [["id"]]},
    )
    model = _comparison(
        "read",
        _read_result({"users": 1}),
        _read_result({"users": 2}),
        record_comparison=dropped,
        target_only_streams=("audit_logs",),
    )
    assert dropped.passed is False
    assert model.passed is False
    assert model.verdict_label == "FAIL (regression)"
    assert model.verdict_detail.startswith(f"{_NOT_EXERCISED_DETAIL}, but ")
    assert "REGRESSION DETECTED" in model.verdict_detail


@pytest.mark.parametrize(
    "target_success,control_success,expected_label",
    [
        pytest.param(False, True, "FAIL (regression)", id="regression"),
        pytest.param(False, False, "FAIL (inconclusive)", id="both-failed"),
    ],
)
def test_unexercised_stream_does_not_hide_a_failed_run(
    target_success, control_success, expected_label
):
    model = _comparison(
        "read",
        _run_result(target_success, record_counts_per_stream={"users": 2}),
        _run_result(control_success, record_counts_per_stream={"users": 2}),
        target_only_streams=("audit_logs",),
    )

    assert model.not_exercised is True
    assert model.verdict_label == expected_label
    assert _NOT_EXERCISED_DETAIL in model.verdict_detail


@pytest.mark.parametrize(
    "target_flags,detail",
    [
        pytest.param(
            {},
            _NOT_EXERCISED_DETAIL,
            id="not-exercised-both-failed",
        ),
        pytest.param(
            {
                "could_not_test": True,
                "could_not_test_detail": (
                    "1 stream(s) the control did not read failed with a config "
                    "error (often a missing permission or scope): audit_logs: "
                    "HTTP 400, code 4711"
                ),
                "excluded_not_exercised_streams": ("audit_logs",),
            },
            "HTTP 400, code 4711",
            id="could-not-test-both-failed",
        ),
    ],
)
def test_new_stream_summary_and_model_share_the_fail_label(
    tmp_path, target_flags, detail
):
    target = _run_result(
        False,
        record_counts_per_stream={"users": 2},
        **target_flags,
    )
    control = _run_result(False, record_counts_per_stream={"users": 2})
    model = _comparison(
        "read",
        target,
        control,
        target_only_streams=("audit_logs",),
    )
    summary_path = generate_action_test_comparison_report(
        target_image=TARGET_IMAGE,
        control_image=CONTROL_IMAGE,
        command="read",
        target_result=target,
        control_result=control,
        output_dir=tmp_path,
        target_only_streams=("audit_logs",),
    )
    result_line = next(
        line
        for line in summary_path.read_text().splitlines()
        if line.startswith("**Result:**")
    )

    assert model.verdict_label == "FAIL (inconclusive)"
    assert result_line.startswith("**Result:** FAIL (inconclusive) —")
    assert detail in model.verdict_detail
    assert detail in result_line


@pytest.mark.parametrize(
    "target_success,control_success,expected_label",
    [
        pytest.param(
            False, True, "COULD NOT TEST (config error)", id="target-config-error"
        ),
        pytest.param(False, False, "FAIL (inconclusive)", id="both-failed"),
    ],
)
def test_config_error_only_yields_could_not_test_without_both_failure(
    target_success, control_success, expected_label
):
    target = _run_result(
        target_success,
        record_counts_per_stream={"users": 2},
        could_not_test=True,
        could_not_test_detail="target-only config error detail",
        excluded_not_exercised_streams=("audit_logs",),
    )
    model = _comparison(
        "read",
        target,
        _run_result(control_success, record_counts_per_stream={"users": 2}),
        target_only_streams=("audit_logs",),
    )

    assert model.verdict_label == expected_label
    assert "target-only config error detail" in model.verdict_detail


@pytest.mark.parametrize(
    "target_result,expected_label,expected_details",
    [
        pytest.param(
            {
                "setup_error": True,
                "setup_error_detail": "1 stream(s) the control did not read are not defined by the target (lone INCOMPLETE status, no records, no error): audit_logs",
                "excluded_not_exercised_streams": ("audit_logs",),
            },
            "SETUP ERROR",
            ("not defined by the target",),
            id="setup-error",
        ),
        pytest.param(
            {
                "could_not_test": True,
                "could_not_test_detail": "1 stream(s) the control did not read failed with a config error (often a missing permission or scope): audit_logs: HTTP 400, code 4711",
                "excluded_not_exercised_streams": ("audit_logs",),
            },
            "COULD NOT TEST (config error)",
            ("HTTP 400", "4711"),
            id="config-error",
        ),
    ],
)
def test_target_only_error_verdicts_preserve_their_detail(
    target_result, expected_label, expected_details
):
    model = _comparison(
        "read",
        _read_result({"users": 2}, **target_result),
        _read_result({"users": 2}),
        target_only_streams=("audit_logs",),
    )

    assert model.passed is False
    assert model.verdict_label == expected_label
    assert all(detail in model.verdict_detail for detail in expected_details)
    assert model.not_exercised is False
    assert model.setup_error == (expected_label == "SETUP ERROR")
    assert model.could_not_test == (expected_label == "COULD NOT TEST (config error)")


def test_setup_error_detail_retains_a_real_target_failure():
    model = _comparison(
        "read",
        _run_result(
            False,
            record_counts_per_stream={"users": 2},
            setup_error=True,
            setup_error_clears_regression=False,
            setup_error_detail="undefined stream setup detail",
            excluded_not_exercised_streams=("audit_logs",),
        ),
        _read_result({"users": 2}),
        target_only_streams=("audit_logs",),
        extra_checks=(CheckResult(name="Shared stream final state", passed=False),),
    )

    assert model.verdict_label == "SETUP ERROR"
    assert "undefined stream setup detail" in model.verdict_detail
    assert "Target failed (exit 1)" in model.verdict_detail
    assert "failed checks: Shared stream final state" in model.verdict_detail
    assert "REGRESSION DETECTED" in model.verdict_detail


@pytest.mark.parametrize(
    "flags,stopped,strict,expected_label,details",
    [
        pytest.param(
            {
                "setup_error": True,
                "setup_error_detail": "undefined stream setup detail",
                "could_not_test": True,
                "could_not_test_detail": "config error detail",
                "excluded_not_exercised_streams": ("undefined", "config"),
            },
            True,
            False,
            "INCOMPLETE",
            (
                "stopped early",
                "undefined stream setup detail",
                "config error detail",
                "1 stream(s) the control did not read returned no records: empty",
            ),
            id="incomplete-precedes-setup-error",
        ),
        pytest.param(
            {
                "setup_error": True,
                "setup_error_detail": "undefined stream setup detail",
                "could_not_test": True,
                "could_not_test_detail": "config error detail",
                "excluded_not_exercised_streams": ("undefined", "config"),
            },
            False,
            True,
            "SETUP ERROR",
            (
                "undefined stream setup detail",
                "config error detail",
                "1 stream(s) the control did not read returned no records: empty",
                "failed checks: shared state",
            ),
            id="setup-error-precedes-fail",
        ),
        pytest.param(
            {
                "could_not_test": True,
                "could_not_test_detail": "config error detail",
                "excluded_not_exercised_streams": ("config",),
            },
            False,
            True,
            "FAIL (regression)",
            (
                "config error detail",
                "1 stream(s) the control did not read returned no records: empty",
                "failed checks: shared state",
            ),
            id="strict-fail-precedes-config-error",
        ),
        pytest.param(
            {
                "could_not_test": True,
                "could_not_test_detail": "config error detail",
                "excluded_not_exercised_streams": ("config",),
            },
            False,
            False,
            "COULD NOT TEST (config error)",
            (
                "config error detail",
                "1 stream(s) the control did not read returned no records: empty",
            ),
            id="config-error-precedes-not-exercised",
        ),
        pytest.param(
            {},
            False,
            False,
            "NOT EXERCISED",
            ("1 stream(s) the control did not read returned no records: empty",),
            id="not-exercised-precedes-pass",
        ),
    ],
)
def test_target_only_verdict_precedence_keeps_each_applicable_reason(
    flags, stopped, strict, expected_label, details
):
    result_flags = dict(flags)
    if stopped:
        result_flags["stopped_early"] = _STOPPED
    strict_checks = (
        (CheckResult(name="shared state", passed=False, summary="state differs"),)
        if strict
        else ()
    )
    target_only_streams = (
        ("undefined", "config", "empty")
        if "setup_error" in result_flags
        else ("config", "empty")
        if "could_not_test" in result_flags
        else ("empty",)
    )
    model = _comparison(
        "read",
        _read_result({"users": 2}, **result_flags),
        _read_result({"users": 2}, stopped_early=_STOPPED if stopped else None),
        target_only_streams=target_only_streams,
        extra_checks=strict_checks,
    )

    assert model.verdict_label == expected_label
    assert all(detail in model.verdict_detail for detail in details)


def test_a_target_only_stream_with_records_changes_nothing():
    target = _read_result({"users": 3, "audit_logs": 1})
    control = _read_result({"users": 3})
    model = _comparison(
        "read",
        target,
        control,
        configured_streams=("audit_logs", "users"),
        target_only_streams=("audit_logs",),
    )
    baseline = _comparison(
        "read", target, control, configured_streams=("audit_logs", "users")
    )

    assert model.not_exercised is False
    assert model.verdict_label == "PASS"
    assert (model.passed, model.verdict_label, model.verdict_detail) == (
        baseline.passed,
        baseline.verdict_label,
        baseline.verdict_detail,
    )
    assert render_inline_summary(model) == render_inline_summary(baseline)


def test_identical_catalogs_on_both_sides_keep_the_rule_silent():
    """One catalog for both sides is the default, an empty set, and an empty
    set is what the CLI computes from it: a stream empty on both sides is the
    stream-coverage warning, not an unexercised stream."""
    target, control = _read_result({"users": 3}), _read_result({"users": 3})
    by_default = _comparison(
        "read", target, control, configured_streams=("audit_logs", "users")
    )
    explicit = _comparison(
        "read",
        target,
        control,
        configured_streams=("audit_logs", "users"),
        target_only_streams=(),
    )

    for model in (by_default, explicit):
        assert model.not_exercised is False
        assert model.passed is True
        assert model.verdict_label == "PASS"
        assert model.context.not_exercised_note is None
        checks = {check.name: check for check in model.checks}
        assert checks["Stream coverage"].status == "warn"
    assert render_inline_summary(by_default) == render_inline_summary(explicit)


def test_a_stop_outranks_an_unexercised_stream_and_names_it_in_the_context():
    """Both flags are up; the Result line is the stop's, word for word, and the
    stream goes in the context block below it."""
    model = _comparison(
        "read",
        _read_result({"users": 3}, stopped_early=_STOPPED),
        _read_result({"users": 3}, stopped_early=_STOPPED),
        target_only_streams=("audit_logs",),
    )
    note = f"Not exercised: {_NOT_EXERCISED_DETAIL}"

    assert model.passed is False
    assert model.not_exercised is True
    assert model.verdict_label == "INCOMPLETE"
    assert (
        model.verdict_detail == "stopped early (timeout) after 1,234 records per side"
    )
    assert model.context.not_exercised_note == note

    summary = render_inline_summary(model)
    assert (
        "**Result:** ❌ INCOMPLETE — stopped early (timeout) after 1,234 records "
        "per side" in summary
    )
    assert "NOT EXERCISED" not in summary
    assert f"- {note}" in summary
    assert summary.index("- Target: stopped early") < summary.index(f"- {note}")

    html = render_html_report(model)
    assert "INCOMPLETE" in html
    assert f"<dt>Not exercised</dt><dd>{note}</dd>" in html
