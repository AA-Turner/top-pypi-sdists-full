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
    from .....models.agent import Agent
    from .....models.agent_patch import AgentPatch
    from .....models.deleted_response import DeletedResponse
    from .....models.error_envelope import ErrorEnvelope
    from .properties.properties_request_builder import PropertiesRequestBuilder
    from .runs.runs_request_builder import RunsRequestBuilder
    from .webhooks.webhooks_request_builder import WebhooksRequestBuilder

class WithAgentItemRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/durable/agents/{agent}
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new WithAgentItemRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/durable/agents/{agent}", path_parameters)
    
    async def delete(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[DeletedResponse]:
        """
        Delete or disable an agent.
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
    
    async def get(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[Agent]:
        """
        Get an agent.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[Agent]
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
        from .....models.agent import Agent

        return await self.request_adapter.send_async(request_info, Agent, error_mapping)
    
    async def patch(self,body: AgentPatch, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[Agent]:
        """
        Update agent fields only. Manage inboxes and channel bindings through the explicit channel endpoints and bindings APIs.
        param body: Agent fields only. Manage inboxes and channel bindings through the channel endpoints and bindings APIs.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[Agent]
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
        from .....models.agent import Agent

        return await self.request_adapter.send_async(request_info, Agent, error_mapping)
    
    def to_delete_request_information(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        Delete or disable an agent.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.DELETE, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        Get an agent.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def to_patch_request_information(self,body: AgentPatch, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        Update agent fields only. Manage inboxes and channel bindings through the explicit channel endpoints and bindings APIs.
        param body: Agent fields only. Manage inboxes and channel bindings through the channel endpoints and bindings APIs.
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
    
    def with_url(self,raw_url: str) -> WithAgentItemRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: WithAgentItemRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return WithAgentItemRequestBuilder(self.request_adapter, raw_url)
    
    @property
    def properties(self) -> PropertiesRequestBuilder:
        """
        The properties property
        """
        from .properties.properties_request_builder import PropertiesRequestBuilder

        return PropertiesRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def runs(self) -> RunsRequestBuilder:
        """
        The runs property
        """
        from .runs.runs_request_builder import RunsRequestBuilder

        return RunsRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def webhooks(self) -> WebhooksRequestBuilder:
        """
        The webhooks property
        """
        from .webhooks.webhooks_request_builder import WebhooksRequestBuilder

        return WebhooksRequestBuilder(self.request_adapter, self.path_parameters)
    
    @dataclass
    class WithAgentItemRequestBuilderDeleteRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    
    @dataclass
    class WithAgentItemRequestBuilderGetRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    
    @dataclass
    class WithAgentItemRequestBuilderPatchRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

