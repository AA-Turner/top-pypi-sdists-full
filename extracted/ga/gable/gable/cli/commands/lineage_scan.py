import os
import shutil

import click
from click.core import Context as ClickContext

from gable.api.client import GableAPIClient
from gable.cli.helpers.lineage import build_sca_args, run_sca_and_capture
from gable.cli.helpers.npm import get_sca_cmd, prepare_npm_environment
from gable.cli.options import global_options


@click.command(
    add_help_option=False,
    name="scan",
    epilog="""Example:
    gable lineage scan --project-root ./path/to/project --language java --build-command "mvn clean install" --java-version 17""",
)
@global_options(add_endpoint_options=False)
@click.option(
    "--project-root",
    help="The root directory of the project that will be analyzed.",
    type=click.Path(exists=True),
    required=True,
)
@click.option(
    "--language",
    help="The programming language of the project.",
    type=click.Choice(["java"]),
    default="java",
)
@click.option(
    "--build-command",
    help="The build command used to build the project (e.g. mvn clean install).",
    type=str,
    required=False,
)
@click.option(
    "--java-version",
    help="The version of Java used to build the project.",
    type=str,
    default="17",
    required=False,
)
@click.option(
    "--dataflow-config-file",
    type=click.Path(exists=True),
    help="The path to the dataflow config JSON file.",
    required=False,
)
@click.option(
    "--schema-depth",
    help="The max depth of the schemas to be extracted.",
    type=int,
    required=False,
)
@click.option(
    "--output",
    type=click.Path(exists=False, file_okay=True, dir_okay=False),
    help="File path to output results.",
    required=False,
    default=os.path.join(os.getcwd(), "gable_lineage_scan_results.json"),
)
@click.pass_context
def lineage_scan(
    ctx: ClickContext,
    project_root: str,
    language: str,  # pylint: disable=unused-argument
    build_command: str,
    java_version: str,
    dataflow_config_file: str,
    schema_depth: int,
    output: click.Path,
):
    """
    Scan a project for data lineage using static code analysis (SCA).
    """
    client: GableAPIClient = ctx.obj.client
    prepare_npm_environment(client)

    output_str = str(output)
    output_dir = os.path.dirname(output_str)

    sca_cmd = get_sca_cmd(
        None,
        build_sca_args(
            project_root,
            java_version,
            build_command,
            dataflow_config_file,
            schema_depth,
            output_dir,
        ),
    )
    final_stdout = run_sca_and_capture(sca_cmd)
    shutil.move(os.path.join(output_dir, "results.json"), output_str)
    print(final_stdout)
