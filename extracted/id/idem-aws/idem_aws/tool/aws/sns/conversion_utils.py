"""Util functions for converting raw attributes to present form and vice versa."""
from collections import OrderedDict
from typing import Any
from typing import Dict


def convert_raw_subscription_to_present(
    hub, raw_resource: Dict[str, Any], idem_resource_name: str = None
) -> Dict[str, Any]:
    """Util functions to convert raw resource state to present input format for SNS topic_subscription."""
    raw_attributes = raw_resource.get("Attributes")
    resource_id = raw_attributes.get("SubscriptionArn")
    resource_parameters = OrderedDict(
        {
            "TopicArn": "topic_arn",
            "Protocol": "protocol",
            "Endpoint": "endpoint",
        }
    )
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource.get("Attributes"):
            resource_translated[parameter_present] = raw_resource.get("Attributes").get(
                parameter_raw
            )

    attribute_params = [
        "DeliveryPolicy",
        "FilterPolicy",
        "RawMessageDelivery",
        "RedrivePolicy",
    ]

    attributes = {}
    for param in attribute_params:
        value = raw_attributes.get(param, None)
        if value:
            attributes[param] = hub.tool.aws.state_comparison_utils.standardise_json(
                value
            )
    resource_translated["attributes"] = attributes

    return resource_translated


def convert_raw_topic_to_present(
    hub,
    raw_resource: Dict[str, Any],
    raw_resource_tags: Dict[str, Any],
    idem_resource_name: str = None,
) -> Dict[str, Any]:
    """Util functions to convert raw resource state to present input format for SNS topic."""
    raw_attributes = raw_resource.get("Attributes")
    resource_id = raw_attributes.get("TopicArn")
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    attribute_params = [
        "DeliveryPolicy",
        "DisplayName",
        "FifoTopic",
        "Policy",
        "KmsMasterKeyId",
        "ContentBasedDeduplication",
    ]

    attributes = {}
    for param in attribute_params:
        if raw_attributes.get(param):
            attributes[param] = raw_attributes.get(param)
    resource_translated["attributes"] = attributes

    if raw_resource_tags.get("ret") and raw_resource_tags.get("ret").get("Tags"):
        resource_translated["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            raw_resource_tags.get("ret").get("Tags")
        )

    return resource_translated


def convert_raw_topic_policy_to_present(
    hub, raw_resource: Dict[str, Any], idem_resource_name: str = None
) -> Dict[str, Any]:
    """Util functions to convert raw resource state to present input format for SNS topic_policy."""
    raw_attributes = raw_resource["ret"].get("Attributes")
    resource_id = raw_attributes.get("TopicArn") + "-policy"
    resource_translated = {
        "name": idem_resource_name,
        "resource_id": resource_id,
        "topic_arn": raw_attributes.get("TopicArn"),
        "policy": hub.tool.aws.state_comparison_utils.standardise_json(
            raw_attributes.get("Policy")
        ),
    }

    return resource_translated
