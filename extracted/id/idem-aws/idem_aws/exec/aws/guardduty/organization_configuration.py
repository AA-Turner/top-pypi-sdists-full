"""Exec module for managing Organization Configuration."""
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict


async def update(
    hub,
    ctx,
    resource_id: str,
    auto_enable: bool,
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
    org_conf=None,
) -> Dict[str, Any]:
    """Updates the delegated administrator account with the values provided.

    Args:
        resource_id(str):
            The ID of the detector to update the delegated administrator for.
        auto_enable(bool):
            Indicates whether to automatically enable member accounts in the organization.
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
        org_conf(Optional):
            Describes current state of Organization Configuration.


    Returns:
        Dict[str, Any]:
            Returns organization Configuration in updated format.

    Examples:
        Calling this exec module function from the cli.

        .. code-block:: yaml

            my_unmanaged_resources:
              exec.run:
                - path: aws.guardduty.organization_configuration.update
                - kwargs:
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
    """
    result = dict(comment=[], ret=None, result=True)

    if not org_conf:
        response = await get(hub, ctx, resource_id=resource_id)
    else:
        response = org_conf
    if response["ret"]:
        resource_updated = await hub.tool.aws.guardduty.config_utils.is_organization_configuration_updated(
            before=response["ret"],
            auto_enable=auto_enable,
            data_sources=data_sources,
        )
        if resource_updated:
            ret = (
                await hub.exec.boto3.client.guardduty.update_organization_configuration(
                    ctx,
                    DetectorId=resource_id,
                    AutoEnable=auto_enable,
                    DataSources=data_sources,
                )
            )
            if ret["result"]:
                result["comment"].append(
                    hub.tool.aws.comment_utils.update_comment(
                        resource_type="aws.guardduty.organization_configuration",
                        name=resource_id,
                    )
                )
                result["ret"] = ret["ret"]
            else:
                result["result"] = ret["result"]
                result["comment"].append(ret["comment"])
            return result
        else:
            result["comment"].append(
                hub.tool.aws.comment_utils.already_exists_comment(
                    resource_type="aws.guardduty.organization_configuration",
                    name=resource_id,
                )
            )
            return result
    else:
        result["result"] = False
        result["comment"] = response["comment"]
        return result


async def get(hub, ctx, resource_id: str) -> Dict:
    """Returns information about the account selected as the delegated administrator for GuardDuty.

    Args:
        resource_id(str):
            AWS Detector ID to identify the resource.

    Returns:
        Dict[str, Any]:
            Returns organization Configuration in updated format

    Examples:
        Calling from the CLI:

        .. code-block:: bash

            $ idem exec aws.guardduty.organization_configuration.get resource_id="detector_id"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.guardduty.organization_configuration.get
                - kwargs:
                    resource_id: "detector_id"
    """
    result = dict(comment=[], ret=None, result=True)
    organization_configuration = (
        await hub.exec.boto3.client.guardduty.describe_organization_configuration(
            ctx, DetectorId=resource_id
        )
    )
    if not organization_configuration["result"]:
        if "NoSuchEntity" in str(organization_configuration["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.guardduty.organization_configuration",
                    name=resource_id,
                )
            )
            result["comment"] += list(organization_configuration["comment"])
            return result
        result["result"] = False
        result["comment"] += list(organization_configuration["comment"])
        return result

    if not (organization_configuration["ret"]):
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.guardduty.organization_configuration",
                organization_configuration=organization_configuration,
                name=resource_id,
            )
        )
        return result

    result[
        "ret"
    ] = hub.tool.aws.guardduty.conversion_utils.convert_raw_organization_configuration_to_present(
        organization_configuration=organization_configuration,
        idem_resource_name=resource_id,
    )
    return result
