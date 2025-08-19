import glob
import json
import os
import platform
import shutil
import subprocess
import tempfile
import threading
from typing import Any, List, Optional, Union

import click
from loguru import logger

import gable.cli.helpers.sca_exceptions as sca_exceptions
from gable.api.client import GableAPIClient
from gable.cli.helpers.auth import set_npm_config_credentials
from gable.cli.helpers.logging import get_winston_log_level
from gable.cli.local import get_local_sca_path, get_local_sca_prime
from gable.openapi import CreateTelemetryRequest, TelemetryType

BASE_NPX_CMD = [
    "npx",
    "-y",
    "-q",
    "@gable-eng/sca@<1.0.0",
]

# Used for gable cli command in docker container environments
DOCKER_NODE_CMD = [
    "node",
    "/app/npm/dist/index.cjs",
]

# Required feature flag value when running in isolated mode
REQUIRED_ISOLATION_FEATURE_FLAG = "GDoBcuPkip0K9RZTTWFJwZ8YyMXgeb"


def prepare_npm_environment(client: GableAPIClient) -> None:
    if os.getenv("GABLE_CLI_ISOLATION", "false").lower() == "true":
        logger.debug("Running Gable cli in isolation")
        # Require a feature flag when running in isolated mode
        feature_flag = os.getenv("GABLE_CLI_FEATURE_FLAG", "")
        if feature_flag != REQUIRED_ISOLATION_FEATURE_FLAG:
            raise click.ClickException(
                f"Limited permission to run Gable CLI. Please contact Gable Support for assistance."
            )
        return
    # Verify node is installed
    check_node_installed()

    # Get temporary NPM credentials, set as environment variables
    npm_credentials = client.get_auth_npm()
    set_npm_config_credentials(npm_credentials)


def check_node_installed():
    try:
        result = subprocess.run(
            ["node", "--version"], check=True, stdout=subprocess.PIPE, text=True
        )
        version = result.stdout.strip().replace("v", "")
        if int(version.split(".")[0]) < 14:
            raise click.ClickException(
                f"Node.js version {version} is not supported. Please install Node.js 14 or later."
            )
    except FileNotFoundError:
        raise click.ClickException(
            "Node.js is not installed. Please install Node.js 18 or later."
        )


def run_sca_pyspark(
    project_root: str,
    python_executable_path: str,
    spark_job_entrypoint: str,
    connection_string: Optional[str],
    metastore_connection_string: Optional[str],
    csv_schema_file: Optional[str],
    csv_path_to_table_file: Optional[str],
    api_endpoint: Union[str, None] = None,
) -> str:
    try:
        commands = [
            "pyspark",
            project_root,
            "--python-executable-path",
            python_executable_path,
            "--spark-job-entrypoint",
            spark_job_entrypoint,
        ]
        if connection_string is not None:
            commands += ["--connection-string", connection_string]
        if metastore_connection_string is not None:
            commands += ["--metastore-connection-string", metastore_connection_string]
        if csv_schema_file is not None:
            commands += ["--csv-schema-file", csv_schema_file]
        if csv_path_to_table_file is not None:
            commands += ["--csv-path-to-table-map-file", csv_path_to_table_file]
        cmd = get_sca_cmd(
            api_endpoint,
            commands,
        )
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode != 0:
            logger.debug(result.stderr)
            raise click.ClickException(result.stdout)
        logger.debug(result.stdout)
        logger.trace(result.stderr)
        # The sca CLI prints the results to stdout,and everything else to trace/warn/debug/error
        return result.stdout
    except Exception as e:
        logger.opt(exception=e).debug("Error running Gable SCA")
        sca_e = sca_exceptions.create_pyspark_exception(e)
        if sca_e is not None:
            logger.info(str(sca_e.markdown))
            raise sca_e
        raise click.ClickException("Error running Gable SCA: \n\n" + str(e))


def run_sca_python(
    project_root: str,
    emitter_file_path: str,
    emitter_function: str,
    emitter_payload_parameter: str,
    event_name_key: str,
    exclude_paths: Optional[str],
    api_endpoint: Union[str, None] = None,
) -> str:
    try:
        excludes = ["--exclude", exclude_paths] if exclude_paths else []
        cmd = get_sca_cmd(
            api_endpoint,
            [
                "python",
                project_root,
                "--emitter-file-path",
                emitter_file_path,
                "--emitter-function",
                emitter_function,
                "--emitter-payload-parameter",
                emitter_payload_parameter,
                "--event-name-key",
                event_name_key,
            ]
            + excludes,
        )

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode != 0:
            logger.debug(result.stderr)
            raise click.ClickException(f"Error running Gable SCA: {result.stderr}")
        logger.debug(result.stdout)
        logger.trace(result.stderr)
        # The sca CLI prints the results to stdout,and everything else to trace/warn/debug/error
        return result.stdout
    except Exception as e:
        logger.opt(exception=e).debug("Error running Gable SCA")
        raise click.ClickException(
            "Error running Gable SCA, run again with --debug to see more details"
        )


def run_sca_typescript(
    library: Optional[str],
    node_modules_include: Optional[str],
    project_root: str,
    emitter_file_path: Optional[str],
    emitter_function: Optional[str],
    emitter_payload_parameter: Optional[str],
    event_name_key: Optional[str],
    event_name_parameter: Optional[str],
    exclude: Optional[str],
    client: GableAPIClient,
) -> tuple[str, dict[str, dict[str, Any]]]:
    try:
        if library is not None:
            options = ["--library", library]
        else:
            options = [
                # TODO: switch this to --emitter-location once the new NPM package is released
                # and some time has passed
                "--emitter-file-path",
                emitter_file_path,
                "--emitter-function",
                emitter_function,
                "--emitter-payload-parameter",
                emitter_payload_parameter,
            ]
            if event_name_key is not None:
                options += ["--event-name-key", event_name_key]
            elif event_name_parameter is not None:
                options += ["--event-name-parameter", event_name_parameter]

        if node_modules_include is not None:
            options += ["--node-modules-include", node_modules_include]
        if exclude is not None:
            options += ["--exclude", exclude]

        cmd = get_sca_cmd(
            client.endpoint,
            ["typescript", project_root] + options,
        )
        sca_prime_results_future = start_sca_prime(client, project_root, [])
        result_proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            universal_newlines=True,
            bufsize=1,
            env={"LOG_LEVEL": get_winston_log_level(), **os.environ},
        )

        # Stream debug logs from the subprocess stderr from subprocess back to logs
        result_proc_stderr_lines = []
        while True:
            output = "" if not result_proc.stderr else result_proc.stderr.readline()
            if output == "" and result_proc.poll() is not None:
                break
            if output:
                result_proc_stderr_lines.append(output)
                logger.debug(output.rstrip())

        result_proc.wait()
        result_proc_stdout = result_proc.stdout.read() if result_proc.stdout else ""
        result_proc_stderr = "".join(result_proc_stderr_lines)
        if result_proc.returncode != 0:
            raise click.ClickException(f"Error running Gable SCA: {result_proc_stderr}")
        logger.debug(result_proc_stdout)

        # Run sca-prime
        sca_prime_results, _ = get_sca_prime_results(
            sca_prime_results_future, client, project_root, True
        )
        # The sca CLI prints the results to stdout,and everything else to trace/warn/debug/error
        return result_proc_stdout, sca_prime_results
    except Exception as e:
        logger.opt(exception=e).debug("Error running Gable SCA")
        raise click.ClickException(
            "Error running Gable SCA, run again with --debug to see more details"
        )


def get_sca_cmd(gable_api_endpoint: Union[str, None], args: list[str]) -> list[str]:
    """Constructs the full command to run sca"""
    # In CI/CD environments, running multiple gable cli commands in parallel
    # can cause a race condition when attempting to delete the npm cache folder.
    # Verify GABLE_CLI_ISOLATION to ensure the installed npm packages
    # are retained during the Docker run.
    if (
        os.environ.get("GABLE_CONCURRENT") != "true"
        and os.environ.get("GABLE_CLI_ISOLATION") != "true"
    ):
        shutil.rmtree(os.path.expanduser("~/.npm/_npx"), ignore_errors=True)
    cmd = get_base_npx_cmd(gable_api_endpoint) + args
    return cmd


def get_base_npx_cmd(gable_api_endpoint: Union[str, None]) -> list[str]:
    """Based on the endpoint and GABLE_LOCAL environment variable, decide if we should use the local package
    Returns: list[str] - The base command to run sca, either using npx + @gable-eng/sca or node + local path
    """

    if should_use_docker_node_cmd():
        logger.debug(
            "GABLE_CLI_ISOLATION is true, passing DOCKER_NODE_CMD", DOCKER_NODE_CMD
        )
        return DOCKER_NODE_CMD

    if should_use_local_sca(gable_api_endpoint):
        logger.trace("Configuring local settings")
        try:
            local_sca_path = get_local_sca_path()
            product_dir = os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.dirname(local_sca_path)))  # type: ignore
            )
            tsx_path = os.path.join(
                product_dir, "node_modules", "tsx", "dist", "cli.mjs"
            )
            return [
                tsx_path,
                local_sca_path,
            ]
        except ImportError as e:
            logger.trace(
                f'Error importing local config, trying GABLE_LOCAL_SCA_PATH: {os.environ.get("GABLE_LOCAL_SCA_PATH")}'
            )
            local_sca_path = os.environ.get("GABLE_LOCAL_SCA_PATH")
            product_dir = os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.dirname(local_sca_path)))  # type: ignore
            )
            tsx_path = os.path.join(
                product_dir, "node_modules", "tsx", "dist", "cli.mjs"
            )
            if local_sca_path is not None:
                return [
                    tsx_path,
                    local_sca_path,
                ]

    return BASE_NPX_CMD


def should_use_docker_node_cmd() -> bool:
    return os.environ.get("GABLE_CLI_ISOLATION", "false") == "true"


def should_use_local_sca(gable_api_endpoint: Optional[str]) -> bool:
    """Based on the GABLE_LOCAL environment variable and API endpoint, decide if we should use the local package"""
    gable_local = os.environ.get("GABLE_LOCAL")
    is_endpoint_localhost = (
        gable_api_endpoint is not None
        and gable_api_endpoint.startswith("http://localhost")
    )

    return gable_local != "false" and (gable_local == "true" or is_endpoint_localhost)


def get_installed_package_dir() -> str:
    """Returns the directory of the SCA package in the npx cache. Currently assumes only one version will be installed
    in the npx cache. Throws an exception if the package is not found.
    """
    package_jsons = glob.glob(
        os.path.expanduser("~/.npm/_npx/*/node_modules/@gable-eng/sca/package.json")
    )
    if package_jsons:
        return os.path.dirname(package_jsons[0])

    raise Exception("SCA package not found in npx cache")


def start_sca_prime(
    client: GableAPIClient,
    project_root: str,
    annotations: List[str],
    sca_debug: bool = False,
    semgrep_bin_path: Optional[str] = None,
) -> Union[tuple[subprocess.Popen, str], None]:
    # return process and tempdir if no error, else None
    if os.environ.get("ENABLE_SCA_PRIME", "true").lower() != "true":
        return None

    os.environ["SEMGREP_DEPLOY_CORE_BIN_PATH"] = semgrep_bin_path or ""

    try:
        logger.debug("Running SCA Prime")
        sca_prime_path = _get_sca_prime_path(client.endpoint)

        if not sca_prime_path:
            logger.error("SCA Prime path not found")
            return None

        temp_dir = tempfile.mkdtemp()
        command = [
            sca_prime_path,
            "run",
            "--project-root",
            project_root,
            "--output-type",
            "fs",
            "--output-path",
            temp_dir,
        ]
        if annotations:
            command += ["--annotations"]
            command += annotations
        if sca_debug:
            command += ["--debug"]

        logger.debug("Running sca-prime command: {}", " ".join(command))
        process = subprocess.Popen(
            command,
            env=os.environ,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        def stream_output(pipe, log_method, label):
            with pipe:
                for line in pipe:
                    log_method(f"[{label}] {line.rstrip()}")

        # Start threads for stdout and stderr
        stdout_thread = threading.Thread(
            target=stream_output, args=(process.stdout, logger.trace, "STDOUT")
        )
        stderr_thread = threading.Thread(
            target=stream_output, args=(process.stderr, logger.trace, "STDERR")
        )

        stdout_thread.start()
        stderr_thread.start()

        return (process, temp_dir)
    except Exception as e:
        logger.opt(exception=e).debug(f"Error running SCA Prime: {e}", e)
        return None


def run_sca_npx_help(
    api_endpoint: Union[str, None] = None,
):
    """
    Implicitly checks to see if @gable-eng/sca is installed
    """
    try:
        cmd = get_sca_cmd(
            api_endpoint,
            ["--help"],
        )
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    except Exception as e:
        logger.opt(exception=e).debug("Error running Gable SCA")
        raise click.ClickException(
            "Error running Gable SCA, run again with --debug to see more details"
        )


def get_sca_prime_results(
    sca_prime_process_data: Union[tuple[subprocess.Popen, str], None],
    client: GableAPIClient,
    project_root: str,
    post_metrics=True,
) -> tuple[dict[str, dict[str, Any]], dict]:
    if sca_prime_process_data is None:
        return {}, {}
    sca_prime_process, temp_dir = sca_prime_process_data
    try:
        sca_prime_process.wait()
        if post_metrics:
            metrics_file = os.path.join(temp_dir, "metrics.json")
            if os.path.exists(metrics_file):
                with open(metrics_file, "r") as f:
                    metrics = json.load(f)
                    logger.debug(f"Posting metrics from sca-prime: {metrics}")
                    post_metrics_request = CreateTelemetryRequest(
                        id=None,
                        data=metrics,
                        type=TelemetryType(root="SCA_PRIME"),
                    )
                    post_metrics_response, post_metrics_success = client.post_telemetry(
                        post_metrics_request
                    )
                    if post_metrics_success:
                        logger.debug(
                            f"Posted metrics from sca-prime: {post_metrics_response}"
                        )
                    else:
                        logger.error(
                            f"Error posting metrics from sca-prime: {post_metrics_response}"
                        )
            else:
                logger.error("SCA prime generated metrics file not found")

        findings_file = os.path.join(temp_dir, "findings.json")

        if not os.path.exists(findings_file):
            logger.debug("SCA prime generated findings file not found")
            return {}, {}

        with open(findings_file, "r") as f:
            all_findings = json.load(f)["findings"]

            location_results = {
                f'{finding["recap"]["name"]}': (
                    finding["recap"],
                    finding["source_location"],
                )
                for finding in all_findings
            }

            recap_results = [finding["recap"] for finding in all_findings]
            dict_result = {
                f'{recap_struct["name"]}': recap_struct
                for recap_struct in recap_results
            }

            logger.debug(f"Results from sca-prime: {dict_result}")
            return dict_result, location_results

    except Exception as e:
        logger.opt(exception=e).debug(f"Error running SCA Prime in shadow mode {e}", e)
        return {}, {}
    finally:
        shutil.rmtree(temp_dir)


def _get_sca_prime_path(gable_api_endpoint: Union[str, None]) -> Union[str, None]:
    """Returns the path to SCA prime"""
    architecture = _get_host_architecture_for_sca_prime_binary()
    if should_use_local_sca(gable_api_endpoint):
        local_sca_prime = get_local_sca_prime()
        logger.debug(f"Using local SCA prime: {local_sca_prime}")
        return local_sca_prime
    return os.path.join(
        get_installed_package_dir(),
        "dist",
        "sca-prime",
        f"sca-prime-{architecture}",
        "sca-prime",
    )


def _get_host_architecture_for_sca_prime_binary() -> str:
    """Returns the host architecture for the current system as a valid rust target"""
    result = "x86_64-unknown-linux-gnu"
    if platform.system() == "Darwin":
        result = "aarch64-apple-darwin"
    elif platform.system() == "Linux":
        result = "x86_64-unknown-linux-gnu"
    else:
        logger.error(
            f"Unsupported platform: {platform.system()}, using default: {result}"
        )
    logger.trace(f"Host architecture for sca-prime binary: {result}")
    return result
