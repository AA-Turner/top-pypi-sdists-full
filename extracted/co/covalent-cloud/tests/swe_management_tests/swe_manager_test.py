# Copyright 2023 Agnostiq Inc.

"""Unit tests for software environment management module."""

import os
from unittest.mock import ANY, MagicMock

from covalent_cloud.service_account_interface.auth_config_manager import AuthConfigManager
from covalent_cloud.shared.classes.settings import settings
from covalent_cloud.swe_management.models.environment import (
    BaseImageConfig,
    EnvironmentRuntimeConfig,
)
from covalent_cloud.swe_management.swe_manager import (
    create_env,
    delete_env,
    get_envs,
    get_pip_pkgs,
    missing_dependency,
    unpack_conda_pkgs,
)

TEMP_REQUIREMENT_FILEPATH = "/tmp/requirements.txt"
TEMP_ENV_YML_FILEPATH = "/tmp/environment.yml"
PIP_PKGS = [
    "numpy==1.19.5",
    "pandas==0.0.1",
    "scikit-learn",
    "aiohttp>1.0.0",
    "boto3<=1.0.0",
    "matplotlib<=1.0.0,>.0.3.4",
    "request!=1.0.0",
    "covalent-cloud>=0.61.0rc0",
]
CONDA_ENV_YML = """
name: mockenv
channels:
  - javascript
dependencies:
  - python=3.9
  - bokeh=2.4.2
  - conda-forge::numpy=1.21.*
  - nodejs=16.13.*
  - flask
  - pip
  - pip:
    - Flask-Testing
"""
CONDA_CHANNELS = ["javascript"]
CONDA_DEPENDENCIES = [
    "python=3.9",
    "bokeh=2.4.2",
    "conda-forge::numpy=1.21.*",
    "nodejs=16.13.*",
    "flask",
    "pip",
    {"pip": ["Flask-Testing"]},
]
MOCK_CONDA_ENV_NAME = "mockenv"
MOCK_PIP_PKGS = ["mock-package-1", "mock-package-2"]
MOCK_CHANNELS = ["mock-channel-1", "mock-channel-2"]
MOCK_DEPENDENCIES = [
    "mock-dependency-1",
    "mock-dependency-2",
    {"pip": ["mock-pip-dependency-1", "mock-pip-dependency-2"]},
]

TEST_API_KEY = "fake_api_key"  # pragma: allowlist secret


def create_temp_requirement_file():
    """Create a temporary requirements.txt file."""
    with open(TEMP_REQUIREMENT_FILEPATH, "w") as f:
        for pkg in PIP_PKGS:
            f.write(pkg + "\n")


def remove_temp_requirement_file():
    """Remove the temporary requirements.txt file."""
    os.remove(TEMP_REQUIREMENT_FILEPATH)


def create_conda_env_file():
    """Create a temporary conda environment.yml file."""
    with open(TEMP_ENV_YML_FILEPATH, "w") as f:
        f.write(CONDA_ENV_YML)


def remove_conda_env_file():
    """Remove the temporary conda environment.yml file."""
    os.remove(TEMP_ENV_YML_FILEPATH)


def test_get_pip_pkgs_str():
    """Test the get pip packages function."""
    create_temp_requirement_file()
    pip_pkgs = get_pip_pkgs(TEMP_REQUIREMENT_FILEPATH)
    assert pip_pkgs == PIP_PKGS
    remove_temp_requirement_file()


def test_get_pip_pkgs_list():
    """Test the get pip packages function."""
    create_temp_requirement_file()
    pip_pkgs = get_pip_pkgs(PIP_PKGS)
    assert pip_pkgs == PIP_PKGS
    remove_temp_requirement_file()


def test_get_pip_pkgs_list_with_requirements():
    """Test the get pip packages function."""
    create_temp_requirement_file()
    pip_pkgs = get_pip_pkgs(["mock-package", TEMP_REQUIREMENT_FILEPATH, "mock-package-2"])
    assert pip_pkgs == ["mock-package"] + PIP_PKGS + ["mock-package-2"]
    remove_temp_requirement_file()


def test_unpack_conda_pkgs_str():
    """Test the unpack conda packages function."""
    create_conda_env_file()
    channels, dependencies = unpack_conda_pkgs(TEMP_ENV_YML_FILEPATH)
    assert channels == CONDA_CHANNELS
    assert dependencies == CONDA_DEPENDENCIES
    remove_conda_env_file()


def test_unpack_conda_pkgs_list():
    """Test the unpack conda packages function."""
    create_conda_env_file()
    channels, dependencies = unpack_conda_pkgs(CONDA_DEPENDENCIES)
    assert channels == []
    assert dependencies == CONDA_DEPENDENCIES
    remove_conda_env_file()


def test_unpack_conda_pkgs_dict():
    """Test the unpack conda packages function."""
    create_conda_env_file()
    channels, dependencies = unpack_conda_pkgs(
        {
            "channels": CONDA_CHANNELS,
            "dependencies": CONDA_DEPENDENCIES,
        }
    )
    assert channels == CONDA_CHANNELS
    assert dependencies == CONDA_DEPENDENCIES
    remove_conda_env_file()


def test_create_with_base_image(mocker):
    """Test the create environment function."""
    MOCK_CREATE_DEPENDENCIES = ["mock-dependency-1", "mock-dependency-2"]
    AuthConfigManager.save_api_key(TEST_API_KEY)  # This will overwrite your local key

    session_mock = MagicMock()
    mocker.patch("requests.Session.__enter__", return_value=session_mock)

    mock_file_handle = MagicMock()
    mock_file_handle.name = "mock_name"
    mock_ctx_mgr = MagicMock()
    mock_ctx_mgr.__enter__ = MagicMock(return_value=mock_file_handle)

    mocker.patch("covalent_cloud.swe_management.swe_manager.open", return_value=mock_ctx_mgr)

    get_pip_pkgs_mock = mocker.patch(
        "covalent_cloud.swe_management.swe_manager.get_pip_pkgs", return_value=MOCK_PIP_PKGS
    )
    unpack_conda_pkgs_mock = mocker.patch(
        "covalent_cloud.swe_management.swe_manager.unpack_conda_pkgs",
        return_value=(MOCK_CHANNELS, MOCK_CREATE_DEPENDENCIES),
    )

    create_env(
        name=MOCK_CONDA_ENV_NAME,
        pip=MOCK_PIP_PKGS,
        conda=MOCK_CREATE_DEPENDENCIES,
        base_image="the_magical_land_of_narnia",
    )

    get_pip_pkgs_mock.assert_called_once_with(MOCK_PIP_PKGS)
    unpack_conda_pkgs_mock.assert_called_once_with(MOCK_CREATE_DEPENDENCIES)

    config = EnvironmentRuntimeConfig(
        image=BaseImageConfig(base_image="the_magical_land_of_narnia")
    )
    data = {
        "name": MOCK_CONDA_ENV_NAME,
        "runtime_config": config.model_dump_json(exclude_none=True),
    }
    files = {"definition": mock_file_handle}
    session_mock.post.assert_called_once_with(
        f"{settings.dispatcher_uri}/api/v2/envs", data=data, files=files, headers=ANY
    )


def test_create_env_empty(mocker):
    """Test the create environment function."""
    AuthConfigManager.save_api_key(TEST_API_KEY)  # This will overwrite your local key

    temp_file_mock = mocker.patch("tempfile.NamedTemporaryFile")
    session_mock = MagicMock()
    mocker.patch("requests.Session.__enter__", return_value=session_mock)

    mock_file_handle = MagicMock()
    mock_file_handle.name = "mock_name"
    mock_ctx_mgr = MagicMock()
    mock_ctx_mgr.__enter__ = MagicMock(return_value=mock_file_handle)

    mocker.patch("covalent_cloud.swe_management.swe_manager.open", return_value=mock_ctx_mgr)

    create_env(name=MOCK_CONDA_ENV_NAME)  # no `pip` or `conda` dependencies

    data = {
        "name": MOCK_CONDA_ENV_NAME,
    }
    files = {"definition": mock_file_handle}
    session_mock.post.assert_called_once_with(
        f"{settings.dispatcher_uri}/api/v2/envs", data=data, files=files, headers=ANY
    )


def test_create_env(mocker):
    """Test the create environment function."""
    MOCK_CREATE_DEPENDENCIES = ["mock-dependency-1", "mock-dependency-2"]
    AuthConfigManager.save_api_key(TEST_API_KEY)  # This will overwrite your local key

    temp_file_mock = mocker.patch("tempfile.NamedTemporaryFile")
    session_mock = MagicMock()
    mocker.patch("requests.Session.__enter__", return_value=session_mock)

    mock_file_handle = MagicMock()
    mock_file_handle.name = "mock_name"
    mock_ctx_mgr = MagicMock()
    mock_ctx_mgr.__enter__ = MagicMock(return_value=mock_file_handle)

    mocker.patch("covalent_cloud.swe_management.swe_manager.open", return_value=mock_ctx_mgr)

    get_pip_pkgs_mock = mocker.patch(
        "covalent_cloud.swe_management.swe_manager.get_pip_pkgs", return_value=MOCK_PIP_PKGS
    )
    unpack_conda_pkgs_mock = mocker.patch(
        "covalent_cloud.swe_management.swe_manager.unpack_conda_pkgs",
        return_value=(MOCK_CHANNELS, MOCK_CREATE_DEPENDENCIES),
    )

    create_env(
        name=MOCK_CONDA_ENV_NAME,
        pip=MOCK_PIP_PKGS,
        conda=MOCK_CREATE_DEPENDENCIES,
    )
    get_pip_pkgs_mock.assert_called_once_with(MOCK_PIP_PKGS)
    unpack_conda_pkgs_mock.assert_called_once_with(MOCK_CREATE_DEPENDENCIES)

    data = {
        "name": MOCK_CONDA_ENV_NAME,
    }
    files = {"definition": mock_file_handle}
    session_mock.post.assert_called_once_with(
        f"{settings.dispatcher_uri}/api/v2/envs", data=data, files=files, headers=ANY
    )


def test_get_envs(mocker):
    """Test the get environments function."""
    mock_get_envs_filtered = mocker.patch(
        "covalent_cloud.swe_management.swe_manager._get_envs_filtered"
    )
    mock_get_envs_filtered.return_value = {"mock-env-name": "mock-env"}

    envs = get_envs()

    mock_get_envs_filtered.assert_called_once_with(count=10, status="READY")
    assert envs == {"mock-env-name": "mock-env"}


def test_delete_env(mocker):
    """Test the delete environment function."""

    env_mock = MagicMock()
    mock_env_name = "mock-env-name"
    env_mock.name = mock_env_name

    mock_client = mocker.patch("covalent_cloud.swe_management.swe_manager.get_client")

    mock_get_envs_filtered = mocker.patch(
        "covalent_cloud.swe_management.swe_manager._get_envs_filtered"
    )
    mock_get_envs_filtered.return_value = {mock_env_name: env_mock}

    delete_env(mock_env_name)

    mock_get_envs_filtered.assert_called_once_with(name="mock-env-name")
    mock_client.return_value.delete.assert_called_once_with(f"/api/v2/envs/{env_mock.id}")


def test_missing_dependency_returns_none_when_missing():
    """Test the dependency is missing function."""
    dependencies = ["mock-dependency-1", "mock-dependency-2", "python-cpp-dep", "llm-cpp-python"]
    assert missing_dependency("python=", dependencies) is None


def test_missing_dependency_returns_dep_when_not_missing():
    """Test the dependency is missing function."""
    dependencies = ["mock-dependency-1", "python=3.9", "mock-dependency-2"]
    assert missing_dependency("python", dependencies) == "python=3.9"


def test_missing_dependency_returns_none_when_exact_match():
    """Test the dependency is missing function."""
    dependencies = ["mock-dependency-1", "pip:"]
    assert missing_dependency("pip", dependencies, True) is None


def test_missing_dependency_returns_dep_when_not_missing_with_exact():
    """Test the dependency is missing function."""
    dependencies = ["python=3.10", "pip", "pip:"]
    assert missing_dependency("pip", dependencies, True) == "pip"
