from typing import Any
from typing import Dict


async def update(
    hub,
    ctx,
    resource_id: str,
    before: Dict[str, Any],
    group_name: str,
    path: str,
):
    """
    Updates the IAM Group name and Path.

    Args:
        hub: required for functions in hub.
        ctx: context.
        resource_id: AWS IAM Group name.
        before(Dict): Existing resource parameters in Amazon Web Services.
        group_name(Str): IAM Group name
        path(str): Path Name of IAM group

    Returns:
        {"result": True|False, "comment": A message Tuple, "ret": Dict}

    """
    result = dict(comment=[], result=True, ret=None)
    update_payload = {}

    if before.get("group_name") != group_name:
        update_payload["NewGroupName"] = group_name
    if before.get("path") != path:
        update_payload["NewPath"] = path

    if update_payload:
        result["ret"] = {}
        if not ctx.get("test", False):
            update_ret = await hub.exec.boto3.client.iam.update_group(
                ctx=ctx, GroupName=resource_id, **update_payload
            )
            if not update_ret["result"]:
                result["comment"] = update_ret["comment"]
                result["result"] = False
                return result

            result["comment"] = hub.tool.aws.comment_utils.update_comment(
                resource_type="aws.iam.group", name=resource_id
            )
        if "NewGroupName" in update_payload:
            result["ret"]["group_name"] = update_payload["NewGroupName"]
        if "NewPath" in update_payload:
            result["ret"]["path"] = update_payload["NewPath"]

    return result
