# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

import uuid
from typing import Any, Dict, List, Optional, Tuple

import click
from click import Context
from confluent_kafka.admin import AdminClient

from tinybird.tb.client import TinyB
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.common import (
    DataConnectorType,
    _get_setting_value,
    echo_safe_humanfriendly_tables_format_smart_table,
    get_gcs_connection_name,
    get_gcs_svc_account_creds,
    get_kafka_connection_name,
    get_s3_connection_name,
    production_aws_iamrole_only,
    run_aws_iamrole_connection_flow,
    run_gcp_svc_account_connection_flow,
    validate_kafka_auto_offset_reset,
    validate_kafka_bootstrap_servers,
    validate_kafka_key,
    validate_kafka_schema_registry_url,
    validate_kafka_secret,
)
from tinybird.tb.modules.create import (
    generate_aws_iamrole_connection_file_with_secret,
    generate_gcs_connection_file_with_secrets,
    generate_kafka_connection_with_secrets,
)
from tinybird.tb.modules.exceptions import CLIConnectionException
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.project import Project
from tinybird.tb.modules.secret import save_secret_to_env_file

DATA_CONNECTOR_SETTINGS: Dict[DataConnectorType, List[str]] = {
    DataConnectorType.KAFKA: [
        "kafka_bootstrap_servers",
        "kafka_sasl_plain_username",
        "kafka_sasl_plain_password",
        "cli_version",
        "endpoint",
        "kafka_security_protocol",
        "kafka_sasl_mechanism",
        "kafka_schema_registry_url",
        "kafka_ssl_ca_pem",
    ],
    DataConnectorType.GCLOUD_SCHEDULER: ["gcscheduler_region"],
    DataConnectorType.SNOWFLAKE: [
        "account",
        "username",
        "password",
        "role",
        "warehouse",
        "warehouse_size",
        "stage",
        "integration",
    ],
    DataConnectorType.BIGQUERY: ["account"],
    DataConnectorType.GCLOUD_STORAGE: [
        "gcs_private_key_id",
        "gcs_client_x509_cert_url",
        "gcs_project_id",
        "gcs_client_id",
        "gcs_client_email",
        "gcs_private_key",
    ],
    DataConnectorType.GCLOUD_STORAGE_HMAC: [
        "gcs_hmac_access_id",
        "gcs_hmac_secret",
    ],
    DataConnectorType.GCLOUD_STORAGE_SA: ["account_email"],
    DataConnectorType.AMAZON_S3: [
        "s3_access_key_id",
        "s3_secret_access_key",
        "s3_region",
    ],
    DataConnectorType.AMAZON_S3_IAMROLE: [
        "s3_iamrole_arn",
        "s3_iamrole_region",
        "s3_iamrole_external_id",
    ],
    DataConnectorType.AMAZON_DYNAMODB: [
        "dynamodb_iamrole_arn",
        "dynamodb_iamrole_region",
        "dynamodb_iamrole_external_id",
    ],
}

SENSITIVE_CONNECTOR_SETTINGS = {
    DataConnectorType.KAFKA: ["kafka_sasl_plain_password"],
    DataConnectorType.GCLOUD_SCHEDULER: [
        "gcscheduler_target_url",
        "gcscheduler_job_name",
        "gcscheduler_region",
    ],
    DataConnectorType.GCLOUD_STORAGE_HMAC: ["gcs_hmac_secret"],
    DataConnectorType.AMAZON_S3: ["s3_secret_access_key", "s3_secret"],
    DataConnectorType.AMAZON_S3_IAMROLE: ["s3_iamrole_arn"],
    DataConnectorType.AMAZON_DYNAMODB: ["dynamodb_iamrole_arn"],
}


@cli.group()
@click.pass_context
def connection(ctx: Context) -> None:
    """Connection commands."""


@connection.command(name="ls")
@click.option("--service", help="Filter by service")
@click.pass_context
def connection_ls(ctx: Context, service: Optional[DataConnectorType] = None) -> None:
    """List connections."""
    obj: Dict[str, Any] = ctx.ensure_object(dict)
    client: TinyB = obj["client"]

    connections = client.connections(connector=service)
    columns = []
    table = []

    click.echo(FeedbackManager.info_connections())

    if not service:
        sensitive_settings = []
        columns = ["service", "name", "id", "connected_datasources"]
    else:
        sensitive_settings = SENSITIVE_CONNECTOR_SETTINGS.get(service, [])
        columns = ["service", "name", "id", "connected_datasources"]
        if connector_settings := DATA_CONNECTOR_SETTINGS.get(service):
            columns += connector_settings

    for connection in connections:
        row = [_get_setting_value(connection, setting, sensitive_settings) for setting in columns]
        table.append(row)

    column_names = [c.replace("kafka_", "") for c in columns]
    echo_safe_humanfriendly_tables_format_smart_table(table, column_names=column_names)
    click.echo("\n")


@connection.group(name="create")
@click.pass_context
def connection_create(ctx: Context) -> None:
    """Create a connection."""


@connection_create.command(name="s3", short_help="Creates a AWS S3 connection.")
@click.pass_context
def connection_create_s3(ctx: Context) -> None:
    """
    Creates a AWS S3 connection.

    \b
    $ tb connection create s3
    """
    project: Project = ctx.ensure_object(dict)["project"]
    obj: Dict[str, Any] = ctx.ensure_object(dict)
    client: TinyB = obj["client"]

    if obj["env"] == "local" and not client.check_aws_credentials():
        click.echo(
            FeedbackManager.error(
                message="No AWS credentials found. Please run `tb local restart --use-aws-creds` to pass your credentials. "
                "Read more about this in https://www.tinybird.co/docs/forward/get-data-in/connectors/s3#local-environment"
            )
        )
        return

    service = DataConnectorType.AMAZON_S3
    click.echo(FeedbackManager.prompt_s3_connection_header())

    # Ask user for access type
    access_type = click.prompt(
        FeedbackManager.highlight(
            message="What type of access do you need for this S3 connection?\n"
            '  - "read" for S3 Data Source (reading from S3)\n'
            '  - "write" for S3 Sink (writing to S3)\n'
            "Access type",
        ),
        type=click.Choice(["read", "write"], case_sensitive=False),
        default="read",
        show_choices=True,
        show_default=True,
    )

    connection_name = get_s3_connection_name(project.folder)
    role_arn, region, bucket_name = run_aws_iamrole_connection_flow(
        client,
        service=service,
        environment=obj["env"],
        connection_name=connection_name,
        policy=access_type.lower(),
    )
    unique_suffix = uuid.uuid4().hex[:8]  # Use first 8 chars of a UUID for brevity
    secret_name = f"s3_role_arn_{connection_name}_{unique_suffix}"
    if obj["env"] == "local":
        save_secret_to_env_file(project=project, name=secret_name, value=role_arn)
    else:
        client.create_secret(name=secret_name, value=role_arn)

    create_in_cloud = (
        click.confirm(FeedbackManager.prompt_connection_in_cloud_confirmation(), default=True)
        if obj["env"] == "local"
        else False
    )

    if create_in_cloud:
        prod_config = obj["config"]
        host = prod_config["host"]
        token = prod_config["token"]
        prod_client = TinyB(
            token=token,
            host=host,
            staging=False,
        )
        prod_role_arn, _, _ = production_aws_iamrole_only(
            prod_client,
            service=service,
            region=region,
            bucket_name=bucket_name,
            environment="cloud",
            connection_name=connection_name,
            policy=access_type.lower(),
        )
        prod_client.create_secret(name=secret_name, value=prod_role_arn)

    connection_file_path = generate_aws_iamrole_connection_file_with_secret(
        name=connection_name,
        service=service,
        role_arn_secret_name=secret_name,
        region=region,
        folder=project.folder,
    )

    if access_type.lower() == "write":
        click.echo(
            FeedbackManager.prompt_s3_iamrole_success_write(
                connection_name=connection_name,
                connection_path=str(connection_file_path),
            )
        )
    else:
        click.echo(
            FeedbackManager.prompt_s3_iamrole_success_read(
                connection_name=connection_name,
                connection_path=str(connection_file_path),
            )
        )


@connection_create.command(name="gcs", short_help="Creates a Google Cloud Storage connection.")
@click.pass_context
def connection_create_gcs(ctx: Context) -> None:
    """
    Creates a Google Cloud Storage connection.

    \b
    $ tb connection create gcs
    """
    project: Project = ctx.ensure_object(dict)["project"]
    obj: Dict[str, Any] = ctx.ensure_object(dict)
    client: TinyB = obj["client"]

    service = DataConnectorType.GCLOUD_STORAGE
    click.echo(FeedbackManager.prompt_gcs_connection_header())
    connection_name = get_gcs_connection_name(project.folder)
    run_gcp_svc_account_connection_flow(environment=obj["env"])
    creds_json = get_gcs_svc_account_creds()
    unique_suffix = uuid.uuid4().hex[:8]  # Use first 8 chars of a UUID for brevity
    secret_name = f"gcs_svc_account_creds_{connection_name}_{unique_suffix}"
    if obj["env"] == "local":
        save_secret_to_env_file(project=project, name=secret_name, value=creds_json)
    else:
        client.create_secret(name=secret_name, value=creds_json)

    connection_path = generate_gcs_connection_file_with_secrets(
        name=connection_name,
        service=service,
        svc_account_creds=secret_name,
        folder=project.folder,
    )

    create_in_cloud = (
        click.confirm(FeedbackManager.prompt_connection_in_cloud_confirmation(), default=True)
        if obj["env"] == "local"
        else False
    )

    if create_in_cloud:
        prod_config = obj["config"]
        host = prod_config["host"]
        token = prod_config["token"]
        prod_client = TinyB(
            token=token,
            host=host,
            staging=False,
        )
        creds_json = get_gcs_svc_account_creds()
        secret_name = f"gcs_svc_account_creds_{connection_name}_{unique_suffix}"
        prod_client.create_secret(name=secret_name, value=creds_json)

    click.echo(
        FeedbackManager.prompt_gcs_success(
            connection_name=connection_name,
            connection_path=connection_path,
        )
    )


@connection_create.command(name="kafka", short_help="Creates a Kafka connection.")
@click.pass_context
def connection_create_kafka_cmd(ctx: Context) -> None:
    """
    Creates a Kafka connection.

    \b
    $ tb connection create kafka
    """
    connection_create_kafka(ctx)


def connection_create_kafka(ctx: Context) -> Tuple[str, str, str, str, str, str, str, str, List[str]]:
    obj: Dict[str, Any] = ctx.ensure_object(dict)
    click.echo(FeedbackManager.gray(message="\n» Creating Kafka connection..."))
    project: Project = ctx.ensure_object(dict)["project"]
    name = get_kafka_connection_name(project.folder, "")
    default_bootstrap_servers = "localhost:9092"
    bootstrap_servers = click.prompt(
        FeedbackManager.highlight(
            message=f"? Bootstrap servers (comma-separated list of host:port pairs) [{default_bootstrap_servers}]"
        ),
        default=default_bootstrap_servers,
        show_default=False,
    )
    if not bootstrap_servers:
        bootstrap_servers = click.prompt("Bootstrap Server")

    validate_kafka_bootstrap_servers(bootstrap_servers)
    secret_required = click.confirm(
        FeedbackManager.highlight(message="  ? Do you want to store the bootstrap server in a .env.local file? [Y/n]"),
        default=True,
        show_default=False,
    )
    tb_secret_bootstrap_servers: Optional[str] = None
    tb_secret_key: Optional[str] = None
    tb_secret_secret: Optional[str] = None

    if secret_required:
        tb_secret_bootstrap_servers = str(click.prompt(FeedbackManager.highlight(message="    ? Secret name")))
        try:
            save_secret_to_env_file(project=project, name=tb_secret_bootstrap_servers, value=bootstrap_servers)
        except Exception as e:
            raise CLIConnectionException(FeedbackManager.error(message=str(e)))

    key = click.prompt(FeedbackManager.highlight(message="? Kafka key"))

    validate_kafka_key(key)

    secret_required = click.confirm(
        FeedbackManager.highlight(message="  ? Do you want to store the Kafka key in a .env.local file? [Y/n]"),
        default=True,
        show_default=False,
    )

    if secret_required:
        tb_secret_key = str(click.prompt(FeedbackManager.highlight(message="    ? Secret name")))
        try:
            save_secret_to_env_file(project=project, name=tb_secret_key, value=key)
        except Exception as e:
            raise CLIConnectionException(FeedbackManager.error(message=str(e)))

    secret = click.prompt(FeedbackManager.highlight(message="? Kafka secret"), hide_input=True)

    validate_kafka_secret(secret)

    secret_required = click.confirm(
        FeedbackManager.highlight(message="  ? Do you want to store the Kafka secret in a .env.local file? [Y/n]"),
        default=True,
        show_default=False,
    )

    if secret_required:
        tb_secret_secret = str(click.prompt(FeedbackManager.highlight(message="    ? Secret name")))
        try:
            save_secret_to_env_file(project=project, name=tb_secret_secret, value=secret)
        except Exception as e:
            raise CLIConnectionException(FeedbackManager.error(message=str(e)))

    security_protocol_options = ["SASL_SSL", "PLAINTEXT"]
    security_protocol = click.prompt(
        FeedbackManager.highlight(message="? Security Protocol (SASL_SSL, PLAINTEXT) [SASL_SSL]"),
        type=click.Choice(security_protocol_options),
        show_default=False,
        show_choices=False,
        default="SASL_SSL",
    )

    sasl_mechanism_options = ["PLAIN", "SCRAM-SHA-256", "SCRAM-SHA-512"]
    sasl_mechanism = click.prompt(
        FeedbackManager.highlight(message="? SASL Mechanism (PLAIN, SCRAM-SHA-256, SCRAM-SHA-512) [PLAIN]"),
        type=click.Choice(sasl_mechanism_options),
        show_default=False,
        show_choices=False,
        default="PLAIN",
    )

    create_in_cloud = (
        click.confirm(
            FeedbackManager.highlight(
                message="? Would you like to create this connection in the cloud environment as well? [Y/n]"
            ),
            default=True,
            show_default=False,
        )
        if obj["env"] == "local" and (tb_secret_bootstrap_servers or tb_secret_key or tb_secret_secret)
        else False
    )

    if create_in_cloud:
        click.echo(FeedbackManager.gray(message="» Creating Secrets in cloud environment..."))
        prod_config = obj["config"]
        host = prod_config["host"]
        token = prod_config["token"]
        prod_client = TinyB(
            token=token,
            host=host,
            staging=False,
        )
        if tb_secret_bootstrap_servers:
            prod_client.create_secret(name=tb_secret_bootstrap_servers, value=bootstrap_servers)
        if tb_secret_key:
            prod_client.create_secret(name=tb_secret_key, value=key)
        if tb_secret_secret:
            prod_client.create_secret(name=tb_secret_secret, value=secret)
        click.echo(FeedbackManager.success(message="✓ Secrets created!"))

    schema_registry_url = click.prompt(
        FeedbackManager.highlight(message="? Schema Registry URL (optional)"),
        default="",
        show_default=False,
    )
    if schema_registry_url:
        validate_kafka_schema_registry_url(schema_registry_url)

    auto_offset_reset_options = ["latest", "earliest"]
    auto_offset_reset = click.prompt(
        FeedbackManager.highlight(message="? Auto offset reset (latest, earliest) [latest]"),
        type=click.Choice(auto_offset_reset_options),
        default="latest",
        show_default=False,
        show_choices=False,
    )
    validate_kafka_auto_offset_reset(auto_offset_reset)
    click.echo(FeedbackManager.gray(message="» Validating connection..."))

    topics = list_kafka_topics(bootstrap_servers, key, secret, security_protocol, sasl_mechanism)

    if topics is None:
        raise CLIConnectionException(FeedbackManager.error(message="Invalid Kafka connection"))

    click.echo(FeedbackManager.success(message="✓ Connection is valid"))
    generate_kafka_connection_with_secrets(
        name=name,
        bootstrap_servers=bootstrap_servers,
        tb_secret_bootstrap_servers=tb_secret_bootstrap_servers,
        key=key,
        tb_secret_key=tb_secret_key,
        secret=secret,
        tb_secret_secret=tb_secret_secret,
        security_protocol=security_protocol,
        sasl_mechanism=sasl_mechanism,
        folder=project.folder,
    )
    click.echo(FeedbackManager.info_file_created(file=f"connections/{name}.connection"))
    click.echo(FeedbackManager.success(message="✓ Connection created!"))
    return (
        name,
        bootstrap_servers,
        key,
        secret,
        schema_registry_url,
        auto_offset_reset,
        sasl_mechanism,
        security_protocol,
        topics,
    )


def list_kafka_topics(bootstrap_servers, sasl_username, sasl_password, security_protocol, sasl_mechanism):
    conf = {
        "bootstrap.servers": bootstrap_servers,
        "security.protocol": security_protocol,
        "sasl.mechanism": sasl_mechanism,
        "sasl.username": sasl_username,
        "sasl.password": sasl_password,
        "log_level": 0,
    }

    try:
        client = AdminClient(conf)
        metadata = client.list_topics(timeout=5)
        return list(metadata.topics.keys())
    except Exception:
        return None
