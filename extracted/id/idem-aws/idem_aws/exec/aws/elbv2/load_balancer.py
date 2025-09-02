"""Exec module for managing managing Amazon Elastic Load Balancing V2"""
from typing import Dict


async def get(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
) -> Dict:
    """
    Pass required params to get a load balancer resource.

    Args:
        name(str): The name of the Idem state.
        resource_id(str, Optional): AWS ELBv2 Load Balancer ARN to identify the resource.

    Examples:

    Using in a state:

    .. code-block:: yaml

        my_unmanaged_resource:
          exec.run:
            - path: aws.elbv2.load_balancer.get
            - kwargs:
                name: my_resource
                resource_id: resource_id

    Calling this exec function from the cli with resource_id:

    .. code-block:: bash

        idem exec aws.elbv2.load_balancer.get resource_id="resource_id" name="name"

    Calling this exec module function from within a state module in pure python

    .. code-block:: python

        async def state_function(hub, ctx, resource_id, **kwargs):
            ret = await hub.exec.aws.elbv2.load_balancer.get(ctx, resource_id=resource_id, name=name)


    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.tool.aws.elbv2.load_balancer.search_raw(
        ctx=ctx, name=name, resource_id=resource_id
    )
    if not ret["result"]:
        if "LoadBalancerNotFoundException" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.elbv2.load_balancer", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["LoadBalancers"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.elbv2.load_balancer", name=name
            )
        )
        return result

    resource_id = ret["ret"]["LoadBalancers"][0].get("LoadBalancerArn")
    tags = attributes = []
    if resource_id:
        tags_ret = await hub.exec.boto3.client.elbv2.describe_tags(
            ctx, ResourceArns=[resource_id]
        )

        if not tags_ret["result"]:
            result["comment"] = list(tags_ret["comment"])
        else:
            if tags_ret["result"] and tags_ret.get("ret")["TagDescriptions"]:
                tags = (tags_ret.get("ret").get("TagDescriptions")[0]).get("Tags")

        attributes_ret = (
            await hub.exec.boto3.client.elbv2.describe_load_balancer_attributes(
                ctx, LoadBalancerArn=resource_id
            )
        )
        if not attributes_ret.get("result"):
            result["comment"] += list(attributes_ret["comment"])
        else:
            if attributes_ret.get("ret") and attributes_ret.get("ret").get(
                "Attributes"
            ):
                attributes = attributes_ret["ret"].get("Attributes")
    result[
        "ret"
    ] = hub.tool.aws.elbv2.conversion_utils.convert_raw_load_balancer_to_present(
        raw_resource=ret["ret"]["LoadBalancers"][0],
        idem_resource_name=name,
        tags=hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags),
        attributes=attributes,
    )
    return result
