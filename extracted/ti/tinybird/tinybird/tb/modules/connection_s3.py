# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

import uuid
from typing import Any, Dict, Optional

import click
from click import Context

from tinybird.tb.client import TinyB
from tinybird.tb.modules.common import (
    DataConnectorType,
    echo_safe_humanfriendly_tables_format_pretty_table,
    get_s3_connection_name,
    run_aws_iamrole_connection_flow,
)
from tinybird.tb.modules.create import generate_aws_iamrole_connection_file_with_secret
from tinybird.tb.modules.exceptions import CLIConnectionException
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.project import Project
from tinybird.tb.modules.secret import save_secret_to_env_file


def select_bucket_uri(bucket_uri: Optional[str]) -> str:
    """Prompt user to enter an S3 bucket URI if not provided."""
    if bucket_uri:
        return bucket_uri

    bucket_uri = click.prompt(
        FeedbackManager.highlight(message="? Enter the S3 bucket URI (e.g., s3://my-bucket/*.csv)"),
        default="",
        show_default=False,
    )

    if not bucket_uri:
        raise CLIConnectionException(FeedbackManager.error(message="Bucket URI is required."))

    return bucket_uri


def select_schedule(schedule: Optional[str]) -> str:
    """Prompt user to select an import schedule if not provided.

    Args:
        schedule: Optional schedule value (@auto or @once)

    Returns:
        The selected schedule value
    """
    if schedule:
        return schedule

    click.echo(FeedbackManager.highlight(message="? Select import schedule:"))
    click.echo("  [1] @auto - Automatically ingest new files")
    click.echo("  [2] @once - Only ingest on-demand (manual sync)")

    choice = click.prompt("\nSelect option", default=1, type=int)

    if choice == 1:
        return "@auto"
    elif choice == 2:
        return "@once"
    else:
        click.echo(FeedbackManager.warning(message="Invalid option. Defaulting to @auto."))
        return "@auto"


def format_file_size(size: int) -> str:
    """Format file size in human-readable format."""
    if size >= 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024 * 1024):.2f} GB"
    elif size >= 1024 * 1024:
        return f"{size / (1024 * 1024):.2f} MB"
    elif size >= 1024:
        return f"{size / 1024:.2f} KB"
    else:
        return f"{size} B"


def select_sample_file_uri(
    sample_file_uri: Optional[str],
    bucket_uri: str,
    connection_id: str,
    client: TinyB,
) -> str:
    """Select or prompt for a sample file URI from the S3 bucket.

    If sample_file_uri is provided, validates it exists in the bucket.
    Otherwise, lists files from the bucket and lets the user select one.
    """
    if sample_file_uri:
        # Validate the provided sample file exists
        click.echo(FeedbackManager.gray(message="» Fetching files from bucket..."))
        response = client.preview_bucket(connection_id, bucket_uri)
        files = response.get("files", [])
        file_names = [f.get("name", "") for f in files]

        if sample_file_uri not in file_names:
            raise CLIConnectionException(
                FeedbackManager.error(
                    message=f"Sample file '{sample_file_uri}' not found in bucket. Files available: {', '.join(file_names[:5])}{'...' if len(file_names) > 5 else ''}"
                )
            )
        return sample_file_uri

    # List files and let user select
    click.echo(FeedbackManager.gray(message="» Fetching files from bucket..."))
    response = client.preview_bucket(connection_id, bucket_uri)
    files = response.get("files", [])

    if not files:
        raise CLIConnectionException(
            FeedbackManager.error(message=f"No files found matching the bucket URI: {bucket_uri}")
        )

    max_files_to_show = 9
    files_to_display = files[:max_files_to_show]
    remaining_files = len(files) - max_files_to_show

    click.echo(FeedbackManager.highlight(message="? Select a sample file:"))
    file_index = -1
    while file_index == -1:
        for index, file_info in enumerate(files_to_display):
            name = file_info.get("name", "")
            size = file_info.get("size", 0)
            size_str = format_file_size(size)
            click.echo(f"  [{index + 1}] {name} ({size_str})")
        if remaining_files > 0:
            click.echo(FeedbackManager.gray(message=f"  ... and {remaining_files} more file(s)"))
        file_index = click.prompt("\nSelect file (or enter a file path directly)", default=1)
        try:
            # Try to parse as index first
            idx = int(file_index) - 1
            if 0 <= idx < len(files_to_display):
                selected_file = files_to_display[idx]
                sample_file_uri = selected_file.get("name", "")
            else:
                file_index = -1
        except ValueError:
            # User entered a file path directly
            sample_file_uri = str(file_index)
            file_index = 0  # Exit the loop

    if not sample_file_uri:
        raise CLIConnectionException(FeedbackManager.error(message="Sample file is required."))

    return sample_file_uri


def preview_to_table(data: list[dict[str, Any]], meta: list[dict[str, Any]]) -> tuple[list[list[Any]], list[str]]:
    column_names = [col["name"] for col in meta]
    # Convert each row dictionary to a list of values ordered by column names
    data_as_lists = []
    for row in data:
        if isinstance(row, dict):
            # Convert dict to list of values in column order
            row_values = [row.get(col_name, "") for col_name in column_names]
            data_as_lists.append(row_values)
        else:
            # If it's already a list, keep it as is
            data_as_lists.append(row)

    return data_as_lists, column_names


def echo_s3_data(
    connection_id: str,
    connection_name: str,
    bucket_uri: str,
    sample_file_uri: str,
    client: TinyB,
    from_time: Optional[str] = None,
) -> dict[str, Any]:
    """Preview data from an S3 bucket and display it in a table.

    Args:
        connection_id: The S3 connection ID
        connection_name: The S3 connection name (for display purposes)
        bucket_uri: The S3 bucket URI to preview (e.g., s3://my-bucket/*.csv)
        client: The TinyB client

    Returns:
        A dictionary with the preview data including 'files' list
    """
    click.echo(FeedbackManager.highlight(message="» Previewing S3 connection..."))
    response = client.preview_s3(connection_id, bucket_uri, sample_file_uri, from_time)
    preview = response.get("preview", {})
    data = preview.get("data", [])
    meta = preview.get("meta", [])
    data_as_lists, column_names = preview_to_table(data, meta)

    if not data_as_lists and not column_names:
        click.echo(FeedbackManager.warning(message="No data to preview."))
    else:
        echo_safe_humanfriendly_tables_format_pretty_table(data_as_lists, column_names)

    return {
        "data": data,
        "meta": meta,
    }


def get_format_from_uri(uri: str) -> str:
    """Determine the file format from a URI or file path.

    Args:
        uri: The S3 bucket URI or sample file path

    Returns:
        The format: 'csv', 'ndjson', or 'parquet'
    """
    uri_lower = uri.lower()
    # Handle .gz compression
    uri_lower = uri_lower.removesuffix(".gz")

    if uri_lower.endswith(".csv"):
        return "csv"
    elif uri_lower.endswith((".ndjson", ".jsonl", ".json")):
        return "ndjson"
    elif uri_lower.endswith(".parquet"):
        return "parquet"
    else:
        # Default to ndjson for unknown formats
        return "ndjson"


def meta_to_schema(meta: list[dict[str, Any]], file_format: str) -> str:
    """Convert meta columns to schema format.

    Args:
        meta: Column metadata from the preview
        file_format: The file format ('csv', 'ndjson', 'parquet')

    Returns:
        The schema string
    """
    if file_format == "csv":
        # CSV files don't use JSONPath
        return ",\n    ".join([f"`{col['name']}` {col['type']}" for col in meta])
    else:
        # NDJSON and Parquet use JSONPath
        return ",\n    ".join([f"`{col['name']}` {col['type']} `json:$.{col['name']}`" for col in meta])


def meta_to_s3_datasource_datafile(
    meta: list[dict[str, Any]],
    connection_name: str,
    bucket_uri: str,
    import_schedule: str = "@auto",
) -> str:
    """Generate S3 datasource datafile content from preview metadata.

    Args:
        meta: Column metadata from the preview
        connection_name: The S3 connection name
        bucket_uri: The S3 bucket URI
        import_schedule: The import schedule (default: @auto)

    Returns:
        The datasource datafile content as a string
    """
    file_format = get_format_from_uri(bucket_uri)
    schema: str = meta_to_schema(meta, file_format)
    ds_content = f"""SCHEMA >
    {schema}

ENGINE "MergeTree"
# ENGINE_SORTING_KEY "user_id, timestamp"
# ENGINE_TTL "timestamp + toIntervalDay(60)"
# Learn more at https://www.tinybird.co/docs/forward/dev-reference/datafiles/datasource-files
IMPORT_CONNECTION_NAME {connection_name}
IMPORT_BUCKET_URI "{bucket_uri}"
IMPORT_SCHEDULE "{import_schedule}"
# Learn more at https://www.tinybird.co/docs/forward/get-data-in/connectors/s3#datasource-settings
"""
    return ds_content


def connection_create_s3(
    ctx: Context,
    connection_name: Optional[str] = None,
    access_type: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create an S3 connection with full IAM role setup workflow.
    Can be called from both the CLI command and the datasource wizard.

    Args:
        ctx: Click context
        connection_name: Optional connection name. If not provided, will prompt user.
        access_type: Optional access type ("read" or "write"). If not provided, will prompt user.

    Returns:
        Dict with 'name' and 'error' keys
    """
    obj: dict[str, Any] = ctx.ensure_object(dict)
    project: Project = obj["project"]
    client: TinyB = obj["client"]
    env: str = obj["env"]
    config: dict[str, Any] = obj["config"]

    # Track if local environment is unavailable due to missing AWS credentials
    local_aws_unavailable = False
    if env == "local" and not client.check_aws_credentials():
        click.echo(
            FeedbackManager.warning(
                message="No AWS credentials found. Please run `tb local restart --use-aws-creds` to pass your credentials. "
                "Read more about this in https://www.tinybird.co/docs/forward/get-data-in/connectors/s3#local-environment"
            )
        )
        click.echo(
            FeedbackManager.warning(
                message="Continuing without Tinybird Local. Only Cloud environment will be available for this connection."
            )
        )
        local_aws_unavailable = True

    service = DataConnectorType.AMAZON_S3

    click.echo(FeedbackManager.gray(message="\n» Creating S3 connection..."))

    # Ask for connection name first
    connection_name = get_s3_connection_name(project.folder, connection_name)

    # Ask user for access type if not provided
    if not access_type:
        click.echo(FeedbackManager.highlight(message="? What type of access do you need for this S3 connection?"))
        click.echo('  [1] "read" for S3 Data Source (reading from S3)')
        click.echo('  [2] "write" for S3 Sink (writing to S3)')

        choice = click.prompt("\nSelect option", default=1, type=int)

        if choice == 1:
            access_type = "read"
        elif choice == 2:
            access_type = "write"
        else:
            click.echo(FeedbackManager.warning(message="Invalid option. Defaulting to 'read'."))
            access_type = "read"

    # Prepare clients based on current environment

    role_arn, region, cloud_client, local_client = run_aws_iamrole_connection_flow(
        config=config,
        client=client,
        service=service,
        connection_name=connection_name,
        policy=access_type.lower(),
        local_unavailable=local_aws_unavailable,
    )
    unique_suffix = uuid.uuid4().hex[:8]  # Use first 8 chars of a UUID for brevity
    secret_name = f"s3_role_arn_{connection_name}_{unique_suffix}"

    # Track which secrets were successfully created and any errors
    secret_created_local = False
    secret_created_cloud = False
    errors: list[str] = []

    # Create secrets only in selected environments
    if local_client:
        try:
            save_secret_to_env_file(project=project, name=secret_name, value=role_arn)
            secret_created_local = True
        except Exception as e:
            errors.append(f"Failed to create secret in local: {e}")
            click.echo(FeedbackManager.warning(message=f"Failed to create secret in local: {e}"))

    if cloud_client:
        try:
            cloud_client.create_secret(name=secret_name, value=role_arn)
            secret_created_cloud = True
        except Exception as e:
            errors.append(f"Failed to create secret in cloud: {e}")
            click.echo(FeedbackManager.warning(message=f"Failed to create secret in cloud: {e}"))

    connection_file_path = generate_aws_iamrole_connection_file_with_secret(
        name=connection_name,
        service=service,
        role_arn_secret_name=secret_name,
        region=region,
        folder=project.folder,
    )

    # Build success message items list
    items = [f"- File created at: {connection_file_path}"]

    # Build secret created message based on environments
    if secret_created_local and secret_created_cloud:
        items.append(f"- Secret created in Local and Cloud for role ARN with name {secret_name}")
    elif secret_created_local:
        items.append(f"- Secret created in Local for role ARN with name {secret_name}")
    elif secret_created_cloud:
        items.append(f"- Secret created in Cloud for role ARN with name {secret_name}")

    items_text = "\n".join(items)

    # Show warning if there were errors but file was still generated
    if errors:
        click.echo(
            FeedbackManager.warning(
                message=f"S3 connection file generated with warnings. Please review the configuration at: {connection_file_path}"
            )
        )
        click.echo(FeedbackManager.warning(message="The following issues occurred:"))
        for error in errors:
            click.echo(FeedbackManager.warning(message=f"  - {error}"))
        click.echo("")

    if access_type.lower() == "write":
        click.echo(
            FeedbackManager.prompt_s3_iamrole_success_write(
                connection_name=connection_name,
                connection_path=str(connection_file_path),
                items=items_text,
            )
        )
        tip_message = """Next steps:
- Use this connection in your Data Sources with: EXPORT_CONNECTION_NAME '{connection_name}'
- Learn more about our S3 Sinks: https://www.tinybird.co/docs/forward/work-with-data/publish-data/s3-sinks""".format(
            connection_name=connection_name
        )
    else:
        click.echo(
            FeedbackManager.prompt_s3_iamrole_success_read(
                connection_name=connection_name,
                connection_path=str(connection_file_path),
                items=items_text,
            )
        )
        tip_message = """Next steps:
- Use this connection in your Data Sources with: IMPORT_CONNECTION_NAME '{connection_name}'
- Learn more about our S3 Connector: https://www.tinybird.co/docs/forward/get-data-in/connectors/s3""".format(
            connection_name=connection_name
        )
    click.echo(FeedbackManager.gray(message=tip_message))

    return {
        "name": connection_name,
        "error": None,
    }
