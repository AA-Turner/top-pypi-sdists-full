"""Tests for deploy service orchestration functions."""

from unittest.mock import MagicMock, patch
from contextlib import contextmanager
import pytest
import tempfile
from pathlib import Path
import typer

from runlayer_cli.deploy.service import (
    _get_or_create_deployment,
    _build_docker_image,
    _push_to_ecr,
    _update_deployment_config,
    _extract_validation_error,
    _trigger_and_monitor_deployment,
    _validate_runlayer_yaml_config,
    _create_backup_path,
    validate_service,
    deploy_service,
    init_deployment_config,
    destroy_deployment,
    pull_deployment,
)
from runlayer_cli.deploy.schema_validation import validate_deploy_yaml_keys
from runlayer_cli.api import (
    RunlayerClient,
    DeploymentPublic,
    ECRCredentials,
    ValidateYAMLResponse,
)
import datetime
import httpx
import yaml


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    return MagicMock(spec=RunlayerClient)


@pytest.fixture
def sample_config():
    """Sample deployment configuration."""
    return {
        "name": "test-service",
        "runtime": "docker",
        "build": {
            "dockerfile": "Dockerfile",
            "context": ".",
            "platform": "x86",
        },
        "service": {"port": 8000},
    }


@pytest.fixture
def mock_deployment():
    """Create a mock deployment."""
    deployment = MagicMock(spec=DeploymentPublic)
    deployment.id = "test-deployment-id"
    deployment.name = "test-service"
    deployment.deletion_status = None
    deployment.connected_servers = []
    deployment.created_at = datetime.datetime.now(datetime.timezone.utc)
    return deployment


@pytest.fixture
def mock_validation_response():
    """Create a successful validation response."""
    return ValidateYAMLResponse(
        valid=True,
        error=None,
        parsed_config={},
    )


@pytest.fixture
def temp_config_file():
    """Create a temporary config file and clean it up after test."""
    files = []

    def _create(config: dict) -> str:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(config, f)
            path = f.name
            files.append(path)
            return path

    yield _create

    # Cleanup
    for path in files:
        Path(path).unlink(missing_ok=True)


@contextmanager
def mock_deploy_dependencies(mock_api_client, config, skip_docker_check=False):
    """Context manager for common deploy_service patches."""
    with (
        patch("runlayer_cli.deploy.service.RunlayerClient") as mock_client_class,
        patch("runlayer_cli.deploy.service.load_config") as mock_load_config,
        patch("runlayer_cli.deploy.service.load_config_raw") as mock_load_raw,
        patch(
            "runlayer_cli.deploy.service.check_docker_available"
        ) as mock_docker_check,
        patch("runlayer_cli.deploy.service._build_docker_image") as mock_build,
        patch("runlayer_cli.deploy.service._push_to_ecr") as mock_push,
        patch("runlayer_cli.deploy.service.typer.echo"),
        patch("runlayer_cli.deploy.service.typer.secho"),
    ):
        mock_client_class.return_value = mock_api_client
        mock_load_config.return_value = config
        mock_load_raw.return_value = yaml.dump(config)
        mock_docker_check.return_value = not skip_docker_check

        yield {
            "client_class": mock_client_class,
            "load_config": mock_load_config,
            "load_raw": mock_load_raw,
            "docker_check": mock_docker_check,
            "build": mock_build,
            "push": mock_push,
        }


def test_get_or_create_deployment_existing(mock_api_client, sample_config):
    """Test using existing deployment ID."""
    deployment_id = "existing-deployment-id"
    sample_config["id"] = deployment_id

    mock_deployment = MagicMock(spec=DeploymentPublic)
    mock_deployment.id = deployment_id
    mock_deployment.name = "test-service"
    mock_deployment.deletion_status = None
    mock_api_client.get_deployment.return_value = mock_deployment

    result = _get_or_create_deployment(
        mock_api_client, sample_config, "test-config.yaml"
    )

    assert result == deployment_id
    mock_api_client.get_deployment.assert_called_once_with(deployment_id)
    mock_api_client.create_deployment.assert_not_called()


def test_get_or_create_deployment_new(mock_api_client, sample_config):
    """Test creating new deployment when ID is missing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        import yaml

        yaml.dump(sample_config, f)
        config_path = f.name

    try:
        mock_deployment = MagicMock(spec=DeploymentPublic)
        mock_deployment.id = "new-deployment-id"
        mock_api_client.create_deployment.return_value = mock_deployment

        with patch("runlayer_cli.deploy.service.update_config_id") as mock_update:
            result = _get_or_create_deployment(
                mock_api_client, sample_config, config_path
            )

            assert result == "new-deployment-id"
            mock_api_client.create_deployment.assert_called_once_with("test-service")
            mock_update.assert_called_once_with(config_path, "new-deployment-id")
    finally:
        Path(config_path).unlink()


def test_get_or_create_deployment_deleted_status(mock_api_client, sample_config):
    """Test that deleted deployment is rejected."""
    deployment_id = "deleted-deployment-id"
    sample_config["id"] = deployment_id

    mock_deployment = MagicMock(spec=DeploymentPublic)
    mock_deployment.id = deployment_id
    mock_deployment.deletion_status = "deleted"
    mock_api_client.get_deployment.return_value = mock_deployment

    with pytest.raises(typer.Exit):
        _get_or_create_deployment(mock_api_client, sample_config, "test-config.yaml")


def test_build_docker_image_success(sample_config):
    """Test successful Docker image build with platform config."""
    deployment_id = "test-deployment-id"

    with (
        patch("runlayer_cli.deploy.service.build_image") as mock_build,
        patch("runlayer_cli.deploy.service.typer"),
    ):
        mock_build.return_value = "sha256:abc123def456"

        result = _build_docker_image(sample_config, deployment_id)

        assert result == "sha256:abc123def456"
        mock_build.assert_called_once()
        call_kwargs = mock_build.call_args[1]
        assert call_kwargs["tag"] == f"runlayer-build:{deployment_id}"
        assert call_kwargs["platform"] == "linux/amd64"


def test_push_to_ecr_success(mock_api_client):
    """Test successful push to ECR and return digest URI."""
    image_id = "sha256:abc123"
    deployment_id = "test-deployment-id"

    expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        hours=1
    )
    ecr_creds = ECRCredentials(
        username="AWS",
        password="test-password",
        registry_url="https://123456789.dkr.ecr.us-east-1.amazonaws.com",
        repository_url="123456789.dkr.ecr.us-east-1.amazonaws.com/my-repo",
        expires_at=expires_at,
    )
    mock_api_client.get_ecr_credentials.return_value = ecr_creds

    with (
        patch("runlayer_cli.deploy.service.authenticate_ecr") as mock_auth,
        patch("runlayer_cli.deploy.service.tag_image") as mock_tag,
        patch("runlayer_cli.deploy.service.push_image") as mock_push,
        patch("runlayer_cli.deploy.service.typer"),
    ):
        mock_auth.return_value = {
            "username": "AWS",
            "password": "test-password",
            "serveraddress": "123456789.dkr.ecr.us-east-1.amazonaws.com",
        }
        mock_tag.return_value = (
            "123456789.dkr.ecr.us-east-1.amazonaws.com/my-repo:test-deployment-id"
        )
        mock_push.return_value = "sha256:def789ghi012"

        result = _push_to_ecr(mock_api_client, image_id, deployment_id)

        expected_uri = (
            "123456789.dkr.ecr.us-east-1.amazonaws.com/my-repo@sha256:def789ghi012"
        )
        assert result == expected_uri
        mock_auth.assert_called_once()
        mock_tag.assert_called_once()
        mock_push.assert_called_once_with(
            "123456789.dkr.ecr.us-east-1.amazonaws.com/my-repo:test-deployment-id",
            auth_config=mock_auth.return_value,
        )


def test_update_deployment_config_success(mock_api_client):
    """Test successful deployment configuration update."""
    deployment_id = "test-deployment-id"
    image_uri = "repo@sha256:abc123"
    yaml_content = "name: test-service\nruntime: docker\n"

    mock_deployment = MagicMock(spec=DeploymentPublic)
    mock_api_client.update_deployment.return_value = mock_deployment

    with patch("runlayer_cli.deploy.service.typer"):
        _update_deployment_config(
            mock_api_client, deployment_id, image_uri, yaml_content
        )

        mock_api_client.update_deployment.assert_called_once_with(
            deployment_id,
            yaml_content=yaml_content,
            docker_image=image_uri,
        )


def test_init_deployment_config_success():
    """Test successful deployment initialization."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "runlayer.yaml"

        mock_deployment = MagicMock(spec=DeploymentPublic)
        mock_deployment.id = "new-deployment-id"
        mock_deployment.template_yaml = "name: test-service\nruntime: docker\n"

        with (
            patch("runlayer_cli.deploy.service.RunlayerClient") as mock_client_class,
            patch("runlayer_cli.deploy.service.typer"),
        ):
            mock_client = MagicMock()
            mock_client.create_deployment.return_value = mock_deployment
            mock_client_class.return_value = mock_client

            init_deployment_config(
                name="test-service",
                config_path=str(config_path),
                secret="test-secret",
                host="http://localhost:3000",
            )

            mock_client.create_deployment.assert_called_once_with("test-service")
            assert config_path.exists()
            assert "test-service" in config_path.read_text()


def test_init_deployment_config_invalid_name():
    """Test that invalid deployment name is rejected."""
    with patch("runlayer_cli.deploy.service.typer.echo"):
        with pytest.raises(typer.Exit) as exc_info:
            init_deployment_config(
                name="Invalid Name With Spaces!",
                config_path="runlayer.yaml",
                secret="test-secret",
                host="http://localhost:3000",
            )

        assert exc_info.value.exit_code == 1


def test_destroy_deployment_success(mock_api_client):
    """Test successful deployment destruction."""
    deployment_id = "test-deployment-id"

    mock_deployment = MagicMock(spec=DeploymentPublic)
    mock_deployment.id = deployment_id
    mock_deployment.name = "test-service"
    mock_deployment.created_at = datetime.datetime.now(datetime.timezone.utc)
    mock_deployment.deletion_status = None
    mock_deployment.connected_servers = []

    with (
        patch("runlayer_cli.deploy.service.RunlayerClient") as mock_client_class,
        patch("runlayer_cli.deploy.service.load_config") as mock_load,
        patch("runlayer_cli.deploy.service.typer.confirm") as mock_confirm,
        patch("runlayer_cli.deploy.service.typer.echo"),
        patch("runlayer_cli.deploy.service.typer.secho"),
    ):
        mock_client = MagicMock()
        mock_client.get_deployment.return_value = mock_deployment
        mock_client_class.return_value = mock_client

        mock_load.return_value = {"id": deployment_id}
        mock_confirm.return_value = True

        destroy_deployment(
            config_path="runlayer.yaml",
            secret="test-secret",
            host="http://localhost:3000",
            deployment_id=deployment_id,
        )

        mock_client.delete_deployment.assert_called_once_with(deployment_id)


def test_destroy_deployment_already_deleted(mock_api_client):
    """Test handling of already deleted deployment."""
    deployment_id = "deleted-deployment-id"

    mock_deployment = MagicMock(spec=DeploymentPublic)
    mock_deployment.id = deployment_id
    mock_deployment.name = "test-service"
    mock_deployment.created_at = datetime.datetime.now(datetime.timezone.utc)
    mock_deployment.deletion_status = "deleted"

    with (
        patch("runlayer_cli.deploy.service.RunlayerClient") as mock_client_class,
        patch("runlayer_cli.deploy.service.typer.echo"),
        patch("runlayer_cli.deploy.service.typer.secho"),
    ):
        mock_client = MagicMock()
        mock_client.get_deployment.return_value = mock_deployment
        mock_client_class.return_value = mock_client

        with pytest.raises(typer.Exit) as exc_info:
            destroy_deployment(
                config_path="runlayer.yaml",
                secret="test-secret",
                host="http://localhost:3000",
                deployment_id=deployment_id,
            )

        assert exc_info.value.exit_code == 0
        mock_client.delete_deployment.assert_not_called()


def test_extract_validation_error_from_422():
    """Test error extraction from 422 HTTP status error."""
    # Create a mock HTTPStatusError with 422 status
    mock_response = MagicMock()
    mock_response.status_code = 422
    mock_response.json.return_value = {
        "detail": "Configuration error: service.port is required"
    }
    mock_response.text = ""

    error = httpx.HTTPStatusError(
        message="422 Unprocessable Entity",
        request=MagicMock(),
        response=mock_response,
    )

    result = _extract_validation_error(error)
    assert result == "Configuration error: service.port is required"


def test_extract_validation_error_from_422_no_detail():
    """Test error extraction from 422 when detail field is missing."""
    mock_response = MagicMock()
    mock_response.status_code = 422
    mock_response.json.return_value = {"error": "Something went wrong"}
    mock_response.text = ""

    error = httpx.HTTPStatusError(
        message="422 Unprocessable Entity",
        request=MagicMock(),
        response=mock_response,
    )

    result = _extract_validation_error(error)
    assert "error" in result.lower() or "something" in result.lower()


def test_extract_validation_error_from_non_422():
    """Test error extraction from non-422 HTTP errors."""
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"

    error = httpx.HTTPStatusError(
        message="500 Internal Server Error",
        request=MagicMock(),
        response=mock_response,
    )

    result = _extract_validation_error(error)
    assert "500" in result
    assert "Internal Server Error" in result


def test_extract_validation_error_from_non_422_detail():
    """Test error extraction from non-422 HTTP errors with backend detail."""
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.json.return_value = {
        "detail": "Cannot trigger deployment while a deployment is in progress."
    }
    mock_response.text = ""

    error = httpx.HTTPStatusError(
        message="400 Bad Request",
        request=MagicMock(),
        response=mock_response,
    )

    result = _extract_validation_error(error)
    assert result == "Cannot trigger deployment while a deployment is in progress."


def test_extract_validation_error_from_non_422_json_without_detail():
    """Test non-422 JSON without detail keeps HTTP status context."""
    mock_response = MagicMock()
    mock_response.status_code = 409
    mock_response.json.return_value = {"message": "locked"}
    mock_response.text = '{"message":"locked"}'

    error = httpx.HTTPStatusError(
        message="409 Conflict",
        request=MagicMock(),
        response=mock_response,
    )

    result = _extract_validation_error(error)
    assert result == 'HTTP 409: {"message":"locked"}'


def test_extract_validation_error_generic():
    """Test error extraction from generic exceptions."""
    error = ValueError("Something went wrong")
    result = _extract_validation_error(error)
    assert result == "Something went wrong"


def test_validate_runlayer_yaml_config_success(mock_api_client):
    """Test successful YAML validation."""
    yaml_content = "name: test-service\nruntime: docker\nservice:\n  port: 8000\n"

    mock_response = ValidateYAMLResponse(
        valid=True,
        error=None,
        parsed_config={"name": "test-service"},
    )
    mock_api_client.validate_yaml.return_value = mock_response

    with (
        patch("runlayer_cli.deploy.service.typer.echo") as _mock_echo,
        patch("runlayer_cli.deploy.service.typer.secho") as mock_secho,
    ):
        _validate_runlayer_yaml_config(mock_api_client, yaml_content)

        mock_api_client.validate_yaml.assert_called_once_with(yaml_content)
        mock_secho.assert_called()
        # Check that success message was shown
        calls = [str(call) for call in mock_secho.call_args_list]
        assert any("valid" in str(call).lower() for call in calls)


def test_validate_runlayer_yaml_config_invalid(mock_api_client):
    """Test YAML validation with invalid configuration."""
    yaml_content = "invalid: yaml"

    mock_response = ValidateYAMLResponse(
        valid=False,
        error="Configuration error: service.port is required",
        parsed_config=None,
    )
    mock_api_client.validate_yaml.return_value = mock_response

    with (
        patch("runlayer_cli.deploy.service.typer.echo") as _mock_echo,
        patch("runlayer_cli.deploy.service.typer.secho") as _mock_secho,
    ):
        with pytest.raises(typer.Exit) as exc_info:
            _validate_runlayer_yaml_config(mock_api_client, yaml_content)

        assert exc_info.value.exit_code == 1
        mock_api_client.validate_yaml.assert_called_once_with(yaml_content)


def test_validate_runlayer_yaml_config_http_error(mock_api_client):
    """Test YAML validation with HTTP error."""
    yaml_content = "name: test-service\nruntime: docker\n"

    mock_response = MagicMock()
    mock_response.status_code = 422
    mock_response.json.return_value = {"detail": "Validation failed"}
    mock_response.text = ""

    http_error = httpx.HTTPStatusError(
        message="422 Unprocessable Entity",
        request=MagicMock(),
        response=mock_response,
    )
    mock_api_client.validate_yaml.side_effect = http_error

    with (
        patch("runlayer_cli.deploy.service.typer.echo") as _mock_echo,
        patch("runlayer_cli.deploy.service.typer.secho") as _mock_secho,
    ):
        with pytest.raises(typer.Exit) as exc_info:
            _validate_runlayer_yaml_config(mock_api_client, yaml_content)

        assert exc_info.value.exit_code == 1


def test_validate_runlayer_yaml_config_shows_backend_env_limit_error(mock_api_client):
    """Test backend env limit error is surfaced unchanged."""
    yaml_content = "name: test-service\nruntime: docker\nservice:\n  port: 8000\n"

    mock_response = ValidateYAMLResponse(
        valid=False,
        error="Configuration error: env.API_KEY is too long (2001 chars, max 2000)",
        parsed_config=None,
    )
    mock_api_client.validate_yaml.return_value = mock_response

    with (
        patch("runlayer_cli.deploy.service.typer.echo") as _mock_echo,
        patch("runlayer_cli.deploy.service.typer.secho") as mock_secho,
    ):
        with pytest.raises(typer.Exit) as exc_info:
            _validate_runlayer_yaml_config(mock_api_client, yaml_content)

        assert exc_info.value.exit_code == 1
        rendered_calls = [str(call) for call in mock_secho.call_args_list]
        assert any("env.API_KEY is too long" in call for call in rendered_calls)


def test_trigger_and_monitor_deployment_shows_backend_trigger_detail(mock_api_client):
    """Test trigger failure surfaces backend detail."""
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.json.return_value = {
        "detail": "Cannot trigger deployment while a deployment is in progress."
    }
    mock_response.text = ""

    http_error = httpx.HTTPStatusError(
        message="400 Bad Request",
        request=MagicMock(),
        response=mock_response,
    )
    mock_api_client.trigger_deployment.side_effect = http_error

    with (
        patch("runlayer_cli.deploy.service.typer.echo"),
        patch("runlayer_cli.deploy.service.typer.secho") as mock_secho,
    ):
        with pytest.raises(typer.Exit) as exc_info:
            _trigger_and_monitor_deployment(
                mock_api_client,
                "test-deployment-id",
            )

        assert exc_info.value.exit_code == 1
        rendered_calls = [str(call) for call in mock_secho.call_args_list]
        assert any(
            "Cannot trigger deployment while a deployment is in progress."
            in call
            for call in rendered_calls
        )


def test_validate_service_success():
    """Test successful validation service call."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        config = {
            "name": "test-service",
            "runtime": "docker",
            "service": {"port": 8000},
        }
        yaml.dump(config, f)
        config_path = f.name

    try:
        mock_response = ValidateYAMLResponse(
            valid=True,
            error=None,
            parsed_config=config,
        )

        with (
            patch("runlayer_cli.deploy.service.RunlayerClient") as mock_client_class,
            patch("runlayer_cli.deploy.service.typer.echo") as _mock_echo,
            patch("runlayer_cli.deploy.service.typer.secho") as _mock_secho,
        ):
            mock_client = MagicMock()
            mock_client.validate_yaml.return_value = mock_response
            mock_client_class.return_value = mock_client

            validate_service(
                config_path=config_path,
                secret="test-secret",
                host="http://localhost:3000",
            )

            mock_client.validate_yaml.assert_called_once()
    finally:
        Path(config_path).unlink()


def test_validate_service_invalid_yaml():
    """Test validation service with invalid YAML."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write("invalid: yaml: content")
        config_path = f.name

    try:
        mock_response = ValidateYAMLResponse(
            valid=False,
            error="Configuration error: service.port is required",
            parsed_config=None,
        )

        with (
            patch("runlayer_cli.deploy.service.RunlayerClient") as mock_client_class,
            patch("runlayer_cli.deploy.service.typer.echo") as _mock_echo,
            patch("runlayer_cli.deploy.service.typer.secho") as _mock_secho,
        ):
            mock_client = MagicMock()
            mock_client.validate_yaml.return_value = mock_response
            mock_client_class.return_value = mock_client

            with pytest.raises(typer.Exit) as exc_info:
                validate_service(
                    config_path=config_path,
                    secret="test-secret",
                    host="http://localhost:3000",
                )

            assert exc_info.value.exit_code == 1
    finally:
        Path(config_path).unlink()


def test_validate_deploy_yaml_keys_rejects_unknown_top_level_key():
    yaml_content = """
name: test-service
runtime: docker
image: repo.example.com/app:latest
service:
  port: 8000
environment:
  API_KEY: secret
"""

    with pytest.raises(ValueError) as exc_info:
        validate_deploy_yaml_keys(yaml_content)

    error = str(exc_info.value)
    assert "Unsupported runlayer.yaml key: environment" in error
    assert "Allowed keys here:" in error
    assert "env" in error


def test_validate_deploy_yaml_keys_rejects_unknown_nested_key():
    yaml_content = """
name: test-service
runtime: docker
image: repo.example.com/app:latest
service:
  port: 8000
  environment:
    API_KEY: secret
"""

    with pytest.raises(ValueError) as exc_info:
        validate_deploy_yaml_keys(yaml_content)

    error = str(exc_info.value)
    assert "Unsupported runlayer.yaml key: service.environment" in error
    assert "Allowed keys here: port, path, expose" in error


def test_validate_deploy_yaml_keys_allows_env_and_build_args_keys():
    yaml_content = """
name: test-service
runtime: docker
build:
  platform: ${BUILD_PLATFORM:-x86}
  args:
    API_KEY: secret
service:
  port: ${PORT}
env:
  ENVIRONMNT: typo-but-user-owned-env-var-name
"""

    validate_deploy_yaml_keys(yaml_content)


def test_validate_service_rejects_unknown_key_before_substitution():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(
            """
name: test-service
runtime: docker
image: repo.example.com/app:latest
service:
  port: 8000
environment:
  API_KEY: ${API_KEY}
"""
        )
        config_path = f.name

    try:
        with (
            patch("runlayer_cli.deploy.service.RunlayerClient") as mock_client_class,
            patch("runlayer_cli.deploy.service.substitute_env_vars") as mock_substitute,
            patch("runlayer_cli.deploy.service.typer.echo"),
            patch("runlayer_cli.deploy.service.typer.secho") as mock_secho,
        ):
            with pytest.raises(typer.Exit) as exc_info:
                validate_service(
                    config_path=config_path,
                    secret="test-secret",
                    host="http://localhost:3000",
                )

            assert exc_info.value.exit_code == 1
            mock_client_class.assert_not_called()
            mock_substitute.assert_not_called()
            rendered_calls = [str(call) for call in mock_secho.call_args_list]
            assert any(
                "Unsupported runlayer.yaml key: environment" in call
                for call in rendered_calls
            )
    finally:
        Path(config_path).unlink()


def test_deploy_service_rejects_unknown_key_before_substitution(sample_config):
    bad_config = {
        **sample_config,
        "environment": {"API_KEY": "${API_KEY}"},
    }

    with (
        patch("runlayer_cli.deploy.service.load_config") as mock_load_config,
        patch("runlayer_cli.deploy.service.load_config_raw") as mock_load_raw,
        patch("runlayer_cli.deploy.service.RunlayerClient") as mock_client_class,
        patch("runlayer_cli.deploy.service.substitute_env_vars") as mock_substitute,
        patch("runlayer_cli.deploy.service.typer.echo"),
        patch("runlayer_cli.deploy.service.typer.secho") as mock_secho,
    ):
        mock_load_config.return_value = bad_config
        mock_load_raw.return_value = yaml.dump(bad_config)

        with pytest.raises(typer.Exit) as exc_info:
            deploy_service(
                config_path="runlayer.yaml",
                secret="test-secret",
                host="http://localhost:3000",
            )

        assert exc_info.value.exit_code == 1
        mock_client_class.assert_not_called()
        mock_substitute.assert_not_called()
        rendered_calls = [str(call) for call in mock_secho.call_args_list]
        assert any(
            "Unsupported runlayer.yaml key: environment" in call
            for call in rendered_calls
        )


def test_deploy_service_validates_early(mock_api_client, sample_config):
    """Test that deploy_service validates configuration before Docker build."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(sample_config, f)
        config_path = f.name

    try:
        mock_response = ValidateYAMLResponse(
            valid=True,
            error=None,
            parsed_config=sample_config,
        )
        mock_api_client.validate_yaml.return_value = mock_response

        mock_deployment = MagicMock(spec=DeploymentPublic)
        mock_deployment.id = "test-deployment-id"
        mock_deployment.name = "test-service"
        mock_deployment.deletion_status = None
        mock_api_client.get_deployment.return_value = mock_deployment

        with (
            patch("runlayer_cli.deploy.service.RunlayerClient") as mock_client_class,
            patch("runlayer_cli.deploy.service.load_config") as mock_load_config,
            patch("runlayer_cli.deploy.service.load_config_raw") as mock_load_raw,
            patch(
                "runlayer_cli.deploy.service.check_docker_available"
            ) as mock_docker_check,
            patch("runlayer_cli.deploy.service.typer") as _mock_typer,
        ):
            mock_client_class.return_value = mock_api_client
            mock_load_config.return_value = sample_config
            mock_load_raw.return_value = yaml.dump(sample_config)
            mock_docker_check.return_value = True

            # This should call validate_yaml before Docker build
            # We'll just verify the call order by checking validate_yaml was called
            # Since we're mocking everything, we expect it to fail at Docker build
            # but validation should have been called first
            try:
                deploy_service(
                    config_path=config_path,
                    secret="test-secret",
                    host="http://localhost:3000",
                )
            except (typer.Exit, AttributeError, TypeError):
                # Expected to fail at some point, but validation should have been called
                pass

            # Verify validation was called
            mock_api_client.validate_yaml.assert_called_once()
    finally:
        Path(config_path).unlink()


def test_deploy_service_image_mode_skips_docker_build(
    mock_api_client, mock_deployment, mock_validation_response, temp_config_file
):
    """Test that when image field is in config, Docker build/push are skipped."""
    config_with_image = {
        "id": "existing-deployment-id",
        "name": "test-service",
        "runtime": "docker",
        "image": "my-registry.example.com/my-app:v1.0.0",
        "service": {"port": 8000},
    }

    config_path = temp_config_file(config_with_image)

    # Setup mock API client
    mock_api_client.validate_yaml.return_value = mock_validation_response
    mock_api_client.get_deployment.return_value = mock_deployment
    mock_api_client.update_deployment.return_value = mock_deployment

    trigger_response = MagicMock()
    trigger_response.history_id = "history-123"
    mock_api_client.trigger_deployment.return_value = trigger_response
    mock_api_client.get_deployment_status.return_value = {"status": "completed"}
    mock_api_client.get_deployment_logs.return_value = ""

    with mock_deploy_dependencies(mock_api_client, config_with_image) as mocks:
        deploy_service(
            config_path=config_path,
            secret="test-secret",
            host="http://localhost:3000",
        )

        # Verify Docker availability check was NOT called
        mocks["docker_check"].assert_not_called()
        # Verify build and push were NOT called
        mocks["build"].assert_not_called()
        mocks["push"].assert_not_called()
        # Verify update was called with docker_image=None (backend will use YAML image field)
        mock_api_client.update_deployment.assert_called_once()
        call_kwargs = mock_api_client.update_deployment.call_args[1]
        assert call_kwargs["docker_image"] is None


def test_deploy_service_build_mode_calls_docker_build(
    mock_api_client, mock_deployment, mock_validation_response, temp_config_file
):
    """Test that when no image field is in config, Docker build/push are called."""
    config_without_image = {
        "id": "existing-deployment-id",
        "name": "test-service",
        "runtime": "docker",
        "build": {
            "dockerfile": "Dockerfile",
            "context": ".",
            "platform": "x86",
        },
        "service": {"port": 8000},
    }

    config_path = temp_config_file(config_without_image)
    built_image_uri = "123456789.dkr.ecr.us-east-1.amazonaws.com/my-repo@sha256:abc123"

    # Setup mock API client
    mock_api_client.validate_yaml.return_value = mock_validation_response
    mock_api_client.get_deployment.return_value = mock_deployment
    mock_api_client.update_deployment.return_value = mock_deployment

    trigger_response = MagicMock()
    trigger_response.history_id = "history-123"
    mock_api_client.trigger_deployment.return_value = trigger_response
    mock_api_client.get_deployment_status.return_value = {"status": "completed"}
    mock_api_client.get_deployment_logs.return_value = ""

    with mock_deploy_dependencies(mock_api_client, config_without_image) as mocks:
        mocks["build"].return_value = "sha256:abc123"
        mocks["push"].return_value = built_image_uri

        deploy_service(
            config_path=config_path,
            secret="test-secret",
            host="http://localhost:3000",
        )

        # Verify Docker availability check WAS called
        mocks["docker_check"].assert_called_once()
        # Verify build and push WERE called
        mocks["build"].assert_called_once()
        mocks["push"].assert_called_once()
        # Verify update was called with docker_image set to built image URI
        mock_api_client.update_deployment.assert_called_once()
        call_kwargs = mock_api_client.update_deployment.call_args[1]
        assert call_kwargs["docker_image"] == built_image_uri


def test_deploy_service_build_mode_fails_without_docker(
    mock_api_client, mock_deployment, mock_validation_response, temp_config_file
):
    """Test that build mode fails when Docker is not available."""
    config_without_image = {
        "id": "existing-deployment-id",
        "name": "test-service",
        "runtime": "docker",
        "build": {
            "dockerfile": "Dockerfile",
            "context": ".",
            "platform": "x86",
        },
        "service": {"port": 8000},
    }

    config_path = temp_config_file(config_without_image)

    # Setup mock API client
    mock_api_client.validate_yaml.return_value = mock_validation_response
    mock_api_client.get_deployment.return_value = mock_deployment

    with mock_deploy_dependencies(
        mock_api_client, config_without_image, skip_docker_check=True
    ) as mocks:
        with pytest.raises(typer.Exit) as exc_info:
            deploy_service(
                config_path=config_path,
                secret="test-secret",
                host="http://localhost:3000",
            )

        assert exc_info.value.exit_code == 1
        # Verify Docker check was called
        mocks["docker_check"].assert_called_once()


# Tests for pull_deployment


def test_create_backup_path_format():
    """Test that backup path is created with timestamp format."""
    config_path = "runlayer.yaml"
    backup_path = _create_backup_path(config_path)

    assert backup_path.startswith("runlayer.yaml.backup.")
    # Should have timestamp format like 2025-12-03-143022
    parts = backup_path.split(".")
    timestamp = parts[-1]
    assert len(timestamp) == 17  # YYYY-MM-DD-HHMMSS


def test_pull_deployment_success():
    """Test successful deployment pull."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "runlayer.yaml"

        mock_deployment = MagicMock(spec=DeploymentPublic)
        mock_deployment.id = "test-deployment-id"
        mock_deployment.name = "test-service"
        mock_deployment.deletion_status = None

        yaml_content = "id: test-deployment-id\nname: test-service\nruntime: docker\n"

        with (
            patch("runlayer_cli.deploy.service.RunlayerClient") as mock_client_class,
            patch("runlayer_cli.deploy.service.typer.echo"),
            patch("runlayer_cli.deploy.service.typer.secho"),
        ):
            mock_client = MagicMock()
            mock_client.get_deployment.return_value = mock_deployment
            mock_client.export_deployment_yaml.return_value = yaml_content
            mock_client_class.return_value = mock_client

            pull_deployment(
                config_path=str(config_path),
                secret="test-secret",
                host="http://localhost:3000",
                deployment_id="test-deployment-id",
            )

            mock_client.export_deployment_yaml.assert_called_once_with(
                "test-deployment-id"
            )
            assert config_path.exists()
            assert "test-service" in config_path.read_text()


def test_pull_deployment_creates_backup():
    """Test that pull creates backup when file exists."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "runlayer.yaml"
        # Create existing file
        config_path.write_text("old content")

        mock_deployment = MagicMock(spec=DeploymentPublic)
        mock_deployment.id = "test-deployment-id"
        mock_deployment.name = "test-service"
        mock_deployment.deletion_status = None

        yaml_content = "id: test-deployment-id\nname: test-service\n"

        with (
            patch("runlayer_cli.deploy.service.RunlayerClient") as mock_client_class,
            patch("runlayer_cli.deploy.service.typer.echo"),
            patch("runlayer_cli.deploy.service.typer.secho"),
        ):
            mock_client = MagicMock()
            mock_client.get_deployment.return_value = mock_deployment
            mock_client.export_deployment_yaml.return_value = yaml_content
            mock_client_class.return_value = mock_client

            pull_deployment(
                config_path=str(config_path),
                secret="test-secret",
                host="http://localhost:3000",
                deployment_id="test-deployment-id",
            )

            # New file should have new content
            assert "test-service" in config_path.read_text()
            # Backup should exist with old content
            backup_files = list(Path(tmpdir).glob("runlayer.yaml.backup.*"))
            assert len(backup_files) == 1
            assert backup_files[0].read_text() == "old content"


def test_pull_deployment_uses_config_file_id():
    """Test that pull uses deployment ID from config file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "runlayer.yaml"
        # Create existing file with deployment ID
        existing_config = {"id": "config-deployment-id", "name": "old-service"}
        config_path.write_text(yaml.dump(existing_config))

        mock_deployment = MagicMock(spec=DeploymentPublic)
        mock_deployment.id = "config-deployment-id"
        mock_deployment.name = "test-service"
        mock_deployment.deletion_status = None

        yaml_content = "id: config-deployment-id\nname: test-service\n"

        with (
            patch("runlayer_cli.deploy.service.RunlayerClient") as mock_client_class,
            patch("runlayer_cli.deploy.service.typer.echo"),
            patch("runlayer_cli.deploy.service.typer.secho"),
        ):
            mock_client = MagicMock()
            mock_client.get_deployment.return_value = mock_deployment
            mock_client.export_deployment_yaml.return_value = yaml_content
            mock_client_class.return_value = mock_client

            # Don't provide deployment_id, should read from config file
            pull_deployment(
                config_path=str(config_path),
                secret="test-secret",
                host="http://localhost:3000",
                deployment_id=None,
            )

            mock_client.get_deployment.assert_called_once_with("config-deployment-id")
            mock_client.export_deployment_yaml.assert_called_once_with(
                "config-deployment-id"
            )


def test_pull_deployment_deleted_fails():
    """Test that pull fails for deleted deployment."""
    mock_deployment = MagicMock(spec=DeploymentPublic)
    mock_deployment.id = "deleted-deployment-id"
    mock_deployment.name = "deleted-service"
    mock_deployment.deletion_status = "deleted"

    with (
        patch("runlayer_cli.deploy.service.RunlayerClient") as mock_client_class,
        patch("runlayer_cli.deploy.service.typer.echo"),
        patch("runlayer_cli.deploy.service.typer.secho"),
    ):
        mock_client = MagicMock()
        mock_client.get_deployment.return_value = mock_deployment
        mock_client_class.return_value = mock_client

        with pytest.raises(typer.Exit) as exc_info:
            pull_deployment(
                config_path="runlayer.yaml",
                secret="test-secret",
                host="http://localhost:3000",
                deployment_id="deleted-deployment-id",
            )

        assert exc_info.value.exit_code == 1
        mock_client.export_deployment_yaml.assert_not_called()


def test_pull_deployment_no_id_fails():
    """Test that pull fails when no deployment ID is available."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "runlayer.yaml"
        # File doesn't exist and no deployment_id provided

        with (
            patch("runlayer_cli.deploy.service.typer.echo"),
            patch("runlayer_cli.deploy.service.typer.secho"),
        ):
            with pytest.raises(typer.Exit) as exc_info:
                pull_deployment(
                    config_path=str(config_path),
                    secret="test-secret",
                    host="http://localhost:3000",
                    deployment_id=None,
                )

            assert exc_info.value.exit_code == 1


def test_pull_deployment_empty_yaml_fails():
    """Test that pull fails when server returns empty YAML content."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "runlayer.yaml"
        # Create existing file that should NOT be backed up if export fails
        config_path.write_text("existing: config\n")

        mock_deployment = MagicMock(spec=DeploymentPublic)
        mock_deployment.id = "test-deployment-id"
        mock_deployment.name = "test-service"
        mock_deployment.deletion_status = None

        with (
            patch("runlayer_cli.deploy.service.RunlayerClient") as mock_client_class,
            patch("runlayer_cli.deploy.service.typer.echo"),
            patch("runlayer_cli.deploy.service.typer.secho"),
        ):
            mock_client = MagicMock()
            mock_client.get_deployment.return_value = mock_deployment
            # Simulate empty YAML content error from API
            mock_client.export_deployment_yaml.side_effect = ValueError(
                "Server returned empty YAML content."
            )
            mock_client_class.return_value = mock_client

            with pytest.raises(typer.Exit) as exc_info:
                pull_deployment(
                    config_path=str(config_path),
                    secret="test-secret",
                    host="http://localhost:3000",
                    deployment_id="test-deployment-id",
                )

            assert exc_info.value.exit_code == 1
            # Verify original file was NOT modified (no backup created)
            assert config_path.read_text() == "existing: config\n"
            # No backup files should exist
            backup_files = list(Path(tmpdir).glob("runlayer.yaml.backup.*"))
            assert len(backup_files) == 0


def test_pull_deployment_write_failure_restores_backup():
    """Test that pull restores backup when write fails after backup creation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "runlayer.yaml"
        original_content = "original: config\nname: my-service\n"
        config_path.write_text(original_content)

        mock_deployment = MagicMock(spec=DeploymentPublic)
        mock_deployment.id = "test-deployment-id"
        mock_deployment.name = "test-service"
        mock_deployment.deletion_status = None

        yaml_content = "id: test-deployment-id\nname: test-service\n"

        with (
            patch("runlayer_cli.deploy.service.RunlayerClient") as mock_client_class,
            patch("runlayer_cli.deploy.service.typer.echo"),
            patch("runlayer_cli.deploy.service.typer.secho") as mock_secho,
            patch("builtins.open", wraps=open) as mock_open,
        ):
            mock_client = MagicMock()
            mock_client.get_deployment.return_value = mock_deployment
            mock_client.export_deployment_yaml.return_value = yaml_content
            mock_client_class.return_value = mock_client

            # Make open fail only for write mode to config_path
            original_open = open

            def side_effect_open(path, mode="r", *args, **kwargs):
                if str(path) == str(config_path) and "w" in mode:
                    raise PermissionError("Permission denied")
                return original_open(path, mode, *args, **kwargs)

            mock_open.side_effect = side_effect_open

            with pytest.raises(typer.Exit) as exc_info:
                pull_deployment(
                    config_path=str(config_path),
                    secret="test-secret",
                    host="http://localhost:3000",
                    deployment_id="test-deployment-id",
                )

            assert exc_info.value.exit_code == 1

            # Verify original file was restored after write failure
            assert config_path.exists()
            assert config_path.read_text() == original_content

            # No backup files should remain since it was restored
            backup_files = list(Path(tmpdir).glob("runlayer.yaml.backup.*"))
            assert len(backup_files) == 0

            # Verify restoration message was shown
            secho_calls = [str(call) for call in mock_secho.call_args_list]
            assert any("Restored original file from backup" in call for call in secho_calls)
