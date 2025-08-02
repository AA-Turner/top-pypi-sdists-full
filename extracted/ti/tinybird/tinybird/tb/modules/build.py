import threading
import time
from copy import deepcopy
from functools import partial
from pathlib import Path
from typing import Any, Callable, Dict, List
from urllib.parse import urlencode

import click

import tinybird.context as context
from tinybird.datafile.exceptions import ParseException
from tinybird.datafile.parse_datasource import parse_datasource
from tinybird.datafile.parse_pipe import parse_pipe
from tinybird.tb.client import TinyB
from tinybird.tb.modules.build_common import process
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.datafile.playground import folder_playground
from tinybird.tb.modules.dev_server import BuildStatus, start_server
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.project import Project
from tinybird.tb.modules.shell import Shell, print_table_formatted
from tinybird.tb.modules.watch import watch_files, watch_project


@cli.command()
@click.option("--watch", is_flag=True, default=False, help="Watch for changes and rebuild automatically")
@click.pass_context
def build(ctx: click.Context, watch: bool) -> None:
    """
    Validate and build the project server side.
    """
    obj: Dict[str, Any] = ctx.ensure_object(dict)
    project: Project = ctx.ensure_object(dict)["project"]
    tb_client: TinyB = ctx.ensure_object(dict)["client"]
    if obj["env"] == "cloud":
        raise click.ClickException(FeedbackManager.error_build_only_supported_in_local())

    if project.has_deeper_level():
        click.echo(
            FeedbackManager.warning(
                message="Your project contains directories nested deeper than the default scan depth (max_depth=3). "
                "Files in these deeper directories will not be processed. "
                "To include all nested directories, run `tb --max-depth <depth> <cmd>` with a higher depth value."
            )
        )

    click.echo(FeedbackManager.highlight_building_project())
    process(project=project, tb_client=tb_client, watch=False)
    if watch:
        run_watch(
            project=project,
            tb_client=tb_client,
            process=partial(process, project=project, tb_client=tb_client, watch=True),
        )


@cli.command("dev", help="Build the project server side and watch for changes.")
@click.option("--data-origin", type=str, default="", help="Data origin: local or cloud")
@click.option("--ui", is_flag=True, default=False, help="Connect your local project to Tinybird UI")
@click.pass_context
def dev(ctx: click.Context, data_origin: str, ui: bool) -> None:
    if data_origin == "cloud":
        return dev_cloud(ctx)
    project: Project = ctx.ensure_object(dict)["project"]
    tb_client: TinyB = ctx.ensure_object(dict)["client"]
    build_status = BuildStatus()
    if ui:
        server_thread = threading.Thread(
            target=start_server, args=(project, tb_client, process, build_status), daemon=True
        )
        server_thread.start()
        # Wait for the server to start
        time.sleep(0.5)

    click.echo(FeedbackManager.highlight_building_project())
    process(project=project, tb_client=tb_client, watch=True, build_status=build_status)
    run_watch(
        project=project,
        tb_client=tb_client,
        process=partial(process, project=project, tb_client=tb_client, build_status=build_status),
    )


def run_watch(project: Project, tb_client: TinyB, process: Callable) -> None:
    shell = Shell(project=project, tb_client=tb_client, playground=False)
    click.echo(FeedbackManager.gray(message="\nWatching for changes..."))
    watcher_thread = threading.Thread(
        target=watch_project,
        args=(shell, process, project),
        daemon=True,
    )
    watcher_thread.start()
    shell.run()


def is_vendor(f: Path) -> bool:
    return f.parts[0] == "vendor"


def get_vendor_workspace(f: Path) -> str:
    return f.parts[1]


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


def dev_cloud(
    ctx: click.Context,
) -> None:
    project: Project = ctx.ensure_object(dict)["project"]
    config = CLIConfig.get_project_config()
    tb_client: TinyB = config.get_client()
    context.disable_template_security_validation.set(True)

    def process(filenames: List[str], watch: bool = False):
        datafiles = [f for f in filenames if f.endswith(".datasource") or f.endswith(".pipe")]
        if len(datafiles) > 0:
            check_filenames(filenames=datafiles)
            folder_playground(
                project, config, tb_client, filenames=datafiles, is_internal=False, current_ws=None, local_ws=None
            )
        if len(filenames) > 0 and watch:
            filename = filenames[0]
            build_and_print_resource(config, tb_client, filename)

    datafiles = project.get_project_files()
    filenames = datafiles

    def build_once(filenames: List[str]):
        ok = False
        try:
            click.echo(FeedbackManager.highlight(message="» Building project...\n"))
            time_start = time.time()
            process(filenames=filenames, watch=False)
            time_end = time.time()
            elapsed_time = time_end - time_start

            click.echo(FeedbackManager.success(message=f"\n✓ Build completed in {elapsed_time:.1f}s"))
            ok = True
        except Exception as e:
            error_path = Path(".tb_error.txt")
            if error_path.exists():
                content = error_path.read_text()
                content += f"\n\n{str(e)}"
                error_path.write_text(content)
            else:
                error_path.write_text(str(e))
            click.echo(FeedbackManager.error_exception(error=e))
            ok = False
        return ok

    build_ok = build_once(filenames)

    shell = Shell(project=project, tb_client=tb_client, playground=True)
    click.echo(FeedbackManager.gray(message="\nWatching for changes..."))
    watcher_thread = threading.Thread(
        target=watch_files, args=(filenames, process, shell, project, build_ok), daemon=True
    )
    watcher_thread.start()
    shell.run()


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
