from ..service import Service
from urllib.parse import quote
from typing import Any, Dict, List, Optional, Union
from ..exception import AppwriteException
from appwrite_console.utils.deprecated import deprecated
from ..models.notification_list import NotificationList
from ..models.notification import Notification


class Notifications(Service):

    def __init__(self, client) -> None:
        super(Notifications, self).__init__(client)

    def list(
        self,
        queries: Optional[List[str]] = None,
        total: Optional[bool] = None,
    ) -> NotificationList:
        """
        Get the list of notifications for the currently logged in console user. Use queries to filter the results by attributes such as read status, view timestamps, or creation date.

        Parameters
        ----------
        queries : Optional[List[str]]
            Array of query strings generated using the Query class provided by the SDK. [Learn more about queries](https://appwrite.io/docs/queries). Maximum of 100 queries are allowed, each 4096 characters long. You may filter on the following attributes: read, type, channel, messageId, projectId, resourceType, resourceId, parentResourceType, parentResourceId, firstSeen, lastSeen
        total : Optional[bool]
            When set to false, the total count returned will be 0 and will not be calculated.
        Returns
        -------
        NotificationList
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/notifications'
        api_params = {}
        if queries is not None:
            api_params['queries'] = self._normalize_value(queries)
        if total is not None:
            api_params['total'] = self._normalize_value(total)

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=NotificationList)

    def update(
        self,
        notification_id: str,
        read: bool,
    ) -> Notification:
        """
        Update a notification by its unique ID. Use the `read` parameter to mark the notification as read or unread.

        Parameters
        ----------
        notification_id : str
            Notification ID.
        read : bool
            Notification read status.
        Returns
        -------
        Notification
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/notifications/{notificationId}'
        api_params = {}
        if notification_id is None or notification_id == '':
            raise AppwriteException('Missing required parameter: "notification_id"')
        if read is None:
            raise AppwriteException('Missing required parameter: "read"')
        api_path = api_path.replace('{notificationId}', self._encode_path(notification_id))
        api_params['read'] = self._normalize_value(read)

        response = self.client.call(
            'patch',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'content-type': 'application/json',
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=Notification)
