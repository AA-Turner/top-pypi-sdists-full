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
    from ....models.content import Content
    from ....models.content_create import ContentCreate
    from ....models.content_list import ContentList
    from ....models.error_envelope import ErrorEnvelope
    from .get_date_mode_query_parameter_type import GetDate_modeQueryParameterType
    from .get_search_type_query_parameter_type import GetSearch_typeQueryParameterType
    from .item.with_content_item_request_builder import WithContentItemRequestBuilder

class ContentRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/durable/content
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new ContentRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/durable/content{?collection*,cursor*,date_mode*,in_last*,kind*,label*,limit*,mention*,relevance_threshold*,search*,search_type*,source*}", path_parameters)
    
    def by_content(self,content: str) -> WithContentItemRequestBuilder:
        """
        Gets an item from the durable_agents.generated.api.durable.content.item collection
        param content: Unique identifier of the item
        Returns: WithContentItemRequestBuilder
        """
        if content is None:
            raise TypeError("content cannot be null.")
        from .item.with_content_item_request_builder import WithContentItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["content"] = content
        return WithContentItemRequestBuilder(self.request_adapter, url_tpl_params)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[ContentRequestBuilderGetQueryParameters]] = None) -> Optional[ContentList]:
        """
        List library content.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ContentList]
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
        from ....models.content_list import ContentList

        return await self.request_adapter.send_async(request_info, ContentList, error_mapping)
    
    async def post(self,body: ContentCreate, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[Content]:
        """
        Add content to the library.
        param body: Create content from a URL or text body. Durable API validates the required fields for each ingest mode.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[Content]
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
        from ....models.content import Content

        return await self.request_adapter.send_async(request_info, Content, error_mapping)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[ContentRequestBuilderGetQueryParameters]] = None) -> RequestInformation:
        """
        List library content.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def to_post_request_information(self,body: ContentCreate, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        Add content to the library.
        param body: Create content from a URL or text body. Durable API validates the required fields for each ingest mode.
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
    
    def with_url(self,raw_url: str) -> ContentRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: ContentRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return ContentRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class ContentRequestBuilderGetQueryParameters():
        """
        List library content.
        """
        # Filter by Graphlit collection GUID or unique collection name. Repeatable.
        collection: Optional[list[str]] = None

        cursor: Optional[str] = None

        # Date field used by `in_last`. `added` filters by date added to the Library; `authored` filters by original/authored metadata date.
        date_mode: Optional[GetDate_modeQueryParameterType] = None

        # Filter to content in the last duration. Accepts ISO-8601-ish timespans such as `P30D` and `PT24H`, or compact forms such as `30d`, `1w`, and `24h`.
        in_last: Optional[str] = None

        # Repeatable public kind filter. Each value resolves internally as a Graphlit content type first, then a Graphlit file type, then an exact file format or MIME alias such as `pdf`, `csv`, `docx`, `markdown`, or `application/pdf`.
        kind: Optional[list[str]] = None

        # Filter by Graphlit label GUID or unique label name. Repeatable.
        label: Optional[list[str]] = None

        limit: Optional[int] = None

        # Repeatable Graphlit observation/observable filter in `<mention-kind>:<mention-ref>` form. Mention kinds come from `MentionKind`. Entity refs may be observable GUIDs or unique names within the mention kind; lookup refs currently support `email` and `phone`.
        mention: Optional[list[str]] = None

        # Minimum Graphlit relevance score from 0 to 1 for hybrid/vector search. Requires `search` and `search_type` of `hybrid` or `vector`.
        relevance_threshold: Optional[float] = None

        search: Optional[str] = None

        # Search mode for `search`. Defaults to `hybrid` when a search query is provided.
        search_type: Optional[GetSearch_typeQueryParameterType] = None

        # Filter by data source GUID or unique source name. Repeatable.
        source: Optional[list[str]] = None

    
    @dataclass
    class ContentRequestBuilderGetRequestConfiguration(RequestConfiguration[ContentRequestBuilderGetQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    
    @dataclass
    class ContentRequestBuilderPostRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

