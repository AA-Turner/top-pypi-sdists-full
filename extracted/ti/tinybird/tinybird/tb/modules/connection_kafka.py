# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

import re
from datetime import datetime
from typing import Any, Dict, Optional

import click
from click import Context
from confluent_kafka.admin import AdminClient

from tinybird.tb.client import TinyB
from tinybird.tb.modules.common import (
    echo_safe_humanfriendly_tables_format_smart_table,
    get_kafka_connection_name,
    validate_kafka_bootstrap_servers,
)
from tinybird.tb.modules.create import generate_kafka_connection_with_secrets
from tinybird.tb.modules.exceptions import CLIConnectionException, CLIException
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.project import Project
from tinybird.tb.modules.secret import save_secret_to_env_file
from tinybird.tb.modules.telemetry import add_telemetry_event


def connection_create_kafka(
    ctx: Context,
    connection_name: Optional[str] = None,
    bootstrap_servers: Optional[str] = None,
    key: Optional[str] = None,
    secret: Optional[str] = None,
    auto_offset_reset: Optional[str] = None,
    schema_registry_url: Optional[str] = None,
    sasl_mechanism: Optional[str] = None,
    security_protocol: Optional[str] = None,
    ssl_ca_pem: Optional[str] = None,
) -> dict[str, Any]:
    obj: Dict[str, Any] = ctx.ensure_object(dict)
    click.echo(FeedbackManager.gray(message="\n» Creating Kafka connection..."))
    project: Project = ctx.ensure_object(dict)["project"]
    name = get_kafka_connection_name(project.folder, connection_name)
    error: Optional[str] = None

    if not bootstrap_servers:
        default_bootstrap_servers = "localhost:9092"
        bootstrap_servers = click.prompt(
            FeedbackManager.highlight(
                message=f"? Bootstrap servers (comma-separated list of host:port pairs) [{default_bootstrap_servers}]"
            ),
            default=default_bootstrap_servers,
            show_default=False,
        )

    assert isinstance(bootstrap_servers, str)

    try:
        validate_kafka_bootstrap_servers(bootstrap_servers)
        click.echo(FeedbackManager.success(message="✓ Server is valid"))
    except CLIException as e:
        error = str(e)
        click.echo(FeedbackManager.error(message=error))
        click.echo(FeedbackManager.warning(message="Process will continue, but the connection might not be valid."))
        add_telemetry_event("connection_error", error=error)

    secret_required = click.confirm(
        FeedbackManager.info(message="  ? Do you want to store the bootstrap server in a .env.local file? [Y/n]"),
        default=True,
        show_default=False,
    )
    tb_secret_bootstrap_servers: Optional[str] = None
    tb_secret_key: Optional[str] = None
    tb_secret_secret: Optional[str] = None
    tb_secret_ssl_ca_pem: Optional[str] = None

    if secret_required:
        tb_secret_bootstrap_servers = str(click.prompt(FeedbackManager.info(message="    ? Secret name")))
        try:
            save_secret_to_env_file(project=project, name=tb_secret_bootstrap_servers, value=bootstrap_servers)
        except Exception as e:
            raise CLIConnectionException(FeedbackManager.error(message=str(e)))

    key = click.prompt(FeedbackManager.highlight(message="? Kafka key"))

    assert isinstance(key, str)

    secret_required = click.confirm(
        FeedbackManager.info(message="  ? Do you want to store the Kafka key in a .env.local file? [Y/n]"),
        default=True,
        show_default=False,
    )

    if secret_required:
        tb_secret_key = str(click.prompt(FeedbackManager.info(message="    ? Secret name")))
        try:
            save_secret_to_env_file(project=project, name=tb_secret_key, value=key)
        except Exception as e:
            raise CLIConnectionException(FeedbackManager.error(message=str(e)))

    secret = secret or click.prompt(FeedbackManager.highlight(message="? Kafka secret"), hide_input=True)

    assert isinstance(secret, str)

    secret_required = click.confirm(
        FeedbackManager.info(message="  ? Do you want to store the Kafka secret in a .env.local file? [Y/n]"),
        default=True,
        show_default=False,
    )

    if secret_required:
        tb_secret_secret = str(click.prompt(FeedbackManager.info(message="    ? Secret name")))
        try:
            save_secret_to_env_file(project=project, name=tb_secret_secret, value=secret)
        except Exception as e:
            raise CLIConnectionException(FeedbackManager.error(message=str(e)))

    security_protocol_options = ["SASL_SSL", "PLAINTEXT"]
    security_protocol = security_protocol or click.prompt(
        FeedbackManager.highlight(message="? Security Protocol (SASL_SSL, PLAINTEXT) [SASL_SSL]"),
        type=click.Choice(security_protocol_options),
        show_default=False,
        show_choices=False,
        default="SASL_SSL",
    )

    if security_protocol not in security_protocol_options:
        raise CLIConnectionException(FeedbackManager.error(message=f"Invalid security protocol: {security_protocol}"))

    sasl_mechanism_options = ["PLAIN", "SCRAM-SHA-256", "SCRAM-SHA-512"]
    sasl_mechanism = sasl_mechanism or click.prompt(
        FeedbackManager.highlight(message="? SASL Mechanism (PLAIN, SCRAM-SHA-256, SCRAM-SHA-512) [PLAIN]"),
        type=click.Choice(sasl_mechanism_options),
        show_default=False,
        show_choices=False,
        default="PLAIN",
    )

    if sasl_mechanism not in sasl_mechanism_options:
        raise CLIConnectionException(FeedbackManager.error(message=f"Invalid SASL mechanism: {sasl_mechanism}"))

    if not schema_registry_url:
        schema_registry_url = click.prompt(
            FeedbackManager.highlight(message="? Schema Registry URL (optional)"),
            default="",
            show_default=False,
        )

    if not ssl_ca_pem:
        yes = click.confirm(
            FeedbackManager.highlight(
                message="? CA certificate in PEM format (optional)", default=True, show_default=False
            )
        )
        if yes:
            ssl_ca_pem = click.edit(
                "IMPORTANT: THIS LINE MUST BE DELETED. Enter your CA certificate value.", extension=".txt"
            )
            secret_required = click.confirm(
                FeedbackManager.info(message="  ? Do you want to store the Kafka key in a .env.local file? [Y/n]"),
                default=True,
                show_default=False,
            )
            if secret_required and ssl_ca_pem:
                tb_secret_ssl_ca_pem = str(click.prompt(FeedbackManager.info(message="    ? Secret name")))
                try:
                    save_secret_to_env_file(project=project, name=tb_secret_ssl_ca_pem, value=ssl_ca_pem)
                except Exception as e:
                    raise CLIConnectionException(FeedbackManager.error(message=str(e)))

    create_in_cloud = (
        click.confirm(
            FeedbackManager.highlight(
                message="? Would you like to create this connection in the cloud environment as well? [Y/n]"
            ),
            default=True,
            show_default=False,
        )
        if obj["env"] == "local"
        and (tb_secret_bootstrap_servers or tb_secret_key or tb_secret_secret or tb_secret_ssl_ca_pem)
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
        if tb_secret_ssl_ca_pem and ssl_ca_pem:
            prod_client.create_secret(name=tb_secret_ssl_ca_pem, value=ssl_ca_pem)
        click.echo(FeedbackManager.success(message="✓ Secrets created!"))

    click.echo(FeedbackManager.gray(message="» Validating connection..."))

    topics: list[str] = []
    try:
        topics = list_kafka_topics(bootstrap_servers, key, secret, security_protocol, sasl_mechanism, ssl_ca_pem)
        click.echo(FeedbackManager.success(message="✓ Connection is valid"))
    except Exception as e:
        error = str(e)
        click.echo(FeedbackManager.error(message=f"Connection is not valid: {e}"))
        add_telemetry_event("connection_error", error=error)

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
        ssl_ca_pem=ssl_ca_pem,
        tb_secret_ssl_ca_pem=tb_secret_ssl_ca_pem,
        schema_registry_url=schema_registry_url,
        folder=project.folder,
    )
    click.echo(FeedbackManager.info_file_created(file=f"connections/{name}.connection"))
    if error:
        click.echo(
            FeedbackManager.warning(
                message="Connection created, but some credentials are missing or invalid. Check https://www.tinybird.co/docs/forward/get-data-in/connectors/kafka#kafka-connection-settings for more details."
            )
        )
    else:
        click.echo(FeedbackManager.success(message="✓ Connection created!"))

    return {
        "name": name,
        "bootstrap_servers": bootstrap_servers,
        "key": key,
        "secret": secret,
        "sasl_mechanism": sasl_mechanism,
        "security_protocol": security_protocol,
        "topics": topics,
        "error": error,
    }


def list_kafka_topics(
    bootstrap_servers, sasl_username, sasl_password, security_protocol, sasl_mechanism, ssl_ca_pem
) -> list[str]:
    conf = {
        "bootstrap.servers": bootstrap_servers,
        "security.protocol": security_protocol,
        "sasl.mechanism": sasl_mechanism,
        "sasl.username": sasl_username,
        "sasl.password": sasl_password,
        "log_level": 0,
    }

    if ssl_ca_pem:
        conf["ssl.ca.pem"] = re.sub(r"\\n", r"\n", ssl_ca_pem)

    client = AdminClient(conf)
    metadata = client.list_topics(timeout=5)
    return list(metadata.topics.keys())


def generate_kafka_group_id(topic: str):
    return f"{topic}_{int(datetime.timestamp(datetime.now()))}"


def select_topic(kafka_topic: Optional[str], connection_id: str, client: TinyB) -> str:
    if kafka_topic:
        topics = client.kafka_list_topics(connection_id)
        if kafka_topic not in topics:
            raise CLIConnectionException(
                FeedbackManager.error(message=f"Topic '{kafka_topic}' not found. Topics available: {', '.join(topics)}")
            )
        topic = kafka_topic
    else:
        topics = client.kafka_list_topics(connection_id)
        click.echo(FeedbackManager.highlight(message="? Select a Kafka topic:"))
        topic_index = -1
        while topic_index == -1:
            for index, topic in enumerate(topics):
                click.echo(f"  [{index + 1}] {topic}")
            topic_index = click.prompt("\nSelect topic", default=1)
            try:
                topic = topics[int(topic_index) - 1]
            except Exception:
                topic_index = -1

    if not topic:
        raise CLIConnectionException(FeedbackManager.error(message="Topic is required."))

    return topic


def select_group_id(kafka_group_id: Optional[str], topic: str, connection_id: str, client: TinyB) -> str:
    group_id = kafka_group_id
    is_valid = False
    if not group_id:
        group_id = click.prompt(
            FeedbackManager.highlight(message="? Enter a Kafka group ID"),
            default=generate_kafka_group_id(topic),
            show_default=True,
        )
    while not is_valid:
        assert isinstance(group_id, str)

        click.echo(FeedbackManager.gray(message=f"» Validating group ID '{group_id}'..."))
        try:
            client.kafka_preview_group(connection_id, topic, group_id)
            is_valid = True
            click.echo(FeedbackManager.success(message=f"✓ Group ID '{group_id}' is valid."))
        except Exception as e:
            click.echo(FeedbackManager.error(message=str(e)))
            group_id = None  # Reset to prompt again

        if not is_valid:
            group_id = click.prompt(
                FeedbackManager.highlight(message="? Enter a Kafka group ID"),
                default=generate_kafka_group_id(topic),
                show_default=True,
            )

    if not group_id:
        raise CLIConnectionException(FeedbackManager.error(message="Group ID is required."))

    return group_id


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


def meta_to_schema(meta: list[dict[str, Any]]) -> str:
    return ",\n    ".join([f"`{col['name']}` {col['type']} `json:$.{col['name']}`" for col in meta])


def echo_kafka_data(
    connection_id: str, connection_name: str, topic: str, group_id: str, client: TinyB
) -> dict[str, list[dict[str, Any]]]:
    click.echo(FeedbackManager.highlight(message="» Previewing data..."))
    response = client.kafka_preview_topic(connection_id, topic, group_id)
    preview = response.get("preview", {})
    data = preview.get("data", [])
    meta = preview.get("meta", [])
    data_as_lists, column_names = preview_to_table(data, meta)

    if not data_as_lists and not column_names:
        click.echo(FeedbackManager.warning(message="No data to preview."))
    else:
        echo_safe_humanfriendly_tables_format_smart_table(data_as_lists, column_names)

    return {
        "data": data,
        "meta": meta,
    }


def select_connection(
    connection_id: Optional[str], connection_type: str, connections: list[dict[str, Any]], client: TinyB
) -> dict[str, Any]:
    click.echo(FeedbackManager.highlight(message=f"? Select a {connection_type.capitalize()} connection:"))
    connection_index = -1
    while connection_index == -1:
        for index, conn in enumerate(connections):
            click.echo(f"  [{index + 1}] {conn['name']}")
        connection_index = click.prompt("\nSelect connection", default=1)
        try:
            connection = connections[int(connection_index) - 1]
        except Exception:
            connection_index = -1
    return connection


def meta_to_datasource_datafile(
    datasource_name: str,
    meta: list[dict[str, Any]],
    connection_name: str,
    kafka_topic: str,
    kafka_group_id: str,
    kafka_auto_offset_reset: str,
) -> str:
    schema: str = meta_to_schema(meta)
    kafka_meta_columns = """# Kafka meta columns
    __topic LowCardinality(String),
    __partition Int16,
    __offset Int64,
    __timestamp DateTime,
    __key String,
    __value String -- Set KAFKA_STORE_RAW_VALUE to True to store the raw value of the message
    # __headers Map(String, String) -- Set KAFKA_STORE_HEADERS to True to store the headers of the message
    # Learn more at https://www.tinybird.co/docs/forward/get-data-in/connectors/kafka#kafka-meta-columns"""
    ds_content = f"""SCHEMA >
    {schema}{"," if schema else ""}
    {kafka_meta_columns}

ENGINE "MergeTree"
# ENGINE_SORTING_KEY "user_id, timestamp"
# ENGINE_TTL "__timestamp + toIntervalDay(60)"
# Learn more at https://www.tinybird.co/docs/forward/dev-reference/datafiles/datasource-files
KAFKA_CONNECTION_NAME {connection_name}
KAFKA_TOPIC {kafka_topic}
KAFKA_GROUP_ID {inject_tb_secret(f"KAFKA_GROUP_ID_LOCAL_{datasource_name}", kafka_group_id)} -- local secret to avoid using the same group_id in Local and Cloud
KAFKA_AUTO_OFFSET_RESET {kafka_auto_offset_reset}
# KAFKA_STORE_RAW_VALUE True
# KAFKA_STORE_HEADERS True
# Learn more at https://www.tinybird.co/docs/forward/get-data-in/connectors/kafka#kafka-datasource-settings
"""
    return ds_content


def inject_tb_secret(secret_name: str, default_value: str) -> str:
    return f"""{{{{ tb_secret("{secret_name}", "{default_value}") }}}}"""
