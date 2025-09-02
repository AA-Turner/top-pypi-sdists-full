from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List


async def get_all_hosted_zones(hub, ctx) -> Dict[str, Any]:
    """
    Describes all the hosted zones available.

    Args:
        hub:
        ctx:

    Returns:
        {"result": True|False, "comment": "A message Tuple", "ret": None}
    """
    result = dict(comment=[], result=True, ret=None)
    hosted_zones = []
    ret = await hub.exec.boto3.client.route53.list_hosted_zones(ctx)
    if not ret["result"]:
        result["result"] = ret["result"]
        result["comment"] = ret["comment"]
        return result
    for hosted_zone in ret["ret"]["HostedZones"]:
        resource_id = hosted_zone.get("Id")
        ret = await hub.exec.boto3.client.route53.get_hosted_zone(ctx, Id=resource_id)
        if not ret["result"]:
            result["result"] = ret["result"]
            result["comment"] = ret["comment"]
            return result

        temp_hosted_zone = ret["ret"]["HostedZone"]

        if ret["ret"].get("VPCs"):
            temp_hosted_zone["VPCs"] = ret["ret"].get("VPCs")
        if ret["ret"].get("DelegationSet"):
            temp_hosted_zone["DelegationSet"] = ret["ret"].get("DelegationSet")

        tags_ret = await hub.exec.boto3.client.route53.list_tags_for_resource(
            ctx, ResourceType="hostedzone", ResourceId=resource_id.split("/")[-1]
        )
        if not tags_ret["result"]:
            result["result"] = tags_ret["result"]
            result["comment"] = tags_ret["comment"]
            return result

        if tags_ret["result"] and tags_ret["ret"].get("ResourceTagSet").get("Tags"):
            temp_hosted_zone["Tags"] = tags_ret["ret"]["ResourceTagSet"].get("Tags")
        hosted_zones.append(temp_hosted_zone)

    result["ret"] = {"HostedZones": hosted_zones}
    return result


def get_hosted_zones_with_filters(
    hub,
    raw_hosted_zones: List,
    hosted_zone_name: str = None,
    private_zone: bool = None,
    vpc_id: str = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass("Tag", [("Key", str), ("Value", str, field(default=None))])
    ] = None,
):
    """
    Returns the hosted_zone with the specified filters, if it is available.

    Args:
        raw_hosted_zones(Dict): Dict of all the described hosted_zones
        hosted_zone_name(str, Optional): Domain name of hosted_zone to filter.
        private_zone(bool, Optional): Bool argument to specify a private hosted_zone. One of the filter option for hosted_zone
        vpc_id(str, Optional): The vpc_id associated with the hosted_zone. One of the filter option for hosted_zone
        tags(List, Optional): Tags of the hosted_zone. One of the filter option for hosted_zone

    """
    result = dict(comment=[], result=True, ret=None)
    hosted_zones = raw_hosted_zones["HostedZones"]

    # filter_hosted_zones() returns True if all the filters match for a hosted_zone, and it is added to the list
    filtered_hosted_zones = list(
        filter(
            lambda x: filter_hosted_zones(
                x, hosted_zone_name, private_zone, vpc_id, tags
            ),
            hosted_zones,
        )
    )

    if not filtered_hosted_zones:
        result["comment"] += [
            f"Unable to find aws.route53.hosted_zone resource with given filters"
        ]
        return result

    result["comment"] += [
        f"Found this {len(filtered_hosted_zones)} aws.route53.hosted_zone resource(s) with given filters"
    ]

    result["ret"] = []
    for filtered_hosted_zone in filtered_hosted_zones:
        # Building the format in which hosted_zone conversion_utils takes the hosted_zone resource
        result["ret"].append(
            {
                "ret": {
                    "HostedZone": filtered_hosted_zone,
                    "VPCs": filtered_hosted_zone.get("VPCs"),
                    "DelegationSet": filtered_hosted_zone.get("DelegationSet"),
                },
                "tags": filtered_hosted_zone.get("Tags"),
            }
        )

    return result


def filter_hosted_zones(
    hosted_zone: Dict,
    hosted_zone_name: str = None,
    private_zone: bool = None,
    vpc_id: str = None,
    tags: List = None,
):
    """
    Returns True if the hosted_zone checks all the filters provided or return False

    Args:
        hosted_zone(Dict): The described hosted_zone
        hosted_zone_name(str, Optional): Domain name of hosted_zone to filter.
        private_zone(bool, Optional): Bool argument to specify a private hosted_zone. One of the filter option for hosted_zone
        vpc_id(str, Optional): The vpc_id associated with the hosted_zone. One of the filter option for hosted_zone
        tags(List, Optional): Tags of the hosted_zone. One of the filter option for hosted_zone

    """
    # Return True if all the provided filters match or return False.

    if hosted_zone_name:
        if hosted_zone["Name"] != hosted_zone_name:
            return False

    if private_zone is not None:
        if hosted_zone["Config"]["PrivateZone"] != private_zone:
            return False

    if vpc_id:
        found = False
        if hosted_zone["VPCs"]:
            for vpc in hosted_zone["VPCs"]:
                if vpc["VPCId"] == vpc_id:
                    found = True
                    break
            if not found:
                return False

    # Checking if all the tags in the filter match with the tags present in the hosted_zone.If not we return False
    if tags:
        tags2 = hosted_zone.get("Tags")
        if tags2 is None:
            return False
        tags2_map = {tag.get("Key"): tag for tag in tags2}
        for tag in tags:
            if tag["Key"] not in tags2_map or (
                tags2_map.get(tag["Key"]).get("Value") != tag["Value"]
            ):
                return False

    return True
