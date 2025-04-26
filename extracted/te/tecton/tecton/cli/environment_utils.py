import json
import logging
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List

from tecton_core.errors import FailedDependencyDownloadError


# need to list out compatible manylinux wheel for pip (https://github.com/pypa/pip/issues/10760)
COMPATIBLE_LINUX_PLATFORMS = [
    "manylinux1_x86_64",
    "manylinux_2_10_x86_64",
    "manylinux2010_x86_64",
    "manylinux_2_17_x86_64",
    "manylinux2014_x86_64",
    "manylinux_2_24_x86_64",
    "manylinux_2_28_x86_64",
    "manylinux_2_31_x86_64",
]

# additional wheel distributions for libs that do not have wheels in pypi
# For example we built a wheel for Pypika which Tecton depends on. (PyPika-0.48.9-py2.py3-none-any.whl)
ADDITIONAL_WHEELS_REPOS = ["https://s3.us-west-2.amazonaws.com/tecton.ai.public/python/index.html"]

PYTHON_VERSION_TO_PLATFORM = {
    "3.8": "x86_64-manylinux_2_31",
    "3.9": "x86_64-manylinux_2_31",
}

MAX_ENVIRONMENTS_NAME_LENGTH = 60

MISSING_REQUIREMENTS_ERROR = "Could not find a version that satisfies the requirement"
ENSURE_WHEELS_EXIST_WARNING = "Please also ensure that the package(s) have wheels (.whl) available for download in PyPI or any other repository used."

logger = logging.getLogger(__name__)


def resolve_dependencies_uv(
    requirements_path: Path,
    resolved_requirements_path: Path,
    python_version: str,
    timeout_seconds: int,
):
    """Resolve dependencies using `uv`
    Parameters:
        requirements_path(Path): Path to the `requirements.txt` file
        resolved_requirements_path(Path): The target path for generating the fully resolved and pinned `resolved-requirements.txt` file
        python_version(str): The python version to resolve dependencies for
        timeout_seconds(int): The timeout in seconds for the dependency resolution
    """
    major_minor_version = _get_major_minor_version(python_version)
    if major_minor_version not in PYTHON_VERSION_TO_PLATFORM:
        msg = f"Invalid `python_version` {major_minor_version}. Expected one of: {list(PYTHON_VERSION_TO_PLATFORM.keys())}"
        raise ValueError(msg)
    platform = PYTHON_VERSION_TO_PLATFORM[major_minor_version]
    logger.debug(f"Resolving dependencies for platform: {platform} python-version: {major_minor_version}")

    _run_uv_compile(
        requirements_path=requirements_path,
        resolved_requirements_path=resolved_requirements_path,
        python_version=major_minor_version,
        platform=platform,
        timeout_seconds=timeout_seconds,
    )


def resolve_dependencies_pex(
    requirements_path: Path,
    lock_output_path: Path,
    resolved_requirements_path: Path,
    python_version: str,
    timeout_seconds: int,
):
    """Resolve dependencies using `pex`
    Parameters:
        requirements_path(Path): Path to the `requirements.txt` file
        lock_output_path(Path): Path to store the output lock.json
        resolved_requirements_path(Path): The target path for generating the fully resolved and pinned `resolved-requirements.txt` file
        python_version(str): The python version to resolve dependencies for
        timeout_seconds(int): The timeout in seconds for the dependency resolution
    """
    # 'linux_x86_64' tells pex to use manylinux (defaults to manylinux2014)
    python_version_to_platform = {
        "3.8": "linux_x86_64-cp-3.8.17-cp38",
        "3.9": "linux_x86_64-cp-3.9.17-cp39",
    }
    major_minor_version = _get_major_minor_version(python_version)
    if major_minor_version not in python_version_to_platform:
        msg = f"Invalid `python_version` {python_version}. Expected one of: {list(python_version_to_platform.keys())}"
        raise ValueError(msg)
    platform = python_version_to_platform[major_minor_version]
    lock_command = _construct_lock_command(
        requirements_path=requirements_path, target_path=lock_output_path, platform=platform
    )
    _run_pex_command(command_list=lock_command, timeout_seconds=timeout_seconds)
    _create_requirements_from_lock_file(lock_output_path, resolved_requirements_path)


def download_dependencies(requirements_path: Path, target_directory: Path, python_version: str):
    """
    Download wheels for all dependencies in a requirements.txt to a target directory
    Parameters:
        requirements_path(Path): Path to requirements.txt
        target_directory(Path): The target directory to download requirements to
        python_version(str): The python version to download dependencies for
    """
    command = _construct_download_command(
        target_path=target_directory, requirements_path=requirements_path, python_version=python_version
    )

    logger.debug(f"Executing command:\n {' '.join(command)}")

    result = subprocess.run(
        command,
        text=True,
    )
    if result.returncode != 0:
        raise FailedDependencyDownloadError(result.stderr)


def is_valid_environment_name(name: str) -> bool:
    # Only letters, numbers, hyphens, or underscores allowed in an environment name
    pattern = r"^[a-zA-Z0-9_-]+$"
    return bool(re.match(pattern, name)) and len(name) <= MAX_ENVIRONMENTS_NAME_LENGTH


def _get_major_minor_version(version: str):
    version_parts = version.split(".")
    return ".".join(version_parts[:2])


def _run_uv_compile(
    requirements_path: Path, resolved_requirements_path: Path, python_version: str, platform: str, timeout_seconds: int
):
    """Run the `uv pip compile` command to resolve and lock dependencies for specific platform and python version.
    Parameters:
        requirements_path(Path): Path to the `requirements.txt` file
        resolved_requirements_path(Path): The target path for generating the fully resolved and pinned `resolved-requirements.txt` file
        python_version(str): The python version to resolve dependencies for
        platform(str): The manylinux platform to resolve dependencies for
        timeout_seconds(int): The timeout in seconds for the pex command
    """
    command_list = [
        "pip",
        "compile",
        "--python-platform",
        platform,
        "--python-version",
        python_version,
        "--no-build",
        "--emit-find-links",
        "--emit-index-annotation",
        "--emit-index-url",
        "--no-strip-extras",
        str(requirements_path),
        "--output-file",
        str(resolved_requirements_path),
    ] + [item for repo in ADDITIONAL_WHEELS_REPOS for item in ("-f", repo)]

    uv_install_dir = os.getenv("UV_INSTALL_DIR")
    if uv_install_dir:
        uv_path = os.path.join(uv_install_dir, "uv")
    else:
        uv_path = "uv"

    command = [uv_path, *command_list]
    logger.debug(f"Executing command:\n {' '.join(command)}")

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        error_message = f"Dependency Resolution timed out after {timeout_seconds} seconds! If problem persists, please contact Tecton Support for assistance."
        raise TimeoutError(error_message)
    if result.returncode != 0:
        raise ValueError(result.stderr)


def _construct_download_command(target_path: Path, requirements_path: Path, python_version: str):
    return [
        sys.executable,
        "-m",
        "pip",
        "download",
        "--no-deps",
        "-r",
        str(requirements_path),
        "-d",
        str(target_path),
        "--no-cache-dir",
        "--only-binary",
        ":all:",
        "--python-version",
        python_version,
        "--implementation",
        "cp",
    ] + [item for platform in COMPATIBLE_LINUX_PLATFORMS for item in ("--platform", platform)]


def _create_requirements_from_lock_file(lock_file, requirements_path):
    lock_data = json.loads(lock_file.read_text())
    with open(requirements_path, "w") as requirements_file:
        for resolve in lock_data["locked_resolves"]:
            for requirement in resolve["locked_requirements"]:
                for artifact in requirement["artifacts"]:
                    url = artifact["url"]
                    hash_value = f"{artifact['algorithm']}:{artifact['hash']}"
                    requirements_file.write(f"{url} --hash={hash_value}\n")


def _construct_lock_command(requirements_path: Path, target_path: Path, platform: str) -> List[str]:
    return [
        "lock",
        "create",
        "-r",
        str(requirements_path),
        "--no-build",
        "--style=strict",
        "--resolver-version=pip-2020-resolver",
        "-o",
        str(target_path),
        "--platform",
        platform,
    ] + [item for repo in ADDITIONAL_WHEELS_REPOS for item in ("-f", repo)]


def _run_pex_command(command_list: List[str], timeout_seconds: int):
    """Run the `pex` command passed as input and process any errors
    Parameters:
        command_list(str): The pex command to be executed
        timeout_seconds(int): The timeout in seconds for the pex command
    """
    command = [sys.executable, "-m", "tecton.cli.pex_wrapper", *command_list]
    logger.debug(f"Executing command: {' '.join(command)}")
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        error_message = (
            "Dependency Resolution timed out! If problem persists, please contact Tecton Support for assistance"
        )
        raise TimeoutError(error_message)
    if result.returncode != 0:
        logger.debug(f"Raw pex error: {result.stderr}")
        cleaned_error = _parse_pex_error(result.stderr)
        raise ValueError(cleaned_error)


def _parse_pex_error(error_string: str) -> str:
    """Parse and cleanup error messages from the `pex` command"""
    start_index = error_string.find("ERROR:")
    if start_index != -1:
        error_string = error_string[start_index + 6 :].replace("\n", " ")
    # The pex error message does not clarify that wheels must be present and so we append it to the original error message
    if MISSING_REQUIREMENTS_ERROR in error_string:
        error_string = f"{error_string}\n\n💡 {ENSURE_WHEELS_EXIST_WARNING}"
    return error_string
