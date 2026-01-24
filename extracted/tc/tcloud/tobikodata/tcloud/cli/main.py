import json
import logging
import os
import subprocess
import time
import typing as t
from dataclasses import dataclass

import click
import requests

from tobikodata.tcloud.cli.auth import auth
from tobikodata.tcloud.cli.project import project
from tobikodata.tcloud.config import load_previous_extras, load_project_config, save_previous_extras
from tobikodata.tcloud.constants import TCLOUD_PYTHON_PATH_ENV_VAR
from tobikodata.tcloud.installer import (
    install_executors,
    install_sqlmesh_enterprise,
    is_executor_installed_and_unpacked,
    is_sqlmesh_enterprise_version_installed,
)

EXECUTOR_MIN_INTERVAL_BETWEEN_RUNS_SEC = 5.0

logger = logging.getLogger(__name__)


def _tcloud_version() -> str:
    try:
        from tobikodata.tcloud import __version__

        return __version__
    except ImportError:
        return "0.0.0"


@dataclass
class Command:
    name: str
    short_help: str
    hidden: bool = False


class DynamicGroup(click.Group):
    COMMANDS: t.Dict[str, Command] = {
        "sqlmesh": Command(name="sqlmesh", short_help="Run SQLMesh Enterprise commands"),
        "sqlmesh_cicd": Command(
            name="sqlmesh_cicd", short_help="Run SQLMesh Enterprise CI/CD commands"
        ),
        "sqlmesh_lsp": Command(
            name="sqlmesh_lsp", short_help="Run SQLMesh Language Server Protocol", hidden=True
        ),
    }

    def list_commands(self, ctx: click.Context) -> t.List[str]:
        # Exclude sqlmesh_lsp from the visible command list
        return super().list_commands(ctx) + [c.name for c in self.COMMANDS.values() if not c.hidden]

    def get_command(self, ctx: click.Context, cmd_name: str) -> t.Optional[click.Command]:
        if cmd_name in self.COMMANDS:
            if not ctx.params:
                # Help was invoked, return a stub command instead
                return click.Command(name=cmd_name, short_help=self.COMMANDS[cmd_name].short_help)
            return self._load_sqlmesh_enterprise(cmd_name, ctx.params.get("project"))
        return super().get_command(ctx, cmd_name)

    def _load_sqlmesh_enterprise(self, cmd_name: str, project: t.Optional[str]) -> click.Command:
        _install_sqlmesh_enterprise(project)
        if cmd_name == "sqlmesh_cicd":
            try:
                from tobikodata.sqlmesh_enterprise.cli.bot import (  # type: ignore
                    bot,  # pants: no-infer-dep
                )
            except ImportError:
                from sqlmesh_enterprise.cli.bot import bot  # type: ignore  # pants: no-infer-dep

            return bot
        if cmd_name == "sqlmesh_lsp":
            from tobikodata.sqlmesh_enterprise.cli.lsp import (  # type: ignore
                main,  # pants: no-infer-dep
            )

            @click.command(hidden=True, context_settings=dict(ignore_unknown_options=True))
            @click.argument("args", nargs=-1, type=click.UNPROCESSED)
            def lsp(args: t.Tuple[str, ...]) -> None:
                """Run SQLMesh Language Server Protocol"""
                import sys

                sys.argv = ["sqlmesh_lsp", *args]
                main()

            return lsp
        try:
            from tobikodata.sqlmesh_enterprise.cli.main import (  # type: ignore
                cli,  # pants: no-infer-dep
            )
        except ImportError:
            from sqlmesh_enterprise.cli.main import cli  # type: ignore  # pants: no-infer-dep

        return cli


@click.group(cls=DynamicGroup, no_args_is_help=True)
@click.version_option(version=_tcloud_version(), message="%(version)s")
@click.option(
    "--project",
    type=str,
    help="The name of the project.",
)
@click.pass_context
def cli(ctx: click.Context, project: t.Optional[str]) -> None:
    ctx.ensure_object(dict)
    ctx.obj["project"] = project


@cli.command()
@click.argument("command", required=True)
@click.argument("args", nargs=-1)
@click.pass_context
def exec(ctx: click.Context, command: str, args: t.Tuple[str, ...]) -> None:
    """Execute an arbitrary command after installing SQLMesh Enterprise"""
    project = ctx.obj["project"]
    _install_sqlmesh_enterprise(project)
    ctx.exit(subprocess.run([command, *args]).returncode)


@cli.command()
@click.argument("executor_type", required=True, type=click.Choice(["run", "apply"]))
@click.option(
    "--once",
    is_flag=True,
    help="Runs the executor once and exit.",
)
@click.option(
    "--check",
    is_flag=True,
    help="Health check the executor. Returns 0 if the executor is healthy, 1 otherwise.",
)
@click.pass_context
def executor(ctx: click.Context, executor_type: str, once: bool, check: bool) -> None:
    """Run the Tobiko Cloud executor"""
    logging.basicConfig(
        format="%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)",
        level=logging.INFO,
    )

    project = ctx.obj["project"]
    project_config = load_project_config(project)

    if check:
        try:
            paths = is_executor_installed_and_unpacked(project_config)
            if not paths:
                raise click.ClickException("Executor is not installed and unpacked")
            return
        except Exception as ex:
            raise click.ClickException(f"Failed to check if executor is installed: {ex}")

    def install_and_run() -> None:
        try:
            executors_bin_path, site_packages_path = install_executors(project_config)
        except Exception as ex:
            raise click.ClickException(f"Failed to install the executor bin package: {ex}")

        environment = {
            **os.environ,
            "TCLOUD_URL": project_config.url,
        }
        if project_config.token:
            environment["TCLOUD_TOKEN"] = project_config.token

        logger.debug("Adding %s to PYTHONPATH from unpacked site packages", site_packages_path)
        environment[TCLOUD_PYTHON_PATH_ENV_VAR] = str(site_packages_path)

        subprocess.run(
            [executors_bin_path, executor_type],
            stdout=None,
            stderr=None,
            env=environment,
        )

    if once:
        install_and_run()
    else:
        while True:
            run_start_ts = time.monotonic()
            install_and_run()
            elapsed_sec = time.monotonic() - run_start_ts
            if elapsed_sec < EXECUTOR_MIN_INTERVAL_BETWEEN_RUNS_SEC:
                time.sleep(EXECUTOR_MIN_INTERVAL_BETWEEN_RUNS_SEC - elapsed_sec)


@cli.command("install_sqlmesh")
@click.pass_context
def install_sqlmesh(ctx: click.Context) -> None:
    """Install the correct version of SQLMesh Enterprise"""
    project = ctx.obj["project"]
    _install_sqlmesh_enterprise(project)


@cli.command("is_sqlmesh_installed", hidden=True)
@click.pass_context
def is_sqlmesh_installed(ctx: click.Context) -> None:
    """Check if SQLMesh Enterprise is installed"""
    project = ctx.obj["project"]
    project_config = load_project_config(project)
    installation_details = is_sqlmesh_enterprise_version_installed(
        project_config, load_previous_extras(project_config.url)
    )
    print(
        json.dumps(
            {
                "is_installed": installation_details.is_installed,
            }
        )
    )


cli.add_command(auth)
cli.add_command(project)


def _install_sqlmesh_enterprise(project: t.Optional[str]) -> None:
    try:
        project_config = load_project_config(project)
        installed = install_sqlmesh_enterprise(
            project_config, load_previous_extras(project_config.url)
        )
        if installed:
            save_previous_extras(project_config.url, project_config.extras or [])
    except (ValueError, requests.exceptions.RequestException) as ex:
        raise click.ClickException(str(ex)) from ex


if __name__ == "__main__":
    cli()
