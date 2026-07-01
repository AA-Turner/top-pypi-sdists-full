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
    from .....models.error_envelope import ErrorEnvelope
    from .....models.run_search_result_list import RunSearchResultList
    from .get_search_type_query_parameter_type import GetSearch_typeQueryParameterType

class SearchRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/durable/runs/search
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new SearchRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/durable/runs/search?query={query}{&agent*,cursor*,in_last*,limit*,relevance_threshold*,search_type*}", path_parameters)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[SearchRequestBuilderGetQueryParameters]] = None) -> Optional[RunSearchResultList]:
        """
        Search completed agent run memories by query. Completed run memories are retained until deleted and may outlive the recent run record used by execution-state and run-control endpoints.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[RunSearchResultList]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        from .....models.error_envelope import ErrorEnvelope

        error_mapping: dict[str, type[ParsableFactory]] = {
            "XXX": ErrorEnvelope,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .....models.run_search_result_list import RunSearchResultList

        return await self.request_adapter.send_async(request_info, RunSearchResultList, error_mapping)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[SearchRequestBuilderGetQueryParameters]] = None) -> RequestInformation:
        """
        Search completed agent run memories by query. Completed run memories are retained until deleted and may outlive the recent run record used by execution-state and run-control endpoints.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> SearchRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: SearchRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return SearchRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class SearchRequestBuilderGetQueryParameters():
        """
        Search completed agent run memories by query. Completed run memories are retained until deleted and may outlive the recent run record used by execution-state and run-control endpoints.
        """
        # Optional Graphlit agent GUID filter. The CLI also accepts an exact agent name and resolves it before calling this API.
        agent: Optional[str] = None

        cursor: Optional[str] = None

        # Filter by run-memory creation time using a duration such as `30d`, `1w`, `P30D`, or `PT24H`.
        in_last: Optional[str] = None

        limit: Optional[int] = None

        # Search text for matching agent runs.
        query: Optional[str] = None

        # Minimum relevance score from 0 to 1 for hybrid/vector search.
        relevance_threshold: Optional[float] = None

        # Search mode. Defaults to hybrid.
        search_type: Optional[GetSearch_typeQueryParameterType] = None

    
    @dataclass
    class SearchRequestBuilderGetRequestConfiguration(RequestConfiguration[SearchRequestBuilderGetQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

