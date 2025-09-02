"""State module for managing SNS Topics."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    attributes: Dict[str, str] = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass("Tag", [("Key", str), ("Value", str, field(default=None))])
    ] = None,
) -> Dict[str, Any]:
    """Creates a topic to which notifications can be published.

    Users can create at most 100,000 standard topics (at most 1,000 FIFO topics). For more information, see Creating an
    Amazon SNS topic in the Amazon SNS Developer Guide. This action is idempotent, so if the requester already owns a
    topic with the specified name, that topic's ARN is returned without creating a new topic.

    Args:
        name(str):
            The idem name for the resource

        resource_id(str, Optional):
            The AWS resource identifier, here it is resource arn

        attributes(dict, Optional):
            Attributes of topic

        tags(dict or list, Optional):
            Dict in the format of ``{tag-key: tag-value}`` or list of tags in the format of
            ``[{"Key": tag-key, "Value": tag-value}]`` to associate with the topic. Each tag consists of a key name and
            an associated value. Defaults to None.

            * Key (str):
                The key of the tag. Constraints: Tag keys are case-sensitive and accept a maximum of 127 Unicode
                characters. May not begin with aws:.

            * Value(str, Optional):
                The value of the tag. Constraints: Tag values are case-sensitive and accept a maximum of 256
                Unicode characters.

    Request Syntax:
        .. code-block:: yaml

            [topic-name]:
              aws.sns.topic.present:
                - resource_id: 'string'
                - attributes: 'Dict'
                - tags:
                  - Key: 'string'
                    Value: 'string'

    Returns:
        dict[str, Any]

    Examples:
        .. code-block:: yaml

            new-topic:
              aws.sns.topic.present:
                - attributes:
                    DeliveryPolicy: '{"http":{"defaultHealthyRetryPolicy":{"minDelayTarget":10,"maxDelayTarget":30,"numRetries":10,"numMaxDelayRetries":7,"numNoDelayRetries":0,"numMinDelayRetries":3,"backoffFunction":"linear"}}}'
                - tags:
                   - Key: Name
                     Value: new-topic
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False
    plan_state = None

    if resource_id:
        resource = await hub.tool.boto3.resource.create(
            ctx, "sns", "Topic", arn=resource_id
        )
        before = await hub.tool.boto3.resource.describe(resource)

    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)

    if before:
        try:
            ret_tags = await hub.exec.boto3.client.sns.list_tags_for_resource(
                ctx, ResourceArn=resource_id
            )
            if not ret_tags["result"]:
                result["comment"] = ret_tags["comment"]
                result["result"] = False
                return result

            result[
                "old_state"
            ] = hub.tool.aws.sns.conversion_utils.convert_raw_topic_to_present(
                raw_resource=before, raw_resource_tags=ret_tags, idem_resource_name=name
            )
            plan_state = copy.deepcopy(result["old_state"])
            old_attributes = plan_state.get("attributes")
            old_tags = plan_state.get("tags")
            if tags is not None and old_tags != tags:
                # Check and update tags
                update_tags_ret = await hub.tool.aws.sns.sns_utils.update_tags(
                    ctx=ctx,
                    resource_arn=resource_id,
                    old_tags=old_tags,
                    new_tags=tags,
                )
                if not update_tags_ret["result"]:
                    result["comment"] = update_tags_ret["comment"]
                    result["result"] = False
                    return result
                resource_updated = bool(update_tags_ret["ret"])
                result["comment"] = update_tags_ret["comment"]
                if ctx.get("test", False) and update_tags_ret["ret"]:
                    plan_state["tags"] = update_tags_ret["ret"]

            if attributes is not None:
                # Check and update Attributes
                update_attributes_ret = (
                    await hub.tool.aws.sns.sns_utils.update_topic_attributes(
                        ctx=ctx,
                        resource_arn=resource_id,
                        old_attributes=old_attributes,
                        new_attributes=attributes,
                    )
                )
                if not update_attributes_ret["result"]:
                    result["comment"] = update_attributes_ret["comment"]
                    result["result"] = False
                    return result
                resource_updated = resource_updated or bool(
                    update_attributes_ret["ret"]
                )
                result["comment"] += update_attributes_ret["comment"]
                if ctx.get("test", False) and update_attributes_ret["ret"]:
                    plan_state["attributes"] = update_attributes_ret["ret"].get(
                        "updated_attributes"
                    )

            if not resource_updated:
                result["comment"] += [f"aws.sns.topic '{name}' already exists"]

        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False

    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "attributes": attributes,
                    "tags": tags,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.sns.topic", name=name
            )
            return result
        try:
            ret = await hub.exec.boto3.client.sns.create_topic(
                ctx,
                Name=name,
                Attributes=attributes,
                Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
                if tags
                else None,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result
            resource_id = ret["ret"].get("TopicArn")
            result["comment"] = hub.tool.aws.comment_utils.create_comment(
                "aws.sns.topic", name
            )
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False

    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif (not before) or resource_updated:
            resource = await hub.tool.boto3.resource.create(
                ctx, "sns", "Topic", arn=resource_id
            )
            after = await hub.tool.boto3.resource.describe(resource)
            ret_tags = await hub.exec.boto3.client.sns.list_tags_for_resource(
                ctx, ResourceArn=resource_id
            )
            if not ret_tags["result"]:
                result["comment"] = ret_tags["comment"]
                result["result"] = False
                return result
            result[
                "new_state"
            ] = hub.tool.aws.sns.conversion_utils.convert_raw_topic_to_present(
                raw_resource=after, raw_resource_tags=ret_tags, idem_resource_name=name
            )
        else:
            result["new_state"] = copy.deepcopy(result["old_state"])
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False
    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deletes a topic and all its subscriptions.

    Deleting a topic might prevent some messages previously sent to the topic from being delivered to subscribers. This
    action is idempotent, so deleting a topic that does not exist does not result in an error.

    Args:
        name(str):
            The name of the state.

        resource_id(str, Optional):
            The AWS resource identifier, here it is resource arn

    Request Syntax:
        .. code-block:: yaml

            [topic-name]:
              aws.sns.topic.absent:
                - resource_id: 'string'

    Returns:
        dict[str, Any]

    Examples:
        .. code-block:: yaml

            test-topic:
              aws.sns.topic.absent:
                - resource_id: arn:aws:sns:eu-west-3:537227425989:test-topic
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.sns.topic", name=name
        )
        return result
    resource = await hub.tool.boto3.resource.create(ctx, "sns", "Topic", resource_id)
    before = await hub.tool.boto3.resource.describe(resource)

    if not before:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            "aws.sns.topic", name
        )

    else:
        ret_tags = await hub.exec.boto3.client.sns.list_tags_for_resource(
            ctx, ResourceArn=resource_id
        )
        if not ret_tags["result"]:
            result["comment"] = ret_tags["comment"]
            result["result"] = False
            return result
        result[
            "old_state"
        ] = hub.tool.aws.sns.conversion_utils.convert_raw_topic_to_present(
            raw_resource=before, raw_resource_tags=ret_tags, idem_resource_name=name
        )
        if ctx.get("test", False):
            result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
                "aws.sns.topic", name
            )
            return result
        try:
            ret = await hub.exec.boto3.client.sns.delete_topic(
                ctx, TopicArn=resource_id
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                result["result"] = False
                return result
            result["comment"] = hub.tool.aws.comment_utils.delete_comment(
                "aws.sns.topic", name
            )
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Returns a list of the requester's topics. Each call returns a limited list of topics, up to 100. If there are
    more topics, a NextToken is also returned. Use the NextToken parameter in a new ListTopics call to get further
    results. This action is throttled at 30 transactions per second (TPS).


    Returns:
        dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.sns.topic
    """
    result = {}
    ret = await hub.exec.boto3.client.sns.list_topics(ctx)

    if not ret["result"]:
        hub.log.warning(f"Could not describe topic {ret['comment']}")
        return {}

    for topic in ret["ret"]["Topics"]:
        # Including fields to match the 'present' function parameters
        resource_id = topic["TopicArn"]
        idem_resource_name = resource_id.split(":")[-1]

        resource = await hub.tool.boto3.resource.create(
            ctx, "sns", "Topic", arn=resource_id
        )
        raw_resource = await hub.tool.boto3.resource.describe(resource)
        ret_tags = await hub.exec.boto3.client.sns.list_tags_for_resource(
            ctx, ResourceArn=resource_id
        )
        if not ret_tags["result"]:
            hub.log.warning(f"Could not describe topic tag {ret_tags['comment']}")
            return {}

        resource_translated = (
            hub.tool.aws.sns.conversion_utils.convert_raw_topic_to_present(
                raw_resource=raw_resource,
                raw_resource_tags=ret_tags,
                idem_resource_name=idem_resource_name,
            )
        )
        result[idem_resource_name] = {
            "aws.sns.topic.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }

    return result
