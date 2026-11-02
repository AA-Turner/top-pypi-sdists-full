from typing import List, Dict, Any, Union
import logging

_logger = logging.getLogger(__name__)

from ...api.notifications import publish_notification as api_publish_notification
from ...models.os_notification import OsNotification
from ...client import Client
from ..exceptions import ApiConnectionError


def sync(
    notification: Union[Dict[str, Any], List[Dict[str, Any]]], client: Client = None
):
    """
    # Publishes desktop notifications to specified channels (users).

    ## Arguments
    - `notification`: One or more notification dictionaries. Each notification should contain:
        - `channel`: Username or channel to send the notification to (required)
        - `title`: Notification title (required)
        - `body`: Notification body text (required)
        - `workspace_id`: Workspace ID related to the notification (optional)
        - `type`: Notification type, e.g., "octostar:desktop:builtins:wso:update" (optional)
        - `expires_at`: ISO 8601 timestamp when notification expires (optional)
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Raises
    - `ApiConnectionError`: If the request was unsuccessful on the server.
    """
    if not isinstance(notification, list):
        notification = [notification]
    default_fields = {"type": "octostar:desktop:builtins:wso:update"}
    notification_objects = [
        OsNotification.from_dict({**default_fields, **notif}) for notif in notification
    ]
    response = api_publish_notification.sync_detailed(
        json_body=notification_objects, client=client
    )
    if response.status_code != 201:
        raise ApiConnectionError("publish_notification", response, client)


async def asyncio(
    notification: Union[Dict[str, Any], List[Dict[str, Any]]], client: Client = None
):
    """
    # Publishes asynchronously desktop notifications to specified channels (users).

    ## Arguments
    - `notification`: One or more notification dictionaries. Each notification should contain:
        - `channel`: Username or channel to send the notification to (required)
        - `title`: Notification title (required)
        - `body`: Notification body text (required)
        - `workspace_id`: Workspace ID related to the notification (optional)
        - `type`: Notification type, e.g., "octostar:desktop:builtins:wso:update" (optional)
        - `expires_at`: ISO 8601 timestamp when notification expires (optional)
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Raises
    - `ApiConnectionError`: If the request was unsuccessful on the server.
    """
    if not isinstance(notification, list):
        notification = [notification]
    default_fields = {"type": "octostar:desktop:builtins:wso:update"}
    notification_objects = [
        OsNotification.from_dict({**default_fields, **notif}) for notif in notification
    ]
    response = await api_publish_notification.asyncio_detailed(
        json_body=notification_objects, client=client
    )
    if response.status_code != 201:
        raise ApiConnectionError("publish_notification", response, client)
