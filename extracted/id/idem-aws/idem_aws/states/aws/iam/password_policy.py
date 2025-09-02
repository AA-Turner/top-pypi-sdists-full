"""State module for managing iam password policy."""
import copy
from typing import Any
from typing import Dict

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    minimum_password_length: int = None,
    require_symbols: bool = False,
    require_numbers: bool = False,
    require_uppercase_characters: bool = False,
    require_lowercase_characters: bool = False,
    allow_users_to_change_password: bool = False,
    max_password_age: int = None,
    password_reuse_prevention: int = None,
    hard_expiry: bool = False,
) -> Dict[str, Any]:
    """Create/Update the password policy settings for the Amazon Web Services account.

    Args:
        name(str): An Idem name of the resource.

        minimum_password_length(int, Optional): The minimum number of characters allowed in an IAM user password.
            If you do not specify a value for this parameter, then the operation uses the default value of 6.

        require_symbols(bool, Optional): Specifies whether IAM user passwords must contain at least one of the following non-alphanumeric characters:
            ! @ # $ % ^ & * ( ) _ + - = [ ] { } | '
            If you do not specify a value for this parameter, then the operation uses the default value of false.
            The result is that passwords do not require at least one symbol character.

        require_numbers(bool, Optional): Specifies whether IAM user passwords must contain at least one numeric character (0 to 9).
            If you do not specify a value for this parameter, then the operation uses the default value of false. The result is that passwords do not require at least one numeric character.

        require_uppercase_characters(bool, Optional): Specifies whether IAM user passwords must contain at least one uppercase character from the ISO basic Latin alphabet (A to Z).
            If you do not specify a value for this parameter, then the operation uses the default value of false. The result is that passwords do not require at least one uppercase character.

        require_lowercase_characters(bool, Optional): Specifies whether IAM user passwords must contain at least one lowercase character from the ISO basic Latin alphabet (a to z).
            If you do not specify a value for this parameter, then the operation uses the default value of false. The result is that passwords do not require at least one lowercase character.

        allow_users_to_change_password(bool, Optional): Allows all IAM users in your account to use the Amazon Web Services Management Console to change their own passwords. For more information, see Permitting IAM users to change their own passwords in the IAM User Guide .
            If you do not specify a value for this parameter, then the operation uses the default value of false. The result is that IAM users in the account do not automatically have permissions to change their own password.

        max_password_age(int, Optional): The number of days that an IAM user password is valid.
            If you do not specify a value for this parameter, then the operation uses the default value of 0. The result is that IAM user passwords never expire.

        password_reuse_prevention(int, Optional): Specifies the number of previous passwords that IAM users are prevented from reusing.
            If you do not specify a value for this parameter, then the operation uses the default value of 0. The result is that IAM users are not prevented from reusing previous passwords.

        hard_expiry(bool, Optional): Prevents IAM users who are accessing the account via the Amazon Web Services Management Console from setting a new console password after their password has expired. The IAM user cannot access the console until an administrator resets the password.
            If you do not specify a value for this parameter, then the operation uses the default value of false. The result is that IAM users can change their passwords after they expire and continue to sign in as the user.

    Request Syntax:
      .. code-block:: sls

        [password-policy]:
          aws.iam.password_policy.present:
          - minimum_password_length: 'string'
          - require_symbols: 'string'
          - require_numbers: 'string'
          - require_uppercase_characters: 'string'
          - require_lowercase_characters: 'string'
          - allow_users_to_change_password: 'string'
          - max_password_age: 'string'
          - password_reuse_prevention: 'string'
          - hard_expiry: 'string'

    Returns:
        Dict[str, str]

    Examples:
        .. code-block:: sls

            password-policy-011922870716:
              aws.iam.password_policy.present:
              - minimum_password_length: 6
              - require_symbols: true
              - require_numbers: true
              - require_uppercase_characters: true
              - require_lowercase_characters: true
              - allow_users_to_change_password: true
              - max_password_age: 90
              - password_reuse_prevention: 3
              - hard_expiry: true
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    resource_updated = False
    plan_state = None

    before = await hub.exec.aws.iam.password_policy.get(ctx, name)
    if not before["result"]:
        result["result"] = False
        result["comment"] = before["comment"]
        return result

    if before["ret"]:
        result["old_state"] = copy.deepcopy(before["ret"])
        plan_state = copy.deepcopy(result["old_state"])

        policy_parameters = {
            "minimum_password_length": minimum_password_length,
            "require_symbols": require_symbols,
            "require_numbers": require_numbers,
            "require_uppercase_characters": require_uppercase_characters,
            "require_lowercase_characters": require_lowercase_characters,
            "allow_users_to_change_password": allow_users_to_change_password,
            "max_password_age": max_password_age,
            "password_reuse_prevention": password_reuse_prevention,
            "hard_expiry": hard_expiry,
        }

        update_ret = await hub.tool.aws.iam.password_policy.update_password_policy(
            ctx,
            name=name,
            before=result["old_state"],
            policy_parameters=policy_parameters,
        )
        result["comment"] += update_ret["comment"]
        resource_updated = resource_updated or bool(update_ret["ret"])
        if not update_ret["result"]:
            result["result"] = False
            return result

        if update_ret["ret"] and ctx.get("test", False):
            for modified_param in update_ret["ret"]:
                plan_state[modified_param] = update_ret["ret"][modified_param]
            result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                resource_type="aws.iam.password_policy", name=name
            )
        if not resource_updated:
            result["comment"] += [f"{name} already exists"]
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "minimum_password_length": minimum_password_length,
                    "require_symbols": require_symbols,
                    "require_numbers": require_numbers,
                    "require_uppercase_characters": require_uppercase_characters,
                    "require_lowercase_characters": require_lowercase_characters,
                    "allow_users_to_change_password": allow_users_to_change_password,
                    "max_password_age": max_password_age,
                    "password_reuse_prevention": password_reuse_prevention,
                    "hard_expiry": hard_expiry,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.iam.password_policy", name=name
            )
            return result
        create_ret = await hub.exec.boto3.client.iam.update_account_password_policy(
            ctx,
            MinimumPasswordLength=minimum_password_length,
            RequireSymbols=require_symbols,
            RequireNumbers=require_numbers,
            RequireUppercaseCharacters=require_uppercase_characters,
            RequireLowercaseCharacters=require_lowercase_characters,
            AllowUsersToChangePassword=allow_users_to_change_password,
            MaxPasswordAge=max_password_age,
            PasswordReusePrevention=password_reuse_prevention,
            HardExpiry=hard_expiry,
        )
        if not create_ret["result"]:
            result["result"] = False
            result["comment"] = create_ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.iam.password_policy", name=name
        )

    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif (not before["ret"]) or resource_updated:
            after_ret = await hub.exec.aws.iam.password_policy.get(ctx, name)
            if not after_ret["result"]:
                result["result"] = False
                result["comment"] += after_ret["comment"]
                return result
            result["new_state"] = after_ret["ret"]
        else:
            result["new_state"] = copy.deepcopy(result["old_state"])
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False
    return result


async def absent(hub, ctx, name: str) -> Dict[str, Any]:
    """Deletes the password policy for the Amazon Web Services account.

    Args:
        name(str): Password policy name.

    Request Syntax:
        .. code-block:: sls

            password-policy:
              aws.iam.password_policy.absent:
              - name: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.iam.password_policy.absent:
              - name: value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    before = await hub.exec.aws.iam.password_policy.get(ctx, name)
    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result

    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.iam.password_policy", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.iam.password_policy", name=name
        )
        return result
    else:
        result["old_state"] = before["ret"]
        ret = await hub.exec.boto3.client.iam.delete_account_password_policy(ctx)
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.iam.password_policy", name=name
        )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Gets information about the iam password policy.

    Retrieves the password policy for the Amazon Web Services account.
    This tells you the complexity requirements and mandatory rotation periods for
    the IAM user passwords in your account.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

           $ idem describe aws.iam.password_policy

    """
    result = {}
    ret = await hub.exec.aws.iam.password_policy.get(ctx, "password_policy")
    if not ret["result"]:
        hub.log.warning(f"Could not describe account password policy {ret['comment']}")
        return {}
    resource_key = "password-policy"
    result[resource_key] = {
        "aws.iam.password_policy.present": [
            {parameter_key: parameter_value}
            for parameter_key, parameter_value in ret["ret"].items()
        ]
    }

    return result
