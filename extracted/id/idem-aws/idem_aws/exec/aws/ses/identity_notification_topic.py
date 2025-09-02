"""Exec module for managing AWS SES Identity notification topic."""

__func_alias__ = {"list_": "list"}


async def get(hub, ctx, name: str, resource_id: str):
    """Get SES Notification Topic from AWS account.

    Args:
        name(str):
            A name for the Identity Notification Topic.

        resource_id (str):
            The identifier for AWS Identity Notification Topic, combination of identity, notification topic separated by
            a separator '::'.

    Returns:
        Dict[str, Any]:
            Returns Notification Topic in present format

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec aws.ses.identity_notification_topic.get name = "my_resource" resource_id="example.com::Complaint"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.ses.identity_notification_topic.get
                - kwargs:
                    name: "my_resource"
                    resource_id:"example.com::Complaint"
    """
    result = dict(comment=[], ret=None, result=True)

    identity = resource_id.split("::")[0]

    ret = await hub.exec.aws.ses.identity_notification_topic.list(ctx, [identity])

    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    if not ret["ret"]:
        result["comment"] += [f"No identity notification set for identity '{identity}'"]

    for resource in ret["ret"]:
        if resource.get("resource_id") == resource_id:
            result["ret"] = resource
            break

    return result


async def list_(hub, ctx, identities: list = None):
    """Lists SES Domain notification topics.

    Args:
        name (str):
            A name for the Identity Notification Topic.

        identities (list):
            List of AWS Identity Notification Topic IDs.

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec aws.ses.identity_notification_topic.list identities="example.com"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.ses.identity_notification_topic.list
                - kwargs:
                    identities:"example.com"

    """
    result = dict(comment=[], ret=[], result=True)

    if not identities:
        ret_ids = await hub.exec.boto3.client.ses.list_identities(ctx)

        if not ret_ids["result"]:
            result["comment"] += ret_ids["comment"]
            result["result"] = False
            return result

        identities = ret_ids["ret"].get("Identities")

    ret = await hub.exec.boto3.client.ses.get_identity_notification_attributes(
        ctx, Identities=identities
    )

    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    for identity, attributes in ret["ret"]["NotificationAttributes"].items():
        if "BounceTopic" in attributes:
            result["ret"].append(
                hub.tool.aws.ses.conversion_utils.convert_raw_identity_notification_topic_to_present(
                    attributes=attributes,
                    identity=identity,
                    notification_type="Bounce",
                )
            )

        if "ComplaintTopic" in attributes:
            result["ret"].append(
                hub.tool.aws.ses.conversion_utils.convert_raw_identity_notification_topic_to_present(
                    attributes=attributes,
                    identity=identity,
                    notification_type="Complaint",
                )
            )

        if "DeliveryTopic" in attributes:
            result["ret"].append(
                hub.tool.aws.ses.conversion_utils.convert_raw_identity_notification_topic_to_present(
                    attributes=attributes,
                    identity=identity,
                    notification_type="Delivery",
                )
            )

    return result
