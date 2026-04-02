import os.path
from pathlib import Path

import toml
import typer
from rich.console import Console
from rich.table import Table

from seshat.general.command import (
    SubmitCommand,
    JobMetadata,
    JobExecutionSchedule,
    ExecutionMode,
)
from seshat.general.command.code_inspect import CodeInspectCommand
from seshat.general.command.job_status import JobStatusCommand
from seshat.general.command.setup_project import RECOMMENDATION, SetUpProjectCommand
from seshat.general.exceptions import NoConfigSetError, RestClientException

app = typer.Typer()
console = Console()
DEFAULT_DATA_SIZE = 1_000_000  # 1 GB
DEFAULT_EXPIRATION = 86400

state = {"verbose": False}


def load_config(config_file: Path = Path.home() / ".codemanager.toml") -> dict:
    try:
        if config_file.exists():
            return toml.load(config_file)
        else:
            raise NoConfigSetError("Config file not found.")
    except toml.TomlDecodeError:
        raise NoConfigSetError("Config file is malformed.")


@app.command(name="create-project")
def create_project(name: str, usecase=typer.Option(default=RECOMMENDATION)):
    command = SetUpProjectCommand(name, usecase, os.getcwd(), report=state["verbose"])
    try:
        command.handle()
    except Exception as exc:
        cli_msg = typer.style(
            f"Setup project in usecase {usecase} failed because of {str(exc)}",
            fg=typer.colors.RED,
            bold=True,
        )
    else:
        cli_msg = typer.style(
            f"""
            Setup project in usecase {usecase} done!\n
            You can deploy your project by this command 🚀:
            'python -m seshat deploy`
            """,
            fg=typer.colors.GREEN,
            bold=True,
        )
    typer.echo(cli_msg)


@app.command(name="inspect")
def inspect_code(
    directory: str = typer.Argument(..., help="Directory containing the code"),
    config_file: Path = typer.Option(
        Path.home() / ".codemanager.toml", help="Path to config file"
    ),
):
    try:
        config = load_config(config_file)
        if not config:
            raise NoConfigSetError()

        manager = CodeInspectCommand(config)
        complexity = manager.handle(directory)
        config["code"] = {**config.get("code", {}), "complexity_factor": complexity}

        with open(config_file, "w") as f:
            toml.dump(config, f)

        typer.echo(f"Configuration updated in {config_file}")
    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(1)


def _execute_job_submission(
    directory: str,
    name: str,
    version: str,
    config: dict,
    confidential_level: str,
    execution_mode: str,
    executor_image_tag: str = None,
    operation_type: str = "submit",
) -> None:
    """
    Common logic for submitting and publishing jobs.

    Args:
        directory: Directory containing the code
        name: Name of the package
        version: Version of the package
        config: Configuration dictionary
        confidential_level: Confidential level for the pipeline
        execution_mode: Execution mode for the pipeline
        executor_image_tag: Image tag of the executor (optional, only for submit)
        operation_type: Type of operation ("submit" or "publish")
    """
    manager = SubmitCommand(config)

    job_execution_schedule = None
    if "execution" in config:
        job_execution_schedule = JobExecutionSchedule(
            **config.get("execution", {}).get("plan", {})
        )

    job_metadata = JobMetadata(
        pipeline_hash="",
        confidential_level=confidential_level,
        execution_mode=ExecutionMode(execution_mode),
        execution_plan=job_execution_schedule,
        main_file_path=config.get("code", {}).get("main_file", "main.py"),
        env_file_path=config.get("code", {}).get("env_file", ".env"),
        data_size=config.get("code", {}).get("data_size", DEFAULT_DATA_SIZE),
        code_size=0 if operation_type == "publish" else None,  # Only for publish
        complexity_factor=config.get("code", {}).get("complexity_factor", 0),
        requirement_file=None,
        requirements_type=None,
        secret_key=None,
        iv=None,
    )

    # Handle package creation
    if operation_type == "submit":
        package = manager.handle(
            directory,
            name,
            version,
            executor_image_tag=executor_image_tag,
            metadata=job_metadata,
        )
    else:
        package = manager.handle(directory, name, version, metadata=job_metadata)

    # Handle code obfuscation
    obfuscate_code = config.get("code", {}).get("obfuscate_code", "false")
    obfuscate_code = obfuscate_code.lower() == "true"
    if obfuscate_code:
        package = manager.obfuscate_code(package)

    job_metadata.pipeline_hash = package.hash
    identifier = manager.store_code(package)

    if operation_type == "submit":
        job_response = manager.submit_job(
            identifier,
            name,
            version,
            job_metadata,
            executor_image_tag=executor_image_tag,
            expiration=config.get("aws", {}).get("expiration", DEFAULT_EXPIRATION),
        )
    else:
        job_response = manager.publish_job(
            identifier,
            name,
            version,
            job_metadata,
            expiration=config.get("aws", {}).get("expiration", DEFAULT_EXPIRATION),
        )

    _display_job_summary(
        package, identifier, job_response, include_executor=bool(executor_image_tag)
    )


def _display_job_summary(
    package, identifier: str, job_response: dict, include_executor: bool = False
) -> None:
    """Display job submission summary in a formatted table."""
    job_response_data = job_response.get("data", {})

    table = Table(title="Upload Summary")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Name", package.name)
    table.add_row("Version", package.version)
    if include_executor:
        table.add_row("ExecutorImageTag", package.executor_image_tag)
    table.add_row("Hash", package.hash)
    table.add_row("S3 Location", identifier)
    table.add_row("Job ID", str(job_response_data.get("id", "N/A")))
    table.add_row("Status", job_response_data.get("status", {}).get("state", "N/A"))

    console.print(table)


@app.command(name="submit")
def submit_job(
    directory: str = typer.Argument(..., help="Directory containing the code"),
    name: str = typer.Option(..., help="Name of the package"),
    version: str = typer.Option(..., help="Version of the package"),
    executor_image_tag: str = typer.Option(
        "latest", help="Image tag of the executor which runs the job"
    ),
    confidential_level: str = typer.Option(
        "default", help="Confidential level desired for the pipeline"
    ),
    execution_mode: str = typer.Option(
        "single", help="Execution mode for the pipeline"
    ),
    config_file: Path = typer.Option(
        Path.home() / ".codemanager.toml", help="Path to config file"
    ),
):
    """Submit a job with executor image tag."""
    try:
        config = load_config(config_file)
        if not config:
            raise NoConfigSetError()

        _execute_job_submission(
            directory=directory,
            name=name,
            version=version,
            config=config,
            confidential_level=confidential_level,
            execution_mode=execution_mode,
            executor_image_tag=executor_image_tag,
            operation_type="submit",
        )

    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(1)


@app.command(name="publish")
def publish_job_on_cook(
    directory: str = typer.Argument(..., help="Directory containing the code"),
    name: str = typer.Option(..., help="Name of the package"),
    version: str = typer.Option(..., help="Version of the package"),
    confidential_level: str = typer.Option(
        "default", help="Confidential level desired for the pipeline"
    ),
    execution_mode: str = typer.Option(
        "single", help="Execution mode for the pipeline"
    ),
    config_file: Path = typer.Option(
        Path.home() / ".codemanager.toml", help="Path to config file"
    ),
):
    """Publish a job on cook without executor image tag."""
    try:
        config = load_config(config_file)
        if not config:
            raise NoConfigSetError()

        _execute_job_submission(
            directory=directory,
            name=name,
            version=version,
            config=config,
            confidential_level=confidential_level,
            execution_mode=execution_mode,
            executor_image_tag=None,
            operation_type="publish",
        )

    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(1)


@app.command(name="configure")
def configure_job(
    bucket: str = typer.Option(..., prompt=True, help="S3 bucket name"),
    prefix: str = typer.Option("code", prompt=True, help="S3 prefix"),
    aws_access_key_id: str = typer.Option(..., prompt=True, help="AWS access key ID"),
    aws_secret_access_key: str = typer.Option(
        ..., prompt=True, hide_input=True, help="AWS secret access key"
    ),
    aws_region: str = typer.Option("us-east-1", prompt=True, help="AWS region"),
    api_base_url: str = typer.Option(
        ..., prompt=True, show_default=True, help="API base URL"
    ),
    api_auth_token: str = typer.Option(
        ...,
        prompt=True,
        hide_input=True,
        prompt_required=True,
        help="API authentication token",
    ),
    main_file_path: str = typer.Option(
        ...,
        prompt=True,
        hide_input=False,
        prompt_required=True,
        help="Path to main file",
    ),
    env_file_path: str = typer.Option(
        ".env",
        prompt=True,
        hide_input=False,
        prompt_required=True,
        help="Path to main file",
    ),
    ignore_file: str = typer.Option(
        ".jobignore",
        prompt=True,
        help="Path to file containing ignore patterns for job files",
    ),
    schedule_mode: str = typer.Option(
        "once", prompt=True, help="Execution schedule mode (e.g. single, recurring)"
    ),
    start_time: str = typer.Option(
        "", prompt=True, help="Start time (YYYY-MM-DDTHH:MM)"
    ),
    until: str = typer.Option("", prompt=True, help="Until time (YYYY-MM-DDTHH:MM)"),
    interval: int = typer.Option("", prompt=True, help="Interval for scheduling jobs"),
    cron_expression: str = typer.Option(
        "",
        prompt=True,
        help="Cron expression for schedule (keep empty if interval is provided)",
    ),
    run_overlap: str = typer.Option(
        "true", prompt=True, help="Allow overlapping runs (true/false)"
    ),
    data_size: float = typer.Option(
        DEFAULT_DATA_SIZE,
        prompt=True,
        help="Estimate of size of data you want processed",
    ),
    complexity_factor: float = typer.Option(
        None,
        prompt=True,
        help="Estimate of process complexity (between 1 to 1000, higher takes more time and is more expensive)",
    ),
    config_file: Path = typer.Option(
        Path.home() / ".codemanager.toml", help="Path to config file"
    ),
):
    config = {
        "aws": {
            "bucket": bucket,
            "prefix": prefix,
            "access_key_id": aws_access_key_id,
            "secret_access_key": aws_secret_access_key,
            "region": aws_region,
        },
        "api": {
            "base_url": api_base_url,
            "auth_token": api_auth_token,
        },
        "code": {
            "main_file": main_file_path,
            "ignore_file": ignore_file,
            "env_file": env_file_path,
            "data_size": data_size,
            "complexity_factor": complexity_factor,
        },
        "execution": {
            "plan": {
                "schedule_mode": schedule_mode,
                "start_time": start_time,
                "until": until,
                "cron_expression": cron_expression,
                "interval": interval,
                "run_overlap": run_overlap,
            }
        },
    }

    config_file.parent.mkdir(parents=True, exist_ok=True)
    with open(config_file, "w") as f:
        toml.dump(config, f)

    typer.echo(f"Configuration saved to {config_file}")


@app.command(name="job-status")
def job_status(
    job_id: str = typer.Argument(..., help="The job ID to check"),
    config_file: Path = typer.Option(
        Path.home() / ".codemanager.toml", help="Path to config file"
    ),
    api_base_url: str = typer.Option(None, help="API base URL"),
    api_auth_token: str = typer.Option(
        None,
        help="API authentication token",
    ),
):
    """Check the status of a submitted job"""
    try:
        try:
            config = load_config(config_file)
        except NoConfigSetError():
            config = None

        if not config and not (api_base_url and api_auth_token):
            raise NoConfigSetError()
        else:
            base_url = api_base_url or config.get("api", {}).get("base_url")
            auth_token = api_auth_token or config.get("api", {}).get("auth_token")

        if not base_url:
            typer.echo("base_url is not set")
            raise NoConfigSetError(
                "base_url parameter must be set in the config file or as command option"
            )
        if not auth_token:
            typer.echo("auth_token is not set")
            raise NoConfigSetError(
                "auth_token parameter must be set in the config file or as command option"
            )

        manager = JobStatusCommand(base_url=base_url, auth_token=auth_token)
        manager.job_status(job_id)

    except NoConfigSetError as e:
        typer.echo(f"Configuration error: {e}")
        raise typer.Exit(2)
    except RestClientException as e:
        typer.echo(f"API error: {e}")
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Unexpected error: {e}")
        raise typer.Exit(1)


@app.callback()
def main(verbose: bool = False):
    state["verbose"] = verbose
