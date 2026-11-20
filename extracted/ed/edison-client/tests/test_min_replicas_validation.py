import pytest
from pydantic import ValidationError

from edison_client.models.app import JobDeploymentConfig, RuntimeConfig


def _make_config(**overrides: object) -> dict:
    """Build a minimal valid JobDeploymentConfig dict."""
    base = {"name": "test-job", "environment": "test_env"}
    return {**base, **overrides}


class TestMinReplicasValidation:
    def test_no_min_replicas_ok(self) -> None:
        # Validator only fires when MIN_REPLICAS is present; absence is fine.
        config = JobDeploymentConfig(**_make_config(environment_variables={}))
        assert config.environment_variables is not None
        assert config.environment_variables.get("MIN_REPLICAS") is None

    def test_no_env_vars_ok(self) -> None:
        config = JobDeploymentConfig(**_make_config())
        assert config.environment_variables is None

    def test_min_replicas_zero_ok(self) -> None:
        config = JobDeploymentConfig(
            **_make_config(environment_variables={"MIN_REPLICAS": "0"})
        )
        assert config.environment_variables is not None
        assert config.environment_variables["MIN_REPLICAS"] == "0"

    def test_min_replicas_one_ok(self) -> None:
        config = JobDeploymentConfig(
            **_make_config(environment_variables={"MIN_REPLICAS": "1"})
        )
        assert config.environment_variables is not None
        assert config.environment_variables["MIN_REPLICAS"] == "1"

    def test_min_replicas_fifty_ok(self) -> None:
        config = JobDeploymentConfig(
            **_make_config(environment_variables={"MIN_REPLICAS": "50"})
        )
        assert config.environment_variables is not None
        assert config.environment_variables["MIN_REPLICAS"] == "50"

    def test_min_replicas_fifty_one_raises(self) -> None:
        with pytest.raises(ValidationError, match="must be between 0 and 50"):
            JobDeploymentConfig(
                **_make_config(environment_variables={"MIN_REPLICAS": "51"})
            )

    def test_min_replicas_non_integer_raises(self) -> None:
        with pytest.raises(ValidationError, match="must be castable to an integer"):
            JobDeploymentConfig(
                **_make_config(environment_variables={"MIN_REPLICAS": "abc"})
            )


class TestMaxStepsDeprecatedNoop:
    """max_steps is deprecated but must be accepted under extra='forbid'."""

    def test_job_deployment_config_accepts_max_steps(self) -> None:
        config = JobDeploymentConfig(**_make_config(max_steps=100))
        assert config.max_steps == 100

    def test_runtime_config_accepts_max_steps(self) -> None:
        rc = RuntimeConfig(max_steps=10)
        assert rc.max_steps == 10
