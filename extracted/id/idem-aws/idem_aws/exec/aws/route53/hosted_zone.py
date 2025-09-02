from typing import Any
from typing import Dict

__func_alias__ = {"list_": "list"}


async def get(hub, ctx, name: str, resource_id: str):
    """Provides details about a specific hosted_zone as a data-source.

    Args:
        name(str):
            The name of the Idem state.

        resource_id(str):
            AWS Hosted Zone id to identify the resource.

    Returns:
        Dict[bool, list, dict or None]:

    Examples:
        Calling this exec module function from the cli with resource_id

        .. code-block:: bash

            idem exec aws.route53.hosted_zone.get name="idem_name" resource_id="resource_id"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.route53.hosted_zone.get
                - kwargs:
                    name: my_resource
                    resource_id: resource_id

    """
    result = dict(comment=[], ret=None, result=True)

    ret = await hub.exec.boto3.client.route53.get_hosted_zone(ctx, Id=resource_id)

    if not ret["result"]:
        if "NoSuchHostedZone" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.route53.hosted_zone", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    tags_ret = await hub.exec.boto3.client.route53.list_tags_for_resource(
        ctx, ResourceType="hostedzone", ResourceId=resource_id
    )
    tags = None
    if tags_ret["result"]:
        tags = tags_ret["ret"].get("ResourceTagSet").get("Tags", [])
    else:
        result["result"] = False
        result["comment"] = tags_ret["comment"]
        return result

    result[
        "ret"
    ] = hub.tool.aws.route53.conversion_utils.convert_raw_hosted_zone_to_present(
        raw_resource=ret,
        idem_resource_name=name,
        tags=tags,
    )

    return result


async def list_(
    hub,
    ctx,
    hosted_zone_name: str = None,
    private_zone: bool = None,
    vpc_id: str = None,
    tags: Dict[str, Any] = None,
    resource_id: str = None,
):
    """
    Args:
        hosted_zone_name(str, Optional):
            The domain name of hosted_zone

        private_zone(bool, Optional):
            Bool argument to specify a private hosted_zone. One of the filter option for hosted_zone

        vpc_id(str, Optional):
            The vpc_id associated with the hosted_zone.One of the filter option for hosted_zone

        tags(dict, Optional):
            Tags of the hosted_zone. One of the filter option for hosted_zone

        resource_id(str, Optional):
            AWS Hosted Zone id to identify the resource.

    Returns:
        Dict[bool, list, dict or None]:

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec aws.route53.hosted_zone.list hosted_zone_name="my_hosted_zone"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.route53.hosted_zone.list
                - kwargs:
                    hosted_zone_name: my_hosted_zone

    """
    result = dict(comment=[], ret=None, result=True)

    hosted_zones = []

    # Even though this is list a resource_id might be specified
    if resource_id:
        get_ret = await hub.exec.aws.route53.hosted_zone.get(
            ctx, name="from-list", resource_id=resource_id
        )
        if get_ret["result"] and get_ret["ret"]:
            result["ret"] = [get_ret["ret"]]
            return result
        return get_ret

    ret = await hub.tool.aws.route53.hosted_zone_utils.get_all_hosted_zones(ctx)
    if not ret["result"]:
        result["result"] = ret["result"]
        result["comment"] = ret["comment"]
        return result

    filtered_ret = hub.tool.aws.route53.hosted_zone_utils.get_hosted_zones_with_filters(
        raw_hosted_zones=ret["ret"],
        hosted_zone_name=hosted_zone_name,
        private_zone=private_zone,
        vpc_id=vpc_id,
        tags=tags,
    )
    result["comment"] = filtered_ret["comment"]
    if not filtered_ret["ret"]:
        result["result"] = filtered_ret["result"]
        return result

    if filtered_ret["ret"] is None:
        hub.tool.aws.comment_utils.list_empty_comment(
            resource_type="aws.route53.hosted_zone", name=hosted_zone_name
        )
        result["result"] = filtered_ret["result"]
        return result

    for raw_hosted_zone in filtered_ret["ret"]:
        name = raw_hosted_zone["ret"]["HostedZone"].get("Name")
        resource_id = raw_hosted_zone["ret"]["HostedZone"].get("Id").split("/")[-1]
        hosted_zone = await hub.exec.aws.route53.hosted_zone.get(
            ctx, name=name, resource_id=resource_id
        )
        if not hosted_zone["result"]:
            result["comment"] = hosted_zone["comment"]
            result["result"] = False
            return result

        hosted_zones.append(hosted_zone["ret"])

    result["ret"] = hosted_zones
    return result
