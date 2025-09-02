import copy
from typing import Any
from typing import Dict


async def update(
    hub,
    ctx,
    before: Dict[str, Any],
    detector_id: str = None,
    finding_publishing_frequency: str = None,
    data_sources: Dict[str, Any] = None,
):
    result = dict(comment=[], result=True, ret=None)
    compare_dict_result = False
    update_payload = {}
    if (finding_publishing_frequency is not None) and before["ret"].get(
        "finding_publishing_frequency"
    ) != finding_publishing_frequency:
        update_payload["FindingPublishingFrequency"] = finding_publishing_frequency
    if data_sources:
        compare_dict_result = hub.tool.aws.guardduty.detector.compare_data_sources(
            data_sources, before["ret"].get("data_sources")
        )
    if not compare_dict_result and data_sources is not None:
        update_payload["DataSources"] = data_sources
    if update_payload:
        if not ctx.get("test", False):
            update_ret = await hub.exec.boto3.client.guardduty.update_detector(
                ctx=ctx, DetectorId=detector_id, **update_payload
            )
            if not update_ret["result"]:
                result["comment"] = update_ret["comment"]
                result["result"] = False
                return result
        result["ret"] = {}
        if "FindingPublishingFrequency" in update_payload:
            result["ret"]["finding_publishing_frequency"] = update_payload[
                "FindingPublishingFrequency"
            ]
            result["comment"] += [
                f"Update finding_publishing_frequency: {update_payload['FindingPublishingFrequency']}"
            ]
        if "DataSources" in update_payload:
            result["ret"]["data_sources"] = update_payload["DataSources"]
            result["comment"] += [
                f"Update data_sources: {update_payload['DataSources']}"
            ]
    return result


async def update_tags(
    hub,
    ctx,
    resource_arn,
    old_tags: Dict[str, Any],
    new_tags: Dict[str, Any],
):
    """

    Args:
        hub:
        ctx:
        resource_arn: aws resource arn
        old_tags: dict of old tags
        new_tags: dict of new tags

    Returns:
        {"result": True|False, "comment": "A message", "ret": None}

    """

    tags_to_add = {}
    tags_to_remove = []
    tags_result = {}
    if old_tags:
        tags_result = copy.deepcopy(old_tags)
    if new_tags is not None:
        for key, value in new_tags.items():
            if (key in old_tags and old_tags.get(key) != new_tags.get(key)) or (
                key not in old_tags
            ):
                tags_to_add[key] = value
    if old_tags:
        for key in old_tags:
            if key not in new_tags:
                tags_to_remove.append(key)
    result = dict(comment=[], result=True, ret=None)
    if (not tags_to_remove) and (not tags_to_add):
        return result
    if tags_to_remove:
        if not ctx.get("test", False):
            delete_ret = await hub.exec.boto3.client.guardduty.untag_resource(
                ctx, ResourceArn=resource_arn, TagKeys=tags_to_remove
            )
            if not delete_ret["result"]:
                result["comment"] = delete_ret["comment"]
                result["result"] = False
                return result
        [tags_result.pop(key, None) for key in tags_to_remove]
    if tags_to_add:
        if not ctx.get("test", False):
            add_ret = await hub.exec.boto3.client.guardduty.tag_resource(
                ctx, ResourceArn=resource_arn, Tags=tags_to_add
            )
            if not add_ret["result"]:
                result["comment"] = add_ret["comment"]
                result["result"] = False
                return result
    tags_to_append = {**tags_result, **tags_to_add}
    result["ret"] = {"tags": tags_to_append}
    result["comment"] += [f"Update tags: Add [{tags_to_add}] Remove [{tags_to_remove}]"]
    return result


def render_data_sources(hub, detector_describe: Dict[str, Any]) -> Dict[str, Any]:
    """
    The syntax for data_sources parameter is different in create and update scenarios. So to make it similar we are
    rendering the data  so that it can be used in update and describe functions.

    Returns:
        Dict

    """
    data_sources_new = {}
    kubernetes_source = {}
    malware_protection_source = {}
    s3_logs = {}
    if "DataSources" in detector_describe:
        if "Kubernetes" in detector_describe["DataSources"]:
            kubernetes_source = detector_describe["DataSources"].pop("Kubernetes")
            if kubernetes_source:
                data_sources_new["Kubernetes"] = {
                    "AuditLogs": {
                        "Enable": kubernetes_source["AuditLogs"]["Status"] == "ENABLED"
                    }
                }
        if "MalwareProtection" in detector_describe["DataSources"]:
            malware_protection_source = detector_describe["DataSources"].pop(
                "MalwareProtection"
            )
            if malware_protection_source:
                data_sources_new["MalwareProtection"] = {
                    "ScanEc2InstanceWithFindings": {
                        "EbsVolumes": malware_protection_source[
                            "ScanEc2InstanceWithFindings"
                        ]["EbsVolumes"]["Status"]
                        == "ENABLED"
                    }
                }
            if "S3Logs" in detector_describe["DataSources"]:
                s3_logs = detector_describe["DataSources"].pop("S3Logs")
                if s3_logs:
                    data_sources_new["S3Logs"] = {
                        "Enable": s3_logs["Status"] == "ENABLED"
                    }

        if kubernetes_source:
            # This is to preserve the input value. We don't have to have this, but it is safer.
            detector_describe["DataSources"]["Kubernetes"] = kubernetes_source
        if malware_protection_source:
            # This is to preserve the input value. We don't have to have this, but it is safer.
            detector_describe["DataSources"][
                "MalwareProtection"
            ] = malware_protection_source
        if s3_logs:
            detector_describe["DataSources"]["S3Logs"] = s3_logs
    return data_sources_new


def compare_data_sources(
    hub, data_sources: Dict[str, Any], data_sources_new: Dict[str, Any]
):
    """
    This functions helps in comparing two dicts.
    It compares each key value in both the dicts and return true or false based on the comparison

    Returns:
        {True|False}

    """

    for key, value in data_sources.items():
        if key in data_sources_new:
            if isinstance(data_sources[key], dict):
                if not compare_data_sources(
                    hub, data_sources[key], data_sources_new[key]
                ):
                    return False
            elif value != data_sources_new[key]:
                return False
        else:
            return False
    return True
