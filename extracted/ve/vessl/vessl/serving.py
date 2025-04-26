import sys
import time
import warnings
from typing import Dict, List

from openapi_client import (
    ModelServiceGatewayUpdateAPIInput,
    ModelserviceModelServiceListResponse,
    ModelserviceModelServiceRevisionListResponse,
    ModelServiceRevisionCreateFromYAMLAPIInput,
    ModelServiceRevisionUpdateAPIInput,
    ModelServiceRolloutCreateAPIInput,
)
from openapi_client import OrmModelServiceGatewayTrafficSplitEntry as TrafficSplitEntry
from openapi_client import (
    ResponseModelServiceGatewayInfo,
    ResponseModelServiceInfo,
    ResponseModelServiceRevision,
    ResponseModelServiceRolloutInfo,
    ResponseSimpleModelServiceRevision,
    V1Autoscaling,
    V1RunArgument
)
from openapi_client.models.model_service_revision_create_from_yamlv2_api_input import (
    ModelServiceRevisionCreateFromYAMLV2APIInput,
)
from vessl import vessl_api
from vessl.util.deprecaate import deprecated
from vessl.util.echo import print_warning, print_info, print_success, print_error
from vessl.util.exception import VesslApiException


def list_services(organization: str) -> ModelserviceModelServiceListResponse:
    """Get a list of all services in an organization

    Args:
        organization(str): The name of the organization.

    Example:
        ```python
        vessl.list_services(organization="my-org")
        ```
    """
    return vessl_api.model_service_list_api(organization_name=organization)

def _read_service(service_name: str) -> ResponseModelServiceInfo:
    """Get a service from a service name.

    Args:
        service_name(str): The name of the service.

    Example:
        ```python
        vessl.read_service(service_name="my-service")
        ```
    """
    return vessl_api.model_service_read_api(
        organization_name=vessl_api.organization.name, model_service_name=service_name
        )

def create_revision_from_yaml(
    organization: str, yaml_body: str
) -> ResponseModelServiceRevision:
    """Create a new revision of service from a YAML file.

    The name of the service should be provided in the YAML in `name:`.

    Args:
        organization (str): The name of the organization.
        yaml_body (str): The YAML body of the service revision.
            It should not be a structured (i.e. list, dict, ...) object, but
            a raw string in YAML.

    Example:
        ```python
        vessl.create_revision_from_yaml(
            organization="my-org",
            yaml_body=yaml_body)
        ```
    """
    payload = ModelServiceRevisionCreateFromYAMLAPIInput(yaml_body)

    return vessl_api.model_service_revision_create_from_yamlapi(
        organization_name=organization,
        model_service_revision_create_from_yamlapi_input=payload,
    )

def create_revision_from_yaml_v2(
    organization: str, service_name: str, yaml_body: str, serverless: bool, arguments: V1RunArgument
) -> ResponseModelServiceRevision:
    """Create a new revision of service from a YAML file.

    Args:
        organization (str): The name of the organization.
        service_name (str): The name of the service to create this revision in.
        yaml_body (str): The YAML body of the service revision.
            It should not be a structured (i.e. list, dict, ...) object, but
            a raw string in YAML.
        serverless  (bool): Whether this revision is in serverless mode.
        arguments (V1RunArgument): User inputs received from prompts.

    Example:
        ```python
        vessl.create_revision_from_yaml(
            organization="my-org",
            service_name="my-svc",
            yaml_body=yaml_body)
        ```
    """
    payload = ModelServiceRevisionCreateFromYAMLV2APIInput(
        serverless=serverless, yaml_spec=yaml_body, arguments=arguments)

    return vessl_api.model_service_revision_create_from_yamlv2_api(
        organization_name=organization,
        model_service_name=service_name,
        model_service_revision_create_from_yamlv2_api_input=payload,
    )


def launch_revision(organization: str, service_name: str, revision_number: int):
    """Launch a service revision from a service name and revision number.

    Args:
        organization(str): The name of the organization.
        service_name(str): The name of the modelservice.
        revision_number(int): The revision number of the modelservice.

    Example:
        ```python
        vessl.launch_revision(
            organization="my-org",
            service_name="my-service",
            revision_number=1)
        ```
    """
    vessl_api.model_service_revision_launch_api(
        organization_name=organization,
        model_service_name=service_name,
        revision_number=revision_number,
    )

@deprecated(target_command="read_revision", new_command="read_service")
def read_revision(
    organization: str, service_name: str, revision_number: int
) -> ResponseModelServiceRevision:
    """Get a service revision from a service name and revision number.

    Args:
        organization(str): The name of the organization.
        service_name(str): The name of the service.
        revision_number(int): The revision number of the service.

    Example:
        ```python
        vessl.read_revision(
            organization="my-org",
            service_name="my-service",
            revision_number=1)
        ```
    """
    return vessl_api.model_service_revision_read_api(
        organization_name=organization,
        model_service_name=service_name,
        revision_number=revision_number,
    )

def terminate_revision(organization: str, service_name: str, revision_number: int):
    """
    Terminate a service revision from a service name and revision number.

    Args:
        organization(str): The name of the organization.
        service_name(str): The name of the service.
        revision_number(int): The revision number of the service.

    Example:
        ```python
        vessl.terminate_revision(
            organization="my-org",
            service_name="my-service",
            revision_number=1)
        ```
    """
    return vessl_api.model_service_revision_terminate_api(
        organization_name=organization,
        model_service_name=service_name,
        revision_number=revision_number,
    )


def update_revision_autoscaler_config(
    organization: str,
    service_name: str,
    revision_number: int,
    autoscaling: V1Autoscaling,
):
    """
    Update the autoscaler config of a service revision from a service name and revision number.

    Args:
        organization(str): The name of the organization.
        service_name(str): The name of the service.
        revision_number(int): The revision number of the service.
        autoscaling(V1Autoscaling): The autoscaler config of the service(servev1/Autoscaling).

    Example:
        ```python
        vessl.update_revision_autoscaler_config(
            organization="my-org",
            service_name="my-service",
            revision_number=1,
            auto_scaler_config=V1Autoscaling(
                min=1,
                max=2,
                metric="cpu",
                target=80,
            ))
        ```
    """
    return vessl_api.model_service_revision_update_api(
        organization_name=organization,
        model_service_name=service_name,
        revision_number=revision_number,
        model_service_revision_update_api_input=ModelServiceRevisionUpdateAPIInput(
            autoscaling=autoscaling,
        ),
    )

def update_revision_autoscaling_v2(
    organization: str,
    service_name: str,
    revision_number: int,
    autoscaling: V1Autoscaling,
):
    """
    Update the autoscaler config of a serving revision from a serving name and revision number.

    Args:
        organization(str): The name of the organization.
        service_name(str): The name of the serving.
        revision_number(int): The revision number of the serving.
        autoscaling(V1Autoscaling): The autoscaler config of the serving.

    Example:
        ```python
        vessl.update_revision_autoscaler_config(
            organization="my-org",
            service_name="my-service",
            revision_number=1,
            autoscaling=V1Autoscaling(
                min=1,
                max=2,
                metric=cpu, [cpu,memory,nvidia.com/gpu]
                target=60
            ))
        ```
    """
    return vessl_api.model_service_revision_update_api(
        organization_name=organization,
        model_service_name=service_name,
        revision_number=revision_number,
        model_service_revision_update_api_input=ModelServiceRevisionUpdateAPIInput(
            autoscaling=autoscaling,
        ),
    )

def read_service(service_name: str):
    """
    Reads a service, including information about its revisions and gateway configurations.

    Args:
        service_name(str): The name of the service.

    Example:
        ```python
        vessl.read_service(service_name="my-service")
        ```
    """
    service_info = vessl_api.model_service_read_api(
        organization_name=vessl_api.organization.name,
        model_service_name=service_name
    )
    revision_info = vessl_api.model_service_revision_list_api(
        organization_name=vessl_api.organization.name,
        model_service_name=service_name
    )
    result = {
        "model_service": service_info,
        "revisions": revision_info.results
    }
    return result


@deprecated(target_command="list_revisions", new_command="read_service")
def list_revisions(
    organization: str, service_name: str
) -> List[ResponseSimpleModelServiceRevision]:
    """Get a list of all revisions of a service.

    Args:
        organization(str): The name of the organization.
        service_name(str): The name of the service.

    Examples:
        ```python
        vessl.list_revisions(
            organization="my-org",
            service_name="my-service")
        ```
    """
    resp: ModelserviceModelServiceRevisionListResponse = vessl_api.model_service_revision_list_api(
        organization_name=organization,
        model_service_name=service_name,
    )
    return resp.results

@deprecated(target_command="read_gateway", new_command="read_service")
def read_gateway(organization: str, service_name: str) -> ResponseModelServiceGatewayInfo:
    """Get the gateway of a service.

    Args:
        organization(str): The name of the organization.
        service_name(str): The name of the service.

    Examples:
        ```python
        vessl.read_gateway(
            organization="my-org",
            service_name="my-service")
        ```
    """
    model_service: ResponseModelServiceInfo = vessl_api.model_service_read_api(
        model_service_name=service_name,
        organization_name=organization,
    )
    return model_service.gateway_config


def update_gateway(
    organization: str, service_name: str, gateway: ModelServiceGatewayUpdateAPIInput
) -> ResponseModelServiceGatewayInfo:
    """Update the gateway of a service.

    Args:
        organization(str): The name of the organization.
        service_name(str): The name of the service.
        gateway(ModelServiceGatewayUpdateAPIInput): The gateway of the service.

    Examples:
        ```python
        from openapi_client import ModelServiceGatewayUpdateAPIInput
        from openapi_client import OrmModelServiceGatewayTrafficSplitEntry

        gateway = ModelServiceGatewayUpdateAPIInput(
            enabled=True,
            ingress_host="my-endpoint",
            traffic_split=[
                OrmModelServiceGatewayTrafficSplitEntry(
                    revision_number=1,
                    port=2222,
                    traffic_weight=100,
                )
            ],
        )

        vessl.update_gateway(
            organization="my-org",
            service_name="my-service",
            gateway=gateway)
        ```
    """
    return vessl_api.model_service_gateway_update_api(
        model_service_name=service_name,
        organization_name=organization,
        model_service_gateway_update_api_input=gateway,
    )


def _get_updated_traffic_split_rule(
    rules_current: List[TrafficSplitEntry], revision_number: int, weight: int
) -> List[TrafficSplitEntry]:
    """
    Combines the previous traffic split rule with new rule.
    When filling the remaining weight, this function uses the one with higher revision number.

    For example, with the current rule of:
    - revision #2 (port 2222) 70%
    - revision #3 (port 3333) 30%

    with a call to this function with:
    - revision #4 (port 4444) 50%

    yields a new rule of:
    - revision #4 (port 4444) 50%
    - revision #3 (port 3333) 30%
    - revision #2 (port 2222) 20%

    Revision #3 takes priority over #2, because it has the higher number (3 > 2).
    """
    # Sort from latest revision (with highest number) to oldest
    rules_current = sorted(rules_current, key=lambda x: x.revision_number, reverse=True)

    rules_new: List[TrafficSplitEntry] = [
        TrafficSplitEntry(revision_number=revision_number, traffic_weight=weight)
    ]

    weight_remaining = 100 - weight

    # Iterate through current traffic rules and add them if possible
    for rule in rules_current:
        if weight_remaining <= 0:
            break
        new_weight = min(weight_remaining, rule.traffic_weight)
        rules_new.append(
            TrafficSplitEntry(
                revision_number=rule.revision_number, traffic_weight=new_weight
            )
        )
        weight_remaining -= new_weight
        if weight_remaining <= 0:
            break

    if weight_remaining > 0:
        # This can happen if rules_current's weight do not sum up to 100
        # (this is possible for disabled gateways).
        # Handle this case safely by delegating all remaining weights to our target rule.
        rules_new[0].traffic_weight += weight_remaining

    return rules_new


def update_gateway_for_revision(
    organization: str,
    service_name: str,
    revision_number: int,
    weight: int,
) -> ResponseModelServiceGatewayInfo:
    """Update the current gateway of a service for a specific revision.

    Args:
        organization(str): The name of the organization.
        service_name(str): The name of the service.
        revision_number(int): The revision number of the service.
        weight(int): The weight of the traffic will be distributed to revision_number.

    Examples:
        ```python
        vessl.update_gateway_for_revision(
            organization="my-org",
            service_name="my-service",
            revision_number=1,
            weight=100)
        ```
    """
    gateway_current = _read_service(service_name=service_name).gateway_config
    rules_new = _get_updated_traffic_split_rule(
        rules_current=gateway_current.rules or [],
        revision_number=revision_number,
        weight=weight,
    )

    gateway_updated = vessl_api.model_service_gateway_update_api(
        organization_name=organization,
        model_service_name=service_name,
        model_service_gateway_update_api_input=ModelServiceGatewayUpdateAPIInput(
            enabled=True,
            ingress_host=gateway_current.endpoint,
            ingress_class=gateway_current.ingress_class,
            annotations=gateway_current.annotations,
            traffic_split=rules_new,
        ),
    )
    return gateway_updated


def create_active_revision_replacement_rollout(
    organization: str, model_service_name: str, desired_active_revisions_to_weight_map: Dict[int, int],
) -> ResponseModelServiceRolloutInfo:
    """
    Create a rollout to replace the active revisions of a service with the desired revisions.
    
    Args:
        organization(str): The name of the organization.
        model_service_name(str): The name of the model service.
        desired_active_revisions_to_weight_map(dict[int, int]): A dictionary of revision numbers and their desired
        traffic weight.
    """

    revisions = []
    gateway_targets = []
    for number, weight in desired_active_revisions_to_weight_map.items():
        revisions.append({
            'type': 'number',
            'number': number,
        })
        gateway_targets.append({
            'revision': {
                'type': 'number',
                'number': number,
            },
            'traffic_weight': weight,
        })

    rollout_input = ModelServiceRolloutCreateAPIInput(
        message=f'{vessl_api.user.email} initiated a rollout',
        rollout_spec={
            'steps': [
                {
                    'step_type': 'ensure_revisions_up_and_running',
                    'ensure_revisions_up_and_running': {
                        'revisions': revisions
                    },
                },
                {
                    'step_type': 'update_endpoint',
                    'update_endpoint': {
                        'annotations': {},
                        'targets': gateway_targets,
                    },
                },
                {
                    'step_type': 'terminate_revisions',
                    'terminate_revisions': {
                        'excluded_revisions': revisions,
                    },
                },
            ],
        },
    )
    return vessl_api.model_service_rollout_create_api(
        organization_name=organization,
        model_service_name=model_service_name,
        model_service_rollout_create_api_input=rollout_input
    )


def update_model_service(service: ResponseModelServiceInfo, number: List[int], weight: List[int]):
    if len(number) == 0 or len(weight) == 0:
        print_error("Please enter target revisions' number and traffic weight.")
        return
    if len(number) != len(weight) and len(number) != 1:
        print_error("Please enter traffic weight for each revision or specify only one revision.")
        return
    if len(weight) != 0 and sum(weight) != 100:
        print_error("Sum of each revision's traffic weight should be exactly 100.")
        return

    if len(number) == 1 and len(weight) == 0:
        weight = [100]

    weight_map = dict()
    for revision_numer, traffic_weight in zip(number, weight):
        weight_map[revision_numer] = traffic_weight

    try:
        create_active_revision_replacement_rollout(
            organization=vessl_api.organization.name,
            model_service_name=service.name,
            desired_active_revisions_to_weight_map=weight_map,
        )
        print_success(f"Successfully requested updating service {service.name}.\n")
        return
    except VesslApiException as e:
        print_error(f"Failed to update service {service.name}: {e.message}")
        sys.exit(1)

def read_rollout(service_name: str, rollout_num: int) -> ResponseModelServiceRolloutInfo:
    return vessl_api.model_service_rollout_read_api(
        organization_name=vessl_api.organization.name,
        model_service_name=service_name,
        rollout_number=rollout_num,
    )

def _request_abort_rollout(service: ResponseModelServiceInfo):
    resp = vessl_api.model_service_rollout_abort_api(
        organization_name=vessl_api.organization.name,
        model_service_name=service.name,
    )
    return resp


def abort_in_progress_rollout(service: ResponseModelServiceInfo) -> bool:
    resp = _request_abort_rollout(service)
    if resp.rollback_requested:
        print_success("Current update aborted. Rollback is requested.\n")
        return True
    else:
        print_warning("Current update aborted.")
        print_warning("Could not determine the original status. Rollback is not requested.\n")
        print_warning(f"Please check the status of the service and the gateway at: {WEB_HOST}/{vessl_api.organization.name}/services/{service.name}\n")
        return False

def abort_in_progress_rollout_by_name(service_name: str) -> bool:
    service = _read_service(service_name)
    return abort_in_progress_rollout(service)

def trigger_abort_and_wait(service_name: str,  max_timeout_sec: int = 8*60, print_output: bool = False) -> bool:
    '''
    Trigger the abort of the current rollout and wait for the rollout to be aborted.

    Args:
        service_name(str): The name of the service.
        max_timeout_sec(int): The maximum time to wait for the rollout to be aborted.
        print_output(bool): Whether to print the output.

    Returns:
        bool: True if the rollout is successfully aborted, False otherwise.

    Example:
        ```python
        trigger_abort_and_wait(service_name="my-service", max_timeout_sec=480, print_output=True)
        ```

    '''

    print_info_or_skip = print_info if print_output else lambda x: None
    print_error_or_skip = print_error if print_output else lambda x: None
    try:
        service = _read_service(service_name)
        resp = _request_abort_rollout(service)
        print_info_or_skip("Aborting the existing rollout...")
        rollout_abort_timeout = max_timeout_sec
        while rollout_abort_timeout > 0:
            aborting_rollout = read_rollout(service_name, resp.target_rollout_number)
            if aborting_rollout.status != "rolling_out" and aborting_rollout.status != "ready":
                print_info_or_skip("Successfully aborted the rollout.")
                break
            rollout_abort_timeout -= 5
            time.sleep(5)
            print_info_or_skip(f">> Waiting for {max_timeout_sec - rollout_abort_timeout} seconds...")
        if rollout_abort_timeout <= 0:
            print_error_or_skip("Rollout abort timeout.")
            return False
        return True
    except VesslApiException as e:
        print_error_or_skip(f"Failed to abort rollout: {e.message}")
        return False

def _wait_for_revision_to_launch(service_name: str, revision_number: int, max_timeout_sec: int = 8*60, print_output: bool = False) -> bool:
    print_info_or_skip = print_info if print_output else lambda x: None
    print_error_or_skip = print_error if print_output else lambda x: None

    revision_launch_timeout = max_timeout_sec
    print_info_or_skip(f">> Wait for the revision to be ready...")
    while revision_launch_timeout > 0:
        revision = vessl_api.model_service_revision_read_api(
        organization_name=vessl_api.organization.name,
        model_service_name=service_name,
        revision_number=revision_number,
        )
        if revision.status == "running":
            print_info_or_skip(f"Successfully created revision in service {service_name}.\n")
            break
        revision_launch_timeout -= 5
        time.sleep(5)
        print_info_or_skip(f">> Waiting for {max_timeout_sec - revision_launch_timeout} seconds...")
    if revision_launch_timeout <= 0:
        print_error_or_skip("Revision launch timeout.")
        return False

    return True

def _wait_for_gateway_enabled(gateway: ResponseModelServiceGatewayInfo, service_name: str, max_timeout_sec: int = 8*60, print_output: bool = False) -> bool:
    print_info_or_skip = print_info if print_output else lambda x: None
    print_error_or_skip = print_error if print_output else lambda x: None
    def _check_gateway_enabled(gateway):
        return gateway.enabled and gateway.status == "success" and gateway.endpoint is not None
    if not _check_gateway_enabled(gateway):
        print_info_or_skip("Endpoint update in progress. Please wait a moment.")
        gateway_update_timeout = max_timeout_sec
        print_info_or_skip(f">> Wait for the endpoint to be ready...")
        while gateway_update_timeout > 0:
            gateway = _read_service(service_name=service_name).gateway_config
            if _check_gateway_enabled(gateway):
                break
            gateway_update_timeout -= 5
            time.sleep(5)
            print_info_or_skip(f">> Waiting for {max_timeout_sec - gateway_update_timeout} seconds...")
    
        if gateway_update_timeout <= 0:
            print_error_or_skip("Endpoint update timeout. Please check the status of the endpoint.")
            return False
    return True

def get_recent_rollout(service_name: str) -> ResponseModelServiceRolloutInfo:
    resp = vessl_api.model_service_rollout_list_api(
            organization_name=vessl_api.organization.name,
            model_service_name=service_name,
        )
    recent_rollout = resp.rollouts[0] if resp.rollouts else None
    return recent_rollout
