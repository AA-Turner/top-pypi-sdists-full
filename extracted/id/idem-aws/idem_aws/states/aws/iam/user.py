"""State module for managing IAM User."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

SERVICE = "iam"
RESOURCE = "User"

__contracts__ = ["resource"]
TREQ = {
    "absent": {
        "require": [
            "aws.iam.user_policy_attachment.absent",
        ],
    },
}


async def present(
    hub,
    ctx,
    name: str,
    user_name: str,
    resource_id: str = None,
    path: str = None,
    permissions_boundary: str = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass(
            "Tag",
            [("Key", str, field(default=None)), ("Value", str, field(default=None))],
        )
    ] = None,
) -> Dict[str, Any]:
    """Creates a new IAM user for your Amazon Web Services account.

    For information about quotas for the number of IAM users you can create, see IAM and STS quotas in the IAM User Guide.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            AWS IAM username

        user_name(str):
            The name of the user to create. IAM user, group, role, and policy names must be unique within
            the account. Names are not distinguished by case. For example, you cannot create resources named
            both "MyResource" and "myresource".

        path(str, Optional):
            The path for the user name. For more information about paths, see IAM identifiers in the IAM
            User Guide. This parameter is Optional. If it is not included, it defaults to a slash (/). This
            parameter allows (through its regex pattern) a string of characters consisting of either a
            forward slash (/) by itself or a string that must begin and end with forward slashes. In
            addition, it can contain any ASCII character from the ! (\u0021) through the DEL character
            (\u007F), including most punctuation characters, digits, and upper and lowercased letters. Defaults to None.

        permissions_boundary(str, Optional):
            The ARN of the policy that is used to set the permissions boundary for the user. Defaults to None.

        tags(dict or list, Optional):
            Dict in the format of ``{tag-key: tag-value}`` or List of tags in the format of
            ``[{"Key": tag-key, "Value": tag-value}]`` to associate with the user. Each tag consists of a key name and an
            associated value. Defaults to None.

            * Key (str):
                The key name that can be used to look up or retrieve the associated value. For example,
                Department or Cost Center are common choices.

            * Value (str):
                The value associated with this tag. For example, tags with a key name of Department could have
                values such as Human Resources, Accounting, and Support. Tags with a key name of Cost Center
                might have values that consist of the number associated with the different cost centers in your
                company. Typically, many resources have tags with the same key name but with different values.
                Amazon Web Services always interprets the tag Value as a single string. If you need to store an
                array, you can store comma-separated values in the string. However, you must interpret the value
                in your code.

    Request Syntax:
        .. code-block:: sls

            user-name:
              aws.iam.user.present:
                - user_name: 'string'
                - resource_id: 'string'
                - path: 'string'
                - permissions_boundary: 'string'
                - tags:
                  - Key: 'string'
                    Value: 'string'

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            user1:
              aws.iam.user.present:
                - user_name: iam-user-1
                - resource_id: iam-user-1
                - path: /
                - permissions_boundary: arn:aew12k3r4kr9efg9
                - tags:
                  - Key: test-key
                    Value: test-value
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    is_user_updated = False
    if resource_id:
        resource = await hub.tool.boto3.resource.create(
            ctx, SERVICE, RESOURCE, name=resource_id
        )
        before = await hub.tool.boto3.resource.describe(resource)

    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)

    if before:
        result[
            "old_state"
        ] = hub.tool.aws.iam.conversion_utils.convert_raw_user_to_present(
            raw_resource=before, idem_resource_name=name
        )
        plan_state = copy.deepcopy(result["old_state"])

        update_ret = await hub.tool.aws.iam.user.update_user(
            ctx, before=result["old_state"], user_name=user_name, path=path
        )
        result["comment"] += update_ret["comment"]
        result["result"] = update_ret["result"]
        if update_ret["ret"] and "user_name" in update_ret["ret"]:
            resource_id = user_name
        is_user_updated = bool(update_ret["ret"])
        if update_ret["ret"] and ctx.get("test", False):
            result["comment"] += [f"Would update aws.iam.user '{name}'"]
            if "user_name" in update_ret["ret"]:
                plan_state["user_name"] = update_ret["ret"]["user_name"]
                plan_state["resource_id"] = update_ret["ret"]["user_name"]
            if "path" in update_ret["ret"]:
                plan_state["path"] = update_ret["ret"]["path"]

        if tags is not None and tags != before.get("Tags", None):
            # Update tags
            update_ret = await hub.tool.aws.iam.user.update_user_tags(
                ctx,
                user_name=resource_id,
                old_tags=result["old_state"].get("tags", {}),
                new_tags=tags,
            )
            result["result"] = result["result"] and update_ret["result"]
            result["comment"] += update_ret["comment"]
            is_user_updated = is_user_updated or bool(update_ret["result"])
            if ctx.get("test", False) and update_ret["ret"] is not None:
                plan_state["tags"] = update_ret["ret"]
        if not is_user_updated:
            result["comment"] += [f"{name} already exists"]
    else:
        try:
            if ctx.get("test", False):
                result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                    enforced_state={},
                    desired_state={
                        "name": name,
                        "user_name": user_name,
                        "arn": "arn_known_after_present",
                        "permissions_boundary": permissions_boundary,
                        "path": path,
                        "tags": tags,
                    },
                )
                result["comment"] += [f"Would create aws.iam.user '{name}'"]
                return result
            # Attempt to create the User
            ret = await hub.exec.boto3.client.iam.create_user(
                ctx,
                Path=path,
                UserName=user_name,
                PermissionsBoundary=permissions_boundary,
                Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
                if tags
                else None,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result
            result["comment"] += [f"Created aws.iam.user '{name}'"]
            resource_id = user_name
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False

    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif (not before) or is_user_updated:
            resource = await hub.tool.boto3.resource.create(
                ctx, SERVICE, RESOURCE, name=resource_id
            )
            after = await hub.tool.boto3.resource.describe(resource)
            result[
                "new_state"
            ] = hub.tool.aws.iam.conversion_utils.convert_raw_user_to_present(
                raw_resource=after, idem_resource_name=name
            )
        else:
            result["new_state"] = copy.deepcopy(result["old_state"])
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False

    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deletes the specified IAM user.

    Unlike the Amazon Web Services Management Console, when you delete a user programmatically, you must delete the items
    attached to the user manually, or the deletion fails. For more information, see Deleting an IAM user.
    Before attempting to delete a user, remove the following items:
    Password (DeleteLoginProfile)   Access keys (DeleteAccessKey)   Signing certificate (DeleteSigningCertificate)
    SSH public key (DeleteSSHPublicKey)   Git credentials (DeleteServiceSpecificCredential)   Multi-factor
    authentication (MFA) device (DeactivateMFADevice, DeleteVirtualMFADevice)   Inline policies (DeleteUserPolicy)
    Attached managed policies (DetachUserPolicy)   Group memberships (RemoveUserFromGroup)

    Args:
        name(str):
            A name, ID to identify the resource.

        resource_id(str, Optional):
            The name of the user to delete. This parameter allows (through its regex pattern) a string of characters
            consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the
            following characters: _+=,.@-.

    Request syntax:
        .. code-block:: sls

            user-1:
              aws.iam.user.absent:
                - name: 'string'
                - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            user-1:
              aws.iam.user.absent:
                - name: user-1
                - resource_id: user-1
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.iam.user", name=name
        )
        return result

    resource = await hub.tool.boto3.resource.create(ctx, SERVICE, RESOURCE, resource_id)
    before = await hub.tool.boto3.resource.describe(resource)

    if not before:
        result["comment"] += [f"'{name}' already absent"]
    elif ctx.get("test", False):
        result[
            "old_state"
        ] = hub.tool.aws.iam.conversion_utils.convert_raw_user_to_present(
            raw_resource=before, idem_resource_name=name
        )
        result["comment"] += [f"Would delete aws.iam.user '{name}'"]
        return result
    else:
        result[
            "old_state"
        ] = hub.tool.aws.iam.conversion_utils.convert_raw_user_to_present(
            raw_resource=before, idem_resource_name=name
        )
        try:
            # Attempt to delete user ssh key
            user_ssh_public_keys_list = (
                await hub.exec.boto3.client.iam.list_ssh_public_keys(ctx, UserName=name)
            )
            if user_ssh_public_keys_list["result"]:
                attached_user_ssh_public_keys_list = user_ssh_public_keys_list[
                    "ret"
                ].get("SSHPublicKeys")
                for ssh_key in attached_user_ssh_public_keys_list:
                    ret_delete = await hub.exec.boto3.client.iam.delete_ssh_public_key(
                        ctx, UserName=name, SSHPublicKeyId=ssh_key.get("SSHPublicKeyId")
                    )
                    if not ret_delete["result"]:
                        result["result"] = False
                        result["comment"] = ret_delete["comment"]
                        hub.log.debug(
                            f"Could not delete user ssh key {ret_delete['comment']}"
                        )
                        return result
            else:
                if (
                    user_ssh_public_keys_list["comment"]
                    and "NoSuchEntityException"
                    in user_ssh_public_keys_list["comment"][0]
                ):
                    result["comment"] += [
                        f"No user_ssh_key associated with aws.iam.user '{name}'"
                    ]
                else:
                    result["result"] = False
                    result["comment"] = user_ssh_public_keys_list["comment"]
                    return result

            # Attempt to delete the User
            ret = await hub.exec.boto3.client.iam.delete_user(
                ctx,
                UserName=resource_id,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result
            result["comment"] = f"Deleted aws.iam.user '{name}'"
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function

    Lists the IAM users that have the specified path prefix. If no path prefix is specified, the operation returns
    all users in the Amazon Web Services account. If there are none, the operation returns an empty list.  IAM
    resource-listing operations return a subset of the available attributes for the resource. For example, this
    operation does not return tags, even though they are an attribute of the returned object. To view all of the
    information for a user, see GetUser.  You can paginate the results using the MaxItems and Marker parameters.


    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.iam.user
    """
    result = {}
    ret = await hub.exec.boto3.client.iam.list_users(ctx)

    if not ret["result"]:
        hub.log.warning(f"Could not describe user {ret['comment']}")
        return {}

    for user in ret["ret"]["Users"]:
        resource_name = user.get("UserName")
        # This is required to get tags for each user
        boto2_resource = await hub.tool.boto3.resource.create(
            ctx, "iam", "User", resource_name
        )
        resource = await hub.tool.boto3.resource.describe(boto2_resource)
        resource_id = resource.get("UserName")
        translated_resource = (
            hub.tool.aws.iam.conversion_utils.convert_raw_user_to_present(
                raw_resource=resource, idem_resource_name=resource_id
            )
        )
        resource_key = f"iam-user-{resource_id}"
        result[resource_key] = {
            "aws.iam.user.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in translated_resource.items()
            ]
        }

    return result
