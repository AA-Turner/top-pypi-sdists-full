import json
import logging
import os
import re
import shutil
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from urllib.parse import unquote
from urllib.parse import urlparse

import click
from pip._internal.req import parse_requirements
from tqdm import tqdm

from tecton import version
from tecton._internals import metadata_service
from tecton.cli import printer
from tecton.cli.cli_utils import display_principal
from tecton.cli.cli_utils import display_table
from tecton.cli.cli_utils import timestamp_to_string
from tecton.cli.command import TectonCommandCategory
from tecton.cli.command import TectonGroup
from tecton.cli.environment_utils import MAX_ENVIRONMENTS_NAME_LENGTH
from tecton.cli.environment_utils import download_dependencies
from tecton.cli.environment_utils import is_valid_environment_name
from tecton.cli.environment_utils import resolve_dependencies_pex
from tecton.cli.environment_utils import resolve_dependencies_uv
from tecton.cli.upload_utils import DEFAULT_MAX_WORKERS_THREADS
from tecton.cli.upload_utils import UploadPart
from tecton.cli.upload_utils import _get_directory_size
from tecton.cli.upload_utils import get_upload_parts
from tecton_core import http
from tecton_core import id_helper
from tecton_proto.common.container_image__client_pb2 import ContainerImage
from tecton_proto.data.remote_compute_environment__client_pb2 import ObjectStoreUploadPart
from tecton_proto.data.remote_compute_environment__client_pb2 import RemoteComputeType
from tecton_proto.data.remote_compute_environment__client_pb2 import RemoteEnvironmentStatus
from tecton_proto.data.remote_compute_environment__client_pb2 import RemoteEnvironmentUploadInfo
from tecton_proto.data.remote_compute_environment__client_pb2 import S3UploadInfo
from tecton_proto.data.remote_compute_environment__client_pb2 import S3UploadPart
from tecton_proto.remoteenvironmentservice.remote_environment_service__client_pb2 import CompletePackagesUploadRequest
from tecton_proto.remoteenvironmentservice.remote_environment_service__client_pb2 import CreateRemoteEnvironmentRequest
from tecton_proto.remoteenvironmentservice.remote_environment_service__client_pb2 import DeleteRemoteEnvironmentsRequest
from tecton_proto.remoteenvironmentservice.remote_environment_service__client_pb2 import GetPackagesUploadUrlRequest
from tecton_proto.remoteenvironmentservice.remote_environment_service__client_pb2 import ListRemoteEnvironmentsRequest
from tecton_proto.remoteenvironmentservice.remote_environment_service__client_pb2 import StartPackagesUploadRequest
from tecton_proto.remoteenvironmentservice.remote_environment_service__client_pb2 import UpdateRemoteEnvironmentRequest


DEFAULT_DEPENDENCY_RESOLUTION_TOOL = "uv"
RESOLVED_REQUIREMENTS_FILENAME = "resolved_requirements.txt"
TECTON_RIFT_MATERIALIZATION_RUNTIME_PACKAGE = "tecton"
TECTON_TRANSFORM_RUNTIME_PACKAGE = "tecton-runtime"
DEFAULT_ARCHITECTURE = "x86_64"
DEFAULT_PYTHON_VERSION = "3.9.17"

DEPENDENCY_RESOLUTION_TIMEOUT_SECONDS = 600
# The maximum size of all dependencies allowed for upload
MAX_ALLOWED_DEPENDENCIES_SIZE_GB = 10

MEGABYTE = 1024 * 1024
GIGABYTE = 1024 * MEGABYTE

CHECK_MARK = "✅"
ERROR_SIGN = "⛔"
ERROR_MESSAGE_PREFIX = "⛔ ERROR: "

logger = logging.getLogger(__name__)


@dataclass
class EnvironmentIdentifier:
    id: Optional[str]
    name: Optional[str]

    def __post_init__(self):
        if not self.id and not self.name:
            printer.safe_print(
                f"{ERROR_MESSAGE_PREFIX} At least one of `environment-id` or `name` must be provided", file=sys.stderr
            )
            sys.exit(1)

    def __str__(self):
        if self.id:
            return f"id: {self.id}"
        elif self.name:
            return f"name: {self.name}"
        else:
            return "No name or id set"

    def __eq__(self, identifier):
        if isinstance(identifier, EnvironmentIdentifier):
            if self.id:
                return self.id == identifier.id
            elif self.name:
                return self.name == identifier.name
        return False


@click.command("environment", cls=TectonGroup, command_category=TectonCommandCategory.INFRA)
def environment():
    """Manage Environments for Realtime and Rift job execution.

    Use `tecton --verbose environment` to print additional debug information with environment commands.
    """


@environment.command("list")
def list_environments():
    """List all available Python Environments"""
    remote_environments = _list_environments()
    _display_environments(remote_environments)


@environment.command("get")
@click.option("-i", "--environment-id", help="Environment Id", required=False, type=str)
@click.option("-n", "--name", help="Environment Name", required=False, type=str)
def get(environment_id: Optional[str] = None, name: Optional[str] = None):
    """Get Python Environment(s) matching a name or an ID"""
    environment_identifier = EnvironmentIdentifier(id=environment_id, name=name)
    remote_environments = _list_environments(environment_identifier=environment_identifier)
    if len(remote_environments) < 1:
        error_message = f"⛔ Could not find a match for environment with {environment_identifier.__str__()}!"
        printer.safe_print(error_message, file=sys.stderr)
        sys.exit(1)
    elif len(remote_environments) > 1:
        error_message = f"⚠️ Could not find an exact match for environment with {environment_identifier.__str__()}. Did you mean one of the following?"
        printer.safe_print(error_message, file=sys.stderr)
        _display_environments(remote_environments)
    else:
        _display_environments(remote_environments, verbose=True)


@environment.command("resolve-dependencies")
@click.option("-r", "--requirements", help="Path to a requirements file", required=True, type=click.Path(exists=True))
@click.option(
    "-o",
    "--output-file",
    help="Output file to write resolved and fully pinned requirements to. If not specified, the pinned requirements will be printed to stdout",
    required=False,
    type=click.Path(exists=False),
)
@click.option(
    "-p",
    "--python-version",
    help=f"Python Version for the environment, defaults to {DEFAULT_PYTHON_VERSION}",
    required=False,
)
def resolve_requirements(
    requirements: str,
    output_file: Optional[str] = None,
    python_version: Optional[str] = None,
):
    """Resolve dependencies and return a fully resolved set of requirements for a given requirements.txt"""
    _python_version = python_version or DEFAULT_PYTHON_VERSION

    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            resolved_requirements_path, _, _ = _run_dependency_resolution(
                requirements_path=Path(requirements),
                resolved_requirements_directory=Path(tmpdir),
                python_version=_python_version,
                tool=DEFAULT_DEPENDENCY_RESOLUTION_TOOL,
            )
        except ValueError as e:
            printer.safe_print(f"{ERROR_MESSAGE_PREFIX} {e}", file=sys.stderr)
            sys.exit(1)

        if output_file is not None:
            output_path = Path(output_file)
            resolved_requirements_str = resolved_requirements_path.read_bytes()
            output_path.write_bytes(resolved_requirements_str)
        else:
            printer.safe_print("\n🎉 Fully Resolved Requirements: \n")
            _display_requirements(requirements_path=resolved_requirements_path)


@environment.command("create")
@click.option("-n", "--name", help="Name of the environment", required=True, type=str)
@click.option(
    "-r",
    "--requirements",
    help="Path to the requirements.txt file containing all dependencies for the environment",
    required=True,
    type=click.Path(exists=True),
)
@click.option("-d", "--description", help="A description for the environment", required=False, type=str)
@click.option(
    "-p",
    "--python-version",
    help=f"Python Version for the environment, defaults to {DEFAULT_PYTHON_VERSION}",
    required=False,
)
@click.option(
    "-t",
    "--tool",
    type=click.Choice(["pex", "uv"]),
    default=DEFAULT_DEPENDENCY_RESOLUTION_TOOL,
    help=f"Tool to use for dependency resolution. Defaults to '{DEFAULT_DEPENDENCY_RESOLUTION_TOOL}'.",
    required=False,
)
def create(
    name: str,
    requirements: str,
    description: Optional[str] = None,
    python_version: Optional[str] = None,
    tool: Optional[str] = DEFAULT_DEPENDENCY_RESOLUTION_TOOL,
):
    """Create a custom Tecton Rift job Environment."""
    return _create(name, requirements, description, python_version, tool)


def _create(
    name: str,
    requirements: str,
    description: Optional[str] = None,
    python_version: Optional[str] = None,
    tool: Optional[str] = DEFAULT_DEPENDENCY_RESOLUTION_TOOL,
):
    """Create a custom Tecton Rift job Environment."""
    _python_version = python_version or DEFAULT_PYTHON_VERSION
    if not is_valid_environment_name(name):
        printer.safe_print(
            f"{ERROR_MESSAGE_PREFIX} Invalid name.\nCustom environment names can only contain letters, numbers, hyphens, and underscores.\nNames must be no more than {MAX_ENVIRONMENTS_NAME_LENGTH} characters long.",
            file=sys.stderr,
        )
        sys.exit(1)

    environment_names = [e.name for e in _list_environments()]
    if name in environment_names:
        printer.safe_print(
            f"{ERROR_MESSAGE_PREFIX} An environment with the name `{name}` already exists in Tecton!",
            file=sys.stderr,
        )
        sys.exit(1)

    resp = _create_environment_with_requirements(
        name,
        description,
        Path(requirements),
        _python_version,
        tool,
    )
    if resp:
        _display_environments([resp.remote_environment])
        printer.safe_print(
            f"\n🎉 Successfully created environment {name} with Status=PENDING. Please run `tecton environment get --name <environment-name>` to monitor the status of the environment"
        )


@environment.command("describe")
@click.option("-i", "--environment-id", help="Environment ID", required=False, type=str)
@click.option("-n", "--name", help="Environment Name", required=False, type=str)
def describe(environment_id: Optional[str] = None, name: Optional[str] = None):
    """
    Print additional information about an environment
    """
    environment_identifier = EnvironmentIdentifier(id=environment_id, name=name)
    environments = _list_environments(environment_identifier)
    if not environments:
        error_message = f"⛔ Could not find a match for environment with {environment_identifier.__str__()}!"
        printer.safe_print(error_message, file=sys.stderr)
        sys.exit(1)
    if len(environments) > 1:
        message = (
            f"Could not find environment with {environment_identifier.__str__()}. Did you mean one of the following?"
        )
        printer.safe_print(f"⚠️ {message}")
        _display_environments(environments)
    else:
        environment_match = environments[0]
        printer.safe_print("\n💡 Environment Details: \n")
        _display_environments(environments, verbose=True)
        printer.safe_print("\n💡 Input Requirements: \n")
        _display_requirements(requirements_str=environment_match.requirements)
        printer.safe_print("\n✅ Fully Resolved Requirements: \n")
        _display_requirements(requirements_str=environment_match.resolved_requirements)


@environment.command("delete")
@click.option("-i", "--environment-id", help="Environment ID", required=False, type=str)
@click.option("-n", "--name", help="Environment Name", required=False, type=str)
def delete(environment_id: Optional[str] = None, name: Optional[str] = None):
    """Delete an existing custom Python Environment by name or ID"""
    return _delete(environment_id=environment_id, name=name)


def _delete(environment_id: Optional[str] = None, name: Optional[str] = None, skip_confirmation: bool = False):
    """Delete an existing custom Python Environment by name or ID"""
    environment_identifier = EnvironmentIdentifier(id=environment_id, name=name)
    environments = _list_environments(environment_identifier=environment_identifier)
    if not environments:
        printer.safe_print(
            f"⛔ No matching environment found for: {environment_identifier.__str__()}. Please verify available environments using the `tecton environment list` command",
            file=sys.stderr,
        )
        sys.exit(1)
    result_identifier = None
    environment_to_delete = None
    if len(environments) == 1:
        environment_to_delete = environments[0]
        result_identifier = EnvironmentIdentifier(id=environment_to_delete.id, name=environment_to_delete.name)

    if len(environments) > 1 or not environment_identifier.__eq__(identifier=result_identifier):
        printer.safe_print(
            f"⚠️ No matching environment found for: {environment_identifier.__str__()}. Did you mean one of the following environment(s)? \n\n",
            file=sys.stderr,
        )
        _display_environments(environments)
    else:
        confirmation_text = f"⚠️  Are you sure you want to delete environment {environment_to_delete.name}? (y/n) :"
        confirmation = "y" if skip_confirmation else input(confirmation_text).lower().strip()
        if confirmation == "y":
            try:
                delete_environment(environment_id=environment_to_delete.id)
                printer.safe_print(f"✅ Marked environment '{environment_identifier.__str__()}' for deletion.")
            except Exception as e:
                printer.safe_print(f"⛔ Failed to delete environment. error = {str(e)}, type= {type(e).__name__}")
        else:
            printer.safe_print(f"Cancelled deletion for environment: {environment_identifier.__str__()}")


def _display_environments(environments: List, verbose: bool = False):
    headings = [
        "Id",
        "Name",
        "Type",
        "Status",
        "Materialization Version",
        "Tecton Runtime Version",
        "Created By",
        "Created At",
        "Batch Image URI",
    ]
    if verbose:
        headings.extend(["Description", "Status Details"])

    rows = []
    for i in environments:
        row = (
            i.id,
            i.name,
            RemoteComputeType.Name(i.type).split("_")[-1],
            RemoteEnvironmentStatus.Name(i.status).split("_")[-1],
            i.rift_batch_job_environment.tecton_materialization_runtime_version or "N/A",
            i.realtime_job_environment.tecton_transform_runtime_version or "N/A",
            display_principal(i.created_by_principal),
            timestamp_to_string(i.created_at),
            i.rift_batch_job_environment.image_info.image_uri or "N/A",
        )
        if verbose:
            row += (i.description or "N/A", i.status_details or "N/A")

        rows.append(row)

    display_table(headings, rows)


def _create_environment_with_image(name: str, description: str, image_uri):
    try:
        req = CreateRemoteEnvironmentRequest()
        req.name = name
        req.description = description

        image_info = ContainerImage()
        image_info.image_uri = image_uri

        req.image_info.CopyFrom(image_info)

        return metadata_service.instance().CreateRemoteEnvironment(req)
    except PermissionError as _:
        printer.safe_print(
            "The user is not authorized to create environment(s) in Tecton. Please reach out to your Admin to complete this "
            "action",
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception as e:
        printer.safe_print(f"⛔ Failed to create environment: {e}", file=sys.stderr)
        sys.exit(1)


def _create_environment_with_requirements(
    name: str,
    description: str,
    requirements_path: Path,
    python_version: str,
    tool: str,
):
    """Create a custom environment by resolving dependencies, downloading wheels and updating MDS
    Parameters:
        name(str): Name of the custom environment
        description(str): Description of the custom environment
        requirements_path(str): Path to the `requirements.txt` file
        python_version(str): The Python version to resolve the dependencies for
        tool(str): The tool to use for dependency resolution ('pex' or 'uv')
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            resolved_requirements_path, tecton_runtime_version, tecton_rift_version = _run_dependency_resolution(
                requirements_path=requirements_path,
                resolved_requirements_directory=Path(tmpdir),
                python_version=python_version,
                tool=tool,
            )
        except ValueError as e:
            printer.safe_print(f"{ERROR_MESSAGE_PREFIX} {e}", file=sys.stderr)
            sys.exit(1)

        assert tecton_runtime_version or tecton_rift_version, (
            f"`tecton-runtime` and/or `tecton[rift-materialization]` must be specified in the resolved requirements: \n{resolved_requirements_path.read_text()}"
        )

        printer.safe_print(
            f"\n💡 Creating environment '{name}' for job types:\n"
            f"{CHECK_MARK if tecton_runtime_version else ERROR_SIGN} Realtime\n"
            f"{CHECK_MARK if tecton_rift_version else ERROR_SIGN} Rift Batch\n"
            f"{CHECK_MARK if tecton_rift_version and tecton_runtime_version else ERROR_SIGN} Rift Stream Ingest\n"
        )

        download_wheels_dir = Path(tmpdir) / "wheels"
        download_wheels_dir.mkdir()
        printer.safe_print("\n⏳ Downloading wheels. This may take a few seconds.....\n")
        download_dependencies(
            requirements_path=resolved_requirements_path,
            target_directory=download_wheels_dir,
            python_version=python_version,
        )
        printer.safe_print("\n✅ Successfully downloaded dependencies")

        directory_size = _get_directory_size(download_wheels_dir)
        if directory_size > (MAX_ALLOWED_DEPENDENCIES_SIZE_GB * GIGABYTE):
            printer.safe_print(
                f"{ERROR_MESSAGE_PREFIX} The total size of the downloaded dependencies exceeds the max allowed limit of {MAX_ALLOWED_DEPENDENCIES_SIZE_GB}GB. Please reduce the total number / size of dependencies and try again!",
                file=sys.stderr,
            )
            sys.exit(1)

        printer.safe_print("\n⏳ Uploading compressed wheels in parts to S3. This may take a few seconds.....")
        environment_id = id_helper.IdHelper.generate_string_id()
        try:
            location = _upload_dependencies(source_path=download_wheels_dir, environment_id=environment_id)
        except ValueError as e:
            printer.safe_print(f"{ERROR_MESSAGE_PREFIX} Unable to upload dependencies - {e}", file=sys.stderr)
            sys.exit(1)

        return create_remote_environment(
            name=name,
            id=environment_id,
            description=description,
            python_version=python_version,
            s3_wheels_location=location,
            requirements=requirements_path.read_text(),
            resolved_requirements=resolved_requirements_path.read_text(),
            transform_runtime_version=tecton_runtime_version,
            rift_materialization_runtime_version=tecton_rift_version,
            sdk_version=version.get_semantic_version(),
        )


def create_remote_environment(**kwargs):
    req = CreateRemoteEnvironmentRequest(**kwargs)
    return metadata_service.instance().CreateRemoteEnvironment(req)


def update_environment_status(**kwargs):
    req = UpdateRemoteEnvironmentRequest(**kwargs)
    return metadata_service.instance().UpdateRemoteEnvironment(req)


def _validate_input_requirements(input_requirements_path: Path):
    reqs = parse_requirements(str(input_requirements_path), session=None)
    for req in reqs:
        for package in ["tecton[rift-materialization]", "tecton-runtime"]:
            if package in req.requirement:
                return

    printer.safe_print(
        f"{ERROR_MESSAGE_PREFIX} Please include at least one of the supporting Tecton libraries:\n"
        f"💡  `tecton-runtime` package (https://pypi.org/project/tecton-runtime) to support Realtime environments\n"
        f"💡  `tecton[rift-materialization]` package (https://pypi.org/project/tecton) to support Rift materialization environments\n",
        "\nFor more information, please see: https://docs.tecton.ai/docs/materializing-features/configure-rift-materialization/python-rift-environments",
        file=sys.stderr,
    )
    sys.exit(1)


def _get_pkg_to_version(resolved_requirements_file: Path, packages: List[str]) -> Dict[str, str]:
    version_pattern = re.compile(r"==([\w.\-]+)")
    file_pattern = re.compile(r"@ (file|https?)://(.+)", re.IGNORECASE)
    wheel_version_pattern = re.compile(r"([\w.\-]+)-([\d.]+.*?)(-py\d|\.tar\.gz|\.zip|\.whl)")
    package_versions = {}

    reqs = parse_requirements(str(resolved_requirements_file), session=None)

    for req in reqs:
        requirement = req.requirement.strip()

        # Split the requirement to extract the package name and version/source
        if "==" in requirement:
            package_name, version_info = requirement.split("==", 1)
        elif "@" in requirement:
            package_name, version_info = requirement.split("@", 1)
        else:
            package_name = requirement
            version_info = None
        package_name = package_name.strip()

        if package_name in packages:
            tecton_version = None

            # Check for version specified with '=='
            if version_info and version_pattern.search(requirement):
                tecton_version = version_pattern.search(requirement).group(1)
            # Check for '@ file://' or '@ https://' notation
            elif version_info and file_pattern.search(requirement):
                file_match = file_pattern.search(requirement)
                url = file_match.group(0).split("@", 1)[1].strip()
                parsed_url = urlparse(url)
                wheel_filename = os.path.basename(parsed_url.path)
                wheel_filename = unquote(wheel_filename)
                # Extract version from the wheel filename
                wheel_match = wheel_version_pattern.match(wheel_filename)
                if wheel_match:
                    tecton_version = wheel_match.group(2)
            # Case 3: Direct URL to wheel file without '==' or '@'
            elif requirement.startswith("https://"):
                parsed_url = urlparse(requirement)
                wheel_filename = os.path.basename(parsed_url.path)
                wheel_filename = unquote(wheel_filename)
                # Extract package name and version from the wheel filename
                wheel_match = wheel_version_pattern.match(wheel_filename)
                if wheel_match:
                    package_name = wheel_match.group(1)
                    tecton_version = wheel_match.group(2)

            if tecton_version:
                package_versions[package_name] = tecton_version
            else:
                printer.safe_print(
                    f"⛔ Failed to parse version from tecton requirement:\n {requirement}\n"
                    f"Check for '==', '@ file://', '@ https://' notations",
                    file=sys.stderr,
                )
                sys.exit(1)

    return package_versions


def _run_dependency_resolution(
    requirements_path: Path, resolved_requirements_directory: Path, python_version: str, tool: str
) -> Tuple[Path, str, str]:
    """
    :param requirements_path: input requirements file path to be resolved
    :param resolved_requirements_directory: where to resolve the requirements file
    :param python_version: python version to resolve against
    :param tool: dependency resolution to use
    :return: resolved_requirements_path, tecton_runtime_version, tecton_rift_materialization_version

    """
    _validate_input_requirements(requirements_path)
    printer.safe_print(
        f"\n⏳ Resolving dependencies for Python {python_version} and architecture {DEFAULT_ARCHITECTURE} using {tool}. This may take a few seconds....."
    )
    resolved_requirements_path = resolved_requirements_directory / RESOLVED_REQUIREMENTS_FILENAME

    if tool == "uv":
        resolve_dependencies_uv(
            python_version=python_version,
            requirements_path=requirements_path,
            resolved_requirements_path=resolved_requirements_path,
            timeout_seconds=DEPENDENCY_RESOLUTION_TIMEOUT_SECONDS,
        )
        tecton_pkg_to_version = _get_pkg_to_version(
            resolved_requirements_path, packages=["tecton[rift-materialization]", "tecton-runtime"]
        )
        tecton_runtime_version = tecton_pkg_to_version.get("tecton-runtime")
        tecton_rift_version = tecton_pkg_to_version.get("tecton[rift-materialization]")
    elif tool == "pex":
        lock_output_path = resolved_requirements_directory / "lock.json"
        resolve_dependencies_pex(
            python_version=python_version,
            lock_output_path=lock_output_path,
            requirements_path=requirements_path,
            resolved_requirements_path=resolved_requirements_path,
            timeout_seconds=DEPENDENCY_RESOLUTION_TIMEOUT_SECONDS,
        )
        dependencies = _validate_and_get_dependencies(lock_output_path)

        tecton_runtime_version = dependencies.get_version(dependency_name=TECTON_TRANSFORM_RUNTIME_PACKAGE)
        tecton_rift_version = dependencies.get_version(dependency_name=TECTON_RIFT_MATERIALIZATION_RUNTIME_PACKAGE)
        tecton_pkg_to_version = {
            "tecton[rift-materialization]": tecton_rift_version,
            "tecton-runtime": tecton_runtime_version,
        }
    else:
        msg = f"Resolution tool {tool} not supported."
        raise ValueError(msg)

    printer.safe_print(
        "\n💡 Tecton versions:\n" + "\n".join(f"{pkg}: {vers}" for pkg, vers in tecton_pkg_to_version.items())
    )
    printer.safe_print("\n✅ Successfully resolved dependencies")
    return resolved_requirements_path, tecton_runtime_version, tecton_rift_version


def delete_environment(environment_id: str):
    try:
        req = DeleteRemoteEnvironmentsRequest()
        req.ids.append(environment_id)
        return metadata_service.instance().DeleteRemoteEnvironments(req)
    except PermissionError as _:
        printer.safe_print(
            "⛔ The user is not authorized to perform environment deletion. Please reach out to your Admin to complete this action.",
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception as e:
        printer.safe_print(f"⛔ Failed to delete environment: {e}", file=sys.stderr)
        sys.exit(1)


def _list_environments(environment_identifier: Optional[EnvironmentIdentifier] = None) -> List:
    try:
        req = ListRemoteEnvironmentsRequest()
        response = metadata_service.instance().ListRemoteEnvironments(req)
        if not environment_identifier:
            return list(response.remote_environments)
        if environment_identifier.id:
            environments = [env for env in response.remote_environments if environment_identifier.id in env.id]
        else:
            # Look for an exact match. If there are no exact matches, we will return all substring matches
            environments = [env for env in response.remote_environments if environment_identifier.name == env.name]
            if not environments:
                environments = [env for env in response.remote_environments if environment_identifier.name in env.name]

        return environments

    except Exception as e:
        printer.safe_print(f"⛔ Failed to fetch environments: {e}", file=sys.stderr)
        sys.exit(1)


def _upload_dependencies(source_path: Path, environment_id: str) -> str:
    """Upload dependencies from the specified source path to S3.

    Args:
        source_path (str): The path to the dependencies to upload.
        environment_id (str): The ID of the environment.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        output_zip_file = Path(tmpdir) / "wheels.zip"
        logger.debug(f"Zipping dependencies at {output_zip_file}")

        shutil.make_archive(str(output_zip_file.with_suffix("")), "zip", str(source_path))
        file_size = output_zip_file.stat().st_size

        logger.debug("Initiating Multi-Part Upload")
        start_request = StartPackagesUploadRequest(environment_id=environment_id)
        start_response = metadata_service.instance().StartPackagesUpload(start_request)

        upload_id = start_response.upload_info.s3_upload_info.upload_id
        upload_parts = _upload_file_in_parts(
            file_size=file_size,
            upload_id=upload_id,
            environment_id=environment_id,
            output_zip_file=output_zip_file,
        )

        complete_request = CompletePackagesUploadRequest(
            upload_info=RemoteEnvironmentUploadInfo(
                environment_id=environment_id,
                s3_upload_info=S3UploadInfo(upload_id=upload_id, upload_parts=upload_parts),
            )
        )
        complete_response = metadata_service.instance().CompletePackagesUpload(complete_request)
        location = complete_response.storage_location
        printer.safe_print("✅ Successfully uploaded dependencies")
        return location


def _upload_file_in_parts(
    file_size: int, upload_id: str, environment_id: str, output_zip_file: Path
) -> List[S3UploadPart]:
    """Upload a file in parallel, dividing it into parts.

    Args:
        file_size (int): The size of the file in bytes.
        upload_id (str): A unique identifier for the file upload, returned by S3.
        environment_id (str): The ID of the environment.
        output_zip_file (str): The path to the file to upload.

    Returns:
        list: A list of upload part results.
    """
    # Calculate all parts for multi part upload
    part_data_list = get_upload_parts(file_size=file_size)
    with ThreadPoolExecutor(DEFAULT_MAX_WORKERS_THREADS) as executor:
        upload_futures = [
            executor.submit(
                _upload_part,
                upload_part=part_data,
                parent_upload_id=upload_id,
                environment_id=environment_id,
                dependency_file_path=output_zip_file,
            )
            for part_data in part_data_list
        ]
        with tqdm(total=len(part_data_list), desc="Upload progress", ncols=100) as pbar:
            for future in as_completed(upload_futures):
                # Increment the tqdm progress bar whenever a future is done
                if future.result():
                    pbar.update(1)

        return [future.result() for future in upload_futures]


def _upload_part(
    upload_part: UploadPart,
    parent_upload_id: str,
    environment_id: str,
    dependency_file_path: str,
):
    """Upload a part of a file.

    Args:
        upload_part (UploadPart): The part to upload.
        parent_upload_id (str): The ID of the parent upload.
        environment_id (str): The ID of the environment.
        dependency_file_path (str): The path to the file to upload.

    Returns:
        S3UploadPart: An object representing the uploaded part.
    """
    request = GetPackagesUploadUrlRequest(
        environment_id=environment_id,
        upload_part=ObjectStoreUploadPart(
            s3_upload_part=S3UploadPart(parent_upload_id=parent_upload_id, part_number=upload_part.part_number)
        ),
    )
    response = metadata_service.instance().GetPackagesUploadUrl(request)
    signed_url = response.upload_url

    with open(dependency_file_path, "rb") as fp:
        fp.seek(upload_part.offset)
        file_data = fp.read(upload_part.part_size)
        response = http.session().put(signed_url, data=file_data)
        if response.ok:
            e_tag = response.headers["ETag"]
            return S3UploadPart(part_number=upload_part.part_number, e_tag=e_tag, parent_upload_id=parent_upload_id)
        else:
            msg = f"Upload failed with status {response.status_code} and error {response.text}"
            raise ValueError(msg)


def _display_requirements(requirements_path: Optional[Path] = None, requirements_str: Optional[str] = None):
    """
    Display requirements from a requirements.txt file after removing hashes from each line, if exists.

    Args:
        requirements_path (Path): Path to the requirements file.
        requirements_str (str): Contents of a requirements.txt file
    """
    cleaned_lines = []
    if requirements_path is not None:
        with requirements_path.open("r") as file:
            cleaned_lines = [line.strip() for line in file.readlines()]
    elif requirements_str is not None:
        cleaned_lines = [line.strip() for line in requirements_str.split("\n")]

    # Skip hashes and empty lines.
    cleaned_lines = [line.rstrip("\\").strip() for line in cleaned_lines if line and not line.startswith("--hash")]
    printer.safe_print("\n".join(cleaned_lines))


# TODO: remove once we deprecate using 'pex' as the dependency resolution tool.
class EnvironmentDependencies:
    def __init__(self, data):
        self.data = data
        self.locked_dependencies = {
            item["project_name"]: item for item in data["locked_resolves"][0]["locked_requirements"]
        }
        self.input_requirements = data["requirements"]

    def get_version(self, dependency_name):
        """Retrieve the version of the specified dependency"""
        package = self.locked_dependencies.get(dependency_name)
        if package:
            return package["version"]
        return None

    def is_dependency_present(self, dependency_name):
        """Check if the specified dependency is present in the requirements."""
        return dependency_name in self.locked_dependencies

    def get_dependency_extras(self, dependency_name):
        """Retrieve a list of extras available for the specified dependency."""
        package = self.locked_dependencies.get(dependency_name)
        if package:
            extras = set()
            for dist in package["requires_dists"]:
                if "; extra ==" in dist:
                    extracted_extra = dist.split("; extra ==")[1].strip(' "').replace("'", "")
                    extras.add(extracted_extra)
            return list(extras)
        return []

    def is_version_pinned(self, package_name):
        """Check if the dependency version is explicitly pinned in the input requirements"""
        for req in self.input_requirements:
            if package_name in req and "==" in req:
                return True
        return False


def _validate_and_get_dependencies(lock_file_path: Path) -> EnvironmentDependencies:
    with open(lock_file_path, "r") as lock_file:
        dependencies_data = json.load(lock_file)
    dependencies = EnvironmentDependencies(dependencies_data)
    tecton_runtime_version = dependencies.get_version(dependency_name=TECTON_TRANSFORM_RUNTIME_PACKAGE)
    tecton_rift_version = dependencies.get_version(dependency_name=TECTON_RIFT_MATERIALIZATION_RUNTIME_PACKAGE)

    if tecton_rift_version is not None:
        rift_extras = dependencies.get_dependency_extras(TECTON_RIFT_MATERIALIZATION_RUNTIME_PACKAGE)
        if "rift-materialization" not in rift_extras:
            printer.safe_print(
                f"{ERROR_MESSAGE_PREFIX} `rift-materialization` extra must be included for package `tecton` to support Rift materialization (tecton[rift-materialization]==x.x.x)",
                file=sys.stderr,
            )
            sys.exit(1)

    if not tecton_runtime_version and not tecton_rift_version:
        printer.safe_print(
            f"{ERROR_MESSAGE_PREFIX} Please include at least one of the supporting Tecton libraries:\n"
            f"💡  `tecton-runtime` package (https://pypi.org/project/tecton-runtime) to support Realtime environments\n"
            f"💡  `tecton[rift-materialization]` package (https://pypi.org/project/tecton) to support Rift materialization environments",
            "\nFor more information, please see: https://docs.tecton.ai/docs/materializing-features/configure-rift-materialization/python-rift-environments",
            file=sys.stderr,
        )
        sys.exit(1)
    return dependencies
