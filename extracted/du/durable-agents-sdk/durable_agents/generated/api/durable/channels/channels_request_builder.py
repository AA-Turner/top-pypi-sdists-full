from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .bindings.bindings_request_builder import BindingsRequestBuilder
    from .connectors.connectors_request_builder import ConnectorsRequestBuilder
    from .discord.discord_request_builder import DiscordRequestBuilder
    from .email.email_request_builder import EmailRequestBuilder
    from .endpoints.endpoints_request_builder import EndpointsRequestBuilder
    from .messaging.messaging_request_builder import MessagingRequestBuilder
    from .slack.slack_request_builder import SlackRequestBuilder
    from .teams.teams_request_builder import TeamsRequestBuilder
    from .whatsapp.whatsapp_request_builder import WhatsappRequestBuilder

class ChannelsRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/durable/channels
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new ChannelsRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/durable/channels", path_parameters)

    @property
    def bindings(self) -> BindingsRequestBuilder:
        """
        The bindings property
        """
        from .bindings.bindings_request_builder import BindingsRequestBuilder

        return BindingsRequestBuilder(self.request_adapter, self.path_parameters)

    @property
    def connectors(self) -> ConnectorsRequestBuilder:
        """
        The connectors property
        """
        from .connectors.connectors_request_builder import ConnectorsRequestBuilder

        return ConnectorsRequestBuilder(self.request_adapter, self.path_parameters)

    @property
    def discord(self) -> DiscordRequestBuilder:
        """
        The discord property
        """
        from .discord.discord_request_builder import DiscordRequestBuilder

        return DiscordRequestBuilder(self.request_adapter, self.path_parameters)

    @property
    def email(self) -> EmailRequestBuilder:
        """
        The email property
        """
        from .email.email_request_builder import EmailRequestBuilder

        return EmailRequestBuilder(self.request_adapter, self.path_parameters)

    @property
    def endpoints(self) -> EndpointsRequestBuilder:
        """
        The endpoints property
        """
        from .endpoints.endpoints_request_builder import EndpointsRequestBuilder

        return EndpointsRequestBuilder(self.request_adapter, self.path_parameters)

    @property
    def messaging(self) -> MessagingRequestBuilder:
        """
        The messaging property
        """
        from .messaging.messaging_request_builder import MessagingRequestBuilder

        return MessagingRequestBuilder(self.request_adapter, self.path_parameters)

    @property
    def slack(self) -> SlackRequestBuilder:
        """
        The slack property
        """
        from .slack.slack_request_builder import SlackRequestBuilder

        return SlackRequestBuilder(self.request_adapter, self.path_parameters)

    @property
    def teams(self) -> TeamsRequestBuilder:
        """
        The teams property
        """
        from .teams.teams_request_builder import TeamsRequestBuilder

        return TeamsRequestBuilder(self.request_adapter, self.path_parameters)

    @property
    def whatsapp(self) -> WhatsappRequestBuilder:
        """
        The whatsapp property
        """
        from .whatsapp.whatsapp_request_builder import WhatsappRequestBuilder

        return WhatsappRequestBuilder(self.request_adapter, self.path_parameters)


