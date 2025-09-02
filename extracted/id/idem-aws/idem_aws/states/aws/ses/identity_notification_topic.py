"""State module to manage AWS SES Identity notification topic."""
import copy
import re
from typing import Any
from typing import Dict

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    identity: str,
    notification_type: str,
    sns_topic: str = None,
    enabled: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Sets an Amazon Simple Notification Service (Amazon SNS) topic to use when delivering notifications.

    When you use this operation, you specify a verified identity, such as an email address or domain. When you send an
    email that uses the chosen identity in the Source field, Amazon SES sends notifications to the topic you specified.

    Args:
        name(str):
            A name for the Identity Notification Topic.

        identity(str):
            The identity (email address or domain) that you want to set the Amazon SNS topic for.

        notification_type(str):
            The type of notifications that will be published to the specified Amazon SNS topic.

        sns_topic(str, Optional):
            The Amazon Resource Name (ARN) of the Amazon SNS topic. If the parameter is omitted from the request or a
            null value is passed, SnsTopic is cleared and publishing is disabled.

        enabled(bool, Optional):
            Sets whether Amazon SES includes the original email headers in Amazon SNS notifications of the specified
            notification type. A value of true specifies that Amazon SES will include headers in notifications, and a
            value of false specifies that Amazon SES will not include headers in notifications.

        resource_id(str, Optional):
            The identifier for AWS Identity Notification Topic, combination of identity, notification topic separated
            by a separator '::'.

    Request Syntax:
        .. code-block:: sls

            resource_is_present:
              aws.ses.identity_notification_topic.present:
                - name: "string"
                - identity: "string"
                - notification_type: "string"
                - sns_topic: "string"

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              aws.ses.identity_notification_topic.present:
                - name: name
                - identity: user@example.com
                - notification_type: Bounce
                - sns_topic: arn:aws:sns:us-west-2:111122223333:MyTopic
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    changed = False

    if resource_id:
        if (
            not re.findall("::", resource_id)
            or not len(re.findall("::", resource_id)) == 1
        ):
            result[
                "comment"
            ] = f"Incorrect aws.ses.identity_notification_topic resource_id: {resource_id}. Expected id <identity>::<notification_type>"
            result["result"] = False
            return result

        before = await hub.exec.aws.ses.identity_notification_topic.get(
            ctx,
            name=name,
            resource_id=resource_id,
        )

        if not before["result"]:
            result["comment"] = before["comment"]
            result["result"] = False
            return result

    if before and before.get("ret"):
        result["old_state"] = before["ret"].copy()
        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.ses.identity_notification_topic", name=name
        )
        if (
            result["old_state"]["sns_topic"] != sns_topic
            or result["old_state"].get("enabled") != enabled
        ):
            changed = True
        else:
            result["new_state"] = copy.deepcopy(result["old_state"])
            return result

    if sns_topic or enabled:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "identity": identity,
                    "notification_type": notification_type,
                    "sns_topic": sns_topic,
                    "enabled": enabled,
                },
            )
            if changed:
                result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                    resource_type="aws.ses.identity_notification_topic", name=name
                )
            else:
                result["comment"] += hub.tool.aws.comment_utils.would_create_comment(
                    resource_type="aws.ses.identity_notification_topic", name=name
                )
            return result

        if sns_topic:
            ret = await hub.exec.boto3.client.ses.set_identity_notification_topic(
                ctx,
                Identity=identity,
                NotificationType=notification_type,
                SnsTopic=sns_topic,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] += ret["comment"]
                return result
            if changed:
                result["comment"] += hub.tool.aws.comment_utils.update_comment(
                    "aws.ses.identity_notification_topic", name
                )
            else:
                result["comment"] += hub.tool.aws.comment_utils.create_comment(
                    "aws.ses.identity_notification_topic", name
                )
        if enabled is not None:
            ret = await hub.exec.boto3.client.ses.set_identity_headers_in_notifications_enabled(
                ctx,
                Identity=identity,
                NotificationType=notification_type,
                Enabled=enabled,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] += ret["comment"]
                return result
            if not (before and before["ret"]) or changed:
                result["comment"] += hub.tool.aws.comment_utils.update_comment(
                    "aws.ses.identity_notification_topic", name
                )
            else:
                result["comment"] += hub.tool.aws.comment_utils.create_comment(
                    "aws.ses.identity_notification_topic", name
                )
        new = await hub.exec.aws.ses.identity_notification_topic.get(
            ctx,
            name=name,
            resource_id=resource_id if changed else identity + "::" + notification_type,
        )
        if not new["result"]:
            result["comment"] += new["comment"]
            result["result"] = False
            return result

        result["new_state"] = new["ret"]

    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Clears the SnsTopic and disables the publishing.

    Args:
        name(str):
            A name for the Identity Notification Topic.

        resource_id(str, Optional):
            The identifier for AWS Identity Notification Topic, combination of identity, notification topic separated by
            a separator '::'.

    Request Syntax:
        .. code-block:: sls

            resource_is_absent:
              aws.ses.identity_notification_topic.absent:
                - name: "string"
                - resource_id: "string"

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.ses.identity_notification_topic.absent:
                - name: value
                - resource_id: value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ses.identity_notification_topic", name=name
        )
        return result
    identity = resource_id.split("::")[0]
    notification_type = resource_id.split("::")[1]
    before = await hub.exec.aws.ses.identity_notification_topic.get(
        ctx,
        name=name,
        resource_id=resource_id,
    )
    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result
    if before.get("ret"):
        result["old_state"] = before["ret"].copy()
        if ctx.get("test", False):
            result["comment"] += getattr(
                hub.tool.aws.comment_utils, "would_delete_comment"
            )(resource_type="aws.ses.identity_notification_topic", name=name)
            return result
        else:
            ret = await hub.exec.boto3.client.ses.set_identity_notification_topic(
                ctx,
                Identity=identity,
                NotificationType=notification_type,
                SnsTopic=None,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] += ret["comment"]
                result["result"] = False
                return result
            result["comment"] += getattr(hub.tool.aws.comment_utils, "delete_comment")(
                resource_type="aws.ses.identity_notification_topic", name=name
            )

    else:
        result["comment"] += getattr(
            hub.tool.aws.comment_utils, "already_absent_comment"
        )(resource_type="aws.ses.identity_notification_topic", name=name)

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            idem describe aws.ses.identity_notification_topic
    """

    result = {}

    ret = await hub.exec.aws.ses.identity_notification_topic.list(ctx)
    if not ret["result"]:
        hub.log.warning(f"Could not list identities {ret['comment']}")
        return {}

    for resource in ret["ret"]:
        resource_id = resource.get("resource_id")

        result[resource_id] = {
            "aws.ses.identity_notification_topic.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }

    return result
