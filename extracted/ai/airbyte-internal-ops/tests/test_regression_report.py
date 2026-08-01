# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for the regression-test report model and its two renderers."""

import re
from dataclasses import replace
from pathlib import Path

import pytest

from airbyte_ops_mcp.regression_tests.ci_output import (
    ARTIFACT_NAME_PREFIX,
    evaluate_comparison_outcome,
    github_artifact_name,
)
from airbyte_ops_mcp.regression_tests.report import (
    HTML_REPORT_FILENAME,
    INLINE_STREAM_TABLE_COLLAPSE_THRESHOLD,
    MAX_DIFF_LINES_PER_BLOCK,
    MAX_INLINE_STREAM_ROWS,
    MAX_LABEL_CHARS,
    MAX_LINE_CHARS,
    MAX_OUTPUT_TAIL_BYTES,
    MAX_STREAM_SECTIONS,
    META_MARKER,
    RECORD_COUNTS_TABLE,
    CheckResult,
    DiffLine,
    build_comparison_report_model,
    build_diff_block,
    build_json_block,
    build_single_version_report_model,
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
        extra_checks=(CheckResult(name="--> <script>alert(1)</script>", passed=False),),
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
