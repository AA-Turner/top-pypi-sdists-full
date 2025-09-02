import base64
from collections import OrderedDict
from datetime import timezone
from typing import Any
from typing import Dict

"""
Util functions to convert raw resource state from AWS EC2 to present input format.
"""
UTC_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


async def convert_raw_vpc_to_present_async(
    hub, ctx, raw_resource: Dict[str, Any], idem_resource_name: str = None
) -> Dict[str, Any]:
    resource_id = raw_resource.get("VpcId")
    resource_parameters = OrderedDict(
        {
            "InstanceTenancy": "instance_tenancy",
        }
    )
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)
    if raw_resource.get("Tags") is not None:
        resource_translated["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            raw_resource.get("Tags")
        )
    # The following code block is to make sure to only output the associated/associating cidr blocks and
    # dis-regard the disassociated cidr blocks.
    if raw_resource.get("CidrBlockAssociationSet"):
        ipv4_cidr_block_association_set = []
        for cidr_block in raw_resource.get("CidrBlockAssociationSet"):
            if cidr_block.get("CidrBlockState").get("State") in [
                "associated",
                "associating",
            ]:
                ipv4_cidr_block_association_set.append(cidr_block)
        resource_translated[
            "cidr_block_association_set"
        ] = ipv4_cidr_block_association_set
    if resource_id:
        enableDnsHostnames = await hub.exec.boto3.client.ec2.describe_vpc_attribute(
            ctx, Attribute="enableDnsHostnames", VpcId=resource_id
        )
        if enableDnsHostnames and enableDnsHostnames["result"] is True:
            resource_translated["enable_dns_hostnames"] = enableDnsHostnames["ret"][
                "EnableDnsHostnames"
            ]["Value"]
        else:
            # TODO - Need to handle the error efficiently.
            hub.log.warning(
                f"Failed on fetching enableDnsHostnames on vpc {resource_id} with error {enableDnsHostnames['comment']}."
            )
        enableDnsSupport = await hub.exec.boto3.client.ec2.describe_vpc_attribute(
            ctx, Attribute="enableDnsSupport", VpcId=resource_id
        )
        if enableDnsSupport and enableDnsSupport["result"] is True:
            resource_translated["enable_dns_support"] = enableDnsSupport["ret"][
                "EnableDnsSupport"
            ]["Value"]
        else:
            # TODO - Need to handle the error efficiently.
            hub.log.warning(
                f"Failed on fetching enableDnsSupport on vpc {resource_id} with error {enableDnsSupport['comment']}."
            )
    if raw_resource.get("Ipv6CidrBlockAssociationSet"):
        ipv6_cidr_block_association_set = []
        for cidr_block in raw_resource.get("Ipv6CidrBlockAssociationSet"):
            if cidr_block.get("Ipv6CidrBlockState").get("State") in [
                "associated",
                "associating",
            ]:
                if "NetworkBorderGroup" in cidr_block:
                    # Translate describe output to the correct present input format
                    ipv6_cidr_block_network_border_group = cidr_block.pop(
                        "NetworkBorderGroup"
                    )
                    cidr_block[
                        "Ipv6CidrBlockNetworkBorderGroup"
                    ] = ipv6_cidr_block_network_border_group
                ipv6_cidr_block_association_set.append(cidr_block)
        resource_translated[
            "ipv6_cidr_block_association_set"
        ] = ipv6_cidr_block_association_set
    return resource_translated


def convert_raw_subnet_to_present(
    hub, raw_resource: Dict[str, Any], idem_resource_name: str = None
) -> Dict[str, Any]:
    resource_id = raw_resource.get("SubnetId")
    resource_parameters = OrderedDict(
        {
            "VpcId": "vpc_id",
            "CidrBlock": "cidr_block",
            "AvailabilityZone": "availability_zone",
            "OutpostArn": "outpost_arn",
            "MapPublicIpOnLaunch": "map_public_ip_on_launch",
            "AssignIpv6AddressOnCreation": "assign_ipv6_address_on_creation",
            "MapCustomerOwnedIpOnLaunch": "map_customer_owned_ip_on_launch",
            "CustomerOwnedIpv4Pool": "customer_owned_ipv4_pool",
            "EnableDns64": "enable_dns_64",
            "PrivateDnsNameOptionsOnLaunch": "private_dns_name_options_on_launch",
            "EnableLniAtDeviceIndex": "enable_lni_at_device_index",
        }
    )
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)
    if "Tags" in raw_resource:
        resource_translated["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            raw_resource.get("Tags")
        )
    if (not raw_resource.get("AvailabilityZone")) and raw_resource.get(
        "AvailabilityZoneId"
    ):
        # Only populate availability_zone_id field when availability_zone doesn't exist
        resource_translated["availability_zone_id"] = raw_resource.get(
            "AvailabilityZoneId"
        )
    if raw_resource.get("Ipv6CidrBlockAssociationSet"):
        ipv6_cidr_block_association_set = (
            hub.tool.aws.network_utils.get_associated_ipv6_cidr_blocks(
                raw_resource.get("Ipv6CidrBlockAssociationSet")
            )
        )
        # We should only output the associated ipv6 cidr block, and theoretically there should only be one,
        # since AWS only supports one ipv6 cidr block association on a subnet
        if ipv6_cidr_block_association_set:
            resource_translated["ipv6_cidr_block"] = ipv6_cidr_block_association_set[
                0
            ].get("Ipv6CidrBlock")
    return resource_translated


def convert_raw_sg_rule_to_present(
    hub, raw_resource: Dict[str, Any], idem_resource_name: str = None
) -> Dict[str, Any]:
    resource_id = raw_resource.get("SecurityGroupRuleId")
    resource_parameters = OrderedDict(
        {
            "GroupId": "group_id",
            "IsEgress": "is_egress",
            "IpProtocol": "ip_protocol",
            "FromPort": "from_port",
            "ToPort": "to_port",
            "CidrIpv4": "cidr_ipv4",
            "CidrIpv6": "cidr_ipv6",
            "PrefixListId": "prefix_list_id",
            "Description": "description",
            "ReferencedGroupInfo": "referenced_group_info",
        }
    )
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)
    if "Tags" in raw_resource:
        resource_translated["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            raw_resource.get("Tags")
        )
    return resource_translated


def convert_raw_transit_gateway_to_present(
    hub, raw_resource: Dict[str, Any], idem_resource_name: str = None
) -> Dict[str, Any]:
    resource_id = raw_resource.get("TransitGatewayId")
    resource_parameters = OrderedDict(
        {
            "State": "state",
            "Description": "description",
            "Options": "options",
        }
    )
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)
    if "Tags" in raw_resource:
        resource_translated["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            raw_resource.get("Tags")
        )
    return resource_translated


def convert_raw_key_pair_to_present(
    hub, raw_resource: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Convert the aws key pair response to a common format

    @param raw_resource: describe key pair response
    @param hub: required for functions in hub

    @return:
        A dictionary key pair's properties
    """
    if not raw_resource:
        return {}

    resource_parameters = OrderedDict(
        {
            "KeyPairId": "resource_id",
            "PublicKey": "public_key",
        }
    )
    resource_translated = {"name": raw_resource.get("KeyName")}
    for raw_parameter, present_parameter in resource_parameters.items():
        if raw_resource.get(raw_parameter):
            resource_translated[present_parameter] = raw_resource.get(raw_parameter)
    if raw_resource.get("Tags") is not None:
        resource_translated["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            raw_resource.get("Tags")
        )
    return resource_translated


def convert_raw_placement_group_to_present(
    hub, raw_resource: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Convert the aws placement_group response to a common format

    Args:
        hub: required for functions in hub
        raw_resource: The aws response to convert

    Returns: Valid idem state for placement_group of type Dict['string', Any]
    """
    if not raw_resource:
        return {}

    resource_parameters = OrderedDict(
        {
            "State": "state",
            "Strategy": "strategy",
            "PartitionCount": "partition_count",
            "GroupId": "group_id",
            "GroupName": "group_name",
            "SpreadLevel": "spread_level",
        }
    )
    resource_translated = {"resource_id": raw_resource.get("GroupName", None)}
    for raw_parameter, present_parameter in resource_parameters.items():
        if raw_resource.get(raw_parameter):
            resource_translated[present_parameter] = raw_resource.get(raw_parameter)
    if raw_resource.get("Tags") is not None:
        resource_translated["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            raw_resource.get("Tags")
        )
    return resource_translated


def convert_raw_flow_log_to_present(hub, flow_log: Dict):
    """
    Convert the aws flow log response to a common format

    Args:
        hub: required for functions in hub
        flow_log: describe flow log response

    Returns:
        A dictionary of flow log
    """
    describe_parameters = OrderedDict(
        {
            "DeliverLogsPermissionArn": "iam_role",
            "LogGroupName": "log_group_name",
            "TrafficType": "traffic_type",
            "LogDestinationType": "log_destination_type",
            "LogDestination": "log_destination",
            "LogFormat": "log_format",
            "MaxAggregationInterval": "max_aggregation_interval",
        }
    )
    translated_flow_log = {}
    flow_log_id = flow_log.get("FlowLogId")
    resource_id = flow_log.get("ResourceId")
    resource_ids = [resource_id]
    resource_type = resource_id.split("-")[0]
    translated_flow_log["resource_ids"] = resource_ids
    if resource_type == "vpc":
        resource_type = "VPC"
    elif resource_type == "subnet":
        resource_type = "Subnet"
    else:
        resource_type = "NetworkInterface"
    translated_flow_log["resource_type"] = resource_type
    translated_flow_log["resource_id"] = flow_log_id

    for parameter_old_key, parameter_new_key in describe_parameters.items():
        if flow_log.get(parameter_old_key) is not None:
            translated_flow_log[parameter_new_key] = flow_log.get(parameter_old_key)
    if flow_log.get("Tags") is not None:
        translated_flow_log["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            flow_log.get("Tags")
        )
    return translated_flow_log


def convert_raw_route_to_present(
    hub, raw_resource: Dict, route_table_id: str, idem_resource_name: str = None
) -> Dict[str, Any]:
    describe_parameters = OrderedDict(
        {
            "DestinationCidrBlock": "destination_cidr_block",
            "DestinationIpv6CidrBlock": "destination_ipv6_cidr_block",
            "DestinationPrefixListId": "destination_prefix_list_id",
            "EgressOnlyInternetGatewayId": "egress_only_internet_gateway_id",
            "GatewayId": "gateway_id",
            "InstanceId": "instance_id",
            "InstanceOwnerId": "instance_owner_id",
            "NatGatewayId": "nat_gateway_id",
            "TransitGatewayId": "transit_gateway_id",
            "LocalGatewayId": "local_gateway_id",
            "CarrierGatewayId": "carrier_gateway_id",
            "NetworkInterfaceId": "network_interface_id",
            "VpcPeeringConnectionId": "vpc_peering_connection_id",
            "CoreNetworkArn": "core_network_arn",
        }
    )
    if not raw_resource:
        return {}
    resource_id = f"{route_table_id}/{(raw_resource.get('DestinationCidrBlock') or raw_resource.get('DestinationIpv6CidrBlock') or raw_resource.get('DestinationPrefixListId'))}"
    resource_translated = {
        "name": idem_resource_name,
        "resource_id": resource_id,
        "route_table_id": route_table_id,
    }

    for parameter_old_key, parameter_new_key in describe_parameters.items():
        if raw_resource.get(parameter_old_key) is not None:
            # vpc_endpoint_id is sent in gateway id field. we have to check if it starts with vpce- and update
            # vpc_endpoint_id field.
            if "gateway_id" == parameter_new_key and raw_resource.get(
                parameter_old_key
            ).startswith("vpce-"):
                resource_translated["vpc_endpoint_id"] = raw_resource.get(
                    parameter_old_key
                )
            else:
                resource_translated[parameter_new_key] = raw_resource.get(
                    parameter_old_key
                )
    return resource_translated


def convert_raw_route_table_to_present(
    hub, raw_resource: Dict, idem_resource_name: str = None
) -> Dict[str, Any]:
    describe_parameters = OrderedDict(
        {"VpcId": "vpc_id", "PropagatingVgws": "propagating_vgws", "Tags": "tags"}
    )
    if not raw_resource:
        return {}
    resource_id = raw_resource.get("RouteTableId")
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    for parameter_old_key, parameter_new_key in describe_parameters.items():
        if raw_resource.get(parameter_old_key) is not None:
            resource_translated[parameter_new_key] = raw_resource.get(parameter_old_key)
    routes_to_add = []
    if raw_resource.get("Routes"):
        for route_to_add in raw_resource.get("Routes"):
            if route_to_add.get("State") == "active":
                routes_to_add.append(route_to_add)
        resource_translated["routes"] = routes_to_add
    if raw_resource.get("Tags") is not None:
        resource_translated["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            raw_resource.get("Tags")
        )
    return resource_translated


def convert_raw_route_table_association_to_present(
    hub, resource: Dict, idem_resource_name: str = None
) -> Dict[str, Any]:
    if not resource:
        return {}
    resource_id = resource.get("RouteTableAssociationId")
    resource_parameters = OrderedDict(
        {
            "RouteTableId": "route_table_id",
            "GatewayId": "gateway_id",
            "SubnetId": "subnet_id",
        }
    )
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in resource:
            resource_translated[parameter_present] = resource.get(parameter_raw)
    return resource_translated


def convert_raw_tg_vpc_attachment(
    hub, raw_resource: Dict, resource_name: str = None
) -> Dict[str, any]:
    resource_id = raw_resource.get("TransitGatewayAttachmentId")
    translated_resource = {"name": resource_name, "resource_id": resource_id}

    resource_parameters_transit_gateway = OrderedDict(
        {
            "TransitGatewayId": "transit_gateway",
            "VpcId": "vpc_id",
            "State": "state",
            "SubnetIds": "subnet_ids",
            "Options": "options",
        }
    )

    for camel_case_key, snake_case_key in resource_parameters_transit_gateway.items():
        if raw_resource.get(camel_case_key):
            translated_resource[snake_case_key] = raw_resource.get(camel_case_key)
    if raw_resource.get("Tags") is not None:
        translated_resource["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            raw_resource.get("Tags")
        )
    return translated_resource


async def convert_raw_dhcp_to_present_async(
    hub, ctx, raw_resource: Dict[str, Any], idem_resource_name: str = None
) -> Dict[str, Any]:
    resource_id = raw_resource.get("DhcpOptionsId")
    resource_parameters = OrderedDict({"Tags": "tags"})
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    result = dict(comment=[], result=True, ret=None)
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)
    if raw_resource.get("DhcpConfigurations"):
        dhcp_configs = []
        for dhcp_conf in raw_resource.get("DhcpConfigurations"):
            dhcp_config_values_list = []
            for dhcp in dhcp_conf.get("Values"):
                if "Value" in dhcp:
                    dhcp_config_values_list.append(dhcp.get("Value"))
            dhcp_config = {
                "Key": dhcp_conf.get("Key"),
                "Values": dhcp_config_values_list,
            }
            dhcp_configs.append(dhcp_config)
        resource_translated["dhcp_configurations"] = dhcp_configs
    vpc_list = []
    vpc_ret = await hub.exec.boto3.client.ec2.describe_vpcs(ctx)
    if not vpc_ret["result"]:
        result["comment"] = vpc_ret["comment"]
        result["result"] = vpc_ret["result"]
    else:
        for vpc in vpc_ret["ret"]["Vpcs"]:
            if vpc["DhcpOptionsId"] == resource_id:
                vpc_list.append(vpc["VpcId"])
    if vpc_list:
        resource_translated["vpc_id"] = vpc_list

    if raw_resource.get("Tags") is not None:
        resource_translated["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            raw_resource.get("Tags")
        )
    result["ret"] = resource_translated
    return result


def convert_raw_dhcp_association_to_present(
    hub, dhcp_id: str, idem_resource_name: str = None, vpc_id: str = None
) -> Dict[str, Any]:
    """
    Convert the AWS EC2 DHCP Options Association response to a common format

    Args:
        hub: required for functions in hub
        dhcp_id: ID of DHCP Options.
        idem_resource_name: name of the resource
        vpc_id: ID of VPC to which DHCP options need to be attached.

    Returns:
        A dictionary of EC2 DHCP options.
    """
    resource_translated = {
        "name": idem_resource_name,
        "dhcp_id": dhcp_id,
        "resource_id": f"{dhcp_id}-{vpc_id}",
    }
    if vpc_id:
        resource_translated["vpc_id"] = vpc_id
    return resource_translated


def convert_raw_sg_to_present(hub, security_group: Dict):
    """
    Convert the aws security group response to a common format

    Args:
        hub: required for functions in hub
        security_group: describe security group response

    Returns:
        A dictionary of sg group
    """
    translated_security_group = {}
    describe_parameters = OrderedDict(
        {
            "GroupId": "resource_id",
            "GroupName": "name",
            "VpcId": "vpc_id",
            "Description": "description",
        }
    )
    for parameter_old_key, parameter_new_key in describe_parameters.items():
        if security_group.get(parameter_old_key) is not None:
            translated_security_group[parameter_new_key] = security_group.get(
                parameter_old_key
            )
    if "Tags" in security_group:
        translated_security_group[
            "tags"
        ] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(security_group.get("Tags"))

    return translated_security_group


def convert_raw_sir_to_present(hub, spot_instance_request: Dict):
    """
    Convert the aws spot instance request response to a common format

    Args:
        hub: required for functions in hub
        spot_instance_request: describe security group response

    Returns:
        A dictionary of sg group
    """
    translated_spot_instance_request = {}
    describe_parameters = OrderedDict(
        {
            "CreateTime": "create-time",
            "InstanceId": "instance-id",
            "ProductDescription": "product-description",
            "SpotInstanceRequestId": "spot-instance-request-id",
            "SpotPrice": "spot-price",
            "State": "state",
            "Type": "type",
        }
    )
    for parameter_old_key, parameter_new_key in describe_parameters.items():
        if spot_instance_request.get(parameter_old_key) is not None:
            translated_spot_instance_request[
                parameter_new_key
            ] = spot_instance_request.get(parameter_old_key)
    if "Tags" in spot_instance_request:
        translated_spot_instance_request[
            "tags"
        ] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            spot_instance_request.get("Tags")
        )

    return translated_spot_instance_request


def convert_raw_internet_gateway_to_present(
    hub, resource: Dict[str, Any], idem_resource_name: str = None
) -> Dict[str, Any]:
    resource_translated = {
        "name": idem_resource_name,
        "resource_id": resource.get("InternetGatewayId"),
    }
    if resource.get("Tags"):
        resource_translated["tags"] = resource.get("Tags")
    if resource.get("Attachments"):
        resource_translated["vpc_id"] = [resource.get("Attachments")[0].get("VpcId")]
        resource_translated["attachments"] = resource.get("Attachments")
    if resource.get("Tags") is not None:
        resource_translated["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            resource.get("Tags")
        )
    return resource_translated


def convert_raw_nat_gateway_to_present(
    hub, raw_resource: Dict[str, Any], idem_resource_name: str = None
) -> Dict[str, Any]:
    resource_id = raw_resource.get("NatGatewayId")
    describe_parameters = OrderedDict(
        {
            "SubnetId": "subnet_id",
            "ConnectivityType": "connectivity_type",
            "State": "state",
        }
    )
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    for parameter_raw, parameter_present in describe_parameters.items():
        if parameter_raw in raw_resource:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)
    if raw_resource.get("NatGatewayAddresses"):
        for nat_gateway_address in raw_resource.get("NatGatewayAddresses"):
            if "AllocationId" in nat_gateway_address:
                resource_translated["allocation_id"] = nat_gateway_address.get(
                    "AllocationId"
                )
                break
    if "Tags" in raw_resource:
        resource_translated["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            raw_resource.get("Tags")
        )
    return resource_translated


def convert_raw_elastic_ip_to_present(
    hub, raw_resource: Dict[str, Any], idem_resource_name: str = None
) -> Dict[str, Any]:
    """
    Given an object state from aws, this function creates a translated resource object in response.

    Args:
        hub: required for functions in hub
        raw_resource (Dict): The dictionary object from where the raw state of resource needs to be translated.
        idem_resource_name (str): The name of the idem resource

    Returns: Dict[str, Any]
    """
    elastic_ip = raw_resource
    resource_id = elastic_ip.get("PublicIp")
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    describe_parameters = OrderedDict(
        {
            "AllocationId": "allocation_id",
            "AssociationId": "association_id",
            "Domain": "domain",
            "InstanceId": "instance_id",
            "NetworkBorderGroup": "network_border_group",
            "PublicIpv4Pool": "public_ipv4_pool",
            "Tags": "tags",
            "PublicIp": "resource_id",
            "CustomerOwnedIpv4Pool": "customer_owned_ipv4_pool",
        }
    )
    for parameter_raw, parameter_present in describe_parameters.items():
        if elastic_ip.get(parameter_raw) is not None:
            resource_translated[parameter_present] = elastic_ip.get(parameter_raw)
    if raw_resource.get("Tags") is not None:
        resource_translated["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            raw_resource.get("Tags")
        )
    return resource_translated


def convert_raw_vpc_endpoint_to_present(
    hub, raw_resource: Dict[str, Any], idem_resource_name: str = None
) -> Dict[str, Any]:
    """
    Convert AWS returned data structure to correct idem vpc-endpoint present state

     Args:
        hub: required for functions in hub
        raw_resource: The aws response to convert

    Returns: Valid idem state for vpc-endpoint of type Dict['string', Any]
    """
    hub.log.debug(
        f"Converting raw aws.ec2.vpc_endpoint: {raw_resource} to valid present state"
    )
    describe_parameters = OrderedDict(
        {
            "VpcEndpointType": "vpc_endpoint_type",
            "VpcId": "vpc_id",
            "ServiceName": "service_name",
            "PolicyDocument": "policy_document",
            "RouteTableIds": "route_table_ids",
            "SubnetIds": "subnet_ids",
            "SecurityGroupIds": "security_group_ids",
            "PrivateDnsEnabled": "private_dns_enabled",
            "State": "state",
            "DnsOptions": "dns_options",
            "DnsEntries": "dns_entries",
        }
    )
    resource_id = raw_resource.get("VpcEndpointId")
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    for parameter_raw, parameter_present in describe_parameters.items():
        if raw_resource.get(parameter_raw) is not None:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)
    if raw_resource.get("Tags") is not None:
        resource_translated["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            raw_resource.get("Tags")
        )
    if raw_resource.get("Groups"):
        security_group_ids = []
        for security_group in raw_resource.get("Groups"):
            security_group_ids.append(security_group.get("GroupId"))
        resource_translated["security_group_ids"] = security_group_ids

    return resource_translated


def convert_raw_ami_to_present(hub, raw_resource: Dict[str, Any]) -> Dict[str, Any]:
    """
    Util function to convert raw resource state from AWS AMI to present input format.
    """
    resource_id = raw_resource.get("ImageId")
    resource_parameters = OrderedDict(
        {
            "Name": "name",
            "CreationDate": "creation_date",
            "ImageLocation": "image_location",
            "Architecture": "architecture",
            "KernelId": "kernel_id",
            "BlockDeviceMappings": "block_device_mappings",
            "Description": "description",
            "EnaSupport": "ena_support",
            "BillingProducts": "billing_products",
            "RamdiskId": "ramdisk_id",
            "RootDeviceName": "root_device_name",
            "SriovNetSupport": "sriov_net_support",
            "VirtualizationType": "virtualization_type",
            "BootMode": "boot_mode",
        }
    )
    resource_translated = {"resource_id": resource_id}
    for parameter_raw, parameter_present in resource_parameters.items():
        if raw_resource.get(parameter_raw):
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    if "Tags" in raw_resource:
        resource_translated["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            raw_resource.get("Tags")
        )
    return resource_translated


def convert_raw_vpc_peering_connection_to_present(
    hub, raw_resource: Dict[str, Any], idem_resource_name: str
) -> Dict[str, Any]:
    if not raw_resource:
        return {}

    resource_translated = {
        "resource_id": raw_resource["VpcPeeringConnectionId"],
        "name": idem_resource_name,
        "peer_owner_id": raw_resource["AccepterVpcInfo"]["OwnerId"],
        "peer_vpc_id": raw_resource["AccepterVpcInfo"]["VpcId"],
        "vpc_id": raw_resource["RequesterVpcInfo"]["VpcId"],
        "peer_region": raw_resource["AccepterVpcInfo"]["Region"],
        "tags": hub.tool.aws.tag_utils.convert_tag_list_to_dict(raw_resource["Tags"]),
        "status": raw_resource["Status"]["Code"],
    }

    return resource_translated


def convert_raw_availability_zone_to_snake_case(
    hub, ctx, raw_resource: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Util function to convert raw resource state from AWS Availability Zone to a snake case format.
    """
    if not raw_resource:
        return {}

    resource_parameters = OrderedDict(
        {
            "GroupName": "group_name",
            "NetworkBorderGroup": "network_border_group",
            "OptInStatus": "opt_in_status",
            "ParentZoneId": "parent_zone_id",
            "ParentZoneName": "parent_zone_name",
            "RegionName": "region_name",
            "State": "state",
            "ZoneName": "zone_name",
            "ZoneType": "zone_type",
        }
    )
    resource_translated = {"resource_id": raw_resource["ZoneId"]}
    for parameter_raw, parameter_present in resource_parameters.items():
        if raw_resource.get(parameter_raw):
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    return resource_translated


async def convert_raw_snapshot_to_present_async(
    hub, ctx, raw_resource: Dict[str, Any], idem_resource_name: str
) -> Dict[str, Any]:
    """
    Util function to convert raw resource state from AWS snapshot to present input format
    """
    resource_id = raw_resource.get("SnapshotId")
    resource_parameters = OrderedDict(
        {
            "Description": "description",
            "OutpostArn": "outpost_arn",
            "Tags": "tags",
            "VolumeId": "volume_id",
        }
    )
    resource_translated = {"resource_id": resource_id}
    resource_translated["name"] = idem_resource_name
    for parameter_raw, parameter_present in resource_parameters.items():
        if raw_resource.get(parameter_raw):
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    """
        Expansion of the volume associated with the snapshot, if present. This is due to the one-way
        relationship with volume once the snapshot is created, to allow the user access to up to date
        values of the volume if it has not been removed. This also fills a feature gap with terraform
        which provides some of this expansion as part of its snapshot support.
    """
    if resource_translated["volume_id"] is not None:
        volume = await hub.exec.aws.ec2.volume.get(
            ctx=ctx,
            resource_id=resource_translated["volume_id"],
            name=resource_translated["name"],
        )

    if volume["result"] and volume["ret"]:
        translated_volume = {}
        for prop in volume["ret"]:
            if prop != "tags":
                translated_volume[prop] = volume["ret"].get(prop)
        resource_translated["associated_volume"] = translated_volume

    if "StartTime" in raw_resource:
        local_time = raw_resource.get("StartTime").astimezone()
        start_time = local_time.astimezone(timezone.utc).strftime(UTC_FORMAT)
        resource_translated["start_time"] = start_time

    if "Tags" in raw_resource:
        resource_translated["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            raw_resource.get("Tags")
        )

    return resource_translated


def convert_raw_volume_to_present(
    hub, raw_resource: Dict[str, Any], idem_resource_name: str
) -> Dict[str, Any]:
    """
    Util function to convert raw resource state from AWS Volume to present input format
    """
    resource_id = raw_resource.get("VolumeId")
    resource_parameters = OrderedDict(
        {
            "AvailabilityZone": "availability_zone",
            "Size": "size",
            "SnapshotId": "snapshot_id",
            "State": "state",
            "Iops": "iops",
            "Tags": "tags",
            "VolumeType": "volume_type",
            "MultiAttachEnabled": "multi_attach_enabled",
            "Throughput": "throughput",
            "Encrypted": "encrypted",
        }
    )
    resource_translated = {"resource_id": resource_id}
    resource_translated["name"] = idem_resource_name
    for parameter_raw, parameter_present in resource_parameters.items():
        if raw_resource.get(parameter_raw):
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    if "CreateTime" in raw_resource:
        local_time = raw_resource.get("CreateTime").astimezone()
        start_time = local_time.astimezone(timezone.utc).strftime(UTC_FORMAT)
        resource_translated["create_time"] = start_time

    if "Tags" in raw_resource:
        resource_translated["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            raw_resource.get("Tags")
        )
    return resource_translated


def convert_raw_vpc_peering_connection_options_to_present(
    hub, raw_resource: Dict[str, Any], idem_resource_name: str
) -> Dict[str, Any]:
    if not raw_resource:
        return {}

    resource_translated = {
        "resource_id": raw_resource["VpcPeeringConnectionId"],
        "name": idem_resource_name,
    }
    # If acceptor or requestor vpc is from a different AWS account we do not get
    # PeeringOptions from vpc in another AWS account.
    if "PeeringOptions" in raw_resource["AccepterVpcInfo"]:
        resource_translated["peer_allow_remote_vpc_dns_resolution"] = raw_resource[
            "AccepterVpcInfo"
        ]["PeeringOptions"]["AllowDnsResolutionFromRemoteVpc"]
        resource_translated["peer_allow_classic_link_to_remote_vpc"] = raw_resource[
            "AccepterVpcInfo"
        ]["PeeringOptions"]["AllowEgressFromLocalClassicLinkToRemoteVpc"]
        resource_translated["peer_allow_vpc_to_remote_classic_link"] = raw_resource[
            "AccepterVpcInfo"
        ]["PeeringOptions"]["AllowEgressFromLocalVpcToRemoteClassicLink"]

    if "PeeringOptions" in raw_resource["RequesterVpcInfo"]:
        resource_translated["allow_remote_vpc_dns_resolution"] = raw_resource[
            "RequesterVpcInfo"
        ]["PeeringOptions"]["AllowDnsResolutionFromRemoteVpc"]
        resource_translated["allow_classic_link_to_remote_vpc"] = raw_resource[
            "RequesterVpcInfo"
        ]["PeeringOptions"]["AllowEgressFromLocalClassicLinkToRemoteVpc"]
        resource_translated["allow_vpc_to_remote_classic_link"] = raw_resource[
            "RequesterVpcInfo"
        ]["PeeringOptions"]["AllowEgressFromLocalVpcToRemoteClassicLink"]

    return resource_translated


def convert_raw_vpc_peering_connection_accepter_to_present(
    hub, raw_resource: Dict[str, Any], idem_resource_name: str
) -> Dict[str, Any]:
    if not raw_resource:
        return {}

    resource_translated = {
        "resource_id": raw_resource["VpcPeeringConnectionId"],
        "name": idem_resource_name,
        "connection_status": raw_resource["Status"]["Code"],
    }
    if "Tags" in raw_resource:
        resource_translated["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            raw_resource.get("Tags")
        )
    return resource_translated


def convert_raw_lauchtemplate_to_present(
    hub,
    raw_resource: Dict[str, Any],
    raw_version: Dict[str, Any],
    idem_resource_name: str = None,
) -> Dict[str, Any]:
    resource_id = raw_resource.get("LaunchTemplateId")
    resource_parameters = OrderedDict(
        {
            "LaunchTemplateName": "name",
            "CreatedBy": "created_by",
            "DefaultVersionNumber": "default_version_number",
            "LatestVersionNumber": "latest_version_number",
        }
    )
    resource_translated = {"resource_id": resource_id}
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)
    if "CreateTime" in raw_resource:
        local_time = raw_resource.get("CreateTime").astimezone()
        start_time = local_time.astimezone(timezone.utc).strftime(UTC_FORMAT)
        resource_translated["create_time"] = start_time
    if "Tags" in raw_resource:
        resource_translated["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            raw_resource.get("Tags")
        )
    resource_translated["version_description"] = raw_version.get("VersionDescription")
    launch_template_data = raw_version.get("LaunchTemplateData")
    if launch_template_data.get("UserData"):
        user_data = launch_template_data.get("UserData")
        launch_template_data["UserData"] = base64.b64decode(user_data.encode()).decode()
    resource_translated["launch_template_data"] = launch_template_data
    return resource_translated
