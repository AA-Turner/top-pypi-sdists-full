"""State module for managing Amazon Elasticache Subnet Groups."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List


__contracts__ = ["resource"]
TREQ = {
    "present": {
        "require": [
            "aws.ec2.subnet.present",
        ],
    },
}


async def present(
    hub,
    ctx,
    name: str,
    subnet_ids: List[str],
    cache_subnet_group_description: str,
    resource_id: str = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass("Tag", [("Key", str), ("Value", str, field(default=None))])
    ] = None,
) -> Dict[str, Any]:
    """Creates an AWS Elasticache Subnet Group.

    Args:
        name(str):
            An Idem name of the resource
        resource_id(str, Optional):
            The name of the AWS Elasticache Subnet Group in Amazon Web Services.
        cache_subnet_group_description(str):
            A description for the cache subnet group.
        subnet_ids(list):
            A list of VPC subnet IDs for the cache subnet group.
        tags(dict or list, Optional):
            Dict in the format of ``{tag-key: tag-value}`` or List of tags in the format of
            ``[{"Key": tag-key, "Value": tag-value}]`` to associate with the subnet group.

            * Key (*str*):
                The key of the tag.
            * Value (*str*):
                The value of the tag.

    Request Syntax:
      .. code-block:: sls

        [idem_test_aws_elasticache_cache_subnet_group]:
          aws.elasticache.cache_subnet_group.present:
            - name: 'string'
            - resource_id: 'string'
            - cache_subnet_group_description: 'string'
            - subnet_id:
                - 'string'
            - tags:
                - Key: 'string'
                  Value: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_elasticache_cache_subnet_group:
              aws.elasticache.cache_subnet_group.present:
                - name: 'idem_test_cache_subnet_group'
                - cache_subnet_group_description: 'My Elasticache Subnet Group'
                - subnet_id:
                  - 'subnet-12345678'
                - tags:
                    - Key: 'provider'
                      Value: 'idem'
    """
    result = dict(comment=[], name=name, old_state=None, new_state=None, result=True)
    before = None
    resource_updated = False
    are_tags_updated = False
    resource_arn = str
    if resource_id:
        before = await hub.exec.boto3.client.elasticache.describe_cache_subnet_groups(
            ctx, CacheSubnetGroupName=resource_id
        )
    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)

    try:
        if before and before["result"] and before["ret"]["CacheSubnetGroups"]:
            convert_ret = await hub.tool.aws.elasticache.conversion_utils.convert_raw_elasticache_subnet_to_present_async(
                ctx=ctx,
                raw_resource=before["ret"]["CacheSubnetGroups"][0],
                idem_resource_name=name,
            )
            result["result"] = convert_ret["result"]
            if not result["result"]:
                result["comment"] += convert_ret["comment"]
            result["old_state"] = convert_ret["ret"]
            plan_state = copy.deepcopy(result["old_state"])
            if cache_subnet_group_description != result["old_state"].get(
                "cache_subnet_group_description"
            ) or not hub.tool.aws.state_comparison_utils.are_lists_identical(
                subnet_ids, result["old_state"].get("subnet_ids")
            ):
                if not ctx.get("test", False):
                    update_ret = await hub.exec.boto3.client.elasticache.modify_cache_subnet_group(
                        ctx=ctx,
                        CacheSubnetGroupName=name,
                        CacheSubnetGroupDescription=cache_subnet_group_description,
                        SubnetIds=subnet_ids,
                    )
                    result["comment"] += update_ret["comment"]
                    result["result"] = update_ret["result"]
                    resource_updated = resource_updated or bool(update_ret["ret"])
                else:
                    if cache_subnet_group_description is not None:
                        plan_state[
                            "cache_subnet_group_description"
                        ] = cache_subnet_group_description
                    if subnet_ids is not None:
                        plan_state["subnet_ids"] = subnet_ids
            resource_arn = before["ret"]["CacheSubnetGroups"][0]["ARN"]
            if tags is not None and tags != result["old_state"].get("tags"):
                # Update tags
                update_ret = (
                    await hub.tool.aws.elasticache.elasticache_utils.update_tags(
                        ctx=ctx,
                        resource_arn=resource_arn,
                        old_tags=result["old_state"].get("tags"),
                        new_tags=tags,
                    )
                )
                result["comment"] += update_ret["comment"]
                result["result"] = result["result"] and update_ret["result"]
                are_tags_updated = bool(update_ret["result"])
                resource_updated = resource_updated or are_tags_updated
                if ctx.get("test", False) and are_tags_updated:
                    plan_state["tags"] = update_ret["ret"]
                    result["comment"] += [
                        f"Would update tags for aws.elasticache.cache_subnet_group {name}"
                    ]
        else:
            if ctx.get("test", False):
                result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                    enforced_state={},
                    desired_state={
                        "name": name,
                        "cache_subnet_group_description:": cache_subnet_group_description,
                        "subnet_ids": subnet_ids,
                        "tags": tags,
                    },
                )
                result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                    resource_type="aws.elasticache.cache_subnet_group", name=name
                )
                return result

            ret = await hub.exec.boto3.client.elasticache.create_cache_subnet_group(
                ctx,
                CacheSubnetGroupName=name,
                CacheSubnetGroupDescription=cache_subnet_group_description,
                SubnetIds=subnet_ids,
                Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
                if tags
                else None,
            )
            resource_id = name
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result
            resource_arn = ret["ret"]["CacheSubnetGroup"]["ARN"]
            result["comment"] = hub.tool.aws.comment_utils.create_comment(
                resource_type="aws.elasticache.cache_subnet_group", name=name
            )
    except hub.tool.boto3.exception.ClientError as e:
        result["result"] = False
        result["comment"] += [f"{e.__class__.__name__}: {e}"]
    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif (not before) or resource_updated:
            after = (
                await hub.exec.boto3.client.elasticache.describe_cache_subnet_groups(
                    ctx, CacheSubnetGroupName=resource_id
                )
            )
            if after and after.get("ret"):
                convert_ret = await hub.tool.aws.elasticache.conversion_utils.convert_raw_elasticache_subnet_to_present_async(
                    ctx=ctx,
                    raw_resource=after["ret"]["CacheSubnetGroups"][0],
                    idem_resource_name=name,
                )
                result["result"] = convert_ret["result"]
                if not result["result"]:
                    result["comment"] += convert_ret["comment"]
                result["new_state"] = convert_ret.get("ret")
            else:
                result["result"] = result["result"] and after["result"]
                if not result["result"]:
                    result["comment"] += after["comment"]
                    return result
        else:
            result["new_state"] = copy.deepcopy(result["old_state"])
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False
    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deletes the specified AWS Elasticache Subnet Group.

    .. warning::
        You cannot delete a default cache subnet group or one that is associated with any clusters.

    Args:
        name(str):
            An Idem name of the resource.
        resource_id(str, Optional):
            The name of the AWS Elasticache Subnet Group in Amazon Web Services.

            .. warning::
              Idem automatically considers this resource being absent if this field is not specified.

    Request Syntax:
      .. code-block:: sls

        [idem_test_aws_elasticache_cache_subnet_group]:
          aws.elasticache.cache_subnet_group.absent:
            - name: 'string'
            - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_elasticache_cache_subnet_group:
              aws.elasticache.cache_subnet_group.absent:
                - name: 'idem_test_cache_subnet_group'
                - resource_id: 'my-subnet-group'
    """
    result = dict(comment=[], name=name, old_state=None, new_state=None, result=True)

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.elasticache.cache_subnet_group", name=name
        )
        return result

    before = await hub.exec.boto3.client.elasticache.describe_cache_subnet_groups(
        ctx, CacheSubnetGroupName=resource_id
    )
    if not before or not before["result"] or not before["ret"].get("CacheSubnetGroups"):
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.elasticache.cache_subnet_group", name=name
        )
        return result
    else:
        convert_ret = await hub.tool.aws.elasticache.conversion_utils.convert_raw_elasticache_subnet_to_present_async(
            ctx=ctx,
            raw_resource=before["ret"]["CacheSubnetGroups"][0],
            idem_resource_name=name,
        )
        result["result"] = convert_ret["result"]
        if not result["result"]:
            result["comment"] += convert_ret["comment"]
        result["old_state"] = convert_ret["ret"]
        if ctx.get("test", False):
            result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
                resource_type="aws.elasticache.cache_subnet_group", name=name
            )
            return result
        try:
            ret = await hub.exec.boto3.client.elasticache.delete_cache_subnet_group(
                ctx, CacheSubnetGroupName=resource_id
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result
            result["comment"] = hub.tool.aws.comment_utils.delete_comment(
                resource_type="aws.elasticache.cache_subnet_group", name=name
            )
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describes Elasticache Subnet Groups in a way that can be recreated/managed with the corresponding "present" function.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.elasticache.cache_subnet_group
    """
    result = {}
    ret = await hub.exec.boto3.client.elasticache.describe_cache_subnet_groups(ctx)
    if not ret["result"]:
        hub.log.warning(f"Could not describe cache_subnet_groups {ret['comment']}")
        return {}

    for resource in ret["ret"]["CacheSubnetGroups"]:
        resource_id = resource.get("CacheSubnetGroupName")
        convert_ret = await hub.tool.aws.elasticache.conversion_utils.convert_raw_elasticache_subnet_to_present_async(
            ctx=ctx,
            raw_resource=resource,
            idem_resource_name=resource_id,
        )
        if not convert_ret["result"]:
            hub.log.warning(
                f"Could not describe elasticache subnet group '{resource_id}' with error {convert_ret['comment']}"
            )
            continue
        resource_translated = convert_ret.get("ret")
        result[resource_id] = {
            "aws.elasticache.cache_subnet_group.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }
    return result
