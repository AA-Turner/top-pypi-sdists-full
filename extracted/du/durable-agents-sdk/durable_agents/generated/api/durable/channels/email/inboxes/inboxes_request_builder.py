from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.base_request_configuration import RequestConfiguration
from kiota_abstractions.default_query_parameters import QueryParameters
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.method import Method
from kiota_abstractions.request_adapter import RequestAdapter
from kiota_abstractions.request_information import RequestInformation
from kiota_abstractions.request_option import RequestOption
from kiota_abstractions.serialization import Parsable, ParsableFactory
from typing import Any, Optional, TYPE_CHECKING, Union
from warnings import warn

if TYPE_CHECKING:
    from ......models.email_inbox import EmailInbox
    from ......models.email_inbox_create import EmailInboxCreate
    from ......models.email_inbox_list import EmailInboxList
    from ......models.error_envelope import ErrorEnvelope
    from .item.with_inbox_item_request_builder import WithInboxItemRequestBuilder

class InboxesRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/durable/channels/email/inboxes
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new InboxesRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/durable/channels/email/inboxes{?cursor*,limit*}", path_parameters)
    
    def by_inbox(self,inbox: str) -> WithInboxItemRequestBuilder:
        """
        Gets an item from the durable_agents.generated.api.durable.channels.email.inboxes.item collection
        param inbox: Unique identifier of the item
        Returns: WithInboxItemRequestBuilder
        """
        if inbox is None:
            raise TypeError("inbox cannot be null.")
        from .item.with_inbox_item_request_builder import WithInboxItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["inbox"] = inbox
        return WithInboxItemRequestBuilder(self.request_adapter, url_tpl_params)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[InboxesRequestBuilderGetQueryParameters]] = None) -> Optional[EmailInboxList]:
        """
        List AgentMail inboxes.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[EmailInboxList]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        from ......models.error_envelope import ErrorEnvelope

        error_mapping: dict[str, type[ParsableFactory]] = {
            "XXX": ErrorEnvelope,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ......models.email_inbox_list import EmailInboxList

        return await self.request_adapter.send_async(request_info, EmailInboxList, error_mapping)
    
    async def post(self,body: EmailInboxCreate, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[EmailInbox]:
        """
        Provision an AgentMail inbox.
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[EmailInbox]
        """
        if body is None:
            raise TypeError("body cannot be null.")
        request_info = self.to_post_request_information(
            body, request_configuration
        )
        from ......models.error_envelope import ErrorEnvelope

        error_mapping: dict[str, type[ParsableFactory]] = {
            "XXX": ErrorEnvelope,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ......models.email_inbox import EmailInbox

        return await self.request_adapter.send_async(request_info, EmailInbox, error_mapping)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[InboxesRequestBuilderGetQueryParameters]] = None) -> RequestInformation:
        """
        List AgentMail inboxes.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def to_post_request_information(self,body: EmailInboxCreate, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        Provision an AgentMail inbox.
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        if body is None:
            raise TypeError("body cannot be null.")
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        request_info.set_content_from_parsable(self.request_adapter, "application/json", body)
        return request_info
    
    def with_url(self,raw_url: str) -> InboxesRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: InboxesRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return InboxesRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class InboxesRequestBuilderGetQueryParameters():
        """
        List AgentMail inboxes.
        """
        cursor: Optional[str] = None

        limit: Optional[int] = None

    
    @dataclass
    class InboxesRequestBuilderGetRequestConfiguration(RequestConfiguration[InboxesRequestBuilderGetQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    
    @dataclass
    class InboxesRequestBuilderPostRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

