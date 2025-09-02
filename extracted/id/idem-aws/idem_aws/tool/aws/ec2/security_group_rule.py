from collections import OrderedDict
from typing import Any
from typing import Dict


async def update_security_group_rule(
    hub,
    ctx,
    before: Dict[str, Any],
    input_params: Dict[str, Any],
    resource_id: str,
):
    """Updates the Security group rule.

    Args:
        before(dict[str, Any]): existing resource
        input_params(dict[str, Any]): a dictionary with newly passed values of params.
        resource_id(str): AWS Security group rule ID.

    Returns:
        .. code-block:: json

           {
             "result": True|False,
             "comment": A message Tuple,
             "ret": Dict
           }

    """
    result = dict(comment=[], result=True, ret=None)
    updated_payload = {}
    updated_rule = {}
    new_modified_rule = dict(SecurityGroupRuleId=None, SecurityGroupRule=None)
    new_modified_rule["SecurityGroupRuleId"] = resource_id
    resource_parameters = OrderedDict(
        {
            "IpProtocol": "ip_protocol",
            "FromPort": "from_port",
            "ToPort": "to_port",
            "CidrIpv4": "cidr_ipv4",
            "CidrIpv6": "cidr_ipv6",
            "PrefixListId": "prefix_list_id",
            "Description": "description",
        }
    )

    for key, value in resource_parameters.items():
        if value in before.keys():
            updated_payload[key] = input_params.get(value)
            if (input_params.get(value) is not None) and (
                input_params.get(value) != before[value]
            ):
                updated_rule[key] = input_params[value]
        elif input_params.get(value):
            updated_payload[key] = input_params[value]
            updated_rule[key] = input_params[value]
    # You must either specify cidr_ipv4 or referenced_group_info. You cannot change source from cidr to reference
    # group id or vice versa
    if before.get(
        "cidr_ipv4"
    ) is None and not hub.tool.aws.state_comparison_utils.compare_dicts(
        input_params.get("referenced_group_info"),
        before.get("referenced_group_info"),
    ):
        if input_params.get("referenced_group_info"):
            updated_rule["ReferencedGroupId"] = input_params.get(
                "referenced_group_info"
            ).get("GroupId")
    if updated_rule:
        if (
            before.get("cidr_ipv4") is None
            and input_params.get("referenced_group_info") is not None
        ):
            updated_payload["ReferencedGroupId"] = input_params.get(
                "referenced_group_info"
            ).get("GroupId")
        new_modified_rule["SecurityGroupRule"] = updated_payload
        if not ctx.get("test", False):
            update_ret = await hub.exec.boto3.client.ec2.modify_security_group_rules(
                ctx,
                GroupId=input_params.get("group_id"),
                SecurityGroupRules=[new_modified_rule],
            )
            if not update_ret["result"]:
                result["comment"] = update_ret["comment"]
                result["result"] = False
                return result
        result["ret"] = {}
        result = update_result(result, updated_rule)

    return result


def update_result(
    result: Dict[str, Any], update_payload: Dict[str, Any]
) -> Dict[str, Any]:
    parameters = OrderedDict(
        {
            "IpProtocol": "ip_protocol",
            "FromPort": "from_port",
            "ToPort": "to_port",
            "CidrIpv4": "cidr_ipv4",
            "CidrIpv6": "cidr_ipv6",
            "PrefixListId": "prefix_list_id",
            "Description": "description",
            "ReferencedGroupId": "referenced_group_id",
        }
    )

    for raw_parameter, present_parameter in parameters.items():
        if raw_parameter in update_payload:
            result["ret"][present_parameter] = update_payload[raw_parameter]
            result["comment"] += [
                f"Update {present_parameter}: {update_payload[raw_parameter]}"
            ]
    return result
