#
# Copyright 2021-2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Mapping, Optional, Type

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_settings.sources import EnvSettingsSource, PydanticBaseSettingsSource

# Support both old and new locations of parse_env_vars
try:
    # Older versions (< 2.3.0) have parse_env_vars in pydantic_settings.sources
    from pydantic_settings.sources import parse_env_vars  # type: ignore[attr-defined,unused-ignore]
except ImportError:
    # Newer versions have it in pydantic_settings.sources.utils
    from pydantic_settings.sources.utils import parse_env_vars  # type: ignore[no-redef,unused-ignore]


def getenv(name: str, default: Optional[str] = None) -> Optional[str]:
    """
    Custom getenv function that checks for Runtime Parameters first.
    """
    rt_name = f"MLOPS_RUNTIME_PARAM_{name}"

    raw = os.getenv(rt_name)

    if raw is None:
        return os.getenv(name, default)

    try:
        value = json.loads(raw)
    except json.JSONDecodeError:
        # not a json, but some primitive type, so return it right away
        return raw

    if isinstance(value, dict):
        if value.get("type") == "string":
            return str(value["payload"])
        if len(value) == 1:
            return str(list(value.values())[0])
        elif "payload" in value:
            payload = value["payload"]
            if "apiToken" in payload:
                return str(payload["apiToken"])

    return raw


class PulumiConfigSettingsSource(EnvSettingsSource):  # type: ignore[misc,unused-ignore]
    """A source class that takes settings from a pulumi_config.json file."""

    def __init__(
        self,
        settings_cls: Type[BaseSettings],
        pulumi_config_file: Optional[str] = None,
        pulumi_config_file_encoding: Optional[str] = None,
        **kwargs: Any,
    ):
        self.pulumi_config_file = pulumi_config_file
        self.pulumi_config_file_encoding = pulumi_config_file_encoding
        super().__init__(settings_cls, **kwargs)

    def _find_config_file(self, config_file: str) -> Optional[Path]:
        """Find config file by searching up the directory tree like .env files."""
        config_path = Path(config_file)

        # If it's an absolute path, just return it if it exists
        if config_path.is_absolute():
            return config_path if config_path.is_file() else None

        # Search from current directory up to root
        cwd = Path.cwd()
        for path in [cwd, *cwd.parents]:
            potential_path = path / config_file
            if potential_path.is_file():
                return potential_path

        return None

    def _load_env_vars(self) -> Mapping[str, Optional[str]]:
        """Load environment variables with pulumi config values as fallback."""
        # Get normal environment variables first
        env_vars = dict(super()._load_env_vars())

        # Load pulumi config and add to env_vars (not os.environ)
        pulumi_config_file = self.pulumi_config_file or "pulumi_config.json"
        pulumi_config_path = self._find_config_file(pulumi_config_file)

        if pulumi_config_path is not None:
            encoding = self.pulumi_config_file_encoding or "utf-8"
            with open(pulumi_config_path, encoding=encoding) as f:
                file_data = json.load(f)

            if isinstance(file_data, dict):
                # Add pulumi config values for each field (only if not already in env)
                for field_name in self.settings_cls.model_fields.keys():
                    env_key = field_name.upper()

                    # Skip if already set in environment
                    if env_key in env_vars and env_vars[env_key]:
                        continue

                    value = None
                    if field_name in file_data:
                        value = file_data[field_name]
                    elif env_key in file_data:
                        value = file_data[env_key]

                    if value is not None and value != "":
                        env_vars[env_key] = str(value)

        return parse_env_vars(  # type: ignore[no-any-return,unused-ignore]
            env_vars,
            self.case_sensitive,
            self.env_ignore_empty,
            self.env_parse_none_str,
        )

    def __repr__(self) -> str:
        return (
            f"PulumiConfigSettingsSource("
            f"pulumi_config_file={self.pulumi_config_file!r}, "
            f"pulumi_config_file_encoding={self.pulumi_config_file_encoding!r})"
        )


class GetenvSettingsSource(EnvSettingsSource):  # type: ignore[misc,unused-ignore]
    """A source class that uses the custom getenv function."""

    def _load_env_vars(self) -> Mapping[str, Optional[str]]:
        """Load environment variables using the custom getenv function."""
        # Start with normal environment variables
        env_vars = dict(super()._load_env_vars())

        # Override with custom getenv for each field
        for field_name in self.settings_cls.model_fields.keys():
            env_key = field_name.upper()
            value = getenv(env_key)
            if value is not None and value != "":
                env_vars[env_key] = value

        return parse_env_vars(  # type: ignore[no-any-return,unused-ignore]
            env_vars,
            self.case_sensitive,
            self.env_ignore_empty,
            self.env_parse_none_str,
        )

    def __repr__(self) -> str:
        return "GetenvSettingsSource()"


class DataRobotAppFrameworkBaseSettings(BaseSettings):  # type: ignore[misc,unused-ignore]
    """
    Base settings class that uses custom source priority:
    1. env variables (including Runtime Parameters)
    2. .env file
    3. file_secrets
    4. pulumi_config.json (fallback)

    Sample usage:

    class Config(DataRobotAppFrameworkBaseSettings):
        my_variable: str = "default_value"
        another_variable: Optional[int]
    config = Config()
    assert config.my_variable == "value_from_env_or_pulumi_or_default"

    Now, however the variable is set, it will pull it in working both locally and once
    deployed in DataRobot to support credentials and basic variables for RuntimeParameters
    in both Custom Applications and Custom Models.
    """

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            GetenvSettingsSource(settings_cls),
            dotenv_settings,
            file_secret_settings,
            PulumiConfigSettingsSource(settings_cls),
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
