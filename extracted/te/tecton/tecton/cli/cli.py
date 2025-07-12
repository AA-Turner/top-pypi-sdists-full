import logging
import sys
import time
import urllib.parse
from pathlib import Path
from typing import Optional

import rich_click as click

import tecton
from tecton import conf
from tecton import tecton_context
from tecton._internals import metadata_service
from tecton._internals import sdk_decorators
from tecton._internals.utils import cluster_url
from tecton.cli import access_control
from tecton.cli import auth
from tecton.cli import cli_utils
from tecton.cli import completion
from tecton.cli import engine
from tecton.cli import environment
from tecton.cli import infra_commands
from tecton.cli import materialization
from tecton.cli import model
from tecton.cli import plan
from tecton.cli import printer
from tecton.cli import repo
from tecton.cli import repo_config
from tecton.cli import secrets
from tecton.cli import server_group
from tecton.cli import service_account
from tecton.cli import test
from tecton.cli import upgrade
from tecton.cli import user
from tecton.cli import workspace
from tecton.cli.command import TectonGroup
from tecton.cli.engine import dump_local_state
from tecton.cli.workspace_utils import WorkspaceType
from tecton.repo_utils import get_tecton_objects_skip_validation
from tecton_proto.metadataservice import metadata_service__client_pb2 as metadata_service_pb2


CONTEXT_SETTINGS = {
    "max_content_width": 160,
    "help_option_names": ["-h", "--help"],
}


@click.group(name="tecton", context_settings=CONTEXT_SETTINGS, cls=TectonGroup)
@click.option("--verbose", "-v", is_flag=True, help="Increase verbosity level to print more information.")
def cli(verbose: bool = False):
    """The Tecton command-line tool is used to manage feature repositories, infrastructure, and access controls in Tecton.

    See https://docs.tecton.ai/ for documentation and more information about building on Tecton.
    """
    sdk_decorators.disable_sdk_public_method_decorator()
    conf.enable_save_tecton_configs()

    logging_level = logging.DEBUG if verbose else logging.ERROR
    logging.basicConfig(
        level=logging_level,
        stream=sys.stderr,
        format="%(levelname)s(%(name)s): %(message)s",
    )

    # add cwd to path
    sys.path.append("")


cli.add_command(auth.login)
cli.add_command(auth.logout)
cli.add_command(auth.get_caller_identity)
cli.add_command(access_control.access_control)
cli.add_command(completion.completion)
cli.add_command(engine.apply)
cli.add_command(engine.plan)
cli.add_command(engine.destroy)
cli.add_command(environment.environment)
cli.add_command(model.model)
cli.add_command(plan.plan_info)
cli.add_command(materialization.materialization)
cli.add_command(repo.init)
cli.add_command(repo_config.repo_config_group)
cli.add_command(secrets.secrets)
cli.add_command(server_group.server_group)
cli.add_command(infra_commands.feature_server_cache)
cli.add_command(infra_commands.feature_server_group)
cli.add_command(infra_commands.ingest_server_group)
cli.add_command(infra_commands.isg)
cli.add_command(infra_commands.transform_server_group)
cli.add_command(infra_commands.tsg)
cli.add_command(service_account.service_account)
cli.add_command(test.test)
cli.add_command(user.user)
cli.add_command(upgrade.upgrade)
cli.add_command(workspace.workspace)


@cli.command(requires_auth=False)
def version():
    """Print CLI version."""
    tecton.version.summary()


@cli.command(hidden=True)
@click.option(
    "--config",
    help="Path to the repo config yaml file. Defaults to the repo.yaml file at the Tecton repo root.",
    default=None,
    type=click.Path(exists=True, dir_okay=False, path_type=Path, readable=True),
)
def dump(config: Optional[Path]) -> None:
    """Print the serialization format for object definitions in this repository.

    Useful for debugging issues related to serializing the Tecton repository to be sent to the Tecton backend.
    """
    # TODO(jake): get_tecton_objects prints out to stdout, which breaks piping the `tecton dump` output. Start printing
    # to stderr.
    top_level_objects, _, _, _ = get_tecton_objects_skip_validation(config)
    dump_local_state(top_level_objects)


@cli.command(uses_workspace=True, hidden=True)
@click.option("--limit", default=10, type=int, help="Number of log entries to return.")
def log(limit):
    """View log of applied plans in workspace."""
    request = metadata_service_pb2.GetStateUpdateLogRequest(
        workspace=tecton_context.get_current_workspace(), limit=limit
    )
    response = metadata_service.instance().GetStateUpdateLog(request)

    headings = ["Plan ID", "Author", "Date", "SDK Version"]
    display_rows = []

    for entry in response.entries:
        display_rows.append(
            (
                entry.commit_id,
                cli_utils.display_principal(entry.applied_by_principal, entry.applied_by),
                str(entry.applied_at.ToDatetime()),
                entry.sdk_version if entry.sdk_version else "",
            )
        )

    cli_utils.display_table(headings, display_rows)


@cli.command()
@click.option(
    "-w",
    "--workspace",
    default=None,
    type=WorkspaceType(),
    help="Workspace selected in Tecton Web UI. Defaults to the current selected workspace.",
)
@click.option(
    "--print/--no-print", "-p", "print_", default=False, help="Print URL instead of automatically launching a browser."
)
def web(workspace, print_) -> None:
    """Opens Tecton UI in a browser."""
    workspace_name = workspace if workspace else tecton_context.get_current_workspace()
    if workspace_name:
        web_url = urllib.parse.urljoin(cluster_url(), f"app/repo/{workspace_name}/")
    else:
        web_url = urllib.parse.urljoin(cluster_url(), "app")

    if print_:
        printer.safe_print(f"Web URL: {web_url}")
    else:
        import click

        printer.safe_print(f"Opening {web_url}")
        # Sleep before opening the browser to improve the UX and make it less jarring.
        time.sleep(1)
        click.launch(web_url)


# Deprecated commands, kept for backwards compatibility but hidden from the cli help output
cli.add_deprecated_command(materialization.freshness, name="freshness", new_target="tecton materialization freshness")
cli.add_deprecated_command(auth.get_caller_identity, name="whoami", new_target="tecton get-caller-identity")
cli.add_deprecated_command(
    materialization.status, name="materialization-status", new_target="tecton materialization status"
)
cli.add_deprecated_command(repo.restore, name="restore", new_target="tecton workspace restore")


@click.command("api-key", cls=TectonGroup, hidden=True)
def api_key():
    """Introspect API key. To create, delete, or list API keys see `tecton service-account` commands"""


cli.add_deprecated_command(api_key, name="api-key", new_target="tecton service-account")
api_key.add_deprecated_command(
    service_account.introspect_api_key, name="introspect", new_target="tecton service-account introspect-api-key"
)


def main():
    try:
        cli()
    finally:
        metadata_service.close_instance()


if __name__ == "__main__":
    main()
