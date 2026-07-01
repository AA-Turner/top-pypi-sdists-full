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
    from .....models.vfs_entry_list import VfsEntryList
    from .get_date_mode_query_parameter_type import GetDate_modeQueryParameterType

class EntriesRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/durable/vfs/entries
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new EntriesRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/durable/vfs/entries{?collection*,cursor*,date_mode*,in_last*,kind*,label*,limit*,mention*,name*,path*,recursive*,source*}", path_parameters)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[EntriesRequestBuilderGetQueryParameters]] = None) -> Optional[VfsEntryList]:
        """
        List Library virtual filesystem entries.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[VfsEntryList]
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
        from .....models.vfs_entry_list import VfsEntryList

        return await self.request_adapter.send_async(request_info, VfsEntryList, error_mapping)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[EntriesRequestBuilderGetQueryParameters]] = None) -> RequestInformation:
        """
        List Library virtual filesystem entries.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> EntriesRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: EntriesRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return EntriesRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class EntriesRequestBuilderGetQueryParameters():
        """
        List Library virtual filesystem entries.
        """
        # Optional Graphlit collection GUID or unique name filter. Repeatable.
        collection: Optional[list[str]] = None

        cursor: Optional[str] = None

        # Date field used by `in_last`. `added` filters by date added to the Library; `authored` filters by original/authored metadata date.
        date_mode: Optional[GetDate_modeQueryParameterType] = None

        # Filter content entries to the last duration. Accepts ISO-8601-ish timespans such as `P30D` and `PT24H`, or compact forms such as `30d`, `1w`, and `24h`.
        in_last: Optional[str] = None

        # Optional public kind filter. Repeatable. Public kinds resolve as Graphlit content type, Graphlit file type, or exact file format/MIME aliases such as `pdf`.
        kind: Optional[list[str]] = None

        # Optional Graphlit label GUID or unique name filter. Repeatable.
        label: Optional[list[str]] = None

        limit: Optional[int] = None

        # Optional mention filter in `<mention-kind>:<mention-ref>` form. Repeatable.
        mention: Optional[list[str]] = None

        name: Optional[str] = None

        # Derived read-only Library VFS path. `/library` is the navigation root, `/library/contents` enumerates all content, `/library/<content-id>` is the canonical item path, and `/library/contents/<content-id>` also resolves item paths under the flat content view. Supported facet roots are `/library/labels`, `/library/labels/<label-ref>`, `/library/collections`, `/library/collections/<collection-ref>`, `/library/kind`, `/library/kind/<kind>`, `/library/mentions`, `/library/mentions/<entity-mention-kind>`, `/library/mentions/<mention-kind>/<mention-ref>`, `/library/sources`, and `/library/sources/<source-ref>`. Entity mention kind folders are browsable; lookup mention kinds such as `email` and `phone` require a reference path like `/library/mentions/email/<encoded-email>` and are invalid as parent directories. Mention kinds come from `MentionKind`. Facet folders enumerate canonical content entries at `/library/<content-id>`.
        path: Optional[str] = None

        recursive: Optional[bool] = None

        # Optional data source GUID or unique source name filter. Repeatable.
        source: Optional[list[str]] = None

    
    @dataclass
    class EntriesRequestBuilderGetRequestConfiguration(RequestConfiguration[EntriesRequestBuilderGetQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

