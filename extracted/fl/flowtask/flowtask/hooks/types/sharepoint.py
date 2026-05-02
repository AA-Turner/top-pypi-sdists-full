from typing import Any, Optional
from collections.abc import Callable
import asyncio
import datetime
from urllib.parse import quote
import aiohttp
from aiohttp import web
from azure.identity.aio import ClientSecretCredential
from msgraph import GraphServiceClient, GraphRequestAdapter
from msgraph.generated.models.subscription import Subscription
from kiota_authentication_azure.azure_identity_authentication_provider import AzureIdentityAuthenticationProvider
from navconfig.logging import logging
from .http import HTTPHook
from ...conf import (
    SHAREPOINT_APP_ID,
    SHAREPOINT_APP_SECRET,
    SHAREPOINT_TENANT_ID,
    SHAREPOINT_DEFAULT_HOST,
    SHAREPOINT_TENANT_NAME
)

logging.getLogger(name='azure.identity.aio').setLevel(logging.WARNING)
logging.getLogger(name='azure.core').setLevel(logging.WARNING)

DEFAULT_SCOPES = ["https://graph.microsoft.com/.default"]


class SharePointTrigger(HTTPHook):
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
        self.methods: list = ['POST']
        super().__init__(*args, **kwargs)
        self.tenant_id = tenant_id or SHAREPOINT_TENANT_ID
        self._tenant_name = kwargs.get('tenant', SHAREPOINT_TENANT_NAME)
        self.client_id = client_id or SHAREPOINT_APP_ID
        self.client_secret = client_secret or SHAREPOINT_APP_SECRET
        self.site_name: str = kwargs.get('site_name')
        self._host: str = kwargs.get('host', SHAREPOINT_DEFAULT_HOST)
        self.folder_path: str = kwargs.get('folder_path')
        self.site_id: Optional[str] = None
        self.resource = resource
        self.webhook_url = webhook_url
        self.client_state: str = kwargs.get('client_state', 'flowtask_state')
        self.changetype: str = kwargs.get('changetype', 'updated')
        self.access_token = None
        self.subscription_id = None
        self._msapp: Callable = None
        self._graph_client: Callable = None
        self.renewal_task = None
        self.renewal_interval = 3600 * 24  # Renew every 24 hours
        self.scopes = kwargs.get('scopes', DEFAULT_SCOPES)

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
        self._client = ClientSecretCredential(
            tenant_id=self.tenant_id,
            client_id=self.client_id,
            client_secret=self.client_secret
        )
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
        expiration_datetime = (datetime.datetime.utcnow() + datetime.timedelta(minutes=4230)).isoformat() + 'Z'
        subscription_data = Subscription(
            change_type=self.changetype,
            notification_url=self.webhook_url,
            resource=self.resource,
            expiration_date_time=expiration_datetime,
            client_state=self.client_state,
        )
        # subscription_data.include_resource_data = True
        self._logger.info(
            f"Using webhook URL: {self.webhook_url}"
        )
        self._logger.info(f"Subscription data: {subscription_data}")
        response = await self._graph_client.subscriptions.post(subscription_data)
        if response:
            self.subscription_id = response.id
        else:
            self._logger.error("Failed to create subscription")
            raise Exception(
                "Failed to create Sharepoint subscription"
            )

    async def delete_subscription(self):
        if not self.subscription_id:
            return
        if not self._graph_client:
            await self.authenticate()
        result = await self._graph_client.subscriptions.by_subscription_id(
            self.subscription_id
        ).delete()
        if result is None:
            self._logger.info("Subscription deleted")
        else:
            self._logger.error("Failed to delete subscription")

    async def renew_subscription(self):
        while True:
            await asyncio.sleep(self.renewal_interval)
            if not self.subscription_id:
                continue
            if not self._graph_client:
                await self.authenticate()
            expiration_datetime = (datetime.datetime.utcnow() + datetime.timedelta(minutes=4230)).isoformat() + 'Z'
            subscription = Subscription()
            subscription.expiration_date_time = expiration_datetime
            response = await self._graph_client.subscriptions.by_subscription_id(
                self.subscription_id
            ).patch(subscription)
            if response:
                self._logger.info("Subscription renewed")
            else:
                self._logger.error("Failed to renew subscription")

    async def on_startup(self, app):
        self._logger.info("Starting SharePointTrigger")
        asyncio.create_task(self._subscription_creation())

    async def _subscription_creation(self):
        # delaying startup for 5 sconds
        await asyncio.sleep(5)
        if not self.resource:
            await self.get_site_id()
            self.build_resource()
        await self.create_subscription()
        self.renewal_task = asyncio.create_task(
            self.renew_subscription()
        )

    async def on_shutdown(self, app):
        self._logger.info("Shutting down SharePointTrigger")
        if self.renewal_task:
            self.renewal_task.cancel()
        await self.delete_subscription()

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
            self._logger.info(
                f"Received notification for resource: {resource}"
            )
            # Fetch details about the changed file
            file_details = await self.get_resource_details(resource)
            # Run actions with the file details
            await self.run_actions(file_details=file_details)

    async def get_resource_details(self, resource):
        client = self.get_client()
        # Get the access token
        token = await client.get_token("https://graph.microsoft.com/.default")
        access_token = token.token

        # Build the full URL
        resource_url = f"https://graph.microsoft.com/v1.0/{resource.lstrip('/')}"

        # Log the resource URL for debugging
        self._logger.info(f"Fetching resource details from URL: {resource_url}")

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json'
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(resource_url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    error_text = await response.text()
                    self._logger.error(f"Failed to get resource details: {error_text}")
                    return {}

    async def get_site_id(self):
        if not self._graph_client:
            await self.authenticate()
        # Ensure site_name does not start with a slash
        site_name = self.site_name.lstrip('/')

        # Construct the site URL
        site_request_url = f"https://graph.microsoft.com/v1.0/sites/{self._tenant_name}.sharepoint.com:/sites/{site_name}"  # noqa

        # Log the constructed URL for debugging
        self._logger.info(
            f"Site request URL: {site_request_url}"
        )

        # Use `with_url` with the relative path, not the full URL
        site_request_builder = self._graph_client.sites.with_url(site_request_url)

        # Fetch the site information
        site = await site_request_builder.get()
        if site:
            self.site_id = site.additional_data.get('id').split(',')[1]
            self._logger.info(
                f"Site ID obtained: {self.site_id}"
            )
        else:
            self._logger.error(
                f"Failed to get site ID for site: {self.site_name}"
            )
            raise Exception(
                f"Failed to get site ID for site: {self.site_name}"
            )

    def build_resource(self):
        if not self.site_id:
            raise Exception("Site ID not available. Cannot build resource URL.")
        folder_path = self.folder_path.strip('/')
        encoded_folder_path = quote(folder_path)
        # /{encoded_folder_path}:/children
        self.resource = f"/sites/{self.site_id}/drive/root"
        self._logger.info(
            f"Resource URL built: {self.resource}"
        )
