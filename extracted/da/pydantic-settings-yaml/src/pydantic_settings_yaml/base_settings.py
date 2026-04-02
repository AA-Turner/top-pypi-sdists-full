import os
import re
from pathlib import Path
from typing import Any, Dict, Tuple, Type

import yaml
from pydantic.fields import FieldInfo
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)


def replace_secrets(secrets_dir: Path, data: str) -> str:
    """
    Replace "<file:xxxx>" secrets in given data

    """
    pattern = re.compile(r"\<file\:([^>]*)\>")

    for match in pattern.findall(data):
        relpath = Path(match)
        path = secrets_dir / relpath

        if not path.exists():
            raise FileNotFoundError(
                f"Secret file referenced in yaml file not found: {path}"
            )

        data = data.replace(f"<file:{match}>", path.read_text("utf-8"))
    return data


def yaml_config_settings_source(settings: "YamlBaseSettings") -> Dict[str, Any]:
    """Loads settings from a YAML file at `Config.yaml_file`

    "<file:xxxx>" patterns are replaced with the contents of file xxxx. The root path
    were to find the files is configured with `secrets_dir`.
    """
    yaml_file = settings.model_config.get("yaml_file")
    secrets_dir = settings.model_config.get("secrets_dir")

    assert yaml_file, "Settings.yaml_file not properly configured"
    assert secrets_dir, "Settings.secrets_dir not properly configured"

    path = Path(yaml_file)
    secrets_path = Path(secrets_dir)

    if not path.exists():
        raise FileNotFoundError(f"Could not open yaml settings file at: {path}")

    return yaml.safe_load(replace_secrets(secrets_path, path.read_text("utf-8")))


class YamlConfigSettingsSource(PydanticBaseSettingsSource):
    """
    A simple settings source class that loads variables from a YAML file

    Note: slightly adapted version of JsonConfigSettingsSource from docs.
    """

    def __init__(self, settings_class):
        super().__init__(settings_class)
        self._yaml_data = yaml_config_settings_source(settings_class)

    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> Tuple[Any, str, bool]:
        field_value = self._yaml_data.get(field_name)
        return field_value, field_name, False

    def prepare_field_value(
        self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool
    ) -> Any:
        return value

    def __call__(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {}

        for field_name, field in self.settings_cls.model_fields.items():
            field_value, field_key, value_is_complex = self.get_field_value(
                field, field_name
            )
            field_value = self.prepare_field_value(
                field_name, field, field_value, value_is_complex
            )
            if field_value is not None:
                d[field_key] = field_value

        return d


class YamlBaseSettings(BaseSettings):
    """Allows to specificy a 'yaml_file' path in the Config section.

    The secrets injection is done differently than in BaseSettings, allowing also
    partial secret replacement (such as "postgres://user:<file:path-to-password>@...").

    Field value priority:

    1. Arguments passed to the Settings class initialiser.
    2. Variables from Config.yaml_file (reading secrets at "<file:xxxx>" entries)
    3. Environment variables
    4. Variables loaded from a dotenv (.env) file (if Config.env_file is set)
    5. Variables from secrets in files one directory.
       (Note: the replace_secrets function  above does not use this method and provides
        a more explicit way of specifying the exact path to the secret file)

    Default paths:

    - secrets_dir: "/etc/secrets" or env.SETTINGS_SECRETS_DIR
    - yaml_file: "/etc/config/config.yaml" or env.SETTINGS_YAML_FILE

    See also:

      https://pydantic-docs.helpmanual.io/usage/settings/
    """

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        """
        Define the sources and their order for loading the settings values.

        Args:
            settings_cls: The Settings class.
            init_settings: The `InitSettingsSource` instance.
            env_settings: The `EnvSettingsSource` instance.
            dotenv_settings: The `DotEnvSettingsSource` instance.
            file_secret_settings: The `SecretsSettingsSource` instance.

        Returns:
            A tuple containing the sources and their order for
            loading the settings values.
        """
        return (
            init_settings,
            YamlConfigSettingsSource(settings_cls),
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )

    model_config = SettingsConfigDict(
        secrets_dir=os.environ.get("SETTINGS_SECRETS_DIR", "/etc/secrets"),
        yaml_file=os.environ.get("SETTINGS_YAML_FILE", "/etc/config/config.yaml"),
    )


__ALL__ = (YamlBaseSettings,)
