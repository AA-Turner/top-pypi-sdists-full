"""State module for managing Organization Configuration."""
from dataclasses import field
from typing import Any
from typing import Dict

__contracts__ = ["resource"]

from dataclasses import make_dataclass


async def present(
    hub,
    ctx,
    name: str,
    auto_enable: bool,
    resource_id: str = None,
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
) -> Dict[str, Any]:
    """Updates the delegated administrator account with the values provided.

    Args:
        name(str):
            An Idem name of the resource.
        auto_enable(bool):
            Indicates whether to automatically enable member accounts in the organization.
        resource_id(str, Optional):
            The ID of the detector to update the delegated administrator for.
        data_sources(dict, Optional):
            Describes which data sources will be updated.

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

    Request Syntax:

        Using in a state:

        .. code-block:: yaml

             aws.guardduty.organization_configuration.present:
                - name: 'string'
                - resource_id: 'string'
                - auto_enable: True|False
                - data_sources:
                    S3Logs:
                        Enable: True|False
                    Kubernetes:
                        AuditLogs:
                            Enable: True|False
                    MalwareProtection:
                        ScanEc2InstanceWithFindings:
                            EbsVolumes: True|False

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              aws.guardduty.organization_configuration.present:
                - name: 6ec3816a325af96978c683c9c81fdf0a
                - resource_id: 6ec3816a325af96978c683c9c81fdf0a
                - auto_enable: false
                - data_sources:
                    Kubernetes:
                        AuditLogs:
                            AutoEnable: false
                    MalwareProtection:
                        ScanEc2InstanceWithFindings:
                            EbsVolumes:
                                AutoEnable: false
                    S3Logs:
                        AutoEnable: false
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        resource_id = name

    before = await hub.exec.aws.guardduty.organization_configuration.get(
        ctx, resource_id=resource_id
    )
    if not before["result"]:
        result["result"] = before["result"]
        result["comment"] = before["comment"]
        return result

    result["old_state"] = before["ret"]
    if ctx.get("test", False):
        result["comment"] = hub.tool.aws.comment_utils.would_update_comment(
            resource_type="aws.guardduty.organization_configuration",
            name=resource_id,
        )
        result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
            enforced_state={},
            desired_state={
                "name": name,
                "auto_enable": auto_enable,
                "resource_id": resource_id,
            },
        )
        return result

    ret = await hub.exec.aws.guardduty.organization_configuration.update(
        ctx,
        resource_id=resource_id,
        auto_enable=auto_enable,
        data_sources=data_sources,
        org_conf=before,
    )

    result["result"] = ret["result"]
    result["comment"] = ret["comment"]
    if not result["result"]:
        return result

    after = await hub.exec.aws.guardduty.organization_configuration.get(
        ctx, resource_id=resource_id
    )
    result["new_state"] = after["ret"]
    return result


async def absent(hub, ctx, name: str) -> Dict[str, Any]:
    """A No-Op function for aws.guardduty.organization_configuration.

    This is a configuration resource of the aws.guardduty.organization_configuration resource.
    It's not possible to delete aws.guardduty.organization_configuration.
    If you want to modify the aws.guardduty.organization_configuration resource,
    use the aws.guardduty.organization_configuration.present.

    Args:
        name:
            An Idem name of the resource.

    Request Syntax:
        .. code-block:: sls

            [guardduty.organization_configuration_id]:
              aws.guardduty.organization_configuration.absent:
                - name: "string"

    Returns:
        Dict[str, Any]
    """
    result = dict(
        comment=(
            "No-Op: The aws.guardduty.organization_configuration can not be deleted",
        ),
        old_state=None,
        new_state=None,
        name=name,
        result=True,
    )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        Calling from the CLI:

        .. code-block:: bash

            $ idem describe aws.guardduty.organization_configuration
    """
    result = {}

    ret = await hub.exec.aws.guardduty.detector.list(ctx, name="list detectors")

    if not ret["result"]:
        hub.log.warning(f"Could not list detector {ret['comment']}")
        return {}

    for detector in ret["ret"]:
        response = await hub.exec.aws.guardduty.organization_configuration.get(
            ctx, resource_id=detector.get("resource_id")
        )
        if not response["result"]:
            hub.log.warning(
                f"Could not list organization_configuration {ret['comment']}"
            )
        else:
            result[detector.get("resource_id")] = {
                "aws.guardduty.organization_configuration.present": [
                    {parameter_key: parameter_value}
                    for parameter_key, parameter_value in response["ret"].items()
                ]
            }
    return result
