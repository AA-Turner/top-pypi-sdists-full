import copy
from typing import Any
from typing import Dict

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    user_name: str,
    resource_id: str = None,
    status: str = "Active",
    pgp_key: str = None,
    secret_access_key: str = None,
) -> Dict[str, Any]:
    """
    Ensures an AWS key has the assigned status.

    This will create a new access key for a user if no access_key_id is passed for this state, either via
    access_key_id or resource_id.

    If a new access key is created, the secret access key will also be returned. This can optionally be encrypted
    with a base 64 encoded PGP public key.

    Args:
        name(str): An Idem name describing the resource.
        user_name(str): AWS IAM user name that the key belongs to.
        resource_id(str, Optional): AWS IAM access key ID.
        status(str, Optional): "Active" or "Inactive"; Active keys are valid for API calls. Defaults to "Active".
        pgp_key(str, Optional): A base 64 encode PGP public key, used to encrypt the secret access key if a new key is created.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            name_describing_key:
              aws.iam.access_key.present:
                - user_name: aws_user
                - status: Active
    """
    # secret_access_key is used internally to make sure the secret_access_key isn't lost after the 1st present run.
    # This parameter should not be inputted on sls and hence it is not added to the function description.
    result = {
        "name": name,
        "old_state": None,
        "new_state": None,
        "comment": [],
        "result": True,
    }

    # ----- look up key
    if resource_id:
        list_ret = await hub.exec.aws.iam.access_key.list(
            ctx, access_key_id=resource_id, user_name=user_name
        )
        if not list_ret["result"]:
            result["result"] = False
            result["comment"] += [f"Error listing access keys"] + list(
                list_ret["comment"]
            )
            return result
        elif len(list_ret["ret"]) == 0:
            # Return error if the specified access key id doesn't exist on AWS.
            message = (
                f"The specified access_key_id {resource_id} in aws.iam.key {name} does not exist, and keys "
                "cannot be recreated by id."
            )
            result["comment"] += [message] + list_ret["comment"]
            result["result"] = False
            return result

        before = list_ret["ret"][0]
        if secret_access_key:
            before["secret_access_key"] = secret_access_key
        result["old_state"] = before
        if before["status"] == status:
            result["comment"] += [f"No changes necessary for aws.iam.key {name}"]
            result["new_state"] = copy.deepcopy(result["old_state"])
            return result
        else:
            # only update is necessary
            if not ctx.get("test", False):
                update_ret = await hub.exec.aws.iam.access_key.update(
                    ctx, user_name=user_name, access_key_id=resource_id, status=status
                )
                if not update_ret["result"]:
                    result["comment"] += update_ret["comment"]
                    result["result"] = False
                    return result
                result["comment"] += [f"Updated aws.iam.key {name} to {status}"]
            else:
                result["comment"] += [f"Would update aws.iam.key {name} to {status}"]
            result["new_state"] = copy.deepcopy(result["old_state"])
            result["new_state"]["status"] = status
    else:
        if ctx.get("test"):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "user_name": user_name,
                    "secret_access_key": "SECRET_ACCESS_KEY",
                    "status": status if status else "Active",
                },
            )
            result["comment"] += hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.iam.access_key", name=name
            )
            return result
        create_ret = await hub.exec.aws.iam.access_key.create(ctx, user_name, pgp_key)
        if not create_ret["result"]:
            result["result"] = False
            result["comment"] += create_ret["comment"]
            return result
        access_key_id = create_ret["ret"]["access_key_id"]
        result[
            "new_state"
        ] = hub.tool.aws.iam.conversion_utils.convert_access_key_to_present(
            create_ret["ret"], name
        )
        result["comment"] += hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.iam.access_key", name=name
        )
        # Create can't set status. So update the status if the status should be "Inactive"
        if status == "Inactive":
            update_ret = await hub.exec.aws.iam.access_key.update(
                ctx, user_name=user_name, access_key_id=access_key_id, status=status
            )
            if not update_ret["result"]:
                result["comment"] += update_ret["comment"]
                result["result"] = False
            result["new_state"]["status"] = "Inactive"
    return result


async def absent(
    hub,
    ctx,
    name: str,
    user_name: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """
    Ensure the specified access key does not exist.
    Both user_name and resource_id must be passed in.

    Args:
        name(str): An Idem name describing the resource.
        user_name(str, Optional): AWS IAM user name that the key belongs to.
        resource_id(str, Optional): AWS IAM access key ID.
    Returns:
        Dict[str, Any]
    Examples:
        .. code-block:: sls

            name_describing_key:
              aws.iam.access_key.absent:
                - user_name: value
                - resource_id: value
    """
    result = {
        "name": name,
        "old_state": None,
        "new_state": None,
        "comment": [],
        "result": True,
    }
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.iam.access_key", name=name
        )
        return result

    if not user_name:
        result["comment"] = hub.tool.aws.comment_utils.missing_args_for_absent_comment(
            resource_type="aws.iam.access_key", name=name, args=["user_name"]
        )
        result["result"] = False
        return result

    # ------ look up key
    list_ret = await hub.exec.aws.iam.access_key.list(
        ctx, access_key_id=resource_id, user_name=user_name
    )
    result["comment"] = list_ret["comment"]
    if not list_ret["result"]:
        result["result"] = False
        return result
    if len(list_ret["ret"]) == 0:
        result["comment"] += hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.iam.access_key", name=name
        )
        return result

    access_key = list_ret["ret"][0]
    result["old_state"] = access_key

    # ------ delete key
    # delete logic is handled inside exec's delete, including ctx["test"]
    if ctx.get("test"):
        result["comment"] += hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.iam.access_key", name=name
        )
        return result
    delete_ret = await hub.exec.aws.iam.access_key.delete(
        ctx, access_key_id=resource_id, user_name=user_name
    )
    result["result"] = delete_ret["result"]
    if not result["result"]:
        result["comment"] += delete_ret["comment"]
    else:
        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.iam.access_key", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Describe access keys and their current status in a way that can be managed via the "present" function.

    We describe all access keys for all users the logged in user can list.

    Returns:
        Dict[str, Any]
    Examples:
        .. code-block:: bash

            $ idem describe aws.iam.access_key
    """
    users_list = await hub.exec.aws.iam.user.list(ctx)
    if not users_list["result"]:
        hub.log.warning(f"Could not describe keys: {users_list['comment']}")
        return {}
    users = [u["user_name"] for u in users_list["ret"]]

    result = {}

    for user in users:
        result.update(await _describe_one_user(hub, ctx, user))
    # The above is pretty slow, if/when we add random exponential backoff on
    #  failures, switch to this code:
    # multi_result = await asyncio.gather(
    #     *[_describe_one_user(hub, ctx, u["user_name"]) for u in users]
    # )
    # for r in multi_result:
    #     result.update(r)

    return result


async def _describe_one_user(hub, ctx, user_name: str) -> Dict[str, Dict[str, Any]]:
    keys = await hub.exec.aws.iam.access_key.list(ctx, user_name=user_name)
    if not keys["result"]:
        hub.log.debug(
            f"Could not list aws.iam.access_key for user {user_name}: {keys['comment']}"
        )
        return {}

    result = {}

    for access_key in keys["ret"]:
        # iterate every loop to give the user another indication if keys are skipped
        if "resource_id" not in access_key or "status" not in access_key:
            # All values are "optionally" returned from AWS but managing a key
            #  without the id and status would be impossible.
            hub.log.debug(
                f"Can not describe an aws key without an id and status {access_key}"
            )
            continue

        idem_declaration_id = f"iam-access-key-{access_key['name']}"
        result[idem_declaration_id] = {
            "aws.iam.access_key.present": [{k: v} for k, v in access_key.items()]
        }

    return result
