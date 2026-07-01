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
    from ....models.api_key_create import ApiKeyCreate
    from ....models.api_key_list import ApiKeyList
    from ....models.error_envelope import ErrorEnvelope
    from ....models.key_create_response import KeyCreateResponse
    from .claim.claim_request_builder import ClaimRequestBuilder
    from .item.with_key_item_request_builder import WithKeyItemRequestBuilder

class KeysRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/durable/keys
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new KeysRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/durable/keys", path_parameters)
    
    def by_key(self,key: str) -> WithKeyItemRequestBuilder:
        """
        Gets an item from the durable_agents.generated.api.durable.keys.item collection
        param key: Unique identifier of the item
        Returns: WithKeyItemRequestBuilder
        """
        if key is None:
            raise TypeError("key cannot be null.")
        from .item.with_key_item_request_builder import WithKeyItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["key"] = key
        return WithKeyItemRequestBuilder(self.request_adapter, url_tpl_params)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[ApiKeyList]:
        """
        List API key metadata for the current workspace member.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ApiKeyList]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        from ....models.error_envelope import ErrorEnvelope

        error_mapping: dict[str, type[ParsableFactory]] = {
            "XXX": ErrorEnvelope,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ....models.api_key_list import ApiKeyList

        return await self.request_adapter.send_async(request_info, ApiKeyList, error_mapping)
    
    async def post(self,body: ApiKeyCreate, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[KeyCreateResponse]:
        """
        Create an API key.
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[KeyCreateResponse]
        """
        if body is None:
            raise TypeError("body cannot be null.")
        request_info = self.to_post_request_information(
            body, request_configuration
        )
        from ....models.error_envelope import ErrorEnvelope

        error_mapping: dict[str, type[ParsableFactory]] = {
            "XXX": ErrorEnvelope,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ....models.key_create_response import KeyCreateResponse

        return await self.request_adapter.send_async(request_info, KeyCreateResponse, error_mapping)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        List API key metadata for the current workspace member.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def to_post_request_information(self,body: ApiKeyCreate, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        Create an API key.
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
    
    def with_url(self,raw_url: str) -> KeysRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: KeysRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return KeysRequestBuilder(self.request_adapter, raw_url)
    
    @property
    def claim(self) -> ClaimRequestBuilder:
        """
        The claim property
        """
        from .claim.claim_request_builder import ClaimRequestBuilder

        return ClaimRequestBuilder(self.request_adapter, self.path_parameters)
    
    @dataclass
    class KeysRequestBuilderGetRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    
    @dataclass
    class KeysRequestBuilderPostRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

