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
    from ....models.error_envelope import ErrorEnvelope
    from ....models.run_list import RunList
    from ....models.run_status import RunStatus
    from .item.with_run_item_request_builder import WithRunItemRequestBuilder
    from .search.search_request_builder import SearchRequestBuilder

class RunsRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/durable/runs
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new RunsRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/durable/runs{?agent*,cursor*,limit*,status*}", path_parameters)
    
    def by_run(self,run: str) -> WithRunItemRequestBuilder:
        """
        Gets an item from the durable_agents.generated.api.durable.runs.item collection
        param run: Unique identifier of the item
        Returns: WithRunItemRequestBuilder
        """
        if run is None:
            raise TypeError("run cannot be null.")
        from .item.with_run_item_request_builder import WithRunItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["run"] = run
        return WithRunItemRequestBuilder(self.request_adapter, url_tpl_params)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[RunsRequestBuilderGetQueryParameters]] = None) -> Optional[RunList]:
        """
        Lists recent run records used for execution state and run-control workflows. Recent run records are retained for about 30 days after their last update.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[RunList]
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
        from ....models.run_list import RunList

        return await self.request_adapter.send_async(request_info, RunList, error_mapping)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[RunsRequestBuilderGetQueryParameters]] = None) -> RequestInformation:
        """
        Lists recent run records used for execution state and run-control workflows. Recent run records are retained for about 30 days after their last update.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> RunsRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: RunsRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return RunsRequestBuilder(self.request_adapter, raw_url)
    
    @property
    def search(self) -> SearchRequestBuilder:
        """
        The search property
        """
        from .search.search_request_builder import SearchRequestBuilder

        return SearchRequestBuilder(self.request_adapter, self.path_parameters)
    
    @dataclass
    class RunsRequestBuilderGetQueryParameters():
        """
        Lists recent run records used for execution state and run-control workflows. Recent run records are retained for about 30 days after their last update.
        """
        agent: Optional[str] = None

        cursor: Optional[str] = None

        limit: Optional[int] = None

        status: Optional[RunStatus] = None

    
    @dataclass
    class RunsRequestBuilderGetRequestConfiguration(RequestConfiguration[RunsRequestBuilderGetQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

