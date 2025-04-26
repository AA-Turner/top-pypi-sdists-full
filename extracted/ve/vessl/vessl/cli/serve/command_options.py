"""
Common options for serving.
"""
import sys
from typing import List
from typing import Optional

import click
import inquirer

from openapi_client import (
    ResponseModelServiceInfo,
    ModelserviceModelServiceListResponse,
    ModelserviceModelServiceRevisionListResponse,
    ResponseModelServiceRevision,
    V1Autoscaling
)
from vessl import vessl_api
from vessl.util.common import parse_time_to_ago
from vessl.util.echo import print_info, print_error
from vessl.util.exception import VesslApiException
from vessl.util.prompt import prompt_confirm, prompt_text


class RevisionOption:
    def __init__(self, number: int, description: str) -> None:
        self.number = number
        self.description = description
    
    def __str__(self):
        return self.description

def prompt_revisions_list(service_name: str) -> int:
    try:
        revisions: ModelserviceModelServiceRevisionListResponse = vessl_api.model_service_revision_list_api(
            organization_name=vessl_api.organization.name,
            model_service_name=service_name
        )
    except VesslApiException as e:
        print(f"Error occurred while fetching revision list for organization {vessl_api.organization.name}.")
    
    if len(revisions.results) == 0:
        print("No revisions found. To create revision, use 'service create' command")
        sys.exit(1)

    revisionOptions = [
        RevisionOption(number=x.number, description=f'Revision #{x.number}: {x.status} (Created {parse_time_to_ago(x.created_dt)})')
        for x in revisions.results
    ]
    choice: int = inquirer.prompt(
        [
            inquirer.List(
                "revision",
                message="Select from revision list",
                choices=revisionOptions,
            )
        ],
        raise_keyboard_interrupt=True,
    ).get("revision")
    return choice.number

def prompt_services_list() -> str:
    try:
        services: ModelserviceModelServiceListResponse = vessl_api.model_service_list_api(vessl_api.organization.name)
    except VesslApiException as e:
        print(f"There was an error while fetching service list for organization {vessl_api.organization.name}.")
    
    if len(services.results) == 0:
        print("No services found")
        sys.exit(1)
    service_names = [x.name for x in services.results]
    service_name = inquirer.prompt(
        [
            inquirer.List(
                "service",
                message="Select from service list",
                choices=service_names,
            )
        ],
        raise_keyboard_interrupt=True,
    ).get("service")
    return service_name

def build_autoscaling_configs(conf: V1Autoscaling, min:int, max:int, target: int, metric:str) -> V1Autoscaling:
    if conf is None:
        conf = V1Autoscaling(
            min=1,
            max=1,
            metric="cpu",
            target=60,
        )

    if any(x is not None for x in [min, max, target, metric]):
        if min is not None:
            conf.min = min
        if max is not None:
            conf.max = max
        if target is not None:
            conf.target = conf
        if metric is not None:
            conf.metric = metric

    return conf

def revision_callback(
    ctx: click.Context, param: click.Parameter, revision_number: Optional[int]
) -> ResponseModelServiceRevision:
    
    if vessl_api.organization is None:
            vessl_api.set_organization()
    service: ResponseModelServiceInfo = ctx.serviceObj
    
    if revision_number is None:
        revision_number = prompt_revisions_list(service_name=service.name)
    
    try:
        revision: ResponseModelServiceRevision = vessl_api.model_service_revision_read_api(
            organization_name=vessl_api.organization.name,
            model_service_name=service.name,
            revision_number=revision_number
        )
    except VesslApiException as e:
        print(f"Error occurred while reading revision #{revision_number} of service {service.name}: {e.message}")
        sys.exit(1)

    return revision
    

def service_name_callback(
    ctx: click.Context, param: click.Parameter, service_name: Optional[str]
) -> ResponseModelServiceInfo:
    if vessl_api.organization is None:
        vessl_api.set_organization()

    if service_name is None:
        service_name = prompt_services_list()

    try:
        service: ResponseModelServiceInfo = vessl_api.model_service_read_api(
            service_name, vessl_api.organization.name
        )
    except VesslApiException as e:
        print(f"Invalid service of name {service_name}: {e.message}")
        sys.exit(1)
    
    ctx.serviceObj = service

    return service

def service_name_string_callback(
    ctx: click.Context, param: click.Parameter, service_name: Optional[str]
) -> str:
    if vessl_api.organization is None:
        vessl_api.set_organization()
    if service_name is None:
        options = []
        try:
            services: ModelserviceModelServiceListResponse = vessl_api.model_service_list_api(vessl_api.organization.name)
            options = [x.name for x in services.results]
        except VesslApiException as e:
            print(f"There was an error while fetching service list for organization {vessl_api.organization.name}.")
            print()
        options.append("Create new service")
        service_name = inquirer.prompt(
            [
                inquirer.List(
                    "service",
                    message="Create revision on existing service or new service",
                    choices=options
                )
            ],
            raise_keyboard_interrupt=True,
        ).get("service")
    if service_name == "Create new service":
        service_name = prompt_text("Enter new service name")
    return service_name

def multiple_rev_nums_callback(
    ctx: click.Context, param: click.Parameter, nums: Optional[List[int]]
) -> List[int]:
    if nums is None or len(nums) == 0:
        target_revision_numbers = []
        rev = prompt_revisions_list(service_name=ctx.serviceObj.name)
        target_revision_numbers.append(rev)
        while True:
            nth_revision = prompt_confirm("Do you want to send traffic to other revisions?")
            if nth_revision:
                revision_number = prompt_revisions_list(service_name=ctx.serviceObj.name)
                target_revision_numbers.append(revision_number)
            else:
                break
        ctx.targetNums = target_revision_numbers
        return target_revision_numbers
    else:
        return nums

def traffic_weights_callback(
    ctx: click.Context, param: click.Parameter, weights: Optional[List[int]]
) -> List[int]:
    if weights is None or len(weights) == 0:
        weights = []
        target_revision_numbers = ctx.targetNums
        target_revision_numbers.sort()
        for i, num in enumerate(target_revision_numbers):
            if i == len(target_revision_numbers) -1:
                remaining_weight = 100 - sum(weights)
                print_info(f"Last revision will take rest of the traffic.({remaining_weight}%)")
                weights.append(remaining_weight)
            else:
                w = prompt_text(f"How much traffic should revision {num} receive?(in percentage)")
                if not w.isdigit():
                    print_error("Please type an integer between 0 and 100.")
                    continue
                elif int(w) > 100 or int(w) < 0:
                    print_error("Please type an integer between 0 and 100.")
                    continue
                elif sum(weights) + int(w) > 100:
                    print_error("Total weight should not exceed 100.")
                    continue
                else:
                    weights.append(int(w))
        return weights
    else:
        return weights

service_name_option = click.option(
    "--service",
    type=click.STRING,
    callback=service_name_callback,
    help="Name of service.",
)

service_name_or_new_option = click.option(
    "-s",
    "--service-name",
    type=click.STRING,
    callback=service_name_string_callback,
    help="Name of service to create this revision inside. "
    "If such service does not exist, you will be be asked on whether to create one. "
    "If service name is not given, but YAML has a name field, "
    "then that name will be used.",
)

revision_option = click.option(
    "--number",
    "-n",
    type=int,
    callback=revision_callback,
    help="Number of revision."
)

detail_option = click.option(
    "-d",
    "--detail",
    type=click.BOOL,
    is_flag=True,
    default=False,
    help="show details about each revision in service.",
)

force_option = click.option(
    "--force",
    type=click.BOOL,
    is_flag=True,
    help="force to abort the existing rollout.",
)

no_prompt_option = click.option(
    "-y",
    "--no-prompt",
    type=click.BOOL,
    is_flag=True,
    help="do not ask anything while creating revision"
)

hub_key_option = click.option(
    "--from-hub",
    type=click.STRING,
    help="Model key to be found in VESSL Hub. This will automatically create service revision from YAML file.",
)

file_path_option = click.option(
    "-f",
    "--file",
    type=click.File("r"),
    help="Path to YAML file for service revision definition.",
)

service_launch_option = click.option(
    "-l",
    "--launch",
    type=click.BOOL,
    is_flag=True,
    help="Launch after creating revision.",
)

service_activate_option = click.option(
    "-a",
    "--set-current-active",
    type=click.BOOL,
    is_flag=True,
    help="Launch and send traffic to the created revision. If another live revision exists, replace the existing revision.",
)

serverless_service_option = click.option(
    "--serverless",
    type=click.BOOL,
    is_flag=True,
    help="If the service does not exist and should be created, this flag requires "
    "the service to be serverless. If not given, it defaults to provisioned. "
    "If this parameter is given, but the named service is not in serverless mode, "
    "an error is raised.",
)

nodeport_option = click.option(
    "--port",
    type=click.INT,
    required=False,
    help=(
        "When creating a new service, the cluster that custom endpoint type is NodePort requires "
        "a port number to be specified. This is the port number that the service will be exposed on."
    ),
)

subdomain_option = click.option(
    "--subdomain",
    type=click.STRING,
    required=False,
    help=(
        "When creating a new service, the cluster that custom endpoint type is Subdomain requires "
        "a subdomain to be specified. This is the subdomain that the service will be exposed on."
    ),
)

update_gateway_option = click.option(
    "--update-gateway/--no-update-gateway",
    "-g/-G",
    is_flag=True,
    default=False,
    help="Whether to update gateway so that it points to this revision.",
)

enable_gateway_if_off_option = click.option(
    "--enable-gateway-if-off/--no-enable-gateway-if-off",
    "-e/-E",
    is_flag=True,
    default=False,
    help="When updating gateway, whether to enable the gateway if it is currently off.",
)

update_gateway_weight_option = click.option(
    "--update-gateway-weight",
    type=click.INT,
    required=False,
    help=(
        "When updating gateway, the amount of traffic that should be "
        "directed to this revision (in percentage)."
    ),
)

update_gateway_port_option = click.option(
    "--update-gateway-port",
    type=click.INT,
    required=False,
    help=(
        "When updating gateway, the port to receive the traffic; "
        "this port must be defined in serving spec."
    ),
)

format_option = click.option(
    "--format",
    type=click.STRING,
    required=True,
    default="text",
    help=("Determines output format, supports text, json"),
)

autoscaling_min_option = click.option(
    "--min",
    required=False,
    type=int,
    help="Number of min replicas."
)

autoscaling_max_option = click.option(
    "--max",
    required=False,
    type=int,
    help="Number of max replicas."
)

autoscaling_target_option = click.option(
    "--target",
    required=False,
    type=int,
    help="Target resource utilization."
)

autoscaling_metric_option = click.option(
    "--metric",
    required=False,
    type=str,
    help="Metric for autoscaling. "
    "Supported autoscaling metrics: 'cpu', 'nvidia.com/gpu', 'memory'"
)

split_traffic_revs_option = click.option(
    "--number",
    "-n",
    required=False,
    type=int,
    multiple=True,
    callback=multiple_rev_nums_callback,
    help="Number of revisions to launch."
)

split_traffic_weights_option = click.option(
    "--weight",
    "-w",
    required=False,
    type=int,
    multiple=True,
    callback=traffic_weights_callback,
    help="Number of traffic weight for the revision",
)