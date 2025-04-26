"""
Serving command definition and delegation.
"""

import json
import sys
from typing import List, Optional, TextIO

import click

from openapi_client import SecretGenericSecretUpsertAPIInput
from openapi_client.models import (
    ModelserviceModelServiceRevisionListResponse,
    ResponseModelServiceInfo,
    ResponseModelServiceRevision,
    secret_generic_secret_upsert_api_input,
)
from vessl import vessl_api
from vessl.cli._base import VesslCommand, VesslGroup, vessl_argument, vessl_option
from vessl.cli.serve.util import (
    print_gateway,
    print_revision,
    print_revisions,
    print_service,
)
from vessl.enums import ModelServiceType
from vessl.serving import _read_service, terminate_revision
from vessl.util.deprecaate import deprecated
from vessl.util.echo import print_info
from vessl.util.exception import VesslApiException
from vessl.util.prompt import prompt_choices, prompt_text

from .command_options import (
    autoscaling_max_option,
    autoscaling_metric_option,
    autoscaling_min_option,
    autoscaling_target_option,
    detail_option,
    file_path_option,
    force_option,
    format_option,
    hub_key_option,
    no_prompt_option,
    revision_option,
    serverless_service_option,
    service_activate_option,
    service_launch_option,
    service_name_option,
    service_name_or_new_option,
    split_traffic_revs_option,
    split_traffic_weights_option,
    nodeport_option, subdomain_option,
)
from .service import (
    abort_update,
    create,
    create_yaml,
    list,
    scale,
    set_access_token,
    split,
)

cli = VesslGroup("service")
alias_cli = VesslGroup("serve", help="Deprecated: Please use 'service'")


@alias_cli.group("revision")
def cli_revision():
    """
    (Deprecated) Root command for revision-related commands.
    """
    pass


@alias_cli.group("gateway")
def cli_gateway():
    """
    (Deprecated) Root command for gateway-related commands.
    """
    pass


@cli.command("read", cls=VesslCommand)
@service_name_option
@detail_option
@format_option
def revision_show(service: ResponseModelServiceInfo, detail: bool, format: str):
    """
    Show current status and information about a service.
    """
    print_service(service=service)

    try:
        resp: ModelserviceModelServiceRevisionListResponse = vessl_api.model_service_revision_list_api(
        organization_name=vessl_api.organization.name,
        model_service_name=service.name,
        )
        revisions = resp.results
    except VesslApiException as e:
        print(f"Failed to read service (name: {service.name}): {e.message}")
        sys.exit(1)

    if detail:
        full_revisions = [
            vessl_api.model_service_revision_read_api(
            organization_name=vessl_api.organization.name,
            model_service_name=service.name,
            revision_number=r.number,
        ) for r in revisions
        ]

    if format == "text":
        print_revisions(revisions=full_revisions if detail else revisions, verbose=detail)
    if format == "json":
        print(json.dumps([r.to_dict() for r in revisions], default=str))
    if format == "yaml":
        print("\n\n".join([r.yaml_spec for r in revisions]))


@cli_revision.command("terminate", cls=VesslCommand, hidden=True)
@service_name_option
@revision_option
@deprecated(target_command="serve revision terminate", new_command="service terminate")
def revision_terminate_deprecated(service: ResponseModelServiceInfo, number: ResponseModelServiceRevision):
    revision_terminate(service=service, revision=number)


@cli.command("terminate", cls=VesslCommand)
@service_name_option
@revision_option
def serve_terminate(service: ResponseModelServiceInfo, number: ResponseModelServiceInfo):
    """
    Terminate specified revision.
    """
    revision_terminate(service=service, revision=number)


def revision_terminate(service: ResponseModelServiceInfo, revision: ResponseModelServiceRevision):
    if revision.status in ["failed", "stopped"]:
        print("Selected revision is already terminated.")
        return

    try:
        if service.type == ModelServiceType.SERVERLESS.value:
            vessl_api.model_service_serverless_terminate_api(
                model_service_name=service.name,
                organization_name=vessl_api.organization.name
            )
        else:
            terminate_revision(
                organization=vessl_api.organization.name,
                service_name=service.name,
                revision_number=revision.number,
            )
        print("Successfully terminated revision.")
    except VesslApiException as e:
        print(f"Failed to terminate revision #{revision.number} of service {service.name}: {e.message}")
        sys.exit(1)


@cli.command("list", cls=VesslCommand)
def service_list():
    """
    List services in current organization.
    """
    list()


@alias_cli.command("list", cls=VesslCommand, hidden=True)
def serve_list(): list()


@cli.command("abort-update", cls=VesslCommand)
@service_name_option
def service_abort_update(service: ResponseModelServiceInfo):
    """
    Abort the current revision update.
    """
    abort_update(service=service)


@alias_cli.command("abort-update", cls=VesslCommand, hidden=True)
@service_name_option
def serve_abort_update(service: ResponseModelServiceInfo):
    abort_update(service=service)


@cli.command("create", cls=VesslCommand)
@hub_key_option
@file_path_option
@no_prompt_option
@service_launch_option
@service_activate_option
@force_option
@service_name_or_new_option
@serverless_service_option
@nodeport_option
@subdomain_option
def revision_create_with_yaml(
        file: TextIO,
        no_prompt: bool,
        launch: bool,
        set_current_active: bool,
        force: bool,
        service_name: str,
        serverless: bool,
        from_hub: str,
        port: int,
        subdomain: str
):
    """
    Create a revision from a YAML file.

    The YAML file should contain the definition of the revision. See https://docs.vessl.ai/guides/serve/service-yaml

    Example:
    $ vessl service create -f service.yaml --set-current-active
    $ vessl service create --from-hub="vllm-service"
    """
    create(
        file=file, no_prompt=no_prompt, launch=launch,
        set_current_active=set_current_active, force=force,
        service_name=service_name, serverless=serverless,
        from_hub=from_hub, node_port=port, subdomain=subdomain
    )


@alias_cli.command("create", cls=VesslCommand, hidden=True)
@hub_key_option
@file_path_option
@no_prompt_option
@service_launch_option
@service_activate_option
@force_option
@service_name_or_new_option
@serverless_service_option
@nodeport_option
@subdomain_option
@deprecated(target_command="serve create", new_command="service create")
def revision_create_with_yaml(
        file: TextIO,
        no_prompt: bool,
        launch: bool,
        set_current_active: bool,
        force: bool,
        service_name: str,
        serverless: bool,
        from_hub: str,
        port: int,
        subdomain: str
):
    create(
        file=file, no_prompt=no_prompt, launch=launch,
        set_current_active=set_current_active, force=force,
        service_name=service_name, serverless=serverless,
        from_hub=from_hub, node_port=port, subdomain=subdomain
    )


@cli.command("scale", cls=VesslCommand)
@service_name_option
@revision_option
@autoscaling_min_option
@autoscaling_max_option
@autoscaling_target_option
@autoscaling_metric_option
def service_scale(
        service: ResponseModelServiceInfo,
        number: ResponseModelServiceRevision,
        min: Optional[int],
        max: Optional[int],
        target: Optional[int],
        metric: Optional[str],
):
    """
    Update revision's autoscaler config. Partial updates of autoscaling options (min, max, target, metric) allowed.
    If current revision does not have autoscaling set, it will default to (min=1, max=1, target=60, metric=cpu).

    Example:
    
    $ vessl service scale --service=my-service --number=1 --min=1
    $ vessl service scale --min=1 --max=5 --metric=nvidia.com/gpu
    """
    scale(service=service, number=number, min=min, max=max, target=target, metric=metric)


@cli.command("set-access-token", cls=VesslCommand)
@service_name_option
@click.option("--secret", type=str, help="Secret to set as access token.")
def service_set_access_token(
        service: ResponseModelServiceInfo,
        secret: Optional[str],
):
    """
    Set access token for the service.

    Example:

    $ vessl serve set-access-token --service=my-service
    $ vessl serve set-access-token --service=my-service --secret=my-secret
    """

    if not secret:
        opt = prompt_choices(
            "How do you want to set access token?",
            ["By linking an existing secret", "By creating a new secret and linking it"],
            "By linking an existing secret",
        )
        if opt == "By linking an existing secret":
            secrets = (vessl_api.
                       secret_list_api(organization_name=vessl_api.organization.name, kind="generic-secret").secrets)
            secret_name = prompt_choices(
                "Select a secret to link as the access token",
                [s.credentials_name for s in secrets],
            )
            secret_obj = next(s for s in secrets if s.credentials_name == secret_name)
        else:
            secret_name = prompt_text("Enter the name of the secret to create as the access token")
            secret_text = prompt_text("Enter the secret text")
            secret_obj = vessl_api.secret_generic_secret_upsert_api(
                organization_name=vessl_api.organization.name,
                secret_generic_secret_upsert_api_input=SecretGenericSecretUpsertAPIInput(
                    secret_name=secret_name,
                    value=secret_text,
                ),
            )
    else:
        secret_name = secret
        secrets = (vessl_api.
                   secret_list_api(organization_name=vessl_api.organization.name, kind="generic-secret").secrets)
        secret_obj = next(s for s in secrets if s.credentials_name == secret_name)

    set_access_token(service=service, secret=secret_obj)
    print_info(f"Secret {secret_obj.credentials_name} is now linked as an access token of service {service.name}.")
    print_info(f"Please include the following header in your requests: \"Authorization: Bearer (your secret goes here)\"")
    print_info(f"$ curl -XPOST -H 'Authorization: Bearer some-secret-text' https://your-service-endpoint.com")


@cli_revision.command("scale", cls=VesslCommand, hidden=True)
@service_name_option
@revision_option
@autoscaling_min_option
@autoscaling_max_option
@autoscaling_target_option
@autoscaling_metric_option
@deprecated(target_command="serve revision scale", new_command="service scale")
def serve_revision_scale(
        service: ResponseModelServiceInfo,
        number: ResponseModelServiceRevision,
        min: Optional[int],
        max: Optional[int],
        target: Optional[int],
        metric: Optional[str],
): scale(service=service, number=number, min=min, max=max, target=target, metric=metric)


@alias_cli.command("update", cls=VesslCommand, hidden=True)
@service_name_option
@split_traffic_revs_option
@split_traffic_weights_option
@click.option(
    "--interactive",
    is_flag=True,
    type=click.BOOL,
    help="Update service interactively"
)
@deprecated(target_command="serve update", new_command="service split-traffic")
def revision_update_deprecated(
    service: ResponseModelServiceInfo,
    number: List[int],
    weight: List[int],
    interactive: bool,
): 
    split(service=service, number=number, weight=weight, interactive=interactive)

@cli.command("split-traffic", cls=VesslCommand)
@service_name_option
@split_traffic_revs_option
@split_traffic_weights_option
def split_traffic(
        service: ResponseModelServiceInfo,
        number: List[int],
        weight: List[int],
):
    """
    Update revision's traffic weight.

    Example:
    
    $ vessl service split-traffic --service my-service -n 1 -w 100 
    $ vessl service split-traffic --service my-service -n 1 -w 60 -n 2 -w 40
    """
    split(service=service, number=number, weight=weight, interactive=True)


@cli.command("create-yaml", cls=VesslCommand, help="Create a service.yaml file with .vessl.model.lock file")
@vessl_argument("service_name", type=str)
@vessl_argument("message", type=str)
@vessl_option("-k", "--api-key", "use_api_key", type=bool, is_flag=True)
def service_create_yaml(
        service_name: str,
        message: str,
        use_api_key: bool = False,
): create_yaml(service_name=service_name, message=message, use_api_key=use_api_key)


@alias_cli.command("create-yaml", cls=VesslCommand, hidden=True)
@vessl_argument("service_name", type=str)
@vessl_argument("message", type=str)
@vessl_option("-k", "--api-key", "use_api_key", type=bool, is_flag=True)
def serve_create_yaml(
        service_name: str,
        message: str,
        use_api_key: bool = False,
): create_yaml(service_name=service_name, message=message, use_api_key=use_api_key)


@cli_gateway.command("show", cls=VesslCommand, hidden=True)
@service_name_option
@format_option
@deprecated(target_command="serve gateway show", new_command="service read")
def gateway_show(service: ResponseModelServiceInfo, format: str):
    """
    Show current status of the gateway of a service.
    """
    try:
        gateway = _read_service(service_name=service.name).gateway_config
    except VesslApiException as e:
        print(f"Failed to read gateway of service {service.name}: {e.message}")
        sys.exit(1)

    if format == "json":
        print(json.dumps(gateway.to_dict(), default=str))
    else:
        print_gateway(gateway)


@cli_revision.command("show", cls=VesslCommand, hidden=True)
@service_name_option
@revision_option
@format_option
@vessl_option("-o", "--output", "output", type=click.Path(), help="Output file path.")
@deprecated(target_command="serve revision show", new_command="service read")
def revision_show(service: ResponseModelServiceInfo, number: ResponseModelServiceRevision, format: str, output: str):
    """
    Show current status and information about a service revision.
    """
    revision = number
    result = ""
    if format == "text":
        print_revision(revision, verbose=True)
        return
    if format == "json":
        result = json.dumps(revision.to_dict(), default=str)
    if format == "yaml":
        result = revision.yaml_spec

    if output:
        with open(output, "w") as f:
            f.write(result)
    else:
        print_info(result)


@cli_revision.command("list", cls=VesslCommand)
@service_name_option
@format_option
@deprecated(target_command="serve revision list", new_command="service read")
def revision_list(service: ResponseModelServiceInfo, format: str):
    """
    List all revisions.
    """
    try:
        resp: ModelserviceModelServiceRevisionListResponse = vessl_api.model_service_revision_list_api(
        organization_name=vessl_api.organization.name,
        model_service_name=service.name,
        )
        revisions = resp.results
    except VesslApiException as e:
        print(f"Failed to list revisions of service {service.name}: {e.message}")
        sys.exit(1)

    if format == "json":
        print(json.dumps([r.to_dict() for r in revisions], default=str))
    if format == "yaml":
        print("\n\n".join([r.yaml_spec for r in revisions]))
    else:
        print(f"{len(revisions)} revision(s) found.\n")
        for i, revision in enumerate(revisions):
            if i > 0:
                print()
            print_revision(revision)


@cli.command("join", cls=VesslCommand, hidden=True)
def join():
    access_token = vessl_api.find_model_service_join_token()
    vessl_api.api_client.set_default_header("Authorization", f"Token {access_token}")
    resp = vessl_api.model_service_revision_workload_join_api()
    vessl_api.configure_jwt_access_token(resp.token)
