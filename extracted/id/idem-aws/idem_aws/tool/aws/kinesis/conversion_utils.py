from collections import OrderedDict
from typing import Any
from typing import Dict


def convert_raw_stream_to_present(
    hub,
    raw_resource: Dict[str, Any],
    idem_resource_name: str = None,
    tags: Dict[str, str] = None,
) -> Dict[str, Any]:
    """
    Util function to convert raw resource state from AWS Kinesis Stream to present input format.

    Args:
        raw_resource(Dict[str, Any]):
            The AWS response from 'Kinesis DescribeStreamSummary' to convert.
        idem_resource_name(str, Optional): An Idem name of the resource.
        tags(Dict[str, str], Optional): The AWS Kinesis Stream tags.

    Returns:
        Dict[str, Any]
    """

    resource_parameters = OrderedDict(
        {
            "OpenShardCount": "shard_count",
            "RetentionPeriodHours": "retention_period_hours",
            "EncryptionType": "encryption_type",
            "KeyId": "key_id",
            "StreamARN": "stream_arn",
        }
    )
    resource_translated = {
        "name": idem_resource_name,
        "resource_id": idem_resource_name,
    }
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    if (
        raw_resource.get("EnhancedMonitoring")
        and len(raw_resource["EnhancedMonitoring"])
        and len(raw_resource["EnhancedMonitoring"][0].get("ShardLevelMetrics")) > 0
    ):
        resource_translated.update(
            {
                "shard_level_metrics": (
                    (raw_resource.get("EnhancedMonitoring")[0]).get("ShardLevelMetrics")
                ).copy()
            }
        )
    if raw_resource.get("StreamModeDetails"):
        resource_translated.update(
            {"stream_mode_details": (raw_resource.get("StreamModeDetails")).copy()}
        )
    if tags:
        resource_translated["tags"] = tags.copy()
    return resource_translated
