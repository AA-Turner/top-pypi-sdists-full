"""Util module to provide support to AWS WAFV2 IPSet state module."""
from collections import OrderedDict
from typing import Any
from typing import Dict


async def update(
    hub,
    ctx,
    name: str,
    current_state: Dict[str, Any],
    desired_state: Dict[str, Any],
):
    """Updates configuration options for an ip_set in AWS.

    Args:
        hub:
             The redistributed pop central hub.
        ctx:
             A dict with the keys/values for the execution of the Idem run located in
              `hub.idem.RUNS[ctx['run_name']]`.
        name(str):
             The name of the ip_set in AWS
        current_state(Dict):
             Previous state of the ip_set resource in AWS
        desired_state(Dict):
             Parameters from SLS file as per the desired final state of the ip_set.

    Returns:
        Dict[str, Any]
    """
    result = dict(comment=[], result=True, ret=None)

    parameters = OrderedDict(
        {
            "addresses": "Addresses",
            "description": "Description",
        }
    )

    parameters_to_update = {}

    if desired_state.get("addresses"):
        desired_set_addresses = set(desired_state.get("addresses"))
        current_set_addresses = set(current_state.get("addresses"))
        if (
            desired_set_addresses is not None
            and desired_set_addresses != current_set_addresses
        ):
            parameters_to_update[parameters["addresses"]] = desired_state.get(
                "addresses"
            )
    if desired_state.get("description"):
        if desired_state.get("description") is not None and desired_state.get(
            "description"
        ) != current_state.get("description"):
            parameters_to_update[parameters["description"]] = desired_state.get(
                "description"
            )

    if parameters_to_update:
        if ctx.get("test", False):
            result["comment"] = hub.tool.aws.comment_utils.would_update_comment(
                resource_type="aws.wafv2.ip_set",
                name=name,
            )
            result["ret"] = parameters_to_update
        if not ctx.get("test", False):
            update_ret = await hub.exec.boto3.client.wafv2.update_ip_set(
                ctx=ctx,
                Name=current_state["name"],
                Scope=current_state["scope"],
                Id=current_state["resource_id"],
                LockToken=current_state["lock_token"],
                **parameters_to_update,
            )
            if not update_ret["result"]:
                result["result"] = False
                result["comment"] = update_ret["comment"]
                return result
            result["comment"] = hub.tool.aws.comment_utils.update_comment(
                resource_type="aws.wafv2.ip_set",
                name=name,
            )
            result["ret"] = parameters_to_update
    else:
        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.wafv2.ip_set",
            name=name,
        )
    return result
