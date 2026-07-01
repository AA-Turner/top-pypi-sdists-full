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
    from .....models.data_source import DataSource
    from .....models.data_source_update import DataSourceUpdate
    from .....models.deleted_response import DeletedResponse
    from .....models.error_envelope import ErrorEnvelope
    from .pause.pause_request_builder import PauseRequestBuilder
    from .resume.resume_request_builder import ResumeRequestBuilder
    from .sync.sync_request_builder import SyncRequestBuilder

class WithSourceItemRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/durable/data-sources/{source}
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new WithSourceItemRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/durable/data-sources/{source}", path_parameters)
    
    async def delete(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[DeletedResponse]:
        """
        Delete a Durable data source.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[DeletedResponse]
        """
        request_info = self.to_delete_request_information(
            request_configuration
        )
        from .....models.error_envelope import ErrorEnvelope

        error_mapping: dict[str, type[ParsableFactory]] = {
            "XXX": ErrorEnvelope,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .....models.deleted_response import DeletedResponse

        return await self.request_adapter.send_async(request_info, DeletedResponse, error_mapping)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[DataSource]:
        """
        Get a Durable data source.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[DataSource]
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
        from .....models.data_source import DataSource

        return await self.request_adapter.send_async(request_info, DataSource, error_mapping)
    
    async def patch(self,body: DataSourceUpdate, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[DataSource]:
        """
        Update safe mutable fields on a Durable data source.
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[DataSource]
        """
        if body is None:
            raise TypeError("body cannot be null.")
        request_info = self.to_patch_request_information(
            body, request_configuration
        )
        from .....models.error_envelope import ErrorEnvelope

        error_mapping: dict[str, type[ParsableFactory]] = {
            "XXX": ErrorEnvelope,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .....models.data_source import DataSource

        return await self.request_adapter.send_async(request_info, DataSource, error_mapping)
    
    def to_delete_request_information(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        Delete a Durable data source.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.DELETE, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        Get a Durable data source.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def to_patch_request_information(self,body: DataSourceUpdate, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        Update safe mutable fields on a Durable data source.
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        if body is None:
            raise TypeError("body cannot be null.")
        request_info = RequestInformation(Method.PATCH, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        request_info.set_content_from_parsable(self.request_adapter, "application/json", body)
        return request_info
    
    def with_url(self,raw_url: str) -> WithSourceItemRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: WithSourceItemRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return WithSourceItemRequestBuilder(self.request_adapter, raw_url)
    
    @property
    def pause(self) -> PauseRequestBuilder:
        """
        The pause property
        """
        from .pause.pause_request_builder import PauseRequestBuilder

        return PauseRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def resume(self) -> ResumeRequestBuilder:
        """
        The resume property
        """
        from .resume.resume_request_builder import ResumeRequestBuilder

        return ResumeRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def sync(self) -> SyncRequestBuilder:
        """
        The sync property
        """
        from .sync.sync_request_builder import SyncRequestBuilder

        return SyncRequestBuilder(self.request_adapter, self.path_parameters)
    
    @dataclass
    class WithSourceItemRequestBuilderDeleteRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    
    @dataclass
    class WithSourceItemRequestBuilderGetRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    
    @dataclass
    class WithSourceItemRequestBuilderPatchRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

