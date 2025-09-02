import copy
from typing import Any
from typing import Dict
from typing import List

STATE_NAME = "aws.neptune.db_parameter_group"


async def search_raw(hub, ctx, resource_id: str = None, filters: List = None):
    """Fetch one or more neptune db_parameter_group objects in its raw form.

    Args:
        resource_id (str, Optional):
            resource_id maps to DBParameterGroupName attribute for AWS neptune service

        filters (list, Optional):
            This is not supported for AWS neptune yet as per AWS documentation.

    Returns Raw representation of one or more AWS neptune DBParameterGroup objects.
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
    ret = await hub.exec.boto3.client.neptune.describe_db_parameter_groups(
        ctx,
        DBParameterGroupName=resource_id if resource_id else None,
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
    """
    Updates the db_parameter_group represented by resource_id which is the db_parameter_group_name to the desired state.
    If is_created flag is set to True, the comment in result is not updated as it is assumed that
    the resource is being updated right after it was created to apply remaining parameters.
    Only following parameters can be modified:
    - parameters
    - tags
    """
    result = dict(comment=[], old_state=None, new_state=None, result=True)
    if ctx.get("test", False) and is_created:
        current_state = desired_state
    else:
        current_state_result = await hub.exec.aws.neptune.db_parameter_group.get(
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
    resource_arn = current_state.get("db_parameter_group_arn")
    params_to_modify = {}
    plan_state = copy.deepcopy(current_state)

    if desired_state[
        "parameters"
    ] and not hub.tool.aws.state_comparison_utils.are_lists_identical(
        current_state["parameters"], desired_state["parameters"]
    ):
        params_to_modify["Parameters"] = desired_state["parameters"]
        plan_state["parameters"] = desired_state["parameters"]

    if params_to_modify:
        if ctx.get("test", False):
            if not is_created:
                result["comment"] = hub.tool.aws.comment_utils.would_update_comment(
                    resource_type=STATE_NAME, name=name
                )
        else:
            modify_db_parameter_group_result = (
                await hub.exec.boto3.client.neptune.modify_db_parameter_group(
                    ctx, DBParameterGroupName=resource_id, **params_to_modify
                )
            )
            if not modify_db_parameter_group_result["result"]:
                result["comment"] = modify_db_parameter_group_result["comment"]
                result["result"] = False
                return result
            if not is_created:
                result["comment"] = result[
                    "comment"
                ] + hub.tool.aws.comment_utils.update_comment(
                    resource_type=STATE_NAME, name=name
                )

    # modify tags if it has changed
    old_tags = current_state.get("tags")
    new_tags = desired_state.get("tags")
    if new_tags is not None and new_tags != old_tags:
        # below code updates tags on AWS only if it is not a test run
        update_tags_ret = await hub.tool.aws.neptune.tag.update_tags(
            ctx=ctx,
            resource_arn=resource_arn,
            old_tags=old_tags,
            new_tags=new_tags,
        )
        if not update_tags_ret["result"]:
            result["comment"] = update_tags_ret["comment"]
            result["result"] = False
            hub.log.debug(f"Failed updating tags for {STATE_NAME} '{name}'")
            return result
        # update comment if tags were updated
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
        current_db_parameter_group_result = (
            await hub.exec.aws.neptune.db_parameter_group.get(
                ctx=ctx, name=name, resource_id=resource_id
            )
        )
        if not (
            current_db_parameter_group_result
            and current_db_parameter_group_result["result"]
            and current_db_parameter_group_result["ret"]
        ):
            result["result"] = False
            result["comment"] += current_db_parameter_group_result["comment"]
            return result
        result["new_state"] = current_db_parameter_group_result["ret"]

    return result
