import copy
from collections import OrderedDict
from typing import Any
from typing import Dict

from dict_tools import data


async def update_password_policy(
    hub,
    ctx,
    name: str,
    before: Dict[str, Any],
    policy_parameters: Dict[str, Any],
):
    """
    Updates the password policy settings for the Amazon Web Services account.

    Args:
        hub: required for functions in hub.
        ctx: context.
        name: Password policy name.
        before(Dict): Existing resource parameters in Amazon Web Services.
        policy_parameters(Dict): Password policy attributes.

    Returns:
        {"result": True|False, "comment": A message Tuple, "ret": Dict}

    """
    result = dict(comment=[], result=True, ret=None)
    parameters_to_update = {}

    parameters = OrderedDict(
        {
            "minimum_password_length": "MinimumPasswordLength",
            "require_symbols": "RequireSymbols",
            "require_numbers": "RequireNumbers",
            "require_uppercase_characters": "RequireUppercaseCharacters",
            "require_lowercase_characters": "RequireLowercaseCharacters",
            "allow_users_to_change_password": "AllowUsersToChangePassword",
            "max_password_age": "MaxPasswordAge",
            "password_reuse_prevention": "PasswordReusePrevention",
            "hard_expiry": "HardExpiry",
        }
    )
    for key, value in parameters.items():
        if key in policy_parameters.keys():
            parameters_to_update[value] = policy_parameters[key]

    # expire_passwords can not be updated as direct param but is available in get
    old_policy = copy.deepcopy(before)
    old_policy.pop("expire_passwords")

    if not policy_parameters["max_password_age"]:
        policy_parameters.pop("max_password_age")
    if not policy_parameters["password_reuse_prevention"]:
        policy_parameters.pop("password_reuse_prevention")
    policy_diff = data.recursive_diff(policy_parameters, old_policy, ignore_order=True)
    if policy_diff:
        result["ret"] = {}

        if not ctx.get("test", False):
            update_ret = await hub.exec.boto3.client.iam.update_account_password_policy(
                ctx=ctx, **parameters_to_update
            )
            if not update_ret["result"]:
                result["comment"] = update_ret["comment"]
                result["result"] = False
                return result
            result["comment"] = hub.tool.aws.comment_utils.update_comment(
                resource_type="aws.iam.password_policy", name=name
            )

        for key, value in parameters.items():
            if value in parameters_to_update:
                result["ret"][key] = parameters_to_update[value]
    return result
