from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .entries.entries_request_builder import EntriesRequestBuilder
    from .item_escaped.item_escaped_request_builder import Item_EscapedRequestBuilder
    from .search.search_request_builder import SearchRequestBuilder

class VfsRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/durable/vfs
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new VfsRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/durable/vfs", path_parameters)
    
    @property
    def entries(self) -> EntriesRequestBuilder:
        """
        The entries property
        """
        from .entries.entries_request_builder import EntriesRequestBuilder

        return EntriesRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def item(self) -> Item_EscapedRequestBuilder:
        """
        The item property
        """
        from .item_escaped.item_escaped_request_builder import Item_EscapedRequestBuilder

        return Item_EscapedRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def search(self) -> SearchRequestBuilder:
        """
        The search property
        """
        from .search.search_request_builder import SearchRequestBuilder

        return SearchRequestBuilder(self.request_adapter, self.path_parameters)
    

