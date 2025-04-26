"""All imports to union in this file should be in the function definition.

This plugin is loaded by flytekit, so any imports to union can lead to circular imports.
"""

from contextlib import suppress
from typing import TYPE_CHECKING, List, Optional

import click
from click import Group, Option
from flytekit import CachePolicy

if TYPE_CHECKING:
    from union.remote import UnionRemote

from union.cache import CacheFunctionBody
from union.cli._cache import cache


class UnionAIPlugin:
    @staticmethod
    def get_remote(
        config: Optional[str],
        project: str,
        domain: str,
        data_upload_location: Optional[str] = None,
    ) -> "UnionRemote":
        from union.remote import UnionRemote

        return UnionRemote(
            config=UnionAIPlugin._get_config_for_remote(config),
            default_project=project,
            default_domain=domain,
            data_upload_location=data_upload_location,
        )

    @staticmethod
    def _get_config_for_remote(config: Optional[str], default_to_union_semantics: bool = False):
        """Get config when creating a UnionRemote when using the CLI."""
        from union._config import _UNION_CONFIG, ConfigSource, _get_config_obj

        if _UNION_CONFIG.config_source == ConfigSource.CLI.value:
            # The config that is passed through the CLI with `--config` will be handled by
            # `UnionRemote` itself
            config = None
        elif not _UNION_CONFIG.is_direct_union_cli_call:
            # Use pyflyte's default config when not using `union` directly
            config = _get_config_obj(config, default_to_union_semantics=default_to_union_semantics)
        return config

    @staticmethod
    def configure_pyflyte_cli(main: Group) -> Group:
        """Configure pyflyte's CLI."""

        import union._config

        # Import filesystems here so they get copied over properly when union is installed in
        # development mode
        import union.filesystems
        from union._config import _get_config_obj, _get_image_builder_priority
        from union.cli._create import create
        from union.cli._delete import delete
        from union.cli._deploy import deploy
        from union.cli._get import get
        from union.cli._info import info
        from union.cli._start import start
        from union.cli._stop import stop
        from union.cli._update import update
        from union.ucimage._image_builder import _register_union_image_builder

        def _cli_main_config_callback(ctx, param, value):
            from union._config import ConfigSource, ConfigWithSource
            from union._exceptions import UnionRequireConfigException

            # Set org based on config from `pyflyte --config` for downstream cli
            # commands to use.
            # Only register image builder for serverless
            with suppress(UnionRequireConfigException):
                if isinstance(value, str):
                    config_source = ConfigWithSource(config=value, source=ConfigSource.CLI)
                    config_obj = _get_config_obj(config_source)
                else:
                    config_obj = _get_config_obj(value)

                _register_union_image_builder(_get_image_builder_priority(config_obj.platform.endpoint))

            return value

        for p in main.params:
            if p.name == "config":
                p.callback = _cli_main_config_callback

        # Configure org at the top level:
        def _set_org(ctx, param, value):
            if value is not None:
                union._config._UNION_CONFIG.org = value

        main.params.append(
            click.Option(
                ["--org"],
                help="Set organization",
                hidden=True,
                callback=_set_org,
                expose_value=False,
            )
        )

        def update_or_create_group(new_group):
            try:
                main_group = main.commands[new_group.name]
                for name, command in new_group.commands.items():
                    main_group.add_command(command, name)
            except KeyError:
                main.add_command(new_group)

        new_groups = [create, delete, update, get, deploy, start, stop, cache]

        for group in new_groups:
            update_or_create_group(group)

        new_commands = [info]
        for command in new_commands:
            main.add_command(command)

        def yield_all_options():
            commands = [main]

            while commands:
                command = commands.pop()
                yield from (p for p in command.params if isinstance(p, Option))

                if isinstance(command, Group):
                    commands.extend(list(command.commands.values()))

        for param in yield_all_options():
            if param.name == "image_config" and param.default is not None and not callable(param.default):
                param.default = lambda: [union._config._get_default_image()]
            elif param.name == "project" and param.default is not None and not callable(param.default):
                param.default = union._config._GetDefaultProject(previous_default=param.default)

        return main

    @staticmethod
    def secret_requires_group() -> bool:
        """Return True if secrets require group entry."""
        return False

    @staticmethod
    def get_default_image() -> Optional[str]:
        """Return default image."""

        from union._config import _get_default_image

        return _get_default_image()

    @staticmethod
    def get_auth_success_html(endpoint: str) -> Optional[str]:
        """Get default success html. Return None to use flytekit's default success html."""
        from union._config import _get_auth_success_html

        return _get_auth_success_html(endpoint)

    @staticmethod
    def get_default_cache_policies() -> List[CachePolicy]:
        """Get default cache policies for tasks."""
        return [CacheFunctionBody()]
