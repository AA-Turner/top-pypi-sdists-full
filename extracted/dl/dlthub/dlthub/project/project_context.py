import os
import re
import sys
import argparse
from types import ModuleType
import tomlkit
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import dlt
from dlt.common.configuration.specs import RuntimeConfiguration
from dlt.common.configuration.specs.pluggable_run_context import (
    ProfilesRunContext,
    PluggableRunContext,
)
from dlt.common.configuration.container import Container
from dlt.common.configuration.providers import (
    EnvironProvider,
    ConfigTomlProvider,
)
from dlt.common.configuration.providers.provider import ConfigProvider
from dlt.common.runtime.init import initialize_runtime
from dlt.common.runtime.run_context import RunContext, DOT_DLT, global_dir, context_uri
from dlt.common.typing import copy_sig_ret

from dlt._workspace.providers import ProfileSecretsTomlProvider
from dlt._workspace.run_context import (
    switch_profile as _switch_profile,
    switch_context as _switch_context,
)
from dlt._workspace.profile import read_profile_pin

from dlthub.common.constants import DEFAULT_PROJECT_CONFIG_FILE
from dlthub.common.license import ensure_license_with_scope

from .config.config import Project, ProjectConfiguration
from .config.config_loader import ConfigLoader
from .exceptions import ProjectRunContextNotAvailable


class ProjectRunContext(ProfilesRunContext):
    def __init__(self, project: Project):
        self._project: Project = project
        self._config: ProjectConfiguration = None
        self._adhoc_sys_path: str = None

    @property
    def name(self) -> str:
        """Returns run dlt package name: as defined in the project yaml or the parent folder name
        if not defined"""
        return self._project.name

    @property
    def global_dir(self) -> str:
        """Directory in which global settings are stored ie ~/.dlt/"""
        return global_dir()

    @property
    def uri(self) -> str:
        return context_uri(self.name, self.run_dir, self.runtime_kwargs)

    @property
    def run_dir(self) -> str:
        """A folder containing dlt project code"""
        return self._project.settings["project_dir"]

    @property
    def settings_dir(self) -> str:
        """Defines where the current settings (secrets and configs) are located"""
        return os.path.join(self.run_dir, DOT_DLT)

    @property
    def data_dir(self) -> str:
        """Pipeline working dirs, other writable folders, local destination files (default).
        Default data_dir isolates by profile name
        """
        return self._project.settings["data_dir"]

    @property
    def local_dir(self) -> str:
        """Destination local files, by default at `.dlt/data/<profile>` under `run_dir`"""
        return self._project.settings["local_dir"]

    def initial_providers(self) -> List[ConfigProvider]:
        providers = [
            EnvironProvider(),
            # load secrets from profiled tomls ie. dev.secrets.toml. use secrets.toml as global
            ProfileSecretsTomlProvider(
                self.settings_dir, self.project.current_profile, self.global_dir
            ),
            # use regular config.toml without profiles, allow for global settings
            ConfigTomlProvider(self.settings_dir, self.global_dir),
            # add project as config provider
            self._project.provider(provider_name=self.name),
        ]
        return providers

    def initialize_runtime(self, runtime_config: RuntimeConfiguration = None) -> None:
        if runtime_config is not None:
            self.config.runtime = runtime_config

        # this also resolves workspace config if necessary
        initialize_runtime(self.name, self.config.runtime)

    @property
    def runtime_config(self) -> RuntimeConfiguration:
        return self.config.runtime

    @property
    def config(self) -> ProjectConfiguration:
        if self._config is None:
            from dlt.common.configuration.resolve import resolve_configuration

            self._config = resolve_configuration(
                ProjectConfiguration(project_config=self._project.config)
            )

        return self._config

    def reset_config(self) -> None:
        self._config = None

    @property
    def module(self) -> Optional[ModuleType]:
        try:
            return RunContext.import_run_dir_module(self.run_dir)
        except ImportError:
            return None

    @property
    def runtime_kwargs(self) -> Dict[str, Any]:
        return {"profile": self.profile}

    def get_data_entity(self, entity: str) -> str:
        """Gets path in data_dir where `entity` (ie. `pipelines`, `repos`) are stored"""
        return os.path.join(self.data_dir, entity)

    def get_run_entity(self, entity: str) -> str:
        """Gets path in run_dir where `entity` (ie. `sources`, `destinations` etc.) are stored"""
        return os.path.join(self.run_dir, entity)

    def get_setting(self, setting_path: str) -> str:
        """Gets path in settings_dir where setting (ie. `secrets.toml`) are stored"""
        return os.path.join(self.settings_dir, setting_path)

    def unplug(self) -> None:
        # remove added sys path
        if self._adhoc_sys_path:
            if self._adhoc_sys_path in sys.path:
                sys.path.remove(self._adhoc_sys_path)
            self._adhoc_sys_path = None

    def plug(self) -> None:
        # validate license
        ensure_license_with_scope("dlthub.project")
        # add to syspath
        self._adhoc_sys_path = self.ensure_importable(self.run_dir)
        # create temp and data dirs
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.local_dir, exist_ok=True)

    # SupportsProfilesOnContext

    @property
    def profile(self) -> str:
        return self._project.current_profile

    @property
    def default_profile(self) -> str:
        return self._project.default_profile

    def available_profiles(self) -> List[str]:
        return list(self.project.profiles.keys())

    def configured_profiles(self) -> List[str]:
        return self.available_profiles()

    def switch_profile(self, new_profile: str) -> "ProjectRunContext":
        """Switches current profile and returns new run context"""
        return switch_context(self.run_dir, profile=new_profile, required="ProjectRunContext")

    # Project specific

    @property
    def project(self) -> Project:
        return self._project

    @project.setter
    def project(self, project: Project) -> None:
        self._project = project

    def switch_context(
        self, project_dir: Optional[str], profile: str = None
    ) -> "ProjectRunContext":
        """Switches the context to `project_dir` and `profile` is provided"""
        return switch_context(project_dir, profile=profile, required="ProjectRunContext")

    def reload(self) -> "ProjectRunContext":
        """Reloads current context, puts it into container and returns new instance"""
        return switch_context(self.run_dir, self.profile, required="ProjectRunContext")

    @staticmethod
    def ensure_importable(run_dir: str) -> Optional[str]:
        """Adds current project to syspath if it is not a module already.

        Allow to create an ad hoc flat Python packages.
        Returns new syspath if added
        """
        try:
            # try to import as regular package
            RunContext.import_run_dir_module(run_dir)
            return None
        except ImportError:
            # add to syspath if necessary
            if run_dir in sys.path:
                return None
            sys.path.append(run_dir)
            return run_dir


switch_context = copy_sig_ret(_switch_context, ProjectRunContext)(_switch_context)
switch_profile = copy_sig_ret(_switch_profile, ProjectRunContext)(_switch_profile)


def active() -> ProjectRunContext:
    """Returns currently active project context"""
    ctx = Container()[PluggableRunContext].context
    if not isinstance(ctx, ProjectRunContext):
        raise ProjectRunContextNotAvailable(ctx.run_dir)
    return ctx


@dataclass
class InstalledDltPackageInfo:
    package_name: str
    module_name: str
    docstring: str
    license_scopes: str = None


def create_project_context(
    project_dir: str, profile: str = None, validate: bool = False
) -> ProjectRunContext:
    """Creates a project context in `project_dir` and switches to `profile`.

    - Uses dlt.yml if found in `project_dir`
    - Otherwise creates a project with an empty (default) config
    - Makes sure that Python code in `project_dir` is importable

    If dirname(project_dir) is a Python module: all OK (package structure)
    NOTE: If not we assume flat structure and we add project_dir to syspath
    """
    project_dir = os.path.abspath(project_dir)
    manifest_path = os.path.join(project_dir, DEFAULT_PROJECT_CONFIG_FILE)
    if os.path.isfile(manifest_path):
        config_loader = ConfigLoader.from_file(
            os.path.join(project_dir, DEFAULT_PROJECT_CONFIG_FILE), validate=validate
        )
    else:
        config_loader = ConfigLoader.from_dict(project_dir, {}, validate=validate)
    return _create_run_context_from_ConfigLoader(profile, config_loader)


def create_empty_project_context(project_dir: str, profile: str = None) -> ProjectRunContext:
    """Creates an empty project context in `project_dir` and switches to `profile`.
    - Makes sure that Python code in `project_dir` is importable

    If dirname(project_dir) is a Python module: all OK (package structure)
    NOTE: If not we assume flat structure and we add project_dir to syspath
    """
    config_loader = ConfigLoader.from_dict(project_dir, {})
    return _create_run_context_from_ConfigLoader(profile, config_loader)


def _create_run_context_from_ConfigLoader(
    profile: str, config_loader: ConfigLoader
) -> ProjectRunContext:
    # make preliminary context to access settings
    context = ProjectRunContext(config_loader.get_project())
    profile = profile or read_profile_pin(context)
    project = config_loader.get_project(profile_name=profile)
    # bind project to context
    context.project = project
    return context


# def import_context_from_dir(project_dir: str, profile: str = None) -> None:
#     """(POC) Imports entities in a given context.
#     Initial version to prove the concept of separate imports"""
#     ctx = create_project_context(project_dir, profile=profile)

#     with injected_run_context(ctx):
#         # TODO: allow to import script from folder that are package (__init__.py) and without
#         # TODO: we assume that __init__ import all sources
#         import_pipeline_script(ctx.run_dir, "sources")


def import_context_from_dist(dist: str) -> None:
    """Import entities form a Python distribution `dist` which contains run context"""
    raise NotImplementedError()


# def find_module_run_dir(module_: str) -> str:
#     """Finds run context in `dist` that follows standard package layout"""
#     if dist is None:
#         # use pyproject


def find_pyproject_project_dir(dist_path: str) -> str:
    """Finds run context by inspecting pyproject.toml in distribution path `dist_path`

    1. pyproject that explicitly defines Python package via `dlt_package` entry point
    2. if not, we use package name to identify Python module path where we expect the project_dir

    In case of (2) project dir must contain dlt.yml or .dlt
    """
    dist_path = os.path.abspath(dist_path)

    # load pyproject or exit
    pyproject_path = os.path.join(dist_path, "pyproject.toml")
    if not os.path.isfile(pyproject_path):
        return None
    with open(pyproject_path, "r", encoding="utf-8") as f:
        pyproject_data = tomlkit.load(f)

    # check explicit pointer to dlt package
    package_ep = ((pyproject_data.get("project") or {}).get("entry-points") or {}).get(
        "dlt_package"
    )
    if package_ep:
        package_name = package_ep.get("dlt-project")
    else:
        package_name = (pyproject_data.get("project") or {}).get("name")

    if not package_name:
        return None
    # convert the package name to a valid module directory name
    package_dir_name = re.sub(r"\W|^(?=\d)", "_", package_name.lower())

    # support two layouts
    for src_dir in [package_dir_name, os.path.join("src", package_dir_name)]:
        project_dir = os.path.join(dist_path, src_dir)
        if os.path.isdir(project_dir):
            if package_ep or is_project_dir(project_dir):
                return project_dir
    return None


def find_project_dir(start_dir: str = None) -> str:
    """Look for dlt project dir, starting in `start_dir` or cwd(), with following rules:

    - look for `pyproject.toml` and check if it points to dlt project
    - if not look for dlt.yml or .dlt folder is found
    - if not, look recursively up from cwd() until, go to 1
    - stop looking when root folder dlt global dir (home dir) is reached and return cwd

    Returns project dir
    """

    current_dir = start_dir or os.getcwd()
    root_dir = os.path.abspath(os.sep)  # platform-independent root directory
    dlt_global_dir = os.path.dirname(global_dir())

    while True:
        if current_dir == dlt_global_dir:
            # Reached global dir (ie. home directory), end of search
            return None
        if is_project_dir(current_dir):
            return current_dir
        if pyproject_dir := find_pyproject_project_dir(current_dir):
            return pyproject_dir
        if current_dir == root_dir:
            # Reached the root directory without finding the file
            return None
        # Move up one directory level
        current_dir = os.path.dirname(current_dir)


def is_project_dir(project_dir: str) -> bool:
    """Checks if `project_dir` contains dlt project, this is true if a config file is found"""
    if os.path.isfile(os.path.join(project_dir, DEFAULT_PROJECT_CONFIG_FILE)):
        return True
    # if os.path.isdir(os.path.join(project_dir, DOT_DLT)):
    #     return True
    return False


def ensure_project(run_dir: str = None, profile: str = None) -> ProjectRunContext:
    """Ensures that project at `run_dir` with `profile` is active in the container."""
    context = dlt.current.run_context()

    # check if run_dir is within current context, if so do not reload it
    if run_dir:
        # this is a wrong way to check if run_dir is within current project
        # TODO: handle a project within a project. ie. we have many projects defined within test
        #  one. most probably we need to always use find_project_dir and see if path changed...
        if os.path.abspath(run_dir).startswith(os.path.abspath(context.run_dir)) and isinstance(
            context, ProjectRunContext
        ):
            run_dir = None
        else:
            # find project dir, if not found raise immediately
            project_dir = find_project_dir(start_dir=run_dir)
            if project_dir is None:
                raise ProjectRunContextNotAvailable(run_dir)
            else:
                run_dir = project_dir
    if run_dir:
        # switch project in explicit path
        context = switch_context(run_dir, profile, required="ProjectRunContext")
    elif profile:
        # only switch profile
        context = switch_profile(profile)

    if not isinstance(context, ProjectRunContext):
        raise ProjectRunContextNotAvailable(context.run_dir)
    return context


def list_dlt_packages() -> List[InstalledDltPackageInfo]:
    """Lists Python packages that contain modules with dlt packages.
    Returns list of tuples (package name, module name, first line of docstring)
    """
    import importlib.metadata
    from dlt._workspace.cli import echo as fmt

    packages: List[InstalledDltPackageInfo] = []
    for dist in importlib.metadata.distributions():
        package_name = dist.metadata.get("Name")  # type: ignore[attr-defined]
        if not package_name:
            continue

        entry_points = dist.entry_points

        # try to read package info
        package_info: InstalledDltPackageInfo = None
        # filter entry points under 'dlt_package'
        dlt_package_eps = [ep for ep in entry_points if ep.group == "dlt_package"]
        if dlt_package_eps:
            for ep in dlt_package_eps:
                if ep.name == "dlt-project":
                    module_name = ep.value
                    try:
                        module = importlib.import_module(module_name)
                        # get the module-level docstring
                        docstring = module.__doc__ or ""
                        fl = docstring.strip().split("\n")[0]
                        package_info = InstalledDltPackageInfo(package_name, module_name, fl)
                    except Exception as e:
                        fmt.error(f"Error processing {package_name}, module {module_name}: {e}")
        if package_info:
            packages.append(package_info)
    return packages


def project_from_args(args: argparse.Namespace) -> ProjectRunContext:
    if args.project and not os.path.exists(args.project):
        import importlib

        try:
            module = importlib.import_module(args.project)
            args.project = os.path.dirname(os.path.abspath(module.__file__))
        except ImportError:
            pass
    return ensure_project(args.project, profile=args.profile)
