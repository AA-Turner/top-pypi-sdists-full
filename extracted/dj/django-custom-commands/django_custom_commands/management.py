__all__ = ["execute_from_command_line", "call_command", "get_commands"]

import functools
import os
import sys
from collections import defaultdict
from difflib import get_close_matches
from pathlib import Path

from django.conf import settings
from django.core.management import (
    BaseCommand,
    CommandError,
    color_style,
    find_commands,
    load_command_class,
)
from django.core.management import ManagementUtility as OriginalManagementUtility
from django.core.management import call_command as original_call_command
from django.core.management import get_commands as original_get_commands


@functools.cache
def get_commands():
    commands = original_get_commands()

    if hasattr(settings, "CUSTOM_COMMAND_LOCATIONS"):
        for custom_module in reversed(settings.CUSTOM_COMMAND_LOCATIONS):
            path = Path(settings.BASE_DIR) / custom_module.replace(".", "/") / "management"
            commands.update({name: custom_module for name in find_commands(path)})

    return commands


class ManagementUtility(OriginalManagementUtility):
    """
    Overridden to use the custom get_commands, no other changes.
    """

    def main_help_text(self, commands_only=False):
        if commands_only:
            usage = sorted(get_commands())
        else:
            usage = [
                "",
                f"Type '{self.prog_name} help <subcommand>' for help on a specific subcommand.",
                "",
                "Available subcommands:",
            ]
            commands_dict = defaultdict(list)
            for name, app in get_commands().items():
                if app == "django.core":
                    app = "django"
                else:
                    app = app.rpartition(".")[-1]
                commands_dict[app].append(name)
            style = color_style()
            for app in sorted(commands_dict):
                usage.append("")
                usage.append(style.NOTICE(f"[{app}]"))
                for name in sorted(commands_dict[app]):
                    usage.append(f"    {name}")
            # Output an extra note if settings are not properly configured
            if self.settings_exception is not None:
                usage.append(
                    style.NOTICE(
                        "Note that only Django core commands are listed "
                        f"as settings are not properly configured (error: {self.settings_exception})."
                    )
                )

        return "\n".join(usage)

    def fetch_command(self, subcommand):
        # Get commands outside of try block to prevent swallowing exceptions
        commands = get_commands()
        try:
            app_name = commands[subcommand]
        except KeyError:
            if os.environ.get("DJANGO_SETTINGS_MODULE"):
                # If `subcommand` is missing due to misconfigured settings, the
                # following line will retrigger an ImproperlyConfigured exception
                # (get_commands() swallows the original one) so the user is
                # informed about it.
                settings.INSTALLED_APPS  # noqa: B018
            elif not settings.configured:
                sys.stderr.write("No Django settings specified.\n")
            possible_matches = get_close_matches(subcommand, commands)
            sys.stderr.write(f"Unknown command: {subcommand!r}")
            if possible_matches:
                sys.stderr.write(f". Did you mean {possible_matches[0]}?")
            sys.stderr.write(f"\nType '{self.prog_name} help' for usage.\n")
            sys.exit(1)
        if isinstance(app_name, BaseCommand):
            # If the command is already loaded, use it directly.
            klass = app_name
        else:
            klass = load_command_class(app_name, subcommand)
        return klass


def call_command(command_name, *args, **options):
    if isinstance(command_name, BaseCommand):
        return original_call_command(command_name, *args, **options)

    # Load the command object by name.
    try:
        app_name = get_commands()[command_name]
    except KeyError:
        raise CommandError(f"Unknown command: {command_name!r}") from None

    if isinstance(app_name, BaseCommand):
        # If the command is already loaded, use it directly.
        command = app_name
    else:
        command = load_command_class(app_name, command_name)

    return original_call_command(command, *args, **options)


def execute_from_command_line(argv=None):
    """Run a ManagementUtility."""
    utility = ManagementUtility(argv)
    utility.execute()
