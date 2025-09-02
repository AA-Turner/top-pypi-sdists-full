"""Exec module for managing Amazon IAM Policies."""
from typing import Dict

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
) -> Dict:
    """Retrieves the specified AWS IAM Policy.

    Args:
        name(str):
            The name of the IAM Policy.
        resource_id(str, Optional):
            The Amazon Resource Name (ARN) of the IAM policy in Amazon Web Services. If not supplied, ``name`` will be used to get the resource.

    Returns:
        Dict[bool, list, dict or None]:

        result(bool):
            Whether the result of the function has been successful (``True``) or not (``False``).
        comment(list):
            A list of messages.
        ret(dict or None):
           The IAM Policy in "present" format.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec aws.iam.policy.get name="idem_name" resource_id="resource_id"

        Calling this exec module function from within a state module in pure python:

        .. code-block:: python

            async def state_function(hub, ctx, name, resource_id, **kwargs):
                ret = await hub.exec.aws.iam.policy.get(
                    ctx, name=name, resource_id=resource_id
                )
    """
    result = dict(comment=[], ret=None, result=True)

    if not resource_id:
        ret = await hub.exec.boto3.client.iam.list_policies(ctx)
        if not ret["result"]:
            result["comment"] += list(ret["comment"])
            result["result"] = False
            return result
        for ret_policy in ret["ret"]["Policies"]:
            if ret_policy["PolicyName"] == name:
                resource_id = ret_policy["Arn"]
                continue
        if not resource_id:
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.iam.policy", name=name
                )
            )
            return result

    ret = await hub.exec.boto3.client.iam.get_policy(ctx, PolicyArn=resource_id)
    if not ret["result"]:
        if "NoSuchEntityException" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.iam.policy", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    policy = ret["ret"]["Policy"]
    ret_get_policy_version = await hub.exec.boto3.client.iam.get_policy_version(
        ctx, PolicyArn=policy["Arn"], VersionId=policy["DefaultVersionId"]
    )
    if not ret_get_policy_version["result"]:
        result["comment"] += list(ret_get_policy_version)
        result["result"] = False
        return result
    policy["Document"] = ret_get_policy_version["ret"]["PolicyVersion"].get("Document")

    result["ret"] = hub.tool.aws.iam.conversion_utils.convert_raw_policy_to_present(
        ctx, raw_resource=policy
    )

    return result


async def list_(
    hub,
    ctx,
    scope: str = None,
    only_attached: bool = None,
    path_prefix: str = None,
    policy_usage_filter: str = None,
) -> Dict:
    """Lists AWS IAM Policies.

    Arg:
        scope(str, Optional):
            The scope to use for filtering the results. To list only Amazon Web Services managed policies, set ``scope`` to ``AWS``.
            To list only the customer managed policies in your Amazon Web Services account, set ``scope`` to ``Local``.
            This parameter is optional. If it is not included, or if it is set to ``All``, all policies are returned.
        only_attached (bool, Optional):
            A flag to filter the results to only the attached policies. When ``True``, the returned list contains only the policies
            that are attached to an IAM user, group, or role. When ``False``, or when the parameter is not included, all policies are returned.
        path_prefix (str, Optional):
            The path prefix for filtering the results. This parameter is optional. If it is not included, it defaults to a slash (``/``),
            listing all policies. This parameter allows (through its regex pattern) a string of characters consisting of either a forward
            slash (``/``) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character
            from the ``!`` (``\u0021``) through the ``DEL`` character (``\u007F``), including most punctuation characters, digits, and upper
            and lowercased letters.
        policy_usage_filter(str, Optional):
            The policy usage method to use for filtering the results. To list only permissions policies, set the value to ``PermissionsPolicy``.
            To list only the policies used to set permissions boundaries, set the value to ``PermissionsBoundary``. This parameter is optional.
            If it is not included, all policies are returned.

    Returns:
        Dict[bool, list, dict or None]:

        result(bool):
            Whether the result of the function has been successful (``True``) or not (``False``).
        comment(list):
            A list of messages.
        ret(dict or None):
           The IAM Policies in "present" format.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec aws.iam.policy.list scope="ALL"

        Calling this exec module function from within a state module in pure python:

        .. code-block:: python

            async def state_function(hub, ctx, name, scope, **kwargs):
                ret = await hub.exec.aws.iam.policy.list(
                    ctx, scope=scope
                )
    """
    result = dict(comment=[], ret=[], result=True)

    ret = await hub.exec.boto3.client.iam.list_policies(
        ctx=ctx,
        Scope=scope,
        OnlyAttached=only_attached,
        PathPrefix=path_prefix,
        PolicyUsageFilter=policy_usage_filter,
    )
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["Policies"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.iam.policy", name=scope
            )
        )
        return result

    for policy in ret["ret"]["Policies"]:
        get_ret = await hub.exec.aws.iam.policy.get(
            ctx, name=policy["PolicyName"], resource_id=policy["Arn"]
        )
        if not get_ret["result"]:
            result["comment"] += list(get_ret["comment"])
            result["result"] = False
            return result
        if get_ret["ret"]:
            result["ret"].append(get_ret["ret"])

    return result
