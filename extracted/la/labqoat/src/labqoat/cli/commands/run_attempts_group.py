"""Attempt history and recovery commands."""

import click

from labqoat.cli.endpoint_command import EndpointCommand
from labqoat.cli.parameter_factory import ParameterFactory
from labqoat.cli.commands.run_recovery_command import RunRecoveryCommand


class RunAttemptsGroup:
    """Group bounded attempt reads and explicit recovery operations."""

    @staticmethod
    def as_click_command() -> click.Group:
        """Build bounded history/discovery reads and explicit recovery mutations lazily."""
        group = click.Group("attempts", help="Inspect attempt history and recover the original Run.")
        listing = [
            ParameterFactory.argument("run_ref"),
            ParameterFactory.limit(),
            ParameterFactory.text_option("cursor"),
        ]
        discovery = [
            ParameterFactory.argument("run_ref"),
            click.Option(["--limit"], type=click.IntRange(1, 200), default=50),
            ParameterFactory.text_option("cursor"),
        ]
        group.add_command(
            EndpointCommand("list", "/api/v1/runs/{ref}/attempts", listing, "List fenced attempts.", "run_ref")
        )
        group.add_command(
            EndpointCommand(
                "recovery", "/api/v1/runs/{ref}/recovery", discovery, "Discover recovery readiness.", "run_ref"
            )
        )
        group.add_command(RunRecoveryCommand.as_click_command("restart"))
        group.add_command(RunRecoveryCommand.as_click_command("resume"))
        group.add_command(RunRecoveryCommand.as_click_command("finalize"))
        group.add_command(RunAttemptsGroup.group_command())
        return group

    @staticmethod
    def group_command() -> click.Command:
        """Inspect a captured attempt's coordinated restoration with bounded pagination."""
        params = [
            ParameterFactory.argument("run_ref"),
            ParameterFactory.argument("attempt_id"),
            click.Option(["--limit"], type=click.IntRange(1, 200), default=50),
            ParameterFactory.text_option("cursor"),
        ]
        return EndpointCommand(
            "group", "/api/v1/runs/{ref}/attempts/{attempt_id}/group", params, "Inspect rank restoration.", "run_ref"
        )
