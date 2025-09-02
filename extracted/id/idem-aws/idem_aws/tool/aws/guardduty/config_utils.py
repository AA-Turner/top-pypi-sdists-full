from typing import Any
from typing import Dict


async def is_organization_configuration_updated(
    hub, before: Dict[str, Any], auto_enable: False | True, data_sources: Dict = None
):
    if auto_enable != before.get("auto_enable"):
        return True
    if data_sources:
        if data_sources.get("S3Logs").get("AutoEnable") != before.get(
            "data_sources"
        ).get("S3Logs").get("AutoEnable"):
            return True
        if data_sources.get("Kubernetes").get("AuditLogs").get(
            "AutoEnable"
        ) != before.get("data_sources").get("Kubernetes").get("AuditLogs").get(
            "AutoEnable"
        ):
            return True
        if data_sources.get("MalwareProtection").get("ScanEc2InstanceWithFindings").get(
            "EbsVolumes"
        ).get("AutoEnable") != before.get("data_sources").get("MalwareProtection").get(
            "ScanEc2InstanceWithFindings"
        ).get(
            "EbsVolumes"
        ).get(
            "AutoEnable"
        ):
            return True

    return False
