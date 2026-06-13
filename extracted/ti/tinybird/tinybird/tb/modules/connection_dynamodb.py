import uuid
from typing import Any, Optional

import click
import requests
from click import Context

from tinybird.tb.client import TinyB
from tinybird.tb.modules.common import (
    DataConnectorType,
    get_connection_name,
    run_aws_iamrole_connection_flow,
    validate_string_connector_param,
)
from tinybird.tb.modules.create import generate_dynamodb_connection_file_with_secret
from tinybird.tb.modules.feedback_manager import FeedbackManager, get_cli_name
from tinybird.tb.modules.project import Project
from tinybird.tb.modules.secret import save_secret_to_local_environment

_DYNAMODB_VALIDATE_REASON_MESSAGES: dict[str, str] = {
    "missing_credentials": (
        "Tinybird could not validate the DynamoDB table because AWS credentials are missing in this environment."
    ),
    "table_not_found": "The DynamoDB table was not found. Check the table ARN and region.",
    "pitr_disabled": "Point-in-Time Recovery (PITR) must be enabled to use the DynamoDB connector.",
    "stream_disabled": "DynamoDB Streams must be enabled to use the DynamoDB connector.",
    "stream_view_invalid": "DynamoDB Streams must use NEW_IMAGE or NEW_AND_OLD_IMAGES.",
    "table_too_large": "The DynamoDB table exceeds the current size limit for this connector.",
    "table_wcu_exceeds_limit": "The DynamoDB table exceeds the current write-capacity limit for this connector.",
    "table_arn_and_region_required": "Both the DynamoDB table ARN and region are required for validation.",
    "role_arn_required": "A role ARN is required to validate the DynamoDB table.",
    "unable_to_assume_role": (
        "Tinybird could not assume the provided IAM role. Check the role ARN and its trust policy."
    ),
    "invalid_json_body": "Tinybird returned an invalid validation request error.",
}


def _extract_reason_from_validation_error(exc: Exception) -> Optional[str]:
    response = getattr(exc, "response", None)
    if response is not None:
        try:
            payload = response.json()
        except Exception:
            pass
        else:
            error = payload.get("error")
            if isinstance(error, dict):
                return error.get("reason")

    error_message = str(exc)
    for reason in _DYNAMODB_VALIDATE_REASON_MESSAGES:
        if reason in error_message:
            return reason
    return None


def _format_dynamodb_validation_message(reason: Optional[str], fallback: str) -> str:
    if reason and reason in _DYNAMODB_VALIDATE_REASON_MESSAGES:
        return _DYNAMODB_VALIDATE_REASON_MESSAGES[reason]
    return fallback


def validate_dynamodb_table(
    client: TinyB,
    table_arn: str,
    region: str,
    role_arn: str,
    *,
    fail_on_error: bool,
    external_id_seed: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    try:
        result = client.validate_dynamodb(
            table_arn=table_arn, region=region, role_arn=role_arn, external_id_seed=external_id_seed
        )
    except requests.HTTPError as exc:
        message = _format_dynamodb_validation_message(_extract_reason_from_validation_error(exc), str(exc))
        if fail_on_error:
            raise click.ClickException(FeedbackManager.error(message=message))
        click.echo(FeedbackManager.warning(message=message))
        return None
    except Exception as exc:
        if fail_on_error:
            raise click.ClickException(FeedbackManager.error(message=str(exc)))
        click.echo(FeedbackManager.warning(message=f"DynamoDB validation failed: {exc}"))
        return None

    click.echo(FeedbackManager.success(message="✓ DynamoDB validation passed"))
    view_type = result.get("stream_view_type")
    if view_type:
        click.echo(FeedbackManager.gray(message=f"  Streams view type: {view_type}"))
    if result.get("table_size_bytes") is not None:
        click.echo(FeedbackManager.gray(message=f"  Table size bytes: {result['table_size_bytes']}"))
    if result.get("table_write_capacity_units") is not None:
        click.echo(
            FeedbackManager.gray(message=f"  Table write capacity units: {result['table_write_capacity_units']}")
        )
    for warning in result.get("messages", []):
        click.echo(FeedbackManager.warning(message=str(warning)))
    return result


def _read_optional_table_arn_for_validation(table_arn: Optional[str]) -> Optional[str]:
    if table_arn is not None:
        return table_arn.strip() or None

    user_input = click.prompt(
        FeedbackManager.highlight(message="? Optional DynamoDB table ARN to validate now (press Enter to skip)"),
        default="",
        show_default=False,
    )
    user_input = user_input.strip()
    return user_input or None


def connection_create_dynamodb(
    ctx: Context,
    connection_name: Optional[str] = None,
    table_arn: Optional[str] = None,
) -> dict[str, Any]:
    obj: dict[str, Any] = ctx.ensure_object(dict)
    project: Project = obj["project"]
    client: TinyB = obj["client"]
    env: str = obj["env"]
    config: dict[str, Any] = obj["config"]

    local_aws_unavailable = False
    if env == "local" and not client.check_aws_credentials():
        click.echo(
            FeedbackManager.warning(
                message=(
                    f"No AWS credentials found. Please run `{get_cli_name()} local restart --use-aws-creds` "
                    "to pass your credentials. Read more about this in "
                    "https://www.tinybird.co/docs/forward/get-data-in/connectors/dynamodb#local-environment"
                )
            )
        )
        click.echo(
            FeedbackManager.warning(
                message=(
                    "Continuing without Tinybird Local. Only Cloud environment will be available for this connection."
                )
            )
        )
        local_aws_unavailable = True

    click.echo(FeedbackManager.gray(message="\n» Creating DynamoDB connection..."))

    if not connection_name:
        connection_name = get_connection_name(project.folder, "DYNAMODB")
    validate_string_connector_param("Connection name", connection_name)

    role_arn, region, cloud_client, local_client = run_aws_iamrole_connection_flow(
        config=config,
        client=client,
        service=DataConnectorType.AMAZON_DYNAMODB,
        connection_name=connection_name,
        policy="read",
        local_unavailable=local_aws_unavailable,
    )

    unique_suffix = uuid.uuid4().hex[:8]
    secret_name = f"dynamodb_role_arn_{connection_name}_{unique_suffix}"
    secret_created_local = False
    secret_created_cloud = False
    errors: list[str] = []

    if local_client:
        try:
            save_secret_to_local_environment(project=project, name=secret_name, value=role_arn, client=local_client)
            secret_created_local = True
        except Exception as exc:
            errors.append(f"Failed to create secret in local: {exc}")
            click.echo(FeedbackManager.warning(message=f"Failed to create secret in local: {exc}"))

    if cloud_client:
        try:
            cloud_client.create_secret(name=secret_name, value=role_arn)
            secret_created_cloud = True
        except Exception as exc:
            errors.append(f"Failed to create secret in cloud: {exc}")
            click.echo(FeedbackManager.warning(message=f"Failed to create secret in cloud: {exc}"))

    connection_file_path = generate_dynamodb_connection_file_with_secret(
        name=connection_name,
        role_arn_secret_name=secret_name,
        region=region,
        folder=project.folder,
    )

    validate_table_arn = _read_optional_table_arn_for_validation(table_arn)
    if validate_table_arn:
        click.echo(FeedbackManager.gray(message="\n» Validating DynamoDB table..."))
        validate_dynamodb_table(
            client,
            validate_table_arn,
            region,
            role_arn,
            fail_on_error=False,
            external_id_seed=connection_name,
        )

    items = [f"- File created at: {connection_file_path}"]
    if secret_created_local and secret_created_cloud:
        items.append(f"- Secret created in Local and Cloud for role ARN with name {secret_name}")
    elif secret_created_local:
        items.append(f"- Secret created in Local for role ARN with name {secret_name}")
    elif secret_created_cloud:
        items.append(f"- Secret created in Cloud for role ARN with name {secret_name}")

    if errors:
        click.echo(
            FeedbackManager.error(
                message=(
                    f"DynamoDB connection '{connection_name}' could not be created. "
                    f"Review the configuration at: {connection_file_path}"
                )
            )
        )
        for error in errors:
            click.echo(FeedbackManager.error(message=f"  - {error}"))
        return {"name": connection_name, "error": "; ".join(errors)}

    click.echo(
        FeedbackManager.success(
            message=f"DynamoDB connection '{connection_name}' created successfully!\n" + "\n".join(items)
        )
    )
    click.echo(
        FeedbackManager.gray(
            message=(
                f"Next steps:\n- Use this connection in your Data Sources with: "
                f"IMPORT_CONNECTION_NAME '{connection_name}'\n"
                "- Learn more about our DynamoDB Connector: "
                "https://www.tinybird.co/docs/forward/get-data-in/connectors/dynamodb"
            )
        )
    )
    return {"name": connection_name, "error": None}
