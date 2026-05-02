import asyncio
import datetime
from typing import Any, Optional
from aiohttp import web
from azure.identity.aio import ClientSecretCredential
from msgraph import GraphRequestAdapter, GraphServiceClient
from msgraph.generated.models.subscription import Subscription
from msgraph.generated.models.message import Message
from kiota_authentication_azure.azure_identity_authentication_provider import AzureIdentityAuthenticationProvider
from navconfig.logging import logging
from .http import HTTPHook
from ...conf import (
    SHAREPOINT_APP_ID,
    SHAREPOINT_APP_SECRET,
    SHAREPOINT_TENANT_ID,
    SHAREPOINT_TENANT_NAME
)

logging.getLogger(name='azure.identity.aio').setLevel(logging.WARNING)
logging.getLogger(name='azure.core').setLevel(logging.WARNING)

DEFAULT_SCOPES = ["https://graph.microsoft.com/.default"]


class EmailTrigger(HTTPHook):

    def __init__(
        self,
        *args,
        webhook_url: str,
        tenant_id: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        resource: Optional[str] = None,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.tenant_id = tenant_id or SHAREPOINT_TENANT_ID
        self._tenant_name = kwargs.get('tenant', SHAREPOINT_TENANT_NAME)
        self.client_id = client_id or SHAREPOINT_APP_ID
        self.client_secret = client_secret or SHAREPOINT_APP_SECRET
        self.webhook_url = webhook_url
        self.client_state: str = kwargs.get('client_state', 'flowtask_state')
        self.changetype: str = kwargs.get('changetype', 'created')
        self.subscription_id = None
        self._graph_client: GraphServiceClient = None
        self._request_adapter: GraphRequestAdapter = None
        self.renewal_task = None
        self.renewal_interval = 3600 * 23  # Renew every 23 hours

    def get_client(self):
        return ClientSecretCredential(
            tenant_id=self.tenant_id,
            client_id=self.client_id,
            client_secret=self.client_secret
        )

    def get_graph_client(
        self,
        client: Any,
        scopes: Optional[list] = None
    ):
        if not scopes:
            scopes = self.scopes
        return GraphServiceClient(credentials=client, scopes=scopes)

    async def authenticate(self):
        """
        Authenticates the client with Azure AD and initializes the Graph client.

        This method creates a ClientSecretCredential using the tenant ID, client ID,
        and client secret. It then sets up an AzureIdentityAuthenticationProvider,
        initializes a GraphRequestAdapter, and finally creates a GraphServiceClient.

        The method doesn't take any parameters as it uses the instance variables
        for authentication details.

        Returns:
            None
        """
        self._client = self.get_client()
        auth_provider = AzureIdentityAuthenticationProvider(self._client)
        self._request_adapter = GraphRequestAdapter(auth_provider)
        self._graph_client = GraphServiceClient(
            credentials=self._client,
            scopes=self.scopes,
            request_adapter=self._request_adapter
        )

    async def create_subscription(self):
        if not self._graph_client:
            await self.authenticate()

        expiration_datetime = (datetime.datetime.utcnow() + datetime.timedelta(hours=23)).isoformat() + 'Z'
        subscription = Subscription(
            change_type=self.changetype,
            notification_url=self.webhook_url,
            resource="me/mailFolders('Inbox')/messages",
            expiration_date_time=expiration_datetime,
            client_state=self.client_state,
            latest_supported_tls_version="v1_2",
        )

        result = await self._graph_client.subscriptions.post(body=subscription)
        if result:
            self.subscription_id = result.id
            self._logger.info(f"Subscription created with ID: {self.subscription_id}")

        else:
            self._logger.error("Failed to create subscription")
            raise Exception("Failed to create email subscription")

    async def delete_subscription(self):
        if not self.subscription_id:
            return
        if not self._graph_client:
            await self.authenticate()

        await self._graph_client.subscriptions.by_subscription_id(self.subscription_id).delete()
        self._logger.info("Subscription deleted")

    async def renew_subscription(self):
        while True:
            await asyncio.sleep(self.renewal_interval)
            if not self.subscription_id:
                continue
            if not self._graph_client:
                await self.authenticate()

            expiration_datetime = (datetime.datetime.utcnow() + datetime.timedelta(hours=23)).isoformat() + 'Z'
            subscription = Subscription(
                expiration_date_time=expiration_datetime
            )
            await self._graph_client.subscriptions.by_subscription_id(self.subscription_id).patch(body=subscription)
            self._logger.info("Subscription renewed")

    async def post(self, request: web.Request):
        self._logger.info("Received POST request")
        # Handle validation token
        validation_token = request.query.get('validationToken')
        if validation_token:
            self._logger.info(f"Received validation token: {validation_token}")
            return web.Response(text=validation_token, status=200)

        # Handle notifications
        try:
            data = await request.json()
            self._logger.info(f"Received notification data: {data}")
        except Exception as e:
            self._logger.error(f"Failed to parse request JSON: {e}")
            return web.Response(status=400)

        # Verify clientState
        if self.client_state:
            client_state = data.get('value', [{}])[0].get('clientState')
            if client_state != self.client_state:
                self._logger.warning("Invalid clientState in notification")
                return web.Response(status=202)

        # Process notifications
        await self.process_notifications(data)
        return web.Response(status=202)

    async def process_notifications(self, data):
        notifications = data.get('value', [])
        for notification in notifications:
            resource = notification.get('resource')
            self._logger.info(f"Received notification for resource: {resource}")
            message_details = await self.get_message_details(resource)
            # Run actions with the message details
            await self.run_actions(message_details=message_details)

    async def get_message_details(self, resource):
        if not self._graph_client:
            await self.authenticate()

        # The resource should be something like "me/messages/{message-id}"
        # Extract the message ID
        parts = resource.split('/')
        if 'messages' in parts:
            message_index = parts.index('messages')
            message_id = parts[message_index + 1]

            message = await self._graph_client.me.messages.by_message_id(message_id).get()
            return message.serialize()
        else:
            self._logger.error(
                f"Cannot extract message ID from resource: {resource}"
            )
            return {}

    async def on_startup(self, app):
        self._logger.info("Starting EmailTrigger")
        asyncio.create_task(self._subscription_creation())

    async def _subscription_creation(self):
        await asyncio.sleep(5)
        await self.create_subscription()
        self.renewal_task = asyncio.create_task(self.renew_subscription())

    async def on_shutdown(self, app):
        self._logger.info("Shutting down EmailTrigger")
        if self.renewal_task:
            self.renewal_task.cancel()
        await self.delete_subscription()
