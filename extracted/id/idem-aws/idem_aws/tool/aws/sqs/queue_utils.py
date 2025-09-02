"""Util functions for SQS Queue."""
from typing import Any
from typing import Dict


DEFAULT_ATTRIBUTES_VALUES = {
    "delay_seconds": 0,
    "maximum_message_size": 262144,
    "message_retention_period": 345600,
    "policy": None,
    "receive_message_wait_time_seconds": 0,
    "redrive_policy": None,
    "visibility_timeout": 30,
    "kms_master_key_id": None,
    "kms_data_key_reuse_period_seconds": 300,
    "sqs_managed_sse_enabled": False,
    "fifo_queue": False,
    "content_based_deduplication": False,
    "deduplication_scope": "queue",
    "fifo_throughput_limit": "perQueue",
}


def compare_present_queue_attributes(
    hub, expected_attributes: Dict[str, Any], actual_attributes: Dict[str, Any]
) -> bool:
    """Checks if the expected_attributes are contained withing actual_attributes.

    A None value in expected_attributes and a default value in actual_attributes are considered equal.

    Args:
        expected_attributes(Dict):
            The expected attributes

        actual_attributes(Dict):
            The actual attributes

    Returns:
        True if expected_attributes is contained within actual_attributes, False otherwise
    """
    for (
        expected_attribute_name,
        expected_attribute_value,
    ) in expected_attributes.items():
        actual_attribute_value = actual_attributes.get(expected_attribute_name)

        if actual_attribute_value is None:
            return actual_attribute_value == expected_attribute_value

        if expected_attribute_name == "policy":
            if not hub.tool.aws.state_comparison_utils.are_policies_equal(
                expected_attribute_value, actual_attribute_value
            ):
                return False
            continue

        if expected_attribute_value != actual_attribute_value:
            if (
                expected_attribute_value is None
                and actual_attributes.get(expected_attribute_name)
                == DEFAULT_ATTRIBUTES_VALUES[expected_attribute_name]
            ):
                continue

            return False

    return True
