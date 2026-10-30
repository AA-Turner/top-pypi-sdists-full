# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for `--discover-missing-streams` through the regression-test CLI."""

from __future__ import annotations

import json
import secrets
from pathlib import Path
from typing import Any, cast
from unittest.mock import patch

import pytest
import yaml
from airbyte_protocol.models import AirbyteCatalog, AirbyteStream, SyncMode
from fastmcp import Context

from airbyte_ops_mcp.cli import cloud
from airbyte_ops_mcp.github_actions import WorkflowDispatchResult
from airbyte_ops_mcp.mcp import connector_qa
from airbyte_ops_mcp.mcp.connector_qa import (
    REGRESSION_TEST_WORKFLOW_FILE,
    ConnectorRepo,
    TestRunStatus,
    run_regression_tests,
)
from airbyte_ops_mcp.regression_tests.config_overrides import StreamsNotDiscoveredError
from airbyte_ops_mcp.regression_tests.models import Command, ComparableOutputs

pytestmark = pytest.mark.unit

TARGET = "airbyte/source-test:dev"
CONTROL = "airbyte/source-test:1.0.0"


def _catalog(*names: str) -> AirbyteCatalog:
    return AirbyteCatalog(
        streams=[
            AirbyteStream(
                name=name,
                json_schema={"type": "object"},
                supported_sync_modes=[SyncMode.full_refresh],
            )
            for name in names
        ]
    )


@pytest.fixture
def stub_injection(monkeypatch, tmp_path):
    """Stub Docker and CI side effects; record each run and the catalog it was given."""
    seen: dict[str, object] = {"runs": [], "outputs": {}, "gh_outputs": {}, "modes": []}

    monkeypatch.setattr(cloud, "ensure_image_available", lambda _image: True)
    monkeypatch.setattr(cloud, "track_regression_test", lambda **_kwargs: None)
    monkeypatch.setattr(cloud, "write_github_summary", lambda _text: None)
    monkeypatch.setattr(
        cloud,
        "write_github_outputs",
        lambda outputs: seen["gh_outputs"].update(outputs),  # type: ignore[union-attr]
    )
    monkeypatch.setattr(
        cloud,
        "write_github_output",
        lambda key, value: seen["outputs"].update({key: value}),  # type: ignore[union-attr]
    )
    monkeypatch.setattr(cloud, "write_json_output", lambda _key, _data: None)

    def _install(discovered: dict[str, AirbyteCatalog | None]) -> dict[str, object]:
        def _fake_run(
            *,
            connector_image,
            command: Command,
            output_dir,
            catalog_path=None,
            output_mode="raw",
            mask_key=None,
            **_kw,
        ):
            output_dir.mkdir(parents=True, exist_ok=True)
            seen["modes"].append((output_dir, command, output_mode, mask_key))  # type: ignore[union-attr]
            streams = (
                [
                    s["stream"]["name"]
                    for s in json.loads(Path(catalog_path).read_text())["streams"]
                ]
                if catalog_path is not None and command.needs_catalog()
                else None
            )
            seen["runs"].append((connector_image, command, streams))  # type: ignore[union-attr]
            outputs = (
                ComparableOutputs(catalog=discovered.get(connector_image))
                if command is Command.DISCOVER
                else ComparableOutputs()
            )
            stdout_file = output_dir / "stdout.txt"
            stdout_file.write_text("")
            result = {
                "command": command.value,
                "success": True,
                "exit_code": 0,
                "stdout_file": str(stdout_file),
                "message_counts": {},
                "record_counts_per_stream": {},
            }
            return result, outputs

        monkeypatch.setattr(cloud, "_run_connector_command", _fake_run)
        return seen

    return _install


def _catalog_file(tmp_path: Path, *names: str) -> str:
    path = tmp_path / "input_catalog.json"
    path.write_text(
        json.dumps(
            {
                "streams": [
                    {
                        "stream": {
                            "name": name,
                            "json_schema": {"type": "object"},
                            "supported_sync_modes": ["full_refresh"],
                        },
                        "sync_mode": "full_refresh",
                        "destination_sync_mode": "overwrite",
                    }
                    for name in names
                ]
            }
        )
    )
    return str(path)


def _reads(seen: dict[str, object]) -> dict[str, list[str] | None]:
    return {
        image: streams
        for image, command, streams in seen["runs"]  # type: ignore[union-attr]
        if command.needs_catalog()
    }


def test_a_new_stream_is_read_by_the_target_and_kept_from_the_control(
    tmp_path, stub_injection
):
    seen = stub_injection(
        {TARGET: _catalog("users", "feedback"), CONTROL: _catalog("users")}
    )

    cloud.regression_test(
        test_image=TARGET,
        control_image=CONTROL,
        command="read",
        catalog_path=_catalog_file(tmp_path, "users"),
        selected_streams="users,feedback",
        discover_missing_streams=True,
        output_dir=str(tmp_path / "out"),
    )

    assert _reads(seen) == {CONTROL: ["users"], TARGET: ["users", "feedback"]}
    summary = json.loads((tmp_path / "out" / "stream_injection.json").read_text())
    assert summary["new_streams"] == ["feedback"]
    assert summary["reference_image"] == CONTROL
    assert json.loads(seen["outputs"]["stream_injection"]) == summary  # type: ignore[index]


@pytest.mark.parametrize(
    "control_streams,not_exercised",
    [
        pytest.param(("users",), True, id="new-stream-with-no-records"),
        pytest.param(("users", "feedback"), False, id="shared-stream"),
    ],
)
def test_a_new_stream_with_no_records_makes_the_read_not_exercised(
    tmp_path, stub_injection, control_streams, not_exercised
):
    """The control catalog the injection builds is the one the NOT EXERCISED
    rule compares against, so a new stream that reads nothing is never a pass."""
    seen = stub_injection(
        {TARGET: _catalog("users", "feedback"), CONTROL: _catalog(*control_streams)}
    )

    cloud.regression_test(
        test_image=TARGET,
        control_image=CONTROL,
        command="read",
        catalog_path=_catalog_file(tmp_path, "users"),
        selected_streams="users,feedback",
        discover_missing_streams=True,
        output_dir=str(tmp_path / "out"),
    )

    gh_outputs = seen["gh_outputs"]
    assert gh_outputs["not_exercised"] is not_exercised  # type: ignore[index]
    if not_exercised:
        assert gh_outputs["success"] is False  # type: ignore[index]


def test_a_stream_not_discovered_by_the_target_emits_setup_error(monkeypatch, tmp_path):
    outputs: dict[str, object] = {}
    monkeypatch.setattr(cloud, "_discovered_catalog", lambda *_args: {"streams": []})
    monkeypatch.setattr(
        cloud,
        "build_injected_catalogs",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            StreamsNotDiscoveredError({"feedback"}, set())
        ),
    )
    monkeypatch.setattr(cloud, "write_github_output", outputs.__setitem__)

    def _exit_with_error(message: str) -> None:
        raise RuntimeError(message)

    monkeypatch.setattr(cloud, "exit_with_error", _exit_with_error)
    with pytest.raises(RuntimeError, match="Setup error:"):
        cloud._inject_discovered_streams(
            catalog_file=None,
            selected_stream_names={"feedback"},
            test_image=TARGET,
            reference_image=None,
            skip_compare=False,
            config_file=None,
            output_path=tmp_path,
            enable_debug_logs=False,
            extra_env=None,
            sync_mode=None,
            output_mode="raw",
            mask_key=None,
        )

    assert outputs["success"] is False
    assert outputs["setup_error"] is True


def test_a_stream_the_released_version_has_is_read_by_both_versions(
    tmp_path, stub_injection
):
    seen = stub_injection(
        {TARGET: _catalog("users", "teams"), CONTROL: _catalog("users", "teams")}
    )

    cloud.regression_test(
        test_image=TARGET,
        control_image=CONTROL,
        command="read",
        catalog_path=_catalog_file(tmp_path, "users"),
        selected_streams="users,teams",
        discover_missing_streams=True,
        output_dir=str(tmp_path / "out"),
    )

    assert _reads(seen) == {CONTROL: ["users", "teams"], TARGET: ["users", "teams"]}


def test_a_masked_run_also_masks_the_discover_that_finds_the_new_streams(
    tmp_path, stub_injection
):
    """Under the run's key: a masked run without one is refused before the
    connector starts, so the read would never be reached."""
    seen = stub_injection(
        {TARGET: _catalog("users", "feedback"), CONTROL: _catalog("users")}
    )
    key_hex = secrets.token_hex(32)
    key_file = tmp_path / "mask_key"
    key_file.write_text(key_hex + "\n")

    cloud.regression_test(
        test_image=TARGET,
        control_image=CONTROL,
        command="read",
        catalog_path=_catalog_file(tmp_path, "users"),
        selected_streams="users,feedback",
        discover_missing_streams=True,
        output_mode="masked",
        mask_key_path=str(key_file),
        output_dir=str(tmp_path / "out"),
    )

    injection_discovers = [
        (mode, key)
        for output_dir, command, mode, key in seen["modes"]  # type: ignore[union-attr]
        if command is Command.DISCOVER and "discover_for_injection" in str(output_dir)
    ]
    key = bytes.fromhex(key_hex)
    assert injection_discovers == [("masked", key), ("masked", key)]


def test_a_stream_the_target_does_not_discover_stops_the_run_before_read(
    tmp_path, stub_injection
):
    seen = stub_injection({TARGET: _catalog("users"), CONTROL: _catalog("users")})

    with pytest.raises(SystemExit):
        cloud.regression_test(
            test_image=TARGET,
            control_image=CONTROL,
            command="read",
            catalog_path=_catalog_file(tmp_path, "users"),
            selected_streams="feedbak",
            discover_missing_streams=True,
            output_dir=str(tmp_path / "out"),
        )

    assert _reads(seen) == {}
    assert seen["outputs"]["success"] is False  # type: ignore[index]
    assert "feedbak" in seen["outputs"]["error"]  # type: ignore[index]


def test_comparing_only_new_streams_asks_for_a_single_version_run(
    tmp_path, stub_injection
):
    seen = stub_injection({TARGET: _catalog("feedback"), CONTROL: _catalog()})

    with pytest.raises(SystemExit):
        cloud.regression_test(
            test_image=TARGET,
            control_image=CONTROL,
            command="read",
            catalog_path=_catalog_file(tmp_path, "users"),
            selected_streams="feedback",
            discover_missing_streams=True,
            output_dir=str(tmp_path / "out"),
        )

    assert _reads(seen) == {}
    assert "--skip-compare" in seen["outputs"]["error"]  # type: ignore[index]


def test_a_single_version_run_reads_a_new_stream_of_unknown_novelty(
    tmp_path, stub_injection
):
    """No connection and no connector name: no released image to compare against."""
    seen = stub_injection({TARGET: _catalog("feedback")})

    cloud.regression_test(
        skip_compare=True,
        test_image=TARGET,
        command="read",
        catalog_path=_catalog_file(tmp_path, "users"),
        selected_streams="feedback",
        discover_missing_streams=True,
        output_dir=str(tmp_path / "out"),
    )

    assert _reads(seen) == {TARGET: ["feedback"]}
    summary = json.loads((tmp_path / "out" / "stream_injection.json").read_text())
    assert summary["unknown_streams"] == ["feedback"]
    assert summary["reference_image"] is None


def test_a_run_without_a_connection_keeps_the_new_streams_from_the_control(
    tmp_path, stub_injection
):
    """Its catalog comes from the target's DISCOVER, so the new stream is in it already."""
    seen = stub_injection(
        {TARGET: _catalog("users", "feedback"), CONTROL: _catalog("users")}
    )

    cloud.regression_test(
        test_image=TARGET,
        control_image=CONTROL,
        command="read",
        catalog_path=_catalog_file(tmp_path, "users", "feedback"),
        selected_streams="users,feedback",
        discover_missing_streams=True,
        output_dir=str(tmp_path / "out"),
    )

    assert _reads(seen) == {CONTROL: ["users"], TARGET: ["users", "feedback"]}
    summary = json.loads((tmp_path / "out" / "stream_injection.json").read_text())
    assert summary["kept_target_only"] == ["feedback"]
    assert summary["new_streams"] == []
    assert summary["reference_image"] == CONTROL


@pytest.mark.parametrize("command", ["spec", "check", "discover"])
def test_commands_without_a_catalog_ignore_a_stream_the_connection_lacks(
    tmp_path, stub_injection, command
):
    """The selected-streams filter would fail them on a stream only READ adds."""
    seen = stub_injection({TARGET: _catalog("feedback")})

    cloud.regression_test(
        skip_compare=True,
        test_image=TARGET,
        command=command,
        catalog_path=_catalog_file(tmp_path, "users"),
        selected_streams="feedback",
        discover_missing_streams=True,
        output_dir=str(tmp_path / "out"),
    )

    assert [run[1].value for run in seen["runs"]] == [command]  # type: ignore[union-attr]


def test_injection_without_selected_streams_is_refused(tmp_path, stub_injection):
    stub_injection({TARGET: _catalog("feedback")})

    with pytest.raises(SystemExit):
        cloud.regression_test(
            skip_compare=True,
            test_image=TARGET,
            command="read",
            discover_missing_streams=True,
            output_dir=str(tmp_path / "out"),
        )


def test_streams_already_in_the_catalog_are_filtered_as_before(
    tmp_path, stub_injection
):
    seen = stub_injection({TARGET: _catalog("users", "orders")})

    cloud.regression_test(
        skip_compare=True,
        test_image=TARGET,
        command="read",
        catalog_path=_catalog_file(tmp_path, "users", "orders"),
        selected_streams="users",
        discover_missing_streams=True,
        output_dir=str(tmp_path / "out"),
    )

    assert _reads(seen) == {TARGET: ["users"]}
    assert not (tmp_path / "out" / "stream_injection.json").exists()


def _dispatch(**kwargs: Any) -> tuple[connector_qa.RunRegressionTestsResponse, dict]:
    """Run the tool with the dispatch stubbed; return its response and the inputs sent."""
    sent: dict[str, str] = {}

    def _fake_dispatch(*, inputs: dict[str, str], **_kwargs: Any):
        sent.update(inputs)
        return WorkflowDispatchResult(workflow_url="https://example.com/workflow")

    with patch.object(
        connector_qa, "trigger_workflow_dispatch", _fake_dispatch
    ), patch.object(connector_qa, "resolve_ci_trigger_github_token", lambda: "token"):
        response = run_regression_tests(
            connector_name="source-pokeapi",
            pr=1,
            repo=ConnectorRepo.AIRBYTE,
            **kwargs,
            ctx=cast(Context, object()),
        )

    return response, sent


def _workflow() -> tuple[dict[str, Any], dict[str, Any]]:
    """The regression-test workflow and its triggers (YAML reads `on:` as `True`)."""
    path = (
        Path(__file__).resolve().parents[1]
        / ".github/workflows"
        / REGRESSION_TEST_WORKFLOW_FILE
    )
    workflow = yaml.safe_load(path.read_text())
    return workflow, workflow[True] if True in workflow else workflow["on"]


def _declared_inputs() -> set[str]:
    """Inputs both of the workflow's triggers declare (see the workflow-inputs tests)."""
    _workflow_yaml, triggers = _workflow()
    return set.intersection(
        *(
            set(triggers[trigger]["inputs"])
            for trigger in ("workflow_dispatch", "workflow_call")
        )
    )


def test_the_injection_inputs_reach_the_workflow_and_are_declared_by_it():
    _response, sent = _dispatch(
        selected_streams=["feedback"],
        discover_missing_streams=True,
        injected_sync_mode="incremental",
    )

    assert sent["discover_missing_streams"] == "true"
    assert sent["injected_sync_mode"] == "incremental"
    assert {"discover_missing_streams", "injected_sync_mode"} <= _declared_inputs()


def test_the_injection_inputs_are_omitted_by_default():
    _response, sent = _dispatch()

    assert "discover_missing_streams" not in sent
    assert "injected_sync_mode" not in sent


def test_the_tool_refuses_injection_without_selected_streams():
    """Refused at the tool, before a dispatch that would fail in the workflow."""
    response, sent = _dispatch(discover_missing_streams=True)

    assert response.status == TestRunStatus.FAILED
    assert "selected_streams" in response.message
    assert sent == {}


def test_the_tool_refuses_a_sync_mode_without_injection():
    """The workflow would refuse it too, but only after a dispatch."""
    response, sent = _dispatch(
        selected_streams="users", injected_sync_mode="incremental"
    )

    assert response.status == TestRunStatus.FAILED
    assert "discover_missing_streams" in response.message
    assert sent == {}


def test_the_injection_summary_is_a_workflow_output():
    """Callers of the reusable workflow read what was added without downloading an artifact."""
    workflow, triggers = _workflow()

    assert (
        workflow["jobs"]["regression-test"]["outputs"]["stream_injection"]
        == "${{ steps.run-read.outputs.stream_injection }}"
    )
    assert (
        triggers["workflow_call"]["outputs"]["stream_injection"]["value"]
        == "${{ jobs.regression-test.outputs.stream_injection || "
        "jobs.regression-test-eu.outputs.stream_injection }}"
    )
    # The EU job never reports what was injected, so no stream name leaves
    # the EU: finalize keeps the output an empty string.
    eu_job = workflow["jobs"]["regression-test-eu"]
    assert (
        eu_job["outputs"]["stream_injection"]
        == "${{ steps.finalize.outputs.stream_injection }}"
    )
    (finalize,) = [step for step in eu_job["steps"] if step.get("id") == "finalize"]
    assert 'stream_injection=""' in finalize["run"]
