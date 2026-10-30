# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Masking end to end: the real runner, the artifacts and the record comparison."""

from __future__ import annotations

import json
import re
import secrets
import sys
from contextlib import suppress
from html import unescape
from pathlib import Path
from typing import Any

import pytest

from airbyte_ops_mcp.cli import cloud
from airbyte_ops_mcp.regression_tests.connection_fetcher import (
    CatalogSchemaEnrichment,
    ConnectionData,
    save_connection_data_to_files,
)
from airbyte_ops_mcp.regression_tests.connector_runner import ConnectorRunner
from airbyte_ops_mcp.regression_tests.masking import (
    MASKED_TEXT_PREFIX,
    MaskPolicy,
    mask_value,
)
from airbyte_ops_mcp.regression_tests.models import (
    Command,
    TargetOrControl,
    split_records_per_stream,
)
from airbyte_ops_mcp.regression_tests.regression import (
    comparators,
    run_record_comparisons_from_files,
)
from tests.test_masking import KEY, OTHER_KEY

pytestmark = pytest.mark.unit

# Replays one file to stdout, standing in for `docker run`; given a second
# file and an exit code, replays it to stderr and exits with that code.
FAKE_CONNECTOR = """
import sys
with open(sys.argv[1], "rb") as source:
    sys.stdout.buffer.write(source.read())
if len(sys.argv) > 2:
    with open(sys.argv[2], "rb") as source:
        sys.stderr.buffer.write(source.read())
    sys.exit(int(sys.argv[3]))
"""

CATALOG = {
    "streams": [
        {
            "stream": {
                "name": "users",
                "json_schema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "updated_at": {"type": "string", "format": "date-time"},
                        "email": {"type": "string"},
                    },
                },
                "supported_sync_modes": ["incremental"],
                "source_defined_primary_key": [["id"]],
                "default_cursor_field": ["updated_at"],
            },
            "sync_mode": "incremental",
            "destination_sync_mode": "append",
        },
        {
            "stream": {
                "name": "tokens",
                "json_schema": {
                    "type": "object",
                    "properties": {"token": {"type": "string"}},
                },
                "supported_sync_modes": ["incremental"],
                "default_cursor_field": ["token"],
            },
            "sync_mode": "incremental",
            "destination_sync_mode": "append",
        },
    ]
}

# The connection's stored state: one stream whose cursor stays readable and
# one whose cursor is a string, so its state must be masked.
READABLE_CURSOR = "2026-01-01T00:00:00Z"
MASKED_CURSOR = "tok-live-7f3a"
INPUT_STATE = [
    {
        "type": "STREAM",
        "stream": {
            "stream_descriptor": {"name": "users"},
            "stream_state": {"updated_at": READABLE_CURSOR},
        },
    },
    {
        "type": "STREAM",
        "stream": {
            "stream_descriptor": {"name": "tokens"},
            "stream_state": {"token": MASKED_CURSOR},
        },
    },
]


def _record(user_id: int, email: str, updated_at: str = "2026-01-01") -> str:
    return json.dumps(
        {
            "type": "RECORD",
            "record": {
                "stream": "users",
                "data": {"id": user_id, "updated_at": updated_at, "email": email},
                "emitted_at": 1,
            },
        }
    )


def _log(level: str, message: str) -> str:
    return json.dumps({"type": "LOG", "log": {"level": level, "message": message}})


def _stdout(*emails: str) -> str:
    lines = [_log("INFO", "Syncing users"), _log("DEBUG", f"GET /users -> {emails}")]
    lines.extend(_record(index + 1, email) for index, email in enumerate(emails))
    return "\n".join(lines) + "\n"


@pytest.fixture
def connector_outputs(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Make each `ConnectorRunner` replay the file named for its role."""
    script = tmp_path / "fake_connector.py"
    script.write_text(FAKE_CONNECTOR)
    outputs: dict[str, Path] = {}
    crash: list[str] = []

    def _fake_build(self: ConnectorRunner, _temp_dir: Path) -> list[str]:
        self._container_name = "connector-test-fake"
        role = self.connector_under_test.target_or_control.value
        return [sys.executable, str(script), str(outputs[role]), *crash]

    monkeypatch.setattr(ConnectorRunner, "_build_docker_command", _fake_build)

    def _install(control: str, target: str, stderr: bytes | None = None) -> None:
        for role, text in (("control", control), ("target", target)):
            path = tmp_path / f"{role}_stdout.jsonl"
            path.write_text(text)
            outputs[role] = path
        if stderr is not None:
            path = tmp_path / "fake_stderr.txt"
            path.write_bytes(stderr)
            crash[:] = [str(path), "1"]

    return _install


@pytest.fixture
def inputs(tmp_path: Path) -> tuple[Path, Path]:
    config = tmp_path / "config.json"
    config.write_text(json.dumps({"api_key": "secret"}))
    catalog = tmp_path / "catalog.json"
    catalog.write_text(json.dumps(CATALOG))
    return config, catalog


def _run(
    tmp_path: Path,
    inputs: tuple[Path, Path],
    role: TargetOrControl,
    mode: str,
    key: bytes = KEY,
) -> dict:
    """One side of a run, masked under `key` as both sides of a real run are."""
    config, catalog = inputs
    result, _outputs = cloud._run_connector_command(
        connector_image=f"airbyte/source-test:{role.value}",
        command=Command.READ,
        output_dir=tmp_path / role.value,
        target_or_control=role,
        config_path=config,
        catalog_path=catalog,
        output_mode=mode,  # type: ignore[arg-type]
        mask_key=key,
    )
    return result


@pytest.fixture
def key_file(tmp_path: Path) -> Path:
    """The run's key as the workflow hands it over: 64 hex characters in a
    file outside the output directory."""
    path = tmp_path / "mask_key"
    path.write_text(KEY.hex() + "\n")
    return path


def _all_output_text(output_dir: Path) -> str:
    return "\n".join(
        path.read_text(errors="replace")
        for path in output_dir.rglob("*")
        if path.is_file()
    )


def test_a_masked_comparison_leaves_no_raw_value_in_any_artifact(
    tmp_path: Path, connector_outputs, inputs
) -> None:
    connector_outputs(
        control=_stdout("alice@example.com", "bob@example.com"),
        target=_stdout("alice@example.com", "bob@example.com"),
    )

    control = _run(tmp_path, inputs, TargetOrControl.CONTROL, "masked")
    target = _run(tmp_path, inputs, TargetOrControl.TARGET, "masked")
    split_records_per_stream(Path(control["stdout_file"]))
    split_records_per_stream(Path(target["stdout_file"]))

    for role in ("control", "target"):
        output_dir = tmp_path / role
        assert (output_dir / "stdout.txt").is_file()
        assert (output_dir / "airbyte_messages/record.jsonl").is_file()
        assert (output_dir / "records_per_stream/users.jsonl").is_file()
        text = _all_output_text(output_dir)
        assert "alice" not in text
        assert "bob" not in text
        assert "example.com" not in text
        assert MASKED_TEXT_PREFIX in text  # the DEBUG line
        assert "Syncing users" in text  # the INFO line
    assert control["output_mode"] == "masked"
    assert control["record_counts_per_stream"] == {"users": 2}
    assert control["readable_fields"] == {
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
    }

    users = (tmp_path / "target/records_per_stream/users.jsonl").read_text()
    records = [json.loads(line)["record"]["data"] for line in users.splitlines()]
    assert [record["id"] for record in records] == [
        mask_value(1, key=KEY),
        mask_value(2, key=KEY),
    ]
    assert [record["updated_at"] for record in records] == ["2026-01-01"] * 2
    assert records[0]["email"] == mask_value("alice@example.com", key=KEY)


def test_the_comparison_matches_masked_records_by_pk_and_passes_on_equal_values(
    tmp_path: Path, connector_outputs, inputs
) -> None:
    connector_outputs(
        control=_stdout("alice@example.com", "bob@example.com"),
        target=_stdout("alice@example.com", "bob@example.com"),
    )
    control = _run(tmp_path, inputs, TargetOrControl.CONTROL, "masked")
    target = _run(tmp_path, inputs, TargetOrControl.TARGET, "masked")

    summary, skip_reason = cloud._compare_read_records(
        target_result=target, control_result=control, catalog_file=inputs[1]
    )

    assert skip_reason is None
    assert summary is not None
    assert summary.passed is True
    assert summary.errored is False


def test_the_comparison_still_sees_a_changed_value_through_the_mask(
    tmp_path: Path, connector_outputs, inputs
) -> None:
    """Deterministic hashing: a value that differs masks differently, so the
    field diff survives, and the PK token that names the record matches on
    both sides."""
    connector_outputs(
        control=_stdout("alice@example.com", "bob@example.com"),
        target=_stdout("alice@example.com", "bob@EXAMPLE.com"),
    )
    control = _run(tmp_path, inputs, TargetOrControl.CONTROL, "masked")
    target = _run(tmp_path, inputs, TargetOrControl.TARGET, "masked")

    summary, _skip_reason = cloud._compare_read_records(
        target_result=target, control_result=control, catalog_file=inputs[1]
    )

    assert summary is not None
    assert summary.passed is False
    payload = json.dumps(summary.to_dict())
    assert "bob@" not in payload
    assert "example.com" not in payload
    field_values = summary.to_dict()["checks"]["field_values"]["streams"]["users"]
    assert field_values["records_with_value_diff"] == 1
    assert list(field_values["value_diff_examples"][0]["pk"]) == [
        mask_value(2, key=KEY)
    ]
    assert summary.field_comparison is not None
    diff = summary.field_comparison.stream_results["users"].record_diff
    assert diff is not None
    kept = diff.records_with_value_diff[0]
    assert kept["control"]["data"]["email"] == mask_value("bob@example.com", key=KEY)
    assert kept["target"]["data"]["email"] == mask_value("bob@EXAMPLE.com", key=KEY)


def test_tokens_from_two_keys_never_pair_so_a_run_matches_no_other_runs_artifacts(
    tmp_path: Path, connector_outputs, inputs
) -> None:
    """Each run hashes under its own key. The two sides of one run share it
    and pair by primary key; a side hashed under another run's key pairs with
    nothing, by design, so no token can be followed from one run to another."""
    text = _stdout("alice@example.com", "bob@example.com")
    connector_outputs(control=text, target=text)
    control = _run(tmp_path, inputs, TargetOrControl.CONTROL, "masked", key=KEY)
    target = _run(tmp_path, inputs, TargetOrControl.TARGET, "masked", key=OTHER_KEY)

    summary, _skip_reason = cloud._compare_read_records(
        target_result=target, control_result=control, catalog_file=inputs[1]
    )

    def ids(result: dict) -> list[str]:
        lines = Path(result["stdout_file"]).read_text().splitlines()
        records = [json.loads(line) for line in lines if '"RECORD"' in line]
        return [record["record"]["data"]["id"] for record in records]

    assert ids(control) == [mask_value(1, key=KEY), mask_value(2, key=KEY)]
    assert ids(target) == [mask_value(1, key=OTHER_KEY), mask_value(2, key=OTHER_KEY)]
    assert not set(ids(control)) & set(ids(target))
    assert summary is not None
    assert summary.passed is False
    field_values = summary.to_dict()["checks"]["field_values"]["streams"]["users"]
    assert field_values["records_only_in_control"] == 2
    assert field_values["records_only_in_target"] == 2


def _user_line(data: dict) -> str:
    return json.dumps(
        {"type": "RECORD", "record": {"stream": "users", "data": data, "emitted_at": 1}}
    )


def test_the_file_based_comparison_reads_masked_records_as_the_full_diff_does(
    tmp_path: Path,
    connector_outputs,
    inputs,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Masked values are tokens, so equal tokens skip by fingerprint and a
    changed one is diffed in full. `1` against `1.0` and a reordered list are
    one value to the comparison, and one token: neither path counts them."""
    day = "2026-01-01"
    control_rows = [
        {"id": 1, "updated_at": day, "email": "a@example.com"},
        {"id": 2, "updated_at": day, "email": "b@example.com"},
        {"id": 3, "updated_at": day, "email": "c@example.com", "score": 1},
        {"id": 4, "updated_at": day, "email": "d@example.com", "tags": [1, 2]},
        {"id": 5, "updated_at": day, "email": "e1@example.com"},
        {"id": 5, "updated_at": day, "email": "e2@example.com"},
        {"id": 6, "updated_at": day, "email": "f@example.com"},
    ]
    target_rows = [
        {"id": 1, "updated_at": day, "email": "a@example.com"},
        {"id": 2, "updated_at": day, "email": "B@example.com"},
        {"id": 3, "updated_at": day, "email": "c@example.com", "score": 1.0},
        {"id": 4, "updated_at": day, "email": "d@example.com", "tags": [2, 1]},
        {"id": 5, "updated_at": day, "email": "e2@example.com"},
        {"id": 5, "updated_at": day, "email": "e1@example.com"},
        {"id": 6, "updated_at": "2026-01-02", "email": "f@example.com"},
    ]
    connector_outputs(
        control="\n".join(_user_line(row) for row in control_rows) + "\n",
        target="\n".join(_user_line(row) for row in target_rows) + "\n",
    )
    control = _run(tmp_path, inputs, TargetOrControl.CONTROL, "masked")
    target = _run(tmp_path, inputs, TargetOrControl.TARGET, "masked")
    control_files = split_records_per_stream(Path(control["stdout_file"]))
    target_files = split_records_per_stream(Path(target["stdout_file"]))
    pks = {"users": [["id"]]}

    from_disk = run_record_comparisons_from_files(control_files, target_files, pks)
    read_lazily = comparators._read_records_file
    monkeypatch.setattr(
        comparators, "_read_records_file", lambda path: list(read_lazily(path))
    )
    held = run_record_comparisons_from_files(control_files, target_files, pks)

    assert from_disk == held
    assert json.dumps(from_disk.to_dict()) == json.dumps(held.to_dict())
    assert from_disk.field_comparison is not None
    diff = from_disk.field_comparison.stream_results["users"].record_diff
    assert diff is not None
    assert {example["pk"] for example in diff.records_with_value_diff} == {
        (mask_value(pk, key=KEY),) for pk in (2, 6)
    }
    assert "example.com" not in json.dumps(from_disk.to_dict())


def test_a_raw_run_writes_what_the_connector_emitted(
    tmp_path: Path, connector_outputs, inputs
) -> None:
    text = _stdout("alice@example.com")
    connector_outputs(control=text, target=text)

    target = _run(tmp_path, inputs, TargetOrControl.TARGET, "raw")

    assert target["output_mode"] == "raw"
    assert "readable_fields" not in target
    assert Path(target["stdout_file"]).read_text() == text


# ---------------------------------------------------------------------------
# The input state file
# ---------------------------------------------------------------------------


def _connection_data(state: list | None = None) -> ConnectionData:
    return ConnectionData(
        connection_id="c-1",
        source_id="s-1",
        source_name="test",
        source_definition_id="d-1",
        config={"api_key": "sk-live-secret"},
        catalog=CATALOG,
        stream_names=["users", "tokens"],
        docker_repository="airbyte/source-test",
        docker_image_tag="2.0.0",
        state=state,
    )


def test_a_masked_state_file_keeps_its_raw_copy_beside_the_config(tmp_path: Path):
    private = tmp_path / "private"
    artifact = tmp_path / "artifact"

    _config, _catalog, state_path = save_connection_data_to_files(
        _connection_data(INPUT_STATE),
        artifact,
        config_dir=private,
        mask_policy=MaskPolicy.from_configured_catalog(CATALOG, key=KEY),
    )

    assert state_path == private / "state.json"
    assert json.loads(state_path.read_text()) == INPUT_STATE
    assert state_path.stat().st_mode & 0o777 == 0o600
    masked = json.loads((artifact / "state.json").read_text())
    assert masked[0] == INPUT_STATE[0]
    assert masked[1]["stream"]["stream_state"] == {
        "token": mask_value(MASKED_CURSOR, key=KEY)
    }
    assert MASKED_CURSOR not in (artifact / "state.json").read_text()


def test_a_raw_run_writes_the_state_file_into_the_artifact_as_before(tmp_path: Path):
    _config, _catalog, state_path = save_connection_data_to_files(
        _connection_data(INPUT_STATE), tmp_path / "artifact", config_dir=tmp_path / "p"
    )

    assert state_path == tmp_path / "artifact" / "state.json"
    assert json.loads(state_path.read_text()) == INPUT_STATE


def test_a_masked_state_file_refuses_to_go_without_a_private_directory(tmp_path: Path):
    with pytest.raises(ValueError, match="private directory"):
        save_connection_data_to_files(
            _connection_data(INPUT_STATE), tmp_path, mask_policy=MaskPolicy(key=KEY)
        )


@pytest.fixture
def connection(monkeypatch: pytest.MonkeyPatch):
    """A `--connection-id` run that fetches `INPUT_STATE` with its schemas."""
    monkeypatch.setattr(cloud, "ensure_image_available", lambda _image: True)
    monkeypatch.setattr(cloud, "track_regression_test", lambda **_kwargs: None)
    monkeypatch.setattr(cloud, "write_github_summary", lambda _text: None)
    monkeypatch.setattr(cloud, "write_github_outputs", lambda _outputs: None)
    monkeypatch.setattr(cloud, "should_use_secret_retriever", lambda: False)
    monkeypatch.setattr(cloud, "get_connection_residency", lambda _connection_id: "us")
    monkeypatch.setattr(cloud, "is_running_on_eu_runner", lambda: False)
    monkeypatch.setattr(
        cloud, "fetch_connection_data", lambda _connection_id: _connection_data()
    )
    monkeypatch.setattr(
        cloud,
        "enrich_catalog_schemas_from_cloud",
        lambda data: CatalogSchemaEnrichment(data, 0, list(INPUT_STATE)),
    )
    captured: dict[str, object] = {}
    real_run = cloud._run_connector_command

    def _capturing_run(**kwargs):
        captured.update(kwargs)
        return real_run(**kwargs)

    monkeypatch.setattr(cloud, "_run_connector_command", _capturing_run)
    return captured


def test_a_masked_connection_run_keeps_the_raw_state_out_of_the_artifacts(
    tmp_path: Path, capsys, connector_outputs, connection, key_file: Path
) -> None:
    text = _stdout("alice@example.com")
    connector_outputs(control=text, target=text)
    output_dir = tmp_path / "out"

    cloud.regression_test(
        skip_compare=True,
        connection_id="c-1",
        command="read",
        output_dir=str(output_dir),
        output_mode="masked",
        mask_key_path=str(key_file),
    )
    capsys.readouterr()

    # The connector read the raw state, from the private directory.
    state_path = connection["state_path"]
    assert isinstance(state_path, Path)
    assert json.loads(state_path.read_text()) == INPUT_STATE
    assert output_dir.resolve() not in state_path.resolve().parents
    assert state_path.parent == connection["config_path"].parent
    assert state_path.stat().st_mode & 0o777 == 0o600

    # The artifact holds the masked copy, and nothing under it holds the
    # masked stream's cursor -- not the state file, not the report.
    masked = json.loads((output_dir / "connection_data/state.json").read_text())
    assert masked[0]["stream"]["stream_state"] == {"updated_at": READABLE_CURSOR}
    assert masked[1]["stream"]["stream_state"] == {
        "token": mask_value(MASKED_CURSOR, key=KEY)
    }
    everything = _all_output_text(output_dir)
    assert MASKED_CURSOR not in everything
    html = (output_dir / "report.html").read_text()
    assert mask_value(MASKED_CURSOR, key=KEY) in html
    assert "State (input)" in html
    assert "<h3>Readable fields</h3>" in html
    assert "cursor readable on 1 of 2 streams" in html
    assert "cursor readable on 1 of 2 streams" in (output_dir / "report.md").read_text()


def test_a_raw_connection_run_leaves_the_state_file_where_it_was(
    tmp_path: Path, capsys, connector_outputs, connection
) -> None:
    text = _stdout("alice@example.com")
    connector_outputs(control=text, target=text)
    output_dir = tmp_path / "out"

    cloud.regression_test(
        skip_compare=True,
        connection_id="c-1",
        command="read",
        output_dir=str(output_dir),
        output_mode="raw",
    )
    capsys.readouterr()

    assert connection["state_path"] == output_dir / "connection_data/state.json"
    assert json.loads(connection["state_path"].read_text()) == INPUT_STATE


def test_without_a_key_file_each_invocation_makes_its_own_key(
    tmp_path: Path, capsys, connector_outputs, connection
) -> None:
    """A run by hand gets a fresh key for its process: the records and the
    artifact's copy of the state are hashed under the one key, and a second
    invocation of the same read gives different tokens for the same values."""
    text = _stdout("alice@example.com")
    connector_outputs(control=text, target=text)
    seen: list[tuple[bytes, str, str]] = []

    for name in ("first", "second"):
        output_dir = tmp_path / name
        cloud.regression_test(
            skip_compare=True,
            connection_id="c-1",
            command="read",
            output_dir=str(output_dir),
            output_mode="masked",
        )
        [stdout_file] = output_dir.rglob("stdout.txt")
        lines = [json.loads(line) for line in stdout_file.read_text().splitlines()]
        [record] = [
            line["record"]["data"] for line in lines if line["type"] == "RECORD"
        ]
        state = json.loads((output_dir / "connection_data/state.json").read_text())
        key = connection["mask_key"]
        assert isinstance(key, bytes)
        seen.append((key, record["email"], state[1]["stream"]["stream_state"]["token"]))
    capsys.readouterr()

    (first_key, first_email, first_state), (second_key, second_email, second_state) = (
        seen
    )
    assert len(first_key) == len(second_key) == 32
    assert first_key != second_key
    assert first_email == mask_value("alice@example.com", key=first_key)
    assert first_state == mask_value(MASKED_CURSOR, key=first_key, normalize=False)
    assert second_email == mask_value("alice@example.com", key=second_key)
    assert first_email != second_email
    assert first_state != second_state


def test_a_seeded_state_shows_only_its_outline_on_a_masked_report(
    tmp_path: Path, capsys, connector_outputs, inputs, connection, key_file: Path
) -> None:
    """The seeded file itself lives wherever the caller put it, outside the
    output directory; the report embeds only the streams it names, so neither
    a value nor a token of one reaches the page."""
    text = _stdout("alice@example.com")
    connector_outputs(control=text, target=text)
    seed = tmp_path / "seed_state.json"
    seed.write_text(json.dumps(INPUT_STATE))
    output_dir = tmp_path / "out"

    cloud.regression_test(
        skip_compare=True,
        connection_id="c-1",
        command="read",
        state_path=str(seed),
        output_dir=str(output_dir),
        output_mode="masked",
        mask_key_path=str(key_file),
    )
    capsys.readouterr()

    assert connection["state_path"] == seed
    assert not (output_dir / "connection_data/state.json").exists()
    html = (output_dir / "report.html").read_text()
    block = html.split("<summary>State (seeded)</summary>", 1)[1].split("</pre>", 1)[0]
    assert json.loads(unescape(re.sub(r"<[^>]+>", "\n", block))) == [
        {
            "namespace": None,
            "name": "users",
            "sync_mode": "incremental",
            "cursor_field": ["updated_at"],
        },
        {
            "namespace": None,
            "name": "tokens",
            "sync_mode": "incremental",
            "cursor_field": ["token"],
        },
    ]
    assert MASKED_CURSOR not in _all_output_text(output_dir)
    for value in (READABLE_CURSOR, MASKED_CURSOR):
        assert value not in html
        assert mask_value(value, key=KEY, normalize=False) not in html


# ---------------------------------------------------------------------------
# The connector's stderr
# ---------------------------------------------------------------------------

CRASH = b"Traceback (most recent call last):\nKeyError: 'alice@example.com'\n"


def test_a_masked_crash_shows_only_line_lengths_in_stderr_and_on_the_report(
    tmp_path: Path,
    capsys,
    caplog: pytest.LogCaptureFixture,
    connector_outputs,
    connection,
) -> None:
    connector_outputs(control="", target="", stderr=CRASH)
    output_dir = tmp_path / "out"

    cloud.regression_test(
        skip_compare=True,
        connection_id="c-1",
        command="read",
        output_dir=str(output_dir),
        output_mode="masked",
    )
    console = capsys.readouterr()

    [stderr_file] = output_dir.rglob("stderr.txt")
    assert stderr_file.read_bytes() == b"masked_len-34\nmasked_len-29\n"
    html = (output_dir / "report.html").read_text()
    assert "stderr — last 2 line(s)" in html
    assert "masked_len-29" in html
    for text in (
        _all_output_text(output_dir),
        console.out,
        console.err,
        caplog.text,
    ):
        assert "alice" not in text
        assert "KeyError" not in text


def test_a_raw_crash_keeps_its_stderr_as_emitted(
    tmp_path: Path, capsys, connector_outputs, connection
) -> None:
    connector_outputs(control="", target="", stderr=CRASH)
    output_dir = tmp_path / "out"

    cloud.regression_test(
        skip_compare=True,
        connection_id="c-1",
        command="read",
        output_dir=str(output_dir),
        output_mode="raw",
    )
    capsys.readouterr()

    [stderr_file] = output_dir.rglob("stderr.txt")
    assert stderr_file.read_bytes() == CRASH
    html = (output_dir / "report.html").read_text()
    assert "stderr — last 2 line(s)" in html
    assert "alice@example.com" in html
    assert "masked_len-" not in html


# What the Python CDK's uncaught-exception hook writes to stdout: the exception
# and the whole traceback in a FATAL message, with nothing on stderr.
FATAL_LINE = _log(
    "FATAL",
    "Traceback (most recent call last):\n"
    '  File "main.py", line 3, in <module>\n'
    "KeyError: 'alice@example.com'",
)


def test_a_masked_crash_in_a_fatal_log_leaves_no_crash_text_anywhere(
    tmp_path: Path,
    capsys,
    caplog: pytest.LogCaptureFixture,
    connector_outputs,
    connection,
) -> None:
    """A Python connector's crash goes out as a FATAL LOG message on stdout,
    and with stderr empty the report's tail is the stdout tail."""
    stdout = _log("INFO", "Syncing users") + "\n" + FATAL_LINE + "\n"
    connector_outputs(control=stdout, target=stdout, stderr=b"")
    output_dir = tmp_path / "out"

    cloud.regression_test(
        skip_compare=True,
        connection_id="c-1",
        command="read",
        output_dir=str(output_dir),
        output_mode="masked",
    )
    console = capsys.readouterr()

    [stdout_file] = output_dir.rglob("stdout.txt")
    info, fatal = stdout_file.read_text().splitlines()
    assert json.loads(info)["log"]["message"] == "Syncing users"
    assert json.loads(fatal)["log"]["message"].startswith(MASKED_TEXT_PREFIX)
    html = (output_dir / "report.html").read_text()
    assert "stdout — last 2 line(s)" in html
    for text in (
        _all_output_text(output_dir),
        console.out,
        console.err,
        caplog.text,
    ):
        assert "alice" not in text
        assert "KeyError" not in text


# A stream keyed by a field of a nested object, as a child stream keyed by its
# parent's id is.
NESTED_PK_CATALOG = {
    "streams": [
        {
            "stream": {
                "name": "readings",
                "json_schema": {
                    "type": "object",
                    "properties": {
                        "parent": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "name": {"type": "string"},
                            },
                        },
                        "updated_at": {"type": "string", "format": "date-time"},
                        "value": {"type": "string"},
                    },
                },
                "supported_sync_modes": ["incremental"],
                "source_defined_primary_key": [["parent", "id"]],
                "default_cursor_field": ["updated_at"],
            },
            "sync_mode": "incremental",
            "destination_sync_mode": "append",
        }
    ]
}


def _reading_line(parent_id: int, value: str) -> str:
    return json.dumps(
        {
            "type": "RECORD",
            "record": {
                "stream": "readings",
                "data": {
                    "parent": {"id": parent_id, "name": f"sensor-{parent_id}"},
                    "updated_at": "2026-01-01",
                    "value": value,
                },
                "emitted_at": 1,
            },
        }
    )


def test_a_nested_primary_key_still_matches_records_and_shows_a_changed_value(
    tmp_path: Path, connector_outputs
) -> None:
    """The key's parent object is masked field by field, so the comparison
    reads the key's token by its path: no record counts as missing its key,
    the pairs match, and the one changed value is the one finding."""
    config = tmp_path / "config.json"
    config.write_text(json.dumps({"api_key": "secret"}))
    catalog = tmp_path / "nested_catalog.json"
    catalog.write_text(json.dumps(NESTED_PK_CATALOG))
    connector_outputs(
        control="\n".join([_reading_line(1, "a"), _reading_line(2, "b")]) + "\n",
        target="\n".join([_reading_line(1, "a"), _reading_line(2, "B")]) + "\n",
    )
    control = _run(tmp_path, (config, catalog), TargetOrControl.CONTROL, "masked")
    target = _run(tmp_path, (config, catalog), TargetOrControl.TARGET, "masked")

    summary, skip_reason = cloud._compare_read_records(
        target_result=target, control_result=control, catalog_file=catalog
    )

    assert skip_reason is None
    assert summary is not None
    checks = summary.to_dict()["checks"]
    assert checks["pk_presence"]["passed"] is True
    field_values = checks["field_values"]["streams"]["readings"]
    assert field_values["records_with_value_diff"] == 1
    assert list(field_values["value_diff_examples"][0]["pk"]) == [
        mask_value(2, key=KEY)
    ]
    assert "sensor" not in json.dumps(summary.to_dict())
    lines = Path(target["stdout_file"]).read_text().splitlines()
    data = json.loads(lines[1])["record"]["data"]
    assert data["parent"] == {
        "id": mask_value(2, key=KEY),
        "name": mask_value("sensor-2", key=KEY),
    }
    assert data["updated_at"] == "2026-01-01"


# ---------------------------------------------------------------------------
# The self-review's leak-path probe: one value per surface a masked run writes
# ---------------------------------------------------------------------------


def _probe_stream(name: str, properties: dict, primary_key: list, cursor: list) -> dict:
    return {
        "stream": {
            "name": name,
            "json_schema": {"type": "object", "properties": properties},
            "supported_sync_modes": ["incremental"],
            "source_defined_primary_key": primary_key,
            "default_cursor_field": cursor,
        },
        "sync_mode": "incremental",
        "destination_sync_mode": "append",
    }


PROBE_CATALOG = {
    "streams": [
        _probe_stream(
            "users",
            {
                "id": {"type": "integer"},
                "updated_at": {"type": "string", "format": "date-time"},
                "email": {"type": "string"},
            },
            [["id"]],
            ["updated_at"],
        ),
        _probe_stream(
            "events",
            {
                "meta": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                    },
                },
                "ts": {"type": "integer"},
            },
            [["meta", "id"]],
            ["ts"],
        ),
        _probe_stream("tokens", {"token": {"type": "string"}}, [["token"]], ["token"]),
        _probe_stream(
            "children",
            {
                "id": {"type": "integer"},
                "updated_at": {"type": "string", "format": "date-time"},
            },
            [["id"]],
            ["updated_at"],
        ),
    ]
}

PROBE_CURSOR = "2026-01-01T00:00:00Z"


def _probe_state(token: str, partition: str) -> list[dict]:
    return [
        {
            "type": "STREAM",
            "stream": {
                "stream_descriptor": {"name": "tokens"},
                "stream_state": {"token": token},
            },
        },
        {
            "type": "STREAM",
            "stream": {
                "stream_descriptor": {"name": "children"},
                "stream_state": {
                    "states": [
                        {
                            "partition": {"parent_id": partition},
                            "cursor": {"updated_at": PROBE_CURSOR},
                        }
                    ]
                },
            },
        },
    ]


def _probe_stdout() -> str:
    def log(level, message):
        return json.dumps({"type": "LOG", "log": {"level": level, "message": message}})

    def trace(kind, **fields):
        return json.dumps(
            {"type": "TRACE", "trace": {"type": kind, "emitted_at": 1.0, **fields}}
        )

    def record(stream, data, **extra):
        return json.dumps(
            {
                "type": "RECORD",
                "record": {"stream": stream, "data": data, "emitted_at": 1, **extra},
            }
        )

    def state(payload):
        return json.dumps({"type": "STATE", "state": payload})

    lines = [
        log("INFO", "x PROBEINFO"),
        log("WARN", "x PROBEWARN"),
        log("DEBUG", "x PROBEDEBUG"),
        log("ERROR", "x PROBEERROR"),
        log("FATAL", "Traceback\nKeyError: PROBEFATAL"),
        log("debug", "x PROBELOWERDEBUG"),
        log("CRITICAL", "x PROBECRITICAL"),
        log("DEBUG", {"body": "PROBEDICTMSG"}),
        trace(
            "ERROR",
            error={
                "message": "x PROBETRACEMSG",
                "internal_message": "x PROBETRACEINTERNAL",
                "stack_trace": "x PROBETRACESTACK",
                "failure_type": "system_error",
            },
        ),
        trace("ANALYTICS", analytics={"type": "x", "value": "PROBEANALYTICS"}),
        trace("ANALYTICS", analytics={"type": "hits", "value": "42"}),
        json.dumps(
            {
                "type": "CONNECTION_STATUS",
                "connectionStatus": {
                    "status": "FAILED",
                    "message": "x PROBECONNSTATUS",
                },
            }
        ),
        json.dumps(
            {
                "type": "CONTROL",
                "control": {
                    "type": "CONNECTOR_CONFIG",
                    "emitted_at": 1.0,
                    "connectorConfig": {"config": {"token": "PROBECONTROLCONFIG"}},
                },
            }
        ),
        json.dumps({"type": "DEBUG", "message": "PROBECDKDEBUG", "data": {}}),
        "plain PROBEPLAINLINE",
        record(
            "users",
            {"id": 1, "updated_at": PROBE_CURSOR, "email": "PROBEEMAIL"},
            meta={
                "changes": [
                    {
                        "field": "PROBEMETAFIELD",
                        "change": "NULLED",
                        "reason": "SOURCE_SERIALIZATION_ERROR",
                    }
                ]
            },
        ),
        record(
            "events",
            {"meta": {"id": "PROBENESTEDPK", "name": "PROBENESTEDSIB"}, "ts": 5},
        ),
        record("users", {"id": 2, "updated_at": "PROBEBADCURSOR@doe.com"}),
        state(
            {
                "type": "STREAM",
                "stream": {
                    "stream_descriptor": {"name": "users"},
                    "stream_state": {"updated_at": "2026-01-01 PROBEDATEPREFIX"},
                },
            }
        ),
        state(
            {
                "type": "STREAM",
                "stream": {
                    "stream_descriptor": {"name": "children"},
                    "stream_state": {
                        "states": [
                            {
                                "partition": {"parent_id": "PROBEPARTITION"},
                                "cursor": {"updated_at": PROBE_CURSOR},
                            }
                        ],
                        "parent_state": {"users": {"updated_at": "PROBEPARENTCURSOR"}},
                        "extra_key": "PROBEEXTRASTATE",
                        "use_global_cursor": False,
                    },
                },
            }
        ),
        state(
            {
                "type": "STREAM",
                "stream": {
                    "stream_descriptor": {"name": "tokens"},
                    "stream_state": {"token": "PROBETOKENSTATE"},
                },
            }
        ),
        state(
            {
                "type": "GLOBAL",
                "global": {
                    "shared_state": {"cdc": "PROBESHARED"},
                    "stream_states": [
                        {
                            "stream_descriptor": {"name": "tokens"},
                            "stream_state": {"token": "PROBETOKENSTATE"},
                        }
                    ],
                },
            }
        ),
    ]
    return "\n".join(lines) + "\n"


# What must come out masked, named by the surface it goes in through.
MASKED_PROBES = {
    "record value": "PROBEEMAIL",
    "free text in a readable record cursor": "PROBEBADCURSOR",
    "text after a date in a readable state cursor": "PROBEDATEPREFIX",
    "nested PK leaf": "PROBENESTEDPK",
    "nested PK sibling": "PROBENESTEDSIB",
    "partition value of a readable stream": "PROBEPARTITION",
    "parent_state cursor of a readable stream": "PROBEPARENTCURSOR",
    "extra key in a readable stream's state": "PROBEEXTRASTATE",
    "masked stream's state cursor": "PROBETOKENSTATE",
    "GLOBAL shared_state": "PROBESHARED",
    "DEBUG message": "PROBEDEBUG",
    "ERROR message": "PROBEERROR",
    "FATAL message": "PROBEFATAL",
    "lowercase 'debug' level": "PROBELOWERDEBUG",
    "CRITICAL level": "PROBECRITICAL",
    "dict message": "PROBEDICTMSG",
    "TRACE error internal_message": "PROBETRACEINTERNAL",
    "TRACE error stack_trace": "PROBETRACESTACK",
    "TRACE analytics value": "PROBEANALYTICS",
    "CONTROL connectorConfig": "PROBECONTROLCONFIG",
    "non-protocol JSON line": "PROBECDKDEBUG",
    "plain text line": "PROBEPLAINLINE",
    "stderr line": "PROBESTDERR",
    "input state masked-stream cursor": "PROBEINPUTTOKEN",
    "input state partition": "PROBEINPUTPARTITION",
    "config secret": "PROBECONFIGSECRET",
}
SEED_PROBES = {
    "seeded state masked-stream cursor": "PROBESEEDTOKEN",
    "seeded state partition": "PROBESEEDPARTITION",
}
# What stays readable on purpose, and is documented as such.
READABLE_PROBES = {
    "INFO message": "PROBEINFO",
    "WARN message": "PROBEWARN",
    "TRACE error message": "PROBETRACEMSG",
    "CONNECTION_STATUS message": "PROBECONNSTATUS",
    "record meta field name": "PROBEMETAFIELD",
    "readable cursor in records and state": PROBE_CURSOR,
    "analytics count": '"value": "42"',
}


@pytest.fixture
def probe_connection(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    """A `--connection-id` run on the probe's catalog and stored state; returns
    what the run wrote to the GitHub outputs and the step summary."""
    captured: dict[str, Any] = {"github_outputs": {}, "step_summary": []}
    data = ConnectionData(
        connection_id="c-1",
        source_id="s-1",
        source_name="test",
        source_definition_id="d-1",
        config={"api_key": "PROBECONFIGSECRET"},
        catalog=PROBE_CATALOG,
        stream_names=["users", "events", "tokens", "children"],
        docker_repository="airbyte/source-test",
        docker_image_tag="2.0.0",
        state=None,
    )
    monkeypatch.setattr(cloud, "ensure_image_available", lambda _image: True)
    monkeypatch.setattr(cloud, "track_regression_test", lambda **_kwargs: None)
    monkeypatch.setattr(cloud, "write_github_summary", captured["step_summary"].append)
    monkeypatch.setattr(
        cloud, "write_github_outputs", captured["github_outputs"].update
    )
    monkeypatch.setattr(cloud, "should_use_secret_retriever", lambda: False)
    monkeypatch.setattr(cloud, "get_connection_residency", lambda _connection_id: "us")
    monkeypatch.setattr(cloud, "is_running_on_eu_runner", lambda: False)
    monkeypatch.setattr(cloud, "fetch_connection_data", lambda _connection_id: data)
    monkeypatch.setattr(
        cloud,
        "enrich_catalog_schemas_from_cloud",
        lambda data: CatalogSchemaEnrichment(
            data, 0, _probe_state("PROBEINPUTTOKEN", "PROBEINPUTPARTITION")
        ),
    )
    return captured


@pytest.mark.parametrize("seeded", [False, True], ids=["connection-state", "seeded"])
def test_a_masked_run_shows_each_probe_value_only_where_it_is_meant_to(
    tmp_path: Path,
    capsys,
    caplog: pytest.LogCaptureFixture,
    connector_outputs,
    probe_connection,
    seeded: bool,
) -> None:
    """One value per way a customer value can reach a surface -- records, a
    nested key, every state shape, every log level and message shape, the
    TRACE kinds, CONTROL, non-protocol lines, stderr, the input and seeded
    state and the config -- checked against every file the run writes, the
    console and the log. The readable ones are the ones the docs name."""
    caplog.set_level("DEBUG")
    connector_outputs(
        control=_probe_stdout(), target=_probe_stdout(), stderr=b"boom PROBESTDERR\n"
    )
    output_dir = tmp_path / "out"
    extra: dict[str, str] = {}
    masked = dict(MASKED_PROBES)
    if seeded:
        seed = tmp_path / "seed_state.json"
        seed.write_text(
            json.dumps(_probe_state("PROBESEEDTOKEN", "PROBESEEDPARTITION"))
        )
        extra["state_path"] = str(seed)
        masked.update(SEED_PROBES)

    with suppress(SystemExit):
        cloud.regression_test(
            skip_compare=True,
            connection_id="c-1",
            command="read",
            output_dir=str(output_dir),
            output_mode="masked",
            **extra,
        )
    console = capsys.readouterr()

    surfaces = {
        str(path.relative_to(output_dir)): path.read_text(errors="replace")
        for path in output_dir.rglob("*")
        if path.is_file()
    }
    surfaces["console.out"] = console.out
    surfaces["console.err"] = console.err
    surfaces["log"] = caplog.text
    assert "stdout.txt" in surfaces and "report.html" in surfaces
    leaked = {
        name: [surface for surface, text in surfaces.items() if value in text]
        for name, value in masked.items()
    }
    assert {name: hits for name, hits in leaked.items() if hits} == {}
    for name, value in READABLE_PROBES.items():
        assert value in surfaces["stdout.txt"], name


def test_a_masked_run_leaves_its_key_in_no_surface(
    tmp_path: Path,
    capsys,
    caplog: pytest.LogCaptureFixture,
    connector_outputs,
    probe_connection,
) -> None:
    """The key is read from the file the workflow hands over and every token
    is hashed under it; it then appears, in hex or raw, in no file the run
    writes, nothing it prints, no log line, no GitHub output and no step
    summary. The probe matrix stands in for a real run's surfaces."""
    caplog.set_level("DEBUG")
    key_hex = secrets.token_hex(32)
    key_file = tmp_path / "mask_key"
    key_file.write_text(key_hex + "\n")
    connector_outputs(
        control=_probe_stdout(), target=_probe_stdout(), stderr=b"boom PROBESTDERR\n"
    )
    output_dir = tmp_path / "out"

    with suppress(SystemExit):
        cloud.regression_test(
            skip_compare=True,
            connection_id="c-1",
            command="read",
            output_dir=str(output_dir),
            output_mode="masked",
            mask_key_path=str(key_file),
        )
    console = capsys.readouterr()

    surfaces = {
        str(path.relative_to(output_dir)): path.read_bytes()
        for path in output_dir.rglob("*")
        if path.is_file()
    }
    assert "stdout.txt" in surfaces and "report.html" in surfaces
    expected = mask_value("PROBEEMAIL", key=bytes.fromhex(key_hex)).encode()
    assert expected in surfaces["stdout.txt"]
    surfaces["console.out"] = console.out.encode()
    surfaces["console.err"] = console.err.encode()
    surfaces["log"] = caplog.text.encode()
    surfaces["github_outputs"] = json.dumps(
        probe_connection["github_outputs"], default=str
    ).encode()
    surfaces["step_summary"] = "\n".join(probe_connection["step_summary"]).encode()
    for needle in (key_hex.encode(), key_hex.upper().encode(), bytes.fromhex(key_hex)):
        assert [name for name, text in surfaces.items() if needle in text] == []
