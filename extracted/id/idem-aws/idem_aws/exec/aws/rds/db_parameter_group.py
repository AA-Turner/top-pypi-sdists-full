"""Exec module for managing db parameter groups."""
from typing import Dict

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    name: str,
) -> Dict:
    """Get DB Parameter Group resource from AWS.

    Args:
        name(str):
            AWS DB Parameter Group name to identify the resource.

    Returns:
        Dict[str, Any]:
            Returns db parameter group in present format

    Examples:
        Calling this exec module function from the cli with filters

        .. code-block:: bash

            idem exec aws.rds.db_parameter_group.get  name=my_resource resource_id=my_resource_id

        Calling this exec module function from within a state module in pure python.

        .. code-block:: python
                await hub.exec.aws.rds.db_parameter_group.get(
                    ctx=ctx,
                    name=name,

        Using in a state:

        .. code-block:: yaml

           my_unmanaged_resource:
              exec.run:
                - path: aws.rds.db_parameter_group.get
                - kwargs:
                    name: my_resource

    """
    result = dict(comment=[], ret=None, result=True)

    resource_ret = await hub.exec.boto3.client.rds.describe_db_parameter_groups(
        ctx, DBParameterGroupName=name
    )
    if not resource_ret["result"]:
        if "DBParameterGroupNotFound" in str(resource_ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.rds.db_parameter_group", name=name
                )
            )
            result["comment"] += list(resource_ret["comment"])
            return result
        result["comment"] += list(resource_ret["comment"])
        result["result"] = resource_ret["result"]
        return result

    if not resource_ret["ret"]["DBParameterGroups"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.rds.db_parameter_group", name=name
            )
        )
        return result

    resource = resource_ret["ret"]["DBParameterGroups"][0]
    resource_id = resource.get("DBParameterGroupName")
    resource_arn = resource.get("DBParameterGroupArn")
    ret_tags = await hub.exec.boto3.client.rds.list_tags_for_resource(
        ctx, ResourceName=resource_arn
    )

    if not ret_tags["result"]:
        result["comment"] += list(ret_tags["comment"])
        result["result"] = ret_tags["result"]
        return result

    tags_list = None
    if ret_tags["ret"]["TagList"]:
        tags_list = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            ret_tags["ret"]["TagList"]
        )

    ret_parameter = await hub.exec.boto3.client.rds.describe_db_parameters(
        ctx, DBParameterGroupName=resource_id
    )

    if not ret_parameter["result"]:
        result["comment"] += list(ret_parameter["comment"])
        result["result"] = ret_parameter["result"]
        return result

    parameters = None
    if ret_parameter["ret"]["Parameters"]:
        parameters = ret_parameter["ret"]["Parameters"]

    result[
        "ret"
    ] = hub.tool.aws.rds.conversion_utils.convert_db_parameter_group_to_present(
        raw_resource=resource,
        tags=tags_list,
        parameters=parameters,
    )

    return result


async def list_(
    hub,
    ctx,
    name: str = None,
) -> Dict:
    """Get DB Parameter Group from AWS.

    Args:
        name(str, Optional):
            The name of the Idem state.

    Returns:
        Dict[str, Any]:
            Returns db_parameter_group in present format

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec aws.rds.db_parameter_group.list name="my_resources"

        Calling this exec module function from within a state module in pure python.

        .. code-block:: python

                await hub.exec.aws.rds.db_parameter_group.list(
                    ctx=ctx,
                    name=name
                )

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.rds.db_parameter_group.list
                - kwargs:
                    name: my_resources
    """
    result = dict(comment=[], ret=None, result=True)

    db_parameter_groups = []
    ret = await hub.exec.boto3.client.rds.describe_db_parameter_groups(ctx)
    if not ret["result"]:
        result["result"] = ret["result"]
        result["comment"] = ret["comment"]
        return result

    if not ret["ret"]["DBParameterGroups"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.rds.db_parameter_group", name=name
            )
        )
        return result

    for resource in ret["ret"]["DBParameterGroups"]:
        resource_id = resource.get("DBParameterGroupName")
        resource_arn = resource.get("DBParameterGroupArn")
        ret_tag = await hub.exec.boto3.client.rds.list_tags_for_resource(
            ctx, ResourceName=resource_arn
        )
        tags = []
        if ret_tag["result"]:
            tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
                ret_tag.get("ret").get("TagList")
            )
        else:
            hub.log.debug(
                f"Could not get tags for db_parameter_groups {resource_id} {ret_tag['comment']}"
            )

        ret_parameter = await hub.exec.boto3.client.rds.describe_db_parameters(
            ctx, DBParameterGroupName=resource_id
        )
        parameters = []
        if ret_parameter["result"]:
            parameters = ret_parameter["ret"]["Parameters"]
        else:
            hub.log.debug(
                f"Could not get parameters for db_parameter_groups {resource_id} {ret_parameter['comment']}"
            )

        converted_db_parameter_group = (
            hub.tool.aws.rds.conversion_utils.convert_db_parameter_group_to_present(
                raw_resource=resource,
                tags=tags,
                parameters=parameters,
            )
        )
        db_parameter_groups.append(converted_db_parameter_group)

    result["ret"] = db_parameter_groups
    return result
