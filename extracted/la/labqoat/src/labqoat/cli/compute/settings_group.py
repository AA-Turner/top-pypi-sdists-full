"""``compute settings`` shows the current policy and hosts the ``set`` subcommand."""

from __future__ import annotations

import click

from labqoat.cli.compute.settings_set_command import SettingsSetCommand
from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.output.result_writer import ResultWriter


class SettingsGroup:
    """Render settings when invoked alone; otherwise dispatch the selected subcommand."""

    @staticmethod
    def group() -> click.Group:
        """Build the settings group with its update leaf."""
        group = click.Group(
            "settings",
            help="Show workspace compute limits and idle delays, or change them with 'set'.",
            callback=SettingsGroup.show,
            invoke_without_command=True,
        )
        group.add_command(SettingsSetCommand())
        return group

    @staticmethod
    def show() -> None:
        """Read and render the current settings document when no subcommand was selected."""
        if click.get_current_context().invoked_subcommand is not None:
            return
        client = ContextAccessor.current().compute()
        try:
            ResultWriter().write_dict(client.settings())
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            client.close()
