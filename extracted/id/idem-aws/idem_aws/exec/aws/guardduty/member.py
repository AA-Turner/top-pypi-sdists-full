"""Exec module for managing Guardduty members."""
from typing import Any
from typing import Dict

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    detector_id: str,
    account_id: str,
    resource_id: str = None,
    name: str = None,
) -> Dict[str, Any]:
    """Get info about AWS Guardduty member based on resource_id which is the combination of detector_id:account_id.

    Args:
        detector_id(str):
            AWS Guardduty Detector id

        account_id(str):
            AWS Guardduty member account_id

        resource_id(str, Optional):
            Combination of AWS Guardduty Detector id and AWS Guardduty Member account id. Format:detector_id:account_id

        name(str, Optional):
            Name of the Idem state

    Returns:
        Dict[str, Any]:
            Returns guardduty member in present format

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec aws.guardduty.member.get name="get member" detector_id="detector_id" account_id="account_id" resource_id="detector_id:account_id"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resources:
              exec.run:
                - path: aws.guardduty.member.get
                - kwargs:
                    name: "get Guardduty member"
                    detector_id: "7ec2638373ab39e421bbc97333706434"
                    account_id: "257230699585"
                    resource_id: "7ec2638373ab39e421bbc97333706434:257230699585 "
    """
    result = dict(comment=[], result=True, ret=None)

    if resource_id and ":" in resource_id:
        extracted_detector_id = resource_id.split(":")[0]
        extracted_account_id = resource_id.split(":")[1]
        if extracted_detector_id != detector_id:
            result["result"] = False
            result[
                "comment"
            ] = f"Detector_id {extracted_detector_id} from resource_id and detector_id {detector_id} passed as arg do not match."
            return result
        elif extracted_account_id != account_id:
            result["result"] = False
            result[
                "comment"
            ] = f"Account_id {extracted_account_id} from resource_id and account_id {account_id} passed as arg do not match."
            return result
        else:
            detector_id = extracted_detector_id
            account_id = extracted_account_id
    account_ids = [account_id]
    ret = await hub.exec.boto3.client.guardduty.get_members(
        ctx, DetectorId=detector_id, AccountIds=account_ids
    )

    if not ret["result"]:
        result["result"] = ret["result"]
        result["comment"] += list(ret["comment"])
        return result

    members = ret["ret"]["Members"]
    if not members:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.guardduty.member", name=name
            )
        )
        return result
    resource = members[0]
    if len(members) > 1:
        result["comment"].append(
            f"More than one aws.guardduty.member resource was found. Use resource {resource.get('AccountId')}"
        )
    result[
        "ret"
    ] = hub.tool.aws.guardduty.conversion_utils.convert_raw_member_to_present(
        member=resource,
        idem_resource_name=name,
        detector_id=detector_id,
    )

    return result


async def list_(
    hub, ctx, detector_id: str, name: str = None, only_associated: str = "False"
) -> Dict[str, Any]:
    """List AWS Guardduty members for a detector.

    Args:
        detector_id(str):
            AWS Guardduty Detector id

        name(str, Optional):
            Name of the Idem state.

        only_associated(str, Optional):
            Specifies whether to only return associated members or return all members.
            All members will include members that haven't been invited or have been disassociated."

    Returns:
        Dict[str, Any]:
            Returns guardduty members in present format

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec aws.guardduty.member.list name="list members" detector_id="detector_id" only_associated="False"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resources:
              exec.run:
                - path: aws.guardduty.member.list
                - kwargs:
                    name: my_resources
                    detector_id: "a6c242807703f20b65afd91d54dc8fb2"
                    only_associated: 'False'
    """
    result = dict(comment=[], result=True, ret=[])
    ret = await hub.exec.boto3.client.guardduty.list_members(
        ctx, DetectorId=detector_id, OnlyAssociated=only_associated
    )
    if not ret["result"]:
        result["result"] = ret["result"]
        result["comment"] += list(ret["comment"])
        return result

    if not ret["ret"]["Members"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.guardduty.member", name=name
            )
        )
        return result
    # list_members returns the same response as get_members so directly passing it to conversion_utils
    for member in ret["ret"]["Members"]:
        result["ret"].append(
            hub.tool.aws.guardduty.conversion_utils.convert_raw_member_to_present(
                member=member,
                idem_resource_name=name,
                detector_id=detector_id,
            )
        )
    return result
