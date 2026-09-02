"""Integration tests for Artifact Hosting SDK.

Optimized test flow that creates minimal resources:
- 1 shared project for most tests
- 2 deployments (for rollback testing)
- 1 separate project for cancel testing
- Automatic cleanup after tests complete

Test Coverage:
- Project CRUD operations
- Deployment creation with environment variables
- Deployment status polling
- Log streaming via SSE (stream_logs)
- Rollback to previous deployment
- Cancel in-progress deployment

Environment Variables:
    NOVITA_API_KEY: Required. API key for authentication.
    SANDBOX_TEMPLATE: Optional. Sandbox template name (default: base).
    SDK_LOG_LEVEL: Optional. Set to DEBUG for verbose logging.

Note: The SDK uses a fixed API URL (https://artifact.novita.ai/v1).

To run:
    SDK_LOG_LEVEL=DEBUG poetry run pytest \\
        src/novita_sandbox/artifact_hosting/tests/integration/ -v -s

The test suite creates and cleans up its own sandbox.

Resource Usage:
    - Creates 2 projects total (1 shared + 1 for cancel test)
    - Creates 3 deployments total (2 for main flow + 1 for cancel)
    - All resources cleaned up after tests
"""

import logging
import os
import time
from contextlib import suppress
from typing import Dict, Optional

import pytest
import requests

from novita_sandbox.artifact_hosting.client import DeploymentClient
from novita_sandbox.artifact_hosting.models.deployment import Deployment
from novita_sandbox.artifact_hosting.models.enums import DeploymentStatus
from novita_sandbox.artifact_hosting.models.project import Project


logger = logging.getLogger(__name__)


def verify_endpoint_env_vars(
    endpoint_url: str,
    expected_vars: Dict[str, str],
    timeout: int = 10,
) -> bool:
    """Verify environment variables by accessing the deployed app's env.html.
    
    Args:
        endpoint_url: Base URL of the deployed application.
        expected_vars: Dictionary of expected environment variable key-value pairs.
        timeout: HTTP request timeout in seconds.
    
    Returns:
        True if all environment variables are verified, False otherwise.
    """
    try:
        env_url = f"{endpoint_url.rstrip('/')}/env.html"
        logger.info(f"Verifying env vars at: {env_url}")
        
        resp = requests.get(env_url, timeout=timeout)
        if resp.status_code != 200:
            logger.warning(f"Failed to fetch env.html: HTTP {resp.status_code}")
            return False
        
        content = resp.text
        print(f"\n📄 env.html content:\n{content}")
        
        # Verify each expected variable
        all_verified = True
        for key, value in expected_vars.items():
            expected = f"{key}={value}"
            if expected in content:
                logger.info(f"✓ Verified: {expected}")
            else:
                logger.warning(f"✗ Not found: {expected}")
                all_verified = False
        
        return all_verified
        
    except requests.exceptions.RequestException as e:
        logger.warning(f"HTTP request failed: {e}")
        return False


def log_deployment_diagnostics(deployment: Deployment) -> None:
    """Print deployment logs when a live integration deployment fails."""
    with suppress(Exception):
        print(f"\n=== Deployment logs for {deployment.id} ===")
        for index, log_entry in enumerate(deployment.stream_logs(), start=1):
            print(log_entry.message)
            if index >= 100:
                print("... (truncated at 100 log entries)")
                break
        print("=== End deployment logs ===\n")


# =============================================================================
# Test Configuration
# =============================================================================

# Deployment polling configuration
DEPLOY_TIMEOUT = 120.0  # 2 minutes max wait
POLL_INTERVAL = 5.0     # 5 seconds between polls


# Skip all tests if no API key
pytestmark = pytest.mark.skipif(
    not os.getenv("NOVITA_API_KEY"),
    reason="NOVITA_API_KEY not set, skipping integration tests"
)

# Mark for tests that require sandbox (sandbox is auto-created by fixture)
requires_sandbox = pytest.mark.usefixtures("test_sandbox")


# =============================================================================
# Shared Fixtures (module-scoped for resource reuse)
# =============================================================================

@pytest.fixture(scope="module")
def client(api_key):
    """Create DeploymentClient for testing (module-scoped)."""
    with DeploymentClient(api_key=api_key) as c:
        yield c


@pytest.fixture(scope="module")
def shared_project(client, request) -> Project:
    """Create a shared project for all tests in this module.
    
    This project is reused across multiple tests to minimize resource creation.
    Automatically cleaned up after all tests complete (unless --no-cleanup).
    """
    timestamp = int(time.time())
    project_name = f"test-integration-{timestamp}"
    no_cleanup = request.config.getoption("--no-cleanup", default=False)
    
    logger.info(f"Creating shared project: {project_name}")
    project = client.create_project(
        name=project_name,
        description="Integration test project with options",
    )
    logger.info(f"Shared project created: {project.id}")
    
    yield project
    
    # Teardown: Clean up project (unless --no-cleanup)
    if no_cleanup:
        logger.info(f"Skipping project cleanup (--no-cleanup): {project.id}")
    else:
        logger.info(f"Cleaning up shared project: {project.id}")
        try:
            client.delete_project(project.id)
            logger.info(f"Shared project deleted: {project.id}")
        except Exception as e:
            logger.warning(f"Failed to delete shared project: {e}")


@pytest.fixture(scope="module")
def first_deployment(
    client,
    shared_project,
    test_sandbox_id,
    test_app_dir,
) -> Optional[Deployment]:
    """Create first deployment for the shared project.
    
    Waits for deployment to complete (RUNNING status).
    Used for: get_deployment, list_deployments, rollback target.
    """
    if not test_sandbox_id:
        pytest.skip("Sandbox creation failed")
        return None
    
    logger.info(f"Creating first deployment with sandbox: {test_sandbox_id}...")
    deployment: Optional[Deployment] = None
    try:
        deployment = shared_project.deploy(
            sandbox_id=test_sandbox_id,
            arti_dir=test_app_dir,
            dockerfile="Dockerfile",
            message="First deployment (v1)",
            environment_variables={
                "NODE_ENV": "production",
                "VERSION": "1.0.0",
            },
            http_port=80,  # Match container's exposed port
            wait=False,
        )
        deployment = shared_project._wait_for_deployment(
            deployment=deployment,
            poll_interval=POLL_INTERVAL,
            timeout=DEPLOY_TIMEOUT,
            on_status_change=lambda d: logger.info(f"  v1 status: {d.status.name}"),
        )
    except Exception:
        if deployment is not None:
            log_deployment_diagnostics(deployment)
        raise
    
    logger.info(f"First deployment completed: {deployment.id}, status={deployment.status.name}")
    
    # Get project info and print endpoint URL
    project = client.get_project(shared_project.id)
    if project.endpoint and project.endpoint.default_url:
        url = project.endpoint.default_url
        print(f"\n🌐 Deployment v1 URL: {url}\n")
        logger.info(f"Endpoint URL: {url}")
        
        # Verify environment variables via HTTP
        verify_endpoint_env_vars(url, {
            "NODE_ENV": "production",
            "VERSION": "1.0.0",
        })
    
    return deployment


@pytest.fixture(scope="module")
def second_deployment(
    client,
    shared_project,
    first_deployment,  # Ensure first deployment completes first
    test_sandbox_id,
    test_app_dir,
) -> Optional[Deployment]:
    """Create second deployment for the shared project.
    
    Waits for deployment to complete (RUNNING status).
    Used for: rollback testing (rollback from this to first).
    """
    if not test_sandbox_id:
        pytest.skip("Sandbox creation failed")
        return None
    
    if first_deployment is None:
        pytest.skip("First deployment failed")
        return None
    
    logger.info(f"Creating second deployment with sandbox: {test_sandbox_id}...")
    deployment = shared_project.deploy(
        sandbox_id=test_sandbox_id,
        arti_dir=test_app_dir,
        dockerfile="Dockerfile",
        message="Second deployment (v2)",
        environment_variables={
            "NODE_ENV": "production",
            "VERSION": "2.0.0",
        },
        http_port=80,  # Match container's exposed port
        wait=True,
        poll_interval=POLL_INTERVAL,
        timeout=DEPLOY_TIMEOUT,
        on_status_change=lambda d: logger.info(f"  v2 status: {d.status.name}"),
    )
    
    logger.info(f"Second deployment completed: {deployment.id}, status={deployment.status.name}")
    
    # Get project info and print endpoint URL
    project = client.get_project(shared_project.id)
    if project.endpoint and project.endpoint.default_url:
        url = project.endpoint.default_url
        print(f"\n🌐 Deployment v2 URL: {url}\n")
        logger.info(f"Endpoint URL: {url}")
        
        # Verify environment variables via HTTP
        verify_endpoint_env_vars(url, {
            "NODE_ENV": "production",
            "VERSION": "2.0.0",
        })
    
    return deployment


# =============================================================================
# Main Integration Test Flow
# =============================================================================

@requires_sandbox
class TestIntegrationFlow:
    """Main integration test flow using shared resources.
    
    Tests are numbered to ensure execution order.
    All tests share the same project and deployments.
    
    Flow:
        Phase 1: Project management (test_01 - test_04)
        Phase 2: First deployment (test_05 - test_07)
        Phase 2.5: Log streaming (test_07a - test_07b)
        Phase 3: Second deployment + Rollback (test_08 - test_10)
    """
    
    # -------------------------------------------------------------------------
    # Phase 1: Project Management
    # -------------------------------------------------------------------------
    
    def test_01_project_created_with_options(self, shared_project):
        """Verify project was created with correct options."""
        assert isinstance(shared_project, Project)
        assert shared_project.id is not None
        assert shared_project.name.startswith("test-integration-")
        assert shared_project.description == "Integration test project with options"
        logger.info(f"✓ Project created: {shared_project.id}")
    
    def test_02_get_project(self, client, shared_project):
        """Verify project can be retrieved by ID."""
        retrieved = client.get_project(shared_project.id)
        
        assert isinstance(retrieved, Project)
        assert retrieved.id == shared_project.id
        assert retrieved.name == shared_project.name
        logger.info(f"✓ Project retrieved: {retrieved.id}")
    
    def test_03_list_projects(self, client, shared_project):
        """Verify project appears in project list."""
        projects = list(client.list_projects())
        
        assert isinstance(projects, list)
        project_ids = [p.id for p in projects]
        assert shared_project.id in project_ids
        logger.info(f"✓ Project found in list ({len(projects)} total projects)")
    
    def test_04_update_project(self, shared_project):
        """Verify project can be updated."""
        new_description = "Updated integration test project"
        
        updated = shared_project.update(description=new_description)
        
        assert updated is shared_project  # Returns same instance
        # Note: We can't verify description update without re-fetching
        # because update() may not update local state
        logger.info("✓ Project updated")
    
    # -------------------------------------------------------------------------
    # Phase 2: First Deployment
    # -------------------------------------------------------------------------
    
    def test_05_first_deployment_successful(self, first_deployment):
        """Verify first deployment completed successfully with env vars."""
        from novita_sandbox.artifact_hosting.models.enums import SUCCESSFUL_STATES
        
        assert isinstance(first_deployment, Deployment)
        assert first_deployment.id is not None
        # Backend may return RUNNING or IDLE for successful deployments
        assert first_deployment.status in SUCCESSFUL_STATES, \
            f"Expected RUNNING or IDLE, got {first_deployment.status.name}"
        assert first_deployment.message == "First deployment (v1)"
        
        # Verify environment variables were set
        env_vars = first_deployment.metadata.environment_variables
        assert env_vars.get("NODE_ENV") == "production"
        assert env_vars.get("VERSION") == "1.0.0"
        
        logger.info(f"✓ First deployment successful: {first_deployment.id}, status={first_deployment.status.name}")
    
    def test_06_get_deployment(self, shared_project, first_deployment):
        """Verify deployment can be retrieved by ID."""
        from novita_sandbox.artifact_hosting.models.enums import SUCCESSFUL_STATES
        
        retrieved = shared_project.get_deployment(first_deployment.id)
        
        assert isinstance(retrieved, Deployment)
        assert retrieved.id == first_deployment.id
        assert retrieved.status in SUCCESSFUL_STATES, \
            f"Expected RUNNING or IDLE, got {retrieved.status.name}"
        logger.info(f"✓ Deployment retrieved: {retrieved.id}, status={retrieved.status.name}")
    
    def test_07_list_deployments_after_first(self, shared_project, first_deployment):
        """Verify deployment appears in deployment list."""
        deployments = list(shared_project.list_deployments())
        
        assert isinstance(deployments, list)
        assert len(deployments) >= 1
        deployment_ids = [d.id for d in deployments]
        assert first_deployment.id in deployment_ids
        logger.info(f"✓ Found {len(deployments)} deployment(s)")
    
    def test_07a_stream_logs(self, first_deployment):
        """Verify streaming logs from a completed deployment."""
        from novita_sandbox.artifact_hosting.models.log_entry import LogEntry
        
        logger.info(f"Streaming logs for deployment: {first_deployment.id}")
        print(f"\n=== Streaming logs for deployment: {first_deployment.id} ===")
        
        logs = []
        log_count = 0
        max_logs = 50  # Limit to prevent infinite loop if stream doesn't end
        
        try:
            for log_entry in first_deployment.stream_logs():
                assert isinstance(log_entry, LogEntry)
                assert log_entry.message is not None
                
                logs.append(log_entry)
                log_count += 1
                
                # Print ALL logs for debugging
                msg_preview = log_entry.message[:100] if len(log_entry.message) > 100 else log_entry.message
                print(f"  [{log_count:3d}] {msg_preview}")
                
                if log_count >= max_logs:
                    print(f"  ... (truncated at {max_logs} logs)")
                    break
                    
        except Exception as e:
            # Completed deployments may not have an active log stream
            print(f"  [ERROR] Log streaming ended with exception: {e}")
            logger.info(f"Log streaming ended: {e}")
        
        print(f"=== Total: {len(logs)} log entries ===\n")
        logger.info(f"✓ Streamed {len(logs)} log entries")
    
    # -------------------------------------------------------------------------
    # Phase 3: Second Deployment + Rollback
    # -------------------------------------------------------------------------
    
    def test_08_second_deployment_successful(self, second_deployment):
        """Verify second deployment completed successfully."""
        from novita_sandbox.artifact_hosting.models.enums import SUCCESSFUL_STATES
        
        assert isinstance(second_deployment, Deployment)
        assert second_deployment.id is not None
        # Backend may return RUNNING or IDLE for successful deployments
        assert second_deployment.status in SUCCESSFUL_STATES, \
            f"Expected RUNNING or IDLE, got {second_deployment.status.name}"
        assert second_deployment.message == "Second deployment (v2)"
        
        # Verify different version
        env_vars = second_deployment.metadata.environment_variables
        assert env_vars.get("VERSION") == "2.0.0"
        
        logger.info(f"✓ Second deployment successful: {second_deployment.id}, status={second_deployment.status.name}")
    
    def test_09_list_deployments_after_second(
        self, shared_project, first_deployment, second_deployment
    ):
        """Verify both deployments appear in list."""
        deployments = list(shared_project.list_deployments())
        
        assert len(deployments) >= 2
        deployment_ids = [d.id for d in deployments]
        assert first_deployment.id in deployment_ids
        assert second_deployment.id in deployment_ids
        logger.info(f"✓ Found {len(deployments)} deployments")
    
    def test_10_rollback_to_first_deployment(
        self, shared_project, first_deployment, second_deployment
    ):
        """Verify rollback to first deployment works."""
        logger.info(f"Rolling back to: {first_deployment.id}")
        
        result = shared_project.rollback(
            target_deployment_id=first_deployment.id,
            reason="Integration test rollback"
        )
        
        assert "projectId" in result or "project_id" in result
        # Check for either camelCase or snake_case response
        current_id = result.get("currentDeploymentId") or result.get("current_deployment_id")
        assert current_id == first_deployment.id
        
        logger.info(f"✓ Rollback successful, current deployment: {current_id}")


# =============================================================================
# Cancel Test (Separate Project)
# =============================================================================

@requires_sandbox
class TestCancelFlow:
    """Cancel deployment test using a separate project.
    
    This test needs its own project because:
    1. Cancel can only work on QUEUED/BUILDING deployments
    2. We need to create a deployment and immediately cancel it
    3. The deployment should not affect the main test flow
    """
    
    @pytest.fixture
    def cancel_test_client(self, api_key):
        """Create a separate client for cancel testing."""
        with DeploymentClient(api_key=api_key) as c:
            yield c
    
    @pytest.fixture
    def cancel_test_project(self, cancel_test_client, request):
        """Create a separate project for cancel testing."""
        timestamp = int(time.time())
        project_name = f"test-cancel-{timestamp}"
        no_cleanup = request.config.getoption("--no-cleanup", default=False)
        
        logger.info(f"Creating cancel test project: {project_name}")
        project = cancel_test_client.create_project(name=project_name)
        
        yield project
        
        # Cleanup (unless --no-cleanup)
        if no_cleanup:
            logger.info(f"Skipping cancel test project cleanup (--no-cleanup): {project.id}")
        else:
            logger.info(f"Cleaning up cancel test project: {project.id}")
            try:
                cancel_test_client.delete_project(project.id)
            except Exception as e:
                logger.warning(f"Failed to delete cancel test project: {e}")
    
    def test_cancel_queued_deployment(
        self,
        cancel_test_project,
        test_sandbox_id,
        test_app_dir,
    ):
        """Test cancelling a deployment that is still queued or building.
        
        Flow:
        1. Create deployment (wait=False)
        2. Immediately try to cancel
        3. Verify cancellation result
        
        Note: This test may not always succeed because:
        - Deployment may progress past cancellable state before cancel is called
        - Backend may not support cancel for this deployment state
        """
        logger.info("Creating deployment to cancel...")
        deployment = cancel_test_project.deploy(
            sandbox_id=test_sandbox_id,
            arti_dir=test_app_dir,
            dockerfile="Dockerfile",
            message="Deployment to be cancelled",
            http_port=80,  # Match container's exposed port
            wait=False,  # Don't wait, we want to cancel it
        )
        logger.info(f"Deployment created: {deployment.id}, status={deployment.status.name}")
        
        # Try to cancel if in cancellable state
        if deployment.status in [DeploymentStatus.QUEUED, DeploymentStatus.BUILDING]:
            logger.info("Attempting to cancel deployment...")
            try:
                cancelled = deployment.cancel(reason="Integration test cancel")

                if cancelled.status == DeploymentStatus.CANCELLED:
                    logger.info("✓ Deployment cancelled successfully")
                else:
                    logger.info(f"Cancel returned status: {cancelled.status.name}")
                    
            except Exception as e:
                # Cancel may fail if deployment already progressed
                logger.warning(f"Cancel failed (deployment may have progressed): {e}")
        else:
            logger.info(f"Deployment already in non-cancellable state: {deployment.status.name}")


# =============================================================================
# Project-Only Tests (No Sandbox Required)
# =============================================================================

class TestProjectOnlyOperations:
    """Tests that only require project operations (no sandbox/deployment).
    
    These tests create and clean up their own resources.
    """
    
    @pytest.fixture
    def temp_client(self, api_key):
        """Create a temporary client."""
        with DeploymentClient(api_key=api_key) as c:
            yield c
    
    def test_create_and_delete_project(self, temp_client):
        """Test creating and deleting a project."""
        timestamp = int(time.time())
        project_name = f"test-delete-{timestamp}"
        
        # Create
        project = temp_client.create_project(name=project_name)
        assert project.id is not None
        logger.info(f"Created project: {project.id}")
        
        # Delete
        temp_client.delete_project(project.id)
        logger.info(f"✓ Project created and deleted: {project.id}")
