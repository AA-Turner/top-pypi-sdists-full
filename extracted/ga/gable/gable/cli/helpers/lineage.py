import os
import select
import subprocess
import uuid
from typing import List, Optional, Tuple, Union

import click
from click.core import Context as ClickContext
from loguru import logger

from gable.api.client import GableAPIClient
from gable.cli.helpers.npm import prepare_npm_environment
from gable.cli.helpers.s3 import poll_sca_job_status, start_sca_run, upload_sca_results
from gable.openapi import (
    CheckDataAssetCommentMarkdownResponse,
    CheckDataAssetDetailedResponse,
    CheckDataAssetErrorResponse,
    CheckDataAssetMissingAssetResponse,
    CheckDataAssetNoChangeResponse,
    CheckDataAssetNoContractResponse,
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
