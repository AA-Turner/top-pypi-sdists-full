from __future__ import annotations

import logging
import os
import sys
import textwrap
from pathlib import Path
from pprint import pformat
from typing import TYPE_CHECKING

from setuptools_git_versioning.defaults import set_default_options
from setuptools_git_versioning.factories import add_to_sys_path
from setuptools_git_versioning.log import DEBUG, INFO
from setuptools_git_versioning.version import version_from_git

if TYPE_CHECKING:
    # avoid importing 'packaging' because setuptools-git-versioning can be installed using sdist
    # where 'packaging' is not installed yet
    from packaging.version import Version
    from setuptools.dist import Distribution

log = logging.getLogger(__name__)


def read_toml(name_or_path: str | os.PathLike = "pyproject.toml", root: str | os.PathLike | None = None) -> dict:
    project_root = Path(root) if root else Path.cwd()
    file_path = project_root.joinpath(name_or_path)
    if not file_path.exists():
        log.log(INFO, "'%s' does not exist", file_path)
        return {}

    if not file_path.is_file():
        msg = f"'{file_path}' is not a file"
        raise OSError(msg)

    log.log(INFO, "Trying 'pyproject.toml' ...")
    try:
        # for Python 3.11+
        import tomllib

        with file_path.open("rb") as file:
            parsed_file = tomllib.load(file)
    except (ImportError, NameError):
        import tomli

        with file_path.open("rb") as file:
            parsed_file = tomli.load(file)

    result = parsed_file.get("tool", {}).get("setuptools-git-versioning", None)
    if result:
        log.log(DEBUG, "'tool.setuptools-git-versioning' section content:\n%s", pformat(result))
    return result


def infer_version(dist: Distribution, root: str | os.PathLike | None = None) -> Version | None:
    log.log(INFO, "Trying 'setup.py' ...")

    # see above
    import setuptools  # isort: skip  # noqa: F401

    from distutils.errors import DistutilsOptionError, DistutilsSetupError

    config = getattr(dist, "setuptools_git_versioning", None)
    toml_config = read_toml(root=root)

    if config is None:
        config = toml_config
    elif toml_config:
        msg = (
            "Both 'setup.py' and 'pyproject.toml' have 'setuptools_git_versioning' config section. "
            "Please remove one of them"
        )
        raise DistutilsSetupError(msg)

    if config is None:
        # Nothing to do here
        return None

    if not isinstance(config, dict):
        msg = f"Wrong config format. Expected dict, got: {config}"
        raise DistutilsOptionError(msg)

    if not config or not config.pop("enabled", True):
        # Nothing to do here
        return None

    set_default_options(config)

    version = version_from_git(dist.metadata.name, **config, root=root)
    dist.metadata.version = str(version)
    return version


def infer_setup_py(name_or_path: str = "setup.py", root: str | os.PathLike | None = None) -> Version | None:
    project_root = Path(root) if root else Path.cwd()
    setup_py_path = project_root.joinpath(name_or_path)
    if not setup_py_path.exists():
        log.log(INFO, "'%s' does not exist", setup_py_path)
        return None

    # because we use distutils in this file, we need to ensure that setuptools is
    # imported first so that it can do monkey patching. this is not always already
    # done for us, for example, when running this in a test or as a module
    import setuptools  # isort: skip  # noqa: F401

    from distutils.core import run_setup

    # distutils does not change current directory, causing version of 'setuptools_git_versioning'
    # is being get instead of target package.
    # also some setup.py files can contain imports of other files from the package,
    # and if they will be missing from sys.path, import will fail.
    # emulating `python setup.py` call by modifying current dir and sys.path, but restore everything back after import
    original_cwd = os.getcwd()  # noqa: PTH109
    original_sys_path = sys.path.copy()
    original_sys_modules = sys.modules.copy()
    try:
        add_to_sys_path(project_root)
        os.chdir(project_root)
        dist = run_setup(os.fspath(setup_py_path), stop_after="init")
        return infer_version(dist, root=root)
    finally:
        sys.path[:] = original_sys_path
        sys.modules = original_sys_modules
        os.chdir(original_cwd)


def get_version(config: dict | None = None, root: str | os.PathLike | None = None) -> Version:
    if not config:
        log.log(INFO, "No explicit config passed")
        log.log(INFO, "Searching for config files in '%s' folder", root or Path.cwd())
        result = infer_setup_py(root=root)
        if result is not None:
            return result

        config = read_toml(root=root)

    if not config or not config.pop("enabled", True):
        raise RuntimeError(
            textwrap.dedent(
                f"""
                'setuptools-git-versioning' command can be used only
                with 'pyproject.toml' or 'setup.py' file present in folder '{root or Path.cwd()}',
                containing the 'enabled: True' setting
                (see https://setuptools-git-versioning.readthedocs.io/en/stable/install.html)
                """,
            ),
        )

    set_default_options(config)
    return version_from_git(**config, root=root)
