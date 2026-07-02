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
    from ......models.error_envelope import ErrorEnvelope
    from ......models.voice_number import VoiceNumber
    from ......models.voice_number_create_request import VoiceNumberCreateRequest
    from ......models.voice_number_list import VoiceNumberList
    from .import_.import_request_builder import ImportRequestBuilder
    from .item.with_phone_item_request_builder import WithPhoneItemRequestBuilder
    from .search.search_request_builder import SearchRequestBuilder

class NumbersRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/durable/channels/voice/numbers
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new NumbersRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/durable/channels/voice/numbers", path_parameters)
    
    def by_phone(self,phone: str) -> WithPhoneItemRequestBuilder:
        """
        Gets an item from the durable_agents.generated.api.durable.channels.voice.numbers.item collection
        param phone: Unique identifier of the item
        Returns: WithPhoneItemRequestBuilder
        """
        if phone is None:
            raise TypeError("phone cannot be null.")
        from .item.with_phone_item_request_builder import WithPhoneItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["phone"] = phone
        return WithPhoneItemRequestBuilder(self.request_adapter, url_tpl_params)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[VoiceNumberList]:
        """
        List voice phone numbers.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[VoiceNumberList]
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
        from ......models.voice_number_list import VoiceNumberList

        return await self.request_adapter.send_async(request_info, VoiceNumberList, error_mapping)
    
    async def post(self,body: VoiceNumberCreateRequest, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[VoiceNumber]:
        """
        Create a managed voice phone number.
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[VoiceNumber]
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
        from ......models.voice_number import VoiceNumber

        return await self.request_adapter.send_async(request_info, VoiceNumber, error_mapping)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        List voice phone numbers.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def to_post_request_information(self,body: VoiceNumberCreateRequest, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        Create a managed voice phone number.
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
    
    def with_url(self,raw_url: str) -> NumbersRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: NumbersRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return NumbersRequestBuilder(self.request_adapter, raw_url)
    
    @property
    def import_(self) -> ImportRequestBuilder:
        """
        The import property
        """
        from .import_.import_request_builder import ImportRequestBuilder

        return ImportRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def search(self) -> SearchRequestBuilder:
        """
        The search property
        """
        from .search.search_request_builder import SearchRequestBuilder

        return SearchRequestBuilder(self.request_adapter, self.path_parameters)
    
    @dataclass
    class NumbersRequestBuilderGetRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    
    @dataclass
    class NumbersRequestBuilderPostRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

