"""State module for managing Amazon GuardDuty Detector."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    enable: bool = True,
    resource_id: str = None,
    client_token: str = None,
    finding_publishing_frequency: str = None,
    data_sources: make_dataclass(
        """Describes which data sources will be enabled for the detector."""
        "DataSourceConfiguration",
        [
            (
                "S3Logs",
                make_dataclass(
                    """Describes whether S3 data event logs are enabled as a data source."""
                    "S3LogsConfiguration",
                    [("Enable", bool)],
                ),
                field(default=None),
            ),
            (
                "Kubernetes",
                make_dataclass(
                    """Describes whether any Kubernetes logs are enabled as data sources."""
                    "KubernetesConfiguration",
                    [
                        (
                            "AuditLogs",
                            make_dataclass(
                                """The status of Kubernetes audit logs as a data source."""
                                "KubernetesAuditLogsConfiguration",
                                [("Enable", bool)],
                            ),
                        )
                    ],
                ),
                field(default=None),
            ),
            (
                "MalwareProtection",
                make_dataclass(
                    """Describes whether Malware Protection is enabled as a data source."""
                    "MalwareProtectionConfiguration",
                    [
                        (
                            "ScanEc2InstanceWithFindings",
                            make_dataclass(
                                """Describes the configuration of Malware Protection for EC2 instances with findings."""
                                "ScanEc2InstanceWithFindingsConfiguration",
                                [("EbsVolumes", bool, field(default=None))],
                            ),
                            field(default=None),
                        )
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    tags: Dict[str, str] = None,
) -> Dict[str, Any]:
    """Creates an Amazon GuardDuty detector.

    A detector is a resource that represents the GuardDuty service.
    To start using GuardDuty, you must create a detector in each Region where you enable the service.
    You can have only one detector per account per Region. All data sources are enabled in a new detector by default.

    Args:
        name(str):
            An Idem name of the resource.
        resource_id(str, Optional):
            The ID of the detector in Amazon Web Services.
        enable(bool, Optional):
            A Boolean value that specifies whether the detector is to be enabled. Default value is ``True``.
        client_token(str, Optional):
            The idempotency token for the create request. This field is auto_populated if not provided.
        finding_publishing_frequency(str, Optional):
            A value that specifies how frequently updated findings are exported.
            Valid values are ``FIFTEEN_MINUTES``, ``ONE_HOUR``, ``SIX_HOURS``.
        data_sources(dict, Optional):
            Describes which data sources will be enabled for the detector.

            * S3Logs (*dict, Optional*):
                Describes whether S3 data event logs are enabled as a data source.

                * Enable (*bool*): The status of S3 data event logs as a data source.

            * Kubernetes (*dict, Optional*):
                Describes whether any Kubernetes logs are enabled as data sources.

                * AuditLogs (*dict*):
                    The status of Kubernetes audit logs as a data source.

                    * Enable (*bool*):
                        The status of Kubernetes audit logs as a data source.

            * MalwareProtection (*dict, Optional*):
                Describes whether Malware Protection is enabled as a data source.

                * ScanEc2InstanceWithFindings (*dict, Optional*):
                    Describes the configuration of Malware Protection for EC2 instances with findings.

                    EbsVolumes (*bool, Optional*):
                        Describes the configuration for scanning EBS volumes as data source.

        tags(dict, Optional):
            Dict in the format of ``{tag-key: tag-value}`` to associate with the detector.

    Request Syntax:
      .. code-block:: sls

        [idem_test_aws_guardduty_detector]:
          aws.guaardduty.detector.present:
            - name: 'string'
            - enable: True|False
            - client_token: 'string'
            - finding_publishing_frequency: 'FIFTEEN_MINUTES|ONE_HOUR|SIX_HOURS'
            - data_sources:
                S3Logs:
                  Enable: True|False
                Kubernetes:
                  AuditLogs:
                    Enable: True|False
                MalwareProtection:
                  ScanEc2InstanceWithFindings:
                    EbsVolumes: True|False
            - tags:
                'string': 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_guardduty_detector:
              aws.guardduty.detector.present:
                - name: idem_test_guardduty_detector
                - enable: True
                - finding_publishing_frequency: 'ONE_HOUR'
                - data_sources:
                    S3Logs:
                      Enable: true
                - tags:
                    provider: idem

    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False
    if resource_id:
        before = await hub.exec.aws.guardduty.detector.get(
            ctx, resource_id=resource_id, name=name
        )
        if not before["result"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result
    if not before or not before["ret"]:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "enable": enable,
                    "finding_publishing_frequency": finding_publishing_frequency,
                    "data_sources": data_sources,
                    "tags": tags,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.guardduty.detector", name=name
            )
            return result
        try:
            ret = await hub.exec.boto3.client.guardduty.create_detector(
                ctx,
                Enable=enable,
                ClientToken=client_token,
                FindingPublishingFrequency=finding_publishing_frequency,
                DataSources=data_sources,
                Tags=tags,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result
            result["comment"] = result[
                "comment"
            ] + hub.tool.aws.comment_utils.create_comment(
                resource_type="aws.guardduty.detector", name=name
            )
            resource_id = ret["ret"]["DetectorId"]
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False
            return result

    else:
        try:
            account_details = await hub.exec.boto3.client.sts.get_caller_identity(ctx)
            account_id = account_details["ret"]["Account"]
            region_name = ctx["acct"]["region_name"]
            detector_arn = hub.tool.aws.arn_utils.build(
                service="guardduty",
                region=region_name,
                account_id=account_id,
                resource="detector/" + resource_id,
            )
            result["old_state"] = copy.deepcopy(before["ret"])
            plan_state = copy.deepcopy(result["old_state"])
            update_ret = await hub.tool.aws.guardduty.detector.update(
                ctx,
                before=before,
                detector_id=resource_id,
                finding_publishing_frequency=finding_publishing_frequency,
                data_sources=data_sources,
            )
            result["comment"] += update_ret["comment"]
            result["result"] = update_ret["result"]
            resource_updated = resource_updated or bool(update_ret["ret"])
            if update_ret["ret"] and ctx.get("test", False):
                if "finding_publishing_frequency" in update_ret["ret"]:
                    plan_state["finding_publishing_frequency"] = update_ret["ret"][
                        "finding_publishing_frequency"
                    ]
                if "data_sources" in update_ret["ret"]:
                    plan_state["data_sources"] = update_ret["ret"]["data_sources"]

            if (tags is not None) and (result["old_state"].get("tags", {}) != tags):
                update_tags_ret = await hub.tool.aws.guardduty.detector.update_tags(
                    ctx=ctx,
                    resource_arn=detector_arn,
                    old_tags=result["old_state"].get("tags", {}),
                    new_tags=tags,
                )
                if not result["result"]:
                    result["comment"] = update_tags_ret["comment"]
                    result["result"] = False
                    return result
                result["comment"] += update_tags_ret["comment"]
                result["result"] = result["result"] and update_tags_ret["result"]
                resource_updated = resource_updated or bool(update_tags_ret["ret"])
                if ctx.get("test", False) and update_tags_ret["ret"] is not None:
                    plan_state["tags"] = update_tags_ret["ret"].get("tags")
            if not resource_updated:
                result["comment"] += [f"{name} already exists"]
            if ctx.get("test", False) and resource_updated:
                result["comment"] = (
                    hub.tool.aws.comment_utils.would_update_comment(
                        resource_type="aws.guardduty.detector", name=name
                    )
                    + result["comment"]
                )
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False
            return result

    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif (not before) or (not before["ret"]) or resource_updated:
            after = await hub.exec.aws.guardduty.detector.get(
                ctx, resource_id=resource_id, name=name
            )
            if not after["result"] or not after["ret"]:
                result["result"] = False
                result["comment"] = after["comment"]
                return result
            result["new_state"] = copy.deepcopy(after["ret"])
        else:
            result["new_state"] = copy.deepcopy(result["old_state"])
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False
    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Deletes an Amazon GuardDuty detector.

    Args:
        name(str):
            An Idem name of the resource.
        resource_id(str, Optional):
            The ID of the detector in Amazon Web Services.

    Request syntax:
      .. code-block:: sls

        [idem_test_aws_guardduty_detector]:
          aws.guardduty.detector.absent:
            - name: 'string'
            - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_guardduty_detector:
              aws.guardduty.detector.absent:
                - name: idem_test_guardduty_detector
                - resource_id: cebf7ced6562d943d61f76a915e32563
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.guardduty.detector", name=name
        )
        return result
    before = await hub.exec.aws.guardduty.detector.get(
        ctx, resource_id=resource_id, name=name
    )
    if not before["result"] or not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.guardduty.detector", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = copy.deepcopy(before["ret"])
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.guardduty.detector", name=name
        )
        return result
    else:
        result["old_state"] = copy.deepcopy(before["ret"])
        try:
            ret = await hub.exec.boto3.client.guardduty.delete_detector(
                ctx, DetectorId=resource_id
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                result["result"] = False
                return result
            result["comment"] = hub.tool.aws.comment_utils.delete_comment(
                resource_type="aws.guardduty.detector", name=name
            )
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describes AWS GuardDuty detectors in a way that can be recreated/managed with the corresponding "present" function.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.guardduty.detector
    """
    result = {}
    ret = await hub.exec.boto3.client.guardduty.list_detectors(ctx)

    if not ret["ret"]["DetectorIds"]:
        hub.log.warning(f"Could not list detector {ret['comment']}")
        return {}

    for resource_id in ret["ret"]["DetectorIds"]:
        detector_id = resource_id
        detector = await hub.exec.boto3.client.guardduty.get_detector(
            ctx, DetectorId=resource_id
        )

        resource_translated = await hub.tool.aws.guardduty.conversion_utils.convert_raw_detector_to_present_async(
            ctx, raw_resource=detector, idem_resource_name=detector_id
        )

        result[detector_id] = {
            "aws.guardduty.detector.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }
    return result
