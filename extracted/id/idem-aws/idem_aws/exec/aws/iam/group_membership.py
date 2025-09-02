"""Exec module for managing IAM Group Membership."""


async def get(hub, ctx, name: str, resource_id: str):
    """Get IAM Group membership.

    Provide group name as input.

    Args:
        hub: required for functions in hub.

        ctx: context.

        name(str): An Idem name of the IAM group.

        resource_id(str): IAM Group Name
    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.exec.boto3.client.iam.get_group(ctx, GroupName=resource_id)
    if not ret["result"]:
        if "NoSuchEntity" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.iam.group_membership", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["result"] = False
        result["comment"] += list(ret["comment"])
        return result

    users = ret["ret"].get("Users")

    result[
        "ret"
    ] = hub.tool.aws.iam.conversion_utils.convert_raw_group_membership_to_present(
        group=resource_id, users=[user.get("UserName") for user in users]
    )

    return result
