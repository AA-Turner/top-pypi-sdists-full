# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

import uuid
from typing import Any, Dict, List, Optional

import click
from click import Context

from tinybird.tb.client import TinyB
from tinybird.tb.modules.build_common import process as build_project
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.common import (
    DataConnectorType,
    _get_setting_value,
    echo_safe_humanfriendly_tables_format_smart_table,
    get_gcs_connection_name,
    get_gcs_svc_account_creds,
    run_gcp_svc_account_connection_flow,
)
from tinybird.tb.modules.connection_kafka import (
    connection_create_kafka,
    echo_kafka_data,
    select_connection,
    select_group_id,
    select_topic,
)
from tinybird.tb.modules.connection_s3 import (
    echo_s3_data,
    select_bucket_uri,
    select_sample_file_uri,
)
from tinybird.tb.modules.create import (
    generate_gcs_connection_file_with_secrets,
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

    datasources = client.datasources()
    connections = client.connections(connector=service, datasources=datasources)
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
def connection_create_s3_cmd(ctx: Context) -> None:
    """
    Creates a AWS S3 connection.

    \b
    $ tb connection create s3
    """
    from tinybird.tb.modules.connection_s3 import connection_create_s3

    obj: Dict[str, Any] = ctx.ensure_object(dict)
    project: Project = obj["project"]
    client: TinyB = obj["client"]
    env: str = obj["env"]
    config = obj["config"]

    # Check AWS credentials before building - skip build if unavailable
    local_aws_unavailable = env == "local" and not client.check_aws_credentials()

    if env == "local" and not local_aws_unavailable:
        click.echo(FeedbackManager.gray(message="» Building project before continue..."))
        error = build_project(project=project, tb_client=client, watch=False, config=config, silent=True)
        if error:
            click.echo(FeedbackManager.error(message=error))
        else:
            click.echo(FeedbackManager.success(message="✓ Build completed"))

    result = connection_create_s3(ctx)

    if result["error"]:
        click.echo(FeedbackManager.error(message=result["error"]))


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


@connection_create.command(name="kafka", help="Create a Kafka connection.")
@click.option("--connection-name", default=None, help="The name of the connection to identify it in Tinybird")
@click.option("--bootstrap-servers", default=None, help="Kafka Bootstrap Server in form mykafka.mycloud.com:9092")
@click.option("--key", default=None, help="Key/User")
@click.option("--secret", default=None, help="Secret/Password")
@click.option(
    "--auto-offset-reset", default=None, help="Offset reset, can be 'latest' or 'earliest'. Defaults to 'latest'."
)
@click.option("--schema-registry-url", default=None, help="Avro Confluent Schema Registry URL")
@click.option(
    "--sasl-mechanism",
    default="PLAIN",
    help="Authentication method for connection-based protocols. Defaults to 'PLAIN'",
)
@click.option(
    "--security-protocol",
    default="SASL_SSL",
    help="Security protocol for connection-based protocols. Defaults to 'SASL_SSL'",
)
@click.option("--ssl-ca-pem", default=None, help="Path or content of the CA Certificate file in PEM format")
@click.pass_context
def connection_create_kafka_cmd(
    ctx: Context,
    connection_name: Optional[str],
    bootstrap_servers: Optional[str],
    key: Optional[str],
    secret: Optional[str],
    auto_offset_reset: Optional[str],
    schema_registry_url: Optional[str],
    sasl_mechanism: Optional[str],
    security_protocol: Optional[str],
    ssl_ca_pem: Optional[str],
) -> None:
    env: str = ctx.ensure_object(dict)["env"]
    project: Project = ctx.ensure_object(dict)["project"]
    client: TinyB = ctx.ensure_object(dict)["client"]
    config: Dict[str, Any] = ctx.ensure_object(dict)["config"]
    if env == "local":
        click.echo(FeedbackManager.gray(message="» Building project before continue..."))
        error = build_project(project=project, tb_client=client, watch=False, config=config, silent=True)
        if error:
            click.echo(FeedbackManager.info(message=error))
            click.echo(
                FeedbackManager.error(message="✗ Build failed. Existing connections might not be available yet.")
            )
        else:
            click.echo(FeedbackManager.success(message="✓ Build completed"))

    result = connection_create_kafka(
        ctx,
        connection_name=connection_name,
        bootstrap_servers=bootstrap_servers,
        key=key,
        secret=secret,
        auto_offset_reset=auto_offset_reset,
        schema_registry_url=schema_registry_url,
        sasl_mechanism=sasl_mechanism,
        security_protocol=security_protocol,
        ssl_ca_pem=ssl_ca_pem,
    )

    if not result["error"]:
        yes = click.confirm(
            FeedbackManager.highlight(message="? Would you like to preview data from the connection?"),
            default=True,
            show_default=True,
        )
        if yes:
            click.echo(FeedbackManager.gray(message="» Building project to preview the connection..."))
            if env == "local":
                error = build_project(project=project, tb_client=client, watch=False, config=config, silent=True)
                if error:
                    click.echo(FeedbackManager.info(message=error))
                    click.echo(
                        FeedbackManager.error(
                            message="✗ Build failed. Please fix the errors and run `tb connection data` to preview this connection."
                        )
                    )
                    return

                click.echo(FeedbackManager.success(message="✓ Build completed"))

            connection_data(connection_name=result["name"], client=client)

        else:
            click.echo(FeedbackManager.gray(message="Skipping data preview."))


@connection.command(name="data", help="Preview data from an existing connection.")
@click.argument("connection_name", type=str, required=False)
@click.option("--kafka-topic", type=str, help="The Kafka topic to preview")
@click.option("--kafka-group-id", type=str, help="The Kafka group ID to use for preview")
@click.option("--s3-bucket-uri", type=str, help="The S3 bucket URI to preview (e.g., s3://my-bucket/*.csv)")
@click.option(
    "--s3-sample-file-uri", type=str, help="The S3 sample file URI to preview (e.g., s3://my-bucket/sample.csv)"
)
@click.pass_context
def connection_data_cmd(
    ctx: Context,
    connection_name: Optional[str] = None,
    kafka_topic: Optional[str] = None,
    kafka_group_id: Optional[str] = None,
    s3_bucket_uri: Optional[str] = None,
    s3_sample_file_uri: Optional[str] = None,
) -> None:
    project: Project = ctx.ensure_object(dict)["project"]
    client: TinyB = ctx.ensure_object(dict)["client"]
    env: str = ctx.ensure_object(dict)["env"]
    config: Dict[str, Any] = ctx.ensure_object(dict)["config"]

    if env == "local":
        click.echo(FeedbackManager.gray(message="» Building project to access the latest connections..."))
        build_project(project=project, tb_client=client, watch=False, config=config, silent=True)
        click.echo(FeedbackManager.success(message="✓ Build completed"))

    if connection_name is None:
        # Get all supported connections (kafka and s3)
        kafka_connections = client.connections("kafka")
        s3_connections = client.connections("s3") + client.connections("s3_iamrole")
        all_connections = kafka_connections + s3_connections

        if not all_connections:
            raise CLIConnectionException(
                FeedbackManager.error(
                    message="No connections found. Create a connection first with `tb connection create`."
                )
            )

        connection = select_connection(None, "data", all_connections, client)
        connection_name = connection["name"]

    connection_data(connection_name, client, kafka_topic, kafka_group_id, s3_bucket_uri, s3_sample_file_uri)


def connection_data(
    connection_name: str,
    client: TinyB,
    kafka_topic: Optional[str] = None,
    kafka_group_id: Optional[str] = None,
    s3_bucket_uri: Optional[str] = None,
    s3_sample_file_uri: Optional[str] = None,
) -> None:
    connection = next((c for c in client.connections() if c["name"] == connection_name), None)
    if not connection:
        raise CLIConnectionException(FeedbackManager.error(message=f"Connection {connection_name} not found."))

    connection_id = connection["id"]
    service = connection["service"]

    supported_services = [DataConnectorType.KAFKA, DataConnectorType.AMAZON_S3, DataConnectorType.AMAZON_S3_IAMROLE]
    if service not in supported_services:
        raise CLIConnectionException(
            FeedbackManager.error(
                message=f"{service} connections are not supported yet for previewing data. Supported connections: kafka, s3, s3_iamrole"
            )
        )

    if service == DataConnectorType.KAFKA:
        topic = select_topic(kafka_topic, connection_id, client)
        group_id = select_group_id(kafka_group_id, topic, connection_id, client)
        echo_kafka_data(connection_id, connection_name, topic, group_id, client)
    elif service in [DataConnectorType.AMAZON_S3, DataConnectorType.AMAZON_S3_IAMROLE]:
        bucket_uri = select_bucket_uri(s3_bucket_uri)
        sample_file_uri = select_sample_file_uri(s3_sample_file_uri, bucket_uri, connection_id, client)
        echo_s3_data(connection_id, connection_name, bucket_uri, sample_file_uri, client)
