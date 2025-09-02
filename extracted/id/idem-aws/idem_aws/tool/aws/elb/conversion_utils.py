from collections import OrderedDict
from typing import Any
from typing import Dict
from typing import List


def convert_raw_load_balancer_to_present(
    hub,
    raw_resource: Dict[str, Any],
    idem_resource_name: str = None,
    tags: Dict[str, str] = None,
    attributes: List[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Util function to convert raw resource state from AWS ElasticLoadBalancing Load Balancer to present input format.

    Args:
        raw_resource(Dict[str, Any]):The AWS response from 'ElasticLoadBalancing describe_load_balancers' to convert.
        idem_resource_name(str, Optional): An Idem name of the resource.
        tags(Dict[str, str], Optional): The AWS ElasticLoadBalancing Load Balancer tags.
        attributes(List[Dict[str, Any]], Optional):
            List of attributes associated with given ElasticLoadBalancing Load Balancer.

    Returns:
        Dict[str, Any]
    """

    resource_id = raw_resource.get("LoadBalancerName")
    resource_parameters = OrderedDict(
        {
            "AvailabilityZones": "availability_zones",
            "Subnets": "subnets",
            "SecurityGroups": "security_groups",
            "Scheme": "scheme",
            "Instances": "instances",
        }
    )
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    listeners = []
    if raw_resource.get("ListenerDescriptions"):
        for listener in raw_resource.get("ListenerDescriptions"):
            listeners.append(listener.get("Listener"))
    resource_translated["listeners"] = listeners
    if attributes:
        resource_translated["load_balancer_attributes"] = attributes
    if tags:
        resource_translated["tags"] = tags
    return resource_translated
