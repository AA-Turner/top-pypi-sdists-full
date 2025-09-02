"""State module for adding/deleting members from Guardduty."""
import copy
from typing import Any
from typing import Dict

__contracts__ = ["resource"]

TREQ = {
    "absent": {
        "require": ["aws.guardduty.organization_admin_account.absent"],
    },
    "present": {
        "require": [
            "aws.guardduty.detector.present",
            "aws.guardduty.organization_admin_account.present",
        ],
    },
}


async def present(
    hub,
    ctx,
    name: str,
    detector_id: str,
    account_id: str,
    email: str,
    resource_id: str = None,
) -> Dict[str, Any]:
    r"""Add member to AWS Guardduty.

    Creates a member account under Guardduty by specifying Amazon Web Services account ID for the member account.
    This step is a prerequisite for managing the associated member accounts either by invitation or
    through an organization. When using Create Members as an organizations delegated administrator this action will
    enable GuardDuty in the added member accounts, with the exception of the organization delegated administrator
    account, which must enable GuardDuty prior to being added as a member. If you are adding accounts by invitation
    use this action after GuardDuty has been enabled in potential member accounts and before using  Invite Members .

    Args:
        name(str):
            An Idem name of the resource.

        detector_id(str):
            AWS Guardduty detector ID

        account_id(str):
            The member account ID.

        email(str):
            The email address of the member account.

        resource_id(str, Optional):
            An identifier refers to an existing resource. The format is <detector_id>:<account_id>

    Request Syntax:
      .. code-block:: sls
        [idem_test_aws_guardduty_member]:
          aws.guardduty.member.present:
            - name: 'string'
            - detector_id: 'string'
            - account_id: 'string'
            - email: 'string'
            - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              aws.guardduty.member.present:
                - name: 'create_members'
                - detector_id: "68c25425ab84ea0dcae26311eddacd34"
                - resource_id: "68c25425ab84ea0dcae26311eddacd34:496603212238"
                - account_id: "496603212238"
                - email: "xyz@vmware.com"
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    update_needed = False
    revised_account_details = []
    # pre-processing for create_members call
    entry = {"AccountId": account_id, "Email": email}
    revised_account_details.append(entry)
    before = await hub.exec.aws.guardduty.member.get(
        ctx,
        detector_id=detector_id,
        account_id=account_id,
        resource_id=resource_id,
        name=name,
    )
    if not before["result"]:
        result["result"] = before["result"]
        result["comment"] = before["comment"]
        return result
    if not before["ret"]:
        # create new resource
        update_needed = True
    else:
        # check if existing member needs to be added
        member_details = before["ret"]
        if member_details.get("relationship_status") not in ("Created", "Enabled"):
            update_needed = True
    if update_needed:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "resource_id": resource_id,
                    "detector_id": detector_id,
                    "account_id": account_id,
                    "email": email,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.guardduty.member", name=name
            )
            return result
        ret = await hub.exec.boto3.client.guardduty.create_members(
            ctx, DetectorId=detector_id, AccountDetails=revised_account_details
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.guardduty.member", name=name
        )
        resource_id = detector_id + ":" + account_id
    else:
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.guardduty.member", name=name
        )
    if update_needed:
        after = await hub.exec.aws.guardduty.member.get(
            ctx,
            detector_id=detector_id,
            account_id=account_id,
            resource_id=resource_id,
            name=name,
        )
        if not after["result"]:
            result["result"] = after["result"]
            result["comment"] += after["comment"]
            return result
        result["new_state"] = after["ret"]
    else:
        result["new_state"] = copy.deepcopy(result["old_state"])
    return result


async def absent(
    hub,
    ctx,
    name: str,
    detector_id: str = None,
    account_id: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    r"""Delete member from AWS Guardduty.

    Deletes GuardDuty member account specified by the account ID.

    Args:
        name(str):
            An Idem name of the resource.

        detector_id(str, Optional):
            AWS Guardduty Detector id

        account_id(str, Optional):
            AWS Guardduty member account id

        resource_id(str, Optional):
            An identifier refers to an existing resource. The format is <detector_id>:<account_id>

    Request Syntax:
      .. code-block:: sls
        [idem_test_aws_guardduty_member]:
          aws.guardduty.member.absent:
            - name: 'string'
            - detector_id: 'string'
            - account_id: 'string'
            - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.guardduty.member.absent:
                - name: test_delete_members
                - detector_id: '68c25425ab84ea0dcae26311eddacd34'
                - account_id: '106828723025'
                - resource_id: '68c25425ab84ea0dcae26311eddacd34:106828723025'
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.guardduty.member", name=name
        )
        return result

    if not detector_id or not account_id:
        result["comment"] = hub.tool.aws.comment_utils.missing_args_for_absent_comment(
            resource_type="aws.guardduty.member",
            name=name,
            args=["detector_id", "account_id"],
        )
        result["result"] = False
        return result

    before = await hub.exec.aws.guardduty.member.get(
        ctx,
        detector_id=detector_id,
        account_id=account_id,
        resource_id=resource_id,
        name=name,
    )

    if not before["result"]:
        result["result"] = before["result"]
        result["comment"] = before["comment"]
        return result

    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.guardduty.member", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.guardduty.member", name=name
        )
        return result
    else:
        account_ids = [account_id]
        result["old_state"] = before["ret"]
        try:
            ret = await hub.exec.boto3.client.guardduty.delete_members(
                ctx, DetectorId=detector_id, AccountIds=account_ids
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result
            result["comment"] = hub.tool.aws.comment_utils.delete_comment(
                resource_type="aws.guardduty.member", name=name
            )
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    List details about all member accounts for the current GuardDuty administrator account.
    Describe returns detector_id, master_id, relationship_status, invited_at, updated_at, administrator_id as additional params
    not used in present input

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.guardduty.member
    """

    result = {}
    ret = await hub.exec.boto3.client.guardduty.list_detectors(ctx)
    if not ret["ret"]["DetectorIds"]:
        hub.log.warning(f"Could not list detector {ret['comment']}")
        return {}

    for detector_id in ret["ret"]["DetectorIds"]:
        members = await hub.exec.aws.guardduty.member.list(
            ctx,
            detector_id=detector_id,
            name=f"Describe members for detector {detector_id}",
        )
        if not members["result"]:
            hub.log.debug(f"Could not find members for detector {detector_id}")
            continue

        for member in members["ret"]:
            account_id = member.get("account_id")
            resource_id = detector_id + ":" + account_id
            # to avoid any other state overriding describe if just resource_id is the state_id
            resource_key = f"aws-guardduty-member-{resource_id}"
            result[resource_key] = {
                "aws.guardduty.member.present": [
                    {parameter_key: parameter_value}
                    for parameter_key, parameter_value in member.items()
                ]
            }
    return result
