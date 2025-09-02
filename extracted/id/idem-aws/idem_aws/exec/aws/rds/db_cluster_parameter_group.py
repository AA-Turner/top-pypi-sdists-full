from typing import Dict

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    name,
    resource_id: str,
) -> Dict:
    """
    Use an un-managed db_cluster_parameter_group as a data-source. Supply resource_id as a filter.

    Args:
        name(str): The name of the Idem state.
        resource_id(str):  AWS DB Cluster Parameter Group name.
    """

    result = dict(comment=[], ret=None, result=True)

    resource_ret = await hub.exec.boto3.client.rds.describe_db_cluster_parameter_groups(
        ctx, DBClusterParameterGroupName=resource_id
    )
    if not resource_ret["result"]:
        if "ParameterGroupNotFound" in str(resource_ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.rds.db_cluster_parameter_group", name=name
                )
            )
            result["comment"] += list(resource_ret["comment"])
            return result
        result["comment"] += list(resource_ret["comment"])
        result["result"] = resource_ret["result"]
        return result

    if not resource_ret["ret"]["DBClusterParameterGroups"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.rds.db_cluster_parameter_group", name=name
            )
        )
        return result

    resource = resource_ret["ret"]["DBClusterParameterGroups"][0]
    resource_id = resource.get("DBClusterParameterGroupName")
    resource_arn = resource.get("DBClusterParameterGroupArn")
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

    ret_parameter = await hub.exec.boto3.client.rds.describe_db_cluster_parameters(
        ctx, DBClusterParameterGroupName=resource_id
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
    ] = hub.tool.aws.rds.conversion_utils.convert_raw_db_cluster_parameter_group_to_present(
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
    """
    Use an un-managed db_cluster_parameter_groups as a data-source.

    Args:
        name (str, Optional):
            The name of the Idem state.

    """
    result = dict(comment=[], ret=None, result=True)

    db_cluster_parameter_groups = []
    ret = await hub.exec.boto3.client.rds.describe_db_cluster_parameter_groups(ctx)
    if not ret["result"]:
        result["result"] = ret["result"]
        result["comment"] = ret["comment"]
        return result

    if not ret["ret"]["DBClusterParameterGroups"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.rds.db_cluster_parameter_group", name=name
            )
        )
        return result

    for resource in ret["ret"]["DBClusterParameterGroups"]:
        resource_id = resource.get("DBClusterParameterGroupName")
        resource_arn = resource.get("DBClusterParameterGroupArn")
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
                f"Could not get tags for db_cluster_parameter_groups {resource_id} {ret_tag['comment']}"
            )

        ret_parameter = await hub.exec.boto3.client.rds.describe_db_cluster_parameters(
            ctx, DBClusterParameterGroupName=resource_id
        )
        parameters = []
        if ret_parameter["result"]:
            parameters = ret_parameter["ret"]["Parameters"]
        else:
            hub.log.debug(
                f"Could not get parameters for db_cluster_parameter_groups {resource_id} {ret_parameter['comment']}"
            )

        converted_db_cluster_parameter_group = hub.tool.aws.rds.conversion_utils.convert_raw_db_cluster_parameter_group_to_present(
            raw_resource=resource,
            tags=tags,
            parameters=parameters,
        )
        db_cluster_parameter_groups.append(converted_db_cluster_parameter_group)

    result["ret"] = db_cluster_parameter_groups
    return result
