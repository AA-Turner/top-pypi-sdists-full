import os
from typing import Any, Mapping, Optional, Set, Tuple, cast

from dlt.common import logger
from dlt.common.validation import validate_dict, DictValidationException

from dlt.common.runtime.run_context import DOT_DLT

from dlt._workspace.profile import DEFAULT_PROFILE
from dlt._workspace.run_context import (
    default_working_dir,
    default_name,
    DEFAULT_WORKSPACE_WORKING_FOLDER,
    DEFAULT_LOCAL_FOLDER,
)

from dlthub.project.config.interpolation import InterpolateEnvironmentVariables
from dlthub.project.exceptions import ProfileNotFound, ProjectDocValidationError
from dlthub.project.config.typing import ProfileConfig, ProjectSettingsConfig, ProjectConfig
from dlthub.project.config.config import Project
from dlthub.project.config import yaml_loader
from dlthub.project.config.utils import clone_dict_nested, update_dict_nested


IMPLICIT_PROFILES = ["tests", "access"]


class ConfigLoader:
    def __init__(self, config_location: str, raw_config: Mapping[str, Any], validate: bool = False):
        if not config_location:
            raise ValueError("Project directory is required")

        # run validation on raw config
        try:
            validate_dict(ProjectConfig, raw_config, ".")
        except DictValidationException as ex:
            if validate:
                raise ProjectDocValidationError(config_location, str(ex)) from ex
            logger.warning(
                f"Project at location {config_location} contains invalid entities: {str(ex)}"
            )
            logger.warning(
                "Strict validation is not enabled by default, because we are still typing "
                " yaml config which may contain all possible OSS dlt configuration fields like "
                "toml configurations"
            )

        # store config file location, note that config may override project location
        self._config_location = config_location
        # safe to assign to type, raw config validated
        self.raw_config: ProjectConfig = raw_config  # type: ignore[assignment]

    def get_project_settings(self, profile_name: Optional[str]) -> ProjectSettingsConfig:
        """Gets project settings from raw config and sets defaults.
        Returns a deep clone of the raw settings
        """
        settings: ProjectSettingsConfig = clone_dict_nested(
            cast(ProjectSettingsConfig, self.raw_config.get("project", None) or {})
        )
        # set default profile
        settings["default_profile"] = settings.get("default_profile", DEFAULT_PROFILE)
        # get current profile name to calculate data and local dirs that depend on profile
        profile_name = self.get_profile_name(settings, profile_name)
        settings["current_profile"] = profile_name

        # set default paths if not present, keep the original paths
        project_dir = settings["project_dir"] = settings.get("project_dir", self._config_location)
        # set name from project_dir
        settings["name"] = settings.get("name", default_name(project_dir))
        settings["data_dir"] = settings.get(
            "data_dir",
            default_working_dir(
                project_dir,  # settings dir
                settings["name"],
                profile_name,
                os.path.join(DOT_DLT, DEFAULT_WORKSPACE_WORKING_FOLDER),  # settings dir
            ),
        )
        # set default local_dir dir
        settings["local_dir"] = settings.get(
            "local_dir",
            default_working_dir(
                project_dir,
                settings["name"],
                profile_name,
                DEFAULT_LOCAL_FOLDER,
            ),
        )

        # validate settings
        try:
            validate_dict(ProjectSettingsConfig, settings, "./project")
        except DictValidationException as ex:
            raise ProjectDocValidationError(self._config_location, str(ex)) from ex

        return settings

    def normalize_settings_paths(self, settings: ProjectSettingsConfig) -> ProjectSettingsConfig:
        """Normalizes paths in settings ie. to make path separators consistent"""
        settings["project_dir"] = os.path.normpath(settings["project_dir"])
        settings["data_dir"] = os.path.normpath(settings["data_dir"])
        settings["local_dir"] = os.path.normpath(settings["local_dir"])
        return settings

    def get_available_profiles(self, project_settings: ProjectSettingsConfig) -> Set[str]:
        # get all explicit profiles, add default profile and implicit
        profiles = set((self.raw_config.get("profiles") or {}).keys())
        profiles.add(project_settings["default_profile"])
        profiles.update(IMPLICIT_PROFILES)
        return profiles

    def get_profile_name(
        self,
        project_settings: ProjectSettingsConfig,
        profile_name: Optional[str],
    ) -> str:
        profile_name = profile_name or project_settings["default_profile"]
        available_profiles = self.get_available_profiles(project_settings)

        # raise if profile missing
        if profile_name not in available_profiles:
            raise ProfileNotFound(self._config_location, profile_name, available_profiles)

        return profile_name

    def get_profile(
        self,
        project_settings: ProjectSettingsConfig,
        profile_name: Optional[str],
    ) -> Tuple[str, ProfileConfig]:
        """Gets profile from raw config, will select default profile if not specified.
        Returns a deep clone of the raw profile
        """
        profile_name = self.get_profile_name(project_settings, profile_name)
        selected_profile = (self.raw_config.get("profiles") or {}).get(profile_name) or {}
        return profile_name, clone_dict_nested(selected_profile)

    def interpolate_config(
        self, config: ProjectConfig, settings: ProjectSettingsConfig
    ) -> Tuple[ProjectConfig, ProjectSettingsConfig]:
        """Interpolates config by running Python formatters on it, we execute two passes:
        - interpolate settings
        - interpolate config using interpolated settings
        """
        # first interpolate project config with self
        interpolator = InterpolateEnvironmentVariables(extra_vars=dict(settings))
        settings = self.normalize_settings_paths(interpolator.interpolate(settings))  # type: ignore

        # then interpolate project config with pre interpolated settings
        interpolator = InterpolateEnvironmentVariables(extra_vars=dict(settings))
        return interpolator.interpolate(config), settings  # type: ignore[arg-type,return-value]

    def get_project(self, profile_name: Optional[str] = None) -> Project:
        # get project settings with defaults
        project_settings = self.get_project_settings(profile_name)

        # get selected or default profile
        profile_name, profile_config = self.get_profile(project_settings, profile_name)

        # use clone to merge profile and settings - make sure raw_config is not modified
        merged_config: ProjectConfig = clone_dict_nested(self.raw_config)

        # merge project settings with defaults into config and merge profile into this
        # we do this so profiles may override project settings
        merged_config = update_dict_nested(merged_config, {"project": project_settings})
        merged_config = update_dict_nested(merged_config, profile_config)
        merged_project_settings = merged_config.pop("project")
        project = Project(*self.interpolate_config(merged_config, merged_project_settings))

        # Validate the merged configuration
        # TODO: we must allow additional properties ie. runtime or normalizer settings
        # the right approach would be to preserve known props or ignore additional props
        # commented out because demo project does not load
        # validate_dict(ProjectConfig, merged_config, ".")
        # TODO: generate json schema to validate yaml and enable autocomplete in editors
        # https://medium.com/@alexmolev/boost-your-yaml-with-autocompletion-and-validation-b74735268ad7
        # it is pretty easy to find SPECs for all known configurations and
        # convert them into JSON schema

        return project

    @classmethod
    def from_file(cls, file_path: str, validate: bool = False) -> "ConfigLoader":
        config = yaml_loader.load_file(file_path)
        return cls(os.path.dirname(file_path), config, validate=validate)

    @classmethod
    def from_string(
        cls, project_dir: str, yaml_string: str, validate: bool = False
    ) -> "ConfigLoader":
        config = yaml_loader.load_string(yaml_string)
        return cls(project_dir, config, validate=validate)

    @classmethod
    def from_dict(
        cls, project_dir: str, raw_config: Mapping[str, Any], validate: bool = False
    ) -> "ConfigLoader":
        return cls(project_dir, raw_config, validate=validate)
