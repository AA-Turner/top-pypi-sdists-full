from copy import deepcopy
from functools import partial
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
from urllib.parse import urlencode

import click

from tinybird.datafile.exceptions import ParseException
from tinybird.datafile.parse_datasource import parse_datasource
from tinybird.datafile.parse_pipe import parse_pipe
from tinybird.tb.client import TinyB
from tinybird.tb.config import CLOUD_HOSTS
from tinybird.tb.modules.build_common import process
from tinybird.tb.modules.cli import cli, get_current_git_branch
from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.project import Project
from tinybird.tb.modules.query_output import print_table_formatted
from tinybird.tb.modules.watch import watch_project


def _get_dashboard_url(config: Dict[str, Any], branch_name: str, is_local: bool) -> Optional[str]:
    host = config.get("host", "")
    cloud_base = CLOUD_HOSTS.get(host)
    workspace_name = config.get("name", "")
    if not cloud_base or not workspace_name:
        return None
    if is_local:
        return f"{cloud_base}/{workspace_name}~local~{branch_name}"
    return f"{cloud_base}/{workspace_name}~{branch_name}"


def echo_branch_info(obj: Dict[str, Any]) -> None:
    local_branch = obj.get("local_branch")
    cloud_branch = obj.get("branch")
    if not local_branch and not cloud_branch:
        return
    git_branch = obj.get("git_branch") or get_current_git_branch()
    branch_created = obj.get("branch_created", False)
    status = "✓ created" if branch_created else "✓ exists"
    config = obj.get("config", {})
    if git_branch:
        click.echo(FeedbackManager.highlight(message=f"» Git branch:            {git_branch}"))
    if local_branch:
        click.echo(FeedbackManager.highlight(message=f"» Tinybird Local branch: {local_branch} {status}"))
        dashboard_url = _get_dashboard_url(config, local_branch, is_local=True)
    elif cloud_branch:
        click.echo(FeedbackManager.highlight(message=f"» Tinybird Cloud branch: {cloud_branch} {status}"))
        dashboard_url = _get_dashboard_url(config, cloud_branch, is_local=False)
    else:
        dashboard_url = None
    if dashboard_url:
        click.echo(FeedbackManager.gray(message=f"  ↳ {dashboard_url}"))


@cli.command()
@click.option("--watch", is_flag=True, default=False, help="Watch for changes and rebuild automatically")
@click.option(
    "--with-connections",
    is_flag=True,
    default=False,
    help="Create data linkers for connection datasources (S3, Kafka, GCS) during build",
)
@click.pass_context
def build(ctx: click.Context, watch: bool, with_connections: bool) -> None:
    """
    Validate and build the project server side.
    """
    obj: Dict[str, Any] = ctx.ensure_object(dict)
    project: Project = ctx.ensure_object(dict)["project"]
    tb_client: TinyB = ctx.ensure_object(dict)["client"]
    config: Dict[str, Any] = ctx.ensure_object(dict)["config"]
    is_branch = bool(ctx.ensure_object(dict)["branch"])
    use_deployment_api = obj["env"] == "cloud" and is_branch

    # TODO: Explain that you can use custom branches too once they are open for everyone
    if obj["env"] == "cloud" and not is_branch:
        raise click.ClickException(FeedbackManager.error_build_only_supported_in_local())

    if project.has_deeper_level():
        click.echo(
            FeedbackManager.warning(
                message=f"Your project contains directories nested deeper than the used scan depth (max_depth={project.max_depth}). "
                "Files in these deeper directories will not be processed. "
                f"If you have tinybird files in directories deeper than {project.max_depth} levels, you can use "
                "`tb --max-depth <depth> <cmd>` with a higher depth value. "
                "Otherwise you can ignore this warning."
            )
        )

    echo_branch_info(obj)
    click.echo(FeedbackManager.highlight_building_project())
    process(
        project=project,
        tb_client=tb_client,
        watch=False,
        config=config,
        is_branch=is_branch,
        with_connections=with_connections,
        use_deployment_api=use_deployment_api,
    )
    if watch:
        run_watch(
            project=project,
            config=config,
            process=partial(
                process,
                project=project,
                tb_client=tb_client,
                watch=True,
                config=config,
                is_branch=is_branch,
                with_connections=with_connections,
                use_deployment_api=use_deployment_api,
            ),
        )


@cli.command("dev", help="Build the project server side and watch for changes.")
@click.option(
    "--with-connections/--no-connections",
    default=None,
    help="Create data linkers for connection datasources (S3, Kafka, GCS). Defaults to true for branches.",
)
@click.pass_context
def dev(ctx: click.Context, with_connections: Optional[bool]) -> None:
    obj: Dict[str, Any] = ctx.ensure_object(dict)
    branch: Optional[str] = ctx.ensure_object(dict)["branch"]
    is_branch = bool(branch)
    use_deployment_api = obj["env"] == "cloud" and is_branch

    # Default with_connections to True for branches, False otherwise
    if with_connections is None:
        with_connections = is_branch

    if obj["env"] == "cloud" and not is_branch:
        raise click.ClickException(FeedbackManager.error_build_only_supported_in_local())

    project: Project = ctx.ensure_object(dict)["project"]
    tb_client: TinyB = ctx.ensure_object(dict)["client"]
    config: Dict[str, Any] = ctx.ensure_object(dict)["config"]

    echo_branch_info(obj)
    click.echo(FeedbackManager.highlight_building_project())
    process(
        project=project,
        tb_client=tb_client,
        watch=True,
        config=config,
        is_branch=is_branch,
        with_connections=with_connections,
        use_deployment_api=use_deployment_api,
    )
    run_watch(
        project=project,
        config=config,
        process=partial(
            process,
            project=project,
            tb_client=tb_client,
            config=config,
            is_branch=is_branch,
            with_connections=with_connections,
            use_deployment_api=use_deployment_api,
        ),
    )


def run_watch(project: Project, process: Callable, config: dict[str, Any]) -> None:
    click.echo(FeedbackManager.gray(message="\nWatching for changes..."))
    watch_project(process=process, project=project, config=config)


def is_vendor(f: Path) -> bool:
    return f.parts[0] == "vendor"


def is_endpoint(f: Path) -> bool:
    return f.suffix == ".pipe" and not is_vendor(f) and f.parts[0] == "endpoints"


def is_pipe(f: Path) -> bool:
    return f.suffix == ".pipe" and not is_vendor(f)


def check_filenames(filenames: List[str]):
    parser_matrix = {".pipe": parse_pipe, ".datasource": parse_datasource}
    incl_suffix = ".incl"

    for filename in filenames:
        file_suffix = Path(filename).suffix
        if file_suffix == incl_suffix:
            continue

        parser = parser_matrix.get(file_suffix)
        if not parser:
            raise ParseException(FeedbackManager.error_unsupported_datafile(extension=file_suffix))

        parser(filename)


def build_and_print_resource(config: CLIConfig, tb_client: TinyB, filename: str):
    resource_path = Path(filename)
    name = resource_path.stem
    playground_name = name if filename.endswith(".pipe") else None
    user_client = deepcopy(tb_client)
    user_client.token = config.get_user_token() or ""
    cli_params = {}
    cli_params["workspace_id"] = config.get("id", None)
    data = user_client._req(f"/v0/playgrounds?{urlencode(cli_params)}")
    playgrounds = data["playgrounds"]
    playground = next((p for p in playgrounds if p["name"] == (f"{playground_name}" + "__tb__playground")), None)
    if not playground:
        return
    playground_id = playground["id"]
    last_node = playground["nodes"][-1]
    if not last_node:
        return
    node_sql = last_node["sql"]
    res = tb_client.query(f"{node_sql} FORMAT JSON", playground=playground_id)
    print_table_formatted(res, name)
