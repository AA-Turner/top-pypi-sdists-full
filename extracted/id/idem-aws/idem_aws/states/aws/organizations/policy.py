"""State module for managing Amazon Organizations Policies."""
import copy
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]

TREQ = {
    "absent": {
        "require": [
            "aws.organizations.policy_attachment.absent",
        ],
    },
    "present": {
        "require": [
            "aws.organizations.account.present",
        ],
    },
}


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    description: str = None,
    policy_type: str = None,
    content: str = None,
    tags: List[Dict[str, Any]] or Dict[str, Any] = None,
) -> Dict[str, Any]:
    """Creates Organization Policy.

    Creates a policy of a specified type that you can attach to a root, an organizational unit (OU), or an individual
    AWS account.

    Args:
        name(str):
            The name of the policy.

        resource_id(str, Optional):
            The ID of the policy in Amazon Web Services.

        description(str, Optional):
            A description to assign to the policy.

        policy_type(str, Optional):
            The type of policy to create. Only supported values are
            SERVICE_CONTROL_POLICY, TAG_POLICY, BACKUP_POLICY and AISERVICES_OPT_OUT_POLICY.

        content(str, Optional):
            The policy text content to add to the new policy. The text that you supply must adhere
            to the rules of the policy type.

        tags(dict or list, Optional):
            Dict in the format of {tag-key: tag-value} or List of tags in the format of
            [{"Key": tag-key, "Value": tag-value}] to associate with the policy.

            * Key (str, Optional): The key identifier, or name, of the tag.
            * Value (str, Optional): The string value that's associated with the key of the tag.

    Request syntax:
        .. code-block:: sls

            [idem_test_aws_organizations_policy]:
              aws.organizations.policy.present:
                - name: 'string'
                - resource_id: 'string'
                - description: 'string'
                - policy_type: 'SERVICE_CONTROL_POLICY|TAG_POLICY|BACKUP_POLICY|AISERVICES_OPT_OUT_POLICY'
                - content: 'string'
                - tags:
                    'string': 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_organizations_policy:
              aws.organizations.policy.present:
                - name: 'idem_test_policy'
                - description: 'Enables admins of attached accounts to delegate all S3 permissions'
                - policy_type: 'SERVICE_CONTROL_POLICY'
                - content:
                    Version: '2012-10-17'
                    Statement:
                      - Sid: 'AllowAllS3Actions'
                        Effect: 'Allow'
                        Action: ['s3:*']
                - tags:
                    provider: idem
    """
    result = dict(comment=[], name=name, result=True, old_state=None, new_state=None)
    before = None

    if resource_id:
        before = await hub.exec.aws.organizations.policy.get(
            ctx=ctx, name=name, resource_id=resource_id
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)
    change_dict = dict(Name=None, Description=None, Content=None)

    resource_updated = False

    # Standardise on the json format
    content = hub.tool.aws.state_comparison_utils.standardise_json(content)

    if before:
        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.organizations.policy", name=name
        )
        result["old_state"] = copy.deepcopy(before["ret"])
        plan_state = copy.deepcopy(result["old_state"])

        resource_id = before["ret"]["resource_id"]

        try:
            if before["ret"]["name"] != name:
                change_dict["Name"] = name

            if before["ret"]["description"] != description:
                change_dict["Description"] = description

            if not hub.tool.aws.state_comparison_utils.are_policies_equal(
                before["ret"]["content"], content
            ):
                change_dict["Content"] = content

            if any(value is not None for value in change_dict.values()):
                if ctx.get("test", False):
                    plan_state["resource_id"] = resource_id
                    if change_dict.get("Name"):
                        plan_state["name"] = change_dict.get("Name")
                    if change_dict.get("Description"):
                        plan_state["description"] = change_dict.get("Description")
                    if change_dict.get("Content"):
                        plan_state["content"] = change_dict.get("Content")
                    result[
                        "comment"
                    ] += hub.tool.aws.comment_utils.would_update_comment(
                        resource_type="aws.organizations.policy", name=name
                    )
                else:
                    update_policy_ret = (
                        await hub.exec.boto3.client.organizations.update_policy(
                            ctx,
                            PolicyId=resource_id,
                            Name=change_dict.get("Name"),
                            Description=change_dict.get("Description"),
                            Content=change_dict.get("Content"),
                        )
                    )

                    if not update_policy_ret["result"]:
                        result["comment"] = (
                            result["comment"] + update_policy_ret["comment"]
                        )
                        result["result"] = update_policy_ret["result"]
                        return result
                    resource_updated = True
                    result["comment"] += [f"Updated aws.organizations.policy '{name}'"]

            # Update tags
            if (tags is not None) and tags != result["old_state"].get("tags"):
                update_ret = await hub.tool.aws.organizations.tag.update_tags(
                    ctx,
                    resource_id=resource_id,
                    old_tags=result["old_state"].get("tags"),
                    new_tags=tags,
                )
                result["result"] = result["result"] and update_ret["result"]
                result["comment"] += update_ret["comment"]
                resource_updated = resource_updated or bool(update_ret["result"])
                if ctx.get("test", False) and update_ret["ret"] is not None:
                    plan_state["tags"] = update_ret["ret"]

        except hub.tool.boto3.exception.ClientError as e:
            result["result"] = False
            result["comment"] += [f"{e.__class__.__name__}: {e}"]

    else:
        # Policy does not exist , create
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "description": description,
                    "policy_type": policy_type,
                    "content": content,
                    "tags": tags,
                },
            )
            result["comment"] += hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.organizations.policy", name=name
            )
            return result

        create_policy_ret = await hub.exec.boto3.client.organizations.create_policy(
            ctx,
            Name=name,
            Description=description,
            Type=policy_type,
            Content=content,
            Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
            if tags
            else None,
        )
        result["result"] = create_policy_ret["result"]
        if not result["result"]:
            result["comment"] += create_policy_ret["comment"]
            return result

        resource_id = create_policy_ret["ret"]["Policy"]["PolicySummary"]["Id"]

        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.organizations.policy", name=name
        )

    if ctx.get("test", False):
        result["new_state"] = plan_state
    elif (not result["old_state"]) or resource_updated:
        after = await hub.exec.aws.organizations.policy.get(
            ctx=ctx, name=name, resource_id=resource_id
        )
        if not after["result"] or not after["ret"]:
            result["result"] = False
            result["comment"] = after["comment"]
            return result
        result["new_state"] = copy.deepcopy(after["ret"])
    else:
        result["new_state"] = copy.deepcopy(result["old_state"])

    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deletes the specified policy from your organization.

    Before you perform this operation, you must first detach the policy from all organizational units (OUs), roots,
    and accounts. This operation can be called only from the organization's management account.

    Args:
        name(str): The name of the policy.
        resource_id(str, Optional): The ID of the policy in Amazon Web Services.

    Request syntax:
      .. code-block:: sls

          [idem_test_aws_organizations_policy]:
            aws.organizations.policy.absent:
              - name: 'string'
              - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_organizations_policy:
              aws.organizations.policy.absent:
                - name: 'idem_test_policy'
                - resource_id: 'p-123456789012'
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.organizations.policy", name=name
        )
        return result

    before = await hub.exec.aws.organizations.policy.get(
        ctx=ctx, name=name, resource_id=resource_id
    )

    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result

    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.organizations.policy", name=name
        )
    else:
        result["old_state"] = copy.deepcopy(before["ret"])
        if ctx.get("test", False):
            result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
                resource_type="aws.organizations.policy", name=name
            )
            return result

        delete_ret = await hub.exec.boto3.client.organizations.delete_policy(
            ctx, PolicyId=resource_id
        )
        if not delete_ret["result"]:
            result["comment"] += delete_ret["comment"]
            result["result"] = delete_ret["result"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.organizations.policy", name=name
        )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Gets information about the Organization Policy.

    Describes AWS Organization Policies in a way that can be recreated/managed with the corresponding present
    function.

    Returns:
        Dict[str, Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.organizations.policy
    """
    result = {}
    list_all_policies = []
    filters = [
        "SERVICE_CONTROL_POLICY",
        "TAG_POLICY",
        "BACKUP_POLICY",
        "AISERVICES_OPT_OUT_POLICY",
    ]

    for filter in filters:
        list_policies = await hub.exec.boto3.client.organizations.list_policies(
            ctx, Filter=filter
        )

        if not list_policies:
            hub.log.warning(
                f"Could not describe policy with error: {list_policies['comment']}"
            )
            return {}

        if list_policies["ret"]["Policies"]:
            list_all_policies.extend(list_policies["ret"]["Policies"])

    for policy in list_all_policies:
        policy_id = policy["Id"]

        policy_ret = await hub.exec.aws.organizations.policy.get(
            ctx, resource_id=policy_id
        )

        if not policy_ret["result"]:
            hub.log.info(
                f"Failed to retrieve aws.organizations.policy with id {policy_id}"
            )
            continue

        result[policy_id] = {
            "aws.organizations.policy.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in policy_ret["ret"].items()
            ]
        }

    return result
