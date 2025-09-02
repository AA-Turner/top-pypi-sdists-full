"""Exec module for managing AWS SQS queue."""
import time
from typing import Any
from typing import Dict


async def get(
    hub,
    ctx,
    resource_id: str,
    expected_attributes: Dict = None,
    expected_tags: Dict = None,
    max_retries: int = 45,
    delay_between_retries: int = 1,
) -> Dict[str, Any]:
    """Returns the state of an SQS queue.

    Args:
        resource_id(str):
            The URL of the queue.

        expected_attributes(dict, Optional):
            Retries getting the attributes until they contain these expected attributes.

        expected_tags(dict, Optional):
            Retries getting the tags until they contain these expected tags.

        max_retries(int, Optional):
            Max retries for getting the attributes and/or the tags when the expected_attributes and/or expected_tags are
            set.

        delay_between_retries(int, Optional):
            The delay in seconds between the retries.

    Examples:
        .. code-block:: yaml

            get_a_queue:
              exec.run:
                - path: aws.sqs.queue.get
                - kwargs:
                   resource_id: "https://us-west-1.queue.amazonaws.com/000000000000/example_fifo_queue.fifo"
    """
    result = dict(ret=None, comment=[], result=True)
    name = resource_id.split("/")[-1]
    ret = dict(name=name, resource_id=resource_id)
    new_queue_attributes_ret = {}

    if expected_attributes:
        # Poll get_queue_attributes() until it returns the expected attributes
        for i in range(max_retries):
            # Get the queue attributes
            new_queue_attributes_ret = (
                await hub.exec.boto3.client.sqs.get_queue_attributes(
                    ctx, QueueUrl=resource_id, AttributeNames=["All"]
                )
            )

            if new_queue_attributes_ret["result"]:
                present_attributes = (
                    hub.tool.aws.sqs.conversion_utils.convert_raw_attributes_to_present(
                        new_queue_attributes_ret["ret"].get("Attributes")
                    )
                )

                if hub.tool.aws.sqs.queue_utils.compare_present_queue_attributes(
                    expected_attributes, present_attributes
                ):
                    break

            time.sleep(delay_between_retries)
    else:
        # Get the queue attributes
        new_queue_attributes_ret = await hub.exec.boto3.client.sqs.get_queue_attributes(
            ctx, QueueUrl=resource_id, AttributeNames=["All"]
        )

    if new_queue_attributes_ret["result"]:
        # Convert the raw queue attributes to present form and add them to the final result
        present_attributes = (
            hub.tool.aws.sqs.conversion_utils.convert_raw_attributes_to_present(
                new_queue_attributes_ret["ret"].get("Attributes")
            )
        )
        ret.update(present_attributes.items())
    else:
        error_comment = new_queue_attributes_ret["comment"]
        if "QueueDoesNotExist" in str(error_comment):
            result["comment"] += (
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.sqs.queue", name=name
                ),
            )
        else:
            result["result"] = False
        result["comment"] += error_comment
        return result

    new_queue_tags_ret = {}
    if expected_tags:
        # Poll list_queue_tags() until it returns the expected tags
        for i in range(max_retries):
            # Get the queue tags
            new_queue_tags_ret = await hub.exec.boto3.client.sqs.list_queue_tags(
                ctx, QueueUrl=resource_id
            )

            if new_queue_tags_ret["result"]:
                if expected_tags.items() <= new_queue_tags_ret["ret"]["Tags"].items():
                    break

            time.sleep(delay_between_retries)
    else:
        # Get the queue tags
        new_queue_tags_ret = await hub.exec.boto3.client.sqs.list_queue_tags(
            ctx, QueueUrl=resource_id
        )

    if new_queue_tags_ret["result"]:
        # Add the queue tags to the final result
        ret["tags"] = dict(new_queue_tags_ret["ret"].get("Tags", {}))
    else:
        error_comment = new_queue_tags_ret["comment"]
        if "QueueDoesNotExist" in str(error_comment):
            result["comment"] += (
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.sqs.queue", name=name
                ),
            )
        else:
            result["result"] = False
        result["comment"] += error_comment
        return result

    result["ret"] = ret

    return result
