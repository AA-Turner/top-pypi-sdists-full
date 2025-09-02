from collections import OrderedDict
from typing import Any
from typing import Dict
from typing import List


def convert_raw_load_balancer_to_present(
    hub,
    raw_resource: Dict[str, Any],
    idem_resource_name: str = None,
    tags: Dict[str, str] = None,
    attributes: List[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    Util function to convert raw resource state from AWS ElasticLoadBalancingv2 Load Balancer to present input format.

    Args:
        raw_resource(Dict[str, Any]):
            The AWS response from 'ElasticLoadBalancingv2 describe_load_balancers' to convert.
        idem_resource_name(str, Optional): An Idem name of the resource.
        tags(Dict[str, str], Optional): The AWS ElasticLoadBalancingv2 Load Balancer tags.
        attributes(List[Dict[str, str]], Optional):
            List of attributes associated with given ElasticLoadBalancingv2 Load Balancer.

    Returns:
        Dict[str, Any]
    """

    resource_id = raw_resource.get("LoadBalancerArn")
    resource_parameters = OrderedDict(
        {
            "SecurityGroups": "security_groups",
            "Scheme": "scheme",
            "Type": "lb_type",
            "IpAddressType": "ip_address_type",
            "CustomerOwnedIpv4Pool": "customer_owned_ipv4_pool",
            "DNSName": "dns_name",
            "CanonicalHostedZoneId": "zone_id",
        }
    )
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    subnets = []
    subnet_mappings = []
    if raw_resource.get("AvailabilityZones"):
        for zone in raw_resource.get("AvailabilityZones"):
            subnets.append(zone.get("SubnetId"))
            if zone.get("LoadBalancerAddresses"):
                mapping_parameters = OrderedDict(
                    {
                        "SubnetId": zone.get("SubnetId"),
                        "AllocationId": zone.get("LoadBalancerAddresses")[0].get(
                            "AllocationId"
                        ),
                        "PrivateIPv4Address": zone.get("LoadBalancerAddresses")[0].get(
                            "PrivateIPv4Address"
                        ),
                        "IPv6Address": zone.get("LoadBalancerAddresses")[0].get(
                            "IPv6Address"
                        ),
                    }
                )
                mapping = {}
                for name, value in mapping_parameters.items():
                    if value:
                        mapping[name] = value
                if mapping:
                    subnet_mappings.append(mapping)
    resource_translated["subnets"] = subnets
    resource_translated["subnet_mappings"] = subnet_mappings

    if attributes:
        resource_translated["attributes"] = attributes
    if tags:
        resource_translated["tags"] = tags
    return resource_translated


def convert_raw_target_group_to_present(
    hub,
    raw_resource: Dict[str, Any],
    idem_resource_name: str = None,
    tags: Dict[str, str] = None,
    attributes: List[Dict[str, str]] = None,
    targets: List[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Util function to convert raw resource state from ElasticLoadBalancingv2 Target Group to present input format.

    Args:
        raw_resource(Dict[str, Any]): The AWS response from 'ElasticLoadBalancingv2 describe_target_groups' to convert.
        idem_resource_name(str, Optional): An Idem name of the resource.
        tags(Dict[str, str], Optional): The AWS ElasticLoadBalancingv2 Target Group tags.
        attributes(List[Dict[str, str]], Optional):
            List of attributes associated with given ElasticLoadBalancingv2 Target Group.
        targets(List[Dict[str, Any]], Optional):
            List of targets associated with given ElasticLoadBalancingv2 Target Group.

    Returns:
        Dict[str, Any]
    """
    resource_id = raw_resource.get("TargetGroupArn")
    resource_parameters = OrderedDict(
        {
            "Protocol": "protocol",
            "Port": "port",
            "VpcId": "vpc_id",
            "HealthCheckProtocol": "health_check_protocol",
            "HealthCheckPort": "health_check_port",
            "HealthCheckEnabled": "health_check_enabled",
            "HealthCheckIntervalSeconds": "health_check_interval_seconds",
            "HealthCheckTimeoutSeconds": "health_check_timeout_seconds",
            "HealthyThresholdCount": "healthy_threshold_count",
            "UnhealthyThresholdCount": "unhealthy_threshold_count",
            "HealthCheckPath": "health_check_path",
            "Matcher": "matcher",
            "TargetType": "target_type",
            "ProtocolVersion": "protocol_version",
            "IpAddressType": "ip_address_type",
        }
    )
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    if attributes:
        resource_translated["attributes"] = attributes
    if tags:
        resource_translated["tags"] = tags

    targets_add = []
    if targets:
        for target in targets:
            targets_add.append(target.get("Target"))
    resource_translated["targets"] = targets_add

    return resource_translated


def convert_raw_listener_to_present(
    hub,
    raw_resource: Dict[str, Any],
    idem_resource_name: str = None,
    tags: Dict[str, str] = None,
    certificates: List[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Util functions to convert raw resource state from AWS ELBv2 Listener to present input format.

    Args:
        raw_resource(dict[str, Any]):
            The AWS response from 'ElasticLoadBalancingv2 describe_listeners' to convert.

        idem_resource_name(str, Optional):
            An Idem name of the resource.

        tags(dict[str, str], Optional):
            The AWS ElasticLoadBalancingv2 Listener tags.

        certificates(list[dict[str, Any]], Optional):
            List of certificates associated with given ElasticLoadBalancingv2 Listener.

    Returns:
        Dict[str, Any]
    """
    resource_id = raw_resource.get("ListenerArn")
    resource_parameters = OrderedDict(
        {
            "Protocol": "protocol",
            "Port": "port",
            "SslPolicy": "ssl_policy",
            "Certificates": "certificates",
            "AlpnPolicy": "alpn_policy",
            "LoadBalancerArn": "lb_arn",
            "DefaultActions": "default_actions",
        }
    )
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)
    if tags:
        resource_translated["tags"] = tags

    default_certificates = certificate_list = []
    if certificates:
        for certificate in certificates:
            is_default = certificate.get("IsDefault", False)
            certificate.pop("IsDefault", None)
            if is_default:
                default_certificates.append(certificate)
            else:
                certificate_list.append(certificate)
        resource_translated["certificates"] = certificate_list
        resource_translated["default_certificates"] = default_certificates
    return resource_translated
