"""This module contains the FabricBusinessEventsClient class for publishing business events."""


import logging
import typing
import uuid

from azure.core.messaging import CloudEvent
from azure.eventgrid import EventGridPublisherClient

from fabric.functions.udf_exception import UserDataFunctionInternalError


# flake8: noqa: I005
class FabricBusinessEventsClient(EventGridPublisherClient):
    """Client for publishing Fabric Business Events.
    
    Extends EventGridPublisherClient with a convenience PublishEvent() method.

    A User Data Function with a parameter of this type must be decorated with
    :meth:`fabric.functions.UserDataFunctions.connection` (see the example under `Remarks`).

    .. remarks::
        To use this class and have Fabric make the proper connections to Business Events, you must:
        * Add a data connection in the Connections tab of your User Data Functions on the portal.
        * Add a parameter to your User Data Function with the type 'FabricBusinessEventsClient'.
        * Add the decorator `connection` to your User Data Function that references the parameter
        and the alias of the data connection you made.

        .. code-block:: python
                import fabric.functions as fn

                udf = fn.UserDataFunctions()

                @udf.connection("<Business Events alias>", "<argName>")
                @udf.function()
                def my_function(<argName>: fn.FabricBusinessEventsClient) -> None:
                    event_data = {
                        "orderId": "12345",
                        "status": "shipped",
                        "orderDeliverAddress": "123 Main St"
                    }
                    <argName>.PublishEvent(type="order.shipped", event_data=event_data, data_version="v1")
    """

    __APPSETTINGS_PATH = "beendpoint"

    def __init__(self, *, alias_name=None, endpoints, **kwargs):
        """Initialize the client.
        
        Args:
            alias_name: The alias name for this connection
            endpoints: FabricItem-style endpoints dict containing beendpoint with
                ConnectionString and AccessToken
        
        Keyword Args:
            udf_rid: UDF resource ID for building Cloud Event source
            schemaset_uri: Schemaset URI base for building dataschema
            <alias>_schemaset_rid: Schema set resource ID for this alias
            allowedEvents: List of allowed event types (for future validation)
        """
        from fabric.internal.custom_token_credential import CustomTokenCredential

        be_info = endpoints.get(self.__APPSETTINGS_PATH, {})
        endpoint = be_info.get("ConnectionString")
        if not endpoint:
            raise UserDataFunctionInternalError("Business Events endpoint URL is not set in endpoints")

        access_token = be_info.get("AccessToken")
        if not access_token:
            raise UserDataFunctionInternalError(f"AccessToken is not set in endpoints['{self.__APPSETTINGS_PATH}']")

        credential = CustomTokenCredential(access_token)

        super().__init__(endpoint=endpoint, credential=credential)
        self._alias_name = alias_name
        self._endpoints = endpoints
        self._udf_rid = kwargs.get('udf_rid')
        # Placeholder default - this value will eventually change once schemaset_uri is provided by the service
        self._schemaset_uri = kwargs.get('schemaset_uri', 'https://api.fabric.microsoft.com')
        self._schemaset_rid = kwargs.get(f'{alias_name}_schemaset_rid') if alias_name else None
        self._allowed_events = kwargs.get('allowedEvents')  # For future use

    @property
    def alias_name(self) -> typing.Optional[str]:
        return self._alias_name

    @property
    def endpoints(self) -> typing.Dict[str, typing.Dict[str, str]]:
        return self._endpoints

    def PublishEvent(self, type: str, event_data: typing.Union[typing.Dict[str, typing.Any], typing.List[typing.Dict[str, typing.Any]]], data_version: str = "v1") -> None:
        """Publishes a CloudEvent with the provided event data.

        This is a convenience method that creates a CloudEvent and sends it in one call.

        Args:
            type: The type of the event (REQUIRED)
            event_data: A dictionary or list of dictionaries containing the event data to be sent (REQUIRED)
            data_version: Version ID for building dataschema (defaults to "v1")

        Example:
            .. code-block:: python

                # Single event
                event_data = {
                    "orderId": "12345",
                    "status": "shipped",
                    "orderDeliverAddress": "123 Main St"
                }

                # or multiple events
                event_data = [
                    {"orderId": "12345", "status": "shipped"},
                    {"orderId": "67890", "status": "shipped"}
                ]

                client.PublishEvent(
                    type="order.shipped",
                    event_data=event_data,
                    data_version="v1"
                )
        """
        # Validate required internal parameters
        if self._udf_rid is None:
            raise UserDataFunctionInternalError("'udf_rid' is required for building Cloud Event source")

        if self._schemaset_rid is None:
            raise UserDataFunctionInternalError(f"'{self._alias_name}_schemaset_rid' is required for building dataschema")

        # Remove trailing slash from schemaset_uri and schemaset_rid if present
        schemaset_uri_base = self._schemaset_uri.rstrip('/')
        schemaset_base = self._schemaset_rid.rstrip('/')

        # Build the CloudEvent type path:
        # /workspaces/<wid>/eventschemasests/<item_id>/eventTypes/<type>
        cloud_event_type = f"{schemaset_base}/eventTypes/{type}"

        # Build dataschema:
        # <schemaset_uri>/workspaces/<wid>/eventschemasests/<item_id>/schemas/<type>/versions/<version>
        dataschema = f"{schemaset_uri_base}{schemaset_base}/schemas/{type}/versions/{data_version}"

        # Build extensions dictionary
        extensions = {"dataversion": data_version}

        # Normalize event_data to a list for consistent processing
        data_items = event_data if isinstance(event_data, list) else [event_data]

        # Create CloudEvents for each data item
        events = []
        for data_item in data_items:
            event_id = str(uuid.uuid4())
            event = CloudEvent(
                source=self._udf_rid,
                type=cloud_event_type,
                data=data_item,
                id=event_id,
                dataschema=dataschema,
                extensions=extensions
            )
            events.append(event)

        # Send the event(s) using the parent class's send method
        self.send(events)

        for event in events:
            logging.info("Published business event with eventId: %s", event.id)