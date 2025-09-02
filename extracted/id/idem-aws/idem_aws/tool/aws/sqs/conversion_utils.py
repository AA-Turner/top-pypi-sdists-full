"""Util functions for converting raw attributes to present form and vice versa."""
import json
from typing import Any
from typing import Dict


ATTRIBUTES_NAMES_RAW_TO_PRESENT = {
    "DelaySeconds": "delay_seconds",
    "MaximumMessageSize": "maximum_message_size",
    "MessageRetentionPeriod": "message_retention_period",
    "Policy": "policy",
    "ReceiveMessageWaitTimeSeconds": "receive_message_wait_time_seconds",
    "RedrivePolicy": "redrive_policy",
    "VisibilityTimeout": "visibility_timeout",
    "KmsMasterKeyId": "kms_master_key_id",
    "KmsDataKeyReusePeriodSeconds": "kms_data_key_reuse_period_seconds",
    "SqsManagedSseEnabled": "sqs_managed_sse_enabled",
    "FifoQueue": "fifo_queue",
    "ContentBasedDeduplication": "content_based_deduplication",
    "DeduplicationScope": "deduplication_scope",
    "FifoThroughputLimit": "fifo_throughput_limit",
    "QueueArn": "arn",
}

PRESENT_ATTRIBUTES_TYPES = {
    "delay_seconds": int,
    "maximum_message_size": int,
    "message_retention_period": int,
    "policy": Dict,
    "receive_message_wait_time_seconds": int,
    "redrive_policy": Dict,
    "visibility_timeout": int,
    "kms_master_key_id": str,
    "kms_data_key_reuse_period_seconds": int,
    "sqs_managed_sse_enabled": bool,
    "fifo_queue": bool,
    "content_based_deduplication": bool,
    "deduplication_scope": str,
    "fifo_throughput_limit": str,
    "arn": str,
}


def convert_raw_attributes_to_present(
    hub, raw_attributes: Dict[str, str]
) -> Dict[str, Any]:
    """Converts raw attributes to a dict of present values.

    The types of the values are also changed from string to whatever the type of the attribute should be in the present
    SLS form.

    Args:
        raw_attributes(Dict):
            The attributes as directly returned by the boto3 API

    Returns:
        a dict of the attributes converted to present form
    """
    present_attributes = {}

    for (
        raw_attribute_name,
        present_attribute_name,
    ) in ATTRIBUTES_NAMES_RAW_TO_PRESENT.items():
        value = raw_attributes.get(raw_attribute_name)

        if value:
            # Convert string values to their correct present value types
            attribute_value_type = PRESENT_ATTRIBUTES_TYPES.get(present_attribute_name)
            if not isinstance(value, attribute_value_type):
                if attribute_value_type == bool:
                    value = value.lower() == "true"
                elif attribute_value_type == int:
                    value = int(value)
                elif attribute_value_type == Dict and value != "":
                    value = json.loads(value)
            present_attributes[present_attribute_name] = value

    return present_attributes


def convert_present_attributes_to_raw(
    hub,
    delay_seconds: int,
    maximum_message_size: int,
    message_retention_period: int,
    policy: Dict,
    receive_message_wait_time_seconds: int,
    redrive_policy: Dict,
    visibility_timeout: int,
    kms_master_key_id: str,
    kms_data_key_reuse_period_seconds: int,
    sqs_managed_sse_enabled: bool,
    fifo_queue: bool,
    content_based_deduplication: bool,
    deduplication_scope: str,
    fifo_throughput_limit: str,
) -> Dict[str, str]:
    """Converts present attributes to a dict of raw string values.

    Args:
        delay_seconds(int):
            The length of time, in seconds, for which the delivery of all messages in the queue is delayed

        maximum_message_size(int):
            The limit of how many bytes a message can contain before Amazon SQS rejects it

        message_retention_period(int):
            The length of time, in seconds, for which Amazon SQS retains a message

        policy(Dict):
            The queue's policy

        receive_message_wait_time_seconds(int):
            The length of time, in seconds, for which a ReceiveMessage action waits for a message to arrive

        redrive_policy(Dict):
            The dict that includes the parameters for the dead-letter queue functionality of the source queue

        visibility_timeout(int):
            The visibility timeout for the queue, in seconds

        kms_master_key_id(str):
            The ID of an Amazon Web Services managed customer master key (CMK) for Amazon SQS or a custom CMK

        kms_data_key_reuse_period_seconds(int):
            The length of time, in seconds, for which Amazon SQS can reuse a data key to encrypt or decrypt messages
            before calling KMS again

        sqs_managed_sse_enabled(bool, Optional):
            enables server-side queue encryption using SQS owned encryption keys. Only one server-side encryption option
            is supported per queue.

        fifo_queue(bool):
            Designates a queue as FIFO

        content_based_deduplication(bool):
            Enables content-based deduplication

        deduplication_scope(str):
            Specifies whether message deduplication occurs at the message group or queue level

        fifo_throughput_limit(str):
            Specifies whether the FIFO queue throughput quota applies to the entire

    Returns:
        a dict of the attributes converted to raw form
    """
    all_attributes = {
        "DelaySeconds": delay_seconds,
        "MaximumMessageSize": maximum_message_size,
        "MessageRetentionPeriod": message_retention_period,
        "Policy": policy,
        "ReceiveMessageWaitTimeSeconds": receive_message_wait_time_seconds,
        "RedrivePolicy": redrive_policy,
        "VisibilityTimeout": visibility_timeout,
        "KmsMasterKeyId": kms_master_key_id,
        "KmsDataKeyReusePeriodSeconds": kms_data_key_reuse_period_seconds,
        "SqsManagedSseEnabled": sqs_managed_sse_enabled,
        "FifoQueue": fifo_queue,
        "ContentBasedDeduplication": content_based_deduplication,
        "DeduplicationScope": deduplication_scope,
        "FifoThroughputLimit": fifo_throughput_limit,
    }

    raw_attributes = {}

    # Remove the None attributes and convert all values to string
    for key, value in all_attributes.items():
        if value is not None:
            # Policy and RedrivePolicy are dict so use json library to convert them to string
            if (key == "Policy" or key == "RedrivePolicy") and not isinstance(
                value, str
            ):
                raw_attributes[key] = json.dumps(value)
            else:
                raw_attributes[key] = str(value)

    return raw_attributes
