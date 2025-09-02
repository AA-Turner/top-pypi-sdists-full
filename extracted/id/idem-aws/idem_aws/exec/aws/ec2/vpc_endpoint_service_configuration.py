"""Exec module for managing EC2 VPC Endpoint Service Configurations."""
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["soft_fail"]

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    resource_id: str,
    filters: List[
        make_dataclass(
            "Filter",
            [
                ("Name", str, field(default=None)),
                ("Values", List[str], field(default=None)),
            ],
        )
    ] = None,
    name: str = None,
) -> Dict[str, Any]:
    """

    Describes the VPC endpoint service configurations in your account (your services).

    Args:
        resource_id(str): The ID of the service.

        filters(List[dict[str, Any]], Optional): The filters.

            * service-name - The name of the service.

            * service-id - The ID of the service.

            * service-state - The state of the service (Pending | Available | Deleting | Deleted | Failed).

            * supported-ip-address-types - The IP address type (ipv4 | ipv6).

            * tag:<key> - The key/value combination of a tag assigned to the resource. Use the tag key in the filter name and the tag value as the filter value.

            * tag-key - The key of a tag assigned to the resource. Use this filter to find all resources assigned a tag with a specific key, regardless of the tag value. Defaults to None.

            Filter names and Filter values are case-sensitive If you specify multiple values for a
            filter, the values are joined with an OR, and the request returns all results that match any of
            the specified values.

        name(str, Optional): Idem name of the resource. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            unmanaged_resource:
              exec.run:
                - path: aws.ec2.vpc_endpoint_service_configuration.get
                - kwargs:
                    resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.ec2.vpc_endpoint_service_configuration.get resource_id=service-id
    """

    result = dict(comment=[], ret=None, result=True)

    get = await hub.exec.boto3.client.ec2.describe_vpc_endpoint_service_configurations(
        ctx=ctx,
        **{
            "ServiceIds": [resource_id],
            "Filters": filters,
        },
    )

    # Case: Error
    if not get["result"]:
        if "NotFound" in str(get["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.ec2.vpc_endpoint_service_configuration",
                    name=resource_id,
                )
            )
            result["comment"].append(get["comment"])
            return result

        result["comment"].append(get["comment"])
        result["result"] = False
        return result

    # Case: Empty results
    if not get["ret"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.ec2.vpc_endpoint_service_configuration",
                name=resource_id,
            )
        )
        return result

    if len(get["ret"]["ServiceConfigurations"]) > 1:
        result["comment"].append(
            hub.tool.aws.comment_utils.find_more_than_one(
                resource_id=resource_id,
                resource_type="aws.ec2.vpc_endpoint_service_configuration",
            )
        )

    raw_resource = get["ret"]["ServiceConfigurations"][0]

    result[
        "ret"
    ] = await hub.tool.aws.ec2.vpc_endpoint_service_configuration.convert_raw_resource_to_present_async(
        ctx=ctx,
        resource_id=resource_id,
        raw_resource=raw_resource,
        idem_resource_name=name,
    )

    return result


async def list_(
    hub,
    ctx,
    service_ids: List[str] = None,
    filters: List[
        make_dataclass(
            "Filter",
            [
                ("Name", str, field(default=None)),
                ("Values", List[str], field(default=None)),
            ],
        )
    ] = None,
) -> Dict[str, Any]:
    """
    Describes the VPC endpoint service configurations in your account (your services).

    Args:
        service_ids(List[str], Optional): The IDs of the endpoint services. Defaults to None.

        filters(List[dict[str, Any]], Optional): The filters.

            * service-name - The name of the service.

            * service-id - The ID of the service.

            * service-state - The state of the service (Pending | Available | Deleting | Deleted | Failed).

            * supported-ip-address-types - The IP address type (ipv4 | ipv6).

            * tag:<key> - The key/value combination of a tag assigned to the resource. Use the tag key in the filter name and the tag value as the filter value.

            * tag-key - The key of a tag assigned to the resource. Use this filter to find all resources assigned a tag with a specific key, regardless of the tag value. Defaults to None.

            Filter names and Filter values are case-sensitive If you specify multiple values for a
            filter, the values are joined with an OR, and the request returns all results that match any of
            the specified values.

    Returns:
        Dict[str, Any]

    Examples:

        Resource State:

        .. code-block:: sls

            unmanaged_resources:
              exec.run:
                - path: aws.ec2.vpc_endpoint_service_configuration.list
                - kwargs:


        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.ec2.vpc_endpoint_service_configuration.list

    """

    result = dict(comment=[], ret=[], result=True)

    ret = await hub.exec.boto3.client.ec2.describe_vpc_endpoint_service_configurations(
        ctx=ctx, **{"ServiceIds": service_ids, "Filters": filters}
    )

    if not ret["result"]:
        result["comment"].append(ret["comment"])
        result["result"] = False
        return result

    if not ret["ret"].get("ServiceConfigurations"):
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.ec2.vpc_endpoint_service_configuration", name=None
            )
        )
        return result

    for resource in ret["ret"]["ServiceConfigurations"]:
        result["ret"].append(
            await hub.tool.aws.ec2.vpc_endpoint_service_configuration.convert_raw_resource_to_present_async(
                ctx=ctx,
                resource_id=resource.get("ServiceId"),
                raw_resource=resource,
                idem_resource_name=None,
            )
        )
    return result


async def create(
    hub,
    ctx,
    name: str = None,
    acceptance_required: bool = None,
    private_dns_name: str = None,
    network_load_balancer_arns: List[str] = None,
    gateway_load_balancer_arns: List[str] = None,
    supported_ip_address_types: List[str] = None,
    client_token: str = None,
    tags: Dict[str, Any] or List = None,
) -> Dict[str, Any]:
    """
    Creates a VPC endpoint service to which service consumers (Amazon Web Services accounts, users, and IAM roles)
    can connect.

    Before you create an endpoint service, you must create one of the following for your service:

        * A Network Load Balancer. Service consumers connect to your service using an interface endpoint.

        * A Gateway Load Balancer. Service consumers connect to your service using a Gateway Load Balancer endpoint.

    If you set the private DNS name, you must prove that you own the private DNS domain name.
    For more information, see the Amazon Web Services PrivateLink Guide.

    Args:
        name(str, Optional): Idem name of the resource. Defaults to None.

        acceptance_required(bool, Optional): Indicates whether requests from service consumers to create an endpoint to your service must be
            accepted manually. Defaults to None.

        private_dns_name(str, Optional): (Interface endpoint configuration) The private DNS name to assign to the VPC endpoint service. Defaults to None.

        network_load_balancer_arns(List[str], Optional): The Amazon Resource Names (ARNs) of the Network Load Balancers. Defaults to None.

        gateway_load_balancer_arns(List[str], Optional): The Amazon Resource Names (ARNs) of the Gateway Load Balancers. Defaults to None.

        supported_ip_address_types(List[str], Optional): The supported IP address types. The possible values are ipv4 and ipv6. Defaults to None.

        client_token(str, Optional): Unique, case-sensitive identifier that you provide to ensure the idempotency of the request. For
            more information, see How to ensure idempotency. Defaults to None.

        tags (Dict or List, Optional): Dict in the format of {tag-key: tag-value} or List of tags in the format of [{"Key": tag-key, "Value": tag-value}] to associate with the VPC. Each tag consists of a key name and an associated value. Defaults to None.

            * Key (str, Optional): The key of the tag. Constraints: Tag keys are case-sensitive and accept a maximum of 127 Unicode characters. May not begin with aws:.
            * Value(str, Optional): The value of the tag. Constraints: Tag values are case-sensitive and accept a maximum of 256 Unicode characters.

    Returns:
        Dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            unmanaged_resources:
              exec.run:
                - path: aws.ec2.vpc_endpoint_service_configuration.create
                - kwargs:

        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.ec2.vpc_endpoint_service_configuration.create
    """

    result = dict(comment=[], ret={}, result=True)

    tags = (
        hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)
        if isinstance(tags, List)
        else tags
    )

    if not network_load_balancer_arns and not gateway_load_balancer_arns:
        result["result"] = False
        result["comment"].append(
            f"Cannot create aws.ec2.vpc_endpoint_service_configuration as one of network_load_balancer_arn "
            f"or gateway_load_balancer_arn is required",
        )
        return result

    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "kwargs", "result") and v is not None
    }

    resource_to_raw_input_mapping = {
        "acceptance_required": "AcceptanceRequired",
        "private_dns_name": "PrivateDnsName",
        "network_load_balancer_arns": "NetworkLoadBalancerArns",
        "gateway_load_balancer_arns": "GatewayLoadBalancerArns",
        "supported_ip_address_types": "SupportedIpAddressTypes",
    }

    payload = {}
    for key, value in desired_state.items():
        if key in resource_to_raw_input_mapping.keys() and value is not None:
            payload[resource_to_raw_input_mapping[key]] = desired_state.get(key)

    if tags:
        payload["TagSpecifications"] = [
            {
                "ResourceType": "vpc-endpoint-service",
                "Tags": hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags),
            }
        ]

    ret = await hub.exec.boto3.client.ec2.create_vpc_endpoint_service_configuration(
        ctx, ClientToken=client_token or name, **payload
    )

    result["result"] = ret["result"]
    if not result["result"]:
        result["comment"].append(ret["comment"])
        return result

    result["comment"].append(
        f"Created aws.ec2.vpc_endpoint_service_configuration '{name}'",
    )

    raw_resource = ret["ret"].get("ServiceConfiguration", {})
    result["ret"]["resource_id"] = raw_resource.get("ServiceId")
    result["ret"]["name"] = name

    return result


async def update(
    hub,
    ctx,
    resource_id: str,
    name: str = None,
    private_dns_name: str = None,
    remove_private_dns_name: bool = None,
    acceptance_required: bool = None,
    add_network_load_balancer_arns: List[str] = None,
    remove_network_load_balancer_arns: List[str] = None,
    add_gateway_load_balancer_arns: List[str] = None,
    remove_gateway_load_balancer_arns: List[str] = None,
    add_supported_ip_address_types: List[str] = None,
    remove_supported_ip_address_types: List[str] = None,
    tags: Dict[str, Any] or List = None,
) -> Dict[str, Any]:
    """
    Modifies the attributes of your VPC endpoint service configuration. You can change the Network Load Balancers or
    Gateway Load Balancers for your service, and you can specify whether acceptance is required for requests to
    connect to your endpoint service through an interface VPC endpoint.

    If you set or modify the private DNS name, you must prove that you own the private DNS domain name.

    Args:
        resource_id(str): The ID of the service.

        name(str, Optional): Idem name of the resource. Defaults to None.

        private_dns_name(str, Optional): (Interface endpoint configuration) The private DNS name to assign to the endpoint service. Defaults to None.

        remove_private_dns_name(bool, Optional): (Interface endpoint configuration) Removes the private DNS name of the endpoint service. Defaults to None.

        acceptance_required(bool, Optional): Indicates whether requests to create an endpoint to your service must be accepted. Defaults to None.

        add_network_load_balancer_arns(List[str], Optional): The Amazon Resource Names (ARNs) of Network Load Balancers to add to your service configuration. Defaults to None.

        remove_network_load_balancer_arns(List[str], Optional): The Amazon Resource Names (ARNs) of Network Load Balancers to remove from your service
            configuration. Defaults to None.

        add_gateway_load_balancer_arns(List[str], Optional): The Amazon Resource Names (ARNs) of Gateway Load Balancers to add to your service configuration. Defaults to None.

        remove_gateway_load_balancer_arns(List[str], Optional): The Amazon Resource Names (ARNs) of Gateway Load Balancers to remove from your service
            configuration. Defaults to None.

        add_supported_ip_address_types(List[str], Optional): The IP address types to add to your service configuration. Defaults to None.

        remove_supported_ip_address_types(List[str], Optional): The IP address types to remove from your service configuration. Defaults to None.

        tags (Dict or List, Optional): Dict in the format of {tag-key: tag-value} or List of tags in the format of [{"Key": tag-key, "Value": tag-value}] to associate with the VPC. Each tag consists of a key name and an associated value. Defaults to None.

            * Key (str, Optional): The key of the tag. Constraints: Tag keys are case-sensitive and accept a maximum of 127 Unicode characters. May not begin with aws:.
            * Value(str, Optional): The value of the tag. Constraints: Tag values are case-sensitive and accept a maximum of 256 Unicode characters.

    Returns:
        Dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            unmanaged_resources:
              exec.run:
                - path: aws.ec2.vpc_endpoint_service_configuration.update
                - kwargs:
                    - resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.ec2.vpc_endpoint_service_configuration.update resource_id=value
    """

    result = dict(comment=[], ret={}, result=True)

    tags = (
        hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)
        if isinstance(tags, List)
        else tags
    )

    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "kwargs", "result") and v is not None
    }

    payload = {}

    resource_to_raw_input_mapping = {
        "private_dns_name": "PrivateDnsName",
        "remove_private_dns_name": "RemovePrivateDnsName",
        "acceptance_required": "AcceptanceRequired",
        "add_network_load_balancer_arns": "AddNetworkLoadBalancerArns",
        "remove_network_load_balancer_arns": "RemoveNetworkLoadBalancerArns",
        "add_gateway_load_balancer_arns": "AddGatewayLoadBalancerArns",
        "remove_gateway_load_balancer_arns": "RemoveGatewayLoadBalancerArns",
        "add_supported_ip_address_types": "AddSupportedIpAddressTypes",
        "remove_supported_ip_address_types": "RemoveSupportedIpAddressTypes",
    }

    for key, value in desired_state.items():
        if key in resource_to_raw_input_mapping.keys() and value is not None:
            payload[resource_to_raw_input_mapping[key]] = desired_state.get(key)

    if payload:
        payload["ServiceId"] = resource_id

        ret = await hub.exec.boto3.client.ec2.modify_vpc_endpoint_service_configuration(
            ctx, **payload
        )

        if not ret["result"] or not ret["ret"].get("Return"):
            result["result"] = False
            result["comment"].append(
                f"Could not update aws.ec2.vpc_endpoint_service_configuration '{name}'",
            )
            result["comment"].append(ret["comment"])
            return result

        result["comment"].append(
            f"Updated aws.ec2.vpc_endpoint_service_configuration '{name}'",
        )

        get_tags_ret = await hub.tool.aws.ec2.tag.get_tags_for_resource(
            ctx, resource_id=resource_id
        )

        if not tags:
            tags = {}

        if get_tags_ret["result"]:
            current_tags = get_tags_ret.get("ret", {})
            update_tags_ret = await hub.tool.aws.ec2.tag.update_tags(
                ctx, resource_id=resource_id, old_tags=current_tags, new_tags=tags
            )
            if not update_tags_ret["result"]:
                result["result"] = False
                result["comment"] += update_tags_ret["comment"]
                return result

        result["ret"]["resource_id"] = resource_id
        result["ret"]["name"] = name

    return result


async def delete(hub, ctx, resource_id: str, name: str = None) -> Dict[str, Any]:
    """
    Deletes the specified VPC endpoint service configurations. Before you can delete an endpoint service
    configuration, you must reject any Available or PendingAcceptance interface endpoint connections that are
    attached to the service.

    Args:
        resource_id(str): The ID of the services.

        name(str, Optional): Idem name of the resource. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            resource_is_absent:
              aws.ec2.vpc_endpoint_service_configuration.absent:
                - resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.ec2.vpc_endpoint_service_configuration.delete resource_id=value
    """

    result = dict(comment=[], ret=[], result=True)

    delete_ret = (
        await hub.exec.boto3.client.ec2.delete_vpc_endpoint_service_configurations(
            ctx, **{"ServiceIds": [resource_id]}
        )
    )

    result["result"] = delete_ret["result"]

    if not result["result"]:
        result["comment"] = delete_ret["comment"]
        result["result"] = False
        return result

    result["comment"] = hub.tool.aws.comment_utils.delete_comment(
        resource_type="aws.ec2.vpc_endpoint_service_configuration", name=name
    )

    return result
