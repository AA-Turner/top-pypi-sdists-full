"""State module for managing Amazon Organizations."""
import copy
from typing import Any
from typing import Dict

__contracts__ = ["resource"]

AWS_Org_Not_In_Use_Exception = "AWSOrganizationsNotInUseException"
ALREADY_EXISTS = "already exists"

TREQ = {
    "absent": {
        "require": [
            "aws.organizations.organization_unit.absent",
        ],
    },
}


async def present(hub, ctx, name: str, feature_set: str) -> Dict[str, Any]:
    """Creates an AWS organization.

    The account whose user is calling the operation automatically becomes the management account of the new organization.
    This operation must be called using credentials from the account that is to become the new organization's management account.
    The principal must also have the relevant IAM permissions.

    Args:
        name(str):
            The name of the organization.
        feature_set(str):
            Specifies the feature set supported by the new organization. Each feature set supports different levels of functionality.

            * ``CONSOLIDATED_BILLING``: All member accounts have their bills consolidated to and paid by the management account.
            * ``ALL``: In addition to all the features supported by the consolidated billing feature set, the management account can also apply any policy type to any member account in the organization.

    Request Syntax:
      .. code-block:: sls

        [idem_test_aws_organizations_organization]:
          aws.organizations.organization.present:
          - name: 'string'
          - feature_set: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_organizations_organization:
              aws.organizations.organization.present:
                - name: 'idem_test_organization'
                - feature_set: 'ALL
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    before = await hub.exec.boto3.client.organizations.describe_organization(ctx)

    if not before:
        # Org not present , create

        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "feature_set": feature_set,
                },
            )
            result["comment"] += [
                f"Would create aws.organizations.organization '{name}'."
            ]
            return result

        try:
            ret = await hub.exec.boto3.client.organizations.create_organization(
                ctx, FeatureSet=feature_set
            )

            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] += ret["comment"]
                return result
            result["comment"] += [f"Created aws.organizations.organization {name}."]
            after = await hub.exec.boto3.client.organizations.describe_organization(ctx)
            if after and after.get("ret"):
                result[
                    "new_state"
                ] = hub.tool.aws.organizations.conversion_utils.convert_raw_organization_to_present(
                    after["ret"]["Organization"], name
                )
                roots_resp = await hub.exec.boto3.client.organizations.list_roots(ctx)

                if roots_resp and roots_resp["ret"] and roots_resp["ret"]["Roots"]:
                    result["new_state"]["roots"] = roots_resp["ret"]["Roots"]
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False
    else:
        # Org present
        result[
            "old_state"
        ] = hub.tool.aws.organizations.conversion_utils.convert_raw_organization_to_present(
            before["ret"]["Organization"], name
        )
        roots_resp = await hub.exec.boto3.client.organizations.list_roots(ctx)

        if roots_resp and roots_resp["ret"] and roots_resp["ret"]["Roots"]:
            result["old_state"]["roots"] = roots_resp["ret"]["Roots"]
        result["new_state"] = copy.deepcopy(result["old_state"])
        result["comment"] += [
            f"aws.organizations.organization '{name}' {ALREADY_EXISTS}."
        ]

    return result


async def absent(hub, ctx, name: str) -> Dict[str, Any]:
    """Deletes the organization.

    You can delete an organization only by using credentials from the management account. The organization must be empty of member accounts.

    Args:
        name(str):
            The name of the organization.

    Request syntax:
      .. code-block:: sls

        [idem_test_aws_organizations_organization]:
          aws.organizations.organization.absent:
            - name: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_organizations_organization:
              aws.organizations.organization.absent:
                - name: 'idem_test_organization'
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    before = await hub.exec.boto3.client.organizations.describe_organization(ctx)
    if before:
        result[
            "old_state"
        ] = hub.tool.aws.organizations.conversion_utils.convert_raw_organization_to_present(
            before["ret"], name
        )
        if ctx.get("test", False):
            result["comment"] += [
                f"Would delete aws.organizations.organization '{name}'."
            ]
            return result

    if not before and AWS_Org_Not_In_Use_Exception in str(before["comment"]):
        result["comment"] += [
            f"aws.organizations.organization '{name}' is already absent"
        ]
        return result
    else:
        try:
            ret = await hub.exec.boto3.client.organizations.delete_organization(ctx)

            if not ret["result"]:
                result["comment"] = ret["comment"]
                result["result"] = False
                return result
            result["comment"] += [f"aws.organizations.organization {name} deleted."]
            result["result"] = ret["result"]
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]

    try:
        after = await hub.exec.boto3.client.organizations.describe_organization(ctx)
        if after.get("ret"):
            result[
                "new_state"
            ] = hub.tool.aws.organizations.conversion_utils.convert_raw_organization_to_present(
                after["ret"], name
            )
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describes AWS Organizations in a way that can be recreated/managed with the corresponding "present" function.

    Returns:
        Dict[str, Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.organizations.organization
    """
    result = {}
    ret = await hub.exec.boto3.client.organizations.describe_organization(ctx)
    if not ret["result"]:
        hub.log.warning(
            f"Could not describe organization with error:  {ret['comment']}"
        )
        return {}

    resource = ret["ret"]["Organization"]

    translated_resource = (
        hub.tool.aws.organizations.conversion_utils.convert_raw_organization_to_present(
            resource
        )
    )
    roots_resp = await hub.exec.boto3.client.organizations.list_roots(ctx)

    if roots_resp and roots_resp["ret"] and roots_resp["ret"]["Roots"]:
        translated_resource["roots"] = roots_resp["ret"]["Roots"]
    result[resource["Id"]] = {
        "aws.organizations.organization.present": [
            {parameter_key: parameter_value}
            for parameter_key, parameter_value in translated_resource.items()
        ]
    }

    return result
