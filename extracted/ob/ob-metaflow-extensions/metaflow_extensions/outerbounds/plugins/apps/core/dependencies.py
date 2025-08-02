import copy
import json
import os
import shutil
import sys
import tempfile
from hashlib import sha256
from typing import List, Optional, Callable, Any
from .app_config import AppConfig
from .utils import TODOException
from metaflow.metaflow_config import (
    get_pinned_conda_libs,
    DEFAULT_DATASTORE,
    KUBERNETES_CONTAINER_IMAGE,
)
from collections import namedtuple

BakingStatus = namedtuple(
    "BakingStatus", ["image_should_be_baked", "python_path", "resolved_image"]
)


class ImageBakingException(Exception):
    pass


def _safe_open_file(path: str):
    if not os.path.exists(path):
        raise ImageBakingException(f"File does not exist: {path}")
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        raise ImageBakingException(f"Failed to open file: {e}")


def bake_deployment_image(
    app_config: AppConfig,
    cache_file_path: str,
    logger: Optional[Callable[[str], Any]] = None,
) -> BakingStatus:
    # When do we bake an image?
    # 1. When the user has specified something like `pypi`/`conda`
    # 2, When the user has specified something like `from_requirements`/ `from_pyproject`
    # TODO: add parsers for the pyproject/requirements stuff.
    from metaflow.ob_internal import bake_image  # type: ignore
    from metaflow.plugins.pypi.parsers import (
        requirements_txt_parser,
        pyproject_toml_parser,
    )

    image = app_config.get("image", KUBERNETES_CONTAINER_IMAGE)
    python_version = "%d.%d.%d" % sys.version_info[:3]

    dependencies = app_config.get_state("dependencies", {})
    pypi_packages = {}
    conda_packages = {}

    parsed_packages = {}

    if dependencies.get("from_requirements_file"):
        parsed_packages = requirements_txt_parser(
            _safe_open_file(dependencies.get("from_requirements_file"))
        )
        pypi_packages = parsed_packages.get("packages", {})
        python_version = parsed_packages.get("python_version", python_version)

    elif dependencies.get("from_pyproject_toml"):
        parsed_packages = pyproject_toml_parser(
            _safe_open_file(dependencies.get("from_pyproject_toml"))
        )
        pypi_packages = parsed_packages.get("packages", {})
        python_version = parsed_packages.get("python_version", python_version)

    elif "pypi" in dependencies:
        pypi_packages = dependencies.get("pypi", {}) or {}

    if "conda" in dependencies:
        conda_packages = dependencies.get("conda", {}) or {}
    if "python" in dependencies:
        python_version = dependencies.get("python", python_version) or python_version

    python_packages_exist = len(pypi_packages) > 0 or len(conda_packages) > 0
    if (not python_packages_exist) or app_config.get_state("skip_dependencies", False):
        # Inform the user that no dependencies are being used.
        if app_config.get_state("skip_dependencies", False) and logger:
            logger(
                "⏭️ Skipping baking dependencies into the image based on the --no-deps flag."
            )
        # TODO: Handle this a little more nicely.
        return BakingStatus(
            image_should_be_baked=False, resolved_image=image, python_path="python"
        )

    pinned_conda_libs = get_pinned_conda_libs(python_version, DEFAULT_DATASTORE)
    pypi_packages.update(pinned_conda_libs)
    _reference = app_config.get("name", "default")
    # `image` cannot be None. If by chance it is none, FB will fart.
    fb_response = bake_image(
        cache_file_path=cache_file_path,
        pypi_packages=pypi_packages,
        conda_packages=conda_packages,
        ref=_reference,
        python=python_version,
        base_image=image,
        logger=logger,
    )
    if fb_response.failure:
        raise ImageBakingException(f"Failed to bake image: {fb_response.response}")

    return BakingStatus(
        image_should_be_baked=True,
        resolved_image=fb_response.container_image,
        python_path=fb_response.python_path,
    )
