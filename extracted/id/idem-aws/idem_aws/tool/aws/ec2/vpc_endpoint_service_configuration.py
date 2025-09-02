"""Utility functions for EC2 VPC Endpoint Service Configurations."""
from typing import Any
from typing import Dict


async def convert_raw_resource_to_present_async(
    hub, ctx, idem_resource_name: str, resource_id: str, raw_resource: dict
) -> Dict[str, Any]:
    r"""
    Convert raw resource of vpc_endpoint_service_configuration type into present format.
    """
    resource_translated = {"resource_id": resource_id}

    resource_parameters = {
        "ServiceType": "service_type",
        "ServiceId": "service_id",
        "ServiceName": "service_name",
        "ServiceState": "service_state",
        "AvailabilityZones": "availability_zones",
        "AcceptanceRequired": "acceptance_required",
        "ManagesVpcEndpoints": "manages_vpc_endpoints",
        "NetworkLoadBalancerArns": "network_load_balancer_arns",
        "GatewayLoadBalancerArns": "gateway_load_balancer_arns",
        "SupportedIpAddressTypes": "supported_ip_address_types",
        "BaseEndpointDnsNames": "base_endpoint_dns_names",
        "PrivateDnsName": "private_dns_name",
        "PrivateDnsNameConfiguration": "private_dns_name_configuration",
        "PayerResponsibility": "payer_responsibility",
    }

    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource and raw_resource.get(parameter_raw):
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    # The resource name could be given by the input or auto generated
    # Default idem creation adds name to tags with Name key (as specified in AWS console)
    resource_name = idem_resource_name or raw_resource.get("ServiceName")
    resource_translated["name"] = resource_name

    resource_translated["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
        raw_resource.get("Tags")
    )

    return resource_translated


def evaluate_update_desired_state(
    hub, ctx, current_state: dict, desired_state: dict
) -> Dict[str, Any]:
    r"""
    Evaluates desired state for updating vpc_endpoint_service_configuration
    """
    _update_added_removed_config(
        "network_load_balancer_arns", current_state, desired_state
    )
    _update_added_removed_config(
        "gateway_load_balancer_arns", current_state, desired_state
    )
    _update_added_removed_config(
        "supported_ip_address_types", current_state, desired_state
    )

    # Default to False. If desired state no longer wants to have private dns name, we can switch it to True.
    desired_state["remove_private_dns_name"] = False
    if (
        current_state.get("private_dns_name", None) is not None
        and desired_state.get("private_dns_name") is None
    ):
        desired_state["remove_private_dns_name"] = True

    return desired_state


def _update_added_removed_config(
    config_name: str, current_state: dict, desired_state: dict
):
    current = current_state.get(config_name, [])
    desired = desired_state.get(config_name, [])

    added = [item for item in desired if item not in current]
    removed = [item for item in current if item not in desired]

    if config_name in desired_state:
        # The request payload is different for modify
        del desired_state[config_name]

    if added:
        print(f"{config_name}: added: {added}")
        desired_state[f"add_{config_name}"] = added

    if removed:
        print(f"{config_name}: removed: {removed}")
        desired_state[f"remove_{config_name}"] = removed
