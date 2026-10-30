# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for the Docker-based connector runner."""

from __future__ import annotations

import json
import logging
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

import pytest
from airbyte_protocol.models import AirbyteMessage, ConfiguredAirbyteCatalog
from airbyte_protocol.models import Type as AirbyteMessageType
from pydantic import ValidationError

from airbyte_ops_mcp.regression_tests import connector_runner as connector_runner_module
from airbyte_ops_mcp.regression_tests.connector_runner import ConnectorRunner
from airbyte_ops_mcp.regression_tests.masking import (
    MASKED_TEXT_PREFIX,
    MaskPolicy,
    mask_value,
)
from airbyte_ops_mcp.regression_tests.models import (
    Command,
    ConnectorUnderTest,
    ExecutionInputs,
    StoppedEarly,
    TargetOrControl,
)
from tests.test_masking import KEY

CONTAINER_CA_PATH = f"{ConnectorRunner.DATA_DIR}/{ConnectorRunner.CA_CERT_FILE}"


@pytest.fixture
def connector_under_test() -> ConnectorUnderTest:
    return ConnectorUnderTest(
        image_name="airbyte/source-shopify:3.2.4",
        target_or_control=TargetOrControl.TARGET,
    )


@pytest.fixture
def execution_inputs(
    connector_under_test: ConnectorUnderTest, tmp_path: Path
) -> ExecutionInputs:
    return ExecutionInputs(
        connector_under_test=connector_under_test,
        command=Command.SPEC,
        output_dir=tmp_path / "output",
    )


@pytest.fixture
def runner(execution_inputs: ExecutionInputs) -> ConnectorRunner:
    return ConnectorRunner(execution_inputs=execution_inputs)


@pytest.mark.parametrize(
    "namespace",
    [pytest.param(None, id="omitted"), pytest.param("sample", id="present")],
)
def test_prepare_data_directory_omits_none_namespace_and_preserves_present(
    connector_under_test: ConnectorUnderTest,
    tmp_path: Path,
    namespace: str | None,
) -> None:
    stream_definition: dict[str, object] = {
        "name": "sample",
        "json_schema": {},
        "supported_sync_modes": ["full_refresh"],
    }
    if namespace is not None:
        stream_definition["namespace"] = namespace
    catalog = ConfiguredAirbyteCatalog.model_validate(
        {
            "streams": [
                {
                    "stream": stream_definition,
                    "sync_mode": "full_refresh",
                    "destination_sync_mode": "append",
                }
            ]
        }
    )
    inputs = ExecutionInputs(
        connector_under_test=connector_under_test,
        command=Command.READ,
        output_dir=tmp_path / "output",
        config={},
        configured_catalog=catalog,
    )
    catalog_runner = ConnectorRunner(execution_inputs=inputs)
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    catalog_runner._prepare_data_directory(data_dir)

    written_stream = json.loads((data_dir / ConnectorRunner.CATALOG_FILE).read_text())[
        "streams"
    ][0]["stream"]
    if namespace is None:
        assert "namespace" not in written_stream
    else:
        assert written_stream["namespace"] == namespace


def test_build_docker_command_overrides_workdir(
    runner: ConnectorRunner, tmp_path: Path
) -> None:
    """The docker command must override the container's WORKDIR to /tmp.

    This ensures the non-root `airbyte` user (UID 1000) can write temporary files
    (e.g. bulk GraphQL result files in source-shopify) via relative paths without
    shadowing the connector code installed at /airbyte/integration_code.
    """
    cmd = runner._build_docker_command(tmp_path)

    assert "-w" in cmd, "Docker command must include -w flag"
    w_idx = cmd.index("-w")
    assert cmd[w_idx + 1] == "/tmp", (
        f"WORKDIR override must be /tmp, got: {cmd[w_idx + 1]}"
    )


@pytest.mark.parametrize(
    "proxy_url,expect_proxy_env",
    [
        pytest.param(None, False, id="no-proxy"),
        pytest.param("http://host.docker.internal:8080", True, id="with-proxy"),
    ],
)
def test_build_docker_command_proxy_settings(
    connector_under_test: ConnectorUnderTest,
    tmp_path: Path,
    proxy_url: str | None,
    expect_proxy_env: bool,
) -> None:
    """Proxy settings should be added when proxy_url is set, regardless of the /tmp WORKDIR override."""
    inputs = ExecutionInputs(
        connector_under_test=connector_under_test,
        command=Command.SPEC,
        output_dir=tmp_path / "output",
    )
    runner = ConnectorRunner(execution_inputs=inputs, proxy_url=proxy_url)
    cmd = runner._build_docker_command(tmp_path)

    if expect_proxy_env:
        assert "-e" in cmd
        env_values = [cmd[i + 1] for i, v in enumerate(cmd) if v == "-e"]
        proxy_envs = [e for e in env_values if "PROXY" in e.upper()]
        assert len(proxy_envs) >= 2, "Should set at least HTTP_PROXY and HTTPS_PROXY"
    else:
        env_values = [cmd[i + 1] for i, v in enumerate(cmd) if v == "-e"]
        proxy_envs = [e for e in env_values if "PROXY" in e.upper()]
        assert len(proxy_envs) == 0, "No proxy env vars expected"

    # WORKDIR override should always be present
    assert "-w" in cmd


IMAGE_ROOT_CA = (
    "-----BEGIN CERTIFICATE-----\nimage-root-ca\n-----END CERTIFICATE-----\n"
)
IMAGE_CERTIFI_PATH = "/usr/local/lib/python3.11/site-packages/certifi/cacert.pem"


@pytest.fixture
def no_certifi_discovery(monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep `_build_docker_command` from shelling out to Docker in unit tests."""
    monkeypatch.setattr(
        connector_runner_module, "_discover_certifi_bundle", lambda _image: None
    )


@pytest.fixture
def image_certifi_bundle(monkeypatch: pytest.MonkeyPatch) -> None:
    """Stand in for an image whose `certifi` bundle already has roots in it."""
    monkeypatch.setattr(
        connector_runner_module,
        "_discover_certifi_bundle",
        lambda _image: (IMAGE_CERTIFI_PATH, IMAGE_ROOT_CA),
    )


@pytest.fixture
def ca_cert_file(tmp_path: Path) -> Path:
    cert = tmp_path / "mitmproxy-ca-cert.pem"
    cert.write_text("-----BEGIN CERTIFICATE-----\nnot-a-real-cert\n")
    return cert


def _env_values(cmd: list[str]) -> list[str]:
    return [cmd[i + 1] for i, value in enumerate(cmd) if value == "-e"]


def test_proxy_ca_cert_is_mounted_and_trusted(
    connector_under_test: ConnectorUnderTest,
    tmp_path: Path,
    ca_cert_file: Path,
    no_certifi_discovery: None,
) -> None:
    """With a proxy but no trusted CA, every HTTPS request fails verification.

    That failure is quiet -- the run just captures few or no flows -- so pin the
    two env vars and the PEM that make the container trust the proxy.
    """
    inputs = ExecutionInputs(
        connector_under_test=connector_under_test,
        command=Command.SPEC,
        output_dir=tmp_path / "output",
    )
    runner = ConnectorRunner(
        execution_inputs=inputs,
        proxy_url="http://host.docker.internal:8080",
        ca_cert_path=ca_cert_file,
    )
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    runner._prepare_data_directory(data_dir)
    cmd = runner._build_docker_command(data_dir)

    assert (
        ca_cert_file.read_text().strip()
        in (data_dir / ConnectorRunner.CA_CERT_FILE).read_text()
    )
    env_values = _env_values(cmd)
    assert f"REQUESTS_CA_BUNDLE={CONTAINER_CA_PATH}" in env_values
    assert f"SSL_CERT_FILE={CONTAINER_CA_PATH}" in env_values


def test_certifi_bundle_is_overridden_when_the_image_has_one(
    connector_under_test: ConnectorUnderTest,
    tmp_path: Path,
    ca_cert_file: Path,
    image_certifi_bundle: None,
) -> None:
    """`httpx` and friends pin `certifi.where()` and ignore the env vars."""
    inputs = ExecutionInputs(
        connector_under_test=connector_under_test,
        command=Command.SPEC,
        output_dir=tmp_path / "output",
    )
    runner = ConnectorRunner(
        execution_inputs=inputs,
        proxy_url="http://host.docker.internal:8080",
        ca_cert_path=ca_cert_file,
    )
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    cmd = runner._build_docker_command(data_dir)

    mounts = [cmd[i + 1] for i, value in enumerate(cmd) if value == "-v"]
    assert (
        f"{data_dir / ConnectorRunner.CA_CERT_FILE}:{IMAGE_CERTIFI_PATH}:ro" in mounts
    )


def test_grpc_clients_trust_the_proxy_through_the_same_bundle(
    connector_under_test: ConnectorUnderTest,
    tmp_path: Path,
    ca_cert_file: Path,
    image_certifi_bundle: None,
) -> None:
    """`grpcio` ignores every setting above and checks its own bundled roots.

    Without this a gRPC client never connects through the proxy, on either
    version, and the comparison says nothing: source-google-ads loads its
    custom-query schemas over gRPC. It must be the combined bundle, not the CA
    alone, so gRPC hosts reached without the proxy still verify.
    """
    inputs = ExecutionInputs(
        connector_under_test=connector_under_test,
        command=Command.SPEC,
        output_dir=tmp_path / "output",
    )
    runner = ConnectorRunner(
        execution_inputs=inputs,
        proxy_url="http://host.docker.internal:8080",
        ca_cert_path=ca_cert_file,
    )
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    runner._prepare_data_directory(data_dir)
    cmd = runner._build_docker_command(data_dir)

    assert f"GRPC_DEFAULT_SSL_ROOTS_FILE_PATH={CONTAINER_CA_PATH}" in _env_values(cmd)
    bundle = (data_dir / ConnectorRunner.CA_CERT_FILE).read_text()
    assert ca_cert_file.read_text().strip() in bundle
    assert bundle.strip() != ca_cert_file.read_text().strip()


def test_the_trust_bundle_extends_the_image_roots_rather_than_replacing_them(
    connector_under_test: ConnectorUnderTest,
    tmp_path: Path,
    ca_cert_file: Path,
    image_certifi_bundle: None,
) -> None:
    """Replacing the image's roots breaks TLS that bypasses the proxy.

    A client honouring `NO_PROXY`, a vendored SDK with its own session, or any
    non-HTTP TLS would fail to verify a perfectly ordinary certificate -- and
    that failure reads as a regression in the connector version under test.
    """
    inputs = ExecutionInputs(
        connector_under_test=connector_under_test,
        command=Command.SPEC,
        output_dir=tmp_path / "output",
    )
    runner = ConnectorRunner(
        execution_inputs=inputs,
        proxy_url="http://host.docker.internal:8080",
        ca_cert_path=ca_cert_file,
    )
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    runner._prepare_data_directory(data_dir)

    written = (data_dir / ConnectorRunner.CA_CERT_FILE).read_text()
    assert IMAGE_ROOT_CA.strip() in written
    assert ca_cert_file.read_text().strip() in written


def test_the_trust_bundle_falls_back_to_the_ca_alone_without_a_certifi_bundle(
    connector_under_test: ConnectorUnderTest,
    tmp_path: Path,
    ca_cert_file: Path,
    no_certifi_discovery: None,
) -> None:
    inputs = ExecutionInputs(
        connector_under_test=connector_under_test,
        command=Command.SPEC,
        output_dir=tmp_path / "output",
    )
    runner = ConnectorRunner(
        execution_inputs=inputs,
        proxy_url="http://host.docker.internal:8080",
        ca_cert_path=ca_cert_file,
    )
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    runner._prepare_data_directory(data_dir)

    assert (data_dir / ConnectorRunner.CA_CERT_FILE).read_text() == (
        ca_cert_file.read_text()
    )


@pytest.mark.parametrize(
    "proxy_url,with_ca",
    [
        pytest.param(None, True, id="ca-without-proxy"),
        pytest.param("http://host.docker.internal:8080", False, id="proxy-without-ca"),
    ],
)
def test_ca_trust_is_left_alone_without_both_a_proxy_and_a_cert(
    connector_under_test: ConnectorUnderTest,
    tmp_path: Path,
    ca_cert_file: Path,
    no_certifi_discovery: None,
    proxy_url: str | None,
    with_ca: bool,
) -> None:
    """A CA without a proxy (or the reverse) must not touch the argv."""
    inputs = ExecutionInputs(
        connector_under_test=connector_under_test,
        command=Command.SPEC,
        output_dir=tmp_path / "output",
    )
    runner = ConnectorRunner(
        execution_inputs=inputs,
        proxy_url=proxy_url,
        ca_cert_path=ca_cert_file if with_ca else None,
    )
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    runner._prepare_data_directory(data_dir)
    cmd = runner._build_docker_command(data_dir)

    assert not (data_dir / ConnectorRunner.CA_CERT_FILE).exists()
    assert not [
        value
        for value in _env_values(cmd)
        if value.startswith(
            (
                "REQUESTS_CA_BUNDLE=",
                "SSL_CERT_FILE=",
                "GRPC_DEFAULT_SSL_ROOTS_FILE_PATH=",
            )
        )
    ]


def test_a_failed_certifi_probe_is_retried_rather_than_cached(
    connector_under_test: ConnectorUnderTest,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """One transient Docker error must not downgrade HTTPS trust for the run.

    Every command in a regression run builds its own container, so caching a
    failure would carry a single hiccup across all of them -- silently, since
    the fallback is a working-looking run with an untrusted proxy.
    """
    monkeypatch.setattr(connector_runner_module, "_CERTIFI_BUNDLES", {})
    attempts: list[str] = []

    def _flaky_run(cmd: list[str], **_kwargs: object):
        attempts.append(cmd[-1])
        if len(attempts) == 1:
            raise OSError("docker socket unavailable")
        return subprocess.CompletedProcess(
            cmd, 0, stdout=f"{IMAGE_CERTIFI_PATH}\n{IMAGE_ROOT_CA}", stderr=""
        )

    monkeypatch.setattr(connector_runner_module.subprocess, "run", _flaky_run)

    assert connector_runner_module._discover_certifi_bundle("airbyte/x:1") is None
    assert connector_runner_module._discover_certifi_bundle("airbyte/x:1") == (
        IMAGE_CERTIFI_PATH,
        IMAGE_ROOT_CA,
    )
    # The success is cached, so a third call does not probe again.
    assert connector_runner_module._discover_certifi_bundle("airbyte/x:1") == (
        IMAGE_CERTIFI_PATH,
        IMAGE_ROOT_CA,
    )
    assert len(attempts) == 2


def test_only_an_image_with_a_certifi_bundle_can_trust_the_proxy(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The env vars alone cover no JVM client, so no bundle means no capture."""
    monkeypatch.setattr(
        connector_runner_module,
        "_discover_certifi_bundle",
        lambda _image: (IMAGE_CERTIFI_PATH, IMAGE_ROOT_CA),
    )
    assert connector_runner_module.proxy_trust_gap("airbyte/source-py:1") is None

    monkeypatch.setattr(
        connector_runner_module, "_discover_certifi_bundle", lambda _image: None
    )
    gap = connector_runner_module.proxy_trust_gap("airbyte/source-jvm:1")
    assert gap is not None
    assert gap.startswith("airbyte/source-jvm:1 has no certifi bundle")
    assert "JKS truststore" in gap


def test_one_runner_probes_certifi_once_so_its_two_consumers_agree(
    connector_under_test: ConnectorUnderTest,
    tmp_path: Path,
    ca_cert_file: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A retried probe must not disagree with the file it already wrote.

    Retrying a failed probe is right, but the trust bundle written by
    `_prepare_data_directory` and the mount decided by `_build_docker_command`
    are two consumers of the same answer. A probe that fails and then succeeds
    would mount a bundle holding the proxy CA *alone* over the image's certifi
    roots -- TLS failures on every connection that does not go through the
    proxy, reading as a regression in the version under test.
    """
    answers: list[tuple[str, str] | None] = [None, (IMAGE_CERTIFI_PATH, IMAGE_ROOT_CA)]
    monkeypatch.setattr(
        connector_runner_module,
        "_discover_certifi_bundle",
        lambda _image: answers.pop(0),
    )

    inputs = ExecutionInputs(
        connector_under_test=connector_under_test,
        command=Command.SPEC,
        output_dir=tmp_path / "output",
    )
    runner = ConnectorRunner(
        execution_inputs=inputs,
        proxy_url="http://host.docker.internal:8080",
        ca_cert_path=ca_cert_file,
    )
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    runner._prepare_data_directory(data_dir)
    cmd = runner._build_docker_command(data_dir)

    written = (data_dir / ConnectorRunner.CA_CERT_FILE).read_text()
    mounts = [cmd[i + 1] for i, value in enumerate(cmd) if value == "-v"]
    certifi_mounts = [mount for mount in mounts if IMAGE_CERTIFI_PATH in mount]

    assert len(answers) == 1, "the runner must probe at most once"
    assert IMAGE_ROOT_CA.strip() not in written
    assert not certifi_mounts, (
        "a CA-only bundle was mounted over the image's certifi roots"
    )


# ---------------------------------------------------------------------------
# run(): streaming capture
# ---------------------------------------------------------------------------

# Stands in for `docker run`: replays a file to stdout line by line, sleeps in
# silence, or emits records -- whichever the test needs the container to do.
FAKE_CONNECTOR = """
import os
import sys
import time

mode = sys.argv[1]
if mode == "cat":
    with open(sys.argv[2], "rb") as source:
        for line in source:
            sys.stdout.buffer.write(line)
            sys.stdout.buffer.flush()
    sys.stderr.write("connector log line\\n")
    sys.stderr.flush()
    sys.exit(int(sys.argv[3]))
elif mode == "stderr":
    with open(sys.argv[2], "rb") as source:
        sys.stderr.buffer.write(source.read())
    sys.stderr.buffer.flush()
    sys.exit(int(sys.argv[3]))
elif mode == "sleep":
    time.sleep(float(sys.argv[2]))
elif mode == "partial":
    sys.stdout.buffer.write(
        b'{"type": "RECORD", "record": {"stream": "users", "data": {"id": 1}, "emitted_at": 1}}\\n'
    )
    sys.stdout.buffer.write(
        b'{"type": "RECORD", "record": {"stream": "users", "data": {"id": 2, "name": "\\xe2\\x82'
    )
    sys.stdout.buffer.flush()
    time.sleep(float(sys.argv[2]))
elif mode == "records":
    for index in range(int(sys.argv[2])):
        sys.stdout.buffer.write(
            b'{"type": "RECORD", "record": {"stream": "users", "data": {"id": %d}, "emitted_at": 1}}\\n'
            % index
        )
        sys.stdout.buffer.flush()
    sys.stderr.write("done emitting\\n")
    sys.stderr.flush()
    time.sleep(float(sys.argv[3]))
elif mode == "linger":
    # Ends its output, then outlives it, as a `docker` CLI can.
    for index in range(int(sys.argv[2])):
        sys.stdout.buffer.write(
            b'{"type": "RECORD", "record": {"stream": "users", "data": {"id": %d}, "emitted_at": 1}}\\n'
            % index
        )
    sys.stdout.buffer.flush()
    os.dup2(os.open(os.devnull, os.O_WRONLY), 1)
    time.sleep(float(sys.argv[3]))
"""

# Every message type a read emits, a line that is not a message, a blank line,
# non-ASCII bytes, and no newline at the end: whatever the connector wrote is
# what the file must hold.
FIXTURE_STDOUT = (
    b'{"type": "LOG", "log": {"level": "INFO", "message": "starting"}}\n'
    b"not a protocol message\n"
    b"\n"
    b'{"type": "RECORD", "record": {"stream": "users", "data": {"id": 1, "name": "h\xc3\xa9llo"}, "emitted_at": 1}}\n'
    b'{"type": "STATE", "state": {"type": "STREAM", "stream": {"stream_descriptor": {"name": "users"}, "stream_state": {"cursor": "2024-01-01"}}}}\n'
    b'{"type": "TRACE", "trace": {"type": "STREAM_STATUS", "emitted_at": 1.0, "stream_status": {"stream_descriptor": {"name": "users"}, "status": "COMPLETE"}}}\n'
    b'{"type": "RECORD", "record": {"stream": "users", "data": {"id": 2}, "emitted_at": 2}}'
)


@pytest.fixture
def fake_connector(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """Make the runner start `FAKE_CONNECTOR` where it would start `docker run`."""
    script = tmp_path / "fake_connector.py"
    script.write_text(FAKE_CONNECTOR)

    def _install(*args: str) -> None:
        def _fake_build(self: ConnectorRunner, _temp_dir: Path) -> list[str]:
            self._container_name = "connector-test-fake"
            return [sys.executable, str(script), *args]

        monkeypatch.setattr(ConnectorRunner, "_build_docker_command", _fake_build)

    return _install


@pytest.fixture
def spawned(monkeypatch: pytest.MonkeyPatch) -> list[subprocess.Popen]:
    """Every process the runner starts, so a test can stand in for Docker."""
    processes: list[subprocess.Popen] = []
    real_popen = subprocess.Popen

    class RecordingPopen(real_popen):  # type: ignore[misc,valid-type]
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            processes.append(self)

    monkeypatch.setattr(connector_runner_module.subprocess, "Popen", RecordingPopen)
    return processes


@pytest.fixture
def removed_containers(
    monkeypatch: pytest.MonkeyPatch, spawned: list[subprocess.Popen]
) -> list[str]:
    """Stand in for `docker rm -f`: record the name and end the fake container."""
    removed: list[str] = []

    def _remove(container_name: str) -> None:
        removed.append(container_name)
        for process in spawned:
            process.kill()

    monkeypatch.setattr(connector_runner_module, "_force_remove_container", _remove)
    return removed


def _read_runner(tmp_path: Path, **kwargs: object) -> ConnectorRunner:
    inputs = ExecutionInputs(
        connector_under_test=ConnectorUnderTest(
            image_name="airbyte/source-test:1.0.0",
            target_or_control=TargetOrControl.TARGET,
        ),
        command=Command.SPEC,
        output_dir=tmp_path / "output",
    )
    return ConnectorRunner(execution_inputs=inputs, **kwargs)  # type: ignore[arg-type]


def test_run_writes_stdout_and_stderr_byte_for_byte(
    tmp_path: Path, fake_connector
) -> None:
    """Streaming the output to disk must not change a byte of it."""
    fixture = tmp_path / "fixture_stdout.jsonl"
    fixture.write_bytes(FIXTURE_STDOUT)
    fake_connector("cat", str(fixture), "0")

    result = _read_runner(tmp_path).run()

    assert result.success is True
    assert result.exit_code == 0
    assert result.stopped_early is None
    assert result.stdout_file_path.read_bytes() == FIXTURE_STDOUT
    assert result.stderr_file_path.read_bytes() == b"connector log line\n"


def test_a_failed_command_keeps_its_exit_code_and_its_stderr(
    tmp_path: Path, fake_connector
) -> None:
    fixture = tmp_path / "fixture_stdout.jsonl"
    fixture.write_bytes(FIXTURE_STDOUT)
    fake_connector("cat", str(fixture), "3")

    result = _read_runner(tmp_path).run()

    assert result.success is False
    assert result.exit_code == 3
    assert result.stdout_file_path.read_bytes() == FIXTURE_STDOUT
    assert result.stderr_file_path.read_bytes() == b"connector log line\n"


def test_a_silent_connector_is_stopped_at_the_deadline(
    tmp_path: Path, fake_connector, removed_containers: list[str]
) -> None:
    """A deadline that only ticks when output arrives never fires on a hang.

    The container has to go too: a killed `docker` CLI leaves it running, and
    `--rm` only fires when the container exits on its own. The kill is the
    harness's doing, so the exit it produces is not reported as a crash.
    """
    fake_connector("sleep", "60")

    started = time.monotonic()
    result = _read_runner(tmp_path, timeout_seconds=1).run()

    assert time.monotonic() - started < 20
    assert removed_containers == ["connector-test-fake"]
    assert result.success is True
    assert result.exit_code == 0
    assert result.stopped_early is not None
    assert result.stopped_early.reason == "timeout"
    assert result.stopped_early.records_seen == 0
    assert 1 <= result.stopped_early.elapsed_s < 20
    assert result.stdout_file_path.read_bytes() == b""
    assert b"Command timed out after 1 seconds" in result.stderr_file_path.read_bytes()


def test_a_connector_cut_off_mid_read_keeps_what_it_had_written(
    tmp_path: Path, fake_connector, removed_containers: list[str]
) -> None:
    fake_connector("records", "5", "60")

    result = _read_runner(tmp_path, timeout_seconds=1).run()

    assert removed_containers == ["connector-test-fake"]
    assert result.stopped_early is not None
    assert result.stopped_early.reason == "timeout"
    assert result.stopped_early.records_seen == 5
    assert result.stdout_file_path.read_bytes().count(b'"RECORD"') == 5
    assert result.get_record_count_per_stream() == {"users": 5}


def test_a_line_cut_mid_character_by_the_deadline_is_not_kept(
    tmp_path: Path, fake_connector, removed_containers: list[str]
) -> None:
    """The kill lands at an arbitrary byte, here inside a three-byte character.

    Only whole lines can be messages, so the fragment is dropped rather than
    written: kept, it would make `stdout.txt` undecodable for every reader.
    """
    fake_connector("partial", "60")

    result = _read_runner(tmp_path, timeout_seconds=1).run()

    assert removed_containers == ["connector-test-fake"]
    assert result.stopped_early is not None
    assert result.stopped_early.reason == "timeout"
    assert result.stopped_early.records_seen == 1
    assert result.stdout_file_path.read_bytes() == (
        b'{"type": "RECORD", "record": {"stream": "users", "data": {"id": 1}, '
        b'"emitted_at": 1}}\n'
    )
    result.save_artifacts(tmp_path / "artifacts")
    assert result.get_record_count_per_stream() == {"users": 1}


def test_the_record_cap_stops_the_read_on_the_record_past_it(
    tmp_path: Path, fake_connector, removed_containers: list[str]
) -> None:
    """A side capped at N must hold exactly N records, so the file ends on
    the N-th record: the one past the cap, and whatever the container flushed
    after it, is not kept."""
    fake_connector("records", "50", "60")

    started = time.monotonic()
    result = _read_runner(tmp_path, timeout_seconds=30, max_records=3).run()

    assert time.monotonic() - started < 20
    assert removed_containers == ["connector-test-fake"]
    assert result.success is True
    assert result.exit_code == 0
    assert result.stopped_early == StoppedEarly(
        reason="cap", records_seen=3, elapsed_s=result.stopped_early.elapsed_s
    )
    lines = result.stdout_file_path.read_bytes().splitlines()
    assert [b'"id": %d' % index in line for index, line in enumerate(lines)] == [
        True,
        True,
        True,
    ]
    assert b"Record cap of 3 reached" in result.stderr_file_path.read_bytes()
    assert result.get_record_count_per_stream() == {"users": 3}


def test_a_capped_chatty_connector_is_drained_rather_than_left_blocked(
    tmp_path: Path,
    fake_connector,
    spawned: list[subprocess.Popen],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Thousands of records are still in the pipe when the cap lands.

    If the runner waited for the CLI before reading them, the CLI would sit
    blocked on a full pipe until the kill fallback; draining first lets it
    exit on its own, so the run ends at once and nothing is killed.
    """
    fake_connector("records", "50000", "0")
    monkeypatch.setattr(
        connector_runner_module, "_force_remove_container", lambda _name: None
    )
    monkeypatch.setattr(connector_runner_module, "CONTAINER_REMOVAL_TIMEOUT_SECONDS", 5)

    started = time.monotonic()
    result = _read_runner(tmp_path, max_records=3).run()

    assert time.monotonic() - started < 4
    assert spawned[-1].returncode == 0
    assert result.stopped_early is not None
    assert result.stopped_early.reason == "cap"
    assert result.get_record_count_per_stream() == {"users": 3}


def test_a_cap_the_connector_never_reaches_leaves_the_run_alone(
    tmp_path: Path, fake_connector, removed_containers: list[str]
) -> None:
    fake_connector("records", "2", "0")

    result = _read_runner(tmp_path, max_records=3).run()

    assert removed_containers == []
    assert result.stopped_early is None
    assert result.success is True
    assert result.get_record_count_per_stream() == {"users": 2}


def test_a_read_of_exactly_the_cap_is_complete(
    tmp_path: Path, fake_connector, removed_containers: list[str]
) -> None:
    """Reaching the cap is not passing it: no record past the N-th arrived."""
    fake_connector("records", "3", "0")

    result = _read_runner(tmp_path, max_records=3).run()

    assert removed_containers == []
    assert result.stopped_early is None
    assert result.success is True
    assert result.get_record_count_per_stream() == {"users": 3}


def test_a_read_of_exactly_the_cap_keeps_the_state_after_its_last_record(
    tmp_path: Path, fake_connector, removed_containers: list[str]
) -> None:
    source = tmp_path / "source.jsonl"
    source.write_bytes(
        b'{"type": "RECORD", "record": {"stream": "users", "data": {"id": 1}, "emitted_at": 1}}\n'
        b'{"type": "RECORD", "record": {"stream": "users", "data": {"id": 2}, "emitted_at": 1}}\n'
        b'{"type": "STATE", "state": {"type": "STREAM", "stream": {"stream_descriptor": {"name": "users"}, "stream_state": {"cursor": 2}}}}\n'
    )
    fake_connector("cat", str(source), "0")

    result = _read_runner(tmp_path, max_records=2).run()

    assert removed_containers == []
    assert result.stopped_early is None
    assert result.stdout_file_path.read_bytes() == source.read_bytes()


class _DeadlineFiringAsItIsCancelled:
    """A deadline timer that fires at the last moment it still can.

    Started, it waits; cancelled, it fires first. The runner cancels its
    deadline only after the output ended and the CLI exited, so this is the
    timer losing the race to a read that is already complete.
    """

    def __init__(self, _interval: float, function) -> None:
        self.function = function
        self.daemon = False

    def start(self) -> None:
        pass

    def cancel(self) -> None:
        self.function()


def test_a_deadline_that_fires_after_the_output_ended_stops_nothing(
    tmp_path: Path,
    fake_connector,
    removed_containers: list[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A read that reached the end of its output is never marked stopped."""
    fixture = tmp_path / "fixture_stdout.jsonl"
    fixture.write_bytes(FIXTURE_STDOUT)
    fake_connector("cat", str(fixture), "0")
    monkeypatch.setattr(
        connector_runner_module.threading, "Timer", _DeadlineFiringAsItIsCancelled
    )

    result = _read_runner(tmp_path, timeout_seconds=1).run()

    assert result.stopped_early is None
    assert result.success is True
    assert result.exit_code == 0
    assert removed_containers == []
    assert result.stdout_file_path.read_bytes() == FIXTURE_STDOUT
    assert b"timed out" not in result.stderr_file_path.read_bytes()


def test_a_cli_that_outlives_its_output_past_the_deadline_is_not_a_stop(
    tmp_path: Path, fake_connector, removed_containers: list[str]
) -> None:
    """The deadline passes while the CLI lingers after its output ended.

    The records are all there, so the read is complete; the CLI exits within
    the grace, so nothing is taken down and its own exit code stands.
    """
    fake_connector("linger", "3", "2")

    result = _read_runner(tmp_path, timeout_seconds=1).run()

    assert result.stopped_early is None
    assert result.success is True
    assert result.exit_code == 0
    assert removed_containers == []
    assert result.get_record_count_per_stream() == {"users": 3}


def test_a_deadline_after_the_cli_failed_keeps_its_exit_code(
    tmp_path: Path,
    fake_connector,
    spawned: list[subprocess.Popen],
    removed_containers: list[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The deadline passes while a failed CLI's buffered output is still read.

    The CLI exited before the deadline, so the read is complete and its
    nonzero exit is reported, not hidden behind a stop with exit code 0.
    """
    fixture = tmp_path / "fixture_stdout.jsonl"
    fixture.write_bytes(FIXTURE_STDOUT)
    fake_connector("cat", str(fixture), "2")
    deadlines: list = []

    class _HeldDeadline:
        def __init__(self, _interval: float, function) -> None:
            deadlines.append(function)
            self.daemon = False

        def start(self) -> None:
            pass

        def cancel(self) -> None:
            pass

    real_is_record = connector_runner_module._is_record

    def _is_record_once_the_cli_exited(line: bytes) -> bool:
        if deadlines:
            spawned[0].wait()
            deadlines.pop()()
        return real_is_record(line)

    monkeypatch.setattr(connector_runner_module.threading, "Timer", _HeldDeadline)
    monkeypatch.setattr(
        connector_runner_module, "_is_record", _is_record_once_the_cli_exited
    )

    result = _read_runner(tmp_path, timeout_seconds=1).run()

    assert result.stopped_early is None
    assert result.success is False
    assert result.exit_code == 2
    assert removed_containers == []
    assert result.stdout_file_path.read_bytes() == FIXTURE_STDOUT
    assert b"timed out" not in result.stderr_file_path.read_bytes()


def test_a_cli_wedged_after_its_output_is_taken_down_and_fails(
    tmp_path: Path,
    fake_connector,
    removed_containers: list[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Past the deadline and the grace, a wedged CLI still has to go.

    Its output was complete, so the run is not stopped early: it reports the
    exit code the kill gave it, a failure.
    """
    fake_connector("linger", "3", "60")
    monkeypatch.setattr(
        connector_runner_module, "CONTAINER_REMOVAL_TIMEOUT_SECONDS", 0.2
    )

    started = time.monotonic()
    result = _read_runner(tmp_path, timeout_seconds=1).run()

    assert time.monotonic() - started < 20
    assert removed_containers == ["connector-test-fake"]
    assert result.stopped_early is None
    assert result.success is False
    assert result.exit_code != 0
    assert result.get_record_count_per_stream() == {"users": 3}


def test_the_docker_cli_is_killed_when_the_container_will_not_go(
    tmp_path: Path,
    fake_connector,
    spawned: list[subprocess.Popen],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Without a daemon to answer `docker rm -f`, the CLI itself is the fallback."""
    fake_connector("sleep", "60")
    monkeypatch.setattr(
        connector_runner_module, "_force_remove_container", lambda _name: None
    )
    monkeypatch.setattr(
        connector_runner_module, "CONTAINER_REMOVAL_TIMEOUT_SECONDS", 0.2
    )

    started = time.monotonic()
    result = _read_runner(tmp_path, timeout_seconds=1).run()

    assert time.monotonic() - started < 20
    assert result.stopped_early is not None
    assert result.stopped_early.reason == "timeout"
    assert spawned[-1].returncode is not None


# ---------------------------------------------------------------------------
# run(): masking in the write pass
# ---------------------------------------------------------------------------

MASKABLE_STDOUT = (
    b'{"type": "LOG", "log": {"level": "INFO", "message": "Syncing users"}}\n'
    b'{"type": "LOG", "log": {"level": "DEBUG", "message": "GET /users -> {\\"email\\": \\"alice@example.com\\"}"}}\n'
    b"print('alice@example.com')\n"
    b'{"type": "RECORD", "record": {"stream": "users", "data": {"id": 1, "updated_at": "2026-01-01", "email": "alice@example.com", "address": {"city": "Paris"}}, "emitted_at": 1}}\n'
    b'{"type": "STATE", "state": {"type": "STREAM", "stream": {"stream_descriptor": {"name": "users"}, "stream_state": {"updated_at": "2026-01-01"}}}}\n'
    b'{"type": "RECORD", "record": {"stream": "users", "data": {"id": 2, "updated_at": "2026-01-02", "email": "bob@example.com", "address": null}, "emitted_at": 2}}\n'
)

# The cursor stays readable; the primary key, like every other value, does not.
USERS_POLICY = MaskPolicy({"users": frozenset({("updated_at",)})}, key=KEY)


def test_a_masked_run_writes_tokens_and_keeps_the_cursor_readable(
    tmp_path: Path, fake_connector
) -> None:
    """The mask is applied before a line is written, so raw values never land."""
    fixture = tmp_path / "fixture_stdout.jsonl"
    fixture.write_bytes(MASKABLE_STDOUT)
    fake_connector("cat", str(fixture), "0")

    result = _read_runner(tmp_path, mask_policy=USERS_POLICY).run()

    assert result.success is True
    stdout = result.stdout_file_path.read_bytes()
    assert b"alice" not in stdout
    assert b"bob" not in stdout
    assert b"Paris" not in stdout
    lines = stdout.splitlines()
    assert lines[0] == MASKABLE_STDOUT.splitlines()[0]  # INFO: byte for byte
    debug = json.loads(lines[1])
    assert debug["log"]["message"].startswith(MASKED_TEXT_PREFIX)
    assert lines[2].startswith(MASKED_TEXT_PREFIX.encode())
    first = json.loads(lines[3])["record"]["data"]
    assert first == {
        "id": mask_value(1, key=KEY),
        "updated_at": "2026-01-01",
        "email": mask_value("alice@example.com", key=KEY),
        "address": mask_value({"city": "Paris"}, key=KEY),
    }
    assert lines[4] == MASKABLE_STDOUT.splitlines()[4]  # STATE: byte for byte
    second = json.loads(lines[5])["record"]["data"]
    assert second["id"] == mask_value(2, key=KEY)
    assert second["email"] == mask_value("bob@example.com", key=KEY)
    assert second["address"] is None
    assert result.get_record_count_per_stream() == {"users": 2}
    assert result.get_final_state_per_stream() == {
        (None, "users"): {"updated_at": "2026-01-01"}
    }


def test_the_artifacts_of_a_masked_run_are_built_from_the_masked_output(
    tmp_path: Path, fake_connector
) -> None:
    fixture = tmp_path / "fixture_stdout.jsonl"
    fixture.write_bytes(MASKABLE_STDOUT)
    fake_connector("cat", str(fixture), "0")

    result = _read_runner(tmp_path, mask_policy=USERS_POLICY).run()
    result.save_artifacts(tmp_path / "artifacts")

    for name in ("record.jsonl", "log.jsonl", "state.jsonl"):
        assert (
            b"alice"
            not in (tmp_path / "artifacts/airbyte_messages" / name).read_bytes()
        )
    records = [
        json.loads(line)
        for line in (tmp_path / "artifacts/airbyte_messages/record.jsonl")
        .read_text()
        .splitlines()
    ]
    assert [record["record"]["data"]["id"] for record in records] == [
        mask_value(1, key=KEY),
        mask_value(2, key=KEY),
    ]
    assert records[0]["record"]["data"]["email"] == mask_value(
        "alice@example.com", key=KEY
    )


def test_the_record_cap_counts_masked_records(
    tmp_path: Path, fake_connector, removed_containers: list[str]
) -> None:
    fake_connector("records", "50", "60")

    result = _read_runner(
        tmp_path, max_records=3, mask_policy=MaskPolicy(key=KEY)
    ).run()

    assert removed_containers == ["connector-test-fake"]
    assert result.stopped_early == StoppedEarly(
        reason="cap", records_seen=3, elapsed_s=result.stopped_early.elapsed_s
    )
    records = [
        json.loads(line) for line in result.stdout_file_path.read_bytes().splitlines()
    ]
    assert len(records) == 3
    assert all(
        record["record"]["data"]["id"].startswith("integer_len-1_")
        for record in records
    )


def test_without_a_policy_the_output_is_written_byte_for_byte(
    tmp_path: Path, fake_connector
) -> None:
    fixture = tmp_path / "fixture_stdout.jsonl"
    fixture.write_bytes(MASKABLE_STDOUT)
    fake_connector("cat", str(fixture), "0")

    result = _read_runner(tmp_path, mask_policy=None).run()

    assert result.stdout_file_path.read_bytes() == MASKABLE_STDOUT


# What the job log gets for a failed command, in either mode: a pointer, never
# the text.
FAILED_COMMAND_LINE = (
    "Command failed with exit code 1. See stderr.txt in the run artifacts"
)

# A crash as a connector prints it: a record value in the message, a blank
# line, a non-ASCII character, and a last line with no newline that ends
# inside a three-byte character.
CRASH_STDERR = (
    b"Traceback (most recent call last):\n"
    b'  File "main.py", line 3, in <module>\n'
    b"KeyError: 'alice@example.com'\n"
    b"\n"
    b"h\xc3\xa9llo \xe2\x82"
)


def test_a_masked_run_writes_each_stderr_line_as_its_length_only(
    tmp_path: Path, fake_connector, caplog: pytest.LogCaptureFixture
) -> None:
    """Same line count, same endings, nothing else; the job log points at the
    file instead of quoting it, so no crash text reaches the log either."""
    fixture = tmp_path / "fixture_stderr.txt"
    fixture.write_bytes(CRASH_STDERR)
    fake_connector("stderr", str(fixture), "1")

    with caplog.at_level(logging.WARNING):
        result = _read_runner(tmp_path, mask_policy=MaskPolicy(key=KEY)).run()

    assert result.exit_code == 1
    stderr = result.stderr_file_path.read_bytes()
    assert stderr == (
        b"masked_len-34\nmasked_len-37\nmasked_len-29\nmasked_len-0\nmasked_len-7"
    )
    assert len(stderr.splitlines()) == len(CRASH_STDERR.splitlines())
    assert FAILED_COMMAND_LINE in caplog.text
    assert "alice" not in caplog.text
    assert "Traceback" not in caplog.text


def test_a_stopped_masked_run_keeps_the_harness_note_readable(
    tmp_path: Path, fake_connector, removed_containers: list[str]
) -> None:
    fake_connector("records", "2", "60")

    result = _read_runner(
        tmp_path, timeout_seconds=1, mask_policy=MaskPolicy(key=KEY)
    ).run()

    assert removed_containers == ["connector-test-fake"]
    stderr = result.stderr_file_path.read_bytes()
    assert stderr.startswith(b"masked_len-13\n")
    assert b"done emitting" not in stderr
    assert b"Command timed out after 1 seconds" in stderr


def test_without_a_policy_stderr_is_written_byte_for_byte(
    tmp_path: Path, fake_connector
) -> None:
    fixture = tmp_path / "fixture_stderr.txt"
    fixture.write_bytes(CRASH_STDERR)
    fake_connector("stderr", str(fixture), "1")

    result = _read_runner(tmp_path, mask_policy=None).run()

    assert result.stderr_file_path.read_bytes() == CRASH_STDERR


def test_a_failed_raw_run_points_the_job_log_at_stderr_without_quoting_it(
    tmp_path: Path, fake_connector, caplog: pytest.LogCaptureFixture
) -> None:
    """The job log outlives the artifacts and nothing masks it, so a raw
    crash's text stays in `stderr.txt`, where the artifact's retention and
    the delete-on-pass apply."""
    fixture = tmp_path / "fixture_stderr.txt"
    fixture.write_bytes(CRASH_STDERR)
    fake_connector("stderr", str(fixture), "1")

    with caplog.at_level(logging.WARNING):
        result = _read_runner(tmp_path, mask_policy=None).run()

    assert result.exit_code == 1
    assert result.stderr_file_path.read_bytes() == CRASH_STDERR
    assert FAILED_COMMAND_LINE in caplog.text
    assert "alice" not in caplog.text
    assert "Traceback" not in caplog.text
    assert "Stderr:" not in caplog.text


def _artifacts_the_old_way(stdout: bytes) -> dict[str, bytes]:
    """The per-type files as the list-building `save_artifacts` wrote them."""
    by_type: dict[str, list[str]] = defaultdict(list)
    for line in stdout.decode().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            message = AirbyteMessage.parse_raw(line)
        except ValidationError:
            continue
        by_type[message.type.value.lower()].append(message.model_dump_json())
    return {
        f"{type_name}.jsonl": "\n".join(messages).encode()
        for type_name, messages in by_type.items()
    }


def test_save_artifacts_writes_the_same_files_in_one_streaming_pass(
    tmp_path: Path, fake_connector
) -> None:
    """Streaming the per-type files must not change a byte of them either."""
    fixture = tmp_path / "fixture_stdout.jsonl"
    fixture.write_bytes(FIXTURE_STDOUT)
    fake_connector("cat", str(fixture), "0")

    result = _read_runner(tmp_path).run()
    result.save_artifacts(tmp_path / "artifacts")

    written = {
        path.name: path.read_bytes()
        for path in (tmp_path / "artifacts" / "airbyte_messages").iterdir()
    }
    assert written == _artifacts_the_old_way(FIXTURE_STDOUT)
    assert set(written) == {"log.jsonl", "record.jsonl", "state.jsonl", "trace.jsonl"}
    assert result.get_message_count_per_type() == {
        AirbyteMessageType.LOG: 1,
        AirbyteMessageType.RECORD: 2,
        AirbyteMessageType.STATE: 1,
        AirbyteMessageType.TRACE: 1,
    }
    assert result.get_record_count_per_stream() == {"users": 2}
