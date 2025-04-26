from typing import Optional

import click

from montecarlodata.agents.agent import AgentService
from montecarlodata.agents.fields import (
    AWS,
    AWS_ASSUMABLE_ROLE,
    AWS_GENERIC,
    AZURE,
    AZURE_BLOB,
    AZURE_FUNCTION_APP_KEY,
    AZURE_STORAGE_ACCOUNT_KEYS,
    DATA_STORE_AGENT,
    GCP,
    GCP_JSON_SERVICE_ACCOUNT_KEY,
    GCS,
    OAUTH2_CLIENT_CREDENTIALS,
    OAUTH2_PASSWORD,
    REMOTE_AGENT,
    S3,
)
from montecarlodata.collector.commands import NETWORK_TEST_OPTIONS
from montecarlodata.collector.network_tests import CollectorNetworkTestService
from montecarlodata.common import create_mc_client
from montecarlodata.common.commands import DC_ID_OPTION
from montecarlodata.integrations.commands import PASSWORD_VERBIAGE
from montecarlodata.tools import (
    AdvancedOptions,
    add_common_options,
    validate_json_callback,
)

DRY_RUN_OPTIONS = [
    click.option(
        "--dry-run",
        required=False,
        default=False,
        show_default=True,
        is_flag=True,
        help="Dry run (validates credentials but doesn't create agent).",
    ),
]

MUTUAL_TLS_OPTIONS = [
    click.option(
        "--client-certificate",
        help="Path to the file that contains a client certificate for agent connectivity.",
        required=False,
        type=click.Path(dir_okay=False, exists=True),
        cls=AdvancedOptions,
    ),
    click.option(
        "--private-key",
        help="Path to the file that contains a private key for the "
        "client certificate for agent connectivity.",
        required=False,
        type=click.Path(dir_okay=False, exists=True),
        cls=AdvancedOptions,
        required_with_options=["client_certificate"],
    ),
]

UPDATE_AGENT_OPTIONS = [
    click.option(
        "--agent-id",
        help="UUID of existing Agent to update.",
        required=False,
    )
]


@click.group(help="Manage a Monte Carlo Agent.")
def agents():
    """
    Group for any Agent related subcommands
    """
    pass


@agents.command(help="Register a Data Store Agent with remote Azure Blob storage container.")
@click.pass_obj
@click.option(
    "--connection-string",
    help=f"A connection string to an Azure Storage account. {PASSWORD_VERBIAGE}",
    required=True,
    cls=AdvancedOptions,
    prompt_if_requested=True,
)
@click.option(
    "--container-name",
    help="Name of Azure Storage container for data store.",
    required=True,
)
@add_common_options(DRY_RUN_OPTIONS)
@add_common_options(DC_ID_OPTION)
@add_common_options(UPDATE_AGENT_OPTIONS)
def register_azure_blob_store(ctx, container_name, **kwargs):
    AgentService(
        config=ctx["config"],
        mc_client=create_mc_client(ctx),
        command_name="agents register_azure_blob_store",
    ).create_agent(
        agent_type=DATA_STORE_AGENT,
        platform=AZURE,
        storage=AZURE_BLOB,
        auth_type=AZURE_STORAGE_ACCOUNT_KEYS,
        endpoint=container_name,
        **kwargs,
    )


@agents.command(help="Register a Data Store Agent with remote S3 bucket.")
@click.pass_obj
@click.option(
    "--assumable-role",
    help="ARN of AWS assumable role.",
    required=True,
)
@click.option(
    "--bucket-name",
    help="Name of S3 bucket for data store.",
    required=True,
)
@click.option(
    "--external-id",
    help="AWS External ID.",
    required=False,
)
@add_common_options(DRY_RUN_OPTIONS)
@add_common_options(DC_ID_OPTION)
@add_common_options(UPDATE_AGENT_OPTIONS)
def register_s3_store(ctx, bucket_name, **kwargs):
    AgentService(
        config=ctx["config"],
        mc_client=create_mc_client(ctx),
        command_name="agents register_s3_store",
    ).create_agent(
        agent_type=DATA_STORE_AGENT,
        platform=AWS,
        storage=S3,
        auth_type=AWS_ASSUMABLE_ROLE,
        endpoint=bucket_name,
        **kwargs,
    )


@agents.command(help="Register a Remote AWS Agent.")
@click.pass_obj
@click.option(
    "--assumable-role",
    help="ARN of AWS assumable role.",
    required=True,
)
@click.option(
    "--lambda-arn",
    help="ARN of AWS Lambda function.",
    required=True,
)
@click.option(
    "--external-id",
    help="AWS External ID.",
    required=False,
)
@add_common_options(DRY_RUN_OPTIONS)
@add_common_options(DC_ID_OPTION)
@add_common_options(UPDATE_AGENT_OPTIONS)
def register_aws_agent(ctx, lambda_arn, **kwargs):
    AgentService(
        config=ctx["config"],
        mc_client=create_mc_client(ctx),
        command_name="agents register_aws_agent",
    ).create_agent(
        agent_type=REMOTE_AGENT,
        platform=AWS,
        storage=S3,
        auth_type=AWS_ASSUMABLE_ROLE,
        endpoint=lambda_arn,
        **kwargs,
    )


@agents.command(help="Register a Remote AWS Proxied Agent.")
@click.pass_obj
@click.option(
    "--authentication",
    help="Authentication type.",
    required=False,
    type=click.Choice(
        [OAUTH2_CLIENT_CREDENTIALS.lower(), OAUTH2_PASSWORD.lower()], case_sensitive=False
    ),
    default=OAUTH2_CLIENT_CREDENTIALS.lower(),
)
@click.option(
    "--proxy-endpoint",
    help="HTTP/HTTPS Proxy URL.",
    required=True,
)
@click.option(
    "--auth-url",
    help="OAuth2 Client Credentials - Authentication URL, used to get the access token.",
    required=False,
    cls=AdvancedOptions,
)
@click.option(
    "--client-id",
    help="OAuth2 Client Credentials - Client ID.",
    required=False,
    cls=AdvancedOptions,
    required_with_options=["client_secret", "auth_url"],
    mutually_exclusive_options=["username", "password"],
)
@click.option(
    "--client-secret",
    help=f"OAuth2 Client Credentials - Client Secret. {PASSWORD_VERBIAGE}",
    required=False,
    cls=AdvancedOptions,
    prompt_if_requested=True,
    required_with_options=["client_id", "auth_url"],
    mutually_exclusive_options=["username", "password"],
)
@click.option(
    "--username",
    help="OAuth2 Username/Password - Username.",
    required=False,
    cls=AdvancedOptions,
    required_with_options=["password", "auth_url", "authentication"],
    mutually_exclusive_options=["client_id", "client_secret"],
)
@click.option(
    "--password",
    help=f"OAuth2 Username/Password - Password. {PASSWORD_VERBIAGE}",
    required=False,
    cls=AdvancedOptions,
    prompt_if_requested=True,
    required_with_options=["username", "auth_url", "authentication"],
    mutually_exclusive_options=["client_id", "client_secret"],
)
@click.option(
    "--deployment-type",
    help="Specify if this AWS Agent is deployed as 'lambda' or 'generic' (e.g. ECS, EKS, EC2)",
    required=False,
    type=click.Choice(["lambda", "generic"], case_sensitive=False),
    default="lambda",
)
@add_common_options(DRY_RUN_OPTIONS)
@add_common_options(DC_ID_OPTION)
@add_common_options(MUTUAL_TLS_OPTIONS)
@add_common_options(UPDATE_AGENT_OPTIONS)
def register_aws_proxied_agent(
    ctx,
    authentication: str,
    proxy_endpoint: str,
    auth_url: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    deployment_type: Optional[str] = None,
    **kwargs,
):
    AgentService(
        config=ctx["config"],
        mc_client=create_mc_client(ctx),
        command_name="agents register_aws_proxied_agent",
    ).create_agent(
        agent_type=REMOTE_AGENT,
        platform=AWS_GENERIC if deployment_type == "generic" else AWS,
        storage=S3,
        auth_type=authentication.upper(),
        endpoint=proxy_endpoint,
        auth_url=auth_url,
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        **kwargs,
    )


@agents.command(help="Register a Data Store Agent with Google Cloud Storage.")
@click.pass_obj
@click.option(
    "--key-file",
    help="JSON Key file if auth type is GCP JSON service account key.",
    type=click.Path(exists=True),
    required=True,
)
@click.option(
    "--bucket-name",
    help="Name of GCS bucket for data store.",
    required=True,
)
@add_common_options(DRY_RUN_OPTIONS)
@add_common_options(DC_ID_OPTION)
@add_common_options(UPDATE_AGENT_OPTIONS)
def register_gcs_store(ctx, bucket_name, **kwargs):
    AgentService(
        config=ctx["config"],
        mc_client=create_mc_client(ctx),
        command_name="agents register_gcs_store",
    ).create_agent(
        agent_type=DATA_STORE_AGENT,
        platform=GCP,
        storage=GCS,
        auth_type=GCP_JSON_SERVICE_ACCOUNT_KEY,
        endpoint=bucket_name,
        **kwargs,
    )


@agents.command(help="Register a Remote GCP Agent.")
@click.pass_obj
@click.option(
    "--key-file",
    help="JSON Key file if auth type is GCP JSON service account key.",
    required=True,
)
@click.option(
    "--url",
    help="URL for accessing agent.",
    required=True,
)
@add_common_options(DRY_RUN_OPTIONS)
@add_common_options(DC_ID_OPTION)
@add_common_options(MUTUAL_TLS_OPTIONS)
@add_common_options(UPDATE_AGENT_OPTIONS)
def register_gcp_agent(ctx, url, **kwargs):
    AgentService(
        config=ctx["config"],
        mc_client=create_mc_client(ctx),
        command_name="agents register_gcp_agent",
    ).create_agent(
        agent_type=REMOTE_AGENT,
        platform=GCP,
        storage=GCS,
        auth_type=GCP_JSON_SERVICE_ACCOUNT_KEY,
        endpoint=url,
        **kwargs,
    )


@agents.command(help="Register a Remote Azure Agent.")
@click.pass_obj
@click.option(
    "--app-key",
    help=f"App key from the Azure Function to use for authentication. {PASSWORD_VERBIAGE}",
    required=True,
    cls=AdvancedOptions,
    prompt_if_requested=True,
)
@click.option(
    "--url",
    help="URL for accessing agent.",
    required=True,
)
@add_common_options(DRY_RUN_OPTIONS)
@add_common_options(DC_ID_OPTION)
@add_common_options(MUTUAL_TLS_OPTIONS)
@add_common_options(UPDATE_AGENT_OPTIONS)
def register_azure_agent(ctx, url, **kwargs):
    AgentService(
        config=ctx["config"],
        mc_client=create_mc_client(ctx),
        command_name="agents register_azure_agent",
    ).create_agent(
        agent_type=REMOTE_AGENT,
        platform=AZURE,
        storage=AZURE_BLOB,
        auth_type=AZURE_FUNCTION_APP_KEY,
        endpoint=url,
        **kwargs,
    )


@agents.command(help="Deregister an Agent.")
@click.pass_obj
@click.option("--agent-id", help="UUID of Agent to deregister.", required=True)
def deregister(ctx, agent_id):
    """
    Deregister an Agent (deletes AgentModel from monolith)
    """
    AgentService(
        config=ctx["config"],
        mc_client=create_mc_client(ctx),
        command_name="agents deregister",
    ).delete_agent(agent_id)


@agents.command(help="Perform a health check of the Agent.")
@click.pass_obj
@click.option("--agent-id", help="UUID of Agent.", required=True)
def health(ctx, agent_id):
    """
    Check the health of an Agent
    """
    AgentService(
        config=ctx["config"],
        mc_client=create_mc_client(ctx),
        command_name="agents health",
    ).check_agent_health(agent_id)


@agents.command(help="Upgrades the running version of an Agent.")
@click.pass_obj
@click.option("--agent-id", help="UUID of Agent to upgrade.", required=True)
@click.option(
    "--image-tag",
    help="Image version to upgrade to.",
    required=False,
)
@click.option(
    "--params",
    "parameters",
    required=False,
    default=None,
    callback=validate_json_callback,
    help="""
              Parameters key,value pairs as JSON. If a key is not specified
              the existing (or default) value is used.
              \b
              \n
              E.g. --params '{"MemorySize":"1024", "ConcurrentExecutions": "25"}'
              """,
)  # \b disables wrapping
def upgrade(ctx, **kwargs):
    """
    Performs an upgrade of an Agent
    """
    AgentService(
        config=ctx["config"],
        mc_client=create_mc_client(ctx),
        command_name="agents upgrade",
    ).upgrade_agent(**kwargs)


@agents.command(help="List all agents in account.", name="list")
@click.pass_obj
@click.option(
    "--show-inactive",
    required=False,
    default=False,
    show_default=True,
    is_flag=True,
    help="Only list active agents.",
)
def list_agents(ctx, **kwargs):
    """
    List all Agents in account
    """
    AgentService(
        config=ctx["config"],
        mc_client=create_mc_client(ctx),
        command_name="agents list_agents",
    ).echo_agents(**kwargs)


@agents.command(help="Checks if telnet connection is usable from the agent.")
@click.pass_obj
@add_common_options(NETWORK_TEST_OPTIONS)
def test_telnet(ctx, **kwargs):
    """
    Network debugging utility to test telnet via the collector
    """
    CollectorNetworkTestService(
        config=ctx["config"],
        command_name="agents test_telnet",
    ).echo_telnet_test(**kwargs)


@agents.command(
    help="Tests if a destination exists and accepts requests. "
    "Opens a TCP Socket to a specific port from the agent."
)
@click.pass_obj
@add_common_options(NETWORK_TEST_OPTIONS)
def test_tcp_open(ctx, **kwargs):
    """
    Network debugging utility to test TCP open via the collector
    """
    CollectorNetworkTestService(
        config=ctx["config"],
        command_name="agents test_tcp_open",
    ).echo_tcp_open_test(**kwargs)


@agents.command(name="get-operation-logs", help="Returns the operation logs for a remote agent.")
@click.pass_obj
@click.option("--agent-id", help="UUID of Agent.", required=True)
@click.option(
    "--start-time",
    help="Optional start time, for example: 2023-12-02T13:40:25Z. Defaults to 10 minutes ago.",
    required=False,
)
@click.option(
    "--end-time",
    help="Optional end time, for example: 2023-12-02T13:45:25Z. Defaults to now.",
    required=False,
)
@click.option(
    "--limit",
    help="Maximum number of log events to return, defaults to 1,000",
    type=click.INT,
    required=False,
)
@click.option(
    "--connection-type",
    help="Optional connection type to filter logs, for example snowflake, redshift, etc.",
    required=False,
)
def get_operation_logs(ctx, **kwargs):
    """
    Displays the operation logs for a remote Agent.
    """
    AgentService(
        config=ctx["config"],
        mc_client=create_mc_client(ctx),
        command_name="agents get_operation_logs",
    ).echo_operation_logs(**kwargs)


@agents.command(
    name="get-aws-upgrade-logs", help="Returns the upgrade logs for a remote AWS Agent."
)
@click.pass_obj
@click.option("--agent-id", help="UUID of Agent.", required=True)
@click.option(
    "--limit",
    help="Maximum number of log events to return, defaults to 100",
    type=click.INT,
    required=False,
)
@click.option(
    "--start-time",
    help="Optional start time, for example: 2023-12-02T13:40:25Z. Defaults to 12 hours ago.",
    required=False,
)
def get_aws_upgrade_logs(ctx, **kwargs):
    """
    Displays the upgrade logs for a remote AWS Agent.
    """
    AgentService(
        config=ctx["config"],
        mc_client=create_mc_client(ctx),
        command_name="agents get_aws_upgrade_logs",
    ).echo_aws_upgrade_logs(**kwargs)


@agents.command(
    name="get-aws-template",
    help="Displays the current CloudFormation template in use by an AWS Agent, in YAML format.",
)
@click.pass_obj
@click.option("--agent-id", help="UUID of Agent.", required=True)
def get_aws_template(ctx, **kwargs):
    """
    Displays the current CloudFormation template in use by an AWS Agent, in YAML format.
    """
    AgentService(
        config=ctx["config"],
        mc_client=create_mc_client(ctx),
        command_name="agents get_aws_template",
    ).echo_aws_template(**kwargs)


@agents.command(
    name="get-aws-template-parameters",
    help=(
        "Displays the current CloudFormation template parameters in use by an AWS Agent."
        " For Terraform it displays the current value for MemorySize and ConcurrentExecutions."
    ),
)
@click.pass_obj
@click.option("--agent-id", help="UUID of Agent.", required=True)
def get_aws_template_parameters(ctx, **kwargs):
    """
    Displays the current CloudFormation template parameters in use by an AWS Agent.
    """
    AgentService(
        config=ctx["config"],
        mc_client=create_mc_client(ctx),
        command_name="agents get_aws_template_parameters",
    ).echo_aws_template_parameters(**kwargs)
