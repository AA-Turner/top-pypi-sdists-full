import os
import select
import subprocess
import tempfile
from typing import Optional
import uuid

import click
from click.core import Context as ClickContext
from gable.api.client import GableAPIClient
from gable.cli.helpers.npm import get_sca_cmd, prepare_npm_environment
from gable.cli.helpers.s3 import upload_sca_results, start_sca_run
from gable.cli.options import global_options
from gable.openapi import S3PresignedUrl

from loguru import logger

@click.command(
    add_help_option=False,
    hidden=True,
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
def lineage(
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
    Run static code analysis (SCA) to extract data lineage.
    """
    run_id: str = str(uuid.uuid4())
    presigned_url: Optional[S3PresignedUrl] = None

    if os.getenv("GABLE_CLI_ISOLATION", "false").lower() == "true":
        logger.info("GABLE_CLI_ISOLATION is true, skipping NPM authentication")
    else:
        client: GableAPIClient = ctx.obj.client
        prepare_npm_environment(client)
        run_id, presigned_url = start_sca_run(client, project_root)
        logger.debug(f"Starting static code analysis run with ID: {run_id}")

    # If SCA_RESULTS_DIR is set, use that. Otherwise use the default temp path with run_id.
    results_dir = os.environ.get('SCA_RESULTS_DIR')
    if results_dir:
        logger.debug(f"Using SCA_RESULTS_DIR from environment: {results_dir}")
    else:
        results_dir = f"/var/tmp/sca_results/{run_id}"
        logger.debug(f"Using default results directory: {results_dir}") 

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

    stdout_output = []

    sca_cmd = get_sca_cmd(None, args)
    logger.debug(f"Running SCA command: {' '.join(sca_cmd)}")

    process = subprocess.Popen(
        sca_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=-1,  # Use system default buffering
    )

    # Read both streams concurrently.
    while True:
        reads = []
        if process.stdout:
            reads.append(process.stdout)
        if process.stderr:
            reads.append(process.stderr)

        if not reads:
            break

        # Wait until at least one stream has data
        ready, _, _ = select.select(reads, [], [])

        for stream in ready:
            line = stream.readline()
            if not line:
                continue
            if stream == process.stdout:
                stdout_output.append(line)
            elif stream == process.stderr:
                logger.debug(line.rstrip("\n"))

        if process.poll() is not None:
            break

    # Drain any remaining stdout (if any)
    if process.stdout:
        remaining = process.stdout.read()
        if remaining:
            stdout_output.append(remaining)

    process.wait()
    final_stdout = "".join(stdout_output)

    print(final_stdout, end="")

    if process.returncode != 0:
        raise click.ClickException(f"Error running Gable SCA")
    
    # Upload the SCA results to S3
    if presigned_url:
        logger.debug(f"Uploading SCA results from run {run_id} to S3: {presigned_url.url}")
        upload_sca_results(run_id, presigned_url, results_dir)

    if llm_extraction:
        run_llm_feature_extraction(final_stdout, project_root)
    else:
        print("Skipping LLM feature extraction")
        return


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
    logger.debug(
        f"Calling feature extraction subprocess: {' '.join(feature_extraction_cmd)}"
    )
    if feature_extraction_result.returncode != 0:
        logger.debug(feature_extraction_result.stdout)
        logger.debug(feature_extraction_result.stderr)
        raise click.ClickException(
            f"Error running Gable feature extraction: {feature_extraction_result.stderr}"
        )
    print(feature_extraction_result.stdout)
