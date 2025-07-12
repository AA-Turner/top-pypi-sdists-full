"""
CLI Generator for Unified Configuration System

This module automatically generates Click CLI options from the CoreConfig,
eliminating the need for manual CLI option definitions and ensuring consistency
between configuration structure and CLI interface.

It also provides machinery for merging configurations from different sources
(CLI options, config files) with proper precedence and behavior handling.
"""

from typing import Any, List, Optional
import json

from ..click_importer import click
from .unified_config import (
    CoreConfig,
    CLIOption,
    ConfigMeta,
)
from .config_utils import (
    PureStringKVPairType,
    JsonFriendlyKeyValuePairType,
    CommaSeparatedListType,
)


class CLIGenerator:
    """Generates Click CLI options from CoreConfig dataclass."""

    def __init__(self, config_class: type = CoreConfig):
        self.config_class = config_class
        self._type_mapping = {
            str: str,
            int: int,
            float: float,
            bool: bool,
            list: CommaSeparatedListType,
            dict: JsonFriendlyKeyValuePairType,
        }

    def generate_options(self):
        """Generate all CLI options from the configuration class."""
        options = []

        # Generate options for all fields automatically
        options.extend(self._generate_all_options(self.config_class))

        return options

    def _generate_all_options(self, config_class: type):
        """Generate all options from a config class. Returns a list of click.Options"""

        def _options_from_cfg_cls(_config_class):
            options = []
            for field_name, field_info in _config_class._fields.items():
                if ConfigMeta.is_instance(field_info.field_type):
                    _subfield_options = _options_from_cfg_cls(field_info.field_type)
                    options.extend(_subfield_options)
                    continue

                cli_meta = field_info.cli_meta
                if not cli_meta or cli_meta.hidden:
                    continue

                option = self._create_option(field_name, field_info, cli_meta)
                if option:
                    options.append(option)
            return options

        return _options_from_cfg_cls(config_class)

    def _create_option(self, field_name: str, field_info, cli_meta: CLIOption):
        """Create a Click option from field info and CLI metadata."""
        # Use the cli_option_str from the CLIOption
        option_str = cli_meta.cli_option_str
        param_name = cli_meta.name

        # Determine Click type
        click_type = self._get_click_type(field_info, cli_meta)

        # Build option parameters
        help_text = cli_meta.help or field_info.help or f"Set {field_name}"
        option_params = {
            "help": help_text,
            "default": cli_meta.default if cli_meta.default is not None else None,
            "type": click_type,
        }

        # Handle multiple values
        if cli_meta.multiple:
            option_params["multiple"] = True

        # Handle choices
        if cli_meta.choices:
            option_params["type"] = click.Choice(cli_meta.choices)

        # Handle flags
        if cli_meta.is_flag:
            option_params["is_flag"] = True
            option_params.pop("type", None)

        # Handle special flag patterns (e.g., --public-access/--private-access)
        return click.option(option_str, param_name, **option_params)

    def _get_click_type(self, field_info, cli_meta: CLIOption) -> Any:
        """Determine the appropriate Click type for a field."""
        if cli_meta.click_type:
            return cli_meta.click_type

        # Get the field type
        field_type = field_info.field_type

        # Handle basic types
        if field_type == list:
            return CommaSeparatedListType
        elif field_type == dict:
            return JsonFriendlyKeyValuePairType
        elif field_type == str:
            return str
        elif field_type == int:
            return int
        elif field_type == bool:
            return bool
        elif field_type == float:
            return float

        # Handle custom config types
        if hasattr(field_type, "__name__") and field_type.__name__.endswith("Config"):
            return str  # Default to string for complex types

        # Use type mapping
        return self._type_mapping.get(field_type, str)

    def create_decorator(self, command_type: str = "deploy") -> callable:
        """Create a decorator that applies all CLI options to a command."""

        def decorator(func):
            # Apply options in reverse order since decorators are applied bottom-up
            for option in reversed(self.generate_options()):
                func = option(func)
            return func

        return decorator


def auto_cli_options(config_class: type = CoreConfig, command_type: str = "deploy"):
    """
    Decorator that automatically adds CLI options from CoreConfig.

    Args:
        command_type: Type of command (e.g., "deploy", "list", "delete")

    Usage:
        @auto_cli_options("deploy")
        def deploy_command(**kwargs):
            config = CoreConfig.from_cli(kwargs)
            # ... use config
    """
    generator = CLIGenerator(config_class)
    return generator.create_decorator(command_type)
