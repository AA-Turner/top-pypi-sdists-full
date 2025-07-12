import json
import os

from typing import Dict, Any
from .config import (
    CoreConfig,
    MergingNotAllowedFieldsException,
    ConfigValidationFailedException,
    RequiredFieldMissingException,
)

CODE_PACKAGE_PREFIX = "mf.obp-apps"

CAPSULE_DEBUG = os.environ.get("OUTERBOUNDS_CAPSULE_DEBUG", False)


class classproperty(property):
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


class AppConfigError(Exception):
    """Exception raised when app configuration is invalid."""

    pass


def _try_loading_yaml(file):
    try:
        import yaml

        return yaml.safe_load(file)
    except ImportError:
        pass

    try:
        from outerbounds._vendor import yaml

        return yaml.safe_load(file)
    except ImportError:
        pass
    return None


class AuthType:
    BROWSER = "Browser"
    API = "API"

    @classmethod
    def enums(cls):
        return [cls.BROWSER, cls.API]

    @classproperty
    def default(cls):
        return cls.BROWSER


class AppConfig:
    """Class representing an Outerbounds App configuration."""

    def __init__(self, core_config: CoreConfig):
        """Initialize configuration from a dictionary."""
        self._core_config = core_config
        self._final_state: Dict[str, Any] = {}
        self.config = {}

    def set_state(self, key, value):
        self._final_state[key] = value
        return self

    def get_state(self, key, default=None):
        return self._final_state.get(key, self.get(key, default))

    def dump_state(self):
        x = {k: v for k, v in self.config.items()}
        for k, v in self._final_state.items():
            x[k] = v
        return x

    def commit(self):
        try:
            self._core_config.commit()
            self.config = self._core_config.to_dict()
        except RequiredFieldMissingException as e:
            raise AppConfigError(
                "The configuration is missing the following required fields: %s. \n\tException: %s"
                % (e.field_name, e.message)
            )
        except ConfigValidationFailedException as e:
            raise AppConfigError(
                "The configuration is invalid. \n\n\tException: %s" % (e.message)
            )

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key."""
        config_value = self.config.get(key, default)
        if config_value is None:
            return default
        return config_value

    def to_json(self):
        return json.dumps(self.config, indent=2)

    def to_yaml(self):
        return self.to_json()

    def to_dict(self):
        return self.config

    @classmethod
    def from_file(cls, file_path: str) -> "AppConfig":
        """Create a configuration from a file."""
        if not os.path.exists(file_path):
            raise AppConfigError(f"Configuration file '{file_path}' does not exist.")

        with open(file_path, "r") as f:
            try:
                config_dict = _try_loading_yaml(f)
                if config_dict is None:
                    config_dict = json.load(f)
            except json.JSONDecodeError as e:
                raise AppConfigError(
                    "The PyYAML package is not available as a dependency and JSON parsing of the configuration file also failed %s: \n%s"
                    % (file_path, str(e))
                )
            except Exception as e:
                raise AppConfigError(f"Failed to parse configuration file: {e}")

        return cls(CoreConfig.from_dict(config_dict))

    @classmethod
    def from_cli(cls, options: Dict[str, Any]):
        return cls(CoreConfig.from_cli(options))

    def update_from_cli_options(self, options):
        cli_options_config = CoreConfig.from_cli(options)
        try:
            self._core_config = CoreConfig.merge_configs(
                self._core_config, cli_options_config
            )
        except MergingNotAllowedFieldsException as e:
            raise AppConfigError(
                "CLI Overrides are not allowed for the following fields: %s. \n\tException: %s"
                % (e.field_name, e.message)
            )
