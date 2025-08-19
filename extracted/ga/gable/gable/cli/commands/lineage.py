from typing import List
from urllib.parse import quote

import click
from click.core import Context as ClickContext
from loguru import logger

from gable.api.client import GableAPIClient
from gable.cli.commands.lineage_enrich import lineage_enrich
from gable.cli.commands.lineage_scan import lineage_scan
from gable.cli.helpers.data_asset import (
    determine_should_block,
    format_check_data_assets_json_output,
    format_check_data_assets_text_output,
)
from gable.cli.helpers.emoji import EMOJI
from gable.cli.helpers.lineage import (
    ResponseTypes,
    build_sca_args,
    ensure_npm_and_maybe_start_run,
    handle_darn_to_string,
    resolve_results_dir,
    run_sca_and_capture,
    try_parse_response,
    upload_results_and_poll,
)
from gable.cli.helpers.npm import get_sca_cmd
from gable.cli.helpers.shell_output import shell_linkify_if_not_in_ci
from gable.cli.options import global_options
from gable.openapi import CheckDataAssetCommentMarkdownResponse, CheckDataAssetResponse


@click.command(
    add_help_option=False,
    name="register",
    epilog="""Example:
    gable lineage register --project-root ./path/to/project --language java --build-command "mvn clean install" --java-version 17""",
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
@click.pass_context
def register_lineage(
    ctx: ClickContext,
    project_root: str,
    language: str,  # pylint: disable=unused-argument
    build_command: str,
    java_version: str,
    dataflow_config_file: str,
    schema_depth: int,
):
    """
    Run static code analysis (SCA) to extract and register data lineage.
    """
    run_id, presigned_url = ensure_npm_and_maybe_start_run(
        ctx, project_root, action="register", output=None, include_unchanged_assets=None
    )
    results_dir = resolve_results_dir(run_id)

    sca_cmd = get_sca_cmd(
        None,
        build_sca_args(
            project_root,
            java_version,
            build_command,
            dataflow_config_file,
            schema_depth,
            results_dir,
        ),
    )
    final_stdout = run_sca_and_capture(sca_cmd)

    if presigned_url:
        client: GableAPIClient = ctx.obj.client
        sca_outcomes = upload_results_and_poll(
            client, run_id, presigned_url, results_dir
        )

        registered_assets = 0
        for outcome in sca_outcomes.get("asset_registration_outcomes", []):
            if outcome.get("error"):
                click.echo(
                    f"{EMOJI.RED_X.value} Error registering data asset: {outcome['error']}"
                )
                continue

            darn_string = handle_darn_to_string(
                outcome.get("data_asset_resource_name", {})
            )
            maybe_linkified_darn = shell_linkify_if_not_in_ci(
                f"{client.ui_endpoint}/assets/{quote(darn_string, safe='')}",
                darn_string,
            )
            registered_assets += 1
            click.echo(
                f"{EMOJI.GREEN_CHECK.value} Data asset {maybe_linkified_darn} registered successfully"
            )
        if registered_assets > 0:
            click.echo(f"{registered_assets} assets registered successfully")


@click.command(
    add_help_option=False,
    name="check",
    epilog="""Example:
    gable lineage check --project-root ./path/to/project --language java --build-command "mvn clean install" --java-version 17""",
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
    "--include-unchanged-assets",
    type=bool,
    default=False,
    help=(
        "Include assets that are the same as Gable's registered version of the asset. "
        "Useful for checking current state; avoid in automated branch checks."
    ),
)
@click.option(
    "-o",
    "--output",
    type=click.Choice(["text", "json", "markdown"]),
    default="text",
    help="Output format: text (default), json, or markdown (for PR comments).",
)
@click.pass_context
def check_lineage(
    ctx: ClickContext,
    project_root: str,
    language: str,  # pylint: disable=unused-argument
    build_command: str,
    java_version: str,
    dataflow_config_file: str,
    schema_depth: int,
    include_unchanged_assets: bool,
    output: str,
):
    """
    Run static code analysis (SCA) to extract and check data lineage.
    """
    run_id, presigned_url = ensure_npm_and_maybe_start_run(
        ctx,
        project_root,
        action="check",
        output=output,
        include_unchanged_assets=include_unchanged_assets,
    )
    results_dir = resolve_results_dir(run_id)

    sca_cmd = get_sca_cmd(
        None,
        build_sca_args(
            project_root,
            java_version,
            build_command,
            dataflow_config_file,
            schema_depth,
            results_dir,
        ),
    )
    final_stdout = run_sca_and_capture(sca_cmd)

    if presigned_url:
        client: GableAPIClient = ctx.obj.client
        sca_outcomes = upload_results_and_poll(
            client, run_id, presigned_url, results_dir
        )

        messages = sca_outcomes.get("message", "") or ""
        lines = messages.splitlines()
        parsed: List[ResponseTypes] = [
            try_parse_response(line) for line in lines if line.strip()
        ]

        for resp in parsed:
            if isinstance(resp, CheckDataAssetCommentMarkdownResponse):
                if resp.markdown:
                    logger.info(resp.markdown)  # stdout-friendly for CI to pick up

                if resp.shouldBlock:
                    raise click.ClickException(
                        f"{EMOJI.RED_X.value} Contract violations found, maximum enforcement level was 'BLOCK'"
                    )
                if resp.shouldAlert:
                    logger.error(
                        f"{EMOJI.YELLOW_WARNING.value} Contract violations found, maximum enforcement level was 'ALERT'"
                    )
                if resp.errors:
                    errors_string = "\n".join([err.json() for err in resp.errors])
                    raise click.ClickException(
                        f"{EMOJI.RED_X.value} Contract checking failed for some data assets:\n{errors_string}"
                    )
                continue

            check_resp = CheckDataAssetResponse.model_validate(resp)
            should_block = determine_should_block([check_resp])

            if output == "markdown":
                raise click.ClickException(
                    "Markdown response not received from backend although requested"
                )
            elif output == "json":
                out = format_check_data_assets_json_output([check_resp])
            else:
                out = format_check_data_assets_text_output([check_resp])

            logger.info(out)
            if should_block:
                raise click.ClickException("Contract violation(s) found")


@click.group(name="lineage")
@global_options(add_endpoint_options=False)
def lineage():
    """Commands for data lineage analysis using static code analysis (SCA)"""


lineage.add_command(register_lineage)
lineage.add_command(check_lineage)
lineage.add_command(lineage_scan)
lineage.add_command(lineage_enrich)
