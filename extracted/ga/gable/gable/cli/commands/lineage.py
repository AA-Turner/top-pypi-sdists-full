import os
import select
import subprocess
import tempfile
import uuid
from typing import List, Optional, Tuple, Union
from urllib.parse import quote

import click
from click.core import Context as ClickContext
from loguru import logger

from gable.api.client import GableAPIClient
from gable.cli.helpers.data_asset import (
    determine_should_block,
    format_check_data_assets_json_output,
    format_check_data_assets_text_output,
)
from gable.cli.helpers.emoji import EMOJI
from gable.cli.helpers.npm import get_sca_cmd, prepare_npm_environment
from gable.cli.helpers.s3 import poll_sca_job_status, start_sca_run, upload_sca_results
from gable.cli.helpers.shell_output import shell_linkify_if_not_in_ci
from gable.cli.options import global_options
from gable.openapi import (
    CheckDataAssetCommentMarkdownResponse,
    CheckDataAssetDetailedResponse,
    CheckDataAssetErrorResponse,
    CheckDataAssetMissingAssetResponse,
    CheckDataAssetNoChangeResponse,
    CheckDataAssetNoContractResponse,
    CheckDataAssetResponse,
    S3PresignedUrl,
)


def handle_darn_to_string(darn: dict) -> str:
    """Convert a DARN to a string representation."""
    source_type = darn.get("source_type", "unknown")
    data_source = darn.get("data_source", "unknown")
    path = darn.get("path", "unknown")
    return f"{source_type}://{data_source}:{path}"


ResponseTypes = Union[
    CheckDataAssetNoContractResponse,
    CheckDataAssetNoChangeResponse,
    CheckDataAssetDetailedResponse,
    CheckDataAssetErrorResponse,
    CheckDataAssetMissingAssetResponse,
    CheckDataAssetCommentMarkdownResponse,
]

DefaultUnion = [
    CheckDataAssetNoContractResponse,
    CheckDataAssetNoChangeResponse,
    CheckDataAssetDetailedResponse,
    CheckDataAssetErrorResponse,
    CheckDataAssetMissingAssetResponse,
]


def try_parse_response(line: str) -> ResponseTypes:
    for model in [
        CheckDataAssetNoContractResponse,
        CheckDataAssetNoChangeResponse,
        CheckDataAssetDetailedResponse,
        CheckDataAssetErrorResponse,
        CheckDataAssetMissingAssetResponse,
        CheckDataAssetCommentMarkdownResponse,
    ]:
        try:
            return model.parse_raw(line)
        except Exception:
            continue
    raise ValueError(f"Could not parse line: {line}")


def resolve_results_dir(run_id: str) -> str:
    """Use SCA_RESULTS_DIR if present; else a default path that includes the run id."""
    env_dir = os.environ.get("SCA_RESULTS_DIR")
    if env_dir:
        logger.debug(f"Using SCA_RESULTS_DIR from environment: {env_dir}")
        return env_dir
    default_dir = f"/var/tmp/sca_results/{run_id}"
    logger.debug(f"Using default results directory: {default_dir}")
    return default_dir


def ensure_npm_and_maybe_start_run(
    ctx: ClickContext,
    project_root: str,
    action: str,
    output: Optional[str],
    include_unchanged_assets: Optional[bool],
) -> Tuple[str, Optional[S3PresignedUrl]]:
    """
    If isolation is disabled, set up npm auth and start a backend SCA run.
    Otherwise just fabricate a run id and skip presigned URL.
    """
    isolation = os.getenv("GABLE_CLI_ISOLATION", "false").lower() == "true"
    if isolation:
        logger.info("GABLE_CLI_ISOLATION is true, skipping NPM authentication")
        return str(uuid.uuid4()), None

    client: GableAPIClient = ctx.obj.client
    prepare_npm_environment(client)
    run_id, presigned_url = start_sca_run(
        client, project_root, action, output, include_unchanged_assets
    )
    logger.debug(f"Starting static code analysis run with ID: {run_id}")
    return run_id, presigned_url


def build_sca_args(
    project_root: str,
    java_version: str,
    build_command: Optional[str],
    dataflow_config_file: Optional[str],
    schema_depth: Optional[int],
    results_dir: str,
) -> List[str]:
    args = (
        [
            "java-dataflow",
            project_root,
            "--java-version",
            java_version,
        ]
        + (["--build-command", build_command] if build_command else [])
        + (
            ["--dataflow-config-file", dataflow_config_file]
            if dataflow_config_file
            else []
        )
        + (["--schema-depth", str(schema_depth)] if schema_depth else [])
        + (["--results-dir", results_dir] if results_dir else [])
    )
    return args


def run_sca_and_capture(sca_cmd: List[str]) -> str:
    """Run SCA, stream logs, return combined stdout; raise on non-zero exit."""
    logger.debug(f"Running SCA command: {' '.join(sca_cmd)}")

    process = subprocess.Popen(
        sca_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=-1,
    )

    stdout_chunks: List[str] = []

    # Stream both pipes to keep live feedback
    while True:
        reads = []
        if process.stdout:
            reads.append(process.stdout)
        if process.stderr:
            reads.append(process.stderr)
        if not reads:
            break

        ready, _, _ = select.select(reads, [], [])
        for stream in ready:
            line = stream.readline()
            if not line:
                continue
            if stream == process.stdout:
                stdout_chunks.append(line)
            else:
                logger.debug(line.rstrip("\n"))

        if process.poll() is not None:
            break

    # Drain any remaining stdout
    if process.stdout:
        remaining = process.stdout.read()
        if remaining:
            stdout_chunks.append(remaining)

    process.wait()
    final_stdout = "".join(stdout_chunks)
    print(final_stdout, end="")

    if process.returncode != 0:
        raise click.ClickException("Error running Gable SCA")

    return final_stdout


def upload_results_and_poll(
    client: GableAPIClient, run_id: str, presigned_url: S3PresignedUrl, results_dir: str
):
    """Upload SCA results to S3 and poll job status; return outcomes dict."""
    logger.debug(f"Uploading SCA results from run {run_id} to S3: {presigned_url.url}")
    upload_sca_results(run_id, presigned_url, results_dir)
    key = presigned_url.fields.get("key", "")
    parts = key.split("/")
    if len(parts) < 3:
        raise click.ClickException("Invalid presigned URL fields format")
    job_id = parts[2]
    return poll_sca_job_status(client, job_id)


def run_llm_feature_extraction(sca_results: str, project_root: str):
    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".json", encoding="utf-8"
    ) as f:
        f.write(sca_results)
    feature_extraction_cmd = [
        "./venv/bin/python",
        "-m",
        "main",
        "--repo",
        os.path.abspath(project_root),
        "--sca",
        f.name,
    ]
    logger.debug(
        f"Calling feature extraction subprocess: {' '.join(feature_extraction_cmd)}"
    )
    feature_extraction_result = subprocess.run(
        feature_extraction_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../../../../../sca-pl-mve/",
        ),
    )
    if feature_extraction_result.returncode != 0:
        logger.debug(feature_extraction_result.stdout)
        logger.debug(feature_extraction_result.stderr)
        raise click.ClickException(
            f"Error running Gable feature extraction: {feature_extraction_result.stderr}"
        )
    print(feature_extraction_result.stdout)


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
    "--llm-extraction/--no-llm-extraction",
    help="Use LLM for feature extraction.",
    type=bool,
    default=False,
    is_flag=True,
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
    llm_extraction: bool,
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

    if llm_extraction:
        run_llm_feature_extraction(final_stdout, project_root)
    else:
        logger.debug("Skipping LLM feature extraction")


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
    "--llm-extraction/--no-llm-extraction",
    help="Use LLM for feature extraction.",
    type=bool,
    default=False,
    is_flag=True,
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
    llm_extraction: bool,
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

    if llm_extraction:
        run_llm_feature_extraction(final_stdout, project_root)
    else:
        print("Skipping LLM feature extraction")


@click.group(name="lineage")
@global_options(add_endpoint_options=False)
def lineage():
    """Commands for data lineage analysis using static code analysis (SCA)"""


lineage.add_command(register_lineage)
lineage.add_command(check_lineage)
