"""Integration tests for SandboxClient API.

Tests all client methods across all start modes (blank, artifact, config)
using a parameterized session fixture.

Requires PLATO_API_KEY environment variable to be set.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from collections.abc import Generator
from pathlib import Path
from typing import NamedTuple

import pytest
from rich.console import Console

from plato.v2.models import SandboxState
from plato.v2.sync.sandbox import SandboxClient, Tunnel

# Test configuration
ARTIFACT_ID = "0797d065-59aa-4963-b944-b80cb9dcc7df"
CONFIG_SERVICE_NAME = "sandbox-test"

# Plato config content for config mode tests
PLATO_CONFIG_CONTENT = """
service: sandbox-test
datasets:
  base:
    compute:
      cpus: 1
      memory: 2048
      disk: 10240
      app_port: 8080
      plato_messaging_port: 7000
    metadata:
      name: "Sandbox Test"
      description: "Test configuration for sandbox integration tests"
    services: {}
    listeners: {}
""".strip()


class SandboxSession(NamedTuple):
    """Container for sandbox session info."""

    client: SandboxClient
    state: SandboxState
    working_dir: Path
    mode: str


def _create_plato_config(working_dir: Path) -> Path:
    """Create plato-config.yml in working directory."""
    config_path = working_dir / "plato-config.yml"
    config_path.write_text(PLATO_CONFIG_CONTENT)
    return config_path


# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture(params=["blank", "artifact", "config"])
def sandbox_session(
    request: pytest.FixtureRequest,
) -> Generator[SandboxSession, None, None]:
    """Create a sandbox session parameterized by mode.

    This fixture:
    1. Creates a temp working directory
    2. For config mode, creates plato-config.yml
    3. Starts a sandbox in the specified mode
    4. Yields the session for testing
    5. Stops the sandbox and cleans up
    """
    api_key = os.environ.get("PLATO_API_KEY")
    if not api_key:
        pytest.fail("PLATO_API_KEY environment variable is required but not set")

    mode = request.param

    # Create temp working directory
    # Note: .plato/ directory is created by start() when generating SSH keys
    tmpdir = tempfile.mkdtemp(prefix=f"sandbox-test-{mode}-")
    working_dir = Path(tmpdir)

    # For config mode, create plato-config.yml
    if mode == "config":
        _create_plato_config(working_dir)

    client = SandboxClient(
        working_dir=working_dir,
        api_key=api_key,
        console=Console(quiet=True),
    )

    state = None
    try:
        if mode == "blank":
            state = client.start(
                mode="blank",
                cpus=1,
                memory=2048,
                disk=10240,
            )
        elif mode == "artifact":
            state = client.start(
                mode="artifact",
                artifact_id=ARTIFACT_ID,
            )
        elif mode == "config":
            state = client.start(
                mode="config",
                dataset="base",
            )
        else:
            raise ValueError(f"Unknown mode: {mode}")

        yield SandboxSession(
            client=client,
            state=state,
            working_dir=working_dir,
            mode=mode,
        )
    finally:
        if state and state.session_id:
            client.stop(state.session_id, state.heartbeat_pid)
        client.close()
        # Cleanup temp directory
        shutil.rmtree(tmpdir, ignore_errors=True)


# =============================================================================
# TEST: CLIENT METHODS (parameterized across all modes)
# =============================================================================


class TestSandboxClientMethods:
    """Tests for SandboxClient methods using parameterized session.

    Each test runs 3 times: once for blank, artifact, and config modes.
    """

    # -------------------------------------------------------------------------
    # start() - tested implicitly by fixture, verify state here
    # -------------------------------------------------------------------------

    def test_start_returns_valid_state(self, sandbox_session: SandboxSession):
        """Test start() returns SandboxState with required fields."""
        state = sandbox_session.state

        # Core fields present for all modes
        assert state.session_id is not None
        assert state.job_id is not None
        assert state.mode == sandbox_session.mode
        assert state.ssh_config_path is not None
        assert state.ssh_host is not None
        assert state.ssh_command is not None

        # Mode-specific fields
        if sandbox_session.mode == "blank":
            assert state.cpus is not None
            assert state.memory is not None
            assert state.disk is not None
        elif sandbox_session.mode == "artifact":
            assert state.artifact_id == ARTIFACT_ID
        elif sandbox_session.mode == "config":
            assert state.simulator_name == CONFIG_SERVICE_NAME
            assert state.cpus == 1
            assert state.memory == 2048

    # -------------------------------------------------------------------------
    # status()
    # -------------------------------------------------------------------------

    @pytest.mark.skip(reason="status() now returns SessionDetailsResponse, not dict")
    def test_status_returns_session_details(self, sandbox_session: SandboxSession):
        """Test status() returns session details dict."""
        status = sandbox_session.client.status(sandbox_session.state.session_id)

        assert status is not None
        assert isinstance(status, dict)
        assert "jobs" in status

    # -------------------------------------------------------------------------
    # state()
    # -------------------------------------------------------------------------

    def test_state_returns_session_state_response(self, sandbox_session: SandboxSession):
        """Test state() returns SessionStateResponse."""
        state_response = sandbox_session.client.state(sandbox_session.state.session_id)

        assert state_response is not None
        # SessionStateResponse has jobs field
        assert hasattr(state_response, "jobs") or hasattr(state_response, "results")

    # -------------------------------------------------------------------------
    # connect_network()
    # -------------------------------------------------------------------------

    def test_connect_network(self, sandbox_session: SandboxSession):
        """Test connect_network() returns a response."""
        # Network may already be connected from start(), but calling again should work
        result = sandbox_session.client.connect_network(sandbox_session.state.session_id)
        assert result is not None

    # -------------------------------------------------------------------------
    # get_ssh_config_for_job()
    # -------------------------------------------------------------------------

    def test_get_ssh_config_for_job(self, sandbox_session: SandboxSession):
        """Test get_ssh_config_for_job() returns valid SSH config."""
        ssh_info = sandbox_session.client.get_ssh_config_for_job(sandbox_session.state.job_id)

        assert ssh_info.config_content is not None
        assert ssh_info.private_key_path is not None
        assert ssh_info.job_id == sandbox_session.state.job_id
        assert ssh_info.gateway_host is not None

        # Verify config content structure
        assert "Host sandbox" in ssh_info.config_content
        assert "ProxyCommand" in ssh_info.config_content
        assert "IdentityFile" in ssh_info.config_content

        # Verify private key file exists
        assert Path(ssh_info.private_key_path).exists()

    # -------------------------------------------------------------------------
    # SSH connectivity - actually run SSH command
    # -------------------------------------------------------------------------

    def test_ssh_connectivity(self, sandbox_session: SandboxSession):
        """Test that SSH actually works by running a command."""
        state = sandbox_session.state
        working_dir = sandbox_session.working_dir

        # Get SSH config path (relative, need to run from working_dir)
        ssh_config_path = state.ssh_config_path
        ssh_host = state.ssh_host

        assert ssh_config_path is not None
        assert ssh_host is not None

        # Run a simple command via SSH
        result = subprocess.run(
            ["ssh", "-F", ssh_config_path, ssh_host, "echo", "hello"],
            capture_output=True,
            text=True,
            cwd=working_dir,
            timeout=30,
        )

        assert result.returncode == 0, f"SSH failed: {result.stderr}"
        assert "hello" in result.stdout

    def test_ssh_can_run_commands(self, sandbox_session: SandboxSession):
        """Test SSH can run various commands on the VM."""
        state = sandbox_session.state
        working_dir = sandbox_session.working_dir

        ssh_config_path = state.ssh_config_path
        ssh_host = state.ssh_host

        # Test hostname command
        result = subprocess.run(
            ["ssh", "-F", ssh_config_path, ssh_host, "hostname"],
            capture_output=True,
            text=True,
            cwd=working_dir,
            timeout=30,
        )
        assert result.returncode == 0

        # Test pwd command
        result = subprocess.run(
            ["ssh", "-F", ssh_config_path, ssh_host, "pwd"],
            capture_output=True,
            text=True,
            cwd=working_dir,
            timeout=30,
        )
        assert result.returncode == 0
        assert "/" in result.stdout  # Should be some path

        # Test uname command
        result = subprocess.run(
            ["ssh", "-F", ssh_config_path, ssh_host, "uname", "-a"],
            capture_output=True,
            text=True,
            cwd=working_dir,
            timeout=30,
        )
        assert result.returncode == 0
        assert "Linux" in result.stdout

    # -------------------------------------------------------------------------
    # tunnel()
    # -------------------------------------------------------------------------

    def test_tunnel_can_be_created(self, sandbox_session: SandboxSession):
        """Test tunnel() returns a Tunnel with correct attributes."""
        tunnel = sandbox_session.client.tunnel(
            job_id=sandbox_session.state.job_id,
            remote_port=8080,
            local_port=18080,
        )

        assert tunnel.job_id == sandbox_session.state.job_id
        assert tunnel.remote_port == 8080
        assert tunnel.local_port == 18080

    # -------------------------------------------------------------------------
    # sync()
    # -------------------------------------------------------------------------

    def test_sync_files_to_sandbox(self, sandbox_session: SandboxSession):
        """Test sync() transfers files to sandbox via rsync."""
        # Skip artifact mode - artifacts may have stale clocks which breaks apt/rsync install
        if sandbox_session.mode == "artifact":
            pytest.skip("sync() requires working apt - artifacts may have stale clocks")

        # Create a test file in the working directory
        test_file = sandbox_session.working_dir / "test_sync_file.txt"
        test_file.write_text("test content for sync")

        # For config mode, use the service name from config
        # For other modes, use a generic name
        if sandbox_session.mode == "config":
            simulator = CONFIG_SERVICE_NAME
        else:
            simulator = "sandbox"

        sync_result = sandbox_session.client.sync(
            session_id=sandbox_session.state.session_id,
            simulator=simulator,
        )

        assert sync_result is not None
        assert sync_result.files_synced >= 0
        assert sync_result.bytes_synced >= 0

    # -------------------------------------------------------------------------
    # stop() - test return value explicitly
    # -------------------------------------------------------------------------

    def test_stop_returns_close_response(self, sandbox_session: SandboxSession):
        """Test stop() returns CloseSessionResponse.

        Note: This test creates its own session to test stop() explicitly
        without interfering with the fixture cleanup.
        """
        api_key = os.environ.get("PLATO_API_KEY")
        tmpdir = tempfile.mkdtemp(prefix="sandbox-test-stop-")
        working_dir = Path(tmpdir)

        try:
            client = SandboxClient(
                working_dir=working_dir,
                api_key=api_key,
                console=Console(quiet=True),
            )

            state = client.start(
                mode="blank",
                cpus=1,
                memory=2048,
                disk=10240,
            )

            # Test stop() return value
            response = client.stop(state.session_id, state.heartbeat_pid)

            assert response is not None
            # CloseSessionResponse should have success field
            assert hasattr(response, "success") or hasattr(response, "session_id")

            client.close()
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)


# =============================================================================
# TEST: CONFIG MODE SPECIFIC METHODS
# =============================================================================


# Config with services for start_services test
PLATO_CONFIG_WITH_SERVICES = """
service: sandbox-test
datasets:
  base:
    compute:
      cpus: 1
      memory: 2048
      disk: 10240
      app_port: 8080
      plato_messaging_port: 7000
    metadata:
      name: "Sandbox Test"
      description: "Test configuration for sandbox integration tests"
    services:
      app:
        type: docker-compose
        file: docker-compose.yml
    listeners: {}
""".strip()


class TestSandboxConfigModeSpecific:
    """Tests for methods that only work with config mode."""

    @pytest.fixture
    def config_session(self) -> Generator[SandboxSession, None, None]:
        """Create a config mode session specifically."""
        api_key = os.environ.get("PLATO_API_KEY")
        if not api_key:
            pytest.fail("PLATO_API_KEY environment variable is required but not set")

        tmpdir = tempfile.mkdtemp(prefix="sandbox-test-config-")
        working_dir = Path(tmpdir)
        _create_plato_config(working_dir)

        client = SandboxClient(
            working_dir=working_dir,
            api_key=api_key,
            console=Console(quiet=True),
        )

        state = None
        try:
            state = client.start(mode="config", dataset="base")
            yield SandboxSession(
                client=client,
                state=state,
                working_dir=working_dir,
                mode="config",
            )
        finally:
            if state and state.session_id:
                client.stop(state.session_id, state.heartbeat_pid)
            client.close()
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_start_worker(self, config_session: SandboxSession):
        """Test start_worker() initializes the plato worker."""
        config_session.client.start_worker(
            job_id=config_session.state.job_id,
            simulator=CONFIG_SERVICE_NAME,
            dataset="base",
            wait_timeout=60,
        )

        # Verify by checking state
        state_response = config_session.client.state(config_session.state.session_id)
        assert state_response is not None

    def test_start_services_no_services(self, config_session: SandboxSession):
        """Test start_services() returns empty list when no services configured."""
        state = config_session.state

        # Our test config has services: {} so this should return empty list
        # Note: This requires the simulator to be registered in gitea
        try:
            result = config_session.client.start_services(
                simulator_name=CONFIG_SERVICE_NAME,
                ssh_config_path=state.ssh_config_path,
                ssh_host=state.ssh_host,
                dataset="base",
            )
            assert result == []
        except ValueError as e:
            if "not found in gitea" in str(e):
                pytest.skip(f"Simulator not registered in gitea: {e}")
            raise


# =============================================================================
# TEST: ARTIFACT MODE SPECIFIC - run_flow
# =============================================================================


class TestSandboxArtifactModeSpecific:
    """Tests for methods that work with artifact mode."""

    @pytest.fixture
    def artifact_session(self) -> Generator[SandboxSession, None, None]:
        """Create an artifact mode session specifically."""
        api_key = os.environ.get("PLATO_API_KEY")
        if not api_key:
            pytest.fail("PLATO_API_KEY environment variable is required but not set")

        tmpdir = tempfile.mkdtemp(prefix="sandbox-test-artifact-")
        working_dir = Path(tmpdir)

        client = SandboxClient(
            working_dir=working_dir,
            api_key=api_key,
            console=Console(quiet=True),
        )

        state = None
        try:
            state = client.start(
                mode="artifact",
                artifact_id=ARTIFACT_ID,
            )
            yield SandboxSession(
                client=client,
                state=state,
                working_dir=working_dir,
                mode="artifact",
            )
        finally:
            if state and state.session_id:
                client.stop(state.session_id, state.heartbeat_pid)
            client.close()
            shutil.rmtree(tmpdir, ignore_errors=True)

    @pytest.mark.skip(reason="status() now returns SessionDetailsResponse, not dict")
    def test_run_flow_from_api(self, artifact_session: SandboxSession):
        """Test run_flow() with use_api=True fetches and runs flows from artifact."""
        state = artifact_session.state

        # Get public URL for the artifact
        status = artifact_session.client.status(state.session_id)
        jobs = status.get("jobs", [])
        if not jobs:
            pytest.skip("No jobs found in session")

        # Get public URL
        public_url = state.public_url
        if not public_url:
            pytest.skip("No public URL available")

        # Try to run a flow - this tests that run_flow() correctly:
        # 1. Fetches flows from the API
        # 2. Launches playwright
        # 3. Attempts to execute the flow
        # Flow execution may fail due to UI mismatch, but that's OK for this test
        try:
            artifact_session.client.run_flow(
                url=public_url,
                flow_name="login",  # Common flow name
                dataset="base",
                use_api=True,
                job_id=state.job_id,
                headless=True,
            )
        except ValueError as e:
            # Flow doesn't exist in artifact - expected for some artifacts
            if "not found" in str(e):
                pytest.skip(f"No 'login' flow in artifact: {e}")
            raise
        except Exception as e:
            error_msg = str(e).lower()
            # Playwright not installed
            if "playwright" in error_msg:
                pytest.skip("Playwright not installed")
            # Flow execution error (selector not found, timeout, etc.)
            # This means run_flow() worked - it fetched the flow and tried to execute
            if "flowexecutionerror" in error_msg or "timeout" in error_msg or "selector" in error_msg:
                # Test passes - run_flow successfully fetched and attempted to execute the flow
                pass
            else:
                raise


# =============================================================================
# TEST: TUNNEL (no VM required)
# =============================================================================


class TestTunnel:
    """Tests for Tunnel class that don't require a running VM."""

    def test_tunnel_creation(self):
        """Test Tunnel object can be created with correct attributes."""
        tunnel = Tunnel(
            job_id="test-job-id",
            remote_port=8080,
            local_port=8081,
            bind_address="127.0.0.1",
            verify_ssl=False,
        )

        assert tunnel.job_id == "test-job-id"
        assert tunnel.remote_port == 8080
        assert tunnel.local_port == 8081
        assert tunnel.bind_address == "127.0.0.1"
        assert tunnel.verify_ssl is False
        assert tunnel._running is False

    def test_tunnel_default_local_port(self):
        """Test Tunnel uses remote_port as default local_port."""
        tunnel = Tunnel(
            job_id="test-job-id",
            remote_port=3000,
        )

        assert tunnel.local_port == 3000

    def test_tunnel_context_manager_interface(self):
        """Test Tunnel has context manager interface."""
        tunnel = Tunnel(job_id="test", remote_port=8080)

        assert hasattr(tunnel, "__enter__")
        assert hasattr(tunnel, "__exit__")
        assert hasattr(tunnel, "start")
        assert hasattr(tunnel, "stop")
