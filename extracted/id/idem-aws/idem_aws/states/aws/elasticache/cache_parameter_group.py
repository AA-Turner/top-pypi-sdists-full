"""State module for managing Amazon Elasticache Parameter Groups."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    cache_parameter_group_family: str,
    description: str,
    resource_id: str = None,
    parameter_name_values: List[
        make_dataclass(
            """A list of parameter names and values for the parameter update."""
            "ParameterNameValue",
            [("ParameterName", str), ("ParameterValue", str, field(default=None))],
        )
    ] = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass("Tag", [("Key", str), ("Value", str, field(default=None))])
    ] = None,
) -> Dict[str, Any]:
    """Creates an AWS Elasticache Parameter Group.

    Args:
        name(str):
            An Idem name of the resource
        resource_id(str, Optional):
            The name of the AWS Elasticache Parameter Group in Amazon Web Services.
        cache_parameter_group_family(str):
            The name of the cache parameter group family that the cache parameter group can be used with.
            Valid values are ``memcached1.4``, ``memcached1.5``, ``memcached1.6``, ``redis2.6``, ``redis2.8``,
            ``redis3.2``, ``redis4.0``, ``redis5.0``, and ``redis6.x``.
        description(str):
            A user-specified description for the cache parameter group.
        parameter_name_values(list, Optional):
            A list of parameter names and values for the parameter update.
            You must supply at least one parameter name and value; subsequent arguments are optional.
            A maximum of 20 parameters may be modified per request.

            * ParameterName (*str, Optional*):
                The name of the parameter.

            * ParameterValue (*str, Optional*):
                The value of the parameter.

        tags(dict or list, Optional):
            Dict in the format of ``{tag-key: tag-value}`` or List of tags in the format of
            ``[{"Key": tag-key, "Value": tag-value}]`` to associate with the parameter group.

            * Key (*str*):
                The key of the tag.
            * Value (*str*):
                The value of the tag.

    Request Syntax:
      .. code-block:: sls

        [idem_test_aws_elasticache_cache_parameter_group]:
          aws.elasticache.cache_parameter_group.present:
            - name: 'string'
            - resource_id: 'string'
            - cache_parameter_group_family: 'memcached1.4|memcached1.5|memcached1.6|redis2.6|redis2.8|redis3.2|redis4.0|redis5.0|redis6.x'
            - description: 'string'
            - parameter_name_values:
                - ParameterName: 'string'
                  ParameterValue: 'string'
            - tags:
                - Key: 'string'
                  Value: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_elasticache_cache_parameter_group:
              aws.elasticache.cache_parameter_group.present:
                - name: 'idem_test_cache_parameter_group'
                - cache_parameter_group_family: 'redis6.x'
                - description: 'My Elasticache Parameter Group'
                - parameter_name_values:
                  - ParameterName: 'acllog-max-len'
                    ParameterValue: '128'
                - tags:
                    - Key: 'provider'
                      Value: 'idem'
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    if resource_id:
        before = (
            await hub.exec.boto3.client.elasticache.describe_cache_parameter_groups(
                ctx, CacheParameterGroupName=resource_id
            )
        )
    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)

    is_updated = False
    are_tags_updated = False
    old_cache_parameter_group = {}
    resource_arn = str
    parameters = []

    if before and before["result"]:
        try:
            convert_ret = await hub.tool.aws.elasticache.conversion_utils.convert_raw_elasticache_parameter_group_to_present_async(
                ctx=ctx,
                raw_resource=before["ret"]["CacheParameterGroups"][0],
                idem_resource_name=resource_id,
            )
            result["result"] = convert_ret["result"]
            if not result["result"]:
                result["comment"] += convert_ret["comment"]
            result["old_state"] = convert_ret["ret"]

            old_cache_parameter_group = copy.deepcopy(result["old_state"])
            plan_state = old_cache_parameter_group
            parameters = result["old_state"].get("parameter_name_values")
            resource_arn = result["old_state"].get("arn")
            result["comment"] += [
                f"aws.elasticache.cache_parameter_group '{name}' already exists"
            ]

            # Update tags
            if tags is not None and tags != result["old_state"].get("tags"):
                update_tags_ret = (
                    await hub.tool.aws.elasticache.elasticache_utils.update_tags(
                        ctx=ctx,
                        resource_arn=resource_arn,
                        old_tags=result["old_state"].get("tags"),
                        new_tags=tags,
                    )
                )
                if not update_tags_ret["result"]:
                    result["comment"] += update_tags_ret["comment"]
                    result["result"] = False
                    return result
                are_tags_updated = bool(update_tags_ret["result"])
                if ctx.get("test", False) and are_tags_updated:
                    plan_state["tags"] = update_tags_ret["ret"]
                    result["comment"] += [
                        f"Would update tags for aws.elasticache.cache_parameter_group {name}"
                    ]
        except Exception as e:
            result["comment"] += [str(e)]
            result["result"] = False
            return result
    else:
        try:
            if ctx.get("test", False):
                result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                    enforced_state={},
                    desired_state={
                        "name": name,
                        "cache_parameter_group_family": cache_parameter_group_family,
                        "description": description,
                        "parameter_name_values": parameter_name_values,
                        "tags": tags,
                    },
                )
                result["comment"] += [
                    f"Would create aws.elasticache.cache_parameter_group '{name}'"
                ]
                return result

            ret = await hub.exec.boto3.client.elasticache.create_cache_parameter_group(
                ctx,
                CacheParameterGroupName=name,
                CacheParameterGroupFamily=cache_parameter_group_family,
                Description=description,
                Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
                if tags
                else None,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result
            resource_id = name
            after_parameters = (
                await hub.exec.boto3.client.elasticache.describe_cache_parameters(
                    ctx, CacheParameterGroupName=resource_id
                )
            )
            if not after_parameters["result"]:
                result["comment"] += after_parameters["comment"]
                result["result"] = False
                return result
            parameters = after_parameters["ret"].get("Parameters")
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False
            return result

    # To add,remove,update the ParameterNameValues.
    # ParameterNameValues are defined automatically when a resource is created,
    # so this needs to be done regardless of whether the resource exists before.
    if parameter_name_values:
        update_parameter = (
            await hub.tool.aws.elasticache.parameters.update_elasticache_parameters(
                ctx=ctx,
                resource_id=resource_id,
                old_parameters=parameters,
                parameter_name_values=parameter_name_values,
            )
        )
        if not update_parameter["result"]:
            result["comment"] += update_parameter["comment"]
            result["result"] = False
            return result
        is_updated = update_parameter["is_updated"]
        if is_updated:
            after_parameters = (
                await hub.exec.boto3.client.elasticache.describe_cache_parameters(
                    ctx, CacheParameterGroupName=resource_id
                )
            )
            if not after_parameters["result"]:
                result["comment"] += after_parameters["comment"]
                result["result"] = False
                return result
            parameters = after_parameters.get("ret").get("Parameters")
        if ctx.get("test", False) and is_updated:
            plan_state["parameter_name_values"] = parameters

    try:
        if ctx.get("test", False):
            new_cache_parameter_group = plan_state
        elif (not (before and before["result"])) or is_updated or are_tags_updated:
            after = (
                await hub.exec.boto3.client.elasticache.describe_cache_parameter_groups(
                    ctx, CacheParameterGroupName=resource_id
                )
            )
            if after and after.get("ret"):
                convert_ret = await hub.tool.aws.elasticache.conversion_utils.convert_raw_elasticache_parameter_group_to_present_async(
                    ctx=ctx,
                    raw_resource=after["ret"]["CacheParameterGroups"][0],
                    idem_resource_name=resource_id,
                )
                result["result"] = convert_ret["result"]
                if not result["result"]:
                    result["comment"] += convert_ret["comment"]
                new_cache_parameter_group = convert_ret.get("ret")
                if not (before and before["result"]):
                    result["comment"] += [
                        f"Created aws.elasticache.cache_parameter_group '{name}'"
                    ]
                elif is_updated or are_tags_updated:
                    result["comment"] += [
                        f"Updated aws.elasticache.cache_parameter_group '{name}'"
                    ]
            else:
                result["result"] = result["result"] and after["result"]
                if not result["result"]:
                    result["comment"] += after["comment"]
                    return result
        else:
            new_cache_parameter_group = copy.deepcopy(old_cache_parameter_group)

        result["old_state"] = old_cache_parameter_group
        result["new_state"] = new_cache_parameter_group

    except Exception as e:
        result["comment"] += [f"{e.__class__.__name__}: {e}"]
        result["result"] = False
    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deletes the specified AWS Elasticache Parameter Group.

    .. warning::
        You cannot delete a cache parameter group if it is associated with any cache clusters.
        You cannot delete the default cache parameter groups in your account.

    Args:
        name(str):
            The name of the AWS Elasticache Parameter Group in Amazon Web Services.
        resource_id(str, Optional):
            The name of the AWS Elasticache Parameter Group in Amazon Web Services.

    Request Syntax:
      .. code-block:: sls

        [idem_test_aws_elasticache_cache_parameter_group]:
          aws.elasticache.cache_parameter_group.absent:
            - name: 'string'
            - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_elasticache_cache_parameter_group:
              aws.elasticache.cache_parameter_group.absent:
                - name: 'idem_test_cache_parameter_group'
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    before = await hub.exec.boto3.client.elasticache.describe_cache_parameter_groups(
        ctx,
        CacheParameterGroupName=name,
    )
    if not (before and before["result"]):
        result["comment"] += [
            f"aws.elasticache.cache_parameter_group '{name}' already absent"
        ]
        return result
    else:
        convert_ret = await hub.tool.aws.elasticache.conversion_utils.convert_raw_elasticache_parameter_group_to_present_async(
            ctx=ctx,
            raw_resource=before["ret"]["CacheParameterGroups"][0],
            idem_resource_name=name,
        )
        result["result"] = convert_ret["result"]
        if not result["result"]:
            result["comment"] += convert_ret["comment"]
        result["old_state"] = convert_ret["ret"]
        if ctx.get("test", False):
            result["comment"] += [
                f"Would delete aws.elasticache.cache_parameter_group '{name}'"
            ]
            return result
        else:
            try:
                ret = await hub.exec.boto3.client.elasticache.delete_cache_parameter_group(
                    ctx,
                    CacheParameterGroupName=name,
                )
                result["result"] = ret["result"]
                if not result["result"]:
                    result["comment"] = ret["comment"]
                    return result
                result["comment"] += [
                    f"Deleted aws.elasticache.cache_parameter_group '{name}'"
                ]
            except hub.tool.boto3.exception.ClientError as e:
                result["comment"] += [f"{e.__class__.__name__}: {e}"]
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describes Elasticache Parameter Groups in a way that can be recreated/managed with the corresponding "present" function.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.elasticache.cache_parameter_group
    """
    result = {}
    ret = await hub.exec.boto3.client.elasticache.describe_cache_parameter_groups(ctx)
    if not ret["result"]:
        hub.log.warning(
            f"Could not describe Elasticache parameter groups {ret['comment']}"
        )
        return {}
    for cache_parameter_group in ret["ret"]["CacheParameterGroups"]:
        resource_id = cache_parameter_group.get("CacheParameterGroupName")
        convert_ret = await hub.tool.aws.elasticache.conversion_utils.convert_raw_elasticache_parameter_group_to_present_async(
            ctx=ctx,
            raw_resource=cache_parameter_group,
            idem_resource_name=resource_id,
        )
        if not convert_ret["result"]:
            hub.log.warning(
                f"Could not describe elasticache parameter group '{resource_id}' with error {convert_ret['comment']}"
            )
            continue
        resource_translated = convert_ret.get("ret")
        result[resource_id] = {
            "aws.elasticache.cache_parameter_group.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }
    return result
