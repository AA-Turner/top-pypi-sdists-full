"""Assembled ``lab`` command tree with a static entrypoint."""

from __future__ import annotations

import click
import os
from dataclasses import replace

from labqoat.cli.cli_context import CliContext
from labqoat.cli.compute_command_catalog import ComputeCommandCatalog
from labqoat.cli.commands.auth.auth_status_command import AuthStatusCommand
from labqoat.cli.commands.auth.login_command import LoginCommand
from labqoat.cli.commands.auth.logout_command import LogoutCommand
from labqoat.cli.commands.completion_command import CompletionCommand
from labqoat.cli.agent.agent_command import AgentCommand
from labqoat.cli.commands.skills_command import SkillsCommand
from labqoat.cli.config.profile import Profile
from labqoat.cli.config.profile_store import ProfileStore
from labqoat.cli.coordination_command_catalog import CoordinationCommandCatalog
from labqoat.cli.core_command_catalog import CoreCommandCatalog
from labqoat.cli.dashboard_command_catalog import DashboardCommandCatalog
from labqoat.cli.dataset_command_catalog import DatasetCommandCatalog
from labqoat.cli.bleat_command import BleatCommand
from labqoat.cli.doctor_command import DoctorCommand
from labqoat.cli.group_help import GroupHelp
from labqoat.cli.init_command import InitCommand
from labqoat.cli.operational_command_catalog import OperationalCommandCatalog
from labqoat.cli.output.field_selection import FieldSelection
from labqoat.cli.output.pretty_help import PrettyHelp
from labqoat.cli.root_group import RootGroup
from labqoat.cli.run_command_catalog import RunCommandCatalog
from labqoat.cli.version_option import VersionOption
from labqoat.cli.update_notifier import UpdateNotifier
from labqoat.cli.workload_command_catalog import WorkloadCommandCatalog
from labqoat.cli.memory_command_catalog import MemoryCommandCatalog
from labqoat.cli.project_command_catalog import ProjectCommandCatalog
from labqoat.cli.secret_command_catalog import SecretCommandCatalog
from labqoat.cli.serving_command_catalog import ServingCommandCatalog
from labqoat.cli.volume_command_catalog import VolumeCommandCatalog


class CliApplication:
    """Root command group and process entrypoint."""

    name = "lab"
    project_key = "labqoat.project"

    @staticmethod
    def main() -> int:
        """Run the CLI from installed launchers and module execution."""
        try:
            UpdateNotifier.notify()
            result = CliApplication.build_root().main(standalone_mode=False)
        except click.ClickException as error:
            error.show()
            return error.exit_code
        except click.Abort:
            click.echo("Interrupted.", err=True)
            return 130
        return result if isinstance(result, int) else 0

    @classmethod
    def build_root(cls) -> click.Group:
        """Assemble groups and commands without network or keyring use."""
        click.Context.formatter_class = PrettyHelp
        root = RootGroup(
            cls.name,
            help="Run Python functions on cloud machines, and follow, store and compare what they produce.",
            callback=cls.configure,
            invoke_without_command=True,
            context_settings={"help_option_names": ["-h", "--help"]},
        )
        root.params.extend(CliApplication.global_params())
        root.add_command(CliApplication.build_auth())
        root.add_command(CompletionCommand.as_click_command())
        root.add_command(SkillsCommand.as_click_command())
        root.add_command(AgentCommand.as_click_command())
        root.add_command(DoctorCommand())
        root.add_command(BleatCommand())
        root.add_command(InitCommand())
        CoreCommandCatalog.add(root)
        root.add_command(ProjectCommandCatalog.group())
        root.add_command(MemoryCommandCatalog.group())
        root.add_command(DashboardCommandCatalog.group())
        root.add_command(DatasetCommandCatalog.group())
        WorkloadCommandCatalog.add(root)
        root.add_command(RunCommandCatalog.group())
        OperationalCommandCatalog.add(root)
        root.add_command(ComputeCommandCatalog.group())
        root.add_command(SecretCommandCatalog.group())
        ServingCommandCatalog.add(root)
        CoordinationCommandCatalog.add(root)
        root.add_command(VolumeCommandCatalog.group())
        return root

    @staticmethod
    def global_params() -> list[click.Option]:
        """Define profile, endpoint, timeout, and output options."""
        return [
            VersionOption(),
            click.Option(
                ["--profile"],
                type=str,
                default="default",
                show_default=True,
                help="Configuration profile name.",
            ),
            click.Option(
                ["--base-url"],
                type=str,
                default=None,
                help="Override the profile or production endpoint (https://app.labqoat.com); use http://127.0.0.1:4000 for local development.",
            ),
            click.Option(
                ["--timeout"],
                type=float,
                default=None,
                help="Request timeout in seconds.",
            ),
            click.Option(["--json", "as_json"], is_flag=True, help="Render compact JSON."),
            click.Option(["--pretty"], is_flag=True, help="Render indented JSON."),
            click.Option(["--endpoint"], type=str, help="Override the API endpoint."),
            click.Option(["--environment"], type=str, help="Override the profile's environment (default: default)."),
            click.Option(
                ["--project"],
                type=str,
                expose_value=False,
                callback=CliApplication.select_project,
                help="Project every command acts on. Without it: LABQOAT_PROJECT, then [tool.labqoat] project in the "
                "nearest pyproject.toml; nothing else selects one.",
            ),
            click.Option(["--no-color"], is_flag=True, help="Disable terminal color; also respects NO_COLOR."),
            click.Option(
                ["--select"],
                type=str,
                expose_value=False,
                callback=CliApplication.select_fields,
                help="Print only these comma-separated fields, dotted for nested ones (status,manifest.args); "
                "on a list, inside each item.",
            ),
        ]

    @staticmethod
    def configure(
        profile: str,
        base_url: str | None,
        timeout: float | None,
        as_json: bool,
        pretty: bool,
        endpoint: str | None,
        environment: str | None,
        no_color: bool,
    ) -> None:
        """Store the resolved profile on the invocation context."""
        context = click.get_current_context()
        if as_json and pretty:
            raise click.UsageError("--json and --pretty are mutually exclusive.", context)
        store = ProfileStore()
        selected = CliApplication.select_profile(store, profile, environment)
        if no_color or "NO_COLOR" in os.environ:
            context.color = False
        if base_url is not None:
            selected = selected.with_base_url(base_url)
        if timeout is not None:
            selected = CliApplication.with_timeout(selected, timeout)
        if endpoint is not None:
            selected = selected.with_base_url(endpoint)
        context.obj = CliContext(
            profile=selected,
            store=store,
            output_mode="pretty" if pretty else "json" if as_json else "human",
            project=context.meta.get(CliApplication.project_key),
        )
        GroupHelp.show()

    @staticmethod
    def select_fields(context: click.Context, _option: click.Parameter, value: str | None) -> None:
        """Keep the --select paths for the invocation's result writer."""
        context.meta[FieldSelection.KEY] = value

    @staticmethod
    def select_project(context: click.Context, _option: click.Parameter, value: str | None) -> None:
        """Keep the explicit project for the invocation context; it is validated when a command first needs it."""
        context.meta[CliApplication.project_key] = value

    @staticmethod
    def group(name: str, help_text: str) -> click.Group:
        """Create a help-first group with consistent help aliases."""
        return click.Group(
            name,
            help=help_text,
            callback=GroupHelp.show,
            invoke_without_command=True,
            context_settings={"help_option_names": ["-h", "--help"]},
        )

    @staticmethod
    def with_timeout(profile: Profile, timeout: float) -> Profile:
        """Return the profile with an explicit timeout."""
        try:
            return replace(profile, timeout_seconds=timeout)
        except ValueError as error:
            raise click.UsageError(str(error)) from error

    @staticmethod
    def select_profile(store: ProfileStore, name: str, environment: str | None) -> Profile:
        """Apply environment overrides while reporting invalid local configuration as usage."""
        try:
            profile = store.load(name)
            return replace(profile, environment=environment) if environment is not None else profile
        except ValueError as error:
            raise click.UsageError(str(error)) from error

    @staticmethod
    def build_auth() -> click.Group:
        """Assemble the auth command group."""
        group = CliApplication.group("auth", "Credential verification and storage.")
        group.add_command(LoginCommand.as_click_command())
        group.add_command(AuthStatusCommand.as_click_command())
        group.add_command(LogoutCommand.as_click_command())
        return group
