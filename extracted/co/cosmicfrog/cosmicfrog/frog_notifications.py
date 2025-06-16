"""
    Notification handler service, for use with CosmicFrog.
    Deprecates the frog_activity.py implementation
    API:
        get_notifications:
            https://{base-api-url}/v0/notifications
            Method: GET
            Returns: {count: int, 
                filters: {level: string, parentId: string, createdBy: string, createdAfter: string ,dataUpdatedAfter: string, includeDeleted: boolean}, 
                items: [Notification]}
        create_notification:
            https://{base-api-url}/v0/notification
            method: POST
            body: {topics: [string], createdBy: string,  parentId: string, level: string,data: {}, expires: string dateTime when the notification should expire, title: string, message: string}
        get_notification_by_id:
            https://{base-api-url}/v0/notification/{notificationId}
            Method: GET
            Returns same as get_notifications
        delete_notification_by_id:
            https://{base-api-url}/v0/notification/{notificationId}
            method: DELETE
        update_notification_data_by_id:
            https://{base-api-url}/v0/notification/{notificationId}/data/{fieldName}
            method: PATCH
            queryString params: value, type
        update_many_notification_by_id:
            https://{base-api-url}/v0/notification/{notificationId}/data
            method: PATCH
        acknowledge_notification:
            https://{base-api-url}/v0/notification/{notificationId}/acknowledge
            method: PATCH
"""

import asyncio
from enum import Enum
import json
import time
from uuid import uuid4
import httpx
from logging import Logger
import os
from typing import Literal, Dict, List, Optional, Union, Any
from .sync_wrapper import sync_wrapper

# possible missing methods that could be called depending on the split
# TODO add missing methods here (hinges on new signal API which is unavailble
# at the moment in June 2024)
from .frog_activity_status import ActivityStatus

# There's a new activity endpoint which deprecates the white-bullfrog one
# however we need to be backwards compatible here..
CF_ACTIVITY_URL = os.getenv("CF_ACTIVITY_URL_NEW", "https://service.optilogic.app/websocket/message")
CF_NOTIFICATION_URL = os.getenv("CF_NOTIFICATION_URL", "https://api.optilogic.app").strip("/")

def safe_int_cast(value, default):
    """
    Try to cast the given value to an integer. If this fails, return the default. Should handle
    empty strings as well as None and some random sets of charaters.
    Args:
        value: The value to be cast to an integer.
        default: The value to be returned if the cast fails.
    Returns:
        The integer value of the given value, or the default if the cast fails.
    """
    if value is None or value == "":
        return default
    try:
        return int(value)
    except ValueError:
        return default


RETRY_COUNT = safe_int_cast(os.getenv("CFLIB_HTTPX_RETRY_COUNT"), 3) 
TIMEOUT = safe_int_cast(os.getenv("CFLIB_HTTPX_ACTIVITY_TIMEOUT"), 30)

def ensure_message_and_title(data: dict, model_name: str, description: str) -> dict:
    """
    Ensure that 'message' and 'title' are present in the data dictionary.
    If not provided, construct them from model_name and description.
    """
    if 'message' not in data:
        data['message'] = description
    if 'title' not in data:
        data['title'] = model_name
    return data


class ModelActivity:
    def __init__(
        self,
        logger: Logger,
        correlation_id: str,
        model_name: str,
        description: str,
        tags: str,
        app_key: str,
        account: Optional[object] = {},
    ) -> None:
        if not CF_NOTIFICATION_URL:
            raise ValueError("CF_NOTIFICATION_URL environment variable not set")
        self.correlation_id = correlation_id
        self.logger = logger
        self.model_name = model_name
        self.description = description
        self.tags = tags
        self.done = False
        self.activity_id = None
        self.status = "pending"
        self.app_key = app_key
        self.account = account
        self.client = httpx.AsyncClient(timeout=TIMEOUT)
        self.notifications_endpoint = f"{CF_NOTIFICATION_URL}/v0/notifications"
        self.notification_endpoint_template = (
            f"{CF_NOTIFICATION_URL}/v0/notification/{{notificationId}}"
        )
        self.create_notification_endpoint = f"{CF_NOTIFICATION_URL}/v0/notification"
        self.delete_notification_endpoint = (
            f"{CF_NOTIFICATION_URL}/v0/notification/{{notificationId}}"
        )
        self.update_notification_data_field_endpoint_template = f"{CF_NOTIFICATION_URL}/v0/notification/{{notificationId}}/data/{{fieldName}}"
        self.update_many_notification_data_fields_endpoint_template = (
            f"{CF_NOTIFICATION_URL}/v0/notification/{{notificationId}}/data"
        )
        self.acknowledge_notification_endpoint = (
            f"{CF_NOTIFICATION_URL}/v0/notification/{{notificationId}}/acknowledge"
        )

    async def close(self):
        self.logger.info("Closing httpx client")
        await self.client.aclose()

    def _get_api_header(self):
        return {"x-app-key": self.app_key, "correlation-id": self.correlation_id}

    async def _request_with_retries(
        self, method: str, url: str, **kwargs
    ) -> Optional[httpx.Response]:
        attempt = 0
        headers = self._get_api_header()

        while attempt < RETRY_COUNT:
            try:
                self.logger.info(f"Attempt {attempt} for {method} request to {url}")
                response = await self.client.request(
                    method, url, headers=headers, **kwargs
                )
                response.raise_for_status()
                return response

            except (
                httpx.HTTPStatusError,
                httpx.RequestError,
                httpx.TimeoutException,
            ) as e:
                attempt += 1

                if attempt >= RETRY_COUNT:
                    self.logger.error(
                        f"All {RETRY_COUNT} retries failed for {method} request to {url}. "
                        f"Final error: {str(e)}. "
                        f"Correlation ID: {self.correlation_id}"
                    )
                    return None
                
                wait_time = 2**attempt  # Exponential backoff
                self.logger.warning(
                    f"Retry {attempt}/{RETRY_COUNT} for {method} request to {url}. "
                    f"Error: {str(e)}. "
                    f"Waiting {wait_time}s before next attempt. "
                    f"Correlation ID: {self.correlation_id}"
                )
                await asyncio.sleep(wait_time)

    async def get_notifications_async(
        self,
        topics: Optional[List[str]] = None,
        level: Optional[str] = None,
        parentId: Optional[str] = None,
        createdBy: Optional[str] = None,
        # assuming correct format is passed
        createdAfter: Optional[str] = None,
        dataUpdatedAfter: Optional[str] = None,
        acknowledged: Optional[str] = None,
        ids: Optional[Union[List[str], str]] = None,
    ) -> dict:
        # leans into dictionary comprehension to avoid having a ton of if statements
        # seems more elegant but when it comes time to debug maybe we revert to basic
        # ifs or switch statement
        params = {
            "topics": ",".join(topics + ["modelEditor"]) if topics else "modelEditor",
            "level": "high", # TODO change to level when HTTP 409 is handled on platform differently
            "parentId": parentId,
            "createdBy": createdBy,
            "createdAfter": createdAfter,
            "dataUpdatedAfter": dataUpdatedAfter,
            "acknowledged": acknowledged,
            "ids": ",".join(ids) if isinstance(ids, list) else ids,
        }
        params = {k: v for k, v in params.items() if v is not None} if params else None
        response = await self._request_with_retries(
            "GET", self.notifications_endpoint, params=params
        )
        return response.json() if response else None

    get_notifications = sync_wrapper(get_notifications_async)

    async def get_notification_by_id_async(self, notificationId: str) -> dict:
        url = self.notification_endpoint_template.format(notificationId=notificationId)

        response = await self._request_with_retries("GET", url)
        return response.json() if response else None

    get_notification_by_id = sync_wrapper(get_notification_by_id_async)

    async def create_notification_async(
        self,
        topics: List[str],
        createdBy: Optional[str] = None,
        parentId: Optional[str] = None,
        level: Optional[str] = None,
        data: Optional[dict] = None,
        # assuming time correct format is passed
        expires: Optional[str] = None,
        title: Optional[str] = None,
        message: Optional[str] = None,
    ) -> dict:
        assert len(topics) > 0
        jsonPayload = {
            "topics": ",".join(topics + ["modelEditor"]) if topics else "modelEditor",
            "createdBy": createdBy,
            "parentId": parentId,
            "level": "high", # TODO change to level when HTTP 409 is handled on platform differently
            "data": data or {},
            "expires": expires,
            "title": title,
            "message": message,
        }
        payload = {k: v for k, v in jsonPayload.items() if v is not None}

        response = await self._request_with_retries(
            "POST", self.create_notification_endpoint, json=payload
        )
        return response.json() if response else None

    create_notification = sync_wrapper(create_notification_async)

    async def delete_notification_by_id_async(self, notificationId: str) -> None:
        url = self.notification_endpoint_template.format(notificationId=notificationId)
        response = await self._request_with_retries("DELETE", url)
        return response.json() if response else None

    delete_notification_by_id = sync_wrapper(delete_notification_by_id_async)

    async def update_notification_data_by_id_async(
        self,
        notificationId: str,
        fieldName: str,
        value: str,
        value_type: Optional[str] = "string",
    ) -> dict:
        url = self.update_notification_data_field_endpoint_template.format(
            notificationId=notificationId, fieldName=fieldName
        )

        params = {"value": value, "type": value_type}

        response = await self._request_with_retries("PATCH", url, params=params)
        return response.json() if response else None

    update_notification_data_by_id = sync_wrapper(update_notification_data_by_id_async)

    async def update_many_notification_data_async(
        self,
        notificationId: str,
        body_params: Optional[
            Dict[str, Union[str, int, float, bool, dict, list]]
        ] = None,
    ) -> dict:
        url = self.update_many_notification_data_fields_endpoint_template.format(
            notificationId=notificationId
        )
        response = await self._request_with_retries("PATCH", url, json=body_params)
        return response.json() if response else None

    update_many_notification_data = sync_wrapper(update_many_notification_data_async)

    async def acknowledge_notification_async(self, notificationId: str) -> dict:
        url = self.acknowledge_notification_endpoint.format(
            notificationId=notificationId
        )
        response = await self._request_with_retries("PATCH", url)
        return response.json() if response else None

    acknowledge_notification = sync_wrapper(acknowledge_notification_async)

    # Bridge functions for tadpole and others consuming activity
    async def create_activity_async(self) -> None:
        try:
            assert (
                self.activity_id is None
            ), "It is not possible to recreate an existing activity"

            self.logger.info(
                f"{self.correlation_id} Creating activity for model: {self.model_name}"
            )

            data = {
                "description": self.description,
                "tags": self.tags,
                "activity_status": ActivityStatus.PENDING.value,
            }
            
            data = ensure_message_and_title(data, self.model_name, self.description)
            
            params = {
                "topics": [self.model_name, "modelEditor"],
                "data": data,
                "level": "high", #TODO change to level when HTTP 409 is handled on platform differently
            }
            async with httpx.AsyncClient() as client:
                response = await self._request_with_retries(
                    "POST",
                    self.create_notification_endpoint,
                    json=params,
                )

                if response.status_code != 200:
                    response.raise_for_status()

                result = response.json() if response else None
                self.activity_id = result["id"]
                self.logger.info(
                    f"{self.correlation_id} Activity ID created: {self.activity_id}"
                )
                return result

        except Exception as e:
            self.logger.error(
                "%s Ignoring exception while creating activity: %s",
                self.correlation_id,
                e,
            )
            self.logger.info(f"{self.correlation_id}")

    create_activity = sync_wrapper(create_activity_async)

    async def update_activity_async(
        self,
        activity_status: ActivityStatus,
        last_message: Optional[str] = None,
        progress: Optional[int] = None,
        tags: Optional[str] = None,
    ):
        try: # TODO Fix this after 409 handling
            assert self.activity_id, "No activity_id. Check create_activity has been called"
            assert len(self.activity_id) == 36
        except Exception as e:
            self.logger.error(
                "%s Ignoring exception while updating activity: %s",
                self.correlation_id,
                e,
            )
            return None
        if self.done:
            raise ValueError("Cannot update a closed activity")

        if activity_status in [ActivityStatus.COMPLETED, ActivityStatus.FAILED]:
            self.done = True

        params = {
            "activity_status": activity_status.value,
            "progress": progress,
            "last_message": last_message,
        }

        if tags:
            params["tags"] = tags

        headers = self._get_api_header()
        endpoint = self.update_many_notification_data_fields_endpoint_template.format(
            notificationId=self.activity_id
        )

        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            for attempt in range(1, RETRY_COUNT + 1):
                try:
                    response = await client.patch(
                        endpoint,
                        headers=headers,
                        json=params,
                    )

                    if response.status_code == 200:
                        self.logger.info(
                            f"{self.correlation_id} Activity ID updated: {self.activity_id}"
                        )
                        return response.json() if response else None   # TODO Fix this after 409 handling

                    response.raise_for_status()

                except (
                    httpx.HTTPStatusError,
                    httpx.RequestError,
                    httpx.TimeoutException,
                ) as e:
                    self.logger.error(
                        f"{self.correlation_id} Attempt {attempt} failed with error: {str(e)}."
                    )
                    if attempt == RETRY_COUNT:
                        raise ConnectionError(
                            f"{self.correlation_id} Unable to update activity: {response.status_code} {response.text}"
                        ) from None
                    await asyncio.sleep(2 ** (attempt - 1))  # Exponential back-off

    update_activity = sync_wrapper(update_activity_async)


class AsyncFrogActivityHandler:
    """
    Async wrapper for Frog Model Activity notifications service

    Supports context manager style usage

    Can be used to create and update activities
    """

    def __init__(
        self,
        logger: Logger,
        correlation_id: str,
        model_name: str,
        description: str,
        tags: str,
        app_key: str,
        account: Optional[object] = {},
    ) -> None:
        self.activity_id = None
        self.model_notifications = ModelActivity(
            logger, correlation_id, model_name, description, tags, app_key, account
        )
        self.logger = logger
        self.correlation_id = correlation_id
        self.model_name = model_name
        self.description = description
        self.tags = tags
        self.done = False
        self.account = account

    async def __aenter__(self):
        try:
            activity_id = await self.create_activity_async()
            self.activity_id = activity_id
        except Exception as e:
            self.logger.debug(
                f"{self.correlation_id} Failed to create activity due to exception: {str(e)}"
            )
            raise e

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if not self.done:
                if exc_type is None and exc_val is None and exc_tb is None:
                    await self.update_activity_async(ActivityStatus.COMPLETED)
                else:
                    await self.update_activity_async(
                        ActivityStatus.FAILED, last_message=str(exc_val)
                    )
                    raise exc_val

                self.done = True

        except Exception as e:
            self.logger.debug(
                f"{self.correlation_id} Failed to close activity due to exception: {str(e)}"
            )
            raise e

        finally:
            await self.model_notifications.close()

    async def create_activity_async(self) -> str:
        try:
            self.logger.info(
                f"{self.correlation_id} Creating activity for model: {self.model_name}"
            )

            data = {
                "model_name": self.model_name,
                "description": self.description,
                "tags": self.tags,
            }
            data = ensure_message_and_title(data, self.model_name, self.description)
            response = await self.model_notifications.create_notification_async(
                topics=[self.model_name],
                createdBy="system",  # Or specify the actual user if available
                data=data,
            )

            activity_id = response.get("id")
            self.logger.info(
                f"{self.correlation_id} Activity ID created: {activity_id}"
            )
            return activity_id
        except Exception as e:
            self.logger.error(
                f"{self.correlation_id} Failed to create activity: {str(e)}"
            )
            raise

    async def update_activity_async(
        self,
        activity_status: ActivityStatus,
        last_message: Optional[str] = None,
        progress: Optional[int] = None,
        tags: Optional[str] = None,
    ):
        """
        Update an existing activity
        """
        try:
            if not self.activity_id:  # TODO Fix this after 409 handling
                self.logger.error(
                    "No activity_id. Check create_activity has been called"
                )
                return None

            self.logger.info(
                f"{self.correlation_id} Updating activity {self.activity_id} with status {activity_status}"
            )

            data = {
                "activity_status": activity_status.value,
                "progress": progress,
                "last_message": last_message,
            }

            if tags:
                data["tags"] = tags

            response = (
                await self.model_notifications.update_many_notification_data_async(
                    notificationId=self.activity_id, body_params=data
                )
            )

            self.logger.info(
                f"{self.correlation_id} Activity ID {self.activity_id} updated"
            )
            return response
        except Exception as e:
            self.logger.error(
                f"{self.correlation_id} Failed to update activity: {str(e)}"
            )
            return None

    update_activity = sync_wrapper(update_activity_async)
    create_activity = sync_wrapper(create_activity_async)


def activity_signal(
    logger: Logger,
    message: Dict[str, Any],
    app_key: str,
    signal_topic: Literal['TADPOLE CREATION', 'TABLE INSERT', 'REFRESH COUNT', 'REFETCH SCENARIO ERRORS', 'REFETCH SCENARIOS', 'REFETCH MAPS', 'CLEAR TABLE'],
    model_name: str = None,
    user_name: str = None,
    correlation_id: str = None,
    email: Optional[str] = None,
):

    assert logger, "Must supply Logger"
    assert model_name or user_name, "Must supply either model or user name"
    assert app_key, "Must supply a valid Optilogic app_key"
    assert type(message) == dict, "Service message must be a valid dictionary"
    assert signal_topic, "Must supply a valid signal topic"

    headers = {
        "x-app-key": app_key,
        "content-type": "application/json",
    }

    if correlation_id:
        headers["correlation-id"] = correlation_id

    if model_name:
        message["storageName"] = model_name
    elif user_name:
        message["username"] = user_name

    data = {
        "message": message,
        "messageID": str(uuid4()),
    }

    url = CF_ACTIVITY_URL or "https://service.optilogic.app/websocket/message" # Because of Andromeda

    attempt = 0
    max_attempts = RETRY_COUNT + 1

    logger.info(f"Sending activity signal: {message} to {signal_topic}")
    try:
        with httpx.Client() as client:
            while attempt < max_attempts:
                logger.debug(f"Attempt {attempt} of {max_attempts}")
                try:
                    attempt += 1
                    response = client.post(
                        url,
                        headers=headers,
                        json=data,
                        params={"topic": signal_topic},
                        timeout=TIMEOUT,
                    )
                    
                    # If response == 204 then DONE
                    if response.status_code == 204:
                        logger.info(f"{signal_topic} Activity signal sent successfully.")
                        return response.status_code

                    response.raise_for_status()

                except (httpx.HTTPStatusError, httpx.RequestError, httpx.TimeoutException) as e:
                    logger.error(f"Attempt {attempt} failed with error: {str(e)}.")
                    if attempt >= max_attempts:
                        raise  # Re-raise the exception after max attempts
                    time.sleep(2 ** (attempt - 1))  # Exponential back-off

    except Exception:  # pylint: disable=broad-except
        logger.exception(
            f"{correlation_id} Exception attempting to send activity signal, ignoring",
            stack_info=True,
            exc_info=True,
        )
