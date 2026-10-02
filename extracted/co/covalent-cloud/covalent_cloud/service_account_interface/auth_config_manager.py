# Copyright 2023 Agnostiq Inc.

import os
from functools import partial
from pathlib import Path
from typing import Dict

import toml
import yaml

from ..shared.classes.settings import DataRobotRegion, Settings


class AuthConfigManager:
    @staticmethod
    def get_config_file(settings: Settings = None) -> str:
        """
        Returns the path to the config file.

        Args:
            settings: The settings object to use. If None, the default settings will be used.

        Returns:
            The path to the config file.

        """

        if settings is None:
            settings = Settings()

        path = Path(settings.auth.config_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        return str(path.resolve())

    @staticmethod
    def get_dr_config_file(settings: Settings = None) -> str:
        """
        Returns the path to the DataRobot config file. The 'DATAROBOT_CONFIG_FILE'
        environment variable takes precedence over the default config file path.

        Args:
            settings: The settings object to use. If None, the default settings will be used.

        Returns:
            The path to the DataRobot config file.

        """

        if settings is None:
            settings = Settings()

        # env override
        if dr_config_file := os.getenv("DATAROBOT_CONFIG_FILE"):
            path = Path(dr_config_file).expanduser().resolve()
            return str(path)

        dr_config_file = settings.auth.dr_config_file
        path = Path(settings.auth.dr_config_file).expanduser().resolve()
        path.parent.mkdir(parents=True, exist_ok=True)

        return str(path)

    @staticmethod
    def get_auth_request_headers(settings: Settings = None) -> Dict[str, str]:
        """
        Returns the headers to use for an authentication request.

        Args:
            settings: The settings object to use. If None, the default settings will be used.

        Returns:
            Authentication request headers as a dictionary.

        """

        if settings is None:
            settings = Settings()

        headers = {}

        if dr_api_token := AuthConfigManager.get_dr_api_token(settings):
            headers["Authorization"] = f"Bearer {dr_api_token}"

            dr_region = os.getenv("DATAROBOT_REGION", "") or settings.auth.dr_region
            headers["x-dr-region"] = DataRobotRegion.validate(dr_region)

        else:
            headers["x-api-key"] = AuthConfigManager.get_api_key(settings)

        return headers

    @staticmethod
    def save_token(token: str, settings: Settings = None) -> None:
        """
        Saves the authentication token to the config file.

        Args:
            token: The authentication token to save.
            settings: The settings object to use. If None, the default settings will be used.

        Returns:
            None

        """

        if settings is None:
            settings = Settings()

        auth_section_header = settings.auth.config_file_section
        token_keyname = settings.auth.config_file_token_keyname

        toml_dict = {auth_section_header: {}}
        toml_dict[auth_section_header][token_keyname] = token or ""

        with open(AuthConfigManager.get_config_file(settings), "w") as f:
            toml.dump(toml_dict, f)

    @staticmethod
    def get_token(settings: Settings = None) -> str:
        """
        Returns the authentication token from the config file.

        Args:
            settings: The settings object to use. If None, the default settings will be used.

        Returns:
            The authentication token.

        """

        if settings is None:
            settings = Settings()

        token = settings.auth.token
        if not token:
            auth_section_header = settings.auth.config_file_section
            token_keyname = settings.auth.config_file_token_keyname

            with open(AuthConfigManager.get_config_file(settings), "r") as f:
                toml_string = f.read()
                parsed_toml = toml.loads(toml_string)
                token = parsed_toml[auth_section_header][token_keyname]
        return token

    @staticmethod
    def get_dr_api_token(settings: Settings = None) -> str:
        """
        Returns the DataRobot API token from the DataRobot config file or environment variables,
        with the latter taking precedence over the former.

        The 'DATAROBOT_API_TOKEN' environment variable is checked first. If it is not set, the
        DataRobot config file is checked for the 'token' key. The config file path is
        determined by the 'DATAROBOT_CONFIG_FILE' environment variable, if set, else the
        default location.

        An empty string is returned if the environment variable is not set and the config file
        does not exist or does not contain the token.

        Args:
            settings: The settings object to use. If None, the default settings will be used.

        Returns:
            The DataRobot API token or an empty string if not found.

        """

        if settings is None:
            settings = Settings()

        # env override
        if dr_api_token := os.getenv("DATAROBOT_API_TOKEN"):
            return dr_api_token

        # settings override
        if dr_api_token := settings.auth.dr_api_token:
            return dr_api_token

        # config file
        dr_config_file = AuthConfigManager.get_dr_config_file(settings)
        if Path(dr_config_file).is_file():
            with open(dr_config_file, "r", encoding="utf-8") as f:
                return yaml.load(f, Loader=yaml.SafeLoader).get("token") or ""

        return ""

    @staticmethod
    def save_dr_api_token(dr_api_token: str, settings: Settings = None) -> None:
        """
        Saves the DataRobot API token to the DataRobot config file.

        Args:
            dr_api_token: The DataRobot API token to save.
            settings: The settings object to use. If None, the default settings will be used.

        Returns:
            None

        """

        if settings is None:
            settings = Settings()

        dr_config_file = AuthConfigManager.get_dr_config_file(settings)

        config: dict = {}
        if Path(dr_config_file).is_file():
            with open(dr_config_file, "r", encoding="utf-8") as f:
                config = yaml.load(f, Loader=yaml.SafeLoader) or {}

        config.update(token=str(dr_api_token))

        with open(dr_config_file, "w", encoding="utf-8") as f:
            yaml.dump(config, f, Dumper=yaml.SafeDumper)

    @staticmethod
    def get_api_key(settings: Settings = None) -> str:
        """
        Returns the API key from the config file.

        Args:
            settings: The settings object to use. If None, the default settings will be used.

        Returns:
            The API key.

        """

        if settings is None:
            settings = Settings()

        api_key = settings.auth.api_key

        if not api_key:
            auth_section_header = settings.auth.config_file_section
            api_keyname = settings.auth.config_file_api_key_keyname

            if not Path(settings.auth.config_file).is_file():
                return ""

            with open(AuthConfigManager.get_config_file(settings), "r") as f:
                toml_string = f.read()
                parsed_toml = toml.loads(toml_string)
                api_key = parsed_toml[auth_section_header][api_keyname]

        return api_key

    @staticmethod
    def save_api_key(api_key: str, settings: Settings = None) -> None:
        """
        Saves the API key to the config file.

        Args:
            api_key: The API key to save.
            settings: The settings object to use. If None, the default settings will be used.

        Returns:
            None

        """

        if settings is None:
            settings = Settings()

        auth_section_header = settings.auth.config_file_section

        api_keyname = settings.auth.config_file_api_key_keyname

        toml_dict = {auth_section_header: {}}
        toml_dict[auth_section_header][api_keyname] = api_key or ""

        with open(AuthConfigManager.get_config_file(settings), "w") as f:
            toml.dump(toml_dict, f)


get_token = partial(AuthConfigManager.get_token)
save_token = partial(AuthConfigManager.save_token)

get_api_key = partial(AuthConfigManager.get_api_key)
save_api_key = partial(AuthConfigManager.save_api_key)

get_dr_api_token = partial(AuthConfigManager.get_dr_api_token)
save_dr_api_token = partial(AuthConfigManager.save_dr_api_token)
