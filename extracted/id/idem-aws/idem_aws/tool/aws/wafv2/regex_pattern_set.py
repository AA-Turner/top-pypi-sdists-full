from typing import Any
from typing import Dict
from typing import List

from dict_tools import data


async def update(
    hub,
    ctx,
    current_state: Dict[str, Any],
    description: str,
    regular_expression_list: List[Dict[str, str]],
) -> Dict[str, Any]:
    # Description and regular_expression_list can be updated. Check if they are modified and update
    result = dict(ret=None, comment=[], result=True)

    if current_state.get("description") != description or data.recursive_diff(
        current_state.get("regular_expression_list"),
        regular_expression_list,
        ignore_order=True,
    ):
        if not ctx.get("test", False):
            update_ret = await hub.exec.boto3.client.wafv2.update_regex_pattern_set(
                ctx=ctx,
                Name=current_state.get("name"),
                Scope=current_state.get("scope"),
                Id=current_state.get("resource_id"),
                Description=description,
                RegularExpressionList=regular_expression_list,
                LockToken=current_state.get("LockToken"),
            )
            result["result"] = update_ret["result"]
            if not result["result"]:
                result["comment"] = update_ret["comment"]
                return result
        result["ret"] = {
            "description": description,
            "regular_expression_list": regular_expression_list,
        }
    return result


def check_if_invalid_scope_and_region(hub, region, scope):
    if region != "us-east-1" and scope == "CLOUDFRONT":
        return "CLOUDFRONT scope is available only in US East (N. Virginia) Region, us-east-1"
    return None
