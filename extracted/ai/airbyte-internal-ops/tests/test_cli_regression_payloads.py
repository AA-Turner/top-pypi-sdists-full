# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for the regression-test CLI's logged verdict payloads."""

from __future__ import annotations

import contextlib
import inspect
import json
import re
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from airbyte_protocol.models import (
    AirbyteCatalog,
    AirbyteStream,
    ConnectorSpecification,
    SyncMode,
)

from airbyte_ops_mcp.cli import cloud
from airbyte_ops_mcp.connector_secrets import (
    DEFAULT_GCP_PROJECT_ID,
    ConnectorSecretsUnavailableError,
)
from airbyte_ops_mcp.regression_tests import connector_runner, read_budget
from airbyte_ops_mcp.regression_tests.ci_output import (
    generate_action_test_comparison_report,
)
from airbyte_ops_mcp.regression_tests.connection_fetcher import ConnectionData
from airbyte_ops_mcp.regression_tests.connector_runner import (
    DEFAULT_TIMEOUT_SECONDS,
    ConnectorRunner,
)
from airbyte_ops_mcp.regression_tests.http_metrics import (
    HttpMetrics,
    MitmproxySession,
)
from airbyte_ops_mcp.regression_tests.masking import MaskPolicy, mask_record_data
from airbyte_ops_mcp.regression_tests.models import (
    Command,
    ComparableOutputs,
    ExecutionInputs,
    ExecutionResult,
    StoppedEarly,
    StreamError,
    TargetOrControl,
)
from airbyte_ops_mcp.regression_tests.validation.record_validators import (
    _MAX_OBSERVED_FIELDS,
)
from tests.test_connector_runner import FAKE_CONNECTOR
from tests.test_masking import KEY

pytestmark = pytest.mark.unit


@pytest.fixture(autouse=True)
def images_trust_the_proxy(monkeypatch):
    """Keep the capture path's certifi probe from shelling out to Docker."""
    monkeypatch.setattr(cloud, "proxy_trust_gap", lambda _image: None)


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
    ("test_image", "connector_name", "builds", "pulls", "loads_gsm"),
    [
        pytest.param(
            "airbyte/source-faker:1.0.0",
            "source-faker",
            False,
            True,
            True,
            id="test-image-takes-precedence",
        ),
        pytest.param(
            None,
            "source-faker",
            True,
            False,
            True,
            id="connector-name-builds-from-source",
        ),
        pytest.param(
            "airbyte/source-faker:1.0.0",
            None,
            False,
            True,
            False,
            id="test-image-only",
        ),
    ],
)
def test_test_image_precedence_preserves_gsm_config_lookup(
    tmp_path,
    capsys,
    stub_run,
    monkeypatch,
    test_image,
    connector_name,
    builds,
    pulls,
    loads_gsm,
):
    stub_run({"success": True, "exit_code": 0})
    build_image = Mock(return_value="airbyte/source-faker:dev")
    ensure_image_available = Mock(return_value=True)
    get_integration_test_config_from_secrets = Mock(return_value=None)
    monkeypatch.setattr(cloud, "_build_connector_image_from_source", build_image)
    monkeypatch.setattr(cloud, "ensure_image_available", ensure_image_available)
    monkeypatch.setattr(
        cloud,
        "get_integration_test_config_from_secrets",
        get_integration_test_config_from_secrets,
    )

    cloud.regression_test(
        skip_compare=True,
        test_image=test_image,
        connector_name=connector_name,
        command="spec",
        output_dir=str(tmp_path),
    )
    capsys.readouterr()

    if builds:
        build_image.assert_called_once_with(
            connector_name="source-faker",
            repo_root=None,
            tag="dev",
            prefer_repo_root=False,
        )
    else:
        build_image.assert_not_called()

    if pulls:
        ensure_image_available.assert_called_once_with(test_image)
    else:
        ensure_image_available.assert_not_called()

    if loads_gsm:
        get_integration_test_config_from_secrets.assert_called_once_with("source-faker")
    else:
        get_integration_test_config_from_secrets.assert_not_called()


_SOURCE_BUILD_SIGNATURE = inspect.signature(cloud._build_connector_image_from_source)


def _build_arguments(build_image: Mock) -> dict[str, object]:
    """The arguments the source build got, defaults filled in."""
    (call,) = build_image.call_args_list
    bound = _SOURCE_BUILD_SIGNATURE.bind(*call.args, **call.kwargs)
    bound.apply_defaults()
    return dict(bound.arguments)


def test_build_target_image_builds_what_regression_test_would_build(
    tmp_path, capsys, stub_run, monkeypatch
):
    """CI builds in a job without credentials and hands the image over as
    `--test-image`, so the image must be the one `--connector-name` built in
    place: same source, same tag."""
    stub_run({"success": True, "exit_code": 0})
    monkeypatch.setattr(
        cloud, "get_integration_test_config_from_secrets", lambda _name: None
    )
    in_place = Mock(return_value="airbyte/source-faker:dev")
    monkeypatch.setattr(cloud, "_build_connector_image_from_source", in_place)
    cloud.regression_test(
        skip_compare=True,
        connector_name="source-faker",
        repo_root=str(tmp_path),
        command="spec",
        output_dir=str(tmp_path / "out"),
    )

    separate = Mock(return_value="airbyte/source-faker:dev")
    monkeypatch.setattr(cloud, "_build_connector_image_from_source", separate)
    github_output = tmp_path / "github_output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(github_output))
    cloud.build_target_image(connector_name="source-faker", repo_root=str(tmp_path))
    capsys.readouterr()

    assert _build_arguments(separate) == _build_arguments(in_place)
    assert github_output.read_text() == "image=airbyte/source-faker:dev\n"


def test_build_target_image_fails_without_an_image(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(
        cloud, "_build_connector_image_from_source", Mock(return_value=None)
    )
    github_output = tmp_path / "github_output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(github_output))

    with pytest.raises(SystemExit) as exc_info:
        cloud.build_target_image(connector_name="source-faker")
    capsys.readouterr()

    assert exc_info.value.code == 1
    assert not github_output.exists()


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


def test_regression_test_fails_fast_when_gsm_config_is_unavailable(
    tmp_path, monkeypatch
):
    github_outputs: dict[str, object] = {}
    monkeypatch.setattr(
        cloud, "get_integration_test_config_from_secrets", lambda _connector: None
    )
    monkeypatch.setattr(
        cloud,
        "_build_connector_image_from_source",
        lambda **_kwargs: "airbyte/source-test:dev",
    )
    monkeypatch.setattr(
        cloud,
        "write_github_output",
        lambda key, value: github_outputs.__setitem__(key, value),
    )

    def fail_with_error(message: str) -> None:
        raise ValueError(message)

    monkeypatch.setattr(cloud, "exit_with_error", fail_with_error)

    with pytest.raises(ValueError, match="No usable GSM integration-test secret"):
        cloud.regression_test(
            skip_compare=True,
            connector_name="source-test",
            command="read",
            output_dir=str(tmp_path),
        )

    assert github_outputs["success"] is False
    assert "connection_id" in github_outputs["error"]
    assert "added or refreshed" in github_outputs["error"]
    assert f"in {DEFAULT_GCP_PROJECT_ID}." in github_outputs["error"]
    assert "(every value blank or null)." in github_outputs["error"]


def test_regression_test_fails_fast_when_gsm_is_unavailable(tmp_path, monkeypatch):
    github_outputs: dict[str, object] = {}
    gsm_error = ConnectorSecretsUnavailableError(
        connector_name="source-test",
        gcp_project_id=DEFAULT_GCP_PROJECT_ID,
        error_types=["PermissionDenied"],
    )
    monkeypatch.setattr(
        cloud,
        "get_integration_test_config_from_secrets",
        Mock(side_effect=gsm_error),
    )
    monkeypatch.setattr(
        cloud,
        "_build_connector_image_from_source",
        lambda **_kwargs: "airbyte/source-test:dev",
    )
    monkeypatch.setattr(
        cloud,
        "write_github_output",
        lambda key, value: github_outputs.__setitem__(key, value),
    )

    def fail_with_error(message: str) -> None:
        raise ValueError(message)

    monkeypatch.setattr(cloud, "exit_with_error", fail_with_error)

    with pytest.raises(ValueError, match="Could not read GSM"):
        cloud.regression_test(
            skip_compare=True,
            connector_name="source-test",
            command="read",
            output_dir=str(tmp_path),
        )

    assert github_outputs["success"] is False
    assert "Could not read GSM" in github_outputs["error"]
    assert "connection_id" in github_outputs["error"]
    assert "added or refreshed" not in github_outputs["error"]


def test_spec_continues_when_gsm_is_unavailable(
    tmp_path, capsys, monkeypatch, stub_run
):
    stub_run(
        {
            "success": True,
            "exit_code": 0,
            "message_counts": {},
            "record_counts_per_stream": {},
        }
    )
    run_connector_command = cloud._run_connector_command
    gsm_error = ConnectorSecretsUnavailableError(
        connector_name="source-test",
        gcp_project_id=DEFAULT_GCP_PROJECT_ID,
        error_types=["PermissionDenied"],
    )
    monkeypatch.setattr(
        cloud,
        "get_integration_test_config_from_secrets",
        Mock(side_effect=gsm_error),
    )
    seen: dict[str, object] = {}

    def capture_run_connector_command(**kwargs):
        seen.update(kwargs)
        return run_connector_command(**kwargs)

    monkeypatch.setattr(cloud, "_run_connector_command", capture_run_connector_command)

    cloud.regression_test(
        skip_compare=True,
        test_image="airbyte/source-test:1.0.0",
        connector_name="source-test",
        command="spec",
        output_dir=str(tmp_path),
    )

    assert seen["config_path"] is None
    captured = capsys.readouterr()
    assert "Could not read GSM" in captured.out + captured.err


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


def test_a_seeded_state_is_labelled_as_such_in_the_report(tmp_path, capsys, stub_run):
    """A reader of the report assumes the input state is the connection's own
    cursors; a state the caller chose has to say so, and its values, which
    are customer state, stay out of everything the run writes."""
    seed = tmp_path / "seed_state.json"
    seed.write_text(
        json.dumps(
            [
                {
                    "type": "STREAM",
                    "stream": {
                        "stream_descriptor": {"name": "users"},
                        "stream_state": {"updated_at": "2026-01-01T00:00:00Z"},
                    },
                }
            ]
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
        command="read",
        state_path=str(seed),
        output_dir=str(tmp_path / "read"),
    )
    captured = capsys.readouterr().out

    assert "Using seeded state" in captured
    html = (tmp_path / "read" / "report.html").read_text()
    assert "State (seeded)" in html
    assert "State (input)" not in html
    written = "\n".join(
        path.read_text(errors="replace")
        for path in (tmp_path / "read").rglob("*")
        if path.is_file()
    )
    assert "2026-01-01T00:00:00Z" not in written


def test_a_fetched_state_keeps_the_plain_input_label(tmp_path):
    state = tmp_path / "state.json"
    state.write_text("[]")

    (block,) = cloud._collect_connection_objects(None, state, None)

    assert block.title == "State (input)"


def _block_json(block) -> object:
    return json.loads("\n".join(line.text for line in block.lines))


def test_a_seeded_state_shows_its_streams_and_cursor_fields_but_no_value(tmp_path):
    """Each seeded stream by namespace and name, with what the catalog says of
    it; a stream the catalog does not configure has neither. No cursor value,
    and no state key either: a key can be a partition value, such as a
    repository name."""
    catalog = tmp_path / "configured_catalog.json"
    catalog.write_text(
        json.dumps(
            {
                "streams": [
                    {
                        "stream": {
                            "namespace": "public",
                            "name": "users",
                            "json_schema": {},
                            "supported_sync_modes": ["incremental"],
                        },
                        "sync_mode": "incremental",
                        "cursor_field": ["updated_at"],
                        "destination_sync_mode": "append",
                    }
                ]
            }
        )
    )
    seed = tmp_path / "seed_state.json"
    seed.write_text(
        json.dumps(
            [
                {
                    "type": "STREAM",
                    "stream": {
                        "stream_descriptor": {"namespace": "public", "name": "users"},
                        "stream_state": {
                            "acme/private-repo": {"updated_at": "2026-01-01T00:00:00Z"}
                        },
                    },
                },
                {
                    "type": "STREAM",
                    "stream": {
                        "stream_descriptor": {"name": "orders"},
                        "stream_state": {"cursor": 1234567},
                    },
                },
            ]
        )
    )

    blocks = cloud._collect_connection_objects(catalog, seed, None, state_seeded=True)
    (block,) = [block for block in blocks if block.title == "State (seeded)"]

    assert _block_json(block) == [
        {
            "namespace": "public",
            "name": "users",
            "sync_mode": "incremental",
            "cursor_field": ["updated_at"],
        },
        {"namespace": None, "name": "orders", "sync_mode": None, "cursor_field": []},
    ]
    shown = "\n".join(line.text for line in block.lines)
    for value in ("acme/private-repo", "2026-01-01T00:00:00Z", "1234567"):
        assert value not in shown


def test_a_seed_that_names_no_stream_is_left_off_the_report(tmp_path):
    """A GLOBAL seed, which the CLI can take, has no stream list to show."""
    seed = tmp_path / "seed_state.json"
    seed.write_text(
        json.dumps(
            {
                "type": "GLOBAL",
                "global": {"shared_state": {"cursor": "2026-01-01T00:00:00Z"}},
            }
        )
    )

    assert cloud._collect_connection_objects(None, seed, None, state_seeded=True) == ()


_SEED = [
    {
        "type": "STREAM",
        "stream": {
            "stream_descriptor": {"name": "users"},
            "stream_state": {"updated_at": "2026-01-01T00:00:00Z"},
        },
    }
]


_Stream = str | tuple[str, str]


def _descriptor(stream: _Stream) -> dict[str, str]:
    """A bare stream name, or a `(namespace, name)` pair, as the catalog and
    the seed spell it."""
    if isinstance(stream, str):
        return {"name": stream}
    namespace, name = stream
    return {"namespace": namespace, "name": name}


def _local_read_files(
    tmp_path, sync_modes: dict[_Stream, str], seeded: tuple[_Stream, ...] = ("users",)
) -> dict[str, str]:
    """A config, a catalog with a stream per `sync_modes` entry and a seed naming
    `seeded`, as `--*-path` arguments."""
    config = tmp_path / "config.json"
    config.write_text("{}")
    catalog = tmp_path / "configured_catalog.json"
    catalog.write_text(
        json.dumps(
            {
                "streams": [
                    {
                        "stream": {
                            **_descriptor(stream),
                            "json_schema": {},
                            "supported_sync_modes": ["full_refresh", "incremental"],
                        },
                        "sync_mode": sync_mode,
                        "destination_sync_mode": "overwrite",
                    }
                    for stream, sync_mode in sync_modes.items()
                ]
            }
        )
    )
    seed = tmp_path / "seed_state.json"
    seed.write_text(
        json.dumps(
            [
                {
                    "type": "STREAM",
                    "stream": {
                        "stream_descriptor": _descriptor(stream),
                        "stream_state": {"updated_at": "2026-01-01T00:00:00Z"},
                    },
                }
                for stream in seeded
            ]
        )
    )
    return {
        "config_path": str(config),
        "catalog_path": str(catalog),
        "state_path": str(seed),
    }


def _refused_read(tmp_path, capsys, stub_run, monkeypatch, **kwargs) -> str:
    """Run a single-version read the CLI should refuse; return its error output."""
    stub_run({"success": True, "exit_code": 0})
    gh_outputs: dict[str, object] = {}
    monkeypatch.setattr(
        cloud, "write_github_output", lambda key, value: gh_outputs.update({key: value})
    )

    with pytest.raises(SystemExit):
        cloud.regression_test(
            skip_compare=True,
            test_image="airbyte/source-test:2.0.0",
            command="read",
            output_dir=str(tmp_path / "read"),
            **kwargs,
        )
    capsys.readouterr()

    assert gh_outputs["success"] is False
    return str(gh_outputs["error"])


def test_a_seed_no_stream_of_the_catalog_can_take_is_refused(
    tmp_path, capsys, stub_run, monkeypatch
):
    """A catalog with every stream on full_refresh -- what a run without a
    connection generates -- ignores the seed, and the run would still call
    the read seeded."""
    error = _refused_read(
        tmp_path,
        capsys,
        stub_run,
        monkeypatch,
        **_local_read_files(tmp_path, {"users": "full_refresh"}),
    )

    assert (
        "it names users, and the configured catalog syncs no stream incrementally"
        in error
    )
    assert "--connection-id" in error


def test_a_seed_naming_only_streams_the_catalog_reads_in_full_is_refused(
    tmp_path, capsys, stub_run, monkeypatch
):
    """`users` incremental and `orders` full_refresh, with a seed for `orders`
    alone: some stream syncs incrementally, but not the seeded one."""
    error = _refused_read(
        tmp_path,
        capsys,
        stub_run,
        monkeypatch,
        **_local_read_files(
            tmp_path, {"users": "incremental", "orders": "full_refresh"}, ("orders",)
        ),
    )

    assert (
        "it names orders, and the configured catalog syncs users incrementally" in error
    )


def _seeded_read(tmp_path, capsys, stub_run, files: dict[str, str]) -> str:
    """Run a single-version read with `files`; return what it printed, uncoloured."""
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
        command="read",
        output_dir=str(tmp_path / "read"),
        **files,
    )

    return " ".join(_ANSI_ESCAPE.sub("", capsys.readouterr().out).split())


def test_a_seed_a_stream_of_the_catalog_can_take_is_used(tmp_path, capsys, stub_run):
    printed = _seeded_read(
        tmp_path,
        capsys,
        stub_run,
        _local_read_files(tmp_path, {"users": "incremental"}),
    )

    assert "Using seeded state" in printed
    assert "will ignore its seeded state" not in printed


def test_a_seeded_stream_the_catalog_reads_in_full_is_warned_about(
    tmp_path, capsys, stub_run
):
    """The seed still applies to `users`; `orders` is named so nobody reads
    the report's `State (seeded)` as covering it."""
    printed = _seeded_read(
        tmp_path,
        capsys,
        stub_run,
        _local_read_files(
            tmp_path,
            {"users": "incremental", "orders": "full_refresh"},
            ("users", "orders"),
        ),
    )

    assert "Using seeded state" in printed
    assert "does not sync 'orders' incrementally" in printed
    assert "does not sync 'users'" not in printed


# `users` in two namespaces: the connector applies a seed only to the stream
# its descriptor names, so the incremental one cannot stand in for the other.
_USERS_IN_TWO_NAMESPACES = {
    ("public", "users"): "full_refresh",
    ("reporting", "users"): "incremental",
}


def test_a_seed_is_matched_to_its_stream_by_namespace_and_name(
    tmp_path, capsys, stub_run, monkeypatch
):
    error = _refused_read(
        tmp_path,
        capsys,
        stub_run,
        monkeypatch,
        **_local_read_files(tmp_path, _USERS_IN_TWO_NAMESPACES, (("public", "users"),)),
    )

    assert (
        "it names public.users, and the configured catalog syncs reporting.users "
        "incrementally" in error
    )


def test_a_seed_for_the_namespace_read_in_full_is_warned_about_by_namespace(
    tmp_path, capsys, stub_run
):
    printed = _seeded_read(
        tmp_path,
        capsys,
        stub_run,
        _local_read_files(
            tmp_path,
            _USERS_IN_TWO_NAMESPACES,
            (("public", "users"), ("reporting", "users")),
        ),
    )

    assert "Using seeded state" in printed
    assert "does not sync 'public.users' incrementally" in printed
    assert "'reporting.users'" not in printed


def test_a_seed_without_a_namespace_does_not_match_a_namespaced_stream(
    tmp_path, capsys, stub_run, monkeypatch
):
    """A missing namespace is no namespace, not any namespace."""
    error = _refused_read(
        tmp_path,
        capsys,
        stub_run,
        monkeypatch,
        **_local_read_files(tmp_path, {("public", "users"): "incremental"}),
    )

    assert "it names users, and the configured catalog syncs public.users" in error


def test_a_seed_in_another_shape_is_held_to_the_coarse_rule(tmp_path, capsys, stub_run):
    """A GLOBAL state names no stream the harness can match; it runs as long
    as some stream syncs incrementally."""
    files = _local_read_files(tmp_path, {"users": "incremental"})
    (tmp_path / "seed_state.json").write_text(
        json.dumps(
            {"type": "GLOBAL", "global": {"shared_state": {}, "stream_states": []}}
        )
    )

    printed = _seeded_read(tmp_path, capsys, stub_run, files)

    assert "Using seeded state" in printed


def test_an_empty_seed_is_refused(tmp_path, capsys, stub_run, monkeypatch):
    """`[]` would run a cold read labelled seeded."""
    seed = tmp_path / "seed_state.json"
    seed.write_text("[]")

    error = _refused_read(tmp_path, capsys, stub_run, monkeypatch, state_path=str(seed))

    assert "empty list" in error


def test_telemetry_tells_a_seeded_read_from_a_warm_one(
    tmp_path, capsys, stub_run, monkeypatch
):
    seed = tmp_path / "seed_state.json"
    seed.write_text(json.dumps(_SEED))
    stub_run(
        {
            "success": True,
            "exit_code": 0,
            "message_counts": {},
            "record_counts_per_stream": {},
        }
    )
    tracked: dict[str, object] = {}
    monkeypatch.setattr(
        cloud, "track_regression_test", lambda **kwargs: tracked.update(kwargs)
    )

    cloud.regression_test(
        skip_compare=True,
        test_image="airbyte/source-test:2.0.0",
        command="read",
        state_path=str(seed),
        output_dir=str(tmp_path / "read"),
    )
    capsys.readouterr()

    properties = tracked["additional_properties"]
    assert properties["with_state"] is True
    assert properties["state_seeded"] is True


def test_a_cap_below_one_is_refused(tmp_path, capsys, stub_run, monkeypatch):
    """A cap of zero reads nothing and would pass; refusing it is the only
    honest answer."""
    stub_run({"success": True, "exit_code": 0})
    gh_outputs: dict[str, object] = {}
    monkeypatch.setattr(
        cloud, "write_github_output", lambda key, value: gh_outputs.update({key: value})
    )

    with pytest.raises(SystemExit):
        cloud.regression_test(
            skip_compare=True,
            test_image="airbyte/source-test:2.0.0",
            command="read",
            output_dir=str(tmp_path),
            max_records=0,
        )
    capsys.readouterr()

    assert gh_outputs["success"] is False
    assert "--max-records" in str(gh_outputs["error"])


def test_a_cap_on_a_command_without_records_is_ignored_and_said_so(
    tmp_path, capsys, stub_run, monkeypatch
):
    """Only a read emits records; elsewhere the flag is a mistake worth naming."""
    seen: dict[str, object] = {}

    def _fake_run(*, command: Command, output_dir, **kwargs):
        output_dir.mkdir(parents=True, exist_ok=True)
        seen.update(kwargs)
        return {"command": command.value, "success": True, "exit_code": 0}, (
            ComparableOutputs()
        )

    stub_run({"success": True, "exit_code": 0})
    monkeypatch.setattr(cloud, "_run_connector_command", _fake_run)

    cloud.regression_test(
        skip_compare=True,
        test_image="airbyte/source-test:2.0.0",
        command="spec",
        output_dir=str(tmp_path),
        max_records=10,
    )
    printed = " ".join(_ANSI_ESCAPE.sub("", capsys.readouterr().out).split())

    assert seen["max_records"] is None
    assert "--max-records only applies to `read`" in printed


@pytest.mark.parametrize(
    "emitted,stopped",
    [
        pytest.param(3, False, id="exactly-the-cap-is-complete"),
        pytest.param(4, True, id="one-past-the-cap-is-stopped"),
    ],
)
def test_max_records_stops_a_single_version_read_only_past_the_cap(
    tmp_path, capsys, monkeypatch, stub_run, emitted, stopped
):
    """Through the real runner: a read of exactly the cap ends on its own and
    can pass, and only a record past it stops the read, with the cap's worth
    kept."""
    script = tmp_path / "fake_connector.py"
    script.write_text(FAKE_CONNECTOR)

    def _fake_build(runner: ConnectorRunner, _temp_dir) -> list[str]:
        runner._container_name = "connector-test-fake"
        return [sys.executable, str(script), "records", str(emitted), "0"]

    monkeypatch.setattr(ConnectorRunner, "_build_docker_command", _fake_build)
    monkeypatch.setattr(
        connector_runner, "_force_remove_container", lambda _container_name: None
    )
    files = _local_read_files(tmp_path, {"users": "full_refresh"})
    del files["state_path"]

    cloud.regression_test(
        skip_compare=True,
        test_image="airbyte/source-test:2.0.0",
        command="read",
        output_dir=str(tmp_path / "read"),
        max_records=3,
        **files,
    )
    payload = _logged_payload(capsys.readouterr().out)

    assert payload["record_counts_per_stream"] == {"users": 3}
    assert payload["incomplete"] is stopped
    assert payload["success"] is not stopped
    if stopped:
        assert payload["stopped_early"]["reason"] == "cap"
        assert payload["stopped_early"]["records_seen"] == 3
    else:
        assert payload["stopped_early"] is None


def test_the_cap_reaches_both_sides_of_a_read(tmp_path, capsys, stub_comparison_run):
    """Capping one side only would compare a prefix against a full read."""
    seen = stub_comparison_run(dict(_CLEAN_SIDE), dict(_CLEAN_SIDE))

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
        max_records=10,
    )
    capsys.readouterr()

    assert [call["max_records"] for call in seen["calls"]] == [10, 10]


def test_a_connection_runs_config_is_never_written_inside_the_output_dir(
    tmp_path, capsys, stub_run, monkeypatch
):
    """The whole output directory is uploaded as the run's artifact; the config
    carries the secrets, so it must land elsewhere, and privately."""
    stub_run(
        {
            "success": True,
            "exit_code": 0,
            "message_counts": {},
            "record_counts_per_stream": {},
        }
    )
    captured: dict[str, object] = {}

    def _fake_run(*, command: Command, output_dir, **kwargs):
        captured.update(kwargs)
        output_dir.mkdir(parents=True, exist_ok=True)
        return {
            "command": command.value,
            "success": True,
            "exit_code": 0,
            "message_counts": {},
            "record_counts_per_stream": {},
        }, ComparableOutputs()

    monkeypatch.setattr(cloud, "_run_connector_command", _fake_run)
    monkeypatch.setattr(cloud, "should_use_secret_retriever", lambda: False)
    monkeypatch.setattr(cloud, "get_connection_residency", lambda _connection_id: "us")
    monkeypatch.setattr(cloud, "is_running_on_eu_runner", lambda: False)
    monkeypatch.setattr(
        cloud,
        "fetch_connection_data",
        lambda _connection_id: ConnectionData(
            connection_id="c-1",
            source_id="s-1",
            source_name="test",
            source_definition_id="d-1",
            config={"api_key": "sk-live-secret"},
            catalog={"streams": []},
            stream_names=[],
            docker_repository="airbyte/source-test",
            docker_image_tag="2.0.0",
        ),
    )
    output_dir = tmp_path / "out"

    cloud.regression_test(
        skip_compare=True,
        connection_id="c-1",
        command="spec",
        output_dir=str(output_dir),
    )
    capsys.readouterr()

    assert list(output_dir.rglob("config.json")) == []
    assert "sk-live-secret" not in "".join(
        path.read_text() for path in output_dir.rglob("*") if path.is_file()
    )
    assert (output_dir / "connection_data/catalog.json").is_file()
    config_path = captured["config_path"]
    assert isinstance(config_path, Path)
    assert config_path.is_file()
    assert output_dir.resolve() not in config_path.resolve().parents
    assert config_path.stat().st_mode & 0o777 == 0o600
    assert config_path.parent.stat().st_mode & 0o777 == 0o700
    assert json.loads(config_path.read_text()) == {"api_key": "sk-live-secret"}
    # Unset is masked on a connection; the config stays out either way.
    assert captured["output_mode"] == "masked"


def _connection(monkeypatch) -> None:
    """Stub a connection fetch, so `--connection-id` resolves without the API."""
    monkeypatch.setattr(cloud, "should_use_secret_retriever", lambda: False)
    monkeypatch.setattr(cloud, "get_connection_residency", lambda _connection_id: "us")
    monkeypatch.setattr(cloud, "is_running_on_eu_runner", lambda: False)
    monkeypatch.setattr(
        cloud,
        "fetch_connection_data",
        lambda _connection_id: ConnectionData(
            connection_id="c-1",
            source_id="s-1",
            source_name="test",
            source_definition_id="d-1",
            config={"api_key": "x"},
            catalog={"streams": []},
            stream_names=[],
            docker_repository="airbyte/source-test",
            docker_image_tag="2.0.0",
        ),
    )


# What the CLI prints when it picked masked for a connection run on its own.
DEFAULT_MASKED_LINE = (
    "Output mode: masked (the default for a connection run); pass "
    "--output-mode raw to keep the output as emitted"
)


def test_a_connection_run_is_masked_by_default_and_says_so(
    tmp_path, capsys, stub_comparison_run, monkeypatch
):
    """A connection reads a customer's data, so unset is masked there; one
    line says the default applied and how to opt out of it."""
    seen = stub_comparison_run(dict(_CLEAN_SIDE), dict(_CLEAN_SIDE))
    _connection(monkeypatch)

    cloud.regression_test(
        connection_id="c-1",
        command="spec",
        output_dir=str(tmp_path / "out"),
    )
    out = " ".join(_ANSI_ESCAPE.sub("", capsys.readouterr().out).split())

    assert [call["output_mode"] for call in seen["calls"]] == ["masked", "masked"]
    assert _logged_payload(out)["output_mode"] == "masked"
    assert DEFAULT_MASKED_LINE in out
    assert "Masking connector output" in out


def test_a_connection_run_is_raw_when_asked_and_prints_no_warning(
    tmp_path, capsys, stub_comparison_run, monkeypatch
):
    """`raw` on a connection is an explicit opt-in: honoured as given, with no
    warning and no default line, since the caller chose it."""
    seen = stub_comparison_run(dict(_CLEAN_SIDE), dict(_CLEAN_SIDE))
    _connection(monkeypatch)

    cloud.regression_test(
        connection_id="c-1",
        command="spec",
        output_dir=str(tmp_path / "out"),
        output_mode="raw",
    )
    out = " ".join(_ANSI_ESCAPE.sub("", capsys.readouterr().out).split())

    assert [call["output_mode"] for call in seen["calls"]] == ["raw", "raw"]
    assert _logged_payload(out)["output_mode"] == "raw"
    assert "Warning:" not in out
    assert "the default for a connection run" not in out
    assert "Masking connector output" not in out


def test_a_connection_run_still_masks_when_asked(
    tmp_path, capsys, stub_comparison_run, monkeypatch
):
    """An explicit `masked` is the same run as the default, minus the line
    that says a default applied."""
    seen = stub_comparison_run(dict(_CLEAN_SIDE), dict(_CLEAN_SIDE))
    _connection(monkeypatch)

    cloud.regression_test(
        connection_id="c-1",
        command="spec",
        output_dir=str(tmp_path / "out"),
        output_mode="masked",
    )
    out = " ".join(_ANSI_ESCAPE.sub("", capsys.readouterr().out).split())

    assert [call["output_mode"] for call in seen["calls"]] == ["masked", "masked"]
    assert _logged_payload(out)["output_mode"] == "masked"
    assert "Masking connector output" in out
    assert "the default for a connection run" not in out


def test_a_connection_run_with_the_mode_unset_switches_debug_logs_off(
    tmp_path, capsys, stub_comparison_run, monkeypatch
):
    """The default is a masked run in every respect, debug logs included."""
    seen = stub_comparison_run(dict(_CLEAN_SIDE), dict(_CLEAN_SIDE))
    _connection(monkeypatch)

    cloud.regression_test(
        connection_id="c-1",
        command="spec",
        output_dir=str(tmp_path / "out"),
        enable_debug_logs=True,
    )
    out = " ".join(_ANSI_ESCAPE.sub("", capsys.readouterr().out).split())

    assert [call["enable_debug_logs"] for call in seen["calls"]] == [False, False]
    assert "Debug logs are off on masked runs; ignoring --enable-debug-logs" in out
    assert DEFAULT_MASKED_LINE in out


def test_eu_connection_run_defaults_to_masked(
    tmp_path, stub_comparison_run, monkeypatch
):
    seen = stub_comparison_run(dict(_CLEAN_SIDE), dict(_CLEAN_SIDE))
    _connection(monkeypatch)
    monkeypatch.setattr(cloud, "get_connection_residency", lambda _connection_id: "eu")
    monkeypatch.setattr(cloud, "is_running_on_eu_runner", lambda: True)

    cloud.regression_test(
        connection_id="c-1",
        command="spec",
        output_dir=str(tmp_path / "out"),
    )

    assert [call["output_mode"] for call in seen["calls"]] == ["masked", "masked"]


def test_a_gsm_or_image_run_is_raw_by_default(tmp_path, capsys, stub_comparison_run):
    """Integration-test credentials are the team's own fixtures."""
    seen = stub_comparison_run(dict(_CLEAN_SIDE), dict(_CLEAN_SIDE))

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="spec",
        output_dir=str(tmp_path),
    )
    out = " ".join(_ANSI_ESCAPE.sub("", capsys.readouterr().out).split())

    assert [call["output_mode"] for call in seen["calls"]] == ["raw", "raw"]
    assert "Warning:" not in out
    assert "Output mode: masked" not in out


def test_both_sides_of_a_masked_run_hash_under_the_key_file_and_print_it_nowhere(
    tmp_path, capsys, stub_comparison_run, monkeypatch
):
    """The workflow makes one key per run and hands every command the path;
    the control and the target are given that key, so their tokens pair, and
    nothing the CLI prints shows it."""
    seen = stub_comparison_run(dict(_CLEAN_SIDE), dict(_CLEAN_SIDE))
    _connection(monkeypatch)
    key_file = tmp_path / "mask_key"
    key_file.write_text(KEY.hex() + "\n")

    cloud.regression_test(
        connection_id="c-1",
        command="spec",
        output_dir=str(tmp_path / "out"),
        mask_key_path=str(key_file),
    )
    console = capsys.readouterr()

    assert [call["mask_key"] for call in seen["calls"]] == [KEY, KEY]
    assert KEY.hex() not in console.out + console.err
    assert KEY.hex() not in json.dumps(seen["json_output"], default=str)
    assert KEY.hex() not in "".join(seen["step_summary"])


def test_without_a_key_file_a_masked_run_makes_one_key_for_both_sides(
    tmp_path, capsys, stub_comparison_run, monkeypatch
):
    """A run by hand gets a fresh key for its process, shared by its two
    sides so they still pair, and matching no other run's."""
    seen = stub_comparison_run(dict(_CLEAN_SIDE), dict(_CLEAN_SIDE))
    _connection(monkeypatch)

    cloud.regression_test(
        connection_id="c-1", command="spec", output_dir=str(tmp_path / "out")
    )
    capsys.readouterr()

    control_key, target_key = (call["mask_key"] for call in seen["calls"])
    assert isinstance(control_key, bytes) and len(control_key) == 32
    assert control_key == target_key
    assert control_key != KEY


def test_a_raw_run_is_given_no_key_and_does_not_read_the_file(
    tmp_path, capsys, stub_comparison_run, monkeypatch
):
    """`--mask-key-path` is in the workflow's common arguments whatever the
    mode; a raw run has no tokens to key, so it neither reads nor judges the
    file, and a missing one cannot fail it."""
    seen = stub_comparison_run(dict(_CLEAN_SIDE), dict(_CLEAN_SIDE))
    _connection(monkeypatch)

    cloud.regression_test(
        connection_id="c-1",
        command="spec",
        output_dir=str(tmp_path / "out"),
        output_mode="raw",
        mask_key_path=str(tmp_path / "no_such_file"),
    )
    capsys.readouterr()

    assert [call["mask_key"] for call in seen["calls"]] == [None, None]


@pytest.mark.parametrize(
    "content",
    [
        pytest.param(None, id="missing-file"),
        pytest.param("", id="empty"),
        pytest.param("not a key at all", id="not-hex"),
        pytest.param("ab" * 16, id="too-short"),
        pytest.param("ab" * 33, id="too-long"),
    ],
)
def test_a_bad_key_file_is_refused_before_anything_is_fetched(
    tmp_path, capsys, stub_comparison_run, monkeypatch, content
):
    """A path that does not hold a 32-byte key as 64 hex characters fails the
    run in seconds, before the connection is fetched, and the error names the
    file rather than what it held."""
    stub_comparison_run(dict(_CLEAN_SIDE), dict(_CLEAN_SIDE))
    _connection(monkeypatch)
    monkeypatch.setattr(
        cloud, "fetch_connection_data", lambda _id: pytest.fail("fetched a connection")
    )
    gh_outputs: dict[str, object] = {}
    monkeypatch.setattr(
        cloud, "write_github_output", lambda key, value: gh_outputs.update({key: value})
    )
    key_file = tmp_path / "mask_key"
    if content is not None:
        key_file.write_text(content)

    with pytest.raises(SystemExit):
        cloud.regression_test(
            connection_id="c-1",
            command="spec",
            output_dir=str(tmp_path / "out"),
            mask_key_path=str(key_file),
        )
    console = capsys.readouterr()

    assert gh_outputs["success"] is False
    error = str(gh_outputs["error"])
    assert error.startswith("--mask-key-path ")
    assert str(key_file) in error
    if content:
        assert content not in error
        assert content not in console.out + console.err


@pytest.fixture
def stub_container(monkeypatch, tmp_path):
    """Run the real `_run_connector_command` against a fake container.

    Returns the `ExecutionInputs` each container was started with, so a test
    can assert on the environment the connector would have seen.
    """
    started: list[ExecutionInputs] = []

    class _StubResult:
        success = True
        exit_code = 0
        stdout_file_path = tmp_path / "stdout.txt"
        stderr_file_path = tmp_path / "stderr.txt"
        stopped_early = None
        airbyte_messages = ()
        # What `save_artifacts` would have collected: no analytics counters.
        summary = SimpleNamespace(analytics={})

        def save_artifacts(self, _output_dir: Path) -> None:
            pass

        def get_message_count_per_type(self) -> dict:
            return {}

        def get_record_count_per_stream(self) -> dict:
            return {}

        def get_connection_status(self):
            return SimpleNamespace(
                status=SimpleNamespace(value="SUCCEEDED"), message=None
            )

    class _StubRunner:
        def __init__(self, execution_inputs: ExecutionInputs, **_kwargs) -> None:
            started.append(execution_inputs)

        def run(self) -> _StubResult:
            return _StubResult()

    monkeypatch.setattr(cloud, "ConnectorRunner", _StubRunner)
    monkeypatch.setattr(
        cloud.ComparableOutputs,
        "from_execution_result",
        classmethod(lambda _cls, _result: ComparableOutputs()),
    )
    return started


@pytest.fixture
def harness_debug_logging(monkeypatch) -> list[dict]:
    """Record harness `logging.basicConfig` calls instead of reconfiguring
    the test process's root logger."""
    calls: list[dict] = []
    monkeypatch.setattr(cloud.logging, "basicConfig", lambda **kw: calls.append(kw))
    return calls


@pytest.mark.parametrize(
    "debug_kwargs,named",
    [
        pytest.param({"enable_debug_logs": True}, "--enable-debug-logs", id="flag"),
        pytest.param(
            {"extra_env": ["LOG_LEVEL=DEBUG"]}, "LOG_LEVEL=DEBUG", id="extra-env-debug"
        ),
        pytest.param(
            {"extra_env": ["LOG_LEVEL=trace"]}, "LOG_LEVEL=trace", id="extra-env-trace"
        ),
        pytest.param(
            {"enable_debug_logs": True, "extra_env": ["LOG_LEVEL=DEBUG"]},
            "--enable-debug-logs and LOG_LEVEL=DEBUG",
            id="both",
        ),
    ],
)
def test_a_masked_run_switches_debug_logs_off_and_says_so(
    tmp_path,
    capsys,
    stub_run,
    stub_container,
    harness_debug_logging,
    debug_kwargs,
    named,
):
    """Debug logs are off on masked runs for now; the run goes on without them."""
    cloud.regression_test(
        skip_compare=True,
        test_image="airbyte/source-test:2.0.0",
        command="spec",
        output_dir=str(tmp_path),
        output_mode="masked",
        **debug_kwargs,
    )
    out = " ".join(_ANSI_ESCAPE.sub("", capsys.readouterr().out).split())

    assert [inputs.environment_variables for inputs in stub_container] == [None]
    assert harness_debug_logging == []
    assert f"Debug logs are off on masked runs; ignoring {named}" in out
    assert _logged_payload(out)["output_mode"] == "masked"
    assert "debug logs off" in (tmp_path / "report.html").read_text()


@pytest.mark.parametrize(
    "explicit",
    [
        pytest.param(None, id="default-is-raw"),
        pytest.param("raw", id="raw-explicit"),
    ],
)
def test_a_raw_run_keeps_debug_logs(
    tmp_path, capsys, stub_run, stub_container, harness_debug_logging, explicit
):
    cloud.regression_test(
        skip_compare=True,
        test_image="airbyte/source-test:2.0.0",
        command="spec",
        output_dir=str(tmp_path),
        output_mode=explicit,
        enable_debug_logs=True,
    )
    out = capsys.readouterr().out

    assert [inputs.environment_variables for inputs in stub_container] == [
        {"LOG_LEVEL": "DEBUG"}
    ]
    assert len(harness_debug_logging) == 1
    assert "Debug logs are off" not in out


def test_a_masked_run_keeps_a_log_level_above_debug(
    tmp_path, capsys, stub_run, stub_container
):
    """Only DEBUG and TRACE count as debug logs; any other level is kept."""
    cloud.regression_test(
        skip_compare=True,
        test_image="airbyte/source-test:2.0.0",
        command="spec",
        output_dir=str(tmp_path),
        output_mode="masked",
        extra_env=["LOG_LEVEL=INFO", "AIRBYTE_EDITION=CLOUD"],
    )
    out = capsys.readouterr().out

    assert [inputs.environment_variables for inputs in stub_container] == [
        {"LOG_LEVEL": "INFO", "AIRBYTE_EDITION": "CLOUD"}
    ]
    assert "Debug logs are off" not in out


def test_the_output_mode_reaches_both_sides_and_the_payload(
    tmp_path, capsys, stub_comparison_run
):
    """One mode per run: the sides must mask alike, and every consumer of the
    payload must be able to tell whether the artifacts hold raw data."""
    seen = stub_comparison_run(
        {**_CLEAN_SIDE, "output_mode": "masked"},
        {**_CLEAN_SIDE, "output_mode": "masked"},
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
        output_mode="masked",
    )
    payload = _logged_payload(capsys.readouterr().out)

    assert [call["output_mode"] for call in seen["calls"]] == [
        "masked",
        "masked",
    ]
    assert payload["output_mode"] == "masked"
    assert payload["target"]["output_mode"] == "masked"
    assert seen["json_output"]["output_mode"] == "masked"


def test_the_readable_fields_reach_the_consolidated_payload(
    tmp_path, capsys, stub_comparison_run
):
    """What a masked run left readable travels beside `output_mode`, so the
    `regression_report` output can say it without opening an artifact."""
    readable = {
        "users": {
            "cursor": ["updated_at"],
            "readable": True,
            "declared": "string/date-time",
            "reason": "readable (string/date-time)",
        }
    }
    seen = stub_comparison_run(
        {**_CLEAN_SIDE, "output_mode": "masked", "readable_fields": readable},
        {**_CLEAN_SIDE, "output_mode": "masked", "readable_fields": readable},
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
        output_mode="masked",
    )
    payload = _logged_payload(capsys.readouterr().out)

    assert payload["readable_fields"] == readable
    assert payload["target"]["readable_fields"] == readable
    assert seen["json_output"]["readable_fields"] == readable


def test_a_raw_payload_carries_no_readable_fields(
    tmp_path, capsys, stub_comparison_run
):
    seen = stub_comparison_run(
        {**_CLEAN_SIDE, "output_mode": "raw"}, {**_CLEAN_SIDE, "output_mode": "raw"}
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
        output_mode="raw",
    )
    payload = _logged_payload(capsys.readouterr().out)

    assert "readable_fields" not in payload
    assert "readable_fields" not in seen["json_output"]


def test_the_output_mode_defaults_to_raw(tmp_path, capsys, stub_comparison_run):
    seen = stub_comparison_run(dict(_CLEAN_SIDE), dict(_CLEAN_SIDE))

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
    )
    payload = _logged_payload(capsys.readouterr().out)

    assert [call["output_mode"] for call in seen["calls"]] == ["raw", "raw"]
    assert payload["output_mode"] == "raw"


def test_a_single_version_run_carries_its_output_mode(
    tmp_path, capsys, stub_run, monkeypatch
):
    captured: dict[str, object] = {}
    gh_outputs = stub_run(
        {
            "success": True,
            "exit_code": 0,
            "message_counts": {},
            "record_counts_per_stream": {},
            "output_mode": "masked",
        }
    )
    real_run = cloud._run_connector_command

    def _spy(**kwargs):
        captured.update(kwargs)
        return real_run(**kwargs)

    monkeypatch.setattr(cloud, "_run_connector_command", _spy)

    cloud.regression_test(
        skip_compare=True,
        test_image="airbyte/source-test:2.0.0",
        command="spec",
        output_dir=str(tmp_path),
        output_mode="masked",
    )
    payload = _logged_payload(capsys.readouterr().out)

    assert captured["output_mode"] == "masked"
    assert payload["output_mode"] == "masked"
    assert gh_outputs["output_mode"] == "masked"


@pytest.mark.parametrize(
    "command,expects_readable_fields",
    [
        pytest.param("read", True, id="read-reads-records"),
        pytest.param("spec", False, id="spec-cannot"),
        pytest.param("check", False, id="check-cannot"),
        pytest.param("discover", False, id="discover-cannot"),
    ],
)
def test_only_record_reading_commands_report_readable_fields(
    tmp_path, capsys, stub_run, stub_container, command, expects_readable_fields
):
    """A command that emits no records gets no schema-enriched catalog, so a
    readable-fields list there would say `masked: schema missing` for every
    stream and `cursor readable on 0 of N` in the summary."""
    config = tmp_path / "config.json"
    config.write_text(json.dumps({"api_key": "secret"}))
    catalog = tmp_path / "catalog.json"
    catalog.write_text(
        json.dumps(
            {
                "streams": [
                    {
                        "stream": {
                            "name": "users",
                            "json_schema": {},
                            "supported_sync_modes": ["incremental"],
                            "default_cursor_field": ["updated_at"],
                        },
                        "sync_mode": "incremental",
                        "destination_sync_mode": "append",
                    }
                ]
            }
        )
    )

    cloud.regression_test(
        skip_compare=True,
        test_image="airbyte/source-test:2.0.0",
        command=command,
        config_path=str(config),
        catalog_path=str(catalog),
        output_dir=str(tmp_path / command),
        output_mode="masked",
    )
    payload = _logged_payload(capsys.readouterr().out)
    summary = "\n".join(stub_run.step_summary)

    assert payload["output_mode"] == "masked"
    assert ("readable_fields" in payload) is expects_readable_fields
    assert ("cursor readable on" in summary) is expects_readable_fields
    if expects_readable_fields:
        assert payload["readable_fields"]["users"]["readable"] is False


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


def test_final_state_comparison_excludes_target_only_streams():
    target_only = ("activity", "ad", "ad_group", "campaign", "conversion")
    shared_state = {"cursor": "same"}
    control = {(None, "shared"): shared_state}
    target = {
        **control,
        **{(None, name): {"cursor": "target-only"} for name in target_only},
    }

    checks, _blocks, detail = cloud._final_state_comparison(
        control, target, no_control_streams=target_only
    )

    assert checks[0].status == "pass"
    assert detail["final_state"]["not_compared"] == sorted(target_only)
    assert "5 stream(s) read by the target only were not compared" in (
        checks[0].summary
    )


def test_final_state_comparison_still_fails_for_one_sided_shared_state():
    target_only = ("new_stream",)

    checks, _blocks, detail = cloud._final_state_comparison(
        {(None, "shared"): {"cursor": "control"}},
        {},
        no_control_streams=target_only,
    )

    assert checks[0].status == "fail"
    assert detail["final_state"]["not_compared"] == ["new_stream"]


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
    # The diff itself has to survive the trip into the `regression_report`
    # output; the printed copy of this raw run says only that it was omitted.
    kept = seen["json_output"]["comparison"]["final_state"]["streams"]["users"]
    assert kept["diff"]
    assert "diff" not in final_state["streams"]["users"]
    assert final_state["streams"]["users"]["diff_omitted"]

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
# The printed payload on a raw run: shape and counts, no record values
# --------------------------------------------------------------------------

# Every list in the comparison payload that carries record values.
EXAMPLE_LIST_KEYS = {
    "missing_pk_examples",
    "duplicate_pk_examples",
    "value_diff_examples",
    "partial_group_diff_examples",
}


def _comparison_with_examples():
    """A read comparison whose every example list holds a record value."""
    from airbyte_ops_mcp.regression_tests.regression import (
        ComparisonResult,
        RecordComparisonSummary,
        RecordDiff,
        StreamComparisonResult,
    )

    changed = {
        "values_changed": {
            "root['name']": {"old_value": "Alice", "new_value": "Alicia"}
        }
    }
    diff = RecordDiff(
        stream_name="users",
        records_with_value_diff=[{"pk": ["alice@example.com"], "diff": changed}],
        partial_group_diffs=[
            {"pk": ["bob@example.com"], "diff": changed, "note": "group cut"}
        ],
    )
    return RecordComparisonSummary(
        passed=False,
        count_comparison=ComparisonResult(passed=True, message="Record counts match"),
        pk_presence=ComparisonResult(
            passed=False,
            stream_results={
                "users": StreamComparisonResult(
                    stream_name="users",
                    passed=False,
                    missing_pks=[("carol@example.com",)],
                )
            },
        ),
        target_pk_uniqueness=ComparisonResult(
            passed=False,
            stream_results={
                "users": StreamComparisonResult(
                    stream_name="users",
                    passed=False,
                    duplicate_pks=[("dave@example.com",)],
                    duplicate_pk_counts={("dave@example.com",): 2},
                )
            },
        ),
        field_comparison=ComparisonResult(
            passed=False,
            stream_results={
                "users": StreamComparisonResult(
                    stream_name="users", passed=False, record_diff=diff
                )
            },
        ),
    )


def _example_lists(payload: dict) -> dict[str, list]:
    """Every `*_examples` list in the payload, by key, wherever it sits."""
    found: dict[str, list] = {}

    def walk(value) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                if key.endswith("_examples") and isinstance(item, list):
                    found[key] = item
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    walk(payload)
    return found


def _diffing_read(tmp_path, monkeypatch, stub_comparison_run, **kwargs) -> dict:
    """A comparison read whose record comparison found an example of everything."""
    side = {"success": True, "exit_code": 0}
    seen = stub_comparison_run(dict(side), dict(side))
    monkeypatch.setattr(
        cloud,
        "_compare_read_records",
        lambda **_kwargs: (_comparison_with_examples(), None),
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
        **kwargs,
    )
    return seen


def test_a_raw_run_prints_the_payload_without_its_examples(
    tmp_path, capsys, monkeypatch, stub_comparison_run
):
    """The job log outlives the artifacts and nothing masks it, so the printed
    copy keeps the shape and the counts and drops every record value; the
    `regression_report` output keeps them, since the artifacts are the place
    for detail."""
    seen = _diffing_read(tmp_path, monkeypatch, stub_comparison_run, output_mode="raw")
    printed = _logged_payload(capsys.readouterr().out)

    assert printed["examples_omitted"] is True
    assert set(_example_lists(printed)) == EXAMPLE_LIST_KEYS
    assert all(examples == [] for examples in _example_lists(printed).values())
    assert "example.com" not in json.dumps(printed)
    checks = printed["record_comparison"]["checks"]
    assert checks["pk_presence"]["streams"]["users"]["missing_pk_count"] == 1
    assert checks["pk_uniqueness_target"]["streams"]["users"]["duplicate_pk_count"] == 1
    assert checks["field_values"]["streams"]["users"]["records_with_value_diff"] == 1
    assert checks["field_values"]["streams"]["users"]["partial_group_diff_count"] == 1
    assert printed["success"] is False

    kept = seen["json_output"]
    assert "examples_omitted" not in kept
    assert set(_example_lists(kept)) == EXAMPLE_LIST_KEYS
    assert all(examples for examples in _example_lists(kept).values())
    assert "alice@example.com" in json.dumps(kept)


def test_a_masked_run_prints_its_examples(
    tmp_path, capsys, monkeypatch, stub_comparison_run
):
    """On a masked run every example is a token, so the log may carry them."""
    _diffing_read(tmp_path, monkeypatch, stub_comparison_run, output_mode="masked")
    printed = _logged_payload(capsys.readouterr().out)

    assert "examples_omitted" not in printed
    assert set(_example_lists(printed)) == EXAMPLE_LIST_KEYS
    assert all(examples for examples in _example_lists(printed).values())


@pytest.mark.parametrize(
    "output_mode,omitted",
    [pytest.param("raw", True, id="raw"), pytest.param("masked", False, id="masked")],
)
def test_a_raw_run_prints_a_final_state_diff_as_omitted(
    tmp_path, capsys, stub_comparison_run, output_mode, omitted
):
    """A state diff is the one diff that carries customer values: a moved
    cursor puts both sides' values in `values_changed`. The printed copy says
    the diff was omitted and why; the `regression_report` output keeps it."""
    seen = stub_comparison_run(
        dict(_CLEAN_RUN),
        dict(_CLEAN_RUN),
        target_outputs=_state_outputs({"users": {"updated_at": "2024-02-01"}}),
        control_outputs=_state_outputs({"users": {"updated_at": "2024-01-01"}}),
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
        output_mode=output_mode,
    )
    printed = _logged_payload(capsys.readouterr().out)

    entry = printed["comparison"]["final_state"]["streams"]["users"]
    assert entry["passed"] is False
    assert ("diff" in entry) is not omitted
    assert ("diff_omitted" in entry) is omitted
    assert ("2024-01-01" in json.dumps(printed["comparison"])) is not omitted

    kept = seen["json_output"]["comparison"]["final_state"]["streams"]["users"]
    assert kept["diff"]
    assert "diff_omitted" not in kept


@pytest.mark.parametrize(
    "output_mode,omitted",
    [
        pytest.param(None, True, id="raw-by-default"),
        pytest.param("masked", False, id="masked"),
    ],
)
def test_a_single_version_run_prints_under_the_same_rule(
    tmp_path, capsys, stub_run, output_mode, omitted
):
    """One rule for both payload shapes, so a reader of either knows whether
    the lists were emptied, even where there is nothing to empty today."""
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
        output_mode=output_mode,
    )
    printed = _logged_payload(capsys.readouterr().out)

    assert ("examples_omitted" in printed) is omitted
    assert printed.get("examples_omitted", False) is omitted


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


def test_a_comparison_without_replay_still_captures_both_sides(
    tmp_path, capsys, stub_comparison_run
):
    """Replay is one use of the capture, not the reason for it.

    The per-version request counts come from the capture, and a run made with
    `--no-http-replay` is the one where a reviewer most needs them: both
    versions hit the live API, so a count that moved is the first thing to
    check. Tying the capture to replay left exactly those runs with no numbers.
    """
    seen = stub_comparison_run(dict(_CLEAN_SIDE), dict(_CLEAN_SIDE))

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
        enable_http_replay=False,
    )
    capsys.readouterr()

    control_call, target_call = seen["calls"]
    assert control_call["enable_http_metrics"] is True
    assert target_call["enable_http_metrics"] is True
    # Captured, not replayed: the two decisions stay separate.
    assert target_call.get("replay_from") is None
    assert "flow_count" in seen["report_control"]["http_metrics"]
    assert "flow_count" in seen["report_target"]["http_metrics"]


def test_single_version_mode_never_starts_a_proxy(
    tmp_path, capsys, stub_run, monkeypatch
):
    """`--skip-compare` has nothing to compare counts against, so it stays proxy-free."""
    stub_run(
        {
            "success": True,
            "exit_code": 0,
            "message_counts": {},
            "record_counts_per_stream": {},
        }
    )

    def _no_proxy(*_args, **_kwargs):
        raise AssertionError("a single-version run must not start mitmproxy")

    monkeypatch.setattr(cloud, "_run_with_optional_http_metrics", _no_proxy)
    monkeypatch.setattr(cloud, "MitmproxyManager", _no_proxy)

    cloud.regression_test(
        skip_compare=True,
        test_image="airbyte/source-test:2.0.0",
        command="spec",
        output_dir=str(tmp_path),
        enable_http_metrics=True,
    )
    capsys.readouterr()

    assert "HTTP requests" not in "\n".join(stub_run.step_summary)


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


def test_the_dump_size_cap_is_not_a_replay_tuning_flag(
    tmp_path, capsys, stub_comparison_run
):
    """`--http-replay-max-dump-size-mb` decides whether a recorded dump is kept.

    Every comparison records, replay or not, so the cap applies on a
    `--no-http-replay` run too; warning that it is ignored there would send a
    reader looking for a dump the run deleted on purpose.
    """
    seen = stub_comparison_run(dict(_CLEAN_SIDE), dict(_CLEAN_SIDE))

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
        enable_http_replay=False,
        http_replay_max_dump_size_mb=64,
    )
    captured = capsys.readouterr()

    assert "Replay tuning flags do nothing" not in captured.out + captured.err
    _control_call, target_call = seen["calls"]
    assert target_call["replay_options"].max_dump_bytes == 64 * 1024 * 1024


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


# ---------------------------------------------------------------------------
# Stopped-early reads: --read-timeout and the per-side `stopped_early` key
# ---------------------------------------------------------------------------

_STOPPABLE_SIDE = {
    "success": True,
    "exit_code": 0,
    "message_counts": {"RECORD": 12},
    "record_counts_per_stream": {"users": 12},
}


class _FakeClock:
    """The read budget's monotonic clock, moved only by the test."""

    def __init__(self) -> None:
        self.now = 1_000.0

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


@pytest.fixture
def fake_clock(monkeypatch):
    clock = _FakeClock()
    monkeypatch.setattr(read_budget, "monotonic", clock)
    return clock


def _each_side_reads_to_its_deadline(monkeypatch, clock: _FakeClock) -> None:
    """Make each stubbed side spend its whole share, as a long read does."""
    stub = cloud._run_with_optional_http_metrics

    def _run(**kwargs):
        clock.advance(kwargs["timeout_seconds"])
        return stub(**kwargs)

    monkeypatch.setattr(cloud, "_run_with_optional_http_metrics", _run)


def test_the_two_reads_share_one_read_timeout(
    tmp_path, capsys, monkeypatch, fake_clock, stub_comparison_run
):
    """Back to back, both reads and the reserve fit inside the one budget."""
    seen = stub_comparison_run(dict(_STOPPABLE_SIDE), dict(_STOPPABLE_SIDE))
    _each_side_reads_to_its_deadline(monkeypatch, fake_clock)

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
        read_timeout=600,
    )
    capsys.readouterr()

    # 60 s kept for the report leaves 540 s to read: the control may take 60%
    # of it, and the target gets what the control left.
    control_call, target_call = seen["calls"]
    assert control_call["timeout_seconds"] == 324
    assert target_call["timeout_seconds"] == 216


def test_setup_is_charged_to_the_read_timeout(
    tmp_path, capsys, monkeypatch, fake_clock, stub_comparison_run
):
    seen = stub_comparison_run(dict(_STOPPABLE_SIDE), dict(_STOPPABLE_SIDE))
    _each_side_reads_to_its_deadline(monkeypatch, fake_clock)

    def _slow_pull(_image):
        fake_clock.advance(50)
        return True

    monkeypatch.setattr(cloud, "ensure_image_available", _slow_pull)

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
        read_timeout=600,
    )
    capsys.readouterr()

    # Two pulls took 100 s of the 540 s to read in.
    assert [call["timeout_seconds"] for call in seen["calls"]] == [264, 176]


def test_a_target_with_no_time_left_is_not_started_and_the_run_is_incomplete(
    tmp_path, capsys, monkeypatch, fake_clock
):
    """The failure the shared budget exists for: the report still gets written.

    The control stops at its share, but parsing its output runs past what was
    left for the target. Starting the target anyway would push the report past
    the step's timeout, so it does not start and the run reads incomplete.
    """
    gh_outputs: dict[str, object] = {}
    step_summary: list[str] = []
    monkeypatch.setattr(cloud, "ensure_image_available", lambda _image: True)
    monkeypatch.setattr(cloud, "track_regression_test", lambda **_kwargs: None)
    monkeypatch.setattr(cloud, "write_github_summary", step_summary.append)
    monkeypatch.setattr(cloud, "write_github_outputs", gh_outputs.update)
    monkeypatch.setattr(cloud, "write_json_output", lambda _key, _data: None)
    started: list[tuple[TargetOrControl, int]] = []

    def _control_overruns(
        *, command, output_dir, target_or_control, timeout_seconds, **_kwargs
    ):
        started.append((target_or_control, timeout_seconds))
        output_dir.mkdir(parents=True, exist_ok=True)
        fake_clock.advance(600)
        stopped = {"reason": "timeout", "records_seen": 12, "elapsed_s": 324.0}
        return (
            {"command": command.value, **_STOPPABLE_SIDE, "stopped_early": stopped},
            ComparableOutputs(),
        )

    monkeypatch.setattr(cloud, "_run_connector_command", _control_overruns)
    # No mitmdump on this runner: the control reads without a proxy.
    monkeypatch.setattr(
        cloud.MitmproxyManager, "running", lambda _self: contextlib.nullcontext(None)
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
        read_timeout=600,
    )
    payload = _logged_payload(capsys.readouterr().out)

    assert started == [(TargetOrControl.CONTROL, 324)]
    assert payload["target"]["stopped_early"] == {
        "reason": "timeout",
        "records_seen": 0,
        "elapsed_s": 0.0,
        "share_s": 0,
        "budget_s": 600,
    }
    assert payload["control"]["stopped_early"]["share_s"] == 324
    # Neither side reads as a pass in its own entry: one was stopped, the
    # other never started. Both exited cleanly.
    assert payload["target"]["success"] is False
    assert payload["target"]["exited_cleanly"] is True
    assert payload["control"]["success"] is False
    assert payload["control"]["exited_cleanly"] is True
    assert payload["success"] is False
    assert payload["incomplete"] is True
    assert payload["regression_detected"] is False
    assert gh_outputs["success"] is False
    assert gh_outputs["incomplete"] is True

    assert (tmp_path / cloud.HTML_REPORT_FILENAME).is_file()
    assert (tmp_path / "report.md").is_file()
    assert (tmp_path / "target" / "stdout.txt").read_text() == ""
    summary = "\n".join(step_summary)
    assert (
        "INCOMPLETE — stopped early (timeout) after 12 (control) / 0 (target) "
        "records" in summary
    )
    assert (
        "- Control: stopped early (timeout) after 12 records in 324 s, at the end "
        "of its 324-second share of the 10-minute read budget" in summary
    )
    assert (
        "- Target: stopped early (timeout) after 0 records in 0 s, without "
        "starting: nothing was left of the 10-minute read budget" in summary
    )


def test_a_side_with_no_time_left_starts_neither_proxy_nor_container(
    tmp_path, monkeypatch
):
    def _must_not_start(*_args, **_kwargs):
        raise AssertionError("a side with no time left was started")

    monkeypatch.setattr(cloud, "MitmproxyManager", _must_not_start)
    monkeypatch.setattr(cloud, "_run_connector_command", _must_not_start)

    result, outputs = cloud._run_with_optional_http_metrics(
        connector_image="airbyte/source-test:2.0.0",
        command=Command.READ,
        output_dir=tmp_path / "target",
        target_or_control=TargetOrControl.TARGET,
        enable_http_metrics=True,
        config_path=None,
        catalog_path=None,
        state_path=None,
        replay_expected=True,
        timeout_seconds=0,
    )

    assert result["success"] is True
    assert result["exit_code"] == 0
    assert result["stopped_early"] == {
        "reason": "timeout",
        "records_seen": 0,
        "elapsed_s": 0.0,
    }
    assert result["message_counts"] == {}
    assert "http_dump_file" not in result
    assert (tmp_path / "target" / "stdout.txt").read_text() == ""
    assert "was not started" in (tmp_path / "target" / "stderr.txt").read_text()
    assert outputs == ComparableOutputs()


def test_read_timeout_leaves_the_other_commands_on_the_runner_default(
    tmp_path, capsys, stub_comparison_run
):
    """`spec` finishes in seconds; the deadline exists for the read that does not."""
    seen = stub_comparison_run(dict(_CLEAN_RUN), dict(_CLEAN_RUN))

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="spec",
        output_dir=str(tmp_path),
        read_timeout=600,
    )
    capsys.readouterr()

    assert [call["timeout_seconds"] for call in seen["calls"]] == [None, None]


def test_without_read_timeout_the_reads_share_the_runner_default(
    tmp_path, capsys, fake_clock, stub_comparison_run
):
    seen = stub_comparison_run(dict(_STOPPABLE_SIDE), dict(_STOPPABLE_SIDE))

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
    )
    capsys.readouterr()

    # Ten minutes kept back; the clock never moved, so the target gets the rest.
    read_time_s = DEFAULT_TIMEOUT_SECONDS - 600
    assert [call["timeout_seconds"] for call in seen["calls"]] == [
        read_time_s * 60 // 100,
        read_time_s,
    ]


def test_a_single_version_read_keeps_the_reserve_and_pays_for_setup(
    tmp_path, capsys, monkeypatch, fake_clock, stub_run
):
    """The one read gets what is left after setup and the reserve, as a
    comparison's target does, so its report still lands inside the step."""
    stub_run(dict(_STOPPABLE_SIDE))

    def _slow_pull(_image):
        fake_clock.advance(100)
        return True

    monkeypatch.setattr(cloud, "ensure_image_available", _slow_pull)
    inner = cloud._run_connector_command
    calls: list[dict] = []

    def _tracking(**kwargs):
        calls.append(kwargs)
        return inner(**kwargs)

    monkeypatch.setattr(cloud, "_run_connector_command", _tracking)

    cloud.regression_test(
        skip_compare=True,
        test_image="airbyte/source-test:2.0.0",
        command="read",
        output_dir=str(tmp_path),
        read_timeout=900,
    )
    capsys.readouterr()

    # A tenth of 900 s kept back for the report, and the pull took 100 s.
    assert [call["timeout_seconds"] for call in calls] == [710]


def test_a_single_version_read_with_no_time_left_is_not_started(
    tmp_path, capsys, monkeypatch, fake_clock, stub_run
):
    stub_run(dict(_STOPPABLE_SIDE))

    def _slow_pull(_image):
        fake_clock.advance(900)
        return True

    def _must_not_start(**_kwargs):
        raise AssertionError("a read with no time left was started")

    monkeypatch.setattr(cloud, "ensure_image_available", _slow_pull)
    monkeypatch.setattr(cloud, "_run_connector_command", _must_not_start)

    cloud.regression_test(
        skip_compare=True,
        test_image="airbyte/source-test:2.0.0",
        command="read",
        output_dir=str(tmp_path),
        read_timeout=900,
    )
    payload = _logged_payload(capsys.readouterr().out)

    assert payload["success"] is False
    assert payload["incomplete"] is True
    assert payload["stopped_early"] == {
        "reason": "timeout",
        "records_seen": 0,
        "elapsed_s": 0.0,
        "share_s": 0,
        "budget_s": 900,
    }


def test_a_masked_read_that_never_started_still_says_it_is_masked(
    tmp_path, capsys, monkeypatch, fake_clock, stub_run
):
    """No container ran, so nothing was masked, but the run was a masked one:
    its payload and its report say so, as any other side's would."""
    stub_run(dict(_STOPPABLE_SIDE))

    def _slow_pull(_image):
        fake_clock.advance(900)
        return True

    monkeypatch.setattr(cloud, "ensure_image_available", _slow_pull)

    cloud.regression_test(
        skip_compare=True,
        test_image="airbyte/source-test:2.0.0",
        command="read",
        output_dir=str(tmp_path),
        read_timeout=900,
        output_mode="masked",
    )
    payload = _logged_payload(capsys.readouterr().out)

    assert payload["incomplete"] is True
    assert payload["output_mode"] == "masked"
    html = (tmp_path / "report.html").read_text()
    assert "record values are type-and-length tokens" in html

    side, _ = cloud._run_with_optional_http_metrics(
        connector_image="airbyte/source-test:2.0.0",
        command=Command.READ,
        output_dir=tmp_path / "control",
        target_or_control=TargetOrControl.CONTROL,
        enable_http_metrics=True,
        config_path=None,
        catalog_path=None,
        state_path=None,
        timeout_seconds=0,
        output_mode="masked",
    )
    assert side["output_mode"] == "masked"


def test_a_non_positive_read_timeout_is_rejected(tmp_path, stub_comparison_run):
    stub_comparison_run(dict(_STOPPABLE_SIDE), dict(_STOPPABLE_SIDE))

    with pytest.raises(SystemExit):
        cloud.regression_test(
            test_image="airbyte/source-test:2.0.0",
            control_image="airbyte/source-test:1.0.0",
            command="read",
            output_dir=str(tmp_path),
            read_timeout=0,
        )


def test_a_stopped_side_is_carried_into_the_payload_as_itself(
    tmp_path, capsys, fake_clock, stub_comparison_run
):
    """The stop travels beside each side's result, as the runner reported it.

    A deadline stop also names the share of the budget it stopped at.
    """
    stopped = {"reason": "timeout", "records_seen": 12, "elapsed_s": 10200.0}
    stub_comparison_run(
        {**_STOPPABLE_SIDE, "stopped_early": stopped},
        {**_STOPPABLE_SIDE, "stopped_early": None},
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
        skip_record_comparison=True,
    )
    payload = _logged_payload(capsys.readouterr().out)

    assert payload["target"]["stopped_early"] == {
        **stopped,
        "share_s": DEFAULT_TIMEOUT_SECONDS - 600,
        "budget_s": DEFAULT_TIMEOUT_SECONDS,
    }
    assert payload["control"]["stopped_early"] is None


def test_a_stopped_side_does_not_read_as_a_pass_in_the_comparison_payload(
    tmp_path, capsys, stub_comparison_run
):
    """Per side, `success` is the verdict, as in single-version mode.

    The container exited cleanly, so `exited_cleanly` stays true, but the
    side read only part of what it would have: its `success` is false. The
    side that ran to completion keeps its pass.
    """
    stub_comparison_run(
        {**_STOPPABLE_SIDE, "stopped_early": _STOPPED_TIMEOUT},
        {**_STOPPABLE_SIDE, "stopped_early": None},
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
        skip_record_comparison=True,
    )
    payload = _logged_payload(capsys.readouterr().out)

    assert payload["target"]["success"] is False
    assert payload["target"]["exited_cleanly"] is True
    assert payload["control"]["success"] is True
    assert payload["control"]["exited_cleanly"] is True
    assert payload["success"] is False
    assert payload["incomplete"] is True
    assert payload["both_succeeded"] is True


def test_run_connector_command_reports_the_stop_and_passes_the_limits(
    tmp_path, monkeypatch
):
    """The one place the runner's result becomes the dict every surface reads."""
    captured: dict[str, object] = {}

    class _FakeRunner:
        def __init__(self, execution_inputs, **kwargs):
            captured.update(kwargs)
            self.inputs = execution_inputs

        def run(self) -> ExecutionResult:
            self.inputs.output_dir.mkdir(parents=True, exist_ok=True)
            stdout = self.inputs.output_dir / "stdout.txt"
            stdout.write_text(
                "\n".join(
                    json.dumps(
                        {
                            "type": "RECORD",
                            "record": {
                                "stream": "users",
                                "data": {"id": i},
                                "emitted_at": i,
                            },
                        }
                    )
                    for i in range(3)
                )
            )
            return ExecutionResult(
                connector_under_test=self.inputs.connector_under_test,
                command=self.inputs.command,
                stdout_file_path=stdout,
                stderr_file_path=self.inputs.output_dir / "stderr.txt",
                success=True,
                exit_code=0,
                stopped_early=StoppedEarly(reason="cap", records_seen=3, elapsed_s=1.5),
            )

    monkeypatch.setattr(cloud, "ConnectorRunner", _FakeRunner)

    result, _ = cloud._run_connector_command(
        connector_image="airbyte/source-test:1.0.0",
        command=Command.SPEC,
        output_dir=tmp_path / "out",
        target_or_control=TargetOrControl.TARGET,
        timeout_seconds=600,
        max_records=3,
    )

    assert captured == {
        "timeout_seconds": 600,
        "proxy_url": None,
        "ca_cert_path": None,
        "max_records": 3,
        "mask_policy": None,
    }
    assert result["stopped_early"] == {
        "reason": "cap",
        "records_seen": 3,
        "elapsed_s": 1.5,
    }
    assert result["message_counts"] == {"RECORD": 3}
    assert result["record_counts_per_stream"] == {"users": 3}
    assert result["output_mode"] == "raw"

    captured.clear()
    _, _ = cloud._run_connector_command(
        connector_image="airbyte/source-test:1.0.0",
        command=Command.SPEC,
        output_dir=tmp_path / "out2",
        target_or_control=TargetOrControl.TARGET,
    )

    assert captured["timeout_seconds"] == DEFAULT_TIMEOUT_SECONDS
    assert captured["max_records"] is None
    assert captured["mask_policy"] is None
    assert result["output_mode"] == "raw"


# ---------------------------------------------------------------------------
# Incomplete verdict: a stopped side never passes
# ---------------------------------------------------------------------------

_STOPPED_TIMEOUT = {"reason": "timeout", "records_seen": 12, "elapsed_s": 10200.0}


def test_a_stopped_read_is_incomplete_not_a_pass(
    tmp_path, capsys, monkeypatch, stub_comparison_run
):
    gh_outputs: dict[str, object] = {}
    monkeypatch.setattr(cloud, "write_github_outputs", gh_outputs.update)
    seen = stub_comparison_run(
        {**_STOPPABLE_SIDE, "stopped_early": _STOPPED_TIMEOUT},
        {**_STOPPABLE_SIDE, "stopped_early": _STOPPED_TIMEOUT},
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
        skip_record_comparison=True,
    )
    payload = _logged_payload(capsys.readouterr().out)

    assert payload["success"] is False
    assert payload["incomplete"] is True
    assert payload["regression_detected"] is False
    assert payload["both_succeeded"] is True
    assert payload["both_failed"] is False
    assert gh_outputs["success"] is False
    assert gh_outputs["incomplete"] is True
    assert gh_outputs["regression_detected"] is False

    summary = "\n".join(seen["step_summary"])
    assert (
        "❌ INCOMPLETE — stopped early (timeout) after 12 records per side" in summary
    )
    assert "- Target: stopped early (timeout) after 12 records in 10,200 s" in summary


def test_a_complete_read_carries_incomplete_false(
    tmp_path, capsys, stub_comparison_run
):
    stub_comparison_run(dict(_STOPPABLE_SIDE), dict(_STOPPABLE_SIDE))

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
        skip_record_comparison=True,
    )
    payload = _logged_payload(capsys.readouterr().out)

    assert payload["success"] is True
    assert payload["incomplete"] is False


def test_a_stopped_reads_final_state_is_diagnostic(
    tmp_path, capsys, stub_comparison_run
):
    """Under a stop neither side emitted a final state, only a checkpoint."""
    seen = stub_comparison_run(
        {**_CLEAN_RUN, "stopped_early": _STOPPED_TIMEOUT},
        {**_CLEAN_RUN, "stopped_early": _STOPPED_TIMEOUT},
        target_outputs=_state_outputs({"users": {"updated_at": "2024-01-01"}}),
        control_outputs=_state_outputs({}),
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
    )
    payload = _logged_payload(capsys.readouterr().out)

    assert payload["success"] is False
    assert payload["incomplete"] is True
    assert payload["regression_detected"] is False
    assert payload["comparison"]["final_state"]["passed"] is False

    summary = "\n".join(seen["step_summary"])
    assert "| Final state per stream | ⚠️ |" in summary
    assert "checkpoints each side had reached" in summary


def test_a_strict_regression_on_a_stopped_run_is_still_detected(
    tmp_path, capsys, stub_comparison_run
):
    """A regression the partial output does show is named beside the stop."""
    seen = stub_comparison_run(
        {**_CLEAN_RUN, "stopped_early": _STOPPED_TIMEOUT},
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
    assert payload["incomplete"] is True
    assert payload["regression_detected"] is True

    summary = "\n".join(seen["step_summary"])
    assert "❌ INCOMPLETE — target stopped early (timeout) after 12 records" in summary
    assert "REGRESSION DETECTED" in summary


def test_a_single_version_stopped_read_is_incomplete(
    tmp_path, capsys, fake_clock, stub_run
):
    gh_outputs = stub_run({**_STOPPABLE_SIDE, "stopped_early": _STOPPED_TIMEOUT})

    cloud.regression_test(
        skip_compare=True,
        test_image="airbyte/source-test:2.0.0",
        command="read",
        output_dir=str(tmp_path),
    )
    payload = _logged_payload(capsys.readouterr().out)

    assert payload["success"] is False
    assert payload["incomplete"] is True
    assert payload["exited_cleanly"] is True
    assert gh_outputs["success"] is False
    assert gh_outputs["incomplete"] is True
    summary = "\n".join(stub_run.step_summary)
    assert "❌ INCOMPLETE — stopped early (timeout) after 12 records" in summary
    # The runner default less the ten-minute reserve, as a comparison's side.
    assert (
        "- Run: stopped early (timeout) after 12 records in 10,200 s, at the end "
        "of its 230-minute share of the 240-minute read budget\n"
    ) in summary


def _connector_stdout(tmp_path, *analytics: tuple[str, str]) -> Path:
    """A run's stdout holding a record plus the given analytics counters."""
    stdout = tmp_path / "stdout.jsonl"
    lines = [
        json.dumps(
            {
                "type": "RECORD",
                "record": {
                    "stream": "users",
                    "data": {"id": 1},
                    "emitted_at": 1_700_000_000_000,
                },
            }
        )
    ] + [
        json.dumps(
            {
                "type": "TRACE",
                "trace": {
                    "type": "ANALYTICS",
                    "emitted_at": 1_700_000_000_000,
                    "analytics": {"type": type_, "value": value},
                },
            }
        )
        for type_, value in analytics
    ]
    stdout.write_text("\n".join(lines))
    return stdout


def _connector_config(tmp_path) -> Path:
    """A config file, so `ExecutionInputs` accepts the command."""
    config = tmp_path / "config.json"
    config.write_text(json.dumps({"api_key": "x"}))
    return config


def _stub_connector_runner(monkeypatch, stdout_path: Path) -> None:
    """Make `_run_connector_command` read its messages from `stdout_path`."""

    def _fake_runner(execution_inputs, **_kwargs):
        result = ExecutionResult(
            connector_under_test=execution_inputs.connector_under_test,
            command=execution_inputs.command,
            stdout_file_path=stdout_path,
            stderr_file_path=stdout_path.parent / "stderr.log",
            success=True,
            exit_code=0,
        )
        return SimpleNamespace(run=lambda: result)

    monkeypatch.setattr(cloud, "ConnectorRunner", _fake_runner)
    monkeypatch.setattr(ExecutionResult, "save_artifacts", lambda _self, _dir: None)


def test_connector_cache_metrics_are_reported_without_the_proxy(tmp_path, monkeypatch):
    """The connector's own cache needs no `--enable-http-metrics` to be measured.

    A `requests_cache` hit never reaches the wire, so the proxy could not see it
    even when it is running. Setting these in `_run_with_optional_http_metrics`
    instead would gate the one metric that needs no proxy on turning one on.
    """
    _stub_connector_runner(
        monkeypatch,
        _connector_stdout(
            tmp_path, ("http-request-count", "40"), ("http-cache-hit-count", "10")
        ),
    )

    result, _outputs = cloud._run_connector_command(
        connector_image="airbyte/source-test:2.0.0",
        command=Command.CHECK,
        output_dir=tmp_path,
        target_or_control=cloud.TargetOrControl.TARGET,
        config_path=_connector_config(tmp_path),
    )

    assert result["http_metrics"] == {
        "connector_request_count": 40,
        "connector_cache_hits_count": 10,
        "connector_cache_hit_ratio": "25.00%",
    }


def test_a_silent_connector_adds_no_http_metrics_key(tmp_path, monkeypatch):
    """Absent, not zero: the key's absence is what renders as *not reported*."""
    _stub_connector_runner(monkeypatch, _connector_stdout(tmp_path))

    result, _outputs = cloud._run_connector_command(
        connector_image="airbyte/source-test:2.0.0",
        command=Command.CHECK,
        output_dir=tmp_path,
        target_or_control=cloud.TargetOrControl.TARGET,
        config_path=_connector_config(tmp_path),
    )

    assert "http_metrics" not in result


def test_proxy_metrics_do_not_overwrite_the_connector_metrics(tmp_path, monkeypatch):
    """Both halves of the payload have to survive a run that used the proxy.

    `_run_with_optional_http_metrics` assigns `http_metrics` wholesale, so
    without a merge it would drop the connector's numbers on exactly the runs a
    reviewer is most likely to read.
    """
    _stub_connector_runner(
        monkeypatch,
        _connector_stdout(
            tmp_path, ("http-request-count", "40"), ("http-cache-hit-count", "10")
        ),
    )
    session = MitmproxySession(
        proxy_host="host.docker.internal",
        proxy_port=8080,
        dump_file_path=tmp_path / "http_traffic.mitm",
        ca_cert_path=None,
    )
    monkeypatch.setattr(
        cloud.MitmproxyManager, "running", lambda _self: contextlib.nullcontext(session)
    )
    monkeypatch.setattr(
        cloud,
        "parse_http_dump",
        lambda *_args, **_kwargs: HttpMetrics(
            flow_count=30,
            duplicate_flow_count=2,
            unique_urls=[],
            replayed_flow_count=30,
            live_flow_count=0,
        ),
    )

    result, _outputs = cloud._run_with_optional_http_metrics(
        connector_image="airbyte/source-test:2.0.0",
        command=Command.CHECK,
        output_dir=tmp_path,
        target_or_control=cloud.TargetOrControl.TARGET,
        enable_http_metrics=True,
        config_path=_connector_config(tmp_path),
        catalog_path=None,
        state_path=None,
    )

    metrics = result["http_metrics"]
    # The proxy's view...
    assert metrics["flow_count"] == 30
    assert metrics["replay_hit_ratio"] == "100.00%"
    # ...and the connector's, which the proxy can never see.
    assert metrics["connector_request_count"] == 40
    assert metrics["connector_cache_hit_ratio"] == "25.00%"
    # The heuristic that used to sit here is gone.
    assert "cache_hits_count" not in metrics
    assert "cache_hit_ratio" not in metrics


def test_the_connector_metrics_survive_a_run_with_no_mitmproxy(tmp_path, monkeypatch):
    """The skip-reason payload must add to the connector's numbers, not replace them."""
    _stub_connector_runner(
        monkeypatch,
        _connector_stdout(
            tmp_path, ("http-request-count", "40"), ("http-cache-hit-count", "10")
        ),
    )
    monkeypatch.setattr(
        cloud.MitmproxyManager, "running", lambda _self: contextlib.nullcontext(None)
    )

    result, _outputs = cloud._run_with_optional_http_metrics(
        connector_image="airbyte/source-test:2.0.0",
        command=Command.CHECK,
        output_dir=tmp_path,
        target_or_control=cloud.TargetOrControl.TARGET,
        enable_http_metrics=True,
        config_path=_connector_config(tmp_path),
        catalog_path=None,
        state_path=None,
        replay_expected=True,
    )

    metrics = result["http_metrics"]
    assert "mitmproxy is unavailable" in metrics["replay_skipped_reason"]
    assert metrics["connector_request_count"] == 40


# ---------------------------------------------------------------------------
# Not-exercised reads: a target-only stream with no records is never a pass
# ---------------------------------------------------------------------------

_NOT_EXERCISED_LINE = (
    "NOT EXERCISED — 1 stream(s) the control did not read returned no records: "
    "audit_logs"
)


def _configured_catalog(path, *names: str):
    path.write_text(
        json.dumps(
            {
                "streams": [
                    {
                        "stream": {
                            "name": name,
                            "json_schema": {},
                            "supported_sync_modes": ["full_refresh"],
                        },
                        "sync_mode": "full_refresh",
                        "destination_sync_mode": "append",
                    }
                    for name in names
                ]
            }
        )
    )
    return path


def _record_catalog(path, *, incremental=False):
    path.write_text(
        json.dumps(
            {
                "streams": [
                    {
                        "stream": {
                            "name": "audit_logs",
                            "json_schema": {
                                "properties": {
                                    "id": {"type": "integer"},
                                    "updated_at": {"type": "integer"},
                                }
                            },
                            "source_defined_primary_key": [["id"]],
                            "default_cursor_field": ["updated_at"],
                            "source_defined_cursor": True,
                            "supported_sync_modes": ["full_refresh", "incremental"],
                        },
                        "sync_mode": "incremental" if incremental else "full_refresh",
                        "destination_sync_mode": "append",
                        "primary_key": [["id"]],
                        "cursor_field": ["updated_at"] if incremental else [],
                    }
                ]
            }
        )
    )
    return path


def _record_stdout(path, *records):
    path.write_text(
        "\n".join(
            json.dumps(
                {
                    "type": "RECORD",
                    "record": {
                        "stream": "audit_logs",
                        "data": record,
                        "emitted_at": 0,
                    },
                }
            )
            for record in records
        )
    )
    return path


def _target_only(monkeypatch, *streams: str) -> None:
    """Fill the seam the stream-injection work will feed: today one catalog
    serves both sides, so the CLI's own computation of this set is empty."""
    monkeypatch.setattr(cloud, "_target_only_stream_names", lambda *_args: streams)


def test_the_target_only_streams_are_the_targets_minus_the_controls(tmp_path):
    target = _configured_catalog(
        tmp_path / "target_catalog.json", "audit_logs", "users"
    )
    control = _configured_catalog(tmp_path / "control_catalog.json", "users")

    assert cloud._target_only_stream_names(Command.READ, target, target) == ()
    assert cloud._target_only_stream_names(Command.READ, target, control) == (
        "audit_logs",
    )
    assert cloud._target_only_stream_names(
        Command.READ_WITH_STATE, target, control
    ) == ("audit_logs",)
    assert cloud._target_only_stream_names(Command.DISCOVER, target, control) == ()


def test_one_catalog_on_both_sides_carries_not_exercised_false(
    tmp_path, capsys, monkeypatch, stub_comparison_run
):
    gh_outputs: dict[str, object] = {}
    monkeypatch.setattr(cloud, "write_github_outputs", gh_outputs.update)
    catalog = _configured_catalog(tmp_path / "catalog.json", "audit_logs", "users")
    seen = stub_comparison_run(dict(_STOPPABLE_SIDE), dict(_STOPPABLE_SIDE))

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        catalog_path=str(catalog),
        output_dir=str(tmp_path / "read"),
        skip_record_comparison=True,
    )
    payload = _logged_payload(capsys.readouterr().out)

    assert [str(call["catalog_path"]) for call in seen["calls"]] == [
        str(catalog),
        str(catalog),
    ]
    assert payload["success"] is True
    assert payload["not_exercised"] is False
    assert payload["setup_error"] is False
    assert payload["could_not_test"] is False
    assert gh_outputs["not_exercised"] is False
    assert gh_outputs["setup_error"] is False
    assert gh_outputs["could_not_test"] is False
    assert "NOT EXERCISED" not in "\n".join(seen["step_summary"])


def test_a_target_only_stream_with_no_records_is_not_exercised_not_a_pass(
    tmp_path, capsys, monkeypatch, stub_comparison_run
):
    gh_outputs: dict[str, object] = {}
    monkeypatch.setattr(cloud, "write_github_outputs", gh_outputs.update)
    _target_only(monkeypatch, "audit_logs")
    seen = stub_comparison_run(dict(_STOPPABLE_SIDE), dict(_STOPPABLE_SIDE))

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
        skip_record_comparison=True,
    )
    payload = _logged_payload(capsys.readouterr().out)

    assert payload["success"] is False
    assert payload["not_exercised"] is True
    assert payload["incomplete"] is False
    assert payload["regression_detected"] is False
    assert payload["both_succeeded"] is True
    assert payload["both_failed"] is False
    assert gh_outputs["success"] is False
    assert gh_outputs["not_exercised"] is True
    assert gh_outputs["incomplete"] is False
    assert gh_outputs["regression_detected"] is False
    assert seen["json_output"]["not_exercised"] is True
    assert f"❌ {_NOT_EXERCISED_LINE}" in "\n".join(seen["step_summary"])


def test_a_target_only_stream_with_records_passes_as_before(
    tmp_path, capsys, monkeypatch, stub_comparison_run
):
    _target_only(monkeypatch, "audit_logs")
    seen = stub_comparison_run(
        {**_STOPPABLE_SIDE, "record_counts_per_stream": {"users": 12, "audit_logs": 1}},
        dict(_STOPPABLE_SIDE),
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
        skip_record_comparison=True,
    )
    payload = _logged_payload(capsys.readouterr().out)

    assert payload["success"] is True
    assert payload["not_exercised"] is False
    assert "Both versions succeeded" in "\n".join(seen["step_summary"])


def test_target_only_records_get_schema_and_primary_key_checks(
    tmp_path, capsys, monkeypatch, stub_comparison_run
):
    _target_only(monkeypatch, "audit_logs")
    catalog = _record_catalog(tmp_path / "catalog.json")
    target_stdout = _record_stdout(
        tmp_path / "target.jsonl",
        {"id": 1, "updated_at": 1},
        {"id": 2, "updated_at": 2},
    )
    control_stdout = _record_stdout(tmp_path / "control.jsonl")
    seen = stub_comparison_run(
        {
            **_STOPPABLE_SIDE,
            "stdout_file": str(target_stdout),
            "record_counts_per_stream": {"audit_logs": 2},
        },
        {**_STOPPABLE_SIDE, "stdout_file": str(control_stdout)},
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        catalog_path=str(catalog),
        output_dir=str(tmp_path / "run"),
    )
    payload = _logged_payload(capsys.readouterr().out)

    assert payload["record_checks"]["audit_logs"]["records"] == 2
    assert payload["record_checks"]["audit_logs"]["schema_mismatched_records"] == 0
    assert payload["record_checks"]["audit_logs"]["pk_null"] == 0
    assert payload["record_checks"]["audit_logs"]["pk_duplicates"] == 0
    assert "Record schema (new streams)" in "\n".join(seen["step_summary"])
    assert "Primary key (new streams)" in "\n".join(seen["step_summary"])


def test_target_only_duplicate_pk_from_comparison_names_control_absence(
    tmp_path, capsys, monkeypatch, stub_comparison_run
):
    _target_only(monkeypatch, "audit_logs")
    catalog = _record_catalog(tmp_path / "catalog.json")
    target_stdout = _record_stdout(tmp_path / "target.jsonl", {"id": 1}, {"id": 1})
    control_stdout = _record_stdout(tmp_path / "control.jsonl")
    seen = stub_comparison_run(
        {
            **_STOPPABLE_SIDE,
            "stdout_file": str(target_stdout),
            "record_counts_per_stream": {"audit_logs": 2},
        },
        {**_STOPPABLE_SIDE, "stdout_file": str(control_stdout)},
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        catalog_path=str(catalog),
        output_dir=str(tmp_path / "run"),
    )
    payload = _logged_payload(capsys.readouterr().out)
    summary = "\n".join(seen["step_summary"])

    assert payload["record_checks"]["audit_logs"]["pk_duplicates"] == 1
    assert "Primary key (new streams)" in summary
    assert "stream not read by control" in summary
    assert "not duplicated in control" not in summary


def test_target_only_schema_mismatch_fails_the_run(
    tmp_path, capsys, monkeypatch, stub_comparison_run
):
    _target_only(monkeypatch, "audit_logs")
    catalog = _record_catalog(tmp_path / "catalog.json")
    target_stdout = _record_stdout(tmp_path / "target.jsonl", {"id": "secret"})
    control_stdout = _record_stdout(tmp_path / "control.jsonl")
    report_models = []
    monkeypatch.setattr(
        cloud,
        "write_html_report",
        lambda model, output_dir: (
            report_models.append(model) or output_dir / "report.html"
        ),
    )
    monkeypatch.setattr(
        cloud, "generate_regression_report", generate_action_test_comparison_report
    )
    seen = stub_comparison_run(
        {
            **_STOPPABLE_SIDE,
            "stdout_file": str(target_stdout),
            "record_counts_per_stream": {"audit_logs": 1},
        },
        {**_STOPPABLE_SIDE, "stdout_file": str(control_stdout)},
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        catalog_path=str(catalog),
        output_dir=str(tmp_path / "run"),
    )
    payload = _logged_payload(capsys.readouterr().out)

    assert payload["success"] is False
    assert payload["regression_detected"] is True
    assert payload["record_checks"]["audit_logs"]["schema_mismatched_records"] == 1
    assert "**Result:** ❌ FAIL (regression)" in "\n".join(seen["step_summary"])
    markdown = (tmp_path / "run" / "report.md").read_text()
    assert (
        "- ❌ Record schema (new streams): audit_logs.id: 1 record(s), observed "
        "string, declared integer" in markdown
    )
    assert "no regression" not in markdown.lower()
    schema_check = next(
        check
        for check in report_models[0].checks
        if check.name == "Record schema (new streams)"
    )
    assert schema_check.status == "fail"


def test_target_only_undeclared_fields_are_diagnostic(
    tmp_path, capsys, monkeypatch, stub_comparison_run
):
    _target_only(monkeypatch, "audit_logs")
    catalog = _record_catalog(tmp_path / "catalog.json")
    target_stdout = _record_stdout(
        tmp_path / "target.jsonl", {"id": 1, "updated_at": 1, "extra": "value"}
    )
    control_stdout = _record_stdout(tmp_path / "control.jsonl")
    report_models = []
    monkeypatch.setattr(
        cloud,
        "write_html_report",
        lambda model, output_dir: (
            report_models.append(model) or output_dir / "report.html"
        ),
    )
    monkeypatch.setattr(
        cloud, "generate_regression_report", generate_action_test_comparison_report
    )
    seen = stub_comparison_run(
        {
            **_STOPPABLE_SIDE,
            "stdout_file": str(target_stdout),
            "record_counts_per_stream": {"audit_logs": 1},
        },
        {**_STOPPABLE_SIDE, "stdout_file": str(control_stdout)},
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        catalog_path=str(catalog),
        output_dir=str(tmp_path / "run"),
    )
    payload = _logged_payload(capsys.readouterr().out)

    schema_check = next(
        check
        for check in report_models[0].checks
        if check.name == "Record schema (new streams)"
    )
    assert schema_check.status == "warn"
    assert payload["success"] is True
    assert payload["regression_detected"] is False
    assert "⚠️" in "\n".join(seen["step_summary"])
    assert (
        "- ⚠️ Record schema (new streams): audit_logs: 1 record(s) have undeclared "
        "field(s)" in (tmp_path / "run" / "report.md").read_text()
    )


def test_target_only_record_check_error_is_inconclusive(
    tmp_path, capsys, monkeypatch, stub_comparison_run
):
    _target_only(monkeypatch, "audit_logs")
    catalog = _record_catalog(tmp_path / "catalog.json")
    target_stdout = _record_stdout(tmp_path / "target.jsonl", {"id": 1})
    control_stdout = _record_stdout(tmp_path / "control.jsonl")
    monkeypatch.setattr(
        cloud, "generate_regression_report", generate_action_test_comparison_report
    )
    seen = stub_comparison_run(
        {
            **_STOPPABLE_SIDE,
            "stdout_file": str(target_stdout),
            "record_counts_per_stream": {"audit_logs": 1},
        },
        {**_STOPPABLE_SIDE, "stdout_file": str(control_stdout)},
    )

    def crash_schema_check(*_args, **_kwargs):
        raise RuntimeError("private exception detail")

    monkeypatch.setattr(cloud, "check_record_schema", crash_schema_check)

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        catalog_path=str(catalog),
        output_dir=str(tmp_path / "run"),
    )
    payload = _logged_payload(capsys.readouterr().out)
    summary = "\n".join(seen["step_summary"])

    assert payload["success"] is False
    assert payload["regression_detected"] is False
    assert "**Result:** ❌ FAIL (inconclusive)" in summary
    assert "errored (RuntimeError)" in summary
    assert "private exception detail" not in summary
    markdown = (tmp_path / "run" / "report.md").read_text()
    assert "**Result:** FAIL (inconclusive)" in markdown
    assert "REGRESSION DETECTED" not in markdown
    assert "no regression" not in markdown.lower()
    assert "- ❌ Record schema (new streams): audit_logs: errored (RuntimeError)" in (
        markdown
    )


def test_target_only_record_check_error_does_not_hide_another_stream_regression(
    tmp_path, capsys, monkeypatch, stub_comparison_run
):
    catalog = _record_catalog(tmp_path / "catalog.json")
    catalog_data = json.loads(catalog.read_text())
    second_stream = json.loads(json.dumps(catalog_data["streams"][0]))
    second_stream["stream"]["name"] = "audit_events"
    catalog_data["streams"].append(second_stream)
    catalog.write_text(json.dumps(catalog_data))
    _target_only(monkeypatch, "audit_logs", "audit_events")
    records = [
        ("audit_logs", {"id": 1, "updated_at": 1}),
        ("audit_events", {"id": "wrong", "updated_at": 2}),
    ]
    target_stdout = tmp_path / "target.jsonl"
    target_stdout.write_text(
        "\n".join(
            json.dumps(
                {
                    "type": "RECORD",
                    "record": {
                        "stream": name,
                        "data": data,
                        "emitted_at": 0,
                    },
                }
            )
            for name, data in records
        )
    )
    control_stdout = _record_stdout(tmp_path / "control.jsonl")
    seen = stub_comparison_run(
        {
            **_STOPPABLE_SIDE,
            "stdout_file": str(target_stdout),
            "record_counts_per_stream": {"audit_logs": 1, "audit_events": 1},
        },
        {**_STOPPABLE_SIDE, "stdout_file": str(control_stdout)},
    )
    original_check = cloud.check_record_schema
    checks_seen = 0

    def crash_first_schema_check(*args, **kwargs):
        nonlocal checks_seen
        checks_seen += 1
        if checks_seen == 1:
            raise RuntimeError("private exception detail")
        return original_check(*args, **kwargs)

    monkeypatch.setattr(cloud, "check_record_schema", crash_first_schema_check)

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        catalog_path=str(catalog),
        output_dir=str(tmp_path / "run"),
    )
    payload = _logged_payload(capsys.readouterr().out)
    summary = "\n".join(seen["step_summary"])

    assert payload["success"] is False
    assert payload["regression_detected"] is True
    assert "audit_logs: errored (RuntimeError)" in summary
    assert "audit_events.id: 1 record(s), observed string, declared integer" in summary


def test_target_only_wide_schema_mismatch_remains_a_strict_failure(
    tmp_path, capsys, monkeypatch, stub_comparison_run
):
    _target_only(monkeypatch, "audit_logs")
    catalog = _record_catalog(tmp_path / "catalog.json")
    catalog_data = json.loads(catalog.read_text())
    properties = catalog_data["streams"][0]["stream"]["json_schema"]["properties"]
    fields = [f"field_{index:03}" for index in range(_MAX_OBSERVED_FIELDS + 1)]
    properties.update({field: {"type": "integer"} for field in fields})
    catalog.write_text(json.dumps(catalog_data))
    target_stdout = _record_stdout(
        tmp_path / "target.jsonl",
        {
            "id": 1,
            "updated_at": 1,
            **dict.fromkeys(fields, "wrong"),
        },
    )
    control_stdout = _record_stdout(tmp_path / "control.jsonl")
    report_models = []
    monkeypatch.setattr(
        cloud,
        "write_html_report",
        lambda model, output_dir: (
            report_models.append(model) or output_dir / "report.html"
        ),
    )
    seen = stub_comparison_run(
        {
            **_STOPPABLE_SIDE,
            "stdout_file": str(target_stdout),
            "record_counts_per_stream": {"audit_logs": 1},
        },
        {**_STOPPABLE_SIDE, "stdout_file": str(control_stdout)},
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        catalog_path=str(catalog),
        output_dir=str(tmp_path / "run"),
    )
    payload = _logged_payload(capsys.readouterr().out)
    summary = "\n".join(seen["step_summary"])

    assert payload["success"] is False
    assert payload["regression_detected"] is True
    assert payload["record_checks"]["audit_logs"]["schema_mismatched_records"] == 1
    assert "errored" not in summary
    assert (
        f"audit_logs.{fields[-1]}: 1 record(s), observed unknown, declared integer"
        in next(
            check.summary
            for check in report_models[0].checks
            if check.name == "Record schema (new streams)"
        )
    )


@pytest.mark.parametrize("output_mode", ["raw", "masked"])
def test_target_only_readable_incremental_cursor_compares_state_to_max_record(
    tmp_path, capsys, monkeypatch, stub_comparison_run, output_mode
):
    _target_only(monkeypatch, "audit_logs")
    catalog = _record_catalog(tmp_path / "catalog.json", incremental=True)
    raw_records = [{"id": 1, "updated_at": 102}]
    if output_mode == "masked":
        policy = MaskPolicy.from_configured_catalog(
            json.loads(catalog.read_text()), key=KEY
        )
        assert policy.cursor_readable("audit_logs")
        records = [
            mask_record_data(
                record,
                policy.readable("audit_logs"),
                policy.primary_key("audit_logs"),
                key=KEY,
            )
            for record in raw_records
        ]
    else:
        records = raw_records
    target_stdout = _record_stdout(tmp_path / "target.jsonl", *records)
    control_stdout = _record_stdout(tmp_path / "control.jsonl")
    report_models = []
    monkeypatch.setattr(
        cloud,
        "write_html_report",
        lambda model, output_dir: (
            report_models.append(model) or output_dir / "report.html"
        ),
    )
    seen = stub_comparison_run(
        {
            **_STOPPABLE_SIDE,
            "stdout_file": str(target_stdout),
            "record_counts_per_stream": {"audit_logs": 1},
            "output_mode": output_mode,
        },
        {
            **_STOPPABLE_SIDE,
            "stdout_file": str(control_stdout),
            "output_mode": output_mode,
        },
        target_outputs=ComparableOutputs(
            final_states={(None, "audit_logs"): {"updated_at": 50}}
        ),
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        catalog_path=str(catalog),
        output_dir=str(tmp_path / "run"),
        output_mode=output_mode,
    )
    payload = _logged_payload(capsys.readouterr().out)

    assert payload["record_checks"]["audit_logs"]["state_below_max"] is True
    assert "Incremental cursor (new streams)" in "\n".join(seen["step_summary"])
    assert payload["success"] is True
    assert payload["regression_detected"] is False
    cursor_check = next(
        check
        for check in report_models[0].checks
        if check.name == "Incremental cursor (new streams)"
    )
    assert cursor_check.status == "warn"


def test_record_failure_takes_precedence_over_not_exercised(
    tmp_path, capsys, monkeypatch, stub_comparison_run
):
    _target_only(monkeypatch, "audit_logs", "unexercised")
    catalog = _record_catalog(tmp_path / "catalog.json")
    target_stdout = _record_stdout(tmp_path / "target.jsonl", {"id": "wrong"})
    control_stdout = _record_stdout(tmp_path / "control.jsonl")
    seen = stub_comparison_run(
        {
            **_STOPPABLE_SIDE,
            "stdout_file": str(target_stdout),
            "record_counts_per_stream": {"audit_logs": 1, "unexercised": 0},
        },
        {**_STOPPABLE_SIDE, "stdout_file": str(control_stdout)},
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        catalog_path=str(catalog),
        output_dir=str(tmp_path / "run"),
    )
    payload = _logged_payload(capsys.readouterr().out)

    assert payload["not_exercised"] is True
    assert payload["regression_detected"] is True
    assert "**Result:** ❌ FAIL (regression)" in "\n".join(seen["step_summary"])


def test_record_failure_with_setup_error_keeps_setup_error_label(
    tmp_path, capsys, monkeypatch, stub_comparison_run
):
    _target_only(monkeypatch, "audit_logs", "undefined_stream")
    catalog = _record_catalog(tmp_path / "catalog.json")
    target_stdout = _record_stdout(tmp_path / "target.jsonl", {"id": "wrong"})
    seen = stub_comparison_run(
        {
            **_STOPPABLE_SIDE,
            "stdout_file": str(target_stdout),
            "record_counts_per_stream": {"audit_logs": 1, "undefined_stream": 0},
        },
        {**_STOPPABLE_SIDE, "success": False, "exit_code": 1},
        target_outputs=ComparableOutputs(
            stream_statuses={"undefined_stream": ["INCOMPLETE"]}
        ),
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        catalog_path=str(catalog),
        output_dir=str(tmp_path / "run"),
    )
    payload = _logged_payload(capsys.readouterr().out)
    summary = "\n".join(seen["step_summary"])

    assert payload["setup_error"] is True
    assert payload["regression_detected"] is True
    assert "**Result:** ❌ SETUP ERROR" in summary
    assert "Record schema (new streams)" in summary


def test_incomplete_takes_precedence_over_record_check_failure(
    tmp_path, capsys, monkeypatch, stub_comparison_run
):
    _target_only(monkeypatch, "audit_logs")
    catalog = _record_catalog(tmp_path / "catalog.json")
    target_stdout = _record_stdout(tmp_path / "target.jsonl", {"id": "wrong"})
    control_stdout = _record_stdout(tmp_path / "control.jsonl")
    seen = stub_comparison_run(
        {
            **_STOPPABLE_SIDE,
            "stopped_early": _STOPPED_TIMEOUT,
            "stdout_file": str(target_stdout),
            "record_counts_per_stream": {"audit_logs": 1},
        },
        {**_STOPPABLE_SIDE, "stdout_file": str(control_stdout)},
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        catalog_path=str(catalog),
        output_dir=str(tmp_path / "run"),
    )
    payload = _logged_payload(capsys.readouterr().out)
    summary = "\n".join(seen["step_summary"])

    assert payload["incomplete"] is True
    assert payload["regression_detected"] is True
    assert "**Result:** ❌ INCOMPLETE" in summary


def test_control_failure_does_not_skip_target_only_record_checks(
    tmp_path, capsys, monkeypatch, stub_comparison_run
):
    _target_only(monkeypatch, "audit_logs")
    catalog = _record_catalog(tmp_path / "catalog.json")
    target_stdout = _record_stdout(
        tmp_path / "target.jsonl", {"id": 1}, {"id": 1}, {"id": None}
    )
    seen = stub_comparison_run(
        {
            **_STOPPABLE_SIDE,
            "stdout_file": str(target_stdout),
            "record_counts_per_stream": {"audit_logs": 3},
        },
        {**_STOPPABLE_SIDE, "success": False, "exit_code": 1},
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        catalog_path=str(catalog),
        output_dir=str(tmp_path / "run"),
    )
    payload = _logged_payload(capsys.readouterr().out)

    assert payload["record_checks"]["audit_logs"]["pk_null"] == 1
    assert payload["record_checks"]["audit_logs"]["pk_duplicates"] == 1
    assert "Primary key (new streams)" in "\n".join(seen["step_summary"])


def test_target_only_incremental_stream_requires_final_state(
    tmp_path, capsys, monkeypatch, stub_comparison_run
):
    _target_only(monkeypatch, "audit_logs")
    catalog = _record_catalog(tmp_path / "catalog.json", incremental=True)
    target_stdout = _record_stdout(
        tmp_path / "target.jsonl", {"id": 1, "updated_at": 4}
    )
    control_stdout = _record_stdout(tmp_path / "control.jsonl")
    report_models = []
    monkeypatch.setattr(
        cloud,
        "write_html_report",
        lambda model, output_dir: (
            report_models.append(model) or output_dir / "report.html"
        ),
    )
    seen = stub_comparison_run(
        {
            **_STOPPABLE_SIDE,
            "stdout_file": str(target_stdout),
            "record_counts_per_stream": {"audit_logs": 1},
        },
        {**_STOPPABLE_SIDE, "stdout_file": str(control_stdout)},
        target_outputs=ComparableOutputs(final_states={}),
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        catalog_path=str(catalog),
        output_dir=str(tmp_path / "run"),
    )
    payload = _logged_payload(capsys.readouterr().out)

    assert payload["record_checks"]["audit_logs"]["state_has_cursor_value"] is False
    assert "**Result:** ❌ FAIL (regression)" in "\n".join(seen["step_summary"])
    cursor_check = next(
        check
        for check in report_models[0].checks
        if check.name == "Incremental cursor (new streams)"
    )
    assert cursor_check.status == "fail"


def test_target_only_catalog_pk_and_cursor_paths_are_strict_failures(
    tmp_path, capsys, monkeypatch, stub_comparison_run
):
    _target_only(monkeypatch, "audit_logs")
    catalog = _record_catalog(tmp_path / "catalog.json", incremental=True)
    catalog_data = json.loads(catalog.read_text())
    catalog_data["streams"][0]["stream"]["json_schema"]["properties"] = {}
    catalog.write_text(json.dumps(catalog_data))
    target_stdout = _record_stdout(
        tmp_path / "target.jsonl", {"id": 1, "updated_at": 4}
    )
    control_stdout = _record_stdout(tmp_path / "control.jsonl")
    seen = stub_comparison_run(
        {
            **_STOPPABLE_SIDE,
            "stdout_file": str(target_stdout),
            "record_counts_per_stream": {"audit_logs": 1},
        },
        {**_STOPPABLE_SIDE, "stdout_file": str(control_stdout)},
        target_outputs=ComparableOutputs(
            final_states={(None, "audit_logs"): {"updated_at": 4}}
        ),
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        catalog_path=str(catalog),
        output_dir=str(tmp_path / "run"),
    )
    payload = _logged_payload(capsys.readouterr().out)
    summary = "\n".join(seen["step_summary"])

    assert payload["success"] is False
    assert payload["regression_detected"] is True
    assert "audit_logs: primary key id missing from schema" in summary
    assert "audit_logs: cursor updated_at missing from schema" in summary
    assert "Primary key (new streams)" in summary
    assert "Incremental cursor (new streams)" in summary


def test_stopped_target_record_check_detail_is_partial(
    tmp_path, capsys, monkeypatch, stub_comparison_run
):
    _target_only(monkeypatch, "audit_logs")
    catalog = _record_catalog(tmp_path / "catalog.json")
    target_stdout = _record_stdout(tmp_path / "target.jsonl", {"id": 1})
    control_stdout = _record_stdout(tmp_path / "control.jsonl")
    seen = stub_comparison_run(
        {
            **_STOPPABLE_SIDE,
            "stopped_early": _STOPPED_TIMEOUT,
            "stdout_file": str(target_stdout),
            "record_counts_per_stream": {"audit_logs": 1},
        },
        {**_STOPPABLE_SIDE, "stdout_file": str(control_stdout)},
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        catalog_path=str(catalog),
        output_dir=str(tmp_path / "run"),
    )
    payload = _logged_payload(capsys.readouterr().out)

    assert payload["incomplete"] is True
    assert payload["record_checks"]["audit_logs"]["partial"] is True
    assert "exercised (partial), record checks passed" in "\n".join(
        seen["step_summary"]
    )


@pytest.mark.parametrize("output_mode", ["raw", "masked"])
def test_target_only_record_checks_never_leak_record_values(
    tmp_path, capsys, monkeypatch, stub_comparison_run, output_mode
):
    _target_only(monkeypatch, "audit_logs")
    catalog = _record_catalog(tmp_path / "catalog.json")
    catalog_data = json.loads(catalog.read_text())
    catalog_data["streams"][0]["stream"]["json_schema"]["properties"].update(
        {
            "name": {"type": "integer"},
            "metadata": {"type": "string"},
        }
    )
    catalog.write_text(json.dumps(catalog_data))

    sentinel = "SENTINEL_7c1e_secret"
    secret_number = 987654321123
    raw_records = [
        {
            "id": secret_number,
            "updated_at": secret_number,
            "name": sentinel,
            "metadata": {"nested": sentinel},
        },
        {
            "id": secret_number,
            "updated_at": secret_number,
            "name": sentinel,
            "metadata": {"nested": sentinel},
        },
        {
            "id": None,
            "updated_at": secret_number,
            "name": sentinel,
            "metadata": {"nested": sentinel},
        },
    ]
    records = (
        [mask_record_data(record, key=KEY) for record in raw_records]
        if output_mode == "masked"
        else raw_records
    )
    target_stdout = _record_stdout(tmp_path / "target.jsonl", *records)
    target_side = {
        **_STOPPABLE_SIDE,
        "stdout_file": str(target_stdout),
        "record_counts_per_stream": {"audit_logs": len(records)},
        "output_mode": output_mode,
    }
    control_side = {
        **_STOPPABLE_SIDE,
        "success": False,
        "exit_code": 1,
        "output_mode": output_mode,
    }
    seen = stub_comparison_run(target_side, control_side)
    monkeypatch.setattr(
        cloud, "generate_regression_report", generate_action_test_comparison_report
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        catalog_path=str(catalog),
        output_dir=str(tmp_path / "run"),
        output_mode=output_mode,
    )
    capsys.readouterr()

    summaries = "\n".join(seen["step_summary"])
    json_payload = json.dumps(seen["json_output"])
    markdown = (tmp_path / "run" / "report.md").read_text()
    html = (tmp_path / "run" / "report.html").read_text()

    for surface in (summaries, json_payload, markdown, html):
        assert sentinel not in surface
        assert str(secret_number) not in surface
    if output_mode == "masked":
        record_check_json = json.dumps(seen["json_output"]["record_checks"])
        assert "_len-" not in summaries
        assert "_len-" not in record_check_json


def test_config_error_read_is_could_not_test_without_reporting_a_regression(
    tmp_path, capsys, monkeypatch, stub_comparison_run
):
    gh_outputs: dict[str, object] = {}
    monkeypatch.setattr(cloud, "write_github_outputs", gh_outputs.update)
    _target_only(monkeypatch, "audit_logs")
    error_message = "HTTP 400 (code 4711): missing permission to read"
    aggregate = StreamError(
        "config_error",
        "During the sync, the following streams did not sync successfully: audit_logs",
    )
    seen = stub_comparison_run(
        {
            **_STOPPABLE_SIDE,
            "success": False,
            "exit_code": 1,
            "record_counts_per_stream": {"audit_logs": 0},
        },
        {**_STOPPABLE_SIDE, "success": True, "exit_code": 0},
        target_outputs=ComparableOutputs(
            stream_errors={
                "audit_logs": [StreamError("config_error", error_message)],
                None: [aggregate],
            }
        ),
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
        skip_record_comparison=True,
    )
    payload = _logged_payload(capsys.readouterr().out)

    assert payload["success"] is False
    assert payload["could_not_test"] is True
    assert payload["not_exercised"] is False
    assert payload["regression_detected"] is False
    assert gh_outputs["could_not_test"] is True
    assert gh_outputs["regression_detected"] is False
    summary = "\n".join(seen["step_summary"])
    assert "COULD NOT TEST (config error)" in summary
    assert error_message in summary


def test_a_lone_incomplete_target_only_stream_is_a_setup_error(
    tmp_path, capsys, monkeypatch, stub_comparison_run
):
    gh_outputs: dict[str, object] = {}
    monkeypatch.setattr(cloud, "write_github_outputs", gh_outputs.update)
    _target_only(monkeypatch, "audit_logs")
    seen = stub_comparison_run(
        {**_STOPPABLE_SIDE, "record_counts_per_stream": {"audit_logs": 0}},
        dict(_STOPPABLE_SIDE),
        target_outputs=ComparableOutputs(
            stream_statuses={"audit_logs": ["INCOMPLETE"]}
        ),
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
        skip_record_comparison=True,
    )
    payload = _logged_payload(capsys.readouterr().out)

    assert payload["setup_error"] is True
    assert payload["not_exercised"] is False
    assert gh_outputs["setup_error"] is True
    assert "SETUP ERROR" in "\n".join(seen["step_summary"])


def test_setup_error_does_not_hide_a_shared_stream_failure(
    tmp_path, capsys, monkeypatch, stub_comparison_run
):
    gh_outputs: dict[str, object] = {}
    monkeypatch.setattr(cloud, "write_github_outputs", gh_outputs.update)
    _target_only(monkeypatch, "audit_logs")
    seen = stub_comparison_run(
        {
            **_STOPPABLE_SIDE,
            "success": False,
            "exit_code": 1,
            "record_counts_per_stream": {"audit_logs": 0},
        },
        {**_STOPPABLE_SIDE, "success": True, "exit_code": 0},
        target_outputs=ComparableOutputs(
            stream_statuses={"audit_logs": ["INCOMPLETE"]},
            stream_errors={"shared": [StreamError("system_error", "system failure")]},
        ),
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
        skip_record_comparison=True,
    )
    payload = _logged_payload(capsys.readouterr().out)
    summary = "\n".join(seen["step_summary"])

    assert payload["setup_error"] is True
    assert payload["regression_detected"] is True
    assert gh_outputs["regression_detected"] is True
    assert "**Result:** ❌ SETUP ERROR" in summary
    result_line = next(line for line in summary.splitlines() if "**Result:**" in line)
    assert result_line.count("Target failed (exit 1), control succeeded") == 1
    assert "REGRESSION DETECTED" in summary


def test_a_stopped_read_with_an_unexercised_stream_is_incomplete_with_both_flags(
    tmp_path, capsys, monkeypatch, stub_comparison_run
):
    gh_outputs: dict[str, object] = {}
    monkeypatch.setattr(cloud, "write_github_outputs", gh_outputs.update)
    _target_only(monkeypatch, "audit_logs")
    seen = stub_comparison_run(
        {**_STOPPABLE_SIDE, "stopped_early": _STOPPED_TIMEOUT},
        {**_STOPPABLE_SIDE, "stopped_early": _STOPPED_TIMEOUT},
    )

    cloud.regression_test(
        test_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        output_dir=str(tmp_path),
        skip_record_comparison=True,
    )
    payload = _logged_payload(capsys.readouterr().out)

    assert payload["success"] is False
    assert payload["incomplete"] is True
    assert payload["not_exercised"] is True
    assert gh_outputs["incomplete"] is True
    assert gh_outputs["not_exercised"] is True
    summary = "\n".join(seen["step_summary"])
    assert (
        "❌ INCOMPLETE — stopped early (timeout) after 12 records per side" in summary
    )
    assert "NOT EXERCISED" not in summary
    assert (
        "- Not exercised: 1 stream(s) the control did not read returned no records: "
        "audit_logs" in summary
    )


def test_a_single_version_read_carries_not_exercised_false(tmp_path, capsys, stub_run):
    gh_outputs = stub_run(dict(_STOPPABLE_SIDE))

    cloud.regression_test(
        skip_compare=True,
        test_image="airbyte/source-test:2.0.0",
        command="read",
        output_dir=str(tmp_path),
    )
    payload = _logged_payload(capsys.readouterr().out)

    assert payload["success"] is True
    assert payload["not_exercised"] is False
    assert gh_outputs["not_exercised"] is False
    assert payload["setup_error"] is False
    assert payload["could_not_test"] is False
    assert gh_outputs["setup_error"] is False
    assert gh_outputs["could_not_test"] is False


_JVM_GAP = (
    "airbyte/source-jvm:2.0.0 has no certifi bundle to trust the capture proxy "
    "with (a JVM image would need a JKS truststore)"
)


def _run_untrusting_side(tmp_path, monkeypatch, **kwargs):
    """Run one side whose image cannot trust the proxy; return it and its kwargs."""
    monkeypatch.setattr(cloud, "proxy_trust_gap", lambda _image: _JVM_GAP)

    def _must_not_start(*_args, **_kwargs):
        raise AssertionError("the proxy was started for an image that cannot trust it")

    monkeypatch.setattr(cloud, "MitmproxyManager", _must_not_start)
    seen: dict[str, object] = {}

    def _fake_run(**run_kwargs):
        seen.update(run_kwargs)
        return (
            {
                "success": True,
                "exit_code": 0,
                "http_metrics": {"connector_request_count": 4},
            },
            ComparableOutputs(),
        )

    monkeypatch.setattr(cloud, "_run_connector_command", _fake_run)
    result, _outputs = cloud._run_with_optional_http_metrics(
        connector_image="airbyte/source-jvm:2.0.0",
        command=Command.CHECK,
        output_dir=tmp_path,
        target_or_control=cloud.TargetOrControl.TARGET,
        enable_http_metrics=True,
        config_path=None,
        catalog_path=None,
        state_path=None,
        **kwargs,
    )
    return result, seen


def test_an_image_that_cannot_trust_the_proxy_runs_direct(tmp_path, monkeypatch):
    """A JVM side under `--no-http-replay` calls the API as it did before capture.

    Through the proxy each of its HTTPS calls would fail verification, so the
    run would read as a connector bug instead of as uncaptured.
    """
    result, seen = _run_untrusting_side(tmp_path, monkeypatch)

    assert "proxy_url" not in seen
    assert "ca_cert_path" not in seen
    assert result["success"] is True
    assert "http_dump_file" not in result
    assert result["http_metrics"] == {
        "connector_request_count": 4,
        "capture_skipped_reason": _JVM_GAP,
    }


def test_a_replaying_side_that_cannot_trust_the_proxy_says_replay_was_skipped(
    tmp_path, monkeypatch
):
    result, _seen = _run_untrusting_side(tmp_path, monkeypatch, replay_expected=True)

    assert result["http_metrics"]["replay_skipped_reason"] == (
        f"{_JVM_GAP}, so nothing could be replayed"
    )


def test_a_jvm_comparison_without_replay_runs_both_sides(tmp_path, capsys, monkeypatch):
    """The thread's case end to end: a JVM `check` with `--no-http-replay`."""
    monkeypatch.setattr(cloud, "ensure_image_available", lambda _image: True)
    monkeypatch.setattr(cloud, "track_regression_test", lambda **_kwargs: None)
    monkeypatch.setattr(cloud, "write_github_outputs", lambda _outputs: None)
    monkeypatch.setattr(cloud, "write_github_summary", lambda _text: None)
    monkeypatch.setattr(cloud, "write_json_output", lambda _key, _data: None)
    monkeypatch.setattr(cloud, "proxy_trust_gap", lambda image: f"{image} gap")

    def _must_not_start(*_args, **_kwargs):
        raise AssertionError("the proxy was started for an image that cannot trust it")

    monkeypatch.setattr(cloud, "MitmproxyManager", _must_not_start)

    def _fake_run(*, output_dir, **kwargs):
        assert "proxy_url" not in kwargs
        output_dir.mkdir(parents=True, exist_ok=True)
        return (
            {"success": True, "exit_code": 0, "connection_status": "SUCCEEDED"},
            ComparableOutputs(),
        )

    monkeypatch.setattr(cloud, "_run_connector_command", _fake_run)

    cloud.regression_test(
        test_image="airbyte/source-jvm:2.0.0",
        control_image="airbyte/source-jvm:1.0.0",
        command="check",
        output_dir=str(tmp_path),
        enable_http_replay=False,
    )

    payload = _logged_payload(capsys.readouterr().out)
    assert payload["success"] is True
    for side, image in (("control", "1.0.0"), ("target", "2.0.0")):
        assert payload[side]["http_metrics"] == {
            "capture_skipped_reason": f"airbyte/source-jvm:{image} gap"
        }
