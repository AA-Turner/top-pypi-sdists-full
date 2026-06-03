# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

import re
import uuid
from datetime import datetime
from typing import Any, Dict, Optional, Tuple

import click
import pyperclip
from click import Context
from confluent_kafka.admin import AdminClient

from tinybird.tb.client import TinyB
from tinybird.tb.modules.common import (
    echo_safe_humanfriendly_tables_format_smart_table,
    get_aws_iamrole_policies,
    get_kafka_connection_name,
    validate_kafka_bootstrap_servers,
    validate_string_connector_param,
)
from tinybird.tb.modules.create import generate_kafka_connection_with_secrets
from tinybird.tb.modules.exceptions import CLIConnectionException, CLIException
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.local_common import get_tinybird_local_client
from tinybird.tb.modules.project import Project
from tinybird.tb.modules.secret import save_secret_to_env_file
from tinybird.tb.modules.telemetry import add_telemetry_event

# SASL mechanisms that authenticate with a username/password pair (the "key" + "secret"
# the wizard collects). OAUTHBEARER is intentionally excluded — its credentials come
# from the AWS IAM role flow, not from a key/secret prompt.
SASL_MECHANISMS_WITH_CREDENTIALS = ("PLAIN", "SCRAM-SHA-256", "SCRAM-SHA-512")


def run_kafka_aws_iamrole_connection_flow(
    config: Dict[str, Any],
    client: TinyB,
    connection_name: str,
    external_id_override: Optional[str] = None,
) -> Tuple[str, str, str, str, Optional[TinyB], Optional[TinyB]]:
    """Interactive AWS IAM Role connection flow for Kafka (MSK).

    Walks the user through creating an IAM access policy and role with the trust
    policy that includes the AWS account IDs of the selected environments
    (local, cloud, or both), then returns everything the caller needs to write
    the `.connection` file and store the role ARN as a secret.
    """
    service = "kafka"

    msk_cluster_arn = click.prompt(
        FeedbackManager.highlight(
            message="? MSK Cluster ARN (e.g., arn:aws:kafka:us-east-1:123456789012:cluster/my-cluster/...)"
        ),
        prompt_suffix="\n> ",
    )
    validate_string_connector_param("MSK Cluster ARN", msk_cluster_arn)

    # ARN can be either ".../cluster/NAME" or ".../cluster/NAME/UUID"; cluster
    # name is the second-to-last segment when a UUID is present, otherwise last.
    if "/" in msk_cluster_arn:
        arn_parts = msk_cluster_arn.split("/")
        cluster_name = arn_parts[-2] if len(arn_parts) >= 3 else arn_parts[-1]
    else:
        cluster_name = "cluster"

    try:
        region = msk_cluster_arn.split(":")[3]
    except (IndexError, AttributeError):
        region = ""

    if not region or not region.strip():
        region = click.prompt(
            FeedbackManager.highlight(message="? Region (the region where the MSK cluster is located)"),
            default="us-east-1",
            show_default=True,
            prompt_suffix="\n> ",
        )
    validate_string_connector_param("Region", region)

    cloud_client, local_client = _choose_environments_and_init_clients(config)

    # Policy fetch can fail if the server doesn't have AWS credentials (typical for
    # tb local) or if the role already exists out-of-band. We don't want that to
    # abort the wizard — the user can still paste a known role ARN + external_id
    # at the end. Show a warning and continue with placeholder text so the
    # walkthrough steps below still display something sensible.
    try:
        access_policy, trust_policy, external_id = get_aws_iamrole_policies(
            client,
            service=service,
            policy="read",
            bucket=msk_cluster_arn,
            external_id_seed=connection_name,
            cloud_client=cloud_client,
            local_client=local_client,
        )
    except Exception as e:
        click.echo(
            FeedbackManager.warning(
                message=(
                    f"⚠ Could not auto-generate IAM policies from Tinybird ({e}). "
                    "Continuing anyway — you can still paste a pre-existing Role ARN + External ID below."
                )
            )
        )
        access_policy = "<could not generate — see your AWS admin or use an existing policy>"
        trust_policy = "<could not generate — see your AWS admin or use an existing role>"
        external_id = ""

    click.echo(FeedbackManager.gray(message="\n» Step 1: AWS Authentication"))
    click.echo(
        FeedbackManager.info(
            message="Please log into your AWS Console. We'll guide you through creating the necessary permissions: https://console.aws.amazon.com/"
        )
    )
    click.echo(
        FeedbackManager.info(
            message="You'll be creating a single IAM Policy and Role to access your Kafka data. Using IAM Roles improves security by providing temporary credentials and following least privilege principles."
        )
    )
    click.echo(FeedbackManager.click_enter_to_continue())
    input()

    access_policy_copied = False
    try:
        pyperclip.copy(access_policy)
        access_policy_copied = True
    except Exception:
        pass

    click.echo(FeedbackManager.gray(message="» Step 2: Create IAM Policy"))
    click.echo(
        FeedbackManager.info(
            message=f"1. Go to AWS IAM > Create Policy: https://console.aws.amazon.com/iamv2/home?region={region}#/policies/create"
        )
    )
    click.echo(FeedbackManager.info(message="2. Select the JSON tab"))
    if access_policy_copied:
        click.echo(FeedbackManager.info(message="3. Paste the following policy (already copied to clipboard):"))
    else:
        click.echo(FeedbackManager.info(message="3. Copy and paste the following policy:"))
    click.echo(FeedbackManager.highlight(message=f"\n{access_policy}\n"))
    click.echo(
        FeedbackManager.info(
            message=f"4. Name the policy something meaningful (e.g., TinybirdKafkaAccess-{cluster_name})"
        )
    )
    click.echo(FeedbackManager.info(message="5. Click 'Create policy'"))
    click.echo(FeedbackManager.click_enter_to_continue())
    input()

    trust_policy_copied = False
    try:
        pyperclip.copy(trust_policy)
        trust_policy_copied = True
    except Exception:
        pass

    click.echo(FeedbackManager.gray(message="» Step 3: Create IAM Role"))
    click.echo(
        FeedbackManager.info(
            message=f"1. Go to AWS IAM > Create Role: https://console.aws.amazon.com/iamv2/home?region={region}#/roles/create"
        )
    )
    click.echo(FeedbackManager.info(message='2. Choose "Custom trust policy"'))
    if trust_policy_copied:
        click.echo(FeedbackManager.info(message="3. Paste the following trust policy (already copied to clipboard):"))
    else:
        click.echo(FeedbackManager.info(message="3. Paste the following trust policy:"))
    click.echo(FeedbackManager.highlight(message=f"\n{trust_policy}\n"))
    click.echo(FeedbackManager.info(message="4. Click Next, search for and select the policy you just created"))
    click.echo(
        FeedbackManager.info(message=f"5. Name the role something meaningful (e.g., TinybirdKafkaRole-{cluster_name})")
    )
    click.echo(FeedbackManager.info(message="6. Click 'Create role'"))
    click.echo(FeedbackManager.info(message="7. Copy the Role ARN from the role details page"))

    role_arn = click.prompt(
        FeedbackManager.highlight(message="? Please enter the ARN of the role you just created"),
        show_default=False,
    )
    validate_string_connector_param("Role ARN", role_arn)

    # Allow a pre-shared external_id (e.g. when the role's trust policy was set up
    # out-of-band with a specific External ID agreed between the cluster owner and
    # Tinybird). Flag wins; otherwise prompt; empty answer keeps the server-generated one.
    if external_id_override and external_id_override.strip():
        external_id = external_id_override.strip()
    else:
        provided = click.prompt(
            FeedbackManager.highlight(
                message="? External ID (optional, leave blank to use the Tinybird-generated one shown in the trust policy above)"
            ),
            default="",
            show_default=False,
        )
        if provided and provided.strip():
            external_id = provided.strip()

    return role_arn, region, external_id, msk_cluster_arn, cloud_client, local_client


def _choose_environments_and_init_clients(
    config: Dict[str, Any],
) -> Tuple[Optional[TinyB], Optional[TinyB]]:
    """Ask the user which environments the connection targets and initialize the
    corresponding clients (used to create the role-ARN secret in both)."""
    click.echo(
        FeedbackManager.highlight(
            message="? Which environments will use this connection? (the role-ARN secret will be created in the selected envs)"
        )
    )
    click.echo("  [1] Local only")
    click.echo("  [2] Cloud only")
    click.echo("  [3] Both")
    env_choice = click.prompt("\nSelect option", default=3, type=int)

    if env_choice == 1:
        use_local, use_cloud = True, False
    elif env_choice == 2:
        use_local, use_cloud = False, True
    else:
        if env_choice != 3:
            click.echo(FeedbackManager.warning(message="Invalid option. Defaulting to 'Both'."))
        use_local, use_cloud = True, True

    local_client: Optional[TinyB] = None
    cloud_client: Optional[TinyB] = None

    if use_local:
        try:
            local_client, _ = get_tinybird_local_client(config)
        except Exception as e:
            click.echo(FeedbackManager.warning(message=f"Failed to initialize local client: {e}"))

    if use_cloud:
        try:
            cloud_client = TinyB(token=config.get("token", ""), host=config.get("host", ""), staging=False)
        except Exception as e:
            click.echo(FeedbackManager.warning(message=f"Failed to initialize cloud client: {e}"))

    return cloud_client, local_client


def run_kafka_aws_iamrole_existing_role_flow(
    config: Dict[str, Any],
    external_id_override: Optional[str] = None,
) -> Tuple[str, str, str, str, Optional[TinyB], Optional[TinyB]]:
    """Fast path for users who already have an IAM role configured for MSK.

    Skips the policy fetch and the AWS Console walkthrough entirely. Collects
    region + role ARN + external ID + env choice for secret storage.
    """
    region = click.prompt(
        FeedbackManager.highlight(message="? AWS region of the MSK cluster"),
        default="us-east-1",
        show_default=True,
    )
    validate_string_connector_param("Region", region)

    role_arn = click.prompt(
        FeedbackManager.highlight(message="? IAM Role ARN to assume for MSK"),
        show_default=False,
    )
    validate_string_connector_param("Role ARN", role_arn)

    external_id = ""
    if external_id_override and external_id_override.strip():
        external_id = external_id_override.strip()
    else:
        provided = click.prompt(
            FeedbackManager.highlight(
                message="? External ID (leave blank to let Tinybird derive one from the workspace)"
            ),
            default="",
            show_default=False,
        )
        if provided and provided.strip():
            external_id = provided.strip()

    cloud_client, local_client = _choose_environments_and_init_clients(config)

    # msk_cluster_arn is never written to the .connection file — return "" since
    # the caller ignores it on this code path.
    return role_arn, region, external_id, "", cloud_client, local_client


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
    oauthbearer_aws_external_id: Optional[str] = None,
) -> dict[str, Any]:
    obj: Dict[str, Any] = ctx.ensure_object(dict)
    click.echo(FeedbackManager.gray(message="\n» Creating Kafka connection..."))
    project: Project = ctx.ensure_object(dict)["project"]
    client: TinyB = ctx.ensure_object(dict)["client"]
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

    security_protocol_options = ["SASL_SSL", "SASL_PLAINTEXT", "PLAINTEXT"]
    security_protocol = security_protocol or click.prompt(
        FeedbackManager.highlight(message="? Security Protocol (SASL_SSL, SASL_PLAINTEXT, PLAINTEXT) [SASL_SSL]"),
        type=click.Choice(security_protocol_options),
        show_default=False,
        show_choices=False,
        default="SASL_SSL",
    )

    if security_protocol not in security_protocol_options:
        raise CLIConnectionException(FeedbackManager.error(message=f"Invalid security protocol: {security_protocol}"))

    kafka_sasl_oauthbearer_method: Optional[str] = None
    kafka_sasl_oauthbearer_aws_region: Optional[str] = None
    kafka_sasl_oauthbearer_aws_role_arn: Optional[str] = None
    kafka_sasl_oauthbearer_aws_external_id: Optional[str] = None
    tb_secret_aws_role_arn: Optional[str] = None
    # Track if the role-ARN secret was already created in cloud during the OAUTHBEARER
    # flow so we don't prompt the user a second time in the cloud-secrets block below.
    aws_role_arn_secret_created_in_cloud = False

    # PLAINTEXT doesn't use SASL, so skip the mechanism prompt entirely.
    if security_protocol == "PLAINTEXT":
        sasl_mechanism = None
    else:
        sasl_mechanism_options = ["PLAIN", "SCRAM-SHA-256", "SCRAM-SHA-512", "OAUTHBEARER"]
        sasl_mechanism = sasl_mechanism or click.prompt(
            FeedbackManager.highlight(
                message="? SASL Mechanism (PLAIN, SCRAM-SHA-256, SCRAM-SHA-512, OAUTHBEARER) [PLAIN]"
            ),
            type=click.Choice(sasl_mechanism_options),
            show_default=False,
            show_choices=False,
            default="PLAIN",
        )
        if sasl_mechanism not in sasl_mechanism_options:
            raise CLIConnectionException(FeedbackManager.error(message=f"Invalid SASL mechanism: {sasl_mechanism}"))

    if sasl_mechanism == "OAUTHBEARER":
        kafka_sasl_oauthbearer_method = "AWS"

        # Fast-path for users who already have the IAM role + trust policy set up
        # (common: the role is owned by the same team as the MSK cluster and the
        # external_id was pre-shared). Skips policy fetch + AWS Console walkthrough.
        has_existing_role = click.confirm(
            FeedbackManager.highlight(
                message="? Do you already have an IAM role configured for this MSK cluster? [y/N]"
            ),
            default=False,
            show_default=False,
        )

        if has_existing_role:
            (
                kafka_sasl_oauthbearer_aws_role_arn,
                kafka_sasl_oauthbearer_aws_region,
                kafka_sasl_oauthbearer_aws_external_id,
                _,
                cloud_client,
                local_client,
            ) = run_kafka_aws_iamrole_existing_role_flow(
                config=obj["config"],
                external_id_override=oauthbearer_aws_external_id,
            )
        else:
            (
                kafka_sasl_oauthbearer_aws_role_arn,
                kafka_sasl_oauthbearer_aws_region,
                kafka_sasl_oauthbearer_aws_external_id,
                _,
                cloud_client,
                local_client,
            ) = run_kafka_aws_iamrole_connection_flow(
                config=obj["config"],
                client=client,
                connection_name=name,
                external_id_override=oauthbearer_aws_external_id,
            )

        # Auto-store the role ARN as a secret (in local + cloud per the user's choice
        # of environments) so the .connection file can reference it via tb_secret().
        unique_suffix = uuid.uuid4().hex[:8]
        secret_name = f"kafka_role_arn_{name}_{unique_suffix}"
        secret_created = False

        if local_client and kafka_sasl_oauthbearer_aws_role_arn:
            try:
                save_secret_to_env_file(project=project, name=secret_name, value=kafka_sasl_oauthbearer_aws_role_arn)
                secret_created = True
            except Exception as e:
                click.echo(FeedbackManager.warning(message=f"Failed to create secret in local: {e}"))

        if cloud_client and kafka_sasl_oauthbearer_aws_role_arn:
            try:
                cloud_client.create_secret(name=secret_name, value=kafka_sasl_oauthbearer_aws_role_arn)
                secret_created = True
                aws_role_arn_secret_created_in_cloud = True
            except Exception as e:
                click.echo(FeedbackManager.warning(message=f"Failed to create secret in cloud: {e}"))

        if secret_created:
            tb_secret_aws_role_arn = secret_name
        else:
            click.echo(
                FeedbackManager.warning(
                    message="No secrets were created. The role ARN will be stored directly in the connection file."
                )
            )

    # PLAIN/SCRAM still need a username + password.
    if sasl_mechanism in SASL_MECHANISMS_WITH_CREDENTIALS:
        key = key or click.prompt(FeedbackManager.highlight(message="? Kafka key"))
        assert isinstance(key, str)

        if click.confirm(
            FeedbackManager.info(message="  ? Do you want to store the Kafka key in a .env.local file? [Y/n]"),
            default=True,
            show_default=False,
        ):
            tb_secret_key = str(click.prompt(FeedbackManager.info(message="    ? Secret name")))
            try:
                save_secret_to_env_file(project=project, name=tb_secret_key, value=key)
            except Exception as e:
                raise CLIConnectionException(FeedbackManager.error(message=str(e)))

        secret = secret or click.prompt(FeedbackManager.highlight(message="? Kafka secret"), hide_input=True)
        assert isinstance(secret, str)

        if click.confirm(
            FeedbackManager.info(message="  ? Do you want to store the Kafka secret in a .env.local file? [Y/n]"),
            default=True,
            show_default=False,
        ):
            tb_secret_secret = str(click.prompt(FeedbackManager.info(message="    ? Secret name")))
            try:
                save_secret_to_env_file(project=project, name=tb_secret_secret, value=secret)
            except Exception as e:
                raise CLIConnectionException(FeedbackManager.error(message=str(e)))

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

    # Skip the role-ARN secret in this check if it was already created in cloud
    # by the OAUTHBEARER flow above.
    has_secrets_needing_cloud_creation = (
        tb_secret_bootstrap_servers
        or tb_secret_key
        or tb_secret_secret
        or tb_secret_ssl_ca_pem
        or (tb_secret_aws_role_arn and not aws_role_arn_secret_created_in_cloud)
    )
    create_in_cloud = (
        click.confirm(
            FeedbackManager.highlight(
                message="? Would you like to create this connection in the cloud environment as well? [Y/n]"
            ),
            default=True,
            show_default=False,
        )
        if obj["env"] == "local" and has_secrets_needing_cloud_creation
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
            request_from=getattr(obj.get("client"), "request_from", None),
        )
        if tb_secret_bootstrap_servers:
            prod_client.create_secret(name=tb_secret_bootstrap_servers, value=bootstrap_servers)
        # tb_secret_key/tb_secret_secret are only set in the PLAIN/SCRAM branch,
        # where key/secret are guaranteed strings.
        if tb_secret_key and key is not None:
            prod_client.create_secret(name=tb_secret_key, value=key)
        if tb_secret_secret and secret is not None:
            prod_client.create_secret(name=tb_secret_secret, value=secret)
        if tb_secret_ssl_ca_pem and ssl_ca_pem:
            prod_client.create_secret(name=tb_secret_ssl_ca_pem, value=ssl_ca_pem)
        if tb_secret_aws_role_arn and kafka_sasl_oauthbearer_aws_role_arn and not aws_role_arn_secret_created_in_cloud:
            prod_client.create_secret(name=tb_secret_aws_role_arn, value=kafka_sasl_oauthbearer_aws_role_arn)
        click.echo(FeedbackManager.success(message="✓ Secrets created!"))

    topics: list[str] = []
    if sasl_mechanism in SASL_MECHANISMS_WITH_CREDENTIALS:
        click.echo(FeedbackManager.gray(message="» Validating connection..."))
        try:
            assert key is not None and secret is not None
            topics = list_kafka_topics(bootstrap_servers, key, secret, security_protocol, sasl_mechanism, ssl_ca_pem)
            click.echo(FeedbackManager.success(message="✓ Connection is valid"))
        except Exception as e:
            error = str(e)
            click.echo(FeedbackManager.error(message=f"Connection is not valid: {e}"))
            add_telemetry_event("connection_error", error=error)
    else:
        # OAUTHBEARER (no AWS creds locally) and PLAINTEXT defer validation to deploy-time.
        click.echo(
            FeedbackManager.info(
                message=f"⚠ Skipping local validation for {sasl_mechanism or 'PLAINTEXT'}. The connection will be validated on deploy."
            )
        )

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
        kafka_sasl_oauthbearer_method=kafka_sasl_oauthbearer_method,
        kafka_sasl_oauthbearer_aws_region=kafka_sasl_oauthbearer_aws_region,
        kafka_sasl_oauthbearer_aws_role_arn=kafka_sasl_oauthbearer_aws_role_arn,
        kafka_sasl_oauthbearer_aws_external_id=kafka_sasl_oauthbearer_aws_external_id,
        tb_secret_aws_role_arn=tb_secret_aws_role_arn,
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
