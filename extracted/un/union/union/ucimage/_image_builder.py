"""All imports to unionai in this file should be in the function definition.

This plugin is loaded by flytekit, so any imports to unionai can lead to circular imports.
"""

import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import warnings
from dataclasses import fields
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from importlib.metadata import version
from pathlib import Path
from typing import ClassVar, List, Optional, Tuple

import click
from flytekit import Labels
from flytekit.configuration import SerializationSettings
from flytekit.constants import CopyFileDetection
from flytekit.exceptions.user import FlyteEntityNotExistException
from flytekit.image_spec.image_spec import _F_IMG_ID, ImageBuildEngine, ImageSpec, ImageSpecBuilder
from flytekit.models import security
from flytekit.models import task as task_models
from flytekit.models.core import execution as core_execution_models
from flytekit.models.core.identifier import Identifier, ResourceType
from flytekit.models.filters import ValueIn
from flytekit.remote import FlyteRemote, FlyteTask, FlyteWorkflowExecution
from flytekit.remote.remote import MOST_RECENT_FIRST
from flytekit.tools.ignore import DockerIgnore, GitIgnore, IgnoreGroup, StandardIgnore
from flytekit.tools.script_mode import ls_files
from flytekit.tools.translator import Options

from union._utils import _sanitize_label

try:
    import tomllib
except ImportError:
    import tomli as tomllib


RECOVER_EXECUTION_PAGE_LIMIT = 1_000
UNIONAI_IMAGE_NAME_KEY = "unionai_image_name"

# Task suffix used to append to build-image task template.
# Used when we we are required to change the build-image task template
_BUILD_IMAGE_SUFFIX = "exec"

_BUILD_IMAGE_SUFFIX_HASH_ALGORITHM = "sha256"
_BUILD_IMAGE_SUFFIX_HASH_LENGTH = 8

_PACKAGE_NAME_RE = re.compile(r"^[\w-]+")
_IMAGE_BUILDER_PROJECT_DOMAIN = {"project": "system", "domain": "production"}


def _is_union(package: str) -> bool:
    """Return True if `package` is union or unionai."""
    m = _PACKAGE_NAME_RE.match(package)
    if not m:
        return False
    name = m.group()
    return name in ("union", "unionai")


def get_unionai_for_pypi():
    union_version = version("union")
    if "dev" in union_version:
        return "union"
    else:
        return f"union=={union_version}"


def _get_remote() -> FlyteRemote:
    from union.configuration import UnionAIPlugin
    from union.remote import UnionRemote

    remote = UnionRemote(
        config=UnionAIPlugin._get_config_for_remote(None, default_to_union_semantics=True),
        default_domain=_IMAGE_BUILDER_PROJECT_DOMAIN["domain"],
        default_project=_IMAGE_BUILDER_PROJECT_DOMAIN["project"],
    )
    return remote


@lru_cache
def _get_fully_qualified_image_name(remote, execution):
    return execution.outputs["fully_qualified_image"]


def _build_image_exec_version(components: List[str]) -> str:
    """
    Generate a consistent version, hash-based, for the build-image task.

    Args:
        components: List of strings to hash
        algorithm: Hash algorithm to use (md5, sha1, sha256, etc.)
        length: Optional length to truncate the hash to

    Returns:
        A hash string representing the array content
    """
    if not components:
        return hashlib.new(_BUILD_IMAGE_SUFFIX_HASH_ALGORITHM, b"").hexdigest()

    # Sort to ensure consistent order regardless of input order
    sorted_array = sorted(components)

    # Join with a delimiter that's unlikely to appear in the strings
    # Use unit separator (ASCII 31) as delimiter
    joined_string = "\u001f".join(sorted_array).encode("utf-8")

    hash_obj = hashlib.new(_BUILD_IMAGE_SUFFIX_HASH_ALGORITHM, joined_string)
    hash_result = hash_obj.hexdigest()

    if _BUILD_IMAGE_SUFFIX_HASH_LENGTH < len(hash_result):
        return hash_result[:_BUILD_IMAGE_SUFFIX_HASH_LENGTH]

    return hash_result


def _sanitize_image_name(image_name: str) -> str:
    """Sanitizes a Docker image name to be used as a Kubernetes label.

    Ensures the image name meets Kubernetes label requirements by sanitizing it.
    If the sanitized name exceeds 63 characters (Kubernetes label limit), it shortens
    the name by extracting just the image name and tag components.

    Args:
        image_name (str): The original Docker image name (may include registry, repository, name and tag)

    Returns:
        str: A sanitized image name that complies with Kubernetes label restrictions
    """

    # Shorten target_image if it exceeds 63 characters
    sanitized_target_image = _sanitize_label(image_name)
    if len(sanitized_target_image) > 63:
        # Parse the FQIN components
        parts = image_name.split("/")
        image_and_tag = parts[-1].split(":")
        image_name = image_and_tag[0]
        tag = image_and_tag[1] if len(image_and_tag) > 1 else "latest"

        # Just use image name and tag
        shortened_target = f"{image_name}:{tag}"
        sanitized_target_image = _sanitize_label(shortened_target)
    return sanitized_target_image


def _apply_task_template_changes(
    remote: FlyteRemote, task: FlyteTask, imagepull_secret_name: Optional[str]
) -> FlyteTask:
    """Creates a new task with image pull secret configuration.

    Takes an existing Flyte task and creates a new version of it with an image pull
    secret added to its security context. This allows the task to pull images from
    private registries during execution.

    Args:
        remote (FlyteRemote): The Flyte remote connection to use for registration
        task (FlyteTask): The original task to modify
        imagepull_secret_name (Optional[str]): The name of the image pull secret to add

    Returns:
        FlyteTask: A new task with the image pull secret configured, or the original
                   task if no imagepull_secret_name was provided
    """
    # Return the reference task if no imagepull secret is provided
    if not imagepull_secret_name:
        return task

    # Register the updated task with a new version
    name = f"{task.name}-{_BUILD_IMAGE_SUFFIX}"
    version = _build_image_exec_version([imagepull_secret_name, task.id.version])

    try:
        task = remote.fetch_task(name=name, version=version)
        click.secho(f"{task.name} already exists. Skipping registration.", fg="blue")
        return task
    except FlyteEntityNotExistException:
        click.secho(f"Task {name} does not exist. Registering a new version.", fg="blue")

        new_task_id = Identifier(
            resource_type=ResourceType.TASK,
            project=remote.default_project,
            domain=remote.default_domain,
            name=name,
            version=version,
        )

        template = task.template
        template._id = new_task_id
        template._security_context = security.SecurityContext(
            secrets=[
                security.Secret(key=imagepull_secret_name, mount_requirement=security.Secret.MountType.FILE),
            ]
        )
        task_spec = task_models.TaskSpec(template=template)
        new_task_id = remote.raw_register(task_spec, SerializationSettings(image_config=None), version)

        new_task = remote.fetch_task(name=new_task_id.name, version=new_task_id.version)

        return new_task


def _build(spec: Path, context: Optional[Path], target_image: str, imagepull_secret_name: Optional[str]) -> str:
    """Build image using UnionAI."""

    remote = _get_remote()
    start = datetime.now(timezone.utc)

    context_url = "" if context is None else remote.upload_file(context)[1]

    spec_url = remote.upload_file(spec)[1]
    entity = _apply_task_template_changes(remote, remote.fetch_task(name="build-image"), imagepull_secret_name)
    sanitized_name = _sanitize_image_name(target_image)
    execution = remote.execute(
        entity,
        inputs={"spec": spec_url, "context": context_url, "target_image": target_image},
        options=Options(
            labels=Labels(values={UNIONAI_IMAGE_NAME_KEY: sanitized_name}),
        ),
        overwrite_cache=True,
    )
    click.secho("👍 Build submitted!", bold=True, fg="yellow")

    console_url = remote.generate_console_url(execution)

    click.secho(
        "⏳ Waiting for build to finish at: " + click.style(console_url, fg="cyan"),
        bold=True,
    )
    execution = remote.wait(execution, poll_interval=timedelta(seconds=1))

    elapsed = str(datetime.now(timezone.utc) - start).split(".")[0]

    if execution.closure.phase == core_execution_models.WorkflowExecutionPhase.SUCCEEDED:
        click.secho(f"✅ Build completed in {elapsed}!", bold=True, fg="green")
    else:
        error_msg = execution.error.message
        raise click.ClickException(
            f"❌ Build failed in {elapsed} at {click.style(console_url, fg='cyan')} with error:\n\n{error_msg}"
        )

    return _get_fully_qualified_image_name(remote, execution)


def _copy_files_into_build_context(image_spec: ImageSpec, spec: dict, context_path: Path):
    if image_spec.source_copy_mode is not None and image_spec.source_copy_mode != CopyFileDetection.NO_COPY:
        if not image_spec.source_root:
            raise ValueError(f"Field source_root for {image_spec} must be set when copy is set")

        # Easter egg
        # Load in additional packages before installing pip/apt packages
        vendor_path = Path(image_spec.source_root) / ".vendor"
        if vendor_path.is_dir():
            spec["dist_dirpath"] = ".vendor"

        ignore = IgnoreGroup(image_spec.source_root, [GitIgnore, DockerIgnore, StandardIgnore])

        ls, _ = ls_files(
            str(image_spec.source_root), image_spec.source_copy_mode, deref_symlinks=False, ignore_group=ignore
        )

        for file_to_copy in ls:
            rel_path = os.path.relpath(file_to_copy, start=str(image_spec.source_root))
            Path(context_path / rel_path).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(
                file_to_copy,
                context_path / rel_path,
            )

    if image_spec.copy:
        for src in image_spec.copy:
            src_path = Path(src)

            if src_path.is_absolute() or ".." in src_path.parts:
                raise ValueError("Absolute paths or paths with '..' are not allowed in COPY command.")

            dst_path = context_path / src_path
            dst_path.parent.mkdir(parents=True, exist_ok=True)

            if src_path.is_dir():
                shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
            else:
                shutil.copy(src_path, dst_path)


class UCImageSpecBuilder(ImageSpecBuilder):
    """ImageSpec builder for UnionAI."""

    _SUPPORTED_UNIVERSAL_PARAMETERS: ClassVar = {
        "name",
        "builder",
        "builder_options",
        "source_root",
        "env",
        "packages",
        "requirements",
        "apt_packages",
        "pip_index",
        "pip_extra_index_url",
        "pip_extra_args",
        "commands",
        "conda_packages",
        "conda_channels",
        "source_copy_mode",
        "registry",
        "copy",
    }

    _SUPPORTED_CUSTOM_BASE_IMAGE_PARAMETERS = _SUPPORTED_UNIVERSAL_PARAMETERS | {
        "base_image",
    }

    _SUPPORTED_UNION_BASE_IMAGE_PARAMETERS = _SUPPORTED_UNIVERSAL_PARAMETERS | {
        "python_version",
        "cuda",
        "cudnn",
        "platform",
    }

    def build_image(self, image_spec: ImageSpec):
        """Build image using UnionAI."""
        image_name = image_spec.image_name()

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            spec_path, archive_path, imagepull_secret_name = self._validate_configuration(
                image_spec, tmp_path, image_name
            )
            return _build(spec_path, archive_path, image_name, imagepull_secret_name)

    def _print_submitting_new_build(self) -> bool:
        click.secho("🐳 Submitting a new build...", bold=True, fg="blue")
        return True

    def should_build(self, image_spec: ImageSpec) -> bool:
        """Check whether the image should be built."""
        image_name = image_spec.image_name()
        remote = _get_remote()

        _check_image_builder_enabled(remote)

        if image_spec.registry:
            click.secho(f"{image_name} configured with external registry.")
            return self._print_submitting_new_build()

        try:
            ImageBuildEngine._IMAGE_NAME_TO_REAL_NAME[image_name] = remote._get_image_fqin(image_name)
            click.secho(f"Image {image_name} found. Skip building.", fg="blue")
            return False
        except FlyteEntityNotExistException:
            click.secho(f"Image {image_name} was not found or has expired.", fg="blue")
            return self._print_submitting_new_build()

    def _validate_configuration(
        self, image_spec: ImageSpec, tmp_path: Path, image_name: str
    ) -> Tuple[Path, Optional[Path], Optional[str]]:
        """Validate and write configuration for builder."""
        field_names = [f.name for f in fields(ImageSpec) if not f.name.startswith("_")]

        if image_spec.base_image is None:  # Union base image
            unsupported_parameters = [
                name
                for name in field_names
                if getattr(image_spec, name) and name not in self._SUPPORTED_UNION_BASE_IMAGE_PARAMETERS
            ]
        else:  # Custom base image
            unsupported_parameters = [
                name
                for name in field_names
                if getattr(image_spec, name) and name not in self._SUPPORTED_CUSTOM_BASE_IMAGE_PARAMETERS
            ]

        if unsupported_parameters:
            msg = f"The following parameters are unsupported and ignored: {unsupported_parameters}"
            warnings.warn(msg, UserWarning)

        # Hardcoded for now since our base image only supports 3.11
        if image_spec.python_version is None:
            major = sys.version_info.major
            minor = sys.version_info.minor
        else:
            version_split = image_spec.python_version.split(".")
            if not (2 <= len(version_split) <= 3):
                raise ValueError("python_version must be in the form major.minor. For example: 3.12")
            major, minor = version_split[:2]
            try:
                major, minor = int(major), int(minor)
            except ValueError:
                raise ValueError("python_version must be in the form major.minor. For example: 3.12")

        if not (major == 3 and 9 <= minor <= 12):
            raise ValueError(f"Only python versions between 3.9 to 3.12 are supported, got {major}.{minor}")

        python_version = f"{major}.{minor}"

        spec = {"python_version": python_version}
        # Transform image spec into a spec we expect
        if image_spec.apt_packages:
            spec["apt_packages"] = image_spec.apt_packages
        if image_spec.commands:
            spec["commands"] = image_spec.commands
        if image_spec.cuda or image_spec.cudnn:
            spec["enable_gpu"] = True
        if image_spec.conda_packages:
            spec["conda_packages"] = image_spec.conda_packages
        if image_spec.conda_channels:
            spec["conda_channels"] = image_spec.conda_channels

        env = image_spec.env or {}
        env = {_F_IMG_ID: image_name, **env}
        if env:
            spec["env"] = env

        packages = []
        if image_spec.packages:
            packages.extend(image_spec.packages)

        spec["python_packages"] = packages

        pip_extra_index_urls = []
        if image_spec.pip_index:
            pip_extra_index_urls.append(image_spec.pip_index)

        if image_spec.pip_extra_index_url:
            pip_extra_index_urls.extend(image_spec.pip_extra_index_url)

        spec["pip_extra_index_urls"] = pip_extra_index_urls
        spec["pip_extra_args"] = image_spec.pip_extra_args

        context_path = tmp_path / "build.uc-image-builder"
        context_path.mkdir(exist_ok=True)

        _all_packages = []
        _all_packages.extend(packages)

        if image_spec.requirements:
            if not Path(image_spec.requirements).exists():
                raise ValueError(f"requirements file {image_spec.requirements} does not exist")
            name = Path(image_spec.requirements).name
            shutil.copy2(image_spec.requirements, context_path / name)
            spec["python_requirements_files"] = [name]
            if str(image_spec.requirements).endswith(".txt"):
                with (context_path / name).open() as f:
                    _all_packages.extend([line.strip() for line in f.readlines()])
            elif str(image_spec.requirements).endswith("poetry.lock"):
                pyproject = Path(image_spec.requirements).parent.joinpath("pyproject.toml")
                self._check_pyproject_for_unsupported_features(pyproject)
                self._check_image_spec_for_unsupported_features(image_spec)
                readme = self._get_package_readme(pyproject)
                if readme:
                    shutil.copy2(readme, context_path / readme.name)

                if pyproject.exists():
                    # almost never happens, but if the user has 'subdir/poetry.lock', note that this will copy the
                    # pyproject file directly into the context folder, removing the subdir.
                    shutil.copy2(pyproject, context_path / pyproject.name)
                else:
                    raise ValueError(f"must have project file if using lock file {image_spec.requirements}")

            elif str(image_spec.requirements).endswith("uv.lock"):
                self._prepare_for_uv_lock(image_spec, context_path)
                readme = self._get_package_readme(Path(image_spec.requirements).parent / "pyproject.toml")
                if readme:
                    shutil.copy2(readme, context_path / readme.name)

        # if union is not specified, then add it here.
        union_pypi_package = get_unionai_for_pypi()
        if not any(_is_union(p) for p in _all_packages) and union_pypi_package:
            packages.append(union_pypi_package)

        # Custom base image
        if image_spec.base_image:
            if not isinstance(image_spec.base_image, str):
                raise ValueError("Union image builder only supports string base images")
            spec["base_image"] = image_spec.base_image

        _copy_files_into_build_context(image_spec, spec, context_path)

        if any(context_path.iterdir()):
            archive_path = Path(shutil.make_archive(tmp_path / "context", "xztar", context_path))
        else:
            archive_path = None

        spec_path = tmp_path / "spec.json"
        with spec_path.open("w") as f:
            json.dump(spec, f)

        builder_options = image_spec.builder_options or {}

        return (spec_path, archive_path, builder_options.get("imagepull_secret_name"))

    @staticmethod
    def _prepare_for_uv_lock(image_spec: ImageSpec, context_path: Path):
        """Prepare image builder for uv.lock."""
        pyproject_path = Path(image_spec.requirements).parent / "pyproject.toml"

        if not pyproject_path.exists():
            raise ValueError("pyproject.toml must exist when using uv.lock")

        for line in pyproject_path.read_text().splitlines():
            if "tool.uv.index" in line:
                raise ValueError("External sources are not supported in pyproject.toml")

        if image_spec.packages is not None:
            raise ValueError(
                "When using uv.lock, setting packages is not supported. "
                "Please include your dependencies in the uv.lock file."
            )

        if image_spec.pip_index or image_spec.pip_extra_index_url:
            raise ValueError("External sources are not supported in image spec when using uv lock file")

        shutil.copy2(pyproject_path, context_path / pyproject_path.name)

    def _get_package_readme(self, pyproject_path: Path) -> Optional[Path]:
        with open(pyproject_path, "rb") as f:
            pyproject = tomllib.load(f)

        poetry_readme = pyproject.get("tool", {}).get("poetry", {}).get("readme", None)
        if poetry_readme:
            return Path(pyproject_path).parent / poetry_readme

        readme = pyproject.get("project", {}).get("readme", None)
        if readme:
            return Path(pyproject_path).parent / readme

        return None

    @staticmethod
    def _check_pyproject_for_unsupported_features(pyproject: Path):
        """
        Use of external sources is prohibited because caching might interfere with other builds, and because the
        image builder might not have network access to it.
        If there's enough request for this for non-pypi but public sources, we can build out smarter caching in all
        our builders.
        See https://python-poetry.org/docs/repositories/#package-sources
        """
        for line in pyproject.read_text().splitlines():
            if "tool.poetry.source" in line:
                raise ValueError("External sources are not supported in pyproject.toml")

    @staticmethod
    def _check_image_spec_for_unsupported_features(image_spec: ImageSpec):
        """
        Use of external sources is prohibited in poetry because it should be declared in the pyproject file instead
        (which in turn should raise an error because we don't want to support non-pypi sources).
        """
        if image_spec.pip_index:
            raise ValueError("External sources are not supported in image spec when using poetry lock file")
        if image_spec.pip_extra_index_url:
            raise ValueError("External sources are not supported in image spec when using poetry lock file")


def _check_image_builder_enabled(remote: FlyteRemote):
    """Checks if the Union image builder is enabled."""
    try:
        remote.fetch_task(name="build-image")
    except FlyteEntityNotExistException as e:
        msg = "Union remote image builder is not enabled. Please contact Union support to enable it."
        raise click.ClickException(msg) from e


def _get_latest_image_build_execution(remote: FlyteRemote, image_name: str) -> Optional[FlyteWorkflowExecution]:
    """
    Get the latest image build execution for the given image name.
    Returns None if no execution is found or the execution is not in QUEUED, RUNNING, or SUCCEEDED phase.
    """
    # Replace ':' with '_' since flyte does not allow ':' in the label value
    target_image = _sanitize_label(image_name)
    executions, _ = remote.client.list_executions_paginated(
        limit=1,
        filters=[
            ValueIn("execution_tag.key", [UNIONAI_IMAGE_NAME_KEY]),
            ValueIn("execution_tag.value", [target_image]),
            ValueIn("phase", ["QUEUED", "RUNNING", "SUCCEEDED"]),
        ],
        sort_by=MOST_RECENT_FIRST,
        **_IMAGE_BUILDER_PROJECT_DOMAIN,
    )

    if len(executions) == 0:
        return None

    return remote.sync_execution(FlyteWorkflowExecution.promote_from_model(executions[0]))


def _register_union_image_builder(priority: int = 10):
    ImageBuildEngine.register("unionai", UCImageSpecBuilder(), priority)
    ImageBuildEngine.register("union", UCImageSpecBuilder(), priority)


def _is_output_not_found(e: Exception) -> bool:
    # Unfortunately, failure to find an execution output doesn't return a 404 but an exception that wraps the 404.
    # Here we check the exception string directly
    return "status code: 404" in str(e)


def get_image_name(image_url: str) -> str:
    """
    Extract the image name from a Docker image string.

    :param image_url: Docker image string (e.g., 'repository/name:tag' or 'name:tag')
    :return: The image name
    """
    pattern = r"^(?:[^/]+/)?([^:]+)(?::[^:]+)?$"
    match = re.match(pattern, image_url)
    if not match:
        raise ValueError(f"Invalid Docker image format: {image_url}")
    return match.group(1)


def is_union_image(image: str):
    return image.startswith("cr.union.ai/")
