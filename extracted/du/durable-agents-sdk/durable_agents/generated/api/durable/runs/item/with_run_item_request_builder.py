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
    from .....models.run import Run
    from .cancel.cancel_request_builder import CancelRequestBuilder
    from .events.events_request_builder import EventsRequestBuilder
    from .pause.pause_request_builder import PauseRequestBuilder
    from .prompt.prompt_request_builder import PromptRequestBuilder
    from .replay.replay_request_builder import ReplayRequestBuilder
    from .resume.resume_request_builder import ResumeRequestBuilder

class WithRunItemRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/durable/runs/{run}
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new WithRunItemRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/durable/runs/{run}", path_parameters)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[Run]:
        """
        Get run state.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[Run]
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
        from .....models.run import Run

        return await self.request_adapter.send_async(request_info, Run, error_mapping)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        Get run state.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> WithRunItemRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: WithRunItemRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return WithRunItemRequestBuilder(self.request_adapter, raw_url)
    
    @property
    def cancel(self) -> CancelRequestBuilder:
        """
        The cancel property
        """
        from .cancel.cancel_request_builder import CancelRequestBuilder

        return CancelRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def events(self) -> EventsRequestBuilder:
        """
        The events property
        """
        from .events.events_request_builder import EventsRequestBuilder

        return EventsRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def pause(self) -> PauseRequestBuilder:
        """
        The pause property
        """
        from .pause.pause_request_builder import PauseRequestBuilder

        return PauseRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def prompt(self) -> PromptRequestBuilder:
        """
        The prompt property
        """
        from .prompt.prompt_request_builder import PromptRequestBuilder

        return PromptRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def replay(self) -> ReplayRequestBuilder:
        """
        The replay property
        """
        from .replay.replay_request_builder import ReplayRequestBuilder

        return ReplayRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def resume(self) -> ResumeRequestBuilder:
        """
        The resume property
        """
        from .resume.resume_request_builder import ResumeRequestBuilder

        return ResumeRequestBuilder(self.request_adapter, self.path_parameters)
    
    @dataclass
    class WithRunItemRequestBuilderGetRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

