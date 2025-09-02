"""Exec module for managing Elastic Load Balancer V2 target groups"""
from typing import Dict


async def get(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    load_balancer_arn: str = None,
) -> Dict:
    """
    Pass required params to get a target group resource.

    .. note::
        Users can specify one of the following to filter the results: the ARN of the load balancer,
        name of the target group, or the ARN of the given target group.

    Order of precedence of input params while performing search: resource_id, load_balancer_arn and finally name.
    If resource_id is not None, regardless whether the 2 other values are None or not, search always is done by
    resource_id only.

    Args:
        name(str): The name of the AWS ELBv2 Target Group. This name must be unique per region per account.
        resource_id(str, Optional): AWS ELBv2 Target Group ARN to identify the resource.
        load_balancer_arn(str, Optional): The Amazon Resource Name (ARN) of the load balancer.

    Examples:
        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.elbv2.target_group.get
                - kwargs:
                    resource_id: resource_id
                    name: name
                    load_balancer_arn: load_balancer_arn

        Calling this exec function from the cli with resource_id

        .. code-block:: bash

            idem exec aws.elbv2.target_group.get resource_id="resource_id" name="name" load_balancer_arn="load_balancer_arn"

        Calling this exec module function from within a state module in pure python

        .. code-block:: python

            async def state_function(hub, ctx, resource_id, **kwargs):
                ret = await hub.exec.aws.elbv2.target_group.get(ctx, resource_id=resource_id, name=name load_balancer_arn=load_balancer_arn)

    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.tool.aws.elbv2.target_group.search_raw(
        ctx=ctx,
        name=name,
        resource_id=resource_id,
        load_balancer_arn=load_balancer_arn,
    )
    if not ret["result"]:
        if "TargetGroupNotFoundException" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.elbv2.target_group", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] = list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["TargetGroups"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.elbv2.target_group", name=name
            )
        )
        return result

    resource_id = ret["ret"]["TargetGroups"][0].get("TargetGroupArn")
    tags = attributes = targets = []
    if resource_id:
        tags_ret = await hub.exec.boto3.client.elbv2.describe_tags(
            ctx, ResourceArns=[resource_id]
        )
        if not tags_ret["result"]:
            result["comment"] = list(tags_ret["comment"])
            result["result"] = False
            return result
        else:
            if tags_ret["ret"] and tags_ret.get("ret")["TagDescriptions"]:
                tags = (tags_ret["ret"]["TagDescriptions"][0]).get("Tags")

        attributes_ret = (
            await hub.exec.boto3.client.elbv2.describe_target_group_attributes(
                ctx, TargetGroupArn=resource_id
            )
        )
        if not attributes_ret.get("result"):
            result["comment"] = list(attributes_ret["comment"])
            result["result"] = False
            return result
        else:
            if attributes_ret.get("ret") and attributes_ret.get("ret").get(
                "Attributes"
            ):
                attributes = attributes_ret["ret"].get("Attributes")

        targets_ret = await hub.exec.boto3.client.elbv2.describe_target_health(
            ctx, TargetGroupArn=resource_id
        )
        if not targets_ret.get("result"):
            result["comment"] = list(targets_ret["comment"])
            result["result"] = False
            return result
        else:
            if targets_ret.get("ret") and targets_ret["ret"].get(
                "TargetHealthDescriptions"
            ):
                targets = targets_ret["ret"].get("TargetHealthDescriptions")

    result[
        "ret"
    ] = hub.tool.aws.elbv2.conversion_utils.convert_raw_target_group_to_present(
        raw_resource=ret["ret"]["TargetGroups"][0],
        idem_resource_name=name,
        tags=hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags),
        attributes=attributes,
        targets=targets,
    )
    return result
