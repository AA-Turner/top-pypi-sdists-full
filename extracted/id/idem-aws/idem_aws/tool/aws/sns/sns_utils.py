"""Util functions for SNS topic policy."""
import copy
import json
from typing import Any
from typing import Dict
from typing import List

from dict_tools import differ


def get_default_topic_policy(hub, topic_arn: str) -> str:
    """Topic policy initialized with default attribute values.

    Args:
        topic_arn(str): AWS ARN of the SNS topic

    Returns:
        Dict(str, Any)
    """
    default_policy = {
        "Version": "2008-10-17",
        "Id": "__default_policy_ID",
        "Statement": [
            {
                "Sid": "__default_statement_ID",
                "Effect": "Allow",
                "Principal": {"AWS": "*"},
                "Action": [
                    "SNS:GetTopicAttributes",
                    "SNS:SetTopicAttributes",
                    "SNS:AddPermission",
                    "SNS:RemovePermission",
                    "SNS:DeleteTopic",
                    "SNS:Subscribe",
                    "SNS:ListSubscriptionsByTopic",
                    "SNS:Publish",
                ],
                "Resource": "topic_arn",
                "Condition": {"StringEquals": {"AWS:SourceOwner": "acct_id"}},
            }
        ],
    }
    default_policy["Statement"][0]["Resource"] = topic_arn
    acct_id = topic_arn.split(":")[4]
    default_policy["Statement"][0]["Condition"]["StringEquals"][
        "AWS:SourceOwner"
    ] = acct_id
    policy = json.dumps(default_policy, separators=(", ", ": "))
    return policy


async def update_topic_attributes(
    hub,
    ctx,
    resource_arn: str,
    old_attributes: Dict[str, str],
    new_attributes: Dict[str, str],
):
    """Given old and new attributes of SNS topic the function updates the attributes.

    Args:
        resource_arn(str):
            AWS resource_arn of SNS topic

        old_attributes(Dict):
            old attribute of SNS topic

        new_attributes(Dict):
            new attribute of SNS topic

    Returns:
        .. code-block:: json

            {"result": True|False, "comment": A message Tuple, "ret": Dict}
    """
    result = dict(comment=[], result=True, ret=None)
    attributes_diff = differ.deep_diff(old_attributes, new_attributes)
    attributes_to_update = attributes_diff.get("new")

    if attributes_to_update:
        if ctx.get("test", False):
            result["ret"] = {"updated_attributes": attributes_to_update}
            result["comment"] += [
                f"Would Update attributes {attributes_to_update.keys()}"
            ]
            return result

        else:
            for key, value in attributes_to_update.items():
                ret = await hub.exec.boto3.client.sns.set_topic_attributes(
                    ctx, TopicArn=resource_arn, AttributeName=key, AttributeValue=value
                )
                if not ret["result"]:
                    result["comment"] = ret["comment"]
                    result["result"] = False
                    return result

            result["ret"] = {"updated_attributes": attributes_to_update}
            result["comment"] += [f"Updated attributes {attributes_to_update.keys()}"]
    return result


async def update_subscription_attributes(
    hub,
    ctx,
    resource_arn: str,
    old_attributes: Dict[str, str],
    new_attributes: Dict[str, str],
):
    """Given old and new attributes of SNS topic_subscription the function updates the attributes.

    Args:
        resource_arn(str):
            AWS resource_arn of SNS topic_subscription

        old_attributes(Dict):
            old attribute of SNS topic_subscription

        new_attributes(Dict):
            new attribute of SNS topic_subscription

    Returns:
        .. code-block:: json

            {"result": True|False, "comment": A message Tuple, "ret": Dict}
    """
    result = dict(comment=[], result=True, ret=None)
    attributes_diff = differ.deep_diff(old_attributes, new_attributes)
    attributes_to_update = attributes_diff.get("new")

    if attributes_to_update:
        if ctx.get("test", False):
            result["ret"] = {"updated_attributes": attributes_to_update}
            result["comment"] += [
                f"Would Update attributes {attributes_to_update.keys()}"
            ]
            return result

        else:
            for key, value in attributes_to_update.items():
                ret = await hub.exec.boto3.client.sns.set_subscription_attributes(
                    ctx,
                    SubscriptionArn=resource_arn,
                    AttributeName=key,
                    AttributeValue=value,
                )
                if not ret["result"]:
                    result["comment"] = ret["comment"]
                    result["result"] = False
                    return result

            result["ret"] = {"updated_attributes": attributes_to_update}
            result["comment"] += [f"Updated attributes {attributes_to_update.keys()}"]
    return result


async def update_tags(
    hub,
    ctx,
    resource_arn,
    old_tags: List[Dict[str, Any]] or Dict[str, Any] = None,
    new_tags: List[Dict[str, Any]] or Dict[str, Any] = None,
):
    """Update tags of AWS SNS resources.

    Args:
        resource_arn(str):
            aws resource arn

        old_tags(List, Optional):
            list of old tags in the format of [{"Key": tag-key, "Value": tag-value}] or dict in the format of
            {tag-key: tag-value}

        new_tags(List, Optional):
            list of new tags in the format of [{"Key": tag-key, "Value": tag-value}] or dict in the format of
            {tag-key: tag-value}

    Returns:
        .. code-block:: json

            {"result": True|False, "comment": A message Tuple, "ret": Dict}
    """
    tags_to_add = {}
    tags_to_remove = {}
    if isinstance(old_tags, List):
        old_tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(old_tags)
    if isinstance(new_tags, List):
        new_tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(new_tags)
    if new_tags is not None:
        tags_to_remove, tags_to_add = hub.tool.aws.tag_utils.diff_tags_dict(
            old_tags=old_tags, new_tags=new_tags
        )
    result = dict(comment=[], result=True, ret={})
    if (not tags_to_remove) and (not tags_to_add):
        result["ret"] = copy.deepcopy(old_tags if old_tags else {})
        return result
    if tags_to_remove:
        if not ctx.get("test", False):
            delete_ret = await hub.exec.boto3.client.sns.untag_resource(
                ctx, ResourceArn=resource_arn, TagKeys=list(tags_to_remove)
            )
            if not delete_ret["result"]:
                result["comment"] = delete_ret["comment"]
                result["result"] = False
                return result
    if tags_to_add:
        if not ctx.get("test", False):
            add_ret = await hub.exec.boto3.client.sns.tag_resource(
                ctx,
                ResourceArn=resource_arn,
                Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags_to_add),
            )
            if not add_ret["result"]:
                result["comment"] = add_ret["comment"]
                result["result"] = False
                return result
    result["ret"] = new_tags
    if ctx.get("test", False):
        result["comment"] = hub.tool.aws.comment_utils.would_update_tags_comment(
            tags_to_remove=tags_to_remove, tags_to_add=tags_to_add
        )
    else:
        result["comment"] = hub.tool.aws.comment_utils.update_tags_comment(
            tags_to_remove=tags_to_remove, tags_to_add=tags_to_add
        )
    return result
