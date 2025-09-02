"""Exec module for managing Amazon Cloudwatchlogs Resource Policy."""
from typing import Any
from typing import Dict


async def get(
    hub,
    ctx,
    name: str,
) -> Dict[str, Any]:
    """Returns resource policy object for the given resource policy name.

    Args:
        name(str): Name of the new policy. An Idem name of the resource

    Returns:
        .. code-block:: python

            {"result": True|False, "comment": A message List, "ret": None|Dict}

    Examples:
        Calling this exec module function from the cli with name

        .. code-block:: bash

            idem exec aws.cloudwatchlogs.resource_policy.get name="name"

        Calling this exec module function from within a state module in pure python.

        .. code-block:: python

            async def state_function(hub, ctx, resource_id):
                before = await hub.exec.aws.cloudwatchlogs.resource_policy.get(
                ctx, name=resource_id
            )
    """
    result = dict(comment=[], result=True, ret=None)
    ret = await hub.exec.boto3.client.logs.describe_resource_policies(ctx)
    result["result"] = ret["result"]
    if not result["result"]:
        result["comment"] += ret["comment"]
        return result
    if ret["ret"]:
        resource_policies = ret["ret"]["resourcePolicies"]
        for resource_policy in resource_policies:
            if resource_policy.get("policyName") == name:
                result["ret"] = resource_policy
                break
    return result
