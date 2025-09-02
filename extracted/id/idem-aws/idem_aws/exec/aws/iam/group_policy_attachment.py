"""Exec module for managing IAM Group Policy Attachment."""
from typing import Any
from typing import Dict


async def get(
    hub,
    ctx,
    name: str,
    group: str,
    policy_arn: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Get managed policy attached to a group.

    Args:
        hub: required for functions in hub.

        ctx: context.

        name(str): An Idem name of the state for logging.

        group(str): The group name to attach the policy to.

        policy_arn(str, Optional): Policy ARN.

        resource_id(str, Optional): Policy ARN
    """
    result = dict(comment=[], result=True, ret=None)

    ret = await hub.exec.boto3.client.iam.list_attached_group_policies(
        ctx, GroupName=group
    )
    if not resource_id:
        resource_id = policy_arn

    if not ret["result"]:
        if "NoSuchEntity" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.iam.group_policy_attachment", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["result"] = False
        result["comment"] += list(ret["comment"])
        return result

    if ret["result"]:
        attached_group_policies_list = ret["ret"].get("AttachedPolicies")
        if attached_group_policies_list:
            policy_arn_list = [
                policy.get("PolicyArn") for policy in attached_group_policies_list
            ]
            if resource_id in policy_arn_list:
                result[
                    "ret"
                ] = hub.tool.aws.iam.conversion_utils.convert_raw_group_policy_attachment_to_present(
                    group=group, policy_arn=resource_id
                )
            else:
                result["comment"].append(
                    hub.tool.aws.comment_utils.get_empty_comment(
                        resource_type="aws.iam.group_policy_attachment", name=name
                    )
                )

    return result
