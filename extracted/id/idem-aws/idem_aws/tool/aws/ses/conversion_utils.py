from typing import Any
from typing import Dict


def convert_raw_domain_identity_to_present(
    hub,
    ctx,
    raw_resource: str,
) -> Dict[str, Any]:
    """
    Util functions to convert raw resource state to present input format for SES Domain Identity.

    """

    resource_translated = {
        "name": raw_resource,
        "domain": raw_resource,
        "resource_id": raw_resource,
    }

    return resource_translated


def convert_raw_identity_notification_topic_to_present(
    hub,
    attributes: Dict[str, Any],
    identity: str,
    notification_type: str = None,
) -> Dict[str, Any]:
    """
    Util functions to convert raw resource state to present input format for SES identity notification topic.

    """

    resource_translated = {"identity": identity}
    if not notification_type:
        return None

    resource_translated["resource_id"] = identity + "::" + notification_type
    resource_translated["notification_type"] = notification_type
    resource_translated["sns_topic"] = attributes.get(f"{notification_type}Topic")
    resource_translated["enabled"] = attributes.get(
        f"HeadersIn{notification_type}NotificationsEnabled"
    )

    return resource_translated
