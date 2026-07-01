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
    from ....models.persona import Persona
    from ....models.persona_create import PersonaCreate
    from ....models.persona_list import PersonaList
    from .item.with_persona_item_request_builder import WithPersonaItemRequestBuilder

class PersonasRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/durable/personas
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new PersonasRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/durable/personas{?cursor*,limit*,search*}", path_parameters)
    
    def by_persona(self,persona: str) -> WithPersonaItemRequestBuilder:
        """
        Gets an item from the durable_agents.generated.api.durable.personas.item collection
        param persona: Unique identifier of the item
        Returns: WithPersonaItemRequestBuilder
        """
        if persona is None:
            raise TypeError("persona cannot be null.")
        from .item.with_persona_item_request_builder import WithPersonaItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["persona"] = persona
        return WithPersonaItemRequestBuilder(self.request_adapter, url_tpl_params)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[PersonasRequestBuilderGetQueryParameters]] = None) -> Optional[PersonaList]:
        """
        List personas.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[PersonaList]
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
        from ....models.persona_list import PersonaList

        return await self.request_adapter.send_async(request_info, PersonaList, error_mapping)
    
    async def post(self,body: PersonaCreate, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[Persona]:
        """
        Create a persona.
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[Persona]
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
        from ....models.persona import Persona

        return await self.request_adapter.send_async(request_info, Persona, error_mapping)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[PersonasRequestBuilderGetQueryParameters]] = None) -> RequestInformation:
        """
        List personas.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def to_post_request_information(self,body: PersonaCreate, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        Create a persona.
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
    
    def with_url(self,raw_url: str) -> PersonasRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: PersonasRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return PersonasRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class PersonasRequestBuilderGetQueryParameters():
        """
        List personas.
        """
        cursor: Optional[str] = None

        limit: Optional[int] = None

        search: Optional[str] = None

    
    @dataclass
    class PersonasRequestBuilderGetRequestConfiguration(RequestConfiguration[PersonasRequestBuilderGetQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    
    @dataclass
    class PersonasRequestBuilderPostRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

