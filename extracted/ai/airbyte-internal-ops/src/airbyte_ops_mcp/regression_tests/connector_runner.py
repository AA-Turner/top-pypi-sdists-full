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


class ConnectorRunner:
    """Runs Airbyte connector commands using Docker.

    This class manages the execution of connector commands (spec, check, discover, read)
    in Docker containers without using Dagger.
    """

    DATA_DIR = "/data"
    CONFIG_FILE = "config.json"
    CATALOG_FILE = "catalog.json"
    STATE_FILE = "state.json"

    def __init__(
        self,
        execution_inputs: ExecutionInputs,
        timeout_seconds: int = 14400,  # 4 hours
        proxy_url: str | None = None,
    ) -> None:
        """Initialize the connector runner.

        Args:
            execution_inputs: The inputs for executing the connector command.
            timeout_seconds: Maximum time to wait for command execution.
            proxy_url: Optional HTTP proxy URL for capturing HTTP traffic.
                       When set, HTTP_PROXY and HTTPS_PROXY env vars are configured.
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
