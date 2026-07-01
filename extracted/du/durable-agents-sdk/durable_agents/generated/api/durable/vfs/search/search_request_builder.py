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
    from .....models.vfs_search_match_list import VfsSearchMatchList
    from .get_date_mode_query_parameter_type import GetDate_modeQueryParameterType
    from .get_search_type_query_parameter_type import GetSearch_typeQueryParameterType

class SearchRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/durable/vfs/search
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new SearchRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/durable/vfs/search?pattern={pattern}{&collection*,cursor*,date_mode*,ignore_case*,in_last*,kind*,label*,limit*,mention*,path*,search_type*,source*}", path_parameters)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[SearchRequestBuilderGetQueryParameters]] = None) -> Optional[VfsSearchMatchList]:
        """
        Search Library virtual filesystem text content.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[VfsSearchMatchList]
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
        from .....models.vfs_search_match_list import VfsSearchMatchList

        return await self.request_adapter.send_async(request_info, VfsSearchMatchList, error_mapping)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[SearchRequestBuilderGetQueryParameters]] = None) -> RequestInformation:
        """
        Search Library virtual filesystem text content.
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
        Search Library virtual filesystem text content.
        """
        # Optional Graphlit collection GUID or unique name filter. Repeatable.
        collection: Optional[list[str]] = None

        cursor: Optional[str] = None

        # Date field used by `in_last`. `added` filters by date added to the Library; `authored` filters by original/authored metadata date.
        date_mode: Optional[GetDate_modeQueryParameterType] = None

        ignore_case: Optional[bool] = None

        # Filter searched content to the last duration. Accepts ISO-8601-ish timespans such as `P30D` and `PT24H`, or compact forms such as `30d`, `1w`, and `24h`.
        in_last: Optional[str] = None

        # Optional public kind filter resolved as content type, file type, or exact file format/MIME alias. Repeatable. There is no separate `format` filter.
        kind: Optional[list[str]] = None

        # Optional Graphlit label GUID or unique name filter. Repeatable.
        label: Optional[list[str]] = None

        limit: Optional[int] = None

        # Optional mention filter in `<mention-kind>:<mention-ref>` form. Repeatable.
        mention: Optional[list[str]] = None

        # Derived read-only Library VFS search scope. `/library` and `/library/contents` search all content. `/library/sources` enumerates source folders only; source-scoped search requires `/library/sources/<source-ref>`. Label, collection, kind, and mention scopes are Graphlit-derived filters, not persisted Durable folders.
        path: Optional[str] = None

        pattern: Optional[str] = None

        # Search mode. `keyword` uses Graphlit keyword search for `durable fs grep`; `hybrid` uses Graphlit hybrid semantic search for `durable fs sgrep`; `vector` is accepted for direct API callers.
        search_type: Optional[GetSearch_typeQueryParameterType] = None

        # Optional data source GUID or unique source name filter. Repeatable.
        source: Optional[list[str]] = None

    
    @dataclass
    class SearchRequestBuilderGetRequestConfiguration(RequestConfiguration[SearchRequestBuilderGetQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

