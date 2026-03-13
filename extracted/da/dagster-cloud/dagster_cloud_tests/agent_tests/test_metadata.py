import pytest
from dagster._core.workspace.workspace import DefinitionsSource
from dagster_cloud.workspace.user_code_launcher.utils import get_grpc_server_env
from dagster_cloud_backend.storage.host_cloud.cloud_storage.workspace import (
    DagsterCloudCodeLocationEntry,
)
from dagster_cloud_cli.core.workspace import CodeLocationDeployData, GitMetadata

PORT = 3456


def test_executable_path():
    metadata = CodeLocationDeployData(image="my_image", python_file="my_file.py")
    assert metadata.get_grpc_server_command() == ["dagster", "api", "grpc"]

    with_executable_path = CodeLocationDeployData(
        image="my_image", python_file="my_file.py", executable_path="my_folder/my_executable_path"
    )

    assert with_executable_path.get_grpc_server_command() == [
        "my_folder/my_executable_path",
        "-m",
        "dagster",
        "api",
        "grpc",
    ]


def test_one_python_target():
    with pytest.raises(Exception, match="Must supply exactly one"):
        CodeLocationDeployData(image="my_image")

    with pytest.raises(Exception, match="Must supply exactly one"):
        CodeLocationDeployData(python_file="my_file", package_name="my_package")

    with pytest.raises(Exception, match="Must supply exactly one"):
        CodeLocationDeployData(python_file="my_file", module_name="my_package")


def test_file(host_instance, agent_instance):
    metadata = CodeLocationDeployData(python_file="my_file")
    env = get_grpc_server_env(
        metadata, PORT, "foo_location", agent_instance.ref_for_deployment("staging")
    )
    assert env["DAGSTER_CLI_API_GRPC_PORT"] == str(PORT)
    assert env["DAGSTER_CLI_API_GRPC_HOST"] == "0.0.0.0"
    assert env["DAGSTER_LOCATION_NAME"] == "foo_location"

    assert env.get("DAGSTER_CLI_API_GRPC_LAZY_LOAD_USER_CODE")

    assert not env.get("DAGSTER_CLI_API_GRPC_WORKING_DIRECTORY")
    assert env["DAGSTER_CLI_API_GRPC_PYTHON_FILE"] == "my_file"

    assert not env.get("DAGSTER_CLI_API_GRPC_MODULE_NAME")
    assert not env.get("DAGSTER_CLI_API_GRPC_PACKAGE_NAME")
    assert not env.get("DAGSTER_CLI_API_GRPC_ATTRIBUTE")
    assert not env.get("DAGSTER_CURRENT_IMAGE")

    assert DagsterCloudCodeLocationEntry(
        location_id=1,
        location_name="location",
        code_location_deploy_data=metadata,
        timestamp=0.0,
        definitions_source=DefinitionsSource.CODE_SERVER,
    ).get_display_metadata(host_instance) == {"python_file": "my_file"}


def test_autoload_defs_module_name(host_instance, agent_instance):
    metadata = CodeLocationDeployData(autoload_defs_module_name="autoload_me")
    env = get_grpc_server_env(
        metadata, PORT, "foo_location", agent_instance.ref_for_deployment("staging")
    )
    assert env["DAGSTER_CLI_API_GRPC_PORT"] == str(PORT)
    assert env["DAGSTER_CLI_API_GRPC_HOST"] == "0.0.0.0"
    assert env["DAGSTER_LOCATION_NAME"] == "foo_location"

    assert env.get("DAGSTER_CLI_API_GRPC_LAZY_LOAD_USER_CODE")

    assert env["DAGSTER_CLI_API_GRPC_AUTOLOAD_DEFS_MODULE_NAME"] == "autoload_me"

    assert not env.get("DAGSTER_CLI_API_GRPC_MODULE_NAME")
    assert not env.get("DAGSTER_CLI_API_GRPC_PYTHON_FILE")
    assert not env.get("DAGSTER_CLI_API_GRPC_PACKAGE_NAME")
    assert not env.get("DAGSTER_CLI_API_GRPC_ATTRIBUTE")
    assert not env.get("DAGSTER_CURRENT_IMAGE")

    assert DagsterCloudCodeLocationEntry(
        location_id=1,
        location_name="location",
        code_location_deploy_data=metadata,
        timestamp=0.0,
        definitions_source=DefinitionsSource.CODE_SERVER,
    ).get_display_metadata(host_instance) == {"autoload_defs_module_name": "autoload_me"}


def test_image(host_instance, agent_instance):
    metadata = CodeLocationDeployData(python_file="my_file", image="my_image")
    assert (
        get_grpc_server_env(
            metadata, PORT, "foo_location_name", agent_instance.ref_for_deployment("staging")
        )["DAGSTER_CURRENT_IMAGE"]
        == "my_image"
    )

    assert DagsterCloudCodeLocationEntry(
        location_id=1,
        location_name="loc",
        code_location_deploy_data=metadata,
        timestamp=0.0,
        definitions_source=DefinitionsSource.CODE_SERVER,
    ).get_display_metadata(host_instance) == {
        "image": "my_image",
        "python_file": "my_file",
    }


def test_git_metadata(host_instance, agent_instance):
    metadata = CodeLocationDeployData(
        python_file="my_file",
        image="my_image",
        git_metadata=GitMetadata(commit_hash="abc123", url="www.github.com"),
    )
    assert (
        get_grpc_server_env(
            metadata, PORT, "foo_location", agent_instance.ref_for_deployment("staging")
        )["DAGSTER_CURRENT_IMAGE"]
        == "my_image"
    )

    assert DagsterCloudCodeLocationEntry(
        location_id=1,
        location_name="loc",
        code_location_deploy_data=metadata,
        timestamp=0.0,
        definitions_source=DefinitionsSource.CODE_SERVER,
    ).get_display_metadata(host_instance) == {
        "image": "my_image",
        "python_file": "my_file",
        "url": "www.github.com",
        "commit_hash": "abc123",
    }


def test_package(host_instance, agent_instance):
    metadata = CodeLocationDeployData(package_name="my_package")
    env = get_grpc_server_env(
        metadata, PORT, "foo_location", agent_instance.ref_for_deployment("staging")
    )

    assert not env.get("DAGSTER_CLI_API_GRPC_PYTHON_FILE")
    assert not env.get("DAGSTER_CLI_API_GRPC_MODULE_NAME")
    assert env.get("DAGSTER_CLI_API_GRPC_PACKAGE_NAME") == "my_package"

    assert DagsterCloudCodeLocationEntry(
        location_id=1,
        location_name="loc",
        code_location_deploy_data=metadata,
        timestamp=0.0,
        definitions_source=DefinitionsSource.CODE_SERVER,
    ).get_display_metadata(host_instance) == {
        "package_name": "my_package",
    }


def test_module(host_instance, agent_instance):
    metadata = CodeLocationDeployData(module_name="my_module")
    env = get_grpc_server_env(
        metadata, PORT, "foo_location", agent_instance.ref_for_deployment("staging")
    )

    assert not env.get("DAGSTER_CLI_API_GRPC_PYTHON_FILE")
    assert env.get("DAGSTER_CLI_API_GRPC_MODULE_NAME") == "my_module"
    assert not env.get("DAGSTER_CLI_API_GRPC_PACKAGE_NAME")

    assert DagsterCloudCodeLocationEntry(
        location_id=1,
        location_name="loc",
        code_location_deploy_data=metadata,
        timestamp=0.0,
        definitions_source=DefinitionsSource.CODE_SERVER,
    ).get_display_metadata(host_instance) == {
        "module_name": "my_module",
    }


def test_working_directory(host_instance, agent_instance):
    metadata = CodeLocationDeployData(
        python_file="my_file", working_directory="my_folder/my_directory"
    )
    env = get_grpc_server_env(
        metadata, PORT, "foo_location", agent_instance.ref_for_deployment("staging")
    )
    assert env.get("DAGSTER_CLI_API_GRPC_WORKING_DIRECTORY") == "my_folder/my_directory"

    assert DagsterCloudCodeLocationEntry(
        location_id=1,
        location_name="location",
        code_location_deploy_data=metadata,
        timestamp=0.0,
        definitions_source=DefinitionsSource.CODE_SERVER,
    ).get_display_metadata(host_instance) == {
        "python_file": "my_file",
        "working_directory": "my_folder/my_directory",
    }


def test_attribute(host_instance, agent_instance):
    metadata = CodeLocationDeployData(python_file="my_file", attribute="my_attribute")
    env = get_grpc_server_env(
        metadata, PORT, "foo_location", agent_instance.ref_for_deployment("staging")
    )
    assert env.get("DAGSTER_CLI_API_GRPC_ATTRIBUTE") == "my_attribute"
    assert DagsterCloudCodeLocationEntry(
        location_id=1,
        location_name="location",
        code_location_deploy_data=metadata,
        timestamp=0.0,
        definitions_source=DefinitionsSource.CODE_SERVER,
    ).get_display_metadata(host_instance) == {
        "python_file": "my_file",
        "attribute": "my_attribute",
    }
