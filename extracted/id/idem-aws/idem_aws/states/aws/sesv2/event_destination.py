"""State module to manage AWS SES event destination."""
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
    configuration_set_name: str,
    event_destination: make_dataclass(
        "EventDestinationDefinition",
        [
            ("Enabled", bool, field(default=None)),
            ("MatchingEventTypes", List[str], field(default=None)),
            (
                "KinesisFirehoseDestination",
                make_dataclass(
                    "KinesisFirehoseDestination",
                    [("IamRoleArn", str), ("DeliveryStreamArn", str)],
                ),
                field(default=None),
            ),
            (
                "CloudWatchDestination",
                make_dataclass(
                    "CloudWatchDestination",
                    [
                        (
                            "DimensionConfigurations",
                            List[
                                make_dataclass(
                                    "CloudWatchDimensionConfiguration",
                                    [
                                        ("DimensionName", str),
                                        ("DimensionValueSource", str),
                                        ("DefaultDimensionValue", str),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                field(default=None),
            ),
            (
                "SnsDestination",
                make_dataclass("SnsDestination", [("TopicArn", str)]),
                field(default=None),
            ),
            (
                "PinpointDestination",
                make_dataclass(
                    "PinpointDestination",
                    [("ApplicationArn", str, field(default=None))],
                ),
                field(default=None),
            ),
        ],
    ),
    resource_id: str = None,
) -> Dict[str, Any]:
    """Create or update an event destination.

    Events include message sends, deliveries, opens, clicks, bounces, and complaints.
    Event destinations are places that you can send information about these events to. For example, you can send
    event data to Amazon SNS to receive notifications when you receive bounces or complaints, or you can use Amazon
    Kinesis Data Firehose to stream data to Amazon S3 for long-term storage. A single configuration set can include
    more than one event destination.

    Args:
        resource_id(str, Optional):
            An identifier that identifies the event destination within the configuration set. Defaults to None.
        name(str):
            A name that identifies the event destination within the configuration set.
        configuration_set_name(str):
            The name of the configuration set.
        event_destination(dict[str, Any]):
            An object that defines the event destination.

            * Enabled (bool, Optional):
                If true, the event destination is enabled. When the event destination is enabled, the specified
                event types are sent to the destinations in this EventDestinationDefinition. If false, the event
                destination is disabled. When the event destination is disabled, events aren't sent to the
                specified destinations.

            * MatchingEventTypes (list[str], Optional):
                An array that specifies which events the Amazon SES API v2 should send to the destinations in
                this EventDestinationDefinition.

            * KinesisFirehoseDestination (dict[str, Any], Optional):
                An object that defines an Amazon Kinesis Data Firehose destination for email events. You can use
                Amazon Kinesis Data Firehose to stream data to other services, such as Amazon S3 and Amazon
                Redshift.

                * IamRoleArn (str):
                    The Amazon Resource Name (ARN) of the IAM role that the Amazon SES API v2 uses to send email
                    events to the Amazon Kinesis Data Firehose stream.
                * DeliveryStreamArn (str):
                    The Amazon Resource Name (ARN) of the Amazon Kinesis Data Firehose stream that the Amazon SES
                    API v2 sends email events to.

            * CloudWatchDestination (dict[str, Any], Optional):
                An object that defines an Amazon CloudWatch destination for email events. You can use Amazon
                CloudWatch to monitor and gain insights on your email sending metrics.

                * DimensionConfigurations (list[dict[str, Any]]):
                    An array of objects that define the dimensions to use when you send email events to Amazon
                    CloudWatch.

                    * DimensionName (str):
                        The name of an Amazon CloudWatch dimension associated with an email sending metric. The name has
                        to meet the following criteria:   It can only contain ASCII letters (a–z, A–Z), numbers (0–9),
                        underscores (_), or dashes (-).   It can contain no more than 256 characters.
                    * DimensionValueSource (str):
                        The location where the Amazon SES API v2 finds the value of a dimension to publish to Amazon
                        CloudWatch. To use the message tags that you specify using an X-SES-MESSAGE-TAGS header or a
                        parameter to the SendEmail or SendRawEmail API, choose messageTag. To use your own email
                        headers, choose emailHeader. To use link tags, choose linkTags.
                    * DefaultDimensionValue (str):
                        The default value of the dimension that is published to Amazon CloudWatch if you don't provide
                        the value of the dimension when you send an email. This value has to meet the following
                        criteria:   It can only contain ASCII letters (a–z, A–Z), numbers (0–9), underscores (_), or
                        dashes (-).   It can contain no more than 256 characters.

            * SnsDestination (dict[str, Any], Optional):
                An object that defines an Amazon SNS destination for email events. You can use Amazon SNS to
                send notification when certain email events occur.

                * TopicArn (str):
                    The Amazon Resource Name (ARN) of the Amazon SNS topic to publish email events to. For more
                    information about Amazon SNS topics, see the Amazon SNS Developer Guide.

            * PinpointDestination (dict[str, Any], Optional):
                An object that defines an Amazon Pinpoint project destination for email events. You can send
                email event data to a Amazon Pinpoint project to view metrics using the Transactional Messaging
                dashboards that are built in to Amazon Pinpoint. For more information, see Transactional
                Messaging Charts in the Amazon Pinpoint User Guide.

                * ApplicationArn (str, Optional):
                    The Amazon Resource Name (ARN) of the Amazon Pinpoint project to send email events to.

    Returns:
        .. code-block:: bash

            {"result": True|False, "comment": ("A tuple",), "ret": None|Dict}


    Examples:
        .. code-block:: sls

            resource_is_present:
              aws.sesv2.event_destination.present:
                - name: value
                - configuration_set_name: value
                - event_destination: value
    """
    result, before, changed, exists = (
        dict(comment=[], old_state=None, new_state=None, name=name, result=True),
        None,
        False,
        False,
    )
    if "SnsDestination" not in event_destination:
        result["comment"] += ["Only SnsDestination is supported now."]
        result["result"] = False
        return result
    before = await hub.exec.aws.sesv2.event_destination.get(
        ctx=ctx,
        resource_id=name,
        configuration_set_name=configuration_set_name,
    )
    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result
    if before.get("ret"):
        exists = True
        result["old_state"] = before["ret"].copy()
        if result["old_state"]["event_destination"] != event_destination:
            changed = True
    payload = {
        "ConfigurationSetName": configuration_set_name,
        "EventDestinationName": name,
        "EventDestination": event_destination,
    }
    action, func = (
        ("update", "update_configuration_set_event_destination")
        if exists
        else ("create", "create_configuration_set_event_destination")
    )
    if ctx.get("test") and (not exists or changed):
        result[
            "new_state"
        ] = hub.tool.aws.sesv2.conversion_utils.convert_raw_event_destination_to_present(
            configuration_set_name=configuration_set_name,
            raw_resource=event_destination,
            name=name,
        )
        result["comment"] = getattr(
            hub.tool.aws.comment_utils, f"would_{action}_comment"
        )(resource_type="aws.sesv2.event_destination", name=name)
    elif exists and not changed:
        result["new_state"] = result["old_state"]
        result["comment"] = getattr(
            hub.tool.aws.comment_utils, "already_exists_comment"
        )(resource_type="aws.sesv2.event_destination", name=name)
    else:
        try:
            ret = await getattr(hub.exec.boto3.client.sesv2, func)(ctx, **payload)
            if not ret["result"]:
                result["comment"] = ret["comment"]
                result["result"] = False
                return result
            else:
                result[
                    "new_state"
                ] = hub.tool.aws.sesv2.conversion_utils.convert_raw_event_destination_to_present(
                    configuration_set_name=configuration_set_name,
                    name=name,
                    raw_resource=event_destination,
                )
                result["comment"] = getattr(
                    hub.tool.aws.comment_utils, f"{action}_comment"
                )(resource_type="aws.sesv2.event_destination", name=name)
        except Exception as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False
    return result


async def absent(
    hub, ctx, name: str, configuration_set_name: str = None, resource_id: str = None
) -> Dict[str, Any]:
    """Delete an event destination.

    Events include message sends, deliveries, opens, clicks, bounces, and complaints.
    Event destinations are places that you can send information about these events to. For example, you can send
    event data to Amazon SNS to receive notifications when you receive bounces or complaints, or you can use Amazon
    Kinesis Data Firehose to stream data to Amazon S3 for long-term storage.

    Args:
        name(str):
            The name of the event destination to delete.
        configuration_set_name(str, Optional):
            The name of the configuration set that contains the event destination to delete.
        resource_id(str, Optional):
            An identifier of the resource in the provider.

    Returns:
        .. code-block:: bash

            {"result": True|False, "comment": ("A tuple",), "ret": None|Dict}


    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.sesv2.event_destination.absent:
                - name: value
                - resource_id: value
                - configuration_set_name: value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.sesv2.event_destination", name=name
        )
        return result

    if not configuration_set_name:
        result["comment"] = hub.tool.aws.comment_utils.missing_args_for_absent_comment(
            resource_type="aws.sesv2.event_destination",
            name=name,
            args=["configuration_set_name"],
        )
        result["result"] = False
        return result

    before = await hub.exec.aws.sesv2.event_destination.get(
        ctx=ctx,
        resource_id=resource_id,
        configuration_set_name=configuration_set_name,
    )

    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result

    if not before.get("ret"):
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.sesv2.event_destination", name=name
        )
        return result

    result["old_state"] = before.get("ret")

    if ctx.get("test", False):
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.sesv2.event_destination", name=name
        )
        return result
    else:
        try:
            ret = await hub.exec.boto3.client.sesv2.delete_configuration_set_event_destination(
                ctx,
                **{
                    "ConfigurationSetName": configuration_set_name,
                    "EventDestinationName": resource_id,
                },
            )
            if not result["result"]:
                result["comment"] = ret["comment"]
                result["result"] = False
                return result
            result["comment"] = hub.tool.aws.comment_utils.delete_comment(
                resource_type="aws.sesv2.event_destination", name=name
            )
        except Exception as e:
            result["result"] = False
            result["comment"] += [f"{e.__class__.__name__}: {e}"]

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            idem describe aws.sesv2.event_destination
    """
    result = await hub.exec.aws.sesv2.event_destination.list(ctx)

    if not result["result"]:
        hub.log.warning(f"Could not describe Event destination {result['comment']}")
        return {}

    return result["ret"]
