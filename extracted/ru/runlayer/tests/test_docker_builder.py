"""Tests for Docker builder utility functions."""

from unittest.mock import MagicMock, patch
import pytest
import docker.errors

from runlayer_cli.deploy.docker_builder import (
    check_docker_available,
    build_image,
    tag_image,
    push_image,
    authenticate_ecr,
    DockerBuildError,
    get_registry_auth_config,
)
from runlayer_cli.api import ECRCredentials
import datetime


def test_check_docker_available_success():
    """Test that Docker availability check returns True when Docker is running."""
    with patch("runlayer_cli.deploy.docker_builder.docker") as mock_docker:
        mock_client = MagicMock()
        mock_client.ping.return_value = True
        mock_docker.from_env.return_value = mock_client

        result = check_docker_available()
        assert result is True
        mock_client.ping.assert_called_once()


def test_check_docker_available_failure():
    """Test that Docker availability check returns False when Docker is not available."""
    with patch("runlayer_cli.deploy.docker_builder.docker") as mock_docker:
        mock_docker.from_env.side_effect = docker.errors.DockerException(
            "Connection failed"
        )

        result = check_docker_available()
        assert result is False


def test_build_image_success():
    """Test successful Docker image build."""
    with (
        patch("runlayer_cli.deploy.docker_builder.docker") as mock_docker,
        patch("runlayer_cli.deploy.docker_builder.Path") as mock_path,
        patch("runlayer_cli.deploy.docker_builder.console") as mock_console,
    ):
        # Setup mocks
        mock_client = MagicMock()
        mock_docker.from_env.return_value = mock_client

        mock_context_path = MagicMock()
        mock_context_path.exists.return_value = True
        mock_context_path.__truediv__ = lambda self, other: MagicMock(
            exists=lambda: True
        )

        mock_path.return_value.resolve.return_value = mock_context_path

        # Mock build response
        build_chunks = [
            {"stream": "Step 1/5 : FROM python:3.10\n"},
            {"stream": "Step 2/5 : COPY . .\n"},
            {"aux": {"ID": "sha256:abc123def456"}},
        ]
        mock_client.api.build.return_value = iter(build_chunks)

        result = build_image(
            context=".",
            dockerfile="Dockerfile",
            tag="test-image:latest",
        )

        assert result == "sha256:abc123def456"
        mock_client.api.build.assert_called_once()


def test_build_image_with_target():
    """Test Docker image build with target parameter."""
    with (
        patch("runlayer_cli.deploy.docker_builder.docker") as mock_docker,
        patch("runlayer_cli.deploy.docker_builder.Path") as mock_path,
        patch("runlayer_cli.deploy.docker_builder.console") as mock_console,
    ):
        # Setup mocks
        mock_client = MagicMock()
        mock_docker.from_env.return_value = mock_client

        mock_context_path = MagicMock()
        mock_context_path.exists.return_value = True
        mock_context_path.__truediv__ = lambda self, other: MagicMock(
            exists=lambda: True
        )

        mock_path.return_value.resolve.return_value = mock_context_path

        # Mock build response
        build_chunks = [
            {"stream": "Step 1/5 : FROM python:3.10\n"},
            {"aux": {"ID": "sha256:abc123def456"}},
        ]
        mock_client.api.build.return_value = iter(build_chunks)

        result = build_image(
            context=".",
            dockerfile="Dockerfile",
            tag="test-image:latest",
            target="production",
        )

        assert result == "sha256:abc123def456"

        # Verify build was called with target parameter
        call_kwargs = mock_client.api.build.call_args[1]
        assert call_kwargs["target"] == "production"
        assert "ssh" not in call_kwargs


def test_build_image_context_not_found():
    """Test that missing build context raises DockerBuildError."""
    with patch("runlayer_cli.deploy.docker_builder.Path") as mock_path:
        mock_context_path = MagicMock()
        mock_context_path.exists.return_value = False
        mock_path.return_value.resolve.return_value = mock_context_path

        with pytest.raises(DockerBuildError) as exc_info:
            build_image(context="/nonexistent", dockerfile="Dockerfile", tag="test")
        assert "not found" in str(exc_info.value).lower()


def test_build_image_dockerfile_not_found():
    """Test that missing Dockerfile raises DockerBuildError."""
    with (
        patch("runlayer_cli.deploy.docker_builder.docker") as mock_docker,
        patch("runlayer_cli.deploy.docker_builder.Path") as mock_path,
    ):
        mock_client = MagicMock()
        mock_docker.from_env.return_value = mock_client

        mock_context_path = MagicMock()
        mock_context_path.exists.return_value = True

        # Mock Dockerfile path that doesn't exist
        mock_dockerfile_path = MagicMock()
        mock_dockerfile_path.exists.return_value = False
        mock_context_path.__truediv__ = lambda self, other: mock_dockerfile_path

        mock_path.return_value.resolve.return_value = mock_context_path

        with pytest.raises(DockerBuildError) as exc_info:
            build_image(context=".", dockerfile="Dockerfile", tag="test")
        assert (
            "dockerfile" in str(exc_info.value).lower()
            or "not found" in str(exc_info.value).lower()
        )


def test_tag_image_success():
    """Test successful image tagging."""
    with patch("runlayer_cli.deploy.docker_builder.docker") as mock_docker:
        mock_client = MagicMock()
        mock_docker.from_env.return_value = mock_client

        mock_image = MagicMock()
        mock_client.images.get.return_value = mock_image

        result = tag_image("sha256:abc123", "registry.example.com/repo", "v1.0.0")

        assert result == "registry.example.com/repo:v1.0.0"
        mock_image.tag.assert_called_once_with(
            "registry.example.com/repo", tag="v1.0.0"
        )


def test_push_image_success():
    """Test successful image push with digest return."""
    with (
        patch("runlayer_cli.deploy.docker_builder.docker") as mock_docker,
        patch("runlayer_cli.deploy.docker_builder.console") as mock_console,
    ):
        mock_client = MagicMock()
        mock_docker.from_env.return_value = mock_client

        # Mock push response with digest
        push_chunks = [
            {"status": "Pushing"},
            {"status": "Layer pushed"},
            {"aux": {"Digest": "sha256:def789ghi012"}},
        ]
        mock_client.images.push.return_value = iter(push_chunks)

        result = push_image("registry.example.com/repo:v1.0.0")

        assert result == "sha256:def789ghi012"
        mock_client.images.push.assert_called_once()


def test_push_image_uses_request_scoped_auth():
    """Push should forward explicit auth to a fresh Docker client."""
    auth_config = {
        "username": "AWS",
        "password": "test-password",
        "serveraddress": "123456789.dkr.ecr.us-east-1.amazonaws.com",
    }

    with (
        patch("runlayer_cli.deploy.docker_builder.docker") as mock_docker,
        patch("runlayer_cli.deploy.docker_builder.console"),
    ):
        mock_client = MagicMock()
        mock_docker.from_env.return_value = mock_client
        mock_client.images.push.return_value = iter(
            [{"aux": {"Digest": "sha256:def789ghi012"}}]
        )

        result = push_image(
            "123456789.dkr.ecr.us-east-1.amazonaws.com/my-repo:v1.0.0",
            auth_config=auth_config,
        )

        assert result == "sha256:def789ghi012"
        mock_client.images.push.assert_called_once_with(
            "123456789.dkr.ecr.us-east-1.amazonaws.com/my-repo:v1.0.0",
            stream=True,
            decode=True,
            auth_config=auth_config,
        )


def test_authenticate_ecr_success():
    """Test successful ECR authentication."""
    # Create valid credentials
    expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        hours=1
    )
    credentials = ECRCredentials(
        username="AWS",
        password="test-password",
        registry_url="https://123456789.dkr.ecr.us-east-1.amazonaws.com",
        repository_url="123456789.dkr.ecr.us-east-1.amazonaws.com/my-repo",
        expires_at=expires_at,
    )

    with (
        patch("subprocess.run") as mock_subprocess_run,
        patch("runlayer_cli.deploy.docker_builder.docker") as mock_docker,
        patch("runlayer_cli.deploy.docker_builder.console") as mock_console,
        patch("runlayer_cli.deploy.docker_builder.Progress") as mock_progress,
    ):
        mock_client = MagicMock()
        mock_docker.from_env.return_value = mock_client

        # Mock successful subprocess login
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_subprocess_run.return_value = mock_result

        # Mock Progress context manager
        mock_progress_instance = MagicMock()
        mock_progress_instance.__enter__ = MagicMock(
            return_value=mock_progress_instance
        )
        mock_progress_instance.__exit__ = MagicMock(return_value=False)
        mock_progress_instance.add_task = MagicMock(return_value="task-id")
        mock_progress_instance.update = MagicMock()
        mock_progress.return_value = mock_progress_instance

        authenticate_ecr(credentials)

        # Verify subprocess.run was called with correct arguments
        mock_subprocess_run.assert_called_once()
        call_args = mock_subprocess_run.call_args
        assert "docker" in call_args[0][0]
        assert "login" in call_args[0][0]


def test_get_registry_auth_config_normalizes_registry_url():
    """Auth config should use the hostname form Docker expects."""
    expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        hours=1
    )
    credentials = ECRCredentials(
        username="AWS",
        password="test-password",
        registry_url="https://123456789.dkr.ecr.us-east-1.amazonaws.com",
        repository_url="123456789.dkr.ecr.us-east-1.amazonaws.com/my-repo",
        expires_at=expires_at,
    )

    assert get_registry_auth_config(credentials) == {
        "username": "AWS",
        "password": "test-password",
        "serveraddress": "123456789.dkr.ecr.us-east-1.amazonaws.com",
    }


def test_authenticate_ecr_sdk_fallback_returns_auth_for_later_push():
    """SDK fallback should still return request-scoped auth for fresh clients."""
    expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        hours=1
    )
    credentials = ECRCredentials(
        username="AWS",
        password="test-password",
        registry_url="https://123456789.dkr.ecr.us-east-1.amazonaws.com",
        repository_url="123456789.dkr.ecr.us-east-1.amazonaws.com/my-repo",
        expires_at=expires_at,
    )

    with (
        patch("subprocess.run") as mock_subprocess_run,
        patch("runlayer_cli.deploy.docker_builder.docker") as mock_docker,
        patch("runlayer_cli.deploy.docker_builder.console"),
        patch("runlayer_cli.deploy.docker_builder.Progress") as mock_progress,
    ):
        mock_client = MagicMock()
        mock_docker.from_env.return_value = mock_client

        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = b"Error saving credentials: The stub received bad data"
        mock_result.stdout = b""
        mock_subprocess_run.return_value = mock_result

        mock_progress_instance = MagicMock()
        mock_progress_instance.__enter__ = MagicMock(
            return_value=mock_progress_instance
        )
        mock_progress_instance.__exit__ = MagicMock(return_value=False)
        mock_progress_instance.add_task = MagicMock(return_value="task-id")
        mock_progress_instance.update = MagicMock()
        mock_progress.return_value = mock_progress_instance

        auth_config = authenticate_ecr(credentials)

        assert auth_config == {
            "username": "AWS",
            "password": "test-password",
            "serveraddress": "123456789.dkr.ecr.us-east-1.amazonaws.com",
        }
        mock_client.login.assert_called_once_with(
            username="AWS",
            password="test-password",
            registry="123456789.dkr.ecr.us-east-1.amazonaws.com",
            reauth=True,
        )
