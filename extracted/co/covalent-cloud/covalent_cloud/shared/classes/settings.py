# Copyright 2023 Agnostiq Inc.

import os
from enum import Enum
from pathlib import Path
from typing import Union

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DataRobotRegion(str, Enum):
    """
    Region prefixes for DataRobot production URLs.

    e.g. https://app.datarobot.com => "USA"
    e.g. https://app.eu.datarobot.com => "Europe"
    e.g. https://app.jp.datarobot.com => "Japan"

    """

    USA = ""  # No prefix for USA, is default region
    EUROPE = "eu"
    JAPAN = "jp"

    @classmethod
    def validate(cls, region: str) -> str:
        """Validate the region prefix."""
        valid_regions = list(cls._value2member_map_.keys())

        region = region.lower()
        if region in valid_regions:
            return cls(region).value

        raise ValueError(
            f"Unknown DataRobot region prefix '{region}'. Valid prefixes are {valid_regions}"
        )


class AuthSettings(BaseModel):
    """
    Authentication settings.

    token: Authentication token.
    api_key: API key.
    config_file: Path to the config file. Defaults to "~/.config/covalent_cloud/credentials.toml".
    config_file_section: Section in the config file. Defaults to "auth".
    config_file_token_keyname: Keyname for the token in the config file. Defaults to "token".
    config_file_api_key_keyname: Keyname for the API key in the config file. Defaults to "api_key".
    dr_api_token: DataRobot API token.
    dr_config_file: Path to the DataRobot config file. Defaults to "~/.config/datarobot/drconfig.yaml".
    """

    token: str = ""  # AUTH__TOKEN env
    api_key: str = ""  # api_key
    config_file: str = str(
        Path.home() / ".config/covalent_cloud/credentials.toml"
    )  # AUTH__CONFIG_FILE env

    config_file_section: str = "auth"
    config_file_token_keyname: str = "token"
    config_file_api_key_keyname: str = "api_key"

    dr_api_token: str = ""
    dr_region: str = ""
    dr_config_file: str = str(Path.home() / ".config/datarobot/drconfig.yaml")


class RedispatchSettings(BaseModel):
    # Note: Internal use only, do not add docstring
    id: str = ""

    @property
    def is_redispatch(self):
        return self.id != ""


class FunctionServeSettings(BaseModel):
    # Note: Internal use only, do not add docstring

    min_executor_memory_gb: int = 4
    recommended_executor_memory_gb: int = 12


class Settings(BaseSettings):
    """
    Settings for the Covalent Cloud.

    auth: Authentication settings.
    dispatcher_uri: URI for the dispatcher. Defaults to "https://api.covalent.xyz".
    dispatcher_port: Port for the dispatcher. Defaults to None.
    dispatch_cache_dir: Directory for the dispatch cache. Defaults to "~/.cache/covalent/dispatches".
    results_dir: Directory for the results. Defaults to "~/.cache/covalent/results".
    validate_executors: Whether to validate executors. Defaults to True.

    """

    auth: AuthSettings = AuthSettings()
    redispatch: RedispatchSettings = (
        RedispatchSettings()
    )  # Note: Internal use only, do not add to docstring

    function_serve: FunctionServeSettings = (
        FunctionServeSettings()
    )  # Note: Internal use only, do not add to docstring

    dispatcher_uri: str = "https://api.covalent.xyz"
    dispatcher_port: Union[int, None] = None

    # Note: consider using `home_folder = os.path.expanduser('~')` instead of `os.environ["HOME"]`
    dispatch_cache_dir: str = os.environ["HOME"] + "/.cache" + "/covalent/dispatches"
    results_dir: str = os.environ["HOME"] + "/.cache" + "/covalent/results"

    validate_executors: bool = True
    model_config = SettingsConfigDict(env_prefix="COVALENT_CLOUD_", env_nested_delimiter="__")


settings = Settings()
