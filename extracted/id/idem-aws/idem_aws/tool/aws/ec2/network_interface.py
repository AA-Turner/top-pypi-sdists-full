from typing import Any
from typing import Dict


def convert_to_present(
    hub, describe_network_interfaces: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Convert the output of describe_network_interfaces to present states format
    """
    result = {}

    for network_interface in describe_network_interfaces.get("NetworkInterfaces", ()):
        resource_id = network_interface.get("NetworkInterfaceId")

        association = network_interface.get("Association", {})
        attachment = network_interface.get("Attachment", {})
        ena_srd_specification = attachment.get("ena_srd_specification", {})

        result[resource_id] = dict(
            name=resource_id,
            resource_id=resource_id,
            # Association
            allocation_id=association.get("AllocationId"),
            ip_owner_id=association.get("IpOwnerId"),
            public_dns_name=association.get("PublicDnsName"),
            public_ip=association.get("PublicIp"),
            customer_owned_ip=association.get("CustomerOwnedIp"),
            carrier_ip=association.get("CarrierIp"),
            # Attachment
            attachment_id=attachment.get("AttachmentId"),
            delete_on_termination=attachment.get("DeleteOnTermination"),
            device_index=attachment.get("DeviceIndex"),
            network_card_index=attachment.get("NetworkCardIndex"),
            ena_srd_enabled=ena_srd_specification.get("EnaSrdEnabled"),
            ena_srd_udp_enabled=ena_srd_specification.get("EnaSrdUdpEnabled"),
            # General
            client_token=None,
            availability_zone=network_interface.get("AvailabilityZone"),
            description=network_interface.get("Description"),
            groups=[
                group.get("GroupId") for group in network_interface.get("Groups", [])
            ],
            interface_type=network_interface.get("InterfaceType"),
            ipv4_address_count=len(network_interface.get("Ipv4Addresses", [])) or None,
            ipv4_prefix_count=len(network_interface.get("Ipv4Prefixes", [])) or None,
            ipv4_prefixes=[
                i.get("Ipv4Prefix") for i in network_interface.get("Ipv4Prefixes", [])
            ]
            or None,
            ipv6_addresses=[
                i.get("Ipv6Address") for i in network_interface.get("Ipv6Addresses", [])
            ]
            or None,
            ipv6_address_count=len(network_interface.get("Ipv6Addresses", [])) or None,
            ipv6_prefix_count=len(network_interface.get("Ipv6Prefixes", [])) or None,
            ipv6_prefixes=[
                i.get("Ipv6Prefix") for i in network_interface.get("Ipv6Prefixes", [])
            ]
            or None,
            mac_address=network_interface.get("MacAddress"),
            outpost_arn=network_interface.get("OutpostArn"),
            owner_id=network_interface.get("OwnerId"),
            private_dns_name=network_interface.get("PrivateDnsName"),
            private_ip_addresses=[
                i.get("PrivateIpAddress")
                for i in network_interface.get("PrivateIpAddresses", [])
            ]
            or None,
            primary_ip_address=network_interface.get("PrivateIpAddress"),
            requester_id=network_interface.get("RequesterId"),
            requester_managed=network_interface.get("RequesterManaged"),
            source_dest_check=network_interface.get("SourceDestCheck"),
            subnet_id=network_interface.get("SubnetId"),
            status=network_interface.get("Status"),
            tags={
                i.get("Key"): i.get("Value")
                for i in network_interface.get("TagSet", [])
            },
            vpc_id=network_interface.get("VpcId"),
            deny_all_igw_traffic=network_interface.get("DenyAllIgwTraffic"),
            ipv6_native=network_interface.get("Ipv6Native"),
            default_ipv6_address=network_interface.get("Ipv6Address"),
        )

    return result
