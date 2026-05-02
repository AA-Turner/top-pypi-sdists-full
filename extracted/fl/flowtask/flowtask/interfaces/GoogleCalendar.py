from abc import ABC
from typing import List, Dict
import asyncio
from datetime import datetime, timedelta
import requests
from googleapiclient.discovery import build
from .GoogleClient import GoogleClient
from ..exceptions import ComponentError


class GoogleCalendarClient(GoogleClient, ABC):
    """
    Google Calendar Client for managing calendar events.
    """

    async def get_client(self):
        """Get the Google Calendar client, with caching."""
        if not hasattr(self, '_client'):
            self.service = await asyncio.to_thread(build, 'calendar', 'v3', credentials=self.credentials)
        return self.service

    async def create_event(self, calendar_id: str, event: Dict) -> Dict:
        """
        Create an event in the specified Google Calendar.

        Args:
            calendar_id (str): The ID of the calendar to add the event to.
            event (dict): The event details.

        Returns:
            dict: Details of the created event.
        """
        client = await self.get_client()
        created_event = await asyncio.to_thread(client.events().insert(calendarId=calendar_id, body=event).execute)
        print(f"Event created: {created_event.get('htmlLink')}")
        return created_event

    async def list_events(self, calendar_id: str, time_min: datetime, time_max: datetime, max_results: int = 10) -> List[Dict]:
        """
        List events in a specified time range.

        Args:
            calendar_id (str): The ID of the calendar to list events from.
            time_min (datetime): Start time to retrieve events.
            time_max (datetime): End time to retrieve events.
            max_results (int): Maximum number of events to retrieve (default is 10).

        Returns:
            list: List of events within the time range.
        """
        client = await self.get_client()
        events_result = await asyncio.to_thread(
            client.events().list,
            calendarId=calendar_id,
            timeMin=time_min.isoformat() + 'Z',
            timeMax=time_max.isoformat() + 'Z',
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime"
        )
        events = events_result.execute().get('items', [])
        return events

    async def update_event(self, calendar_id: str, event_id: str, updated_event: Dict) -> Dict:
        """
        Update an existing event in the calendar.

        Args:
            calendar_id (str): The ID of the calendar containing the event.
            event_id (str): The ID of the event to update.
            updated_event (dict): The updated event details.

        Returns:
            dict: Details of the updated event.
        """
        client = await self.get_client()
        event = await asyncio.to_thread(client.events().update, calendarId=calendar_id, eventId=event_id, body=updated_event)
        return event.execute()

    async def delete_event(self, calendar_id: str, event_id: str):
        """
        Delete an event from the specified calendar.

        Args:
            calendar_id (str): The ID of the calendar.
            event_id (str): The ID of the event to delete.
        """
        client = await self.get_client()
        await asyncio.to_thread(client.events().delete(calendarId=calendar_id, eventId=event_id).execute)
        print(f"Event {event_id} deleted.")

    async def get_event(self, calendar_id: str, event_id: str) -> Dict:
        """
        Retrieve details of a specific event.

        Args:
            calendar_id (str): The ID of the calendar.
            event_id (str): The ID of the event.

        Returns:
            dict: Details of the event.
        """
        client = await self.get_client()
        event = await asyncio.to_thread(client.events().get(calendarId=calendar_id, eventId=event_id).execute)
        return event

    async def setup_watch(self, calendar_id: str, webhook_url: str, channel_id: str) -> Dict:
        """
        Sets up a watch on the specified calendar to receive notifications when events are created, updated, or deleted.
        
        Args:
            calendar_id (str): The ID of the calendar to monitor.
            webhook_url (str): The URL of the webhook endpoint to receive notifications.
            channel_id (str): Unique ID for this notification channel.
        
        Returns:
            dict: The response from the Google Calendar API containing the channel information.
        """
        # Define request body for the watch request
        request_body = {
            "id": channel_id,  # Unique identifier for the channel
            "type": "webhook",
            "address": webhook_url,  # Webhook URL to receive notifications
            "params": {
                "ttl": "86400"  # Time-to-live in seconds, max 604800 (7 days)
            }
        }
        if not self.service:
            await self.get_client()
        
        try:
            # Set up the watch on the specified calendar
            response = self.service.events().watch(calendarId=calendar_id, body=request_body).execute()
            print("Watch setup successful:", response)
            return response
        except Exception as e:
            print(f"Error setting up watch: {e}")
            raise

    async def check_event_start_time(self, event_start_time: datetime):
        """
        Check if the current time has reached or passed the event's start time and trigger an action if so.
        
        Args:
            event_start_time (datetime): The start time of the event to check.
        
        """
        while True:
            now = datetime.utcnow()
            if now >= event_start_time:
                # Trigger the action when event time is reached
                print("Event time has been reached! Triggering action...")
                # You can add your custom action here
                break
            await asyncio.sleep(60)  # Check every minute

    async def create_subscription(self, webhook_url: str, client_state: str = "secret_string", expiration_hours: int = 1) -> dict:
        """
        Create a subscription to receive notifications when events are created, updated, or deleted in the calendar.

        Args:
            webhook_url (str): The webhook URL that will receive the notifications.
            client_state (str): A client secret string for verifying notifications.
            expiration_hours (int): Duration for which the subscription should be valid (maximum is 4230 minutes or 7 days).

        Returns:
            dict: The response from Microsoft Graph API with subscription details.
        """
        # Set up expiration for subscription (max 7 days)
        expiration_date = datetime.utcnow() + timedelta(hours=expiration_hours)
        expiration_datetime = expiration_date.isoformat() + "Z"

        # Define the subscription request body
        request_body = {
            "changeType": "created,updated,deleted",
            "notificationUrl": webhook_url,
            "resource": "me/events",  # Subscribe to the user's calendar events
            "expirationDateTime": expiration_datetime,
            "clientState": client_state
        }

        # Acquire access token for authentication
        access_token = self._access_token
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        # Send the subscription request to Microsoft Graph API
        url = "https://graph.microsoft.com/v1.0/subscriptions"
        response = requests.post(url, headers=headers, json=request_body)

        # Check for successful response
        if response.status_code == 201:
            subscription_info = response.json()
            print("Subscription created successfully:", subscription_info)
            return subscription_info
        else:
            error_message = response.json().get("error", {}).get("message", "Unknown error")
            print(f"Failed to create subscription: {error_message}")
            raise ComponentError(f"Failed to create subscription: {error_message}")
