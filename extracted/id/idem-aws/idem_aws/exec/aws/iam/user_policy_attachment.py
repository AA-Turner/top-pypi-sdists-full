from typing import Any
from typing import Dict


async def get(
    hub,
    ctx,
    *,
    name: str = None,
    user_name: str = None,
    policy_arn: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Check if a managed policy is attached to a user

    Args:
        name(str, Optional):
            An Idem name of the state for logging.

        user_name(str, Optional):
            The name (friendly name, not ARN) of the IAM user to attach the policy to.
            This parameter allows (through its regex pattern ) a string of characters consisting of upper and lowercase
            alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        policy_arn(str, Optional):
            The Amazon Resource Name (ARN) of the IAM policy you want to attach.

        resource_id(str, Optional):
            An identifier refers to an existing resource. The format is <user_name>/<policy_arn> Either resource_id
            or both user_name and policy_arn should be specified for absent.

    Returns:
        Dict[str, Any]:
            Returns IAM user policy attachemnt in present format

    Examples:
        Calling this exec module function from the cli with resource_id

        .. code-block:: bash

            idem exec aws.iam.user_policy_attachment.get name="name" resource_id="resource_id"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.iam.user_policy_attachment.get
                - kwargs:
                    name: my_resource
                    resource_id: resource_id
    """
    result = dict(comment=[], result=True, ret=None)
    if resource_id:
        user_name, policy_arn = resource_id.split("/", 1)
    elif user_name and policy_arn:
        resource_id = f"{user_name}/{policy_arn}"
    else:
        result["result"] = False
        result["comment"] = [
            f"iam.user_policy_attachment {name} either resource_id or both user_name and policy_arn"
            f" should be specified."
        ]
        return result
    user_policies_list = await hub.exec.boto3.client.iam.list_attached_user_policies(
        ctx, UserName=user_name
    )
    if user_policies_list["result"]:
        attached_user_policies_list = user_policies_list["ret"].get("AttachedPolicies")
        if attached_user_policies_list:
            policy_arn_list = [
                policy.get("PolicyArn") for policy in attached_user_policies_list
            ]
            if policy_arn in policy_arn_list:
                result["ret"] = {
                    "name": name,
                    "user_name": user_name,
                    "policy_arn": policy_arn,
                    "resource_id": resource_id,
                }
    else:
        result["comment"] = list(user_policies_list["comment"])
        result["result"] = False
    return result
