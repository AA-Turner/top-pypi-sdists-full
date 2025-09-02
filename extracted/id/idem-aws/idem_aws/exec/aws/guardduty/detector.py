"""Exec module for managing Guardduty detectors."""
__func_alias__ = {"list_": "list"}

from typing import Dict


async def get(hub, ctx, resource_id: str, name: str = None) -> Dict:
    """Get info about AWS Guardduty detector based on the detector_id passed.

    Args:
        resource_id(str):
            AWS Guardduty Detector id
        name(str, Optional):
            Name of the Idem state
    """
    result = dict(comment=[], ret=None, result=True)
    before = await hub.exec.boto3.client.guardduty.get_detector(
        ctx, DetectorId=resource_id
    )
    if not before["result"]:
        if "BadRequestException" in str(before["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.guardduty.detector", name=name
                )
            )
            return result
        result["comment"] += list(before["comment"])
        result["result"] = False
        return result

    result[
        "ret"
    ] = await hub.tool.aws.guardduty.conversion_utils.convert_raw_detector_to_present_async(
        ctx, raw_resource=before, idem_resource_name=resource_id
    )
    return result


async def list_(hub, ctx, name: str = None) -> Dict:
    """List AWS guard duty detectors.

    Args:
        name(str, Optional):
            Name of the Idem state for logging purposes.

    Returns:
        Dict[str, Any]:
            Return detectors.
    """
    result = dict(comment=[], ret=[], result=True)
    before = await hub.exec.boto3.client.guardduty.list_detectors(ctx)
    if not before["result"]:
        result["comment"] += list(before["comment"])
        result["result"] = False
        return result
    if not before["ret"]["DetectorIds"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.guardduty.detector", name=name
            )
        )
        return result
    for detector_id in before["ret"]["DetectorIds"]:
        detector_ret = await get(hub, ctx, resource_id=detector_id)
        if not detector_ret["result"]:
            hub.log.warning(
                f"Could not get detector info for id {detector_id}, hence skipping it in list"
            )
            result["comment"].append(detector_ret["comment"])
            continue
        result["ret"].append(detector_ret["ret"])

    return result
