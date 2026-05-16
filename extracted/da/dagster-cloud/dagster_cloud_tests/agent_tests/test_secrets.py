import os

from dagster._core.test_utils import environ
from dagster_cloud.secrets import DagsterCloudSecretsLoader
from dagster_cloud_backend.storage.host_cloud.cloud_storage.secrets import (
    DagsterCloudSecretMetadata,
    FullDeploymentSecretScope,
    SecretValue,
)
from dagster_cloud_test_infra.secrets.fixtures import mock_secret_store  # noqa: F401 (fixture)


def test_instance_secrets_loader(
    agent_instance_local_ursula,
    host_instance,
    mock_secret_store,  # noqa: F811 (fixture)
):
    agent_instance = agent_instance_local_ursula
    assert isinstance(
        agent_instance._secrets_loader,  # noqa: SLF001
        DagsterCloudSecretsLoader,
    )

    host_instance.cloud_storage.create_secret(
        DagsterCloudSecretMetadata(
            secret_name="FOO_KEY",
            deployment_scopes=[FullDeploymentSecretScope()],
            location_names=["foo_location"],
        ),
        SecretValue("bar_with_location"),
        updated_by=None,
    )

    host_instance.cloud_storage.create_secret(
        DagsterCloudSecretMetadata(
            secret_name="FOO_KEY",
            deployment_scopes=[FullDeploymentSecretScope()],
        ),
        SecretValue("bar"),
        updated_by=None,
    )

    assert "FOO_KEY" not in os.environ

    with environ(
        {"FOO_KEY": None}  # ty: ignore[invalid-argument-type]
    ):  # clean up after messing with os.environ
        agent_instance.inject_env_vars(location_name="foo_location")

        assert os.environ.get("FOO_KEY") == "bar_with_location"

    with environ(
        {"FOO_KEY": None}  # ty: ignore[invalid-argument-type]
    ):  # clean up after messing with os.environ
        agent_instance.inject_env_vars(location_name=None)

        assert os.environ.get("FOO_KEY") == "bar"
