"""Exec module for managing IAM Groups."""


async def get(hub, ctx, name: str, resource_id: str):
    """Get an IAM group from AWS.

    Provide group name as input.

    Args:
        hub: required for functions in hub.
        ctx: context.
        name(str): An Idem name of the IAM group.
        resource_id(str, Optional): AWS IAM group name.

    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.exec.boto3.client.iam.get_group(ctx, GroupName=resource_id)
    if not ret["result"]:
        if "NoSuchEntity" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.iam.group", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["result"] = False
        result["comment"] += list(ret["comment"])
        return result

    result["ret"] = hub.tool.aws.iam.conversion_utils.convert_raw_group_to_present(
        raw_resource=ret["ret"]["Group"], idem_resource_name=resource_id
    )
    return result
