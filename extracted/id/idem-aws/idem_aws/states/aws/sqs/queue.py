"""State module for managing AWS SQS queue."""
import copy
from dataclasses import make_dataclass
from typing import Any
from typing import Dict

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    delay_seconds: int = None,
    maximum_message_size: int = None,
    message_retention_period: int = None,
    policy: str or Dict = None,
    receive_message_wait_time_seconds: int = None,
    redrive_policy: make_dataclass(
        "RedrivePolicy", [("deadLetterTargetArn", str), ("maxReceiveCount", int)]
    ) = None,
    visibility_timeout: int = None,
    kms_master_key_id: str = None,
    kms_data_key_reuse_period_seconds: int = None,
    sqs_managed_sse_enabled: bool = None,
    fifo_queue: bool = None,
    content_based_deduplication: bool = None,
    deduplication_scope: str = None,
    fifo_throughput_limit: str = None,
    tags: Dict[str, str] = None,
) -> Dict[str, Any]:
    """Creates a new standard or FIFO queue.

    You can pass one or more attributes in the request. Keep the following in mind - if you don't specify the
    fifo_queue attribute, Amazon SQS creates a standard queue. You can't change the queue type after you create it, and
    you can't convert an existing standard queue into a FIFO queue. You must either create a new FIFO queue for your
    application or delete your existing standard queue and recreate it as a FIFO queue. For more information, see Moving
    From a Standard Queue to a FIFO Queue in the Amazon SQS Developer Guide. If you don't provide a value for an
    attribute, the queue is created with the default value for the attribute. If you delete a queue, you must wait at
    least 60 seconds before creating a queue with the same name. To successfully create a new queue, you must provide a
    queue name that adheres to the limits related to queues and is unique within the scope of your queues. After you
    create a queue, you must wait at least one second after the queue is created to be able to use the queue.
    Cross-account permissions don't apply to this action. For more information, see Grant cross-account permissions to a
    role and a user name in the Amazon SQS Developer Guide.

    Args:
        name(str):
            The name of the new queue. A queue name can have up to 80 characters. Valid values: alphanumeric characters,
            hyphens (-), and underscores (_). A FIFO queue name must end with the .fifo suffix. Case-sensitive.

        resource_id(str, Optional):
            The URL of the Amazon SQS queue. Case-sensitive. Defaults to None.

        delay_seconds(int, Optional):
            The length of time, in seconds, for which the delivery of all messages in the
            queue is delayed. Valid values: An integer from 0 to 900 seconds (15 minutes). Default: 0.

        maximum_message_size(int, Optional):
            The limit of how many bytes a message can contain before Amazon SQS rejects it. Valid values: An integer
            from 1,024 bytes (1 KiB) to 262,144 bytes (256 KiB). Default: 262,144 (256 KiB).

        message_retention_period(int, Optional):
            The length of time, in seconds, for which Amazon SQS retains a message. Valid values: An integer from 60
            seconds (1 minute) to 1,209,600 seconds (14 days). Default: 345,600 (4 days).

        policy(dict or str, Optional):
            The queue's policy. A valid Amazon Web Services policy. For more information about policy structure, see
            Overview of Amazon Web Services IAM Policies in the Amazon IAM User Guide.

        receive_message_wait_time_seconds(int, Optional):
            The length of time, in seconds, for which a ReceiveMessage action waits for a message to arrive. Valid
            values: An integer from 0 to 20 (seconds). Default: 0.

        redrive_policy(dict, Optional):
            The dictionary that includes the parameters for the dead-letter queue functionality of the source queue. For
            more information about the redrive policy and dead-letter queues, see Using Amazon SQS Dead-Letter Queues in
            the Amazon SQS Developer Guide.

            * deadLetterTargetArn (str):
                The Amazon Resource Name (ARN) of the dead-letter queue to which Amazon SQS moves messages after the
                value of maxReceiveCount is exceeded.

            * maxReceiveCount (int):
                The number of times a message is delivered to the source queue before being moved to the dead-letter
                queue. When the ReceiveCount for a message exceeds the maxReceiveCount for a queue, Amazon SQS moves
                the message to the dead-letter-queue. The dead-letter queue of a FIFO queue must also be a FIFO queue.
                Similarly, the dead-letter queue of a standard queue must also be a standard queue.

        visibility_timeout(int, Optional):
            The visibility timeout for the queue, in seconds. Valid values: An integer from 0 to 43,200 (12 hours).
            Default: 30. For more information about the visibility timeout, see Visibility Timeout in the Amazon SQS
            Developer Guide.

    The following attributes apply only to server-side-encryption:

    Args:
        kms_master_key_id(str, Optional):
            The ID of an Amazon Web Services managed customer master key (CMK) for Amazon SQS or a custom CMK. For more
            information, see Key Terms. While the alias of the Amazon Web Services managed CMK for Amazon SQS is always
            alias/aws/sqs, the alias of a custom CMK can, for example, be alias/MyAlias . For more examples, see KeyId
            in the Key Management Service API Reference.

        kms_data_key_reuse_period_seconds(int, Optional):
            The length of time, in seconds, for which Amazon SQS can reuse a data key to encrypt or decrypt messages
            before calling KMS again. An integer representing seconds, between 60 seconds (1 minute) and 86,400 seconds
            (24 hours). Default: 300 (5 minutes). A shorter time period provides better security but results in more
            calls to KMS which might incur charges after Free Tier. For more information, see How Does the Data Key
            Reuse Period Work?

        sqs_managed_sse_enabled(bool, Optional):
            enables server-side queue encryption using SQS owned encryption keys. Only one server-side encryption option
            is supported per queue.

    The following attributes apply only to FIFO (first-in-first-out) queues:

    Args:
        fifo_queue(bool, Optional):
            Designates a queue as FIFO. Valid values are true and false. If you don't specify the FifoQueue attribute,
            Amazon SQS creates a standard queue. You can provide this attribute only during queue creation. You can't
            change it for an existing queue. When you set this attribute, you must also provide the MessageGroupId for
            your messages explicitly. For more information, see FIFO queue logic in the Amazon SQS Developer Guide.

        content_based_deduplication(bool, Optional):
            Enables content-based deduplication. Valid values are true and false. For more information, see Exactly-once
            processing in the Amazon SQS Developer Guide. Note the following:

            Every message must have a unique MessageDeduplicationId. You may provide a MessageDeduplicationId explicitly.

            If you aren't able to provide a MessageDeduplicationId and you enable ContentBasedDeduplication for your
            queue, Amazon SQS uses a SHA-256 hash to generate the MessageDeduplicationId using the body of the
            message (but not the attributes of themessage).

            If you don't provide a MessageDeduplicationId and the queue doesn't have ContentBasedDeduplication set,
            the action fails with an error.

            If the queue has ContentBasedDeduplication set, your MessageDeduplicationId overrides the generated one.

            When ContentBasedDeduplication is in effect, messages with identical content sent within the deduplication
            interval are treated as duplicates and only one copy of the message is delivered.

            If you send one message with ContentBasedDeduplication enabled and then another message with a
            MessageDeduplicationId that is the same as the one generated for the first MessageDeduplicationId, the two
            messages are treated as duplicates and only one copy of the message is delivered.

    The following attributes apply only to high throughput for FIFO queues:

    Args:
        deduplication_scope(str, Optional):
            Specifies whether message deduplication occurs at the message group or queue level. Valid values are
            messageGroup and queue.

        fifo_throughput_limit(str, Optional):
            Specifies whether the FIFO queue throughput quota applies to the entire queue or per message group. Valid
            values are perQueue and perMessageGroupId. The perMessageGroupId value is allowed only when the value for
            DeduplicationScope is messageGroup.
            To enable high throughput for FIFO queues, do the following:

            - Set DeduplicationScope to messageGroup.
            - Set FifoThroughputLimit to perMessageGroupId.

            If you set these attributes to anything other than the values shown for enabling high throughput, normal
            throughput is in effect and deduplication occurs as specified.

            For information on throughput quotas, see Quotas related to messages in the Amazon SQS Developer Guide.
            Defaults to None.

        tags(dict, Optional):
            Add cost allocation tags to the specified Amazon SQS queue. For an overview, see Tagging Your Amazon SQS
            Queues in the Amazon SQS Developer Guide. When you use queue tags, keep the following guidelines in mind:

            - Adding more than 50 tags to a queue isn't recommended.
            - Tags don't have any semantic meaning. Amazon SQS interprets tags as character strings.
            - Tags are case-sensitive.
            - A new tag with a key identical to that of an existing tag overwrites the existing tag.

            For a full list of tag restrictions, see Quotas related to queues in the Amazon SQS Developer Guide.
            To be able to tag a queue on creation, you must have the sqs:CreateQueue and sqs:TagQueue permissions.
            Cross-account permissions don't apply to this action. For more information, see Grant cross-account
            permissions to a role and a user name in the Amazon SQS Developer Guide. Defaults to None.

    Returns:
        dict[str, Any]

    Examples:
        .. code-block:: yaml

            example_fifo_queue.fifo:
              aws.sqs.queue.present:
                - delay_seconds: 35
                - maximum_message_size: 12345
                - message_retention_period: 1759
                - policy:
                    Version: 2022-03-30
                    Id: Example_Queue_Policy
                    Statement:
                      Effect: Deny
                      Principal:
                        AWS:
                         - "000000000000"
                      Action: sqs:SendMessage
                      Resource: arn:aws:sqs:us-west-1:000000000000:example_sqs_queue.fifo
                - receive_message_wait_time_seconds: 3
                - redrive_policy:
                    deadLetterTargetArn: arn:aws:sqs:us-west-1:000000000000:dead_letter_sqs_queue.fifo
                    maxReceiveCount: 5
                - visibility_timeout: 75
                - kms_master_key_id: alias/sample/key
                - kms_data_key_reuse_period_seconds: 735
                - fifo_queue: true
                - content_based_deduplication: true
                - deduplication_scope: message_group
                - fifo_throughput_limit: perMessageGroupId
                - tags:
                    something: this-is-just-some-text
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    resource_updated = False
    before = None
    queue_url = resource_id

    # Try to get the state of the resource if such is available
    if queue_url:
        queue_state_ret = await hub.exec.aws.sqs.queue.get(ctx, queue_url)
        if not queue_state_ret["result"] or not queue_state_ret["ret"]:
            result["result"] = False
            result["comment"] += queue_state_ret["comment"]
            return result

        before = queue_state_ret["ret"]

    present_attributes = {
        "delay_seconds": delay_seconds,
        "maximum_message_size": maximum_message_size,
        "message_retention_period": message_retention_period,
        "policy": policy,
        "receive_message_wait_time_seconds": receive_message_wait_time_seconds,
        "redrive_policy": redrive_policy,
        "visibility_timeout": visibility_timeout,
        "kms_master_key_id": kms_master_key_id,
        "kms_data_key_reuse_period_seconds": kms_data_key_reuse_period_seconds,
        "sqs_managed_sse_enabled": sqs_managed_sse_enabled,
        "fifo_queue": fifo_queue,
        "content_based_deduplication": content_based_deduplication,
        "deduplication_scope": deduplication_scope,
        "fifo_throughput_limit": fifo_throughput_limit,
    }

    # Convert the new state attributes to a dict of string values with raw attribute names
    plan_state_raw_attributes = (
        hub.tool.aws.sqs.conversion_utils.convert_present_attributes_to_raw(
            **present_attributes
        )
    )

    if before:
        # Check if the resource needs to be updated

        result["old_state"] = before

        # Convert the old state attributes to a dict of string values with raw attribute names
        old_state_raw_attributes = (
            hub.tool.aws.sqs.conversion_utils.convert_present_attributes_to_raw(
                before.get("delay_seconds"),
                before.get("maximum_message_size"),
                before.get("message_retention_period"),
                before.get("policy"),
                before.get("receive_message_wait_time_seconds"),
                before.get("redrive_policy"),
                before.get("visibility_timeout"),
                before.get("kms_master_key_id"),
                before.get("kms_data_key_reuse_period_seconds"),
                before.get("sqs_managed_sse_enabled"),
                before.get("fifo_queue"),
                before.get("content_based_deduplication"),
                before.get("deduplication_scope"),
                before.get("fifo_throughput_limit"),
            )
        )

        # Get only the attributes that need to be updated
        attributes_to_update = dict(
            plan_state_raw_attributes.items() - old_state_raw_attributes.items()
        )

        tags_to_remove, tags_to_add = hub.tool.aws.tag_utils.diff_tags_dict(
            before.get("tags"), tags
        )

        resource_updated = attributes_to_update or tags_to_add or tags_to_remove

        # Handle the case when updating the resource with --test
        if ctx.get("test", False):
            # Construct the new state in the case of updating the resource with --test
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "resource_id": resource_id,
                    **present_attributes,
                    "tags": tags,
                },
            )
            if attributes_to_update:
                # Updated resource
                result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                    "aws.sqs.queue", name
                )

            if tags_to_add or tags_to_remove:
                # Updated tags
                result[
                    "comment"
                ] += hub.tool.aws.comment_utils.would_update_tags_comment(
                    tags_to_remove, tags_to_add
                )
        else:
            # Update the attributes
            if attributes_to_update:
                updated_attributes_ret = (
                    await hub.exec.boto3.client.sqs.set_queue_attributes(
                        ctx, QueueUrl=queue_url, Attributes=attributes_to_update
                    )
                )

                updated_attributes_result = updated_attributes_ret["result"]
                result["result"] = result["result"] and updated_attributes_result
                result["comment"] += (
                    hub.tool.aws.comment_utils.update_comment("aws.sqs.queue", name)
                    if updated_attributes_result
                    else updated_attributes_ret["comment"]
                )

            # tags_to_remove may contain the tags to be updated. They do not need to be deleted and then added,
            # they can be updated just by calling the hub.exec.boto3.client.sqs.tag_queue with those updated tags,
            # so they can be removed from the dict of tags to remove
            tag_keys_to_delete = list(tags_to_remove.keys() - tags_to_add.keys())
            deleted_tags = False
            if tag_keys_to_delete:
                # Delete any tags from the old state which are not in the new state
                deleted_tags_ret = await hub.exec.boto3.client.sqs.untag_queue(
                    ctx, QueueUrl=queue_url, TagKeys=tag_keys_to_delete
                )
                deleted_tags = deleted_tags_ret["result"]
                if not deleted_tags:
                    result["result"] = False
                    result["comment"] += deleted_tags_ret["comment"]

            # Update or add tags
            updated_tags = False
            if tags_to_add:
                updated_tags_ret = await hub.exec.boto3.client.sqs.tag_queue(
                    ctx, QueueUrl=queue_url, Tags=tags_to_add
                )
                updated_tags = updated_tags_ret["result"]
                if not updated_tags:
                    result["result"] = False
                    result["comment"] += updated_tags_ret["comment"]

            if updated_tags or deleted_tags:
                result["comment"] += hub.tool.aws.comment_utils.update_tags_comment(
                    tags_to_remove, tags_to_add
                )

    else:
        # Handle the case when creating the resource with --test
        if ctx.get("test", False):
            # Construct the new state in the case of creating the resource with --test
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "resource_id": resource_id,
                    **present_attributes,
                    "tags": tags,
                },
            )
            result["comment"] += hub.tool.aws.comment_utils.would_create_comment(
                "aws.sqs.queue", name
            )
        else:
            # Create a new SQS queue

            ret = await hub.exec.boto3.client.sqs.create_queue(
                ctx,
                QueueName=name,
                Attributes=plan_state_raw_attributes,
                tags=tags,
            )

            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result
            queue_url = ret["ret"].get("QueueUrl")
            result["comment"] += hub.tool.aws.comment_utils.create_comment(
                "aws.sqs.queue", name
            )

    if (not before) or resource_updated:
        if not ctx.get("test", False):
            # Get the new state after creating or updating the resource
            queue_state_after = await hub.exec.aws.sqs.queue.get(
                ctx,
                queue_url,
                expected_attributes=present_attributes,
                expected_tags=tags,
            )
            result["new_state"] = queue_state_after["ret"]
            result["result"] = result["result"] and queue_state_after["result"]
            result["comment"] += queue_state_after["comment"]
    else:
        # Resource already exists or there are no updates to properties
        result["comment"] += hub.tool.aws.comment_utils.already_exists_comment(
            "aws.sqs.queue", name
        )
        result["new_state"] = copy.deepcopy(result["old_state"])

    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deletes the queue specified by the QueueUrl, regardless of the queue's contents.

    Be careful with the DeleteQueue action: When you delete a queue, any messages in the queue are no longer available.
    When you delete a queue, the deletion process takes up to 60 seconds. Requests you send involving that queue during
    the 60 seconds might succeed. For example, a  SendMessage  request might succeed, but after 60 seconds the queue and
    the message you sent no longer exist. When you delete a queue, you must wait at least 60 seconds before creating
    a queue with the same name. Cross-account permissions don't apply to this action. For more information, see
    Grant cross-account permissions to a role and a user name in the Amazon SQS Developer Guide.

    Args:
        name(str):
            The name of the SQS queue to delete.

        resource_id(str, Optional):
            The URL of the Amazon SQS queue to delete. Case-sensitive. Idem automatically considers this resource being
            absent if this field is not specified.

    Returns:
        dict[str, Any]

    Examples:
        .. code-block:: yaml

            resource_is_absent:
              aws.sqs.queue.absent:
                - resource_id: value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None

    # Try to get the previous state of the resource if such is available
    if resource_id:
        # resource_id is the queue URL
        queue_state_ret = await hub.exec.aws.sqs.queue.get(ctx, resource_id)

        if queue_state_ret["result"]:
            before = queue_state_ret["ret"]
        else:
            result["result"] = False
            result["comment"] += queue_state_ret["comment"]
            return result

    if not before:
        # Resource already absent
        result["comment"] += hub.tool.aws.comment_utils.already_absent_comment(
            "aws.sqs.queue", name
        )
    else:
        # Delete the resource

        result["old_state"] = before

        if ctx.get("test", False):
            result["comment"] += hub.tool.aws.comment_utils.would_delete_comment(
                "aws.sqs.queue", name
            )
            return result

        ret = await hub.exec.boto3.client.sqs.delete_queue(ctx, QueueUrl=resource_id)
        result["result"] = ret["result"]

        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] += hub.tool.aws.comment_utils.delete_comment(
            "aws.sqs.queue", name
        )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Returns a list of your queues in the current region.

    Returns:
        dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.sqs.queue
    """
    result = {}
    queue_urls_ret = await hub.exec.boto3.client.sqs.list_queues(ctx)

    if not queue_urls_ret["result"]:
        hub.log.warning(f"Could not describe aws.sqs.queue {queue_urls_ret['comment']}")
        return {}

    # The resource_id is the queue URL
    for resource_id in queue_urls_ret["ret"]["QueueUrls"]:
        queue_state_ret = await hub.exec.aws.sqs.queue.get(ctx, resource_id)

        if not queue_state_ret["ret"]:
            hub.log.debug(queue_state_ret["comment"])
            continue

        # queue_state_ret["ret"] can contain items of type NamespaceDict
        # which cannot be represented as a valid yaml, so they need to be
        # converted to dict which is done via this copy method
        queue_state = copy.copy(queue_state_ret["ret"])
        queue_state.pop("name")
        queue_state_list = [{k: v} for k, v in queue_state.items()]

        # The queue name is the last part of the queue URL, it is used as the idem resource name in describe
        name = resource_id.split("/")[-1]
        result[name] = {"aws.sqs.queue.present": queue_state_list}

    return result
