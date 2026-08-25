# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Docker-based connector runner for live tests.

This module provides a connector runner that uses Docker SDK directly
instead of Dagger for container orchestration.
"""

from __future__ import annotations

import json
import logging
import subprocess
import tempfile
import uuid
from pathlib import Path
from typing import TYPE_CHECKING

from airbyte_ops_mcp.regression_tests.models import (
    Command,
    ExecutionInputs,
    ExecutionResult,
)

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

CERTIFI_DISCOVERY_TIMEOUT_SECONDS = 60
CONTAINER_REMOVAL_TIMEOUT_SECONDS = 30

# Prints the bundle's path on the first line and its contents on the rest, so
# one container start answers both "where is it" and "what is already in it".
_CERTIFI_PROBE = "\n".join(
    (
        "import certifi",
        "path = certifi.where()",
        "print(path)",
        "print(open(path).read(), end='')",
    )
)


def _force_remove_container(container_name: str) -> None:
    """Remove a container `subprocess` could only orphan.

    A `subprocess.run` timeout kills the `docker` CLI, not the container it
    started, and `--rm` only fires when the container itself exits.
    """
    try:
        subprocess.run(
            ["docker", "rm", "-f", container_name],
            capture_output=True,
            timeout=CONTAINER_REMOVAL_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        logger.debug(f"Could not remove container {container_name}: {exc}")


# Successful probes only. Caching a *failure* would let one transient Docker
# hiccup silently downgrade HTTPS trust for every later container in the run,
# and a probe is one short container start -- cheap enough to retry.
_CERTIFI_BUNDLES: dict[str, tuple[str, str]] = {}


def _discover_certifi_bundle(image_name: str) -> tuple[str, str] | None:
    """The `certifi` bundle inside a connector image: where it is and what it holds.

    `REQUESTS_CA_BUNDLE` and `SSL_CERT_FILE` cover `requests` and stdlib `ssl`,
    but a client that pins `certifi.where()` directly -- `httpx` does -- ignores
    both, so that file has to be replaced on disk. Its current contents come back
    with it so the replacement can *extend* the image's roots rather than drop
    them; see `ConnectorRunner._trust_bundle`.

    Best-effort by design: an image without Python or without `certifi` simply
    gets no bundle override. Successful answers are cached, since they only
    depend on the image; failures are not, so a transient Docker error costs one
    retry rather than the rest of the run's HTTPS trust. That retry must not
    reach a single run's two consumers separately -- see
    `ConnectorRunner._image_certifi_bundle`.

    Returns:
        The bundle's absolute path inside the image and its contents, or `None`
        when the image has none.
    """
    cached = _CERTIFI_BUNDLES.get(image_name)
    if cached is not None:
        return cached

    container_name = f"certifi-probe-{uuid.uuid4().hex[:8]}"
    try:
        result = subprocess.run(
            [
                "docker",
                "run",
                "--rm",
                "--name",
                container_name,
                "--entrypoint",
                "python",
                image_name,
                "-c",
                _CERTIFI_PROBE,
            ],
            capture_output=True,
            text=True,
            timeout=CERTIFI_DISCOVERY_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        _force_remove_container(container_name)
        logger.debug(f"Could not read the certifi bundle in {image_name}: {exc}")
        return None
    except (OSError, subprocess.SubprocessError) as exc:
        # Everything here degrades: a broken Docker socket must not be the
        # difference between a regression test running and not running.
        logger.debug(f"Could not read the certifi bundle in {image_name}: {exc}")
        return None

    path, _, contents = result.stdout.partition("\n")
    path = path.strip()
    if result.returncode != 0 or not path.startswith("/") or not contents.strip():
        logger.debug(
            f"Image {image_name} has no usable certifi bundle "
            f"(exit {result.returncode})"
        )
        return None

    _CERTIFI_BUNDLES[image_name] = (path, contents)
    return path, contents


class ConnectorRunner:
    """Runs Airbyte connector commands using Docker.

    This class manages the execution of connector commands (spec, check, discover, read)
    in Docker containers without using Dagger.
    """

    DATA_DIR = "/data"
    CONFIG_FILE = "config.json"
    CATALOG_FILE = "catalog.json"
    STATE_FILE = "state.json"
    CA_CERT_FILE = "mitmproxy-ca.pem"

    def __init__(
        self,
        execution_inputs: ExecutionInputs,
        timeout_seconds: int = 14400,  # 4 hours
        proxy_url: str | None = None,
        ca_cert_path: Path | None = None,
    ) -> None:
        """Initialize the connector runner.

        Args:
            execution_inputs: The inputs for executing the connector command.
            timeout_seconds: Maximum time to wait for command execution.
            proxy_url: Optional HTTP proxy URL for capturing HTTP traffic.
                       When set, HTTP_PROXY and HTTPS_PROXY env vars are configured.
            ca_cert_path: Path to the proxy's CA certificate on the host. Only
                          used together with `proxy_url`: without it every HTTPS
                          request through the proxy fails TLS verification, which
                          shows up as a near-empty traffic capture rather than as
                          an error.
        """
        self.connector_under_test = execution_inputs.connector_under_test
        self.command = execution_inputs.command
        self.output_dir = execution_inputs.output_dir
        self.config = execution_inputs.config
        self.configured_catalog = execution_inputs.configured_catalog
        self.state = execution_inputs.state
        self.environment_variables = execution_inputs.environment_variables or {}
        self.timeout_seconds = timeout_seconds
        self.proxy_url = proxy_url
        self.ca_cert_path = ca_cert_path
        # Resolved once per runner, and shared by the two decisions that must
        # never disagree: `_trust_bundle`, which decides whether the file it
        # writes extends the image's roots or holds the proxy CA alone, and
        # `_build_docker_command`, which decides whether to mount that file over
        # the image's certifi bundle. Probing independently would let a failed
        # probe followed by a successful one mount a CA-only bundle over the
        # image's roots -- TLS failures on every non-proxied connection, reading
        # as a regression in the version under test.
        self._certifi_bundle: tuple[str, str] | None = None
        self._certifi_bundle_probed = False

        self.logger = logging.getLogger(
            f"{self.connector_under_test.name}-{self.connector_under_test.version}"
        )

    def _get_airbyte_command(self) -> list[str]:
        """Get the Airbyte protocol command arguments."""
        if self.command == Command.SPEC:
            return ["spec"]
        elif self.command == Command.CHECK:
            return ["check", "--config", f"{self.DATA_DIR}/{self.CONFIG_FILE}"]
        elif self.command == Command.DISCOVER:
            return ["discover", "--config", f"{self.DATA_DIR}/{self.CONFIG_FILE}"]
        elif self.command == Command.READ:
            return [
                "read",
                "--config",
                f"{self.DATA_DIR}/{self.CONFIG_FILE}",
                "--catalog",
                f"{self.DATA_DIR}/{self.CATALOG_FILE}",
            ]
        elif self.command == Command.READ_WITH_STATE:
            return [
                "read",
                "--config",
                f"{self.DATA_DIR}/{self.CONFIG_FILE}",
                "--catalog",
                f"{self.DATA_DIR}/{self.CATALOG_FILE}",
                "--state",
                f"{self.DATA_DIR}/{self.STATE_FILE}",
            ]
        else:
            raise ValueError(f"Unknown command: {self.command}")

    def _prepare_data_directory(self, temp_dir: Path) -> None:
        """Prepare the data directory with config, catalog, and state files.

        Args:
            temp_dir: Temporary directory to write files to.
        """
        if self.config is not None:
            config_path = temp_dir / self.CONFIG_FILE
            config_path.write_text(json.dumps(self.config))
            config_path.chmod(0o666)
            self.logger.debug(f"Wrote config to {config_path}")

        if self.configured_catalog is not None:
            catalog_path = temp_dir / self.CATALOG_FILE
            catalog_path.write_text(self.configured_catalog.json())
            catalog_path.chmod(0o666)
            self.logger.debug(f"Wrote catalog to {catalog_path}")

        if self.state is not None:
            state_path = temp_dir / self.STATE_FILE
            state_path.write_text(json.dumps(self.state))
            state_path.chmod(0o666)
            self.logger.debug(f"Wrote state to {state_path}")

        if self._trusts_proxy_ca:
            ca_path = temp_dir / self.CA_CERT_FILE
            ca_path.write_text(self._trust_bundle())
            # World-readable: connector images run as their own non-root user.
            ca_path.chmod(0o644)
            self.logger.debug(f"Wrote the trust bundle to {ca_path}")

    @property
    def _trusts_proxy_ca(self) -> bool:
        """Whether the container should be made to trust the proxy's CA."""
        return bool(self.proxy_url and self.ca_cert_path)

    def _image_certifi_bundle(self) -> tuple[str, str] | None:
        """The image's certifi bundle, probed at most once for this runner."""
        if not self._certifi_bundle_probed:
            self._certifi_bundle = _discover_certifi_bundle(
                self.connector_under_test.image_name
            )
            self._certifi_bundle_probed = True

        return self._certifi_bundle

    def _trust_bundle(self) -> str:
        """The proxy's CA appended to the image's own roots, never replacing them.

        Pointing the container's trust store at the proxy CA *alone* would work
        for everything that goes through the proxy and break everything that
        does not: a client honouring `NO_PROXY`, a vendored SDK that builds its
        own session, any non-HTTP TLS. That failure surfaces as a TLS error
        inside the connector under test -- indistinguishable, to a reviewer,
        from a regression in the version being tested.
        """
        assert self.ca_cert_path is not None
        ca_pem = self.ca_cert_path.read_text()

        bundle = self._image_certifi_bundle()
        if bundle is None:
            return ca_pem

        _path, contents = bundle
        return contents.rstrip("\n") + "\n" + ca_pem

    def _build_docker_command(self, temp_dir: Path) -> list[str]:
        """Build the docker run command.

        Args:
            temp_dir: Temporary directory containing data files.

        Returns:
            List of command arguments for subprocess.
        """
        container_name = f"connector-test-{uuid.uuid4().hex[:8]}"

        cmd = [
            "docker",
            "run",
            "--rm",
            "--name",
            container_name,
            "-v",
            f"{temp_dir}:{self.DATA_DIR}",
            # Override the container's WORKDIR to /tmp so that relative file
            # writes (e.g. bulk GraphQL result files in source-shopify) land
            # in a directory writable by the non-root `airbyte` user (UID 1000).
            # The image entrypoint uses an absolute path, and Python imports
            # resolve via sys.path, so changing CWD is safe.
            "-w",
            "/tmp",
        ]

        if self.proxy_url:
            cmd.extend(["--add-host", "host.docker.internal:host-gateway"])

        for key, value in self.environment_variables.items():
            cmd.extend(["-e", f"{key}={value}"])

        if self.proxy_url:
            cmd.extend(["-e", f"HTTP_PROXY={self.proxy_url}"])
            cmd.extend(["-e", f"HTTPS_PROXY={self.proxy_url}"])
            cmd.extend(["-e", f"http_proxy={self.proxy_url}"])
            cmd.extend(["-e", f"https_proxy={self.proxy_url}"])

        if self._trusts_proxy_ca:
            # `_prepare_data_directory` puts the trust bundle in the mounted
            # data dir.
            host_bundle_path = temp_dir / self.CA_CERT_FILE
            container_ca_path = f"{self.DATA_DIR}/{self.CA_CERT_FILE}"
            # `requests` (most of the Python CDK) and stdlib `ssl` / `aiohttp`,
            # which pick it up through `load_default_certs()`.
            cmd.extend(["-e", f"REQUESTS_CA_BUNDLE={container_ca_path}"])
            cmd.extend(["-e", f"SSL_CERT_FILE={container_ca_path}"])

            # The same answer `_trust_bundle` wrote the file from: mounting a
            # CA-only bundle over the image's roots is the regression this
            # sharing prevents.
            bundle = self._image_certifi_bundle()
            if bundle is not None:
                certifi_path, _contents = bundle
                cmd.extend(["-v", f"{host_bundle_path}:{certifi_path}:ro"])
            else:
                # Not fatal -- the env vars still cover `requests` and stdlib
                # `ssl` -- but on a JVM image nothing above covers anything, and
                # the resulting TLS failures read as a connector bug.
                self.logger.warning(
                    f"No certifi bundle found in "
                    f"{self.connector_under_test.image_name}; clients that pin "
                    "certifi will not trust the capture proxy. Java connectors "
                    "need a JKS truststore and are not supported."
                )

        cmd.append(self.connector_under_test.image_name)
        cmd.extend(self._get_airbyte_command())

        return cmd

    def run(self) -> ExecutionResult:
        """Execute the connector command and return the result.

        Returns:
            ExecutionResult containing stdout, stderr, and success status.
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)

        stdout_path = self.output_dir / "stdout.txt"
        stderr_path = self.output_dir / "stderr.txt"

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            # Make temp directory world-writable so non-root container users can read/write
            # Many connector images run as non-root users (e.g., 'airbyte' user) with
            # different UIDs than the host user, so they need write access for config migration
            temp_path.chmod(0o777)
            self._prepare_data_directory(temp_path)

            docker_cmd = self._build_docker_command(temp_path)
            self.logger.info(f"Running command: {' '.join(docker_cmd)}")

            try:
                result = subprocess.run(
                    docker_cmd,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout_seconds,
                )

                stdout_path.write_text(result.stdout)
                stderr_path.write_text(result.stderr)

                success = result.returncode == 0
                exit_code = result.returncode

                if not success:
                    self.logger.warning(
                        f"Command failed with exit code {exit_code}. "
                        f"Stderr: {result.stderr[:500]}"
                    )
                else:
                    self.logger.info("Command completed successfully")

            except subprocess.TimeoutExpired as e:
                self.logger.error(f"Command timed out after {self.timeout_seconds}s")
                stdout_path.write_text(e.stdout or "" if hasattr(e, "stdout") else "")
                stderr_path.write_text(
                    f"Command timed out after {self.timeout_seconds} seconds"
                )
                success = False
                exit_code = -1

            except FileNotFoundError:
                self.logger.error("Docker not found. Is Docker installed and running?")
                stdout_path.write_text("")
                stderr_path.write_text(
                    "Docker not found. Is Docker installed and running?"
                )
                success = False
                exit_code = -1

        return ExecutionResult(
            connector_under_test=self.connector_under_test,
            command=self.command,
            stdout_file_path=stdout_path,
            stderr_file_path=stderr_path,
            success=success,
            exit_code=exit_code,
            configured_catalog=self.configured_catalog,
            config=self.config,
        )


def pull_connector_image(image_name: str) -> bool:
    """Pull a connector image from Docker Hub.

    Args:
        image_name: Full image name with tag (e.g., airbyte/source-github:1.0.0).

    Returns:
        True if pull succeeded, False otherwise.
    """
    logger.info(f"Pulling image: {image_name}")
    try:
        result = subprocess.run(
            ["docker", "pull", image_name],
            capture_output=True,
            text=True,
            timeout=600,
        )
        if result.returncode == 0:
            logger.info(f"Successfully pulled {image_name}")
            return True
        else:
            logger.error(f"Failed to pull {image_name}: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        logger.error(f"Timeout pulling {image_name}")
        return False
    except FileNotFoundError:
        logger.error("Docker not found")
        return False


def image_exists_locally(image_name: str) -> bool:
    """Check if a Docker image exists locally.

    Args:
        image_name: Full image name with tag.

    Returns:
        True if image exists locally, False otherwise.
    """
    try:
        result = subprocess.run(
            ["docker", "image", "inspect", image_name],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def ensure_image_available(image_name: str) -> bool:
    """Ensure a Docker image is available locally, pulling if necessary.

    Args:
        image_name: Full image name with tag.

    Returns:
        True if image is available, False otherwise.
    """
    if image_exists_locally(image_name):
        logger.info(f"Image {image_name} already exists locally")
        return True
    return pull_connector_image(image_name)
