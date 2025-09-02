"""Exec module for managing managing Amazon Elastic Load Balancing"""
from typing import Dict


async def get(
    hub,
    ctx,
    resource_id: str,
) -> Dict:
    """
    Pass required params to get a ElasticLoadBalancing Load Balancer resource.

    Args:
        resource_id(str): The name of the ElasticLoadBalancing Load Balancer. Must have a maximum of 32 characters.

    Returns:
        .. code-block:: python

            {"result": True|False, "comment": A message List, "ret": None}

    Examples:
        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.elb.load_balancer.get
                - kwargs:
                    resource_id: resource_id

        Calling this exec function from the cli with resource_id

        .. code-block:: bash

            idem exec aws.elb.load_balancer.get resource_id="resource_id"

        Calling this exec module function from within a state module in pure python

        .. code-block:: python

            async def state_function(hub, ctx, resource_id, **kwargs):
                ret = await hub.exec.aws.elb.load_balancer.get(ctx, resource_id=resource_id)

    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.tool.aws.elb.load_balancer.search_raw(
        ctx=ctx, resource_id=resource_id
    )
    if not ret["result"]:
        if "LoadBalancerNotFound" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.elb.load_balancer", name=resource_id
                )
            )
            result["comment"] += ret["comment"]
            return result
        result["comment"] += ret["comment"]
        result["result"] = False
        return result
    if not ret["ret"]["LoadBalancerDescriptions"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.elb.load_balancer", name=resource_id
            )
        )
        return result

    tags = attributes = []
    tags_ret = await hub.exec.boto3.client.elb.describe_tags(
        ctx, LoadBalancerNames=[resource_id]
    )
    if not tags_ret["result"]:
        result["comment"] = list(tags_ret["comment"])
        result["result"] = False
        return result
    else:
        if tags_ret.get("ret") and tags_ret.get("ret")["TagDescriptions"]:
            tags = (tags_ret["ret"]["TagDescriptions"][0]).get("Tags")

    attributes_ret = await hub.exec.boto3.client.elb.describe_load_balancer_attributes(
        ctx, LoadBalancerName=resource_id
    )
    if not attributes_ret["result"]:
        result["comment"] = list(attributes_ret["comment"])
        result["result"] = False
        return result
    else:
        if attributes_ret.get("ret") and attributes_ret.get("ret").get(
            "LoadBalancerAttributes"
        ):
            attributes = attributes_ret["ret"].get("LoadBalancerAttributes")

    result[
        "ret"
    ] = hub.tool.aws.elb.conversion_utils.convert_raw_load_balancer_to_present(
        raw_resource=ret["ret"]["LoadBalancerDescriptions"][0],
        idem_resource_name=resource_id,
        tags=hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags),
        attributes=attributes,
    )
    return result
