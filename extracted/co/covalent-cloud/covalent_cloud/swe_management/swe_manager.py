# Copyright 2023 Agnostiq Inc.

"""Software environment management module."""

import re
import sys
import tempfile
import time
import warnings
from typing import Dict, List, Optional, Tuple, Union

import requests
import yaml
from packaging import version

from covalent_cloud import get_client
from covalent_cloud.shared.classes.helpers import check_env_is_ready
from covalent_cloud.shared.classes.settings import Settings, settings
from covalent_cloud.swe_management.models.environment import (
    BaseImageConfig,
    Environment,
    EnvironmentRuntimeConfig,
)
from covalent_cloud.swe_management.models.environment_logs import EnvironmentLogs
from covalent_cloud.swe_management.models.hardware import HardwareSpec

from ..shared.classes.exceptions import (
    CovalentAPIKeyError,
    CovalentGenericAPIError,
    CovalentSDKError,
)

__all__ = [
    "create_env",
    "get_envs",
    "delete_env",
    "get_environment_yaml",
    "get_environment_build_logs",
    "list_hardware",
]

PY_VERSION_WARNING_TEMPLATE = (
    "Specified version '{dependency}' is either invalid or does not "
    "guarantee Python {local_version} to match your local environment. "
    "Dispatches and deployments may fail unexpectedly if the local version "
    "differs from the cloud environment. To avoid this warning, omit the "
    "'python' conda dependency or specify exactly the local Python version. "
    "Note: `create_env` selects your local Python version by default."
)


def get_pip_pkgs(pip: Union[str, List[str]]) -> List[str]:
    """
    Unpacks the pip packages in the requirements.txt file and combines it into a list of required pip packages.

    """

    if not isinstance(pip, list):
        pip = [pip]

    pip_pkgs = []
    for pkg in pip:
        if pkg.endswith(".txt"):
            with open(pkg, "r") as f:
                pip_pkgs += f.read().splitlines()
        else:
            pip_pkgs.append(pkg)

    return pip_pkgs


def unpack_conda_pkgs(
    conda: Union[str, List[str], Dict[str, List[str]]],
) -> Tuple[List[str], List[str]]:
    """
    Unpacks the conda packages in the environment.yml file and combines it into a dictionary of required conda packages.

    Returns:
        channels, dependencies: channels and dependencies according to the conda environment.yml file. Note that these terms are chosen according to the conda nomenclature.

    """

    channels, dependencies = [], []

    if isinstance(conda, dict):
        channels = conda.get("channels", [])
        dependencies = conda.get("dependencies", [])

    elif isinstance(conda, str):
        if conda.endswith(".yml"):
            with open(conda, "r") as f:
                parsed_conda_env_yaml = yaml.safe_load(f)

            channels = parsed_conda_env_yaml.get("channels", [])
            dependencies = parsed_conda_env_yaml.get("dependencies", [])

    elif isinstance(conda, list):
        dependencies = conda

    return channels, dependencies


def missing_dependency(
    dependency: str, dependencies: List[str], exact: bool = False
) -> Optional[str]:
    """
    Checks if the dependencies list contains anything starting with the string.

    Args:
        dependency: String to check if it's in the dependencies list.
        dependencies: List of dependencies to be installed in the environment.
        exact: If True, checks if the dependency is exactly the same as the one in the dependencies list.
        verbose: If True, returns the exact string for the dependency that is missing.

    Returns:
        The missing dependency as a string, if applicable, or None if no dependency is missing.
    """

    for dep in dependencies:
        # check if any dependency starts with the string
        if (not exact and str(dep).startswith(dependency)) or (
            exact and str(dep).strip() == dependency.strip()
        ):
            return str(dep).strip()

    return None


def _check_local_python_dependency(dependency: str) -> None:
    """
    Checks the local python version and warns the user if the requested python version is different from the local python version.
    Args:
        dependency: The python dependency (python version) to be checked against the local python installation.
    Returns:
        None

    """
    # Get local release tuple
    local_release = tuple(sys.version_info[:3])
    local_version = ".".join(map(str, local_release))

    # Get remote version or version range
    pattern = r"python(=|>=|<=|<|>|!=)(.*)"
    pattern_match = re.match(pattern, dependency)

    if pattern_match is None:
        raise ValueError(f"Invalid python dependency: {dependency}")

    warn = False
    try:
        # Separate pattern groups
        sep, remote_version = pattern_match.groups()

        # Try to parse the version code
        remote_release = None
        if "," in pattern_match.groups()[1]:
            # Try to parse anyway just in case there is a detectable error
            for r in remote_version.split(","):
                version.parse(r.strip("=><!"))
            warn = True
        else:
            remote_release = version.parse(remote_version).release

    except version.InvalidVersion as e:
        raise ValueError(f"Invalid python version: {remote_version}") from e

    # Finally, show warning if version is valid but not exactly local version
    if warn or remote_release != local_release or sep != "=":
        warnings.warn(
            PY_VERSION_WARNING_TEMPLATE.format(
                local_version=local_version,
                dependency=dependency,
            )
        )


def create_env(
    name: str,
    pip: Optional[Union[str, List[str]]] = [],
    conda: Optional[Union[str, List[str], Dict[str, List[str]]]] = [],
    settings: Optional[Settings] = settings,
    wait: Optional[bool] = False,
    timeout: Optional[int] = 1800,
    base_image: Optional[str] = None,
    nvidia: bool = False,
) -> None:
    """
    Sends the create request to the Covalent Cloud server with the environment dependency list.

    Args:
        name: Identifier/name for the software environment.

        pip: Python packages to be installed in the environment using pip. This value can be a string `requirements.txt` and/or a list of packages. Note, that if it's a list, it's possible that one of the values is the string `requirements.txt`. In case a `requirements.txt` is passed, it will be parsed into a list of packages and combined with the list of packages passed.`

        conda: List of packages to be installed in the environment using conda. This value can either be a list of packages, a filepath to `environment.yml`. It could also be a dictionary with channels and dependencies as keys and a list of strings as their values. For example:

            conda={
                        "channels": ["conda-forge", "defaults"],
                        "dependencies": ["numpy=1.21.*", "xarray=0.15.1"],
            }

        Whatever is passed, it will be parsed into a dictionary as shown above and sent as JSON to the Covalent Cloud server. If a list of packages is provided, they will be installed using the default conda channel.

        settings: Settings object with the dispatcher URI.

        wait: If True, waits until the environment is ready before returning.

        timeout: Timeout in seconds for the environment to be ready.

        base_image: Base image of the runtime environment. If base_image is provided, it should be of the form <url>/<image>:<tag> (e.g. docker.io/python:3.9.6), where the
        :tag is optional and will default to latest if not specified. Only publicly accessible images are supported for now.

    Returns:
        None

    Examples:
        Create an environment with a list of packages:
            >>> create_env("test-env", ["typing"], ["numpy=1.21.*", "xarray=0.15.1"])

        Create an environment with a filepath to `environment.yml`:
            >>> create_env("test-env", "requirements.txt", "environment.yml")

        Create an environment with a dictionary of channels and dependencies
            >>> create_env("test-env", "requirements.txt", {"channels": ["conda-forge", "defaults"], "dependencies": ["numpy=1.21.*", "xarray=0.15.1"]})

      Create an environment with a different base image:
            >>> create_env("test-env", ["typing"], ["numpy=1.21.*", "xarray=0.15.1"], base_image="docker.io/python:slim")

    Note:
        - In case of a conflict of package between pip and conda, pip will take precedence and the conda one will be ignored.
        - If the python dependency is not provided, the local environment python version will be used.
        - If the python dependency that is provided is different from the local environment python version the user will be give a warning.
        - If the pip dependency is not provided, it will be added to the dependencies.

    """
    pip = pip or []
    conda = conda or {}

    notes = []
    pip_pkgs = get_pip_pkgs(pip)
    channels, dependencies = unpack_conda_pkgs(conda)

    # check dependencies contains pip and if not add pip
    dependency = missing_dependency("pip", dependencies, exact=True)
    if not dependency:
        dependencies = ["pip"] + dependencies
        notes.append("pip was added to the dependencies.")

    # add pip packages to dependencies after checking if pip is explicitly in the dependencies
    dependencies.append({"pip": pip_pkgs})

    # check dependencies contains python and if not set to current python version
    dependency = missing_dependency("python", dependencies)
    if not dependency:
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        dependencies = [f"python={python_version}"] + dependencies
        notes.append(f"Python version {python_version} was added to the dependencies.")
    else:
        # user indicated python version. Check if there is version compatibility with local python version and give user warnings as needed
        _check_local_python_dependency(dependency)

    yaml_template = {
        "name": name,
        "channels": channels,
        "dependencies": dependencies,
    }

    response_body = None
    start_time = time.time()
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as definition_file:

        yaml.dump(yaml_template, definition_file, default_flow_style=False)

        client = get_client(settings)

        # Open a separate reader in binary mode per Requests doc
        try:
            with open(definition_file.name, "rb") as def_file_reader:
                data = {
                    "name": name,
                }
                # add the runtime_config only if base_image is provided
                if base_image:
                    image_config = EnvironmentRuntimeConfig(
                        image=(
                            BaseImageConfig(base_image=base_image, nvidia=nvidia)
                            if base_image
                            else None
                        )
                    )
                    data["runtime_config"] = image_config.model_dump_json(exclude_none=True)
                response = client.post(
                    "/api/v2/envs",
                    {
                        "files": {"definition": def_file_reader},
                        "data": data,
                    },
                )
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                print("Environment Already Exists.")
                return
            elif (
                e.response.status_code == 401 and e.response.json()["code"] == "auth/unauthorized"
            ):
                CovalentAPIKeyError(
                    message="A valid API key is required to create an environment.",
                    code=e.response.json()["code"],
                ).rich_print(level="error")
                return
            else:
                raise CovalentGenericAPIError(error=e) from e

        response_body = response.json()

    env_is_ready = False
    if wait:
        env_is_ready, env_response = check_env_is_ready(name, settings, wait=True, timeout=timeout)

    if env_is_ready:
        env_name = env_response["records"][0]["name"]
        env_status = env_response["records"][0]["status"]
        env_build_estimate = int(time.time() - start_time)
    else:
        env_name = response_body["name"]
        env_status = response_body["status"]
        env_build_estimate = response_body["estimated_time"]

    print(f"Name: {env_name}")
    print(f"Status: {env_status}")
    print(f"Estimated Time: {env_build_estimate} seconds")
    if notes:
        print("Notes:")
        for note in notes:
            print(f"\t{note}")

    print("Environment file contains:")
    print("==========================")
    print(yaml.dump(yaml_template, default_flow_style=False))


def _get_envs_filtered(settings: Settings = settings, **filters) -> Dict[str, Environment]:
    """
    Retrieves the envs from the Covalent Cloud server which match the filters.
    """

    client = get_client(settings)

    try:

        response = client.get(
            "/api/v2/envs",
            request_options={
                "params": filters,
            },
        )

        response.raise_for_status()

        response_dict = response.json()

        envs = {}
        for env in response_dict["records"]:
            readable_env = {
                "id": env["id"],
                "name": env["name"],
                "created_at": env["created_at"],
                "status": env["status"],
                "definition_url": env["definition"],
            }
            envs[env["name"]] = Environment(**readable_env)

    except requests.exceptions.HTTPError:
        print("Error response: ", response.text)
        raise

    return envs


def get_envs(count: int = 10) -> Dict[str, Environment]:
    """
    Retrieves the last `count` created environments from the Covalent Cloud server which are ready.

    Returns:
        Dictionary of environments with their names as keys and their details as values.

    """

    envs = _get_envs_filtered(count=count, status="READY")
    return envs


def delete_env(env_name: str) -> None:
    """
    Deletes the environment with the given name from the Covalent Cloud server.

    Args:
        env_name: Name of the environment to be deleted.

    Returns:
        None

    """

    client = get_client()

    try:
        env = _get_envs_filtered(name=env_name)
        env_id = env[env_name].id

        response = client.delete(f"/api/v2/envs/{env_id}")
        response.raise_for_status()
        print(f"Environment {env_name} deleted successfully.")
    except requests.exceptions.HTTPError:
        print("Error response: ", response.text)
        raise


def get_environment_yaml(env_name_or_id: str, settings: Settings = settings) -> str:
    """
    Get the YAML definition for an environment.

    Args:
        env_name_or_id: Environment name or ID

    Returns:
        YAML string containing the environment definition

    Raises:
        CovalentGenericAPIError: If environment not found or API error occurs

    Examples:
        Get YAML by environment name:
            >>> yaml_content = get_environment_yaml("ml-environment")
            >>> print(yaml_content)
            # name: ml-environment
            # channels:
            #   - conda-forge
            # dependencies:
            #   - python=3.9
            #   - numpy=1.21.*
            #   - pip:
            #     - tensorflow==2.10.0

        Get YAML by environment ID:
            >>> yaml_content = get_environment_yaml("550e8400-e29b-41d4-a716-446655440000")
    """

    client = get_client(settings)

    try:
        # First try to get the environment by name to find its ID
        if not env_name_or_id.count("-") == 4:  # Simple heuristic to check if it's a UUID
            envs = _get_envs_filtered(settings, name=env_name_or_id)
            if not envs or env_name_or_id not in envs:
                raise CovalentSDKError(
                    message=f"Environment '{env_name_or_id}' not found.",
                    code="error/environment_not_found",
                )
            env_id = envs[env_name_or_id].id
        else:
            env_id = env_name_or_id

        # Get the environment details which includes the definition URL
        response = client.get(f"/api/v2/envs/{env_id}")
        response.raise_for_status()
        env_data = response.json()

        definition_url = env_data.get("definition")
        if not definition_url:
            raise CovalentSDKError(
                message=f"Environment definition not available for '{env_name_or_id}'.",
                code="error/definition_not_available",
            )

        # Download the YAML definition from the S3 URL
        # The server provides a presigned S3 URL that should be directly accessible
        try:
            yaml_response = requests.get(definition_url, timeout=30)
            yaml_response.raise_for_status()
            return yaml_response.text
        except requests.exceptions.RequestException as req_err:
            # If the S3 URL fails, it might be expired or inaccessible
            raise CovalentSDKError(
                message=f"Failed to download environment definition: {str(req_err)}",
                code="error/download_failed",
            ) from req_err

    except requests.exceptions.HTTPError as e:
        # Always treat 404 as environment not found, regardless of context
        if e.response is not None and e.response.status_code == 404:
            raise CovalentSDKError(
                message=f"Environment '{env_name_or_id}' not found.",
                code="error/environment_not_found",
            )
        else:
            # For other HTTP errors, convert to CovalentSDKError with meaningful message
            raise CovalentSDKError(
                message=f"HTTP {e.response.status_code} error while fetching environment '{env_name_or_id}': {str(e)}",
                code=f"error/http_{e.response.status_code}",
            ) from e
    except (CovalentSDKError, CovalentGenericAPIError):
        # Re-raise Covalent errors without wrapping to preserve the original message
        raise
    except Exception as e:
        # Convert general exceptions to CovalentSDKError to preserve error messages
        raise CovalentSDKError(
            message=f"Unexpected error while fetching environment YAML for '{env_name_or_id}': {str(e)}",
            code="error/unexpected",
        ) from e


def get_environment_build_logs(
    env_name_or_id: str,
    next_token: Optional[str] = None,
    limit: int = 10000,
    settings: Settings = settings,
) -> EnvironmentLogs:
    """
    Get build logs for an environment with optional filtering.

    Args:
        env_name_or_id: Environment name or ID
        next_token: Pagination token for retrieving next page of results
        limit: Number of log events to retrieve (default: 10000, max: 10000)

    Returns:
        EnvironmentLogs containing log events and pagination token

    Raises:
        CovalentSDKError: If environment not found, invalid parameters, or server error
        CovalentGenericAPIError: If other API errors occur

    Examples:
        Get recent build logs:
            >>> logs = get_environment_build_logs("ml-environment")
            >>> for log in logs.events:
            ...     print(f"[{log.timestamp}] {log.message}")

        Paginate through logs:
            >>> logs = get_environment_build_logs("ml-environment", limit=50)
            >>> while logs.next_token:
            ...     logs = get_environment_build_logs(
            ...         "ml-environment",
            ...         next_token=logs.next_token,
            ...         limit=50
            ...     )
            ...     # Process logs...
    """

    client = get_client(settings)

    # Validate count parameter
    if limit <= 0 or limit > 10000:
        raise CovalentSDKError(
            message="limit must be between 1 and 10000", code="error/invalid_parameter"
        )

    try:
        # First try to get the environment by name to find its ID
        if not env_name_or_id.count("-") == 4:  # Simple heuristic to check if it's a UUID
            envs = _get_envs_filtered(settings, name=env_name_or_id)
            if not envs or env_name_or_id not in envs:
                raise CovalentSDKError(
                    message=f"Environment '{env_name_or_id}' not found.",
                    code="error/environment_not_found",
                )
            env_id = envs[env_name_or_id].id
        else:
            env_id = env_name_or_id

        # Prepare query parameters
        params = {"limit": limit}

        if next_token:
            params["next_token"] = next_token

        # Get the build logs
        response = client.get(
            f"/api/v2/envs/{env_id}/logs",
            request_options={
                "params": params,
            },
        )
        response.raise_for_status()

        # Parse response and return EnvironmentLogs object
        return EnvironmentLogs(**response.json())

    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 404:
            raise CovalentSDKError(
                message=f"Environment '{env_name_or_id}' not found.",
                code="error/environment_not_found",
            )
        elif e.response is not None and e.response.status_code == 500:
            raise CovalentSDKError(
                message=f"Server error while fetching logs for environment '{env_name_or_id}'. The environment may not have build logs available or there may be a server issue.",
                code="error/server_error",
            )
        else:
            # For other HTTP errors, convert to CovalentSDKError with meaningful message
            raise CovalentSDKError(
                message=f"HTTP {e.response.status_code} error while fetching logs for environment '{env_name_or_id}': {str(e)}",
                code=f"error/http_{e.response.status_code}",
            ) from e
    except (CovalentSDKError, CovalentGenericAPIError):
        # Re-raise Covalent errors without wrapping to preserve the original message
        raise
    except Exception as e:
        # Convert general exceptions to CovalentSDKError to preserve error messages
        raise CovalentSDKError(
            message=f"Unexpected error while fetching build logs for environment '{env_name_or_id}': {str(e)}",
            code="error/unexpected",
        ) from e


def list_hardware(settings: Settings = settings) -> List[HardwareSpec]:
    """
    List available hardware options for the user.

    Args:
        settings: Settings instance (optional)

    Returns:
        List of HardwareSpec objects with specifications and pricing

    Raises:
        CovalentGenericAPIError: If API error occurs

    Examples:
        List all available hardware:
            >>> hardware = list_hardware()
            >>> for hw in hardware:
            ...     print(f"{hw.name}: {hw.display_cost}/hour - {hw.vcpus} vCPUs, {hw.memory}MB RAM")
            ...     if hw.gpu_type:
            ...         print(f"  GPU: {hw.gpu_type} ({hw.gpu_vendor})")

        Filter for GPU hardware:
            >>> hardware = list_hardware()
            >>> gpu_hardware = [hw for hw in hardware if hw.has_gpu]
            >>> print(f"Found {len(gpu_hardware)} GPU hardware configurations")
    """

    client = get_client(settings)

    try:
        response = client.get("/api/v2/hardware")
        response.raise_for_status()

        hardware_data = response.json()
        hardware_list = hardware_data.get("hardware", [])

        # Convert to HardwareSpec objects
        hardware_specs = []
        for hw_data in hardware_list:
            hardware_specs.append(HardwareSpec.model_validate(hw_data))

        return hardware_specs

    except requests.exceptions.HTTPError as e:
        raise CovalentGenericAPIError(error=e) from e
