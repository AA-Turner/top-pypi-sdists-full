"""State module for managing Amazon IAM Policies."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    policy_document: Dict or str,
    resource_id: str = None,
    path: str = "/",
    description: str = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass(
            "Tag",
            [("Key", str, field(default=None)), ("Value", str, field(default=None))],
        )
    ] = None,
    timeout: make_dataclass(
        """Timeout configuration for AWS IAM Policy.""" "Timeout",
        [
            (
                "create",
                make_dataclass(
                    """Timeout configuration when creating an AWS IAM Policy."""
                    "CreateTimeout",
                    [
                        ("delay", int, field(default=1)),
                        ("max_attempts", int, field(default=40)),
                    ],
                ),
                field(default=None),
            ),
            (
                "update",
                make_dataclass(
                    """Timeout configuration when updating an AWS IAM Policy."""
                    "UpdateTimeout",
                    [
                        ("delay", int, field(default=1)),
                        ("max_attempts", int, field(default=40)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
) -> Dict[str, Any]:
    """Creates or updates an AWS IAM Policy.

    When creating a policy, this operation creates a policy version with a version identifier of `v1` and sets `v1` as the
    policy's default version. When updating a policy, this operation creates a new policy version, sets the new policy to
    the default version, and deletes the old policy.

    Args:
        name(str):
            The name of the IAM Policy.
        policy_document(dict or str):
            The JSON policy document that you want to use as the content for the new policy.
            You must provide policies in JSON format in IAM. However, for CloudFormation templates formatted in YAML,
            you can provide the policy in JSON or YAML format. CloudFormation always converts a YAML policy to JSON format
            before submitting it to IAM.
        resource_id(str, Optional):
            The Amazon Resource Name (ARN) of the IAM policy in Amazon Web Services.
        path(str, Optional):
            The path for the policy. This parameter is optional. If it is not included, it defaults to a slash (``/``).
        description(str, Optional):
            A friendly description of the policy.
        tags(dict or list, Optional):
            Dict in the format of ``{tag-key: tag-value}`` or List of tags in the format of
            ``[{"Key": tag-key, "Value": tag-value}]`` to associate with the policy.

            * Key (*str*):
                The key of the tag.
            * Value (*str*):
                The value of the tag.
        timeout(dict, Optional):
            Timeout configuration for AWS IAM Policy.

            * create (*dict, Optional*):
                Timeout configuration when creating an AWS IAM Policy.

                * delay (*int, Optional*):
                    The amount of time in seconds to wait between attempts. Default value is ``1``.
                * max_attempts (*int, Optional*):
                    Max attempts of waiting for change. Default value is ``40``.

            * update (*dict, Optional*):
                Timeout configuration when updating an AWS IAM Policy.

                * delay (*int, Optional*):
                    The amount of time in seconds to wait between attempts. Default value is ``1``.
                * max_attempts (*int, Optional*):
                    Max attempts of waiting for change. Default value is ``40``.

    Request Syntax:
      .. code-block:: sls

        [idem_test_aws_iam_policy]:
          aws.iam.policy.present:
            - name: 'string'
            - resource_id: 'string'
            - policy_document: 'dict' or 'string'
            - path: 'string'
            - description: 'string'
            - tags:
                - Key: 'string'
                  Value: 'string'
            - timeout:
                create:
                  delay: int
                  max_attemps: int
                update:
                  delay: int
                  max_attemps: int

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_iam_policy:
              aws.iam.policy.present:
                - name: 'idem_test_iam_policy'
                - policy_document:
                    Version: '2012-10-17'
                    Statement:
                      - Sid: 'AllowCreateSubnet'
                        Effect: 'Allow'
                        Action: ['ec2:CreateSubnet']
                        Resource: '*'
                - path: '/'
                - description: 'My IAM Policy'
                - tags:
                    - Key: 'provider'
                      Value: 'idem'
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    update_ret = None

    tags = (
        hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)
        if isinstance(tags, List)
        else tags
    )

    # Standardise on the json format
    policy_document = hub.tool.aws.state_comparison_utils.standardise_json(
        policy_document
    )

    if resource_id:
        before = await hub.exec.aws.iam.policy.get(
            ctx, name=name, resource_id=resource_id
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["old_state"] = before["ret"]
        plan_state = copy.deepcopy(result["old_state"])
        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.iam.policy", name=name
        )
        # Update policy document if needed
        if (
            result["old_state"] is not None
            and result["old_state"]["policy_document"]
            and not hub.tool.aws.state_comparison_utils.are_policies_equal(
                result["old_state"]["policy_document"], policy_document
            )
        ):
            if ctx.get("test", False):
                plan_state["policy_document"] = policy_document
                result["comment"] = result[
                    "comment"
                ] + hub.tool.aws.comment_utils.would_update_comment(
                    resource_type="aws.iam.policy", name=name
                )
            else:
                update_ret = await hub.tool.aws.iam.policy.update(
                    ctx=ctx,
                    policy_arn=resource_id,
                    policy_version_id=result["old_state"].get("default_version_id"),
                    new_policy_document=policy_document,
                    timeout=timeout,
                )
                if not update_ret["result"]:
                    result["comment"] += update_ret["comment"]
                    result["result"] = False

        if (
            result["old_state"] is not None
            and tags is not None
            and tags != result["old_state"].get("tags")
        ):
            update_ret = await hub.tool.aws.iam.policy.update_tags(
                ctx=ctx,
                police_arn=resource_id,
                old_tags=result["old_state"].get("tags"),
                new_tags=tags,
            )
            result["comment"] += update_ret["comment"]
            if not update_ret["result"]:
                result["result"] = False
            if ctx.get("test", False) and update_ret["result"]:
                plan_state["tags"] = update_ret["ret"]

        if update_ret is not None and result["result"] and not ctx.get("test", False):
            result["comment"] = result[
                "comment"
            ] + hub.tool.aws.comment_utils.update_comment(
                resource_type="aws.iam.policy", name=name
            )
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "resource_id": f"policy-{name}-resource_id",
                    "id": f"policy-{name}-id",
                    "path": path,
                    "policy_document": policy_document,
                    "description": description,
                    "tags": tags,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.iam.policy", name=name
            )
            return result

        ret = await hub.exec.boto3.client.iam.create_policy(
            ctx,
            PolicyName=name,
            Path=path,
            PolicyDocument=policy_document,
            Description=description,
            Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
            if tags
            else None,
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
            default_delay=1,
            default_max_attempts=40,
            timeout_config=timeout.get("create") if timeout else None,
        )
        hub.log.debug(f"Waiting on creation of aws.iam.policy '{name}'")
        try:
            await hub.tool.boto3.client.wait(
                ctx,
                "iam",
                "policy_exists",
                PolicyArn=ret["ret"].get("Policy")["Arn"],
                WaiterConfig=waiter_config,
            )
        except Exception as e:
            result["comment"] += [str(e)]
            result["result"] = False
            return result
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.iam.policy", name=name
        )
        resource_id = ret["ret"]["Policy"]["Arn"]

    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif before and (update_ret is None):
            result["new_state"] = copy.deepcopy(result["old_state"])
        else:
            after = await hub.exec.aws.iam.policy.get(
                ctx, name=name, resource_id=resource_id
            )
            result["new_state"] = after["ret"]
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False
    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deletes the specified AWS IAM Policy.

    Before you can delete a managed policy, you must first detach the policy from all users, groups, and roles that it is attached to.
    In addition, you must delete all the policy's versions. The following steps describe the process for deleting a managed policy:

    * Detach the policy from all users, groups, and roles that the policy is attached to.
    * Delete all versions of the policy.
    * Delete the policy (this automatically deletes the policy's default version).

    Args:
        name(str):
            The name of the IAM Policy.
        resource_id(str, Optional):
            The Amazon Resource Name (ARN) of the IAM policy in Amazon Web Services.

            .. warning::
              Idem automatically considers this resource being absent if this field is not specified.

    Request Syntax:
      .. code-block:: sls

        [idem_test_aws_iam_policy]:
          aws.iam.policy.absent:
            - name: 'string'
            - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_iam_policy:
              aws.iam.policy:
                - name: 'idem_test_iam_policy'
                - resource_id: 'arn:aws:iam::123456789012:policy/idem_test_iam_policy'
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.iam.policy", name=name
        )
        return result

    before = await hub.exec.aws.iam.policy.get(ctx, name=name, resource_id=resource_id)
    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result
    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.iam.policy", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.iam.policy", name=name
        )
        return result
    else:
        result["old_state"] = before["ret"]
        ret = await hub.exec.boto3.client.iam.delete_policy(ctx, PolicyArn=resource_id)
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.iam.policy", name=name
        )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describes IAM Local Policies in a way that can be recreated/managed with the corresponding "present" function.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.iam.policy
    """
    result = {}

    # Set scope to local to only list the customer-defined managed policies.
    ret = await hub.exec.aws.iam.policy.list(ctx, scope="Local")
    if not ret["result"]:
        hub.log.warning(f"Could not describe policies {ret['comment']}")
        return {}

    for policy in ret["ret"]:
        resource_key = f"iam-policy-{policy['resource_id']}"
        result[resource_key] = {
            "aws.iam.policy.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in policy.items()
            ]
        }

    return result
