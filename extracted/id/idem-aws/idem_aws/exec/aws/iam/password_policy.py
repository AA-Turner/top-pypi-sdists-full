"""Exec module for managing IAM password policy."""
from typing import Dict


async def get(hub, ctx, name: str) -> Dict:
    """Retrieves the password policy for the Amazon Web Services account.

    Args:
        name(str): Password policy name.

    Returns:
        Dict[bool, list, dict or None]:

        result(bool):
            Whether the result of the function has been successful (``True``) or not (``False``).
        comment(list):
            A list of messages.
        ret(dict or None):
           The IAM password policy in "present" format.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec aws.iam.password_policy.get name="idem_name"

        Calling this exec module function from within a state module in pure python:

        .. code-block:: python

            async def state_function(hub, ctx, name, resource_id, **kwargs):
                ret = await hub.exec.aws.iam.password_policy.get(
                    ctx, name=name
                )

    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.exec.boto3.client.iam.get_account_password_policy(ctx)

    if not ret["result"]:
        if "NoSuchEntity" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.iam.password_policy", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    result[
        "ret"
    ] = hub.tool.aws.iam.conversion_utils.convert_raw_password_policy_to_present(
        ctx, raw_password_policy=ret["ret"]["PasswordPolicy"]
    )
    return result
