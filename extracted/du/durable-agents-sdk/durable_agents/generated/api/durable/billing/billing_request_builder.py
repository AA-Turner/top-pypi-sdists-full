from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .funding_requests.funding_requests_request_builder import FundingRequestsRequestBuilder
    from .usage.usage_request_builder import UsageRequestBuilder

class BillingRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/durable/billing
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new BillingRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/durable/billing", path_parameters)
    
    @property
    def funding_requests(self) -> FundingRequestsRequestBuilder:
        """
        The fundingRequests property
        """
        from .funding_requests.funding_requests_request_builder import FundingRequestsRequestBuilder

        return FundingRequestsRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def usage(self) -> UsageRequestBuilder:
        """
        The usage property
        """
        from .usage.usage_request_builder import UsageRequestBuilder

        return UsageRequestBuilder(self.request_adapter, self.path_parameters)
    

