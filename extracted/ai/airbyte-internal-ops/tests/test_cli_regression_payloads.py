# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for the regression-test CLI's logged verdict payloads."""

from __future__ import annotations

import json
import re

import pytest

from airbyte_ops_mcp.cli import cloud
from airbyte_ops_mcp.regression_tests.models import Command

pytestmark = pytest.mark.unit


@pytest.fixture
def stub_run(monkeypatch):
    """Stub out Docker, telemetry and CI side effects; capture the GitHub outputs.

    The step summary is captured rather than discarded, so tests can assert on
    what a reviewer would actually read.
    """
    gh_outputs: dict[str, object] = {}
    step_summary: list[str] = []

    monkeypatch.setattr(cloud, "ensure_image_available", lambda _image: True)
    monkeypatch.setattr(cloud, "track_regression_test", lambda **_kwargs: None)
    monkeypatch.setattr(cloud, "write_github_summary", step_summary.append)
    monkeypatch.setattr(cloud, "write_github_outputs", gh_outputs.update)

    def _install(result: dict) -> dict[str, object]:
        def _fake_run(*, command: Command, output_dir, **_kwargs) -> dict:
            output_dir.mkdir(parents=True, exist_ok=True)
            return {"command": command.value, **result}

        monkeypatch.setattr(cloud, "_run_connector_command", _fake_run)
        return gh_outputs

    _install.step_summary = step_summary

    return _install


_ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*m")


def _logged_payload(captured: str) -> dict:
    """Parse the first complete JSON object the CLI printed to stdout.

    `raw_decode` stops at the end of that object, so unrelated output around it --
    a second payload, or a brace inside a log line -- cannot corrupt the parse.
    Colour codes are stripped first: `print_json` syntax-highlights whenever the
    terminal supports it, which would otherwise make these tests pass only under
    a dumb terminal.
    """
    plain = _ANSI_ESCAPE.sub("", captured)
    obj, _end = json.JSONDecoder().raw_decode(plain[plain.index("{") :])
    return obj


@pytest.mark.parametrize(
    "connection_status,expected_success",
    [
        pytest.param("SUCCEEDED", True, id="check-connected"),
        pytest.param("FAILED", False, id="check-failed-status-despite-clean-exit"),
        pytest.param(None, False, id="check-missing-status-fails-closed"),
    ],
)
def test_single_version_check_logs_the_verdict_not_the_exit_status(
    tmp_path, capsys, stub_run, connection_status, expected_success
):
    """The logged payload must not read as a pass when the verdict is a failure.

    `result["success"]` is the container exit status, and CHECK exits 0 even when
    the connector cannot connect -- so printing it unqualified would contradict
    the `success` output, the report and the workflow verdict.
    """
    gh_outputs = stub_run(
        {
            "success": True,  # exited cleanly
            "exit_code": 0,
            "connection_status": connection_status,
            "message_counts": {},
            "record_counts_per_stream": {},
        }
    )

    cloud.regression_test(
        skip_compare=True,
        test_image="airbyte/source-test:2.0.0",
        command="check",
        output_dir=str(tmp_path),
    )

    payload = _logged_payload(capsys.readouterr().out)

    assert payload["success"] is expected_success
    assert payload["exited_cleanly"] is True
    assert gh_outputs["success"] is expected_success


def test_single_version_spec_verdict_is_the_exit_status(tmp_path, capsys, stub_run):
    """For non-CHECK commands the exit status is the verdict, and both are logged."""
    gh_outputs = stub_run(
        {
            "success": False,
            "exit_code": 1,
            "message_counts": {},
            "record_counts_per_stream": {},
        }
    )

    cloud.regression_test(
        skip_compare=True,
        test_image="airbyte/source-test:2.0.0",
        command="spec",
        output_dir=str(tmp_path),
    )

    payload = _logged_payload(capsys.readouterr().out)

    assert payload["success"] is False
    assert payload["exited_cleanly"] is False
    assert gh_outputs["success"] is False


def test_single_version_emits_the_html_report_and_a_concise_summary(
    tmp_path, capsys, stub_run
):
    """`--skip-compare` gets both surfaces too, and the summary stays short."""
    stub_run(
        {
            "success": True,
            "exit_code": 0,
            "message_counts": {"SPEC": 1},
            "record_counts_per_stream": {},
        }
    )

    cloud.regression_test(
        skip_compare=True,
        test_image="airbyte/source-test:2.0.0",
        command="spec",
        output_dir=str(tmp_path),
    )
    capsys.readouterr()

    assert (tmp_path / "report.html").read_text().startswith("<!DOCTYPE html>")

    summary = "\n".join(stub_run.step_summary)
    assert summary.startswith("## `SPEC` Test Results")
    assert "| Check | Result | Details |" in summary
    # The old path appended a metric table *and* the whole report; now one block.
    assert len(stub_run.step_summary) == 1
    assert "Execution details" not in summary


@pytest.mark.parametrize(
    "command,expects_coverage",
    [
        pytest.param("read", True, id="read-reads-records"),
        pytest.param("spec", False, id="spec-cannot"),
        pytest.param("discover", False, id="discover-cannot"),
    ],
)
def test_only_record_reading_commands_get_stream_coverage(
    tmp_path, capsys, stub_run, command, expects_coverage
):
    """`--connection-id` fetches a catalog for every command, not just `read`.

    Handing it to a command that cannot emit records would produce an all-zero
    stream table and a warning that no stream returned anything -- true,
    meaningless, and enough noise to devalue the warning where it matters.
    """
    catalog = tmp_path / "catalog.json"
    catalog.write_text(
        json.dumps(
            {
                "streams": [
                    {
                        "stream": {
                            "name": "users",
                            "json_schema": {},
                            "supported_sync_modes": ["full_refresh"],
                        },
                        "sync_mode": "full_refresh",
                        "destination_sync_mode": "append",
                    }
                ]
            }
        )
    )
    stub_run(
        {
            "success": True,
            "exit_code": 0,
            "message_counts": {},
            "record_counts_per_stream": {},
        }
    )

    cloud.regression_test(
        skip_compare=True,
        test_image="airbyte/source-test:2.0.0",
        command=command,
        catalog_path=str(catalog),
        output_dir=str(tmp_path / command),
    )
    capsys.readouterr()

    summary = "\n".join(stub_run.step_summary)
    assert ("Stream coverage" in summary) is expects_coverage
    assert ("| `users` |" in summary) is expects_coverage


def test_consolidate_command_folds_a_runs_reports_into_one_page(tmp_path, capsys):
    """The CLI entry point CI uses to build the run-level report."""
    from airbyte_ops_mcp.regression_tests.report import (
        build_single_version_report_model,
        write_html_report,
    )

    for command in ("spec", "read"):
        (tmp_path / command).mkdir()
        write_html_report(
            build_single_version_report_model(
                connector_image="airbyte/source-test:2.0.0",
                command=command,
                result={"success": True, "exit_code": 0},
            ),
            tmp_path / command,
        )

    cloud.consolidate_regression_reports(str(tmp_path))
    capsys.readouterr()

    consolidated = (tmp_path / "report.html").read_text()
    assert 'id="command-spec"' in consolidated
    assert 'id="command-read"' in consolidated


def test_consolidate_command_is_a_no_op_when_there_is_nothing_to_fold(tmp_path, capsys):
    """A run that produced no report must not fail the workflow step."""
    cloud.consolidate_regression_reports(str(tmp_path))

    # Colour codes stripped and wrapping undone: rich decides both from the
    # terminal, and neither is what this test is about.
    printed = " ".join(_ANSI_ESCAPE.sub("", capsys.readouterr().out).split())
    assert "nothing to consolidate" in printed
    assert not (tmp_path / "report.html").exists()


@pytest.fixture
def stub_comparison_run(monkeypatch, tmp_path):
    """Stub the comparison-mode path; capture the results handed to the report."""
    seen: dict[str, object] = {}

    monkeypatch.setattr(cloud, "ensure_image_available", lambda _image: True)
    monkeypatch.setattr(cloud, "track_regression_test", lambda **_kwargs: None)
    monkeypatch.setattr(
        cloud,
        "write_github_summary",
        lambda text: seen.setdefault("step_summary", []).append(text),
    )
    monkeypatch.setattr(cloud, "write_github_outputs", lambda outputs: None)
    monkeypatch.setattr(
        cloud, "write_json_output", lambda _key, data: seen.update(json_output=data)
    )

    def _fake_report(*, target_result, control_result, output_dir, **_kwargs):
        seen["report_target"] = target_result
        seen["report_control"] = control_result
        output_dir.mkdir(parents=True, exist_ok=True)
        report = output_dir / "report.md"
        report.write_text("stub report")
        return report

    monkeypatch.setattr(cloud, "generate_regression_report", _fake_report)

    def _install(target: dict, control: dict) -> dict[str, object]:
        def _fake_run(*, command: Command, target_or_control, output_dir, **_kwargs):
            output_dir.mkdir(parents=True, exist_ok=True)
            side = (
                target if target_or_control is cloud.TargetOrControl.TARGET else control
            )
            return {"command": command.value, **side}

        monkeypatch.setattr(cloud, "_run_with_optional_http_metrics", _fake_run)
        return seen

    return _install


def test_comparison_payload_reports_per_side_verdicts(
    tmp_path, capsys, stub_comparison_run
):
    """Nested `success` must be the side's verdict, not its exit status.

    An agent reading the payload goes to the block naming the version it cares
    about, so `target.success` has to mean "this side passed" the same way the
    top-level `success` does -- for a CHECK that exits 0 without connecting, the
    exit status would say `true` for the side that regressed.
    """
    seen = stub_comparison_run(
        {
            "success": True,
            "exit_code": 0,
            "connection_status": "FAILED",
            "message_counts": {},
            "record_counts_per_stream": {},
        },
        {
            "success": True,
            "exit_code": 0,
            "connection_status": "SUCCEEDED",
            "message_counts": {},
            "record_counts_per_stream": {},
        },
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="check",
        output_dir=str(tmp_path),
    )

    payload = _logged_payload(capsys.readouterr().out)

    assert payload["success"] is False
    assert payload["regression_detected"] is True
    assert payload["target"]["success"] is False
    assert payload["target"]["exited_cleanly"] is True
    assert payload["control"]["success"] is True
    assert payload["control"]["exited_cleanly"] is True
    # The `regression_report` output carries the same annotated payload.
    assert seen["json_output"]["target"]["success"] is False


def test_report_generator_still_receives_the_raw_exit_status(
    tmp_path, capsys, stub_comparison_run
):
    """The report reads `success` as the exit status, so it must get the originals.

    Annotating in place would make `_describe_run` describe a clean exit as a
    crash ("exited 0 after reporting connectionStatus FAILED").
    """
    seen = stub_comparison_run(
        {
            "success": True,
            "exit_code": 0,
            "connection_status": "FAILED",
            "message_counts": {},
            "record_counts_per_stream": {},
        },
        {
            "success": True,
            "exit_code": 0,
            "connection_status": "SUCCEEDED",
            "message_counts": {},
            "record_counts_per_stream": {},
        },
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="check",
        output_dir=str(tmp_path),
    )
    capsys.readouterr()

    assert seen["report_target"]["success"] is True
    assert "exited_cleanly" not in seen["report_target"]
    assert seen["report_control"]["success"] is True
    # The HTML report and the step summary read `success` the same way, so the
    # same mistake would degrade the most-read line of both surfaces: a clean
    # exit described as a crash. Pin it where a reviewer would see it.
    summary = "\n".join(seen["step_summary"])
    assert "connectionStatus FAILED" in summary
    assert "exited 0 after reporting" not in summary


def test_comparison_mode_emits_the_html_report_and_a_concise_summary(
    tmp_path, capsys, stub_comparison_run
):
    """Both new surfaces must actually be produced by the comparison path.

    The step summary and the workflow both advertise `report.html`, so a missing
    one is a broken promise rather than a missing extra.
    """
    side = {
        "success": True,
        "exit_code": 0,
        "message_counts": {"RECORD": 5},
        "record_counts_per_stream": {"users": 5},
    }
    seen = stub_comparison_run(dict(side), dict(side))

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
    )
    capsys.readouterr()

    html = (tmp_path / "report.html").read_text()
    assert html.startswith("<!DOCTYPE html>")
    assert "airbyte/source-test:2.0.0" in html

    summary = "\n".join(seen["step_summary"])
    assert summary.startswith("## `READ` Test Results")
    assert "| Check | Result | Details |" in summary
    assert "report.html" in summary
    # Concise, not the whole report: no execution details, no full markdown dump.
    assert "Execution details" not in summary
    assert len(summary) < 2_000
