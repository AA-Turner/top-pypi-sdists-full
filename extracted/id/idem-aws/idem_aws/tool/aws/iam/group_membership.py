from typing import Any
from typing import Dict
from typing import List


async def update(
    hub,
    ctx,
    resource_id: str,
    before: Dict[str, Any],
    users: List,
):
    """Updates association of users in IAM Group.

    Args:
        hub: required for functions in hub.
        ctx: context.
        resource_id: AWS IAM Group name.
        before(Dict): Existing resource parameters in Amazon Web Services.
        users(List): List of users

    Returns:
        {"result": True|False, "comment": A message Tuple, "ret": Dict}

    """
    result = dict(comment=[], result=True, ret=None)
    if set(before.get("users")) != set(users):
        users_to_add = list(set(users).difference(before.get("users")))
        users_to_remove = list(set(before.get("users")).difference(users))

        if users_to_remove:
            for user in users_to_remove:
                if not ctx.get("test", False):
                    remove_usr_ret = (
                        await hub.exec.boto3.client.iam.remove_user_from_group(
                            ctx=ctx, GroupName=resource_id, UserName=user
                        )
                    )
                    if not remove_usr_ret["result"]:
                        result["comment"] = remove_usr_ret["comment"]
                        result["result"] = False
                        return result

        if users_to_add:
            for user in users_to_add:
                if not ctx.get("test", False):
                    add_usr_ret = await hub.exec.boto3.client.iam.add_user_to_group(
                        ctx, GroupName=resource_id, UserName=user
                    )
                    if not add_usr_ret["result"]:
                        result["comment"] = add_usr_ret["comment"]
                        result["result"] = False
                        return result

        result["ret"] = {}
        result["ret"]["users"] = users
        if ctx.get("test", False):
            result["comment"] = hub.tool.aws.comment_utils.would_update_comment(
                resource_type="aws.iam.group_membership", name=resource_id
            )
        else:
            result["comment"] = hub.tool.aws.comment_utils.update_comment(
                resource_type="aws.iam.group_membership", name=resource_id
            )

    return result
