from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .phones.phones_request_builder import PhonesRequestBuilder
    from .status.status_request_builder import StatusRequestBuilder

class MessagingRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/durable/channels/messaging
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new MessagingRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/durable/channels/messaging", path_parameters)
    
    @property
    def phones(self) -> PhonesRequestBuilder:
        """
        The phones property
        """
        from .phones.phones_request_builder import PhonesRequestBuilder

        return PhonesRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def status(self) -> StatusRequestBuilder:
        """
        The status property
        """
        from .status.status_request_builder import StatusRequestBuilder

        return StatusRequestBuilder(self.request_adapter, self.path_parameters)
    

