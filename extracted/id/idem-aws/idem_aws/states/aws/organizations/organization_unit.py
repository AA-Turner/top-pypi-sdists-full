"""State module for managing Amazon Organization Units."""
import copy
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]

ALREADY_EXISTS = "already exists"

TREQ = {
    "absent": {
        "require": [
            "aws.organizations.account.absent",
        ],
    },
    "present": {
        "require": [
            "aws.organizations.organization.present",
        ],
    },
}


async def present(
    hub,
    ctx,
    name: str,
    parent_id: str,
    tags: List[Dict[str, Any]] or Dict[str, Any] = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Creates an organizational unit (OU) within a root or parent OU.

    An OU is a container for accounts that enables you to organize your accounts to apply policies according
    to your business requirements. The number of levels deep that you can nest OUs is dependent upon the policy
    types enabled for that root. For service control policies, the limit is five.

    Args:
        name(str):
            An Idem name of the resource.
        parent_id(str):
            The unique identifier (ID) of the parent root or OU that you want to create the new OU in.
        resource_id(str, Optional):
            The ID of the organization unit in Amazon Web Services.
        tags(dict or list, Optional):
            Dict in the format of ``{tag-key: tag-value}`` or List of tags in the format of
            ``[{"Key": tag-key, "Value": tag-value}]`` to associate with the organization unit.

            * Key (*str*):
                The key identifier, or name, of the tag.
            * Value (*str*):
                The string value that's associated with the key of the tag.

    Request Syntax:
      .. code-block:: sls

        [idem_test_aws_organizations_organization_unit]:
          aws.organizations.organization_unit.present:
          - name: 'string'
          - resource_id: 'string'
          - parent_id: 'string'
          - tags:
            - Key: 'string'
              Value: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_organizations_organization_unit:
              aws.organizations.organization_unit.present:
                - name: 'idem_test_organization_unit'
                - parent_id: 'o-parent-id'
                - tags:
                  - Key: 'provider'
                    Value: 'idem'
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    existing_tags = None

    if resource_id:
        before = await hub.exec.boto3.client.organizations.describe_organizational_unit(
            ctx, OrganizationalUnitId=resource_id
        )
    update = False
    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)
    if not before:
        # organization unit does not exist, create

        try:
            if ctx.get("test", False):
                result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                    enforced_state={},
                    desired_state={
                        "parent_id": parent_id,
                        "name": name,
                        "tags": tags,
                    },
                )
                result["comment"] += [
                    f"Would create aws.organizations.organization_unit '{name}'."
                ]
                return result

            create_ret = (
                await hub.exec.boto3.client.organizations.create_organizational_unit(
                    ctx,
                    ParentId=parent_id,
                    Name=name,
                    Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
                    if tags
                    else None,
                )
            )

            result["result"] = create_ret["result"]

            if not result["result"]:
                result["comment"] += create_ret["comment"]
                return result
            resource_id = create_ret["ret"]["OrganizationalUnit"]["Id"]
            result["comment"] += [
                f"Created aws.organizations.organization_unit '{name}'."
            ]
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False
    else:
        # organizational_unit exists , update
        existing_ou_name = before["ret"]["OrganizationalUnit"]["Name"]

        old_tags = await hub.exec.boto3.client.organizations.list_tags_for_resource(
            ctx, ResourceId=resource_id
        )
        if not old_tags["result"]:
            hub.log.debug(
                f"Unable to list tags for resource {resource_id} with error: {old_tags['comment']}"
            )
            result["comment"] += old_tags["comment"]
            result["result"] = old_tags["result"]
        else:
            existing_tags = old_tags["ret"]["Tags"]

        result[
            "old_state"
        ] = hub.tool.aws.organizations.conversion_utils.convert_raw_ou_to_present(
            before["ret"]["OrganizationalUnit"], parent_id, existing_tags
        )
        plan_state = copy.deepcopy(result["old_state"])

        try:
            if existing_ou_name != name:
                if ctx.get("test", False):
                    plan_state["name"] = name
                else:
                    update_ret = await hub.exec.boto3.client.organizations.update_organizational_unit(
                        ctx,
                        OrganizationalUnitId=resource_id,
                        Name=name,
                    )
                    result["result"] = update_ret["result"]
                    if not result["result"]:
                        result["comment"] += update_ret["comment"]
                        return result
                    result["comment"] += [
                        f"Updated ou name on aws.organizations.organization_unit '{name}'."
                    ]

                update = True
            if tags is not None and tags != result["old_state"].get("tags"):
                update_tags_ret = await hub.tool.aws.organizations.tag.update_tags(
                    ctx, resource_id, result["old_state"].get("tags"), tags
                )
                if not update_tags_ret["result"]:
                    result["comment"] += update_tags_ret["comment"]
                    result["result"] = False
                    return result

                elif update_tags_ret["ret"] is not None:
                    update = True
                    result["comment"] += [
                        f"Updated tags on aws.organizations.organization_unit '{name}'."
                    ]

                if ctx.get("test", False) and update_tags_ret["ret"]:
                    plan_state["tags"] = update_tags_ret["ret"]

            if not update:
                result["comment"] += [
                    f"aws.organizations.organization_unit '{name}' {ALREADY_EXISTS}."
                ]
            if ctx.get("test", False) and update:
                result["comment"] += [
                    f"Would update aws.organizations.organization_unit '{name}'"
                ]
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False

    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
            return result

        if not before or update:
            after = (
                await hub.exec.boto3.client.organizations.describe_organizational_unit(
                    ctx, OrganizationalUnitId=resource_id
                )
            )

            if after.get("ret"):
                updated_tag = (
                    await hub.exec.boto3.client.organizations.list_tags_for_resource(
                        ctx, ResourceId=resource_id
                    )
                )
                if not updated_tag["result"]:
                    hub.log.debug(
                        f"Unable to list tags for resource {resource_id} with error: {updated_tag['comment']}"
                    )
                    result["comment"] += updated_tag["comment"]
                    result["result"] = updated_tag["result"]
                result[
                    "new_state"
                ] = hub.tool.aws.organizations.conversion_utils.convert_raw_ou_to_present(
                    after["ret"]["OrganizationalUnit"],
                    parent_id,
                    updated_tag["ret"].get("Tags")
                    if updated_tag and updated_tag.get("ret")
                    else None,
                )
        else:
            result["new_state"] = copy.deepcopy(result["old_state"])
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False

    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deletes an organizational unit (OU) from a root or another OU.

    You must first remove all accounts and child OUs from the OU that you want to delete.
    This operation can be called only from the organization's management account.

    Args:
        name(str):
            An Idem name of the resource.
        resource_id(str, Optional):
            The ID of the organization unit in Amazon Web Services.

    Request syntax:
      .. code-block:: sls

        [idem_test_aws_organizations_organization_unit]:
          aws.organizations.organization_unit.absent:
            - name: 'string'
            - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_organizations_organization_unit:
              aws.organizations.organization_unit.absent:
                - name: 'idem_test_organization_unit'
                - resource_id: 'ou-rootid-ouid'
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.organizations.organization_unit",
            name=name,
        )
        return result

    before = await hub.exec.boto3.client.organizations.describe_organizational_unit(
        ctx, OrganizationalUnitId=resource_id
    )

    if not before:
        result["comment"] += [
            f"aws.organizations.organization_unit '{name}' already absent"
        ]
    else:
        result[
            "old_state"
        ] = hub.tool.aws.organizations.conversion_utils.convert_raw_ou_to_present(
            before["ret"]["OrganizationalUnit"]
        )

        if ctx.get("test", False):
            result["comment"] += [
                f"Would delete aws.organizations.organization_unit '{name}'"
            ]
            return result
        try:
            ret = await hub.exec.boto3.client.organizations.delete_organizational_unit(
                ctx, OrganizationalUnitId=resource_id
            )

            if not ret["result"]:
                result["comment"] += ret["comment"]
                result["result"] = False
                return result
            result["comment"] += [
                f"aws.organizations.organization_unit '{name}' deleted."
            ]
            result["result"] = ret["result"]
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describes AWS Organizations Units (OUs) in a way that can be recreated/managed with the corresponding "present" function.

    Idem does not support passing arguments to the describe function as of today, hence describe organization_unit
    will describe all the organizational units one level under the root of the organization.
    In future if Idem starts supporting input arguments, we can pass any parent_id and this function will list
    all organizational units one level under the parent.

    Returns:
        Dict[str, Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.organizations.organization_unit
    """
    result = {}

    list_roots_resp = await hub.exec.boto3.client.organizations.list_roots(ctx)

    if not (list_roots_resp and list_roots_resp["ret"].get("Roots")):
        return result

    parent_id = list_roots_resp["ret"]["Roots"][0]["Id"]

    if parent_id is None:
        return result

    org_units = (
        await hub.exec.boto3.client.organizations.list_organizational_units_for_parent(
            ctx, ParentId=parent_id
        )
    )

    if not org_units["result"]:
        hub.log.warning(
            f"Could not describe organization units for parent_id {parent_id} with error: {org_units['comment']}"
        )
        return {}

    organizational_units = org_units["ret"]["OrganizationalUnits"]

    for ou in organizational_units:
        tags = await hub.exec.boto3.client.organizations.list_tags_for_resource(
            ctx, ResourceId=ou["Id"]
        )
        if not tags["result"]:
            hub.log.debug(
                f"Unable to list tags for resource {ou['Id']} with error: {tags['comment']}"
            )
            continue
        translated_resource = (
            hub.tool.aws.organizations.conversion_utils.convert_raw_ou_to_present(
                ou, parent_id, tags["ret"].get("Tags") if tags else None
            )
        )

        result[ou["Name"]] = {
            "aws.organizations.organization_unit.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in translated_resource.items()
            ]
        }

    return result
