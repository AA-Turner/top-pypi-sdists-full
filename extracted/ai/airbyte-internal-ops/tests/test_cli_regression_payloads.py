# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for the regression-test CLI's logged verdict payloads."""

from __future__ import annotations

import contextlib
import json
import re

import pytest
from airbyte_protocol.models import (
    AirbyteCatalog,
    AirbyteStream,
    ConnectorSpecification,
    SyncMode,
)

from airbyte_ops_mcp.cli import cloud
from airbyte_ops_mcp.regression_tests.http_metrics import (
    HttpMetrics,
    MitmproxySession,
)
from airbyte_ops_mcp.regression_tests.models import Command, ComparableOutputs

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
        def _fake_run(*, command: Command, output_dir, **_kwargs):
            output_dir.mkdir(parents=True, exist_ok=True)
            return {"command": command.value, **result}, ComparableOutputs()

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

    def _install(
        target: dict,
        control: dict,
        target_outputs: ComparableOutputs | None = None,
        control_outputs: ComparableOutputs | None = None,
    ) -> dict[str, object]:
        calls: list[dict] = []
        seen["calls"] = calls

        def _fake_run(*, command: Command, target_or_control, output_dir, **kwargs):
            output_dir.mkdir(parents=True, exist_ok=True)
            is_target = target_or_control is cloud.TargetOrControl.TARGET
            side = target if is_target else control
            declared = target_outputs if is_target else control_outputs

            calls.append({"role": target_or_control, **kwargs})
            result = {"command": command.value, **side}
            if kwargs.get("enable_http_metrics"):
                # Mirrors the real runner: the dump and its metrics only exist
                # when the proxy ran.
                result["http_dump_file"] = str(output_dir / "http_traffic.mitm")
                result["http_metrics"] = {
                    "flow_count": 0,
                    "duplicate_flow_count": 0,
                }
            return result, declared or ComparableOutputs()

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


_CLEAN_RUN = {
    "success": True,
    "exit_code": 0,
    "message_counts": {},
    "record_counts_per_stream": {},
}


def _spec_outputs(properties: dict, required: list[str] | None = None):
    """A side that emitted a spec with the given config properties."""
    return ComparableOutputs(
        spec=ConnectorSpecification(
            connectionSpecification={
                "type": "object",
                "required": required or [],
                "properties": properties,
            }
        )
    )


def _catalog_outputs(json_schema: dict, name: str = "users"):
    """A side that discovered one stream with the given schema."""
    return ComparableOutputs(
        catalog=AirbyteCatalog(
            streams=[
                AirbyteStream(
                    name=name,
                    json_schema=json_schema,
                    supported_sync_modes=[SyncMode.full_refresh],
                )
            ]
        )
    )


def _state_outputs(final_states: dict):
    """A side that finished a read leaving this state per stream.

    Named streams here, keyed on `(namespace, name)` for the comparison the way
    extraction hands them over.
    """
    return ComparableOutputs(
        final_states={(None, name): state for name, state in final_states.items()}
    )


def test_a_removed_spec_property_fails_a_run_whose_commands_both_passed(
    tmp_path, capsys, stub_comparison_run
):
    """The gap this closes: `spec` exits 0 no matter what the spec says.

    Without the comparison the two clean exits are the whole verdict, and a
    connector that dropped a config field ships.
    """
    seen = stub_comparison_run(
        dict(_CLEAN_RUN),
        dict(_CLEAN_RUN),
        target_outputs=_spec_outputs({"api_key": {"type": "string"}}),
        control_outputs=_spec_outputs(
            {"api_key": {"type": "string"}, "start_date": {"type": "string"}}
        ),
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="spec",
        output_dir=str(tmp_path),
    )

    payload = _logged_payload(capsys.readouterr().out)

    assert payload["success"] is False
    # Both commands ran cleanly, so the outcome alone would have said no
    # regression: the finding has to reach the flag the workflow reads.
    assert payload["both_succeeded"] is True
    assert payload["regression_detected"] is True
    assert payload["comparison"]["spec"]["breaking_changes"] == [
        "`connectionSpecification.properties.start_date` was removed"
    ]

    summary = "\n".join(seen["step_summary"])
    assert "Spec compatibility" in summary
    assert "start_date" in summary


def test_an_added_optional_spec_property_passes(tmp_path, capsys, stub_comparison_run):
    """The additive case still passes, and says what was added."""
    seen = stub_comparison_run(
        dict(_CLEAN_RUN),
        dict(_CLEAN_RUN),
        target_outputs=_spec_outputs(
            {"api_key": {"type": "string"}, "page_size": {"type": "integer"}}
        ),
        control_outputs=_spec_outputs({"api_key": {"type": "string"}}),
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="spec",
        output_dir=str(tmp_path),
    )

    payload = _logged_payload(capsys.readouterr().out)

    assert payload["success"] is True
    assert payload["regression_detected"] is False
    assert payload["comparison"]["spec"]["compatible_changes"] == [
        "`connectionSpecification.properties.page_size` was added"
    ]
    assert "page_size" in "\n".join(seen["step_summary"])


def test_a_discovered_schema_change_fails_the_run(
    tmp_path, capsys, stub_comparison_run
):
    """`discover` gets the same treatment, strictly."""
    seen = stub_comparison_run(
        dict(_CLEAN_RUN),
        dict(_CLEAN_RUN),
        target_outputs=_catalog_outputs(
            {"type": "object", "properties": {"id": {"type": "string"}}}
        ),
        control_outputs=_catalog_outputs(
            {"type": "object", "properties": {"id": {"type": "integer"}}}
        ),
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="discover",
        output_dir=str(tmp_path),
    )

    payload = _logged_payload(capsys.readouterr().out)

    assert payload["success"] is False
    assert payload["comparison"]["catalog_schema"]["changed_streams"] == ["users"]
    # The diff itself has to survive the trip into the payload.
    assert payload["comparison"]["catalog_schema"]["streams"]["users"]["diff"]
    assert "Catalog schema" in "\n".join(seen["step_summary"])


def test_the_report_shows_what_changed_not_just_that_something_did(
    tmp_path, capsys, stub_comparison_run
):
    """A one-line check row cannot answer "which field?", so the diff ships too."""
    stub_comparison_run(
        dict(_CLEAN_RUN),
        dict(_CLEAN_RUN),
        target_outputs=_catalog_outputs(
            {"type": "object", "properties": {"id": {"type": "string"}}}
        ),
        control_outputs=_catalog_outputs(
            {"type": "object", "properties": {"id": {"type": "integer"}}}
        ),
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="discover",
        output_dir=str(tmp_path),
    )
    capsys.readouterr()
    html = (tmp_path / "report.html").read_text()

    assert "Schema diff — users" in html
    # The field, and both of its types: the answer to "which field changed?"
    assert "values_changed" in html
    assert "&#39;id&#39;" in html
    assert "integer" in html and "string" in html


def test_a_comparison_that_cannot_run_is_not_reported_as_a_regression(
    tmp_path, stub_comparison_run, monkeypatch
):
    """A tooling failure must not be announced as the connector regressing.

    Catching it here produced exactly that: `regression_detected: true` and
    "REGRESSION DETECTED" over a run where nothing was ever compared. It
    propagates instead, and the workflow's `internal_failure` path calls it what
    it is — an infrastructure error, with the artifacts still uploaded.
    """

    def _boom(*_args, **_kwargs):
        raise TypeError("unexpected spec shape")

    monkeypatch.setattr(cloud, "compare_specs", _boom)
    stub_comparison_run(dict(_CLEAN_RUN), dict(_CLEAN_RUN))

    with pytest.raises(TypeError, match="unexpected spec shape"):
        cloud.regression_test(
            test_image="airbyte/source-test:2.0.0",
            control_image="airbyte/source-test:1.0.0",
            command="spec",
            output_dir=str(tmp_path),
        )


def test_a_catalog_that_only_grew_warns_instead_of_failing(
    tmp_path, capsys, stub_comparison_run
):
    """Connectors add streams constantly; a red on every one of them is ignored.

    The change is still reported — the row, the findings list and the payload
    all carry it — it just does not gate the release.
    """
    seen = stub_comparison_run(
        dict(_CLEAN_RUN),
        dict(_CLEAN_RUN),
        target_outputs=_catalog_outputs(
            {
                "type": "object",
                "properties": {"id": {"type": "integer"}, "email": {"type": "string"}},
            }
        ),
        control_outputs=_catalog_outputs(
            {"type": "object", "properties": {"id": {"type": "integer"}}}
        ),
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="discover",
        output_dir=str(tmp_path),
    )

    payload = _logged_payload(capsys.readouterr().out)

    assert payload["success"] is True
    assert payload["regression_detected"] is False
    # Reported, not hidden: the payload says why a `passed: false` did not gate.
    assert payload["comparison"]["catalog_schema"]["passed"] is False
    assert payload["comparison"]["catalog_schema"]["additive_only"] is True

    summary = "\n".join(seen["step_summary"])
    assert "| Catalog schema | ⚠️ |" in summary
    assert "Stream users has schema differences" in summary


def test_a_removed_stream_still_fails_the_run(tmp_path, capsys, stub_comparison_run):
    """The additive exemption must not swallow a destructive change beside it."""
    stub_comparison_run(
        dict(_CLEAN_RUN),
        dict(_CLEAN_RUN),
        target_outputs=_catalog_outputs({"type": "object"}, name="brand_new"),
        control_outputs=_catalog_outputs({"type": "object"}, name="vanished"),
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="discover",
        output_dir=str(tmp_path),
    )

    payload = _logged_payload(capsys.readouterr().out)

    assert payload["success"] is False
    assert payload["regression_detected"] is True
    assert payload["comparison"]["catalog_schema"]["additive_only"] is False


def test_the_report_carries_findings_the_check_row_truncates(
    tmp_path, capsys, stub_comparison_run
):
    """The step summary pointed at a report that did not carry the rest.

    A stream that is missing or new has no schema diff, so with the row showing
    only the first three, five of eight findings appeared nowhere in the HTML.
    """
    gone = [f"gone_{index}" for index in range(4)]
    fresh = [f"new_{index}" for index in range(4)]

    def _catalog_of(names):
        return ComparableOutputs(
            catalog=AirbyteCatalog(
                streams=[
                    AirbyteStream(
                        name=name,
                        json_schema={"type": "object"},
                        supported_sync_modes=[SyncMode.full_refresh],
                    )
                    for name in names
                ]
            )
        )

    seen = stub_comparison_run(
        dict(_CLEAN_RUN),
        dict(_CLEAN_RUN),
        target_outputs=_catalog_of(fresh),
        control_outputs=_catalog_of(gone),
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="discover",
        output_dir=str(tmp_path),
    )
    capsys.readouterr()
    html = (tmp_path / "report.html").read_text()

    assert [name for name in gone + fresh if name not in html] == []
    assert "All 8 findings" in html
    # The step summary lists them too, so neither surface is the thin one.
    summary = "\n".join(seen["step_summary"])
    assert [name for name in gone + fresh if name not in summary] == []


def test_an_oversized_catalog_diff_is_bounded_and_says_so(
    tmp_path, capsys, stub_comparison_run, monkeypatch
):
    """The payload goes to `GITHUB_OUTPUT`, which is size-limited.

    Dropping a diff silently would read as "nothing more to see", so the payload
    names what it dropped and the run says it on the console.
    """
    monkeypatch.setattr(cloud, "_MAX_DIFF_PAYLOAD_CHARS", 10)
    stub_comparison_run(
        dict(_CLEAN_RUN),
        dict(_CLEAN_RUN),
        target_outputs=_catalog_outputs(
            {"type": "object", "properties": {"id": {"type": "string"}}}
        ),
        control_outputs=_catalog_outputs(
            {"type": "object", "properties": {"id": {"type": "integer"}}}
        ),
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="discover",
        output_dir=str(tmp_path),
    )
    captured = capsys.readouterr().out
    payload = _logged_payload(captured)

    users = payload["comparison"]["catalog_schema"]["streams"]["users"]
    assert "diff" not in users
    assert users["diff_omitted"]
    assert payload["comparison"]["catalog_schema"]["streams_with_omitted_diffs"] == [
        "users"
    ]
    # The verdict is unaffected: the change was still found.
    assert payload["success"] is False
    assert "too large" in " ".join(_ANSI_ESCAPE.sub("", captured).split())
    # And the report says which diff it dropped, rather than skipping it in
    # silence -- a missing block otherwise reads as "nothing to see".
    html = (tmp_path / "report.html").read_text()
    assert "Schema diffs omitted for size" in html
    assert "catalog.jsonl" in html


def test_the_payload_caps_how_many_streams_it_lists(
    tmp_path, capsys, stub_comparison_run, monkeypatch
):
    """Diffs were bounded; one line per stream was not.

    A wide source has thousands of streams, and an entry each is enough to
    exceed the same `GITHUB_OUTPUT` budget without a single diff attached.
    """
    monkeypatch.setattr(cloud, "_MAX_PAYLOAD_STREAMS", 2)
    changed = {"type": "object", "properties": {"id": {"type": "string"}}}
    unchanged = {"type": "object", "properties": {"id": {"type": "integer"}}}

    def _catalog_of(first_schema):
        return ComparableOutputs(
            catalog=AirbyteCatalog(
                streams=[
                    AirbyteStream(
                        name=name,
                        json_schema=first_schema if name == "aaa" else unchanged,
                        supported_sync_modes=[SyncMode.full_refresh],
                    )
                    for name in ("aaa", "bbb", "ccc", "ddd")
                ]
            )
        )

    stub_comparison_run(
        dict(_CLEAN_RUN),
        dict(_CLEAN_RUN),
        target_outputs=_catalog_of(changed),
        control_outputs=_catalog_of(unchanged),
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="discover",
        output_dir=str(tmp_path),
    )
    captured = capsys.readouterr().out
    catalog = _logged_payload(captured)["comparison"]["catalog_schema"]

    assert len(catalog["streams"]) == 2
    assert catalog["streams_omitted"] == 2
    # The changed stream is kept, not crowded out by the three that passed.
    assert "aaa" in catalog["streams"]
    assert "lists 2 of 4 streams" in " ".join(_ANSI_ESCAPE.sub("", captured).split())


def test_a_failed_command_is_not_also_reported_as_a_comparison_failure(
    tmp_path, capsys, stub_comparison_run
):
    """A crashed run has nothing to compare; saying so twice weakens the first."""
    stub_comparison_run(
        {**_CLEAN_RUN, "success": False, "exit_code": 1},
        dict(_CLEAN_RUN),
        control_outputs=_spec_outputs({"api_key": {"type": "string"}}),
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="spec",
        output_dir=str(tmp_path),
    )

    payload = _logged_payload(capsys.readouterr().out)

    assert payload["success"] is False
    assert payload["regression_detected"] is True
    assert "comparison" not in payload


def test_check_has_no_output_to_compare(tmp_path, capsys, stub_comparison_run):
    """`check` reports its own status, so it is the one command with nothing to diff."""
    stub_comparison_run(
        {**_CLEAN_RUN, "connection_status": "SUCCEEDED"},
        {**_CLEAN_RUN, "connection_status": "SUCCEEDED"},
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="check",
        output_dir=str(tmp_path),
    )

    payload = _logged_payload(capsys.readouterr().out)

    assert payload["success"] is True
    assert "comparison" not in payload


def test_a_restructured_final_state_fails_a_read_whose_commands_both_passed(
    tmp_path, capsys, stub_comparison_run
):
    """The gap this closes: a `read` that corrupts its state exits 0.

    Nothing else in the run looks at the state, so a dropped cursor key ships
    and the damage shows up as missed records on a customer's next sync.
    """
    seen = stub_comparison_run(
        dict(_CLEAN_RUN),
        dict(_CLEAN_RUN),
        target_outputs=_state_outputs({"users": {"updated_at": "2024-01-01"}}),
        control_outputs=_state_outputs(
            {"users": {"updated_at": "2024-01-01", "page": 3}}
        ),
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
    )

    payload = _logged_payload(capsys.readouterr().out)

    assert payload["success"] is False
    # Both commands ran cleanly, so the outcome alone would have said no
    # regression: the finding has to reach the flag the workflow reads.
    assert payload["both_succeeded"] is True
    assert payload["regression_detected"] is True

    final_state = payload["comparison"]["final_state"]
    assert final_state["value_only"] is False
    assert final_state["changed_streams"] == ["users"]
    # The diff itself has to survive the trip into the payload.
    assert final_state["streams"]["users"]["diff"]

    summary = "\n".join(seen["step_summary"])
    assert "| Final state per stream | ❌ |" in summary
    assert "State for users changed shape" in summary
    # And a reviewer's next question -- which key? -- is answered in the report.
    html = (tmp_path / "report.html").read_text()
    assert "Final state diff — users" in html
    assert "page" in html


def test_an_advanced_cursor_warns_instead_of_failing_the_read(
    tmp_path, capsys, stub_comparison_run
):
    """Both versions call the live API separately until HTTP replay lands.

    A timestamp cursor advances between the two runs on its own, so failing on
    it would redden every incremental read. It is still reported.
    """
    seen = stub_comparison_run(
        dict(_CLEAN_RUN),
        dict(_CLEAN_RUN),
        target_outputs=_state_outputs(
            {"users": {"updated_at": "2024-01-01T00:05:00Z"}}
        ),
        control_outputs=_state_outputs(
            {"users": {"updated_at": "2024-01-01T00:00:00Z"}}
        ),
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
    )

    payload = _logged_payload(capsys.readouterr().out)

    assert payload["success"] is True
    assert payload["regression_detected"] is False
    # Reported, not hidden: the payload says why a `passed: false` did not gate.
    assert payload["comparison"]["final_state"]["passed"] is False
    assert payload["comparison"]["final_state"]["value_only"] is True
    assert payload["comparison"]["final_state"]["inconclusive"] is False

    summary = "\n".join(seen["step_summary"])
    assert "| Final state per stream | ⚠️ |" in summary
    assert "State for users changed value" in summary


def test_a_read_that_emitted_no_state_is_warned_about_rather_than_passed(
    tmp_path, capsys, stub_comparison_run
):
    """A read that emitted no state at all cannot fail, and must not go green.

    Not the full-refresh case -- the CDK emits a terminal sentinel per stream
    there. This is a connector that emitted nothing, which is no fault of the
    target version; a check that passes over something it never looked at is how
    a silent state regression ships.
    """
    seen = stub_comparison_run(dict(_CLEAN_RUN), dict(_CLEAN_RUN))

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
    )

    payload = _logged_payload(capsys.readouterr().out)

    assert payload["success"] is True
    assert payload["comparison"]["final_state"]["passed"] is False
    assert (
        payload["comparison"]["final_state"]["message"]
        == "Neither version emitted any state; nothing was compared"
    )
    # Why it did not gate: nothing was compared -- not "every change was benign",
    # which is what reporting this through `value_only` would have claimed.
    assert payload["comparison"]["final_state"]["inconclusive"] is True
    assert payload["comparison"]["final_state"]["value_only"] is False
    assert "| Final state per stream | ⚠️ |" in "\n".join(seen["step_summary"])


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


def test_control_runs_before_target_in_comparison_mode(
    tmp_path, monkeypatch, stub_comparison_run
):
    """The whole directional design rests on this order: extra rows created
    upstream between the two live runs must land in the target output (where
    they are tolerated), not in the control output (where they would read as
    records missing from target). A reorder would invert the semantics with
    every other test still green."""
    side = {"success": True, "exit_code": 0}
    stub_comparison_run(dict(side), dict(side))

    inner = cloud._run_with_optional_http_metrics
    order: list[object] = []

    def _tracking(*, target_or_control, **kwargs):
        order.append(target_or_control)
        return inner(target_or_control=target_or_control, **kwargs)

    monkeypatch.setattr(cloud, "_run_with_optional_http_metrics", _tracking)

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
    )

    assert order == [cloud.TargetOrControl.CONTROL, cloud.TargetOrControl.TARGET]


def test_skip_record_comparison_gates_on_command_outcomes_only(
    tmp_path, capsys, monkeypatch, stub_comparison_run
):
    """The escape hatch for sources whose data changes between the two live
    runs: the record comparison must not even run, and the verdict is the
    command outcome alone."""
    side = {"success": True, "exit_code": 0}
    seen = stub_comparison_run(dict(side), dict(side))

    called: list[int] = []
    monkeypatch.setattr(
        cloud, "_compare_read_records", lambda **_kwargs: called.append(1)
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
        skip_record_comparison=True,
    )

    assert not called
    payload = _logged_payload(capsys.readouterr().out)
    assert payload["success"] is True
    assert payload["regression_detected"] is False
    assert "record_comparison" not in payload
    # The skip is visible on the report surfaces, not only on stdout: a
    # diagnostic (warn) row, so the run cannot read as a pass that
    # compared records.
    summary = "\n".join(seen["step_summary"])
    assert "Record comparison" in summary
    assert "records were not compared" in summary or "not compared" in summary


def test_an_errored_comparison_is_inconclusive_not_a_regression(
    tmp_path, capsys, monkeypatch, stub_comparison_run
):
    """A comparator crash fails the run (fail closed) but must not tell a
    connector developer their change caused a regression — same treatment
    as both_failed: success=false, regression_detected=false."""
    from airbyte_ops_mcp.regression_tests.regression import (
        ComparisonResult,
        RecordComparisonSummary,
    )

    side = {"success": True, "exit_code": 0}
    stub_comparison_run(dict(side), dict(side))
    errored_summary = RecordComparisonSummary(
        passed=False,
        errored=True,
        count_comparison=ComparisonResult(
            passed=False, message="Record comparison errored"
        ),
        errors=["Record comparison errored: OSError('boom')"],
    )
    monkeypatch.setattr(
        cloud, "_compare_read_records", lambda **_kwargs: (errored_summary, None)
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
    )

    captured = capsys.readouterr()
    payload = _logged_payload(captured.out)
    assert payload["success"] is False
    assert payload["regression_detected"] is False
    assert payload["record_comparison"]["errored"] is True
    # Errors go to stderr, and the console wraps long lines — normalize.
    assert "tooling failure, not evidence of a regression" in " ".join(
        captured.err.split()
    )


# --------------------------------------------------------------------------
# HTTP replay: the target run is served the control run's recorded responses
# --------------------------------------------------------------------------

_CLEAN_SIDE = {
    "success": True,
    "exit_code": 0,
    "message_counts": {"RECORD": 5},
    "record_counts_per_stream": {"users": 5},
}


def test_the_target_replays_the_dump_the_control_run_recorded(
    tmp_path, capsys, stub_comparison_run
):
    """Getting this wiring wrong disables replay silently rather than failing.

    The control-before-target order it depends on is pinned separately by
    `test_control_runs_before_target_in_comparison_mode`.
    """
    seen = stub_comparison_run(dict(_CLEAN_SIDE), dict(_CLEAN_SIDE))

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
        enable_http_replay=True,
    )
    capsys.readouterr()

    control_call, target_call = seen["calls"]
    assert control_call["role"] is cloud.TargetOrControl.CONTROL
    # Replay is a use of the capture, so asking for it turns the capture on.
    assert control_call["enable_http_metrics"] is True
    assert control_call.get("replay_from") is None
    assert target_call["replay_from"] == tmp_path / "control" / "http_traffic.mitm"


def test_replay_is_on_by_default_in_comparison_mode(
    tmp_path, capsys, stub_comparison_run
):
    """No flag at all still replays, and turns the capture on to do it."""
    seen = stub_comparison_run(dict(_CLEAN_SIDE), dict(_CLEAN_SIDE))

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
    )
    capsys.readouterr()

    control_call, target_call = seen["calls"]
    assert control_call["enable_http_metrics"] is True
    assert target_call["replay_from"] == tmp_path / "control" / "http_traffic.mitm"


def test_no_http_replay_runs_both_versions_live(tmp_path, capsys, stub_comparison_run):
    """The opt-out has to reach the runs, not just the flag parser."""
    seen = stub_comparison_run(dict(_CLEAN_SIDE), dict(_CLEAN_SIDE))

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
        enable_http_replay=False,
    )
    capsys.readouterr()

    assert [call.get("replay_from") for call in seen["calls"]] == [None, None]


def test_single_version_mode_does_not_complain_about_the_replay_default(
    tmp_path, capsys, stub_run
):
    """Replay is comparison-only, so `--skip-compare` simply has none of it.

    The default landing somewhere it cannot apply is not worth a warning on
    every single-version run; only an explicit request is.
    """
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
        command="spec",
        output_dir=str(tmp_path),
    )

    printed = " ".join(_ANSI_ESCAPE.sub("", capsys.readouterr().out).split())
    assert "needs a control run" not in printed


def test_replay_tuning_reaches_the_target_run(tmp_path, capsys, stub_comparison_run):
    """The knobs exist for connectors that need them; pin that they arrive."""
    seen = stub_comparison_run(dict(_CLEAN_SIDE), dict(_CLEAN_SIDE))

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
        enable_http_replay=True,
        http_replay_max_body="10m",
        http_replay_max_dump_size_mb=64,
        http_replay_reuse=True,
        http_replay_ignore_params="timestamp, nonce",
        strict_replay=True,
    )
    capsys.readouterr()

    control_call, target_call = seen["calls"]
    options = target_call["replay_options"]
    assert options.reuse is True
    assert options.extra == "kill"
    assert options.ignore_params == ("timestamp", "nonce")
    assert options.max_dump_bytes == 64 * 1024 * 1024
    # The body threshold governs recording, so both sides get it.
    assert control_call["stream_large_bodies"] == "10m"
    assert target_call["stream_large_bodies"] == "10m"


def test_replay_tuning_without_replay_says_it_is_being_ignored(
    tmp_path, capsys, stub_comparison_run
):
    """Silence here reads as "strict mode found nothing wrong"."""
    stub_comparison_run(dict(_CLEAN_SIDE), dict(_CLEAN_SIDE))

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
        enable_http_replay=False,
        strict_replay=True,
    )

    printed = " ".join(_ANSI_ESCAPE.sub("", capsys.readouterr().out).split())
    assert "do nothing with --no-http-replay" in printed


def test_the_recording_threshold_is_not_reported_as_an_ignored_replay_flag(
    tmp_path, capsys, stub_comparison_run
):
    """`--http-replay-max-body` governs recording, so it applies on its own.

    Pinned with replay explicitly off, the only case where the ignored-flags
    warning can fire at all.
    """
    seen = stub_comparison_run(dict(_CLEAN_SIDE), dict(_CLEAN_SIDE))

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
        enable_http_replay=False,
        enable_http_metrics=True,
        http_replay_max_body="10m",
    )

    printed = " ".join(_ANSI_ESCAPE.sub("", capsys.readouterr().out).split())
    assert "do nothing with --no-http-replay" not in printed
    assert all(call["stream_large_bodies"] == "10m" for call in seen["calls"])


def test_an_oversized_dump_is_not_left_on_the_runners_disk(
    tmp_path, capsys, monkeypatch, stub_comparison_run
):
    """Recording bodies makes dumps grow with everything the run downloads.

    Two of them, on a runner with ~14 GB of disk shared with the connector
    container. What the run leaves behind has to be bounded even though the peak
    during capture cannot be. Disk is the reason, not the artifact upload: dumps
    are excluded from every upload step at any size, so a warning that says
    otherwise sends the reader looking for the wrong cap.
    """
    seen = stub_comparison_run(dict(_CLEAN_SIDE), dict(_CLEAN_SIDE))
    written: list = []

    def _fake_discard(dump_path, max_bytes):
        written.append((dump_path, max_bytes))
        return 900 * 1024 * 1024

    monkeypatch.setattr(cloud, "discard_oversized_dump", _fake_discard)

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
        enable_http_replay=True,
        http_replay_max_dump_size_mb=64,
    )
    printed = " ".join(_ANSI_ESCAPE.sub("", capsys.readouterr().out).split())

    assert [call[1] for call in written] == [64 * 1024 * 1024] * 2
    assert "exceeds the retention cap" in printed
    assert "never uploaded as artifacts" in printed
    # No dangling path to a file that is gone, and the report says how big it was.
    payload = seen["json_output"]
    assert "http_dump_file" not in payload["control"]
    assert payload["control"]["http_metrics"]["discarded_dump_mb"] == 900


def test_a_runner_without_mitmdump_does_not_report_a_clean_replayed_run(
    tmp_path, capsys, monkeypatch
):
    """Drives the whole comparison, because the gap is in how the sides compose.

    When `mitmdump` is missing the *control* run also gets no session, so it
    records no dump, so the target is handed `replay_from=None` and takes the
    same no-session branch. Each side is individually well-behaved; between
    them, a run that was supposed to replay ran entirely live and reported an
    ordinary green comparison. Keying the report off `replay_from` looks right
    and is never true in this failure.
    """
    monkeypatch.setattr(cloud, "ensure_image_available", lambda _image: True)
    monkeypatch.setattr(cloud, "track_regression_test", lambda **_kwargs: None)
    monkeypatch.setattr(cloud, "write_github_outputs", lambda _outputs: None)
    monkeypatch.setattr(cloud, "write_github_summary", lambda _text: None)
    monkeypatch.setattr(cloud, "write_json_output", lambda _key, _data: None)
    # No mitmdump on PATH: `MitmproxyManager.running` yields no session at all.
    monkeypatch.setattr(
        cloud.MitmproxyManager,
        "running",
        lambda _self: contextlib.nullcontext(None),
    )

    def _fake_run(*, output_dir, **_kwargs):
        output_dir.mkdir(parents=True, exist_ok=True)
        return (
            {
                "success": True,
                "exit_code": 0,
                "message_counts": {"RECORD": 5},
                "record_counts_per_stream": {"users": 5},
            },
            ComparableOutputs(),
        )

    monkeypatch.setattr(cloud, "_run_connector_command", _fake_run)

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
    )

    payload = _logged_payload(capsys.readouterr().out)

    reason = payload["target"]["http_metrics"]["replay_skipped_reason"]
    assert "mitmproxy is unavailable" in reason
    # The control run was recording, not replaying; nothing to report there.
    assert "http_metrics" not in payload["control"]


def test_a_control_run_that_captured_nothing_is_reported_as_a_skip(
    tmp_path, capsys, monkeypatch
):
    """The proxy came up, but there was no recording to replay from.

    A third way replay silently does not happen, and it has to read like the
    other two rather than like a clean replayed run.
    """
    session = MitmproxySession(
        proxy_host="host.docker.internal",
        proxy_port=8080,
        dump_file_path=tmp_path / "target" / "http_traffic.mitm",
        ca_cert_path=None,
    )
    monkeypatch.setattr(
        cloud.MitmproxyManager,
        "running",
        lambda _self: contextlib.nullcontext(session),
    )
    monkeypatch.setattr(
        cloud,
        "_run_connector_command",
        lambda **_kwargs: ({"success": True, "exit_code": 0}, ComparableOutputs()),
    )
    monkeypatch.setattr(
        cloud, "parse_http_dump", lambda *_args, **_kwargs: HttpMetrics.empty()
    )

    result, _outputs = cloud._run_with_optional_http_metrics(
        connector_image="airbyte/source-test:2.0.0",
        command=Command.READ,
        output_dir=tmp_path / "target",
        target_or_control=cloud.TargetOrControl.TARGET,
        enable_http_metrics=True,
        config_path=None,
        catalog_path=None,
        state_path=None,
        replay_expected=True,
        replay_from=None,
    )
    capsys.readouterr()

    assert (
        result["http_metrics"]["replay_skipped_reason"]
        == "the control run recorded no HTTP dump to replay from"
    )


def _replaying_session(tmp_path, corpus_name="http_replay_corpus.mitm"):
    """A session that came up and is replaying from a corpus."""
    return MitmproxySession(
        proxy_host="host.docker.internal",
        proxy_port=8080,
        dump_file_path=tmp_path / "target" / "http_traffic.mitm",
        ca_cert_path=None,
        replay_source=tmp_path / corpus_name,
    )


def _run_target(tmp_path, **kwargs):
    return cloud._run_with_optional_http_metrics(
        connector_image="airbyte/source-test:2.0.0",
        command=Command.READ,
        output_dir=tmp_path / "target",
        target_or_control=cloud.TargetOrControl.TARGET,
        enable_http_metrics=True,
        config_path=None,
        catalog_path=None,
        state_path=None,
        **kwargs,
    )


def test_a_replaying_run_reports_which_urls_went_live(tmp_path, capsys, monkeypatch):
    """The one field that can explain a coverage shortfall after the fact.

    `unreplayable_flow_count` covers exclusion from the corpus and nothing else,
    so a request that reached mitmproxy and matched nothing was only ever visible
    as the aggregate live count -- and the dumps that hold the URLs are excluded
    from the uploaded artifacts by design.
    """
    session = _replaying_session(tmp_path)
    monkeypatch.setattr(
        cloud.MitmproxyManager, "running", lambda _self: contextlib.nullcontext(session)
    )
    monkeypatch.setattr(
        cloud,
        "_run_connector_command",
        lambda **_kwargs: ({"success": True, "exit_code": 0}, ComparableOutputs()),
    )
    monkeypatch.setattr(
        cloud,
        "parse_http_dump",
        lambda *_args, **_kwargs: HttpMetrics(
            flow_count=4,
            duplicate_flow_count=1,
            unique_urls=["https://example.com/a"],
            replayed_flow_count=1,
            live_flow_count=3,
            live_url_counts={
                "https://example.com/job/1": 2,
                "https://example.com/b": 1,
            },
        ),
    )

    result, _outputs = _run_target(
        tmp_path, replay_expected=True, replay_from=tmp_path / "control.mitm"
    )
    capsys.readouterr()

    metrics = result["http_metrics"]
    assert metrics["live_urls"] == [
        {"url": "https://example.com/job/1", "count": 2},
        {"url": "https://example.com/b", "count": 1},
    ]
    assert metrics["live_unique_url_count"] == 2


def test_a_recording_run_does_not_carry_a_request_log(tmp_path, capsys, monkeypatch):
    """Every request on a recording run is live, so the list explains nothing.

    URLs can carry credentials in their query strings; that is not a surface to
    widen where there is no diagnostic value in return.
    """
    session = MitmproxySession(
        proxy_host="host.docker.internal",
        proxy_port=8080,
        dump_file_path=tmp_path / "target" / "http_traffic.mitm",
        ca_cert_path=None,
    )
    monkeypatch.setattr(
        cloud.MitmproxyManager, "running", lambda _self: contextlib.nullcontext(session)
    )
    monkeypatch.setattr(
        cloud,
        "_run_connector_command",
        lambda **_kwargs: ({"success": True, "exit_code": 0}, ComparableOutputs()),
    )
    monkeypatch.setattr(
        cloud,
        "parse_http_dump",
        lambda *_args, **_kwargs: HttpMetrics(
            flow_count=2,
            duplicate_flow_count=0,
            unique_urls=["https://example.com/a"],
            live_flow_count=2,
            live_url_counts={"https://example.com/a?token=secret": 2},
        ),
    )

    result, _outputs = _run_target(tmp_path)
    capsys.readouterr()

    assert "live_urls" not in result["http_metrics"]


def test_a_killed_shutdown_is_recorded_on_the_run(tmp_path, capsys, monkeypatch):
    """`SIGKILL` costs the dump its unflushed tail, always in the flattering
    direction -- the counts have to say they are a lower bound."""
    session = _replaying_session(tmp_path)

    @contextlib.contextmanager
    def _running(manager):
        yield session
        # What `_stop` does when `SIGINT` was not serviced in time; only knowable
        # after the block, which is why it lives on the manager.
        manager.metrics_incomplete_reason = "mitmproxy ... was killed"

    monkeypatch.setattr(cloud.MitmproxyManager, "running", _running)
    monkeypatch.setattr(
        cloud,
        "_run_connector_command",
        lambda **_kwargs: ({"success": True, "exit_code": 0}, ComparableOutputs()),
    )
    monkeypatch.setattr(
        cloud, "parse_http_dump", lambda *_args, **_kwargs: HttpMetrics.empty()
    )

    result, _outputs = _run_target(
        tmp_path, replay_expected=True, replay_from=tmp_path / "control.mitm"
    )
    capsys.readouterr()

    assert result["http_metrics"]["metrics_incomplete"] == "mitmproxy ... was killed"


def test_a_startup_failure_is_reported_as_itself_not_as_a_missing_mitmproxy(
    tmp_path, capsys, monkeypatch
):
    """A proxy that died on startup, or a corpus slower to load than the ceiling,
    points at a code fix -- the fixed string sent a reader to install mitmproxy."""

    @contextlib.contextmanager
    def _running(manager):
        manager.startup_failure_reason = (
            "mitmproxy did not accept connections on port 4242 in 60s"
        )
        yield None

    monkeypatch.setattr(cloud.MitmproxyManager, "running", _running)
    monkeypatch.setattr(
        cloud,
        "_run_connector_command",
        lambda **_kwargs: ({"success": True, "exit_code": 0}, ComparableOutputs()),
    )

    result, _outputs = _run_target(
        tmp_path, replay_expected=True, replay_from=tmp_path / "control.mitm"
    )
    capsys.readouterr()

    assert result["http_metrics"]["replay_skipped_reason"] == (
        "mitmproxy did not accept connections on port 4242 in 60s, so nothing "
        "could be replayed"
    )


def test_the_dump_is_parsed_only_after_mitmproxy_has_flushed_it(
    tmp_path, capsys, monkeypatch
):
    """mitmproxy's `save` addon only flushes and closes the dump in `done()`.

    It writes each flow through a block-buffered file and holds in-flight flows
    until shutdown, so parsing inside the `with` block misses the buffered tail
    -- and `live_flow_count` is the acceptance criterion for replay, not a rough
    count.
    """
    session = MitmproxySession(
        proxy_host="host.docker.internal",
        proxy_port=8080,
        dump_file_path=tmp_path / "target" / "http_traffic.mitm",
        ca_cert_path=None,
    )
    events: list[str] = []

    @contextlib.contextmanager
    def _fake_start(*_args, **_kwargs):
        try:
            yield session
        finally:
            events.append("mitmproxy stopped")

    monkeypatch.setattr(
        cloud.MitmproxyManager,
        "running",
        lambda _self: _fake_start(),
    )
    monkeypatch.setattr(
        cloud,
        "_run_connector_command",
        lambda **_kwargs: ({"success": True, "exit_code": 0}, ComparableOutputs()),
    )

    def _parse(*_args, **_kwargs):
        events.append("dump parsed")
        return HttpMetrics.empty()

    monkeypatch.setattr(cloud, "parse_http_dump", _parse)

    cloud._run_with_optional_http_metrics(
        connector_image="airbyte/source-test:2.0.0",
        command=Command.READ,
        output_dir=tmp_path / "target",
        target_or_control=cloud.TargetOrControl.TARGET,
        enable_http_metrics=True,
        config_path=None,
        catalog_path=None,
        state_path=None,
    )
    capsys.readouterr()

    assert events == ["mitmproxy stopped", "dump parsed"]
