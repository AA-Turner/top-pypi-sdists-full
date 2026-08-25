# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for the Docker-based connector runner."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from airbyte_ops_mcp.regression_tests import connector_runner as connector_runner_module
from airbyte_ops_mcp.regression_tests.connector_runner import ConnectorRunner
from airbyte_ops_mcp.regression_tests.models import (
    Command,
    ConnectorUnderTest,
    ExecutionInputs,
    TargetOrControl,
)

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
        if value.startswith(("REQUESTS_CA_BUNDLE=", "SSL_CERT_FILE="))
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
