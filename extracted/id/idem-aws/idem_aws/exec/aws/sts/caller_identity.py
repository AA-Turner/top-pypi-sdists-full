"""Exec module for caller identity."""
from typing import Any
from typing import Dict


async def get(hub, ctx) -> Dict[str, Any]:
    """Returns details about the IAM user whose credentials are used to call the operation.

    Returns:
        Dict[str, Any]:
            Return the identity details such as UserId, Account, and ARN about the IAM user

    Examples:
        Call from the CLI:

        .. code-block:: bash

            $ idem exec aws.sts.caller_identity.get

        Call from code:

        .. code-block:: python

            async def my_func(hub, ctx):
                await hub.exec.aws.sts.caller_identity.get(ctx)

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.sts.caller_identity.get
    """
    ret = dict(result=True, ret={}, comment=[])
    caller_identity = await hub.exec.boto3.client.sts.get_caller_identity(ctx)

    ret["result"] = caller_identity.result
    ret["comment"] = caller_identity.comment
    if caller_identity.result:
        ret["ret"]["UserId"] = caller_identity.ret["UserId"]
        ret["ret"]["Account"] = caller_identity.ret["Account"]
        ret["ret"]["Arn"] = caller_identity.ret["Arn"]
    return ret
