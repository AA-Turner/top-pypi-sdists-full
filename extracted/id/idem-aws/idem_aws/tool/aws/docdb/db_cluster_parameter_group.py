import copy
from collections import OrderedDict
from typing import Any
from typing import Dict
from typing import List

STATE_NAME = "aws.docdb.db_cluster_parameter_group"


async def search_raw(hub, ctx, filters: List = None, resource_id: str = None) -> Dict:
    """
    Fetch one or more docdb db_cluster_parameter_group objects in its raw form.

    Args:
        filters(list, Optional): list of filters for boto3 call
        resource_id(str, Optional): Document DB Cluster Parameter Group Name

    Returns:
        .. code-block:: python
        {"result": True|False, "comment": A message List, "ret": Dict}
    """

    result = dict(comment=[], ret=None, result=True)
    syntax_validation = hub.tool.aws.search_utils.search_filter_syntax_validation(
        filters=filters
    )
    if not syntax_validation["result"]:
        result["result"] = False
        result["comment"] = list(syntax_validation["comment"])
        return result
    boto3_filter = hub.tool.aws.search_utils.convert_search_filter_to_boto3(
        filters=filters
    )

    ret = await hub.exec.boto3.client.docdb.describe_db_cluster_parameter_groups(
        ctx,
        DBClusterParameterGroupName=resource_id if resource_id else None,
        Filters=boto3_filter,
    )
    result["result"] = ret["result"]
    result["comment"] = list(ret["comment"])
    result["ret"] = ret["ret"]
    return result


async def update(
    hub,
    ctx,
    name: str,
    resource_id: str,
    desired_state: Dict,
    is_created: bool,
) -> Dict[str, Any]:
    result = dict(comment=[], old_state=None, new_state=None, result=True)
    if ctx.get("test", False) and is_created:
        current_state = desired_state
    else:
        current_state_result = await hub.exec.aws.docdb.db_cluster_parameter_group.get(
            ctx=ctx, name=name, resource_id=resource_id
        )
        if not (
            current_state_result
            and current_state_result["result"]
            and current_state_result["ret"]
        ):
            result["result"] = False
            result["comment"] = current_state_result["comment"]
            return result
        current_state = current_state_result["ret"]
    if not is_created:
        result["old_state"] = current_state
    resource_arn = current_state.get("db_cluster_parameter_group_arn")
    params_to_modify = {}
    plan_state = copy.deepcopy(current_state)

    if None not in (
        desired_state,
        desired_state["parameters"],
    ) and not hub.tool.aws.state_comparison_utils.are_lists_identical(
        current_state["parameters"], desired_state["parameters"]
    ):
        params_to_modify["Parameters"] = desired_state["parameters"]
        plan_state["parameters"] = desired_state["parameters"]

    if params_to_modify:
        if ctx.get("test", False):
            if not is_created:
                result["comment"].append(
                    hub.tool.aws.comment_utils.would_update_comment(
                        resource_type=STATE_NAME, name=name
                    )
                )
        else:
            modify_db_cluster_parameter_group_result = (
                await hub.exec.boto3.client.docdb.modify_db_cluster_parameter_group(
                    ctx, DBClusterParameterGroupName=resource_id, **params_to_modify
                )
            )
            if not modify_db_cluster_parameter_group_result["result"]:
                result["comment"] = modify_db_cluster_parameter_group_result["comment"]
                result["result"] = False
                return result
            if not is_created:
                result["comment"].append(
                    hub.tool.aws.comment_utils.update_comment(
                        resource_type=STATE_NAME, name=name
                    )
                )

    old_tags = current_state.get("tags")
    new_tags = desired_state.get("tags")
    if new_tags is not None and new_tags != old_tags:
        update_tags_ret = await hub.tool.aws.docdb.tag.update_tags(
            ctx=ctx, resource_arn=resource_arn, old_tags=old_tags, new_tags=new_tags
        )
        if not update_tags_ret["result"]:
            result["comment"] = update_tags_ret["comment"]
            result["result"] = False
            return result
        if not is_created:
            result["comment"] = hub.tool.aws.comment_utils.update_comment(
                resource_type=STATE_NAME, name=name
            )
            result["comment"] += update_tags_ret["comment"]

        if ctx.get("test", False) and update_tags_ret["ret"] is not None:
            plan_state["tags"] = update_tags_ret["ret"]
            if not is_created:
                result["comment"] = hub.tool.aws.comment_utils.would_update_comment(
                    resource_type=STATE_NAME, name=resource_id
                )
                result["comment"] += update_tags_ret["comment"]

    # set new_state
    if ctx.get("test", False):
        result["new_state"] = plan_state
    else:
        current_db_cluster_parameter_group_result = (
            await hub.exec.aws.docdb.db_cluster_parameter_group.get(
                ctx=ctx, name=name, resource_id=resource_id
            )
        )
        if not (
            current_db_cluster_parameter_group_result
            and current_db_cluster_parameter_group_result["result"]
            and current_db_cluster_parameter_group_result["ret"]
        ):
            result["result"] = False
            result["comment"] += current_db_cluster_parameter_group_result["comment"]
            return result
        result["new_state"] = current_db_cluster_parameter_group_result["ret"]

    return result


def convert_raw_db_cluster_parameter_group_to_present(
    hub,
    raw_resource: Dict[str, Any],
    idem_resource_name: str,
    tags: List = None,
    parameters: List[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    raw_resource["Parameters"] = parameters
    resource_parameters = OrderedDict(
        {
            "DBClusterParameterGroupName": "resource_id",
            "DBParameterGroupFamily": "db_parameter_group_family",
            "Description": "description",
            "Parameters": "parameters",
            "DBClusterParameterGroupArn": "db_cluster_parameter_group_arn",
        }
    )
    resource_translated = {"name": raw_resource.get("DBClusterParameterGroupName")}
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    if tags:
        resource_translated["tags"] = tags
    return resource_translated
