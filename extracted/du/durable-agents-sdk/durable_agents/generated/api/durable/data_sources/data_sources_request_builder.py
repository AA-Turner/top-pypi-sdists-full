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
    from ....models.data_source_create import DataSourceCreate
    from ....models.data_source_create_result import DataSourceCreateResult
    from ....models.data_source_list import DataSourceList
    from ....models.data_source_provider import DataSourceProvider
    from ....models.data_source_status import DataSourceStatus
    from ....models.data_source_type import DataSourceType
    from ....models.error_envelope import ErrorEnvelope
    from .discover.discover_request_builder import DiscoverRequestBuilder
    from .item.with_source_item_request_builder import WithSourceItemRequestBuilder

class DataSourcesRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/durable/data-sources
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new DataSourcesRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/durable/data-sources{?account*,cursor*,limit*,provider*,search*,status*,type*}", path_parameters)
    
    def by_source(self,source: str) -> WithSourceItemRequestBuilder:
        """
        Gets an item from the durable_agents.generated.api.durable.dataSources.item collection
        param source: Unique identifier of the item
        Returns: WithSourceItemRequestBuilder
        """
        if source is None:
            raise TypeError("source cannot be null.")
        from .item.with_source_item_request_builder import WithSourceItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["source"] = source
        return WithSourceItemRequestBuilder(self.request_adapter, url_tpl_params)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[DataSourcesRequestBuilderGetQueryParameters]] = None) -> Optional[DataSourceList]:
        """
        List Durable data sources.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[DataSourceList]
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
        from ....models.data_source_list import DataSourceList

        return await self.request_adapter.send_async(request_info, DataSourceList, error_mapping)
    
    async def post(self,body: DataSourceCreate, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[DataSourceCreateResult]:
        """
        Create a Durable data source.
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[DataSourceCreateResult]
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
        from ....models.data_source_create_result import DataSourceCreateResult

        return await self.request_adapter.send_async(request_info, DataSourceCreateResult, error_mapping)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[DataSourcesRequestBuilderGetQueryParameters]] = None) -> RequestInformation:
        """
        List Durable data sources.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def to_post_request_information(self,body: DataSourceCreate, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        Create a Durable data source.
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
    
    def with_url(self,raw_url: str) -> DataSourcesRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: DataSourcesRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return DataSourcesRequestBuilder(self.request_adapter, raw_url)
    
    @property
    def discover(self) -> DiscoverRequestBuilder:
        """
        The discover property
        """
        from .discover.discover_request_builder import DiscoverRequestBuilder

        return DiscoverRequestBuilder(self.request_adapter, self.path_parameters)
    
    @dataclass
    class DataSourcesRequestBuilderGetQueryParameters():
        """
        List Durable data sources.
        """
        account: Optional[str] = None

        cursor: Optional[str] = None

        limit: Optional[int] = None

        provider: Optional[DataSourceProvider] = None

        search: Optional[str] = None

        status: Optional[DataSourceStatus] = None

        type: Optional[DataSourceType] = None

    
    @dataclass
    class DataSourcesRequestBuilderGetRequestConfiguration(RequestConfiguration[DataSourcesRequestBuilderGetQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    
    @dataclass
    class DataSourcesRequestBuilderPostRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

